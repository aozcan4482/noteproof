# Üye dosyası — Eylem Sarıbal (`eylem`)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **Eylem'in** rolünü, kapsamını, kurulumunu ve görevlerini tanımlamak.
Yalnızca Eylem ile çalışan araç bu dosyayı uygular.

## 1. Roller

| | |
| --- | --- |
| İdari rol | Work-log steward: her hafta herkesin kayıt girdiğini ve zincirin sağlam olduğunu kontrol eder |
| Geliştirme rolü | Knowledge engineer: ontoloji, sözlükler, shape'ler; veri modelinin sahibi |
| Lider olduğu process | P06 System analysis |
| Sahip olduğu modül | **Note ontology and SKOS course vocabulary** (E2; story S4, S3 ve S5'in sözlük kısmı) |
| İkincisi olduğu modül | AI tagger (`tagger/`) — Aleyna'nın PR'larını inceler |
| Planlanan iş payı | %14 |
| Sorumlu olduğu ara teslim | Ders sözlüğü, not ontolojisi ve shape'ler (30 Ekim, gecikmiş) |

## 2. Kapsam

**Senin klasörlerin:** `ontology/`, `shapes/`, `tests/ontology/`, `tests/shapes/`, `docs/worklog/eylem.md`.

**Dokunmayacakların:** diğer bütün klasörler. SPARQL arama sorguları `search/queries/` altında
Erdener'indir; `skos:narrower*` yolunu doğru kullandığını sen incelersin ama dosyayı o yazar.

Senin modülün en çok beklenen modüldür: tagger, kayıt servisi, arama ve değerlendirme seti senin
konu kimliklerine dayanır. Bu yüzden önce kimlikleri yayımla, sonra ayrıntıyı doldur. Bir kimlik `main`'e
girdikten sonra yeniden adlandırılmaz (`03` bölüm 7).

## 3. Ek kurulum

`06_KURULUM.md` tamamlandıktan sonra:

1. RDFLib ve pySHACL `pip install -e ".[dev,all]"` ile gelir. Kontrol: `python -c "import rdflib, pyshacl; print('ok')"`.
2. İsteğe bağlı: Turtle dosyalarını görsel incelemek için Protégé (`https://protege.stanford.edu`).
   Zorunlu değil; dosyaları araç yazar, sen VS Code'da okursun.
3. VS Code için bir Turtle sözdizimi eklentisi (isteğe bağlı).
4. `.env`: yalnızca `NOTEPROOF_DATA_DIR=./data`.

## 4. Görevler

### 4.1 Önce: proposal'da yapılmış görünen işler

Proposal'ın work log'unda aşağıdaki işler yapılmış olarak kayıtlı, ama repoda hiçbirinin çıktısı ya da
kanıtı yok. Bu işler **yapılmamış sayılır** ve modül görevlerinden önce, sıfırdan yapılır. Eski kayda
dayanarak "bu zaten var" deme; çıktı `main`'de değilse yoktur (`05_PIPELINE.md` bölüm 1.1).

| No | Görev | Çıktı ve kabul ölçütü | Eski kayıt | Bitiş |
| --- | --- | --- | --- | --- |
| EYL-R1 | Sözlük kapsamı: Mastering Bitcoin'in (3. baskı) 14 bölümünü kitabın kendisinden çıkar; her bölüm için konu kimliği (`Topic_<PascalCase>`) ile Türkçe ve İngilizce etiket öner | `docs/analysis/eylem-vocabulary-scope.md`: 14 satırlık tablo; bölüm adları kitapla birebir; kimlikler `02` bölüm 3 kalıbında | #5 | 21 Kas |
| EYL-R2 | Transactions bölümünün alt konularını broader/narrower bağlantılarıyla taslakla (en az `Topic_TransactionFees` ve altında `Topic_FeeRate`) | Aynı dosyada hiyerarşi taslağı; EYL-2 bu taslaktan yazılır | #6 | 22 Kas |

Bu görevler de diğerleri gibi branch → PR → `main` yolundan geçer ve commit'lerinde `Task: EYL-R1 (done)`
biçiminde izlenir. Work log'a iki kayıt girilir (`04_GIT_AKISI.md` bölüm 9.1): yapılan iş için kanıtlı bir **Work** kaydı
ve tablodaki "Eski kayıt" numarasını gösteren bir **Correction** kaydı.

### 4.2 Modül görevleri

| No | Görev | Kabul ölçütü | Bağımlılık | Bitiş |
| --- | --- | --- | --- | --- |
| EYL-1 | K-001: namespace kararını Arda ile kapat | `07_KARARLAR.md` K-001 "Verildi"; `core/ns.py` son değerde | — | 22 Kas |
| EYL-2 | `ontology/courses.ttl`: `np:CourseScheme`; `np:Course_SEN0401`; dersin konuları (EYL-R1 ve EYL-R2'de çıkardığın 14 bölüm ve Transactions bölümünün alt konuları). Her kavram: `skos:prefLabel` `@tr` ve `@en`, `skos:broader` / `skos:narrower`, `skos:inScheme`; ders için `skos:notation "SEN0401"` | Dosya RDFLib ile ayrıştırılıyor; her konunun derse giden bir `broader` zinciri var; `Topic_Transactions` altında `Topic_TransactionFees`, onun altında `Topic_FeeRate` var (S5 kabul kriteri) | EYL-1, EYL-R2 | 22 Kas |
| EYL-3 | `ontology/vocab.py`: `Concept` ve `Vocabulary` (`02` bölüm 5.2); `python -m ontology.list` bütün kimlikleri ve etiketleri tablo olarak yazar | `tests/ontology/` yeşil: `narrower("Topic_Transactions")` hem `Topic_TransactionFees` hem `Topic_FeeRate` içerir; bilinmeyen kimlik için `is_topic` `False` | EYL-2 | 23 Kas |
| EYL-4 | `ontology/noteproof.ttl`: `02` bölüm 4'teki sınıflar ve özellikler, `rdfs:label` ve `rdfs:comment` ile; `ontology/context.jsonld` | Bütün terimler `02` bölüm 4 ile birebir aynı adda; gerçek isim ya da öğrenci numarası tutan özellik yok | EYL-1 | 23 Kas |
| EYL-5 | `shapes/note.shapes.ttl` ve `shapes/validate.py` (`validate_note`, `Violation`, `Report`) | Olumlu örnek uyuyor; dört olumsuz örnek adıyla reddediliyor: hash yok, ders yok, sözlükte olmayan konu, `tagsConfirmed` `true` değil. İhlal mesajları Türkçe. Boş grafik sessizce "uyuyor" dönmez | EYL-3, EYL-4 | 24 Kas |
| EYL-6 | Kimlik listesini duyur: Aleyna (tagger istemi), Emine (`manifest.csv`), Erdener (arama) için `python -m ontology.list` çıktısını PR açıklamasına koy | Üçü de kimlikleri bu listeden alıyor | EYL-3 | 24 Kas |
| EYL-7 | Entegrasyon desteği: Arda'nın ürettiği gerçek not grafiğini shape'lerden geçir; Erdener'in arama sorgusunu incele | Kayıt servisinin testlerinde pySHACL gerçek shape'lerle çalışıyor (DoD 2) | ARD-4, ERD-5 | 27 Kas |
| EYL-8 | Sözlük genişletme: pilot gönüllülerinin not paylaşacağı dersler (Aysu'dan liste) için ders ve konu kavramları | Yeni dersler aynı kalıpta; mevcut kimlikler değişmemiş | AYS-3 | 2 Ara |
| EYL-9 | O2 ölçümü: pilot notlarından onaylı etiketleri shape'lerden geçenlerin oranı | Sayı ve nasıl ölçüldüğü Emine'nin raporunda | pilot | 10 Ara |

**Tasarım notları (aracın uyacağı):**

- Kimlik kalıbı: ders `Course_<KOD>`, konu `Topic_<PascalCase>`; İngilizce, boşluksuz, Türkçe karakter yok.
- Etiketler iki dilde. Arayüz `@tr` etiketini gösterir; tagger istemi ikisini de görür.
- Dersin altında en çok üç düzey konu olur (konu → alt konu → alt-alt konu). Daha derini aramayı ve etiketlemeyi zorlaştırır.
- Shape'ler yalnızca notun kaydedilmeye hazır hâlini denetler; önizleme aşamasındaki öneriyi denetlemez.
- `validate_note` hiçbir şey yazmaz ve ağa çıkmaz.

## 5. Başkalarına sağladıkların

| Kime | Ne | Ne zaman |
| --- | --- | --- |
| Aleyna, Emine, Erdener, Arda | Konu ve ders kimlikleri (`courses.ttl`, `python -m ontology.list`) | 22–23 Kas |
| Arda, Aleyna, Erdener | `Vocabulary` | 23 Kas |
| Arda | `validate_note` | 24 Kas |
| Arda, Erdener | Ontoloji terimleri ve JSON-LD context | 23 Kas |

## 6. Başkalarından beklediklerin

| Kimden | Ne | Hazır değilse |
| --- | --- | --- |
| Arda | `core.ns` | Namespace'i geçici olarak dosyanın başındaki tek bir sabitten oku, `NP-TODO(arda)` bırak |
| Aysu | Pilot dersleri listesi | EYL-8 bekler |

## 7. İdari görevler

- **Work-log steward.** Her cuma: `main`'deki `proposal/proposal.json`'ı Workbench'te aç, zincir
  kontrolünün temiz olduğuna bak; Arda, Aysu, Aleyna ve Emine'nin o hafta kayıt girip girmediğini ve
  `docs/worklog/<slug>.md` taslaklarında "girilmedi" kalan satır olup olmadığını kontrol et. (Eylem,
  Burak ve Erdener'i Aleyna kontrol eder.) Sonucu `docs/worklog/steward-check.md`'ye bir satır olarak yaz;
  eksiği olan üyeye aynı gün haber ver. Zincirde anomali görürsen kimse yeni kayıt eklemeden Arda'ya bildir.
- **Reviewer:** Aleyna'nın `tagger/` PR'larını incele; özellikle modelin yalnızca sözlükteki kimlikleri döndürdüğünü.
- **System analysis lideri (P06):** veri modeliyle ilgili soruların ilk muhatabısın.
- Değerlendirme seti için en az 9 kendi notunu Emine'ye ver.

## 8. Work log için tipik process'ler

P06 (analiz, sözlük kapsamı), P05 (ontoloji ve shape tasarımı), P07 (okuyucu ve doğrulama kodu), P09 (shape testleri).
