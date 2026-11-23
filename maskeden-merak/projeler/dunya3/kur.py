"""dunya3 karşılıklarını tarih.md'deki hikâyeden kurar: karsiliklar_taslak.json ve YER_SEKILLERI.md.
Koordinatlar boylam/enlem; hedef noktalar kıyıya çok yakınsa içeri itilir. Sonra: python3 -m mk.denetle projeler/dunya3 oturt
Kullanım (maskeden-merak klasöründen): python3 projeler/dunya3/kur.py"""
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
OVA = [[0, 0], [50, 80], [150, 160], [300, 230], [600, 370], [1000, 580], [1500, 860], [2500, 1300], [9000, 1700]]  # üst uç kapalı: kaynağa dağ girerse yükselmesin
KALKAN = [[0, 0], [200, 150], [500, 320], [1000, 650], [1600, 1000], [9000, 1500]]
ESKI_DAG = [[0, 0], [300, 200], [1000, 700], [2000, 1450], [3000, 2100]]
GENC_DAG = [[0, 0], [300, 200], [1000, 650], [2000, 1300], [3000, 2000], [4500, 2900], [6000, 3700], [7000, 4100]]
DIKIS = [[0, 0], [300, 200], [1000, 700], [2000, 1400], [3500, 2400], [5000, 3300], [6500, 4100], [8800, 5000]]
HAVZA = [[0, 0], [500, 250], [800, 320], [1100, 420], [1500, 700], [2500, 1400], [4000, 2600], [5500, 3200], [7500, 3900]]
HAVZA_DOGU = [[0, 0], [500, 250], [800, 320], [1100, 420], [1500, 700], [2500, 1300], [3500, 1650], [4500, 1850], [6000, 2200]]  # yayla kesilmez; yükseklik eğrisiyle yarıklı ve alçak kalır (kes kenarı düz çizgi bırakıyordu)
TANRI = [[0, 0], [500, 250], [800, 320], [1100, 420], [1500, 700], [2500, 1300], [3500, 1550], [4300, 1300], [5200, 950], [6000, 1750], [7000, 2300]]  # Kunlun ve Tibet yayla yüzeyi (4300 ile 5200 m) aşağı katlanır; yalnız sırtlar yüksek kalır
YAYLA = [[0, 0], [300, 180], [800, 380], [1200, 600], [1800, 1000], [2500, 1600], [3500, 2300], [4500, 2900], [9000, 3300]]

K = []


def ek(ad, olay, parca, kutu, bolge, nokta, egri=None, ayna=False, **e):
    K.append(dict(ad=ad, olay=olay, parca=parca, kutu=kutu, bolge=bolge, nokta=nokta, egri=egri, ayna=ayna, **e))



CEKME = [[0, 0], [300, 200], [800, 520], [1500, 1000], [2500, 1700], [4000, 2700], [6000, 3600]]   # genç ama alçak tutulmuş dağ
# ---------------------------------------------------------------- Batı Kıtası (bati)
ek("KolDaglari", "Batı'nın iki kalkanının çarpışması (320 MYÖ): kol boyunca eski kıvrımlar (Apalaş benzeri)", ["bati"],
   [-88, -72, 33, 43], [(-118, 50), (-98, 50), (-98, 22), (-118, 22)],
   [(-109, 27, -85.5, 34.5), (-108, 44, -76, 41.2)], ESKI_DAG, sira=True)
ek("BatiKuzeyKalkan", "Kuzey kalkanı; buzul aşındırması, göller (Kanada kalkanının kuzeybatısı benzeri)", ["bati"],
   [-125, -98, 57, 68], [(-114, 68), (-66, 68), (-66, 40), (-114, 40)],
   [(-95, 58, -112, 62.5), (-78, 55, -104, 61)], KALKAN)
ek("KuzeyYarikOmzuBati", "Kuzey Yarığı'nın açılması (20 MYÖ'den beri): batı omzu (Baykal benzeri)", ["bati"],
   [101, 114, 49, 58], [(-84, 64), (-64, 64), (-64, 40), (-84, 40)],
   [(-73, 47, 102.5, 51.4), (-71.5, 60, 113, 56.5)], ESKI_DAG, sira=True)
ek("BatiIcKalkanKuzey", "Batı Kalkanı: aşınmış düzlükler ve kum denizi", ["bati"],
   [121, 136, -33, -24], [(-130, 24), (-75, 24), (-72, -5), (-130, -5)],
   [(-115, 5, 128, -28.5), (-95, 8, 132, -29)], KALKAN)
ek("BatiIcKalkanGuney", "Batı Kalkanı'nın güneyi: yaşlı kalkan, demirli sıralar", ["bati"],
   [113, 125, -31, -19], [(-134, -3), (-66, -3), (-66, -25), (-134, -40)],
   [(-115, -15, 118, -25), (-95, -15, 121, -23)], [[0, 0], [200, 150], [500, 320], [1000, 700], [1300, 1000]])
ek("BatiKiyiKuzey", "Büyük Okyanus kıyısı: edilgen kıyı basamağı", ["bati"],
   [25, 34, -33, -23], [(-140, 36), (-122, 36), (-122, 12), (-140, 12)],
   [(-130.5, 32, 31.5, -24), (-130.5, 17, 26.5, -32.5)], ESKI_DAG, ayna=True, sira=True)
ek("BatiKiyiGuney", "Büyük Okyanus kıyısı güneyi: edilgen kıyı basamağı", ["bati"],
   [-50, -39, -27, -19], [(-142, -8), (-120, -8), (-118, -40), (-142, -40)],
   [(-131, -14, -40.5, -20.5), (-128, -32, -49.5, -26.5)], ESKI_DAG, ayna=True, sira=True)
ek("GuneyYarikHavzalari", "Güney kıyısında başarısız yarık kolları (Kenya yarığı benzeri), yanardağlı", ["bati"],
   [33, 40, -4, 3], [(-112, -10), (-84, -10), (-84, -30), (-112, -30)],
   [(-100, -15, 36.3, 0.5), (-94, -24, 36.5, -3)], YAYLA)
ek("KorfezOvasi", "Kol Dağları önünde batan önülke; körfez kıyısı ovası", ["bati"],
   [-96, -84, 29, 37.5], [(-112, 24), (-74, 24), (-72, 2), (-112, 2)],
   [(-95, 14, -90, 33), (-82, 8, -88, 31)], OVA)
ek("BatiDoguKiyi", "Orta Okyanus kıyısı: kumtaşı yaylaları ve kuesta basamakları", ["bati"],
   [-15, -4, 7, 23], [(-84, 8), (-62, 8), (-62, -20), (-84, -20)],
   [(-72, -10, -11, 10.5), (-76, 2, -10, 18)], [[0, 0], [200, 150], [500, 330], [1000, 700], [1500, 1100]])
# ---------------------------------------------------------------- Kuzey Kıtası (kuzey)
ek("KuzeyKalkan", "Kuzey Kalkanı; buzul aşındırması, göl düzlükleri", ["kuzey"],
   [-103, -85, 59, 67], [(-48, 77), (38, 77), (38, 58), (-48, 58)],
   [(-30, 66, -96, 63), (10, 68, -90, 64)], KALKAN)
ek("OrtaSira", "Kuzey'in iki kalkanının çarpışması (400 MYÖ): aşınmış orta sıra (Kafkas dokusu, alçaltılmış)", ["kuzey"],
   [36, 51, 39.5, 45], [(-24, 56), (4, 56), (4, 30), (-24, 30)],
   [(-12, 38, 39.5, 43.6), (-6, 50, 49, 41.3)], [[0, 0], [300, 200], [1000, 650], [2500, 1500], [4000, 2200], [5600, 2700]], sira=True)
ek("KuzeyIcOva", "Kuzey platformu: geniş, alçak tortul ova", ["kuzey"],
   [-63.5, -56, -38, -30], [(-60, 56), (-18, 56), (-18, 24), (-60, 24)],
   [(-35, 40, -61, -34), (-22, 48, -59, -32)], OVA, kutu_sabit=True, oturt={"kutu_pay": 0})
ek("BatiKiyiYarikOmzu", "Kuzey Yarığı'nın doğu omzu (Baykal yarığının kuzeydoğu kolu benzeri)", ["kuzey"],
   [106, 121, 52, 59], [(-66, 64), (-46, 64), (-46, 38), (-66, 38)],
   [(-59.5, 47, 109.5, 54.3), (-57.5, 56, 117.5, 56.8)], ESKI_DAG, sira=True)
ek("DoguKiyiDaglari", "Doğu Okyanusu açılırken ters dönen eski yarık havzası dağları (Atlas benzeri)", ["kuzey"],
   [-10, 5, 28, 36], [(10, 74), (38, 74), (38, 36), (10, 36)],
   [(21, 44, -8, 31), (26, 61, 3, 34.5)], GENC_DAG, sira=True)
ek("GuneyKivrimKusagi", "Orta Kıta'nın Kuzey'e yaklaşması: genç kıvrım yayı (Karpat benzeri)", ["kuzey"],
   [15, 29, 43, 51], [(-42, 26), (-6, 26), (-6, 10), (-42, 10)],
   [(-32, 17.5, 18, 49), (-24, 18, 24, 48), (-17, 16.5, 25, 45.5)], CEKME, ayna=True, sira=True)
ek("GuneyBatiOva", "Kuzey'in güneybatısı: alçak, düz kuru ova", ["kuzey"],
   [-65, -56, -27, -18], [(-64, 32), (-36, 32), (-36, 10), (-64, 10)],
   [(-50, 22, -61, -23), (-40, 25, -59, -22)], OVA)
ek("GuneyDoguYayla", "Kuzey'in güneydoğusu: yatay katmanlı yayla, kanyonlar", ["kuzey"],
   [-115, -105, 33, 40.5], [(-8, 42), (28, 42), (28, 8), (-8, 8)],
   [(5, 25, -111, 37), (15, 32, -109, 38)], [[0, 0], [1000, 250], [1500, 500], [2000, 800], [2500, 1150], [3500, 1800]])
# ---------------------------------------------------------------- Orta Kıta (orta)
ek("OrtaKalkan", "Orta Kıta: batıda kalkan, doğuda tortul örtü; kuzeyi Kuzey'e dalan önülke (Arabistan benzeri)", ["orta"],
   [34, 58, 14, 32], [(-38, 12), (-2, 12), (-2, -26), (-38, -26)],
   [(-21, -6, 45, 23), (-22, 6, 48.5, 27.5), (-25, -16, 42, 18)], YAYLA)
# ---------------------------------------------------------------- Güney Kıtası (guney)
ek("GuneyMeseta", "Güney Kıtası: bazalt mesetaları, rüzgâr aşındırması", ["guney"],
   [-72, -64, -51, -41], [(-74, -38), (-40, -38), (-40, -58), (-74, -58)],
   [(-58, -47, -68, -46), (-45, -50, -67, -48.5)], [[0, 0], [300, 200], [800, 500], [1500, 900], [2500, 1500]])
ek("GuneyBuzulDaglari", "Kutup yakınında eski yığışım kuşağı, buzul vadili (Doğu Sayan benzeri)", ["guney"],
   [92, 104, 49, 55.5], [(-56, -52), (-22, -52), (-22, -70), (-56, -70)],
   [(-42, -60, 98, 52.5), (-32, -56, 101, 52)], ESKI_DAG)
ek("GuneyKuzeyKiyi", "Orta Kıta'dan kopma (80 MYÖ): kopma kenarında yükselmiş yaylalar (Zimbabve doğu yaylaları benzeri)", ["guney"],
   [27, 37, -23, -14], [(-48, -26), (-20, -26), (-20, -48), (-48, -48)],
   [(-30, -35, 32.8, -19), (-38, -42, 31, -20.5)], YAYLA)
# ---------------------------------------------------------------- Doğu Kıtası (dogu)
ek("BatiKalkanKuzeyD", "Doğu Kıtası'nın batı kalkanı: kumtaşı yaylaları ve çöl havzası", ["dogu"],
   [15, 27, 11, 20], [(44, 32), (85, 32), (85, 0), (44, 0)],
   [(60, 15, 21, 16.5), (75, 20, 23, 17.5)], [[0, 0], [300, 200], [600, 380], [1000, 650], [1500, 1000]])
ek("BatiKalkanGuneyD", "Doğu Kıtası'nın batı kalkanı güneyi: kuru havza ve kenar yaylaları", ["dogu"],
   [14, 28, -29, -16], [(35, 2), (85, 2), (85, -42), (40, -42)],
   [(55, -15, 20, -22), (70, -25, 24, -24)], [[0, 0], [300, 200], [800, 480], [1200, 750], [2500, 1600]])
ek("GuneyBatiKiyiD", "Doğu Okyanusu kıyısında eski kıvrım kuşağı (Kap kıvrımları benzeri)", ["dogu"],
   [17, 28, -35, -31.5], [(34, -24), (62, -24), (62, -46), (34, -46)],
   [(42, -31, 18.5, -33.0), (48, -35.5, 23, -33.6), (54, -38, 27.5, -33.6)], ESKI_DAG, sira=True)
ek("BoynuzKuzey", "Boynuz: eklenmiş yay parçalarının kıvrım kuşağı (Çerski benzeri)", ["dogu"],
   [136, 156, 60, 70], [(80, 75), (112, 75), (112, 50), (80, 50)],
   [(98, 70, 141, 66), (97, 56, 151, 63.5)], ESKI_DAG)
ek("BoynuzGuney", "Boynuzun güneyi: havza ve sıra (Transbaykal benzeri)", ["dogu"],
   [106, 131, 48, 59], [(76, 54), (104, 54), (104, 28), (76, 28)],
   [(90, 48, 112, 52), (91, 34, 122, 55)], ESKI_DAG)
ek("KavusmaDaglari", "Kuzeydoğu parçasının ana kıtaya çarpması (30 MYÖ'den beri): kıvrım kuşağı (Zagros dokusu, aynalı)", ["dogu"],
   [44, 60, 25, 37], [(98, 24), (128, 20), (128, 2), (98, 6)],
   [(105, 13, 45.5, 35.5), (113, 11, 50.5, 31.5), (121, 8.5, 55.5, 28.8)], GENC_DAG, ayna=True, sira=True, oncelik=1.5)
ek("KuzeydoguYay", "Büyük Okyanus'un dalması: kuzeydoğu kıyısında yanardağ sırası (Barisan benzeri)", ["dogu"],
   [94, 107, -7, 7], [(137, 44), (147, 44), (147, 12), (137, 12)],
   [(139, 38, 96.5, 4.5), (141, 16, 104, -4.5)], GENC_DAG, ayna=True, sira=True)
ek("KuzeydoguIc", "Kuzeydoğu parçasının içi: yay ardı ovası ve sıralar (Mançurya benzeri)", ["dogu"],
   [117, 131, 41, 51], [(108, 46), (136, 46), (136, 12), (108, 16)],
   [(122, 30, 124, 46), (130, 22, 127, 44.5)], OVA)
ek("OrtaKalkanDogu", "Ana kalkanın ortası: masa yaylaları", ["dogu"],
   [-63, -51, -17, -9], [(78, 30), (116, 30), (116, -16), (78, -16)],
   [(90, 10, -57, -13), (100, -5, -55, -14)], [[0, 0], [300, 200], [600, 350], [1000, 600], [1500, 950]])
ek("OrtaKalkanGuneyD", "Ana kalkanın güneyi: yatay katmanlar, dolerit masaları (Karoo benzeri)", ["dogu"],
   [19, 29, -34, -28], [(78, -14), (120, -14), (120, -46), (78, -46)],
   [(95, -28, 23, -31), (108, -32, 26, -31.5)], [[0, 0], [500, 220], [1000, 450], [1500, 800], [2500, 1500]])
ek("DoguIcHavza", "Dalma ardında kırık önülke: sıralar ve tuzlu havzalar", ["dogu"],
   [-67.3, -61, -34, -26], [(112, -18), (150, -18), (150, -48), (112, -48)],
   [(128, -28, -65.5, -30), (140, -36, -64, -32)], YAYLA, kutu_sabit=True, oturt={"kutu_pay": 0})
ek("GuneyDoguAnd", "Büyük Okyanus'un dalması: güneydoğu kıyısında And benzeri sıra", ["dogu"],
   [-81, -68, -17, -3], [(146, -6), (166, -6), (160, -48), (142, -48)],
   [(159, -12, -79.5, -5), (159, -25, -75.5, -11), (152, -38, -70, -16)], GENC_DAG, ayna=True, sira=True)
ek("GuneyKutupBati", "Kutup yakınında eski kubbe yaylası (Hangay benzeri)", ["dogu"],
   [94, 105, 44, 51], [(86, -42), (118, -42), (118, -70), (86, -70)],
   [(102, -55, 99, 47.5), (110, -62, 101.5, 47)], ESKI_DAG)
ek("GuneyKutupDogu", "Kutup yakınında buzul aşındırmalı kalkan (Västerbotten benzeri)", ["dogu"],
   [13, 23, 62, 67], [(114, -44), (152, -44), (152, -64), (114, -64)],
   [(125, -52, 18, 64.5), (140, -50, 20.5, 64.5)], KALKAN)
# ---------------------------------------------------------------- adalar
ADA_EGRI = [[0, 0], [500, 350], [1500, 1050], [2500, 1700], [4200, 2500]]
for ad, parca, (tlo, tla, tgen_lo, tgen_la), (kaynak, slo, sla, skm, kutu), aci, olay in [
        ("AdaKuzeybati", "adaKB", (-144.5, 36.9, 9.6, 9.2), ("İzlanda", -18.6, 64.9, 380, [-25, -13, 63, 67]), 120,
         "Büyük Okyanus'ta sıcak nokta adası"),
        ("AdaGuneydogu", "adaGD", (160.8, -65.5, 22.4, 13.9), ("Baffin", -71.0, 68.5, 900, [-82, -60, 63, 74]), 70,
         "Kutup bölgesinde kopmuş kalkan parçası, buzul dağlı"),
        ("AdaOrtaOkyanus", "adaOrta", (4.4, -42.0, 2.7, 4.8), ("Sicilya", 14.2, 37.6, 230, [12.2, 15.8, 36.5, 38.4]), 200,
         "Orta Okyanus sırtına yakın sıcak nokta")]:
    tkm = max(tgen_lo * np.cos(np.radians(tla)), tgen_la) * 111 * 0.9
    olc = tkm / (skm * 0.85)   # adalar: kaynak ada küçükse 2 katı aşabilir (istisna, KARARLAR.md)
    r = 0.25 * tgen_la; ar = np.radians(aci); dkm = r * 111 / olc
    s2 = (slo + dkm * np.sin(ar) / (111.32 * np.cos(np.radians(sla))), sla + dkm * np.cos(ar) / 110.6)
    ek(ad, olay + f" ({kaynak})", [parca], kutu,
       [(tlo - tgen_lo / 2 - 1, tla + tgen_la / 2 + 1), (tlo + tgen_lo / 2 + 1, tla + tgen_la / 2 + 1),
        (tlo + tgen_lo / 2 + 1, tla - tgen_la / 2 - 1), (tlo - tgen_lo / 2 - 1, tla - tgen_la / 2 - 1)],
       [(tlo, tla, slo, sla), (tlo, tla + r, round(s2[0], 4), round(s2[1], 4))], ADA_EGRI, itme=False, oturt=False, yumusak_km=30)

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
    if ol > OLCEK_UST and not k.get("sira") and not k["ad"].startswith("Ada"):
        nk = kaynak_donustur(nk, 0, ol / OLCEK_UST)
    t1, dy1, ol1 = yon_olcek(P, nk, k["ayna"])
    uyari = ("  YÖN İHLALİ" if dy1 < YON_ALT - 0.5 else "") + ("  ÖLÇEK" if ol1 > OLCEK_UST + 0.05 else "")
    print(f"{k['ad']:<24} dönme {t0:+6.1f} → {t1:+6.1f}  sapma {dy:4.1f} → {dy1:4.1f}  büyütme {ol:4.2f} → {ol1:4.2f}{uyari}")
    xs2 = [q[2] for q in nk]; ys2 = [q[3] for q in nk]
    # kaynak kutusu, hedef bölgenin kaynaktaki karşılığını kapsasın (kutu dışı deniz sayılır)
    blo = [q[0] for q in k["bolge"]]; bla = [q[1] for q in k["bolge"]]
    gkm = max((max(blo) - min(blo)) * np.cos(np.radians(np.mean(bla))), max(bla) - min(bla)) * 111 / ol1
    yd = gkm / 111 * 0.6; cx, cy = np.mean(xs2), np.mean(ys2); xd = yd / max(np.cos(np.radians(cy)), 0.2)
    # ama seçilen kaynak alanından en çok 3° taşar: daha geniş kutu istenmeyen yer şekillerini (başka sıradağlar) içeri alır
    k0 = k["kutu"] if not k.get("kutu_sabit") else None
    if k0 is not None:
      k["kutu"] = [round(max(k0[0] - 3, min(k0[0], min(xs2) - 1, cx - xd)), 2), round(min(k0[1] + 3, max(k0[1], max(xs2) + 1, cx + xd)), 2),
                   round(max(-84, k0[2] - 3, min(k0[2], min(ys2) - 1, cy - yd)), 2), round(min(84, k0[3] + 3, max(k0[3], max(ys2) + 1, cy + yd)), 2)]
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
