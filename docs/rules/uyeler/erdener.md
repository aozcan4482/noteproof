# Üye dosyası — Erdener Çimen (`erdener`)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **Erdener'in** rolünü, kapsamını, kurulumunu ve görevlerini tanımlamak.
Yalnızca Erdener ile çalışan araç bu dosyayı uygular.

## 1. Roller

| | |
| --- | --- |
| İdari roller | Process facilitator: haftalık toplantıyı ve ritmi yürütür, engelleri kaldırır. Documentation lead: proposal, raporlar ve toplantı notlarının eksiksiz ve zamanında olmasını sağlar |
| Geliştirme rolleri | Front-end developer, Interaction designer |
| Lider olduğu process | P13 Maintenance |
| Sahip olduğu özellik | **Search and proof pages** (E3; story S5 ve S7; deliverable D7, D9, D10; S1, S3, S4, S6'nın arayüzü) |
| İkincisi | Aysu Akdüzen (senin PR'larını kullanıcı gözüyle inceler) |
| Planlanan iş payı | %14 |

## 2. Kapsam

**Senin klasörlerin:** `web/`, `search/`, `tests/web/`, `tests/search/`, `README.md`, `docs/guide/`,
`docs/minutes/`, `docs/analysis/erdener-*.md`, `docs/worklog/erdener.md`, `AGENTS.md`, `docs/rules/` (kural seti, K-010).

**Dokunmayacakların:** diğer bütün klasörler. API'yi (`register/`) Arda yazar; sen `02` bölüm 7'deki
biçime göre kullanırsın. Merkle kurallarını (`anchor/`) Burak belirler; sen tarayıcıda aynısını uygularsın.

Üç sayfa ve bir arama servisi yazıyorsun:

| Sayfa | Dosya | Kullanıcı | Ne yapar |
| --- | --- | --- | --- |
| Arama | `web/index.html` | Note reader (telefonda) | Ders ve konu süzgeçleri, not kartları: başlık, yazar (takma ad), tarih, proof rozeti, varsa "olası kopya" bağlantısı |
| Yükleme | `web/upload.html` | Note author | Dosya bırakma alanı; AI önerileri çıkarılabilir etiketler olarak; konu yalnızca sözlük listesinden eklenir; benzer önceki not uyarısı; onay |
| Proof | `web/proof.html` | Note verifier (hesapsız) | Dosya + proof → hash'i yeniden hesaplar, Merkle path'i yürür ve küçük bir ağaç olarak çizer, txid ve blok zamanını gösterir |

Proof sayfasının en önemli gereği (S7): **arşivin sunucusu kapalıyken de çalışır.** Bu yüzden sayfa, proof'u
sunucudan alabildiği gibi kullanıcının seçtiği yerel bir proof dosyasından da okuyabilmeli ve hiçbir dış
kütüphaneye bağlı olmamalıdır.

## 3. Ek kurulum

`06_KURULUM.md` tamamlandıktan sonra:

1. **Node.js LTS** (yalnızca tarayıcı kodunun testleri için; derleme adımı yok): `https://nodejs.org`.
   Kontrol: `node --version` → v20 ya da üstü.
2. **Sayfaları yerelde açmak** (API hazır olmadan): repo kökünde `python -m http.server 5500 --directory web`,
   tarayıcıda `http://localhost:5500`. ES modülleri dosyaya çift tıklayarak açıldığında çalışmaz; her zaman bu sunucuyla aç.
3. **Telefon görünümü:** tarayıcının geliştirici araçlarında (F12) cihaz modu, 360 piksel genişlik.
   Gerçek telefonda denemek için bilgisayar ve telefon aynı ağdayken `http://<bilgisayarın-IP'si>:5500`.
4. Python paketleri (`search/` için RDFLib ve pyoxigraph) `pip install -e ".[dev,all]"` ile gelir.
5. `.env`: yalnızca `NOTEPROOF_DATA_DIR=./data`.

## 4. Görevler

### 4.1 Önce: proposal'da yapılmış görünen işler

Proposal'ın work log'unda aşağıdaki işler yapılmış olarak kayıtlı, ama repoda hiçbirinin çıktısı ya da
kanıtı yok. Bu işler **yapılmamış sayılır** ve modül görevlerinden önce, sıfırdan yapılır. Eski kayda
dayanarak "bu zaten var" deme; çıktı `main`'de değilse yoktur (`05_PIPELINE.md` bölüm 1.1).

| No | Görev | Çıktı ve kabul ölçütü | Eski kayıt | Bitiş |
| --- | --- | --- | --- | --- |
| ERD-R1 | Ekran taslakları: arama sayfası ve proof rozetli not kartı; ayrıca yükleme ve proof sayfaları. 360 piksel genişlik için | `docs/analysis/erdener-ui-sketches.md`: dört taslak (çizim görseli ya da metin tel kafes), her ekranda hangi API alanının nerede göründüğü. ERD-1 bu taslaklardan yazılır; Aysu inceledi | #11 | 22 Kas |
| ERD-R2 | `README.md`: proje özeti, modüller ve sahipleri, nasıl kurulur ve çalıştırılır (kısa); kural setinin repoda olmadığı, ekipten alınacağı notu | Repo kökünde `README.md` var (şu an yok); ERD-7 bunu genişletir | #12 | 22 Kas |

Bu görevler de diğerleri gibi branch → PR → `main` yolundan geçer ve commit'lerinde `Task: ERD-R1 (done)`
biçiminde izlenir. Work log'a iki kayıt girilir (`04_GIT_AKISI.md` bölüm 9.1): yapılan iş için kanıtlı bir **Work** kaydı
ve tablodaki "Eski kayıt" numarasını gösteren bir **Correction** kaydı.

### 4.2 Modül görevleri

| No | Görev | Kabul ölçütü | Bağımlılık | Bitiş |
| --- | --- | --- | --- | --- |
| ERD-0 | `TestBranch`'i yayımla ve `main`'e PR aç. Kural setini ekibe zip olarak dağıt (herkese ortak dosyalar + kendi üye dosyası) ve "önce `AGENTS.md`'yi aracınıza okutun" duyurusunu yap | Yedi üye de dosyaları aldığını teyit etti; PR açık, reviewer Burak ve Arda | — | 21 Kas |
| ERD-1 | Arayüz iskeleti: `web/index.html`, `upload.html`, `proof.html`, `web/css/app.css`, `web/js/config.js` (API tabanı, public signet API adresi, sahte veri anahtarı), `web/js/api.js` (bütün `fetch` çağrıları burada), `web/mock/*.json` (`02` bölüm 7'deki yanıtların örnekleri) | Üç sayfa 360 pikselde düzgün; sahte veriyle arama listesi ve yükleme önizlemesi görünüyor; bütün metinler Türkçe | ERD-R1 | 23 Kas |
| ERD-2 | `web/js/verify.js`: `sha256Hex(bytes)`, `verifyProof(fileBytes, proof)` → `{ok, reason}`. WebCrypto ile; yaprak `SHA256(0x00 ‖ hash)`, iç düğüm `SHA256(0x01 ‖ sol ‖ sağ)`; `side` `left` ise kardeş solda | Repo kökünde `node --test` Burak'ın `tests/vectors/merkle_vectors.json` dosyasındaki bütün vektörlerde Python ile aynı sonucu veriyor; örnek not + örnek proof doğrulanıyor; tek karakteri değişen not reddediliyor | BRK-3 | 24 Kas |
| ERD-3 | Proof sayfası: bağlantıdan (`proof.html?hash=…`) ya da yerel proof dosyasından okuma; dosya seçimi; çevrimdışı kontrol; Merkle path'in ağaç çizimi; zincir kontrolü (`web/js/chain.js`: txid'nin OP_RETURN çıktısında kök var mı, blok zamanı) | Senaryo 1: geçerli dosya → "Kanıtlandı" + hash, path, txid, blok zamanı. Senaryo 2: değişmiş dosya → "Bu dosya kayıtlı dosya değil". API kapalıyken yerel proof dosyasıyla çalışıyor (S7) | ERD-2, BRK-6 (K-008) | 25 Kas |
| ERD-4 | Yükleme sayfası: `POST /api/notes/preview` → öneriler; etiket çıkarma ve sözlük listesinden ekleme (`GET /api/vocabulary`); kopya uyarısı şeridi ve önceki notun proof'una bağlantı; onay → `POST /api/notes`; ihlallerin gösterimi; takma adlı hesap oluşturma ve token'ın tarayıcıda saklanması | S3: onaya kadar hiçbir kayıt isteği gitmiyor. S4: `shape_violation` gelince ihlal mesajları görünüyor, kullanıcı listeden seçmeye yönleniyor. Serbest metinle konu yazılamıyor | ERD-1, ARD-3, ARD-4 (önce `web/mock/` ile) | 26 Kas |
| ERD-5 | Arama: `search/queries/notes.rq` (konu ve bütün alt konuları: `skos:narrower*`), `search/service.py` (`search_notes`, `NoteCard`), `search/router.py` (`GET /api/search`); arama sayfasının gerçek API'ye bağlanması | S5 kabul testi (`tests/search/`): `Topic_TransactionFees` ve `Topic_FeeRate` etiketli iki not, `Course_SEN0401` içinde `Topic_Transactions` aranınca yazar ve tarihleriyle listeleniyor | ARD-0, EYL-3, EYL-4 | 27 Kas |
| ERD-6 | Hız ve kullanılabilirlik (D10): arama sonucu ve proof kontrolü telefonda 3 saniyenin altında; klavyeyle kullanılabilirlik, kontrast, hata durumları, boş sonuç ekranı | Ölçüm (ağ kısıtlı cihaz modunda) `docs/reports/` için Emine'ye verilir; Aysu'nun deneme oturumu geri bildirimleri kapatılmış | ARD-7, AYS-5 | 2 Ara |
| ERD-7 | Belgeler: `README.md` (proje ne, nasıl kurulur, nasıl çalıştırılır, nasıl test edilir), `docs/guide/kullanim.md` (üç kullanıcı için adım adım, ekran görüntüleriyle) | Yeni bir kişi yalnızca README ile uygulamayı yerelde açabiliyor; kılavuz pilotta gönüllülere veriliyor | Faz 2 | 4 Ara |
| ERD-8 | (Vakit kalırsa) Arama yanıtları (D7'nin ikinci yarısı): `search/answer.py` — model yalnızca grafiğin döndürdüğü notları ifade eder ve her cümlede nota atıf yapar; modele `tagger.llm.client_from_env` ile ulaşılır | Yanıtta grafikten gelmeyen bilgi yok; model kapalıyken arama yanıtsız ama çalışır | ERD-5, ALY-2 | 4 Ara |

**Tasarım notları (aracın uyacağı):**

- Çerçeve, paketleyici, CDN yok (K-003). Her sayfa tek HTML + ortak CSS + ES modülleri.
- Bütün ağ çağrıları `web/js/api.js` ve `web/js/chain.js` içindedir; adresler `web/js/config.js`'tedir.
- Rozet metinleri: Beklemede, Kanıtlandı, Değiştirilmiş. Kopya için metin her zaman "Olası kopya"dır ve
  önceki notun proof'una bağlanır; hüküm bildiren ifade kullanılmaz.
- Yazar olarak yalnızca takma ad gösterilir. Sayfalarda gerçek isim ya da öğrenci numarası isteyen alan olmaz.
- Proof sayfası, proposal'ın dürüstlük sınırını kullanıcıya söyler: kanıt, dosyanın o tarihte var olduğunu
  ve kimin kaydettiğini gösterir; notu ilk kimin yazdığını göstermez.
- Hata mesajları API'nin `code` alanına göre arayüzde Türkçe üretilir; API'nin `message` alanı ekrana basılmaz.
- SPARQL sorguları `.rq` dosyalarındadır; kullanıcı girdisi sorguya metin olarak eklenmez, parametre olarak bağlanır.
- `search_notes` yalnızca okur; grafiğe yazmaz.

## 5. Başkalarına sağladıkların

| Kime | Ne | Ne zaman |
| --- | --- | --- |
| Arda | `search.router` (uygulamaya bağlanmak üzere) | 27 Kas |
| Aysu | Denenebilir sayfalar (önce sahte veriyle, sonra gerçek) | 23 Kas, 27 Kas |
| Emine | Hız ölçümleri | 2 Ara |
| Herkes | Kural seti, README, toplantı notları | sürekli |

## 6. Başkalarından beklediklerin

| Kimden | Ne | Hazır değilse |
| --- | --- | --- |
| Burak | `tests/vectors/`; public signet API adresi (K-008) | ERD-2'yi `02` bölüm 5.5'teki kurallara göre yaz, kendi küçük vektörünle dene; zincir kontrolünü `NP-TODO(burak)` ile beklet |
| Arda | `/api` uç noktaları | `web/mock/*.json` (`config.js`'te sahte veri anahtarı açık) |
| Eylem | Konu kimlikleri ve `Vocabulary` | Sahte sözlük JSON'u; arama testinde birkaç kavramlık `NP-STUB` grafik |

## 7. İdari görevler

- **Process facilitator.** Her pazartesi haftalık toplantı: gündem (geçen haftanın faz kapısı, engeller, bu
  haftanın görevleri) bir gün önce paylaşılır; notlar `docs/minutes/YYYY-MM-DD.md`'ye aynı gün yazılır
  (katılanlar, kararlar, kim neyi ne zamana kadar yapacak). Çarşamba: bağımlılık bekleyen var mı diye sor;
  bekleyeni ve bekleteni buluştur.
- **Documentation lead.** Kural setinin bakımı sende: sözleşme ya da karar değişince ilgili dosyayı
  bir `docs/rules-...` PR'ıyla güncelle, `AGENTS.md`'deki sürümü ve her dosyanın başındaki sürüm satırını
  artır; merge edilince ekip grubuna duyur (`04` bölüm 6). Final için gereken belgelerin
  (test raporu, değerlendirme raporu, pilot sonuçları, lessons learned) sahiplerinden zamanında geldiğini izle.
- **Maintenance lideri (P13):** pilot sırasında çıkan arayüz hatalarının düzeltilmesi.
- Değerlendirme seti için en az 9 kendi notunu Emine'ye ver.

## 8. Work log için tipik process'ler

P05 (ekran ve akış tasarımı), P07 (arayüz ve arama kodu), P09 (vektör ve arama testleri), P13 (belge ve bakım).
