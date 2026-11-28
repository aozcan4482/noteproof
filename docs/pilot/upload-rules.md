# Yükleme kuralları

Görev: AYS-2 · Sahip: aysu · İnceleyen: emine · Kural seti sürüm 2.3 · Karar: K-006

**Durum: öğrencilerle teyit edildi (27 Kasım 2026).** 8 öğrenciden 6'sı "yalnızca kendi notu" kuralına,
dosya türleri ve boyut sorusunda 4'ü mevcut sınırlara katıldı. Kurallar K-006'daki hâliyle geçerlidir.
Öğrencilerin değişiklik istekleri (bölüm 6) Arda'ya iletildi; kabul edilen olursa K-006 ve bu sayfa
birlikte güncellenir.

## 1. Neler yüklenir

| Kural | Ayrıntı |
| --- | --- |
| Yalnızca **kendi** ders notun | Kendi elinle ya da bilgisayarında yazdığın not |
| Dosya türleri | PDF, JPEG, PNG, düz metin (`.txt`), Markdown (`.md`). Word dosyanı PDF olarak kaydedip yükle |
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

| | |
| --- | --- |
| Kime soruldu | 8 öğrenci: 3'ü 3. sınıf, 5'i 4. sınıf. Ekip üyesi yok |
| Nasıl | Aysu tarafından yüz yüze ya da tek tek, 27 Kasım 2026. Dört soru |
| Kayıt | Yalnızca toplu sayılar ve isimsiz ifadeler. İsimler alınmadı |

| Soru | Katılıyor | Katılmıyor / değişiklik istiyor | Belirsiz |
| --- | --- | --- | --- |
| 1. Yalnızca kendi notun yüklenir | 6 | 1 — arkadaşının notunu ve hocanın sınıfta verdiği etkinlikleri de yüklemek istiyor | 1 — "notum yok" dedi |
| 2. PDF, JPEG, PNG, metin; en çok 10 MB yeterli mi | 4 | 3 — ikisi Word (`.docx`) istiyor; biri 10 MB yerine 25 MB istiyor | 1 — "No" dedi, anlamı netleşmedi |
| 3. Bildirilen notun arşivden silinmesi | 6 | 1 — bildirim yerine yazarın kendisinin silebileceği bir düğme istiyor | 1 — "fark etmez" |

4. soru (eklemek istediğin kural), her biri bir öğrenciden:

- Ek kural yok (3 öğrenci).
- "Notlarım kamuya açıktır."
- Notlara isim etiketi eklensin.
- Bir etiketleme sistemi olsun.
- Ses kaydı da yüklenebilsin.
- Ders kodu zorunlu olsun.

## 6. İstekler ve yanıtları

| İstek | Yanıt | Kime |
| --- | --- | --- |
| Arkadaşının notunu yüklemek | Kapsam dışı (`01` bölüm 5). Notu arkadaşı kendisi yükler; kanıt da doğru kişiye ait olur | — |
| Hocanın sınıfta verdiği etkinlikler | Kapsam dışı (`01` bölüm 5). Öğrencinin o etkinliğe kendi yazdığı çözüm ya da not yüklenebilir | — |
| Word (`.docx`) desteği (2 öğrenci) | Şimdilik PDF olarak kaydedip yükleme. Yeni dosya türü sözleşme değişikliğidir (`02` bölüm 7, metin çıkarma: Aleyna) | Arda |
| 25 MB sınırı (1 öğrenci) | K-006 değişikliği | Arda |
| Yazarın kendi notunu silebileceği düğme (1 öğrenci) | Şu an kaldırma bildirimle yapılıyor (ARD-8). Öneri olarak iletildi | Arda |
| Ses kaydı (1 öğrenci) | Kabul edilen türler arasında yok; K-006 değişikliği | Arda |
| İsim etiketi (1 öğrenci) | Gerçek isim saklanmaz (K-007). Not zaten yazarın takma adıyla görünür | — |
| Etiketleme sistemi (1 öğrenci) | Var: AI dersi ve konuları önerir, yazar onaylar (S3) | — |
| Ders kodu zorunlu (1 öğrenci) | Var: her notun tam bir dersi olmak zorunda (shape kuralı) | — |

Teyit tarihi: 27 Kasım 2026
