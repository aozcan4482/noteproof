# Signet node'u ve test coin'i

Görev: BRK-R2 · Sahibi: burak · İnceleyen: arda · Durum: sürüyor (senkron devam ediyor, faucet bekleniyor)

Bu belge, günlük zaman damgasının yazılacağı Bitcoin signet node'unun nasıl kurulduğunu ve hazır olduğunun
nasıl doğrulandığını kayda geçirir. Proposal'daki eski kayıt (#10, "signet node'u kuruldu, faucet'ten coin
alındı") için repoda kanıt yoktu; bu iş sıfırdan yapıldı ve kanıtı bu belgedir.

**Bu belgede asla olmayacaklar:** RPC şifresi, cüzdan dosyası, özel anahtar ya da seed. RPC kullanıcı adı da
yazılmaz. Bunlar yalnızca node'un çalıştığı bilgisayarda durur.

## 1. Kurulum

| Ne | Değer |
| --- | --- |
| Yazılım | Bitcoin Core v32.1.0 (`bitcoind`, `bitcoin-cli`), macOS'ta `brew install bitcoin` |
| Veri klasörü | macOS: `~/Library/Application Support/Bitcoin/` (signet verisi `signet/` alt klasöründe) |
| Ağ | signet (mainnet'e bağlanılmaz; `anchor/daily.py` mainnet'i zaten reddeder) |
| RPC portu | 38332 (signet'in varsayılanı) |

`bitcoin.conf` (şifre ve kullanıcı adı burada gösterilmiyor):

```
signet=1
server=1
[signet]
rpcuser=<yerelde seçildi>
rpcpassword=<yerelde seçildi>
rpcport=38332
```

Kullanıcı adı ve şifre rastgele üretildi. Dosyanın izinleri yalnızca sahibine açık (`chmod 600`).

Başlatma ve durdurma:

```
bitcoind -signet -daemon
bitcoin-cli -signet stop
```

## 2. Senkron

Node'un bütün signet zincirini indirip doğrulaması gerekir. Bitene kadar `initialblockdownload` değeri `true`
kalır ve cüzdan bakiyesi tam görünmez.

| Zaman (UTC) | `blocks` / `headers` | `verificationprogress` | `initialblockdownload` |
| --- | --- | --- | --- |
| 2026-11-20 08:51 | 0 / 0 | 0.00 | true (başlatıldı) |
| 2026-11-23 15:38 | 236475 / 332169 | 0.45 | true |
| *bitince eklenecek* | | | **false** |

Not: Node 20 Kasım'da bilgisayar kapandığı için durdu ve 23 Kasım'da kaldığı yerden yeniden başlatıldı.
Senkron sürerken bilgisayarın uyku moduna geçmemesi gerekir.

Kontrol komutu:

```
bitcoin-cli -signet getblockchaininfo
```

## 3. Cüzdan

| Ne | Değer |
| --- | --- |
| Cüzdan adı | `noteproof` (`.env` içindeki `NOTEPROOF_RPC_WALLET` ile aynı) |
| Tür | Descriptor cüzdanı, Bitcoin Core'un varsayılanı |
| Açılışta yükleme | Açık: node her başladığında `noteproof` cüzdanı kendiliğinden yüklenir |
| Faucet adresi | `tb1p60zdl7zrp8uh8h8jj9wz992ta8pwqx8j2e4htj2xf5jsasft9amsy3xpk9` (bech32m) |

Adres herkese açık bir bilgidir; zincirde zaten görünür. Cüzdanın özel anahtarları yalnızca veri klasöründe durur.

Oluşturma komutları:

```
bitcoin-cli -signet createwallet noteproof
bitcoin-cli -signet -rpcwallet=noteproof getnewaddress "faucet" bech32m
```

## 4. Test coin'i (faucet)

| Ne | Değer |
| --- | --- |
| Faucet | *eklenecek: hangi signet faucet'i kullanıldı* |
| İstek zamanı (UTC) | *eklenecek* |
| Gelen işlem (txid) | *eklenecek* |
| Bakiye | *senkron bitince eklenecek; sıfırdan büyük olmalı* |

Bakiye kontrolü:

```
bitcoin-cli -signet -rpcwallet=noteproof getbalances
```

## 5. BRK-R2 kabul ölçütü

- [ ] `getblockchaininfo` çıktısında `chain: signet` ve `initialblockdownload: false`
- [ ] Cüzdan bakiyesi sıfırdan büyük
- [ ] Coin'in hangi faucet'ten ne zaman alındığı yazılı
- [x] Şifre, cüzdan dosyası ve özel anahtar belgede yok
