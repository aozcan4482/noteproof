# 03 — Kod kuralları ve yorum satırı protokolü

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **kodun nasıl yazılacağını** ve yedi ayrı aracın ürettiği kodun birbirini
tanıması için **yorum satırlarının nasıl kullanılacağını** tanımlamak.

## 1. Dil

| Yer | Dil |
| --- | --- |
| Değişken, fonksiyon, sınıf, dosya, klasör, JSON alanı, IRI adları | İngilizce |
| Yorum satırları ve docstring'ler | Türkçe |
| Kullanıcının gördüğü arayüz metinleri ve hata mesajları | Türkçe |
| Commit mesajları ve PR başlıkları | İngilizce |
| `docs/` altındaki belgeler | Türkçe (rapor ve proposal metinleri İngilizce) |

## 2. Dosya başlığı

Yeni oluşturduğun her kaynak dosyanın en üstüne bu başlığı koy. Başka bir aracın dosyayı açtığında ilk
okuyacağı şey budur: dosyanın kime ait olduğunu, hangi sözleşmeyi uyguladığını ve neye bağlı olduğunu söyler.

Python (başlık yorumdur, modül docstring'i hemen altından gelir):

```python
# NOTEPROOF-FILE
# module:   register
# owner:    arda            second: burak
# story:    S1, S3
# contract: 02#7 POST /api/notes/preview
# depends:  tagger.suggest.suggest, copywarn.CopyChecker.check
# status:   wip
"""Önizleme uç noktası: dosyayı alır, hash'ler, öneri ve kopya uyarısı döndürür."""
```

Alanlar:

| Alan | Değer |
| --- | --- |
| `module` | Üst klasörün adı |
| `owner`, `second` | Üye slug'ları (`02` bölüm 2) |
| `story` | Hizmet ettiği story'ler; yoksa `-` |
| `contract` | Uyguladığı sözleşmenin `02` içindeki bölümü; yoksa `-` |
| `depends` | Başka modüllerden çağırdığı sözleşme fonksiyonları; yoksa `-` |
| `status` | `stub` (sahte, yerine gerçeği gelecek), `wip` (yarım), `stable` (testli ve sözleşmeye uygun) |

Diğer dillerde aynı satırlar o dilin yorum biçimiyle yazılır: JavaScript ve CSS'te `/* ... */`,
HTML'de `<!-- ... -->`, Turtle, SPARQL, YAML ve TOML'da `#`.

Mevcut dosyalar (`anchor/`, `copywarn/`, `evalset/`) başlıksızdır. Başlığı, dosyanın sahibi o dosyaya
bir sonraki dokunuşunda ekler. Başkasının dosyasına yalnızca başlık eklemek için dokunma.

## 3. Satır içi işaretler

Beş işaret vardır. Hepsi `NP-` ile başlar; böylece `grep -rn "NP-" .` bütün koordinasyon notlarını listeler.

| İşaret | Anlamı | Kural |
| --- | --- | --- |
| `# NP-CONTRACT(02#5.3): ...` | Bu fonksiyon, sınıf ya da sabit `02`'deki sabit bir sözleşmedir | İmzasını, adını, dönüş biçimini değiştirme. Gövdesini yalnızca sahibi değiştirir |
| `# NP-STUB(owner=aleyna, contract=02#5.3): ...` | Başka bir üyenin modülünün geçici sahtesi | Yalnızca `tests/` altında ya da `<modül>/_stubs.py` içinde durur. Gerçek modül `main`'e girince silinir |
| `# NP-TODO(emine): ...` | Adı geçen üyeden bir şey bekleniyor ya da ona bir soru var | Kısa ve tek satır. Çözülünce silinir |
| `# NP-DECISION(K-002): ...` | Bu kod `07_KARARLAR.md`'deki bir karara dayanıyor | Kararı değiştirmeden bu kodu "düzeltme" |
| `# NP-OWNER(burak): ...` | Dosya sahibinden farklı bir üyenin sorumlu olduğu bölüm | Yalnızca `02` bölüm 2'de yazılı istisnalar için |

Bir dosyayı düzenlemeden önce içindeki `NP-` işaretlerini oku ve onlara uy. Kod üretirken:

- Sözleşme uygulayan her fonksiyonun üstüne `NP-CONTRACT` koy.
- Henüz `main`'de olmayan bir modüle ihtiyacın varsa onu kendin yazma; sözleşmedeki imzaya birebir uyan
  bir `NP-STUB` yaz ve gerçek modülü çağıran kodu bu sahteyle test et.
- Bilmediğin bir şeyi varsayma; `NP-TODO(<slug>)` bırak ve üyeye söyle.

## 4. Yorum yazımı

Mevcut kodun üslubunu sürdür:

- Her modülün başında, ne yaptığını ve proposal'ın hangi adımını karşıladığını anlatan Türkçe bir docstring.
- Yorumlar **neden**'i anlatır: tasarım kararı, proposal'daki karşılığı, güvenlik gerekçesi.
  Kodun zaten söylediğini tekrarlama.
- Başka bir modülle temas eden her yerde bunu yorumda adıyla söyle: "Kayıt servisiyle (Arda) sözleşme: ...".
- Öğrenci düzeyinde okunabilirlik: ekip arkadaşı bu dosyayı açıp ne yaptığını anlayabilmeli.

## 5. Python

- `from __future__ import annotations` ile başla; bütün fonksiyon imzalarında tip belirt.
- Veri taşıyan yapılar için `@dataclass(frozen=True)`.
- Paketler arası içe aktarma yalnızca `02` bölüm 5'teki adlarla. Göreli içe aktarma yalnızca aynı paket içinde.
- Paket içinde döngüsel bağımlılık kurma. Yön: `core` ← `ontology`, `shapes`, `anchor`, `copywarn`, `tagger`, `search` ← `register`.
  `anchor` ve `copywarn` standart kütüphane dışında bağımlılık almaz.
- Sırlar ve yollar koda yazılmaz; `02` bölüm 8'deki ortam değişkenlerinden okunur.
- Hata durumunda sessizce boş sonuç dönme. Boş girdi, eksik dosya, boş sözlük açık bir hata ya da açık bir mesaj üretir.
- Satır uzunluğu yeni kodda en çok 120 karakter.
- Komut satırından çalışan her şey `python -m <paket>.<modül>` biçimindedir ve repo kökünden çalışır.

## 6. JavaScript, HTML, CSS

- Çerçeve, paketleyici, derleme adımı yok. ES modülleri (`<script type="module">`), sade CSS.
- Dış CDN bağımlılığı yok: proof sayfası çevrimdışı açılabilmelidir.
- Önce telefon: 360 piksel genişlikte düzgün çalışır, sonra genişler.
- API adresleri ve public signet API adresi yalnızca `web/js/config.js` içinde durur.
- Hash ve Merkle hesapları yalnızca `web/js/verify.js` içinde yapılır ve WebCrypto kullanır.

## 7. RDF, SHACL, SPARQL

- Turtle dosyalarında önekler `02` bölüm 3'teki gibi; her terimin `rdfs:label` ve `rdfs:comment`'i olur.
- Kavram kimlikleri bir kez yayımlandıktan sonra yeniden adlandırılmaz; yanlışsa `owl:deprecated` ile işaretlenir, yenisi eklenir.
- SPARQL sorguları Python string'lerine gömülmez; `search/queries/*.rq` dosyalarında durur.

## 8. Testler

- Her story'nin kabul kriteri en az bir testtir ve adında story geçer: `test_s6_acceptance_...`.
- Testler `tests/<paket>/` altında durur; paketle aynı sahibe aittir.
- Testler dış dünyaya bağlanmaz: Bitcoin node'u yerine `tests/anchor/fake_rpc.py`, dil modeli yerine
  `FakeLLM`. Gerçek node isteyen testler `@pytest.mark.regtest` ile işaretlenir ve node yoksa atlanır.
- Test verisi sentetiktir: gerçek öğrenci notu, isim, öğrenci numarası içermez. Gerçek notlar yalnızca
  `evalset/notes/` altında, `evalset/README.md` kurallarıyla durur.
- `01_PROJE.md` bölüm 7'deki iki reddetme senaryosunun testi zorunludur.
- Tarayıcı kodunun testleri `tests/web/` altında `*.test.mjs` adıyla durur ve repo kökünde `node --test` ile
  çalışır. Klasör adı verilmez: Node 22 ve üstü `node --test tests/web/` biçimini kabul etmez.
- Push'tan önce repo kökünde `python -m pytest -q` çalıştır. Başarısız test varken push yapılmaz;
  yarım iş için kural `04_GIT_AKISI.md` bölüm 4'tedir.

## 9. Gizlilik ve güvenlik

- Zincire giden veri: yalnızca 32 byte'lık kök. `anchor/opreturn.py` dışında OP_RETURN üreten kod yazılmaz.
- Mainnet'e bağlanan kod yazılmaz; `anchor/daily.py` içindeki ağ kontrolü kaldırılmaz.
- Grafikte, günlüklerde, test verisinde, commit'lerde gerçek isim ve öğrenci numarası olmaz. Yazar her yerde takma addır.
- Anket ham verisi, `.env`, API anahtarı, cüzdan dosyası, `data/` içeriği commit edilmez.
- Günlüklere not içeriği yazılmaz; hash yazılır.
- Yazarın onayı (`confirmed: true`) olmadan grafiğe not, etiket ya da özet yazan bir kod yolu olmaz.

## 10. Kod yazmadan önce kontrol listesi

Her kod üretiminden önce kendine şunları sor:

1. Bu dosya, üyenin sahip olduğu bir klasörde mi? (`02` bölüm 2)
2. Dokunduğum şey sabit bir sözleşme mi? Öyleyse imzası `02` ile birebir aynı mı?
3. Başka bir modüle ihtiyacım var mı? Varsa `main`'de mi, yoksa `NP-STUB` mu gerekiyor?
4. `01_PROJE.md` bölüm 5'teki kapsam dışı maddelerden birine giriyor muyum?
5. Dosyada uymam gereken `NP-` işaretleri var mı?
6. Bu iş için test yazdım mı, test hangi story'ye bağlı?
7. Değiştirmediğim satırları yeniden biçimlendirdim mi? (Yapma: gereksiz diff, merge çakışması üretir.)
