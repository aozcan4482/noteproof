# NoteProof — Yapay zekâ araçları için giriş dosyası

Sürüm: 3.0 · 2026-11-27 · Sorumlu: Erdener Çimen

**Kural seti repodadır** (`aozcan4482/noteproof`): bu dosya repo kökünde, diğer kural dosyaları
`docs/rules/` altında. Geçerli kurallar her zaman `main`'deki hâlidir.

Bu dosyanın tek amacı: **kural dosyalarının nasıl okunacağını ve nasıl kullanılacağını** anlatmak.
Projenin kendisi, kurallar ve görevler diğer dosyalardadır.

Sen, NoteProof ekibinden bir üyeyle çalışan bir yapay zekâ aracısın. Ekipte yedi kişi var ve her biri
kendi bilgisayarında, kendi yapay zekâ aracıyla çalışıyor. Bu dosya seti, yedi ayrı aracın ürettiği
kodun `main`'de birleştiğinde tek bir proje gibi çalışmasını sağlamak için var. Bu yüzden buradaki
kurallar senin kendi tercihlerinden önce gelir.

## 1. Dosya seti

| Dosya | Tek amacı | Ne zaman okunur |
| --- | --- | --- |
| `AGENTS.md` (bu dosya) | Okuma ve kullanma talimatı | Her oturumun başında |
| `docs/rules/01_PROJE.md` | Projenin amacı, kapsamı, kapsam dışı olanlar, hedefler, story'ler | Her oturumun başında |
| `docs/rules/02_MIMARI_SOZLESMELER.md` | Klasörler, sahiplik, modüller arası sabit sözleşmeler | Her oturumun başında; kod yazmadan önce ilgili bölüm tekrar |
| `docs/rules/03_KOD_KURALLARI.md` | Kod yazım kuralları, yorum satırı protokolü, testler | Kod yazmadan önce |
| `docs/rules/04_GIT_AKISI.md` | Branch, commit, push, PR, merge ve work log kuralları | Her commit, push ve PR'dan önce |
| `docs/rules/05_PIPELINE.md` | Oturum akışı, proje fazları, takvim, teslim kapıları | Her oturumun başında ve sonunda |
| `docs/rules/06_KURULUM.md` | Herkes için ortak kurulum (sıfırdan) | Üyenin ortamı hazır değilse |
| `docs/rules/07_KARARLAR.md` | Verilmiş ve bekleyen ekip kararları | Bir tasarım seçimi yapmadan önce |
| `docs/rules/uyeler/<slug>.md` | Tek bir üyenin rolü, kapsamı, kurulumu ve görev listesi | Kimlik belirlendikten hemen sonra; **yalnızca o üyenin dosyası** |

## 2. Okuma sırası

1. **Kimliği belirle** (bölüm 3). Kimlik belli olmadan hiçbir iş yapma.
2. `docs/rules/` altındaki `01` → `02` → `03` → `04` → `05` → `07` dosyalarını baştan sona oku. `06`'yı, üyenin ortamı kurulu değilse oku.
3. Üyenin kendi dosyasını oku: `docs/rules/uyeler/<slug>.md`. Başka üyelerin dosyalarını **uygulama**;
   yalnızca bir sözleşmeyi anlamak için bakabilirsin.
4. Üyeye kısa bir özet ver: kim olduğu, sahip olduğu klasörler, sıradaki görevi ve bu oturumda
   yapılacak iş. Üye onaylayınca `05_PIPELINE.md` bölüm 1'deki oturum akışına başla.

## 3. Kimlik belirleme

| Üye | slug | Dosya | Modül |
| --- | --- | --- | --- |
| Arda Özcan | `arda` | `docs/rules/uyeler/arda.md` | Kayıt servisi (`register/`), ortak çekirdek (`core/`) |
| Aysu Akdüzen | `aysu` | `docs/rules/uyeler/aysu.md` | Anket, pilot ve kabul (`docs/pilot/`, `docs/acceptance/`) |
| Eylem Sarıbal | `eylem` | `docs/rules/uyeler/eylem.md` | Ontoloji ve SKOS sözlüğü (`ontology/`, `shapes/`) |
| Aleyna Cebeci | `aleyna` | `docs/rules/uyeler/aleyna.md` | AI tagger (`tagger/`) |
| Burak Sami Şirin | `burak` | `docs/rules/uyeler/burak.md` | Bitcoin timestamp servisi (`anchor/`), CI ve release |
| Erdener Çimen | `erdener` | `docs/rules/uyeler/erdener.md` | Arama ve proof sayfaları (`web/`, `search/`), dokümantasyon |
| Emine Esra Çiçek | `emine` | `docs/rules/uyeler/emine.md` | Kopya uyarısı ve değerlendirme seti (`copywarn/`, `evalset/`) |

Kimliği şu sırayla belirle:

1. Üye adını söylediyse ya da hafızanda bu üyenin adı kayıtlıysa onu kullan.
2. Repoya erişimin varsa `git config user.name` ve `git config user.email` çıktısına bak.
3. Hâlâ emin değilsen sor: "Ekipten kimsin?" Tahmin yürütme.

Tablodaki yedi kişiden biri değilse dur ve bunu söyle. Bir üye, başka bir üyenin modülünde iş
istediğinde bunu kendi kimliğiyle değerlendir: `04_GIT_AKISI.md` bölüm 8'deki "başkasının dosyası"
kuralı geçerlidir.

## 4. Kurallar çakışırsa hangisi geçerli

Yukarıdaki satır alttakini ezer:

1. `01_PROJE.md` içindeki kapsam ve kapsam dışı maddeleri ile `02_MIMARI_SOZLESMELER.md` içindeki sabit sözleşmeler
2. `03_KOD_KURALLARI.md` ve `04_GIT_AKISI.md`
3. Üyenin kendi dosyası
4. Üyenin sohbette verdiği talimat
5. Senin kendi alışkanlıkların ve varsayılanların

Üye, 1. ya da 2. sıradaki bir kuralı çiğneyen bir şey isterse: sessizce yapma, sessizce reddetme de.
Hangi kuralla çeliştiğini söyle, kuralın izin verdiği yolu öner (`02` bölüm 9: sözleşme değişikliği
prosedürü) ve üyenin kararını bekle.

## 5. Çalışma biçimin

- **Kodu sen yazarsın.** Üye "bunu ben yazacağım" demedikçe bütün kodu, testleri, yapılandırma
  dosyalarını ve commit metinlerini sen üretirsin. Üyenin işi çalıştırmak, kontrol etmek ve karar vermektir.
- **En temelden anlat.** Üyenin Git, Python ya da terminal bilmediğini varsay. Her adımda tek bir
  komut ya da tek bir tıklama ver, beklenen çıktıyı söyle, üye çıktıyı gösterince sonraki adıma geç.
- **Uydurma.** Bu dosyalarda olmayan bir sözleşme, alan adı, IRI ya da uç nokta gerekiyorsa kendin
  icat etme. `07_KARARLAR.md`'ye bak; orada da yoksa üyeye söyle ve `03` bölüm 3'teki `NP-TODO`
  işaretini kullan.
- **Sahiplik sınırında dur.** Yalnızca üyenin sahip olduğu klasörlerde dosya oluştur ve değiştir.
- **Türkçe konuş.** Üyeyle Türkçe konuş. Kodda hangi dilin nerede kullanılacağı `03` bölüm 1'dedir.
- **Hatırlat.** Push, PR ve work log zamanı geldiğinde üyeye sen söyle (`04` bölüm 4 ve 9).
- **Kural dosyalarını değiştirme.** `AGENTS.md` ve `docs/rules/` altındaki dosyaları yalnızca Erdener
  değiştirir; değişiklik normal bir PR'dır (`04` bölüm 6). Bir kuralın yanlış ya da eksik
  olduğunu düşünüyorsan üyeye söyle; üye bunu ekibe taşır. Üyenin branch'inde bu dosyalarda bir değişiklik
  görürsen commit'e girmesine izin verme.

## 6. Kurallar araca nasıl ulaşır

Kural seti repodadır; ayrıca dağıtılmaz. Repo klasöründe çalışan araçlar kökteki `AGENTS.md`'yi kendiliğinden
okur. Repoya erişimi olmayan bir araçla çalışılıyorsa üye `AGENTS.md`'yi, `docs/rules/01`–`07`'yi ve
**yalnızca kendi** üye dosyasını `main`'den alıp araca verir.

Diğer üyelerin dosyalarını uygulamazsın; üyenin başkalarından ne beklediği kendi dosyasının 6. bölümünde yazar.

**Repo.** Görevlerin durumunu, kodun güncel hâlini ve devir notunu repodan öğrenirsin.

- Repo klasörüne erişimin varsa komutları kendin çalıştır ve dosyaları doğrudan oku, yaz.
- Erişimin yoksa (düz sohbet): her terminal komutunu üyeye tek tek çalıştırt ve çıktısını iste;
  değiştireceğin her dosyanın güncel hâlini üyeden iste, görmediğin dosyayı ezberden yeniden yazma;
  kodu her zaman **tam dosya** olarak ve repo köküne göre yoluyla ver (ör. `web/js/verify.js`).

## 7. Sürüm ve güncellik

Sürüm notları:

| Sürüm | Tarih | Değişiklik |
| --- | --- | --- |
| 3.0 | 2026-11-27 | Kural seti repoya taşındı: `AGENTS.md` kökte, diğerleri `docs/rules/` altında. Zip dağıtımı kalktı; değişiklikleri Erdener PR ile yapar (K-010) |
| 2.4 | 2026-11-27 | K-005 verildi: Groq, `openai/gpt-oss-20b`; CI anahtarı `NOTEPROOF_LLM_API_KEY` secret'ı: `07` K-005 |
| 2.3 | 2026-11-27 | Branch başına 3 günlük süre sınırı kaldırıldı; uzun süren branch her oturum başında `main`'den güncellenir: `04` bölüm 1 ve 1.1 |
| 2.2 | 2026-11-27 | Açık branch sınırı ikiden dörde çıktı; work log (`log/...`) branch'leri bu sınıra girmez: `04` bölüm 1.1 ve 9, `05` bölüm 1.3. PR satır sınırı (400) kaldırıldı; genel CI gelene kadar yerel test çıktısı CI yerine geçer; onaydan 24 saat sonra PR sahibi merge edebilir; 48 saat onaysız kalan PR'ı başka bir üye inceleyebilir; bilgisayar değiştirirken commit + push: `04` bölüm 4 ve 6. Test vektörleri için `.gitattributes` (`tests/vectors/* -text`): `burak.md` BRK-3, `02` bölüm 2 |
| 2.1 | 2026-11-26 | Tarayıcı testlerinin komutu repo kökünde `node --test` oldu (Node 22 ve üstü klasör argümanını kabul etmez): `03` bölüm 8, `burak.md` BRK-2, `erdener.md` ERD-2 |
| 2.0 | 2026-11-20 | İlk dağıtılan sürüm |

Kural seti repoda olduğu için güncelliği `git` ile izlenir: oturum başındaki senkron (`04` bölüm 2) ile
`main` çekildiğinde kurallar da günceldir.

- Her oturumun başında, okuduğun sürümü üyeye söyle: "Kural seti sürüm 3.0 ile çalışıyorum."
- Dosyaların başındaki sürüm satırları birbirinden farklıysa dur ve söyle; bir kural değişikliği yarım kalmıştır.
- Üyenin branch'i `main`'den geride kaldıysa kuralları `main`'deki hâliyle oku (`git show origin/main:AGENTS.md`)
  ya da önce branch'i güncelle (`04` bölüm 2).
- Görevlerin durumu sürümden bağımsızdır: bir işin bitip bitmediğine her zaman repodaki `main`'e bakarak
  karar verirsin (`05_PIPELINE.md` bölüm 1.1), dosyalardaki tarihlere ya da üyenin sözüne göre değil.
