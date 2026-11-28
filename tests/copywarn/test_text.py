# NOTEPROOF-FILE
# module:   copywarn
# owner:    emine           second: aleyna
# story:    S6
# contract: -
# depends:  -
# status:   stable
"""copywarn/text.py testleri: normalleştirme ve ölçüler."""

from copywarn import text as T


def test_normalize_folds_turkish_and_punctuation():
    assert T.normalize("İşlem ÜCRETİ, ağaç; Şeker!") == "islem ucreti agac seker"
    assert T.normalize("IŞIK ılık") == "isik ilik"


def test_normalize_is_equal_for_ascii_folded_copy():
    assert T.normalize("Çocuk işlem ücreti öder") == T.normalize("Cocuk islem ucreti oder")


def test_cosine_identical_and_disjoint():
    v = T.tf_vector(T.char_ngrams("merkle agaci ve kok"))
    assert abs(T.cosine(v, v) - 1.0) < 1e-9
    assert T.cosine(v, T.tf_vector(T.char_ngrams("zzzzzz qqqqqq"))) == 0.0


def test_containment():
    a = T.shingles("bir iki uc dort bes alti")
    b = T.shingles("bir iki uc dort bes alti yedi sekiz")
    assert T.containment(a, b) == 1.0
    assert 0 < T.containment(b, a) < 1


def test_empty_text_is_safe():
    assert T.char_ngrams("") == {} or not T.char_ngrams("")
    assert T.shingles("") == set()
    assert T.tf_vector(T.char_ngrams("")) == {}
