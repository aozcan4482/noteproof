# Anket özeti ve baseline kontrolü

Görev: AYS-R1, AYS-R2 · Sahip: aysu · İnceleyen: emine · Kural seti sürüm 2.3

Bu belge, 16 Ekim 2026'da 3. ve 4. sınıf Yazılım Mühendisliği öğrencilerine yapılan anketin sayılarını
Google Forms dışa aktarımından yeniden sayar. Sayılar proposal'ın problem statement'ındaki sayılarla
karşılaştırılır ve objective'lerin başlangıç değerleri (baseline) ankete göre kontrol edilir.

Bu belgede yalnızca toplu sayılar vardır. Ham yanıtlar, zaman damgaları ve dışa aktarım dosyası repoya
girmez (`aysu.md` bölüm 2, kişisel veri kuralı). Formda isim ya da öğrenci numarası sorulmamıştır.

## 1. Kaynak

| | |
| --- | --- |
| Form | Google Forms, beş soru (aşağıda) |
| Dışa aktarım | Formun "Yanıtları indir (.csv)" çıktısı, 27 Kasım 2026'da alındı |
| Yanıt sayısı | **24** (hepsi 16 Ekim 2026 tarihli) |
| Sayım yöntemi | CSV bir betikle sayıldı. Çok seçimli soruda (soru 2) her seçenek ayrı sayıldı |

Sorular:

1. Kendi ders notlarını başkalarıyla paylaşıyor musun?
2. Paylaşıyorsan nerede paylaşıyorsun? (çok seçimli)
3. Senin yazdığın bir not adın verilmeden, başkasının adıyla ya da izinsiz paylaşıldı veya satıldı mı?
4. Sınavdan önce bir konunun notunu bulmak ortalama kaç dakikanı alıyor?
5. Notların derse ve konuya göre arandığı, kimin notu olduğunun kanıtlandığı bir arşivi kullanır mıydın? (1–5)

## 2. Temel bulgu: proposal 20 yanıtla, form 24 yanıtla

Proposal "20 öğrenci" diyor, dışa aktarımda ise 24 yanıt var. Gönderilme sırasına göre **ilk 20 yanıt**
sayıldığında proposal'daki bütün sayılar birebir çıkıyor. Kalan 4 yanıt aynı gün, ilk 20'den sonra geldi.
Proposal büyük olasılıkla anket o gün kapanmadan yapılan sayıma dayanıyor.

Hangi sayının proposal'da kalacağına proposal'ın sahibi Arda karar verir. Bu belge iki sayımı da gösterir
(bölüm 5).

## 3. Karşılaştırma tablosu

| Problem statement'taki sayı | Proposal'daki | İlk 20 yanıttan sayılan | 24 yanıtın hepsinden sayılan | Durum |
| --- | --- | --- | --- | --- |
| Yanıt sayısı | 20 | 20 | 24 | Uyuşmuyor (4 geç yanıt) |
| Notlarını paylaşan (soru 1: "Evet, …") | 17 | 17 | 21 | İlk 20 ile uyuşuyor |
| Bunlardan düzenli paylaşan | 3 | 3 | 4 | İlk 20 ile uyuşuyor |
| Paylaşanlardan WhatsApp gruplarında paylaşan | 10 | 10 | 13 | İlk 20 ile uyuşuyor |
| Paylaşanlardan sayfaların fotoğrafını gönderen | 9 | 9 | 13 | İlk 20 ile uyuşuyor |
| Notu izinsiz ya da isimsiz paylaşılmış ("Evet") | 5 | 5 | 6 | İlk 20 ile uyuşuyor |
| Emin olmayan ("Emin değilim") | 5 | 5 | 8 | İlk 20 ile uyuşuyor |
| Bir konudaki notu bulmanın medyan süresi | 10–20 dk | 10–20 dk | 10–20 dk | Uyuşuyor |
| 10 dakika ya da daha uzun süren | 13 | 13 | 17 | İlk 20 ile uyuşuyor |
| Arşivi kullanırdı (soru 5'te 4 ya da 5) | 14 | 14 | 17 | İlk 20 ile uyuşuyor |

## 4. Soru soru dağılım (24 yanıtın hepsi)

**Soru 1 — Paylaşım**

| Yanıt | Sayı |
| --- | --- |
| Evet, ara sıra | 17 |
| Evet, düzenli olarak | 4 |
| Hayır | 3 |

**Soru 2 — Nerede (çok seçimli; bir kişi birden çok seçenek seçebilir)**

| Seçenek | Sayı |
| --- | --- |
| WhatsApp grupları | 13 |
| Notun fotoğrafını çekip gönderiyorum | 13 |
| Google Drive / OneDrive | 2 |
| Instagram | 2 |
| Telegram | 1 |
| Paylaşmıyorum | 4 |

**Soru 3 — İzinsiz ya da isimsiz paylaşım**

| Yanıt | Sayı |
| --- | --- |
| Hayır | 10 |
| Emin değilim | 8 |
| Evet | 6 |

**Soru 4 — Bir konunun notunu bulma süresi**

| Yanıt | Sayı |
| --- | --- |
| 5 dakikadan az | 4 |
| 5–10 dakika | 3 |
| 10–20 dakika | 10 |
| 20–30 dakika | 4 |
| 1 saatten fazla | 3 |

Medyan: 24 yanıt sıraya dizildiğinde 12. ve 13. yanıtların ikisi de "10–20 dakika". İlk 20 yanıtta da
10. ve 11. yanıtlar "10–20 dakika".

**Soru 5 — Arşivi kullanır mıydın (1 = hiç, 5 = kesinlikle)**

| Puan | Sayı |
| --- | --- |
| 5 | 13 |
| 4 | 4 |
| 3 | 6 |
| 1 | 1 |

## 5. Notlar ve açık noktalar

- **Geç gelen 4 yanıt.** Proposal'daki sayılar ilk 20 yanıta dayanıyor. Sayılar ya 20 yanıtla kalır ve
  proposal'a "16 Ekim'deki ilk 20 yanıt" diye yazılır, ya da 24 yanıtla güncellenir. Karar Arda'nındır.
  İki durumda da yön değişmiyor: çoğunluk not paylaşıyor, WhatsApp ve fotoğraf en sık kanal, medyan
  10–20 dakika, çoğunluk arşivi kullanırdı.
- **Tutarsız bir yanıt.** Bir yanıtta soru 1'e "Evet, ara sıra", soru 2'ye "Paylaşmıyorum" denmiş. Bu
  yanıt "paylaşan" sayısına girdi (soru 1'e göre), soru 2'de hiçbir kanala sayılmadı. Bu yanıt ilk 20'nin
  içinde ve proposal'daki 17'ye dahil.
- **"Kullanırdı" tanımı.** Proposal'daki 14, soru 5'te 4 ya da 5 verenlerin sayısıdır. Yalnızca 5
  sayılırsa ilk 20'de 10, 24'te 13 olur. Bu tanım proposal'da yazmıyor. Final raporunda belirtilmesi önerilir.
- **"Paylaşan" kanal sayıları.** WhatsApp (10) ve fotoğraf (9) sayıları yalnızca soru 1'e "Evet" diyenler
  içinden sayıldı. Proposal'daki "10 of the 17" ifadesi de bunu söylüyor.

  ## 6. Baseline kontrolü (AYS-R2)

Kaynak: `proposal/proposal.json` → `objectives`.

| Objective | Proposal baseline | Kaynak | Sonuç |
| --- | --- | --- | --- |
| O1 — 24 saat içinde geçerli proof'u olan pilot notlarının oranı | %0 | Sistem henüz yok; hiçbir notun signet proof'u yok | Doğru |
| O2 — Onaylı etiketleri shape'lerden geçen pilot notlarının oranı | %0 | Sistem henüz yok; etiketli not yok | Doğru |
| O3 — 60 değerlendirme notunda düzeltmeden onaylanan AI konu önerilerinin oranı | %0 | Tagger henüz ölçülmedi; öneri yok | Doğru |
| O4 — Bir konudaki notu bulmanın medyan süresi | 15 dk | Anket, soru 4: medyan yanıt "10–20 dakika" (hem ilk 20 hem 24 yanıtta); aralığın ortası 15 dk | Doğru. Yalnız proposal'daki tanımda "20 students" yazıyor; 24 yanıtla güncellenirse bu ifade de değişir (bölüm 5) |
| O5 — 20 planted copy'den kopya uyarısının yakaladığı oran | %0 | Kopya uyarısı gerçek değerlendirme setinde henüz çalışmadı | Doğru |
| O6 — 32 byte'lık kök dışında veri taşıyan OP_RETURN + onaysız kayıtlı etiket sayısı | 0 | Sistem henüz yok; sızıntı yok. Hedef de 0 (korunacak değer) | Doğru |

O4 için not: anketteki süre öğrencinin kendi tahminidir, ölçüm değildir. Pilottaki ölçüm ise kronometreyle
yapılacak (AYS-3, AYS-6). İki sayının yöntemi farklı. Bu fark final raporunda yazılmalı.
