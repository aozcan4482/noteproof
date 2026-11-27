# 02 — Mimari ve sabit sözleşmeler

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **hangi kodun nerede duracağını, kimin olduğunu ve modüllerin birbirine hangi
sabit arayüzlerle bağlandığını** tanımlamak. Yedi ayrı araçla yazılan kodun birleşince çalışması bu
dosyaya bağlıdır. Buradaki bir adı, imzayı ya da alanı kendi başına değiştirme (bölüm 9).

## 1. Teknoloji yığını

| Katman | Seçim |
| --- | --- |
| Dil | Python ≥ 3.11 (CI: 3.12). Paketler repo kökünde, `pytest` `pythonpath = ["."]` ile bulur |
| HTTP API | FastAPI + uvicorn (`register/app.py`) |
| Bilgi grafiği | RDFLib (Python'da işleme), Oxigraph (`pyoxigraph`, gömülü depo), SPARQL |
| Doğrulama | SHACL, pySHACL |
| Sözlükler | schema.org, PROV-O, SKOS; kayıtlar JSON-LD olarak taşınır |
| Zincir | Bitcoin Core (signet; testlerde regtest), JSON-RPC. Timestamp kuyruğu SQLite |
| Metin çıkarma | pypdf (PDF), Tesseract + pytesseract (fotoğraf) |
| Dil modeli | `tagger/llm.py` arayüzü arkasında; sağlayıcı kararı `07_KARARLAR.md` K-005 |
| Arayüz | Statik HTML + CSS + sade JavaScript (ES modülleri). Çerçeve yok, derleme adımı yok |
| Testler | pytest; tarayıcı tarafı için `node --test` |

Bağımlılıklar `pyproject.toml` içinde modül gruplarıyla tutulur:
`[project.optional-dependencies]` altında `dev`, `register`, `ontology`, `tagger`, `search`, `all`.
Paket listesi `[tool.setuptools] packages` altında açıkça yazılır (repo kökünde birden çok paket olduğu için
otomatik keşif çalışmaz); yeni bir üst klasör paketi eklendiğinde bu listeye de girer.
Dosyanın sahibi Burak'tır, bağımlılık listesini Arda onaylar. Yeni bir kütüphaneye ihtiyaç varsa
kendi branch'inde `pyproject.toml`'u düzenleme; `04_GIT_AKISI.md` bölüm 8'deki ortak dosya talebini kullan.

## 2. Klasörler ve sahiplik

Bir klasörün sahibi olmayan üye ve onun aracı, o klasörde dosya oluşturmaz ve değiştirmez.

| Yol | İçerik | Sahip | İkinci (reviewer) |
| --- | --- | --- | --- |
| `core/` | Ortak çekirdek: namespace, IRI üreticiler, hash, ayarlar, grafik deposu | arda | burak |
| `register/` | Kayıt servisi ve HTTP API | arda | burak |
| `anchor/` | Bitcoin timestamp servisi | burak | arda |
| `ontology/` | Not ontolojisi, SKOS ders/konu sözlüğü, JSON-LD context, sözlük okuyucu | eylem | aleyna |
| `shapes/` | SHACL shape'leri ve doğrulama fonksiyonu | eylem | aleyna |
| `tagger/` | Metin çıkarma, dil modeli istemcisi, etiket önerisi | aleyna | eylem |
| `copywarn/` | Kopya uyarısı | emine | aleyna |
| `evalset/` | Değerlendirme seti ve ölçüm betikleri | emine | aleyna |
| `evalset/run_tagger.py` | Tagger ölçümü (tek dosya istisnası) | aleyna | emine |
| `search/` | SPARQL arama servisi ve `/api/search` router'ı | erdener | aysu |
| `web/` | Statik sayfalar: arama, yükleme, proof | erdener | aysu |
| `tests/<paket>/` | O paketin testleri | paketin sahibi | paketin ikincisi |
| `tests/vectors/` | Python ve JavaScript'in ortak test vektörleri | burak | erdener |
| `tests/web/` | Tarayıcı kodunun testleri | erdener | burak |
| `tests/e2e/` | Uçtan uca testler | emine | arda |
| `docs/acceptance/`, `docs/pilot/` | Kabul senaryoları, pilot planı ve sonuçları | aysu | emine |
| `docs/reports/` | Test raporu, değerlendirme raporu | emine | arda |
| `docs/ops/` | Node, signet, zamanlama, release notları | burak | arda |
| `docs/guide/`, `docs/minutes/`, `README.md` | Kullanıcı kılavuzu, toplantı notları | erdener | aysu |
| `docs/analysis/<slug>-<konu>.md` | Üyenin analiz, karşılaştırma ve taslak belgeleri | o üye | modülünün ikincisi |
| `docs/worklog/<slug>.md` | Üyenin work log taslakları | o üye | — |
| `AGENTS.md`, `docs/rules/` | Kural seti (K-010) | erdener | — |
| `proposal/` | Proposal dosyaları ve work log zinciri | arda | erdener |
| `pyproject.toml`, `.gitignore`, `.gitattributes`, `.github/workflows/ci.yml`, `.github/CODEOWNERS` | Ortak yapılandırma | burak | arda |
| `.github/workflows/copywarn.yml` | Kopya uyarısı CI'ı | emine | burak |
| `.github/pull_request_template.md` | PR şablonu | emine | burak |

Çalışma verisi repoya girmez. Hepsi `data/` altında durur ve `.gitignore`'dadır:

```
data/notes/<hash>.<uzantı>    yüklenen not dosyaları
data/text/<hash>.txt          çıkarılan metin
data/graph/                   Oxigraph deposu
data/noteproof.sqlite         timestamp kuyruğu
data/proofs/<hash>.json       üretilen proof dosyaları
```

Aktivite adımlarının sahipleri (`01_PROJE.md` bölüm 3): 1, 5, 6, 14–17 → `web/`; 2, 3, 7'nin çağrılması,
8, 9 → `register/`; 4a → `tagger/`; 4b → `copywarn/`; 7'nin kuralları → `shapes/`; 10–13 → `anchor/`;
14'ün sorgusu → `search/`.

## 3. Adlandırma ve kimlikler

**Namespace.** Tek bir yerde tanımlıdır ve oradan içe aktarılır; hiçbir dosyada elle yeniden yazılmaz.

```python
# core/ns.py
NAMESPACE = "https://github.com/aozcan4482/noteproof/ns#"   # K-001
```

Turtle ve SPARQL dosyalarında önek her zaman `np:` olur. Diğer önekler: `schema:` `<https://schema.org/>`,
`prov:`, `skos:`, `sh:`, `xsd:`.

**IRI şeması.** `{NS}` namespace'tir, `{hash}` notun küçük harfli 64 karakterlik SHA-256 hex'idir.

| Şey | IRI |
| --- | --- |
| Not | `{NS}note/{hash}` |
| Kayıt | `{NS}registration/{hash}` |
| Proof | `{NS}proof/{hash}` |
| Hesap | `{NS}account/{takma-ad}` |
| Günlük timestamp | `{NS}timestamp/{txid}` |
| Kopya uyarısı | `{NS}copywarning/{sonraki-hash}-{önceki-hash}` |
| Ders | `{NS}Course_{KOD}` — ör. `np:Course_SEN0401` |
| Konu | `{NS}Topic_{PascalCase}` — ör. `np:Topic_TransactionFees` |
| Kavram şeması | `{NS}CourseScheme` |

API'de, `evalset/manifest.csv`'de ve tagger çıktısında dersler ve konular **yerel kimlikleriyle** geçer:
`Course_SEN0401`, `Topic_TransactionFees`. Etiket metniyle (ör. "Transaction fees") eşleştirme yapılmaz.

**Yazım.** JSON ve JSON-LD alanları `camelCase`; Python `snake_case`; ortam değişkenleri `NOTEPROOF_` önekli;
zamanlar ISO 8601, UTC; hash'ler küçük harfli hex.

**Durum değerleri.**

| Alan | Değerler |
| --- | --- |
| Not durumu (`np:status`) | `uploaded`, `tagged`, `confirmed`, `registered`, `timestamped`, `superseded` |
| Proof durumu (API `proofStatus`) | `pending`, `proven` |
| Proof rozeti (arayüz) | Beklemede (`pending`), Kanıtlandı (`proven`), Değiştirilmiş (dosya proof ile eşleşmedi) |
| Batch durumu (`anchor/store.py`) | `built`, `broadcast`, `confirmed` |

## 4. Veri modeli (ontoloji terimleri)

`ontology/noteproof.ttl` bu terimleri tanımlar. Diğer modüller yalnızca bu adları kullanır.

| Sınıf | Üst sınıf | Özellikler |
| --- | --- | --- |
| `np:Note` | `schema:CreativeWork` | `np:noteHash`, `schema:name` (başlık), `schema:encodingFormat` (MIME türü), `schema:abstract` (özet), `np:course` (tam 1), `np:topic` (en az 1), `np:tagsConfirmed` (`true` olmalı), `np:status`, `prov:wasGeneratedBy`, `prov:wasAttributedTo`, `prov:wasRevisionOf` (varsa), `np:hasProof` (varsa) |
| `np:Registration` | `prov:Activity` | `prov:wasAssociatedWith` (hesap), `prov:endedAtTime` |
| `np:StudentAccount` | `prov:Agent` | `schema:alternateName` (takma ad). Gerçek isim ya da öğrenci numarası tutan özellik **yoktur** |
| `np:DailyTimestamp` | — | `np:day`, `np:merkleRoot`, `np:txid`, `np:blockHeight`, `np:blockHash`, `np:blockTime`, `np:network` |
| `np:Proof` | — | Bölüm 6'daki proof dosyasının alanları |
| `np:CopyWarning` | — | `np:laterNote`, `np:earlierNote`, `np:score`, `np:method` |
| Ders, Konu | `skos:Concept` | `skos:prefLabel` (`@tr` ve `@en`), `skos:notation` (ders kodu), `skos:broader`, `skos:narrower`, `skos:inScheme np:CourseScheme` |

`NoteShape` şunları reddeder: hash'i olmayan not, dersi olmayan not, konusu olmayan not, şemada olmayan
konu, `np:tagsConfirmed` değeri `true` olmayan not.

## 5. Python sözleşmeleri

Aşağıdaki imzalar sabittir. Bir modül diğerine yalnızca bu fonksiyonlar üzerinden dokunur; başka bir
paketin iç fonksiyonlarını ve alt çizgiyle başlayan adlarını içe aktarma.

### 5.1 `core/` — sahip: arda

```python
# core/ns.py
NAMESPACE: str
def note_iri(note_hash: str) -> str
def registration_iri(note_hash: str) -> str
def proof_iri(note_hash: str) -> str
def account_iri(pseudonym: str) -> str
def timestamp_iri(txid: str) -> str
def concept_iri(local_id: str) -> str          # "Topic_FeeRate" -> tam IRI

# core/hashing.py
def sha256_hex(data: bytes) -> str             # küçük harfli 64 hex

# core/config.py
def data_dir() -> pathlib.Path                 # NOTEPROOF_DATA_DIR, varsayılan ./data

# core/graph.py
def open_store(path: pathlib.Path | None = None) -> "pyoxigraph.Store"
```

### 5.2 `ontology/` ve `shapes/` — sahip: eylem

```python
# ontology/vocab.py
@dataclass(frozen=True)
class Concept:
    id: str                 # "Topic_TransactionFees"
    label_tr: str
    label_en: str
    broader: str | None     # üst kavramın id'si; dersler için None

class Vocabulary:
    @classmethod
    def load(cls) -> "Vocabulary"                       # ontology/courses.ttl'i okur
    def courses(self) -> list[Concept]
    def topics(self, course_id: str) -> list[Concept]   # dersin bütün konuları (alt konular dahil)
    def is_course(self, concept_id: str) -> bool
    def is_topic(self, concept_id: str) -> bool
    def narrower(self, topic_id: str) -> list[str]      # geçişli; kendisi dahil değil
    def as_graph(self) -> "rdflib.Graph"

# shapes/validate.py
@dataclass(frozen=True)
class Violation:
    shape: str      # ör. "NoteShape"
    path: str       # ör. "np:topic"
    message: str    # Türkçe, kullanıcıya gösterilebilir

@dataclass(frozen=True)
class Report:
    conforms: bool
    violations: list[Violation]

def validate_note(note_graph: "rdflib.Graph") -> Report
```

### 5.3 `tagger/` — sahip: aleyna

```python
# tagger/extract.py
def extract_text(data: bytes, media_type: str) -> str
# Desteklenen media_type: application/pdf, image/jpeg, image/png, text/plain, text/markdown.
# Desteklenmeyen tür -> ValueError. Metin çıkmazsa boş string döner.

# tagger/llm.py
class LLMClient(Protocol):
    def complete(self, prompt: str, *, system: str | None = None) -> str
def client_from_env() -> LLMClient            # NOTEPROOF_LLM_* değişkenlerinden

# tagger/suggest.py
@dataclass(frozen=True)
class TagSuggestion:
    course: str | None      # "Course_SEN0401" ya da None
    topics: list[str]       # yalnızca sözlükteki "Topic_*" kimlikleri; boş olabilir
    summary: str            # iki cümle, notun dilinde

def suggest(text: str, vocabulary: Vocabulary, llm: LLMClient | None = None) -> TagSuggestion
```

`suggest` hiçbir şey kaydetmez ve sözlükte olmayan kimliği asla döndürmez (modelin çıktısı kodla süzülür).
Dil modelini etiketleme için çağıran tek bileşen `tagger/`'dır.

### 5.4 `copywarn/` — sahip: emine (mevcut kod)

```python
from copywarn import CopyChecker, CopyWarning, RegisteredNote

RegisteredNote(note_id: str, text: str, author: str, registered_at: str, proof: str = "")
CopyChecker(threshold: float = 0.60)
    .add(note: RegisteredNote) -> None                                   # adım 9'dan sonra
    .check(text: str, author: str | None = None, before: str | None = None) -> list[CopyWarning]   # adım 4b
CopyWarning: earlier_note_id, earlier_author, earlier_registered_at, earlier_proof, score, method
```

`note_id` notun hash'idir; `author` takma addır. Aynı hesabın notu kopya sayılmaz.

### 5.5 `anchor/` — sahip: burak (mevcut kod)

```python
from anchor.store import Store
Store(path: str).enqueue(note_hash_hex: str, registered_at: str | None = None) -> bool
# True: kuyruğa eklendi. False: bu hash zaten kayıtlıydı.

from anchor import proof
proof.verify_offline(proof: dict, note_file: bytes) -> tuple[bool, str]
proof.verify_on_chain(proof: dict, rpc) -> tuple[bool, str]

# Günlük iş
python -m anchor.daily --db data/noteproof.sqlite --out data/proofs
```

Kayıt servisi timestamp servisine yalnızca `Store.enqueue` ile dokunur. Merkle kuralları (yaprak öneki
`0x00`, iç düğüm öneki `0x01`, tek kalan düğüm kopyalanmadan yukarı taşınır, tek SHA-256) sabittir;
`web/js/verify.js` aynı kuralları uygular ve `tests/vectors/` altındaki vektörlerle doğrulanır.

### 5.6 `search/` — sahip: erdener

```python
# search/service.py
@dataclass(frozen=True)
class NoteCard:
    note_hash: str
    title: str
    course: str                  # "Course_SEN0401"
    topics: list[str]
    summary: str
    author: str                  # takma ad
    registered_at: str
    proof_status: str            # "pending" | "proven"
    possible_copy_of: str | None # önceki notun hash'i

def search_notes(store, course: str | None = None, topic: str | None = None, q: str | None = None) -> list[NoteCard]
# topic verilirse o konu ve bütün alt konuları aranır (SPARQL: skos:narrower*).

# search/router.py
router: fastapi.APIRouter      # GET /api/search; register/app.py bunu bağlar
```

## 6. Proof dosyası (JSON-LD)

`anchor/proof.py` üretir, `web/js/verify.js` okur. Alanlar ve yazımları sabittir.

```json
{
  "@context": {"@vocab": "https://github.com/aozcan4482/noteproof/ns#"},
  "@type": "Proof",
  "@id": "https://github.com/aozcan4482/noteproof/ns#proof/<hash>",
  "noteHash": "<64 hex>",
  "hashAlgorithm": "SHA-256",
  "leafPrefix": "00",
  "nodePrefix": "01",
  "merklePath": [{"side": "left|right", "sibling": "<64 hex>"}],
  "merkleRoot": "<64 hex>",
  "network": "signet|regtest",
  "txid": "<64 hex>",
  "blockHeight": 0,
  "blockHash": "<64 hex>",
  "blockTime": "2026-11-12T20:15:00+00:00"
}
```

Proof sayfası yalnızca üç şeyle çalışır: bu dosya, notun kendisi ve herhangi bir public signet node'u.
Arşivin sunucusu kapalıyken de çalışmak zorundadır (S7).

## 7. HTTP API

Sunan: `register/app.py` (arda). Kullanan: `web/` (erdener). Taban yol `/api`. İstek ve yanıtlar JSON'dur
(dosya yükleme hariç). Kimlik: `X-NoteProof-Token` başlığı; okuma uç noktaları ve proof kimlik istemez.

| Uç nokta | İstek | Yanıt |
| --- | --- | --- |
| `GET /api/health` | — | `200 {"status": "ok"}` |
| `POST /api/accounts` | `{"pseudonym": "..."}` | `201 {"account": "...", "token": "..."}` — token yalnızca bir kez gösterilir |
| `GET /api/vocabulary` | — | `200 {"courses": [{"id", "labelTr", "labelEn", "topics": [{"id", "labelTr", "labelEn", "broader"}]}]}` |
| `POST /api/notes/preview` | `multipart/form-data`, alan adı `file` | `200` aşağıdaki önizleme. **Hiçbir şey kaydedilmez** |
| `POST /api/notes` | Aşağıdaki onay gövdesi | `201 {"noteHash", "registeredAt", "status": "registered", "proofStatus": "pending"}` |
| `GET /api/notes/{hash}` | — | `200` not kartı (`/api/search` sonucundaki öğeyle aynı biçim) |
| `GET /api/notes/{hash}/proof` | — | `200` proof dosyası (bölüm 6) ya da `404` hata kodu `proof_pending` |
| `GET /api/search?course=&topic=&q=` | — | `200 {"results": [not kartı, ...]}` |

Önizleme yanıtı:

```json
{
  "previewToken": "...",
  "noteHash": "<64 hex>",
  "alreadyRegistered": null,
  "suggestion": {"course": "Course_SEN0401", "topics": ["Topic_TransactionFees"], "summary": "..."},
  "copyWarnings": [
    {"earlierNoteHash": "...", "earlierAuthor": "...", "earlierRegisteredAt": "...",
     "earlierProofUrl": "...", "score": 0.93, "method": "char-cosine"}
  ]
}
```

Hash zaten kayıtlıysa `alreadyRegistered` şu olur: `{"registeredAt": "...", "author": "...", "proofUrl": "..."}`
ve `suggestion` ile `copyWarnings` boş gelir.

Onay gövdesi:

```json
{"previewToken": "...", "title": "...", "course": "Course_SEN0401",
 "topics": ["Topic_TransactionFees"], "summary": "...", "confirmed": true}
```

Not kartı:

```json
{"noteHash": "...", "title": "...", "course": "Course_SEN0401", "topics": ["..."], "summary": "...",
 "author": "takma-ad", "registeredAt": "...", "proofStatus": "pending|proven", "possibleCopyOf": null}
```

Hata biçimi her uç noktada aynıdır:

```json
{"error": {"code": "shape_violation", "message": "...",
           "violations": [{"shape": "NoteShape", "path": "np:topic", "message": "..."}]}}
```

| HTTP | `code` | Ne zaman |
| --- | --- | --- |
| 400 | `unsupported_type` | Dosya türü PDF, JPEG, PNG ya da metin değil |
| 400 | `too_large` | Dosya 10 MB'tan büyük (K-006) |
| 400 | `not_confirmed` | `confirmed` alanı `true` değil |
| 401 | `unauthorized` | Token yok ya da geçersiz |
| 404 | `not_found` | Not yok |
| 404 | `proof_pending` | Not var, proof henüz üretilmedi |
| 410 | `preview_expired` | `previewToken` süresi doldu ya da bilinmiyor |
| 422 | `shape_violation` | SHACL ihlali; `violations` dolu gelir |

Arayüz kullanıcıya `code` değerine göre kendi Türkçe metnini gösterir.

## 8. Ortam değişkenleri

| Değişken | Kullanan | Açıklama |
| --- | --- | --- |
| `NOTEPROOF_DATA_DIR` | hepsi | Çalışma verisi klasörü; varsayılan `./data` |
| `NOTEPROOF_RPC_URL`, `NOTEPROOF_RPC_USER`, `NOTEPROOF_RPC_PASSWORD`, `NOTEPROOF_RPC_WALLET` | `anchor/` | Bitcoin Core bağlantısı |
| `NOTEPROOF_LLM_PROVIDER`, `NOTEPROOF_LLM_MODEL`, `NOTEPROOF_LLM_API_KEY` | `tagger/` | Dil modeli bağlantısı |

Değerler yerelde `.env` dosyasında durur. `.env`, cüzdan dosyaları ve API anahtarları repoya girmez.
Yeni bir değişken eklemek sözleşme değişikliğidir (bölüm 9).

## 9. Sözleşme değişikliği prosedürü

Bu dosyadaki bir ad, imza, alan, IRI, uç nokta ya da değişkeni değiştirmek gerekiyorsa:

1. Dur. Kendi branch'inde sözleşmenin farklı bir hâlini uygulama.
2. Üyeye ne değişmesi gerektiğini ve hangi modülleri etkilediğini söyle.
3. Üye, etkilenen modüllerin sahiplerine ve Arda'ya (mimar) bildirir.
4. Arda (mimar) kabul ederse: Erdener bu dosyayı ve `07_KARARLAR.md`'yi bir PR ile günceller ve sürüm numarasını
   artırır. Merge edilince Erdener ekip grubuna duyurur (`AGENTS.md` bölüm 7).
5. Herkes `main`'i çeker ve kodunu yeni sözleşmeye göre günceller.

Karar çıkana kadar eski sözleşmeyle çalış ve ilgili yere `NP-TODO` bırak (`03_KOD_KURALLARI.md` bölüm 3).
