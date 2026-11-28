# Değerlendirme seti (evalset/)

Proposal'daki deliverable: **"Evaluation set of 60 notes with known topics and 20 planted copies"**.
İki şeyi ölçer:

| Ölçü | Hedef | Nasıl |
| --- | --- | --- |
| Kopya uyarısının yakaladığı planted copy (O5, S6) | ≥ %90 (20'de 18) | `python -m evalset.run_copywarn` |
| AI tagger'ın değiştirilmeden kabul edilen konu önerileri (O3, S3) | ≥ %80 | tagger hazır olunca `manifest.csv`'deki `topics` ile karşılaştırılacak (Aleyna) |

## Durum

- [x] Klasör yapısı, okuma/yazma (`data.py`), kopya üretici (`plant.py`), kopya değerlendirmesi (`run_copywarn.py`)
- [x] Hattın kendisi `tests/copywarn/` altında **sentetik** metinlerle test ediliyor
- [ ] **60 gerçek not** — ekipten toplanıyor (aşağıdaki kurallar). 28 Kasım: 9/60 (`yazar-01`, SEN0401)
- [x] Manifest denetimi: `tests/copywarn/test_manifest.py` (konu kimlikleri sözlükte mi, yazar takma ad mı, kişisel veri var mı)
- [ ] `python -m evalset.plant` ile 20 planted copy üretilip commit'lenecek
- [ ] Tagger değerlendirmesi (Aleyna ile)

## Not ekleme kuralları

1. **Yalnızca ekibin KENDİ notları.** Hoca slaytı, kitap sayfası, başkasının notu yok (proposal: exclusions).
2. **Kişisel veri yok.** Notta isim, öğrenci numarası, telefon varsa silin. Yazar sütununa gerçek isim değil takma ad yazılır: `yazar-01`, `yazar-02` … (KVKK). Takma ad ↔ kişi eşleşmesi repoya girmez.
3. Not düz metin olarak `notes/<id>.txt` dosyasına konur (UTF-8). Fotoğraf/PDF ise önce metni çıkarın.
4. Her not `manifest.csv`'ye bir satır olarak eklenir.

### `manifest.csv`

```csv
id,course,topics,author,registered_at
sen0401-001,SEN0401,Topic_TransactionFees;Topic_FeeRate,yazar-01,2026-10-20T18:30:00
```

- `id`: dosya adıyla aynı, küçük harf, boşluksuz
- `course`: ders kodu
- `topics`: SKOS konu kimlikleri, `;` ile ayrılmış — **Eylem'in sözlüğündeki kimliklerle aynı olmalı**
- `author`: takma ad
- `registered_at`: ISO 8601; notun yazıldığı/paylaşıldığı gün (kopya sırası buna göre belirlenir)

## Çalıştırma (repo kökünden)

```bash
python -m evalset.plant          # planted/ klasörünü yeniden üretir (seed sabit: aynı notlar -> aynı kopyalar)
python -m evalset.run_copywarn   # raporu yazar; hedefin altındaysa çıkış kodu 1 (CI kırmızı)
```

Not: 60 notun bir kısmı aynı ders içeriğini anlattığı için özgün notlar arasında da benzerlik çıkabilir.
`run_copywarn` bunları **yanlış alarm** olarak raporlar; eşik (`copywarn/checker.py`, `DEFAULT_THRESHOLD`)
gerçek veriyle bu iki sayıya bakılarak ayarlanmalı.
