# Work log taslakları ve devir notu — Burak (`burak`)

Bu dosyayı yalnızca Burak düzenler (K-009). En üstteki "Durum" bölümü her oturumun sonunda güncellenir;
bir sonraki oturum buradan devam eder. Alttaki tablo, Workbench'e girilecek work log kayıtlarının
taslağıdır.

## Durum (2026-11-28)

Kural seti: 2.3 (#31 ile 3.0 bekliyor)
Biten (main'de): BRK-R1 (#2) · BRK-R2 (#5) · BRK-0 (#8) · BRK-2 (#18)
PR'da: BRK-4 (branch: `feature/S2-anchor-maintenance`)
Sürüyor: BRK-1 — branch koruması açık, "CI yeşil" şartı eksik (Arda) · BRK-3 — vektörler main'de (#20); Erdener'in `tests/web/` testi bekleniyor
Beklediklerim: Erdener — vektör testi (BRK-3) · Arda — CI şartı, K-001 (BRK-5), `v0.3.0` kararı, #31 onayı
Sıradaki adım: #31 merge edilince `CODEOWNERS`'a `AGENTS.md` ve `docs/rules/`; K-001 kapanınca BRK-5
Açık sorular: Workbench kayıtları henüz girilmedi (ilk numara 28) · `v0.3.0` ertelensin mi? · Commit yazar e-postasında öğrenci numarası var (03 bölüm 9)
Not: #2, #5, #8, #20 ve #25'i kural 04 bölüm 6.7'nin aksine ben merge ettim; PR'lara açıklama yazıldı.

## Work log taslakları

| Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-20 | P06 | S2 | 2 | Summarised Nakamoto sections 3, 7 and 8 and mapped them to the anchor/ timestamp files | https://github.com/aozcan4482/noteproof/commit/b5a7263800c485c3529e27f2ef8c41912a1ad4b9 | hayır |
| 2026-11-20 | P06 | S2 | 2 | Summarised the Mastering Bitcoin OP_RETURN section and wrote the end-to-end anchoring flow with a source-to-test table | https://github.com/aozcan4482/noteproof/commit/d6a97f0927566266bc47c48aad7db63f29d266b4 | hayır |
| 2026-11-23 | P12 | S2 | 2 | Restarted the signet node, created the noteproof wallet and documented the node setup in docs/ops/signet.md | https://github.com/aozcan4482/noteproof/commit/e6187681acb160d478ecc9adbda4965f9f1928e1 | hayır |
| 2026-11-24 | P12 | S2 | 1.5 | Finished the signet sync, confirmed the faucet coins and completed the BRK-R2 signet record | https://github.com/aozcan4482/noteproof/commit/0d194e3a6905cf9e26d5f6445eb0482178232951 | hayır |
| 2026-11-24 | P10 | S2 | 0.5 | Reviewed the TestBranch pull request, ran its 61 tests and requested removal of the personal log | https://github.com/aozcan4482/noteproof/pull/3 | hayır |
| 2026-11-25 | P10 | - | 1 | Reviewed the open pull request queue and merged the approved UI sketches pull request into main | https://github.com/aozcan4482/noteproof/pull/4 | hayır |
| 2026-11-26 | P10 | - | 1 | Merged the approved BRK-R1 and BRK-R2 pull requests into main and deleted their branches | https://github.com/aozcan4482/noteproof/pull/5 | hayır |
| 2026-11-26 | P10 | - | 1 | Moved the old personal progress log into the work-log file and closed the BRK-0 task | https://github.com/aozcan4482/noteproof/pull/8 | hayır |
| 2026-11-27 | P10 | - | 2.5 | Tested and merged seven approved pull requests and reviewed the web skeleton and work-log pull requests | https://github.com/aozcan4482/noteproof/pull/13 | hayır |
| 2026-11-27 | P10 | - | 1.5 | Added the build system, package list, dependency groups, CODEOWNERS and ignore rules for BRK-1 | https://github.com/aozcan4482/noteproof/pull/14 | hayır |
| 2026-11-27 | P10 | - | 1 | Wrote the general CI workflow with a verified Bitcoin Core download and a regtest check that cannot be skipped | https://github.com/aozcan4482/noteproof/pull/18 | hayır |
| 2026-11-27 | P09 | S7 | 1 | Generated the shared Merkle test vectors and a sample note with its proof and tested them against anchor/ | https://github.com/aozcan4482/noteproof/pull/20 | hayır |

### BRK-R1 ve BRK-R2 `main`'de: girilecek düzeltme kayıtları (04 bölüm 9.1)

Aynı Workbench oturumunda art arda, tek `log/...` PR'ında:

- **Correction of an entry** · Corrects entry no.: **9** · Saat: 0.25 · Kanıt: merge edilmiş BRK-R1 PR linki ·
  Açıklama (Burak'a sorulacak: eski iş hiç yapılmadı mı, yapılıp repoya mı konmadı?):
  `Output of entry 9 was never committed; the timestamp design summary was redone and delivered in entry <no>`
  ya da `... was not done; ...` · BRK-R1 PR: https://github.com/aozcan4482/noteproof/pull/2
- **Correction of an entry** · Corrects entry no.: **10** · Saat: 0.25 · Kanıt: https://github.com/aozcan4482/noteproof/pull/5 ·
  Açıklama (aynı soru): `Output of entry 10 was never committed; the signet node and faucet coins were redone and recorded in entry <no>`
  ya da `... was not done; ...`

## `anchor/` dosya rehberi

`BURAK_ILERLEME.md`'den taşındı (K-009, BRK-0). O dosya 10–12 Kasım'da eski `burak` branch'inde tutuluyordu
ve `main`'e girmedi. Rehber, `anchor/`'ın `main`'e girdiği 2026-11-25 hâlini anlatır; varsayılan yolların `data/`
altına taşınması BRK-4'te yapılacak.

Okuma sırası önerisi: `merkle.py` → `opreturn.py` → `store.py` → `daily.py` → `proof.py` → `rpc.py`.

#### `anchor/` — Bitcoin timestamp servisi (benim modülüm)

| Dosya | Ne yapıyor |
| --- | --- |
| `anchor/__init__.py` | Paketin genel açıklaması: 5 adımlık akış ve hangi adımın hangi dosyada olduğu. |
| `anchor/merkle.py` | Merkle tree. Not hash'lerinden 32 byte'lık kökü hesaplar, her not için Merkle path üretir ve path'i doğrular (`build_tree`, `verify_path`). Yaprak için `0x00`, iç düğüm için `0x01` öneki kullanılır; tek kalan düğüm kopyalanmaz, yukarı taşınır. |
| `anchor/opreturn.py` | OP_RETURN çıktısı. Kökü `6a 20 <32 byte>` scriptine çevirir ve bir işlemin yalnızca 32 byte'lık kök taşıyıp taşımadığını kontrol eder (KVKK kuralı). |
| `anchor/store.py` | SQLite kuyruğu. **Arda'nın kayıt servisiyle sözleşme burada:** `Store.enqueue(note_hash_hex)`. Ayrıca batch kayıtları (kök, txid, blok, durum: `built → broadcast → confirmed`) tutulur. |
| `anchor/rpc.py` | Bitcoin Core JSON-RPC istemcisi (bitcoin-cli'nin Python karşılığı). Ayarlar ortam değişkenlerinden okunur: `NOTEPROOF_RPC_URL`, `NOTEPROOF_RPC_USER`, `NOTEPROOF_RPC_PASSWORD`, `NOTEPROOF_RPC_WALLET`. |
| `anchor/daily.py` | Günlük iş (proposal aktivite modeli B, adım 10–13): kuyruğu topla, ağacı kur, işlemi gönder, onay bekle, 6 blokta onay yoksa `bumpfee`, proof dosyalarını yaz. Mainnet'te çalışmayı reddeder. Yarıda kalan batch'leri bir sonraki çalışmada tamamlar. Çalıştırma: `python -m anchor.daily --db noteproof.sqlite --out proofs/` |
| `anchor/proof.py` | Proof dosyası (JSON-LD): `noteHash`, `merklePath`, `merkleRoot`, `txid`, `blockHeight`, `blockHash`, `blockTime`. `verify_offline` dosya + proof ile internetsiz kontrol yapar, `verify_on_chain` ise kökün gerçekten o işlemin OP_RETURN'ünde olduğunu node'dan kontrol eder. |

#### `tests/anchor/` — testler

| Dosya | Ne test ediyor |
| --- | --- |
| `test_merkle.py` | 1–101 not için her path'in doğrulandığını; yanlış not, bozulmuş path, yanlış kök ve "iç düğümü yaprak gibi gösterme" saldırısının reddedildiğini. |
| `test_opreturn.py` | Yalnızca 32 byte'lık kökün kabul edildiğini, başka bütün OP_RETURN biçimlerinin reddedildiğini. |
| `test_daily.py` | Sahte node ile bütün akış: 40 not → tek işlem; her proof geçerli; tek karakteri değişen dosya "kayıtlı dosya değil"; boş kuyruk; aynı hash iki kez kuyruğa girmez; mainnet reddi; 6 blok sonra fee bump; yarıda kalan batch'in tamamlanması. |
| `fake_rpc.py` | Testler için sahte Bitcoin node'u (bitcoind olmadan akışı denemek için). |
| `test_regtest.py` | Gerçek `bitcoind -regtest` ile 40 not testi. bitcoind kurulu değilse otomatik atlanır. |

#### Kök dizin

| Dosya | Ne yapıyor |
| --- | --- |
| `pyproject.toml` | Proje tanımı ve pytest ayarları. Ek bağımlılık yok, yalnızca standart kütüphane kullanılıyor. |
| `.gitignore` | `__pycache__`, `*.sqlite`, `proofs/` gibi çalışma çıktılarını repoya sokmaz. |

Testleri çalıştırmak için: `python -m pytest -q`

### Eski günlükten tamamlananlar (10–12 Kasım)

- 2026-11-10: Repo klonlandı, proposal okundu, görevler çıkarıldı; `burak` branch'i açıldı.
- 2026-11-12: `anchor/` paketi (merkle, opreturn, store, rpc, daily, proof) ve testleri yazıldı.
- 2026-11-12: Bitcoin Core v32.1.0 kuruldu; gerçek regtest testi geçti (40 not → tek işlem, 40 proof doğrulandı).

Bu işler 2026-11-25'te PR #3 (`16aeaaf`) ile `main`'e girdi.
