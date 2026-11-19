"""copywarn/checker.py testleri: story S6'nın kabul kriteri ve kurallar."""

import random

import pytest

from copywarn import CopyChecker, RegisteredNote
from evalset import plant

from .fixtures import NOTES


def archive(**kw) -> CopyChecker:
    c = CopyChecker(**kw)
    for i, (nid, text) in enumerate(NOTES.items()):
        c.add(RegisteredNote(nid, text, author=f"yazar-{i}", registered_at=f"2026-11-0{1 + i % 9}T10:00:00", proof=f"proof/{nid}"))
    return c


def test_s6_acceptance_nearly_identical_note_is_linked_to_earlier_proof():
    # Given: başka bir öğrencinin bir hafta önce kaydettiği nota neredeyse aynı bir not
    # When: yüklendiğinde  Then: possible copy olarak işaretlenir ve önceki notun proof'una bağlanır
    c = archive()
    nearly = NOTES["merkle"].replace("En üstte", "En tepede").replace("hafif cüzdanlar", "SPV cüzdanları")
    w = c.check(nearly, author="baska-ogrenci", before="2026-11-20T09:00:00")
    assert w, "kopya yakalanmadı"
    assert w[0].earlier_note_id == "merkle"
    assert w[0].earlier_proof == "proof/merkle"
    assert w[0].score >= c.threshold


@pytest.mark.parametrize("name", sorted(plant.TRANSFORMS))
def test_every_planted_transform_is_caught(name):
    c = archive()
    r = random.Random(1)
    fn = plant.TRANSFORMS[name]
    for nid, text in NOTES.items():
        copy = fn(text, r, NOTES["keys"]) if name == "add_own" else fn(text, r)
        w = c.check(copy, author="kopyalayan")
        assert w and w[0].earlier_note_id == nid, f"{name}: {nid} kopyası yakalanmadı ({w[:1]})"


def test_two_original_notes_on_the_same_topic_are_not_copies():
    c = CopyChecker()
    s, _ = c.score(NOTES["fees_a"], NOTES["fees_b"])
    assert s < c.threshold, f"aynı konudaki iki özgün not kopya sayıldı: {s:.2f}"


def test_no_false_alarm_between_any_two_originals():
    c = CopyChecker()
    ids = list(NOTES)
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            s, m = c.score(NOTES[a], NOTES[b])
            assert s < c.threshold, f"{a} ~ {b} = {s:.2f} ({m})"


def test_same_author_is_a_revision_not_a_copy():
    c = archive()
    w = c.check(NOTES["mining"] + " Ek: halving tarihleri.", author="yazar-4")
    assert all(x.earlier_note_id != "mining" for x in w)


def test_only_earlier_notes_are_compared():
    c = archive()
    # "keys" 2026-11-04'te kaydedildi; ondan önceki bir anda kontrol edilen not ona bağlanmamalı.
    assert c.check(NOTES["keys"], author="x", before="2026-11-02T00:00:00") == []
    assert c.check(NOTES["keys"], author="x", before="2026-11-30T00:00:00")[0].earlier_note_id == "keys"


def test_unrelated_new_note_gets_no_warning():
    c = archive()
    text = (
        "Veri tabanında normalizasyon tekrar eden veriyi azaltır. Birinci normal form atomik değerler ister. "
        "İkinci normal form kısmi bağımlılıkları kaldırır. Üçüncü normal form geçişli bağımlılıkları kaldırır. "
        "Fazla normalizasyon sorguları yavaşlatabilir ve join sayısını artırır."
    )
    assert c.check(text, author="x") == []


def test_warnings_are_sorted_by_score():
    c = archive()
    w = c.check(NOTES["fees_a"] + " " + NOTES["fees_b"], author="x", before="2026-12-01T00:00:00")
    assert [x.score for x in w] == sorted((x.score for x in w), reverse=True)
