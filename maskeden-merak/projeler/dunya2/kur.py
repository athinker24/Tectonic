"""dunya2 karşılıklarını tarih.md'deki hikâyeden kurar: karsiliklar_taslak.json ve YER_SEKILLERI.md.
Koordinatlar boylam/enlem; hedef noktalar kıyıya çok yakınsa içeri itilir. Sonra: python3 -m mk.denetle projeler/dunya2 oturt
Kullanım (maskeden-merak klasöründen): python3 projeler/dunya2/kur.py"""
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

KOK = os.path.dirname(os.path.abspath(__file__))
m = np.asarray(Image.open(os.path.join(KOK, "maske.png"))) > 127
D = 15.0  # piksel / derece
px = lambda lo, la: [round((lo + 180) * D, 1), round((90 - la) * D, 1)]
uzak = ndimage.distance_transform_edt(m)
_, (IY, IX) = ndimage.distance_transform_edt(uzak < 20, return_indices=True)

# yükseklik eğrileri (kaynak m → hedef m)
OVA = [[0, 0], [150, 110], [300, 190], [600, 330], [1000, 560], [1500, 850], [2500, 1500]]
KALKAN = [[0, 0], [200, 150], [500, 320], [1000, 650], [1600, 1100]]
ESKI_DAG = [[0, 0], [300, 200], [1000, 700], [2000, 1450], [3000, 2100]]
GENC_DAG = [[0, 0], [300, 200], [1000, 650], [2000, 1300], [3000, 2000], [4500, 2900], [6000, 3700], [7000, 4100]]
DIKIS = [[0, 0], [300, 200], [1000, 700], [2000, 1400], [3500, 2400], [5000, 3300], [6500, 4100], [8800, 5000]]
HAVZA = [[0, 0], [500, 250], [800, 320], [1100, 420], [1500, 700], [2500, 1400], [4000, 2600], [5500, 3200], [7500, 3900]]
YAYLA = [[0, 0], [300, 180], [800, 380], [1200, 600], [1800, 1000], [2500, 1600], [3500, 2300], [4500, 2900]]

K = []


def ek(ad, olay, parca, kutu, bolge, nokta, egri=None, ayna=False, **e):
    K.append(dict(ad=ad, olay=olay, parca=parca, kutu=kutu, bolge=bolge, nokta=nokta, egri=egri, ayna=ayna, **e))


# ---------------------------------------------------------------- Batı Kıtası
ek("BatiKiyiSiralari", "Dar Okyanus'un Batı Kıtası altına dalması (Kordilyera, 180 MYÖ'den beri)", ["bati"],
   [-136, -114, 37, 60], [(-170, 64), (-142, 64), (-142, 22), (-170, 22)],
   [(-147, 56, -128, 55.5), (-158, 42, -122.5, 47), (-159, 28, -121, 40.5)], GENC_DAG)
ek("BatiYanardagYayi", "Dalmanın güney kesimi: volkanik yay ve ignimbrit yaylası", ["bati"],
   [-112, -95, 16, 30], [(-168, 26), (-140, 26), (-118, -6), (-110, -24), (-135, -24), (-160, 0)],
   [(-152, 18, -106, 26.5), (-148, 4, -104.5, 21.5), (-133, -8, -100, 19.5), (-117, -15, -97.5, 19.0)], GENC_DAG)
ek("BatiIcHavza", "Batı Kalkanı üstünde çökme havzası (Kongo benzeri)", ["bati"],
   [8, 34, -13, 8], [(-148, 16), (-110, 16), (-104, -20), (-140, -14)],
   [(-128, 1, 21, -1), (-128, -11, 21.5, -9)], OVA, ayna=True)
ek("SahraKalkani", "Batı Kalkanı; levha içi sıcak nokta masifleri (Ahaggar, Tibesti benzeri)", ["bati"],
   [-3, 26, 14, 30], [(-150, 48), (-98, 48), (-92, 22), (-148, 14)],
   [(-130, 32, 5.5, 23.2), (-110, 28, 18.5, 21), (-122, 42, 9, 27.5)],
   [[0, 0], [300, 180], [600, 330], [1000, 600], [2000, 1400], [3400, 2500]])
ek("HavzaSiraDokusu", "Kordilyera ardında gerilme (Havza ve Sıra benzeri); yalnız doku katmanı", ["bati"],
   [-121, -110, 34, 44], [(-152, 50), (-128, 50), (-126, 28), (-150, 28)],
   [(-140, 42, -116.5, 41), (-138, 32, -115.5, 37)], ESKI_DAG, bant=[1, 1, 0.3, 0])
ek("BatiKuzeyKalkan", "Batı Kalkanı'nın kuzeyi; buzul aşındırması, göller", ["bati"],
   [-80, -58, 46, 58], [(-150, 66), (-110, 66), (-104, 47), (-150, 47)],
   [(-138, 56, -75, 51.5), (-118, 56, -63, 51.5)], KALKAN)
ek("BatiEskiDaglar", "Kaledon-Apalaş benzeri çarpışma (450 MYÖ); Kuzey'in Batı Yarımadası ile ikiz", ["bati"],
   [-88, -70, 32, 46], [(-120, 61), (-100, 61), (-78, 45), (-78, 33), (-98, 38), (-120, 48)],
   [(-116, 54, -76.5, 41.2), (-92, 42, -84, 35.5)], ESKI_DAG)
ek("DoguBasamagi", "Orta Okyanus'un açılması (190 MYÖ); edilgen kıyı basamağı", ["bati"],
   [-54, -38, -27, -12], [(-98, 40), (-76, 42), (-76, 24), (-92, 6), (-106, -12), (-114, -10), (-100, 14)],
   [(-80, 31, -40.5, -15), (-88, 20, -42.5, -21), (-96, 9, -47, -23.8)],
   [[0, 0], [300, 200], [800, 500], [1500, 1000], [2800, 1900]])
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
    olc = tkm / skm                                   # hedef km / kaynak km
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
   [0, 30, 41, 52], [(-2, 48), (32, 48), (32, 36), (-2, 36)],
   [(6, 42, 9.5, 46.4), (24, 42, 24.5, 46.2)], [[0, 0], [300, 200], [1000, 700], [2000, 1400], [3000, 2200], [4800, 3300]])
ek("KuzeyOva", "Kuzey platformu: kalkan üstünde yatay tortul örtü", ["kuzey"],
   [26, 58, 49, 64], [(-2, 62), (45, 62), (45, 47), (-2, 47)],
   [(15, 55, 37, 56), (35, 55, 50, 56)], OVA)
ek("KuzeyKiyiKalkani", "Kuzey Kalkanı; buzul aşındırması", ["kuzey"],
   [20, 42, 60, 70], [(0, 80), (72, 80), (72, 64), (0, 60)],
   [(25, 70, 26, 64), (55, 68, 36, 66)], KALKAN)
ek("EskiDikis", "Kuzey'in iki kalkanının birleşmesi (300 MYÖ, Ural benzeri), bükük", ["kuzey"],
   [52, 66, 48, 67], [(36, 74), (56, 74), (57, 42), (38, 42)],
   [(46, 70, 60.5, 65.5), (49, 62, 59.3, 61), (45, 54, 58.8, 56.5), (47, 46, 58.2, 52)],
   [[0, 0], [200, 150], [600, 500], [1200, 1200], [1900, 2100]], oncelik=2, oturt=False)
ek("OrtaSibiryaBasamaklari", "Manto sorgucu tuz bazaltları (250 MYÖ), kanyonlu basamaklar", ["kuzey"],
   [88, 120, 56, 72], [(56, 72), (100, 72), (100, 46), (56, 46)],
   [(65, 60, 97, 65), (82, 52, 110, 62)], [[0, 0], [300, 200], [800, 550], [1700, 1300]])
ek("ZagrosKusagi", "Orta Deniz'in Kuzey altına dalması, eklenen blokların kıvrım kuşağı", ["kuzey"],
   [44, 60, 25, 37], [(18, 36), (50, 30), (50, 14), (30, 20), (18, 28)],
   [(25, 33, 45.5, 35.5), (40, 24, 50.5, 31.0), (52, 21, 55.5, 28.8)], GENC_DAG)
ek("MakranKusagi", "Dalma önünde yığışım prizması ve kıvrım yayı", ["kuzey"],
   [57, 71, 24, 31], [(48, 28), (82, 24), (82, 8), (48, 14)],
   [(55, 21, 59, 26.5), (72, 15.5, 67.5, 27.0)], GENC_DAG)
ek("AnadoluBloklari", "Orta Deniz kapanırken eklenen kıta blokları", ["kuzey"],
   [26, 45, 36, 42], [(10, 43), (46, 43), (46, 30), (28, 29), (10, 33)],
   [(22, 38, 30, 39), (40, 33, 40, 38.8)], YAYLA)
ek("IranYaylasi", "Eklenen bloklar; havzalar alçaltıldı", ["kuzey"],
   [48, 64, 27, 37], [(42, 42), (68, 42), (68, 24), (48, 22), (42, 28)],
   [(48, 32, 52, 33.5), (62, 30, 60, 32)], YAYLA)
ek("TanriDaglariHavza", "Çarpışmanın uzak etkisi: kıta içi sıralar ve havzalar", ["kuzey"],
   [70, 96, 35, 48], [(62, 52), (100, 52), (100, 30), (62, 28)],
   [(72, 42, 77, 42), (94, 40, 90, 42.5)], HAVZA)
ek("SichuanYunnan", "Doğu sözdizimi çevresinde kabuk akışı; çanak havza", ["kuzey"],
   [96, 112, 21, 34], [(78, 32), (104, 32), (104, 12), (78, 10)],
   [(88, 26, 105, 30.3), (97, 24, 102.5, 25.0)], HAVZA)
ek("DikisDaglari", "Doğu Kolu'nun Kuzey'e çarpması (50 MYÖ'den beri), Himalaya benzeri ama daha alçak", ["kuzey", "dogu"],
   [72, 97, 25, 34], [(110, 20), (118, 17), (126, 30), (134, 44), (134, 50), (126, 50), (118, 36), (110, 26)],
   [(115.5, 21, 78.5, 30.3), (123, 34, 85, 28.4), (129, 44, 92.5, 27.9)], DIKIS, oncelik=2,
   kes=[[[77, 35], [79, 33], [81, 31], [84, 29.8], [88, 29.2], [92, 29.2], [97, 30], [97, 40], [77, 40]]], oturt={"km": 120, "aci": 10})
ek("ArakanSiralari", "Sözdiziminin güney ucu: Kalıntı Denizi'ne inen paralel sırtlar", ["kuzey", "dogu"],
   [90, 98, 15, 27], [(104, 8), (114, 8), (120, 26), (112, 28)],
   [(117, 23, 94, 25.5), (111, 13, 94.5, 18)], GENC_DAG, ayna=True, oncelik=1.5, oturt={"km": 120, "aci": 10})
# ---------------------------------------------------------------- Doğu Kolu
ek("OnulkeOvasi", "Çarpışma önünde Doğu Kolu üstünde önülke havzası", ["dogu"],
   [-106, -92, 31, 48], [(120, 46), (136, 46), (142, 26), (128, 10), (116, 12), (124, 30)],
   [(128, 40, -103, 45), (119, 20, -102, 33)],
   [[0, 0], [300, 120], [600, 220], [1000, 380], [1500, 600], [2000, 900], [3000, 1500]])
ek("DoguAndKuzey", "Dar Okyanus'un Doğu Kolu altına dalması", ["dogu"],
   [-80, -66, -5, 12], [(140, 50), (168, 50), (162, 18), (138, 18)],
   [(156, 42, -73.5, 9.5), (153.5, 24, -77.5, 1.0)], GENC_DAG, ayna=True)
ek("DoguAndGuney", "Dalmanın güney kesimi; kırık önülke sıraları", ["dogu"],
   [-73, -62, -40, -25], [(136, 24), (162, 24), (156, -2), (147, -12), (143, -30), (132, -30), (138, -2)],
   [(153, 16, -69.5, -27.5), (148, 0, -70.0, -33.0), (138, -20, -71, -39.5)], GENC_DAG, ayna=True)
ek("ArdyayKiyisi", "Yay ardı havzasının açılması (Ardyay Körfezi, 25 ile 15 MYÖ): güney kıyısında yükselen kenar", ["dogu"],
   [128, 142, 41, 52], [(122, 42), (152, 42), (152, 28), (122, 28)],
   [(130, 34, 138.5, 47.5), (144, 35, 134.5, 44.0)], ESKI_DAG)
ek("KuzeydoguYanardagYayi", "Dar Okyanus'un kuzey ucunda eklenmiş yay parçaları ve yanardağlar (Alaska Sırası benzeri)", ["dogu"],
   [-158, -138, 59, 66], [(140, 74), (170, 74), (170, 52), (140, 54)],
   [(152, 66, -147.5, 63.3), (161, 56, -152.5, 61.0)], GENC_DAG, oturt={"km": 400, "aci": 45})
ek("DoguIcOva", "İki önülkenin birleştiği alçak iç ova", ["dogu"],
   [-76, -60, -14, -2], [(126, 32), (150, 32), (148, 0), (126, 0)],
   [(138, 22, -70, -4), (138, 6, -66, -12)], OVA)
ek("TepuiKalkani", "Eski kumtaşı örtülü kalkan (masa dağları)", ["dogu"],
   [-68, -54, 0, 9], [(96, 3), (126, 3), (126, -16), (96, -14)],
   [(105, -6, -64, 5.5), (120, -8, -57, 4.0)], [[0, 0], [300, 200], [600, 350], [1500, 1000], [2800, 1900]])
ek("DoguPlanalto", "Güney Kalkanı'nın kuzey ucu; aşınmış masa yaylaları", ["dogu"],
   [-56, -42, -20, -8], [(118, -4), (146, -4), (142, -30), (118, -30)],
   [(128, -12, -50, -12.5), (136, -24, -45.5, -17.5)], [[0, 0], [300, 200], [800, 450], [1200, 700], [2000, 1300]])
# ---------------------------------------------------------------- Güney Kıtası
ek("KuzeyBazaltDogu", "Orta Deniz açılırken tuz bazaltları (130 MYÖ), kıyıya bakan basamak", ["guney"],
   [72, 81, 14, 23], [(60, -6), (98, -1), (98, -16), (62, -20)],
   [(68, -6, 73.6, 20.5), (80, -4, 74.0, 17.0), (92, -9, 74.6, 14.5)], [[0, 0], [300, 200], [800, 550], [1500, 1100]], ayna=True)
ek("KuzeyBazaltBati", "Aynı bazalt evresi; basamak ve bazalt yaylası", ["guney"],
   [-57, -46, -31, -19], [(40, -22), (64, -10), (64, -26), (52, -36), (40, -36)],
   [(60, -16, -50.5, -29.5), (49, -27, -48.0, -20.0)], [[0, 0], [300, 200], [800, 550], [1500, 1100]])
ek("KavsakYanardagYaylasi", "Üçlü kavşak (30 MYÖ): yarık omzunda volkanik yayla", ["guney"],
   [35, 44, 5, 15], [(42, -26), (60, -26), (60, -46), (42, -46)],
   [(52, -34, 38.5, 10), (52, -42, 38.8, 7)], YAYLA, ayna=True)
ek("IcDenizYarigi", "Üçlü kavşağın başarısız kolu: İç Deniz çevresinde yarık basamakları", ["guney"],
   [26, 40, -16, 4], [(50, -38), (80, -38), (80, -68), (50, -68)],
   [(70, -44, 30.5, 1.5), (64, -54, 30, -6), (59, -63, 34.5, -13)], YAYLA, itme=False)
ek("OrtaColKalkani", "Güney Kalkanı'nın iç kesimi; aşınmış sıralar ve tuz gölleri", ["guney"],
   [118, 146, -32, -17], [(78, -4), (118, -10), (122, -40), (80, -40)],
   [(95, -20, 128, -24), (110, -30, 138, -27)], [[0, 0], [200, 140], [500, 330], [1000, 650], [1500, 1000]])
ek("GuneyTepelik", "Aşınmış eski kıvrımlar, alçak tepelik", ["guney"],
   [64, 84, 45, 53], [(76, -36), (124, -36), (124, -56), (76, -56)],
   [(88, -46, 70, 49.5), (112, -46, 79, 49.5)], [[0, 0], [300, 200], [600, 380], [1200, 800], [1600, 1100]])
ek("DoguSiradaglari", "Eski orojen; edilgen kıyı yükselmesi", ["guney"],
   [141, 154, -40, -22], [(112, -24), (142, -24), (140, -50), (112, -50)],
   [(129, -28, 150.5, -27), (121.5, -44, 147, -37)], ESKI_DAG)
ek("GuneyBasamagi", "Bazalt basamağı (Drakensberg benzeri), kıyıya bakar", ["guney"],
   [24, 33, -34, -23], [(116, -48), (140, -48), (140, -70), (116, -70)],
   [(126, -52, 31, -25), (127, -64, 27, -32)], [[0, 0], [300, 200], [1000, 700], [2000, 1400], [3400, 2300]])
ek("GuneyKutupKalkani", "Güney Kalkanı; buzul aşındırması", ["guney"],
   [-79, -58, 49, 58], [(46, -58), (100, -58), (100, -76), (46, -76)],
   [(60, -66, -72, 53), (88, -66, -62, 53)], KALKAN)
ek("GuneyKiyiDaglari", "Eski yığışım kuşağı, buzul vadili (Altay benzeri)", ["guney"],
   [84, 100, 47, 54], [(96, -56), (136, -56), (136, -76), (96, -76)],
   [(105, -66, 88, 50), (125, -66, 96, 51)], ESKI_DAG)
# ---------------------------------------------------------------- Güneybatı Kıtası
ek("YarikOmzu", "Yarık Boğazı'nın açılması (25 MYÖ'den beri): kanala bakan omuz (Asir benzeri)", ["gb"],
   [39, 48, 12, 22], [(18, -38), (44, -38), (44, -66), (18, -66)],
   [(37, -46, 42.2, 19), (35, -58, 44, 14)], YAYLA, ayna=True)
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
