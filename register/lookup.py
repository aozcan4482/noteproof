# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1
# contract: 02#4 veri modeli, 02#7 alreadyRegistered
# depends:  core.ns
# status:   wip
"""Grafikte kayıtlı bir notu hash'iyle bulma (proposal aktivite adımı 3: "hash zaten kayıtlıysa önceki
kaydı ve proof'unu gösterir").

Not ile kayıt arasındaki bağ 02 bölüm 4'teki terimlerledir: not prov:wasGeneratedBy kayıt; kayıt
prov:endedAtTime zaman; not prov:wasAttributedTo hesap; hesap schema:alternateName takma ad.
Bu üçlüleri kayıt uç noktası (ARD-4) yazar; burada yalnızca okunur.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from core.ns import note_iri

if TYPE_CHECKING:
    import pyoxigraph

PROV = "http://www.w3.org/ns/prov#"
SCHEMA = "https://schema.org/"


@dataclass(frozen=True)
class RegisteredNoteInfo:
    note_hash: str
    registered_at: str  # ISO 8601, UTC
    author: str         # takma ad


def proof_url(note_hash: str) -> str:
    """Proof dosyasının API yolu (02 bölüm 7: GET /api/notes/{hash}/proof); web/mock/*.json ile aynı biçim."""
    return f"/api/notes/{note_hash}/proof"


def _single(graph: "pyoxigraph.Store", subject, predicate: str):
    import pyoxigraph

    for quad in graph.quads_for_pattern(subject, pyoxigraph.NamedNode(predicate), None):
        return quad.object
    return None


def find_registered(graph: "pyoxigraph.Store", note_hash: str) -> RegisteredNoteInfo | None:
    """Hash grafikte kayıtlıysa kayıt zamanı ve yazarıyla döndürür; değilse None."""
    import pyoxigraph

    note = pyoxigraph.NamedNode(note_iri(note_hash))
    registration = _single(graph, note, PROV + "wasGeneratedBy")
    if registration is None:
        return None
    ended = _single(graph, registration, PROV + "endedAtTime")
    account = _single(graph, note, PROV + "wasAttributedTo")
    pseudonym = _single(graph, account, SCHEMA + "alternateName") if account is not None else None
    return RegisteredNoteInfo(
        note_hash=note_hash,
        registered_at=ended.value if ended is not None else "",
        author=pseudonym.value if pseudonym is not None else "",
    )
