# Work log taslakları ve devir notu — Burak (`burak`)

Bu dosyayı yalnızca Burak düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-23)

Biten (main'de): —
PR'da: BRK-R1 (#2, 20 Kasım'dan beri review bekliyor; Arda ve Emine'ye hatırlatılacak)
Sürüyor: BRK-R2 — `docs/ops/signet.md` 1. yarı yazıldı, cüzdan ve faucet adresi hazır; signet senkronu %45'te, faucet coin'i bekleniyor (branch: `docs/brk-r2-signet`)
Beklediklerim: ERD-0 başlamadı, son tarih (21 Kas) geçti → Erdener ve Arda'ya yazılacak. BRK-0, BRK-1, BRK-2, BRK-3, BRK-4 buna bağlı
Sıradaki adım: Senkron bitince `getblockchaininfo` çıktısı, faucet bilgisi ve bakiye `signet.md`'ye; ardından `Task: BRK-R2 (done)` ve PR
Açık sorular: `TestBranch`'teki `BURAK_ILERLEME.md` `main`'e girmemeli (K-009) · Düzenlenebilir Workbench dosyası henüz yok · Eski kayıt #9 ve #10 için: "was not done" mı, "was never committed" mı?

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-20 | P06 | S2 | 2 | Summarised Nakamoto sections 3, 7 and 8 and mapped them to the anchor/ timestamp files | https://github.com/aozcan4482/noteproof/commit/b5a7263800c485c3529e27f2ef8c41912a1ad4b9 | hayır |
| 2026-11-20 | P06 | S2 | 2 | Summarised the Mastering Bitcoin OP_RETURN section and wrote the end-to-end anchoring flow with a source-to-test table | https://github.com/aozcan4482/noteproof/commit/d6a97f0927566266bc47c48aad7db63f29d266b4 | hayır |
| 2026-11-23 | P12 | S2 | 2 | Restarted the signet node, created the noteproof wallet and documented the node setup in docs/ops/signet.md | https://github.com/aozcan4482/noteproof/commit/e6187681acb160d478ecc9adbda4965f9f1928e1 | hayır |

### BRK-R1 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/...` PR'ında:

- **Correction of an entry** · Corrects entry no.: **9** · Saat: 0.25 · Kanıt: merge edilmiş BRK-R1 PR linki ·
  Açıklama (Burak'a sorulacak: eski iş hiç yapılmadı mı, yapılıp repoya mı konmadı?):
  `Output of entry 9 was never committed; the timestamp design summary was redone and delivered in entry <no>`
  ya da `... was not done; ...`
