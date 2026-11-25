# Signet node'u ve test coin'i

Görev: BRK-R2 · Sahibi: burak · İnceleyen: arda · Durum: tamam

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

| Zaman (UTC) | `chain` | `blocks` / `headers` | `verificationprogress` | `initialblockdownload` |
| --- | --- | --- | --- | --- |
| 2026-11-20 08:51 | signet | 0 / 0 | 0.00 | true (başlatıldı) |
| 2026-11-23 15:38 | signet | 236475 / 332169 | 0.45 | true |
| 2026-11-24 08:59 | **signet** | 332266 / 332266 | 1.00 | **false** (senkron tamam) |

Not: Node 20 Kasım'da ve 23–24 Kasım gecesi bilgisayar kapandığı için durdu; her seferinde kaldığı yerden
yeniden başlatıldı. Node kapalıyken günlük iş çalışamaz; işletim kılavuzu BRK-7'de yazılacak.

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
| Faucet | `alt.signetfaucet.com` (ana site `signetfaucet.com` 2026-11-23'te yanıt vermiyordu) |
| İstek zamanı (UTC) | 2026-11-23, yaklaşık 15:45 |
| Onaylanan işlem (txid) | `0c4af8b479c714196b0df09b99e945893f349b9276bfa34e811dc9cb76bb39a5` · 1.858.050 sat · blok 332171 · 2026-11-23 15:50:37 UTC |
| Bakiye | 0,0185805 signet BTC (`trusted`, 2026-11-24 08:59 UTC) |

Not: Faucet sayfası istekten hemen sonra `b325287d…6a6175d8` kimlikli, 3.353.611 sat'lık onaysız bir işlem
gösterdi. Bu işlem bloğa girmedi; beş dakika sonra yukarıdaki işlem onaylandı. Faucet'in ilk işlemini başka
bir işlemle değiştirdiği düşünülüyor; public API istek sınırına takıldığı için bu doğrulanamadı. Cüzdana
onaylı olarak gelen tek işlem yukarıdakidir.

Bakiye kontrolü:

```
bitcoin-cli -signet -rpcwallet=noteproof getbalances
```

## 5. BRK-R2 kabul ölçütü

- [x] `getblockchaininfo` çıktısında `chain: signet` ve `initialblockdownload: false` (bölüm 2)
- [x] Cüzdan bakiyesi sıfırdan büyük: 0,0185805 signet BTC (bölüm 4)
- [x] Coin'in hangi faucet'ten ne zaman alındığı yazılı (bölüm 4)
- [x] Şifre, cüzdan dosyası ve özel anahtar belgede yok
