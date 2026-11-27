# NOTEPROOF-FILE
# module:   shapes
# owner:    eylem           second: aleyna
# story:    S1, S4
# contract: 02#5.2 Violation, Report, validate_note
# depends:  ontology.vocab.Vocabulary
# status:   wip
"""Bir notun grafiğini SHACL shape'lerinden geçirir (proposal'daki kayıt akışında adım 6).

Kayıt servisi (Arda) notu kaydetmeden hemen önce `validate_note` çağırır; `Report.conforms` False ise
not kaydedilmez ve API 422 `shape_violation` döner (S4). İhlal mesajları Türkçedir ve kullanıcıya
gösterilebilir.

Nasıl çalışır:
1. Not grafiği ile sözlük grafiği (`Vocabulary.as_graph()`) tek bir veri grafiğinde birleştirilir;
   ders ve konunun sözlükte olup olmadığı böyle anlaşılır.
2. pySHACL, `shapes/note.shapes.ttl` ile çıkarımsız (inference="none") çalışır.
3. Sonuç grafiğindeki her ihlal bir `Violation`'a çevrilir: shape adı, `np:topic` gibi kısa yol ve
   shape'teki Türkçe mesaj; ihlal edilen değer varsa mesajın sonuna eklenir.

Grafikte hiç `np:Note` yoksa SHACL'in hedefi olmadığı için sonuç "uyuyor" çıkardı; bu modül o durumu
açıkça uymaz sayar. Bu modül hiçbir şey yazmaz, girdi grafiğini değiştirmez ve ağa çıkmaz.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pyshacl
import rdflib
from rdflib.namespace import RDF, SH, SKOS

from ontology.vocab import NAMESPACE, Vocabulary

SHAPES_TTL = Path(__file__).with_name("note.shapes.ttl")

_NP = rdflib.Namespace(NAMESPACE)
_PREFIXES = {
    NAMESPACE: "np:",
    "https://schema.org/": "schema:",
    "http://www.w3.org/ns/prov#": "prov:",
    str(SKOS): "skos:",
    str(RDF): "rdf:",
}


# NP-CONTRACT(02#5.2): alan adları ve türleri sabittir.
@dataclass(frozen=True)
class Violation:
    shape: str      # ör. "NoteShape"
    path: str       # ör. "np:topic"
    message: str    # Türkçe, kullanıcıya gösterilebilir


# NP-CONTRACT(02#5.2)
@dataclass(frozen=True)
class Report:
    conforms: bool
    violations: list[Violation]


# NP-CONTRACT(02#5.2): imza sabittir.
def validate_note(note_graph: rdflib.Graph) -> Report:
    """Not grafiğini NoteShape ile denetler. Girdi grafiğini değiştirmez."""
    if not any(note_graph.subjects(RDF.type, _NP.Note)):
        return Report(
            conforms=False,
            violations=[Violation("NoteShape", "rdf:type", "Grafikte kaydedilecek bir not (np:Note) yok.")],
        )

    data = rdflib.Graph()
    for triple in note_graph:
        data.add(triple)
    for triple in _vocabulary_graph():
        data.add(triple)

    shapes = _shapes_graph()
    conforms, results, _text = pyshacl.validate(
        data,
        shacl_graph=shapes,
        inference="none",
        abort_on_first=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
    )

    # Aynı kısıttan iki sonuç gelebilir (ör. minCount ve hasValue); kullanıcıya bir kez gösterilir.
    violations = sorted(set(_violations(results, shapes)), key=lambda v: (v.path, v.message))
    if not conforms and not violations:
        # pySHACL uymadı dedi ama ihlal okunamadı: sessizce geçmesin.
        violations = [Violation("NoteShape", "-", "Not doğrulanamadı; shape sonucu okunamadı.")]
    return Report(conforms=bool(conforms) and not violations, violations=violations)


@lru_cache(maxsize=1)
def _shapes_graph() -> rdflib.Graph:
    if not SHAPES_TTL.is_file():
        raise FileNotFoundError(f"Shape dosyası bulunamadı: {SHAPES_TTL}")
    graph = rdflib.Graph()
    graph.parse(str(SHAPES_TTL), format="turtle")
    return graph


@lru_cache(maxsize=1)
def _vocabulary_graph() -> rdflib.Graph:
    return Vocabulary.load().as_graph()


def _violations(results: rdflib.Graph, shapes: rdflib.Graph) -> list[Violation]:
    out = []
    for result in results.objects(None, SH.result):
        if results.value(result, SH.resultSeverity) not in (None, SH.Violation):
            continue
        path = results.value(result, SH.resultPath)
        source = results.value(result, SH.sourceShape)
        value = results.value(result, SH.value)
        message = _turkish_message(results, result)
        if isinstance(value, rdflib.URIRef):
            # Kullanıcı kimliği tanır ("Topic_X"), öneki değil.
            message = message.rstrip(".") + ": " + _short(value).removeprefix("np:")
        out.append(Violation(shape=_shape_name(shapes, source), path=_short(path), message=message))
    return out


def _turkish_message(results: rdflib.Graph, result: rdflib.term.Node) -> str:
    messages = list(results.objects(result, SH.resultMessage))
    for message in messages:
        if getattr(message, "language", None) == "tr":
            return str(message)
    return str(messages[0]) if messages else "Not shape'lere uymuyor."


def _shape_name(shapes: rdflib.Graph, source: rdflib.term.Node | None) -> str:
    # Property shape'ler boş düğümdür; adı, onu sh:property ile taşıyan node shape'ten alınır.
    if isinstance(source, rdflib.BNode):
        parent = shapes.value(None, SH.property, source)
        if parent is not None:
            source = parent
    if isinstance(source, rdflib.URIRef):
        return _short(source).split(":", 1)[-1]
    return "NoteShape"


def _short(node: rdflib.term.Node | None) -> str:
    if node is None:
        return "-"
    text = str(node)
    for base, prefix in _PREFIXES.items():
        if text.startswith(base):
            return prefix + text[len(base):]
    return text
