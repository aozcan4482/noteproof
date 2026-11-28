# Work log taslakları ve devir notu — Eylem (`eylem`)

Bu dosyayı yalnızca Eylem düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-27)

Biten (main'de): EYL-2, EYL-3 (#16; `(part)` — EYL-1 / K-001 ve EYL-R2 main'e girince son commit ile `(done)`)
PR'da: EYL-R1, EYL-R2 (#19, Aleyna inceliyor) · EYL-4 (branch: feature/S4-note-ontology, `(part)`, EYL-1'e bağlı)
Sürüyor: —
Beklediklerim: EYL-1 / K-001 namespace kararı (Arda) · #19 review (Aleyna)
Sıradaki adım: EYL-5 `shapes/note.shapes.ttl` ve `shapes/validate.py`; aynı branch'te `tests/ontology` içindeki `importorskip` kaldırılabilir (rdflib #14 ile pyproject'e girdi)
Açık sorular: NP-TODO(arda) ontology/vocab.py ve tests/ontology — core/ main'de olmadığı için yedek NAMESPACE kullanılıyor

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | P07 | S5 | 2.5 | Wrote the SKOS course vocabulary and the Vocabulary reader with 24 tests | https://github.com/aozcan4482/noteproof/pull/16 | hayır |
| 2026-11-26 | P06 | S5 | 0.5 | Extracted the 14 chapters of Mastering Bitcoin 3rd ed. into topic IDs and drafted the Transactions hierarchy | https://github.com/aozcan4482/noteproof/pull/19 | hayır |
| 2026-11-27 | P05 | S4 | 1 | Wrote the note ontology (noteproof.ttl) and the JSON-LD context with 11 tests | PR_LINKI_C | hayır |

### EYL-R1 ve EYL-R2 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/...` PR'ında:

- **Work** · P06 · S5 · gerçek saat · yukarıdaki ikinci satırın açıklaması · Kanıt: merge edilmiş #19 linki
- **Correction of an entry** · Corrects entry no.: **5** · Saat: 0.25 · Kanıt: aynı PR linki ·
  Açıklama: `Entry 5 was not done at the time; the chapter list was done and delivered in entry <no>`
- **Correction of an entry** · Corrects entry no.: **6** · Saat: 0.25 · Kanıt: aynı PR linki ·
  Açıklama: `Entry 6 was not done at the time; the Transactions SKOS draft was done and delivered in entry <no>`
