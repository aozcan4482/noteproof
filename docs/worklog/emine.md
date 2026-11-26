# Emine — devir notu ve work log taslağı

Sahip: emine (Quality lead, test engineer, AI engineer) · Modül: `copywarn/`, `evalset/`, `tests/copywarn/`,
`tests/e2e/`, `docs/reports/`. Bu dosyayı yalnızca Emine düzenler (07_KARARLAR K-009).

## Durum (2026-11-26)

Biten (main'de): S6 kodu (`copywarn/`, `evalset/`, `tests/copywarn/`, `copywarn.yml`, PR şablonu) — #3 ile
`16aeaaf`; `main`'de 60 passed, 1 skipped, copywarn CI yeşil
PR'da: EMN-R2 test planı (#7, 26 Kas'ta güncel main'e göre yenilendi; Arda'nın onayını bekliyor) · bu dosya (#6)
Sürüyor: —
Beklediklerim: BRK-0 artık beklemiyor (#3 merge edildi; Burak'ın #8'i kalan parçası) → EMN-0 yapılabilir ·
EYL-3 konu kimlikleri başlamadı → EMN-2'nin `topics` sütunu bunu bekliyor · ARD-4, ARD-6 başlamadı → EMN-4 ·
Ekipten 9'ar not gelmedi → EMN-2
Gecikenler: EMN-R1 (23 Kas), EMN-1 (22 Kas; not çağrısı gruba yazıldı, repoda çıktısı yok) · EMN-2 bitiş 27 Kas,
bağımlılıkları yok
Sıradaki adım: EMN-0 (başlık ve `NP-CONTRACT` işaretleri, `copywarn/checker.py` yorumundaki yol) ve EMN-R1 —
#6 ya da #7 main'e girince yeni branch (en çok iki açık branch kuralı)
Açık sorular: Work log PR'ı (`log/emine-<no>`) da açık branch sayılıyor mu? (Burak da sordu) · Düzenlenebilir
Workbench kimde? · #7'nin iki commit'inde `Task: EMN-R2 (done)` var; ikincisi 26 Kas yenilemesi
İncelemelerim: #2, #4, #5 onaylandı (25 Kas) · #8, #9, #10 onaylandı (26 Kas), hepsi küçük notlarla

## Work log taslağı

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-19 | P07 | S6 | 2 | Implemented the copy warning (char n-gram cosine and shingle containment), the evaluation-set pipeline and 23 tests | https://github.com/aozcan4482/noteproof/commit/ce3ecf5 | hayır |
| 2026-11-25 | P09 | - | 1 | Set up the work-log draft and handover note under the team rule set v2.0 | https://github.com/aozcan4482/noteproof/pull/6 | hayır |
| 2026-11-25 | P09 | - | 1.5 | Reviewed the seven story test cases and the four DoD criteria against the existing tests and named the owner of each gap | https://github.com/aozcan4482/noteproof/pull/7 | hayır |
| 2026-11-25 | P09 | - | 1 | Reviewed pull requests 2, 4 and 5 against the quality-lead checklist and approved them with notes | https://github.com/aozcan4482/noteproof/pull/4 | hayır |
| 2026-11-26 | P09 | S3 | 1 | Reviewed pull requests 8, 9 and 10, ran the tagger tests and refreshed the test plan after the merge of PR 3 | https://github.com/aozcan4482/noteproof/pull/10 | hayır |

Not: 19 Kasım kaydı Workbench'e geç giriliyor; Workbench zamanı kendisi damgaladığı için kayıt 25 Kasım
tarihini taşır. Açıklama işin 19 Kasım'da yapıldığını değiştirmez, kanıt commit'i 19 Kasım tarihlidir.

### EMN-R2 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda, yukarıdaki 1.5 saatlik Work kaydından hemen sonra:

- **Correction of an entry** · Corrects entry no.: **14** · Saat: 0.25 · Kanıt: merge edilmiş #7 linki ·
  Açıklama: `Output of entry 14 was never committed; the test plan review was redone and delivered in entry <no>`
