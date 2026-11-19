"""NoteProof — kopya uyarısı (copywarn/).

Proposal'daki "Copy warning and evaluation set" modülü (E3, story S6):
yeni yüklenen bir notun metni, daha önce kaydedilmiş notlarla karşılaştırılır;
benzerlik eşiği geçilirse not "possible copy" olarak işaretlenir ve önceki
notun proof'una bağlanır (proposal aktivite modeli A, adım 4b ve 8).

  text.py     -> metni normalleştirir (Türkçe harfler, OCR gürültüsü, noktalama)
                 ve karşılaştırma özelliklerini çıkarır (karakter n-gram, kelime shingle)
  checker.py  -> CopyChecker: önceki notları tutar, yeni notu karşılaştırır,
                 CopyWarning listesi döner

Kurallar:
  * Uyarı yalnızca DAHA ÖNCE kaydedilmiş notlara verilir (kim önce kaydettiyse o "önceki not").
  * Aynı hesabın kendi notu kopya sayılmaz; o bir revizyondur (prov:wasRevisionOf).
  * Sistem karar vermez, yalnızca kanıt gösterir (proposal: exclusions).

Paket yalnızca Python standart kütüphanesini kullanır. Sentence-embedding
karşılaştırması ileride `Similarity` arayüzüyle eklenebilir (checker.py).
"""

from .checker import CopyChecker, CopyWarning, RegisteredNote

__all__ = ["CopyChecker", "CopyWarning", "RegisteredNote"]
