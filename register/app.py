# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1
# contract: 02#7 GET /api/health, POST /api/accounts, X-NoteProof-Token, hata biçimi
# depends:  core.graph.open_store
# status:   wip
"""Kayıt servisinin FastAPI uygulaması: /api uç noktaları ve web/ sayfalarının sunumu.

Çalıştırma (repo kökünden): python -m uvicorn register.app:app --reload
Sonra tarayıcıda http://127.0.0.1:8000/ arama sayfası, http://127.0.0.1:8000/api/health sağlık kontrolü.

Sıra önemlidir: önce /api uç noktaları, sonra /api altındaki bilinmeyen yollar için yakalayıcı, en son
web/ klasörünün statik sunumu. Statik sunum "/" köküne bağlandığı için kendinden önce eklenmeyen her
yolu yutar.
"""

from __future__ import annotations

import logging
import pathlib
from typing import Annotated, Any

from fastapi import Depends, FastAPI, File, Header, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from copywarn import CopyChecker
from ontology.vocab import Vocabulary

from . import preview, registration, state
from .accounts import AccountStore, InvalidPseudonym, PseudonymTaken, pseudonym_of
from .errors import (
    ALREADY_REGISTERED,
    INTERNAL_ERROR,
    INVALID_REQUEST,
    METHOD_NOT_ALLOWED,
    NOT_CONFIRMED,
    NOT_FOUND,
    PREVIEW_EXPIRED,
    PSEUDONYM_TAKEN,
    SHAPE_VIOLATION,
    TOO_LARGE,
    UNAUTHORIZED,
    UNSUPPORTED_TYPE,
    ApiError,
    error_body,
)
from .lookup import find_registered

log = logging.getLogger(__name__)

# Erdener'in statik sayfaları (02 bölüm 2). Sayfalar /api'yi aynı sunucuda bekler (web/js/config.js).
WEB_DIR = pathlib.Path(__file__).resolve().parent.parent / "web"

app = FastAPI(title="NoteProof", docs_url="/api/docs", openapi_url="/api/openapi.json", redoc_url=None)


# --- Hata işleyiciler: her hata 02 bölüm 7'deki ortak biçimde döner -----------------------------------

@app.exception_handler(ApiError)
async def _api_error(_: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(error_body(exc.code, exc.message, exc.violations), status_code=exc.status)


# FastAPI ve Starlette'in kendi ürettiği HTTP hataları (bilinmeyen dosya, yanlış metot).
_HTTP_CODES = {
    401: (UNAUTHORIZED, "Kimlik doğrulanamadı."),
    404: (NOT_FOUND, "İstenen adres bulunamadı."),
    405: (METHOD_NOT_ALLOWED, "Bu adres bu HTTP metodunu desteklemiyor."),
}


@app.exception_handler(StarletteHTTPException)
async def _http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    code, message = _HTTP_CODES.get(exc.status_code, (INTERNAL_ERROR, "Beklenmeyen bir hata oluştu."))
    return JSONResponse(error_body(code, message), status_code=exc.status_code, headers=exc.headers)


@app.exception_handler(RequestValidationError)
async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    # Gövde ya da parametre biçimi bozuk. Bu shape_violation değildir: SHACL doğrulamasına hiç gelinmedi.
    return JSONResponse(error_body(INVALID_REQUEST, "İstek biçimi geçersiz."), status_code=422)


@app.exception_handler(Exception)
async def _unexpected_error(_: Request, exc: Exception) -> JSONResponse:
    # Ayrıntı yanıta yazılmaz (iç yol, not içeriği sızabilir); yalnızca sunucu günlüğüne gider.
    log.exception("Beklenmeyen hata: %s", type(exc).__name__)
    return JSONResponse(error_body(INTERNAL_ERROR, "Beklenmeyen bir hata oluştu."), status_code=500)


# --- /api uç noktaları --------------------------------------------------------------------------------

# NP-CONTRACT(02#7): GET /api/health → 200 {"status": "ok"}
@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# --- Hesaplar ve kimlik (K-007) -----------------------------------------------------------------------

class AccountRequest(BaseModel):
    # Yalnızca takma ad alınır. Gövdede başka alan (isim, numara, e-posta) gelirse yok sayılır, saklanmaz.
    pseudonym: str


# NP-CONTRACT(02#7): POST /api/accounts {"pseudonym"} → 201 {"account", "token"}; token yalnızca bir kez gösterilir.
@app.post("/api/accounts", status_code=201)
def create_account(
    body: AccountRequest,
    accounts: Annotated[AccountStore, Depends(state.account_store)],
    graph: Annotated[object, Depends(state.graph_store)],
) -> dict[str, str]:
    try:
        iri, token = accounts.create(body.pseudonym, graph)
    except InvalidPseudonym as exc:
        raise ApiError(422, INVALID_REQUEST, str(exc)) from exc
    except PseudonymTaken as exc:
        raise ApiError(409, PSEUDONYM_TAKEN, "Bu takma ad alınmış; başka bir takma ad seçin.") from exc
    return {"account": iri, "token": token}


# NP-CONTRACT(02#7): kimlik X-NoteProof-Token başlığıyla; yoksa ya da geçersizse 401 unauthorized.
# Yazma uç noktaları (ARD-3, ARD-4) bunu Depends(require_account) ile kullanır; okuma ve proof kimlik istemez.
def require_account(
    accounts: Annotated[AccountStore, Depends(state.account_store)],
    token: Annotated[str | None, Header(alias="X-NoteProof-Token")] = None,
) -> str:
    """Geçerli token'ın hesap IRI'sini döndürür."""
    account = accounts.account_for_token(token)
    if account is None:
        raise ApiError(401, UNAUTHORIZED, "Token yok ya da geçersiz.")
    return account


# --- Önizleme (aktivite adımları 2–5) -----------------------------------------------------------------

# NP-CONTRACT(02#7): POST /api/notes/preview, multipart alan adı "file" → 200 önizleme. Hiçbir şey kaydedilmez.
@app.post("/api/notes/preview")
def preview_note(
    file: Annotated[UploadFile, File()],
    account: Annotated[str, Depends(require_account)],
    graph: Annotated[object, Depends(state.graph_store)],
    vocabulary: Annotated[Vocabulary, Depends(state.vocabulary)],
    llm: Annotated[object, Depends(state.llm_client)],
    checker: Annotated[CopyChecker, Depends(state.copy_checker)],
    previews: Annotated[preview.PreviewCache, Depends(state.preview_cache)],
) -> dict:
    # Sınırın bir byte fazlası okunur: dosyanın tamamını belleğe almadan "10 MB'tan büyük" denebilsin.
    data = file.file.read(preview.MAX_BYTES + 1)
    try:
        entry = preview.build_preview(
            data=data,
            content_type=file.content_type,
            filename=file.filename,
            account=account,
            author=pseudonym_of(account),
            vocabulary=vocabulary,
            llm=llm,
            checker=checker,
            find_registered=lambda note_hash: find_registered(graph, note_hash),
        )
    except preview.TooLarge as exc:
        raise ApiError(400, TOO_LARGE, str(exc)) from exc
    except preview.UnsupportedType as exc:
        raise ApiError(400, UNSUPPORTED_TYPE, str(exc)) from exc
    except preview.EmptyFile as exc:
        raise ApiError(422, INVALID_REQUEST, str(exc)) from exc
    previews.put(entry)
    return preview.preview_response(entry)


# --- Kayıt (aktivite adımları 6–9) --------------------------------------------------------------------

class ConfirmRequest(BaseModel):
    previewToken: str
    title: str
    course: str
    topics: list[str]
    summary: str = ""
    # Dönüştürülmeden alınır: Pydantic "true" metnini ve 1'i de True yapardı. Yalnızca JSON true onaydır (G4).
    confirmed: Any = None


# NP-CONTRACT(02#7): POST /api/notes onay gövdesi → 201 {"noteHash", "registeredAt", "status", "proofStatus"}.
@app.post("/api/notes", status_code=201)
def register_note(
    body: ConfirmRequest,
    account: Annotated[str, Depends(require_account)],
    graph: Annotated[object, Depends(state.graph_store)],
    open_queue: Annotated[object, Depends(state.anchor_queue)],
    checker: Annotated[CopyChecker, Depends(state.copy_checker)],
    previews: Annotated[preview.PreviewCache, Depends(state.preview_cache)],
) -> dict:
    # G4: yazar onaylamadan hiçbir etiket ya da özet kaydedilmez; onay denetimi her şeyden önce gelir.
    if body.confirmed is not True:
        raise ApiError(400, NOT_CONFIRMED, "Ders ve konular onaylanmadan not kaydedilmez.")
    entry = previews.get(body.previewToken, account)
    if entry is None:
        raise ApiError(410, PREVIEW_EXPIRED, "Önizlemenin süresi doldu; dosyayı yeniden yükleyin.")
    title = body.title.strip()
    if not title:
        raise ApiError(422, INVALID_REQUEST, "Notun bir başlığı olmalı.")
    if entry.already_registered is not None or find_registered(graph, entry.note_hash) is not None:
        # Aynı dosya iki kez kaydedilmez (adım 3); önceki kayıt önizlemede gösterilmişti.
        raise ApiError(409, ALREADY_REGISTERED, "Bu dosya zaten kayıtlı.")

    confirmation = registration.Confirmation(
        title=title,
        course=body.course.strip(),
        topics=list(dict.fromkeys(t.strip() for t in body.topics)),  # sırayı koruyarak tekrarı at
        summary=body.summary.strip(),
    )
    try:
        done = registration.register_note(
            entry=entry, confirmation=confirmation, author=pseudonym_of(account),
            graph=graph, open_queue=open_queue, checker=checker,
        )
    except registration.ShapeViolation as exc:
        # Önizleme silinmez: yazar etiketleri düzeltip aynı previewToken ile yeniden onaylayabilir (adım 7 → 6).
        violations = [{"shape": v.shape, "path": v.path, "message": v.message} for v in exc.violations]
        raise ApiError(422, SHAPE_VIOLATION, "Not shape'lere uymuyor.", violations) from exc
    previews.discard(body.previewToken)
    return {
        "noteHash": done.note_hash,
        "registeredAt": done.registered_at,
        "status": registration.STATUS_REGISTERED,
        "proofStatus": "pending",
    }


# Arama servisinin router'ı (Erdener, 02 bölüm 5.6): GET /api/search.
# NP-TODO(erdener): search/ main'e girince aşağıdaki iki satırı aç (yakalayıcıdan önce kalmalı).
# from search.router import router as search_router
# app.include_router(search_router)


# --- /api altındaki bilinmeyen yollar -----------------------------------------------------------------

def _methods_for(path: str) -> set[str]:
    """Bu yolu karşılayan /api uç noktalarının metotları; yakalayıcının kendisi hariç."""
    methods: set[str] = set()
    for route in app.router.routes:
        if isinstance(route, APIRoute) and route.endpoint is not _unknown_api_path and route.path_regex.match(path):
            methods |= route.methods
    return methods


@app.api_route("/api/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
               include_in_schema=False)
def _unknown_api_path(request: Request, rest: str) -> None:
    # Bu yakalayıcı olmasa /api/... istekleri statik sunuma düşer ve POST bilinmeyen yola 404 yerine 405 alır.
    # Starlette, yolu tutan ama metodu tutmayan bir uç nokta varken de buraya gelir; o durumda 405 döneriz.
    allowed = _methods_for(request.url.path)
    if allowed:
        raise StarletteHTTPException(405, headers={"Allow": ", ".join(sorted(allowed))})
    raise StarletteHTTPException(404)


# --- web/ sayfaları (en sonda) ------------------------------------------------------------------------

# html=True: "/" isteğine index.html döner. Bilinmeyen dosya 404 not_found olarak ortak biçimde döner.
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
