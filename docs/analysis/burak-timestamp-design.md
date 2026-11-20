# Zaman damgası tasarım özeti: tek bir Merkle kökü zincire nasıl gider

Görev: BRK-R1 · Sahibi: burak · İnceleyen: arda · Durum: taslak (1. yarı)

Bu belge, NoteProof'un Bitcoin zaman damgası tasarımının hangi kaynağa dayandığını ve `anchor/`
dosyalarının bu kaynakların hangi kısmını karşıladığını özetler. Her iddia, köşeli parantez içinde
kaynağın bölümüne bağlanır.

Not: Belgede adı geçen `anchor/` ve `tests/anchor/` dosyaları şu an `TestBranch`'te duruyor. `main`'e
BRK-0 ile girecekler.

Kaynaklar:

- **[N]** Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System.* Bölüm numaraları makaledeki gibidir.
- **[MB]** Antonopoulos, A. M. & Harding, D. A. (2023). *Mastering Bitcoin*, 3. baskı. O'Reilly. (2. yarıda)

## 1. Zaman damgası sunucusu — [N §3]

**Kaynak ne diyor.**

- Zaman damgası sunucusu, damgalanacak bir grup öğenin hash'ini alır ve bu hash'i geniş çapta yayımlar. [N §3]
- Yayımlanan hash, o verinin o anda var olduğunu kanıtlar; çünkü veri o anda var olmasaydı hash'i
  hesaplanıp yayımlanamazdı. [N §3]
- Her zaman damgası, kendi hash'ine bir önceki zaman damgasını da katar. Böylece bir zincir oluşur ve
  her yeni damga, kendinden öncekileri güçlendirir. [N §3]
- Bu zinciri tek bir kişinin değil, herkesin değiştiremeyeceği bir kayda dönüştüren şey iş kanıtıdır
  (proof-of-work): bir bloğu değiştirmek, o blokla ondan sonraki bütün blokların işini yeniden yapmayı
  gerektirir. [N §4]

**NoteProof'ta karşılığı.**

| Kaynaktaki kavram | NoteProof | Dosya |
| --- | --- | --- |
| Damgalanacak "öğe grubu" | Bir gün içinde kuyruğa giren not hash'leri | `anchor/store.py` (`enqueue`, `pending_hashes`) |
| Grubun hash'ini almak | Günün hash'lerinden tek bir Merkle kökü hesaplamak | `anchor/merkle.py` (`build_tree`) |
| Hash'i "geniş çapta yayımlamak" | Kökü bir signet işleminin OP_RETURN çıktısına yazıp ağa göndermek | `anchor/daily.py` (`broadcast_root`) |
| Önceki damgaya bağlanmak | Bunu biz yapmıyoruz; Bitcoin'in blok zinciri yapıyor. İşlemimiz bir bloğa girdiği anda, o bloktan sonraki her blok damgamızı güçlendirir | — |

Proposal'ın "Blockchain design" bölümündeki gerekçe de budur: arşivi çalıştıran kişi kendi
veritabanındaki tarihleri değiştirebilir, ama bloğa girmiş bir işlemi değiştiremez. [N §3, §4]

## 2. Merkle tree ile yer kazanmak — [N §7]

**Kaynak ne diyor.**

- Bir bloktaki işlemler bir Merkle tree'de hash'lenir ve blok başlığına yalnızca ağacın kökü konur. [N §7]
- Ağacın iç dalları sonradan atılabilir; kökün kendisi değişmediği için blok hash'i bozulmaz. [N §7]
- Makale bu tekniği zaman damgası literatürüne dayandırır: Haber ve Stornetta (1991) ile Bayer, Haber ve
  Stornetta (1993). Proposal'ın kaynakçasında 3. ve 4. sırada geçen çalışmalar bunlardır. [N §7, kaynakça]

**NoteProof'ta karşılığı.**

- Bitcoin her işlemi ayrı ayrı zincire yazmaz; biz de her notu ayrı yazmayız. Günün bütün not hash'leri
  bir Merkle tree'de birleşir ve zincire **yalnızca kök** gider. 40 not da 4.000 not da tek işlem,
  tek 32 byte'tır (story S2). `anchor/merkle.py`, `anchor/opreturn.py`
- Bilinçli farklar. Bunlar sabit sözleşmedir (`02` bölüm 5.5) ve proof sayfası da aynısını uygular:
  - **Önekler.** Yaprak hash'i `SHA256(0x00 || not_hash)`, iç düğüm hash'i `SHA256(0x01 || sol || sağ)`.
    Bitcoin'in blok ağacında bu ayrım yoktur. Öneksiz bir ağaçta iki hash'in birleşimi bir yaprakmış gibi
    gösterilebilir; önek bunu engeller. `tests/anchor/test_merkle.py::test_internal_node_cannot_pose_as_leaf`
  - **Tek kalan düğüm.** Bitcoin, bir seviyede tek sayıda düğüm kalırsa sonuncuyu kopyalar. Bu kural farklı
    iki listenin aynı kökü vermesine izin verir (CVE-2012-2459). Biz tek kalan düğümü kopyalamadan bir üst
    seviyeye taşırız. `test_odd_node_is_promoted_not_duplicated`
  - **Hash.** Bitcoin çift SHA-256 kullanır; biz tek SHA-256 kullanırız. Kanıt için yeterlidir ve not
    hash'iyle (SHA-256) aynı algoritmadır.

## 3. Basitleştirilmiş doğrulama (SPV) — [N §8]

**Kaynak ne diyor.**

- Bir işlemi doğrulamak için tam bir node çalıştırmak gerekmez. Kullanıcı en uzun zincirin blok
  başlıklarını tutar ve işlemi bloğun zaman damgasına bağlayan Merkle dalını (Merkle branch) alır. [N §8]
- Kullanıcı işlemi kendisi denetleyemez; ama onu zincirdeki yerine bağlayarak ağın işlemi kabul ettiğini
  görür. Ondan sonra eklenen her blok bu kabulü pekiştirir. [N §8]

**NoteProof'ta karşılığı.**

- Bir notun proof'u, notun hash'ini günün köküne bağlayan Merkle path'tir. Yanında kökü taşıyan işlemin
  `txid`'si ve bloğun hash'i, yüksekliği ve zamanı bulunur. Proof dosyasının alanları `02` bölüm 6'da
  sabittir. `anchor/proof.py` (`build_proof`)
- Doğrulama iki adımlıdır:
  1. **Çevrimdışı:** dosyanın SHA-256'sı `noteHash` ile eşleşiyor mu, path yürüyünce `merkleRoot`'a
     varılıyor mu? İnternet gerekmez. `verify_offline`; tarayıcıdaki karşılığı Erdener'in
     `web/js/verify.js`'idir.
  2. **Zincirde:** `txid`'li işlem `blockHash`'teki blokta mı ve OP_RETURN çıktısı bu kökü taşıyor mu?
     `verify_on_chain`
- **Bilinen sınır.** [N §8]'deki SPV, işlemin bloğa girdiğini de bir Merkle dalıyla kanıtlar ve yalnızca
  blok başlıklarına güvenir. Bizim 2. adımımız ise işlemi ve bloğu bir node'a ya da public bir signet
  API'sine sorar; yani o kaynağa güvenir. Proof'a işlemin bloktaki Merkle dalını da eklemek tam SPV'ye
  yaklaştırırdı, ama bu proof dosyasına alan eklemek demektir ve sözleşme değişikliği gerektirir
  (`02` bölüm 9). Şimdilik yalnızca not olarak kalıyor; tarayıcı tarafındaki kaynak K-008 ile seçilecek.

## 4. OP_RETURN: kök işleme nasıl konur — [MB]

*2. yarıda yazılacak (21 Kasım): Mastering Bitcoin'in OP_RETURN bölümü, `6a 20 <32 byte>` script'i,
neden yalnızca 32 byte ve `anchor/opreturn.py` ile `anchor/daily.py`'deki işlem kurma adımları.*

## 5. Uçtan uca: bir notun kökü zincire nasıl gider

*2. yarıda yazılacak (21 Kasım): yukarıdaki bölümleri tek akışta birleştiren adım listesi ve
`anchor/` dosyalarının her adımı karşılayıp karşılamadığını gösteren özet tablo.*
