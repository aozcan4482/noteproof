# NOTEPROOF-FILE
# module:   shapes
# owner:    eylem           second: aleyna
# story:    S1, S4
# contract: 02#5.2 Violation, Report, validate_note
# depends:  -
# status:   wip
"""shapes/note.shapes.ttl ve shapes/validate.py testleri (EYL-5).

Kabul ölçütü: olumlu örnek uyuyor; dört olumsuz örnek adıyla reddediliyor (hash yok, ders yok,
sözlükte olmayan konu, tagsConfirmed true değil); ihlal mesajları Türkçe; boş grafik sessizce uymaz.
Gerçek sözlük (ontology/courses.ttl) kullanılır; dış dünyaya bağlanmaz.
"""

from __future__ import annotations

import dataclasses

import pytest
import rdflib
from rdflib.namespace import RDF

from ontology.vocab import NAMESPACE
from shapes.validate import Report, Violation, validate_note

NP = rdflib.Namespace(NAMESPACE)
SCHEMA = rdflib.Namespace("https://schema.org/")
NOTE_HASH = "ab" * 32
NOTE = rdflib.URIRef(f"{NAMESPACE}note/{NOTE_HASH}")

_DEFAULT = object()


def make_note(
    *,
    note_hash=NOTE_HASH,
    courses=("Course_SEN0401",),
    topics=("Topic_TransactionFees",),
    tags_confirmed=_DEFAULT,
) -> rdflib.Graph:
    """Kayda hazır bir not grafiği; parametrelerle tek tek alanlar bozulur ya da çıkarılır."""
    g = rdflib.Graph()
    g.add((NOTE, RDF.type, NP.Note))
    g.add((NOTE, SCHEMA.name, rdflib.Literal("İşlem ücretleri notu")))
    if note_hash is not None:
        g.add((NOTE, NP.noteHash, rdflib.Literal(note_hash)))
    for course in courses:
        g.add((NOTE, NP.course, NP[course]))
    for topic in topics:
        g.add((NOTE, NP.topic, NP[topic]))
    if tags_confirmed is _DEFAULT:
        g.add((NOTE, NP.tagsConfirmed, rdflib.Literal(True)))
    elif tags_confirmed is not None:
        g.add((NOTE, NP.tagsConfirmed, rdflib.Literal(tags_confirmed)))
    return g


def paths(report: Report) -> list[str]:
    return [v.path for v in report.violations]


# -- olumlu örnek -------------------------------------------------------------------------------------

def test_valid_note_conforms() -> None:
    report = validate_note(make_note())
    assert report == Report(conforms=True, violations=[])


def test_valid_note_with_several_topics_conforms() -> None:
    report = validate_note(make_note(topics=("Topic_Transactions", "Topic_FeeRate", "Topic_FeeBumping")))
    assert report.conforms is True


# -- dört olumsuz örnek (kabul ölçütü) ----------------------------------------------------------------

def test_rejects_note_without_hash() -> None:
    report = validate_note(make_note(note_hash=None))
    assert report.conforms is False
    assert paths(report) == ["np:noteHash"]
    assert report.violations[0].message == "Notun SHA-256 hash'i yok."


def test_rejects_note_without_course() -> None:
    report = validate_note(make_note(courses=()))
    assert report.conforms is False
    assert paths(report) == ["np:course"]
    assert report.violations[0].message == "Notun tam bir dersi olmalı."


def test_s4_acceptance_rejects_topic_not_in_vocabulary() -> None:
    # S4: sözlükte olmayan bir konuyla onaylanan not reddedilir.
    report = validate_note(make_note(topics=("Topic_TransactionFees", "Topic_QuantumMoney")))
    assert report.conforms is False
    assert paths(report) == ["np:topic"]
    assert report.violations[0].shape == "NoteShape"
    assert report.violations[0].message == "Konu sözlükte yok: Topic_QuantumMoney"


def test_rejects_note_whose_tags_are_not_confirmed() -> None:
    report = validate_note(make_note(tags_confirmed=False))
    assert report.conforms is False
    assert paths(report) == ["np:tagsConfirmed"]
    assert "onaylanmamış" in report.violations[0].message


# -- diğer olumsuz durumlar ---------------------------------------------------------------------------

def test_rejects_note_without_tags_confirmed_value() -> None:
    report = validate_note(make_note(tags_confirmed=None))
    assert report.conforms is False
    assert "np:tagsConfirmed" in paths(report)


def test_rejects_note_without_topic() -> None:
    report = validate_note(make_note(topics=()))
    assert report.conforms is False
    assert paths(report) == ["np:topic"]
    assert report.violations[0].message == "Notun en az bir konusu olmalı."


def test_rejects_course_that_is_not_in_vocabulary() -> None:
    report = validate_note(make_note(courses=("Course_XXX9999",)))
    assert report.conforms is False
    assert paths(report) == ["np:course"]
    assert report.violations[0].message == "Ders sözlükte yok: Course_XXX9999"


def test_rejects_course_id_used_as_topic() -> None:
    report = validate_note(make_note(topics=("Course_SEN0401",)))
    assert report.conforms is False
    assert paths(report) == ["np:topic"]


def test_rejects_note_with_two_courses() -> None:
    report = validate_note(make_note(courses=("Course_SEN0401", "Course_XXX9999")))
    assert report.conforms is False
    assert "np:course" in paths(report)


def test_rejects_malformed_hash() -> None:
    report = validate_note(make_note(note_hash="ABC"))
    assert report.conforms is False
    assert paths(report) == ["np:noteHash"]


def test_reports_every_problem_at_once() -> None:
    report = validate_note(make_note(note_hash=None, courses=(), topics=(), tags_confirmed=False))
    assert report.conforms is False
    assert set(paths(report)) == {"np:noteHash", "np:course", "np:topic", "np:tagsConfirmed"}


# -- boş grafik ve genel davranış ---------------------------------------------------------------------

def test_empty_graph_does_not_silently_conform() -> None:
    report = validate_note(rdflib.Graph())
    assert report.conforms is False
    assert report.violations and report.violations[0].message


def test_graph_without_note_type_does_not_conform() -> None:
    g = make_note()
    g.remove((NOTE, RDF.type, NP.Note))
    assert validate_note(g).conforms is False


def test_validate_does_not_modify_the_input_graph() -> None:
    g = make_note(topics=("Topic_QuantumMoney",))
    before = set(g)
    validate_note(g)
    assert set(g) == before


def test_every_violation_message_is_non_empty_turkish_text() -> None:
    report = validate_note(make_note(note_hash=None, courses=(), topics=(), tags_confirmed=False))
    for violation in report.violations:
        assert violation.message.strip()
        assert not violation.message.startswith("Value ") and "does not" not in violation.message


def test_report_and_violation_are_frozen() -> None:
    violation = Violation("NoteShape", "np:topic", "Konu sözlükte yok.")
    with pytest.raises(dataclasses.FrozenInstanceError):
        violation.message = "x"  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        Report(conforms=True, violations=[]).conforms = False  # type: ignore[misc]
