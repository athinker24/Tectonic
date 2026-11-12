"""Aşama 3: tek çarpışmadan zaman kareleri ve animasyon.

Kullanım: python -m deneyler.tek_carpisma NSIDE K ETIKET [BASLANGIC_MA]
"""
import json
import sys
import time

import numpy as np
from PIL import Image

from tektonik.gorsel import kabartma, tuval_kur
from tektonik.izgara import izgara_kur, maske_oku
from tektonik.model import ModelAyar, kos
from tektonik.olaylar import Carpisma


def olcum(iz, tv, z):
    zi = np.where(tv.kara, z[tv.dugum], np.nan)
    dy = tv.derece * 111.19e3
    dx = dy * np.cos(np.radians(tv.lat))[:, None]
    gy, gx = np.gradient(zi)
    e = np.degrees(np.arctan(np.hypot(gx / dx, gy / dy)))
    LA = np.broadcast_to(tv.lat[:, None], zi.shape)
    kusak = np.isfinite(e) & (LA > 31.5) & (LA < 34.5)
    plato = iz.kara & (iz.lat > 35.5) & (iz.lat < 40) & (iz.lon > -25) & (iz.lon < 30)
    return dict(
        zmax=float(np.nanmax(zi)), kara_medyan=float(np.median(z[iz.kara])),
        kusak_egim_ortanca=float(np.nanmedian(e[kusak])), kusak_egim_p90=float(np.nanpercentile(e[kusak], 90)),
        kusak_z_ort=float(np.nanmean(zi[kusak])), kusak_z_p95=float(np.nanpercentile(zi[kusak], 95)),
        plato_z_ort=float(z[plato].mean()), plato_z_p10=float(np.percentile(z[plato], 10)), plato_z_p90=float(np.percentile(z[plato], 90)),
    )


def main():
    nside, k, etiket = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    bas = float(sys.argv[4]) if len(sys.argv) > 4 else 50.0
    n = float(sys.argv[5]) if len(sys.argv) > 5 else 2.0
    t0 = time.time()
    iz = izgara_kur(maske_oku("veri/test_maske.png"), nside=nside)
    cephe = np.array([[x, 31.2] for x in np.linspace(-37, 41, 40)])
    buyuk = Carpisma("Büyük çarpışma", cephe, ust_sol=True, baslangic_ma=bas, hiz_cm_yil=4.0,
                     kusak_km=280.0, plato_km=700.0, kusak_hmax_m=70_000.0, plato_hmax_m=44_000.0)
    son = kos(iz, [buyuk], bas, ModelAyar(k=k, n=n, m=n / 2.0, kare_myr=2.0))
    tv = tuval_kur(iz, derece=0.08 if nside >= 512 else 0.16)
    kareler = []
    for ma, z in son.kareler:
        im = kabartma(iz, z, tv)
        kareler.append(im)
    kareler[-1].save(f"cikti/{etiket}_son.png")
    # animasyon: küçültülmüş, son karede bekle
    kucuk = [im.resize((im.width // 2, im.height // 2), Image.LANCZOS) for im in kareler]
    kucuk[0].save(f"cikti/{etiket}.gif", save_all=True, append_images=kucuk[1:] + [kucuk[-1]] * 6,
                  duration=180, loop=0, optimize=True)
    r = dict(etiket=etiket, nside=nside, hucre_km=round(iz.hucre_km, 1), k=k, n=n, baslangic_ma=bas,
             kare=len(kareler), sure_s=round(time.time() - t0, 1), **olcum(iz, tv, son.z),
             hmax_km=float(son.h[iz.kara].max() / 1e3), gunluk=son.gunluk)
    json.dump(r, open(f"cikti/{etiket}.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in r.items() if k != "gunluk"}, ensure_ascii=False))
    for g in son.gunluk[::2]:
        print("  ", g)


if __name__ == "__main__":
    main()
