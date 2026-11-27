# Yükleme kuralları

Görev: AYS-2 · Sahip: aysu · İnceleyen: emine · Kural seti sürüm 2.3 · Karar: K-006

**Durum: taslak, öğrencilerle teyit ediliyor.** Bu sayfadaki kurallar ekibin K-006 kararıdır. Arşivin
sahibi olan 3. ve 4. sınıf öğrencileri teyit edince durum "teyit edildi" olur. Görüşler bölüm 5'e eklenir
ve K-006 kapanır.

## 1. Neler yüklenir

| Kural | Ayrıntı |
| --- | --- |
| Yalnızca **kendi** ders notun | Kendi elinle ya da bilgisayarında yazdığın not |
| Dosya türleri | PDF, JPEG, PNG, düz metin (`.txt`), Markdown (`.md`) |
| En büyük dosya | 10 MB |
| Bir dosya bir not | Birden çok dersin notu tek dosyada olmaz |

## 2. Ne "kendi notu" sayılır

**Sayılır:**

- Derste ya da ders sonrasında kendi yazdığın not; elle yazıp fotoğrafladığın ya da taradığın sayfalar dahil.
- Kendi notunun düzenlenmiş, temize çekilmiş hâli.
- Kendi hazırladığın özet, çalışma kâğıdı, çözdüğün soru notları.

**Sayılmaz:**

- Hocanın slaytları, ders kitabının ya da başka bir kaynağın sayfaları (tarama ya da fotoğraf da olsa).
- Başka bir öğrencinin notu, onun izni olsa bile. O notu sahibi kendisi yükler.
- Sınav soruları ve cevap anahtarları.

## 3. Yükleyince ne olur

- Sistem notun dijital parmak izini (SHA-256 hash) hesaplar ve kaydı takma adınla tutar.
- Her gece 23:00'te o günün notlarının ortak parmak izi Bitcoin signet ağına yazılır. **Zincire notun
  içeriği, adın ya da numaran gitmez;** yalnızca 32 byte'lık bir değer gider.
- Kanıt, notun o tarihte var olduğunu ve kimin kaydettiğini gösterir. **Notu ilk kimin yazdığını göstermez.**
- Yeni not daha önce kaydedilmiş bir nota çok benziyorsa "olası kopya" olarak işaretlenir ve önceki notun
  kanıtına bağlanır. Bu bir hüküm değildir; kararı insanlar verir.
- Kaydedilen not değiştirilemez. Yeni sürümü yeni bir not olarak yüklenir ve eskisine bağlanır.

## 4. Bildirilen not nasıl kaldırılır

1. Bir notun kendisine ait olduğunu düşünen ya da yanlışlıkla yüklendiğini fark eden kişi bunu
   müşteri temsilcisine (Aysu) bildirir. Bildirimde notun bağlantısı ya da hash'i olur; isim gerekmez.
2. Bildirim bir GitHub issue'su olarak kaydedilir (etiket `feedback`). Kişisel bilgi issue'ya yazılmaz.
3. Not arşivden kaldırılır: dosyası, çıkarılan metni ve kayıtları silinir (ARD-8).
4. Zincirdeki 32 byte'lık değer silinemez, ama ondan notun içeriğine geri dönülemez. Kaldırılan notun
   kanıtı artık arşivde gösterilmez.

## 5. Öğrenci görüşleri

<!-- Gruplardan gelen yanıtların özeti buraya. Yalnızca toplu sayılar ve anonim alıntılar; isim yok. -->

| Soru | Yanıt veren | Özet |
| --- | --- | --- |
| Dosya türleri ve 10 MB yeterli mi | | |
| "Kendi notu" tanımına katılıyor musun | | |
| Kaldırma yolu uygun mu | | |
| Eklemek istediğin kural | | |

Teyit tarihi: —
