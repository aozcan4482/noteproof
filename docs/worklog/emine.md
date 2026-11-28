# Emine — devir notu ve work log taslağı

Sahip: emine (Quality lead, test engineer, AI engineer) · Modül: `copywarn/`, `evalset/`, `tests/copywarn/`,
`tests/e2e/`, `docs/reports/`. Bu dosyayı yalnızca Emine düzenler (07_KARARLAR K-009).

## Durum (2026-11-28)

Biten (main'de): S6 kodu (#3) · EMN-R2 test planı (#7)
PR'da: EMN-2 (part) — 9/60 not ve manifest denetimi (branch: `feature/S6-evalset-notes`)
Sürüyor: EMN-2 — 51 not daha gerekiyor; ekipten 9'ar not bekleniyor
Beklediklerim: EYL-3 bitti (sözlük main'de, 18 konu) · Ekipten notlar (Eylem'inkiler geldi) → EMN-2 ·
ARD-4, ARD-6 → EMN-4
Gecikenler: EMN-R1 (23 Kas) · EMN-0 (22 Kas, artık yapılabilir) · EMN-1 (22 Kas, çağrı yapıldı) · EMN-2 (27 Kas)
Sıradaki adım: EMN-0 (başlık ve `NP-CONTRACT` işaretleri, `copywarn/checker.py` yorumundaki yol) ve EMN-R1;
notlar geldikçe EMN-2'ye ekleme
Açık sorular: Erdener'in "internetten not" önerisi kapsam dışı (yalnızca kendi notu) — gruba iletildi mi? ·
Kural seti 3.0 (#31) merge olunca Masaüstündeki 2.3 klasörü silinecek
İncelemelerim: #2, #4, #5 (25 Kas) · #8, #9, #10 (26 Kas) · #12, #15, #17, #22, #27, #30, #31, #32, #33, #35
onaylandı, #34'e yorum (28 Kas)

## Work log taslağı

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-19 | P07 | S6 | 2 | Implemented the copy warning (char n-gram cosine and shingle containment), the evaluation-set pipeline and 23 tests | https://github.com/aozcan4482/noteproof/commit/ce3ecf5 | hayır |
| 2026-11-25 | P09 | - | 1 | Set up the work-log draft and handover note under the team rule set v2.0 | https://github.com/aozcan4482/noteproof/pull/6 | hayır |
| 2026-11-25 | P09 | - | 1.5 | Reviewed the seven story test cases and the four DoD criteria against the existing tests and named the owner of each gap | https://github.com/aozcan4482/noteproof/pull/7 | hayır |
| 2026-11-25 | P09 | - | 1 | Reviewed pull requests 2, 4 and 5 against the quality-lead checklist and approved them with notes | https://github.com/aozcan4482/noteproof/pull/4 | hayır |
| 2026-11-26 | P09 | S3 | 1 | Reviewed pull requests 8, 9 and 10, ran the tagger tests and refreshed the test plan after the merge of PR 3 | https://github.com/aozcan4482/noteproof/pull/10 | hayır |
| 2026-11-28 | P09 | - | 2 | Reviewed ten pull requests and the pilot plan, ran the tests of the three code pull requests and raised the cross-border data point for the consent text | https://github.com/aozcan4482/noteproof/pull/34 | hayır |

Not: 19 Kasım kaydı Workbench'e geç giriliyor; Workbench zamanı kendisi damgaladığı için kayıt 25 Kasım
tarihini taşır. Açıklama işin 19 Kasım'da yapıldığını değiştirmez, kanıt commit'i 19 Kasım tarihlidir.

### EMN-R2 düzeltme kaydı (04 bölüm 9.1) — #7 main'de, girilebilir

Aynı Workbench oturumunda, yukarıdaki 1.5 saatlik Work kaydından hemen sonra:

- **Correction of an entry** · Corrects entry no.: **14** · Saat: 0.25 · Kanıt: merge edilmiş #7 linki ·
  Açıklama: `Output of entry 14 was never committed; the test plan review was redone and delivered in entry <no>`
