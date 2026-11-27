# Work log taslakları ve devir notu — Aleyna (`aleyna`)

Bu dosyayı yalnızca Aleyna düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-26)

Biten (main'de): —
PR'da: ALY-2 (part) ve ALY-4 (part) — #10, Emine'nin review'u bekleniyor; bu yollar için CI yok (BRK-2)
Sürüyor: ALY-2 — `LLMClient`, `client_from_env`, `FakeLLM` hazır; sağlayıcı istemcisi K-005 kararını bekliyor (branch: `feature/S3-ai-tagger`) · ALY-4 — `suggest`, `TagSuggestion` ve S3 testleri hazır; Eylem'in sözlüğü yerine `tests/tagger/fake_vocab.py` (NP-STUB) ile çalışıyor (aynı branch) · ALY-R1 — kurulum tamam (Python 3.12, Tesseract 5.5.4 `tur+eng`); test notları bu akşam yazılıyor
Beklediklerim: EYL-3 (`Vocabulary`, konu kimlikleri) — GitHub'da görünmüyor, bitiş 23 Kas · EMN-2 (60 not) — başlamadı, bitiş 27 Kas · BRK-1 (`pyproject.toml` bağımlılık grupları; `.gitignore`'da `.env` ve `data/` yok)
Sıradaki adım: ALY-R1 karşılaştırması ve `docs/analysis/aleyna-text-extraction.md` (branch: `docs/aleyna-text-extraction`)
Açık sorular: Eski kayıt #7 ve #8 için: "was not done" mı, "was never committed" mı? (Arda'ya sorulacak) · K-005 dil modeli sağlayıcısı · 22–23 Kasım tarihli görevlerin yeni tarihleri (repoya erişim 23 Kasım 19:17'de geldi; Erdener ve Arda'ya sorulacak) · `suggest` boş metinde `ValueError` veriyor; sözleşmede tanımlı değil (Arda'ya not iletilecek, `NP-TODO(arda)`)

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-26 | P07 | S3 | 8 | Set up Python 3.12 and Tesseract with Turkish data, then wrote the tag suggestion module, the LLM client interface, FakeLLM and the S3 acceptance tests | https://github.com/aozcan4482/noteproof/pull/10 | hayır |
