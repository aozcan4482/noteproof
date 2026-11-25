# Emine — devir notu ve work log taslağı

Sahip: emine (Quality lead, test engineer, AI engineer) · Modül: `copywarn/`, `evalset/`, `tests/copywarn/`,
`tests/e2e/`, `docs/reports/`. Bu dosyayı yalnızca Emine düzenler (07_KARARLAR K-009).

## Durum (2026-11-25)

Biten (main'de): —
PR'da: EMN-R2 test planı (#7, Arda'nın onayını bekliyor) · bu dosya (#6) · S6 kodu #3 içinde (#1 kapatıldı:
bütün commit'leri #3'te; #3 merge edilince main'e girer)
Sürüyor: —
Beklediklerim: BRK-0 (#3, Burak'ın `BURAK_ILERLEME.md` silme commit'i bekleniyor) → EMN-0 bunu bekliyor ·
EYL-3 konu kimlikleri başlamadı → EMN-2'nin `topics` sütunu bunu bekliyor · ARD-4, ARD-6 başlamadı → EMN-4
Gecikenler: EMN-R1 (23 Kas), EMN-1 (22 Kas; not çağrısı gruba yazıldı, repoda çıktısı yok)
Sıradaki adım: EMN-R1 benzerlik yöntemleri karşılaştırması — #6 ya da #7 main'e girince yeni branch
(en çok iki açık branch kuralı)
Açık sorular: Work log PR'ı (`log/emine-<no>`) da açık branch sayılıyor mu? Şu an #6 ve #7 açık
İncelemelerim: #2, #4, #5 onaylandı (2026-11-25), küçük notlarla

## Work log taslağı

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-19 | P07 | S6 | 2 | Implemented the copy warning (char n-gram cosine and shingle containment), the evaluation-set pipeline and 23 tests | https://github.com/aozcan4482/noteproof/commit/ce3ecf5 | hayır |
| 2026-11-25 | P09 | - | 1 | Set up the work-log draft and handover note under the team rule set v2.0 | https://github.com/aozcan4482/noteproof/pull/6 | hayır |
| 2026-11-25 | P09 | - | 1.5 | Reviewed the seven story test cases and the four DoD criteria against the existing tests and named the owner of each gap | https://github.com/aozcan4482/noteproof/pull/7 | hayır |
| 2026-11-25 | P09 | - | 1 | Reviewed pull requests 2, 4 and 5 against the quality-lead checklist and approved them with notes | https://github.com/aozcan4482/noteproof/pull/4 | hayır |

Not: 19 Kasım kaydı Workbench'e geç giriliyor; Workbench zamanı kendisi damgaladığı için kayıt 25 Kasım
tarihini taşır. Açıklama işin 19 Kasım'da yapıldığını değiştirmez, kanıt commit'i 19 Kasım tarihlidir.

### EMN-R2 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda, yukarıdaki 1.5 saatlik Work kaydından hemen sonra:

- **Correction of an entry** · Corrects entry no.: **14** · Saat: 0.25 · Kanıt: merge edilmiş #7 linki ·
  Açıklama: `Output of entry 14 was never committed; the test plan review was redone and delivered in entry <no>`
