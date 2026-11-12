# Burak — İlerleme Günlüğü

Bu dosya yalnızca `burak` branch'inde tutulur; `main`'e taşınmaz.
Her tamamlanan iş tarih ve kısa açıklamayla madde madde eklenir.

**Sorumluluklarım:** Bitcoin timestamp service (anchor/), registration service yedeği, repo ve release yönetimi, CI, v1.0.0 release.
**Yaklaşan teslim:** 2026-11-13 — Signet üzerinde günlük timestamp ve public proof page.

---

## Dosya rehberi — hangi dosya ne işe yarıyor?

Okuma sırası önerisi: `merkle.py` → `opreturn.py` → `store.py` → `daily.py` → `proof.py` → `rpc.py`.

### `anchor/` — Bitcoin timestamp servisi (benim modülüm)

| Dosya | Ne yapıyor |
| --- | --- |
| `anchor/__init__.py` | Paketin genel açıklaması: 5 adımlık akış ve hangi adımın hangi dosyada olduğu. |
| `anchor/merkle.py` | Merkle tree. Not hash'lerinden 32 byte'lık kökü hesaplar, her not için Merkle path üretir ve path'i doğrular (`build_tree`, `verify_path`). Yaprak için `0x00`, iç düğüm için `0x01` öneki kullanılır; tek kalan düğüm kopyalanmaz, yukarı taşınır. |
| `anchor/opreturn.py` | OP_RETURN çıktısı. Kökü `6a 20 <32 byte>` scriptine çevirir ve bir işlemin yalnızca 32 byte'lık kök taşıyıp taşımadığını kontrol eder (KVKK kuralı). |
| `anchor/store.py` | SQLite kuyruğu. **Arda'nın kayıt servisiyle sözleşme burada:** `Store.enqueue(note_hash_hex)`. Ayrıca batch kayıtları (kök, txid, blok, durum: `built → broadcast → confirmed`) tutulur. |
| `anchor/rpc.py` | Bitcoin Core JSON-RPC istemcisi (bitcoin-cli'nin Python karşılığı). Ayarlar ortam değişkenlerinden okunur: `NOTEPROOF_RPC_URL`, `NOTEPROOF_RPC_USER`, `NOTEPROOF_RPC_PASSWORD`, `NOTEPROOF_RPC_WALLET`. |
| `anchor/daily.py` | Günlük iş (proposal aktivite modeli B, adım 10–13): kuyruğu topla, ağacı kur, işlemi gönder, onay bekle, 6 blokta onay yoksa `bumpfee`, proof dosyalarını yaz. Mainnet'te çalışmayı reddeder. Yarıda kalan batch'leri bir sonraki çalışmada tamamlar. Çalıştırma: `python -m anchor.daily --db noteproof.sqlite --out proofs/` |
| `anchor/proof.py` | Proof dosyası (JSON-LD): `noteHash`, `merklePath`, `merkleRoot`, `txid`, `blockHeight`, `blockHash`, `blockTime`. `verify_offline` dosya + proof ile internetsiz kontrol yapar, `verify_on_chain` ise kökün gerçekten o işlemin OP_RETURN'ünde olduğunu node'dan kontrol eder. |

### `tests/anchor/` — testler

| Dosya | Ne test ediyor |
| --- | --- |
| `test_merkle.py` | 1–101 not için her path'in doğrulandığını; yanlış not, bozulmuş path, yanlış kök ve "iç düğümü yaprak gibi gösterme" saldırısının reddedildiğini. |
| `test_opreturn.py` | Yalnızca 32 byte'lık kökün kabul edildiğini, başka bütün OP_RETURN biçimlerinin reddedildiğini. |
| `test_daily.py` | Sahte node ile bütün akış: 40 not → tek işlem; her proof geçerli; tek karakteri değişen dosya "kayıtlı dosya değil"; boş kuyruk; aynı hash iki kez kuyruğa girmez; mainnet reddi; 6 blok sonra fee bump; yarıda kalan batch'in tamamlanması. |
| `fake_rpc.py` | Testler için sahte Bitcoin node'u (bitcoind olmadan akışı denemek için). |
| `test_regtest.py` | Gerçek `bitcoind -regtest` ile 40 not testi. bitcoind kurulu değilse otomatik atlanır. |

### Kök dizin

| Dosya | Ne yapıyor |
| --- | --- |
| `pyproject.toml` | Proje tanımı ve pytest ayarları. Ek bağımlılık yok, yalnızca standart kütüphane kullanılıyor. |
| `.gitignore` | `__pycache__`, `*.sqlite`, `proofs/` gibi çalışma çıktılarını repoya sokmaz. |

Testleri çalıştırmak için: `python3 -m pytest -q`

---

## Tamamlananlar

### 2026-11-10
- [x] Repo `~/code/noteproof` içine klonlandı, proposal okundu ve görevler çıkarıldı
- [x] `burak` branch'i `main`'den açıldı ve GitHub'a push edildi
- [x] İlerleme günlüğü (`BURAK_ILERLEME.md`) oluşturuldu

### 2026-11-12
- [x] Repo iskeleti: `pyproject.toml`, `.gitignore`, `anchor/` ve `tests/anchor/` klasörleri
- [x] Merkle modülü (`anchor/merkle.py`): kök, path ve doğrulama, testleriyle
- [x] OP_RETURN modülü (`anchor/opreturn.py`): yalnızca 32 byte'lık kök kuralı, testleriyle
- [x] Kuyruk ve batch kayıtları (`anchor/store.py`): `enqueue` sözleşmesi
- [x] Bitcoin Core RPC istemcisi (`anchor/rpc.py`)
- [x] Günlük timestamp işi (`anchor/daily.py`): fee bump, yarıda kalanı tamamlama, mainnet reddi
- [x] Proof JSON-LD ve doğrulama (`anchor/proof.py`)
- [x] Testler: 37 geçti, regtest testi bitcoind olmadığı için atlandı

## Sıradakiler
- [ ] `bitcoind` kurup regtest testini gerçekten çalıştırmak
- [ ] Regtest node'lu GitHub Actions CI
- [ ] Signet'te gerçek bir günlük timestamp atmak (cüzdan + faucet coin)
- [ ] Tarayıcı için JS doğrulama fonksiyonu (Erdener'e), Python ile aynı test vektörleri
- [ ] Proof JSON alanlarını ve `NAMESPACE` IRI'sini Erdener ve Eylem ile sabitlemek
- [ ] `enqueue` sözleşmesini Arda'ya iletmek
