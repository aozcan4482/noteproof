# NOTEPROOF-FILE
# module:   evalset
# owner:    emine           second: aleyna
# story:    S6
# contract: -
# depends:  copywarn.CopyChecker.check
# status:   stable
"""Değerlendirme hattının (plant -> evaluate) uçtan uca testi, sentetik notlarla.

Gerçek 60 notluk set evalset/ altına eklendiğinde CI aynı hattı
`python -m evalset.run_copywarn` ile gerçek veride çalıştırır.
"""

from evalset import plant, run_copywarn
from evalset.data import EvalNote, load_notes, load_planted, write_planted

from .fixtures import NOTES


def synthetic_notes() -> list[EvalNote]:
    return [
        EvalNote(nid, "SEN0401", ("Topic_X",), f"yazar-{i % 3}", f"2026-11-{1 + i:02d}T10:00:00", text)
        for i, (nid, text) in enumerate(NOTES.items())
    ]


def test_plant_is_reproducible_and_sound():
    notes = synthetic_notes()
    a, b = plant.plant(notes), plant.plant(notes)
    assert a == b
    assert len(a) == plant.N_COPIES
    by_id = {n.id: n for n in notes}
    for c in a:
        src = by_id[c.source_id]
        assert c.author != src.author, "kopyalayan, kaynağın yazarı olmamalı"
        assert c.registered_at > src.registered_at, "kopya kaynaktan sonra kaydedilmeli"
        assert c.text != src.text
    assert {c.transform for c in a} == set(plant.TRANSFORMS)


def test_evaluation_meets_the_90_percent_target_on_synthetic_notes():
    notes = synthetic_notes()
    r = run_copywarn.evaluate(notes, plant.plant(notes))
    assert r.copies == 20
    assert r.recall >= run_copywarn.TARGET_RECALL, r.missed
    assert r.passed
    assert r.false_positives == []


def test_planted_files_roundtrip(tmp_path):
    notes = synthetic_notes()
    copies = plant.plant(notes)
    write_planted(copies, tmp_path)
    assert load_planted(tmp_path) == copies


def test_empty_evalset_fails_loudly(tmp_path, capsys):
    # Boş set "%0 hata" diye sessizce geçmemeli (ScenarioKind: Absent).
    assert load_notes(tmp_path) == []
    assert run_copywarn.main(["--root", str(tmp_path)]) == 1
    assert "boş" in capsys.readouterr().out
