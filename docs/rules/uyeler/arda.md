# Üye dosyası — Arda Özcan (`arda`)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **Arda'nın** rolünü, kapsamını, kurulumunu ve görevlerini tanımlamak.
Yalnızca Arda ile çalışan araç bu dosyayı uygular.

## 1. Roller

| | |
| --- | --- |
| İdari rol | Team lead: ekibi planlar ve koordine eder, proposal'ın ve backlog'un sahibidir |
| Geliştirme rolleri | Architect, Back-end developer |
| Lider olduğu process'ler | P01 Mission analysis, P04 Architecture definition, P08 Integration |
| Sahip olduğu modül | **Registration service** (E1; story S1, kısmen S3, S4, S6) |
| İkincisi olduğu modül | Bitcoin timestamp service (`anchor/`) — Burak'ın PR'larını inceler ve merge eder |
| Planlanan iş payı | %15 |
| Sorumlu olduğu ara teslim | 11 Aralık: pilot, değerlendirme raporu, `v1.0.0` |

## 2. Kapsam

**Senin klasörlerin:** `core/`, `register/`, `tests/core/`, `tests/register/`, `proposal/`, `docs/worklog/arda.md`.

**Dokunmayacakların:** diğer bütün klasörler. `anchor/`, `tagger/`, `copywarn/`, `ontology/`, `shapes/`,
`search/` modüllerini yalnızca `02` bölüm 5'teki sözleşme fonksiyonlarıyla çağırırsın; içlerini değiştirmezsin.

Kayıt servisi sistemin ortasıdır: diğer altı modülü birbirine o bağlar. Bu yüzden iki şey senden beklenir:
sözleşmelere en sıkı uyan sen olmalısın, ve bir sözleşme yetersiz kalıyorsa değişikliği sen başlatırsın
(`02` bölüm 9); kendi kodunda sessizce etrafından dolaşmazsın.

## 3. Ek kurulum

`06_KURULUM.md` tamamlandıktan sonra:

1. Bağımlılıklar `pip install -e ".[dev,all]"` ile gelir: FastAPI, uvicorn, python-multipart, RDFLib,
   pySHACL, pyoxigraph, httpx (test istemcisi için). Oxigraph ayrı bir sunucu değildir; `pyoxigraph`
   paketi depoyu `data/graph/` klasöründe kendisi tutar.
2. Kontrol: `python -c "import fastapi, rdflib, pyshacl, pyoxigraph; print('ok')"` → `ok`.
3. Resimden metin çıkarmayı yerelde denemek istersen Tesseract gerekir (Aleyna'nın dosyası, bölüm 3).
   Zorunlu değil: testlerde `tagger.extract` yerine sahte kullanılır.
4. `.env`: yalnızca `NOTEPROOF_DATA_DIR=./data`.

## 4. Görevler

### 4.1 Önce: proposal'da yapılmış görünen işler

Proposal'ın work log'unda aşağıdaki işler yapılmış olarak kayıtlı, ama repoda hiçbirinin çıktısı ya da
kanıtı yok. Bu işler **yapılmamış sayılır** ve modül görevlerinden önce, sıfırdan yapılır. Eski kayda
dayanarak "bu zaten var" deme; çıktı `main`'de değilse yoktur (`05_PIPELINE.md` bölüm 1.1).

| No | Görev | Çıktı ve kabul ölçütü | Eski kayıt | Bitiş |
| --- | --- | --- | --- | --- |
| ARD-R1 | Proje seçimi: dört fikri (repair passport, signet quests, lecture-note proof, designer artwork proof) ölçütlerle karşılaştır ve NoteProof'un neden seçildiğini yaz | `docs/analysis/arda-project-selection.md`: karşılaştırma tablosu ve gerekçe; ekipçe okunup onaylanmış | #1 | 22 Kas |
| ARD-R2 | Anket tasarımı: beş soruyu, yanıt seçeneklerini, nerede ve ne zaman paylaşıldığını belgeye geçir; yanıt dışa aktarımını Aysu'ya repo dışından ilet | `docs/analysis/arda-survey-design.md`: soruların tam metni. Ham yanıtlar repoda yok; Aysu dışa aktarımı aldığını teyit etti | #3 | 22 Kas |

Bu görevler de diğerleri gibi branch → PR → `main` yolundan geçer ve commit'lerinde `Task: ARD-R1 (done)`
biçiminde izlenir. Work log'a iki kayıt girilir (`04_GIT_AKISI.md` bölüm 9.1): yapılan iş için kanıtlı bir **Work** kaydı
ve tablodaki "Eski kayıt" numarasını gösteren bir **Correction** kaydı.

### 4.2 Modül görevleri

Sırayla yapılır. Her görev ayrı branch ve ayrı PR'dır.


| No | Görev | Kabul ölçütü | Bağımlılık | Bitiş |
| --- | --- | --- | --- | --- |
| ARD-0 | `core/` paketi: `ns.py`, `hashing.py`, `config.py`, `graph.py` (`02` bölüm 5.1). `pyproject.toml` bağımlılık gruplarını Burak'la birlikte tanımla | `tests/core/` yeşil; IRI üreticiler `02` bölüm 3'teki şemayı üretir; `sha256_hex` küçük harfli 64 hex döner | — | 22 Kas |
| ARD-1 | `register/app.py`: FastAPI uygulaması, `GET /api/health`, ortak hata biçimi, `web/` klasörünün statik sunumu, `search.router`'ın bağlanacağı yer | `/api/health` → 200; bilinmeyen yol ortak hata biçiminde 404 | ARD-0 | 23 Kas |
| ARD-2 | Hesaplar: `POST /api/accounts`, `X-NoteProof-Token` denetimi (K-007) | Token bir kez döner, özetlenerek saklanır; geçersiz token → 401 `unauthorized`; hiçbir yerde gerçek isim alanı yok | ARD-1 | 23 Kas |
| ARD-3 | `POST /api/notes/preview`: tür ve boyut kontrolü, SHA-256, mükerrer kontrolü, `tagger.extract.extract_text`, ardından `tagger.suggest` ve `CopyChecker.check` paralel | Yanıt `02` bölüm 7'deki önizleme biçiminde; çağrıdan sonra grafikte ve `data/` altında **hiçbir kalıcı kayıt yok** (testle kanıtlanır); kayıtlı hash için `alreadyRegistered` dolu | ARD-2; sahtelerle başlanır | 25 Kas |
| ARD-4 | `POST /api/notes`: not ve PROV-O kaydının RDF'i, `shapes.validate.validate_note`, Oxigraph'a yazma, `np:CopyWarning` üçlüleri, `Store.enqueue`, `CopyChecker.add`, dosya ve metnin `data/` altına yazılması | S1 kabul testi; sözlükte olmayan konu → 422 `shape_violation` ve grafikte kayıt yok (S4); `confirmed` yoksa 400; başarılı kayıttan sonra hash kuyrukta | ARD-3, EYL-3, EYL-5 | 26 Kas |
| ARD-5 | `GET /api/notes/{hash}`, `GET /api/notes/{hash}/proof`, `GET /api/vocabulary`; `search.router`'ı bağla | Yanıtlar `02` bölüm 7 biçiminde; proof yokken 404 `proof_pending` | ARD-4, EYL-3 | 26 Kas |
| ARD-6 | Açılışta kopya havuzunu grafikten yükleme; `python -m register.sync_proofs`: `data/proofs/` altındaki proof'ları okuyup notu `timestamped` yapar ve `np:hasProof` ekler | Sunucu yeniden başlayınca önceki notlar kopya denetiminde; `anchor.daily` + `sync_proofs` sonrası `proofStatus` `proven` | ARD-4 | 27 Kas |
| ARD-7 | Entegrasyon (P08): sahteleri gerçek modüllerle değiştir; regtest'te uçtan uca akışı Emine ve Burak'la çalıştır | `05` Faz 2 çıkış kapısı; `register/_stubs.py` silinmiş | herkesin Faz 1 çıktısı | 27 Kas |
| ARD-8 | Revizyon ve kaldırma: aynı hesabın yeni sürümü `prov:wasRevisionOf` ile bağlanır, eski not `superseded` olur; bildirilen notun arşivden kaldırılması | Revizyon testi; kaldırılan notun dosyası, metni ve üçlüleri silinir, zincirdeki kök etkilenmez | ARD-7 | 2 Ara |
| ARD-9 | Final: proposal dosyasını Workbench'te final aşamasına güncelle (teslim durumları, ulaşılan değerler, test raporu linki, doğrulama, lessons learned) | `05` bölüm 3'teki bütün kapılar dolu | AYS-7, EMN-7, BRK-8 | 11 Ara |

**Tasarım notları (aracın uyacağı):**

- Önizleme durumsuzdur: dosya ve çıkarılan metin `previewToken` ile bellekte, kısa bir süre (ör. 15 dakika)
  tutulur; yazar onaylamazsa hiçbir iz kalmaz. Bu, G4'ün ve "author cancels → nothing is saved" adımının gereğidir.
- Grafiğe yazma tek bir işlemdir: shape doğrulaması geçmeden hiçbir üçlü yazılmaz.
- Hesabın gerçek kimliği yoktur; `prov:wasAssociatedWith` takma adlı hesap IRI'sini gösterir.
- `anchor`'a yalnızca `Store.enqueue` ile dokun. Proof dosyalarını sen üretmezsin, yalnızca okursun.
- Başlangıçta `register/_stubs.py` içinde `NP-STUB` işaretli sahteler kullan: sahte sözlük, sahte
  `validate_note`, sahte `suggest`. Her biri `02` bölüm 5'teki imzayla birebir aynı olmalı.

## 5. Başkalarına sağladıkların

| Kime | Ne | Ne zaman |
| --- | --- | --- |
| Herkes | `core/` | 22 Kas |
| Erdener | `/api` uç noktaları (`02` bölüm 7); önce çalışan iskelet, sonra gerçek veri | 23 Kas iskelet, 26 Kas gerçek |
| Emine | Uçtan uca test için çalışan uygulama (`register.app:app`) | 26 Kas |
| Burak | Kuyruğa hash yazan kayıt akışı | 26 Kas |

## 6. Başkalarından beklediklerin

| Kimden | Ne | Hazır değilse |
| --- | --- | --- |
| Eylem | `ontology.vocab.Vocabulary`, `shapes.validate.validate_note` | `NP-STUB` |
| Aleyna | `tagger.extract.extract_text`, `tagger.suggest.suggest` | `NP-STUB` |
| Emine | `copywarn.CopyChecker` (hazır) | — |
| Burak | `anchor.store.Store` (hazır) | — |
| Erdener | `search.router` | Bağlama satırı `NP-TODO(erdener)` ile bekler |

## 7. İdari görevler

- **Team lead:** her cuma faz kapısını kontrol et (`05` bölüm 2); geride kalan görevi olan üyeyle konuş;
  backlog'u ve story durumlarını güncel tut; değerlendiriciye karşı ekibin sözcüsüsün.
- **Mimar:** sözleşme değişikliği taleplerini (`02` bölüm 9) 24 saat içinde karara bağla; bir kural seti
  değişikliği sözleşmeye dokunuyorsa son söz sende (`02` bölüm 9); `07_KARARLAR.md`'deki açık kararları son
  tarihlerinde kapattır.
- **Reviewer:** Burak'ın PR'larını incele ve merge et; Emine'nin PR'larında ikinci reviewer'sın.
- **Proposal:** `proposal/` altındaki dosyaların sahibisin; work log PR'ları dışında bu klasöre kimse dokunmaz.
- Değerlendirme seti için en az 9 kendi notunu Emine'ye ver (`evalset/README.md` kurallarıyla).

## 8. Work log için tipik process'ler

P04 (mimari, sözleşmeler), P07 (kayıt servisi kodu), P08 (entegrasyon), P01 (planlama). En az iki farklı
process'te kayıt gir.
