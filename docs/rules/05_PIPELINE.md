# 05 — Pipeline: oturum akışı, fazlar, takvim

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **işin hangi sırayla yapılacağını** tanımlamak. İki düzeyi vardır: her çalışma
oturumunda izlenen akış (bölüm 1) ve projenin 11 Aralık'a kadarki fazları (bölüm 2).

## 1. Oturum akışı

Her oturumda bu dokuz adımı sırayla izle. Bir adımı atlama; adımın çıktısını üyeye kısaca söyle.

| Adım | Ne yapılır | Çıktı |
| --- | --- | --- |
| 1. Kimlik | `AGENTS.md` bölüm 3 | Üyenin slug'ı |
| 2. Okuma | Ortak dosyalar ve üyenin dosyası; sürümü üyeye söyle (`AGENTS.md` bölüm 7) | Okundu onayı ve sürüm |
| 3. Senkron | `04` bölüm 2: fetch, `main`'i çek, branch'i güncelle, testleri çalıştır | Güncel branch, test sonucu |
| 4. Görev seçimi | Önce durum taraması (bölüm 1.1 ve 1.2): kendi görevlerin ve beklediğin görevler `main`'de mi. Sonra üyenin listesinde bitmemiş ilk görev; bölüm 4.1'deki `R` görevleri modül görevlerinden önce gelir. Bağımlılığı `main`'de değilse sahteyle (`NP-STUB`) ilerleme ya da sıradaki bağımsız görev | Durum tablosu, görev kimliği ve bu oturumun hedefi |
| 5. Sözleşme kontrolü | `03` bölüm 10'daki yedi soru; `07_KARARLAR.md`'de ilgili karar | "Dokunacağım dosyalar ve sözleşmeler" listesi |
| 6. Üretim | Kodu ve testleri yaz. Küçük adımlarla: her dosyadan sonra üye çalıştırır | Çalışan kod, geçen testler |
| 7. Doğrulama | `python -m pytest -q`; arayüz işi ise telefonda ve masaüstünde elle deneme; görevin kabul ölçütü | Test çıktısı |
| 8. Kayıt | `04` bölüm 3–6: dosya listesini kontrol et, commit metnini ver, push'u hatırlat, gerekiyorsa PR | Commit, push, PR linki |
| 9. Kapanış | Work log taslağı (`04` bölüm 9); devir notu | Taslak satırı, devir notu |

### 1.1 Bir iş ne zaman bitmiş sayılır

Bir görevin dört durumu vardır. Durumu söze, hafızana ya da devir notuna göre değil, **repoya bakarak** belirle.

| Durum | Anlamı | Nasıl anlaşılır |
| --- | --- | --- |
| Başlamadı | Hiçbir commit yok | Aşağıdaki iki arama da boş döner |
| Sürüyor | Üyenin branch'inde `(part)` commit'leri var | İkinci arama `(part)` satırları bulur |
| PR'da | `(done)` commit'i push edilmiş, `main`'e girmemiş | İkinci arama `(done)` bulur, birinci boş döner |
| **Bitti** | `(done)` commit'i `main`'de | Birinci arama sonuç verir |

```
git fetch origin
git log origin/main --oneline --grep "Task: ERD-2 (done)"       # 1: main'de mi?
git log --remotes   --oneline --grep "Task: ERD-2"               # 2: herhangi bir branch'te var mı?
```

Komutlar repo kökünde çalışır. Repoya erişimin yoksa üyeye çalıştırt ve çıktıyı iste. Çıktı boşsa
"sonuç yok" demektir; hata değildir.

Kesin kural: **`main`'e girmemiş iş bitmiş sayılmaz.** Bu, üyenin kendi görevleri için de başkalarının
görevleri için de geçerlidir. Buna göre:

- Kod yazıldı, testler yerelde geçti, push edildi, PR açıldı: görev hâlâ **bitmedi**. Üyeye "bitti" deme;
  "PR'da, onay bekliyor" de.
- Devir notunun "Biten" satırına yalnızca birinci aramanın sonuç verdiği görevleri yaz.
- Work log'da "delivered" ya da "completed" yazılacaksa kanıt linki merge edilmiş PR olmalıdır.
- Bir görevin bitmesi başka bir görevin bitmesine bağlıysa (üye dosyasındaki "Bağımlılık" sütunu),
  bağımlı olunan görev `main`'de değilken bu görev de `(done)` olamaz: sahteyle çalışan kod bitmiş kod değildir.
  O zamana kadar commit'ler `(part)` ile gider.
- Bir üye "Burak bitirdiğini söyledi" derse yine birinci aramaya bak. Sonuç yoksa iş senin için hazır değildir.

### 1.2 Başkasının işini beklerken (bağımlılık kontrolü)

Her oturumun 4. adımında, üyenin dosyasındaki "Başkalarından beklediklerin" tablosundaki ve sıradaki
görevin "Bağımlılık" sütunundaki her görev kimliği için bölüm 1.1'deki iki aramayı yap ve üyeye kısa bir
durum tablosu göster:

```
BRK-3  Bitti (main'de, 23 Kas)      → sahte vektörleri sil, gerçek dosyaya bağlan
BRK-6  PR'da (#14, onay bekliyor)   → sahteyle devam; istersen review'u hızlandırmasını iste
ARD-4  Başlamadı (bitiş: 26 Kas)    → sahteyle devam
```

Sonuca göre:

| Beklenen görev | Ne yaparsın |
| --- | --- |
| **Bitti** | Oturum başındaki senkronu (`04` bölüm 2) zaten yaptığın için iş bilgisayarındadır. İlgili `NP-STUB`'ı ve `NP-TODO`'yu sil, gerçek modülü çağır, testleri çalıştır. Gerçek modül sözleşmeden farklı davranıyorsa kendi tarafında etrafından dolaşma; farkı modülün sahibine bildir (`04` bölüm 8) |
| **PR'da** | Sahteyle devam et. O branch'i kendi branch'ine merge etme, dosyalarını kopyalama. Üyeye PR numarasını söyle; iş acilse üye PR'ın reviewer'ından incelemeyi öne almasını ister |
| **Sürüyor** | Sahteyle devam et. Bitiş tarihi geçtiyse üyeye söyle |
| **Başlamadı**, bitiş tarihi gelmemiş | Sahteyle devam et |
| **Başlamadı**, bitiş tarihi geçmiş | Üyeye söyle. Üye, görevin sahibine ve Arda'ya ekip grubundan yazar: hangi görevi beklediğini, kendi hangi görevinin buna bağlı olduğunu ve ne zamana kadar sahteyle idare edebileceğini |

Sahteyle ilerlemenin kuralı: sahte, `02` bölüm 5'teki imzaya **birebir** uyar ve `NP-STUB(owner=..., contract=...)`
ile işaretlenir. Böylece gerçek modül geldiğinde değişen tek şey içe aktarma satırıdır. Beklediğin şey bir
sözleşmede yazmıyorsa (ör. henüz kararlaştırılmamış bir adres), sahte de yazma; `NP-TODO(<slug>)` bırak ve
o parçayı sona bırak.

Kimsenin işini kendin yaparak bekleme süresini kısaltma. Burak'ın vektör dosyasını, Arda'nın uç noktasını
ya da Eylem'in sözlüğünü "geçici olarak" kendi branch'inde gerçek yoluna (`tests/vectors/`, `register/`,
`ontology/`) yazarsan, o üyenin PR'ı geldiğinde iki sürüm çakışır.

### 1.3 Kendi PR'ın `main`'e girdikten sonra

PR mor "Merged" olduğunda (üye GitHub'dan görür ya da bölüm 1.1'deki birinci arama sonuç verir):

1. GitHub Desktop → **Current branch** → `main` → **Fetch origin** → **Pull origin**.
2. Repo kökünde `python -m pytest -q`. Yeşil olmalı. Kırmızıysa üyeye söyle; üye hemen Burak'a bildirir.
3. Biten branch'i sil: **Branch** menüsü → **Delete…** → "Yes, delete this branch on the remote" kutusu işaretli.
   (Burak merge sırasında uzaktakini silmişse yalnızca yereldeki silinir.)
4. Devir notunda görevi "Biten"e taşı.
5. Bu görevi bekleyen üyeler varsa (PR'daki `Unblocks:` satırı), üye ekip grubuna tek satır yazar:
   "ERD-2 main'de; ERD-3 ve ARD-5 için hazır."
6. Sıradaki görev için `04` bölüm 1.2'deki adımlarla yeni branch aç.

PR beklerken boş durma: üye `main`'e dönüp (1. adım) sıradaki bağımsız görev için yeni bir branch açabilir
(`04` bölüm 1.1: aynı anda en çok dört açık görev branch'i; `log/...` branch'leri sayılmaz). Sıradaki görev, PR'daki göreve bağlıysa ve başka
bağımsız görev yoksa, sıradaki görevin testlerini ve belgelerini yeni branch'te sahteyle hazırla.

**Devir notu.** Oturumun sonunda `docs/worklog/<slug>.md` dosyasının en üstündeki "Durum" bölümünü
güncelle. Üyenin bir sonraki oturumu başka bir araçla ya da hafızasız bir sohbetle başlayabilir; bu not
kaldığı yeri söyler:

```
## Durum (2026-11-24)
Biten (main'de): ERD-1
PR'da: ERD-2 (#12, onay bekliyor)
Sürüyor: ERD-3 — proof.html dosya seçimi ve çevrimdışı kontrol tamam; zincir kontrolü eksik (branch: feature/S7-proof-page)
Beklediklerim: BRK-3 bitti (main'de) · BRK-6 başlamadı → zincir kontrolünü gerçek adresle denemek için
Sıradaki adım: web/js/chain.js içinde public signet API çağrısı
Açık sorular: NP-TODO(burak) web/js/config.js — public signet API adresi
```

**Takılma kuralı.** Aynı sorunda 30 dakikadan uzun kalındıysa dur: sorunu, denenenleri ve gereken şeyi
üç cümleyle yaz, üyeye ekip grubuna iletmesini söyle. Başkasının modülünü kendin düzelterek ilerleme.

## 2. Fazlar ve takvim

Bugün 20 Kasım 2026. Proposal'daki 30 Ekim ve 13 Kasım ara teslimleri repoya göre gecikmiştir; kalan iş
aşağıdaki dört faza sıkıştırılmıştır. Proposal'daki son iki tarih (27 Kasım ve 11 Aralık) korunur.

| Faz | Bitiş | Amaç | Çıkış kapısı |
| --- | --- | --- | --- |
| **0 — İskelet** | 22 Kasım Pazar | Herkesin aynı tabandan başlaması | `main`'de: `anchor/`, `copywarn/`, `evalset/`, `core/`, bağımlılık grupları, genel CI. Kural seti herkese dağıtılmış. `python -m pytest -q` yeşil |
| **1 — Sözleşmeye göre modüller** | 25 Kasım Çarşamba | Her modül kendi başına, sahtelerle çalışır | Her modülün sözleşme fonksiyonları `main`'de ve testli |
| **2 — Entegrasyon** | 27 Kasım Cuma | Uçtan uca akış regtest'te çalışır | Yükle → öner → onayla → kuyruğa al → damgala → proof sayfasında doğrula; konu araması alt konuları bulur. Etiket `v0.3.0` |
| **3 — Sağlamlaştırma** | 4 Aralık Cuma | Hedefler ölçülür, signet canlı | Signet'te günlük timestamp çalışıyor; 60 not + 20 kopya; O3 ≥ %80, O5 ≥ %90; uçtan uca testler; telefonda 3 saniye. Etiket `v0.9.0` |
| **4 — Pilot ve teslim** | 11 Aralık Cuma | Kullanıcılarla doğrulama ve final | Pilot yapıldı, her story'nin kabul durumu ve kanıtı var, değerlendirme raporu, güncel proposal. Etiket `v1.0.0` |

### Faz 0 — İskelet (22 Kasım)

| Görev | Kim |
| --- | --- |
| `TestBranch` (`main` + `burak` + `feature/S6-copy-warning`, çakışmasız birleştirildi) branch'ini yayımla ve `main`'e PR aç; kural setini ekibe zip olarak dağıt | erdener |
| PR'ı incele ve `main`'e al; `BURAK_ILERLEME.md` `main`'e girmez, içeriği `docs/worklog/burak.md`'ye taşınır | burak |
| `core/` paketini ve `pyproject.toml` bağımlılık gruplarını ekle | arda, burak |
| Genel CI (`ci.yml`), `CODEOWNERS`, `main` için branch koruması | burak |
| `07_KARARLAR.md`'deki açık kararları kapat (K-001, K-005) | eylem, aleyna, arda |
| Kurulumu tamamla (`06_KURULUM.md`) ve ilk oturumu yap | herkes |
| Proposal'da yapılmış görünen ama repoda çıktısı olmayan işleri yeniden yap: üye dosyalarında bölüm 4.1, `XXX-R1` ve `XXX-R2` (son tarihleri 21–24 Kasım) | herkes |

### Faz 1 — Modüller (25 Kasım)

Bağımlılık sırası. Solda olan, sağdakini bekletir; bu yüzden soldakiler önce `main`'e girer.

```
core/ (arda)  ──────────────►  hepsi
ontology/ + shapes/ (eylem) ─►  tagger/ (aleyna), register/ (arda), search/ (erdener), evalset manifest (emine)
tests/vectors/ (burak) ──────►  web/js/verify.js (erdener)
tagger/extract.py (aleyna) ──►  register/ önizleme (arda)
register/ API (arda) ────────►  web/ sayfaları (erdener), tests/e2e/ (emine)
docs/acceptance/ (aysu) ─────►  pilot ve kabul
```

Bağımlılığı hazır olmayan üye beklemez: sözleşmeye uyan bir `NP-STUB` ile kendi modülünü yazar ve test eder.
Arayüz için bu, `web/mock/` altındaki örnek JSON yanıtlarıdır.

### Faz 2 — Entegrasyon (27 Kasım)

Entegrasyonun sahibi Arda'dır (P08). Sıra:

1. `register/` gerçek `ontology/`, `shapes/`, `tagger/`, `copywarn/`, `anchor.store` ile bağlanır; sahteler silinir.
2. `web/` sahte JSON yerine gerçek API'ye bağlanır.
3. Regtest'te tam akış: bir not yüklenir, onaylanır, `anchor.daily` çalıştırılır, proof sayfasında doğrulanır.
4. Emine uçtan uca testi `tests/e2e/` altına yazar; iki reddetme senaryosu dahil.
5. Burak `v0.3.0` etiketini atar.

### Faz 3 — Sağlamlaştırma (4 Aralık)

- Burak: signet'te her gün 23:00 timestamp; işlem kimlikleri `docs/ops/` altında.
- Emine, herkes: 60 gerçek not (her üye en az 9 kendi notunu verir), 20 planted copy, eşik ayarı.
- Aleyna: tagger ölçümü ≥ %80.
- Erdener: telefonda 3 saniye ölçümü, erişilebilirlik, Türkçe metinler.
- Arda: revizyon ve kaldırma akışı, proof durumu eşitleme.
- Aysu: 2–3 öğrenciyle deneme oturumu; geri bildirimler GitHub Issues'a.
- Eylem: pilot gönüllülerinin dersleri için sözlük genişletmesi.

### Faz 4 — Pilot ve teslim (11 Aralık)

- 5–9 Aralık: pilot (Aysu yürütür, Emine yardım eder).
- 10 Aralık: her story için kabul durumu ve kanıt; değerlendirme raporu; lessons learned.
- 11 Aralık: Arda proposal dosyasını final aşamasına günceller; Burak `v1.0.0` etiketini atar.

## 3. Final teslim kapıları

Final değerlendirmesi proposal dosyası üzerinden yapılır ve şunları arar. Faz 4'ün sonunda hepsi tamam olmalı:

| Kapı | Sorumlu |
| --- | --- |
| Story'lerin en az %60'ı teslim edilmiş; her story'nin teslim durumu ve kanıtı var | aysu (kabul), arda |
| Her objective'in ulaşılan değeri ve nasıl ölçüldüğü yazılı (O1–O6) | emine (rapor), burak (O1, O6), aleyna (O3), aysu (O4) |
| Repoda etiketlenmiş bir sürüm | burak |
| Test sonuçları bir rapor bağlantısıyla raporlanmış | emine |
| Son kullanıcılarla doğrulama yapılmış; en az 80 kelimelik lessons learned | aysu |
| Work log zinciri sağlam, anomali yok; her üyenin kaydı var | eylem, aleyna |
| Her üye: en az 6 kayıt, en az 2 process, kayıtların en az yarısı kanıtlı, saat payı planın en az yarısı, modülü story teslim etmiş | her üye kendisi |

## 4. Haftalık ritim

| Gün | Ne |
| --- | --- |
| Her gün | Oturum akışı; biten iş için push ve PR; work log kaydı |
| Pazartesi | Haftalık toplantı (Erdener yürütür): geçen haftanın kapısı, engeller, bu haftanın görevleri. Not: `docs/minutes/YYYY-MM-DD.md` |
| Çarşamba | Ara kontrol: bağımlılık bekleyen var mı |
| Cuma | Faz kapısı kontrolü (Arda); work log kontrolü (Eylem, Aleyna); PR kuyruğunun boşaltılması (Burak, Emine) |
