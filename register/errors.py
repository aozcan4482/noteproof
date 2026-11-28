# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    -
# contract: 02#7 hata biçimi
# depends:  -
# status:   wip
"""API'nin ortak hata biçimi: {"error": {"code", "message", "violations"}}.

Her uç nokta hatayı aynı biçimde döndürür; arayüz (web/js/api.js, Erdener) kullanıcıya message'ı değil,
code değerine göre kendi Türkçe metnini gösterir (02 bölüm 7). Bu yüzden code değerleri sözleşmedir;
message yalnızca geliştirici ve günlük içindir ama yine de Türkçe yazılır (03 bölüm 1).

Uç noktalar hata vermek için ApiError fırlatır; app.py'deki işleyiciler onu JSON'a çevirir.
"""

from __future__ import annotations

from typing import Any

# NP-CONTRACT(02#7): hata kodları ve HTTP durumları sabit.
UNSUPPORTED_TYPE = "unsupported_type"      # 400
TOO_LARGE = "too_large"                    # 400
NOT_CONFIRMED = "not_confirmed"            # 400
UNAUTHORIZED = "unauthorized"              # 401
NOT_FOUND = "not_found"                    # 404
PROOF_PENDING = "proof_pending"            # 404
PREVIEW_EXPIRED = "preview_expired"        # 410
SHAPE_VIOLATION = "shape_violation"        # 422

# Sözleşme tablosunda olmayan, FastAPI'nin kendiliğinden ürettiği durumlar. Arda'nın (mimar) kararıyla
# eklendi; 02 bölüm 9 prosedürü sürüyor.
# NP-TODO(erdener): 02 bölüm 7 tablosuna method_not_allowed (405), invalid_request (422), internal_error (500).
METHOD_NOT_ALLOWED = "method_not_allowed"  # 405
INVALID_REQUEST = "invalid_request"        # 422, gövde ya da parametre biçimi bozuk (SHACL'a gelinmedi)
INTERNAL_ERROR = "internal_error"          # 500
# NP-TODO(erdener): 02 bölüm 7 tablosuna 409 pseudonym_taken (POST /api/accounts, takma ad alınmış; ARD-2).
PSEUDONYM_TAKEN = "pseudonym_taken"        # 409
# NP-TODO(erdener): 02 bölüm 7 tablosuna 409 already_registered (POST /api/notes, hash zaten kayıtlı; ARD-4).
ALREADY_REGISTERED = "already_registered"  # 409


class ApiError(Exception):
    """Uç noktalardan fırlatılan, ortak biçime çevrilecek hata.

    violations yalnızca shape_violation için doludur; her öğe {"shape", "path", "message"} (02 bölüm 7).
    """

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        violations: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.violations = violations or []


def error_body(code: str, message: str, violations: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """Ortak hata gövdesi. violations boşsa alan hiç yazılmaz (web/mock/error-*.json ile aynı biçim)."""
    error: dict[str, Any] = {"code": code, "message": message}
    if violations:
        error["violations"] = violations
    return {"error": error}
