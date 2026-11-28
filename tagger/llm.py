# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3, 02#8
# depends:  -
# status:   stable
"""Dil modeli istemcisi: sağlayıcıdan bağımsız LLMClient arayüzü, Groq istemcisi ve ortam değişkenlerinden kurulum.

Sağlayıcıya özel her şey bu dosyada kalır; tagger/suggest.py yalnızca LLMClient.complete çağırır.
Böylece sağlayıcı değişirse (K-005) yalnızca bu dosya ve .env değişir.

Testler gerçek istemciyi ağa çıkarmadan dener: GroqClient'a sahte bir urlopen verilir. Etiket önerisi
testleri ise tests/tagger/fake_llm.py içindeki FakeLLM ile çalışır (03 bölüm 8).

Arama yanıtları (Erdener, ERD-8) da modele client_from_env üzerinden ulaşır.
"""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Protocol, runtime_checkable

# 02#8: dil modeli bağlantısının ortam değişkenleri. Değerler yerelde .env dosyasında durur, repoya girmez.
ENV_PROVIDER = "NOTEPROOF_LLM_PROVIDER"
ENV_MODEL = "NOTEPROOF_LLM_MODEL"
ENV_API_KEY = "NOTEPROOF_LLM_API_KEY"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Ücretsiz planda kısa sürede ~20 çağrıdan sonra HTTP 429 geliyor (ALY-R2, docs/analysis/aleyna-prompt-v0.md).
# 429 ve geçici sunucu hatalarında bekleyip yeniden denenir.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


# NP-CONTRACT(02#5.3): imza ve dönüş türü sabit; sağlayıcı istemcileri bu arayüze uyar.
@runtime_checkable
class LLMClient(Protocol):
    def complete(self, prompt: str, *, system: str | None = None) -> str:
        """İstemi modele gönderir, modelin düz metin yanıtını döndürür."""
        ...


class GroqClient:
    """Groq'un OpenAI uyumlu sohbet ucuna istek atan LLMClient (K-005: Groq, openai/gpt-oss-20b).

    Yalnızca standart kütüphaneyi kullanır; ek bağımlılık gerekmez. Not metni ve API anahtarı hiçbir
    hata mesajına ya da günlüğe yazılmaz.
    """

    def __init__(
        self,
        model: str,
        api_key: str,
        *,
        url: str = GROQ_URL,
        timeout: float = 60.0,
        max_retries: int = 3,
        max_tokens: int = 2048,
        urlopen: Callable[..., Any] | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if not model.strip() or not api_key.strip():
            raise ValueError("GroqClient için model adı ve API anahtarı gerekli.")
        self.model = model.strip()
        self._api_key = api_key.strip()
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries
        # gpt-oss modelleri yanıttan önce akıl yürütme token'ı harcıyor; sınır düşük olursa yanıt boş kalabilir.
        self.max_tokens = max_tokens
        self._urlopen = urlopen or urllib.request.urlopen
        self._sleep = sleep
        self._ssl = _ssl_context()

    def __repr__(self) -> str:  # anahtar repr'de de görünmesin
        return f"GroqClient(model={self.model!r})"

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        body = json.dumps({"model": self.model, "messages": messages, "max_tokens": self.max_tokens}).encode()
        request = urllib.request.Request(
            self.url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                # Groq'un önündeki Cloudflare, Python'un varsayılan User-Agent'ını reddedebiliyor.
                "User-Agent": "noteproof-tagger",
            },
        )

        for attempt in range(self.max_retries + 1):
            try:
                with self._urlopen(request, timeout=self.timeout, context=self._ssl) as response:
                    data = json.load(response)
                break
            except urllib.error.HTTPError as err:
                if err.code in RETRY_STATUSES and attempt < self.max_retries:
                    self._sleep(_retry_delay(err, attempt))
                    continue
                raise RuntimeError(_http_error_message(err.code)) from None
            except json.JSONDecodeError:
                raise RuntimeError("Dil modeli JSON olmayan bir yanıt döndürdü.") from None
            except OSError as err:
                # URLError (bağlantı kurulamadı), okuma sırasında zaman aşımı (TimeoutError) ve
                # bağlantının kopması (ConnectionResetError) OSError'dır; hepsi geçici sayılır.
                if attempt < self.max_retries:
                    self._sleep(2.0**attempt)
                    continue
                reason = getattr(err, "reason", None) or type(err).__name__
                raise RuntimeError(f"Dil modeline bağlanılamadı: {reason}") from None

        try:
            content = data["choices"][0]["message"].get("content")
        except (KeyError, IndexError, TypeError, AttributeError):
            raise RuntimeError("Dil modeli beklenmeyen biçimde bir yanıt döndürdü.") from None
        # Boş yanıt hata değildir: suggest bunu boş öneri olarak ele alır.
        return content or ""


# NP-CONTRACT(02#5.3): NOTEPROOF_LLM_* değişkenlerinden bir LLMClient kurar.
def client_from_env() -> LLMClient:
    """Ortam değişkenlerine göre dil modeli istemcisini kurar.

    Değişkenlerden biri eksikse sessizce sahte bir istemciye düşmez; neyin eksik olduğunu söyleyen
    açık bir hata verir (03 bölüm 5). API anahtarının değeri hiçbir mesaja yazılmaz.
    """
    missing = [name for name in (ENV_PROVIDER, ENV_MODEL, ENV_API_KEY) if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError(
            "Dil modeli ayarları eksik: " + ", ".join(missing) + ". "
            "Bu değişkenleri repo kökündeki .env dosyasına yazın (uyeler/aleyna.md bölüm 3)."
        )

    provider = os.environ[ENV_PROVIDER].strip().lower()
    # NP-DECISION(K-005): sağlayıcı Groq, model openai/gpt-oss-20b (model adı .env'de durur).
    if provider == "groq":
        return GroqClient(os.environ[ENV_MODEL], os.environ[ENV_API_KEY])
    raise RuntimeError(f"Desteklenmeyen dil modeli sağlayıcısı: '{provider}'. Desteklenen: 'groq' (K-005).")


def _ssl_context() -> ssl.SSLContext:
    """Sistem sertifikalarıyla TLS bağlamı; certifi kuruluysa onun sertifikalarını kullanır.

    python.org'un macOS kurulumu sistem sertifikalarını görmüyor (CERTIFICATE_VERIFY_FAILED); certifi
    bu durumda yerel geliştirmeyi kurtarır. CI'da (Linux) sistem sertifikaları yeterli.
    """
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


def _retry_delay(err: urllib.error.HTTPError, attempt: int) -> float:
    """Sunucu Retry-After verdiyse ona uyar (en çok 30 sn), vermediyse 1, 2, 4... sn bekler."""
    header = err.headers.get("Retry-After") if err.headers else None
    try:
        return min(max(float(header), 0.0), 30.0)
    except (TypeError, ValueError):
        return 2.0**attempt


def _http_error_message(status: int) -> str:
    if status == 401:
        return "Dil modeli API anahtarı geçersiz (HTTP 401). .env'deki NOTEPROOF_LLM_API_KEY değerini kontrol edin."
    if status == 429:
        return "Dil modelinin istek sınırı aşıldı (HTTP 429); bir süre sonra yeniden deneyin."
    return f"Dil modeli isteği başarısız oldu (HTTP {status})."
