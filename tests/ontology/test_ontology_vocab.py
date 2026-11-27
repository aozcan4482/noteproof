# NOTEPROOF-FILE
# module:   ontology
# owner:    eylem           second: aleyna
# story:    S3, S4, S5
# contract: 02#5.2 Concept, Vocabulary
# depends:  -
# status:   wip
"""ontology/courses.ttl ve ontology/vocab.py testleri (EYL-2, EYL-3).

Gerçek sözlük dosyası üzerinde çalışır; bozuk sözlük örnekleri küçük Turtle metinleriyle kurulur.
Dış dünyaya bağlanmaz.
"""

from __future__ import annotations

import dataclasses
import re

import pytest

# NP-TODO(burak): pyproject.toml'da rdflib yok; "ontology" grubu eklenene kadar rdflib kurulu değilse
# bu dosya hata vermek yerine atlanır, böylece main'deki diğer testler kırmızıya dönmez.
rdflib = pytest.importorskip("rdflib")

from rdflib.namespace import RDF, SKOS  # noqa: E402

from ontology import list as ontology_list  # noqa: E402
from ontology.vocab import COURSES_TTL, MAX_TOPIC_DEPTH, NAMESPACE, Concept, Vocabulary, VocabularyError  # noqa: E402

# Sözlükte yayımlanan kimlikler. Bir kimlik main'e girdikten sonra yeniden adlandırılmaz (03#7);
# bu liste değişirse ekip haberdar edilmelidir (tagger, evalset/manifest.csv, arama).
EXPECTED_TOPICS = {
    "Topic_BitcoinIntroduction",
    "Topic_HowBitcoinWorks",
    "Topic_BitcoinCore",
    "Topic_KeysAndAddresses",
    "Topic_WalletRecovery",
    "Topic_Transactions",
    "Topic_TransactionInputs",
    "Topic_TransactionOutputs",
    "Topic_TransactionFees",
    "Topic_FeeRate",
    "Topic_FeeBumping",
    "Topic_AuthorizationAndAuthentication",
    "Topic_DigitalSignatures",
    "Topic_BitcoinNetwork",
    "Topic_Blockchain",
    "Topic_MiningAndConsensus",
    "Topic_BitcoinSecurity",
    "Topic_SecondLayerApplications",
}

PREFIXES = f"""
@prefix np:   <{NAMESPACE}> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
"""

GOOD_COURSE = """
np:Course_TEST1 a skos:Concept ; skos:inScheme np:CourseScheme ; skos:notation "TEST1" ;
    skos:prefLabel "Deneme"@tr , "Test"@en ; skos:narrower np:Topic_A .
"""


@pytest.fixture(scope="module")
def vocab() -> Vocabulary:
    return Vocabulary.load()


def _from_turtle(body: str) -> Vocabulary:
    graph = rdflib.Graph()
    graph.parse(data=PREFIXES + body, format="turtle")
    return Vocabulary.from_graph(graph)


# -- EYL-2: courses.ttl --------------------------------------------------------------------------------

def test_courses_ttl_parses_with_rdflib() -> None:
    graph = rdflib.Graph()
    graph.parse(str(COURSES_TTL), format="turtle")
    assert len(graph) > 0


def test_ttl_namespace_matches_core_namespace() -> None:
    # Namespace tek yerde tanımlıdır (core/ns.py, K-001); Turtle dosyasındaki np: öneki onunla aynı olmalı.
    text = COURSES_TTL.read_text(encoding="utf-8")
    match = re.search(r"@prefix\s+np:\s+<([^>]+)>", text)
    assert match is not None
    assert match.group(1) == NAMESPACE


def test_course_sen0401_with_notation_and_labels(vocab: Vocabulary) -> None:
    assert [c.id for c in vocab.courses()] == ["Course_SEN0401"]
    course = vocab.get("Course_SEN0401")
    assert course.broader is None
    assert course.label_tr and course.label_en
    graph = vocab.as_graph()
    notations = [str(n) for n in graph.objects(rdflib.URIRef(NAMESPACE + "Course_SEN0401"), SKOS.notation)]
    assert notations == ["SEN0401"]


def test_published_topic_ids_are_exactly_the_expected_set(vocab: Vocabulary) -> None:
    assert {c.id for c in vocab.topics("Course_SEN0401")} == EXPECTED_TOPICS


def test_every_topic_has_broader_chain_to_course(vocab: Vocabulary) -> None:
    for topic in vocab.topics("Course_SEN0401"):
        current = topic
        steps = 0
        while current.broader is not None:
            current = vocab.get(current.broader)
            steps += 1
        assert current.id == "Course_SEN0401", topic.id
        assert 1 <= steps <= MAX_TOPIC_DEPTH, topic.id


def test_every_concept_has_tr_and_en_label(vocab: Vocabulary) -> None:
    for concept in [*vocab.courses(), *vocab.topics("Course_SEN0401")]:
        assert concept.label_tr.strip(), concept.id
        assert concept.label_en.strip(), concept.id


def test_ids_are_ascii_without_spaces(vocab: Vocabulary) -> None:
    for concept in [*vocab.courses(), *vocab.topics("Course_SEN0401")]:
        assert concept.id.isascii() and " " not in concept.id, concept.id


def test_s5_acceptance_transactions_fees_feerate_hierarchy(vocab: Vocabulary) -> None:
    assert vocab.get("Topic_Transactions").broader == "Course_SEN0401"
    assert vocab.get("Topic_TransactionFees").broader == "Topic_Transactions"
    assert vocab.get("Topic_FeeRate").broader == "Topic_TransactionFees"


# -- EYL-3: Vocabulary --------------------------------------------------------------------------------

def test_s5_acceptance_narrower_transactions_contains_fees_and_feerate(vocab: Vocabulary) -> None:
    below = vocab.narrower("Topic_Transactions")
    assert "Topic_TransactionFees" in below
    assert "Topic_FeeRate" in below


def test_narrower_is_transitive_and_excludes_self(vocab: Vocabulary) -> None:
    assert "Topic_Transactions" not in vocab.narrower("Topic_Transactions")
    assert sorted(vocab.narrower("Topic_TransactionFees")) == ["Topic_FeeBumping", "Topic_FeeRate"]
    assert vocab.narrower("Topic_FeeRate") == []


def test_s4_unknown_id_is_not_topic(vocab: Vocabulary) -> None:
    assert vocab.is_topic("Topic_TransactionFees") is True
    assert vocab.is_topic("Topic_DoesNotExist") is False
    assert vocab.is_topic("Transaction fees") is False      # etiket metniyle eşleştirme yapılmaz (02#3)
    assert vocab.is_topic("Course_SEN0401") is False


def test_is_course(vocab: Vocabulary) -> None:
    assert vocab.is_course("Course_SEN0401") is True
    assert vocab.is_course("Course_XXX9999") is False
    assert vocab.is_course("Topic_Transactions") is False


def test_unknown_ids_raise_instead_of_returning_empty(vocab: Vocabulary) -> None:
    with pytest.raises(KeyError):
        vocab.topics("Course_XXX9999")
    with pytest.raises(KeyError):
        vocab.narrower("Topic_DoesNotExist")


def test_topics_are_in_tree_order(vocab: Vocabulary) -> None:
    ids = [c.id for c in vocab.topics("Course_SEN0401")]
    assert ids.index("Topic_Transactions") < ids.index("Topic_TransactionFees") < ids.index("Topic_FeeRate")


def test_concept_is_frozen_dataclass(vocab: Vocabulary) -> None:
    concept = vocab.get("Topic_FeeRate")
    assert isinstance(concept, Concept)
    with pytest.raises(dataclasses.FrozenInstanceError):
        concept.label_tr = "x"  # type: ignore[misc]


def test_as_graph_returns_independent_copy(vocab: Vocabulary) -> None:
    graph = vocab.as_graph()
    before = len(graph)
    graph.add((rdflib.URIRef(NAMESPACE + "x"), RDF.type, SKOS.Concept))
    assert len(vocab.as_graph()) == before


# -- Bozuk sözlükler açık hata verir (03#5) -----------------------------------------------------------

def test_empty_graph_raises() -> None:
    with pytest.raises(VocabularyError, match="boş"):
        Vocabulary.from_graph(rdflib.Graph())


def test_valid_minimal_vocabulary_loads() -> None:
    v = _from_turtle(GOOD_COURSE + """
np:Topic_A a skos:Concept ; skos:inScheme np:CourseScheme ;
    skos:prefLabel "A"@tr , "A"@en ; skos:broader np:Course_TEST1 .
""")
    assert v.is_topic("Topic_A")


def test_topic_without_broader_raises() -> None:
    with pytest.raises(VocabularyError, match="broader"):
        _from_turtle(GOOD_COURSE.replace(" ; skos:narrower np:Topic_A", "") + """
np:Topic_A a skos:Concept ; skos:inScheme np:CourseScheme ; skos:prefLabel "A"@tr , "A"@en .
""")


def test_missing_english_label_raises() -> None:
    with pytest.raises(VocabularyError, match="@en"):
        _from_turtle(GOOD_COURSE + """
np:Topic_A a skos:Concept ; skos:inScheme np:CourseScheme ;
    skos:prefLabel "A"@tr ; skos:broader np:Course_TEST1 .
""")


def test_broader_without_matching_narrower_raises() -> None:
    with pytest.raises(VocabularyError, match="uyuşmuyor"):
        _from_turtle(GOOD_COURSE.replace(" ; skos:narrower np:Topic_A", "") + """
np:Topic_A a skos:Concept ; skos:inScheme np:CourseScheme ;
    skos:prefLabel "A"@tr , "A"@en ; skos:broader np:Course_TEST1 .
""")


def test_bad_id_pattern_raises() -> None:
    with pytest.raises(VocabularyError, match="kalıba"):
        _from_turtle(GOOD_COURSE.replace(" ; skos:narrower np:Topic_A", " ; skos:narrower np:Topic_fee_rate") + """
np:Topic_fee_rate a skos:Concept ; skos:inScheme np:CourseScheme ;
    skos:prefLabel "A"@tr , "A"@en ; skos:broader np:Course_TEST1 .
""")


def test_too_deep_hierarchy_raises() -> None:
    body = GOOD_COURSE + """
np:Topic_A a skos:Concept ; skos:inScheme np:CourseScheme ; skos:prefLabel "A"@tr , "A"@en ;
    skos:broader np:Course_TEST1 ; skos:narrower np:Topic_B .
np:Topic_B a skos:Concept ; skos:inScheme np:CourseScheme ; skos:prefLabel "B"@tr , "B"@en ;
    skos:broader np:Topic_A ; skos:narrower np:Topic_C .
np:Topic_C a skos:Concept ; skos:inScheme np:CourseScheme ; skos:prefLabel "C"@tr , "C"@en ;
    skos:broader np:Topic_B ; skos:narrower np:Topic_D .
np:Topic_D a skos:Concept ; skos:inScheme np:CourseScheme ; skos:prefLabel "D"@tr , "D"@en ;
    skos:broader np:Topic_C .
"""
    with pytest.raises(VocabularyError, match="düzey"):
        _from_turtle(body)


# -- python -m ontology.list ---------------------------------------------------------------------------

def test_list_cli_prints_every_id_and_label(capsys: pytest.CaptureFixture[str], vocab: Vocabulary) -> None:
    assert ontology_list.main() == 0
    out = capsys.readouterr().out
    for concept in [*vocab.courses(), *vocab.topics("Course_SEN0401")]:
        assert f"`{concept.id}`" in out
        assert concept.label_tr in out
        assert concept.label_en in out
    assert "1 ders, 18 konu." in out
