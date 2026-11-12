"""Örnek tabanlı kabartmanın üzerinde kısa aşınma koşusu: vadileri keskinleştir, nehir ağını birleştir.

Kullanım: python -m deneyler.asindir_son [Z_NPY] [SURE_MYR] [K]

Lat-lon 0,1° kabartma, kıtanın ortasına yerleşen Lambert eşit alanlı 10 km düzenli ızgaraya
taşınır; fastscapelib ile akarsu aşınması (m 0,5, n 1, deniz sabit taban, çukurlar en düşük
eşikten taşar) ve 80 km bükülmeyle izostatik geri sıçrama (0,85) koşulur; sonuç lat-lon'a geri
örneklenir. Büyük nehirler (drenaj alanı > 80 000 km²) mavi çizilir.
"""
import sys
import time

import fastscapelib as fs
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from tektonik.gorsel import _DENIZ, _RENK
from tektonik.izgara import maske_yukle
from tektonik.levha import duzlem_kur, laea_ileri
from tektonik.yazi import yazi_tipi

DER = 0.1


def latlon_izgara():
    maske, sinir = maske_yukle("veri/maske.json")
    b, g, d_, k = sinir
    lon = np.arange(b, d_, DER) + DER / 2
    lat = np.arange(k, g, -DER) - DER / 2
    LO, LA = np.meshgrid(lon, lat)
    H, W = maske.shape
    kara = maske[np.clip(((k - LA) / (k - g) * H).astype(int), 0, H - 1), np.clip(((LO - b) / (d_ - b) * W).astype(int), 0, W - 1)]
    return maske, sinir, lon, lat, LO, LA, kara


def gorsel(z, kara, LA, nehir=None, baslik=""):
    rgb = np.stack([np.interp(np.clip(z, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    dyy = DER * 111.19e3
    gy, gx = np.gradient(z * 3, dyy)
    gx = gx / np.cos(np.radians(LA))
    rgb = rgb * np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9, 0.3, 1.3)[..., None]
    if nehir is not None:
        rgb = np.where(nehir[..., None], np.array([60, 110, 190]), rgb)
    rgb = np.where(kara[..., None], rgb, _DENIZ)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    if baslik:
        ImageDraw.Draw(im).text((8, 6), baslik, fill=(0, 0, 0), font=yazi_tipi(16))
    return im


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else "cikti/nakil3_4_z.npy"
    sure = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    K = float(sys.argv[3]) if len(sys.argv) > 3 else 5e-7
    t0 = time.time()
    maske, sinir, lon, lat, LO, LA, kara_ll = latlon_izgara()
    z_ll = np.load(yol).astype(float)

    dz = duzlem_kur(maske, sinir, h_km=10.0, pay_km=60.0)
    ny, nx = dz.sekil
    # lat-lon -> düzlem
    r = (sinir[3] - dz.lat) / DER - 0.5
    c = (dz.lon - sinir[0]) / DER - 0.5
    z = ndimage.map_coordinates(z_ll, [r, c], order=1, mode="nearest")
    kara = dz.kara
    z = np.where(kara, np.maximum(z, 0), 0.0)
    durum = {(int(i), int(j)): fs.NodeStatus.FIXED_VALUE for i, j in zip(*np.nonzero(~kara))}
    grid = fs.RasterGrid([ny, nx], [dz.h, dz.h], fs.NodeStatus.FIXED_VALUE, durum)
    router = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
    eroder = fs.SPLEroder(router, K, 0.5, 1.0, 1e-4)
    dt = 2e4
    n = int(round(sure * 1e6 / dt))
    kar = kara.astype(float)
    sig = 80.0 / 10.0
    top_e = np.zeros(dz.sekil)
    for i in range(n):
        zf = z.copy()
        router.update_routes(zf)
        A = np.asarray(router.accumulate(1.0))
        e = np.asarray(eroder.erode(zf, A, dt)).reshape(dz.sekil)
        e = np.where(kara, e, 0.0)
        reb = ndimage.gaussian_filter(e, sig) / np.maximum(ndimage.gaussian_filter(kar, sig), 1e-6)
        z = np.where(kara, np.maximum(z - e + 0.85 * reb, 0.0), 0.0)
        top_e += e
    router.update_routes(z.copy())
    A = np.asarray(router.accumulate(1.0)).reshape(dz.sekil)
    print(f"{n} adım, {time.time() - t0:.0f} s; ortalama aşınma {top_e[kara].mean():.0f} m, en çok {top_e.max():.0f} m", flush=True)

    # düzlem -> lat-lon
    px, py = laea_ileri(LO, LA, dz.lon0, dz.lat0)
    cc = (px - dz.x[0]) / dz.h
    rr = (dz.y[0] - py) / dz.h
    z2 = ndimage.map_coordinates(z, [rr, cc], order=1, mode="nearest")
    A2 = ndimage.map_coordinates(A, [rr, cc], order=0, mode="nearest")
    z2 = np.where(kara_ll, z2, 0.0)
    nehir = kara_ll & (A2 > 8e10)
    once = gorsel(np.where(kara_ll, z_ll, 0), kara_ll, LA, None, "Aşınmadan önce")
    sonra = gorsel(z2, kara_ll, LA, None, f"{sure:g} milyon yıl aşınmadan sonra")
    ag = gorsel(z2, kara_ll, LA, nehir, "Sonra, büyük nehirlerle")
    W, Hh = once.size
    tuv = Image.new("RGB", (W, Hh * 3 + 20), "white")
    for i, im in enumerate((once, sonra, ag)):
        tuv.paste(im, (0, i * (Hh + 10)))
    on = yol.replace("_z.npy", "")
    tuv.save(f"{on}_asinma.png")
    sonra.save(f"{on}_asinmis.png")
    ag.save(f"{on}_nehirli.png")
    np.save(f"{on}_asinmis_z.npy", z2.astype(np.float32))
    print(f"en yüksek {z2.max():.0f} m, kara ortanca {np.median(z2[kara_ll]):.0f} m, toplam {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
