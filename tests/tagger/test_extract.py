# NOTEPROOF-FILE
# module:   tagger
# owner:    aleyna          second: eylem
# story:    S3
# contract: 02#5.3
# depends:  tagger.extract.extract_text
# status:   wip
"""tagger/extract.py testleri: her dosya türü, desteklenmeyen tür, boş dosya ve ALY-R1 bulguları.

Test verisi sentetiktir: metin, PDF ve resimler test sırasında kodla üretilir; gerçek öğrenci notu yoktur.
OCR testleri Tesseract (tur+eng) ister; kurulu değilse atlanır (bitcoind'siz regtest testleri gibi).
"""

from __future__ import annotations

import io
import shutil

import pytest
from PIL import Image, ImageDraw, ImageFont

from tagger.extract import SUPPORTED_MEDIA_TYPES, extract_text

needs_tesseract = pytest.mark.skipif(shutil.which("tesseract") is None, reason="Tesseract kurulu değil")
WORDS = "MERKLE ROOT HASH"


def text_image(text: str = WORDS) -> Image.Image:
    image = Image.new("RGB", (1200, 200), "white")
    ImageDraw.Draw(image).text((30, 60), text, fill="black", font=ImageFont.load_default(size=56))
    return image


def encode(image: Image.Image, fmt: str, **kw) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format=fmt, **kw)
    return buf.getvalue()


def text_pdf(text: str) -> bytes:
    """Metin katmanı olan tek sayfalık en küçük PDF (Helvetica, ASCII metin)."""
    stream = f"BT /F1 24 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = io.BytesIO(), []
    out.write(b"%PDF-1.4\n")
    for i, body in enumerate(objects, start=1):
        offsets.append(out.tell())
        out.write(f"{i} 0 obj\n".encode() + body + b"\nendobj\n")
    xref = out.tell()
    out.write(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for off in offsets:
        out.write(f"{off:010d} 00000 n \n".encode())
    out.write(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return out.getvalue()


# --- düz metin ve Markdown -------------------------------------------------------------------------------

def test_plain_text_keeps_turkish_letters():
    note = "İŞLEM ÜCRETLERİ\nMadenci, ücret oranı yüksek işlemi seçer: ç ğ ı ö ş ü"
    assert extract_text(note.encode("utf-8"), "text/plain") == note


def test_markdown_and_media_type_parameters_are_accepted():
    data = "﻿# Merkle ağacı\n- kök".encode("utf-8")  # BOM'lu UTF-8 (Windows Not Defteri)
    assert extract_text(data, "Text/Markdown; charset=utf-8") == "# Merkle ağacı\n- kök"


def test_nfkc_splits_ligatures_without_touching_turkish_letters():
    # ALY-R1 bulgu 1: PDF'ten "teklifi" -> "tekliﬁ" geliyordu.
    assert extract_text("tekliﬁ İşlem".encode("utf-8"), "text/plain") == "teklifi İşlem"


def test_text_that_is_not_utf8_is_an_explicit_error():
    with pytest.raises(ValueError):
        extract_text("işlem".encode("cp1254"), "text/plain")


def test_empty_text_file_gives_empty_string():
    assert extract_text(b"  \n\t ", "text/plain") == ""


# --- desteklenmeyen tür ve bozuk dosya -------------------------------------------------------------------

@pytest.mark.parametrize("media_type", ["image/heic", "application/msword", "image/gif", "", "pdf"])
def test_unsupported_media_type_raises_value_error(media_type):
    with pytest.raises(ValueError):
        extract_text(b"anything", media_type)


def test_supported_types_match_the_contract():
    assert set(SUPPORTED_MEDIA_TYPES) == {"application/pdf", "image/jpeg", "image/png", "text/plain", "text/markdown"}


@pytest.mark.parametrize("media_type", ["application/pdf", "image/jpeg", "image/png"])
def test_corrupt_file_raises_value_error(media_type):
    with pytest.raises(ValueError):
        extract_text(b"bu bir dosya degil", media_type)


# --- PDF -------------------------------------------------------------------------------------------------

def test_pdf_with_text_layer_is_read_by_pypdf():
    assert extract_text(text_pdf("Merkle root and fee rate"), "application/pdf") == "Merkle root and fee rate"


def test_pdf_without_text_or_images_gives_empty_string():
    assert extract_text(text_pdf(""), "application/pdf") == ""


@needs_tesseract
def test_scanned_pdf_falls_back_to_ocr_of_the_page_image():
    # ALY-R1 bulgu 2: taranmış PDF'te metin katmanı yok, sayfadaki resim Tesseract'a gider.
    scanned = encode(text_image(), "PDF")
    assert WORDS in extract_text(scanned, "application/pdf").upper()


# --- resimler --------------------------------------------------------------------------------------------

@needs_tesseract
@pytest.mark.parametrize("fmt, media_type", [("PNG", "image/png"), ("JPEG", "image/jpeg")])
def test_image_is_read_with_ocr(fmt, media_type):
    assert WORDS in extract_text(encode(text_image(), fmt), media_type).upper()


@needs_tesseract
def test_phone_photo_exif_rotation_is_applied_before_ocr():
    # ALY-R1 bulgu 3: telefon resmi yatay kaydeder, dikliği EXIF yönünden (6 = 90° döndür) gelir.
    sideways = text_image().rotate(90, expand=True)
    exif = Image.Exif()
    exif[0x0112] = 6
    assert WORDS in extract_text(encode(sideways, "JPEG", exif=exif), "image/jpeg").upper()


@needs_tesseract
def test_iphone_mpo_jpeg_is_converted_before_ocr():
    # ALY-R1 bulgu 4: iPhone JPEG'i Pillow'da MPO (iki kareli) açılıyor; pytesseract MPO'yu reddeder.
    first, second = text_image(), text_image("SECOND FRAME")
    data = encode(first, "MPO", save_all=True, append_images=[second])
    assert Image.open(io.BytesIO(data)).format == "MPO"
    assert WORDS in extract_text(data, "image/jpeg").upper()


@needs_tesseract
def test_blank_image_gives_empty_string():
    assert extract_text(encode(Image.new("RGB", (400, 300), "white"), "PNG"), "image/png") == ""
