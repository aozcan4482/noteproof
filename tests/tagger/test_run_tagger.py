# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#3, 02#5.3
# depends:  evalset.run_tagger
# status:   stable
"""evalset/run_tagger.py testleri (ALY-5), sentetik notlar ve FakeLLM ile. Ağa çıkılmaz, anahtar gerekmez.

Gerçek ölçüm Emine'nin değerlendirme setinde (evalset/notes, manifest.csv) API anahtarıyla çalışır.
"""

from __future__ import annotations

import json
from dataclasses import asdict

import pytest

from evalset import run_tagger
from evalset.data import EvalNote
from ontology.vocab import Vocabulary
from tagger.llm import ENV_API_KEY

from .fake_llm import FakeLLM


def note(nid: str, *topics: str) -> EvalNote:
    return EvalNote(nid, "Course_SEN0401", topics, "yazar-01", "2026-11-28T10:00:00", f"{nid} sentetik not metni")


def answer(*topics: str, course: str = "Course_SEN0401") -> str:
    return json.dumps({"course": course, "topics": list(topics), "summary": "Bir. İki."})


@pytest.fixture(scope="module")
def vocab() -> Vocabulary:
    return Vocabulary.load()


def test_precision_is_correct_suggested_topics_over_all_suggested_topics(vocab):
    notes = [note("n1", "Topic_TransactionFees"), note("n2", "Topic_FeeRate"), note("n3", "Topic_Blockchain")]
    llm = FakeLLM(
        answer("Topic_TransactionFees", "Topic_FeeRate"),  # 1 doğru, 1 yanlış
        answer("Topic_FeeRate"),  # doğru
        answer("Topic_Blockchain"),  # doğru
    )
    r = run_tagger.evaluate(notes, vocab, llm)
    assert (r.suggested, r.correct, r.precision) == (4, 3, 0.75)
    assert not r.passed  # 0.75 < 0.80
    assert r.course_correct == 3
    assert r.per_note[0]["correct"] == ["Topic_TransactionFees"]


def test_reaching_the_target_passes(vocab):
    notes = [note(f"n{i}", "Topic_FeeRate") for i in range(5)]
    r = run_tagger.evaluate(notes, vocab, FakeLLM(*[answer("Topic_FeeRate")] * 4, answer("Topic_Blockchain")))
    assert r.precision == 0.8 and r.passed


def test_ids_outside_the_vocabulary_are_filtered_before_counting(vocab):
    # Model sözlükte olmayan bir kimlik uydurursa suggest onu süzer; ölçüye yanlış öneri olarak girmez.
    r = run_tagger.evaluate([note("n1", "Topic_FeeRate")], vocab, FakeLLM(answer("Topic_FeeRate", "Topic_Uydurma")))
    assert (r.suggested, r.correct) == (1, 1)


def test_note_without_any_topic_is_listed_and_nothing_suggested_fails(vocab):
    r = run_tagger.evaluate([note("n1", "Topic_FeeRate")], vocab, FakeLLM("bozuk yanıt"))
    assert r.no_topic == ["n1"] and r.suggested == 0 and not r.passed


class FailingLLM:
    def complete(self, prompt, *, system=None):
        raise RuntimeError("Dil modelinin istek sınırı aşıldı (HTTP 429)")


def test_a_failed_call_is_recorded_and_the_run_does_not_pass(vocab):
    r = run_tagger.evaluate([note("n1", "Topic_FeeRate")], vocab, FailingLLM())
    assert r.errors == [{"note": "n1", "error": "Dil modelinin istek sınırı aşıldı (HTTP 429)"}]
    assert not r.passed


def test_calls_are_spaced_by_the_delay(vocab):
    waits = []
    notes = [note(f"n{i}", "Topic_FeeRate") for i in range(3)]
    run_tagger.evaluate(notes, vocab, FakeLLM(answer("Topic_FeeRate")), delay=2.5, sleep=waits.append)
    assert waits == [2.5, 2.5]  # ilk çağrıdan önce beklenmez


def test_report_never_contains_note_text_or_summary(vocab):
    r = run_tagger.evaluate([note("n1", "Topic_FeeRate")], vocab, FakeLLM(answer("Topic_FeeRate")))
    dumped = json.dumps(asdict(r), ensure_ascii=False)
    assert "sentetik not metni" not in dumped and "Bir. İki." not in dumped


def write_set(root, rows):
    (root / "notes").mkdir(parents=True)
    lines = ["id,course,topics,author,registered_at"]
    for nid, topic in rows:
        lines.append(f"{nid},Course_SEN0401,{topic},yazar-01,2026-11-28T10:00:00")
        (root / "notes" / f"{nid}.txt").write_text("sentetik", encoding="utf-8")
    (root / "manifest.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_main_empty_set_is_a_clear_failure(tmp_path, capsys):
    assert run_tagger.main(["--root", str(tmp_path)]) == 1
    assert "boş" in capsys.readouterr().out


def test_main_without_api_key_is_skipped_with_a_notice(tmp_path, capsys, monkeypatch):
    write_set(tmp_path, [("n1", "Topic_FeeRate")])
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    assert run_tagger.main(["--root", str(tmp_path)]) == 0
    assert "atlandı" in capsys.readouterr().out


def test_main_runs_and_writes_the_json_report(tmp_path, capsys, monkeypatch):
    write_set(tmp_path, [("n1", "Topic_FeeRate"), ("n2", "Topic_Blockchain")])
    monkeypatch.setenv(ENV_API_KEY, "test-anahtari")
    monkeypatch.setattr(run_tagger, "client_from_env", lambda: FakeLLM(answer("Topic_FeeRate")))
    out = tmp_path / "rapor.json"
    code = run_tagger.main(["--root", str(tmp_path), "--json", str(out), "--delay", "0"])
    report = json.loads(out.read_text(encoding="utf-8"))
    assert code == 1 and report["precision"] == 0.5  # n2'de yanlış öneri
    assert "test-anahtari" not in capsys.readouterr().out
