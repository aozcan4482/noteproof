# Burak — İlerleme Günlüğü

Bu dosya yalnızca `burak` branch'inde tutulur; `main`'e taşınmaz.
Her tamamlanan iş tarih ve kısa açıklamayla madde madde eklenir.

**Sorumluluklarım:** Bitcoin timestamp service (anchor/), registration service yedeği, repo ve release yönetimi, CI, v1.0.0 release.
**Yaklaşan teslim:** 2026-11-13 — Signet üzerinde günlük timestamp ve public proof page.

## Tamamlananlar

### 2026-11-10
- [x] Repo `~/code/noteproof` içine klonlandı, proposal okundu ve görevler çıkarıldı
- [x] `burak` branch'i `main`'den açıldı ve GitHub'a push edildi
- [x] İlerleme günlüğü (`BURAK_ILERLEME.md`) oluşturuldu

## Sıradakiler
- [ ] Repo iskeleti (klasör yapısı, `pyproject.toml`)
- [ ] Regtest node'lu GitHub Actions CI
- [ ] Merkle modülü (kök, path, doğrulama) ve testleri
- [ ] Regtest'te OP_RETURN transaction'ı (32 byte kök)
- [ ] Günlük anchor işi ve proof JSON-LD çıktısı
- [ ] Tarayıcı için JS doğrulama fonksiyonu (Erdener'e)
- [ ] 40 not testi ve OP_RETURN 32 byte testi
