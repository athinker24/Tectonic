"""Çarpışma laboratuvarı denemesi: güneydeki kıta okyanusu geçip kuzeydeki kıtaya çarpar.

Kullanım: python -m deneyler.carpisma_lab [SURE_MYR] [H_KM] [HIZ_CM]
Çıktı: cikti/lab/ (animasyon, son harita, kuzey güney kesitleri).
"""
import json
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from tektonik.gorsel import _RENK
from tektonik.lab import Lab, LabAyar
from tektonik.yazi import yazi_tipi

DENIZ_RENK = np.array([[-6000, 20, 50, 110], [-3000, 40, 90, 160], [-200, 110, 160, 210], [0, 160, 200, 225]], float)


def kita_bicimi(ny, nx, h_km, merkez, yaricap_km, tohum, uzama=(1.0, 1.0)):
    rng = np.random.default_rng(tohum)
    yy, xx = np.mgrid[0:ny, 0:nx].astype(float)
    dx = (xx - merkez[1]) * h_km / uzama[1]
    dy = (yy - merkez[0]) * h_km / uzama[0]
    r = np.hypot(dx, dy)
    g = ndimage.gaussian_filter(rng.standard_normal((ny, nx)), 6); g /= g.std()
    g2 = ndimage.gaussian_filter(rng.standard_normal((ny, nx)), 2); g2 /= g2.std()
    return r < yaricap_km * (1 + 0.18 * g + 0.05 * g2)


def resim(z, h_km, olcek=3):
    kara = z > 0
    rgb_k = np.stack([np.interp(np.clip(z, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    rgb_d = np.stack([np.interp(np.clip(z, -6000, 0), DENIZ_RENK[:, 0], DENIZ_RENK[:, i]) for i in (1, 2, 3)], -1)
    gy, gx = np.gradient(np.where(kara, z, 0) * 3, h_km * 1e3)
    isik = np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9, 0.3, 1.3)
    rgb = np.where(kara[..., None], rgb_k * isik[..., None], rgb_d)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    return im.resize((im.width * olcek, im.height * olcek), Image.BILINEAR)


def kesit(z, S, sutun, h_km, gen=600, yuk=260):
    """Kuzey güney kesit: yükselti (renk dolgulu) ve kabuk kalınlığı (çizgi)."""
    im = Image.new("RGB", (gen, yuk), "white")
    d = ImageDraw.Draw(im)
    p = z[:, sutun][::-1]  # güneyden kuzeye
    s = S[:, sutun][::-1] / 1e3
    n = len(p)
    xs = np.linspace(40, gen - 10, n)
    def zy(v):
        return 140 - v / 6000 * 120
    for i in range(n - 1):
        c = (110, 160, 210) if p[i] < 0 else (150, 120, 80)
        d.polygon([(xs[i], zy(p[i])), (xs[i + 1], zy(p[i + 1])), (xs[i + 1], zy(-6000) + 10), (xs[i], zy(-6000) + 10)], fill=c)
    d.line([(40, zy(0)), (gen - 10, zy(0))], fill=(60, 60, 200))
    for v in (-4000, 0, 2000, 4000, 6000):
        d.text((2, zy(v) - 6), f"{v // 1000} km", fill=(0, 0, 0), font=yazi_tipi(10))
    # kabuk kalınlığı: alt bölümde
    def sy(v):
        return yuk - 10 - (v - 0) / 90 * 90
    d.line(list(zip(xs, sy(s))), fill=(180, 40, 40), width=2)
    d.text((gen - 170, yuk - 100), "kırmızı: kabuk kalınlığı (0-90 km)", fill=(180, 40, 40), font=yazi_tipi(10))
    d.text((40, 2), "güney", fill=(0, 0, 0), font=yazi_tipi(11)); d.text((gen - 50, 2), "kuzey", fill=(0, 0, 0), font=yazi_tipi(11))
    return im


def main():
    sure = float(sys.argv[1]) if len(sys.argv) > 1 else 45.0
    h_km = float(sys.argv[2]) if len(sys.argv) > 2 else 15.0
    hiz = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
    os.makedirs("cikti/lab", exist_ok=True)
    ny, nx = int(5000 / h_km), int(3600 / h_km)
    # kuzey kıtası: geniş, güney kıyısı düzensiz
    kuzey = kita_bicimi(ny, nx, h_km, (-int(800 / h_km), nx // 2), 3500, 3, uzama=(1.0, 1.3))
    guney = kita_bicimi(ny, nx, h_km, (int(4150 / h_km), nx // 2), 560, 7, uzama=(1.0, 1.15))
    S0 = np.where(kuzey | guney, 35e3, 7e3)
    et = np.zeros((ny, nx))
    et[int(3000 / h_km):, :] = 1.0  # güneydeki levha (kıta + önündeki okyanus) gelen
    a = LabAyar(h_km=h_km, Te_km=float(sys.argv[4]) if len(sys.argv) > 4 else 30.0)
    lab = Lab(S0, et, (0.0, hiz), sure, a)
    t0 = time.time()
    kareler, kesitler = [], []
    sutun = nx // 2
    adim = int(round(sure / a.dt_myr))
    for i in range(adim):
        d = lab.adim()
        if i % 4 == 3 or i == adim - 1:
            im = resim(d.z, h_km, 2)
            ImageDraw.Draw(im).text((8, 6), f"{d.ma:.0f} milyon yıl önce", fill=(255, 255, 255), font=yazi_tipi(16))
            kareler.append(im)
            if i % 20 == 19 or i == adim - 1:
                g = d.gunluk[-1]
                print(f"{d.ma:5.1f} Ma  zmax {g['zmax']:5.0f} m  Smax {g['Smax_km']:4.1f} km  kara %{100 * g['kara_orani']:.0f}  "
                      f"temas {g['temas_ma']}  vmax {g['vmax_cm']:.1f} cm/yıl  aşınma {g['asinma_km3']:.0f} km³/adım  {time.time() - t0:.0f} s", flush=True)
            if i % 40 == 39 or i == adim - 1:
                kesitler.append((d.ma, d.z.copy(), d.S.copy()))
    on = f"cikti/lab/lab_{sure:g}my_{h_km:g}km_{hiz:g}cm"
    kareler[0].save(f"{on}.gif", save_all=True, append_images=kareler[1:] + [kareler[-1]] * 8, duration=150, loop=0)
    kareler[-1].save(f"{on}_son.png")
    ks = [kesit(z, S, sutun, h_km) for _, z, S in kesitler]
    tuv = Image.new("RGB", (600, 270 * len(ks)), "white")
    for i, ((ma, _, _), k) in enumerate(zip(kesitler, ks)):
        tuv.paste(k, (0, i * 270))
        ImageDraw.Draw(tuv).text((300, i * 270 + 2), f"{ma:.0f} milyon yıl önce", fill=(0, 0, 0), font=yazi_tipi(12))
    tuv.save(f"{on}_kesit.png")
    np.save(f"{on}_z.npy", lab.durum.z.astype(np.float32)); np.save(f"{on}_S.npy", lab.durum.S.astype(np.float32))
    json.dump(lab.durum.gunluk, open(f"{on}.json", "w"), indent=0)
    print(f"toplam {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
