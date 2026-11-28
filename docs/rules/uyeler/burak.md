# Üye dosyası — Burak Sami Şirin (`burak`)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **Burak'ın** rolünü, kapsamını, kurulumunu ve görevlerini tanımlamak.
Yalnızca Burak ile çalışan araç bu dosyayı uygular.

## 1. Roller

| | |
| --- | --- |
| İdari rol | Repository and release manager: branch'ler, review'lar, etiketler, sürümler |
| Geliştirme rolleri | Zincir geliştiricisi (Bitcoin tarafındaki kod), Release and operations |
| Lider olduğu process'ler | P07 Implementation, P10 Transition, P12 Operation, P14 Disposal |
| Sahip olduğu modül | **Bitcoin timestamp service** (E1; story S2, S1'in proof kısmı) |
| İkincisi olduğu modül | Registration service (`register/`, `core/`) — Arda'nın PR'larını inceler |
| Planlanan iş payı | %15 |
| Sorumlu olduğu ara teslim | Signet'te günlük timestamp ve public proof sayfası (13 Kasım, gecikmiş) |

## 2. Kapsam

**Senin klasörlerin:** `anchor/`, `tests/anchor/`, `tests/vectors/`, `docs/ops/`, `pyproject.toml`,
`.gitignore`, `.gitattributes`, `.github/workflows/ci.yml`, `.github/CODEOWNERS`, `docs/worklog/burak.md`.

**Dokunmayacakların:** diğer bütün klasörler. Proof sayfasının tarayıcı kodu (`web/js/verify.js`)
Erdener'indir; sen ona test vektörlerini ve Merkle kurallarını verirsin.

**Mevcut durum.** `anchor/` hazır ve regtest'te doğrulanmış durumda: `merkle.py`, `opreturn.py`,
`store.py`, `rpc.py`, `daily.py`, `proof.py`. Eksikler: `main`'e alınması, genel CI, signet'te gerçek
işlem, zamanlama, test vektörleri, sürüm etiketleri.

**Değişmeyecekler.** Aşağıdakiler başka modüllerin dayandığı sabit sözleşmelerdir (`02` bölüm 5.5 ve 6):
`Store.enqueue` imzası, proof dosyasının alan adları, Merkle kuralları (önekler `0x00` / `0x01`, tek kalan
düğümün kopyalanmadan yukarı taşınması, tek SHA-256), OP_RETURN'ün yalnızca 32 byte'lık kök taşıması,
mainnet reddi.

## 3. Ek kurulum

`06_KURULUM.md` tamamlandıktan sonra:

1. **Bitcoin Core.** macOS: `brew install bitcoin`. Windows: `https://bitcoincore.org/en/download/`
   adresinden kurulum dosyası; kurulumdan sonra `bitcoind.exe` ve `bitcoin-cli.exe`'nin bulunduğu
   klasör PATH'e eklenir. Kontrol: `bitcoind --version`.
2. **Regtest testi.** `python -m pytest -q -m regtest` → `test_40_notes_anchored_on_regtest` geçer.
3. **Signet node'u.** Veri klasöründeki `bitcoin.conf`:

   ```
   signet=1
   server=1
   [signet]
   rpcuser=<kendi seçtiğin>
   rpcpassword=<kendi seçtiğin>
   rpcport=38332
   ```

   `bitcoind -signet -daemon` ile başlat. Kontrol: `bitcoin-cli -signet getblockchaininfo` çıktısında
   `"chain": "signet"`; `initialblockdownload` `false` olana kadar bekle.
4. **Cüzdan.** `bitcoin-cli -signet createwallet noteproof`, ardından `bitcoin-cli -signet -rpcwallet=noteproof getnewaddress`.
   Adrese bir signet faucet'inden test coin'i iste. Kontrol: `getbalance` sıfırdan büyük.
5. **`.env`:**

   ```
   NOTEPROOF_DATA_DIR=./data
   NOTEPROOF_RPC_URL=http://127.0.0.1:38332
   NOTEPROOF_RPC_USER=...
   NOTEPROOF_RPC_PASSWORD=...
   NOTEPROOF_RPC_WALLET=noteproof
   ```

   RPC şifresi, cüzdan dosyası ve `.bitcoin/` klasörü repoya girmez.
6. **Node.js LTS** (CI'da tarayıcı testlerini yerelde de denemek için): `https://nodejs.org`. Kontrol: `node --version`.

## 4. Görevler

### 4.1 Önce: proposal'da yapılmış görünen işler

Proposal'ın work log'unda aşağıdaki işler yapılmış olarak kayıtlı, ama repoda hiçbirinin çıktısı ya da
kanıtı yok. Bu işler **yapılmamış sayılır** ve modül görevlerinden önce, sıfırdan yapılır. Eski kayda
dayanarak "bu zaten var" deme; çıktı `main`'de değilse yoktur (`05_PIPELINE.md` bölüm 1.1).

| No | Görev | Çıktı ve kabul ölçütü | Eski kayıt | Bitiş |
| --- | --- | --- | --- | --- |
| BRK-R1 | Tasarım özeti: Mastering Bitcoin'in OP_RETURN bölümünü ve Nakamoto makalesinin 3., 7. ve 8. bölümlerini oku; tek bir Merkle kökünün zincire nasıl gittiğini ve `anchor/` dosyalarının bunların hangisini karşıladığını yaz | `docs/analysis/burak-timestamp-design.md`: bir sayfa; her iddia kaynağın bölümüne bağlı | #9 | 22 Kas |
| BRK-R2 | Signet node'u ve test coin'i: bölüm 3'teki 3. ve 4. adımları baştan doğrula | `docs/ops/signet.md`: `getblockchaininfo` çıktısında `chain: signet` ve eşitleme tamam; cüzdan bakiyesi sıfırdan büyük; coin'in hangi faucet'ten ne zaman alındığı. Şifre, cüzdan dosyası, özel anahtar belgede yok | #10 | 23 Kas |

Bu görevler de diğerleri gibi branch → PR → `main` yolundan geçer ve commit'lerinde `Task: BRK-R1 (done)`
biçiminde izlenir. Work log'a iki kayıt girilir (`04_GIT_AKISI.md` bölüm 9.1): yapılan iş için kanıtlı bir **Work** kaydı
ve tablodaki "Eski kayıt" numarasını gösteren bir **Correction** kaydı.

### 4.2 Modül görevleri

| No | Görev | Kabul ölçütü | Bağımlılık | Bitiş |
| --- | --- | --- | --- | --- |
| BRK-0 | İskeletin `main`'e alınması: Erdener'in `TestBranch` PR'ını incele ve merge et. `BURAK_ILERLEME.md` `main`'e girmez; içeriğini `docs/worklog/burak.md`'ye taşı (K-009). `burak` ve `feature/S6-copy-warning` branch'lerini sil | `main`'de `anchor/`, `copywarn/`, `evalset/`; `python -m pytest -q` yeşil | ERD-0 | 21 Kas |
| BRK-1 | Repo düzeni: `main` için branch koruması (PR zorunlu, 1 onay, CI yeşil), `.github/CODEOWNERS` (`02` bölüm 2'deki tablodan), `pyproject.toml`: `[build-system]`, açık paket listesi (`[tool.setuptools] packages`; şu an `pip install -e .` "Multiple top-level packages" hatası veriyor) ve bağımlılık grupları (Arda ile); `.gitignore`'a `data/`, `.env`, `node_modules/` | Korumasız push reddediliyor; PR'da sahipler otomatik reviewer oluyor; temiz bir sanal ortamda `pip install -e ".[dev,all]"` ve ardından `python -m pytest -q` çalışıyor | BRK-0 | 22 Kas |
| BRK-2 | Genel CI (`ci.yml`): Python 3.12, `pip install -e ".[dev,all]"`, `python -m pytest -q`, regtest testi için bitcoind kurulumu, `tests/web/` varsa repo kökünde `node --test` (Node 22 ve üstü `node --test tests/web/` biçimindeki klasör argümanını kabul etmez) | Her push ve PR'da çalışır; regtest testi CI'da atlanmadan geçer | BRK-1 | 23 Kas |
| BRK-3 | Test vektörleri: `python -m anchor.vectors` → `tests/vectors/merkle_vectors.json` (1, 2, 3, 5, 8 yapraklı ağaçlar; her yaprağın path'i ve kökü; bozulmuş path, yanlış kök, yanlış taraf için beklenen `false`) ve bir örnek çift: `tests/vectors/sample_note.txt` + `tests/vectors/sample_proof.json` | Aynı dosyayı hem `tests/anchor/` hem Erdener'in `tests/web/` testi okur ve ikisi de geçer. Repo kökünde `.gitattributes` dosyasında `tests/vectors/* -text` satırı var: Windows'ta Git satır sonlarını değiştirmez, `sample_note.txt`'nin hash'i her bilgisayarda aynı kalır | — | 23 Kas |
| BRK-4 | `anchor/` bakımı: `NAMESPACE`'i `core.ns`'ten içe aktar; dosya başlıklarını ve `NP-CONTRACT` işaretlerini ekle (`03` bölüm 2–3); varsayılan yolları `data/` altına al | Testler yeşil; proof çıktısı değişmemiş | ARD-0 | 24 Kas |
| BRK-5 | Signet'te ilk gerçek günlük timestamp: birkaç test hash'i kuyruğa al, `python -m anchor.daily` çalıştır | Onaylı bir signet txid; üretilen proof `verify_offline` ve `verify_on_chain`'den geçer; txid ve adımlar `docs/ops/signet.md`'de | BRK-R2; K-001 kapanmış olmalı | 25 Kas |
| BRK-6 | K-008: proof sayfası için public signet API adayını doğrula (işlemin çıktıları ve blok zamanı tarayıcıdan okunabiliyor mu) ve Erdener'e bildir | `07_KARARLAR.md` K-008 kapatılır | BRK-5 | 25 Kas |
| BRK-7 | Zamanlama: her gün 23:00'te `anchor.daily`, ardından `register.sync_proofs` (macOS/Linux: cron; Windows: Görev Zamanlayıcı). İşletim kılavuzu: node kapalıysa, bakiye bittiyse, işlem takıldıysa ne yapılır. Yedek: `docs/ops/demo-regtest.md` | Art arda 3 gün kendiliğinden timestamp; kılavuzdaki her durum bir kez denenmiş | BRK-5, ARD-6 | 30 Kas |
| BRK-8 | Ölçümler: `python -m anchor.report` → O1 (24 saat içinde geçerli proof'u olan notların oranı) ve O6'nın zincir kısmı (çalışmadaki her OP_RETURN çözülür, 32 byte dışı sayılır) | JSON rapor; Emine'nin değerlendirme raporuna girer | BRK-7 | 4 Ara |
| BRK-9 | Sürümler: `v0.3.0` (27 Kas), `v0.9.0` (4 Ara), `v1.0.0` (11 Ara); her biri için kısa sürüm notu | Etiketler GitHub'da; `v1.0.0` sürüm notunda teslim edilen story'ler ve bilinen eksikler | Faz kapıları | 11 Ara |

**Tasarım notları (aracın uyacağı):**

- `anchor/` standart kütüphane dışında bağımlılık almaz; tek istisna `core`'dan içe aktarmadır.
- CI'a hiçbir sır konmaz: signet cüzdanı CI'da kullanılmaz; CI yalnızca regtest ve sahte node ile çalışır.
- Günlük iş yarıda kalırsa bir sonraki çalışmada tamamlanır; bu davranışı bozan değişiklik yapma.
- Proof dosyasına alan eklemek sözleşme değişikliğidir (`02` bölüm 9).

## 5. Başkalarına sağladıkların

| Kime | Ne | Ne zaman |
| --- | --- | --- |
| Herkes | Çalışan `main`, CI, bağımlılık grupları | 22–23 Kas |
| Erdener | `tests/vectors/` ve Merkle kurallarının açıklaması; public signet API adresi | 23 Kas, 25 Kas |
| Arda | `Store.enqueue` (hazır); proof dosyalarının `data/proofs/` altındaki biçimi | hazır |
| Emine | O1 ve O6 ölçümleri | 4 Ara |

## 6. Başkalarından beklediklerin

| Kimden | Ne | Hazır değilse |
| --- | --- | --- |
| Arda | `core.ns.NAMESPACE`; `register.sync_proofs` | Mevcut sabitle devam; BRK-7 bekler |
| Eylem, Arda | K-001 kararı | BRK-5'i regtest'te prova et, signet'e karar çıkınca geç |

## 7. İdari görevler

- **Release manager:** PR kuyruğuna her gün bak. CI yeşil ve onayı olan PR'ı "Create a merge commit" ile
  merge et, branch'i sil. Sahiplik sınırını aşan ya da sabit sözleşmeyi değiştiren PR'ı merge etme; sahibine döndür.
- **Reviewer:** Arda'nın `core/` ve `register/` PR'larını incele. Kendi PR'larını Arda merge eder.
- **Implementation lideri (P07):** `main` kırmızıysa önceliğin onu yeşile çevirmektir; nedenini bul, sahibine bildir.
- **Operation (P12):** signet node'u ve günlük iş pilot boyunca (5–9 Aralık) açık kalmalı.
- Değerlendirme seti için en az 9 kendi notunu Emine'ye ver.

## 8. Work log için tipik process'ler

P07 (kod), P09 (regtest ve vektör testleri), P10 (CI, sürüm, branch düzeni), P12 (node ve günlük iş).
