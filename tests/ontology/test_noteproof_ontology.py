# NOTEPROOF-FILE
# module:   ontology
# owner:    eylem           second: aleyna
# story:    S1, S2, S4, S6, S7
# contract: 02#4 Veri modeli, 02#6 Proof dosyası
# depends:  -
# status:   wip
"""ontology/noteproof.ttl ve ontology/context.jsonld testleri (EYL-4).

Ontolojideki np: terimlerinin 02 bölüm 4 ve 6'daki adlarla birebir aynı olduğunu, her terimin iki dilde
etiketi ve açıklaması olduğunu, öğrenci hesabında kişisel veri tutan özellik bulunmadığını ve JSON-LD
context'inin API'deki not alanlarını doğru terimlere çevirdiğini denetler. Dış dünyaya bağlanmaz.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

# NP-TODO(burak): pyproject.toml'da rdflib yok; "ontology" grubu eklenene kadar rdflib kurulu değilse
# bu dosya hata vermek yerine atlanır, böylece main'deki diğer testler kırmızıya dönmez.
rdflib = pytest.importorskip("rdflib")

from rdflib.namespace import OWL, RDF, RDFS  # noqa: E402

try:
    from core.ns import NAMESPACE
except ImportError:  # core/ henüz main'de değilse
    # NP-TODO(arda): core.ns main'e girince bu yedek değer silinecek; değer K-001'deki geçici değerdir.
    NAMESPACE = "https://github.com/aozcan4482/noteproof/ns#"

ROOT = Path(__file__).resolve().parents[2]
ONTOLOGY_TTL = ROOT / "ontology" / "noteproof.ttl"
CONTEXT_JSONLD = ROOT / "ontology" / "context.jsonld"

NP = rdflib.Namespace(NAMESPACE)
SCHEMA = rdflib.Namespace("https://schema.org/")
PROV = rdflib.Namespace("http://www.w3.org/ns/prov#")

# 02 bölüm 4: sınıf → üst sınıf (yoksa None).
EXPECTED_CLASSES = {
    "Note": SCHEMA.CreativeWork,
    "Registration": PROV.Activity,
    "StudentAccount": PROV.Agent,
    "DailyTimestamp": None,
    "Proof": None,
    "CopyWarning": None,
}

# 02 bölüm 6: proof dosyasının alanları, sırasıyla; merklePath'in her adımında side ve sibling.
PROOF_FIELDS = [
    "noteHash", "hashAlgorithm", "leafPrefix", "nodePrefix", "merklePath", "merkleRoot",
    "network", "txid", "blockHeight", "blockHash", "blockTime",
]
MERKLE_STEP_FIELDS = ["side", "sibling"]

# 02 bölüm 4'teki np: özellikleri ve proof dosyasının alanları. Başka np: özelliği olmamalı.
EXPECTED_PROPERTIES = (
    {"noteHash", "course", "topic", "tagsConfirmed", "status", "hasProof"}
    | {"day", "merkleRoot", "txid", "blockHeight", "blockHash", "blockTime", "network"}
    | {"laterNote", "earlierNote", "score", "method"}
    | set(PROOF_FIELDS)
    | set(MERKLE_STEP_FIELDS)
)

PERSONAL_DATA_PATTERN = re.compile(r"(?i)name|student|email|phone|number|surname|tckn")

SAMPLE_HASH = "a" * 64


@pytest.fixture(scope="module")
def graph() -> rdflib.Graph:
    g = rdflib.Graph()
    g.parse(str(ONTOLOGY_TTL), format="turtle")
    return g


@pytest.fixture(scope="module")
def context() -> dict:
    return json.loads(CONTEXT_JSONLD.read_text(encoding="utf-8"))


def _np_terms(graph: rdflib.Graph, kinds: tuple) -> set[str]:
    out = set()
    for kind in kinds:
        for subject in graph.subjects(RDF.type, kind):
            iri = str(subject)
            if iri.startswith(NAMESPACE):
                out.add(iri[len(NAMESPACE):])
    return out


def _np_properties(graph: rdflib.Graph) -> set[str]:
    return _np_terms(graph, (OWL.ObjectProperty, OWL.DatatypeProperty))


# -- noteproof.ttl ------------------------------------------------------------------------------------

def test_ontology_parses_and_prefix_matches_core_namespace(graph: rdflib.Graph) -> None:
    assert len(graph) > 0
    text = ONTOLOGY_TTL.read_text(encoding="utf-8")
    match = re.search(r"@prefix\s+np:\s+<([^>]+)>", text)
    assert match is not None
    assert match.group(1) == NAMESPACE


def test_classes_are_exactly_the_contract_classes(graph: rdflib.Graph) -> None:
    assert _np_terms(graph, (OWL.Class,)) == set(EXPECTED_CLASSES)
    for name, parent in EXPECTED_CLASSES.items():
        parents = set(graph.objects(NP[name], RDFS.subClassOf))
        assert parents == ({parent} if parent is not None else set()), name


def test_properties_are_exactly_the_contract_properties(graph: rdflib.Graph) -> None:
    assert _np_properties(graph) == EXPECTED_PROPERTIES


def test_every_np_term_has_tr_en_label_and_comment(graph: rdflib.Graph) -> None:
    terms = _np_terms(graph, (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty))
    for name in terms:
        labels = {getattr(label, "language", None) for label in graph.objects(NP[name], RDFS.label)}
        assert {"tr", "en"} <= labels, name
        comments = [str(c) for c in graph.objects(NP[name], RDFS.comment)]
        assert comments and all(c.strip() for c in comments), name


def test_student_account_has_no_personal_data_property(graph: rdflib.Graph) -> None:
    # 02#4: StudentAccount yalnızca takma ad taşır; gerçek isim ya da öğrenci numarası tutan özellik yoktur.
    for name in _np_properties(graph):
        assert not PERSONAL_DATA_PATTERN.search(name), name
        assert (NP[name], RDFS.domain, NP.StudentAccount) not in graph, name


def test_schema_prov_and_skos_terms_are_reused_not_redefined(graph: rdflib.Graph) -> None:
    for subject in set(graph.subjects(RDF.type, None)):
        iri = str(subject)
        assert iri.startswith(NAMESPACE) or iri == NAMESPACE.rstrip("#"), iri


def test_every_proof_file_field_is_an_ontology_term(graph: rdflib.Graph) -> None:
    # anchor/proof.py "@vocab": NAMESPACE ile yazar; her alan np:<alan> olur ve ontolojide tanımlı olmalı.
    defined = _np_properties(graph) | _np_terms(graph, (OWL.Class,))
    for field in [*PROOF_FIELDS, *MERKLE_STEP_FIELDS, "Proof"]:
        assert field in defined, field


# -- context.jsonld -----------------------------------------------------------------------------------

def test_context_vocab_is_the_namespace(context: dict) -> None:
    ctx = context["@context"]
    assert ctx["@vocab"] == NAMESPACE
    assert ctx["np"] == NAMESPACE


def test_context_np_terms_exist_in_ontology(graph: rdflib.Graph, context: dict) -> None:
    defined = _np_properties(graph)
    for key, value in context["@context"].items():
        target = value["@id"] if isinstance(value, dict) else value
        if isinstance(target, str) and target.startswith("np:"):
            assert target[len("np:"):] in defined, key


def test_context_also_accepts_ontology_style_field_names(context: dict) -> None:
    note_iri = f"{NAMESPACE}note/{SAMPLE_HASH}"
    document = {
        "@context": context["@context"],
        "@id": note_iri,
        "@type": "Note",
        "noteHash": SAMPLE_HASH,
        "name": "İşlem ücretleri notu",
        "course": "Course_SEN0401",
        "topic": ["Topic_TransactionFees", "Topic_FeeRate"],
        "tagsConfirmed": True,
        "status": "registered",
        "wasAttributedTo": f"{NAMESPACE}account/kuzgun",
    }
    g = rdflib.Graph()
    g.parse(data=json.dumps(document), format="json-ld")
    note = rdflib.URIRef(note_iri)

    assert (note, RDF.type, NP.Note) in g
    assert (note, NP.course, NP.Course_SEN0401) in g
    assert set(g.objects(note, NP.topic)) == {NP.Topic_TransactionFees, NP.Topic_FeeRate}
    assert (note, NP.tagsConfirmed, rdflib.Literal(True)) in g
    assert (note, NP.noteHash, rdflib.Literal(SAMPLE_HASH)) in g
    assert (note, SCHEMA.name, rdflib.Literal("İşlem ücretleri notu")) in g
    assert (note, PROV.wasAttributedTo, rdflib.URIRef(f"{NAMESPACE}account/kuzgun")) in g


def test_context_turns_the_api_confirm_body_into_shape_ready_triples(graph: rdflib.Graph, context: dict) -> None:
    # 02#7'deki onay gövdesi, alan adlarıyla olduğu gibi; kayıt servisi yalnızca @id, @type ve noteHash ekler.
    # NoteShape'in (shapes/) istediği np:course, np:topic ve np:tagsConfirmed buradan çıkmalı.
    note_iri = f"{NAMESPACE}note/{SAMPLE_HASH}"
    confirm_body = {
        "previewToken": "tok-123",
        "title": "İşlem ücretleri notu",
        "course": "Course_SEN0401",
        "topics": ["Topic_TransactionFees", "Topic_FeeRate"],
        "summary": "Ücret, girdiler ile çıktılar arasındaki farktır.",
        "confirmed": True,
    }
    document = {"@context": context["@context"], "@id": note_iri, "@type": "Note", "noteHash": SAMPLE_HASH,
                **confirm_body}
    g = rdflib.Graph()
    g.parse(data=json.dumps(document), format="json-ld")
    note = rdflib.URIRef(note_iri)

    assert (note, NP.course, NP.Course_SEN0401) in g
    assert set(g.objects(note, NP.topic)) == {NP.Topic_TransactionFees, NP.Topic_FeeRate}
    assert (note, NP.tagsConfirmed, rdflib.Literal(True)) in g
    assert (note, SCHEMA.name, rdflib.Literal("İşlem ücretleri notu")) in g
    assert (note, SCHEMA.abstract, rdflib.Literal("Ücret, girdiler ile çıktılar arasındaki farktır.")) in g

    # previewToken grafiğe girmez ve ontolojide olmayan bir np: terimi oluşmaz.
    defined = _np_properties(graph)
    for predicate in set(g.predicates()):
        text = str(predicate)
        assert "previewToken" not in text
        if text.startswith(NAMESPACE):
            assert text[len(NAMESPACE):] in defined, text


def test_proof_document_from_contract_uses_only_ontology_terms(graph: rdflib.Graph) -> None:
    # 02#6'daki proof dosyası kendi {"@vocab": NAMESPACE} context'iyle okunur.
    proof = {
        "@context": {"@vocab": NAMESPACE},
        "@type": "Proof",
        "@id": f"{NAMESPACE}proof/{SAMPLE_HASH}",
        "noteHash": SAMPLE_HASH,
        "hashAlgorithm": "SHA-256",
        "leafPrefix": "00",
        "nodePrefix": "01",
        "merklePath": [{"side": "left", "sibling": "b" * 64}],
        "merkleRoot": "c" * 64,
        "network": "signet",
        "txid": "d" * 64,
        "blockHeight": 1,
        "blockHash": "e" * 64,
        "blockTime": "2026-11-12T20:15:00+00:00",
    }
    g = rdflib.Graph()
    g.parse(data=json.dumps(proof), format="json-ld")
    defined = _np_properties(graph)
    predicates = {str(p) for p in g.predicates()} - {str(RDF.type)}
    assert predicates, "proof dosyasından hiç üçlü çıkmadı"
    for predicate in predicates:
        assert predicate.startswith(NAMESPACE), predicate
        assert predicate[len(NAMESPACE):] in defined, predicate
