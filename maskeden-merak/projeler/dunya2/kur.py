"""dunya2 karşılıklarını tarih.md'deki hikâyeden kurar: karsiliklar_taslak.json ve YER_SEKILLERI.md.
Koordinatlar boylam/enlem; hedef noktalar kıyıya çok yakınsa içeri itilir. Sonra: python3 -m mk.denetle projeler/dunya2 oturt
Kullanım (maskeden-merak klasöründen): python3 projeler/dunya2/kur.py"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(KOK)))
from mk.denetle import kaynak_donustur, yon_olcek  # noqa: E402
from mk.proje import Proje  # noqa: E402
P = Proje(KOK)
YON_ALT = 35.0      # doğal yönden en az sapma (derece), CLAUDE.md §2.1 madde 7
OLCEK_UST = 2.0     # en çok büyütme
m = np.asarray(Image.open(os.path.join(KOK, "maske.png"))) > 127
D = 15.0  # piksel / derece
px = lambda lo, la: [round((lo + 180) * D, 1), round((90 - la) * D, 1)]
uzak = ndimage.distance_transform_edt(m)
_, (IY, IX) = ndimage.distance_transform_edt(uzak < 20, return_indices=True)

# yükseklik eğrileri (kaynak m → hedef m)
OVA = [[0, 0], [50, 80], [150, 160], [300, 230], [600, 370], [1000, 580], [1500, 860], [2500, 1500]]
KALKAN = [[0, 0], [200, 150], [500, 320], [1000, 650], [1600, 1100]]
ESKI_DAG = [[0, 0], [300, 200], [1000, 700], [2000, 1450], [3000, 2100]]
GENC_DAG = [[0, 0], [300, 200], [1000, 650], [2000, 1300], [3000, 2000], [4500, 2900], [6000, 3700], [7000, 4100]]
DIKIS = [[0, 0], [300, 200], [1000, 700], [2000, 1400], [3500, 2400], [5000, 3300], [6500, 4100], [8800, 5000]]
HAVZA = [[0, 0], [500, 250], [800, 320], [1100, 420], [1500, 700], [2500, 1400], [4000, 2600], [5500, 3200], [7500, 3900]]
HAVZA_DOGU = [[0, 0], [500, 250], [800, 320], [1100, 420], [1500, 700], [2500, 1300], [3500, 1650], [4500, 1850], [6000, 2200]]  # yayla kesilmez; yükseklik eğrisiyle yarıklı ve alçak kalır (kes kenarı düz çizgi bırakıyordu)
TANRI = [[0, 0], [500, 250], [800, 320], [1100, 420], [1500, 700], [2500, 1300], [3500, 1550], [4300, 1300], [5200, 950], [6000, 1750], [7000, 2300]]  # Kunlun ve Tibet yayla yüzeyi (4300 ile 5200 m) aşağı katlanır; yalnız sırtlar yüksek kalır
YAYLA = [[0, 0], [300, 180], [800, 380], [1200, 600], [1800, 1000], [2500, 1600], [3500, 2300], [4500, 2900]]

K = []


def ek(ad, olay, parca, kutu, bolge, nokta, egri=None, ayna=False, **e):
    K.append(dict(ad=ad, olay=olay, parca=parca, kutu=kutu, bolge=bolge, nokta=nokta, egri=egri, ayna=ayna, **e))


# ---------------------------------------------------------------- Batı Kıtası
ek("BatiKiyiSiralari", "Dar Okyanus'un Batı Kıtası altına dalması (Kordilyera, 180 MYÖ'den beri)", ["bati"],
   [-136, -114, 37, 60], [(-170, 64), (-142, 64), (-142, 22), (-170, 22)],
   [(-147, 56, -128, 55.5), (-158, 42, -122.5, 47), (-159, 28, -121, 40.5)], GENC_DAG, sira=True)
ek("BatiYanardagYayiKuzey", "Dar Okyanus'un Batı Kıtası altına dalması, batı kıyısında yanardağ kuşağı (Meksika yanardağ kuşağı benzeri)", ["bati"],
   [-107, -95, 17, 22.5], [(-168, 28), (-142, 28), (-140, 2), (-165, 2)],
   [(-152, 22, -104.5, 19.8), (-151, 14, -101.0, 19.6), (-150, 7, -97.5, 19.1)], GENC_DAG, sira=True)
ek("BatiYanardagYayiGuney", "Dalmanın güney kıyıdaki kolu; yayla kesildi, komşu karşılıklar doldurur", ["bati"],
   [-72, -64, -41, -17], [(-155, 4), (-125, 4), (-108, -10), (-110, -24), (-135, -24), (-155, -6)],
   [(-145, -2, -69.3, -19.5), (-132, -7.5, -69.5, -27.0), (-117, -14.9, -70.6, -35.5)], GENC_DAG, sira=True,
   kes=[[[-69.2, -15], [-65, -15], [-64.5, -27.5], [-67.6, -27.8], [-68.4, -22]]])
ek("BatiIcHavza", "Batı Kalkanı üstünde çökme havzası (Kongo benzeri)", ["bati"],
   [8, 34, -13, 8], [(-148, 16), (-110, 16), (-104, -20), (-140, -14)],
   [(-128, 1, 21, -1), (-128, -11, 21.5, -9)], OVA, ayna=True)
ek("SahraKalkani", "Batı Kalkanı; levha içi sıcak nokta masifleri (Ahaggar, Tibesti benzeri)", ["bati"],
   [-3, 26, 14, 30], [(-150, 48), (-98, 48), (-92, 22), (-98, 6), (-148, 14)],
   [(-130, 32, 5.5, 23.2), (-110, 28, 18.5, 21), (-122, 42, 9, 27.5)],
   [[0, 0], [300, 180], [600, 330], [1000, 600], [2000, 1400], [3400, 2500]])
ek("HavzaSiraDokusu", "Kordilyera ardında gerilme (Havza ve Sıra benzeri); yalnız doku katmanı", ["bati"],
   [-121, -110, 34, 44], [(-152, 50), (-128, 50), (-126, 28), (-150, 28)],
   [(-140, 42, -116.5, 41), (-138, 32, -115.5, 37)], ESKI_DAG, bant=[0.6, 0.6, 0.2, 0], oncelik=0.7, yumusak_km=220)
ek("BatiKuzeyKalkan", "Batı Kalkanı'nın kuzeyi; buzul aşındırması, göller", ["bati"],
   [-80, -58, 46, 58], [(-150, 66), (-110, 66), (-104, 47), (-150, 47)],
   [(-138, 56, -75, 51.5), (-118, 56, -63, 51.5)], KALKAN)
ek("BatiEskiDaglar", "Kaledon-Apalaş benzeri çarpışma (450 MYÖ); Kuzey'in Batı Yarımadası ile ikiz", ["bati"],
   [-88, -70, 32, 46], [(-120, 61), (-100, 61), (-78, 45), (-78, 33), (-98, 38), (-120, 48)],
   [(-116, 54, -76.5, 41.2), (-92, 42, -84, 35.5)], ESKI_DAG)
ek("DoguBasamagi", "Orta Okyanus'un açılması (190 MYÖ); edilgen kıyı basamağı (Batı Gat basamağı benzeri)", ["bati"],
   [72, 78, 9, 22], [(-100, 40), (-76, 42), (-76, 24), (-88, 10), (-98, 12)],
   [(-92, 16, 73.4, 20.5), (-87, 25, 74.4, 15.5), (-82, 33, 76.6, 10.5)],
   [[0, 0], [300, 200], [800, 500], [1500, 1000], [2800, 1900]], sira=True)
# ---------------------------------------------------------------- Orta Adalar, Güney Adası
# Orta Adalar: her ada ayrı bir yanardağ adası karşılığı alır (adalar dağınık; tek kaynak çoğunu denize düşürür)
ADA_EGRI = [[0, 0], [500, 350], [1500, 1050], [2500, 1700], [4200, 2500]]
for ad, (tlo, tla, tgen_lo, tgen_la), (kaynak, slo, sla, skm, kutu), aci, olay in [
        ("AdaBuyukKuzey", (-47.6, 21.7, 6.7, 8.4), ("İzlanda", -18.6, 64.9, 380, [-25, -13, 63, 67]), 90,
         "Orta Okyanus sırtında sıcak nokta (İzlanda benzeri, son 20 MY)"),
        ("AdaBuyukGuney", (-38.9, 10.4, 6.9, 9.8), ("Kuzey Ada (YZ)", 175.6, -38.6, 560, [172, 179, -42, -34]), 160,
         "Açılmada geride kalan kıta kırıntısı, sonradan yanardağlı"),
        ("AdaJeju", (-33.9, 33.3, 1.2, 1.4), ("Jeju", 126.55, 33.38, 60, [126, 127.1, 33.1, 33.7]), 30, "Sıcak nokta izi: genç kalkan yanardağı"),
        ("AdaHavai", (-35.4, 31.2, 2.0, 3.0), ("Havai", -155.5, 19.6, 120, [-156.2, -154.7, 18.8, 20.4]), 200, "Sıcak nokta izi: kalkan yanardağları"),
        ("AdaSicilya", (-40.3, 27.8, 2.6, 1.2), ("Sicilya", 14.2, 37.6, 230, [12.2, 15.8, 36.5, 38.4]), 0, "Kıta kırıntısı ve yanardağ"),
        ("AdaTenerife", (-43.2, 25.5, 1.5, 1.3), ("Tenerife", -16.6, 28.27, 60, [-17.0, -16.1, 27.9, 28.65]), 120, "Sıcak nokta izi: tabakalı yanardağ"),
        ("AdaKorsika", (-36.0, 23.2, 2.2, 2.2), ("Korsika", 9.05, 42.15, 150, [8.4, 9.7, 41.3, 43.1]), 300, "Kıta kırıntısı: granit dağları"),
        ("AdaGranKanarya", (-44.2, 20.2, 2.1, 1.9), ("Gran Kanarya", -15.6, 27.95, 42, [-15.9, -15.3, 27.7, 28.2]), 60, "Sıcak nokta izi: aşınmış yanardağ"),
        ("AdaMaui", (-41.8, 18.1, 1.6, 1.3), ("Maui", -156.3, 20.8, 65, [-156.75, -155.9, 20.5, 21.1]), 250, "Sıcak nokta izi: ikiz kalkan yanardağ")]:
    tkm = max(tgen_lo * np.cos(np.radians(tla)), tgen_la) * 111 * 0.9
    olc = tkm / (skm * 0.6)                           # hedef km / kaynak km; ada kaynakta tamamen karada kalsın
    r = 0.25 * tgen_la                                # ikinci nokta: merkezden kuzeye
    ar = np.radians(aci)
    dkm = r * 111 / olc                               # kaynakta karşılığı (km)
    s2 = (slo + dkm * np.sin(ar) / (111.32 * np.cos(np.radians(sla))), sla + dkm * np.cos(ar) / 110.6)
    ek(ad, olay + f" ({kaynak})", ["adalar"], kutu,
       [(tlo - tgen_lo / 2 - 1, tla + tgen_la / 2 + 1), (tlo + tgen_lo / 2 + 1, tla + tgen_la / 2 + 1),
        (tlo + tgen_lo / 2 + 1, tla - tgen_la / 2 - 1), (tlo - tgen_lo / 2 - 1, tla - tgen_la / 2 - 1)],
       [(tlo, tla, slo, sla), (tlo, tla + r, round(s2[0], 4), round(s2[1], 4))], ADA_EGRI, itme=False, oturt=False, yumusak_km=30)
ek("GuneyAdasi", "Kutup bölgesinde sıcak nokta adası, buzullu", ["gada"],
   [-25, -13, 63, 67], [(-98, -61), (-80, -61), (-80, -72), (-98, -72)],
   [(-89, -66.5, -18, 64.9), (-93, -66.5, -21, 65.2)], [[0, 0], [500, 350], [1000, 750], [2100, 1500]], ayna=True, oturt={"km": 100})
# ---------------------------------------------------------------- Kuzey Kıtası
ek("BatiYarimadaEskiDaglar", "Kaledon çarpışması (450 MYÖ), Batı Kıtası'ndaki eski dağların ikizi", ["kuzey"],
   [4, 22, 58, 71], [(-20, 61), (1, 61), (3, 44), (-2, 30), (-20, 30)],
   [(-8, 50, 17, 68.5), (-7, 37, 8, 60)], [[0, 0], [300, 220], [1000, 750], [2000, 1500], [2500, 1900]], oturt={"km": 600, "aci": 45})
ek("AlpKusagi", "Küçük bir kıta parçasının Kuzey'e çarpması (40 MYÖ)", ["kuzey"],
   [0, 30, 41, 52], [(-2, 48), (32, 48), (32, 26), (-2, 26)],
   [(6, 42, 9.5, 46.4), (24, 42, 24.5, 46.2)], [[0, 0], [300, 200], [1000, 700], [2000, 1400], [3000, 2200], [4800, 3300]])
ek("KuzeyOva", "Kuzey platformu: kalkan üstünde yatay tortul örtü", ["kuzey"],
   [26, 58, 49, 64], [(-2, 62), (45, 62), (45, 47), (-2, 47)],
   [(15, 55, 37, 56), (35, 55, 50, 56)], OVA)
ek("KuzeyKiyiKalkani", "Kuzey Kalkanı; buzul aşındırması", ["kuzey"],
   [20, 42, 60, 70], [(0, 80), (72, 80), (72, 64), (0, 60)],
   [(25, 70, 26, 64), (55, 68, 36, 66)], KALKAN)
ek("EskiDikis", "Kuzey'in iki kalkanının birleşmesi (300 MYÖ, Ural benzeri); dikiş kuzeydoğuya bükük", ["kuzey"],
   [52, 66, 48, 67], [(28, 74), (50, 74), (66, 46), (52, 42), (28, 66)],
   [(32, 70, 60.5, 65.5), (42, 63, 59.3, 61), (50, 56, 58.8, 56.5), (61, 48, 58.2, 52)],
   [[0, 0], [200, 150], [600, 500], [1200, 1200], [1900, 2100]], oncelik=2, oturt=False)
ek("OrtaSibiryaBasamaklari", "Manto sorgucu tuz bazaltları (250 MYÖ), kanyonlu basamaklar", ["kuzey"],
   [88, 120, 56, 72], [(56, 72), (100, 72), (100, 46), (56, 46)],
   [(65, 60, 97, 65), (82, 52, 110, 62)], [[0, 0], [300, 200], [800, 550], [1700, 1300]])
ek("ElbursKusagi", "Orta Deniz'in Kuzey altına dalması; batı kesimde eklenen blokların sıraları (Elburs ve Kopet Dağ benzeri)", ["kuzey"],
   [49, 63, 33, 40], [(14, 40), (38, 34), (38, 20), (26, 24), (14, 30)],
   [(20, 36, 61.0, 36.6), (28, 31, 55.5, 36.8), (36, 25.5, 50.5, 36.4)], GENC_DAG, ayna=True, sira=True)
ek("ZagrosKusagi", "Orta Deniz'in Kuzey altına dalması, eklenen blokların kıvrım kuşağı", ["kuzey"],
   [44, 60, 25, 37], [(38, 30), (64, 28), (64, 14), (38, 16)],
   [(42, 23.5, 45.5, 35.5), (52, 21, 50.5, 31.5), (61, 21, 55.5, 28.8)], GENC_DAG, sira=True)
ek("SuleymanKusagi", "Dalma önünde kıvrım yayları (Süleyman ve Kirthar benzeri)", ["kuzey"],
   [64, 73, 23, 34], [(60, 26), (82, 22), (82, 6), (60, 12)],
   [(64, 20.5, 70.2, 32.5), (70, 17, 68.5, 28.5), (77, 14.5, 67.3, 25.0)], GENC_DAG, ayna=True, sira=True)
ek("AnadoluBloklari", "Orta Deniz kapanırken eklenen kıta blokları", ["kuzey"],
   [26, 45, 36, 42], [(10, 43), (46, 43), (46, 30), (28, 29), (10, 33)],
   [(22, 38, 30, 39), (40, 33, 40, 38.8)], YAYLA)
ek("IranYaylasi", "Eklenen bloklar; havzalar alçaltıldı", ["kuzey"],
   [48, 64, 27, 37], [(42, 42), (68, 42), (68, 24), (48, 22), (42, 28)],
   [(48, 32, 52, 33.5), (62, 30, 60, 32)], YAYLA)
ek("TanriDaglariHavza", "Çarpışmanın uzak etkisi: kıta içi sıralar ve havzalar", ["kuzey"],
   [70, 96, 35, 48], [(62, 52), (118, 52), (114, 32), (62, 28)],
   [(72, 42, 77, 42), (94, 40, 90, 42.5)], TANRI)
ek("SichuanYunnan", "Doğu sözdizimi çevresinde kabuk akışı; çanak havza", ["kuzey"],
   [96, 112, 21, 34], [(78, 34), (112, 36), (110, 12), (78, 10)],
   [(88, 26, 105, 30.3), (97, 24, 102.5, 25.0)], HAVZA_DOGU)
ek("DikisDaglari", "Doğu Kolu'nun Kuzey'e çarpması (50 MYÖ'den beri), Himalaya benzeri ama daha alçak", ["kuzey", "dogu"],
   [72, 97, 25, 34], [(110, 20), (118, 17), (126, 30), (134, 44), (134, 50), (126, 50), (118, 36), (110, 26)],
   [(115.5, 21, 78.5, 30.3), (123, 34, 85, 28.4), (129, 44, 92.5, 27.9)], DIKIS, oncelik=2,
   kes=[[[77, 35], [79, 33], [81, 31], [84, 29.8], [88, 29.2], [92, 29.2], [97, 30], [97, 40], [77, 40]]], oturt={"km": 120, "aci": 10}, sira=True)
ek("ArakanSiralari", "Sözdiziminin güney ucu: Kalıntı Denizi'ne inen kıvrık sırtlar (Arakan ve Naga benzeri)", ["kuzey", "dogu"],
   [90, 99, 15, 29], [(104, 8), (114, 8), (120, 26), (112, 28)],
   [(111, 13, 94.5, 18), (114, 18, 94.0, 23.5), (117, 23, 96.5, 27.3)], GENC_DAG, ayna=True, oncelik=1.5, sira=True, oturt={"km": 120, "aci": 10})
# ---------------------------------------------------------------- Doğu Kolu
ek("OnulkeOvasi", "Çarpışma önünde Doğu Kolu üstünde önülke havzası", ["dogu"],
   [-106, -92, 31, 48], [(120, 46), (136, 46), (142, 26), (128, 10), (116, 12), (124, 30)],
   [(128, 40, -103, 45), (119, 20, -102, 33)],
   [[0, 0], [300, 120], [600, 220], [1000, 380], [1500, 600], [2000, 900], [3000, 1500]])
ek("DoguAndKuzey", "Dar Okyanus'un Doğu Kolu altına dalması", ["dogu"],
   [-80, -66, -5, 12], [(140, 50), (168, 50), (162, 18), (138, 18)],
   [(156, 42, -73.5, 9.5), (153.5, 24, -77.5, 1.0)], GENC_DAG, ayna=True, sira=True)
ek("DoguAndGuney", "Dalmanın güney kesimi; yassı dalma, kırık önülke yükselimleri (Kayalık Dağlar benzeri)", ["dogu"],
   [-118, -102, 34, 52], [(136, 24), (162, 24), (156, -2), (147, -14), (134, -14), (138, -2)],
   [(153, 16, -106.5, 37.5), (149, 2, -109.5, 43.0), (144, -10, -113.5, 48.0)], GENC_DAG, sira=True)
ek("ArdyayKiyisi", "Yay ardı havzasının açılması (Ardyay Körfezi, 25 ile 15 MYÖ): güney kıyısında yükselen kenar", ["dogu"],
   [128, 142, 41, 52], [(122, 42), (152, 42), (152, 28), (122, 28)],
   [(130, 34, 139.0, 48.0), (144, 35, 132.5, 43.5)], ESKI_DAG, sira=True)
ek("KuzeydoguYanardagYayi", "Dar Okyanus'un kuzey ucunda eklenmiş yay parçaları ve yanardağlar (Alaska Sırası benzeri)", ["dogu"],
   [-158, -138, 59, 66], [(140, 74), (170, 74), (170, 52), (140, 54)],
   [(152, 66, -143.0, 62.8), (161, 56, -154.0, 60.5)], GENC_DAG, oturt={"km": 400, "aci": 45}, sira=True)
ek("DoguIcOva", "İki önülkenin birleştiği alçak iç ova", ["dogu"],
   [-68, -50, -12, 0], [(126, 32), (150, 32), (148, 0), (126, 0)],
   [(138, 22, -62, -3), (138, 6, -60, -9)], OVA, oturt={"km": 200})
ek("TepuiKalkani", "Eski kumtaşı örtülü kalkan (masa dağları)", ["dogu"],
   [-68, -54, 0, 9], [(96, 12), (126, 12), (126, -16), (96, -14)],
   [(105, -6, -64, 5.5), (120, -8, -57, 4.0)], [[0, 0], [300, 200], [600, 350], [1500, 1000], [2800, 1900]])
ek("DoguPlanalto", "Güney Kalkanı'nın kuzey ucu; aşınmış masa yaylaları", ["dogu"],
   [-56, -42, -20, -8], [(118, -4), (146, -4), (142, -30), (118, -30)],
   [(128, -12, -50, -12.5), (136, -24, -45.5, -17.5)], [[0, 0], [300, 200], [800, 450], [1200, 700], [2000, 1300]])
# ---------------------------------------------------------------- Güney Kıtası
ek("KuzeyBazaltDogu", "Orta Deniz açılırken tuz bazaltları (130 MYÖ), kıyıya bakan basamak", ["guney"],
   [72, 81, 14, 23], [(60, -6), (98, -1), (98, -16), (62, -20)],
   [(68, -6, 73.6, 20.5), (80, -4, 74.0, 17.0), (92, -9, 74.6, 14.5)], [[0, 0], [300, 200], [800, 550], [1500, 1100]], ayna=True, sira=False)
ek("KuzeyBazaltBati", "Aynı bazalt evresi; basamaklı bazalt yaylası (Columbia benzeri)", ["guney"],
   [-123, -115, 43, 49], [(40, -22), (64, -10), (64, -26), (52, -36), (40, -36)],
   [(60, -16, -119.0, 46.5), (49, -27, -118.0, 44.5)], [[0, 0], [300, 200], [800, 550], [1500, 1100], [2500, 1700]])
ek("KavsakYanardagYaylasi", "Üçlü kavşak (30 MYÖ): yarık omzunda volkanik yayla", ["guney"],
   [35, 44, 5, 15], [(42, -26), (60, -26), (60, -46), (42, -46)],
   [(52, -34, 38.5, 10), (52, -42, 38.8, 7)], YAYLA, ayna=True)
ek("IcDenizYarigi", "Üçlü kavşağın başarısız kolu: İç Deniz çevresinde yarık basamakları", ["guney"],
   [26, 40, -16, 4], [(38, -38), (80, -38), (80, -68), (38, -68)],
   [(70, -44, 30.5, 1.5), (64, -54, 30, -6), (59, -63, 34.5, -13)], YAYLA, itme=False, sira=True)
ek("OrtaColKalkani", "Güney Kalkanı'nın iç kesimi; aşınmış sıralar ve tuz gölleri", ["guney"],
   [118, 146, -32, -17], [(62, -10), (118, -10), (122, -40), (62, -40)],
   [(95, -20, 128, -24), (110, -30, 138, -27)], [[0, 0], [200, 140], [500, 330], [1000, 650], [1500, 1000]])
ek("GuneyTepelik", "Aşınmış eski kıvrımlar, alçak tepelik", ["guney"],
   [64, 84, 45, 53], [(76, -36), (124, -36), (124, -56), (76, -56)],
   [(88, -46, 70, 49.5), (112, -46, 79, 49.5)], [[0, 0], [300, 200], [600, 380], [1200, 800], [1600, 1100]])
ek("DoguSiradaglari", "Eski orojen; edilgen kıyı yükselmesi (Serra do Mar benzeri)", ["guney"],
   [-50, -39, -27, -19], [(112, -24), (142, -24), (140, -50), (112, -50)],
   [(128, -30, -41.5, -21.5), (125, -36, -44.5, -23.0), (122, -42, -48.5, -25.3)], ESKI_DAG, sira=True)
ek("GuneyBasamagi", "Bazalt basamağı (Drakensberg benzeri), kıyıya bakar", ["guney"],
   [24, 33, -34, -23], [(116, -48), (140, -48), (140, -70), (116, -70)],
   [(126, -52, 31, -25), (127, -64, 27, -32)], [[0, 0], [300, 200], [1000, 700], [2000, 1400], [3400, 2300]], sira=True)
ek("GuneyKutupKalkani", "Güney Kalkanı; buzul aşındırması", ["guney"],
   [-79, -58, 49, 58], [(46, -58), (100, -58), (100, -76), (46, -76)],
   [(60, -66, -72, 53), (88, -66, -62, 53)], KALKAN)
ek("GuneyKiyiDaglari", "Eski yığışım kuşağı, buzul vadili (Altay benzeri)", ["guney"],
   [84, 100, 47, 54], [(96, -56), (136, -56), (136, -76), (96, -76)],
   [(105, -66, 88, 50), (125, -66, 96, 51)], ESKI_DAG)
# ---------------------------------------------------------------- Güneybatı Kıtası
ek("YarikOmzu", "Yarık Boğazı'nın açılması (25 MYÖ'den beri): kanala bakan omuz (Aden kıyısı benzeri)", ["gb"],
   [43, 53, 12.5, 17], [(18, -38), (44, -38), (44, -66), (18, -66)],
   [(37, -46, 51.0, 15.6), (36, -52, 48.5, 14.7), (35, -58, 45.5, 13.8)], YAYLA, sira=True)
ek("GuneybatiKalkan", "Güneybatı Kalkanı; buzul aşındırması, göller", ["gb"],
   [21, 33, 60, 68], [(-14, -52), (24, -52), (24, -76), (-14, -76)],
   [(0, -62, 25, 64), (16, -62, 30, 64)], KALKAN)
ek("GuneybatiAtlas", "Kıta içi ters çevrilmiş eski yarık havzası (Atlas benzeri)", ["gb"],
   [-10, 4, 29, 36], [(-14, -36), (22, -36), (22, -54), (-14, -54)],
   [(-2, -44, -6, 31.5), (14, -46, 1.5, 33)], GENC_DAG)

# ---------------------------------------------------------------- çıktı
cikti = []; satir = []
for k in K:
    nk = []
    for lo, la, slo, sla in k["nokta"]:
        x, y = px(lo, la); xi, yi = int(x), int(y)
        if uzak[yi, xi] < 20 and k.get("itme", True):
            x2, y2 = int(IX[yi, xi]), int(IY[yi, xi])
            print(f"{k['ad']}: hedef nokta ({lo}, {la}) kıyıya çok yakın ya da denizde; içeri itildi ({x2 / D - 180:.1f}, {90 - y2 / D:.1f})")
            x, y = x2, y2
        nk.append([x, y, slo, sla])
    # yön ve ölçek kuralı: alan karşılıkları kaynakta döndürülür ve yayılır; sıralar yalnız 14°'ye kadar döndürülür
    t0, dy, ol = yon_olcek(P, nk, k["ayna"])
    h = sum(ord(c) * (i + 1) for i, c in enumerate(k["ad"]))
    if dy < YON_ALT and (not k.get("sira") or YON_ALT - dy <= 14):
        ek_aci = YON_ALT - dy + (3 + h % 12 if not k.get("sira") else 2)
        for isaret in ((1, -1) if h % 2 else (-1, 1)):
            aday = kaynak_donustur(nk, isaret * ek_aci)
            if yon_olcek(P, aday, k["ayna"])[1] >= YON_ALT:
                nk = aday; break
    if ol > OLCEK_UST and not k.get("sira"):
        nk = kaynak_donustur(nk, 0, ol / OLCEK_UST)
    t1, dy1, ol1 = yon_olcek(P, nk, k["ayna"])
    uyari = ("  YÖN İHLALİ" if dy1 < YON_ALT - 0.5 else "") + ("  ÖLÇEK" if ol1 > OLCEK_UST + 0.05 else "")
    print(f"{k['ad']:<24} dönme {t0:+6.1f} → {t1:+6.1f}  sapma {dy:4.1f} → {dy1:4.1f}  büyütme {ol:4.2f} → {ol1:4.2f}{uyari}")
    xs2 = [q[2] for q in nk]; ys2 = [q[3] for q in nk]
    # kaynak kutusu, hedef bölgenin kaynaktaki karşılığını kapsasın (kutu dışı deniz sayılır)
    blo = [q[0] for q in k["bolge"]]; bla = [q[1] for q in k["bolge"]]
    gkm = max((max(blo) - min(blo)) * np.cos(np.radians(np.mean(bla))), max(bla) - min(bla)) * 111 / ol1
    yd = gkm / 111 * 0.6; cx, cy = np.mean(xs2), np.mean(ys2); xd = yd / max(np.cos(np.radians(cy)), 0.2)
    k["kutu"] = [round(min(k["kutu"][0], min(xs2) - 4, cx - xd), 2), round(max(k["kutu"][1], max(xs2) + 4, cx + xd), 2),
                 round(max(-84, min(k["kutu"][2], min(ys2) - 4, cy - yd)), 2), round(min(84, max(k["kutu"][3], max(ys2) + 4, cy + yd)), 2)]
    d = {"ad": k["ad"], "kutu": k["kutu"], "parca": k["parca"], "bolge": [px(lo, la) for lo, la in k["bolge"]], "nokta": nk}
    for a in ("ayna", "oncelik", "bant", "kes", "oturt", "yumusak_km"):
        if k.get(a) not in (None, False) or (a == "oturt" and k.get(a) is False):
            d[a] = k[a]
    if k["egri"]:
        d["yukseklik_egri"] = k["egri"]
    d["olay"] = k["olay"]
    cikti.append(d)
    tepe = max(e[1] for e in k["egri"]) if k["egri"] else None
    satir.append(f"| {k['ad']} | {', '.join(k['parca'])} | {k['olay']} | kutu {k['kutu']}{', aynalı' if k['ayna'] else ''}"
                 f"{', yalnız doku' if k.get('bant') else ''} | {tepe if tepe else ''} |")
with open(os.path.join(KOK, "karsiliklar_taslak.json"), "w", encoding="utf-8") as f:
    json.dump(cikti, f, ensure_ascii=False, indent=1)
with open(os.path.join(KOK, "YER_SEKILLERI.md"), "w", encoding="utf-8") as f:
    f.write("# Yer şekilleri ve karşılıkları\n\n`kur.py` üretir. Tepe: yükseklik eğrisinin üst ucu (m).\n\n"
            "| ad | parça | sebebi (olay) | karşılık | tepe |\n|---|---|---|---|---|\n" + "\n".join(satir) + "\n")
print(len(cikti), "karşılık yazıldı")
