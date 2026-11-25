# Ekran taslakları: arama, not kartı, yükleme, proof

Görev: ERD-R1 · Sahip: erdener · İnceleyen: aysu · Kural seti sürüm 2.0

Bu belge NoteProof arayüzünün dört ekranını 360 piksel genişlikte (telefon) metin tel kafes olarak
gösterir ve her ekranda hangi API alanının nerede göründüğünü eşler. ERD-1'deki iskelet
(`web/index.html`, `web/upload.html`, `web/proof.html`) bu taslaklardan yazılır.

Kaynak sözleşmeler: `02_MIMARI_SOZLESMELER.md` bölüm 6 (proof dosyası) ve bölüm 7 (HTTP API).
Taslaklarda geçen her alan adı bu iki bölümde vardır; yeni alan eklenmemiştir.

## Ortak kurallar

- Genişlik 360 piksel, tek sütun. Tel kafeslerde bir satır yaklaşık 34 karakterdir.
- Bütün metinler Türkçe. Ders ve konu adları `GET /api/vocabulary` yanıtındaki `labelTr` alanından
  gelir; ekranda kimlik (`Topic_FeeRate`) gösterilmez, yalnızca etiket.
- Yazar olarak yalnızca takma ad (`author`) görünür. Hiçbir ekranda gerçek isim ya da öğrenci
  numarası isteyen alan yoktur.
- Proof rozetinin üç hâli vardır: **Beklemede** (`proofStatus: "pending"`), **Kanıtlandı**
  (`proofStatus: "proven"`), **Değiştirilmiş** (yalnızca proof sayfasında, dosya proof ile eşleşmezse).
- Kopya için metin her zaman **"Olası kopya"**dır ve önceki notun proof sayfasına bağlanır. Hüküm
  bildiren ifade ("kopyalanmış", "intihal") kullanılmaz.
- Tarihler `registeredAt` ve `blockTime` alanlarından gelir (ISO 8601, UTC); ekranda yerel saate
  çevrilip `24 Kas 2026, 14:05` biçiminde gösterilir.
- Hata metinleri API'nin `error.code` alanına göre arayüzde üretilir; `error.message` ekrana basılmaz.

## 1. Arama sayfası (`web/index.html`)

Kullanıcı: Note reader, telefonda. Story: S5 (alt konular dahil arama), S6 (olası kopya bağlantısı).

```
+----------------------------------+
| NoteProof                 [Yükle]|
+----------------------------------+
| Ders                             |
| [ SEN 401 Blockchain        v ]  |
| Konu                             |
| [ İşlemler                  v ]  |
|   (alt konular da aranır)        |
| [ Başlıkta ara...           ]    |
| [          Ara           ]       |
+----------------------------------+
| 3 not bulundu                    |
| +------------------------------+ |
| | İşlem ücretleri ders notu    | |
| | SEN 401 · İşlem ücretleri    | |
| | @kuzgun · 18 Kas 2026        | |
| | [Kanıtlandı]                 | |
| +------------------------------+ |
| +------------------------------+ |
| | Ücret oranı özeti            | |
| | SEN 401 · Ücret oranı        | |
| | @mavi_kalem · 20 Kas 2026    | |
| | [Beklemede]                  | |
| | ! Olası kopya → önceki not   | |
| +------------------------------+ |
| ...                              |
+----------------------------------+
```

Boş sonuç: kart listesi yerine "Bu ders ve konuda kayıtlı not yok." ve süzgeçleri sıfırlayan bir
bağlantı.

| Ekrandaki yer | Kaynak |
| --- | --- |
| Ders seçimi | `GET /api/vocabulary` → `courses[].labelTr`; isteğe `course=<id>` olarak gider |
| Konu seçimi | Seçilen dersin `topics[].labelTr`; alt konular `broader` ile girintili listelenir; isteğe `topic=<id>` |
| Başlıkta ara | `GET /api/search?q=` |
| "3 not bulundu" | `results` dizisinin uzunluğu |
| Kart başlığı | not kartı `title` |
| Ders · konu satırı | `course` ve `topics` (etiketleri sözlükten) |
| Yazar · tarih | `author`, `registeredAt` |
| Rozet | `proofStatus` |
| "Olası kopya" satırı | `possibleCopyOf` boş değilse görünür; `proof.html?hash=<possibleCopyOf>` adresine bağlanır |
| Karta dokunma | 2. ekran (not kartı ayrıntısı), `GET /api/notes/{noteHash}` |

## 2. Proof rozetli not kartı (ayrıntı)

Arama listesinde bir karta dokununca açılır. Aynı sayfada ayrı görünüm (`web/index.html`), ayrı HTML değil.

```
+----------------------------------+
| < Sonuçlar                       |
+----------------------------------+
| İşlem ücretleri ders notu        |
| SEN 401 Blockchain               |
| Konular:                         |
|  (İşlem ücretleri) (Ücret oranı) |
|                                  |
| Özet                             |
| Bu not, işlem ücretlerinin nasıl |
| belirlendiğini ve ücret oranının |
| bloğa girişi nasıl etkilediğini  |
| anlatır.                         |
|                                  |
| Yazar: @kuzgun                   |
| Kayıt: 18 Kas 2026, 14:05        |
| +------------------------------+ |
| | [Kanıtlandı]                 | |
| | Bu dosya 18 Kas 2026'da      | |
| | Bitcoin'e damgalandı.        | |
| | [ Kanıtı kontrol et  > ]     | |
| +------------------------------+ |
| Hash: 3f9a...c21e  [Kopyala]     |
+----------------------------------+
```

Rozet "Beklemede" iken kutudaki metin: "Kayıt alındı. Kanıt, günlük zaman damgasından (23:00) sonra
hazır olur." ve düğme gösterilmez.

| Ekrandaki yer | Kaynak |
| --- | --- |
| Başlık | `title` |
| Ders, konu etiketleri | `course`, `topics` (etiketleri sözlükten) |
| Özet | `summary` |
| Yazar, kayıt zamanı | `author`, `registeredAt` |
| Rozet ve kutu metni | `proofStatus` |
| "Kanıtı kontrol et" | `proof.html?hash=<noteHash>` |
| Hash satırı | `noteHash` (ilk 4 ve son 4 karakter; "Kopyala" tamamını kopyalar) |
| Olası kopya (varsa) | `possibleCopyOf`; 1. ekrandaki satırın aynısı |

## 3. Yükleme sayfası (`web/upload.html`)

Kullanıcı: Note author. Story: S1, S3 (öneri ve onay), S4 (sözlük dışı konu reddi), S6 (kopya uyarısı).
Akış üç adımdır; onaya kadar hiçbir kayıt isteği gitmez (S3).

### 3a. Dosya seçimi

```
+----------------------------------+
| < Arama          Not yükle       |
+----------------------------------+
| Takma ad: @kuzgun  [Değiştir]    |
|                                  |
| +- - - - - - - - - - - - - - - + |
| |                              | |
| |  Dosyayı buraya bırak        | |
| |  ya da [ Dosya seç ]         | |
| |  PDF, JPEG, PNG, metin       | |
| |  En çok 10 MB                | |
| +- - - - - - - - - - - - - - - + |
+----------------------------------+
```

Hesap yoksa bu ekranın yerine yalnızca "Takma ad" kutusu ve "Hesap oluştur" düğmesi görünür.
Takma ad dışında hiçbir şey istenmez.

### 3b. Öneriler ve onay

```
+----------------------------------+
| < Geri           Not yükle       |
+----------------------------------+
| ders-notu-ucretler.pdf           |
| Hash: 3f9a...c21e                |
|                                  |
| ! Olası kopya                    |
|   @mavi_kalem · 11 Kas 2026      |
|   [ Önceki notun kanıtı > ]      |
|                                  |
| Başlık                           |
| [ İşlem ücretleri ders notu  ]   |
| Ders (AI önerisi)                |
| [ SEN 401 Blockchain        v ]  |
| Konular (AI önerisi)             |
|  (İşlem ücretleri x)             |
|  [ + Listeden konu ekle     v ]  |
| Özet (AI önerisi)                |
| [ Bu not, işlem ücretlerinin  ]  |
| [ nasıl belirlendiğini ...    ]  |
|                                  |
| [ ] Etiketleri kontrol ettim     |
| [ Vazgeç ]        [ Kaydet ]     |
+----------------------------------+
```

- AI'ın önerdiği konular çıkarılabilir etiketler (x) olarak gelir. Konu yalnızca sözlük listesinden
  eklenir; serbest metin kutusu yoktur (S4).
- "Kaydet", "Etiketleri kontrol ettim" işaretlenmeden etkin olmaz.
- "Vazgeç" hiçbir istek göndermez ve 3a'ya döner.
- Dosya daha önce kaydedilmişse öneri alanları yerine şu kutu görünür: "Bu dosya 18 Kas 2026'da
  @kuzgun tarafından kaydedildi." ve "Kanıtı gör" bağlantısı.

### 3c. Sonuç

```
+----------------------------------+
| Kaydedildi                       |
| Hash: 3f9a...c21e  [Kopyala]     |
| Kayıt: 24 Kas 2026, 11:40        |
| [Beklemede]                      |
| Kanıt bu gece 23:00'teki zaman   |
| damgasından sonra hazır olur.    |
| [ Notu gör ]  [ Yeni not ]       |
+----------------------------------+
```

İhlal durumu (`422 shape_violation`): 3b ekranı açık kalır, üstte kırmızı kutuda her ihlalin
`violations[].message` metni listelenir ve ilgili alan (ör. `np:topic` için Konular) işaretlenir.
Kullanıcı konuyu listeden seçmeye yönlendirilir: "Konuyu listeden seç."

| Ekrandaki yer | Kaynak |
| --- | --- |
| Takma ad, hesap oluşturma | `POST /api/accounts` `{"pseudonym"}` → `account`, `token` (tarayıcıda saklanır, `X-NoteProof-Token` başlığıyla gider) |
| Dosya bırakma | `POST /api/notes/preview`, `multipart/form-data`, alan `file` |
| Dosya adı | Tarayıcıdaki dosya nesnesi (API'den gelmez) |
| Hash | önizleme `noteHash` |
| "Daha önce kaydedildi" kutusu | `alreadyRegistered.registeredAt`, `.author`, `.proofUrl` |
| Olası kopya şeridi | `copyWarnings[]`: `earlierAuthor`, `earlierRegisteredAt`, `earlierProofUrl` (puan `score` ve `method` gösterilmez) |
| Ders önerisi | `suggestion.course` |
| Konu etiketleri | `suggestion.topics` |
| Konu ekleme listesi | `GET /api/vocabulary` → seçilen dersin `topics[]` |
| Özet | `suggestion.summary` |
| Başlık | Kullanıcı yazar; onay gövdesinde `title` |
| Kaydet | `POST /api/notes` `{previewToken, title, course, topics, summary, confirmed: true}` |
| Sonuç ekranı | `201` yanıtı: `noteHash`, `registeredAt`, `proofStatus` |
| İhlal kutusu | `error.violations[].message`, `.path` |

Hata metinleri (`error.code` → ekrandaki metin):

| `code` | Metin |
| --- | --- |
| `unsupported_type` | "Bu dosya türü desteklenmiyor. PDF, JPEG, PNG ya da metin dosyası yükle." |
| `too_large` | "Dosya 10 MB'tan büyük." |
| `not_confirmed` | "Kaydetmeden önce etiketleri kontrol ettiğini işaretle." |
| `unauthorized` | "Oturumun bulunamadı. Takma adınla yeniden hesap oluştur." |
| `preview_expired` | "Önizlemenin süresi doldu. Dosyayı yeniden yükle." |
| `shape_violation` | İhlal kutusu (yukarıda) |

## 4. Proof sayfası (`web/proof.html`)

Kullanıcı: Note verifier, hesapsız. Story: S7. Arşivin sunucusu kapalıyken de çalışır: proof
dosyası sunucudan (`proof.html?hash=…`) ya da kullanıcının seçtiği yerel bir dosyadan okunur.

### 4a. Giriş

```
+----------------------------------+
| NoteProof · Kanıt kontrolü       |
+----------------------------------+
| 1. Not dosyası                   |
| [ Dosya seç ]  ders-notu.pdf     |
| 2. Kanıt dosyası                 |
| (o) Sunucudan al (3f9a...c21e)   |
| ( ) Bilgisayarımdan seç          |
|     [ Dosya seç ]                |
| [       Kontrol et        ]      |
|                                  |
| Dosyan bu cihazdan çıkmaz; hash  |
| tarayıcıda hesaplanır.           |
+----------------------------------+
```

Sunucuya ulaşılamazsa "Sunucuya ulaşılamadı. Kanıt dosyan varsa bilgisayarından seç." yazar ve
ikinci seçenek seçili gelir. `404 proof_pending` gelirse: "Bu notun kanıtı henüz hazır değil."

### 4b. Sonuç: Kanıtlandı

```
+----------------------------------+
| [Kanıtlandı]                     |
| Bu dosya, aşağıdaki Bitcoin      |
| işleminden önce vardı.           |
+----------------------------------+
| Hash     3f9a...c21e             |
| Ağ       signet                  |
| Blok     #214 392                |
| Zaman    18 Kas 2026, 23:14      |
| İşlem    a71c...09bd  [Aç]       |
|                                  |
| Merkle yolu                      |
|          [ kök e2f0.. ]  ✓ zincir|
|           /        \             |
|     [ 9c1d.. ]   [ 44ab.. ]      |
|      /     \                     |
| [*3f9a..] [ 7be2.. ]             |
| (* senin dosyan)                 |
|                                  |
| Kanıt, dosyanın bu tarihte var   |
| olduğunu ve kimin kaydettiğini   |
| gösterir; notu ilk kimin         |
| yazdığını göstermez.             |
+----------------------------------+
```

### 4c. Sonuç: Değiştirilmiş

```
+----------------------------------+
| [Değiştirilmiş]                  |
| Bu dosya kayıtlı dosya değil.    |
| Hesaplanan hash kanıttaki hash   |
| ile eşleşmiyor.                  |
| Hesaplanan  51e0...aa73          |
| Kanıttaki   3f9a...c21e          |
| [ Başka dosya seç ]              |
+----------------------------------+
```

Zincir kontrolü yapılamazsa (public signet API'ye ulaşılamaz) yerel kontrol sonucu yine gösterilir,
"✓ zincir" yerine "Zincir kontrol edilemedi" yazar.

| Ekrandaki yer | Kaynak |
| --- | --- |
| Not dosyası | Kullanıcının seçtiği dosya; hash `web/js/verify.js` `sha256Hex` ile tarayıcıda |
| Sunucudan kanıt | `GET /api/notes/{hash}/proof` |
| Yerel kanıt | Kullanıcının seçtiği JSON (bölüm 6 biçimi) |
| Hash satırı | proof `noteHash` (4c'de ayrıca hesaplanan hash) |
| Ağ | proof `network` |
| Blok | proof `blockHeight` |
| Zaman | proof `blockTime` |
| İşlem | proof `txid`; "Aç" public signet gezginine gider (adres K-008 ile `config.js`'te) |
| Merkle ağacı | proof `merklePath[]` (`side`, `sibling`) ve `merkleRoot`; yaprak `noteHash` |
| "✓ zincir" | `web/js/chain.js`: `txid`'nin OP_RETURN çıktısında `merkleRoot` var mı |
| Rozet | `verifyProof` sonucu `{ok, reason}`: `ok` → Kanıtlandı, hash eşleşmezse → Değiştirilmiş |
| Dürüstlük notu | Sabit metin (`erdener.md` tasarım notları) |

## Açık sorular

- Konu seçiminde alt konuların girintili gösterimi `broader` alanına dayanıyor. Eylem'in sözlüğü
  gelince derinlik ikiden fazlaysa liste uzayabilir; ERD-1'de sahte sözlükle denenecek.
- İşlemi açan public signet gezgininin adresi K-008'e bağlı (Burak). Karar çıkana kadar "Aç"
  bağlantısı `NP-TODO(burak)` ile bekletilir.
