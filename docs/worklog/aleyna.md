# Work log taslakları ve devir notu — Aleyna (`aleyna`)

Bu dosyayı yalnızca Aleyna düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-27)

Biten (main'de): —
PR'da: ALY-R1 — #12, Emine'nin review'u bekleniyor · Steward kontrolü 27 Kas — #15
Sürüyor: ALY-2 (part, main'de #10 ile) — `LLMClient`, `client_from_env`, `FakeLLM`; sağlayıcı istemcisi K-005 kararını bekliyor · ALY-4 (part, main'de #10 ile) — `suggest`, `TagSuggestion` ve S3 testleri; `tests/tagger/fake_vocab.py` (NP-STUB) ile çalışıyor, EYL-3 main'e girince gerçek sözlüğe bağlanacak
Beklediklerim: EYL-3 — Eylem'in `feature/S5-course-vocabulary` branch'inde (27 Kas 00:05; imzalar 02#5.2 ile aynı, `Topic_TransactionFees` ve `Topic_FeeRate` var), PR henüz yok · EMN-2 (60 not) — kimlikler ve notlar bekleniyor · BRK-1 (`pyproject.toml` bağımlılık grupları, `rdflib` dahil; `.gitignore`'da `.env` ve `data/` yok)
Sıradaki adım: ALY-3 `tagger/extract.py` (karar: `docs/analysis/aleyna-text-extraction.md` bölüm 5) · ALY-5 sentetik örneklerle · Emine için 9 kendi notum (EMN-2)
Açık sorular: K-005 dil modeli sağlayıcısı · 22–23 Kasım tarihli görevlerin yeni tarihleri (repoya erişim 23 Kasım 19:17'de geldi; Erdener kural setini 27 Kasım'da revize ediyor) · `suggest` boş metinde `ValueError` veriyor; sözleşmede tanımlı değil (`NP-TODO(arda)`) · Özetin "iki cümle" olması kodla denetlenmiyor (Emine'nin #10 notu) → ALY-6
Cevaplanan: Eski kayıt #7 ve #8 plan olarak yazılmış, iş yapılmamış → Correction'larda "was not done" (Aleyna, 27 Kas) · Work log `log/` branch'leri 2 açık branch sınırına dahil değil (ekip grubu, 27 Kas)

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | P07 | S3 | 8 | Set up Python 3.12 and Tesseract with Turkish data, then wrote the tag suggestion module, the LLM client interface, FakeLLM and the S3 acceptance tests | https://github.com/aozcan4482/noteproof/pull/10 | evet (kayıt 15, #11) |
| 2026-11-26 | P06 | S3 | 4 | Wrote three handwritten note pages and compared pypdf and Tesseract on three photos and three PDFs for the text extraction decision | https://github.com/aozcan4482/noteproof/pull/12 | hayır (#12 main'e girince) |

### ALY-R1 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/aleyna-<no>` PR'ında:

1. **Work** — yukarıdaki 2026-11-26 P06 satırı. Kanıt: merge edilmiş #12.
2. **Correction of an entry** · Corrects entry no.: **7** · Saat: 0.25 · Kanıt: aynı #12 linki · Açıklama:
   `Entry 7 was written as a plan and the work was not done; the text extraction comparison was done and delivered in entry <no>`
   (`<no>`: 1. maddedeki Work kaydının numarası)

Kayıt #8 (ilk istem) için Correction, ALY-R2 bitince aynı biçimde girilir.
