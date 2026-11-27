# 06 — Ortak kurulum (sıfırdan)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **her üyenin bilgisayarını projede çalışacak hâle getirmek**. Burada herkes için
ortak olan adımlar vardır; modüle özel ek kurulumlar üyenin kendi dosyasındadır.

Üyeye yol gösterirken:

- Önce işletim sistemini sor (Windows ya da macOS) ve yalnızca o sistemin adımlarını ver.
- Her adımda tek bir işlem yaptır, sonra adımın "Kontrol" komutunu çalıştırt ve çıktıyı iste.
  Çıktı beklenen gibi değilse sonraki adıma geçme.
- Zaten kurulu olanı yeniden kurdurma: önce kontrol komutunu çalıştırt.
- Komutlar Windows'ta **PowerShell**'de, macOS'te **Terminal**'de çalışır.

## 1. Git ve GitHub Desktop

1. GitHub hesabı: üyenin hesabı repoya (`aozcan4482/noteproof`) eklenmiş olmalı. Eklenmemişse Arda'dan davet istenir.
2. GitHub Desktop'ı `https://desktop.github.com` adresinden kur ve GitHub hesabıyla giriş yap.
3. Git'i kur: Windows'ta `https://git-scm.com/download/win` (varsayılan seçeneklerle);
   macOS'te Terminal'e `git --version` yazılır, kurulu değilse sistem kurmayı önerir.
4. Kontrol: `git --version` bir sürüm numarası yazar.
5. Kimlik ayarı (GitHub Desktop → File → Options → Git): ad olarak üyenin adı soyadı, e-posta olarak
   GitHub hesabındaki e-posta. Commit'lerin üyeye sayılması buna bağlıdır.
   Kontrol: `git config --global user.name` ve `git config --global user.email`.

## 2. Repoyu klonlama

1. GitHub Desktop → File → Clone repository → `aozcan4482/noteproof`.
2. Yerel yol: Windows'ta `Belgeler\GitHub\noteproof`, macOS'te `~/Documents/GitHub/noteproof`.
   Yol içinde OneDrive, iCloud gibi eşitlenen bir klasör olmasın.
3. Kontrol: GitHub Desktop'ta Current repository `noteproof`, Current branch `main` görünür.
4. Terminali repo klasöründe aç: GitHub Desktop → Repository → Open in Command Prompt / Terminal.
   Bundan sonraki bütün komutlar bu klasörde (repo kökünde) çalışır.

## 3. Python

1. Python 3.12'yi `https://www.python.org/downloads/` adresinden kur.
   Windows'ta kurulumun ilk ekranında **"Add python.exe to PATH"** kutusu işaretlenir.
2. Kontrol: Windows'ta `py -3.12 --version`, macOS'te `python3.12 --version` → `Python 3.12.x`.
3. Sanal ortam (repo kökünde, bir kez):
   - Windows: `py -3.12 -m venv .venv`
   - macOS: `python3.12 -m venv .venv`
4. Sanal ortamı etkinleştir (**her yeni terminalde**):
   - Windows: `.venv\Scripts\Activate.ps1`
     ("running scripts is disabled" hatası gelirse bir kez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`)
   - macOS: `source .venv/bin/activate`
   - Kontrol: satırın başında `(.venv)` görünür.
5. Bağımlılıklar: `python -m pip install --upgrade pip` ve ardından
   `python -m pip install -e ".[dev,all]"`.
   Bu komut "Multiple top-level packages discovered" hatası veriyorsa ya da `all` grubu yoksa Faz 0
   henüz `main`'e girmemiştir (Burak'ın BRK-1 görevi). O zamana kadar: `python -m pip install "pytest>=8"`.
6. Kontrol: `python -m pytest -q` → son satır `passed` ile biter, `failed` yoktur.
   (Faz 0 sonrası beklenen: en az 60 passed; bitcoind kurulu değilse 1 skipped.)

`.venv/` klasörü repoya girmez; `.gitignore`'dadır.

## 4. Editör

Visual Studio Code önerilir (`https://code.visualstudio.com`), Python eklentisiyle. Açılış:
GitHub Desktop → Repository → Open in Visual Studio Code. Sağ altta yorumlayıcı olarak `.venv` seçilir.
Başka bir editör de olur; kural yoktur.

## 5. Yerel ayarlar

1. Repo kökünde `.env` adında bir dosya oluştur (repoya girmez). İçeriği üyenin modülüne göre
   üye dosyasında yazar; herkes için ortak tek satır:

   ```
   NOTEPROOF_DATA_DIR=./data
   ```

2. `data/` klasörü ilk çalıştırmada kendiliğinden oluşur; repoya girmez.

## 6. Uygulamayı yerelde çalıştırma (Faz 2'den sonra)

```
python -m uvicorn register.app:app --reload --port 8000
```

Tarayıcıda `http://localhost:8000` arama sayfasını, `http://localhost:8000/api/health` ise `{"status": "ok"}` yanıtını gösterir.

## 7. Kurulum bitti mi

Şu dördü doğruysa kurulum tamamdır ve `05_PIPELINE.md` bölüm 1'e geçilir:

1. GitHub Desktop'ta `noteproof` açık ve `main` güncel.
2. `git config user.name` üyenin adını yazıyor.
3. `(.venv)` etkin ve `python -m pytest -q` yeşil.
4. Üyenin dosyasındaki ek kurulum adımları tamam.
