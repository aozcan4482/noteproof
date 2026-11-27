# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    S1
# contract: 02#5.1 core/hashing.py
# depends:  -
# status:   stable
"""Notun SHA-256 hash'i (proposal aktivite adımı 3).

Not, dosyasının hash'iyle tanımlanır: IRI'ler, kuyruk ve proof sayfası hep bu değeri kullanır.
Proof sayfası (web/js/verify.js, Erdener) aynı hash'i tarayıcıda dosyanın ham byte'larından yeniden
hesaplar; bu yüzden burada hiçbir ön işlem (satır sonu, metin dönüştürme) yapılmaz.
"""

from __future__ import annotations

import hashlib


# NP-CONTRACT(02#5.1): imza sabit; dönüş küçük harfli 64 karakterlik hex.
def sha256_hex(data: bytes) -> str:
    """Byte dizisinin SHA-256 özetini küçük harfli hex olarak döndürür."""
    if not isinstance(data, (bytes, bytearray, memoryview)):
        # str kabul edilmez: hangi kodlamayla byte'a çevrileceği belirsizdir ve hash tarayıcıdakiyle tutmaz.
        raise TypeError(f"sha256_hex byte bekler, {type(data).__name__} geldi.")
    return hashlib.sha256(data).hexdigest()
