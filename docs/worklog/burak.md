# Work log taslakları ve devir notu — Burak (`burak`)

Bu dosyayı yalnızca Burak düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-20)

Biten (main'de): —
PR'da: BRK-R1 — `Task: BRK-R1 (done)` commit'i push edildi; PR açılıp Arda'nın onayı ve merge'ü bekleniyor (branch: `docs/brk-r1-timestamp-design`)
Sürüyor: —
Beklediklerim: ERD-0 başlamadı → `TestBranch` yayımlandı ama `main`'e PR'ı açılmadı; BRK-0 bunu bekliyor (bitiş 21 Kas)
Sıradaki adım: BRK-1 — `infra/repo-setup`: `pyproject.toml`, `CODEOWNERS`, `.gitignore` (`noteproof-kurallar/`, `.DS_Store`, `data/`, `.env`, `node_modules/` dahil), branch koruması (22 Kas)
Açık sorular: `TestBranch`'teki `BURAK_ILERLEME.md` `main`'e girmemeli (K-009); PR'da Erdener'den çıkarmasını iste · Düzenlenebilir Workbench dosyası henüz yok (eldeki kopya salt okunur)

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-20 | P06 | S2 | 2 | Summarised Nakamoto sections 3, 7 and 8 and mapped them to the anchor/ timestamp files | https://github.com/aozcan4482/noteproof/commit/b5a7263800c485c3529e27f2ef8c41912a1ad4b9 | hayır |
| 2026-11-20 | P06 | S2 | 2 | Summarised the Mastering Bitcoin OP_RETURN section and wrote the end-to-end anchoring flow with a source-to-test table | https://github.com/aozcan4482/noteproof/commit/d6a97f0927566266bc47c48aad7db63f29d266b4 | hayır |

### BRK-R1 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/...` PR'ında:

- **Correction of an entry** · Corrects entry no.: **9** · Saat: 0.25 · Kanıt: merge edilmiş BRK-R1 PR linki ·
  Açıklama (Burak'a sorulacak: eski iş hiç yapılmadı mı, yapılıp repoya mı konmadı?):
  `Output of entry 9 was never committed; the timestamp design summary was redone and delivered in entry <no>`
  ya da `... was not done; ...`
