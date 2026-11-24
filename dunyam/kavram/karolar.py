"""Kavram bölgesini Earth Platform'un yükseklik önbelleğine yazar: terrarium PNG karoları, `terrarium-v1/{z}/{x}/{y}.png`.

Earth Platform'dan (pirut/earth-platform dd31a85, kaynak okunarak) gelen kurallar:
- Yakın arazi z15'e kadar okunur, en kaba z9 (`EarthGenerator.zoom`, `COARSEST_ZOOM`); deniz derinliği z10'dan gelir
  (`GlobalElevation.BATHYMETRY_ZOOM`). z10'dan ince karolarda açık deniz tam 0 m olmalı; derinlik z10 ve daha kaba karolarda.
- Çevrimdışı kipte önbellekte olmayan karo üretilmez (`TerrariumTileSource.load`).

Kapsam: bölge (154 km) z9 ile z15; çevresi yalnız v3 tabanıyla (ince doku yok) z12'de 120 km'ye, z9 ile z11'de 300 km'ye kadar
(uzak görüş boşluksuz olsun). Bölge kenarında son 3 km'de doku tabana yumuşakça iner (dikiş olmasın)."""
import math
import os
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image
from scipy import ndimage

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kavram as K  # noqa: E402

CIKTI = os.path.join(KOK, "cikti", "paket", "earthplatform", "cache", "terrarium-v1")
KENAR_PX = 100           # bölge kenarında dokunun söndüğü genişlik (3 km)
HALKA_KM = {9: 300, 10: 300, 11: 300, 12: 120}
G = {}


def merc_ters(px, py, z):
    n = 256 * 2 ** z
    lon = px / n * 360 - 180
    lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * py / n))))
    return lon, lat


def merc(lon, lat, z):
    n = 256 * 2 ** z
    la = np.radians(lat)
    return (lon + 180) / 360 * n, (1 - np.log(np.tan(la) + 1 / np.cos(la)) / math.pi) / 2 * n


def hazirla():
    iz = K.Izgara(K.AYAR)
    Z = np.load(os.path.join(KOK, "cikti", "z30.npy"))
    G["iz"] = iz
    G["Z"] = {15: Z, 14: Z, 13: Z, 12: Z, 11: ndimage.gaussian_filter(Z, 1.0), 10: ndimage.gaussian_filter(Z, 2.0),
              9: ndimage.gaussian_filter(Z, 4.0)}
    # halka: v3, merkezin ±350 km'si
    lon0, lat0 = iz.lon0, iz.lat0
    dlat = 350 / 111.2; dlon = dlat / math.cos(math.radians(lat0))
    xs, ys = K.ll_v3(np.array([lon0 - dlon, lon0 + dlon]), np.array([lat0 + dlat, lat0 - dlat]))
    x0, x1, y0, y1 = int(xs.min()) - 4, int(xs.max()) + 5, int(ys.min()) - 4, int(ys.max()) + 5
    g = np.asarray(Image.open(os.path.join(KOK, "..", "kaynak", "ana_v3_16k.png")))[y0:y1, x0:x1]
    G["v3"] = ndimage.spline_filter(K.coz(g).astype(np.float64), 3)
    G["v3o"] = (x0, y0)


def deger(lon, lat, z):
    iz = G["iz"]
    x, y = K.ll_v3(lon, lat)
    halka = ndimage.map_coordinates(G["v3"], [y - G["v3o"][1], x - G["v3o"][0]], order=3, prefilter=False, mode="nearest")
    c, r = iz.px(lon, lat)
    ic = (c >= 0) & (c <= iz.n - 1) & (r >= 0) & (r <= iz.n - 1)
    v = halka.astype(np.float64)
    if ic.any():
        kenar = np.minimum(np.minimum(c, iz.n - 1 - c), np.minimum(r, iz.n - 1 - r))[ic]
        t = np.clip(kenar / KENAR_PX, 0, 1); w = t * t * (3 - 2 * t)
        bolge = ndimage.map_coordinates(G["Z"][z], [r[ic], c[ic]], order=1)
        v[ic] = w * bolge + (1 - w) * halka[ic]
    return v


def kodla(v):
    v = np.clip(v, -11000, 9000) + 32768
    q = np.round(v * 8) / 8                                  # 1/8 m: sıkıştırma için
    R = np.floor(q / 256); Gc = np.floor(q - R * 256); B = np.round((q - np.floor(q)) * 256)
    return np.stack([R, Gc, B], -1).astype(np.uint8)


def karo(arg):
    z, tx, ty = arg
    j, i = np.mgrid[0:256, 0:256]
    lon, lat = merc_ters(tx * 256 + i + 0.5, ty * 256 + j + 0.5, z)
    v = deger(lon, lat, z)
    kara = v > 0
    v = np.where(kara, np.maximum(v, 0.5), np.minimum(v, -1.0))
    if z > 10:
        v = np.where(kara, v, 0.0)                         # açık deniz: tam 0 (derinlik z10'dan)
    yol = os.path.join(CIKTI, str(z), str(tx), f"{ty}.png")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    Image.fromarray(kodla(v)).save(yol, compress_level=9)
    return os.path.getsize(yol), float(v.max()), int(kara.sum())


def karolar_listesi():
    iz = K.Izgara(K.AYAR)
    yari = (iz.n - 1) / 2 * iz.d / 1000
    liste = []
    for z in range(9, 16):
        km = max(HALKA_KM.get(z, 0), yari)
        dlat = km / 111.2; dlon = dlat / math.cos(math.radians(iz.lat0))
        X0, Y1 = merc(iz.lon0 - dlon, iz.lat0 - dlat, z); X1, Y0 = merc(iz.lon0 + dlon, iz.lat0 + dlat, z)
        for tx in range(int(X0 // 256), int(X1 // 256) + 1):
            for ty in range(int(Y0 // 256), int(Y1 // 256) + 1):
                liste.append((z, tx, ty))
    return liste


def main():
    hazirla()
    liste = karolar_listesi()
    print("karo sayısı", len(liste), {z: sum(1 for t in liste if t[0] == z) for z in range(9, 16)}, flush=True)
    with Pool(4) as p:
        sonuc = p.map(karo, liste, chunksize=64)
    boy = sum(s[0] for s in sonuc)
    print(f"toplam {boy / 1e9:.2f} GB; en yüksek {max(s[1] for s in sonuc):.0f} m")


if __name__ == "__main__":
    main()
