# NOTEPROOF-FILE
# module:   evalset
# owner:    emine           second: aleyna
# story:    S3, S6
# contract: 02#3 manifest.csv'de yerel kavram kimlikleri, 02#5.2 Vocabulary
# depends:  ontology.vocab.Vocabulary
# status:   stable
"""Gerçek değerlendirme setinin (evalset/notes/ + manifest.csv) kurallara uyduğunu denetler (EMN-2).

Kabul ölçütü: her `topics` değeri Eylem'in sözlüğünde (`Vocabulary.is_topic`) var olmalı; hiçbir dosyada isim
ya da numara olmamalı; yazar her zaman takma addır. Bu testler sözlük dosyasını (ontology/courses.ttl) okuduğu
için rdflib ister; rdflib kurulu değilse sözlük testleri atlanır (genel CI `.[dev,all]` ile kurar).
"""

from __future__ import annotations

import re
from datetime import datetime

import pytest

from evalset.data import ROOT, load_notes

NOTES = load_notes(ROOT)
ROWS = [pytest.param(n, id=n.id) for n in NOTES]

# Takma ad biçimi evalset/README.md'deki kuraldır; gerçek isim ve eşleşme tablosu hiçbir dosyada tutulmaz.
PSEUDONYM = re.compile(r"^yazar-\d{2}$")
# Kişisel veri işaretleri: e-posta, 9 ve daha uzun rakam dizisi (öğrenci no, telefon), okul e-posta alanı.
PERSONAL = [
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    re.compile(r"(?<!\d)\d{9,}(?!\d)"),
    re.compile(r"stu\.iku", re.IGNORECASE),
    re.compile(r"\+90[\s\d]{6,}"),
]


@pytest.fixture(scope="module")
def vocab():
    pytest.importorskip("rdflib", reason="sözlük okuyucu rdflib ister (ontology grubu)")
    from ontology.vocab import Vocabulary

    return Vocabulary.load()


def test_manifest_ids_are_unique_and_every_row_has_its_file():
    ids = [n.id for n in NOTES]
    assert len(ids) == len(set(ids)), "manifest.csv'de tekrar eden id var"
    # load_notes dosyayı okuyamazsa zaten hata verir; burada boş dosya kalmadığını da denetle.
    assert all(n.text.strip() for n in NOTES)


def test_no_note_file_is_left_outside_the_manifest():
    listed = {n.id for n in NOTES}
    on_disk = {p.stem for p in (ROOT / "notes").glob("*.txt")}
    assert on_disk == listed, f"manifest'te olmayan dosyalar: {sorted(on_disk - listed)}"


@pytest.mark.parametrize("note", ROWS)
def test_s6_author_is_a_pseudonym_and_date_is_iso(note):
    assert PSEUDONYM.match(note.author), f"{note.id}: yazar takma ad değil: {note.author!r}"
    datetime.fromisoformat(note.registered_at)


@pytest.mark.parametrize("note", ROWS)
def test_note_text_has_no_personal_data(note):
    for pattern in PERSONAL:
        assert not pattern.search(note.text), f"{note.id}: kişisel veri olabilir ({pattern.pattern})"


@pytest.mark.parametrize("note", ROWS)
def test_s3_course_and_topics_come_from_the_vocabulary(note, vocab):
    assert vocab.is_course(note.course), f"{note.id}: sözlükte olmayan ders {note.course}"
    assert note.topics, f"{note.id}: konu yok"
    allowed = {t.id for t in vocab.topics(note.course)}
    for topic in note.topics:
        assert vocab.is_topic(topic), f"{note.id}: sözlükte olmayan konu {topic}"
        assert topic in allowed, f"{note.id}: {topic} {note.course} dersinin konusu değil"
