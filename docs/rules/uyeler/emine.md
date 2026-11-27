# Üye dosyası — Emine Esra Çiçek (`emine`)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **Emine'nin** rolünü, kapsamını, kurulumunu ve görevlerini tanımlamak.
Yalnızca Emine ile çalışan araç bu dosyayı uygular.

## 1. Roller

| | |
| --- | --- |
| İdari rol | Quality lead: Definition of Done'ı korur, merge edilen her şeyi inceler |
| Geliştirme rolleri | Test engineer, AI and language-model engineer |
| Lider olduğu process | P09 Verification |
| Sahip olduğu özellik | **Copy warning and evaluation set** (E3; story S6; deliverable D6 ve D8) |
| İkincisi olduğu modül | Student survey, pilot and acceptance — Aysu'nun PR'larını inceler, pilotta yardım eder |
| Planlanan iş payı | %14 |

## 2. Kapsam

**Senin klasörlerin:** `copywarn/`, `evalset/` (`evalset/run_tagger.py` hariç; o Aleyna'nın),
`tests/copywarn/`, `tests/e2e/`, `docs/reports/`, `.github/workflows/copywarn.yml`,
`.github/pull_request_template.md`, `docs/worklog/emine.md`.

**Dokunmayacakların:** diğer bütün klasörler. Quality lead olarak başkalarının kodunu **incelersin**,
düzeltmezsin: bulduğun sorunu PR yorumuna yazarsın, düzeltmeyi dosyanın sahibi yapar.

**Mevcut durum.** `copywarn/` (metin normalleştirme, karakter n-gram kosinüs, shingle containment,
`CopyChecker`) ve `evalset/` (okuma/yazma, kopya üretici, kopya ölçümü) hazır ve sentetik notlarla test
ediliyor. Eksikler: `main`'e alınması, 60 gerçek not, 20 planted copy, gerçek veriyle eşik ayarı,
uçtan uca testler, raporlar.

**Değişmeyecekler** (`02` bölüm 5.4): `CopyChecker.add`, `CopyChecker.check`, `RegisteredNote` ve
`CopyWarning` alanları, `manifest.csv` sütunları. Kurallar: uyarı yalnızca daha önce kaydedilmiş notlara
verilir; aynı hesabın notu kopya değil revizyondur; sistem karar vermez, kanıt gösterir.

## 3. Ek kurulum

`06_KURULUM.md` tamamlandıktan sonra ek bir program gerekmez: `copywarn/` ve `evalset/` yalnızca Python
standart kütüphanesini kullanır.

1. Kontrol: `python -m pytest -q tests/copywarn` yeşil.
2. Uçtan uca testler için `pip install -e ".[dev,all]"` yeterlidir (FastAPI test istemcisi dahil).
3. Regtest'li uçtan uca testi yerelde çalıştırmak istersen Bitcoin Core gerekir (Burak'ın dosyası,
   bölüm 3, 1. adım). Zorunlu değil: bitcoind yoksa test atlanır, CI'da çalışır.
4. `.env`: yalnızca `NOTEPROOF_DATA_DIR=./data`.

## 4. Görevler

### 4.1 Önce: proposal'da yapılmış görünen işler

Proposal'ın work log'unda aşağıdaki işler yapılmış olarak kayıtlı, ama repoda hiçbirinin çıktısı ya da
kanıtı yok. Bu işler **yapılmamış sayılır** ve modül görevlerinden önce, sıfırdan yapılır. Eski kayda
dayanarak "bu zaten var" deme; çıktı `main`'de değilse yoktur (`05_PIPELINE.md` bölüm 1.1).

| No | Görev | Çıktı ve kabul ölçütü | Eski kayıt | Bitiş |
| --- | --- | --- | --- | --- |
| EMN-R1 | Benzerlik yöntemleri karşılaştırması: TF-IDF, sentence embedding ve mevcut yöntemi (karakter n-gram kosinüs + shingle containment) `tests/copywarn/fixtures.py`'deki sentetik notlar ve `evalset.plant` dönüşümleriyle karşılaştır | `docs/analysis/emine-similarity-methods.md`: yöntem başına yakalanan kopya, yanlış alarm, ek bağımlılık; K-002'nin gerekçesi bu belgeye dayanır | #13 | 23 Kas |
| EMN-R2 | Test planı incelemesi: proposal'daki yedi test case'i (S1–S7) ve dört Definition of Done ölçütünü tek tek gözden geçir: otomatik testi var mı, hangi dosyada, eksikse kimin görevi | `docs/reports/test-plan.md`: story başına bir satır; eksikler ilgili üyeye bildirildi. EMN-4 ve EMN-6 bundan yazılır | #14 | 24 Kas |

Bu görevler de diğerleri gibi branch → PR → `main` yolundan geçer ve commit'lerinde `Task: EMN-R1 (done)`
biçiminde izlenir. Work log'a iki kayıt girilir (`04_GIT_AKISI.md` bölüm 9.1): yapılan iş için kanıtlı bir **Work** kaydı
ve tablodaki "Eski kayıt" numarasını gösteren bir **Correction** kaydı.

### 4.2 Modül görevleri

| No | Görev | Kabul ölçütü | Bağımlılık | Bitiş |
| --- | --- | --- | --- | --- |
| EMN-0 | İskelet: `TestBranch` PR'ında kendi kodunun doğru birleştiğini doğrula; `copywarn/checker.py`'deki `eval/run_copywarn.py` yorumunu `evalset/run_copywarn.py` olarak düzelt; dosya başlıklarını ve `NP-CONTRACT` işaretlerini ekle | `tests/copywarn` yeşil; `copywarn.yml` `main`'de çalışıyor | BRK-0 | 22 Kas |
| EMN-1 | Not toplama çağrısı: her üyeden en az 9 kendi notu (7 × 9 = 63). Kuralları ve teslim biçimini (`evalset/README.md`) ekibe duyur; dersler ve konular yeterince çeşitli olsun | Her üye ne vereceğini ve son tarihi biliyor | — | 22 Kas |
| EMN-2 | 60 notu `evalset/notes/` ve `manifest.csv`'ye ekle. Her notta: kişisel veri temizliği, takma adlı yazar (`yazar-01` …), konu kimlikleri Eylem'in listesinden | 60 satır; `python -c "from evalset.data import load_notes; print(len(load_notes()))"` → 60; her `topics` değeri `Vocabulary.is_topic` ile doğrulanıyor (bunun testi var); hiçbir dosyada isim ya da numara yok | EMN-1, EYL-3 | 27 Kas |
| EMN-3 | `python -m evalset.plant` ile 20 planted copy üret ve commit et; `python -m evalset.run_copywarn` çalıştır; yanlış alarm ve kaçan kopyalara bakarak eşiği ayarla | O5 ≥ %90 (20'de en az 18); yanlış alarm sayısı ve eşik gerekçesi `docs/reports/copywarn.md`'de. Hedef tutmuyorsa K-002'ye göre embedding seçeneği Aleyna ile | EMN-2 | 28 Kas |
| EMN-4 | Uçtan uca test (`tests/e2e/`), `FakeLLM` ve sahte node ile: yükle → önizle → onayla → günlük timestamp → proof'u doğrula. Ayrıca: tek karakteri değişen dosya reddi; sözlükte olmayan konu reddi; onaysız kayıt olmaması; aynı hesabın notunun kopya sayılmaması; olası kopyanın önceki proof'a bağlanması | Yedi story'nin her biri için en az bir test, adında story numarasıyla; CI'da yeşil | ARD-4, ARD-6 | 30 Kas |
| EMN-5 | Performans: kopya denetimi arşivde 500 not varken tek not için ne kadar sürüyor; önizleme ve arama süreleri | Sayılar raporda; 3 saniye sınırını aşan varsa sahibine `NP-TODO` ve issue | ARD-7 | 2 Ara |
| EMN-6 | Test raporu: `docs/reports/test-report.md` — story başına test listesi, CI çalışma linki, son sonuç | Final kapısı "test sonuçları rapor bağlantısıyla" karşılanıyor | EMN-4 | 4 Ara, 10 Ara güncelleme |
| EMN-7 | Değerlendirme raporu: `docs/reports/evaluation.md` — O1…O6'nın her biri için ulaşılan değer, nasıl ölçüldüğü, ölçüm komutu ya da kaynağı | Altı objective'in hepsi dolu; sayılar ilgili üyelerden (Burak O1 ve O6, Eylem O2, Aleyna O3, Aysu O4) | pilot | 10 Ara |

**Tasarım notları (aracın uyacağı):**

- `copywarn/` standart kütüphane dışında bağımlılık almaz. Embedding eklenecekse isteğe bağlı bir yol
  olarak eklenir ve varsayılan davranış değişmez.
- Değerlendirme seti boşken ölçüm "başarılı" dönmez; açık mesaj ve çıkış kodu 1 (mevcut davranış korunur).
- Gerçek notlar yalnızca `evalset/notes/` altındadır. `tests/` altındaki bütün metinler sentetiktir.
- Takma ad ↔ kişi eşleşmesi hiçbir dosyaya yazılmaz.
- Arayüzde ve raporlarda ifade "olası kopya"dır; "kopya" ya da "intihal" hükmü yazılmaz.

## 5. Başkalarına sağladıkların

| Kime | Ne | Ne zaman |
| --- | --- | --- |
| Arda | `CopyChecker` (hazır) | hazır |
| Aleyna | 60 not ve `manifest.csv` (tagger ölçümü için) | 27 Kas |
| Arda, Aysu | Test raporu ve değerlendirme raporu (final için) | 10 Ara |
| Herkes | PR incelemesi | 24 saat içinde |

## 6. Başkalarından beklediklerin

| Kimden | Ne | Hazır değilse |
| --- | --- | --- |
| Eylem | Konu kimlikleri | Notları topla, `topics` sütununu kimlikler gelince doldur |
| Herkes | 9'ar not | Cuma kontrolünde eksik olanı Arda'ya bildir |
| Arda | Çalışan `register.app:app` | EMN-4'ün test iskeletini `02` bölüm 7'deki API'ye göre yaz, `NP-STUB` ile |

## 7. İdari görevler

- **Quality lead.** Her PR'ı 24 saat içinde incele. Kontrol listen:
  1. Değişen dosyalar PR sahibinin klasörlerinde mi? (`02` bölüm 2)
  2. Sabit bir sözleşme değişmiş mi? Değiştiyse karar numarası var mı?
  3. Her yeni davranışın testi var mı, test story'ye bağlı mı?
  4. `01` bölüm 5'teki kapsam dışı maddelerden biri eklenmiş mi?
  5. Kişisel veri, sır, çalışma verisi var mı?
  6. Dosya başlıkları ve `NP-` işaretleri doğru mu; `main`'e giren kodda gereksiz `NP-STUB` kalmış mı?
  7. PR şablonundaki Definition of Done kutuları gerçekten doğru mu?

  Onay vermeden önce CI'ın yeşil olduğuna bak. Kendi PR'larında ikinci reviewer Arda'dır.
- **Verification lideri (P09):** hangi story'nin hangi testle doğrulandığının güncel listesi sende (`docs/reports/test-report.md`).
- **Pilotun ikincisi:** Aysu'nun `docs/acceptance/` ve `docs/pilot/` PR'larını incele; pilot oturumlarında ölçüm tutmasına yardım et.

## 8. Work log için tipik process'ler

P09 (testler, ölçümler, PR incelemesi), P07 (kopya uyarısı kodu), P06 (yöntem karşılaştırması), P11 (pilot desteği).
