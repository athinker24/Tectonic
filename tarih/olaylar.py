"""Dünyam tektonik tarihi: tek kaynak.

Koordinatlar görüntü pikseli: maske 2000 × 1530'a ölçeklenmiş çerçeve, 1 px = 4 km, x doğuya, y güneye.
Enlem: üst kenar 50°K, alt kenar yaklaşık 5°G (enlem = 50 − y × 4 / 111,2).
Zaman: milyon yıl önce (MYÖ), bugün 0.

Parça numaraları sahibin numaralarıdır: 1 kuzeybatı, 2 kuzeydoğu, 3 doğu dil, 4 güneybatı,
5 güney orta, 6 iç deniz adası, 7 güneydoğu (uzun) yarımada.
"""
import numpy as np

KM_PX = 4.0
GEN, YUK = 2000, 1530


def enlem(y):
    return 50.0 - np.asarray(y, float) * KM_PX / 111.2


# ---------------------------------------------------------------------------------------------
# Parça sınırları (bugünkü), sahibin çizgileri ve benim eklediğim şerit sınırı
# ---------------------------------------------------------------------------------------------
CIZGI = {
    "mavi": [(800, 0), (805, 200), (810, 400), (813, 600)],
    "mor": [(1080, 615), (1140, 565), (1300, 572), (1500, 628), (1720, 690)],
    "sari": [(800, 930), (785, 965), (755, 1005), (735, 1060), (725, 1130), (722, 1200), (728, 1250), (745, 1330), (755, 1400)],
    "yesil": [(910, 1115), (898, 1132), (885, 1150), (883, 1180), (895, 1215), (915, 1245), (940, 1275), (950, 1290)],
    # İnce Şerit'in kuzey dikişi (210 MYÖ kapanan Eski Mor Okyanusu'nun izi); 2'nin içinde
    "serit": [(1060, 520), (1180, 455), (1400, 425), (1600, 445), (1800, 515), (1990, 560)],
    # Batı kara köprüsü: 1 ile 4 arası (Köprü Dağları dikişi)
    "kopru": [(0, 740), (90, 790), (170, 805)],
}

# ---------------------------------------------------------------------------------------------
# Hareket: her parça için (zaman, açı°, dx, dy) bugünden geçmişe dönüşüm, parça ağırlık merkezi
# etrafında; açı + görüntüde saat yönü. 1 ve 2 (Kuzey) sabit çerçevedir.
# ---------------------------------------------------------------------------------------------
HAREKET = {
    # 4: makas açılması 130 ile 85 MYÖ; kapalıyken 29° saat yönünün tersine (geri), Biscay benzeri
    "4": [(0, 0, 0, 0), (85, 0, 0, 0), (100, -10, 25, -40), (115, -20, 50, -80), (130, -29, 76, -116), (400, -29, 76, -116)],
    # 6: 130 MYÖ'de 4 ile birlikte 1'e bitişik; 25 MYÖ'den beri yay ardı gerilmesiyle güneye çekiliyor
    "6": [(0, 0, 0, 0), (12, -1, -10, -20), (25, -4, -30, -55), (85, -6, -40, -70), (100, -11, -52, -100),
          (115, -17, -64, -132), (130, -22, -76, -164), (400, -22, -76, -164)],
    # 3: Güney Kıtası'ndan 150 MYÖ'de kopar, kuzeye koşar, 50 MYÖ'de 2'ye (İnce Şerit) çarpar
    "3": [(0, 0, 0, 0), (10, 3, 0, 38), (20, 6, 0, 80), (35, 10, -5, 150), (50, 16, -20, 260), (66, 22, -40, 520),
          (85, 28, -60, 800), (120, 32, -80, 1150), (150, 35, -90, 1400), (400, 35, -90, 1400)],
    # İnce Şerit: 2'nin güney kuşağı; 270 MYÖ'de Güney Kıtası'ndan kopar, 210 MYÖ'de 2'ye yapışır
    "serit": [(0, 0, 0, 0), (210, 0, 0, 0), (225, 2, 0, 300), (240, 4, -10, 650), (255, 6, -20, 1000), (270, 8, -30, 1330), (400, 8, -30, 1330)],
}
# 5 ve 7: 22 MYÖ'ye kadar 3'ün batısına bağlı (göreli konum: 3'ün bugünkü çerçevesinde)
BAGLI_3 = {
    "5": (-24, 176, -44),   # kanal kapatma uydurması (7 ayrık): açı, dx, dy
    "7": (0, 220, 108),     # yanal fay boyunca geri kaydırma
}
KOPMA_5_7 = 22.0  # MYÖ
# Güney Kıtası (çerçeve dışı, şematik): 320 MYÖ'de 4'ün güneyine çarpar, 160 MYÖ'de ayrılıp güneye gider
GUNEY_KITA = [(0, 0, 1500), (60, 0, 1150), (100, 0, 700), (130, 0, 380), (160, 0, 0), (320, 0, 0), (340, 0, 260), (400, 0, 600)]

# ---------------------------------------------------------------------------------------------
# Bugünkü levhalar
# ---------------------------------------------------------------------------------------------
LEVHALAR = [
    ("Kuzey Levhası", "büyük", "1, 2 ve 4 ile batı iç deniz tabanı, kuzey ve batı kıta sahanlıkları", "sabit çerçeve"),
    ("Doğu Dil Levhası", "küçük", "3 ve doğu kıyısının önündeki kabuk", "kuzeye, doğu ucunda yaklaşık 2,4 cm/yıl, batı ucunda 1,2 cm/yıl; saat yönünün tersine milyon yılda 0,3° dönüş"),
    ("Orta Blok", "mikro", "5", "batıya yaklaşık 2,8 cm/yıl, saat yönünde dönüş; 4'ün altına dalıyor"),
    ("Uzun Yarımada Bloğu", "mikro", "7", "kuzeybatıya yaklaşık 4,6 cm/yıl; 3'e göre kanal fayı boyunca yanal kayma"),
    ("Ada Bloğu", "mikro", "6", "güneye yaklaşık 0,7 cm/yıl; yay ardı gerilmesi"),
    ("Doğu Havza Levhası", "mikro (okyanusal)", "doğu iç denizin tabanı, eski Mor Okyanusu kalıntısı", "kuzeybatıya 0,8 cm/yıl; 6'nın altına dalıyor"),
    ("Kaçış Bloğu", "mikro", "2'nin güneydoğu köşesi", "doğuya yaklaşık 1,2 cm/yıl; Büyük Kaçış Fayı boyunca sol yanal"),
    ("Doğu Okyanusu Levhası", "büyük (okyanusal)", "doğudaki açık okyanus", "batıya yaklaşık 6,5 cm/yıl; 3'ün doğu kıyısının altına dalıyor"),
    ("Batı Okyanusu Levhası", "büyük (okyanusal)", "batıdaki okyanus", "sırt çerçeve dışında, yılda 2,4 cm açılma; kıyılar edilgen kenar"),
    ("Güney Okyanusu Levhası", "büyük (okyanusal)", "güneydeki okyanus", "sırt çerçeve dışında; 4 ve 5 kıyıları edilgen kenar"),
    ("Kutup Levhası", "küçük (okyanusal)", "kuzey okyanusu", "Kuzey Levhası'ndan yılda 0,6 cm ayrılıyor; sırt çerçeve dışında"),
]

# ---------------------------------------------------------------------------------------------
# Dönemler ve olaylar. Her olay: (MYÖ, başlık, açıklama). Zaman aralıkları "ile" ile yazılır.
# ---------------------------------------------------------------------------------------------
DONEMLER = [
    {
        "ad": "Kalkanların doğuşu",
        "aralik": (3400, 2500),
        "ozet": (
            "Kıtanın en eski kabuğu dört ayrı çekirdekte oluştu. Bugün 1'in kuzeyinde Ak Kalkan, 2'nin doğu yarısında "
            "Boz Kalkan, 2'nin batısında Kır Çekirdeği ve 3'ün ortasında Kızıl Kalkan bu dönemin kayalarını taşır. "
            "Bu çekirdekler o zaman birbirinden binlerce kilometre uzaktı. Hepsi kalın, soğuk ve yüzer bir kök "
            "geliştirdi; sonraki üç milyar yıl boyunca hemen hiç deforme olmamalarının nedeni bu köktür. Bugün düz, "
            "alçak ve buzulların kazıdığı göllerle dolu ovalar olarak görünürler."),
        "olaylar": [
            (3400, "Ak Kalkan çekirdeği", "1'in kuzeyindeki granit ve gnays çekirdeği; kıtanın bilinen en yaşlı kayaları."),
            (3100, "Boz Kalkan", "2'nin doğu yarısının çekirdeği; sonradan en geniş kalkan."),
            (2900, "Kızıl Kalkan", "3'ün ortasındaki çekirdek; bugün bazalt örtünün altında."),
            (2700, "Kır Çekirdeği", "2'nin batısında küçük ve ince bir çekirdek; ileride çarpışmalarda en çok örselenen."),
        ],
    },
    {
        "ad": "Kaynak orojenleri",
        "aralik": (2100, 1700),
        "ozet": (
            "Kır Çekirdeği ile Boz Kalkan arasındaki dar okyanus kapandı ve 2'nin bugünkü iç kısmı tek parça oldu. "
            "Ak Kalkan'ın güney kenarına da yaylar ve küçük kıta parçaları eklendi. Bu dönemin sıradağları çoktan "
            "aşındı; izleri yalnız 2'nin ortasında kuzey güney uzanan hafif sırtlar, göl dizileri ve nehirlerin "
            "aniden yön değiştirdiği yerlerde görülür."),
        "olaylar": [
            (2000, "Kaynak dikişi", "Kır Çekirdeği ile Boz Kalkan birleşir; 2'nin ortasında kuzey güney uzanan eski dikiş."),
            (1850, "Ak Kalkan güney eklentisi", "Ak Kalkan'ın güneyine yay kabuğu eklenir; 1'in bugünkü orta kesimi."),
            (1750, "Kaynak sıradağlarının çöküşü", "Kalınlaşmış kabuk yayılarak incelir; geniş granit sokulumları."),
        ],
    },
    {
        "ad": "İlk Birlik",
        "aralik": (1150, 750),
        "ozet": (
            "Bütün çekirdekler ve dünyanın başka kıtaları İlk Birlik adını verdiğim bir süper kıtada toplandı. "
            "1'in batı kenarında, bugünkü batı kıyısına paralel uzun bir çarpışma kuşağı yükseldi: Ulu Dağlar. "
            "Süper kıta 800 ile 750 milyon yıl önce parçalandığında 1 ile 2 arasında Ata Okyanusu açıldı. "
            "Ulu Dağlar bugün 1'in batısında yuvarlak sırtlı, 1300 metreyi pek aşmayan eski dağlardır."),
        "olaylar": [
            (1100, "Ulu Dağlar orojeni", "1'in batı kenarında kıta çarpışması; bugünkü batı kıyısına paralel kuşak."),
            (1000, "İlk Birlik tamamlanır", "Bütün çekirdekler tek kıtada."),
            (800, "Ata yarığı", "1 ile 2 arasında yarılma; bugünkü mavi çizginin yerinde."),
            (750, "Ata Okyanusu", "Yarık okyanusa dönüşür; 1 ile 2 ayrı kıtalar olarak uzaklaşır."),
        ],
    },
    {
        "ad": "Buz ve Ata Okyanusu",
        "aralik": (750, 520),
        "ozet": (
            "Ata Okyanusu genişlerken iki büyük buzullaşma oldu ve buzullar tropik enlemlere kadar indi. 1 ve 2'nin "
            "edilgen kenarlarında kalın kıyı çökelleri birikti. Bu çökeller sonraki çarpışmada Mavi Dağlar'ın "
            "kıvrımlı kayalarını oluşturacaktı."),
        "olaylar": [
            (700, "Birinci büyük buzullaşma", "Buzul çökelleri 1'in ve 2'nin kenarlarında."),
            (640, "İkinci büyük buzullaşma", "Daha kısa; sonrasında ılık ve sığ denizler."),
            (600, "Edilgen kenar çökelleri", "Ata Okyanusu kıyılarında kireçtaşı ve kumtaşı yığılır."),
            (540, "Ata Okyanusu en geniş", "Yaklaşık 3000 km; okyanus sırtı 1 ile 2'nin ortasında."),
        ],
    },
    {
        "ad": "Mavi orojeni",
        "aralik": (520, 400),
        "ozet": (
            "Ata Okyanusu 2'nin batı kenarının altına dalarak kapanmaya başladı. Önce okyanus içi yaylar, sonra "
            "küçük kıta parçaları 2'ye eklendi. 430 milyon yıl önce 1 ile 2 çarpıştı ve mavi çizgi boyunca "
            "Kaledonya benzeri bir sıradağ yükseldi. Bu dikiş bugün de kabuğun en zayıf yerlerinden biri: kuzey "
            "kıyıdaki dar ve uzun girinti, buzulların bu eski zayıflık hattını oyarak açtığı bir fiyorttur. Mavi Dağlar "
            "sonraki dönemlerde birkaç kez hafifçe yeniden yükseldi ve bugün 1500 ile 1800 metrelik yaylalar halinde "
            "duruyor."),
        "olaylar": [
            (500, "Ata dalması başlar", "Okyanus 2'nin batısının altına doğuya doğru dalar; yay volkanları."),
            (470, "Yay eklenmesi", "Okyanus içi yay 2'ye yapışır."),
            (445, "Mikro kıta eklenmesi", "Küçük bir kıta parçası 2'nin batı kenarına çarpar."),
            (430, "1 ile 2 çarpışır", "Mavi çizgi boyunca Mavi Dağlar; 1 ve 2 Kuzey Kıtası olur."),
            (410, "Çöküş ve yanal faylar", "Kalınlaşmış kuşak yanal faylarla parçalanır; dağ arası havzalar."),
        ],
    },
    {
        "ad": "Köz orojeni ve Büyük Birlik",
        "aralik": (400, 290),
        "ozet": (
            "Kuzey Kıtası'nın güneyindeki Orta Okyanus, güneyden gelen Güney Kıtası'nın önünde kapandı. Okyanus "
            "kapanırken araya sıkışan yaylar ve kıta parçaları 1'in güney kenarına eklendi; bugünkü 4'ün temeli "
            "bu parçalardan oluşur. 320 milyon yıl önce Güney Kıtası çarptı ve Köz orojeni yükseldi. Böylece "
            "Büyük Birlik süper kıtası oluştu. Çarpışma batıdan başladığı için doğuda kapanmayan kama biçimli bir "
            "okyanus kaldı: Mor Okyanusu. 4'ün içindeki granit masifleri ve yuvarlak tepeler bu dağların aşınmış "
            "kökleridir. Ön ülke havzalarında, o zaman ekvatorda olan bataklıklarda kalın kömür katmanları birikti."),
        "olaylar": [
            (390, "Orta Okyanus dalması", "Okyanus 1'in güney kenarının altına kuzeye dalar."),
            (370, "Güney yayı eklenir", "Bugünkü 4'ün kuzey kesiminin temeli."),
            (345, "Köz mikro kıtası", "4'ün güneyindeki kıta parçası; bugünkü güney kıyısının temeli."),
            (320, "Güney Kıtası çarpışması", "Köz orojeni; 4'ün tamamı kıvrılır."),
            (305, "Kömür bataklıkları", "Ekvator ormanları; ön ülke havzalarında kömür."),
            (295, "Büyük Birlik", "Süper kıta tamamlanır; doğuda Mor Okyanusu kaması açık."),
        ],
    },
    {
        "ad": "Mor kaması ve İnce Şerit",
        "aralik": (290, 200),
        "ozet": (
            "Büyük Birlik'in içi kurak ve sıcaktı; kızıl kumtaşları ve tuz gölleri yaygındı. Mor Okyanusu'nun güney "
            "kıyısında, Güney Kıtası'nın kenarından uzun ve ince bir kıta şeridi koptu. Arkasında Yeni Mor Okyanusu "
            "açılırken önündeki Eski Mor Okyanusu 2'nin altına daldı. İnce Şerit 210 milyon yıl önce 2'nin güney "
            "kenarına yapıştı. Bugünkü Mor Yaylası'nın kabuğu çoğunlukla bu şerittir; yaylanın içindeki doğu batı "
            "uzanan sırtlar bu eski dikişlerin yeniden sıkışmasıdır. 252 milyon yıl önce 2'nin kuzeyinde büyük bir "
            "bazalt püskürmesi oldu; o dönemde canlıların büyük kısmı yok oldu. Kuzey Tuzakları bugün 2'nin kuzeyinde "
            "basamaklı bir bazalt yaylası olarak duruyor."),
        "olaylar": [
            (280, "Kurak iç kıta", "Kızıl kumtaşı, kum tepeleri, tuz gölleri."),
            (270, "İnce Şerit kopar", "Güney Kıtası'nın kuzeyinden şerit ayrılır; Yeni Mor Okyanusu açılmaya başlar."),
            (252, "Kuzey Tuzakları", "2'nin kuzeyinde taşkın bazaltları; büyük yok oluş."),
            (240, "Eski Mor dalması", "Eski Mor Okyanusu 2'nin güney kenarının altına dalar; yay volkanları."),
            (210, "Şerit çarpışması", "İnce Şerit 2'ye yapışır; Şerit dağları (bugün Mor Yaylası'nın içindeki sırtlar)."),
        ],
    },
    {
        "ad": "Büyük Birlik'in parçalanması",
        "aralik": (200, 130),
        "ozet": (
            "Süper kıta batıdan ve güneyden yarıldı. 190 milyon yıl önce 1 ile 4'ün batısında Batı Okyanusu "
            "açılmaya başladı; batı kıyıları o zamandan beri sakin, geniş sahanlıklı edilgen kenarlardır. 160 "
            "milyon yıl önce Güney Kıtası 4'ten ayrıldı ve Güney Okyanusu açıldı. 150 milyon yıl önce Güney "
            "Kıtası'nın kuzeydoğusundan 3, 5 ve 7'yi taşıyan bir parça koptu ve kuzeye, Yeni Mor Okyanusu'na doğru "
            "yola çıktı. Yeni Mor Okyanusu'nun kuzey kenarı İnce Şerit'in altına dalmaya başladı ve 2'nin güney "
            "kenarında And tipi bir volkan sırası yükseldi."),
        "olaylar": [
            (195, "Batı yarığı", "1 ile 4'ün batısında kıta yarılır; kısa bir bazalt evresi."),
            (185, "Batı Okyanusu", "Okyanus kabuğu oluşur; batı kıyıları edilgen kenar."),
            (170, "Yeni Mor dalması", "Yeni Mor Okyanusu İnce Şerit'in altına dalar; 2'nin güneyinde volkan yayı."),
            (160, "Güney Okyanusu açılır", "Güney Kıtası 4'ten ayrılır."),
            (150, "Doğu Parça kopar", "3, 5 ve 7 Güney Kıtası'ndan ayrılır, kuzeye yönelir."),
        ],
    },
    {
        "ad": "Makas açılması",
        "aralik": (130, 85),
        "ozet": (
            "4, 6 ile birlikte 1'den ayrıldı. Açılma bir makas gibiydi: dönme merkezi batı körfezinin batı ucundaydı ve "
            "4, 45 milyon yılda yaklaşık 29° saat yönünde döndü. İç denizin batısı ile batı körfezi doğuya doğru "
            "genişleyen bir kama olarak açıldı; doğuda okyanus kabuğu oluştu, batıda kabuk yalnız inceldi. Bu dönüş "
            "batıdaki kara köprüsünü sıkıştırdı: dönme merkezinin öbür yanında kalan köprüde 95 milyon yıl önce "
            "Köprü Dağları yükselmeye başladı. 1'in iç denize bakan kıyıları yarık omzu olarak yükseldi."),
        "olaylar": [
            (130, "Makas yarığı", "4 ve 6, 1'den ayrılmaya başlar."),
            (115, "Batı iç deniz tabanı", "İç denizin batısında ince okyanus kabuğu; batı körfezinde aşırı incelmiş kıta kabuğu."),
            (100, "Hızlı dönüş", "4 ve 6 yılda yaklaşık 3,5 cm hızla güneydoğuya döner."),
            (95, "Köprü sıkışması", "Kara köprüsünde bindirmeler; Köprü Dağları başlar."),
            (85, "Dönüş durur", "4 bugünkü yönüne ulaşır; makas açılması sona erer."),
        ],
    },
    {
        "ad": "Kuzeye koşu",
        "aralik": (85, 50),
        "ozet": (
            "3, 5 ve 7'yi taşıyan Doğu Parça Yeni Mor Okyanusu'nu hızla geçti. En hızlı olduğu 66 ile 50 milyon yıl "
            "arasında yılda yaklaşık 6,5 cm ilerledi. 66 milyon yıl önce bir sıcak noktanın üzerinden geçti: 3'ün "
            "ortası taşkın bazaltlarıyla örtüldü ve bugünkü Kızıl Basamaklar oluştu. Bu sırada Doğu Okyanusu 3'ün "
            "doğu kenarının altına dalmaya başladı. Köprü Dağları bu dönemde en yüksek haline ulaştı."),
        "olaylar": [
            (80, "Hızlanma", "Doğu Parça'nın hızı yılda 5 cm'yi aşar."),
            (66, "Kızıl Basamaklar", "Sıcak nokta üzerinde taşkın bazaltları; 3'ün ortası."),
            (60, "Doğu dalması", "Doğu Okyanusu 3'ün doğu kenarının altına dalar; Doğu Yay Dağları başlar."),
            (55, "Köprü Dağları zirvede", "Kara köprüsünde sıkışma en yüksek düzeyde."),
        ],
    },
    {
        "ad": "Mor çarpışması",
        "aralik": (50, 25),
        "ozet": (
            "3, 2'ye (İnce Şerit'in güney kenarına) önce doğu ucundan, yaklaşık 50 milyon yıl önce çarptı. Çarpışma "
            "batıya doğru ilerledi ve 35 milyon yıl önce batı ucuna ulaştı. 3 saat yönünün tersine yavaşça dönerek "
            "geldiği için doğu ucu hep daha hızlı sıkıştı. 3'ün kuzey kenarı 2'nin altına daldı ve yaklaşık 1000 km "
            "genişliğinde bir kıta kenarı bu dalmada kayboldu. Kalınlaşan kabuk Mor Sıradağları'nı ve arkasında Mor "
            "Yaylası'nı yükseltti. Sıkışma uzağa iletildi: 2'nin içinde Uzak Sıra eski dikişler boyunca yeniden "
            "yükseldi, aralarında Kum Havzası çöktü, 2'nin güneydoğu köşesi doğuya kaçmaya başladı. Batı ucu yavaş "
            "kapandığı için orada kapanmamış bir deniz kolu kaldı: bugünkü üçgen koy. Yeni Mor Okyanusu'nun 3'ün batısında "
            "kalan parçası kuşatıldı; doğu iç denizin tabanı bu eski okyanusun kalıntısıdır."),
        "olaylar": [
            (50, "Doğu ucunda ilk temas", "3'ün kuzeydoğu köşesi İnce Şerit'e değer."),
            (45, "Mor Sıradağları yükselir", "Doğu kesimde hızlı kalınlaşma."),
            (40, "Mor Yaylası başlar", "Sıradağların arkasında kabuk kalınlaşır; Şerit dikişleri yeniden sıkışır."),
            (35, "Batı ucu kapanır", "Çarpışma üçgen koya ulaşır; koy kapanmamış ön ülke denizi olarak kalır."),
            (32, "Doğu iç deniz kuşatılır", "Yeni Mor Okyanusu'nun kalıntısı iç denizde kapana kısılır."),
            (30, "Derin Göl Yarığı", "2'nin içinde çarpışmanın uzak etkisiyle kuzeydoğu güneybatı uzanan yarık açılır."),
            (28, "Uzak Sıra ve Kum Havzası", "Eski dikişler boyunca yeniden yükselme; arada çöküntü havzası."),
            (26, "Kaçış Bloğu", "2'nin güneydoğu köşesi Büyük Kaçış Fayı boyunca doğuya kaymaya başlar."),
        ],
    },
    {
        "ad": "İç deniz evresi",
        "aralik": (25, 2.6),
        "ozet": (
            "Doğu iç denizin okyanus tabanı 6'nın altına dalmaya başladı ve dalan levha güneye doğru geri çekildi. "
            "Üstteki 6 gerildi; parmak biçimli yarımadaları ve aralarındaki körfezler bu gerilmenin yükselmiş bloklar "
            "ile çöküntüler halindeki izidir. 6, 4'ten koparak güneye kaydı ve güney açığında küçük volkan adaları "
            "yükseldi. Aynı dönemde 4'ün doğu kenarının altına dalan levhanın çekişi 5'i batıya sürükledi: 5, 22 "
            "milyon yıl önce 3'ten koptu ve arkasında güneydoğu kanalı yarık olarak açıldı. Kanalın kuzeyinde 8 milyon "
            "yıldan beri okyanus kabuğu oluşuyor. 5 dönerek ilerlediği için güney ucu önce, yaklaşık 8 milyon yıl önce "
            "4'e çarptı; Sarı Sıradağları en yüksek güney orta kesimdedir ve kuzeye doğru alçalır. 5'in güney ucu "
            "kanal fayı boyunca kesildi ve kuzeybatıya sürüklenen 7 oldu. 7, 5'e sıkışarak bastırdığı için dar ve "
            "dik bir dağ sırtı taşır; kuzeyindeki dar girinti ilerlemeden kalmış bir yarık koludur."),
        "olaylar": [
            (25, "Ada Hendeği", "Doğu iç deniz tabanı 6'nın altına kuzeye dalar; geri çekilme başlar."),
            (22, "5 kopar", "5, 3'ten ayrılır; güneydoğu kanalı yarığı açılır."),
            (20, "Kanal Fayı ve 7", "5'in güney ucu kesilir, 7 kuzeybatıya kaymaya başlar."),
            (18, "6, 4'ten kopar", "Ada bloğu güneye çekilirken 4'ten ayrılır; parmak biçimli horst ve graben dizisi."),
            (14, "Sarı yayı", "4'ün doğu kenarında volkanlar (5'in önündeki okyanus kabuğu dalar)."),
            (10, "Ada yayı volkanları", "6'nın güney açığında volkan adaları."),
            (8, "Sarı çarpışması", "5'in güney ucu 4'e çarpar; çarpışma kuzeye ilerler."),
            (8, "Kanalda okyanus kabuğu", "Güneydoğu kanalının kuzeyinde deniz tabanı yayılması."),
            (5, "Sarı Sıradağları hızla yükselir", "Genç, dik, hızla aşınan dağlar; Tayvan benzeri."),
            (4, "Mor Yaylası bugünkü yüksekliğinde", "Ortalama yaklaşık 4,3 km."),
        ],
    },
    {
        "ad": "Buzul çağları ve bugün",
        "aralik": (2.6, 0),
        "ozet": (
            "Kuzeyde, 40. enlemin üstünde büyük buz örtüleri defalarca ilerleyip çekildi. 1 ve 2'nin kuzeyi buzla "
            "kazındı: sayısız küçük göl, fiyortlar, sürüklenmiş kaya örtüsü. Mor Sıradağları, Uzak Sıra ve Sarı "
            "Sıradağları'nda dağ buzulları vadileri derinleştirdi. Deniz seviyesi buzul dönemlerinde 120 metreye kadar "
            "düştü; son buzul çağından sonra yükselen deniz 4'ün güney kıyısındaki dallı nehir vadilerini boğarak "
            "bugünkü girintili kıyıyı yarattı. Bugün iki çarpışma etkin: 3, 2'nin altına; 5, 4'ün altına giriyor."),
        "olaylar": [
            (2.6, "Buzullaşma başlar", "Kuzey kıyılarında buz örtüsü."),
            (0.9, "Büyük buz örtüleri", "Kuzeyde 100 bin yıllık döngüler; Mavi fiyordu derinleşir."),
            (0.02, "Son buzul maksimumu", "Deniz seviyesi 120 m aşağıda; sahanlıklar kara."),
            (0.007, "Boğulmuş vadiler", "Deniz yükselir; 4'ün güney kıyısında dallı girintiler."),
            (0, "Bugün", "İki etkin çarpışma, bir yanal fay, bir yay ardı gerilmesi, bir yarık."),
        ],
    },
]

# ---------------------------------------------------------------------------------------------
# Yer şekilleri: arazi üretimi için. Çizgiler görüntü pikseli; yükseklik metre; yarı genişlik km.
# yas: ana yükselmenin yaşı (MYÖ); genç kuşak keskin, yaşlı kuşak yuvarlak.
# dik: profilin dik yanı; +1 çizginin sağı (ilerleme yönüne göre), −1 solu, 0 simetrik.
# ---------------------------------------------------------------------------------------------
KUSAKLAR = [
    # ad, çizgi, tepe yükseklikleri (her köşe), yarı genişlik km, yaş, dik yan
    ("Mor Sıradağları", [(1095, 600), (1150, 548), (1300, 553), (1500, 607), (1712, 668)], [2600, 4800, 6400, 7300, 6600], 120, 0, +1),
    ("Kuzey Kenar Sırası", [(1180, 470), (1400, 438), (1600, 458), (1770, 520)], [4800, 5600, 5800, 5200], 55, 5, -1),
    ("Şerit Sırtları", [(1220, 505), (1450, 485), (1650, 510), (1760, 560)], [5200, 5600, 5900, 5500], 35, 10, 0),
    ("Uzak Sıra", [(990, 340), (1080, 305), (1180, 300), (1280, 270), (1380, 285), (1480, 310), (1560, 285), (1640, 240)], [2000, 2900, 3600, 4300, 4500, 4100, 3700, 2800], 105, 15, 0),
    ("Mavi Dağlar", [(790, 40), (830, 150), (800, 260), (780, 380), (820, 470), (830, 560)], [1100, 1400, 1500, 1300, 1200, 1000], 150, 430, 0),
    ("Ulu Dağlar", [(160, 200), (120, 300), (150, 400), (115, 500), (140, 600), (170, 660)], [900, 1150, 1250, 1100, 1000, 800], 100, 1000, 0),
    ("Köprü Dağları", [(0, 760), (90, 790), (170, 830), (240, 885)], [2400, 3100, 2900, 1800], 60, 50, 0),
    ("Köz Masifleri", [(80, 960), (200, 1010), (300, 1080), (420, 1120), (500, 1190), (620, 1260)], [700, 950, 800, 900, 850, 650], 160, 310, 0),
    ("Sarı Sıradağları", [(772, 975), (748, 1030), (733, 1100), (728, 1180), (733, 1250), (746, 1310)], [1700, 2500, 3200, 3900, 3700, 2300], 70, 0, +1),
    ("Kanal Omzu (3)", [(1035, 965), (1055, 1030), (1080, 1110), (1120, 1180)], [1500, 2000, 1900, 1400], 45, 15, -1),
    ("Kanal Omzu (5)", [(905, 1000), (925, 1050), (935, 1095)], [1100, 1300, 900], 30, 15, +1),
    ("Uzun Yarımada Sırtı", [(905, 1150), (980, 1188), (1060, 1228), (1150, 1268)], [2200, 2700, 2400, 1600], 28, 3, 0),
    ("Doğu Yay Dağları", [(1580, 790), (1530, 870), (1495, 960), (1497, 1050), (1490, 1090)], [3000, 3900, 4200, 3600, 2800], 70, 2, -1),
    ("Kanca Yayı", [(1440, 875), (1462, 905), (1492, 918)], [1600, 2100, 1500], 18, 1, 0),
    ("Güneydoğu Yay Dağları", [(1530, 1140), (1500, 1230), (1462, 1320), (1440, 1395)], [2800, 3300, 2600, 1600], 35, 1, 0),
    ("Ada Omurgası", [(605, 760), (700, 722), (820, 735), (892, 805)], [1600, 2300, 2100, 1500], 35, 8, 0),
    ("1 İç Deniz Omzu", [(575, 545), (552, 630), (530, 720)], [1200, 1500, 1100], 50, 110, +1),
    ("Doğu Düğümü", [(1700, 650), (1780, 690), (1860, 700)], [5200, 5800, 4200], 50, 0, 0),
]

PLATOLAR = [
    # ad, çokgen, yükseklik (batı → doğu iki değer, doğrusal), kenar yumuşatma km
    ("Mor Yaylası", [(1160, 548), (1190, 478), (1400, 446), (1600, 466), (1770, 530), (1790, 600), (1740, 640), (1500, 595), (1300, 545)], (3900, 4700), 60),
    ("Kum Havzası", [(1100, 430), (1130, 360), (1220, 330), (1350, 315), (1480, 330), (1570, 345), (1615, 410), (1520, 425), (1400, 415), (1280, 440), (1180, 455)], (1150, 1250), 40),
    ("Kızıl Basamaklar", [(1150, 860), (1230, 820), (1350, 830), (1420, 900), (1420, 1000), (1390, 1120), (1300, 1220), (1220, 1240), (1150, 1170), (1120, 1050), (1130, 940)], (900, 1100), 25),
    ("Kuzey Tuzakları", [(1150, 90), (1250, 55), (1380, 70), (1460, 60), (1500, 130), (1480, 210), (1400, 250), (1300, 240), (1220, 260), (1160, 200)], (1100, 1300), 25),
    ("Köz Yaylası", [(150, 950), (500, 900), (650, 1000), (650, 1250), (350, 1300), (150, 1150)], (650, 750), 80),
]

OVALAR = [
    # ad, çokgen, hedef yükseklik (alçaltma)
    ("Mor Ön Ovası", [(1085, 640), (1300, 598), (1500, 650), (1700, 712), (1620, 780), (1400, 765), (1200, 725), (1090, 700)], 90),
    ("Sarı Ön Havzası", [(790, 1000), (845, 1010), (865, 1150), (845, 1300), (762, 1312), (758, 1100)], 140),
    ("Batı Kıyı Ovası (1)", [(60, 450), (110, 300), (130, 230), (100, 520), (60, 520)], 60),
]

GOLLER = [
    # ad, çokgen ya da çizgi + yarı genişlik (px), su seviyesi m
    ("Derin Göl", {"cizgi": [(1605, 335), (1650, 255), (1700, 175), (1755, 115)], "gen": 7}, 450),
    ("Kum Gölü", {"cizgi": [(1560, 395), (1590, 405)], "gen": 9}, 1080),
    ("Yayla Gölü", {"cizgi": [(1420, 470), (1470, 468)], "gen": 7}, 4550),
    ("Kuzey Yayla Gölü", {"cizgi": [(1300, 492), (1335, 488)], "gen": 5}, 4600),
]

VOLKANLAR = [
    (1555, 830), (1520, 900), (1500, 985), (1500, 1060), (1465, 905), (1515, 1170), (1490, 1260), (1455, 1345),
    (770, 920), (1025, 1110), (760, 1040), (742, 1150),
]

DIP = {
    # deniz tabanı: (ad, çizgi, derinlik m, yarı genişlik km)
    "hendekler": [
        ("Doğu Hendeği", [(1620, 760), (1580, 900), (1560, 1050), (1580, 1200), (1620, 1380)], -7200, 60),
        ("Ada Hendeği", [(610, 975), (720, 985), (860, 950), (960, 880)], -3600, 40),
    ],
    "havzalar": [
        ("Doğu İç Deniz", [(880, 600), (1050, 650), (1120, 780), (1080, 900), (950, 930), (900, 800)], -3000),
        ("Batı İç Deniz", [(300, 820), (520, 860), (600, 940), (450, 900)], -2200),
        ("Kanal Kuzey", [(930, 950), (1040, 960), (1060, 1080), (980, 1090)], -2600),
    ],
}

# ---------------------------------------------------------------------------------------------
# Ek olaylar (küçük olaylar, ofiyolitler, granitler, havzalar); dönemlerine eklenir ve sıralanır
# ---------------------------------------------------------------------------------------------
_EK = {
    "Kalkanların doğuşu": [(3000, "Yeşiltaş kuşakları", "Kalkanların içinde volkanik ve tortul kuşaklar; altın ve demir yatakları.")],
    "Kaynak orojenleri": [(1950, "Boz okyanus içi yayı", "Boz Kalkan ile Kır Çekirdeği arasındaki okyanusta yay; bugün 2'nin ortasında gömülü."),
                          (1800, "Kızıl kenar orojeni", "Kızıl Kalkan'ın çevresine kuşak eklenir.")],
    "İlk Birlik": [(1080, "Ulu granitleri", "Çarpışma sonrası granit sokulumları; bugün Ulu Dağlar'ın dorukları."),
                   (900, "Uzun sakinlik", "Süper kıtanın içinde aşınma; geniş düzlükler.")],
    "Buz ve Ata Okyanusu": [(720, "Ata yarık bazaltları", "Yarık kenarlarında bazalt akıntıları."),
                            (580, "Canlılığın çeşitlenmesi", "Sığ denizlerde ilk karmaşık canlılar.")],
    "Mavi orojeni": [(490, "Ata ofiyoliti", "Okyanus kabuğundan bir dilim 1'in kenarına itilir; bugün Mavi Dağlar'ın batı yamacında."),
                     (420, "Mavi granitleri", "Çarpışma sonrası granitler; Mavi Dağlar'ın en dayanıklı kayaları.")],
    "Köz orojeni ve Büyük Birlik": [(380, "Orta yay volkanları", "1'in güney kenarında volkan yayı."),
                                    (335, "Köz ofiyolitleri", "Orta Okyanus tabanından dilimler 4'e bindirilir."),
                                    (300, "Köz granitleri", "Çarpışma sonrası granitler; bugünkü Köz Masifleri.")],
    "Mor kaması ve İnce Şerit": [(230, "Yeni Mor sırtı hızlanır", "Şerit kuzeye yılda 9 cm'ye varan hızla ilerler."),
                                 (220, "Şerit önü yayı", "Şerit'in önündeki okyanus içi yay, Şerit'le birlikte 2'ye eklenir."),
                                 (205, "Çarpışma sonrası tuz havzaları", "2'nin güneyinde kapalı havzalarda kalın tuz.")],
    "Büyük Birlik'in parçalanması": [(180, "Batı kıyı havzaları", "Batı Okyanusu kıyısında tuz ve organik çamur birikir."),
                                     (155, "Kireçtaşı platformları", "Yeni Mor Okyanusu kıyılarında sığ deniz platformları."),
                                     (140, "Güney sırt atlaması", "Güney Okyanusu sırtı yön değiştirir; küçük bir kıta parçası batıya sürüklenir (çerçeve dışında).")],
    "Makas açılması": [(125, "Batı körfezi tuzları", "Dar açılan körfezde tuz birikir."),
                       (105, "Aşırı incelme", "Batı iç denizin batısında manto yüzeye yaklaşır; kıta kabuğu 10 km'nin altına iner.")],
    "Kuzeye koşu": [(70, "Yeni Mor ofiyolitleri", "Okyanus kabuğu dilimleri 3'ün kuzey kenarına bindirilir; bugün Mor Sıradağları'nın güney yamacında."),
                    (62, "Sıcak nokta izi", "3 ayrıldıktan sonra sıcak nokta okyanus tabanında deniz altı dağları dizer.")],
    "Mor çarpışması": [(42, "Ön ova çöker", "3'ün kuzeyi sıradağın yükü altında esner; Mor Ön Ovası oluşur."),
                       (38, "Doğu Düğümü", "Doğu köşede sıkışma düğümü; nehirler keskin dirsekler yapar.")],
    "İç deniz evresi": [(12, "Ada Bloğu bağımsızlaşır", "6 kendi hareketi olan bir mikro levha olur."),
                        (6, "Uzun Yarımada sırtı yükselir", "7'nin 5'e bastırmasıyla dar sırt."),
                        (3, "Kanal çekme havzaları", "Kanal fayı boyunca derin, dik kenarlı havzalar.")],
    "Buzul çağları ve bugün": [(1.5, "Yayla buzulları", "Mor Yaylası'nda buzul gölleri ve moren setleri."),
                               (0.13, "Son buzul arası", "Deniz bugünden yaklaşık 6 m yüksek."),
                               (0.0115, "Buz örtüsü çekilir", "Kuzeyde binlerce göl açığa çıkar.")],
}
for _D in DONEMLER:
    _D["olaylar"] = sorted(_D["olaylar"] + _EK.get(_D["ad"], []), key=lambda q: -q[0])
