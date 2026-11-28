# NoteProof

**Öğrencilerin kendi ders notları için Bitcoin zaman damgalı, yapay zekâ ile etiketlenmiş bir arşiv.**

SEN0401 — Special Topics in Software Engineering (Blockchain), 2026-2027 Güz dönemi ekip projesi.
Müşteri: İstanbul Kültür Üniversitesi Yazılım Mühendisliği 3. ve 4. sınıf öğrencileri.

## Proje ne yapar

Öğrenci notunu (PDF, fotoğraf ya da metin) yükler. Sistem:

1. Notun SHA-256 hash'ini hesaplar ve kimin ne zaman kaydettiğini PROV-O ile tutar.
2. Bir yapay zekâ, notun dersini, konularını ve iki cümlelik özetini ortak bir SKOS sözlüğünden **önerir**;
   yazar onaylamadan hiçbir etiket kaydedilmez.
3. Not önceki notlara çok benziyorsa **"Olası kopya"** uyarısı gösterir ve önceki notun kanıtına bağlar.
4. Günde bir kez, o günün bütün hash'lerinden bir Merkle ağacı kurar ve yalnızca 32 byte'lık kökü
   Bitcoin **signet** ağına OP_RETURN çıktısı olarak yazar. Her not kendi Merkle path'ini (proof) alır.
5. Okuyucular notları ders ve konuya göre arar; arama alt konuları da kapsar.
6. Herkes, hesap açmadan ve arşivin sunucusu kapalıyken bile, bir not dosyasını proof sayfasında
   Bitcoin işlemine karşı kontrol edebilir.

**Neyi kanıtlamaz:** zaman damgası, dosyanın o tarihte var olduğunu ve hangi hesabın kaydettiğini gösterir;
notu ilk kimin yazdığını göstermez. Sistem intihal kararı vermez.

Zincire not içeriği, isim ya da öğrenci numarası gitmez. Hesaplar takma adlıdır; gerçek kimlik istenmez.

## Modüller ve sahipleri

| Klasör | İçerik | Sahip | İkinci (reviewer) | Durum |
| --- | --- | --- | --- | --- |
| `anchor/` | Bitcoin timestamp servisi: Merkle ağacı, OP_RETURN, kuyruk, günlük iş, proof | Burak Sami Şirin | Arda Özcan | `main`'de, testli |
| `copywarn/` | Kopya uyarısı (karakter 5-gram ve kelime 3-shingle benzerliği) | Emine Esra Çiçek | Aleyna Cebeci | `main`'de, testli |
| `evalset/` | Değerlendirme seti (60 not, 20 planted copy) ve ölçüm betikleri | Emine Esra Çiçek | Aleyna Cebeci | `main`'de; gerçek notlar toplanıyor |
| `core/` | Ortak çekirdek: namespace, IRI üreticiler, hash, ayarlar, grafik deposu | Arda Özcan | Burak Sami Şirin | Henüz yok |
| `register/` | Kayıt servisi ve HTTP API (FastAPI) | Arda Özcan | Burak Sami Şirin | Henüz yok |
| `ontology/`, `shapes/` | Not ontolojisi, SKOS ders ve konu sözlüğü, SHACL shape'leri | Eylem Sarıbal | Aleyna Cebeci | Henüz yok |
| `tagger/` | Metin çıkarma, dil modeli istemcisi, etiket önerisi | Aleyna Cebeci | Eylem Sarıbal | Henüz yok |
| `search/` | SPARQL arama servisi ve `/api/search` | Erdener Çimen | Aysu Akdüzen | Henüz yok |
| `web/` | Statik sayfalar: arama, yükleme, proof | Erdener Çimen | Aysu Akdüzen | Henüz yok |
| `docs/acceptance/`, `docs/pilot/` | Kabul senaryoları, pilot planı ve sonuçları | Aysu Akdüzen | Emine Esra Çiçek | Henüz yok |
| `proposal/` | Proposal ve SHA-256 zincirli work log | Arda Özcan | Erdener Çimen | `main`'de |

Testler `tests/<paket>/` altında durur ve paketin sahibine aittir. Ortak yapılandırma
(`pyproject.toml`, `.gitignore`, `.github/`) Burak'ındır. Bir klasörün sahibi olmayan üye o klasörde
dosya oluşturmaz ve değiştirmez; değişiklik isteği sahibine iletilir.

Belgeler: `docs/analysis/` (üyelerin analiz ve taslakları), `docs/ops/` (signet node'u ve işletim),
`docs/reports/` (test ve değerlendirme raporları), `docs/worklog/<üye>.md` (her üyenin devir notu ve
work log taslakları).

## Kurulum (kısa)

Gerekenler: Git, GitHub Desktop, Python 3.12.

```
# 1. Repoyu klonla: GitHub Desktop → File → Clone repository → aozcan4482/noteproof
#    (Yol içinde OneDrive ya da iCloud gibi eşitlenen bir klasör olmasın.)

# 2. Repo kökünde sanal ortam (bir kez)
py -3.12 -m venv .venv            # Windows
python3.12 -m venv .venv          # macOS

# 3. Sanal ortamı etkinleştir (her yeni terminalde)
.venv\Scripts\Activate.ps1        # Windows (PowerShell)
source .venv/bin/activate         # macOS

# 4. Bağımlılıklar
python -m pip install --upgrade pip
python -m pip install "pytest>=8"
```

`pyproject.toml`'a modül bağımlılık grupları eklendiğinde 4. adım şu olacak:
`python -m pip install -e ".[dev,all]"`. Şu an yalnızca `dev` grubu var ve paket listesi henüz yazılmadığı
için `pip install -e .` çalışmaz.

Repo kökünde bir `.env` dosyası oluştur (repoya girmez):

```
NOTEPROOF_DATA_DIR=./data
```

Bitcoin Core (regtest testleri ve signet için) ve dil modeli ayarları yalnızca o modüllerde çalışan
üyeler için gereklidir; ayrıntı `docs/ops/signet.md` ve kural setindedir.

## Testleri çalıştırma

Repo kökünde, sanal ortam etkinken:

```
python -m pytest -q
```

Bugün beklenen çıktı: `60 passed, 1 skipped`. Atlanan test gerçek bir `bitcoind` ister
(`@pytest.mark.regtest`); bilgisayarda Bitcoin Core yoksa otomatik atlanır.

Tarayıcı kodunun testleri (`tests/web/`, Node.js 20 ya da üstü), repo kökünde:

```
node --test
```

Klasör adı verilmez; Node 22 ve üstü `node --test tests/web/` biçimini kabul etmez.

## Uygulamayı çalıştırma

Kayıt servisi (`register/app.py`) henüz `main`'de değil. Entegrasyondan (Faz 2) sonra:

```
python -m uvicorn register.app:app --reload --port 8000
```

Tarayıcıda `http://localhost:8000` arama sayfasını, `http://localhost:8000/api/health` ise
`{"status": "ok"}` yanıtını gösterecek.

Günlük timestamp işi (`anchor/`, şimdiden çalışır; Bitcoin Core bağlantısı gerekir):

```
python -m anchor.daily --db data/noteproof.sqlite --out data/proofs
```

## Katkı kuralları (özet)

- `main`'e doğrudan commit atılmaz. Her görev kendi branch'inde yapılır ve PR ile `main`'e girer:
  **bir görev → bir branch → bir PR → `main` → branch silinir.**
- Branch adları: `feature/S<no>-<kısa-ad>`, `infra/<kısa-ad>`, `docs/<kısa-ad>`, `fix/<kısa-ad>`, `log/<üye>-<no>`.
- Commit mesajları İngilizce; açıklamada `Task: <görev> (part|done)` satırı bulunur.
- Merge yöntemi: merge commit (squash yok). Merge'i Burak yapar; onaydan 24 saat sonra PR sahibi de
  merge edebilir. Work log PR'larını sahibi merge eder.
- `proposal/proposal.json` elle düzenlenmez; work log kayıtları yalnızca Proposal Workbench ile eklenir.
- Repoya girmeyenler: `data/`, `.env`, `.venv/`, cüzdan dosyaları, API anahtarları, gerçek isim ve öğrenci
  numarası, anket ham verisi.

## Ekip kuralları

Ekibin ayrıntılı çalışma kuralları (proje kapsamı, mimari sözleşmeler, kod kuralları, git akışı, takvim,
kararlar ve her üyenin görev listesi) repodadır: giriş dosyası kökteki `AGENTS.md`, diğerleri `docs/rules/`
altında. Geçerli kurallar `main`'deki hâlidir. Kural setinin sorumlusu Erdener Çimen'dir (documentation lead);
değişiklikler `docs/rules-...` PR'larıyla yapılır.
