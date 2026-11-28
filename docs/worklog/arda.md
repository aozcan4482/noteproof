# Work log taslakları ve devir notu — Arda (`arda`)

Bu dosyayı yalnızca Arda düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-28)

Kural seti: 3.0
Biten (main'de): ARD-0 (#24) · ARD-1 (#41)
PR'da: ARD-2 (#44, review bekliyor)
Sürüyor: ARD-3 — önizleme uç noktası ve testleri tamam, `(part)` commit; #44 merge edilince `main`'den güncellenip `(done)` ve PR (branch: `feature/S1-note-preview`)
Beklediklerim: EYL-3, EYL-5 — kod `main`'de ama `(done)` değil; ARD-4'ün `(done)`'u bunlara bağlı · Erdener — 02#7 hata kodları (405, 422 `invalid_request`, 500, 409 `pseudonym_taken`) ve 02#2 `data/accounts.sqlite` sözleşme notu
Sıradaki adım: ARD-4 `POST /api/notes` (not ve PROV-O RDF'i, `validate_note`, Oxigraph, `Store.enqueue`, `CopyChecker.add`, `data/` dosyaları)
Açık sorular: K-001 (Eylem'le; öneri: mevcut değerde kalmak) · ARD-R1 ve ARD-R2 ARD-5'ten sonraya bilerek ertelendi · #42 (Emine'nin kayıtları) merge edilmeden kendi log PR'ım açılmaz (zincir çakışması)
Not: 27 Kasım kayıtları o gün girilmedi; 28 Kasım'da, açıklamada tarihi belirtilerek geç girilecek (tek seferlik sapma, 04 bölüm 9).

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-27 | P07 | S1 | 3 | On 27 Nov built the core package with the namespace, IRI builders, SHA-256 hashing, data directory and Oxigraph store, with 62 tests | https://github.com/aozcan4482/noteproof/pull/24 | hayır |
| 2026-11-27 | P10 | - | 1 | On 27 Nov reviewed and merged the repository setup and general CI pull requests 14 and 18 | https://github.com/aozcan4482/noteproof/pull/18 | hayır |
| 2026-11-28 | P07 | S1 | 2 | Wrote the register FastAPI app with the health check, the common error format and static web serving, and fixed its CI skip | https://github.com/aozcan4482/noteproof/pull/41 | hayır |
| 2026-11-28 | P10 | - | 0.5 | Reviewed and merged pull requests 35, 40 and 43 and approved the copy-warning file headers in 39 | https://github.com/aozcan4482/noteproof/pull/43 | hayır |
| 2026-11-28 | P12 | S3 | 0.5 | Set up the Groq account with zero data retention and added the CI language-model key as a repository secret (K-005) | - | hayır |
| 2026-11-28 | P07 | S1 | 1 | Added pseudonymous accounts with a one-time token stored only as a hash and the X-NoteProof-Token check | https://github.com/aozcan4482/noteproof/pull/44 | hayır |
| 2026-11-28 | P07 | S3 | 1 | Added the note preview endpoint with type and size checks, parallel tag suggestion and copy check, and nothing saved | https://github.com/aozcan4482/noteproof/commit/15435aa | hayır |
