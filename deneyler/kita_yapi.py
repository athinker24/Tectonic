"""Sahibin kıtası: tektonik katman (kita_lab) + yapı katmanı + ince ızgarada aşınma.

Kullanım: python -m deneyler.kita_yapi ON_EK [KABA_H_KM] [PAY_KM] [H_KM] [SURE_MYR] [K] [GENLIK_M]
  ON_EK: kita_lab çıktısının öneki (…_z.npy ve …_S.npy olmadan).

Kurallar gerçek dünya sınamasındakiyle aynı (deneyler.yapi_kanit.yapi_ve_asinma); sert çekirdek yok.
İki çizim: kıyı simülasyondan (serbest) ve kıyı sahibin maskesinden (yükseklik simülasyondan).
"""
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.yapi_kanit import ciz, yapi_ve_asinma
from tektonik.izgara import maske_yukle
from tektonik.levha import duzlem_kur, laea_geri
from tektonik.yazi import yazi_tipi


def main():
    on = sys.argv[1]
    kaba_h = float(sys.argv[2]) if len(sys.argv) > 2 else 45.0
    pay = float(sys.argv[3]) if len(sys.argv) > 3 else 1800.0
    h_km = float(sys.argv[4]) if len(sys.argv) > 4 else 2.5
    sure = float(sys.argv[5]) if len(sys.argv) > 5 else 5.0
    K = float(sys.argv[6]) if len(sys.argv) > 6 else 4e-6
    genlik = float(sys.argv[7]) if len(sys.argv) > 7 else 1100.0
    t0 = time.time()
    maske, sinir = maske_yukle("veri/maske.json")
    dzk = duzlem_kur(maske, sinir, h_km=kaba_h, pay_km=pay)
    zk = np.load(f"{on}_z.npy").astype(float); Sk = np.load(f"{on}_S.npy").astype(float)
    # ince ızgara: kıtanın (model karası ya da maske) çevresi + 150 km
    kara_k = (zk > 0) | dzk.kara
    r, c = np.nonzero(kara_k)
    m = int(150.0 / kaba_h) + 1
    x0, x1 = dzk.x[max(c.min() - m, 0)], dzk.x[min(c.max() + m, len(dzk.x) - 1)]
    y0, y1 = dzk.y[max(r.min() - m, 0)], dzk.y[min(r.max() + m, len(dzk.y) - 1)]
    h = h_km * 1e3
    x = np.arange(x0, x1, h); y = np.arange(y0, y1, -h)
    X, Y = np.meshgrid(x, y)
    LO, LA = laea_geri(X, Y, dzk.lon0, dzk.lat0)
    cc = (X - dzk.x[0]) / dzk.h; rr = (dzk.y[0] - Y) / dzk.h
    z = ndimage.map_coordinates(zk, [rr, cc], order=3, mode="nearest")
    S = ndimage.map_coordinates(Sk, [rr, cc], order=1, mode="nearest")
    kara = ndimage.map_coordinates(zk, [rr, cc], order=1, mode="nearest") > 0
    print(f"ızgara {X.shape[0]}×{X.shape[1]}, {h_km} km", flush=True)
    zs, hedef, z_deniz = yapi_ve_asinma(z, S, kara, LA, h_km, sure, K, genlik, None, t0)
    sure_s = time.time() - t0
    son = f"{on}_yapi{h_km:g}km_g{genlik:g}"
    np.save(f"{son}_z.npy", zs.astype(np.float32))
    # sahibin maskesi ince ızgarada
    b, g, d, k = sinir
    H, W = maske.shape
    ic = (LO >= b) & (LO < d) & (LA > g) & (LA <= k)
    mr = np.clip(((k - LA) / (k - g) * H).astype(int), 0, H - 1); mc = np.clip(((LO - b) / (d - b) * W).astype(int), 0, W - 1)
    km = np.zeros(X.shape, bool); km[ic] = maske[mr[ic], mc[ic]]
    serbest = ciz(zs, kara, h)
    zm = np.where(km, np.maximum(zs, 5.0), np.minimum(np.where(kara, -50.0, zs), -1.0))
    maskeli = ciz(zm, km, h)
    for ad, im in (("serbest", serbest), ("maskeli", maskeli)):
        Wd = 1000; s = Wd / im.width
        im2 = im.resize((Wd, int(im.height * s)), Image.LANCZOS)
        ImageDraw.Draw(im2).text((8, 6), f"{'kıyı simülasyondan' if ad == 'serbest' else 'kıyı sahibin maskesinden'}; {h_km:g} km, {sure:g} milyon yıl aşınma",
                                 fill=(255, 255, 255), font=yazi_tipi(18))
        im2.save(f"{son}_{ad}.png")
    # yakın plan: en yüksek bölgenin çevresi, tam çözünürlük
    i, j = np.unravel_index(np.argmax(ndimage.gaussian_filter(np.where(kara, zs, 0), 20)), zs.shape)
    r0 = int(np.clip(i - 225, 0, max(zs.shape[0] - 450, 0))); c0 = int(np.clip(j - 350, 0, max(zs.shape[1] - 700, 0)))
    maskeli.crop((c0, r0, c0 + 700, r0 + 450)).save(f"{son}_yakin.png")
    print(f"en yüksek {zs.max():.0f} m; toplam {sure_s:.0f} s")


if __name__ == "__main__":
    main()
