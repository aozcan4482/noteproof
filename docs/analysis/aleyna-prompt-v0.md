# İlk istem (v0) ve dil modeli karşılaştırması

Görev: ALY-R2 (ve ALY-1 / K-005 için ölçüm) · Sahip: aleyna · İnceleyen: eylem, emine · Kural seti sürüm 2.3

Bu belge iki şeyi kaydeder:

1. **ALY-R2:** modelin konularını sözlüğe sınırlayan ilk istem ve üç nottaki sonucu.
2. **ALY-1:** aynı istemle iki aday modelin karşılaştırması ve K-005 için önerilen karar.

Notların içeriği ve modelin ürettiği özetler bu belgede yoktur; yalnızca kimlikler ve sayılar vardır.

## 1. İstem (v0)

İstem kodda tek bir yerdedir: `tagger/suggest.py` (`SYSTEM_PROMPT` ve `build_prompt`). Sözlük isteme her
çağrıda `Vocabulary`'den üretilir, elle yazılmaz.

**Sistem mesajı:**

```
Sen öğrencilerin ders notlarını etiketleyen bir yardımcısın. Notu oku ve aşağıdaki sözlükten notun
dersini ve konularını seç. Yalnızca sözlükte yazan kimlikleri kullan; yeni kimlik uydurma. Notun
dersini bulamıyorsan course için null, topics için boş liste döndür. Notu iki cümleyle, notun yazıldığı
dilde özetle. Yanıtın yalnızca şu biçimde tek bir JSON nesnesi olsun:
{"course": "...", "topics": ["..."], "summary": "..."}
```

**Kullanıcı mesajı** (sözlük `main`'deki `ontology/courses.ttl`'den, yani EYL-R1'in tablosundan üretilir):

```
SÖZLÜK
Dersler ve konuları (kimlik | Türkçe etiket | İngilizce etiket | üst kavram):
- Course_SEN0401 | Özel Konular: Blokzincir | Special Topics: Blockchain
    - Topic_AuthorizationAndAuthentication | Yetkilendirme ve kimlik doğrulama | Authorization and authentication | Course_SEN0401
    ... (1 ders, 18 konu; her satır kimlik, iki dilde etiket ve üst kavram)

NOT
<notun metni>
```

Modelin yanıtı `suggest` içinde süzülür: sözlükte olmayan ders ya da konu kimliği çıktıya giremez,
bozuk JSON boş öneri olur (ALY-4, #10).

## 2. Deneme düzeni

| | |
| --- | --- |
| Notlar | ALY-R1'in (#12) üç el yazısı sayfasının bilgisayara yazılmış, yazarın onayladığı metni: işlem ücretleri, Merkle ağacı, iş ispatı. Notlar 7–8 Türkçe madde |
| Beklenen konu | Not 1: `Topic_TransactionFees` (ve alt konusu `Topic_FeeRate`) · Not 2: `Topic_Blockchain` (Merkle ağacı 11. bölümde; sözlükte ayrı konu yok) · Not 3: `Topic_MiningAndConsensus` |
| Sağlayıcı | Groq, ücretsiz plan, hesapta Zero Data Retention açık |
| Modeller | `openai/gpt-oss-20b` ve `openai/gpt-oss-120b` (ikisi de Groq'ta "production") |
| Tekrar | Her not her modelde 4 kez (toplam 24 çağrı), 27 Kasım 2026 |
| Ölçülenler | Önerilen ders ve konular; modelin **ham** yanıtındaki bütün `Course_`/`Topic_` kimlikleri ve bunlardan sözlükte olmayanların sayısı; yanıt saf JSON mı; özet iki cümle mi; süre ve token |

Deneme betiği notları okuduğu için repo dışında çalıştırıldı. Model `suggest`'e `LLMClient` arayüzüne uyan
geçici bir Groq istemcisiyle bağlandı; yani istem ve süzme, kodda olduğu gibi denendi.

## 3. Sonuçlar

### 3.1 ALY-R2: üç not, ilk çalıştırma (`openai/gpt-oss-20b`)

| Not | Önerilen ders | Önerilen konular | Ham yanıttaki sözlük dışı kimlik | Saf JSON | Özet |
| --- | --- | --- | --- | --- | --- |
| 1 — işlem ücretleri | `Course_SEN0401` | `Topic_TransactionFees` | 0 | evet | 2 cümle |
| 2 — Merkle ağacı | `Course_SEN0401` | `Topic_Blockchain` | 0 | evet | 2 cümle |
| 3 — iş ispatı | `Course_SEN0401` | `Topic_MiningAndConsensus` | 0 | evet | 2 cümle |

**Sözlük dışına çıkan öneri sayısı: 0.**

### 3.2 ALY-1: iki model, 4 tekrar

| | `openai/gpt-oss-20b` | `openai/gpt-oss-120b` |
| --- | --- | --- |
| Beklenen konuyu içeren öneri | **10/11** | 9/12 |
| Not 1 — işlem ücretleri | 3/4 (1 kez boş) | 4/4 (2 kez `Topic_FeeRate` de) |
| Not 2 — Merkle ağacı | **4/4** `Topic_Blockchain` | 1/4 (3 kez konu önermedi) |
| Not 3 — iş ispatı | 3/3 | 4/4 (1 kez fazladan `Topic_Blockchain`) |
| Beklenmeyen konu | 0 | 1 |
| Ham yanıtta sözlük dışı kimlik | **0** | **0** |
| Saf JSON yanıt | 11/11 | 12/12 |
| Özet iki cümle | 11/11 | 12/12 |
| Ortalama süre | **~0,8 sn** | ~1,4 sn |
| Ortalama token (istem + yanıt) | ~1.300 | ~1.280 |
| Hata | 1 × HTTP 429 (ücretsiz plan istek sınırı) | 0 |

20b'deki tek eksik deneme 429 hatasıdır; yaklaşık 20 çağrı birkaç dakika içinde art arda yapılmıştı.

## 4. Çıkarılan dersler

1. **İstem sözlüğe sınırlamada işe yarıyor.** Başarılı 23 çağrının hiçbirinde model sözlükte olmayan bir
   kimlik yazmadı. `suggest`'teki süzme yine de kalmalı (güvence), ama bu istemle nadiren devreye girecek.
2. **JSON biçimi tutarlı.** Yanıtların hepsi saf JSON; `suggest`'in kod bloğu ve açıklama metni ayıklaması
   bu modellerde gerekmedi ama başka modeller için kalmalı.
3. **Özet uzunluğu istemle tutuyor.** Bütün özetler iki cümleydi; Emine'nin #10 notu (iki cümle kodla
   denetlenmiyor) bu modelde pratikte sorun değil. ALY-6'da 60 notta yine bakılacak.
4. **Sözlükte olmayan bir alt konu boş öneriye yol açabiliyor.** Merkle ağacı sözlükte ayrı konu değil;
   120b modeli çoğunlukla hiç konu önermedi, 20b `Topic_Blockchain`'i seçti. Değerlendirme setinde de böyle
   notlar olursa Eylem'e alt konu önerilecek (ALY-6; #16'daki review notu 4). Kimlikler yeniden
   adlandırılmaz, yeni alt konu eklenir.
5. **Alt konu seçimi kararsız.** Not 1'de `Topic_FeeRate` bazen önerildi, bazen önerilmedi. Ölçü (O3)
   "önerilen konulardan bilinen konular arasında olanlar" olduğu için bu ölçüyü düşürmez; ama manifest'te
   alt konu yazılan notlarda dikkat edilmeli.
6. **Ücretsiz planın istek sınırı gerçek.** Kısa sürede ~20 çağrıdan sonra 429 geldi. Gerçek istemci
   (`tagger/llm.py`, ALY-2) 429'da bekleyip yeniden denemeli; `evalset/run_tagger.py` (ALY-5) çağrıları
   aralıklı yapmalı.
7. **Tekrar şart.** Aynı not aynı modelde farklı sonuçlar verebiliyor: tek çalıştırma 20b'nin bir kez boş
   önerisini ya da 120b'nin bir kez fazladan konusunu göstermezdi. ALY-6'daki ölçüm de en az iki tekrarla
   yapılmalı.

## 5. K-005 için önerilen karar (ALY-1)

**Sağlayıcı: Groq · Model: `openai/gpt-oss-20b`**

| Ölçüt (07_KARARLAR.md, K-005) | Değerlendirme |
| --- | --- |
| Türkçe not metninde doğruluk | Bu denemede 20b 10/11, 120b 9/12; ikisi de Türkçe notları ve Türkçe özeti sorunsuz işledi |
| JSON çıktısı | İkisinde de bütün yanıtlar saf JSON |
| Öğrenci bütçesi | Ücretsiz plan; kredi kartı gerekmiyor |
| API anahtarının CI'da kullanılabilmesi | Anahtar GitHub secret olarak eklenebilir; ücretsiz plan sınırı yüzünden ALY-5 çağrıları aralıklı yapmalı |
| Gizlilik (ek ölçüt) | Groq varsayılan olarak çıkarım verisini saklamıyor; hesapta Zero Data Retention açık. Veriler ABD'de işleniyor; notlarda kişisel veri olmadığı için risk düşük |

Elenen adaylar ve nedenleri:

- **Anthropic Claude:** ücretli; kredi kartı gerektiriyor (öğrenci bütçesi ölçütü).
- **Google Gemini:** ücretsiz plan kart istemiyor, ama Google'ın fiyat sayfasına göre ücretsiz planda
  gönderilen içerik ürünlerini geliştirmek için kullanılıyor (Türkiye AB/İngiltere istisnasında değil).
  Öğrencilerin notlarını korumayı amaçlayan bir proje için bu kabul edilmedi.

Sınırlılık: üç not ve 4 tekrar küçük bir örnek. Model adı kodda değil, `.env`'deki `NOTEPROOF_LLM_MODEL`
değişkeninde durur; ALY-6'da 60 notta 120b daha iyi çıkarsa değişen tek satır budur. Groq modelleri sık
kaldırdığı için (son yılda dokuz kez) "preview" değil "production" model seçildi.

`07_KARARLAR.md` kural setindedir, repoda değildir; karar bu belgeyle Erdener'e ve Arda'ya iletilir.
