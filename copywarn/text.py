# NOTEPROOF-FILE
# module:   copywarn
# owner:    emine           second: aleyna
# story:    S6
# contract: -
# depends:  -
# status:   stable
"""Metin normalleştirme ve karşılaştırma özellikleri.

Kopyalar çoğu zaman birebir aynı dosya değildir (aynı dosya zaten aynı SHA-256'yı
verir ve kayıt servisinde yakalanır). Tipik kopyalar:
  * fotoğraftan OCR ile çıkarılmış, harf hataları olan metin
  * Türkçe karakterleri silinmiş metin (ç->c, ş->s ...)
  * cümle/paragraf sırası değiştirilmiş metin
  * birkaç cümlesi silinmiş ya da başına sonuna ek yapılmış metin

Bu yüzden iki ölçü kullanılır:
  * karakter n-gram vektörlerinin kosinüs benzerliği -> harf hatalarına ve sıra değişimine dayanıklı
  * kelime shingle "containment" oranı -> notun bir kısmı kopyalanmışsa yakalar
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

# Türkçe harfleri ASCII'ye indir: bir kopyada "ş" yerine "s" yazılması benzerliği düşürmesin.
_TR_FOLD = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a", "î": "i", "û": "u"})
_NON_WORD = re.compile(r"[^0-9a-z]+")

# NP-DECISION(K-002): yöntem ve uzunluklar bu karara dayanır.
# Değişirse EMN-3 ölçümü yeniden yapılır.
CHAR_N = 5  # karakter n-gram uzunluğu
SHINGLE_K = 3  # kelime shingle uzunluğu


def normalize(text: str) -> str:
    """Küçük harf, Türkçe harfleri ASCII'ye indir, noktalama ve fazla boşlukları at."""
    # Türkçe "İ" ve "I" doğru küçülsün diye önce elle çevir.
    text = text.replace("İ", "i").replace("I", "ı").lower()
    text = text.translate(_TR_FOLD)
    # Kalan aksanları (é, ä ...) ayır ve at.
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return _NON_WORD.sub(" ", text).strip()


def words(text: str) -> list[str]:
    return normalize(text).split()


def char_ngrams(text: str, n: int = CHAR_N) -> Counter:
    """Normalleştirilmiş metnin karakter n-gram sayıları (kelime sınırları tek boşluk)."""
    s = " " + " ".join(words(text)) + " "
    if len(s) < n:
        return Counter([s]) if s.strip() else Counter()
    return Counter(s[i : i + n] for i in range(len(s) - n + 1))


def shingles(text: str, k: int = SHINGLE_K) -> set[tuple[str, ...]]:
    """Ardışık k kelimelik grupların kümesi."""
    w = words(text)
    if len(w) < k:
        return {tuple(w)} if w else set()
    return {tuple(w[i : i + k]) for i in range(len(w) - k + 1)}


def tf_vector(counts: Counter) -> dict[str, float]:
    """Sublinear tf (1 + log) ile L2-normalleştirilmiş vektör."""
    v = {g: 1.0 + math.log(c) for g, c in counts.items()}
    norm = math.sqrt(sum(x * x for x in v.values()))
    return {g: x / norm for g, x in v.items()} if norm else {}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    """Normalleştirilmiş iki vektörün kosinüs benzerliği."""
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(g, 0.0) for g, x in a.items())


def containment(part: set, whole: set) -> float:
    """`part` kümesinin ne kadarı `whole` içinde? (0..1)"""
    if not part:
        return 0.0
    return len(part & whole) / len(part)
