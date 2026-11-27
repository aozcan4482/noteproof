# Üye dosyası — Aleyna Cebeci (`aleyna`)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **Aleyna'nın** rolünü, kapsamını, kurulumunu ve görevlerini tanımlamak.
Yalnızca Aleyna ile çalışan araç bu dosyayı uygular.

## 1. Roller

| | |
| --- | --- |
| İdari rol | Work-log steward: her hafta herkesin kayıt girdiğini ve zincirin sağlam olduğunu kontrol eder |
| Geliştirme rolü | AI and language-model engineer |
| Lider olduğu process | P05 Design definition |
| Sahip olduğu özellik | **AI tagger** (E2; story S3) |
| İkincisi olduğu modüller | Ontoloji ve sözlük (`ontology/`, `shapes/`) ile kopya uyarısı ve değerlendirme seti (`copywarn/`, `evalset/`) — Eylem'in ve Emine'nin PR'larını inceler |
| Planlanan iş payı | %14 |
| Sorumlu olduğu ara teslim | 27 Kasım: AI tagger, kopya uyarısı ve konu araması |

## 2. Kapsam

**Senin klasörlerin:** `tagger/`, `tests/tagger/`, `evalset/run_tagger.py` (tek dosya istisnası; `evalset/`
klasörünün geri kalanı Emine'nindir), `docs/worklog/aleyna.md`.

**Dokunmayacakların:** diğer bütün klasörler. Sözlüğü `ontology.vocab.Vocabulary` ile okursun; konu
eklemek ya da değiştirmek gerekiyorsa Eylem'e iletirsin.

Tagger'ın üç kesin sınırı vardır:

1. **Yalnızca önerir.** Hiçbir şey kaydetmez, grafiğe ya da diske yazmaz. Kaydı, yazar onayladıktan sonra kayıt servisi yapar.
2. **Yalnızca sözlükten seçer.** Modelin yanıtı kodla süzülür; sözlükte olmayan kimlik çıktıya giremez.
3. **Dil modelini etiketleme için çağıran tek bileşendir.** Başka modüller modele `tagger/llm.py` üzerinden ulaşır.

## 3. Ek kurulum

`06_KURULUM.md` tamamlandıktan sonra:

1. **Tesseract OCR** (fotoğraftan metin için).
   - Windows: UB Mannheim'ın Tesseract kurulum dosyası; kurulumda ek dil olarak **Turkish** seçilir;
     kurulum klasörü PATH'e eklenir.
   - macOS: `brew install tesseract tesseract-lang`.
   - Kontrol: `tesseract --version` ve `tesseract --list-langs` çıktısında `tur` ve `eng`.
2. Python paketleri `pip install -e ".[dev,all]"` ile gelir: pypdf, pytesseract, Pillow, httpx.
   Kontrol: `python -c "import pypdf, pytesseract, PIL; print('ok')"`.
3. **Dil modeli erişimi** (K-005 kararından sonra): seçilen sağlayıcıdan bir API anahtarı al.
4. **`.env`:**

   ```
   NOTEPROOF_DATA_DIR=./data
   NOTEPROOF_LLM_PROVIDER=...
   NOTEPROOF_LLM_MODEL=...
   NOTEPROOF_LLM_API_KEY=...
   ```

   API anahtarı repoya, commit mesajına, test dosyasına, ekran görüntüsüne girmez.

## 4. Görevler

### 4.1 Önce: proposal'da yapılmış görünen işler

Proposal'ın work log'unda aşağıdaki işler yapılmış olarak kayıtlı, ama repoda hiçbirinin çıktısı ya da
kanıtı yok. Bu işler **yapılmamış sayılır** ve modül görevlerinden önce, sıfırdan yapılır. Eski kayda
dayanarak "bu zaten var" deme; çıktı `main`'de değilse yoktur (`05_PIPELINE.md` bölüm 1.1).

| No | Görev | Çıktı ve kabul ölçütü | Eski kayıt | Bitiş |
| --- | --- | --- | --- | --- |
| ALY-R1 | Metin çıkarma karşılaştırması: kendi notlarından en az 3 PDF ve 3 fotoğrafta pypdf ve Tesseract'ı (`tur+eng`) dene; ne kadar metin çıktı, Türkçe karakterler ve el yazısı ne oldu | `docs/analysis/aleyna-text-extraction.md`: dosya başına sonuç tablosu ve varılan karar. Not içerikleri ve kişisel veri belgede yok | #7 | 22 Kas |
| ALY-R2 | İlk istem: modelin konularını sözlüğe sınırlayan bir istem yaz ve üç notta dene (sözlük olarak EYL-R1'in tablosu) | `docs/analysis/aleyna-prompt-v0.md`: istem metni, üç deneme sonucu, sözlük dışına çıkan önerilerin sayısı, çıkarılan dersler. ALY-1 ve ALY-4 bundan beslenir | #8 | 23 Kas |

Bu görevler de diğerleri gibi branch → PR → `main` yolundan geçer ve commit'lerinde `Task: ALY-R1 (done)`
biçiminde izlenir. Work log'a iki kayıt girilir (`04_GIT_AKISI.md` bölüm 9.1): yapılan iş için kanıtlı bir **Work** kaydı
ve tablodaki "Eski kayıt" numarasını gösteren bir **Correction** kaydı.

### 4.2 Modül görevleri

| No | Görev | Kabul ölçütü | Bağımlılık | Bitiş |
| --- | --- | --- | --- | --- |
| ALY-1 | K-005: sağlayıcı ve model kararı. İki ya da üç adayı ALY-R2'deki istemle, üç notta karşılaştır | `07_KARARLAR.md` K-005 "Verildi" (gerekçesiyle) | ALY-R2 | 23 Kas |
| ALY-2 | `tagger/llm.py`: `LLMClient` arayüzü, seçilen sağlayıcının istemcisi, `client_from_env()`; `tests/tagger/fake_llm.py` içinde `FakeLLM` | Anahtar yokken `client_from_env()` açık bir hata verir; testler ağa çıkmadan `FakeLLM` ile geçer | ALY-1 | 23 Kas |
| ALY-3 | `tagger/extract.py`: `extract_text` — PDF (pypdf), JPEG/PNG (Tesseract, `tur+eng`), düz metin ve Markdown | Her tür için test; desteklenmeyen tür `ValueError`; metni olmayan dosya boş string döner. ALY-R1'deki karşılaştırmanın sonucu docstring'de | ALY-R1 | 23 Kas |
| ALY-4 | `tagger/suggest.py`: `suggest` ve `TagSuggestion`. İstem sözlüğü kimlik + iki dilde etiket olarak içerir, modelden JSON ister; yanıt ayrıştırılır ve süzülür | S3 kabul testi (`FakeLLM` ile): transaction fee notu → `Course_SEN0401` ve `Topic_TransactionFees`. Model sözlükte olmayan bir kimlik döndürürse çıktıda yok. Bozuk JSON → boş öneri, hata değil. Fonksiyon hiçbir şey kaydetmiyor | ALY-2, EYL-3 | 25 Kas |
| ALY-5 | `evalset/run_tagger.py`: O3 ölçümü. Her değerlendirme notu için öneriyi üret, `manifest.csv`'deki bilinen konularla karşılaştır; ölçü: önerilen konulardan bilinen konular arasında olanların oranı. JSON rapor; hedefin altındaysa çıkış kodu 1; set boşsa açık mesaj ve çıkış kodu 1 | Sentetik örneklerle testli; CI'da API anahtarı sırrı yoksa adım "atlandı" notuyla geçer, varsa çalışır | ALY-4, EMN-2 | 27 Kas |
| ALY-6 | İstem iyileştirme: 60 gerçek notta O3 ≥ %80. Sık karışan konuları Eylem'e bildir (etiket ya da hiyerarşi düzeltmesi gerekebilir) | `python -m evalset.run_tagger` ≥ %80; sonuç Emine'nin raporunda | EMN-2 | 2 Ara |
| ALY-7 | Maliyet ve hız: aynı metin için öneriyi önbelleğe al; uzun notlarda metni kısalt; önizleme 10 saniyeyi geçmesin | Ölçüm `docs/reports/` için Emine'ye verilir | ALY-4 | 2 Ara |
| ALY-8 | (Vakit kalırsa) Arama yanıtları: Erdener'in `search/answer.py` dosyası için istem incelemesi. Model yalnızca grafiğin döndürdüğü notları ifade eder ve onlara atıf yapar | Yanıtta grafikten gelmeyen bilgi yok; her cümle bir nota bağlı | ERD-5 | 4 Ara |

**Tasarım notları (aracın uyacağı):**

- İstem ve yanıt biçimi kodda tek bir yerde durur; sözlük isteme her çağrıda `Vocabulary`'den üretilir, elle yazılmaz.
- Özet iki cümledir ve notun dilindedir.
- Modele gönderilen metin not içeriğidir; günlüklere yazılmaz. Günlüğe yalnızca hash ve süre yazılır.
- Model ders bulamazsa `course` `None`, `topics` boş döner; yazar listeden kendisi seçer. Tahmin uydurma.
- Sağlayıcıya özel her şey `tagger/llm.py` içinde kalır; `suggest.py` yalnızca `LLMClient.complete` çağırır.

## 5. Başkalarına sağladıkların

| Kime | Ne | Ne zaman |
| --- | --- | --- |
| Arda | `extract_text` | 23 Kas |
| Arda | `suggest` | 25 Kas |
| Emine | Tagger ölçümü (O3) | 27 Kas ilk sonuç, 2 Ara hedef |
| Erdener | `tagger.llm.client_from_env` (arama yanıtları için) | 23 Kas |

## 6. Başkalarından beklediklerin

| Kimden | Ne | Hazır değilse |
| --- | --- | --- |
| Eylem | `Vocabulary` ve konu kimlikleri | Testte birkaç kavramlık sahte sözlük (`NP-STUB`) |
| Emine | 60 not ve `manifest.csv` | ALY-5'i sentetik örneklerle yaz, gerçek ölçümü set gelince çalıştır |

## 7. İdari görevler

- **Work-log steward.** Her cuma: `main`'deki `proposal/proposal.json`'ı Workbench'te aç, zincir
  kontrolünün temiz olduğuna bak; Eylem, Burak ve Erdener'in o hafta kayıt girip girmediğini ve
  `docs/worklog/<slug>.md` taslaklarında "girilmedi" kalan satır olup olmadığını kontrol et. (Diğer dört
  üyeyi Eylem kontrol eder.) Sonucu `docs/worklog/steward-check.md`'ye yaz; eksiği olana aynı gün haber ver.
- **Reviewer:** Eylem'in `ontology/` ve `shapes/` PR'larını, Emine'nin `copywarn/` ve `evalset/` PR'larını incele.
- **Design definition lideri (P05):** tasarım modelleriyle (sınıf, sıra, durum diyagramları) kod arasındaki farkları Arda'ya bildir.
- Değerlendirme seti için en az 9 kendi notunu Emine'ye ver.

## 8. Work log için tipik process'ler

P05 (istem ve arayüz tasarımı), P06 (model ve OCR karşılaştırması), P07 (kod), P09 (tagger ölçümü).
