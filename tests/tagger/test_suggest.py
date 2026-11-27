# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3
# depends:  tagger.suggest.suggest
# status:   wip
"""tagger/suggest.py testleri: story S3'ün kabul kriteri ve tagger'ın üç sınırı.

Testler dil modeli yerine FakeLLM, Eylem'in sözlüğü yerine NP-STUB sahte sözlük kullanır.
"""

from __future__ import annotations

import json
import os

import pytest

from tagger.suggest import TagSuggestion, suggest

from .fake_llm import FakeLLM
from .fake_vocab import Vocabulary

FEE_NOTE = (
    "İŞLEM ÜCRETLERİ\n"
    "1. Bloğa hangi işlemin gireceğini o bloğu üreten madenci seçer.\n"
    "2. Ücret, girdilerin toplamı ile çıktıların toplamı arasındaki farktır.\n"
    "3. Madenci ücreti işlemin boyutuna böler; en yüksek ücret oranını (sat/vB) seçer.\n"
)


def answer(course=None, topics=(), summary="") -> str:
    return json.dumps({"course": course, "topics": list(topics), "summary": summary}, ensure_ascii=False)


@pytest.fixture
def vocab() -> Vocabulary:
    return Vocabulary.load()


def test_s3_acceptance_transaction_fee_note_suggests_sen0401_and_transaction_fees(vocab):
    # Given: transaction fee hakkında bir not  When: yüklendiğinde
    # Then: AI, SEN0401 dersini ve sözlükten "Transaction fees" konusunu önerir
    llm = FakeLLM(
        answer(
            "Course_SEN0401",
            ["Topic_TransactionFees"],
            "İşlem ücreti girdiler ile çıktılar arasındaki farktır. "
            "Madenciler ücret oranı yüksek işlemleri seçer.",
        )
    )
    s = suggest(FEE_NOTE, vocab, llm)
    assert s.course == "Course_SEN0401"
    assert s.topics == ["Topic_TransactionFees"]
    assert s.summary.startswith("İşlem ücreti")


def test_s3_prompt_carries_vocabulary_ids_labels_and_the_note(vocab):
    # İstem sözlükten üretilir (elle yazılmış liste yok): her kimlik ve iki dildeki etiketi istemde olmalı.
    llm = FakeLLM(answer())
    suggest(FEE_NOTE, vocab, llm)
    prompt, system = llm.calls[0]
    for course in vocab.courses():
        for c in [course, *vocab.topics(course.id)]:
            assert c.id in prompt and c.label_tr in prompt and c.label_en in prompt
    assert FEE_NOTE.strip() in prompt
    assert system and "JSON" in system


def test_s3_ids_not_in_vocabulary_never_reach_the_output(vocab):
    # Model sözlükte olmayan bir konu uydurursa çıktıya giremez (02#5.3). Tekrarlar da bir kez kalır.
    llm = FakeLLM(answer("Course_SEN0401", ["Topic_Uydurma", "Topic_FeeRate", "Topic_FeeRate", 42, None]))
    s = suggest(FEE_NOTE, vocab, llm)
    assert s.topics == ["Topic_FeeRate"]
    assert all(vocab.is_topic(t) for t in s.topics)


def test_s3_unknown_course_gives_no_course_and_no_topics(vocab):
    # Model sözlükte olmayan bir ders döndürürse ders None, konu boş: yazar listeden kendisi seçer.
    for bad_course in ["Course_UYDURMA", "Topic_TransactionFees", None, 7]:
        s = suggest(FEE_NOTE, vocab, FakeLLM(answer(bad_course, ["Topic_TransactionFees"], "Özet.")))
        assert s.course is None
        assert s.topics == []


@pytest.mark.parametrize(
    "broken",
    [
        "Bu notun dersi SEN0401.",  # JSON yok
        '{"course": "Course_SEN0401", "topics": [',  # yarım JSON
        '["Course_SEN0401"]',  # nesne değil liste
        '{"course": "Course_SEN0401", "topics": "Topic_TransactionFees"}',  # topics liste değil
        "",
    ],
)
def test_s3_broken_model_answer_gives_empty_suggestion_not_an_error(vocab, broken):
    s = suggest(FEE_NOTE, vocab, FakeLLM(broken))
    assert isinstance(s, TagSuggestion)
    assert s.topics == []
    assert s.course in (None, "Course_SEN0401")


def test_s3_json_wrapped_in_a_code_block_is_still_read(vocab):
    wrapped = "İşte yanıt:\n```json\n" + answer("Course_SEN0401", ["Topic_TransactionFees"], "Özet.") + "\n```"
    s = suggest(FEE_NOTE, vocab, FakeLLM(wrapped))
    assert (s.course, s.topics) == ("Course_SEN0401", ["Topic_TransactionFees"])


def test_s3_suggest_saves_nothing(vocab, tmp_path, monkeypatch):
    # "Yazar onaylayana kadar hiçbir şey kaydedilmez": suggest çalışırken hiçbir dosya oluşmamalı.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("NOTEPROOF_DATA_DIR", str(tmp_path / "data"))
    s = suggest(FEE_NOTE, vocab, FakeLLM(answer("Course_SEN0401", ["Topic_TransactionFees"], "Özet.")))
    assert s.course == "Course_SEN0401"
    assert os.listdir(tmp_path) == []
    with pytest.raises(AttributeError):
        s.course = "Course_BASKA"  # öneri değiştirilemez; onaylanan hâli kayıt servisi ayrı kurar


def test_empty_note_text_is_an_explicit_error(vocab):
    with pytest.raises(ValueError):
        suggest("   \n", vocab, FakeLLM(answer()))


def test_empty_vocabulary_is_an_explicit_error():
    with pytest.raises(ValueError):
        suggest(FEE_NOTE, Vocabulary([]), FakeLLM(answer()))
