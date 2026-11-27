# 07 — Kararlar

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **ekibin verdiği ve vermesi gereken tasarım kararlarını** tek yerde tutmak.
Bir tasarım seçimi yapmadan önce buraya bak. "Verildi" durumundaki bir kararı kod yazarken değiştirme;
"Açık" durumundaki bir kararda geçici değerle çalış ve koda `# NP-DECISION(K-0xx)` yaz.

Yeni karar eklemek ya da bir kararı değiştirmek: `02_MIMARI_SOZLESMELER.md` bölüm 9.

| No | Karar | Durum | Sahibi | Son tarih |
| --- | --- | --- | --- | --- |
| K-001 | Namespace IRI'si | Açık (geçici değer kullanılıyor) | eylem, arda | 22 Kasım |
| K-002 | Kopya uyarısının benzerlik yöntemi | Verildi | emine | — |
| K-003 | Web yığını | Verildi | arda, erdener | — |
| K-004 | Depolama | Verildi | arda, burak | — |
| K-005 | Dil modeli sağlayıcısı | Verildi | aleyna | — |
| K-006 | Yükleme sınırları | Verildi (müşteriyle teyit edilecek) | aysu | 27 Kasım |
| K-007 | Hesaplar ve kimlik | Verildi | arda | — |
| K-008 | Proof sayfasının zincir kontrolü | Açık | burak, erdener | 25 Kasım |
| K-009 | Kişisel ilerleme dosyaları | Verildi | burak | — |
| K-010 | Kural setinin yeri | Verildi | erdener | — |

## K-001 — Namespace IRI'si

Geçici değer: `https://github.com/aozcan4482/noteproof/ns#` (`anchor/proof.py` içinde zaten kullanılıyor).
Proposal "stable IRIs" diyor; bu adres tarayıcıda açılmıyor. Karar verilecek: bu değer mi kalacak, yoksa
açılabilen bir adrese mi geçilecek. Karar çıkana kadar herkes değeri yalnızca `core/ns.py`'den içe aktarır;
böylece değişiklik tek satır olur. Proof dosyaları üretildikten sonra değer değiştirilmez; bu yüzden karar
signet'teki ilk gerçek timestamp'ten önce verilmelidir.

## K-002 — Kopya uyarısının benzerlik yöntemi

`copywarn/` karakter 5-gram kosinüs benzerliği ile kelime 3-shingle containment ölçüsünü kullanır;
eşik 0.60. Proposal "text embeddings" diyor. Bu bilinçli bir sapmadır: mevcut yöntem ek bağımlılık
gerektirmiyor ve sentetik sette hedefi tutturuyor. Gerçek 60 notta O5 (%90) tutmazsa embedding karşılaştırması
isteğe bağlı ikinci bir ölçü olarak eklenir (Emine, Aleyna). Sapma final raporunda yazılır.

## K-003 — Web yığını

API: FastAPI. Arayüz: statik HTML, CSS ve sade JavaScript; çerçeve ve derleme adımı yok. Gerekçe: proof
sayfası arşivin sunucusu olmadan açılabilmeli (S7); statik dosya bunu en basit yoldan sağlar.

## K-004 — Depolama

Arşivin grafiği Oxigraph'ta (`data/graph/`), timestamp kuyruğu SQLite'ta (`data/noteproof.sqlite`),
not dosyaları ve çıkarılan metin dosya sisteminde (`data/notes/`, `data/text/`). Kuyruğun Oxigraph'a
taşınması bu dönemin kapsamında değildir.

## K-005 — Dil modeli sağlayıcısı

Verildi (27 Kasım, Aleyna). Sağlayıcı: **Groq**. Model: **`openai/gpt-oss-20b`**. Gerekçe ve aday
karşılaştırması: ALY-R2 belgesi (PR #27). Ölçütler: Türkçe not metninde doğruluk, JSON çıktısı, öğrenci
bütçesi, API anahtarının CI'da kullanılabilmesi.

- API anahtarı repoya girmez. Yerelde `.env` içindeki `NOTEPROOF_LLM_API_KEY`'de, CI'da aynı adlı GitHub
  secret'ında durur. CI anahtarını Arda kendi Groq hesabından oluşturur (hesabın Data Controls ayarında ZDR,
  yani verilerin saklanmaması açık) ve repoya secret olarak ekler; anahtar kimseyle paylaşılmaz.
- Kod `tagger/llm.py` içindeki `LLMClient` arayüzünün arkasında kalır; sağlayıcıya özel her şey o dosyadadır.
  Testler ağa çıkmadan `FakeLLM` ile çalışır. Sağlayıcı değişirse yalnızca `tagger/llm.py` ve `.env` değişir.

## K-006 — Yükleme sınırları

Kabul edilen türler: PDF, JPEG, PNG, düz metin, Markdown. En büyük dosya: 10 MB. Arşive yalnızca
öğrencinin kendi notu yüklenir. Yükleme kurallarının sahibi müşteridir (3. ve 4. sınıf öğrencileri);
Aysu bu sınırları onlarla teyit eder ve sonucu `docs/pilot/upload-rules.md`'ye yazar.

## K-007 — Hesaplar ve kimlik

Hesaplar takma adlıdır: öğrenci bir takma ad seçer, sistem bir kez gösterilen bir token üretir; token
özetlenerek saklanır. Gerçek isim, öğrenci numarası, e-posta istenmez ve saklanmaz. Okul girişi, e-posta
doğrulaması gibi gerçek kimlik denetimi kapsam dışıdır.

## K-008 — Proof sayfasının zincir kontrolü

Açık. Tarayıcı, işlemin OP_RETURN çıktısını ve blok zamanını public bir signet API'sinden okuyacak.
Karar verilecek: hangi public servis kullanılacak ve tarayıcıdan erişime (CORS) izin veriyor mu. Burak
adayı doğrular, Erdener adresi `web/js/config.js`'e yazar. Regtest demolarında public node olmadığı için
sayfa çevrimdışı kontrolü yapar ve "zincir kontrolü bu ağda yapılamıyor" der.

## K-009 — Kişisel ilerleme dosyaları

`BURAK_ILERLEME.md` gibi kişisel dosyalar `main`'e girmez. Her üyenin ilerleme ve work log taslağı
`docs/worklog/<slug>.md` dosyasında tutulur; bu dosya `main`'e girer ve yalnızca o üye düzenler.

## K-010 — Kural setinin yeri

Verildi (27 Kasım). Kural seti repodadır: `AGENTS.md` kökte, diğer dosyalar `docs/rules/` altında. Zip ile
dağıtım kalktı. Gerekçe: proje zaten açıkça yapay zekâ destekli yürüyor; kuralların repoda olması herkesin
aynı sürümle çalışmasını `git` ile sağlıyor, değişiklikleri PR review'una bağlıyor ve repo klasöründe çalışan
araçların kökteki `AGENTS.md`'yi kendiliğinden okumasını sağlıyor. Kural setinin sorumlusu Erdener'dir;
değişiklikleri yalnızca o yapar (`04` bölüm 6).
