"""Dünya karşılıklarıyla topografya: her bölgeye gerçek bir yükseklik modelinden (AWS Terrain Tiles) bir parça,
döndürülüp ölçeklenip bükülerek (ince levha eğrisi) yerleştirilir; kıyı sahibin maskesidir.

Bir karşılık: kaynak kutusu, denetim noktaları (hedef görüntü pikseli ↔ kaynak boylam enlem), hedef bölge çokgeni,
hangi parçalara uygulandığı, yükseklik çarpanı ve kaynağa göre adlandırılan yer şekilleri.

Kullanım: python3 benzer.py onizle [AD ...] | bilesik | ciz
"""
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.interpolate import RBFInterpolator

import dem
import olaylar as O

T0 = time.time()
CIKTI = "cikti"
ONIZ = "/tmp/claude-0/-home-user-Tectonic/1cb340b3-df7d-519b-96f4-5170b8cfb37a/scratchpad"
YAZI = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def log(s):
    print(f"[{time.time() - T0:6.0f} s] {s}", flush=True)


# Parça numaraları: animasyon.parcalar() sırası 1..7 (sahibin numaraları); "serit" 2'ye katılır
KARSILIK = [
    {   # 1: İskandinav dağları batı kıyısında (Ulu Dağlar), Fin kalkanı göllü kuzey, Urallar doğu sınırda (Mavi Dağlar)
        "ad": "Avrupa", "kutu": (-4, 84, 42, 72), "parca": {"1", "2"},
        "etiket": [("ULU DAĞLAR", 13.5, 63.0, 16), ("MAVİ DAĞLAR", 59.5, 61.5, 16), ("Ak Kalkan", 30.5, 64.0, 16)],
        "nokta": [(105, 470, 7.0, 58.0), (190, 105, 25.8, 71.1), (800, 110, 59.2, 65.0), (808, 520, 58.3, 54.2)],
        "bolge": [(0, 0), (1100, 0), (1100, 470), (1000, 600), (860, 620), (600, 720), (560, 960), (400, 880), (260, 880), (170, 795), (90, 775), (0, 725)],
    },
    {   # 2'nin kuzeyi ve ortası: Orta Sibirya; Putorana = Kuzey Tuzakları, Baykal = Derin Göl, Sayanlar = Uzak Sıra
        "ad": "Sibirya", "kutu": (60, 140, 44, 78), "parca": {"2", "serit"},
        "etiket": [("Derin Göl", 110.6, 54.6, 15), ("UZAK SIRA", 96.5, 52.6, 17), ("Boz Kalkan", 110.0, 64.0, 16)],
        "nokta": [(1250, 150, 93.0, 69.0), (1680, 240, 106.5, 53.0)],
        "gol": [("Derin Göl", [(103.7, 51.5), (104.9, 51.5), (106.2, 52.1), (107.4, 52.8), (108.6, 53.4), (109.5, 54.4), (110.0, 55.7),
                               (109.4, 55.9), (108.5, 54.9), (107.3, 53.9), (106.3, 53.3), (105.2, 52.6), (104.1, 51.9)])],
        "bolge": [(1550, 0), (2000, 0), (2000, 560), (1780, 450), (1700, 150)],
    },
    {   # 2'nin ortası ve Mor çizgisi tek parça: Kunlun = Mor Sıradağları, Tarım = Tuzak Çanağı (sahibin bozkır platosu),
        # Tanrı Dağları = Çanak Sıraları, Cungarya ve Altay kuzeyde. Tibet dahil değil: Mor'un güneyi 3'tür (Hindistan karşılığı).
        # Yükseklik eğrisi: çanak tabanı 800 ile 1000 m, Mor doruğu 6 km dolayı.
        "ad": "Tarım", "kutu": (66, 104, 33, 52), "parca": {"2", "3", "serit"}, "yumusak_km": 110, "ayna": True, "bukme_kat": 2.5,
        "yukseklik_egri": [(0, 0), (1300, 1000), (3500, 2600), (8000, 6000)],
        "etiket": [("Tuzak Çanağı", 83.0, 39.4, 18), ("ÇANAK SIRALARI", 84.5, 42.6, 14)],
        "nokta": [(1720, 670, 77.0, 36.6), (1500, 612, 84.0, 36.0), (1300, 565, 90.0, 36.0), (1100, 595, 96.0, 35.6),
                  (1350, 230, 84.0, 42.8)],
        "bolge": [(1010, 60), (1550, 40), (1700, 150), (1780, 450), (2000, 560), (2000, 700), (1720, 640), (1500, 580), (1300, 530),
                  (1120, 540), (1060, 520), (1020, 450)],
    },
    {   # Mor Sıradağları: yalnız dar sıra şeridi; karşılığı aynalanmış Himalaya'nın ön kuşağı (arkasındaki yayla dahil değil),
        # yükseklik 6 km dolayına ölçekli. Çanak bölgesinin üstüne baskın yazılır.
        "ad": "Mor", "kutu": (62, 100, 24, 40), "parca": {"2", "3", "serit"}, "ayna": True, "oncelik": 3.0, "yumusak_km": 45,
        "yukseklik_egri": [(0, 0), (1000, 900), (4000, 3300), (8800, 6300)],
        "etiket": [("MOR SIRADAĞLARI", 86.5, 28.6, 19)],
        "nokta": [(1110, 595, 95.0, 29.6), (1300, 565, 88.1, 27.8), (1500, 614, 83.5, 28.7), (1620, 645, 79.6, 30.9),
                  (1715, 674, 74.6, 35.2)],
        "bolge": [(1080, 575), (1150, 525), (1300, 527), (1500, 578), (1715, 638), (1900, 668), (1900, 760), (1715, 735),
                  (1500, 675), (1300, 628), (1150, 628), (1060, 660)],
    },
    {   # 3: Ganj ovası = Mor Ön Ovası, Dekkan = Kızıl Basamaklar, Batı Gatlar = kanal omzu
        "ad": "Hindistan", "kutu": (62, 95, 3, 32), "parca": {"3"},
        "etiket": [("Kızıl Basamaklar", 76.5, 19.0, 17)],
        "benzerlik": (1220, 950, 77.0, 18.0, 18.0, 1.55, False),
        "bolge": [(1000, 620), (1200, 610), (1500, 660), (1750, 720), (1560, 790), (1480, 1000), (1420, 1200), (1360, 1460), (1100, 1360), (980, 1100)],
    },
    {   # 3'ün doğu kıyısı: Sumatra ve Cava yayı (aynalı) = Doğu Yay Dağları ve güneydoğu yarımadası
        "ad": "Sumatra", "kutu": (92, 117, -11, 9), "parca": {"3"}, "ayna": True,
        "etiket": [("DOĞU YAY DAĞLARI", 101.0, -1.5, 14)],
        "nokta": [(1600, 785, 95.3, 5.6), (1515, 965, 100.35, -0.95), (1570, 985, 99.0, -2.2), (1420, 940, 101.6, 0.6),
                  (1500, 1075, 102.3, -3.8), (1515, 1150, 105.7, -5.9), (1475, 1280, 110.4, -7.8), (1440, 1385, 113.8, -8.0)],
        "bolge": [(1600, 730), (1720, 730), (1650, 900), (1580, 1100), (1600, 1300), (1520, 1450), (1350, 1450), (1410, 1300),
                  (1450, 1150), (1470, 1000), (1520, 850)],
    },
    {   # 4'ün kuzeybatısı: İberya (aynalı); Pireneler köprüde = Köprü Dağları, Meseta = Köz Yaylası
        "ad": "İberya", "kutu": (-12, 6, 34, 46), "parca": {"1", "4"},
        "etiket": [("KÖPRÜ DAĞLARI", 0.5, 42.7, 15), ("Köz Yaylası", -3.6, 40.0, 16)],
        "benzerlik": (230, 980, -3.7, 40.4, -30.0, 1.75, True),
        "bolge": [(0, 725), (90, 775), (170, 795), (260, 880), (420, 880), (500, 960), (480, 1150), (300, 1180), (0, 1160)],
    },
    {   # 4'ün güneyi: Fransa (kuzey güney aynalı): Bretanya'nın girintili kıyısı güneybatıda, Masif Santral içeride
        "ad": "Fransa", "kutu": (-6, 5.0, 42.6, 51.5), "parca": {"4"},
        "etiket": [("Köz Masifleri", 2.8, 45.3, 15)],
        "benzerlik": (300, 1310, 2.5, 46.5, 180.0, 1.8, True),
        "bolge": [(0, 1160), (300, 1180), (480, 1150), (560, 1250), (680, 1330), (700, 1530), (0, 1530)],
    },
    {   # 4'ün doğusu ve 5: Zagros = Sarı Sıradağları, Mezopotamya ve Basra = Sarı Ön Havzası, Orta İran = 4'ün doğu yaylası
        "ad": "İran", "kutu": (32, 66, 16, 42), "parca": {"4", "5"},
        "etiket": [("SARI SIRADAĞLARI", 51.5, 30.6, 15), ("Sarı Ön Havzası", 48.5, 29.0, 14), ("Tuz Çölü", 54.5, 34.3, 14)],
        "nokta": [(748, 1370, 45.5, 35.6), (730, 1180, 51.4, 30.9), (785, 975, 56.3, 27.4)],
        "bolge": [(500, 900), (620, 940), (820, 920), (900, 960), (960, 1060), (920, 1120), (900, 1300), (760, 1430), (640, 1400), (560, 1250), (500, 1100)],
    },
    {   # 6: Ege; Yunanistan ve Batı Anadolu, yay ardı gerilmesinin parmak yarımadaları
        "ad": "Ege", "kutu": (17, 32, 33, 44), "parca": {"6"},
        "etiket": [],
        "nokta": [(630, 770, 21.2, 39.8), (740, 715, 24.5, 41.4), (880, 820, 28.3, 38.2), (640, 900, 22.4, 36.9)],
        "bolge": [(540, 640), (950, 640), (960, 1000), (540, 1000)],
    },
    {   # 7: Aşağı Kaliforniya; kanal = Kaliforniya Körfezi, yanal fay boyunca kuzeybatıya kayan yarımada
        "ad": "Baja", "kutu": (-119, -107, 21, 35), "parca": {"7", "5"},
        "etiket": [("Uzun Yarımada Sırtı", -114.5, 29.0, 13)],
        "nokta": [(905, 1140, -116.9, 32.4), (1175, 1285, -109.9, 22.9), (1040, 1190, -113.3, 27.8), (1060, 1240, -113.8, 26.6)],
        "bolge": [(870, 1100), (960, 1100), (1210, 1250), (1210, 1320), (1100, 1330), (880, 1320), (860, 1200)],
    },
]


# ------------------------------------------------------------------ eşleme
def _benzerlik(k):
    """Hedef px → kaynak (boylam, enlem) benzerlik dönüşümü: (tx, ty, boylam, enlem, açı°, ölçek, ayna).
    Açı: kaynak saat yönünün tersine döndürülerek hedefe konur; ölçek: hedef km / kaynak km; ayna: doğu batı."""
    if "benzerlik" in k:
        tx, ty, lo0, la0, aci, olc, ayna = k["benzerlik"]
    else:  # denetim noktalarından en küçük kareler
        n = np.array(k["nokta"], float)
        lo0, la0 = n[:, 2].mean(), n[:, 3].mean(); tx, ty = n[:, 0].mean(), n[:, 1].mean()
        ayna = k.get("ayna", False)
        X = (n[:, 2] - lo0) * 111.32 * np.cos(np.radians(la0)) * (-1 if ayna else 1); Y = (n[:, 3] - la0) * 110.6
        u = (n[:, 0] - tx) * O.KM_PX; v = -(n[:, 1] - ty) * O.KM_PX
        zs = X + 1j * Y; zt = u + 1j * v
        c = (np.conj(zs) @ zt) / (np.conj(zs) @ zs)
        aci, olc = np.degrees(np.angle(c)), abs(c)
    r = np.radians(aci); cl = np.cos(np.radians(la0))
    def f(xy):
        u = (xy[:, 0] - tx) * O.KM_PX / olc; v = -(xy[:, 1] - ty) * O.KM_PX / olc
        X = u * np.cos(-r) - v * np.sin(-r); Y = u * np.sin(-r) + v * np.cos(-r)
        if ayna:
            X = -X
        return np.stack([lo0 + X / (111.32 * cl), la0 + Y / 110.6], 1)
    return f, (aci, olc)


def esleme(k):
    """Hedef görüntü pikseli (x, y) → kaynak (boylam, enlem): benzerlik dönüşümü + denetim noktalarında ince levha bükmesi.
    Bölgenin çevresine benzerlikten çapa noktaları konur; böylece bükme yerel kalır."""
    f, _ = _benzerlik(k)
    xs = [p[0] for p in k["bolge"]]; ys = [p[1] for p in k["bolge"]]
    x0, x1, y0, y1 = min(xs) - 400, max(xs) + 400, min(ys) - 400, max(ys) + 400
    capa = np.array([(x, y) for x in np.linspace(x0, x1, 5) for y in np.linspace(y0, y1, 5)
                     if x in (x0, x1) or y in (y0, y1)], float)
    n = np.array(k.get("nokta", []), float).reshape(-1, 4)
    hed = np.vstack([capa, n[:, :2]]); kay = np.vstack([f(capa), n[:, 2:]])
    ileri = RBFInterpolator(hed, kay, kernel="thin_plate_spline", degree=1, smoothing=k.get("puruz", 0.0))
    geri = RBFInterpolator(kay, hed, kernel="thin_plate_spline", degree=1)
    return ileri, geri


def parca_etiket(ny, nx):
    import animasyon as A
    lab, adlar = A.parcalar()
    lab = np.asarray(Image.fromarray(lab.astype(np.uint8)).resize((nx, ny), Image.NEAREST))
    return lab, adlar


def agirlik(k, lab, adlar, ny, nx, s):
    """Bölge çokgeni ∩ izinli parçalar; yumuşatılmış; parça dışına taşma kesilir."""
    im = Image.new("L", (nx, ny), 0)
    ImageDraw.Draw(im).polygon([(x * s, y * s) for x, y in k["bolge"]], fill=255)
    p = np.asarray(im) > 0
    izin = np.isin(lab, [adlar.index(a) + 1 for a in k["parca"]])
    sig = k.get("yumusak_km", 80) / (O.KM_PX / s)
    w = ndimage.gaussian_filter((p & izin).astype(np.float32), sig)
    # suyu aşmadan, yalnız kara üzerinden genişletilmiş izin: kara sınırlarında yumuşak geçiş, boğaz ötesine taşma yok
    kara = lab > 0
    izin_g = ndimage.binary_dilation(izin, iterations=int(2 * sig), mask=kara)
    w *= ndimage.gaussian_filter(izin_g.astype(np.float32), 2.0)
    return w


def ornekle(k, ny, nx, s, maske_w, kaynaklar, bukme=None):
    """Ağırlığı sıfır olmayan hücrelerde kaynak yüksekliği; parçalı değerlendirme. bukme: (WX, WY) görüntü pikseli."""
    ileri, _ = esleme(k)
    if k["ad"] not in kaynaklar:
        kaynaklar[k["ad"]] = dem.Kaynak(*k["kutu"], z=k.get("z", 6)).doldur(kutu=k["kutu"], kes=k.get("kes"))
    K = kaynaklar[k["ad"]]
    out = np.zeros((ny, nx), np.float32); deniz = np.zeros((ny, nx), np.float32)
    ii, jj = np.nonzero(maske_w > 1e-3)
    for a in range(0, len(ii), 400000):
        i, j = ii[a:a + 400000], jj[a:a + 400000]
        x, y = j / s, i / s
        if bukme is not None:
            kb = k.get("bukme_kat", 1.0)
            x = x + kb * bukme[0][i, j]; y = y + kb * bukme[1][i, j]
        ll = ileri(np.stack([x, y], 1))
        h = K.ornek(ll[:, 0], ll[:, 1]) * k.get("carpan", 1.0)
        if k.get("yukseklik_egri"):
            e = np.array(k["yukseklik_egri"], float)
            h = np.interp(h, e[:, 0], e[:, 1])
        out[i, j] = h
        deniz[i, j] = K.deniz_ornek(ll[:, 0], ll[:, 1])
        if k.get("gol"):
            if not hasattr(K, "golm"):
                K.golm = np.zeros(K.h.shape, np.float32)
                for ad, cokgen in k["gol"]:
                    px, py = dem.merc(np.array([p[0] for p in cokgen]), np.array([p[1] for p in cokgen]), K.z)
                    im = Image.new("L", (K.h.shape[1], K.h.shape[0]), 0)
                    ImageDraw.Draw(im).polygon(list(zip(px - K.tx0 * 256, py - K.ty0 * 256)), fill=1)
                    K.golm = np.maximum(K.golm, np.asarray(im, np.float32))
            px, py = dem.merc(ll[:, 0], ll[:, 1], K.z)
            GOL[i, j] = np.maximum(GOL[i, j], ndimage.map_coordinates(K.golm, [py - K.ty0 * 256, px - K.tx0 * 256], order=1))
    return out, deniz



# ------------------------------------------------------------------ tasarlanan bölge
# 2'nin ortası ve Mor kuşağı: büyük şekil elle tasarlanır (kopya olmasın), gerçek veriden yalnız küçük ölçekli doku alınır
# (Tarım karşılığının 25 km'den küçük sırt ve vadileri). Görüntü pikseli; yükseklik m.
TASARIM = {
    "etkin": False,  # denendi, kenar sıraları yapay kaldı; yerine aynalı ve güçlü bükülmüş Tarım karşılığı
    "alan": [(900, 40), (1560, 20), (1730, 250), (1800, 480), (2000, 560), (2000, 770), (1760, 745), (1500, 705), (1080, 668),
             (960, 610), (900, 400)],
    "taban": ([(1000, 330), (1040, 200), (1110, 150), (1210, 130), (1340, 135), (1430, 205), (1470, 300), (1500, 420),
               (1420, 480), (1250, 470), (1100, 470), (1010, 430)], (1000, 820)),   # çanak tabanı: batıda 1000, doğuda 820
    "siralar": [
        # ad, çizgi, köşe yükseklikleri, yarı genişlik km (kuzey/batı yanı, güney/doğu yanı)
        ("Çanak Sıraları", [(985, 340), (1015, 190), (1090, 110), (1210, 82), (1350, 88), (1460, 160), (1515, 280)],
         [1800, 2700, 3300, 3600, 3400, 3000, 2600], (85, 70)),
        ("Doğu Kolu", [(1515, 280), (1555, 400), (1600, 520), (1640, 630)], [2600, 2900, 3500, 4600], (75, 75)),
        ("Batı Kolu", [(985, 340), (975, 450), (1010, 560), (1080, 610)], [1800, 1600, 2200, 3600], (45, 45)),
        ("Mor Sıradağları", [(1075, 615), (1150, 562), (1300, 562), (1500, 614), (1715, 674), (1870, 700)],
         [3600, 4600, 5200, 5600, 4900, 3200], (115, 75)),
        ("Şerit Sırtları", [(1180, 510), (1350, 505), (1520, 545), (1640, 590)], [1700, 2000, 2300, 2600], (40, 40)),
    ],
    # doku kaynağı: engebeli bir iç yayla (aynalı Tibet içi); yalnız 25 km'den küçük sırt ve vadileri kullanılır
    "doku": {"ad": "doku", "kutu": (76, 102, 28, 38), "benzerlik": (1400, 380, 89.0, 33.0, 0.0, 1.0, True), "bolge": [(0, 0)]},
    "etiket": [("MOR SIRADAĞLARI", (1330, 590), 19), ("Tuzak Çanağı", (1230, 300), 18), ("ÇANAK SIRALARI", (1150, 70), 14),
               ("Şerit Yaylası", (1360, 488), 14)],
}


def tasarla(z, kara, s, doku):
    """Tasarlanan bölgeyi bileşiğe işler. doku: aynı ızgarada Tarım karşılığından örneklenen yükseklik (yalnız ayrıntısı alınır)."""
    ny, nx = z.shape
    hk = O.KM_PX / s
    r = np.random.default_rng(77)
    def gur(km, kok):
        g = ndimage.gaussian_filter(np.random.default_rng(kok).standard_normal((ny // 4, nx // 4)), km / hk / 4, mode="wrap")
        return ndimage.zoom(g / g.std(), (ny / g.shape[0], nx / g.shape[1]), order=1)[:ny, :nx]
    II, JJ = np.indices((ny, nx), dtype=np.float32)
    # çizgiler düz durmasın: alan bükmesi (yaklaşık ±45 km)
    bx = (gur(400, 1) * 9 + gur(120, 2) * 3) * s; by = (gur(400, 3) * 9 + gur(120, 4) * 3) * s
    def cokgen_al(p, sig_km):
        im = Image.new("F", (nx, ny), 0.0)
        ImageDraw.Draw(im).polygon([(x * s, y * s) for x, y in p], fill=1.0)
        a = ndimage.map_coordinates(np.asarray(im), [II + by, JJ + bx], order=1)
        return ndimage.gaussian_filter(a, sig_km / hk)
    W = cokgen_al(TASARIM["alan"], 60) * kara
    # arka plan: bileşiğin çok yumuşatılmışı
    makro = ndimage.gaussian_filter(np.where(kara, z, 0.0), 120 / hk)
    tp, (h0, h1) = TASARIM["taban"]
    tb = cokgen_al(tp, 70)
    xs = np.array([p[0] for p in tp]); egim = h0 + (h1 - h0) * np.clip((JJ / s - xs.min()) / (xs.max() - xs.min()), 0, 1)
    makro = makro * (1 - tb) + egim * tb
    from scipy.spatial import cKDTree
    sirt = np.zeros((ny, nx), np.float32)
    for ad, c, hs, (wk, wg) in TASARIM["siralar"]:
        c = np.array(c, float)
        pts, val, nrm = [], [], []
        for i in range(len(c) - 1):
            n = max(2, int(np.hypot(*(c[i + 1] - c[i])) * s / 2))
            t = np.linspace(0, 1, n, endpoint=False)
            pts.append(c[i] + (c[i + 1] - c[i]) * t[:, None]); val.append(hs[i] + (hs[i + 1] - hs[i]) * t)
            d = (c[i + 1] - c[i]) / np.hypot(*(c[i + 1] - c[i])); nrm.append(np.repeat([[-d[1], d[0]]], n, 0))
        pts = np.vstack(pts) * s; val = np.concatenate(val); nrm = np.vstack(nrm)
        # yalnız çevresinde hesapla
        x0, y0 = pts.min(0) - 250 * s / O.KM_PX * 4; x1, y1 = pts.max(0) + 250 * s / O.KM_PX * 4
        r0, r1 = int(max(y0, 0)), int(min(y1, ny)); c0, c1 = int(max(x0, 0)), int(min(x1, nx))
        qy = II[r0:r1, c0:c1] + by[r0:r1, c0:c1]; qx = JJ[r0:r1, c0:c1] + bx[r0:r1, c0:c1]
        dist, idx = cKDTree(pts).query(np.stack([qx.ravel(), qy.ravel()], 1))
        dist = dist.reshape(qx.shape) * hk
        yan = ((qx.ravel() - pts[idx, 0]) * nrm[idx, 0] + (qy.ravel() - pts[idx, 1]) * nrm[idx, 1]).reshape(qx.shape)
        w = np.where(yan < 0, wk, wg)   # çizgi yönünün solu (kuzey ya da batı) ile sağı ayrı genişlikte
        H = val[idx].reshape(qx.shape) * (0.85 + 0.15 * gur(60, 9)[r0:r1, c0:c1])
        prof = H * np.exp(-(dist / w) ** 2)
        sirt[r0:r1, c0:c1] = np.maximum(sirt[r0:r1, c0:c1], prof)
    makro = np.maximum(makro, sirt)
    # doku: Tarım karşılığının küçük ölçekli kısmı, yerel yüksekliğe göre genlik
    ince = doku - ndimage.gaussian_filter(doku, 22 / hk)
    ince = np.clip(ince / (ndimage.gaussian_filter(np.abs(ince), 60 / hk) + 30), -2.2, 2.2)  # birim genliğe yakın
    genlik = 50 + 380 * np.clip((makro - 900) / 2500, 0, 1.3)
    yeni = makro + ince * genlik
    return np.where(kara, z * (1 - W) + np.maximum(yeni, 5) * W, z)


GOL = None


def bilesik():
    """Tam çözünürlükte (maske boyutu, 2,1 km) karşılıkların ağırlıklı birleşimi."""
    global GOL
    kara = np.asarray(Image.open("maske.png").convert("L")) > 127
    ny, nx = kara.shape; s = nx / O.GEN
    GOL = np.zeros((ny, nx), np.float32)
    lab, adlar = parca_etiket(ny, nx)
    r = np.random.default_rng(14)
    def gur(km):
        g = ndimage.gaussian_filter(r.standard_normal((ny // 4, nx // 4)), km / (O.KM_PX / s) / 4, mode="wrap")
        return ndimage.zoom(g / g.std(), (ny / g.shape[0], nx / g.shape[1]), order=1)[:ny, :nx]
    # hafif alan bükmesi: karşılıklar birebir kopya olmasın (görüntü pikseli; yaklaşık 40 km)
    bukme = (gur(500) * 8 + gur(150) * 3, gur(500) * 8 + gur(150) * 3)
    toplam = np.zeros((ny, nx), np.float32); wtop = np.zeros((ny, nx), np.float32)
    genis = []
    kaynaklar = {}
    # ağırlık sınırlarını kıvır: karşılıklar arasındaki geçiş düz çizgi olmasın (yaklaşık ±70 km)
    II, JJ = np.indices((ny, nx), dtype=np.float32)
    kd = (gur(350) * 22 + gur(90) * 7) * s, (gur(350) * 22 + gur(90) * 7) * s
    for k in KARSILIK:
        w = agirlik(k, lab, adlar, ny, nx, s)
        w = ndimage.map_coordinates(w, [II + kd[1], JJ + kd[0]], order=1, mode="nearest").astype(np.float32) * kara * k.get("oncelik", 1.0)
        z, _ = ornekle(k, ny, nx, s, w, kaynaklar, bukme)
        toplam += w * z; wtop += w
        genis.append((k, w))
        if k["ad"] == "Tarım":
            doku_t = z.copy()
        log(f"{k['ad']}: tamam (en yüksek {z.max():.0f} m)")
    # boşluk kalan kara: en yakın karşılığın geniş yumuşatılmış ağırlığıyla
    bos = kara & (wtop < 0.05)
    if bos.any():
        log(f"boş kara hücresi {bos.sum()}")
        for k, w in genis:
            wb = ndimage.gaussian_filter(w, 40) * bos
            z, _ = ornekle(k, ny, nx, s, wb, kaynaklar, bukme)
            toplam += wb * z; wtop += wb
    z = toplam / np.maximum(wtop, 1e-6)
    # Tarım dokusu tasarlanan alanın tamamında gerekir
    if TASARIM.get("etkin"):
        k_t = TASARIM["doku"]
        im = Image.new("L", (nx, ny), 0)
        ImageDraw.Draw(im).polygon([(x * s, y * s) for x, y in TASARIM["alan"]], fill=1)
        alan = ndimage.binary_dilation(np.asarray(im) > 0, iterations=int(80 * s))
        doku_t, _ = ornekle(k_t, ny, nx, s, alan.astype(np.float32), kaynaklar, bukme)
        z = tasarla(z, kara, s, doku_t)
        log("tasarlanan bölge işlendi")
    # kıyı rampası: kaynakta iç kesim olan yer hedefte kıyıya düşerse yumuşak iniş
    dk = ndimage.distance_transform_edt(kara) * O.KM_PX / s
    u = np.clip(dk / 45.0, 0, 1)
    z = z * (0.3 + 0.7 * u * u * (3 - 2 * u))
    z = np.where(kara, np.maximum(z, 1.0), 0.0)
    np.save(f"{CIKTI}/benzer_z.npy", z.astype(np.float32))
    np.save(f"{CIKTI}/benzer_gol.npy", (GOL > 0.5) & kara)
    log(f"bileşik en yüksek {z.max():.0f} m")


def golge(z, h_m):
    gy, gx = np.gradient(ndimage.gaussian_filter(z, 0.6), h_m)
    a, e = np.radians(315), np.radians(40)
    lx, ly, lz = np.sin(a) * np.cos(e), np.cos(a) * np.cos(e), np.sin(e)
    nx_, ny_ = -gx * 3, gy * 3
    return np.clip(0.45 + 0.7 * (nx_ * lx + ny_ * ly + lz) / np.sqrt(nx_ ** 2 + ny_ ** 2 + 1), 0.25, 1.1)


def onizle(adlar_sec):
    s = 0.5
    ny, nx = int(O.YUK * s), int(O.GEN * s)
    kara = np.asarray(Image.open("maske.png").convert("L").resize((nx, ny), Image.BOX)) > 127
    lab, adlar = parca_etiket(ny, nx)
    kaynaklar = {}
    for k in KARSILIK:
        if adlar_sec and k["ad"] not in adlar_sec:
            continue
        im = Image.new("L", (nx, ny), 0)
        ImageDraw.Draw(im).polygon([(x * s, y * s) for x, y in k["bolge"]], fill=255)
        alan = ndimage.binary_dilation(np.asarray(im) > 0, iterations=60)
        z, deniz = ornekle(k, ny, nx, s, alan.astype(float), kaynaklar)
        g = golge(z, O.KM_PX / s * 1e3)
        rgb = np.stack([np.interp(z, [0, 500, 1500, 3000, 6000], c) for c in
                        ([90, 170, 200, 160, 240], [140, 170, 160, 130, 240], [80, 100, 110, 110, 240])], -1) * g[..., None]
        rgb = np.where((deniz > 0.5)[..., None], np.array([70, 110, 170]) * g[..., None], rgb)
        rgb = np.where(alan[..., None], rgb, 30)
        kenar = kara ^ ndimage.binary_erosion(kara)
        rgb[kenar] = [255, 40, 40]
        img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(img)
        d.line([(x * s, y * s) for x, y in k["bolge"] + k["bolge"][:1]], fill=(255, 255, 0), width=1)
        for tx, ty, _, _ in k.get("nokta", []) + ([k["benzerlik"][:4]] if "benzerlik" in k else []):
            d.ellipse([tx * s - 4, ty * s - 4, tx * s + 4, ty * s + 4], outline=(0, 255, 255), width=2)
        # kırp
        xs = [p[0] * s for p in k["bolge"]]; ys = [p[1] * s for p in k["bolge"]]
        img = img.crop((max(0, min(xs) - 80), max(0, min(ys) - 80), min(nx, max(xs) + 80), min(ny, max(ys) + 80)))
        img.save(f"{ONIZ}/oniz_{k['ad']}.png")
        log(f"{k['ad']}: önizleme")


def etiketler():
    """Karşılıkların yer şekli adları: kaynak (boylam, enlem) → hedef görüntü pikseli (bükmesiz yaklaşık)."""
    out = []
    for k in KARSILIK:
        if not k.get("etiket"):
            continue
        _, geri = esleme(k)
        xy = geri(np.array([[e[1], e[2]] for e in k["etiket"]], float))
        out += [(e[0], (float(x), float(y)), e[3]) for e, (x, y) in zip(k["etiket"], xy)]
    return out


def etiketle(im):
    W, H = im.size; s = W / O.GEN
    d = ImageDraw.Draw(im)
    YK = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    f = lambda n, k=False: ImageFont.truetype(YK if k else YAZI, int(n * s))
    import arazi as AR
    for la in range(-5, 55, 5):
        y = (50 - la) * 111.2 / O.KM_PX * s
        if 0 < y < H:
            for x in range(0, W, int(24 * s)):
                d.line([(x, y), (x + 10 * s, y)], fill=(255, 255, 255), width=max(1, int(s)))
            d.text((6 * s, y + 2 * s), f"{abs(la)}°{'K' if la >= 0 else 'G'}", fill=(255, 255, 255), font=f(13))
    yazi = [("1", (380, 330), 46, True), ("2", (1560, 120), 46, True), ("3", (1260, 1080), 46, True), ("4", (330, 1150), 46, True),
            ("5", (885, 1075), 34, True), ("6", (720, 790), 32, True), ("7", (1040, 1255), 30, True),
            ("İÇ DENİZ", (900, 700), 22, False), ("Batı Körfezi", (215, 790), 15, False), ("Güneydoğu Kanalı", (1060, 1150), 14, False),
            ("KUZEY OKYANUSU", (1100, 18), 22, False), ("DOĞU OKYANUSU", (1660, 1100), 22, False),
            ("GÜNEY OKYANUSU", (800, 1470), 22, False), ("Doğu Hendeği", (1590, 1250), 14, False)]
    yazi += [(t, (x - len(t) * n * 0.3, y - n * 0.6), n, False) for t, (x, y), n in etiketler() + (TASARIM["etiket"] if TASARIM.get("etkin") else [])]
    for t, (x, y), n, k in yazi:
        d.text((x * s, y * s), t, fill=(25, 25, 25), font=f(n, k), stroke_width=max(1, int(2.5 * s)), stroke_fill=(250, 250, 245))
    kat = Image.new("RGBA", (int(260 * s), int(40 * s)), (0, 0, 0, 0))
    ImageDraw.Draw(kat).text((0, 0), "BATI OKYANUSU", fill=(25, 25, 25), font=f(20), stroke_width=max(1, int(2.5 * s)), stroke_fill=(250, 250, 245))
    kat = kat.rotate(90, expand=True)
    im.paste(kat, (int(4 * s), int(380 * s)), kat)
    x0, y0, gw, gh = 1640 * s, 1380 * s, 300 * s, 14 * s
    for kk in range(int(gw)):
        zz = -4000 + 13000 * kk / gw
        c = AR.renk(AR.HIPSO, np.array([max(zz, 0)]))[0] if zz >= 0 else AR.renk(AR.DENIZ, np.array([zz]))[0]
        d.line([(x0 + kk, y0), (x0 + kk, y0 + gh)], fill=tuple(int(v) for v in c))
    for zz in (-4000, 0, 2000, 4000, 6000, 8000):
        xx = x0 + (zz + 4000) / 13000 * gw
        d.line([(xx, y0 + gh), (xx, y0 + gh + 4 * s)], fill=(255, 255, 255))
        d.text((xx - 10 * s, y0 + gh + 5 * s), f"{zz}", fill=(255, 255, 255), font=f(9))
    d.text((x0, y0 - 16 * s), "yükseklik (m)", fill=(255, 255, 255), font=f(11))
    x0, y0 = 1650 * s, 1480 * s; L = 1000 / O.KM_PX * s
    d.rectangle([x0, y0, x0 + L, y0 + 6 * s], fill=(255, 255, 255)); d.rectangle([x0, y0, x0 + L / 2, y0 + 6 * s], fill=(30, 30, 30))
    d.text((x0, y0 - 18 * s), "0        500      1000 km", fill=(255, 255, 255), font=f(12))
    return im


def buzul_golleri(z, kara):
    """1'in kuzeyindeki kalkanda (Ak Kalkan) buzulların kazıdığı küçük göller: alçak, düz, nemli kesimde."""
    ny, nx = kara.shape; s = nx / O.GEN
    r = np.random.default_rng(31)
    gol = np.zeros((ny, nx), bool)
    egim = ndimage.generic_gradient_magnitude(ndimage.gaussian_filter(z, 2), ndimage.sobel) / 8
    say, deneme = 0, 0
    while say < 380 and deneme < 200000:
        deneme += 1
        x = r.uniform(120, 820); y = r.uniform(60, 470)
        if x > 520 and y > 330:
            continue
        i, j = int(y * s), int(x * s)
        if not kara[i, j] or z[i, j] > 350 or egim[i, j] > 25:
            continue
        L = r.uniform(1.5, 6.5) * s; B = L * r.uniform(0.25, 0.5); a = np.radians(-40 + r.normal(0, 12))
        r0, r1 = max(i - 20, 0), min(i + 21, ny); c0, c1 = max(j - 20, 0), min(j + 21, nx)
        dy, dx = np.mgrid[r0:r1, c0:c1]; dy = dy - i; dx = dx - j
        u = (dx * np.cos(a) + dy * np.sin(a)) / L; v = (-dx * np.sin(a) + dy * np.cos(a)) / B
        m = (u * u + v * v < 1) & kara[r0:r1, c0:c1]
        if m.sum() < 3:
            continue
        gol[r0:r1, c0:c1] |= m
        say += 1
    return gol


def ciz():
    import arazi as AR
    z = np.load(f"{CIKTI}/benzer_z.npy").astype(float)
    kt = np.asarray(Image.open("maske.png").convert("L")) > 127
    nyt, nxt = kt.shape
    kara = AR.maske()
    zg = ndimage.zoom(z, (AR.NY / nyt, AR.NX / nxt), order=1)[:AR.NY, :AR.NX]
    lat = O.enlem(AR.RR / AR.G)
    P = AR.yagis(kara, np.where(kara, zg, 0.0), lat)
    np.save(f"{CIKTI}/benzer_yagis.npy", P.astype(np.float32))
    Pt = ndimage.zoom(P, (nyt / AR.NY, nxt / AR.NX), order=1)[:nyt, :nxt]
    dk = ndimage.distance_transform_edt(kara) * AR.H_KM
    zd = AR.batimetri(kara, dk)
    zdt = ndimage.zoom(zd, (nyt / AR.NY, nxt / AR.NX), order=1)[:nyt, :nxt]
    zt = np.where(kt, z, np.minimum(zdt, -5.0))
    np.save(f"{CIKTI}/benzer_son_z.npy", zt.astype(np.float32))
    log("nehirler")
    nh = AR.nehirler(z, kt, Pt, AR.H_M / 2)
    log(f"nehir parçası {len(nh)}")
    gol = buzul_golleri(zt, kt)
    gol |= np.load(f"{CIKTI}/benzer_gol.npy") & kt
    im, _, _ = AR.ciz(zt, kt, Pt, None, gol, 1, AR.H_M / 2, nh, kar_kurak=0.0, kar_bolge=True)
    im.save(f"{CIKTI}/topografya.png")
    etiketle(im.copy()).save(f"{CIKTI}/topografya_etiketli.png")
    np.save(f"{CIKTI}/son_z_tam.npy", np.where(gol, zt, zt).astype(np.float32))
    np.save(f"{CIKTI}/son_z.npy", ndimage.zoom(zt, (AR.NY / nyt, AR.NX / nxt), order=1)[:AR.NY, :AR.NX].astype(np.float32))
    log("çizim tamam")


if __name__ == "__main__":
    adim = sys.argv[1] if len(sys.argv) > 1 else "onizle"
    if adim == "onizle":
        onizle(sys.argv[2:])
    if adim == "bilesik":
        bilesik()
    if adim == "ciz":
        ciz()
