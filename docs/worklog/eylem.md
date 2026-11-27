# Work log taslakları ve devir notu — Eylem (`eylem`)

Bu dosyayı yalnızca Eylem düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-26)

Biten (main'de): —
PR'da: EYL-2, EYL-3 (branch: feature/S5-course-vocabulary, `(part)`) · EYL-R1, EYL-R2 (branch: docs/vocabulary-scope)
Sürüyor: —
Beklediklerim: EYL-1 / K-001 namespace kararı (Arda) → EYL-2 ve EYL-3 bu karar ve EYL-R2 main'e girince `(done)` olur · `pyproject.toml`'a rdflib ve pyshacl (Burak)
Sıradaki adım: EYL-4 `ontology/noteproof.ttl` ve `ontology/context.jsonld`; ardından EYL-5 shape'ler
Açık sorular: NP-TODO(arda) ontology/vocab.py — core/ main'de olmadığı için yedek NAMESPACE kullanılıyor · NP-TODO(burak) tests/ontology — rdflib bağımlılığı · Düzenlenebilir Workbench dosyası kimde?

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | P07 | S5 | 2.5 | Wrote the SKOS course vocabulary and the Vocabulary reader with 24 tests | PR_LINKI_B | hayır |
| 2026-11-26 | P06 | S5 | SAAT | Extracted the 14 chapters of Mastering Bitcoin 3rd ed. into topic IDs and drafted the Transactions hierarchy | PR_LINKI_A | hayır |

### EYL-R1 ve EYL-R2 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/...` PR'ında:

- **Work** · P06 · S5 · gerçek saat · yukarıdaki ikinci satırın açıklaması · Kanıt: merge edilmiş PR A linki
- **Correction of an entry** · Corrects entry no.: **5** · Saat: 0.25 · Kanıt: aynı PR linki ·
  Açıklama: `Entry 5 was not done at the time; the chapter list was done and delivered in entry <no>`
- **Correction of an entry** · Corrects entry no.: **6** · Saat: 0.25 · Kanıt: aynı PR linki ·
  Açıklama: `Entry 6 was not done at the time; the Transactions SKOS draft was done and delivered in entry <no>`
