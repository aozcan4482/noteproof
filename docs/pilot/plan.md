# Pilot planı

Görev: AYS-3 · Sahip: aysu · İnceleyen: arda, emine · Kural seti sürüm 2.3

**Durum: taslak.** "Öneri" diye işaretli maddeler Arda ve Emine'nin incelemesinden sonra kesinleşir.
Ölçüm protokolü (bölüm 6) pilot başlamadan önce kesinleşir ve pilot sırasında değişmez.

## 1. Amaç

Sistemin gerçek kullanıcılar için çalıştığını göstermek (P11 Validation):

- **O4:** Bir konudaki notu bulmanın medyan süresi. Başlangıç 15 dakika, hedef 2 dakika ya da daha az.
- Gönüllülerin üç ana işi (not yükle, not ara, kanıtı kontrol et) yardımsız yapıp yapamadığı.
- Geri bildirim: neyin anlaşılmadığı, neyin eksik olduğu. Her bulgu bir GitHub issue'su olur.
- Pilot notları O1 (24 saat içinde kanıt) ve O2 (onaylı etiketler shape'lerden geçiyor) ölçümlerinde de
  kullanılır (Burak, Eylem).

## 2. Tarihler

| Tarih | Ne |
| --- | --- |
| 1 Aralık | Deneme oturumu, `v0.3.0` ile 2–3 öğrenci (AYS-5). Plan ve form burada denenir |
| 2–4 Aralık | Gönüllü çağrısı ve kayıt; dersler listesi Eylem'de (EYL-8, 2 Aralık) |
| 4 Aralık | `v0.9.0` (signet'te günlük timestamp çalışıyor) |
| 5–6 Aralık | **Yükleme:** gönüllüler kendi notlarını yükler |
| 7–9 Aralık | **Arama:** quiz haftasında not arama; O4 ölçümleri; kanıt kontrolü |
| 9 Aralık | Geri bildirim formu kapanır; `docs/pilot/results.md` |
| 10 Aralık | Kabul ve doğrulama yazısı (AYS-7) |

Ön koşul: signet'te günlük timestamp (Burak, BRK-7). Hazır değilse pilot regtest demosuyla yapılmaz;
tarih Arda ile konuşulur.

## 3. Gönüllüler

| | |
| --- | --- |
| Kimler | Yazılım Mühendisliği 3. ve 4. sınıf öğrencileri (müşteri). Ekip üyeleri gönüllü sayılmaz |
| Hedef sayı | **Öneri: 10 gönüllü.** Her biri 2 ölçülü arama yaparsa O4 için gereken 20 süre çıkar |
| Nasıl bulunur | 3. ve 4. sınıf WhatsApp gruplarına duyuru; ankete katılanlara öncelik. Katılım gönüllüdür, karşılığında not ya da ödül yoktur |
| Kimlik | Her gönüllü kendi takma adını seçer. Belgelerde `gönüllü-01` … diye anılır. Takma adla `gönüllü-NN` eşleşmesi yalnızca Aysu'nun bilgisayarında tutulur, repoya girmez |

## 4. Dersler (Eylem'e iletilecek liste)

Şu an sözlükte yalnızca SEN0401 (Blokzincir) var. Pilotta gönüllülerin kendi notlarını yükleyebilmesi
için notlarının olduğu derslerin sözlüğe eklenmesi gerekir (EYL-8).

**Öneri:** Gönüllü kayıt formunda "Hangi derslerin notunu yükleyebilirsin?" sorusu sorulur. En çok
işaretlenen 2–3 ders (SEN0401 dahil) 2 Aralık'tan önce Eylem'e iletilir.

| Ders kodu | Ders adı | Kaç gönüllünün notu var |
| --- | --- | --- |
| SEN0401 | Özel Konular: Blokzincir | |
| | | |

## 5. Görevler

Her gönüllü üç iş yapar:

| # | Görev | Ne zaman | Başarı |
| --- | --- | --- | --- |
| G1 | **Not yükle:** kendi notlarından en az 2'sini yükle, AI'ın önerdiği ders ve konuları kontrol edip onayla | 5–6 Aralık | Not kaydedildi; etiketler onaylandı |
| G2 | **Not ara:** verilen bir konudaki notu bul ve aç (ölçülür, bölüm 6) | 7–9 Aralık | Doğru not açıldı |
| G3 | **Kanıtı kontrol et:** kendi notunun proof sayfasını aç, dosyanı seç, sonucu gör | 7–9 Aralık (kanıt hazır olduktan sonra) | "Kanıtlandı" görüldü |

## 6. Ölçüm protokolü (O4)

Bu protokol ölçmeden önce kesinleşir ve ölçüm sırasında değişmez.

| | |
| --- | --- |
| Kim ölçer | Aysu; Emine yardım eder. Her ölçümde bir gözlemci, kronometre (telefon) ile |
| Cihaz | Gönüllünün kendi telefonu |
| Konu nasıl verilir | Gözlemci, arşivde en az bir notu bulunan bir konuyu ders adıyla birlikte söyler (ör. "SEN 401, İşlem ücretleri"). Konular önceden listelenir; gönüllü kendi yüklediği notun konusunu almaz |
| Süre ne zaman başlar | Gözlemci konuyu söylemeyi bitirdiği anda |
| Süre ne zaman biter | Gönüllü o konudaki doğru bir notun ayrıntı ekranını açtığı anda |
| Doğru not | O konuyla (ya da alt konularından biriyle) etiketli herhangi bir not |
| Yardım | Gözlemci yardım etmez, ipucu vermez. Gönüllü soru sorarsa "sistemde nasıl yapardın?" der |
| Başarısız arama | **Öneri:** 10 dakikada bulunamazsa durdurulur ve süre 10 dakika olarak, "bulunamadı" notuyla yazılır. Medyana dahil edilir (dışarıda bırakılmaz) |
| Kaç ölçüm | 20 arama. Bir gönüllüye en çok 2 arama |
| Ne kaydedilir | gönüllü kodu, tarih, konu, süre (saniye), bulundu / bulunamadı, gözlemci notu. İsim yok |
| Sonuç | 20 sürenin medyanı. Hedef ≤ 2 dakika. Sonuç olduğu gibi yazılır; hedef tutmazsa olası nedeni yazılır |

Not: Anketteki 15 dakika öğrencilerin tahminiydi; pilottaki süre kronometreyle ölçülür. Bu fark sonuç
yazısında belirtilir.

## 7. Bilgilendirme ve açık rıza metni

Gönüllüye katılmadan önce okunur ya da gönderilir. Kayıt formunun ilk sorusu olarak onaylanır.

> **NoteProof pilotuna katılım hakkında**
>
> NoteProof, öğrencilerin kendi ders notlarını kaydettiği ve konuya göre aradığı bir arşivdir. Bu pilot,
> Yazılım Mühendisliği proje dersindeki ekibimizin sistemi gerçek kullanıcılarla denemesi içindir.
>
> **Ne topluyoruz:** yüklediğin notlar, seçtiğin takma ad, not arama süren ölçümleri ve geri bildirim
> formuna verdiğin yanıtlar.
>
> **Ne toplamıyoruz:** adın, öğrenci numaran ya da e-posta adresin. Sistem bunları sormaz ve saklamaz.
>
> **Notların zincire gitmez.** Her gece o günün notlarından hesaplanan 32 byte'lık tek bir değer Bitcoin
> test ağına (signet) yazılır. Bu değerden notun içeriğine ulaşılamaz.
>
> **Kanıtın sınırı:** Kanıt, notunun o tarihte var olduğunu ve onu senin kaydettiğini gösterir. Notu ilk
> kimin yazdığını göstermez.
>
> **Katılım gönüllüdür.** İstediğin zaman bırakabilirsin. Notunun arşivden kaldırılmasını istersen
> Aysu'ya yazman yeterli; not, dosyası ve kayıtlarıyla birlikte silinir.
>
> **Sonuçlar** yalnızca toplu sayılar ve isimsiz alıntılar olarak proje raporunda kullanılır.
>
> ☐ Okudum, pilota gönüllü olarak katılmayı kabul ediyorum.

## 8. Geri bildirim formu soruları

Google Forms, pilotun sonunda. İsim ve numara sorulmaz. Gönüllü kodunu (`gönüllü-NN`) gözlemci verir.

1. Gönüllü kodun: (kısa yanıt)
2. Not yüklemek ne kadar kolaydı? (1 = çok zor … 5 = çok kolay)
3. AI'ın önerdiği ders ve konular notuna uyuyor muydu? (Hepsi uydu / Bazıları uydu / Hiçbiri uymadı)
4. Önerileri düzeltmen gerekti mi? Gerektiyse neyi? (uzun yanıt)
5. Not aramak ne kadar kolaydı? (1–5)
6. Aradığın notu bulmak, alıştığın yoldan (WhatsApp, fotoğraflar) daha mı hızlıydı? (Daha hızlı / Aynı / Daha yavaş)
7. Kanıt sayfasında ne gördüğünü anladın mı? (Evet / Kısmen / Hayır)
8. "Olası kopya" uyarısı gördüysen ne anladın? (uzun yanıt; görmediysen boş bırak)
9. Takıldığın ya da anlamadığın bir yer oldu mu? (uzun yanıt)
10. Bu arşivi derslerin için kullanır mıydın? (1 = hiç … 5 = kesinlikle)
11. Eklemek istediğin bir şey var mı? (uzun yanıt)

10. soru anketteki 5. soruyla aynı ölçekte. Böylece pilot öncesi ve sonrası karşılaştırılabilir.

## 9. Veri ve gizlilik

- Ham veri (kronometre kayıtları, form yanıtları, takma ad eşleşmeleri) repoya girmez. Aysu'nun
  bilgisayarında ya da ekibin kapalı klasöründe kalır.
- Repoya yalnızca `docs/pilot/results.md` girer: katılımcı sayısı, yüklenen not sayısı, 20 süre (gönüllü
  koduyla), medyan, form özetleri, isimsiz alıntılar.
- Pilot bitince isteyen gönüllünün notları kaldırılır (`upload-rules.md` bölüm 4).

## 10. İnceleme

| Kim | Neye bakar | Durum |
| --- | --- | --- |
| Arda | Tarihler, ön koşullar, "öneri" maddeleri, ölçüm protokolü | Bekliyor |
| Emine | Ölçüm protokolü (O4 raporuna girecek), form soruları | Bekliyor |
| Eylem | Dersler listesi (bölüm 4) | Gönüllü kaydından sonra |
