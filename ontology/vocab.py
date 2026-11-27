# NOTEPROOF-FILE
# module:   ontology
# owner:    eylem           second: aleyna
# story:    S3, S4, S5
# contract: 02#5.2 Concept, Vocabulary
# depends:  core.ns.NAMESPACE
# status:   wip
"""Ders ve konu sözlüğünün okuyucusu.

`ontology/courses.ttl` dosyasını RDFLib ile okur ve diğer modüllere tek bir arayüz sunar:
tagger (Aleyna) önerilerini `is_topic` ile süzer, kayıt servisi (Arda) `/api/vocabulary` yanıtını
`courses` ve `topics` ile üretir, arama (Erdener) alt konuları `narrower` ile bulur (S5).

Yükleme sırasında sözlük denetlenir; bozuk bir sözlük sessizce yarım yüklenmez, `VocabularyError` verir.
Denetlenenler: kimlik kalıbı, iki dilde etiket, her konunun derse giden bir `skos:broader` zinciri,
`broader`/`narrower` tutarlılığı ve dersin altında en çok üç düzey konu.
Bu modül hiçbir şey yazmaz ve ağa çıkmaz.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import rdflib
from rdflib.namespace import RDF, SKOS

try:
    from core.ns import NAMESPACE
except ImportError:  # core/ henüz main'de değilse
    # NP-TODO(arda): core.ns main'e girince bu yedek değer silinecek; değer K-001'deki geçici değerdir.
    NAMESPACE = "https://github.com/aozcan4482/noteproof/ns#"

COURSES_TTL = Path(__file__).with_name("courses.ttl")
SCHEME_ID = "CourseScheme"
MAX_TOPIC_DEPTH = 3  # konu → alt konu → alt-alt konu (uyeler/eylem.md, tasarım notları)

_COURSE_RE = re.compile(r"^Course_[A-Z0-9]+$")
_TOPIC_RE = re.compile(r"^Topic_[A-Z][A-Za-z0-9]*$")


class VocabularyError(ValueError):
    """Sözlük dosyası kurallara uymuyor. Mesaj Türkçedir ve hangi kavramın bozuk olduğunu söyler."""


# NP-CONTRACT(02#5.2): alan adları ve türleri sabittir.
@dataclass(frozen=True)
class Concept:
    id: str                 # "Topic_TransactionFees"
    label_tr: str
    label_en: str
    broader: str | None     # üst kavramın id'si; dersler için None


# NP-CONTRACT(02#5.2): public metotların adları, parametreleri ve dönüş türleri sabittir.
class Vocabulary:
    """Yüklenmiş ve denetlenmiş sözlük. Değiştirilemez; her çağrı aynı sonucu verir."""

    def __init__(self, graph: rdflib.Graph, concepts: dict[str, Concept]) -> None:
        # Doğrudan çağırma; `load()` ya da `from_graph()` kullan. Denetim orada yapılır.
        self._graph = graph
        self._concepts = concepts
        self._children: dict[str, list[str]] = {cid: [] for cid in concepts}
        for concept in concepts.values():
            if concept.broader is not None:
                self._children[concept.broader].append(concept.id)
        for kids in self._children.values():
            kids.sort()

    # -- yükleme -------------------------------------------------------------------------------------

    @classmethod
    def load(cls) -> "Vocabulary":
        """`ontology/courses.ttl` dosyasını okur ve denetler."""
        if not COURSES_TTL.is_file():
            raise VocabularyError(f"Sözlük dosyası bulunamadı: {COURSES_TTL}")
        graph = rdflib.Graph()
        graph.parse(str(COURSES_TTL), format="turtle")
        return cls.from_graph(graph)

    @classmethod
    def from_graph(cls, graph: rdflib.Graph) -> "Vocabulary":
        """Hazır bir RDF grafiğinden sözlük kurar. Testler ve shape doğrulaması için."""
        scheme = rdflib.URIRef(NAMESPACE + SCHEME_ID)
        members = sorted({str(s) for s in graph.subjects(SKOS.inScheme, scheme)})
        if not members:
            raise VocabularyError("Sözlük boş: np:CourseScheme şemasında hiç kavram yok.")

        concepts: dict[str, Concept] = {}
        for iri in members:
            cid = _local_id(iri)
            concepts[cid] = _read_concept(graph, rdflib.URIRef(iri), cid)

        _check_structure(graph, concepts)
        return cls(graph, concepts)

    # -- sorgular ------------------------------------------------------------------------------------

    def courses(self) -> list[Concept]:
        """Bütün dersler, kimliğe göre sıralı."""
        return [c for cid, c in sorted(self._concepts.items()) if _COURSE_RE.match(cid)]

    def topics(self, course_id: str) -> list[Concept]:
        """Dersin bütün konuları, alt konular dahil; ağaç sırasıyla (üst konu, sonra altları)."""
        if not self.is_course(course_id):
            raise KeyError(f"Sözlükte böyle bir ders yok: {course_id}")
        return [self._concepts[cid] for cid in self._descendants(course_id)]

    def is_course(self, concept_id: str) -> bool:
        return concept_id in self._concepts and bool(_COURSE_RE.match(concept_id))

    def is_topic(self, concept_id: str) -> bool:
        return concept_id in self._concepts and bool(_TOPIC_RE.match(concept_id))

    def narrower(self, topic_id: str) -> list[str]:
        """Konunun bütün alt konuları (geçişli). Konunun kendisi dahil değildir."""
        if not self.is_topic(topic_id):
            raise KeyError(f"Sözlükte böyle bir konu yok: {topic_id}")
        return self._descendants(topic_id)

    def get(self, concept_id: str) -> Concept:
        """Tek bir kavram. Bilinmeyen kimlik için KeyError."""
        try:
            return self._concepts[concept_id]
        except KeyError:
            raise KeyError(f"Sözlükte böyle bir kavram yok: {concept_id}") from None

    def as_graph(self) -> rdflib.Graph:
        """Sözlüğün RDF grafiğinin bir kopyası. Shape doğrulaması (shapes/validate.py) bunu kullanır."""
        copy = rdflib.Graph()
        for triple in self._graph:
            copy.add(triple)
        copy.bind("np", rdflib.Namespace(NAMESPACE))
        copy.bind("skos", SKOS)
        return copy

    # -- iç yardımcılar ------------------------------------------------------------------------------

    def _descendants(self, concept_id: str) -> list[str]:
        out: list[str] = []
        stack = list(reversed(self._children[concept_id]))
        while stack:
            cid = stack.pop()
            out.append(cid)
            stack.extend(reversed(self._children[cid]))
        return out


def _local_id(iri: str) -> str:
    if not iri.startswith(NAMESPACE):
        raise VocabularyError(f"Kavram NoteProof namespace'inde değil: {iri} (beklenen önek: {NAMESPACE})")
    cid = iri[len(NAMESPACE):]
    if not (_COURSE_RE.match(cid) or _TOPIC_RE.match(cid)):
        raise VocabularyError(
            f"Kimlik kalıba uymuyor: {cid}. Ders 'Course_<KOD>', konu 'Topic_<PascalCase>' olmalı."
        )
    return cid


def _read_concept(graph: rdflib.Graph, iri: rdflib.URIRef, cid: str) -> Concept:
    if (iri, RDF.type, SKOS.Concept) not in graph:
        raise VocabularyError(f"{cid} bir skos:Concept olarak tanımlanmamış.")

    labels: dict[str, str] = {}
    for label in graph.objects(iri, SKOS.prefLabel):
        lang = getattr(label, "language", None)
        if lang in ("tr", "en"):
            if lang in labels:
                raise VocabularyError(f"{cid} için birden çok skos:prefLabel@{lang} var.")
            labels[lang] = str(label)
    for lang in ("tr", "en"):
        if not labels.get(lang, "").strip():
            raise VocabularyError(f"{cid} için skos:prefLabel@{lang} eksik.")

    broaders = [_local_id(str(b)) for b in graph.objects(iri, SKOS.broader)]
    if _COURSE_RE.match(cid):
        if broaders:
            raise VocabularyError(f"Ders {cid} bir üst kavrama bağlanmamalı (skos:broader yok olmalı).")
        code = cid[len("Course_"):]
        notations = [str(n) for n in graph.objects(iri, SKOS.notation)]
        if notations != [code]:
            raise VocabularyError(f'{cid} için tek bir skos:notation "{code}" olmalı; bulunan: {notations}')
        broader = None
    else:
        if len(broaders) != 1:
            raise VocabularyError(f"Konu {cid} tam bir skos:broader taşımalı; bulunan: {len(broaders)}.")
        broader = broaders[0]

    return Concept(id=cid, label_tr=labels["tr"], label_en=labels["en"], broader=broader)


def _check_structure(graph: rdflib.Graph, concepts: dict[str, Concept]) -> None:
    # Her broader şemadaki bir kavramı göstermeli ve konu zinciri bir derste bitmeli (S4, S5).
    for concept in concepts.values():
        if concept.broader is not None and concept.broader not in concepts:
            raise VocabularyError(f"{concept.id} sözlükte olmayan {concept.broader} kavramına bağlı.")
    for concept in concepts.values():
        if concept.broader is None:
            continue
        seen = {concept.id}
        depth = 0
        current = concept
        while current.broader is not None:
            depth += 1
            if current.broader in seen:
                raise VocabularyError(f"{concept.id} için skos:broader zincirinde döngü var.")
            seen.add(current.broader)
            current = concepts[current.broader]
        if not _COURSE_RE.match(current.id):
            raise VocabularyError(f"{concept.id} konusunun skos:broader zinciri bir derste bitmiyor.")
        if depth > MAX_TOPIC_DEPTH:
            raise VocabularyError(
                f"{concept.id} dersin {depth}. düzeyinde; en çok {MAX_TOPIC_DEPTH} düzey konu olabilir."
            )

    # broader ve narrower birbirinin tersi olmalı: arama skos:narrower* ile yürür (02#5.6).
    for concept in concepts.values():
        iri = rdflib.URIRef(NAMESPACE + concept.id)
        declared = sorted(_local_id(str(n)) for n in graph.objects(iri, SKOS.narrower))
        expected = sorted(c.id for c in concepts.values() if c.broader == concept.id)
        if declared != expected:
            raise VocabularyError(
                f"{concept.id} için skos:narrower ile skos:broader uyuşmuyor. "
                f"narrower: {declared}, broader'dan beklenen: {expected}"
            )
