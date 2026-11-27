# 01 — Proje: amaç, kapsam, hedefler

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: NoteProof'un **ne olduğunu, ne yaptığını ve ne yapmadığını** tanımlamak.
Kaynak: `proposal/proposal.json` (SEN0401, 2026-2027 Güz, onaylı proposal). Bu dosya ile proposal
çelişirse proposal geçerlidir; çelişkiyi üyeye bildir.

## 1. Tek cümleyle

NoteProof, öğrencilerin kendi ders notlarını kaydettiği bir arşivdir: her notun SHA-256 hash'i günde
bir kez Bitcoin signet'e zaman damgası olarak yazılır, bir yapay zekâ notu ortak bir ders ve konu
sözlüğüne göre etiketler, okuyucular notları konuya göre bulur ve bir notu kimin önce kaydettiğini
arşive güvenmeden kontrol edebilir.

## 2. Kimin için

| Kim | Ne yapar |
| --- | --- |
| **Müşteri:** İstanbul Kültür Üniversitesi Yazılım Mühendisliği 3. ve 4. sınıf öğrencileri | Arşivin sahibidir, yükleme kurallarına karar verir |
| **Note author** (not yazarı) | Not yükler, AI'ın önerdiği ders ve konuları onaylar, zaman damgası kanıtı alır |
| **Note reader** (not okuyucu) | Ders ve konuya göre not arar, notu kimin önce kaydettiğine bakar (çoğunlukla telefondan) |
| **Note verifier** (doğrulayıcı) | Bir notun proof sayfasını açar, ne zaman ve kim tarafından kaydedildiğini kontrol eder |

Çözülen sorun (16 Ekim 2026 anketi, 20 öğrenci): notlar WhatsApp gruplarına ve fotoğraflara dağılmış
durumda; 20 öğrencinin 5'inin notu izinsiz ya da isimsiz paylaşılmış; bir konudaki notu bulmak medyan
10–20 dakika sürüyor; kimin notu önce yazdığı kanıtlanamıyor.

## 3. Sistem ne yapar

Proposal'daki aktivite modeli. Her adımın sahibi `02_MIMARI_SOZLESMELER.md` bölüm 2'dedir.

**A. Not kaydı**

1. Yazar notu yükler (PDF, fotoğraf ya da metin).
2. Kayıt servisi dosya türünü ve boyutunu kontrol eder; uygun değilse nedenini söyleyerek reddeder.
3. Notun SHA-256 hash'ini hesaplar. Hash zaten kayıtlıysa önceki kaydı ve proof'unu gösterir, biter.
4. Paralel olarak: (4a) AI tagger metni çıkarır, SKOS sözlüğünden ders ve konu ile iki cümlelik özet
   önerir; (4b) kopya denetimi metni önceki notlarla karşılaştırır.
5. Yazar önerileri ve varsa benzer önceki notu görür.
6. Yazar her etiketi onaylar ya da düzeltir. Vazgeçerse **hiçbir şey kaydedilmez**.
7. pySHACL onaylanan etiketleri shape'lere göre doğrular; geçersizse ihlaller gösterilir, 6. adıma dönülür.
8. Benzer önceki not bulunduysa not "possible copy" olarak işaretlenir ve önceki notun proof'una bağlanır.
9. Not ve PROV-O kaydı saklanır, hash kuyruğa girer; yazar "proof bekleniyor" görür.

**B. Günlük zaman damgası (her gün 23:00)**

10. Timestamp servisi günün kuyruktaki hash'lerini toplar; kuyruk boşsa biter.
11. Merkle tree'yi kurar, 32 byte'lık kökü bir OP_RETURN çıktısına koyar.
12. İşlemi Bitcoin Core üzerinden signet'e gönderir, bir onay bekler; 6 blokta onay yoksa fee'yi artırır.
13. txid'yi, blok yüksekliğini ve her notun Merkle path'ini saklar, notları "timestamped" yapar.

**C. Bulma ve kontrol**

14. Okuyucu ders ve konuya göre arar; arama alt konuları da kapsar.
15. Okuyucu not kartını açar: yazar (takma ad), tarih, proof rozeti.
16. Proof sayfasında tarayıcı dosyanın hash'ini yeniden hesaplar, Merkle path'i yürür, bloğu public bir signet node'undan alır.
17. Hash ve kök eşleşirse "kanıtlandı" ve blok zamanı; eşleşmezse "kayıtlı dosya değil".

## 4. Kapsamdakiler (deliverable'lar)

| No | Deliverable | Alan |
| --- | --- | --- |
| D1 | Her notu SHA-256 ile hash'leyen, kimin ne zaman kaydettiğini PROV-O ile tutan kayıt servisi | A1 |
| D2 | Bitcoin signet'te günlük Merkle kökü zaman damgası ve her not için Merkle path kanıtı | A1 |
| D3 | Zincirde yalnızca 32 byte'lık kök: not içeriği, isim, öğrenci numarası yok | A1 |
| D4 | schema.org üzerine not ontolojisi, ders ve konuların SKOS sözlüğü, SHACL shape'leri | A2 |
| D5 | Notun dersini, konularını ve kısa özetini yazarın onayına sunan AI tagger | A2 |
| D6 | Konuları bilinen 60 not ve 20 planted copy içeren değerlendirme seti | A2 |
| D7 | Alt konuları da bulan konu araması; notlara atıf yapan yanıtlar | A3 |
| D8 | Yeni notu önceki zaman damgalı notlarla karşılaştıran kopya uyarısı | A3 |
| D9 | Bir not dosyasını arşivin sunucusu olmadan Bitcoin işlemine karşı kontrol eden public proof sayfası | A3 |
| D10 | Arama sonuçları ve proof kontrolleri telefonda 3 saniyenin altında | A3 |

## 5. Kapsam dışı — bunları yapma, üye istese de önce uyar

| Yapılmayacak | Neden |
| --- | --- |
| Bitcoin **mainnet** işlemi ve gerçek ücret | Proje signet'te çalışır; testler regtest'te |
| Bir notu **ilk kimin yazdığını** kanıtlama iddiası | Zaman damgası yalnızca dosyanın o anda var olduğunu ve kimin kaydettiğini gösterir |
| İntihal kararı verme, öğrenciyi cezalandırma | Sistem kanıt gösterir; karar insanlarındır |
| Hoca slaytları, kitap sayfaları, başkasının materyali | Arşiv öğrencilerin kendi notları içindir |

Bu maddelerden türeyen, her modül için geçerli yasaklar:

- Zincire 32 byte'lık Merkle kökünden başka hiçbir veri yazılmaz.
- Gerçek isim ve öğrenci numarası hiçbir yerde saklanmaz: grafikte, zincirde, test verisinde, repoda yok. Hesaplar takma adlıdır.
- Yazar onaylamadan hiçbir AI etiketi ya da özeti kaydedilmez.
- Arayüzde ve kodda "kopya", "intihal" hükmü verilmez; ifade her zaman "olası kopya" (possible copy) ve kanıta bağlantıdır.
- Zaman damgalanmış bir not düzenlenmez; yeni sürüm yeni bir nottur (`prov:wasRevisionOf`).
- Ödeme, puan, oyunlaştırma, mesajlaşma, mobil uygulama, gerçek kimlik doğrulama (e-Devlet, okul SSO) gibi proposal'da olmayan özellikler eklenmez.

## 6. Hedefler ve ölçüler

| Goal | Objective | Nasıl ölçülür | Hedef |
| --- | --- | --- | --- |
| G1 Her not, arşivsiz kontrol edilebilen bir kanıt taşır | O1 | Yüklendikten sonra 24 saat içinde Merkle path'i onaylı bir signet işlemine karşı doğrulanan pilot notlarının oranı | %100 |
| G2 Her not ortak sözlükten ders ve konu ile etiketlidir | O2 | Onaylı etiketleri shape'lerden geçen pilot notlarının oranı | %100 |
| G2 | O3 | 60 değerlendirme notunda yazarın düzeltmeden onayladığı AI konu önerilerinin oranı | ≥ %80 |
| G3 Okuyucu konuya göre bulur, kopyalar için uyarılır | O4 | Bir konudaki notu bulmak için gereken medyan süre (pilot, 20 arama) | 15 dk → ≤ 2 dk |
| G3 | O5 | 20 planted copy'den kopya uyarısının yakaladığı oran | ≥ %90 |
| G4 Zincire içerik ya da kişisel veri gitmez; onaysız etiket kaydedilmez | O6 | 32 byte'lık kök dışında veri taşıyan OP_RETURN sayısı + yazarın onaylamadığı kayıtlı etiket sayısı | 0 |

## 7. Story'ler

| No | Epic | Rol | İstek | Kabul kriteri (özet) |
| --- | --- | --- | --- | --- |
| S1 | E1 | Note author | Notumu yükleyip ne zaman kaydettiğimin kanıtını almak | PDF yüklenince SHA-256 hash ve kayıt zamanı görünür; sonraki günlük timestamp'ten sonra signet işlemine bağlı proof |
| S2 | E1 | Note author | Bir günde kaydedilen bütün notların tek Bitcoin işleminde damgalanması | 40 not → tek signet işlemi Merkle kökünü taşır, her notun kendi Merkle path'i var |
| S3 | E2 | Note author | AI'ın dersi ve konuları önermesi, benim onaylamam | Transaction fee notu → SEN0401 ve sözlükten "Transaction fees" önerilir; onaya kadar hiçbir şey kaydedilmez |
| S4 | E2 | Note author | Dersi olmayan ya da konusu bilinmeyen notun durdurulması | Sözlükte olmayan konu onaylanınca not reddedilir, listeden konu seçmesi istenir |
| S5 | E3 | Note reader | Bir konuyu arayınca alt konulardaki notları da bulmak | "Transaction fees" ve "Fee rate" etiketli notlar, SEN0401'de "Transactions" aranınca yazar ve tarihleriyle listelenir |
| S6 | E3 | Note reader | Bir not önceki bir notun kopyasına benziyorsa uyarılmak | Başka öğrencinin bir hafta önce kaydettiği nota neredeyse aynı not yüklenince olası kopya olarak işaretlenir, önceki notun proof'una bağlanır |
| S7 | E3 | Note verifier | Hesap açmadan bir bağlantıdan proof kontrol etmek | Arşiv sunucusu kapalıyken proof sayfası hash'i yeniden hesaplar, Merkle path'i yürür, signet işleminin blok zamanını gösterir |

Epic'ler: E1 "Register and timestamp notes on Bitcoin", E2 "Tag notes with the course knowledge graph",
E3 "Search, copy warnings and proof pages".

Reddetme senaryoları (testleri zorunlu):

- Zaman damgasından sonra tek karakteri değişen dosya → hash eşleşmez, sayfa "kayıtlı dosya değil" der.
- Sözlükte olmayan konu → not reddedilir.

## 8. Definition of Done

Bir iş, aşağıdakilerin hepsi doğruysa bitmiştir:

1. Bütün testler CI'da geçer (GitHub Actions, her push'ta; timestamp testleri için regtest node'u).
2. Notlar shape'lere uyar (kayıt servisinin testlerinde pySHACL).
3. Zincire yalnızca 32 byte'lık kök gider (test çalışmasındaki her OP_RETURN çıktısını çözen test).
4. AI tagger ve kopya uyarısı hedeflerini tutturur (60 notluk değerlendirme seti, CI'da).

## 9. Sözlük

| Terim | Anlamı |
| --- | --- |
| Note | Öğrencinin kendi ders notu dosyası; SHA-256 hash'iyle tanımlanır |
| Registration | Hangi hesabın hangi hash'i ne zaman kaydettiğini tutan PROV-O aktivitesi |
| Topic | Bir dersin konusu olan SKOS kavramı; broader ve narrower bağlantıları vardır |
| Daily timestamp | OP_RETURN çıktısı günün Merkle kökünü taşıyan signet işlemi |
| Proof | Notun Merkle path'i ve txid; herkes bloğa karşı kontrol edebilir |
| CopyWarning | Bir notu, benzerlik skoruyla önceki bir nota bağlayan kayıt |
| signet / regtest | Bitcoin test ağları. signet: gerçek zaman damgaları; regtest: otomatik testler ve yedek demo |

## 10. 20 Kasım 2026 itibarıyla durum

| Parça | Durum |
| --- | --- |
| `proposal/` | `main`'de. 14 work log kaydı, zincir sağlam |
| `anchor/` (Burak) | `burak` branch'inde hazır: Merkle, OP_RETURN, kuyruk, günlük iş, proof, RPC; regtest'te doğrulandı. Signet'te gerçek işlem ve genel CI yok |
| `copywarn/`, `evalset/` (Emine) | `feature/S6-copy-warning` branch'inde hazır: denetleyici, kopya üretici, değerlendirme hattı; sentetik notlarla test ediliyor. 60 gerçek not yok |
| `ontology/`, `shapes/` (Eylem) | Yok |
| `register/`, `core/` (Arda) | Yok |
| `tagger/` (Aleyna) | Yok |
| `web/`, `search/` (Erdener) | Yok |
| Pilot ve kabul (Aysu) | Yok |

Proposal'ın work log'unda yapılmış görünen 14 işin (anket analizi, bölüm listesi, SKOS taslağı, metin çıkarma
karşılaştırması, ilk istem, tasarım okuması, signet node'u, ekran taslakları, README, yöntem karşılaştırması,
test incelemesi) repoda çıktısı yoktur. Bunlar yapılmamış sayılır ve her üyenin dosyasında bölüm 4.1'de
`XXX-R1`, `XXX-R2` görevleri olarak yeniden yer alır.

Üç branch birleştirildiğinde `python -m pytest -q` çıktısı: 60 passed, 1 skipped (bitcoind kurulu değilse).
Proposal'daki 30 Ekim ve 13 Kasım ara teslimleri repoya göre gecikmiştir; güncel takvim `05_PIPELINE.md` bölüm 2'dedir.
