# NOTEPROOF-FILE
# module:   copywarn
# owner:    emine           second: aleyna
# story:    S6
# contract: 02#5.4 CopyChecker, RegisteredNote, CopyWarning
# depends:  -
# status:   stable
"""CopyChecker: yeni bir notu önceki notlarla karşılaştırır.

Kayıt servisiyle (Arda) sözleşme:
    checker.check(text, author=...)           -> list[CopyWarning]   (adım 4b: yazar onaylamadan önce)
    checker.add(RegisteredNote(...))          -> not kaydedildikten sonra (adım 9)

CopyWarning, proposal'daki class modelinde "CopyWarning links a Note to an
earlier Note with a similarity score" satırının karşılığıdır.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import text as T

# Eşikler testlerle ve değerlendirme setiyle ayarlanır (evalset/run_copywarn.py).
# NP-DECISION(K-002): karakter 5-gram kosinüs + kelime 3-shingle containment, eşik 0.60.
# Eşik gerçek veriyle EMN-3'te ayarlanır.
DEFAULT_THRESHOLD = 0.60
# Containment ölçüsü, kısa metinlerde yanıltıcı olmasın diye en az bu kadar shingle ister.
MIN_SHINGLES = 15


# NP-CONTRACT(02#5.4): alan adları ve sırası sabit; kayıt servisi (Arda) bu sınıfla not ekler.
@dataclass(frozen=True)
class RegisteredNote:
    """Arşivde kayıtlı bir not (karşılaştırma için gereken kadarı)."""

    note_id: str  # notun SHA-256 hash'i (hex) ya da IRI'si
    text: str
    author: str  # takma adlı öğrenci hesabı (gerçek isim değil — KVKK)
    registered_at: str  # ISO 8601, kayıt zamanı
    proof: str = ""  # önceki notun proof sayfası linki (varsa)


# NP-CONTRACT(02#5.4): alan adları sabit; önizleme yanıtındaki copyWarnings bunlardan üretilir (02#7).
@dataclass(frozen=True)
class CopyWarning:
    earlier_note_id: str
    earlier_author: str
    earlier_registered_at: str
    earlier_proof: str
    score: float  # 0..1, en yüksek ölçünün değeri
    method: str  # "char-cosine" ya da "shingle-containment"


@dataclass
class _Indexed:
    note: RegisteredNote
    vec: dict[str, float]
    sh: set = field(default_factory=set)


# NP-CONTRACT(02#5.4): CopyChecker(threshold=0.60) kurucusu sabit.
class CopyChecker:
    def __init__(self, threshold: float = DEFAULT_THRESHOLD):
        self.threshold = threshold
        self._notes: list[_Indexed] = []

    def __len__(self) -> int:
        return len(self._notes)

    # NP-CONTRACT(02#5.4): imza sabit. Aktivite modeli adım 9'dan sonra çağrılır.
    def add(self, note: RegisteredNote) -> None:
        """Kaydedilmiş bir notu karşılaştırma havuzuna ekle."""
        self._notes.append(_Indexed(note, T.tf_vector(T.char_ngrams(note.text)), T.shingles(note.text)))

    def score(self, a: str, b: str) -> tuple[float, str]:
        """İki metnin benzerlik skoru ve skoru veren ölçü."""
        return self._score(T.tf_vector(T.char_ngrams(a)), T.shingles(a), T.tf_vector(T.char_ngrams(b)), T.shingles(b))

    @staticmethod
    def _score(va, sa, vb, sb) -> tuple[float, str]:
        best, method = T.cosine(va, vb), "char-cosine"
        # Biri ötekinin bir parçasını içeriyorsa (yarısı kopyalanmış not, ya da önceki not + ekler).
        for part, whole in ((sa, sb), (sb, sa)):
            if len(part) >= MIN_SHINGLES:
                c = T.containment(part, whole)
                if c > best:
                    best, method = c, "shingle-containment"
        return best, method

    # NP-CONTRACT(02#5.4): imza sabit. Aktivite modeli adım 4b; aynı hesabın notu kopya sayılmaz.
    def check(self, text: str, author: str | None = None, before: str | None = None) -> list[CopyWarning]:
        """Yeni notun metnine benzeyen önceki notlar, en benzer olan önce.

        author: yeni notu yükleyen hesap; aynı hesabın notları atlanır (revizyon, kopya değil).
        before: yalnızca bu zamandan ÖNCE kaydedilmiş notlarla karşılaştır (ISO 8601).
                Verilmezse havuzdaki bütün notlar "önceki" sayılır.
        """
        v, sh = T.tf_vector(T.char_ngrams(text)), T.shingles(text)
        out = []
        for ix in self._notes:
            n = ix.note
            if author is not None and n.author == author:
                continue
            if before is not None and not n.registered_at < before:
                continue
            s, m = self._score(v, sh, ix.vec, ix.sh)
            if s >= self.threshold:
                out.append(CopyWarning(n.note_id, n.author, n.registered_at, n.proof, round(s, 4), m))
        out.sort(key=lambda w: (-w.score, w.earlier_registered_at))
        return out
