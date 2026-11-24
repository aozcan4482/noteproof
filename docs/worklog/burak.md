# Work log taslakları ve devir notu — Burak (`burak`)

Bu dosyayı yalnızca Burak düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-24)

Biten (main'de): —
PR'da: BRK-R1 (#2, 20 Kas'tan beri review bekliyor) · BRK-R2 (#5, signet senkronu tamam, bakiye 0,0185805 signet BTC)
Sürüyor: BRK-0 — PR #3'e (TestBranch) "Request changes" gönderildi: `BURAK_ILERLEME.md` silinsin (K-009). Silinince onay + merge, ardından `burak` ve `feature/S6-copy-warning` branch'leri silinecek (#1 #3'ün içinde)
Beklediklerim: ERD-0 — #3'te `BURAK_ILERLEME.md`'nin silinmesi · Arda ve Emine'den #2 ve #5 review'ları
Sıradaki adım: #3 merge edilince BRK-1 (`infra/repo-setup`), ardından BRK-2 (CI) ve BRK-3 (test vektörleri)
Açık sorular: Düzenlenebilir Workbench dosyası henüz yok · Eski kayıt #9 ve #10 için: "was not done" mı, "was never committed" mı? · Commit yazar e-postasında öğrenci numarası var (03 bölüm 9) → ekiple konuşulacak

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-20 | P06 | S2 | 2 | Summarised Nakamoto sections 3, 7 and 8 and mapped them to the anchor/ timestamp files | https://github.com/aozcan4482/noteproof/commit/b5a7263800c485c3529e27f2ef8c41912a1ad4b9 | hayır |
| 2026-11-20 | P06 | S2 | 2 | Summarised the Mastering Bitcoin OP_RETURN section and wrote the end-to-end anchoring flow with a source-to-test table | https://github.com/aozcan4482/noteproof/commit/d6a97f0927566266bc47c48aad7db63f29d266b4 | hayır |
| 2026-11-23 | P12 | S2 | 2 | Restarted the signet node, created the noteproof wallet and documented the node setup in docs/ops/signet.md | https://github.com/aozcan4482/noteproof/commit/e6187681acb160d478ecc9adbda4965f9f1928e1 | hayır |
| 2026-11-24 | P12 | S2 | 1.5 | Finished the signet sync, confirmed the faucet coins and completed the BRK-R2 signet record | https://github.com/aozcan4482/noteproof/commit/0d194e3a6905cf9e26d5f6445eb0482178232951 | hayır |
| 2026-11-24 | P10 | S2 | 0.5 | Reviewed the TestBranch pull request, ran its 61 tests and requested removal of the personal log | https://github.com/aozcan4482/noteproof/pull/3 | hayır |

### BRK-R1 `main`'e girince (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/...` PR'ında:

- **Correction of an entry** · Corrects entry no.: **9** · Saat: 0.25 · Kanıt: merge edilmiş BRK-R1 PR linki ·
  Açıklama (Burak'a sorulacak: eski iş hiç yapılmadı mı, yapılıp repoya mı konmadı?):
  `Output of entry 9 was never committed; the timestamp design summary was redone and delivered in entry <no>`
  ya da `... was not done; ...`
