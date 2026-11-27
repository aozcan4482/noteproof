# NOTEPROOF-FILE
# module:   core
# owner:    arda            second: burak
# story:    -
# contract: 02#5.1 core/graph.py
# depends:  -
# status:   stable
"""Arşivin grafik deposu: gömülü Oxigraph (K-004).

Oxigraph ayrı bir sunucu değildir; depo data/graph/ klasöründe durur. Kayıt servisi (Arda) yazar,
arama servisi (Erdener) SPARQL ile okur; ikisi de depoyu bu fonksiyonla açar.

pyoxigraph yalnızca fonksiyon çağrılınca içe aktarılır: anchor ve copywarn standart kütüphane dışında
bağımlılık almaz (03 bölüm 5) ve core'un diğer dosyalarını pyoxigraph kurulu olmadan da kullanabilmelidir.
"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from .config import data_dir

if TYPE_CHECKING:
    import pyoxigraph

GRAPH_SUBDIR = "graph"


# NP-CONTRACT(02#5.1): imza sabit.
def open_store(path: pathlib.Path | None = None) -> "pyoxigraph.Store":
    """Kalıcı Oxigraph deposunu açar; path verilmezse data_dir()/graph kullanılır.

    Klasör yoksa oluşturulur. Aynı klasörü aynı anda iki süreç açamaz (Oxigraph kilit koyar);
    sunucu depoyu bir kez açıp paylaşmalıdır.
    """
    try:
        import pyoxigraph
    except ImportError as exc:  # açık mesaj: hangi kurulum eksik
        raise ImportError('pyoxigraph kurulu değil: pip install -e ".[dev,all]"') from exc

    target = pathlib.Path(path) if path is not None else data_dir() / GRAPH_SUBDIR
    target.mkdir(parents=True, exist_ok=True)
    return pyoxigraph.Store(str(target))
