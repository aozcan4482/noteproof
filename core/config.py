# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    -
# contract: 02#5.1 core/config.py, 02#8 NOTEPROOF_DATA_DIR
# depends:  -
# status:   stable
"""Ortak ayarlar: çalışma verisinin klasörü.

Yollar koda yazılmaz, ortam değişkeninden okunur (03 bölüm 5). data/ altındaki düzen 02 bölüm 2'dedir:
notes/, text/, graph/, noteproof.sqlite, proofs/.
"""

from __future__ import annotations

import os
import pathlib

ENV_DATA_DIR = "NOTEPROOF_DATA_DIR"
DEFAULT_DATA_DIR = "./data"


# NP-CONTRACT(02#5.1): imza sabit.
def data_dir() -> pathlib.Path:
    """Çalışma verisi klasörü: NOTEPROOF_DATA_DIR, yoksa ./data (çalışılan klasöre göre).

    Klasörü oluşturmaz; yazan modül gerektiğinde oluşturur. Değişken tanımlı ama boşsa hata verir:
    .env'de yanlışlıkla boş bırakılan bir değer, verinin beklenmedik bir yere yazılmasına yol açmamalı.
    """
    value = os.environ.get(ENV_DATA_DIR)
    if value is None:
        return pathlib.Path(DEFAULT_DATA_DIR)
    if not value.strip():
        raise ValueError(f"{ENV_DATA_DIR} tanımlı ama boş; bir klasör yolu yazın ya da değişkeni kaldırın.")
    return pathlib.Path(value)
