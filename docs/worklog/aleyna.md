# Work log taslakları ve devir notu — Aleyna (`aleyna`)

Bu dosyayı yalnızca Aleyna düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-28)

Biten (main'de): ALY-R1 — #12 · ALY-R2 — #27 · ALY-1 — K-005 "Verildi" (Groq, `openai/gpt-oss-20b`; 07, #31) · ALY-3 — #17 · Steward kontrolü 27 Kas — #15
PR'da: ALY-2 — Groq istemcisi (`GroqClient`, 429'da bekleyip yeniden deneme), branch `feature/S3-groq-client`
Sürüyor: ALY-4 (part, main'de #10 ile) — testler hâlâ `tests/tagger/fake_vocab.py` (NP-STUB) ile; Eylem'in `ontology.vocab.Vocabulary`'si main'de (#16), testler ona bağlanacak
Beklediklerim: EMN-2 — main'de 9 not var (#38), 60 bekleniyor; ALY-5 bunlarla ölçecek
Sıradaki adım: Workbench: #42 merge olunca ALY-R1 ve ALY-R2 kayıtları (aşağıda) · ALY-4: gerçek sözlüğe geçiş · ALY-5 `evalset/run_tagger.py` (CI secret'ı `NOTEPROOF_LLM_API_KEY` Arda'da hazır)
Açık sorular: `suggest` boş metinde `ValueError` veriyor; sözleşmede tanımlı değil (`NP-TODO(arda)`) · Özetin "iki cümle" olması kodla denetlenmiyor (Emine'nin #10 notu) → ALY-6
Cevaplanan: Eski kayıt #7 ve #8 plan olarak yazılmış, iş yapılmamış → Correction'larda "was not done" (Aleyna, 27 Kas) · Work log `log/` branch'leri açık branch sınırına dahil değil (ekip grubu, 27 Kas)

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | P07 | S3 | 8 | Set up Python 3.12 and Tesseract with Turkish data, then wrote the tag suggestion module, the LLM client interface, FakeLLM and the S3 acceptance tests | https://github.com/aozcan4482/noteproof/pull/10 | evet (kayıt 15, #11) |
| 2026-11-26 | P06 | S3 | 4 | Wrote three handwritten note pages and compared pypdf and Tesseract on three photos and three PDFs for the text extraction decision | https://github.com/aozcan4482/noteproof/pull/12 | hayır (#42 merge olunca) |
| 2026-11-27 | P05 | S3 | 6 | Tested the vocabulary-limited tagging prompt on three notes with two Groq models and wrote the comparison for the K-005 model decision | https://github.com/aozcan4482/noteproof/pull/27 | hayır (#42 merge olunca) |
| 2026-11-28 | P07 | S3 | 2 | Wrote the Groq client behind the LLM client interface with waiting and retrying on rate limits, its offline tests and a live check on a sample note | https://github.com/aozcan4482/noteproof/pull/45 | hayır (bugün, R1 ve R2 kayıtlarıyla aynı oturumda) |

### ALY-R1 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/aleyna-<no>` PR'ında:

1. **Work** — yukarıdaki 2026-11-26 P06 satırı. Kanıt: merge edilmiş #12.
2. **Correction of an entry** · Corrects entry no.: **7** · Saat: 0.25 · Kanıt: aynı #12 linki · Açıklama:
   `Entry 7 was written as a plan and the work was not done; the text extraction comparison was done and delivered in entry <no>`
   (`<no>`: 1. maddedeki Work kaydının numarası)

### ALY-R2 `main`'e girince

ALY-R1 çiftinin hemen arkasından, aynı PR'da:

1. **Work** — yukarıdaki 2026-11-27 P05 satırı. Kanıt: merge edilmiş #27.
2. **Correction of an entry** · Corrects entry no.: **8** · Saat: 0.25 · Kanıt: aynı #27 linki · Açıklama:
   `Entry 8 was written as a plan and the work was not done; the first tagging prompt and its trial were done and delivered in entry <no>`
