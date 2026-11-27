# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3, 02#8
# depends:  -
# status:   wip
"""Dil modeli istemcisi: sağlayıcıdan bağımsız LLMClient arayüzü ve ortam değişkenlerinden istemci kurulumu.

Sağlayıcıya özel her şey bu dosyada kalır; tagger/suggest.py yalnızca LLMClient.complete çağırır.
Böylece sağlayıcı değişirse (K-005) yalnızca bu dosya değişir.

Testler bu dosyadaki gerçek istemciyi hiç kullanmaz: tests/tagger/fake_llm.py içindeki FakeLLM,
LLMClient arayüzüne uyan, ağa çıkmayan bir sahtedir (03 bölüm 8).

Arama yanıtları (Erdener, ERD-8) da modele client_from_env üzerinden ulaşır.
"""

from __future__ import annotations

import os
from typing import Protocol, runtime_checkable

# 02#8: dil modeli bağlantısının ortam değişkenleri. Değerler yerelde .env dosyasında durur, repoya girmez.
ENV_PROVIDER = "NOTEPROOF_LLM_PROVIDER"
ENV_MODEL = "NOTEPROOF_LLM_MODEL"
ENV_API_KEY = "NOTEPROOF_LLM_API_KEY"


# NP-CONTRACT(02#5.3): imza ve dönüş türü sabit; sağlayıcı istemcileri bu arayüze uyar.
@runtime_checkable
class LLMClient(Protocol):
    def complete(self, prompt: str, *, system: str | None = None) -> str:
        """İstemi modele gönderir, modelin düz metin yanıtını döndürür."""
        ...


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
    # NP-DECISION(K-005): sağlayıcı ve model kararı henüz verilmedi. Karar verilince seçilen sağlayıcının
    # istemcisi bu dosyaya eklenir ve burada döndürülür; o zamana kadar hiçbir sağlayıcı desteklenmez.
    raise RuntimeError(
        f"Desteklenmeyen dil modeli sağlayıcısı: '{provider}'. "
        "Sağlayıcı kararı (07_KARARLAR.md, K-005) henüz verilmedi."
    )
