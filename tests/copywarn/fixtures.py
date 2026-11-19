"""Testler için SENTETİK not metinleri.

Bunlar gerçek öğrenci notları DEĞİLDİR: testlerin çalışması için yazılmış kısa
örnek metinlerdir. Gerçek değerlendirme seti (60 not) evalset/notes/ altına ekibin
kendi notlarından eklenir.

"fees_a" ve "fees_b" aynı konuyu (işlem ücretleri) FARKLI cümlelerle anlatır:
aynı konudaki iki özgün not birbirinin kopyası sayılmamalı.
"""

NOTES = {
    "fees_a": (
        "İşlem ücreti, girdilerin toplamı ile çıktıların toplamı arasındaki farktır. "
        "Madenciler blok alanı sınırlı olduğu için yüksek ücret ödeyen işlemleri önce seçer. "
        "Ücret genelde satoshi bölü sanal bayt olarak, yani fee rate olarak ifade edilir. "
        "Mempool doluysa düşük ücretli işlem saatlerce bekleyebilir. "
        "Replace-by-fee ile aynı girdileri harcayan, daha yüksek ücretli yeni bir işlem gönderilebilir. "
        "Child-pays-for-parent yönteminde çocuk işlem, ebeveynin düşük ücretini telafi eder. "
        "Cüzdanlar ücreti tahmin etmek için son blokların ücret dağılımına bakar."
    ),
    "fees_b": (
        "Bitcoin'de ücret ayrı bir alan olarak yazılmaz, girdiler eksi çıktılar kadar kalan miktar ücrettir. "
        "Bir işlemin ne kadar hızlı onaylanacağını belirleyen şey ödediği vbayt başına ücrettir. "
        "Ağ yoğun olduğunda cüzdanın önerdiği ücret yükselir. "
        "Takılan bir işlemi hızlandırmanın iki yolu vardır: RBF ve CPFP. "
        "RBF orijinal işlemi yenisiyle değiştirir, CPFP ise yeni bir çocuk işlemle ikisini birlikte cazip yapar. "
        "Toz miktarındaki çıktıları harcamak bazen ücretten daha pahalıya gelir."
    ),
    "merkle": (
        "Merkle ağacında her yaprak bir işlemin hash'idir ve iki düğüm birleştirilip yeniden hash'lenir. "
        "En üstte kalan tek değer Merkle köküdür ve blok başlığına yazılır. "
        "Bir işlemin blokta olduğunu kanıtlamak için bütün bloğa değil, yalnızca Merkle yoluna ihtiyaç vardır. "
        "Yolun uzunluğu işlem sayısının logaritması kadardır. "
        "Basitleştirilmiş ödeme doğrulaması bu fikre dayanır ve hafif cüzdanlar böyle çalışır. "
        "Tek sayıda düğüm kaldığında Bitcoin son düğümü kopyalar, bu da bilinen bir zayıflığa yol açmıştır."
    ),
    "keys": (
        "Özel anahtar rastgele seçilmiş 256 bitlik bir sayıdır. "
        "Açık anahtar, özel anahtarın secp256k1 eğrisi üzerinde üreteç noktasıyla çarpılmasıyla elde edilir. "
        "Bu işlem tek yönlüdür, açık anahtardan özel anahtar bulunamaz. "
        "Adres, açık anahtarın hash'inden türetilir ve kodlama olarak bech32 kullanılabilir. "
        "Taproot ile Schnorr imzaları geldi ve çoklu imzalar tek imza gibi görünebiliyor. "
        "Seed cümlesi kaybedilirse cüzdandaki paraya bir daha erişilemez."
    ),
    "mining": (
        "Madenci, blok başlığının hash'i hedef değerden küçük olana kadar nonce değerini değiştirir. "
        "Zorluk her 2016 blokta bir, blokların ortalama on dakikada bulunması için ayarlanır. "
        "Bloğu bulan madenci coinbase işlemiyle blok ödülünü ve ücretleri alır. "
        "Blok ödülü her 210000 blokta bir yarıya iner. "
        "İki madenci aynı anda blok bulursa zincir geçici olarak çatallanır ve en çok işi olan zincir kazanır. "
        "Madencilik havuzları ödülü katkıya göre paylaştırır."
    ),
    "network": (
        "Bitcoin düğümleri eşler arası bir ağ kurar ve birbirlerine işlem ile blok iletir. "
        "Yeni bir düğüm önce DNS tohumlarından eş adresleri öğrenir. "
        "Tam düğüm her bloğu ve işlemi kurallara göre kendisi doğrular. "
        "Compact block yöntemi, düğümlerin zaten bildiği işlemleri tekrar göndermeyerek bant genişliği kazandırır. "
        "Signet, imzalı blokların kullanıldığı ve gerçek para gerektirmeyen bir test ağıdır. "
        "Regtest ise blokların komutla anında üretildiği tamamen yerel bir ağdır."
    ),
    "script": (
        "Bitcoin Script yığın tabanlı ve kasıtlı olarak Turing-tam olmayan bir dildir. "
        "Kilitleme scripti bir çıktının hangi şartla harcanacağını söyler. "
        "Kilit açma scripti bu şartı sağlayan imzayı ve açık anahtarı verir. "
        "OP_RETURN çıktısı harcanamaz ve en fazla seksen bayt veri taşıyabilir. "
        "Zaman kilitleri, bir çıktının belirli bir blok yüksekliğinden önce harcanmasını engeller. "
        "Çoklu imza scriptleri birden fazla anahtarın onayını ister."
    ),
    "wallets": (
        "Hiyerarşik deterministik cüzdanlar tek bir tohumdan sınırsız anahtar türetir. "
        "Türetme yolları BIP32 ve BIP44 gibi standartlarla belirlenir. "
        "Her ödeme için yeni bir adres kullanmak gizliliği artırır. "
        "Donanım cüzdanları özel anahtarı bilgisayara hiç göstermeden imza atar. "
        "İzleme cüzdanı yalnızca açık anahtarları bilir ve bakiye gösterir ama harcayamaz. "
        "Yedekleme için tohum cümlesi kağıda yazılıp güvenli bir yerde saklanır."
    ),
}
