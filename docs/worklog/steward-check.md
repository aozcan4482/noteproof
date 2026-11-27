# Work log steward kontrolleri

Her cuma iki steward kontrol eder (uyeler/aleyna.md ve uyeler/eylem.md bölüm 7):
Aleyna → Eylem, Burak, Erdener · Eylem → Arda, Aysu, Aleyna, Emine.

Her kontrol bir satırdır: `main`'deki `proposal/proposal.json` zincirinin sağlam olup olmadığı, kontrol edilen
üyelerin o hafta Workbench'e kayıt girip girmediği ve `docs/worklog/<slug>.md` taslaklarında "hayır" kalan satırlar.
Eksiği olana aynı gün ekip grubundan haber verilir.

| Tarih | Steward | Zincir (`main`) | Kontrol edilen | Bu hafta girilen kayıt | Taslakta bekleyen ("hayır") | Haber verildi |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-27 | aleyna | Sağlam: 14 kayıt, hash'ler yeniden hesaplandı; son kayıt 2026-10-16 | Eylem | 0 | Taslak dosyası yok | evet (grup, 27 Kas) |
| 2026-11-27 | aleyna | ″ | Burak | 0 | 8 satır, 11 saat (20–26 Kas; `docs/brk-0-worklog-move`, #8) | evet (grup, 27 Kas) |
| 2026-11-27 | aleyna | ″ | Erdener | 0 | 2 satır, 3 saat (24 ve 26 Kas; `docs/readme`, #9) | evet (grup, 27 Kas) |

Notlar (2026-11-27):

- Zincir, Workbench'in kendi formülüyle (`SHA-256(prev + U+001E + alanlar)`) yeniden hesaplandı; 14 kaydın hepsi tutuyor.
- Kontrol anında (27 Kasım sabahı) 23–27 Kasım haftasında `main`'e hiçbir üyenin kaydı girmemişti. Sonra Aleyna'nın kayıt 15'i #11 ile 11:31'de `main`'e girdi; zincir 15 kayıtla sağlam.
- Risk: bekleyen kayıtlar tek oturumda girilirse "aynı üyenin 10 dakika içinde 5 kaydı" ihlali oluşur; 10 dakikada en çok 4 kayıt.
