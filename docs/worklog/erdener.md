# Work log taslakları ve devir notu — Erdener (`erdener`)

Bu dosyayı yalnızca Erdener düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-26)

Biten (main'de): ERD-R1 (#4, 25 Kas)
PR'da: ERD-R2 — `README.md` (branch: `docs/readme`)
Sürüyor: —
Beklediklerim: BRK-3 başlamadı (test vektörleri; ERD-2 için) · ARD-0/3/4 başlamadı (`core/`, `/api`; ERD-4, ERD-5 için) · EYL-3/4 başlamadı (sözlük; ERD-5 için) · BRK-6 / K-008 açık (public signet API adresi; ERD-3 için)
Sıradaki adım: ERD-1 — arayüz iskeleti (`web/`), `web/mock/*.json` ile; ERD-R1 taslaklarından
Açık sorular: ERD-0 — `TestBranch` #3 ile `main`'e girdi; kural seti dağıtımının yedi üyeden teyidi ekip grubunda kontrol edilecek · Burak'ın sorusu: work log PR'ları "en çok 2 açık branch" sınırına dahil mi? · Eski kayıt #11 ve #12 için: "was not done" mı, "was never committed" mı?

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-24 | P05 | S5 | 2 | Drew 360 px text wireframes for the search, note card, upload and proof pages and mapped every API field to them | https://github.com/aozcan4482/noteproof/pull/4 | hayır |
| 2026-11-26 | P13 | - | 1 | Wrote the repository README with the project summary, module owners, setup and test steps | <ERD-R2 PR linki> | hayır |

### ERD-R1 için Correction kaydı (#4 `main`'de; 04 bölüm 9.1)

ERD-R1 Work kaydıyla aynı Workbench oturumunda, art arda:

- **Correction of an entry** · Corrects entry no.: **11** · Saat: 0.25 · Kanıt: https://github.com/aozcan4482/noteproof/pull/4 ·
  Açıklama: `Output of entry 11 was never committed; the UI sketches were redone and delivered in entry <no>`
  (eski iş hiç yapılmadıysa `was not done` yazılır)

### ERD-R2 için Correction kaydı (README PR'ı `main`'e girince)

- **Correction of an entry** · Corrects entry no.: **12** · Saat: 0.25 · Kanıt: merge edilmiş ERD-R2 PR linki ·
  Açıklama: `Output of entry 12 was never committed; the README was redone and delivered in entry <no>`
  (eski iş hiç yapılmadıysa `was not done` yazılır)
