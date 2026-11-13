"""Tarihten araziye: yapı (kuşaklar, yaylalar, havzalar, volkanlar) + aşınma + topografik harita.

Kullanım: python arazi.py [ADIM] [ON_EK]
Çıktı: cikti/arazi_z.npy (ızgara 1457 × 1904, 4,2 km), cikti/topografya.png (3808 × 2914) ve etiketli sürüm.
"""
import sys
import time

import fastscapelib as fs
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage
from scipy.spatial import cKDTree

import olaylar as O

T0 = time.time()
NY, NX = 1457, 1904
G = NX / O.GEN                     # görüntü pikselinden ızgara hücresine
H_KM = O.KM_PX / G                 # hücre boyu km (yaklaşık 4,2)
H_M = H_KM * 1e3
RNG = np.random.default_rng(20261113)
YAZI = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
YAZI_K = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def log(s):
    print(f"[{time.time() - T0:6.0f} s] {s}", flush=True)


def maske():
    m = Image.open("maske.png").convert("L").resize((NX, NY), Image.BOX)
    return np.asarray(m) > 127


def cokgen(p, deger=1.0, buk=True):
    im = Image.new("F", (NX, NY), 0.0)
    ImageDraw.Draw(im).polygon([(x * G, y * G) for x, y in p], fill=deger)
    a = np.asarray(im)
    if buk:
        a = ndimage.map_coordinates(a, [RR + WY, CC + WX], order=1, mode="nearest")
    return a


def gurultu(olcek_km, kok=None):
    r = kok or RNG
    n = ndimage.gaussian_filter(r.standard_normal((NY, NX)), olcek_km / H_KM, mode="wrap")
    return n / (n.std() + 1e-12)


def fraktal(olcekler):
    return sum(a * gurultu(s) for s, a in olcekler)


def cizgi_ornek(cizgi, deger=None):
    """Çizgiyi 1 hücre adımla örnekler; köşe değerlerini doğrusal enterpole eder."""
    p = np.array(cizgi, float) * G
    pts, vals, tan = [], [], []
    for i in range(len(p) - 1):
        a, b = p[i], p[i + 1]
        L = max(int(np.hypot(*(b - a))), 1)
        t = np.linspace(0, 1, L, endpoint=False)
        pts.append(a + (b - a) * t[:, None])
        d = (b - a) / (np.hypot(*(b - a)) + 1e-9)
        tan.append(np.repeat(d[None], L, 0))
        if deger is not None:
            vals.append(deger[i] + (deger[i + 1] - deger[i]) * t)
    pts.append(p[-1:]); tan.append(tan[-1][-1:])
    if deger is not None:
        vals.append(np.array([deger[-1]]))
    pts = np.concatenate(pts); tan = np.concatenate(tan)
    # teğeti düzgünleştir (köşelerde kırık yön olmasın)
    tan = ndimage.uniform_filter1d(tan, 15, axis=0, mode="nearest")
    tan /= np.linalg.norm(tan, axis=1, keepdims=True) + 1e-9
    return pts, (np.concatenate(vals) if deger is not None else None), tan


RR, CC = np.mgrid[0:NY, 0:NX].astype(np.float32)
XY = np.stack([CC.ravel(), RR.ravel()], 1)
# alan bükme: elle çizilmiş çizgi ve çokgenler doğal kıvrılsın (250 km ölçekte 35 km, 70 km ölçekte 9 km)
_r = np.random.default_rng(77)
def _g(s):
    n = ndimage.gaussian_filter(_r.standard_normal((NY, NX)), s / 4.2, mode="wrap"); return n / n.std()
WX = (_g(600) * 110 + _g(160) * 35 + _g(50) * 8) / 4.2
WY = (_g(600) * 110 + _g(160) * 35 + _g(50) * 8) / 4.2
XYW = np.stack([(CC + WX).ravel(), (RR + WY).ravel()], 1)


def kusak_alani(cizgi, deger, yari_km, dik):
    """Her hücre için: uzaklık (km), tepe değeri, teğet, yan (+1 sağ, −1 sol)."""
    pts, vals, tan = cizgi_ornek(cizgi, deger)
    tr = cKDTree(pts)
    d, i = tr.query(XYW, distance_upper_bound=yari_km * 4 / H_KM)
    ok = np.isfinite(d)
    i = np.where(ok, i, 0)
    v = (XYW - pts[i])
    cross = tan[i, 0] * v[:, 1] - tan[i, 1] * v[:, 0]   # görüntü koordinatında (y aşağı): + sağ
    yan = np.sign(cross)
    dkm = np.where(ok, d * H_KM, np.inf)
    # uç noktalarda yuvarlak sönme: çizginin ucundan ötede uzaklık zaten büyür; ek olarak tepe uçlarda azalır
    s = np.arange(len(pts)) / max(len(pts) - 1, 1)
    uc = np.clip(np.minimum(s, 1 - s) * len(pts) * H_KM / (1.5 * yari_km), 0, 1)
    uc = 0.35 + 0.65 * (uc * uc * (3 - 2 * uc))
    tepe = vals[i] * uc[i]
    return (dkm.reshape(NY, NX), tepe.reshape(NY, NX), tan[i, 0].reshape(NY, NX), tan[i, 1].reshape(NY, NX),
            yan.reshape(NY, NX))


def lic(N, tx, ty, adim):
    """Gürültüyü doğrultu alanı boyunca ortalar (çizgi tümlevi)."""
    ny, nx = N.shape
    rr, cc = np.mgrid[0:ny, 0:nx].astype(np.float32)
    top = N.copy(); say = np.ones_like(N)
    for yon in (1.0, -1.0):
        r, c = rr.copy(), cc.copy(); px = py = None
        for k in range(adim):
            ii = np.clip(np.rint(r).astype(int), 0, ny - 1); jj = np.clip(np.rint(c).astype(int), 0, nx - 1)
            dx, dy = tx[ii, jj], ty[ii, jj]
            if px is not None:
                ters = dx * px + dy * py < 0
                dx = np.where(ters, -dx, dx); dy = np.where(ters, -dy, dy)
            px, py = dx, dy
            c = c + yon * dx; r = r + yon * dy
            w = np.exp(-(k / (0.8 * adim)) ** 2)
            top += w * ndimage.map_coordinates(N, [r, c], order=1, mode="reflect"); say += w
    return top / say


def desen(tx, ty, aralik_km, boy_km):
    f = max(1, int(round(aralik_km / 8 / H_KM)))
    hc = H_KM * f
    N = ndimage.gaussian_filter(RNG.standard_normal(tx[::f, ::f].shape), aralik_km / 4 / hc)
    L = lic(N.astype(np.float32), tx[::f, ::f], ty[::f, ::f], max(2, int(boy_km / 2 / hc)))
    L = L - ndimage.gaussian_filter(L, aralik_km / hc)
    L /= L.std() + 1e-12
    up = ndimage.zoom(L, f, order=3)[:NY, :NX]
    up = np.pad(up, ((0, NY - up.shape[0]), (0, NX - up.shape[1])), mode="edge")
    return np.clip(up / 2.0, -1, 1)


def yapi(kara):
    """Hedef yüzey (aşınmadan önce) ve yardımcı alanlar."""
    dk = ndimage.distance_transform_edt(kara) * H_KM            # kıyıya uzaklık (karada)
    lat = O.enlem(RR / G)
    # taban: alçak kıyı ovaları, iç kesimde hafif yükselme, uzun dalga dalgalanma
    taban = 120 + 260 * np.clip(dk / 500, 0, 1) ** 0.8 + 140 * gurultu(350) + 60 * gurultu(120)
    # kalkanlar daha alçak ve düz (Ak, Boz)
    kalkan = np.clip(cokgen([(200, 120), (650, 110), (700, 420), (400, 520), (180, 450)]) +
                     cokgen([(1520, 40), (1900, 60), (1950, 420), (1700, 470), (1560, 380)]), 0, 1)
    kalkan = ndimage.gaussian_filter(kalkan, 60 / H_KM)
    taban = taban * (1 - 0.45 * kalkan)
    z = taban.copy()
    # doğrultu ve şiddet alanları (desen için)
    TX = np.zeros((NY, NX), np.float32); TY = np.zeros((NY, NX), np.float32); W = np.zeros((NY, NX), np.float32)
    genc = np.zeros((NY, NX), np.float32); tepe_yuk = np.zeros((NY, NX), np.float32)
    for ad, c, deger, yari, yas, dik in O.KUSAKLAR:
        d, tp, tx, ty, yan = kusak_alani(c, deger, yari, dik)
        w_yan = np.where(yan * dik > 0, 0.6, 1.0) if dik != 0 else 1.0
        if dik != 0:
            w_yan = np.where(yan * dik < 0, 1.35, w_yan)
        u = d / (yari * w_yan)
        f = np.exp(-1.1 * u ** 2.6)
        f = np.where(np.isfinite(d), f, 0.0)
        hk = taban + (tp - taban) * f
        z = np.maximum(z, hk)
        wgt = f ** 1.5
        TX += wgt * tx; TY += wgt * ty; W += wgt
        g = np.clip(1 - yas / 200.0, 0.15, 1)  # gençlik: 0 MYÖ 1, 200+ MYÖ 0,15
        genc = np.maximum(genc, f * g); tepe_yuk = np.maximum(tepe_yuk, f * tp)
        log(f"kuşak {ad}")
    # yaylalar
    PW = np.zeros((NY, NX), np.float32)
    for ad, p, (yb, yd), yum in O.PLATOLAR:
        m = cokgen(p)
        yum = max(yum, 60)
        w = np.clip(ndimage.gaussian_filter(m, yum / H_KM) * 1.7 - 0.35 + 0.35 * gurultu(70) * ndimage.gaussian_filter(m, 2 * yum / H_KM), 0, 1)
        w = w * w * (3 - 2 * w)
        xs = np.array([q[0] for q in p]) * G
        t = np.clip((CC - xs.min()) / (xs.max() - xs.min()), 0, 1)
        hedef = yb + (yd - yb) * t + 120 * gurultu(80) + 60 * gurultu(25)
        if ad in ("Kızıl Basamaklar", "Kuzey Tuzakları"):
            # basamaklı bazalt: yükseklik kademeli (her 180 m bir basamak), kenarlar dik
            hedef = np.round(hedef / 180.0) * 180.0 + 40 * gurultu(15)
        if ad in ("Mor Yaylası", "Kum Havzası"):
            PW = np.maximum(PW, w)
        if ad == "Kum Havzası":
            z = np.where(w > 0, (1 - w) * z + w * np.minimum(z, hedef) + w * 0, z)
            z = (1 - w) * z + w * hedef
        else:
            z = np.maximum(z, (1 - w) * z + w * hedef)
        log(f"yayla {ad}")
    # ovalar ve ön havzalar
    for ad, p, hy in O.OVALAR:
        w = np.clip(ndimage.gaussian_filter(cokgen(p), 60 / H_KM) * 1.6 - 0.3 + 0.3 * gurultu(60), 0, 1)
        z = (1 - w) * z + w * (hy + 40 * gurultu(40))
    # sırt deseni: doğrultu alanı (kuşakların teğeti) boyunca
    n = np.sqrt(TX ** 2 + TY ** 2) + 1e-6
    tx, ty = TX / n, TY / n
    tx = np.where(W > 1e-3, tx, 1.0); ty = np.where(W > 1e-3, ty, 0.0)
    ana = desen(tx, ty, 90.0, 300.0)
    ikinci = desen(tx, ty, 32.0, 110.0)
    orta = desen(tx, ty, 50.0, 70.0)
    tepe = lambda q: np.clip(q, 0, 1) ** 1.2
    d = 1.1 * tepe(ana) + 0.6 * tepe(orta) + 0.45 * tepe(ikinci) * (0.4 + 0.6 * np.clip(ana + 0.5, 0, 1)) - 0.38
    yukseklik_payi = np.clip((z - taban) / 2500.0, 0, 1)
    gen = (0.35 + 0.65 * genc) * yukseklik_payi * (1 - 0.65 * PW)
    z = z + 1500.0 * gen * d
    # eski kuşakların izi: rastgele doğrultulu yaşlı sırtlar (kuşak dışı her yerde, 150 ile 350 m)
    aci = gurultu(900) * 1.6
    ox, oy = np.cos(aci).astype(np.float32), np.sin(aci).astype(np.float32)
    yasli = desen(ox, oy, 75.0, 200.0)
    z = z + np.clip(yasli, -0.3, 1) * (50 + 90 * np.clip(gurultu(400) + 0.3, 0, 1)) * (1 - np.clip(W, 0, 1)) * (1 - PW)
    # genel engebe: yükseklikle artan
    z = z + (40 + 0.08 * np.clip(z, 0, None)) * fraktal([(60, 0.6), (20, 0.4)])
    # volkanlar
    for (x, y) in O.VOLKANLAR:
        r = np.hypot(CC - x * G, RR - y * G) * H_KM
        hv = 1600 + 900 * RNG.random()
        z = z + hv * np.exp(-(r / 11.0) ** 1.4)
    z = np.where(kara, np.maximum(z, 5.0), 0.0)
    log("yapı katmanı tamam")
    return z, dk, lat


def yagis(kara, z, lat):
    """Göreli yağış: enlem kuşakları, rüzgâr yönünde karasallık ve yağmur gölgesi."""
    la = lat
    temel = np.interp(la, [-6, 0, 8, 14, 20, 26, 32, 38, 44, 52], [1.7, 1.8, 1.5, 0.9, 0.45, 0.4, 0.55, 0.85, 1.0, 0.9])
    zs = ndimage.gaussian_filter(np.where(kara, z, 0.0), 30 / H_KM)
    # batı rüzgârı (enlem > 34): batıdan doğuya biriken kara uzaklığı ve engel
    deniz = (~kara).astype(float)
    def birikim(ters):
        k = np.zeros((NY, NX)); e = np.zeros((NY, NX))
        kk = np.zeros(NY); ee = np.zeros(NY)
        rng_ = range(NX - 1, -1, -1) if ters else range(NX)
        for j in rng_:
            kk = np.where(deniz[:, j] > 0, 0.0, kk + H_KM)
            ee = np.where(deniz[:, j] > 0, 0.0, np.maximum(ee * np.exp(-H_KM / 600.0), zs[:, j]))
            k[:, j] = kk; e[:, j] = ee
        return k, e
    karasal = ndimage.distance_transform_edt(kara) * H_KM
    w_bati = np.clip((la - 28) / 14, 0, 1)
    # rüzgârın önündeki engel: rüzgâr yönünde 20 km adımlarla, 600 km'de e kadar sönen en yüksek engel
    adim = max(1, int(20 / H_KM))
    eb = np.zeros_like(zs); ed = np.zeros_like(zs)
    for k in range(1, 60):
        sn = np.exp(-k * adim * H_KM / 600.0)
        eb = np.maximum(eb, np.roll(zs, k * adim, axis=1) * sn)
        ed = np.maximum(ed, np.roll(zs, -k * adim, axis=1) * sn)
    engel = w_bati * eb + (1 - w_bati) * ed
    P = temel * np.exp(-karasal / 1100.0) * np.exp(-np.clip(engel - zs, 0, None) / 2200.0)
    # rüzgâra bakan yamaç: yükselen yüzey
    gy, gx = np.gradient(zs, H_M)
    ruzgar = w_bati * gx - (1 - w_bati) * gx
    P = P * (1 + np.clip(ruzgar * 40, -0.4, 1.2))
    P = ndimage.gaussian_filter(P, 110 / H_KM)
    return np.clip(P, 0.05, 3.0)


def asinma(z_hedef, kara, P, sure=3.0, K=2.2e-6, h_m=H_M, dt=2e4, s_km=14.0):
    ny_, nx_ = z_hedef.shape
    pur = ndimage.gaussian_filter(np.random.default_rng(9).standard_normal((ny_, nx_)), 1.0)
    zz = np.where(kara, z_hedef + np.abs(5 * pur / pur.std()), 0.0)
    NY_, NX_ = ny_, nx_
    grid = fs.RasterGrid([ny_, nx_], [h_m, h_m], fs.NodeStatus.FIXED_VALUE)
    router = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver(), fs.MultiFlowRouter(1.0)])
    eroder = fs.SPLEroder(router, K, 0.45, 1.0, 1e-4)
    yamac = fs.DiffusionADIEroder(grid, 1.5)
    n = int(round(sure * 1e6 / dt))
    s15 = s_km / (h_m / 1e3)
    hedef_d = ndimage.gaussian_filter(np.where(kara, z_hedef, 0.0), s15)
    Pm = np.ascontiguousarray(P * kara + 1e-3, dtype=np.float64)
    for i in range(n):
        zf = np.ascontiguousarray(zz, dtype=np.float64)
        router.update_routes(zf)
        A = np.asarray(router.accumulate(Pm))
        e = np.asarray(eroder.erode(zf, A, dt)).reshape(NY_, NX_)
        zz = zz - np.where(kara, np.clip(e, 0, None), 0.0)
        zd = np.ascontiguousarray(zz, dtype=np.float64)
        zz = zz - np.where(kara, np.asarray(yamac.erode(zd, dt)).reshape(NY_, NX_), 0.0)
        U = (hedef_d - ndimage.gaussian_filter(zz, s15)) * min(1.0, dt / 4e5)
        zz = np.where(kara, np.maximum(zz + U, 1.0), 0.0)
        if i % 25 == 24:
            log(f"aşınma {i + 1}/{n}")
    zf = np.ascontiguousarray(zz, dtype=np.float64)
    router.update_routes(zf)
    A = np.asarray(router.accumulate(Pm))
    return zz, A


def batimetri(kara, dk_kara):
    dd = ndimage.distance_transform_edt(~kara) * H_KM
    # sahanlık genişliği: edilgen kenarda geniş, etkin kenarda dar
    sahanlik = 130 + 60 * gurultu(300) + 25 * gurultu(80)
    etkin = ndimage.gaussian_filter(cokgen([(1560, 700), (1990, 700), (1990, 1530), (1500, 1530), (1530, 1100)]), 50 / H_KM)
    sahanlik = sahanlik * (1 - 0.8 * etkin)
    ic = ndimage.gaussian_filter(cokgen([(150, 480), (1180, 480), (1200, 1320), (880, 1320), (600, 1000), (150, 900)]), 30 / H_KM)
    sahanlik = sahanlik * (1 - 0.6 * ic)
    u = dd / np.maximum(sahanlik, 15)
    z = np.where(u < 1, -20 - 160 * u ** 1.5, -180 - 4200 * (1 - np.exp(-(u - 1) * 0.9)))
    z = z * (1 - 0.35 * ic) + ic * np.minimum(0, z)
    for ad, c, derin, yari in O.DIP["hendekler"]:
        pts, _, _ = cizgi_ornek(c)
        d, _ = cKDTree(pts).query(XY)
        f = np.exp(-(d.reshape(NY, NX) * H_KM / yari) ** 2)
        z = np.minimum(z, (1 - f) * z + f * derin)
    for ad, p, derin in O.DIP["havzalar"]:
        w = ndimage.gaussian_filter(cokgen(p), 40 / H_KM)
        z = np.minimum(z, (1 - w) * z + w * derin)
    z = z + 80 * gurultu(30) * np.clip(-z / 1000, 0, 1)
    return np.where(kara, 0.0, np.minimum(z, -5.0))


def goller(kara, z):
    gol = np.zeros((NY, NX), bool); seviye = np.zeros((NY, NX))
    for ad, g, sv in O.GOLLER:
        pts, _, _ = cizgi_ornek(g["cizgi"])
        d, _ = cKDTree(pts).query(XY)
        m = (d.reshape(NY, NX) <= g["gen"] * G * (0.8 + 0.4 * (gurultu(10) > 0))) & kara
        gol |= m; seviye[m] = sv
    # kuzeydeki buzul gölleri: kalkanlarda, 52. enlemin kuzeyinde, KB GD uzanımlı küçük göller
    lat = O.enlem(RR / G)
    say = 0
    while say < 420:
        x = RNG.uniform(60, 1960) * G; y = RNG.uniform(60, 420) * G
        i, j = int(y), int(x)
        if not kara[i, j] or lat[i, j] < 41 or z[i, j] > 700:
            continue
        L = RNG.uniform(1.5, 6.0); B = L * RNG.uniform(0.25, 0.5); a = np.radians(-35 + RNG.normal(0, 12))
        r0, r1 = max(i - 8, 0), min(i + 9, NY); c0, c1 = max(j - 8, 0), min(j + 9, NX)
        dy = RR[r0:r1, c0:c1] - y; dx = CC[r0:r1, c0:c1] - x
        u = (dx * np.cos(a) + dy * np.sin(a)) / L; v = (-dx * np.sin(a) + dy * np.cos(a)) / B
        m = (u * u + v * v < 1) & kara[r0:r1, c0:c1]
        gol[r0:r1, c0:c1] |= m; seviye[r0:r1, c0:c1][m] = z[i, j]
        say += 1
    return gol, seviye


# ------------------------------------------------------------------ çizim
HIPSO = np.array([
    # yükseklik, R, G, B (kurak olmayan ton)
    [0, 86, 136, 78], [200, 112, 156, 88], [500, 160, 176, 108], [900, 198, 186, 128], [1400, 204, 170, 120],
    [2000, 178, 144, 104], [3000, 150, 118, 92], [4000, 146, 128, 112], [5000, 150, 140, 132], [8000, 170, 166, 162]], float)
KURAK = np.array([
    [0, 196, 182, 140], [150, 208, 190, 146], [400, 214, 192, 148], [800, 210, 180, 136], [1300, 198, 164, 120],
    [2000, 178, 142, 104], [3000, 158, 126, 98], [4000, 150, 130, 112], [5000, 150, 140, 132], [8000, 170, 166, 162]], float)
DENIZ = np.array([[-8000, 18, 40, 82], [-5000, 30, 64, 118], [-3000, 44, 88, 146], [-1000, 64, 116, 170],
                  [-200, 96, 152, 196], [-20, 128, 180, 214], [0, 136, 186, 218]], float)


def renk(tablo, z):
    return np.stack([np.interp(z, tablo[:, 0], tablo[:, i]) for i in (1, 2, 3)], -1)


def ciz(z, kara, P, A, gol, olcek=2, h_m=H_M, nehir=None):
    """Tam çözünürlükte (maske boyutu) gölgeli kabartma ve hipsometrik renk."""
    ny, nx = z.shape[0] * olcek, z.shape[1] * olcek
    zb = ndimage.zoom(z, olcek, order=3)[:ny, :nx]
    kb = np.asarray(Image.open("maske.png").convert("L").resize((nx, ny), Image.BILINEAR)) > 127
    # büyütmeye ince ayrıntı: yerel engebeyle orantılı küçük ölçekli gürültü
    eng = ndimage.zoom(ndimage.generic_gradient_magnitude(z, ndimage.sobel), olcek, order=1)[:ny, :nx] / (8 * h_m)
    r2 = np.random.default_rng(5)
    ince = ndimage.gaussian_filter(r2.standard_normal((ny, nx)), 1.2)
    ince /= ince.std()
    zb = np.where(kb, np.maximum(zb + ince * np.clip(eng, 0, 0.5) * 900 * (h_m / 1e3) / olcek * 0.06, 2), np.minimum(zb, -5))
    Pb = ndimage.zoom(P, olcek, order=1)[:ny, :nx]
    golb = ndimage.zoom(gol.astype(np.uint8), olcek, order=0)[:ny, :nx] > 0
    h = h_m / olcek
    zg = ndimage.gaussian_filter(np.where(kb, zb, 0.0), 0.7)
    gy, gx = np.gradient(zg, h)
    isik = 0.0
    for az, yuk, w in ((315, 40, 0.6), (250, 50, 0.2), (20, 55, 0.2)):
        a = np.radians(az); e = np.radians(yuk)
        lx, ly, lz = np.sin(a) * np.cos(e), np.cos(a) * np.cos(e), np.sin(e)
        ab = 3.0
        nx_, ny_ = -gx * ab, gy * ab
        isik = isik + w * (nx_ * lx + ny_ * ly + lz) / np.sqrt(nx_ ** 2 + ny_ ** 2 + 1)
    isik = np.clip(0.42 + 0.75 * isik, 0.3, 1.15)
    kurak = np.clip((0.55 - Pb) / 0.35, 0, 1)[..., None]
    rk = (1 - kurak) * renk(HIPSO, np.clip(zb, 0, 8000)) + kurak * renk(KURAK, np.clip(zb, 0, 8000))
    # kar çizgisi enleme bağlı; üstü beyaz, geçiş 600 m
    latb = O.enlem(np.arange(ny)[:, None] * O.YUK / ny) * np.ones((1, nx))
    kc = np.interp(latb, [-6, 5, 15, 25, 32, 40, 48, 56], [4800, 4900, 5000, 5400, 5200, 4100, 3000, 2000])
    zk = ndimage.gaussian_filter(zb, 2.0) + 120 * ndimage.gaussian_filter(r2.standard_normal((ny, nx)), 3.0) / 0.1
    kar = np.clip((zk - kc) / 700.0, 0, 1)[..., None] * 0.92
    rk = rk * (1 - kar) + np.array([246, 246, 250]) * kar
    rd = renk(DENIZ, np.clip(zb, -8000, 0))
    # deniz tabanına hafif gölge
    isik_d = np.clip(0.85 + 0.25 * (isik - 0.8), 0.7, 1.05)
    rgb = np.where(kb[..., None], rk * isik[..., None], rd * isik_d[..., None])
    # göller
    rgb = np.where((golb & kb)[..., None], np.array([118, 170, 210]) * 0.97, rgb)
    # nehirler: yumuşatılmış çizgiler (2 kat örneklemeyle kenar yumuşatma)
    if nehir is not None:
        kat = Image.new("L", (nx * 2, ny * 2), 0)
        dn = ImageDraw.Draw(kat)
        for pts, w in nehir:
            dn.line([(x * 2 * olcek, y * 2 * olcek) for x, y in pts], fill=255, width=max(1, int(round(w * 2))), joint="curve")
        kat = np.asarray(kat.resize((nx, ny), Image.LANCZOS), float)[..., None] / 255.0
        kat = kat * (kb & ~golb)[..., None]
        rgb = rgb * (1 - 0.85 * kat) + np.array([64, 116, 178]) * 0.85 * kat
    # kıyı çizgisi
    kenar = kb ^ ndimage.binary_erosion(kb)
    rgb = np.where(kenar[..., None], rgb * 0.55, rgb)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), zb, kb


def etiketle(im):
    W, H = im.size; s = W / O.GEN
    d = ImageDraw.Draw(im)
    f = lambda n, k=False: ImageFont.truetype(YAZI_K if k else YAZI, int(n * s))
    # enlem çizgileri
    for la in range(-5, 55, 5):
        y = (50 - la) * 111.2 / O.KM_PX * s
        if 0 < y < H:
            for x in range(0, W, int(24 * s)):
                d.line([(x, y), (x + 10 * s, y)], fill=(255, 255, 255, 90), width=max(1, int(s)))
            d.text((6 * s, y + 2 * s), f"{abs(la)}°{'K' if la >= 0 else 'G'}", fill=(255, 255, 255), font=f(13))
    def bukulmus(x, y):
        """Yapı katmanındaki alan bükmesi: çizgideki nokta haritada (x − WX, y − WY) yerine düşer."""
        gx, gy = int(np.clip(x * G, 0, NX - 1)), int(np.clip(y * G, 0, NY - 1))
        return x - WX[gy, gx] / G, y - WY[gy, gx] / G
    kus = {k[0]: k[1] for k in O.KUSAKLAR}
    def kusak_yeri(ad, kay=(0, 0), oran=0.5):
        c = np.array(kus[ad], float); L = np.r_[0, np.cumsum(np.hypot(*np.diff(c, axis=0).T))]
        t = oran * L[-1]; i = min(np.searchsorted(L, t) - 1, len(c) - 2); i = max(i, 0)
        p = c[i] + (c[i + 1] - c[i]) * (t - L[i]) / max(L[i + 1] - L[i], 1e-6)
        x, y = bukulmus(*p)
        return x + kay[0], y + kay[1]
    yazi = [
        ("1", (380, 330), 46, True), ("2", (1560, 120), 46, True), ("3", (1260, 980), 46, True), ("4", (330, 1150), 46, True),
        ("5", (820, 1190), 36, True), ("6", (720, 790), 32, True), ("7", (1040, 1255), 30, True),
        ("MOR SIRADAĞLARI", kusak_yeri("Mor Sıradağları", (-110, 45), 0.55), 20, False),
        ("MOR YAYLASI", kusak_yeri("Şerit Sırtları", (-60, 12), 0.5), 20, False),
        ("UZAK SIRA", kusak_yeri("Uzak Sıra", (-50, -35), 0.45), 18, False),
        ("Kum Havzası", (1290, 375), 17, False), ("Derin Göl", (1700, 245), 16, False),
        ("MAVİ DAĞLAR", kusak_yeri("Mavi Dağlar", (15, 0), 0.45), 17, False),
        ("ULU DAĞLAR", kusak_yeri("Ulu Dağlar", (20, 0), 0.5), 16, False),
        ("KÖPRÜ DAĞLARI", kusak_yeri("Köprü Dağları", (-60, 40), 0.4), 16, False),
        ("SARI SIRADAĞLARI", kusak_yeri("Sarı Sıradağları", (-190, 20), 0.6), 16, False),
        ("Kızıl Basamaklar", (1180, 1060), 17, False),
        ("DOĞU YAY DAĞLARI", kusak_yeri("Doğu Yay Dağları", (25, 0), 0.6), 15, False),
        ("Kuzey Tuzakları", (1240, 150), 17, False), ("Köz Yaylası", (300, 1060), 17, False),
        ("Mor Ön Ovası", (1300, 715), 16, False),
        ("İÇ DENİZ", (900, 700), 22, False), ("Batı Körfezi", (215, 790), 15, False), ("Güneydoğu Kanalı", (1060, 1150), 14, False),
        ("KUZEY OKYANUSU", (1100, 18), 22, False), ("DOĞU OKYANUSU", (1660, 1100), 22, False),
        ("GÜNEY OKYANUSU", (800, 1470), 22, False), ("Doğu Hendeği", (1590, 1250), 14, False),
    ]
    for t, (x, y), n, k in yazi:
        ff = f(n, k)
        d.text((x * s, y * s), t, fill=(25, 25, 25), font=ff, stroke_width=max(1, int(2.5 * s)), stroke_fill=(250, 250, 245))
    # batı okyanusu: dikey yazı
    ff = f(20)
    kat = Image.new("RGBA", (int(260 * s), int(40 * s)), (0, 0, 0, 0))
    ImageDraw.Draw(kat).text((0, 0), "BATI OKYANUSU", fill=(25, 25, 25), font=ff, stroke_width=max(1, int(2.5 * s)), stroke_fill=(250, 250, 245))
    kat = kat.rotate(90, expand=True)
    im.paste(kat, (int(4 * s), int(380 * s)), kat)
    # yükseklik göstergesi
    x0, y0, gw, gh = 1640 * s, 1380 * s, 300 * s, 14 * s
    for k in range(int(gw)):
        zz = -4000 + (7000 + 4000) * k / gw
        c = renk(HIPSO, np.array([max(zz, 0)]))[0] if zz >= 0 else renk(DENIZ, np.array([zz]))[0]
        d.line([(x0 + k, y0), (x0 + k, y0 + gh)], fill=tuple(int(v) for v in c))
    for zz in (-4000, 0, 1000, 3000, 5000, 7000):
        xx = x0 + (zz + 4000) / 11000 * gw
        d.line([(xx, y0 + gh), (xx, y0 + gh + 4 * s)], fill=(255, 255, 255))
        d.text((xx - 10 * s, y0 + gh + 5 * s), f"{zz}", fill=(255, 255, 255), font=f(9))
    d.text((x0, y0 - 16 * s), "yükseklik (m)", fill=(255, 255, 255), font=f(11))
    # ölçek çubuğu
    x0, y0 = 1650 * s, 1480 * s; L = 1000 / O.KM_PX * s
    d.rectangle([x0, y0, x0 + L, y0 + 6 * s], fill=(255, 255, 255)); d.rectangle([x0, y0, x0 + L / 2, y0 + 6 * s], fill=(30, 30, 30))
    d.text((x0, y0 - 18 * s), "0        500      1000 km", fill=(255, 255, 255), font=f(12))
    return im


def nehirler(z, kara, A, h_m, esik_km2=6000.0):
    """D8 en dik iniş alıcıları; eşiğin üstündeki hücrelerden aşağı akış çizgileri; yumuşatılmış."""
    ny_, nx_ = z.shape
    grid = fs.RasterGrid([ny_, nx_], [h_m, h_m], fs.NodeStatus.FIXED_VALUE)
    fg = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
    zf = np.ascontiguousarray(np.where(kara, z, -10.0), dtype=np.float64)
    fg.update_routes(zf)
    al = np.asarray(fg.impl().receivers)[:, 0].astype(np.int64).reshape(ny_, nx_)
    al = np.where(al == np.arange(ny_ * nx_).reshape(ny_, nx_), -1, al)
    A = np.asarray(fg.accumulate(np.ascontiguousarray(np.where(kara, A, 0.0), dtype=np.float64)))
    Akm = np.nan_to_num(A / 1e6, nan=0.0, posinf=0.0)
    nehir_m = (Akm > esik_km2) & kara
    sira = np.argsort(Akm[nehir_m])
    hucre = np.flatnonzero(nehir_m.ravel())[sira]
    gor = np.zeros(ny_ * nx_, bool)
    alr = al.ravel(); kr = kara.ravel(); Ar = Akm.ravel()
    cizgiler = []
    for c in hucre:
        if gor[c]:
            continue
        yol = [c]; gor[c] = True; k = c
        for _ in range(20000):
            r = alr[k]
            if r < 0:
                break
            yol.append(r)
            if gor[r] or not kr[r]:
                break
            gor[r] = True; k = r
        if len(yol) < 3:
            continue
        yy, xx = np.divmod(np.array(yol), nx_)
        xs = ndimage.gaussian_filter1d(xx.astype(float), 1.6, mode="nearest"); ys = ndimage.gaussian_filter1d(yy.astype(float), 1.6, mode="nearest")
        xs[0], ys[0], xs[-1], ys[-1] = xx[0], yy[0], xx[-1], yy[-1]
        a_ = Ar[np.array(yol)]
        # genişliği parçalara böl (alan arttıkça kalınlaşır)
        w = 0.5 + 0.9 * np.log10(np.maximum(a_ / esik_km2, 1.0))
        for s0 in range(0, len(yol) - 1, 12):
            s1 = min(s0 + 13, len(yol))
            cizgiler.append((list(zip(xs[s0:s1] + 0.5, ys[s0:s1] + 0.5)), float(w[s0:s1].mean())))
    return cizgiler


def main():
    adim = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    kara = maske()
    if adim in ("hepsi", "yapi"):
        z, dk, lat = yapi(kara)
        P = yagis(kara, z, lat)
        np.save("cikti/hedef_z.npy", z.astype(np.float32)); np.save("cikti/yagis.npy", P.astype(np.float32))
        log(f"hedef en yüksek {z.max():.0f} m")
        im, _, _ = ciz(z, kara, P, np.zeros_like(z), np.zeros_like(kara), olcek=1)
        im.save("cikti/hedef_onizleme.png")
    if adim in ("hepsi", "asinma"):
        z = np.load("cikti/hedef_z.npy").astype(float); P = np.load("cikti/yagis.npy").astype(float)
        sure = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
        za, A = asinma(z, kara, P, sure)
        np.save("cikti/arazi_z.npy", za.astype(np.float32)); np.save("cikti/akis.npy", A.astype(np.float32))
        log(f"aşınma sonrası en yüksek {za.max():.0f} m")
    if adim == "asinma_tam":
        z = np.load("cikti/hedef_z.npy").astype(float); P = np.load("cikti/yagis.npy").astype(float)
        kt = np.asarray(Image.open("maske.png").convert("L")) > 127
        nyt, nxt = kt.shape
        zt = ndimage.zoom(z, (nyt / NY, nxt / NX), order=3)[:nyt, :nxt]
        Pt = ndimage.zoom(P, (nyt / NY, nxt / NX), order=1)[:nyt, :nxt]
        zt = np.where(kt, np.maximum(zt, 3.0), 0.0)
        sure = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
        Kx = float(sys.argv[3]) if len(sys.argv) > 3 else 2.2e-6
        za, A = asinma(zt, kt, Pt, sure, Kx, H_M / 2, 2.5e4, s_km=float(sys.argv[4]) if len(sys.argv) > 4 else 14.0)
        np.save("cikti/arazi_z_tam.npy", za.astype(np.float32)); np.save("cikti/akis_tam.npy", A.astype(np.float32))
        log(f"tam aşınma sonrası en yüksek {za.max():.0f} m")
    if adim == "ciz_tam":
        za = np.load("cikti/arazi_z_tam.npy").astype(float); A = np.load("cikti/akis_tam.npy").astype(float)
        kt = np.asarray(Image.open("maske.png").convert("L")) > 127
        nyt, nxt = kt.shape
        P = np.load("cikti/yagis.npy").astype(float)
        Pt = ndimage.zoom(P, (nyt / NY, nxt / NX), order=1)[:nyt, :nxt]
        dk = ndimage.distance_transform_edt(kara) * H_KM
        zd = batimetri(kara, dk)
        zdt = ndimage.zoom(zd, (nyt / NY, nxt / NX), order=1)[:nyt, :nxt]
        zl = np.load("cikti/hedef_z.npy").astype(float)
        gol, sv = goller(kara, zl)
        golt = ndimage.gaussian_filter(ndimage.zoom(gol.astype(float), (nyt / NY, nxt / NX), order=1)[:nyt, :nxt], 2.5)
        golt = (golt + 0.25 * ndimage.gaussian_filter(np.random.default_rng(4).standard_normal((nyt, nxt)), 1.5) / 0.2 * 0.3) > 0.5
        svt = ndimage.zoom(ndimage.grey_dilation(sv, size=5), (nyt / NY, nxt / NX), order=0)[:nyt, :nxt]
        golt &= kt
        zt = np.where(kt, np.where(golt, svt, za), np.minimum(zdt, -5.0))
        np.save("cikti/son_z_tam.npy", zt.astype(np.float32))
        nh = nehirler(za, kt & ~golt, Pt, H_M / 2)
        log(f"nehir parçası {len(nh)}")
        im, _, _ = ciz(zt, kt, Pt, A, golt, 1, H_M / 2, nh)
        im.save("cikti/topografya.png")
        etiketle(im.copy()).save("cikti/topografya_etiketli.png")
        log("tam çizim tamam")
    if adim in ("hepsi", "ciz"):
        za = np.load("cikti/arazi_z.npy").astype(float); P = np.load("cikti/yagis.npy").astype(float)
        A = np.load("cikti/akis.npy").astype(float) / (H_M * H_M)
        dk = ndimage.distance_transform_edt(kara) * H_KM
        zd = batimetri(kara, dk)
        gol, sv = goller(kara, za)
        zt = np.where(kara, np.where(gol, sv, za), zd)
        np.save("cikti/son_z.npy", zt.astype(np.float32)); np.save("cikti/gol.npy", gol)
        olcek = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        im, zb, kb = ciz(zt, kara, P, A, gol, olcek)
        im.save("cikti/topografya.png")
        etiketle(im.copy()).save("cikti/topografya_etiketli.png")
        log("çizim tamam")


if __name__ == "__main__":
    main()
