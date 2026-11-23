"""Ana kalıp: son_temiz_16k.png + batıdaki kara köprüsü, komşu sıranın güneye uzanan kolu olarak.
Arazi: iki kara kütlesinin kıyı yüksekliklerinden harmonik taban + köprü ekseni boyunca sırt + aynı haritanın komşu dağından
alınan ince doku; eksenden uzaklaştıkça deniz tabanına iner. Kıyı, bu arazinin 0 m eğrisidir (elle çizilmez).
Mevcut hiçbir kara pikseli değişmez; yalnız BOLGE içindeki deniz pikselleri karaya dönebilir."""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
S = 14642
KOK = os.path.dirname(os.path.abspath(__file__))
AYAR = {
    "kutu16k": [2780, 3060, 6820, 7180],
    "eksen": [[7008, 2885], [7024, 2915], [7034, 2962]],     # kuzey kıyıdaki sıradan güney kütleye
    "bolge": [[6930, 2840], [7110, 2840], [7110, 3010], [6930, 3010]],
    "d0_px": 16, "rampa_m_px": 22, "sirt_m": 800, "sirt_gen_px": 9, "kivrim_px": 6,
    "doku_kaydir": [-95, -35], "doku_kat": 1.4, "tohum": 11, "dikis_px": 7,
}


def coz(g):
    g = g.astype(np.float64)
    return np.where(g > S, 8000 * np.clip((g - S) / (65535 - S), 0, None) ** 2, -6840 * np.clip(1 - g / S, 0, None) ** (1 / 0.607))


def kodla(m):
    kara = S + 1 + (65534 - S) * np.sqrt(np.clip(m, 0, 8000) / 8000); deniz = S * (1 - np.clip(-m / 6840, 0, 1) ** 0.607)
    return np.round(np.where(m > 0, kara, np.minimum(deniz, S))).clip(0, 65535).astype(np.uint16)


def cizgi_uzakligi(shape, noktalar):
    yy, xx = np.indices(shape).astype(np.float64)
    d = np.full(shape, np.inf); t_all = np.zeros(shape)
    for (ax, ay), (bx, by) in zip(noktalar[:-1], noktalar[1:]):
        ab = np.array([bx - ax, by - ay], float); px = xx - ax; py = yy - ay
        t = np.clip((px * ab[0] + py * ab[1]) / (ab @ ab), 0, 1)
        dd = np.hypot(px - t * ab[0], py - t * ab[1]); d = np.minimum(d, dd)
    return d


def main(ayar=AYAR, yaz=True, onek="_b2"):
    g = np.asarray(Image.open(os.path.join(KOK, "kaynak", "son_temiz_16k.png")))
    y0, y1, x0, x1 = ayar["kutu16k"]
    blok = g[y0:y1, x0:x1]; k = blok > S; z = coz(blok)
    rng = np.random.default_rng(ayar["tohum"])
    # taban: kara yüksekliklerinin denize harmonik uzantısı
    zl = np.where(k, np.maximum(z, 0), 0.0); f = np.where(k, zl, np.median(zl[k]))
    for _ in range(700):
        f = np.where(k, zl, ndimage.uniform_filter(f, 3))
    taban = ndimage.gaussian_filter(f, 3) * 0.6
    # eksen uzaklığı, kıvrılmış
    ek = [[x - x0, y - y0] for x, y in ayar["eksen"]]
    d = cizgi_uzakligi(k.shape, ek)
    gur = ndimage.gaussian_filter(rng.standard_normal(k.shape), 10); gur /= gur.std()
    gur2 = ndimage.gaussian_filter(rng.standard_normal(k.shape), 3.5); gur2 /= gur2.std()
    d = np.maximum(d + ayar["kivrim_px"] * gur + 2.2 * gur2, 0)
    sirt = ayar["sirt_m"] * np.exp(-(d / ayar["sirt_gen_px"]) ** 2) * (0.75 + 0.25 * gur)
    # ince doku: aynı haritanın komşu dağından (yüksek geçiren), karada
    dy, dx = ayar["doku_kaydir"]
    kay = g[y0 + dy:y1 + dy, x0 + dx:x1 + dx]; kk = kay > S; zk = coz(kay)
    alcak = ndimage.gaussian_filter(np.where(kk, zk, 0), 4) / np.maximum(ndimage.gaussian_filter(kk.astype(float), 4), 1e-3)
    doku = np.where(kk, zk - alcak, 0) * ayar["doku_kat"]
    F = taban + sirt + doku * np.clip((taban + sirt) / 400, 0.25, 1.2) - ayar["rampa_m_px"] * np.clip(d - ayar["d0_px"], 0, None)
    im = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(im).polygon([(x - x0, y - y0) for x, y in ayar["bolge"]], fill=1)
    R = (np.asarray(im) > 0) & ~k
    yeni_kara = R & (F > 0)
    L, n = ndimage.label(k | yeni_kara); ana = L == L[2900 - y0, 7010 - x0]
    yeni_kara &= ana
    deniz = ~(k | yeni_kara); Ld, nd = ndimage.label(deniz); sz = ndimage.sum(deniz, Ld, range(1, nd + 1))
    yeni_kara |= np.isin(Ld, np.nonzero(sz < 40)[0] + 1) & R
    sinir = (np.asarray(im) > 0) & ~ndimage.binary_erosion(np.asarray(im) > 0)
    kesik = int((yeni_kara & ndimage.binary_dilation(sinir, iterations=1)).sum())
    Lk = ndimage.label(k)[0]
    zz = np.maximum(F, 3.0)
    # dikiş: eski kıyının alçak şeridi yeni karanın içinde kaldıysa (Merak'ın kıyı rampası) çevresiyle harmanlanır.
    # Kıyı çizgisi değişmez; yalnız yeni karaya dikis_px içindeki eski kara pikselleri yükselebilir.
    dn = ndimage.distance_transform_edt(~yeni_kara)
    w = np.clip(1 - dn / ayar["dikis_px"], 0, 1) * k
    w = w * w * (3 - 2 * w)
    zyeni = np.where(yeni_kara, zz, np.nan)
    pay = ndimage.gaussian_filter(np.nan_to_num(zyeni), 3) / np.maximum(ndimage.gaussian_filter(yeni_kara.astype(float), 3), 1e-3)
    hedef = np.maximum(z, 0.5 * z + 0.5 * pay)
    zeski = np.where(w > 0, (1 - w) * z + w * hedef, z)
    G = g.copy(); b2 = blok.copy(); b2[yeni_kara] = kodla(zz[yeni_kara])
    degis = (w > 0.01) & k; b2[degis] = kodla(np.maximum(zeski[degis], 1)); G[y0:y1, x0:x1] = b2
    ka_once = ndimage.label(k)[1]; ka_sonra = ndimage.label(G[y0:y1, x0:x1] > S)[1]
    print(f"kesik {kesik}, kara bileşeni {ka_once} -> {ka_sonra}, eklenen {int(yeni_kara.sum())}, "
          f"yükseklik %10/50/90 {np.percentile(zz[yeni_kara], [10, 50, 90]).round()}, en yüksek {zz[yeni_kara].max():.0f}, "
          f"karada yüksekliği değişen (kıyı çizgisi aynı) {int(((G != g) & (g > S)).sum())}, kıyı farkı dışında kara kaybı {int(((G <= S) & (g > S)).sum())}")
    cc = G[y0:y1, x0:x1]; zc = coz(cc); kk2 = cc > S
    v = np.where(kk2, 60 + 195 * np.clip(zc / 1500, 0, 1) ** 0.6, 25).astype(np.uint8)
    Image.fromarray(v).resize((cc.shape[1] * 3, cc.shape[0] * 3), Image.NEAREST).save(os.path.join(KOK, f"{onek}.png"))
    if yaz:
        Image.fromarray(G).save(os.path.join(KOK, "kaynak", "ana_16k.png"))
        json.dump({**ayar, "eklenen_piksel": int(yeni_kara.sum())}, open(os.path.join(KOK, "bagla_ayar.json"), "w"), ensure_ascii=False, indent=1)
    return G


if __name__ == "__main__":
    main()
