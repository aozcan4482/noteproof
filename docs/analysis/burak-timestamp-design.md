# Zaman damgası tasarım özeti: tek bir Merkle kökü zincire nasıl gider

Görev: BRK-R1 · Sahibi: burak · İnceleyen: arda · Durum: tamam

Bu belge, NoteProof'un Bitcoin zaman damgasının hangi kaynağa dayandığını ve `anchor/` dosyalarının
bunun hangi kısmını karşıladığını özetler. Her iddia köşeli parantez içinde kaynağın bölümüne bağlanır.
Adı geçen `anchor/` ve `tests/anchor/` dosyaları şu an `TestBranch`'te; `main`'e BRK-0 ile girecekler.

- **[N]** Nakamoto, S. (2008). *Bitcoin: A Peer-to-Peer Electronic Cash System.* Bölüm numaraları makaledeki gibidir.
- **[MB]** Antonopoulos, A. M. & Harding, D. A. (2023). *Mastering Bitcoin*, 3. baskı. "Data Recording Output (OP_RETURN)" bölümü.
- **[BC]** Bitcoin Core v32.1.0, `bitcoind -help` çıktısı: `-datacarrier` (varsayılan 1) ve `-datacarriersize` (varsayılan 100000, birden çok çıktıya izin verir) seçenekleri.

## 1. Kaynaklar ne diyor

**Zaman damgası sunucusu [N §3].** Bir grup öğenin hash'i alınır ve geniş çapta yayımlanır. Yayımlanan
hash, verinin o anda var olduğunu kanıtlar. Her damga bir öncekini de içerdiği için zincir oluşur ve her
yeni damga öncekileri güçlendirir. Zinciri kimsenin tek başına değiştiremediği bir kayıt yapan şey iş
kanıtıdır: bir bloğu değiştirmek, ondan sonraki bütün blokların işini yeniden yapmayı gerektirir [N §4].

**Merkle tree [N §7].** Bir bloktaki işlemler bir Merkle tree'de hash'lenir; blok başlığına yalnızca kök
girer. Teknik, Haber ve Stornetta (1991) ile Bayer, Haber ve Stornetta'nın (1993) zaman damgası
çalışmalarına dayanır; ikisi de proposal'ın kaynakçasında var.

**Basit doğrulama, SPV [N §8].** Doğrulayıcının tam node'a ihtiyacı yoktur: blok başlıklarını ve işlemi
bloğa bağlayan Merkle dalını tutması yeter. İşlemi zincirdeki yerine bağlayınca ağın onu kabul ettiğini
görür; sonraki her blok bunu pekiştirir.

**OP_RETURN [MB].** OP_RETURN çıktısı ispatlanabilir biçimde harcanamaz. Bu yüzden node'lar onu harcanmamış
çıktılar kümesinde (UTXO) tutmaz ve zincire küçük veri yazmanın zararsız yolu budur. Kitap bu çıktıyı tam da
bir belgenin hash'ini kaydedip var olduğunu kanıtlamak için örnekler. Kitap yazıldığında node'ların varsayılan
politikası 80 byte'a kadar veri ve işlem başına tek OP_RETURN çıktısına izin veriyordu. Kullandığımız Bitcoin
Core v32.1.0'da ise varsayılan sınır toplam 100.000 byte ve birden çok veri çıktısına izin veriliyor [BC].
Bizim 34 byte'lık script'imiz her iki politikaya da sığar.

## 2. NoteProof bunları nasıl uyguluyor: bir notun kökü zincire nasıl gider

Adımlar proposal'ın aktivite modelindeki numaraları taşır.

1. **Kuyruk (adım 9).** Kayıt servisi onaylanmış notun SHA-256 hash'ini `Store.enqueue` ile kuyruğa
   koyar. Bu, Arda'nın modülüyle tek temas noktasıdır (`02` bölüm 5.5). `anchor/store.py`
2. **Grubu toplamak (adım 10) [N §3].** Günlük iş her gün 23:00'te kuyrukta bekleyen bütün hash'leri alır;
   "damgalanacak öğe grubu" budur. `anchor/daily.py` (`run_daily`)
3. **Tek kök (adım 11) [N §7].** Hash'ler bir Merkle tree'de birleşir; 40 not da 4.000 not da tek bir
   32 byte'lık kök verir (story S2). `anchor/merkle.py` (`build_tree`). Bitcoin'den bilinçli farklar
   sabit sözleşmedir (`02` bölüm 5.5):
   - yaprak `SHA256(0x00 || hash)`, iç düğüm `SHA256(0x01 || sol || sağ)`: önek, iki hash'in birleşiminin
     yaprak gibi gösterilmesini engeller;
   - tek kalan düğüm kopyalanmaz, yukarı taşınır: Bitcoin'in kopyalama kuralı farklı iki listeye aynı kökü
     verdirebilir (CVE-2012-2459);
   - çift değil tek SHA-256 kullanılır; not hash'iyle aynı algoritmadır.
4. **Kökü işleme koymak (adım 11) [MB].** Çıktının script'i tam 34 byte'tır: `6a` (OP_RETURN), `20`
   (32 byte koy) ve kök. Başka bir biçim reddedilir. Zincire not içeriği, isim ya da öğrenci numarası gitmez
   (KVKK, D3). `anchor/opreturn.py` (`build_script`, `tx_holds_only_root`)
5. **Yayımlamak (adım 12) [N §3].** İşlem cüzdandan fonlanır, imzalanır, gönderilmeden önce çözülüp yalnızca
   kökü taşıdığı kontrol edilir ve signet'e gönderilir. 6 blokta onay gelmezse fee artırılır. Mainnet
   reddedilir. `anchor/daily.py` (`broadcast_root`, `wait_for_confirmation`, `check_network`)
6. **Zincirin güvencesi [N §3, §4].** İşlem bir bloğa girince damgayı arşiv değil Bitcoin'in iş kanıtı korur;
   arşivi çalıştıran kişi kendi veritabanındaki tarihi değiştirebilir, bloğu değiştiremez.
7. **Proof (adım 13) [N §8].** Her not için Merkle path, kök, `txid` ve blok bilgisi bir JSON-LD dosyasına
   yazılır; alanlar `02` bölüm 6'da sabittir. `anchor/proof.py` (`build_proof`)
8. **Doğrulama (adım 16–17) [N §8].** Önce çevrimdışı: dosyanın hash'i `noteHash`'e eşit mi, path köke
   varıyor mu (`verify_offline`; tarayıcıda Erdener'in `web/js/verify.js`'i). Sonra zincirde: işlem o blokta
   mı ve OP_RETURN'ü bu kökü taşıyor mu (`verify_on_chain`).

## 3. Özet: kaynak → kod → kanıt

| Kaynaktaki fikir | Karşılayan dosya | Testi | Durum |
| --- | --- | --- | --- |
| Grubun hash'ini yayımlamak [N §3] | `daily.py` | `test_40_notes_one_transaction_and_valid_proofs` | Karşılanıyor (regtest); signet'te ilk gerçek işlem BRK-5 |
| Merkle tree, yalnızca kök [N §7] | `merkle.py` | `test_every_path_verifies`, `test_internal_node_cannot_pose_as_leaf`, `test_odd_node_is_promoted_not_duplicated` | Karşılanıyor |
| OP_RETURN ile veri kaydı [MB] | `opreturn.py` | `test_only_32_bytes_allowed`, `test_only_32_byte_roots_reach_the_chain` | Karşılanıyor |
| Merkle dalıyla doğrulama [N §8] | `proof.py` | `test_changed_file_is_not_the_registered_file`, `test_40_notes_anchored_on_regtest` | Kısmen (aşağıya bakın) |

**Bilinen sınır.** [N §8]'deki SPV, işlemin bloğa girdiğini de bir Merkle dalıyla kanıtlar ve yalnızca blok
başlıklarına güvenir. Bizim zincir kontrolümüz ise işlemi bir node'a ya da public bir signet API'sine sorar;
yani o kaynağa güvenir. İşlemin bloktaki dalını proof'a eklemek bu güveni kaldırırdı, ama bu proof dosyasına
alan eklemek demektir ve sözleşme değişikliği gerektirir (`02` bölüm 9). Tarayıcının kullanacağı kaynak
K-008 ile seçilecek (BRK-6).
