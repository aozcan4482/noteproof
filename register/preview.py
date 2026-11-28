# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1, S3, S6
# contract: 02#7 POST /api/notes/preview; K-006
# depends:  tagger.extract.extract_text, tagger.suggest.suggest, copywarn.CopyChecker.check
# status:   wip
"""Önizleme: dosyayı denetler, hash'ler, etiket önerisi ve kopya uyarısı üretir; HİÇBİR ŞEY KAYDETMEZ.

Proposal aktivite adımları 2–5. Yazar önizlemeyi görür, sonra onaylar (ARD-4) ya da vazgeçer. Vazgeçerse
hiçbir iz kalmamalıdır (G4, "author cancels → nothing is saved"). Bu yüzden dosya, metin ve öneriler
yalnızca bellekte, previewToken ile kısa bir süre tutulur; grafiğe ve data/ altına hiçbir şey yazılmaz.
Günlüklere not içeriği yazılmaz, yalnızca hash (03 bölüm 9).
"""

from __future__ import annotations

import logging
import secrets
import threading
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable

from copywarn import CopyChecker, CopyWarning
from core.hashing import sha256_hex
from ontology.vocab import Vocabulary
from tagger.extract import extract_text
from tagger.llm import LLMClient
from tagger.suggest import TagSuggestion, suggest

from .lookup import RegisteredNoteInfo, proof_url

log = logging.getLogger(__name__)

# NP-DECISION(K-006): en büyük dosya 10 MB; kabul edilen türler PDF, JPEG, PNG, düz metin, Markdown.
MAX_BYTES = 10 * 1024 * 1024
SUPPORTED_TYPES = ("application/pdf", "image/jpeg", "image/png", "text/plain", "text/markdown")

# Tarayıcı türü boş ya da "application/octet-stream" gönderirse (ör. Windows'ta .md) uzantıdan bulunur.
_BY_EXTENSION = {
    ".pdf": "application/pdf", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".txt": "text/plain", ".md": "text/markdown", ".markdown": "text/markdown",
}

# İkili türlerde ilk byte'lar türü doğrular: ".pdf" adı verilmiş bir program dosyası kabul edilmez.
_MAGIC = {
    "application/pdf": (b"%PDF-",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
    "image/jpeg": (b"\xff\xd8\xff",),
}

# Önizleme bellekte 15 dakika durur (arda.md tasarım notu). En çok 100 önizleme: 10 MB'lık dosyalarla
# bellek ~1 GB'ı aşmasın diye; dolarsa en eski önizleme düşer ve yazar yeniden yükler (410 preview_expired).
PREVIEW_TTL_SECONDS = 15 * 60
MAX_PREVIEWS = 100

EMPTY_SUGGESTION = TagSuggestion(course=None, topics=[], summary="")


class UnsupportedType(ValueError):
    """Dosya türü kabul edilmiyor ya da içerik türüyle uyuşmuyor (400 unsupported_type)."""


class TooLarge(ValueError):
    """Dosya 10 MB'tan büyük (400 too_large)."""


class EmptyFile(ValueError):
    """Dosya boş (422 invalid_request)."""


def detect_media_type(content_type: str | None, filename: str | None, data: bytes) -> str:
    """Dosyanın türünü belirler ve denetler (aktivite adımı 2); uygun değilse nedenini söyleyerek reddeder."""
    kind = (content_type or "").split(";", 1)[0].strip().lower()
    if kind in ("", "application/octet-stream"):
        name = (filename or "").lower()
        kind = next((t for ext, t in _BY_EXTENSION.items() if name.endswith(ext)), kind)
    if kind not in SUPPORTED_TYPES:
        raise UnsupportedType("Bu dosya türü kabul edilmiyor. Kabul edilenler: PDF, JPEG, PNG, düz metin, Markdown.")
    magic = _MAGIC.get(kind)
    if magic and not data.startswith(magic):
        raise UnsupportedType("Dosyanın içeriği türüyle uyuşmuyor; dosya bozuk ya da uzantısı yanlış olabilir.")
    return kind


def check_size(data: bytes) -> None:
    if len(data) > MAX_BYTES:
        raise TooLarge("Dosya 10 MB'tan büyük.")
    if not data:
        raise EmptyFile("Dosya boş.")


@dataclass(frozen=True)
class PreviewEntry:
    """Onaya kadar bellekte duran önizleme. ARD-4 bunu previewToken ile alır ve ancak o zaman kaydeder."""

    token: str
    account: str                      # önizlemeyi isteyen hesabın IRI'si; onay da aynı hesaptan gelmeli
    note_hash: str
    data: bytes
    media_type: str
    filename: str
    text: str
    suggestion: TagSuggestion | None  # None: hash zaten kayıtlı
    copy_warnings: list[CopyWarning]
    already_registered: RegisteredNoteInfo | None


class PreviewCache:
    """previewToken → PreviewEntry; süresi dolan ve fazla olan önizlemeler düşer. Diske hiçbir şey yazmaz."""

    def __init__(self, ttl: float = PREVIEW_TTL_SECONDS, max_entries: int = MAX_PREVIEWS,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.ttl = ttl
        self.max_entries = max_entries
        self._clock = clock
        self._entries: OrderedDict[str, tuple[float, PreviewEntry]] = OrderedDict()
        self._lock = threading.Lock()

    def put(self, entry: PreviewEntry) -> None:
        with self._lock:
            self._expire()
            self._entries[entry.token] = (self._clock(), entry)
            while len(self._entries) > self.max_entries:
                self._entries.popitem(last=False)

    def get(self, token: str, account: str) -> PreviewEntry | None:
        """Token geçerli, süresi dolmamış ve aynı hesaba aitse önizlemeyi döndürür; değilse None (410)."""
        with self._lock:
            self._expire()
            item = self._entries.get(token)
            if item is None or item[1].account != account:
                return None
            return item[1]

    def discard(self, token: str) -> None:
        with self._lock:
            self._entries.pop(token, None)

    def __len__(self) -> int:
        with self._lock:
            self._expire()
            return len(self._entries)

    def _expire(self) -> None:
        limit = self._clock() - self.ttl
        while self._entries:
            token, (stamp, _) = next(iter(self._entries.items()))
            if stamp > limit:
                break
            del self._entries[token]


def _suggest_or_empty(text: str, vocabulary: Vocabulary, llm: LLMClient | None, note_hash: str) -> TagSuggestion:
    """Etiket önerisi (adım 4a). Öneri yoksa yazar dersi ve konuyu elle seçer; önizleme yine de çalışır."""
    if not text.strip():
        # tagger.suggest boş metinde ValueError verir (Aleyna'nın NP-TODO'su): metni çıkmayan dosya (ör. boş
        # taranmış PDF) için öneri boş döner, yazar elle seçer.
        log.info("Önizleme %s: metin çıkmadı, öneri yok", note_hash)
        return EMPTY_SUGGESTION
    if llm is None:
        log.warning("Önizleme %s: dil modeli yapılandırılmamış (NOTEPROOF_LLM_*), öneri yok", note_hash)
        return EMPTY_SUGGESTION
    try:
        return suggest(text, vocabulary, llm)
    except Exception:  # ağ hatası, kota vb.: önizlemeyi düşürmez, yazar elle seçer
        log.exception("Önizleme %s: dil modeli önerisi alınamadı", note_hash)
        return EMPTY_SUGGESTION


def _extract_or_empty(data: bytes, media_type: str, note_hash: str) -> str:
    try:
        return extract_text(data, media_type)
    except RuntimeError:
        # Sunucuda Tesseract kurulu değil: fotoğraftan metin çıkmaz ama yazar yine de etiketleri elle seçebilir.
        log.error("Önizleme %s: metin çıkarılamadı (OCR kurulu değil)", note_hash)
        return ""


def build_preview(
    *,
    data: bytes,
    content_type: str | None,
    filename: str | None,
    account: str,
    author: str,
    vocabulary: Vocabulary,
    llm: LLMClient | None,
    checker: CopyChecker,
    find_registered: Callable[[str], RegisteredNoteInfo | None],
) -> PreviewEntry:
    """Aktivite adımları 2–4: tür ve boyut, hash, mükerrer kontrolü, metin, öneri ve kopya denetimi (paralel)."""
    check_size(data)
    media_type = detect_media_type(content_type, filename, data)
    note_hash = sha256_hex(data)
    token = secrets.token_urlsafe(24)

    earlier = find_registered(note_hash)
    if earlier is not None:
        # Adım 3: hash zaten kayıtlı → önceki kayıt ve proof'u gösterilir; öneri ve kopya denetimi yapılmaz.
        return PreviewEntry(token, account, note_hash, data, media_type, filename or "", "", None, [], earlier)

    try:
        text = _extract_or_empty(data, media_type, note_hash)
    except ValueError as exc:  # bozuk PDF, okunamayan resim, UTF-8 olmayan metin
        raise UnsupportedType(str(exc)) from exc

    # Adım 4a ve 4b paraleldir: dil modeli çağrısı saniyeler sürebilir, kopya denetimi onu beklemez.
    with ThreadPoolExecutor(max_workers=2) as pool:
        suggestion_f = pool.submit(_suggest_or_empty, text, vocabulary, llm, note_hash)
        # Aynı hesabın notları kopya sayılmaz (02#5.4): author takma addır.
        warnings_f = pool.submit(checker.check, text, author) if text.strip() else None
        suggestion = suggestion_f.result()
        warnings = warnings_f.result() if warnings_f is not None else []

    return PreviewEntry(token, account, note_hash, data, media_type, filename or "", text, suggestion, warnings, None)


def preview_response(entry: PreviewEntry) -> dict:
    """02 bölüm 7'deki önizleme yanıtı."""
    earlier = entry.already_registered
    return {
        "previewToken": entry.token,
        "noteHash": entry.note_hash,
        "alreadyRegistered": None if earlier is None else {
            "registeredAt": earlier.registered_at,
            "author": earlier.author,
            "proofUrl": proof_url(earlier.note_hash),
        },
        "suggestion": None if entry.suggestion is None else {
            "course": entry.suggestion.course,
            "topics": list(entry.suggestion.topics),
            "summary": entry.suggestion.summary,
        },
        "copyWarnings": [
            {
                "earlierNoteHash": w.earlier_note_id,
                "earlierAuthor": w.earlier_author,
                "earlierRegisteredAt": w.earlier_registered_at,
                "earlierProofUrl": w.earlier_proof or proof_url(w.earlier_note_id),
                "score": round(w.score, 4),
                "method": w.method,
            }
            for w in entry.copy_warnings
        ],
    }
