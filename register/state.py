# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    -
# contract: -
# depends:  core.graph.open_store, core.config.data_dir, ontology.vocab.Vocabulary.load, tagger.llm.client_from_env
# status:   wip
"""Kayıt servisinin paylaşılan kaynakları: grafik deposu, hesap tablosu, sözlük, dil modeli, kopya havuzu,
önizlemeler.

Oxigraph aynı klasörü aynı anda iki kez açamaz (kilit koyar); bu yüzden depo süreç başına bir kez açılır
ve bütün uç noktalar onu paylaşır. Uç noktalar bu fonksiyonları FastAPI'nin Depends'i ile alır; testler
NOTEPROOF_DATA_DIR'i geçici bir klasöre çevirip reset() çağırır ya da app.dependency_overrides kullanır.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import TYPE_CHECKING

from copywarn import CopyChecker
from core.config import data_dir
from core.graph import open_store
from ontology.vocab import Vocabulary
from tagger.llm import LLMClient, client_from_env

from .accounts import ACCOUNTS_DB, AccountStore
from .preview import PreviewCache

if TYPE_CHECKING:
    import pyoxigraph

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def graph_store() -> "pyoxigraph.Store":
    return open_store()


@lru_cache(maxsize=1)
def account_store() -> AccountStore:
    return AccountStore(data_dir() / ACCOUNTS_DB)


@lru_cache(maxsize=1)
def vocabulary() -> Vocabulary:
    return Vocabulary.load()


@lru_cache(maxsize=1)
def llm_client() -> LLMClient | None:
    """K-005 dil modeli istemcisi; NOTEPROOF_LLM_* tanımlı değilse None (önizleme öneri vermeden çalışır)."""
    try:
        return client_from_env()
    except RuntimeError as exc:
        log.warning("Dil modeli yapılandırılmamış; etiket önerisi verilmeyecek: %s", exc)
        return None


@lru_cache(maxsize=1)
def copy_checker() -> CopyChecker:
    # NP-TODO(arda): ARD-6 — açılışta grafikteki kayıtlı notlarla doldurulacak; şimdilik süreç içinde boş başlar.
    return CopyChecker()


@lru_cache(maxsize=1)
def preview_cache() -> PreviewCache:
    return PreviewCache()


def reset() -> None:
    """Önbelleğe alınmış kaynakları bırakır (testler ve veri klasörü değişince)."""
    for cached in (graph_store, account_store, vocabulary, llm_client, copy_checker, preview_cache):
        cached.cache_clear()
