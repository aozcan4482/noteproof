# SEN0401 ders sözlüğünün kapsamı (EYL-R1, EYL-R2)

Hazırlayan: Eylem Sarıbal (`eylem`) · Tarih: 2026-11-26 · Reviewer: Aleyna Cebeci (`aleyna`)

Bu belge `ontology/courses.ttl` dosyasının kaynağıdır. Dersin konuları, dersin ana kaynağı olan kitabın
bölümlerinden çıkarıldı:

> Antonopoulos, A. M. & Harding, D. A. (2023). *Mastering Bitcoin: Programming the Open Blockchain*, 3. baskı. O'Reilly.

## 1. Kimlik kuralları

- Ders: `Course_<KOD>`; konu: `Topic_<PascalCase>` (`02_MIMARI_SOZLESMELER.md` bölüm 3).
- Kimlikler İngilizce, boşluksuz, Türkçe karakter yok.
- Her kavramın iki etiketi var: `@tr` (arayüz bunu gösterir) ve `@en` (tagger istemi ikisini de görür).
- Dersin altında en çok üç düzey konu: konu → alt konu → alt-alt konu.
- Kimlikler ders adıyla öneklenmez ama başka derslerle çakışabilecek genel adlar (ör. "Introduction")
  belirginleştirilir: pilot dersleri eklendiğinde (EYL-8) bütün kimlikler aynı namespace'te durur.
- Bir kimlik `main`'e girdikten sonra yeniden adlandırılmaz; yanlışsa `owl:deprecated` ile işaretlenir.

## 2. EYL-R1 — Kitabın 14 bölümü ve konu kimlikleri

| No | Bölüm adı (kitaptaki gibi) | Konu kimliği | Türkçe etiket | İngilizce etiket | Üst kavram |
| --- | --- | --- | --- | --- | --- |
| 1 | Introduction | `Topic_BitcoinIntroduction` | Bitcoin'e giriş | Introduction to Bitcoin | `Course_SEN0401` |
| 2 | How Bitcoin Works | `Topic_HowBitcoinWorks` | Bitcoin nasıl çalışır | How Bitcoin works | `Course_SEN0401` |
| 3 | Bitcoin Core: The Reference Implementation | `Topic_BitcoinCore` | Bitcoin Core: referans uygulama | Bitcoin Core: the reference implementation | `Course_SEN0401` |
| 4 | Keys and Addresses | `Topic_KeysAndAddresses` | Anahtarlar ve adresler | Keys and addresses | `Course_SEN0401` |
| 5 | Wallet Recovery | `Topic_WalletRecovery` | Cüzdan kurtarma | Wallet recovery | `Course_SEN0401` |
| 6 | Transactions | `Topic_Transactions` | İşlemler | Transactions | `Course_SEN0401` |
| 7 | Authorization and Authentication | `Topic_AuthorizationAndAuthentication` | Yetkilendirme ve kimlik doğrulama | Authorization and authentication | `Course_SEN0401` |
| 8 | Digital Signatures | `Topic_DigitalSignatures` | Dijital imzalar | Digital signatures | `Course_SEN0401` |
| 9 | Transaction Fees | `Topic_TransactionFees` | İşlem ücretleri | Transaction fees | `Topic_Transactions` (bkz. karar 3.1) |
| 10 | The Bitcoin Network | `Topic_BitcoinNetwork` | Bitcoin ağı | The Bitcoin network | `Course_SEN0401` |
| 11 | The Blockchain | `Topic_Blockchain` | Blokzincir | The blockchain | `Course_SEN0401` |
| 12 | Mining and Consensus | `Topic_MiningAndConsensus` | Madencilik ve uzlaşı | Mining and consensus | `Course_SEN0401` |
| 13 | Bitcoin Security | `Topic_BitcoinSecurity` | Bitcoin güvenliği | Bitcoin security | `Course_SEN0401` |
| 14 | Second-Layer Applications | `Topic_SecondLayerApplications` | İkinci katman uygulamaları | Second-layer applications | `Course_SEN0401` |

Ders kavramı: `Course_SEN0401` · `skos:notation "SEN0401"` · "Özel Konular: Blokzincir"@tr ·
"Special Topics: Blockchain"@en.

## 3. Kararlar

### 3.1 "Transaction Fees" bölümü `Topic_Transactions`'ın altında

3. baskıda "Transaction Fees" ayrı bir bölümdür (9. bölüm). Ancak S5'in kabul kriteri, SEN0401'de
"Transactions" arandığında "Transaction fees" ve "Fee rate" etiketli notların da bulunmasını ister; EYL-2'nin
kabul ölçütü de `Topic_Transactions` → `Topic_TransactionFees` → `Topic_FeeRate` zincirini şart koşar.
Bu yüzden 9. bölüm sözlükte dersin doğrudan altında değil, `Topic_Transactions`'ın alt konusu olarak durur.
Anlam açısından da tutarlıdır: ücret, bir işlemin girdileri ile çıktıları arasındaki farktır.

### 3.2 1. bölümün kimliği `Topic_BitcoinIntroduction`

`Topic_Introduction` her ders için anlamsız ve ileride eklenecek derslerle çakışır. Kimlik belirginleştirildi.

### 3.3 Alt konular yalnızca S5'in gerektirdiği yerde

Bu aşamada yalnızca Transactions bölümü alt konulara ayrıldı (EYL-R2). Diğer bölümlerin alt konuları,
değerlendirme setindeki ve pilottaki notlar gerçekten gerektirirse eklenir. Az ama kalıcı kimlik, çok ama
sonradan `owl:deprecated` yapılacak kimlikten iyidir.

## 4. EYL-R2 — Transactions hiyerarşisi

```
Course_SEN0401                         Özel Konular: Blokzincir
└── Topic_Transactions                 İşlemler                        (6. bölüm)
    ├── Topic_TransactionInputs        İşlem girdileri
    ├── Topic_TransactionOutputs       İşlem çıktıları
    └── Topic_TransactionFees          İşlem ücretleri                 (9. bölüm)
        ├── Topic_FeeRate              Ücret oranı
        └── Topic_FeeBumping           Ücret artırma (RBF, CPFP)
```

| Kimlik | `skos:broader` | `skos:narrower` | Türkçe etiket | İngilizce etiket |
| --- | --- | --- | --- | --- |
| `Topic_Transactions` | `Course_SEN0401` | `Topic_TransactionInputs`, `Topic_TransactionOutputs`, `Topic_TransactionFees` | İşlemler | Transactions |
| `Topic_TransactionInputs` | `Topic_Transactions` | — | İşlem girdileri | Transaction inputs |
| `Topic_TransactionOutputs` | `Topic_Transactions` | — | İşlem çıktıları | Transaction outputs |
| `Topic_TransactionFees` | `Topic_Transactions` | `Topic_FeeRate`, `Topic_FeeBumping` | İşlem ücretleri | Transaction fees |
| `Topic_FeeRate` | `Topic_TransactionFees` | — | Ücret oranı | Fee rate |
| `Topic_FeeBumping` | `Topic_TransactionFees` | — | Ücret artırma (RBF, CPFP) | Fee bumping (RBF, CPFP) |

Derinlik: `Topic_FeeRate` ve `Topic_FeeBumping` üçüncü düzeydedir; bu, izin verilen en derin düzeydir.

## 5. Sonuç: sözlükteki bütün kimlikler

1 ders, 18 konu: 14 bölüm konusu ve 4 alt konu (`Topic_TransactionInputs`, `Topic_TransactionOutputs`,
`Topic_FeeRate`, `Topic_FeeBumping`).
Güncel liste her zaman `python -m ontology.list` komutuyla alınır; bu belge ile dosya çelişirse `ontology/courses.ttl` geçerlidir.
