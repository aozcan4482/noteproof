# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1, S4, S6
# contract: 02#4 veri modeli, 02#7 POST /api/notes, 02#2 data/ düzeni
# depends:  shapes.validate.validate_note, anchor.store.Store.enqueue, copywarn.CopyChecker.add, core.ns
# status:   wip
"""Notun kaydı: yazarın onayladığı etiketlerle not ve PROV-O kaydı (proposal aktivite adımları 6–9).

Sıra bilinçlidir:
1. Not grafiği bellekte kurulur (rdflib) ve shapes.validate.validate_note (Eylem) ile denetlenir.
   Shape'ler geçmezse hiçbir şey yazılmaz (S4); yazar ihlalleri görür ve düzeltir.
2. Dosya ve çıkarılan metin data/notes/ ve data/text/ altına yazılır.
3. Üçlüler Oxigraph'a tek bir işlemde yazılır (Store.extend işlemseldir: ya hepsi ya hiçbiri).
4. Hash, zaman damgası kuyruğuna girer: anchor.store.Store.enqueue (Burak). Kayıt servisi anchor'a
   yalnızca buradan dokunur.
5. Metin kopya havuzuna eklenir: CopyChecker.add (Emine); sonraki notlar bununla karşılaştırılır.

2–4 arasında bir adım hata verirse önceki adımlar geri alınır: yarım kayıt (grafikte olup kuyrukta
olmayan not) kalmaz. Zincire hiçbir şey buradan gitmez; yalnızca hash kuyruğa girer.
"""

from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Callable

import rdflib
from rdflib.namespace import RDF, XSD

from anchor.store import Store as AnchorStore
from copywarn import CopyChecker, RegisteredNote
from core.config import data_dir
from core.ns import NAMESPACE, concept_iri, note_iri, registration_iri
from shapes.validate import Violation, validate_note

from .lookup import proof_url
from .preview import PreviewEntry

if TYPE_CHECKING:
    import pyoxigraph

log = logging.getLogger(__name__)

NP = rdflib.Namespace(NAMESPACE)
SCHEMA = rdflib.Namespace("https://schema.org/")
PROV = rdflib.Namespace("http://www.w3.org/ns/prov#")

# 02 bölüm 2: data/notes/<hash>.<uzantı>, data/text/<hash>.txt
_EXTENSIONS = {
    "application/pdf": "pdf", "image/jpeg": "jpg", "image/png": "png", "text/plain": "txt", "text/markdown": "md",
}

STATUS_REGISTERED = "registered"  # 02 bölüm 3: np:status değerlerinden biri


class ShapeViolation(ValueError):
    """Not shape'lere uymuyor (422 shape_violation). Hiçbir şey yazılmadı."""

    def __init__(self, violations: list[Violation]) -> None:
        super().__init__("Not shape'lere uymuyor.")
        self.violations = violations


@dataclass(frozen=True)
class Confirmation:
    """Yazarın onay gövdesindeki alanlar (02 bölüm 7)."""

    title: str
    course: str          # "Course_SEN0401"
    topics: list[str]    # ["Topic_TransactionFees"]
    summary: str


@dataclass(frozen=True)
class Registered:
    note_hash: str
    registered_at: str


def now_utc() -> str:
    """ISO 8601, UTC, saniye hassasiyetinde ve "Z" ile (Oxigraph xsd:dateTime'ı da böyle yazar)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def copywarning_iri(later_hash: str, earlier_hash: str) -> str:
    """02 bölüm 3: {NS}copywarning/{sonraki-hash}-{önceki-hash}."""
    return f"{NAMESPACE}copywarning/{later_hash}-{earlier_hash}"


def _concept(local_id: str, path: str, message: str) -> rdflib.URIRef:
    try:
        return rdflib.URIRef(concept_iri(local_id))
    except ValueError:
        # Kimlik biçimi bile tutmuyor (ör. etiket metni "Transaction fees"): sözlükte olmayan kavramla aynı
        # sonuç, aynı biçimde gösterilir (S4).
        raise ShapeViolation([Violation("NoteShape", path, f"{message}: {local_id!r}")]) from None


def build_note_graph(entry: PreviewEntry, confirmation: Confirmation, registered_at: str) -> rdflib.Graph:
    """Not, kayıt aktivitesi ve (varsa) olası kopya uyarıları; 02 bölüm 4'teki terimlerle."""
    h = entry.note_hash
    note, reg, account = rdflib.URIRef(note_iri(h)), rdflib.URIRef(registration_iri(h)), rdflib.URIRef(entry.account)

    g = rdflib.Graph()
    g.add((note, RDF.type, NP.Note))
    g.add((note, NP.noteHash, rdflib.Literal(h)))
    g.add((note, SCHEMA.name, rdflib.Literal(confirmation.title)))
    g.add((note, SCHEMA.encodingFormat, rdflib.Literal(entry.media_type)))
    if confirmation.summary:
        g.add((note, SCHEMA.abstract, rdflib.Literal(confirmation.summary)))
    g.add((note, NP.course, _concept(confirmation.course, "np:course", "Ders sözlükte yok")))
    for topic in confirmation.topics:
        g.add((note, NP.topic, _concept(topic, "np:topic", "Konu sözlükte yok")))
    # Bu kod yoluna yalnızca confirmed: true ile gelinir (app.py); G4: onaysız etiket kaydedilmez.
    g.add((note, NP.tagsConfirmed, rdflib.Literal(True)))
    g.add((note, NP.status, rdflib.Literal(STATUS_REGISTERED)))
    g.add((note, PROV.wasGeneratedBy, reg))
    g.add((note, PROV.wasAttributedTo, account))

    g.add((reg, RDF.type, NP.Registration))
    g.add((reg, PROV.wasAssociatedWith, account))
    g.add((reg, PROV.endedAtTime, rdflib.Literal(registered_at, datatype=XSD.dateTime)))

    # Aktivite adımı 8: benzer önceki not varsa "possible copy" olarak işaretlenir ve ona bağlanır.
    # Hüküm değil, kanıttır (01 bölüm 5): skor ve yöntem saklanır, karar insanlarındır.
    for w in entry.copy_warnings:
        cw = rdflib.URIRef(copywarning_iri(h, w.earlier_note_id))
        g.add((cw, RDF.type, NP.CopyWarning))
        g.add((cw, NP.laterNote, note))
        g.add((cw, NP.earlierNote, rdflib.URIRef(note_iri(w.earlier_note_id))))
        g.add((cw, NP.score, rdflib.Literal(round(w.score, 4), datatype=XSD.decimal)))
        g.add((cw, NP.method, rdflib.Literal(w.method)))
    return g


def _to_quads(g: rdflib.Graph) -> list["pyoxigraph.Quad"]:
    import pyoxigraph

    return list(pyoxigraph.parse(g.serialize(format="nt", encoding="utf-8"), pyoxigraph.RdfFormat.N_TRIPLES))


def register_note(
    *,
    entry: PreviewEntry,
    confirmation: Confirmation,
    author: str,
    graph: "pyoxigraph.Store",
    open_queue: Callable[[], AnchorStore],
    checker: CopyChecker,
    root: pathlib.Path | None = None,
) -> Registered:
    """Aktivite adımları 7–9. Shape'ler geçmezse ShapeViolation; o durumda hiçbir şey yazılmamıştır."""
    registered_at = now_utc()
    note_graph = build_note_graph(entry, confirmation, registered_at)

    report = validate_note(note_graph)
    if not report.conforms:
        raise ShapeViolation(report.violations)

    root = root if root is not None else data_dir()
    h = entry.note_hash
    note_file = root / "notes" / f"{h}.{_EXTENSIONS[entry.media_type]}"
    text_file = root / "text" / f"{h}.txt"
    quads = _to_quads(note_graph)
    written: list[pathlib.Path] = []
    in_graph = False
    try:
        for path, content in ((note_file, entry.data), (text_file, entry.text.encode("utf-8"))):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            written.append(path)
        graph.extend(quads)
        in_graph = True
        # Kayıt servisiyle timestamp servisi (Burak) arasındaki tek temas noktası (02#5.5).
        queue = open_queue()
        try:
            queue.enqueue(h, registered_at)
        finally:
            if hasattr(queue, "close"):
                queue.close()
    except Exception:
        log.exception("Kayıt %s yarıda kaldı; yazılanlar geri alınıyor", h)
        if in_graph:
            for quad in quads:
                graph.remove(quad)
        for path in written:
            path.unlink(missing_ok=True)
        raise

    checker.add(RegisteredNote(note_id=h, text=entry.text, author=author, registered_at=registered_at,
                               proof=proof_url(h)))
    log.info("Not kaydedildi: %s", h)
    return Registered(note_hash=h, registered_at=registered_at)
