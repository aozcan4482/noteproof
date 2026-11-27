# Üye dosyası — Aysu Akdüzen (`aysu`)

Kural seti sürüm 3.0 · 2026-11-27

Bu dosyanın tek amacı: **Aysu'nun** rolünü, kapsamını, kurulumunu ve görevlerini tanımlamak.
Yalnızca Aysu ile çalışan araç bu dosyayı uygular.

## 1. Roller

| | |
| --- | --- |
| İdari rol | Customer liaison: müşteri ve son kullanıcılarla iletişimi yürütür, geri bildirimlerini backlog'a taşır |
| Geliştirme rolü | Requirements analyst: story'ler, kabul kriterleri, spesifikasyon |
| Lider olduğu process'ler | P02 Stakeholder needs and requirements, P03 Requirements definition, P11 Validation |
| Sahip olduğu modül | **Student survey, pilot and acceptance** (E3; yedi story'nin kabulü; objective O4) |
| İkincisi olduğu modül | Search and proof pages (`web/`, `search/`) — Erdener'in PR'larını kullanıcı gözüyle inceler |
| Planlanan iş payı | %14 |

## 2. Kapsam

**Senin klasörlerin:** `docs/acceptance/`, `docs/pilot/`, `docs/worklog/aysu.md`.

**Dokunmayacakların:** kod klasörlerinin hepsi. Senin modülün kod değil, kanıttır: sistemin gerçek
kullanıcılar için çalıştığını gösteren senaryolar, pilot ve ölçümler. Final notunun "son kullanıcılarla
doğrulama", "her story'nin teslim durumu ve kanıtı" ve "lessons learned" kapıları senin çıktılarına bağlıdır.

Aracın senin için yazacağı şeyler belgelerdir (Markdown): kabul senaryoları, pilot planı, bilgilendirme
metni, geri bildirim formu soruları, sonuç özetleri, GitHub issue metinleri. Kod yazdırma; bir hata ya da
eksik görürsen bunu issue olarak yazdır ve modülün sahibine ilet.

**Kişisel veri kuralı.** Anket ve pilotun ham verisi (isimler, numaralar, tek tek yanıtlar, ekran
kayıtları) repoya girmez; kendi bilgisayarında ya da ekibin kapalı klasöründe kalır. Repoya yalnızca
toplu sayılar ve anonim alıntılar girer. Gönüllüler belgelerde `gönüllü-01` gibi anılır.

## 3. Ek kurulum

`06_KURULUM.md` tamamlandıktan sonra:

1. Markdown yazmak için VS Code yeterlidir (önizleme: `Ctrl+Shift+V`, macOS'te `Cmd+Shift+V`).
2. Uygulamayı kendi bilgisayarında açabilmelisin (kabul senaryolarını denemek için): `06` bölüm 6.
   Faz 2'den önce Erdener'in sayfalarını sahte veriyle açmak için: `python -m http.server 5500 --directory web`.
3. Pilotta zincir tarafını göstermek için Bitcoin Core kurman gerekmez; proof sayfası public signet
   node'unu kullanır.
4. GitHub Issues kullanımı: repo sayfası → Issues → New issue. Etiketler: `feedback`, ve ilgili story (`S1` … `S7`).
5. Geri bildirim formu için Google Forms (anketi yaptığın hesap).
6. `.env`: yalnızca `NOTEPROOF_DATA_DIR=./data`.

## 4. Görevler

### 4.1 Önce: proposal'da yapılmış görünen işler

Proposal'ın work log'unda aşağıdaki işler yapılmış olarak kayıtlı, ama repoda hiçbirinin çıktısı ya da
kanıtı yok. Bu işler **yapılmamış sayılır** ve modül görevlerinden önce, sıfırdan yapılır. Eski kayda
dayanarak "bu zaten var" deme; çıktı `main`'de değilse yoktur (`05_PIPELINE.md` bölüm 1.1).

| No | Görev | Çıktı ve kabul ölçütü | Eski kayıt | Bitiş |
| --- | --- | --- | --- | --- |
| AYS-R1 | Anket analizi: Arda'dan aldığın dışa aktarımdan sayıları yeniden say. Problem statement'taki her sayı için (20 yanıt; 17 paylaşan, 3'ü düzenli; 17'nin 10'u WhatsApp, 9'u fotoğraf; 5 izinsiz paylaşım, 5 emin değil; medyan 10–20 dk, 13'ü ≥ 10 dk; 14'ü kullanırdı) "proposal'daki / dışa aktarımdan sayılan" tablosu | `docs/pilot/survey-summary.md`: yalnızca toplu sayılar, ham yanıt ve isim yok. Uyuşmayan sayı varsa Arda'ya bildirildi | #2 | 23 Kas |
| AYS-R2 | Başlangıç değerlerinin kontrolü: objective'lerin baseline'larını ankete karşı doğrula (O4: 15 dk = 10–20 dk medyan yanıtının ortası; diğerleri 0) | Aynı dosyada "Baseline kontrolü" bölümü: her objective için kaynak ve sonuç | #4 | 23 Kas |

Bu görevler de diğerleri gibi branch → PR → `main` yolundan geçer ve commit'lerinde `Task: AYS-R1 (done)`
biçiminde izlenir. Work log'a iki kayıt girilir (`04_GIT_AKISI.md` bölüm 9.1): yapılan iş için kanıtlı bir **Work** kaydı
ve tablodaki "Eski kayıt" numarasını gösteren bir **Correction** kaydı.

### 4.2 Modül görevleri

| No | Görev | Kabul ölçütü | Bağımlılık | Bitiş |
| --- | --- | --- | --- | --- |
| AYS-1 | Kabul senaryoları: `docs/acceptance/S1.md` … `S7.md`. Her dosyada: story metni, Given/When/Then kabul kriteri (`01` bölüm 7), elle izlenecek adımlar (hangi sayfa, ne tıklanır, ne görülmeli), gereken test verisi, sonuç tablosu (tarih, sürüm, geçti/kaldı, kanıt linki). Üç proposal senaryosu (bir olağan, iki reddetme) ilgili dosyalarda | Yedi dosya; projeyi bilmeyen biri adımları izleyebiliyor; Emine inceledi | — | 23 Kas |
| AYS-2 | Yükleme kuralları: müşteriyle (3. ve 4. sınıf grupları) teyit — hangi dosyalar, ne "kendi notu" sayılır, bildirilen not nasıl kaldırılır. `docs/pilot/upload-rules.md`; K-006'yı kapat | Kurallar bir sayfa; en az birkaç öğrencinin görüşü alınmış; `07_KARARLAR.md` K-006 teyit edildi | — | 27 Kas |
| AYS-3 | Pilot planı: `docs/pilot/plan.md` — hedef gönüllü sayısı ve nasıl bulunacakları, tarihler (5–9 Aralık), hangi dersler (Eylem'e liste), görevler (not yükle, not ara, proof kontrol et), ölçüm protokolü, bilgilendirme ve açık rıza metni, geri bildirim formu soruları | Plan Arda ve Emine tarafından incelendi; dersler listesi Eylem'e iletildi | AYS-1 | 27 Kas |
| AYS-4 | Erdener'in PR'larını incele: metinler anlaşılır mı, akış kabul senaryosuna uyuyor mu, telefonda kullanılıyor mu, "olası kopya" dili hüküm içeriyor mu | Her `web/` PR'ına 24 saat içinde yorum | ERD-1 … | sürekli |
| AYS-5 | Deneme oturumu: `v0.3.0` ile 2–3 öğrenci, her biri üç görevi yapar; takıldıkları yerler not edilir | Her bulgu bir GitHub issue (`feedback` + story etiketi); özet `docs/pilot/dry-run.md`'de | Faz 2 | 1 Ara |
| AYS-6 | Pilot: gönüllüler kendi notlarını yükler; quiz haftasında not ararlar. Ölçümler: **O4** — 20 arama süresi (kronometreyle, konu verildiği andan doğru notun açıldığı ana kadar), medyan; geri bildirim formu | `docs/pilot/results.md`: katılımcı sayısı, yüklenen not sayısı, 20 süre ve medyan (hedef ≤ 2 dk; başlangıç 15 dk), form özetleri, anonim alıntılar. Ham veri repoda yok | AYS-3, BRK-7, `v0.9.0` | 9 Ara |
| AYS-7 | Kabul ve doğrulama: `v0.9.0` ya da sonrası üzerinde yedi kabul senaryosunu çalıştır, sonuç tablolarını doldur; her story için "teslim edildi / edilmedi" ve kanıt linki; doğrulama yazısı ve **lessons learned** (İngilizce, en az 80 kelime; proposal'a girecek) | `docs/acceptance/` sonuçları dolu; `docs/pilot/validation.md` hazır ve Arda'ya iletildi | AYS-6 | 10 Ara |

**Araç için notlar:**

- Kabul senaryosu yazarken kabul kriterini değiştirme; `01` bölüm 7'deki metin sabittir. Kriter gerçeğe
  uymuyorsa bunu Arda'ya iletilecek bir not olarak yaz.
- Ölçüm protokolü ölçmeden önce yazılır ve ölçüm sırasında değişmez: kim ölçer, süre ne zaman başlar ve
  biter, başarısız arama nasıl sayılır.
- Sonuçları olduğu gibi yaz. Hedef tutmadıysa tutmadığını ve olası nedenini yaz; sayı düzeltme, örnek seçme.
- Bilgilendirme metni şunları söyler: ne toplanıyor (yüklenen notlar, takma ad, süre ölçümleri, form
  yanıtları), ne toplanmıyor (isim, numara), notların zincire gitmediği (yalnızca 32 byte'lık kök),
  katılımın gönüllü olduğu ve notun istenince arşivden kaldırılabildiği.
- Her gönüllüye proof'un sınırı söylenir: kanıt, notun o tarihte var olduğunu ve kimin kaydettiğini
  gösterir; ilk yazanın kim olduğunu göstermez.

## 5. Başkalarına sağladıkların

| Kime | Ne | Ne zaman |
| --- | --- | --- |
| Emine, Erdener, Arda | Kabul senaryoları (test ve arayüz bunlara göre yapılır) | 23 Kas |
| Eylem | Pilot dersleri listesi | 27 Kas |
| Erdener | Arayüz geri bildirimi (PR yorumu ve issue) | sürekli |
| Emine | O4 ölçümü (değerlendirme raporu için) | 9 Ara |
| Arda | Story teslim durumları, doğrulama yazısı, lessons learned | 10 Ara |

## 6. Başkalarından beklediklerin

| Kimden | Ne | Hazır değilse |
| --- | --- | --- |
| Erdener | Denenebilir sayfalar | Senaryoları `01` ve `02` bölüm 7'ye göre yaz; ekran adlarını sayfalar gelince düzelt |
| Burak | Signet'te çalışan günlük timestamp (pilot için) | Pilotu regtest demosuyla yapma; Arda ile tarihi konuş |
| Emine | Pilotta ölçüm yardımı | — |

## 7. İdari görevler

- **Customer liaison:** 3. ve 4. sınıf gruplarıyla iletişim sende: yükleme kuralları, pilot duyurusu,
  gönüllüler, sonuçların onlara geri bildirilmesi. Gelen her istek ve şikâyet bir issue olur.
- **Requirements lideri (P02, P03):** bir story'nin ya da kabul kriterinin ne anlama geldiği sorulduğunda
  yanıtı sen verirsin; yanıtı ilgili `docs/acceptance/` dosyasına da yazarsın.
- **Validation lideri (P11):** "teslim edildi" kararını sen verirsin; karar kabul senaryosunun sonucuna dayanır.
- Değerlendirme seti için en az 9 kendi notunu Emine'ye ver.

## 8. Push ve work log

Kod yazmasan da düzenli push kuralı sana da geçerlidir (`04` bölüm 4): her biten belge bir commit ve bir
PR'dır (`docs/<kısa-ad>` branch'i, özet `docs: ...` ya da story'ye bağlıysa `S5: ...`). Reviewer'ın Emine'dir.

Tipik process'ler: P02 (müşteriyle görüşme, yükleme kuralları), P03 (kabul senaryoları), P11 (deneme
oturumu, pilot, kabul). Kanıt linki olarak belge PR'ını ya da issue'yu ver.
