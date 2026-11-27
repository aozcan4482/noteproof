# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3
# depends:  -
# status:   wip
"""Metin çıkarma: yüklenen not dosyasından AI tagger'ın okuyacağı düz metni çıkarır.

Proposal'daki aktivite modelinde adım 4a.

Kayıt servisi (Arda) önizlemede bu fonksiyonu çağırır; çıkan metin `tagger.suggest.suggest`'e ve kopya
uyarısına (Emine) gider. Fonksiyon hiçbir şey kaydetmez ve not içeriğini günlüğe yazmaz.

Yolların dayanağı ALY-R1 ölçümüdür (docs/analysis/aleyna-text-extraction.md, 26 Kasım 2026):

- Dijital PDF'te pypdf yeterli (CER 0,004). Ama "fi" gibi bağlı harfler tek karakter (U+FB01) olarak
  geliyor; bu yüzden her çıktı Unicode NFKC'ye çevrilir. NFKC Türkçe harfleri (İ, ı, ş, ğ...) değiştirmez.
- Taranmış PDF'te metin katmanı yok; pypdf sayfadaki resmi verir ve Tesseract onu okur. Aynı el yazısı
  sayfada en iyi sonuç buydu (CER 0,441). Yeni bağımlılık gerekmez.
- Telefon fotoğrafı yatay kaydedilir; EXIF yönü uygulanmazsa okuma çöker (CER 0,81–0,94). iPhone JPEG'i
  Pillow'da MPO olarak açılır ve pytesseract MPO'yu reddeder; EXIF düzeltmesinin döndürdüğü kopya bu
  sorunu da giderir. Resim ayrıca RGB'ye çevrilir.
- `tur` dil verisi olmadan Türkçe harflerin hiçbiri okunmadı; dil her zaman `tur+eng`.
- Basit ön işleme (gri ton, kontrast, küçültme) işe yaramadı; yapılmaz.
- El yazısı fotoğrafta Tesseract zayıf (CER 0,59–0,77): öneri çoğu zaman zayıf ya da boş olur ve yazar
  dersi ve konuyu listeden seçer. Bu beklenen bir sonuçtur, hata değildir.
"""

from __future__ import annotations

import io
import unicodedata

# NP-CONTRACT(02#5.3): kabul edilen türler sabittir; K-006 (yükleme sınırları) ile aynıdır.
SUPPORTED_MEDIA_TYPES = ("application/pdf", "image/jpeg", "image/png", "text/plain", "text/markdown")

OCR_LANG = "tur+eng"  # ALY-R1: yalnızca `eng` ile Türkçe harflerin hiçbiri okunmadı.

# NP-TODO(burak): pypdf, pytesseract ve Pillow pyproject.toml'da yok (BRK-1, `tagger` grubu).
# Bu yüzden içe aktarmalar fonksiyonların içinde: paket kurulmamışsa metin dosyaları yine çalışır,
# PDF ve resimler ise açık bir ImportError verir.


# NP-CONTRACT(02#5.3): imza sabit. Desteklenmeyen tür -> ValueError; metin çıkmazsa boş string.
def extract_text(data: bytes, media_type: str) -> str:
    """Not dosyasının baytlarından düz metni çıkarır.

    media_type büyük/küçük harf ve ";" sonrası parametreler ("text/plain; charset=utf-8") yok sayılarak
    okunur. Bozuk ya da okunamayan dosya ValueError verir; okunan ama metni olmayan dosya "" döner.
    """
    kind = (media_type or "").split(";", 1)[0].strip().lower()
    if kind not in SUPPORTED_MEDIA_TYPES:
        allowed = ", ".join(SUPPORTED_MEDIA_TYPES)
        raise ValueError(f"Desteklenmeyen dosya türü: '{media_type}'. Kabul edilenler: {allowed}.")

    if kind in ("text/plain", "text/markdown"):
        text = _from_text(data)
    elif kind == "application/pdf":
        text = _from_pdf(data)
    else:
        text = _ocr(_open_image(data))
    return _normalize(text)


def _normalize(text: str) -> str:
    """NFKC: PDF'teki bağlı harfleri ("ﬁ" -> "fi") ve benzeri biçim karakterlerini sadeleştirir."""
    text = unicodedata.normalize("NFKC", text)
    return text.strip()


def _from_text(data: bytes) -> str:
    try:
        return data.decode("utf-8-sig")  # -sig: Windows'un eklediği BOM karakterini atar
    except UnicodeDecodeError as err:
        raise ValueError("Metin dosyası UTF-8 değil; dosyayı UTF-8 olarak kaydedip yeniden yükleyin.") from err


def _from_pdf(data: bytes) -> str:
    import pypdf
    from PIL import Image

    try:
        reader = pypdf.PdfReader(io.BytesIO(data))
        pages = list(reader.pages)
    except Exception as err:  # pypdf bozuk dosyada farklı hata türleri verebiliyor
        raise ValueError("PDF dosyası okunamadı.") from err

    parts: list[str] = []
    for page in pages:
        text = page.extract_text() or ""
        if text.strip():
            parts.append(text)
            continue
        # Metin katmanı yok (taranmış sayfa): sayfadaki resimleri OCR ile oku (ALY-R1, bulgu 2).
        for image in page.images:
            parts.append(_ocr(Image.open(io.BytesIO(image.data))))
    return "\n".join(p for p in parts if p.strip())


def _open_image(data: bytes):
    from PIL import Image, UnidentifiedImageError

    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError) as err:
        raise ValueError("Resim dosyası okunamadı.") from err
    return image


def _ocr(image) -> str:
    import pytesseract
    from PIL import ImageOps

    # Önce EXIF yönü: telefon fotoğrafı yatay kaydedilir. exif_transpose yeni bir kopya döndürdüğü için
    # resmin "MPO" biçim bilgisi de düşer ve pytesseract onu reddetmez (ALY-R1 bulgu 4).
    # Sonra RGB: saydam ya da paletli PNG'lerin Tesseract'a hep aynı biçimde gitmesi için.
    upright = ImageOps.exif_transpose(image).convert("RGB")
    try:
        return pytesseract.image_to_string(upright, lang=OCR_LANG)
    except pytesseract.TesseractNotFoundError as err:
        raise RuntimeError(
            "Tesseract kurulu değil ya da PATH'te yok. Kurulum: uyeler/aleyna.md bölüm 3 (tur ve eng dil verisiyle)."
        ) from err
