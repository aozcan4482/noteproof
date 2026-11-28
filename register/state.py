# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    -
# contract: -
# depends:  core.graph.open_store, core.config.data_dir
# status:   wip
"""Kayıt servisinin paylaşılan kaynakları: grafik deposu ve hesap tablosu.

Oxigraph aynı klasörü aynı anda iki kez açamaz (kilit koyar); bu yüzden depo süreç başına bir kez açılır
ve bütün uç noktalar onu paylaşır. Uç noktalar bu fonksiyonları FastAPI'nin Depends'i ile alır; testler
NOTEPROOF_DATA_DIR'i geçici bir klasöre çevirip reset() çağırır.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from core.config import data_dir
from core.graph import open_store

from .accounts import ACCOUNTS_DB, AccountStore

if TYPE_CHECKING:
    import pyoxigraph


@lru_cache(maxsize=1)
def graph_store() -> "pyoxigraph.Store":
    return open_store()


@lru_cache(maxsize=1)
def account_store() -> AccountStore:
    return AccountStore(data_dir() / ACCOUNTS_DB)


def reset() -> None:
    """Önbelleğe alınmış kaynakları bırakır (testler ve veri klasörü değişince)."""
    graph_store.cache_clear()
    account_store.cache_clear()
