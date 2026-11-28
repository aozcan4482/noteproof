# Metin çıkarma karşılaştırması: pypdf ve Tesseract

Görev: ALY-R1 · Sahip: aleyna · İnceleyen: eylem, emine · Kural seti sürüm 2.0

Bu belge, AI tagger'ın (adım 4a) notun metnini nasıl çıkaracağına karar vermek için yapılan ölçümü anlatır:
kendi notlarımdan 3 fotoğraf ve 3 PDF üzerinde pypdf ve Tesseract (`tur+eng`) ne kadar metin çıkarıyor,
Türkçe harfler ve el yazısı ne oluyor. Sonuçtaki karar, ALY-3'teki `tagger.extract.extract_text`'in
nasıl yazılacağını belirler (bölüm 5).

Notların içeriği bu belgede yoktur; yalnızca sayılar vardır. Not dosyaları ve doğru metinler repoya girmez.

## 1. Örnekler

Notlar 26 Kasım 2026'da bu ölçüm için yazıldı. Konular SEN0401'den: işlem ücretleri, Merkle ağacı ve iş
ispatı. Maddeler, Mastering Bitcoin 3. baskının 9, 11 ve 12. bölümlerinden seçilen cümlelerin elle yazılmış
Türkçe özetleridir. Bu sayfalar yalnızca bu ölçüm içindir; değerlendirme setine (EMN-2) verilmez.
Her sayfa 7–8 Türkçe madde içerir; Merkle sayfasında
ayrıca elle çizilmiş, kutularında yazı olan 4 yapraklı bir ağaç vardır.

| Dosya | Tür | Nasıl üretildi | Doğru metin |
| --- | --- | --- | --- |
| foto1.jpg | El yazısı fotoğraf | Spiralli çizgili defter, iPhone kamerası, "En Uyumlu" biçim | 559 karakter |
| foto2.jpg | El yazısı fotoğraf (çizimli) | Aynı | 525 karakter |
| foto3.jpg | El yazısı fotoğraf | Aynı | 392 karakter |
| tarama3.pdf | Taranmış PDF | foto3 ile aynı sayfa; iOS Notlar "Belgeleri Tara", macOS Notlar'dan PDF olarak dışa aktarıldı | 392 karakter |
| dijital1.pdf | Bilgisayarda yazılmış PDF | foto1'in metni bilgisayara yazılıp PDF'e basıldı | 559 karakter |
| dijital2.pdf | Bilgisayarda yazılmış PDF | foto2'nin metni (çizimdeki yazılar dahil) | 525 karakter |

Doğru metin: her sayfanın bilgisayara yazılmış hâli; yazar kâğıtla satır satır karşılaştırıp onayladı.
Sayfa 3'ün doğru metni yalnızca ölçüm için yazıldı, PDF'i yapılmadı.

Dosyalar hakkında ölçüm sırasında görülenler:

- Fotoğraflar 4032×3024 piksel ve **yatay** kaydedilmiş; dik görünmeleri EXIF yön bilgisinden (değer 6, 90° döndür) geliyor.
- Pillow, iPhone JPEG'lerini **MPO** (iki kareli JPEG) olarak açıyor; pytesseract bu biçimi
  `TypeError: Unsupported image format/type` ile reddediyor. Resmi önce RGB'ye çevirmek gerekiyor.
- tarama3.pdf'te **metin katmanı yok**; sayfada yalnızca bir PNG resim var (1536×1917 piksel).

## 2. Yöntem

- Araçlar: Python 3.12.10, pypdf 7.1.1, Tesseract 5.5.4 (`tessdata_fast` dil verisi: `tur`, `eng`),
  pytesseract 0.3.13, Pillow 13.0.0, macOS 26.4.
- PDF'lerde `PdfReader(...).pages[i].extract_text()`. Taranmış PDF'te ayrıca `page.images` ile sayfadaki
  resim çıkarılıp Tesseract'a verildi.
- Fotoğraflarda Tesseract üç biçimde: EXIF yönü uygulanmadan (`tur+eng`), uygulanarak yalnızca `eng`,
  uygulanarak `tur+eng`. Ek olarak basit ön işleme (gri ton, otomatik kontrast, 2000 piksel genişliğe
  küçültme, medyan filtre) denendi.
- Ölçüler (boşluklar tek boşluğa indirgenip Unicode NFC'ye çevrildikten sonra):
  - **CER**: karakter hata oranı = Levenshtein mesafesi / doğru metnin uzunluğu. 0 kusursuz.
  - **WER**: kelime hata oranı. Tesseract'ın uydurduğu fazladan kelimeler yüzünden 1'i geçebilir.
  - **Türkçe harf**: doğru metindeki ç, ğ, ı, İ, ö, ş, ü (büyük ve küçük) harflerinden, hizalamada
    doğru eşlenenlerin sayısı.
  - **Konu kelimesi**: tagger için asıl önemli olan ölçü. Doğru metinde geçen konu kelimelerinden
    (madenci, işlem, ücret, teklif, blok, merkle, ağaç, hash, yaprak, düğüm, kök, sha256, nonce, hedef,
    dakika, bit, satoshi, vbyte) çıktıda da geçenlerin sayısı. Kaba bir ölçüdür (alt dize araması).
- Ölçüm betiği notları okuduğu için repo dışında çalıştırıldı; adımlar yukarıdakilerdir.

## 3. Dosya başına sonuçlar

| Dosya | Yöntem | Çıkan / doğru karakter | CER | WER | Türkçe harf | Konu kelimesi | Süre |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dijital1.pdf | pypdf | 558 / 559 | 0,004 | 0,014 | 42/42 | 7/7 | 0,01 sn |
| dijital2.pdf | pypdf | 524 / 525 | 0,004 | 0,015 | 53/53 | 9/9 | 0,01 sn |
| tarama3.pdf | pypdf `extract_text` | 0 / 392 | 1,000 | 1,000 | 0/31 | 0/8 | 0,00 sn |
| tarama3.pdf | pypdf `page.images` → Tesseract `tur+eng` | 408 / 392 | **0,441** | 1,412 | 16/31 | 4/8 | 1,5 sn |
| foto1.jpg | Tesseract `tur+eng`, EXIF yok | 379 / 559 | 0,809 | 1,563 | 0/42 | — | 3,1 sn |
| foto1.jpg | Tesseract `eng`, EXIF uygulandı | 172 / 559 | 0,785 | 0,972 | 0/42 | — | 1,8 sn |
| foto1.jpg | Tesseract `tur+eng`, EXIF uygulandı | 171 / 559 | 0,758 | 0,930 | 6/42 | 2/7 | 2,1 sn |
| foto2.jpg | Tesseract `tur+eng`, EXIF yok | 119 / 525 | 0,909 | 0,985 | 0/53 | — | 2,2 sn |
| foto2.jpg | Tesseract `eng`, EXIF uygulandı | 450 / 525 | 0,802 | 2,074 | 0/53 | — | 2,3 sn |
| foto2.jpg | Tesseract `tur+eng`, EXIF uygulandı | 430 / 525 | 0,768 | 2,000 | 6/53 | 3/9 | 2,9 sn |
| foto3.jpg | Tesseract `tur+eng`, EXIF yok | 59 / 392 | 0,944 | 1,000 | 0/31 | — | 2,3 sn |
| foto3.jpg | Tesseract `eng`, EXIF uygulandı | 393 / 392 | 0,643 | 1,745 | 0/31 | — | 2,4 sn |
| foto3.jpg | Tesseract `tur+eng`, EXIF uygulandı | 371 / 392 | 0,587 | 1,667 | 7/31 | 3/8 | 3,0 sn |

Basit ön işlemenin etkisi (`tur+eng`, EXIF uygulandı):

| Dosya | CER önce → sonra | Türkçe harf önce → sonra | Konu kelimesi önce → sonra |
| --- | --- | --- | --- |
| foto1.jpg | 0,758 → 0,758 | 6 → 6 | 2/7 → 3/7 |
| foto2.jpg | 0,768 → 0,800 | 6 → 4 | 3/9 → 4/9 |
| foto3.jpg | 0,587 → 0,717 | 7 → 4 | 3/8 → 2/8 |
| tarama3.pdf | 0,441 → 0,469 | 16 → 11 | 4/8 → 4/8 |

## 4. Bulgular

1. **Dijital PDF'te pypdf yeterli.** CER 0,004; Türkçe harflerin ve konu kelimelerinin hepsi doğru,
   OCR'a gerek yok. Tek fark: "fi" harf çifti PDF'te tek bir bağlı harf (U+FB01 "ﬁ") olarak duruyor ve
   pypdf onu öyle döndürüyor ("teklifi" → "tekliﬁ", "Kriptografik" → "Kriptograﬁk"). Böyle kelimeler
   aramada, kopya karşılaştırmasında ve istemde eşleşmeyebilir. Unicode NFKC dönüşümü bunu "fi"ye çevirir.
2. **Taranmış PDF'te pypdf tek başına hiçbir şey vermez**, ama sayfadaki resmi çıkarabilir. O resim
   Tesseract'a verilince el yazısında en iyi sonuç alınır (CER 0,441). Yeni bir kütüphane gerekmez.
3. **Fotoğrafta EXIF yönü uygulanmazsa okuma çöker** (CER 0,81–0,94; Türkçe harf 0). Telefon fotoğrafları
   yatay kaydediliyor; yön bilgisi okunmadan Tesseract yan yatmış metne bakıyor.
4. **iPhone JPEG'i RGB'ye çevrilmeden Tesseract'a verilemez** (MPO biçimi hatası). Bu adım atlanırsa
   iPhone'dan yüklenen her fotoğraf hata verir.
5. **`tur` dil verisi şart.** Yalnızca `eng` ile 126 Türkçe harfin hiçbiri okunmadı; `tur+eng` ile 19'u
   okundu. Az ama sıfır değil; ayrıca CER her fotoğrafta `tur+eng` ile daha düşük.
6. **El yazısı fotoğrafta Tesseract zayıf.** CER 0,59–0,77; Türkçe harflerin %15'i, konu kelimelerinin
   yaklaşık üçte biri doğru çıkıyor. Taranmış hâli aynı sayfada belirgin olarak daha iyi (0,587 → 0,441):
   kenar kırpma, düzleştirme ve kontrast, tarama uygulamasında zaten yapılıyor.
7. **Basit ön işleme işe yaramadı**: dört dosyanın hiçbirinde CER iyileşmedi, üçünde kötüleşti. Eklenmemeli.
8. Süre sorun değil: fotoğraf başına 2–3 saniye, PDF'te milisaniyeler. ALY-7'deki "önizleme 10 saniyeyi
   geçmesin" sınırının içinde.

## 5. Karar: `extract_text` böyle yazılacak (ALY-3)

| `media_type` | Yol |
| --- | --- |
| `application/pdf` | Her sayfada pypdf `extract_text`. Sayfanın metni boşsa sayfadaki resimler (`page.images`) Tesseract `tur+eng` ile okunur |
| `image/jpeg`, `image/png` | Pillow ile aç → `ImageOps.exif_transpose` → `convert("RGB")` → Tesseract `tur+eng` |
| `text/plain`, `text/markdown` | UTF-8 olarak çöz |
| Diğer | `ValueError` (02#5.3) |

- Dil her zaman `tur+eng`. Ön işleme yok.
- Çıkan metin her yolda Unicode NFKC'ye çevrilir (`unicodedata.normalize("NFKC", ...)`): PDF'teki "ﬁ"
  gibi bağlı harfler ayrılır; Türkçe harfler (İ, ı, ş, ğ…) bu dönüşümde değişmez.
- Hiç metin çıkmazsa boş string döner (02#5.3); `suggest` boş metinde açık hata verir ve kayıt servisi
  bunu yazara "metin okunamadı" olarak göstermelidir (PR #10'daki `NP-TODO(arda)`).
- Beklenti: el yazısı fotoğraflarda öneri çoğu zaman zayıf ya da boş olacak; yazar ders ve konuyu listeden
  kendisi seçer. Sözleşme bunu zaten öngörür (ders bulunamazsa `course` `None`).
- Yeni bağımlılık yok: pypdf, pytesseract ve Pillow, uyeler/aleyna.md bölüm 3'teki listede.

## 6. Açık konular (karar başkasında)

- **Görüntüyü okuyabilen bir dil modeli** el yazısında Tesseract'tan çok daha iyi olabilir. Bu, not
  resminin sağlayıcıya gönderilmesi demektir (gizlilik ve maliyet); K-005 kararında ölçüt olarak ele
  alınmalı. Kodda değişiklik gerekirse sözleşme prosedürü (02 bölüm 9) uygulanır. Bu belgede önerilmez,
  yalnızca not edilir.
- **HEIC:** iPhone'un varsayılan "Yüksek Verimlilik" ayarı fotoğrafı HEIC olarak kaydeder; K-006 ve
  02 bölüm 7 yalnızca JPEG ve PNG kabul eder. Tarayıcının yükleme sırasında JPEG'e çevirip çevirmediği
  denenmedi. Yükleme kuralları (Aysu, K-006) ve kayıt servisinin hata mesajı (Arda) için bildirilir.

## 7. Sınırlılıklar

Üç sayfa, tek yazar, tek telefon, tek ışık ortamı ve tek defter türü. Sayılar karar için yön gösterir;
genel bir doğruluk oranı değildir. Gerçek oran, ALY-5/ALY-6'da 60 notluk değerlendirme setiyle ve pilotta
görülecek.
