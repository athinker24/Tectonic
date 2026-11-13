"""340 milyon yıldan bugüne levha hareketleri (katı parça geri kurgusu).

Kullanım: python animasyon.py [KARE_KLASORU]
Çıktı: cikti/animasyon.mp4, cikti/animasyon.gif, cikti/kareler/*.png; ayrıca belge için dönem kareleri.
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage

import olaylar as O

YAZI = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
YAZI_K = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
X0, Y0, X1, Y1 = -200, -120, 2200, 3000      # tuval (görüntü pikseli)
S = 1080 / (X1 - X0)                         # tuval ölçeği
CW, CH = int((X1 - X0) * S), int((Y1 - Y0) * S)
PANEL = 230                                  # alttaki yazı paneli yüksekliği

RENK = {
    "1": (201, 179, 138), "2": (186, 164, 124), "serit": (214, 160, 112), "3": (201, 142, 106), "4": (166, 182, 124),
    "5": (224, 177, 90), "6": (150, 184, 168), "7": (230, 194, 122), "guney": (170, 140, 122),
}
TOHUM = {"1": (400, 300), "2": (1300, 200), "serit": (1400, 515), "3": (1300, 900), "4": (300, 1100),
         "5": (820, 1150), "6": (720, 780), "7": (1050, 1240)}


def parcalar():
    m = np.asarray(Image.open("maske.png").convert("L").resize((O.GEN, O.YUK), Image.BOX)) > 127
    im = Image.fromarray(m.astype(np.uint8) * 255)
    d = ImageDraw.Draw(im)
    kes = dict(O.CIZGI)
    kes["mor"] = [(1060, 640)] + O.CIZGI["mor"] + [(1745, 705)]
    kes["serit"] = [(1025, 610), (1035, 580)] + O.CIZGI["serit"] + [(2000, 560)]
    kes["kopru"] = [(-5, 735), (90, 790), (175, 812), (200, 830)]
    for ad in ("mavi", "mor", "sari", "yesil", "serit", "kopru"):
        d.line(kes[ad], fill=0, width=3)
    k = np.asarray(im) > 0
    L, n = ndimage.label(k)
    etiket = np.full(L.shape, "", object)
    lab = np.zeros(L.shape, np.int16)
    adlar = list(TOHUM)
    for i, (ad, (x, y)) in enumerate(TOHUM.items(), 1):
        l = L[y, x]
        assert l > 0, ad
        lab[L == l] = i
    # kalan küçük parçalar ve kesim çizgileri: en yakın etiketli parçaya
    ata = m & (lab == 0)
    _, (ii, jj) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    lab = np.where(ata, lab[ii, jj], lab)
    lab = np.where(m, lab, 0)
    return lab, adlar


def merkez(lab, i):
    y, x = np.nonzero(lab == i)
    return np.array([x.mean(), y.mean()])


def ara(kf, t):
    """Anahtar karelerden (t, a, dx, dy) doğrusal ara değer."""
    ts = np.array([k[0] for k in kf], float)
    return tuple(np.interp(t, ts, [k[j] for k in kf]) for j in (1, 2, 3))


def dondur(a):
    r = np.radians(a)
    return np.array([[np.cos(r), -np.sin(r)], [np.sin(r), np.cos(r)]])


class Donusum:
    """p_gecmis = R (p − c) + c + d (görüntü pikseli)."""
    def __init__(self, a=0.0, c=(0, 0), d=(0, 0)):
        self.R = dondur(a); self.c = np.array(c, float); self.d = np.array(d, float); self.a = a

    def __call__(self, p):
        p = np.atleast_2d(np.array(p, float))
        return (p - self.c) @ self.R.T + self.c + self.d


def donusum(ad, t, mer):
    if ad in ("1", "2"):
        return Donusum()
    if ad in ("5", "7"):
        a_r, dx_r, dy_r = O.BAGLI_3[ad]
        A = Donusum(a_r, mer[ad], (dx_r, dy_r))
        def bilesik(tt):
            T3 = donusum("3", tt, mer)
            yeni_c = T3(A(mer[ad]))[0]
            return T3.a + A.a, yeni_c
        if t >= O.KOPMA_5_7:
            a, c2 = bilesik(t)
        else:
            a22, c22 = bilesik(O.KOPMA_5_7)
            f = t / O.KOPMA_5_7
            a = a22 * f; c2 = mer[ad] + (c22 - mer[ad]) * f
        return Donusum(a, mer[ad], c2 - mer[ad])
    a, dx, dy = ara(O.HAREKET[ad], t)
    return Donusum(a, mer[ad], (dx, dy))


def tuvale(p):
    p = np.atleast_2d(p)
    return np.stack([(p[:, 0] - X0) * S, (p[:, 1] - Y0) * S], 1)


def katman_ciz(tuval, rgba, T):
    """rgba (görüntü pikseli çerçevesinde) katmanını T dönüşümüyle tuvale yapıştırır."""
    Ri = T.R.T
    # çıkış q → giriş p: p = Ri ((q / S + O) − c − d) + c
    a, b = Ri[0, 0] / S, Ri[0, 1] / S
    dd, e = Ri[1, 0] / S, Ri[1, 1] / S
    o = np.array([X0, Y0]) - T.c - T.d
    c0 = Ri[0] @ o + T.c[0]; f0 = Ri[1] @ o + T.c[1]
    katman = rgba.transform((CW, CH), Image.AFFINE, (a, b, c0, dd, e, f0), resample=Image.BILINEAR)
    tuval.alpha_composite(katman)


def guney_kita(lab, mer, i4):
    """Güney Kıtası'nın 4'e yapışık (320 ile 160 MYÖ) konumdaki maskesi, görüntü pikseli çerçevesinde (tuval boyu)."""
    W, H = X1 - X0, Y1 - Y0
    T4 = donusum("4", 200, mer)
    y4, x4 = np.nonzero(lab == i4)
    p = T4(np.stack([x4, y4], 1))
    kenar = np.full(W, np.nan)
    xs = np.round(p[:, 0] - X0).astype(int)
    ok = (xs >= 0) & (xs < W)
    for x, y in zip(xs[ok], p[ok, 1]):
        if np.isnan(kenar[x]) or y > kenar[x]:
            kenar[x] = y
    xx = np.arange(W) + X0
    # 4'ün altındaki sütunlar: kıyıya bitişik; doğuda kenar 3'ün 150 MYÖ'deki güney ucuna doğru iner
    bati = ~np.isnan(kenar)
    kenar_b = np.where(bati, kenar + 4, np.nan)
    son_x = xx[bati].max()
    k = np.interp(xx, np.r_[xx[bati], son_x + 250, 1250, 2200], np.r_[kenar_b[bati], kenar_b[bati][-1] + 250, 2080, 2050])
    k = ndimage.maximum_filter1d(k, 60)
    k = ndimage.gaussian_filter1d(k, 22) + ndimage.gaussian_filter1d(np.random.default_rng(3).standard_normal(W), 12) * 25
    yy = np.arange(H)[:, None] + Y0
    m = yy > k[None, :]
    return m


def cizgi_ciz(d, pts, renk, gen=3, tur="hendek", yan=1):
    q = tuvale(np.array(pts))
    d.line([tuple(v) for v in q], fill=renk, width=gen)
    if tur == "hendek":
        L = np.cumsum(np.r_[0, np.hypot(*np.diff(q, axis=0).T)])
        for s in np.arange(8, L[-1], 16):
            i = min(np.searchsorted(L, s) - 1, len(q) - 2); i = max(i, 0)
            u = (s - L[i]) / max(L[i + 1] - L[i], 1e-6)
            p = q[i] + (q[i + 1] - q[i]) * u
            t = (q[i + 1] - q[i]) / max(np.hypot(*(q[i + 1] - q[i])), 1e-6)
            n = np.array([-t[1], t[0]]) * yan
            d.polygon([tuple(p - t * 4), tuple(p + t * 4), tuple(p + n * 7)], fill=renk)
    elif tur == "sirt":
        q2 = q + np.array([3, 3])
        d.line([tuple(v) for v in q2], fill=renk, width=gen)


def olay_metni(t):
    don = None
    for D in O.DONEMLER:
        a, b = D["aralik"]
        if b <= t <= a or (don is None and t <= a):
            don = D
    for D in O.DONEMLER:
        a, b = D["aralik"]
        if b <= t <= a:
            don = D
    yakın = []
    for D in O.DONEMLER:
        for (ty, bas, ac) in D["olaylar"]:
            if t - 0.5 <= ty <= t + 6 + 0.04 * t:
                yakın.append((ty, bas))
    yakın.sort(key=lambda q: -q[0])
    return don, yakın[-4:]


def kare(t, lab, adlar, mer, renkli, guney_m, topo=None, topo_w=0.0):
    tuval = Image.new("RGBA", (CW, CH), (24, 62, 112, 255))
    # okyanus: hafif derinlik dokusu
    d = ImageDraw.Draw(tuval)
    # Güney Kıtası
    gdx, gdy = (np.interp(t, [k[0] for k in O.GUNEY_KITA], [k[j] for k in O.GUNEY_KITA]) for j in (1, 2))
    gm = Image.fromarray((guney_m * 255).astype(np.uint8)).resize((CW, CH), Image.BILINEAR)
    g_rgba = Image.new("RGBA", (CW, CH), RENK["guney"] + (0,))
    g_rgba.putalpha(gm)
    kay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); kay.alpha_composite(g_rgba, (int(gdx * S), int(gdy * S)))
    tuval.alpha_composite(kay)
    # dalan kıta kenarı (3'ün kuzeyi, 50 MYÖ'den beri 2'nin altına giren kesim)
    T = {ad: donusum(ad, t, mer) for ad in adlar}
    if t < 50:
        ust = np.array(O.CIZGI["mor"]); alt = T["3"](ust)
        poly = tuvale(np.vstack([ust, alt[::-1]]))
        d.polygon([tuple(v) for v in poly], fill=(176, 130, 100, 255))
        for i in range(0, len(poly) // 2):
            pass
    # parçalar (ön planda en son 3, 5, 7)
    sira = ["1", "2", "serit", "4", "6", "3", "5", "7"]
    for ad in sira:
        katman_ciz(tuval, renkli[ad], T[ad])
    d = ImageDraw.Draw(tuval)
    kirmizi, mor_r, beyaz = (230, 60, 50), (150, 70, 200), (245, 245, 245)
    # levha sınırları (döneme göre)
    if 340 >= t > 320:
        T4 = T["4"]; y4, x4 = np.nonzero(lab == adlar.index("4") + 1)
        xs = np.linspace(x4.min(), x4.max(), 25)
        ys = [y4[np.abs(x4 - x) < 8].max() + 10 for x in xs]
        cizgi_ciz(d, T4(np.stack([xs, ys], 1)), kirmizi, 3, "hendek", -1)
    if 250 >= t > 210:
        cizgi_ciz(d, O.CIZGI["serit"], kirmizi, 3, "hendek", -1)
    if 175 >= t > 50:
        cizgi_ciz(d, T["serit"](O.CIZGI["mor"]), kirmizi, 3, "hendek", -1)
    if 60 >= t >= 0:
        cizgi_ciz(d, T["3"](O.DIP["hendekler"][0][1]), kirmizi, 3, "hendek", -1)
    if 25 >= t >= 0:
        cizgi_ciz(d, O.DIP["hendekler"][1][1], kirmizi, 2, "hendek", -1)
    if 22 >= t > 8:
        cizgi_ciz(d, O.CIZGI["sari"], kirmizi, 2, "hendek", 1)
    if 270 >= t > 150:
        # Yeni Mor sırtı: İnce Şerit ile Güney Kıtası arası
        yS = T["serit"]([(1400, 640)])[0, 1]; yG = 2050 + gdy
        ym = (yS + yG) / 2 if t > 210 else (T["3"]([(1300, 560)])[0, 1] + yS) / 2 + 200
        cizgi_ciz(d, [(1050, ym + 40), (1500, ym), (2150, ym - 30)], beyaz, 2, "sirt")
    if 150 >= t > 50:
        y3 = T["3"]([(1300, 1420)])[0, 1]; yG = 2050 + gdy
        ym = (y3 + yG) / 2
        cizgi_ciz(d, [(800, ym + 60), (1300, ym), (2150, ym - 40)], beyaz, 2, "sirt")
    if 190 >= t:
        cizgi_ciz(d, [(-150, -100), (-150, 1600)], beyaz, 2, "sirt")
    if 160 >= t:
        yG = 1480 + gdy
        cizgi_ciz(d, [(-150, (1480 + yG) / 2 + 30), (500, (1480 + yG) / 2), (1000, (1500 + yG) / 2)], beyaz, 2, "sirt")
    if 22 >= t:
        cizgi_ciz(d, [(950, 960), (1070, 1110), (1210, 1290)], (255, 170, 60), 2, "yarik")
    # sıcak nokta
    hs = tuvale(donusum("3", 66, mer)((1280, 1030)))[0]
    if t <= 70:
        d.ellipse([hs[0] - 7, hs[1] - 7, hs[0] + 7, hs[1] + 7], outline=(255, 120, 0), width=3)
    # parça numaraları
    fn = ImageFont.truetype(YAZI_K, 22)
    for i, ad in enumerate(adlar, 1):
        if ad == "serit":
            continue
        p = tuvale(T[ad](mer[ad]))[0]
        d.text((p[0] - 7, p[1] - 12), ad, fill=(40, 25, 20), font=fn, stroke_width=2, stroke_fill=(255, 255, 255))
    p = tuvale(T["serit"]((1450, 560)))[0]
    d.text((p[0] - 30, p[1] - 9), "Şerit", fill=(40, 25, 20), font=ImageFont.truetype(YAZI_K, 15), stroke_width=2, stroke_fill=(255, 255, 255))
    if t < 340:
        p = tuvale(np.array([[900, 2600 + gdy]]))[0]
        if p[1] < CH - 20:
            d.text((p[0], p[1]), "GÜNEY KITASI", fill=(60, 40, 30), font=ImageFont.truetype(YAZI_K, 20), stroke_width=2, stroke_fill=(240, 230, 220))
    # bugünkü topografya ile geçiş
    if topo is not None and topo_w > 0:
        tp = topo.resize((int(O.GEN * S), int(O.YUK * S)), Image.LANCZOS).convert("RGBA")
        tp.putalpha(int(255 * topo_w))
        tuval.alpha_composite(tp, (int(-X0 * S), int(-Y0 * S)))
    # panel
    son = Image.new("RGB", (CW, CH + PANEL), (250, 248, 244))
    son.paste(tuval.convert("RGB"), (0, 0))
    dp = ImageDraw.Draw(son)
    don, yakin = olay_metni(t)
    yas = f"{t:.0f} milyon yıl önce" if t >= 1 else ("bugün" if t == 0 else f"{t * 1000:.0f} bin yıl önce")
    dp.text((16, CH + 10), yas, fill=(20, 20, 20), font=ImageFont.truetype(YAZI_K, 34))
    if don:
        dp.text((16, CH + 56), don["ad"], fill=(120, 40, 30), font=ImageFont.truetype(YAZI_K, 24))
    fy = ImageFont.truetype(YAZI, 19)
    for k, (ty, bas) in enumerate(yakin):
        dp.text((16, CH + 94 + k * 30), f"{ty:g} MYÖ  {bas}", fill=(40, 40, 40), font=fy)
    # zaman çubuğu
    x0, x1 = 600, CW - 20; yb = CH + 24
    dp.line([(x0, yb), (x1, yb)], fill=(120, 120, 120), width=3)
    xt = x1 - (x1 - x0) * t / 340
    dp.ellipse([xt - 8, yb - 8, xt + 8, yb + 8], fill=(200, 60, 40))
    fk = ImageFont.truetype(YAZI, 14)
    for tt in (340, 250, 150, 66, 0):
        xx = x1 - (x1 - x0) * tt / 340
        dp.text((xx - 12, yb + 12), str(tt), fill=(90, 90, 90), font=fk)
    # açıklama
    dp.text((600, CH + 70), "kırmızı dişli çizgi: dalma (dişler üst levhada)", fill=(150, 40, 30), font=fk)
    dp.text((600, CH + 92), "beyaz çift çizgi: okyanus sırtı; turuncu: yarık", fill=(60, 60, 60), font=fk)
    dp.text((600, CH + 114), "kahverengi kuşak: 2'nin altına dalan kıta kenarı", fill=(110, 70, 50), font=fk)
    dp.text((600, CH + 136), "turuncu halka: sıcak nokta (Kızıl Basamaklar)", fill=(200, 100, 0), font=fk)
    return son


def main():
    kl = sys.argv[1] if len(sys.argv) > 1 else "cikti/kareler"
    os.makedirs(kl, exist_ok=True)
    lab, adlar = parcalar()
    mer = {ad: merkez(lab, i) for i, ad in enumerate(adlar, 1)}
    topo = Image.open("cikti/topografya.png").convert("RGB") if os.path.exists("cikti/topografya.png") else None
    golge = None
    if topo is not None:
        golge = np.asarray(topo.resize((O.GEN, O.YUK), Image.LANCZOS).convert("L"), float) / 255.0
    renkli = {}
    for i, ad in enumerate(adlar, 1):
        m = lab == i
        rgb = np.zeros((O.YUK, O.GEN, 4), np.uint8)
        c = np.array(RENK[ad], float)
        if golge is not None:
            sh = np.clip(0.55 + 0.6 * (golge - golge[m].mean()) + 0.45, 0.6, 1.25)
            col = c[None, None, :] * sh[..., None]
        else:
            col = np.broadcast_to(c, (O.YUK, O.GEN, 3))
        rgb[..., :3] = np.clip(col, 0, 255).astype(np.uint8)
        kenar = m ^ ndimage.binary_erosion(m)
        rgb[kenar, :3] = (90, 70, 55)
        rgb[..., 3] = (m * 255).astype(np.uint8)
        renkli[ad] = Image.fromarray(rgb, "RGBA")
    gm = guney_kita(lab, mer, adlar.index("4") + 1)
    zamanlar = list(np.arange(340, 60, -2.0)) + list(np.arange(60, 20, -1.0)) + list(np.arange(20, 0, -0.5)) + [0.0]
    n = 0
    for t in zamanlar:
        im = kare(float(t), lab, adlar, mer, renkli, gm)
        im.save(f"{kl}/k{n:04d}.png"); n += 1
    for k in range(36):
        im = kare(0.0, lab, adlar, mer, renkli, gm, topo, min(1.0, k / 18))
        im.save(f"{kl}/k{n:04d}.png"); n += 1
    # dönem kareleri (belge için)
    os.makedirs("cikti/donem", exist_ok=True)
    for t in (340, 300, 250, 210, 170, 130, 100, 85, 66, 50, 35, 22, 10, 0):
        kare(float(t), lab, adlar, mer, renkli, gm).save(f"cikti/donem/t{t:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "12", "-i", f"{kl}/k%04d.png", "-vf",
                    "scale=1080:-2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "cikti/animasyon.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "12", "-i", f"{kl}/k%04d.png", "-vf",
                    "scale=540:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse", "cikti/animasyon.gif"], check=True)
    print("kare", n)


if __name__ == "__main__":
    main()
