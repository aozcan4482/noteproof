# 04 — Git akışı: branch, commit, push, PR, work log

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **değişikliklerin repoya nasıl gireceğini** tanımlamak. Üyeler GitHub Desktop
kullanır; aşağıdaki adımları üyeye GitHub Desktop'taki karşılığıyla, tek tek anlat.

Repo: `https://github.com/aozcan4482/noteproof` · Ana branch: `main`

## 1. Branch'ler

- `main` her zaman çalışır durumdadır. `main`'e doğrudan commit atılmaz; her şey PR ile girer.
  Work log PR'ları da PR'dır, ama hızlı yoldan geçer (bölüm 9).
- Her iş kendi branch'inde yapılır ve branch her zaman güncel `main`'den açılır.

| Tür | Ad kalıbı | Örnek |
| --- | --- | --- |
| Bir story'ye hizmet eden iş | `feature/S<no>-<kısa-ad>` | `feature/S7-proof-page` |
| Story'ye bağlı olmayan altyapı | `infra/<kısa-ad>` | `infra/ci-regtest` |
| Yalnızca belge | `docs/<kısa-ad>` | `docs/acceptance-scripts` |
| Hata düzeltme | `fix/<kısa-ad>` | `fix/proof-status-sync` |
| Work log kaydı | `log/<slug>-<sıra-no>` | `log/erdener-15` |

Kısa ad küçük harf, tire ile ayrılmış, İngilizce. Bir branch tek bir üyeye aittir; başkasının
branch'ine commit atılmaz. Branch için süre sınırı yoktur; ama uzun süren
bir branch'i her oturum başında `main`'den güncelle (bölüm 2), yoksa en sonda büyük çakışmalar çıkar.

Mevcut `burak` ve `feature/S6-copy-warning` branch'leri `main`'e girdikten sonra silinir; sonraki
işler bu kalıpla açılır.

### 1.1 Modelin özeti

Çalışma biçimi şudur: **bir görev → bir branch → bir PR → `main` → branch silinir.**

- **Kişi adına branch açılmaz.** `erdener`, `burak` gibi, üyenin bütün işini biriktirdiği uzun ömürlü
  branch yoktur. Böyle bir branch haftalarca `main`'den uzaklaşır ve en sonda büyük çakışmalar üretir.
- **Bütün güncellemeler `main`'e gider**, ama doğrudan değil: her zaman bir PR üzerinden.
- **Bir branch tek bir görev içindir.** Görev bitip PR `main`'e girince branch silinir; sıradaki görev
  için güncel `main`'den yeni bir branch açılır. Eski branch'e yeni iş eklenmez.
- **Başkasının branch'i kendi branch'ine merge edilmez**, o iş ne kadar gerekli olursa olsun. Başkasının
  işi sana yalnızca `main` üzerinden gelir (`05_PIPELINE.md` bölüm 1.2). Gerekçe: o branch review'da
  değişebilir, senin PR'ında onun commit'leri görünür ve reviewer kimin neyi yazdığını ayıramaz.
- **Aynı anda en çok dört açık görev branch'i.** PR'ları review beklerken yeni görevler için branch
  açılabilir; beşincisi açılmadan önce bekleyenlerden biri `main`'e girmelidir. Her branch yine tek bir
  görev içindir. Work log branch'leri (`log/<slug>-<no>`) bu sayıya girmez:
  kısa ömürlüdür ve hızlı yoldan merge edilir (bölüm 9).

### 1.2 Yeni branch açma (GitHub Desktop, adım adım)

Üyeye sırayla yaptır; her adımdan sonra ekranda ne gördüğünü sor.

1. Üstteki **Current branch** düğmesine tıkla, listeden `main`'i seç.
2. Üstteki **Fetch origin** düğmesine tıkla. Düğme **Pull origin** olarak değişirse ona da tıkla.
   Bu, `main`'in en güncel hâlini bilgisayara indirir. Bu adım atlanırsa branch eski bir `main`'den açılır.
3. Yeniden **Current branch** → **New branch**.
4. Ad kutusuna yukarıdaki kalıpla adı yaz (adı sen ver, ör. `feature/S7-proof-page`).
   Altında "based on main" yazdığını kontrol ettir. Başka bir branch yazıyorsa iptal ettir ve 1. adıma dön.
5. **Create branch**. Üstte Current branch artık yeni adı gösterir.
6. **Publish branch** düğmesine tıkla. Branch GitHub'a gider; ekip onun var olduğunu görür.

Bilgisayarda yarım, commit'lenmemiş değişiklik varken branch değiştirilirse GitHub Desktop ne yapılacağını
sorar. Değişiklikler şu anki göreve aitse **Leave my changes on <branch>** seçtirilir; emin değilsen
üyeyi durdur ve önce o değişikliği commit ettir.

## 2. Oturum başında senkron

Her oturumun ilk işi (üyeye yaptır):

1. GitHub Desktop → **Fetch origin**.
2. Current branch → `main` → **Pull origin**.
3. Kendi branch'ine dön → Branch menüsü → **Update from main**.
4. Çakışma çıkarsa bölüm 7.
5. Repo kökünde `python -m pytest -q`. Kendi değişikliğin olmadan kırmızıysa bunu üyeye söyle; sorun `main`'dedir, Burak'a bildirilir.

Rebase ve force push kullanılmaz.

## 3. Commit

- Bir commit tek bir mantıksal değişikliktir ve yalnızca üyenin sahip olduğu dosyaları içerir.
- Commit'ten önce GitHub Desktop'ın Changes listesindeki **her dosyayı** üyeyle birlikte kontrol et.
  Listede üyenin sahip olmadığı bir yol varsa işaretini kaldırt ve nedenini araştır.
- Şunlar listede görünüyorsa commit'e girmez: `data/`, `.env`, `*.sqlite`, `proofs/`, `__pycache__/`,
  `.venv/`, `node_modules/`, cüzdan dosyaları, anket ham verisi, kişisel not dosyaları.

## 4. Push: ne zaman hatırlatacaksın

Düzenli push bu dersin gereğidir ve her üyenin bireysel notuna kanıt olur. Aşağıdaki durumların her
birinde üyeye push atması gerektiğini **sen söyle** ve bölüm 5'teki metni hazır ver:

| Durum | Ne yapılır |
| --- | --- |
| Bir görev (üye dosyasındaki bir `XXX-n` maddesi) ya da görevin anlamlı bir parçası bitti, testler yeşil | Commit + push |
| Oturum bitiyor | İş bitmişse commit + push. Yarımsa bölüm 4.1 |
| Başka bir bilgisayara geçilecek | Yarım da olsa commit + push (bölüm 4.1). Yeni bilgisayarda ilk iş **Fetch origin**, sonra ilgili branch'e geçiş; commit'lenmemiş iş öbür bilgisayarda kalır ve görünmez |
| Başka bir üye bu çıktıyı bekliyor (bir sözleşme fonksiyonu, test vektörü, sözlük dosyası) | Hemen commit + push + PR |
| Son push'un üzerinden 2 gün geçti ve yerelde commit'lenmemiş iş var | Commit + push |
| Büyük bir yeniden düzenlemeye başlamadan hemen önce | Çalışan hâli commit + push |
| Review istenecek | Push, sonra PR |

Her üyenin haftada en az 3 ayrı günde push'u olmalıdır. Oturum sonunda son push tarihine bak
(`git log -1 --format=%cd origin/<branch>`) ve hedefin gerisindeyse söyle.

### 4.1 Yarım iş

Oturum biterken iş yarımsa ve testler kırmızıysa: kırık testi `main`'e taşımamak için iş branch'te kalır,
ama yine de push edilir. Commit özeti `WIP` ile başlar (bölüm 5) ve açıklamada neyin eksik olduğu yazar.
`WIP` commit'i olan branch için PR açılmaz ya da PR "Draft" olarak açılır.

## 5. Commit mesajı

GitHub Desktop'ta iki alan vardır: **Summary** ve **Description**. İkisini de sen yazarsın, üye yapıştırır.

**Summary** — tek satır, İngilizce, en çok 72 karakter, emir kipi, sonunda nokta yok:

```
<kapsam>: <ne yapıldı>
```

| Kapsam | Ne zaman |
| --- | --- |
| `S1` … `S7` | Değişiklik bir story'ye hizmet ediyor |
| `infra` | CI, bağımlılık, yapılandırma, `core/` |
| `docs` | Yalnızca belge |
| `fix` | Hata düzeltme (story biliniyorsa `S5 fix: ...`) |
| `log` | Work log kaydı |
| `WIP S3` gibi | Yarım iş (bölüm 4.1) |

Örnekler: `S7: Add browser Merkle path verifier with shared test vectors` ·
`infra: Run regtest node in CI` · `log: Add work-log entry 15 (erdener)`

**Description** — İngilizce, bu kalıpla:

```
What:
- <değişiklik 1>
- <değişiklik 2>

Why: <bir cümle; hangi kabul kriteri ya da hangi görev>

Module: <klasör> (owner: <slug>)
Task: <görev kimliği> (part) | <görev kimliği> (done)
Contract: none | implements 02#<bölüm> | changes 02#<bölüm> (K-0xx)
Tests: <python -m pytest -q çıktısının son satırı>
```

`Task` satırı, ekipteki diğer araçların bu görevin durumunu bulmak için aradığı satırdır; biçimi birebir
böyle olmalıdır:

- `Task: ERD-2 (part)` — bu commit görevin bir parçasıdır, görev sürüyor.
- `Task: ERD-2 (done)` — bu commit ile görevin kabul ölçütü karşılandı. Bir görev için yalnızca bir kez,
  son commit'te yazılır. Kabul ölçütünü (üye dosyasındaki tablo) tek tek kontrol etmeden `(done)` yazma.
- Hiçbir göreve bağlı olmayan commit'te (ör. work log) satır `Task: -` olur.

`(done)` yazmak görevi bitirmez; yalnızca "bitirmeye hazır" der. Görev, bu commit `main`'e girdiğinde
biter (`05_PIPELINE.md` bölüm 1.1).

Kurallar:

- `Tests` satırına gerçek çıktıyı yaz; çalıştırmadıysan çalıştırt.
- `Contract: changes ...` yalnızca `02` bölüm 9'daki prosedür tamamlandıysa yazılabilir.
- Mesajda kişisel veri, anahtar, not içeriği olmaz.
- Kodu yapay zekânın yazdığını belirtmek serbesttir ama zorunlu değildir; ekip tek bir biçim
  seçerse `07_KARARLAR.md`'ye yazılır.

## 6. Pull request

1. Push'tan sonra GitHub Desktop → **Create Pull Request**. Hedef her zaman `main`.
2. Başlık: commit özeti kalıbıyla aynı.
3. Gövde: `.github/pull_request_template.md` doldurulur. Sen doldur, üye kontrol etsin:
   ne değişti, hangi story, Definition of Done kutuları (yalnızca gerçekten doğru olanlar işaretlenir).
4. Reviewer: modülün **ikinci** üyesi (`02` bölüm 2) ve Quality Lead (Emine). Emine'nin kendi PR'larında
   ikinci reviewer Arda'dır.
5. Bir PR tek bir görev içindir; satır sınırı yoktur. Büyük bir PR'da açıklamaya reviewer için kısa bir
   okuma sırası yaz (önce hangi dosyalar, sahte veri ve örnek dosyalar hangileri).
6. CI yeşil olmadan ve en az bir onay gelmeden merge edilmez. Genel CI (`ci.yml`, BRK-2) `main`'e girene
   kadar CI yerine şu geçerlidir: PR açıklamasının `Tests` bölümünde, PR sahibinin yerelde çalıştırdığı
   `python -m pytest -q` ve (`tests/web/` varsa) `node --test` çıktılarının son satırı yazar ve ikisinde de
   `failed` yoktur. Reviewer emin olmazsa branch'i çekip kendisi de çalıştırır.
7. Merge'i Burak yapar (Repository and release manager); Burak'ın PR'larını Arda merge eder.
   Work log PR'larını sahibi merge eder (bölüm 9). **Bekleme sınırı:** onay geldikten sonra 24 saat içinde
   merge edilmeyen PR'ı, onay hâlâ geçerliyse ve 6. maddedeki test koşulu sağlanıyorsa, PR sahibi kendisi
   merge eder ve ekip grubuna "#<no> 24 saat kuralıyla merge edildi" yazar. Bekleyen başka bir review
   ("pending review") merge'ü engellemez; en az bir onay yeterlidir.
   Yöntem: **Create a merge commit**. Squash kullanılmaz: tek tek commit'ler bireysel emeğin kanıtıdır.
8. Merge'den sonra branch silinir. Üye `main`'i çeker ve sıradaki iş için yeni branch açar
   (adımlar: `05_PIPELINE.md` bölüm 1.3).
9. PR gövdesinin ilk satırına görev durumunu yaz: `Task: ERD-2 (done)` ya da `Task: ERD-2 (part)`.
   Bu PR'ı bekleyen başka üyeler varsa onları da yaz: `Unblocks: ERD-3, ARD-5`.

**Kural seti değişikliği.** `AGENTS.md` ve `docs/rules/` yalnızca Erdener'in PR'larıyla değişir (K-010):
branch `docs/rules-<kısa-ad>`, özet `docs: ...`; onayı herhangi bir üye verebilir. PR açıklamasına hangi kuralın neden
değiştiği yazılır; dosyaların sürüm satırı ve `AGENTS.md` bölüm 7'deki sürüm notu aynı PR'da güncellenir.
Merge edilince Erdener ekip grubuna tek satır yazar: "Kural seti <sürüm> main'de: <ne değişti>."

PR'ın durumunu üye şuradan görür: GitHub'da repo sayfası → **Pull requests**. Yeşil "Open" incelemede,
mor "Merged" `main`'e girmiş, kırmızı "Closed" reddedilmiş ya da geri çekilmiş demektir. PR sayfasının
altında CI sonucu (yeşil tik ya da kırmızı çarpı) ve reviewer onayları görünür.

PR 24 saatten uzun süredir onaysız bekliyorsa üyeye söyle; üye reviewer'a ve Burak'a ekip grubundan yazar.
48 saat geçtiyse PR sahibi dışındaki herhangi bir üye (tercihen Quality Lead ya da modülün ikincisi) review
yapıp onay verebilir; reviewer'ın bakacağı şeyler aşağıdakiyle aynıdır.
Reviewer değişiklik isterse düzeltme **aynı branch'e** yeni commit olarak atılır ve push edilir; PR
kendiliğinden güncellenir. Yeni PR açılmaz.

Reviewer'ın bakacağı şeyler: sahiplik sınırı aşılmış mı, sabit sözleşmeler değişmiş mi, testler story'ye
bağlı mı, kapsam dışı bir şey eklenmiş mi, kişisel veri var mı. Review 24 saat içinde yapılır.

## 7. Çakışma (merge conflict)

| Çakışan dosya | Ne yapılır |
| --- | --- |
| Üyenin sahip olduğu dosya | İki değişikliğin amacını da koruyarak çöz, testleri çalıştır |
| Başkasının sahip olduğu dosya | `main`'deki hâli al. Kendi değişikliğin gerekiyorsa bölüm 8 |
| `proposal/proposal.json` | **Elle asla çözme.** Bölüm 9, adım 6 |
| `pyproject.toml`, `.gitignore`, `.gitattributes`, `.github/` | `main`'deki hâli al, ihtiyacını Burak'a bildir |

Çakışmayı "hangisi daha yeni" diye çözme. Emin değilsen merge'i iptal ettir ve dosyanın sahibine sordur.

## 8. Başkasının dosyası ve ortak dosyalar

Üyenin sahip olmadığı bir dosyada değişiklik gerekiyorsa değişikliği kendin yapma. Üyeye, dosyanın
sahibine iletmesi için şu notu hazırla:

```
Kimden: <slug> · Kime: <sahip slug> · Dosya: <yol>
İstek: <ne değişmeli, tek cümle>
Neden: <hangi görev ya da kabul kriteri için>
Öneri: <istenen satırlar ya da imza>
```

Aynı anda kendi kodunda ilgili yere `# NP-TODO(<sahip slug>): ...` bırak. Sahip, değişikliği kendi
branch'inde yapar. İstisna: tek karakterlik yazım hatası gibi şeyler bile bu yoldan gider; istisna yok.

## 9. Work log

Work log, `proposal/proposal.json` içinde SHA-256 ile zincirlenmiş kayıtlardır. Her kayıt bir öncekinin
hash'ine bağlıdır; dosya elle düzenlenirse ya da iki kişi aynı anda farklı kopyalara kayıt eklerse zincir
kırılır ve ekip puan kaybeder. Kayıt yalnızca Proposal Workbench (proposal'ın HTML aracı) ile eklenir.

**Sen `proposal/` altındaki hiçbir dosyayı düzenlemezsin.** Senin işin taslağı hazırlamak ve üyeye
adımları yaptırmaktır.

Her çalışma oturumunun sonunda:

1. `docs/worklog/<slug>.md` dosyasına bir taslak satırı ekle (dosya üyenindir, işle birlikte commit edilir):

   ```
   | Tarih | Process | Story | Saat | Açıklama | Kanıt | Workbench'e girildi |
   | 2026-11-23 | P07 | S7 | 2 | Wrote the browser Merkle verifier and tested it on the shared vectors | <commit ya da PR linki> | hayır |
   ```

2. Üyeye söyle: "Bu kaydı bugün Workbench'e girmen gerekiyor."
3. Üye `main`'i çeker, `log/<slug>-<sıra-no>` branch'ini açar. Bu branch, açık branch sınırına
   (bölüm 1.1) girmez.
4. Workbench'te `proposal/proposal.json` dosyasını açar, kaydı ekler (üye, process, story, saat,
   açıklama, kanıt linki), dosyayı kaydeder ve `proposal/proposal.json`'ın üzerine yazar.
5. Commit: `log: Add work-log entry <no> (<slug>)` → push → PR. Bu PR hızlı yoldan geçer: üye ekip
   grubuna "log PR'ı açtım" yazar, müsait olan ilk üye yalnızca `proposal/` dışında dosya değişmediğine
   bakıp onaylar, üye CI geçince kendi merge eder. Kod incelemesi yapılmaz, Burak beklenmez.
6. PR çakışırsa (araya başka kayıt girmiştir): PR kapatılır, branch silinir, `main` çekilir ve 3. adımdan
   yeniden başlanır. Dosya elle birleştirilmez.
7. Taslak dosyasındaki satırda son sütun `evet` yapılır.

Kayıt kuralları (Workbench bunları denetler; ihlal ekip puanını düşürür):

| Kural | Sınır |
| --- | --- |
| Kayıt, iş yapıldığı gün girilir; toplu giriş yapılmaz | Aynı üyenin 10 dakika içinde 5 kaydı ihlaldir |
| Tek kayıt | 0'dan büyük, en çok 12 saat |
| Bir üyenin bir gündeki toplamı | En çok 12 saat |
| Açıklama | İngilizce, o oturumda gerçekten yapılan iş. Aynı açıklama en çok 2 kez kullanılabilir |
| Kanıt | Commit ya da PR linki. Final'de her üyenin kayıtlarının en az %50'si kanıtlı olmalı |
| Process çeşitliliği | Her üye en az 2 farklı process'te kayıt girmeli |
| Kayıt sayısı | Final'de üye başına en az 6 |
| Saat payı | Üyenin kayıtlı saat payı, planlanan payının en az yarısı olmalı (Arda ve Burak %15, diğerleri %14) |

Saatleri ve açıklamaları üyenin gerçekte yaptığı işe göre yaz; şişirme, uydurma, geriye dönük toplu kayıt önerme.

### 9.1 Yeniden yapılan işler: revize (Correction) kaydı

Workbench'te kayıt eklerken **Kind** alanının iki değeri vardır: "Work" ve "Correction of an entry".
Correction seçilince "Corrects entry no." kutusuna düzeltilen kaydın numarası yazılır. Eski kayıtlar
silinemez ve değiştirilemez (zincir kırılır); bir kaydın durumunu düzeltmenin tek yolu budur.

Üye dosyalarının bölüm 4.1'indeki `R` görevleri (proposal'da yapılmış görünen, repoda çıktısı olmayan işler)
bittiğinde, yani PR `main`'e girdiğinde, **iki kayıt** girilir:

| Sıra | Kind | Ne yazılır |
| --- | --- | --- |
| 1 | Work | Bu oturumlarda gerçekten yapılan iş, gerçek saatiyle. Kanıt: merge edilmiş PR linki. Process ve story normal kurallarla |
| 2 | Correction of an entry | "Corrects entry no.": görev tablosundaki eski kayıt numarası. Saat: 0.25 (alan boş bırakılamıyor). Açıklama (İngilizce, en az 8 kelime): eski kaydın çıktısının repoya girmediği, işin yeniden yapıldığı ve hangi kayıtta olduğu. Örnek: `Output of entry 5 was never committed; the chapter list was redone and delivered in entry 17`. Kanıt: aynı PR linki |

Neden iki kayıt: Workbench bireysel değerlendirmede (kayıt sayısı, saat payı, process çeşitliliği, kanıtlı
kayıt oranı) yalnızca "Work" kayıtlarını sayar; Correction kayıtları sayılmaz. İş yalnızca Correction olarak
girilirse üyenin emeği ve kanıtı hesaba girmez. Yalnızca Work olarak girilirse eski kanıtsız kayıt açıklamasız
kalır ve aynı iş iki kez yapılmış gibi görünür.

Correction kaydını, Work kaydından sonra ve ayrı bir `log/...` PR'ı açmadan, aynı Workbench oturumunda art
arda gir; ikisi tek commit'te gider. Açıklamada yalnızca doğru olanı yaz: eski iş hiç yapılmadıysa "was not
done", yapılıp repoya konmadıysa "was never committed". Hangisi olduğunu üyeye sor; kendin karar verme.

Process kodları: P01 Mission analysis · P02 Stakeholder needs · P03 Requirements definition ·
P04 Architecture definition · P05 Design definition · P06 System analysis · P07 Implementation ·
P08 Integration · P09 Verification · P10 Transition · P11 Validation · P12 Operation ·
P13 Maintenance · P14 Disposal.

Work-log steward'lar (Eylem ve Aleyna) her cuma zincirin sağlam olduğunu ve her üyenin kayıt girdiğini
kontrol eder.

## 10. Sürümler

Etiketleri yalnızca Burak atar: `v0.3.0` (27 Kasım, entegrasyon), `v0.9.0` (4 Aralık, pilot adayı),
`v1.0.0` (11 Aralık, final). Etiketlenmiş sürüm final notunun bir koşuludur.

## 11. Yasaklar

- `main`'e doğrudan push, force push, rebase, başkasının branch'ine commit.
- Kişi adına uzun ömürlü branch açmak; başkasının branch'ini kendi branch'ine merge etmek; `main`'e girmiş bir branch'e yeni iş eklemek.
- Başka bir üyenin modülünü kendi branch'inde "geçici olarak" yazmak.
- Kırmızı testle PR açmak (Draft hariç) ya da kırmızı CI'ı merge etmek.
- `proposal/proposal.json`'ı elle ya da bir araçla düzenlemek.
- Sır, kişisel veri, çalışma verisi commit etmek.
