"""Gerçek dünya deneyi: Afrika, Arabistan, Hindistan, Avrasya; kalıpsız ince levha + aşınma.

Kullanım: python -m deneyler.dunya [ETA0] [K] [H_KM] [OKYANUS]
Bugünkü kıyılar GMT earth_relief 10' verisinden (z > 0). Avrasya sabit; diğer bloklar
GPS ve levha modellerinden yuvarlanmış hızlarla iter (Hindistan 50 milyon yıldır,
Arabistan 25 milyon yıldır, Afrika baştan beri). Başlangıçta kabuk her yerde 35 km
(önceden var olan dağlar yok). Sonuç aynı ızgaraya örneklenmiş gerçek yükseklikle
karşılaştırılır.
"""
import json
import os
import sys
import time

import h5py
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from tektonik.gorsel import _DENIZ, _RENK
from tektonik.levha import duzlem_kur
from tektonik.levha_model import LevhaAyar, kos_levha
from tektonik.tarih import Asama, BlokTarihi, hareket_kutbu
from tektonik.yazi import yazi_tipi

SINIR = (-20.0, -36.0, 150.0, 72.0)  # batı, güney, doğu, kuzey

# Blok çokgenleri (boylam, enlem); kabaca levha sınırları. Kalan kara Avrasya.
HINDISTAN = [(61, 24), (66.5, 25), (67.5, 29), (69.5, 31.8), (72, 33.8), (74.5, 32.8), (78, 30.2), (81, 28.8),
             (84, 27.6), (88, 26.8), (92, 26.9), (95.5, 27.8), (94, 24.5), (92.5, 21), (90, 5), (75, 2), (61, 12)]
ARABISTAN = [(33.8, 28.5), (35.2, 32.5), (36.4, 36.3), (39, 37), (42, 37.6), (45.5, 35.6), (47.8, 32.5),
             (50, 30), (53, 27.6), (56.4, 26.8), (60, 22), (54, 15), (44, 12.3), (42.5, 15), (37, 21)]


# Sert bölgeler (kratonlar ve katı havzalar), genel bilgiyle kabaca çizildi; kesin harita değil.
SERT = {
    "Tarim": [(76, 39.5), (78, 37.3), (83, 36.8), (88, 37.5), (90, 39), (89, 40.5), (84, 41.8), (79, 41), (76, 40.5)],
    "Junggar": [(83, 45), (86, 44.2), (90, 44.5), (91, 46), (88, 47), (84, 46.5)],
    "Sichuan": [(103, 29), (106, 28.5), (108.5, 30), (108, 32), (106, 32.5), (104, 31.5)],
    "Ordos": [(106, 35), (110, 35), (111, 38), (110, 40), (107, 39.5), (106, 37.5)],
    "Kuzey Çin": [(111, 35), (118, 34), (122, 38), (120, 41), (114, 42), (111, 40)],
    "Sibirya kalkanı": [(90, 60), (100, 55), (110, 55), (120, 56), (130, 60), (130, 68), (115, 73), (95, 72), (88, 68)],
    "Doğu Avrupa kalkanı": [(24, 50), (30, 46.5), (40, 46), (50, 48), (56, 52), (58, 60), (50, 66), (35, 69), (28, 60), (22, 55)],
}


def cokgen_ici(lon, lat, p):
    p = np.asarray(p, float)
    ic = np.zeros(lon.shape, bool)
    j = len(p) - 1
    for i in range(len(p)):
        xi, yi, xj, yj = p[i, 0], p[i, 1], p[j, 0], p[j, 1]
        kes = ((yi > lat) != (yj > lat)) & (lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-12) + xi)
        ic ^= kes
        j = i
    return ic


def gercek_yukseklik():
    f = h5py.File("veri/dunya/earth_relief_10m_p.grd", "r")
    lon, lat = f["lon"][:], f["lat"][:]
    z = f["z"][:].astype(np.float32) * float(f["z"].attrs.get("scale_factor", [1.0])[0])
    if lat[0] < lat[-1]:
        lat, z = lat[::-1], z[::-1]
    b, g, d, k = SINIR
    ci = (lon >= b) & (lon < d)
    ri = (lat > g) & (lat <= k)
    return z[np.ix_(ri, ci)], lon[ci], lat[ri]


def kabartma(dz, z, olcek=2, isaret=None):
    zz = np.where(dz.kara, z, 0.0)
    rgb = np.stack([np.interp(np.clip(zz, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    gy, gx = np.gradient(zz * 4, dz.h)
    rgb = rgb * np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9, 0.3, 1.3)[..., None]
    rgb = np.where(dz.kara[..., None], rgb, _DENIZ)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    return im.resize((im.width * olcek, im.height * olcek), Image.LANCZOS)


def kutu(dz, lo0, lo1, la0, la1):
    return dz.kara & (dz.lon >= lo0) & (dz.lon <= lo1) & (dz.lat >= la0) & (dz.lat <= la1)


BOLGELER = {
    "Tibet platosu (80-95°D, 30-36°K)": (80, 95, 30, 36),
    "Himalaya (78-92°D, 27-30°K)": (78, 92, 27, 30),
    "Zagros (46-56°D, 28-34°K)": (46, 56, 28, 34),
    "İran platosu (53-62°D, 30-36°K)": (53, 62, 30, 36),
    "Alpler (6-14°D, 45-47,5°K)": (6, 14, 45, 47.5),
    "Tien Şan (75-88°D, 40-44°K)": (75, 88, 40, 44),
    "Moğolistan (95-110°D, 44-50°K)": (95, 110, 44, 50),
    "Sibirya (60-120°D, 55-68°K)": (60, 120, 55, 68),
}


def main():
    eta0 = float(sys.argv[1]) if len(sys.argv) > 1 else 1e22
    k = float(sys.argv[2]) if len(sys.argv) > 2 else 4e-9
    h_km = float(sys.argv[3]) if len(sys.argv) > 3 else 50.0
    oky = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    avr_km = float(sys.argv[5]) if len(sys.argv) > 5 else 700.0
    sert = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0  # sert bölge viskozite çarpanı (1 = yok)
    yagis = (sys.argv[7] == "1") if len(sys.argv) > 7 else False
    tasima = (sys.argv[8] == "1") if len(sys.argv) > 8 else False
    kenar_km = float(sys.argv[9]) if len(sys.argv) > 9 else 150.0  # sert bölge kenar yumuşatması
    t0 = time.time()
    os.makedirs("cikti/dunya", exist_ok=True)
    on = f"cikti/dunya/dunya_{h_km:g}km_eta{eta0:.0e}_k{k:.0e}_o{oky:g}_avr{avr_km:g}_s{sert:g}_y{int(yagis)}_t{int(tasima)}_kn{kenar_km:g}"

    zr, lon_r, lat_r = gercek_yukseklik()
    maske = zr > 0
    dz = duzlem_kur(maske, SINIR, h_km=h_km, pay_km=500.0)
    ny, nx = dz.sekil
    # gerçek yükseklik ızgaraya: hücre içindeki ortalama (kara)
    b, g, d, kk = SINIR
    H, W = zr.shape
    LO, LA = np.meshgrid(lon_r, lat_r)
    from tektonik.levha import laea_ileri
    px, py = laea_ileri(LO, LA, dz.lon0, dz.lat0)
    jx = np.clip(np.round((px - dz.x[0]) / dz.h).astype(int), 0, nx - 1)
    iy = np.clip(np.round((dz.y[0] - py) / dz.h).astype(int), 0, ny - 1)
    top = np.zeros(dz.sekil); say = np.zeros(dz.sekil)
    np.add.at(top, (iy, jx), np.where(zr > 0, zr, 0)); np.add.at(say, (iy, jx), 1)
    gercek = np.where(say > 0, top / np.maximum(say, 1), 0)
    gercek = np.where(dz.kara, gercek, 0)
    print(f"ızgara {ny}×{nx}, hücre {h_km} km, kara {dz.kara.sum()}", flush=True)

    blok = np.where(dz.kara, 0, -1)  # 0 Avrasya
    adlar = ["Avrasya", "Afrika", "Arabistan", "Hindistan"]
    hin = dz.kara & cokgen_ici(dz.lon, dz.lat, HINDISTAN)
    ara = dz.kara & cokgen_ici(dz.lon, dz.lat, ARABISTAN)
    afr = dz.kara & ~ara & ((dz.lat < 35.95) & ((dz.lon < 33.0) | (dz.lat < 29.5)) & (dz.lon < 52))
    afr &= ~((dz.lon > 22) & (dz.lon < 36) & (dz.lat > 34.4))  # Girit, Kıbrıs Avrasya
    blok[afr] = 1; blok[ara] = 2; blok[hin] = 3

    def merkez(m):
        return float(dz.lon[m].mean()), float(dz.lat[m].mean())

    def tarih(ad, m, asamalar):
        c = merkez(m)
        out = []
        for bas, bit, yon, hiz in asamalar:
            lo, la, w = hareket_kutbu(c, yon, hiz)
            out.append(Asama(bas, bit, lo, la, w))
        return BlokTarihi(ad, out)

    tarihler = {
        "Hindistan": tarih("Hindistan", hin, [(50, 20, 20, 5.0), (20, 0, 15, 4.0)]),
        "Arabistan": tarih("Arabistan", ara, [(25, 0, -15, 2.0)]),
        "Afrika": tarih("Afrika", afr, [(50, 0, -30, 0.6)]),
    }
    ayar = LevhaAyar(eta0=eta0, k=k, okyanus=oky, cekirdek_ozel={"Avrasya": avr_km}, yagis=yagis, tasima=tasima)
    carpan = np.ones(dz.sekil)
    if sert != 1.0:
        m = np.zeros(dz.sekil, bool)
        for c in SERT.values():
            m |= cokgen_ici(dz.lon, dz.lat, c)
        w = ndimage.gaussian_filter(m.astype(float), kenar_km / h_km)
        carpan = np.exp(np.log(sert) * np.clip(w * 2, 0, 1))
    son = kos_levha(dz, blok, adlar, tarihler, 50.0, ayar,
                    gunluk_yaz=lambda gun: print(gun, f"{time.time() - t0:.0f} s", flush=True), eta_carpan=carpan)
    z = son.z

    olc = {}
    for ad, (a0, a1, b0, b1) in BOLGELER.items():
        m = kutu(dz, a0, a1, b0, b1)
        olc[ad] = dict(model_ortanca=round(float(np.median(z[m]))), gercek_ortanca=round(float(np.median(gercek[m]))),
                       model_p95=round(float(np.percentile(z[m], 95))), gercek_p95=round(float(np.percentile(gercek[m], 95))))
    hip = {}
    for esik in (1000, 2000, 3000, 4000):
        hip[f">{esik} m Mkm²"] = dict(model=round(float((z[dz.kara] > esik).sum() * h_km ** 2 / 1e6), 2),
                                      gercek=round(float((gercek[dz.kara] > esik).sum() * h_km ** 2 / 1e6), 2))
    # görsel: model | gerçek, aynı izdüşüm ve renk
    a_im, b_im = kabartma(dz, z, 2), kabartma(dz, gercek, 2)
    W2 = a_im.width
    tuv = Image.new("RGB", (W2 * 2 + 12, a_im.height + 30), "white")
    tuv.paste(a_im, (0, 30)); tuv.paste(b_im, (W2 + 12, 30))
    dr = ImageDraw.Draw(tuv)
    dr.text((6, 5), f"Model (kalıpsız, η0 {eta0:.0e}, K {k:.0e})", fill=(0, 0, 0), font=yazi_tipi(18))
    dr.text((W2 + 18, 5), "Gerçek (GMT earth_relief, aynı ızgara)", fill=(0, 0, 0), font=yazi_tipi(18))
    tuv.save(f"{on}_karsilastirma.png")
    if son.yagis is not None:
        yg = np.clip(son.yagis / 2.5, 0, 1)
        rgb = np.stack([200 - 170 * yg, 190 - 60 * yg, 140 + 80 * yg], -1)
        rgb = np.where(dz.kara[..., None], rgb, 235).astype(np.uint8)
        Image.fromarray(rgb).resize((dz.sekil[1] * 2, dz.sekil[0] * 2), Image.NEAREST).save(f"{on}_yagis.png")
    np.save(f"{on}_z.npy", z.astype(np.float32))
    r = dict(eta0=eta0, k=k, h_km=h_km, okyanus=oky, avrasya_cekirdek_km=avr_km, sert=sert, yagis=yagis, tasima=tasima, sure_s=round(time.time() - t0), bolgeler=olc, hipsometri=hip,
             gunluk=son.gunluk)
    json.dump(r, open(f"{on}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for ad, v in olc.items():
        print(f"{ad}: model {v['model_ortanca']} m (p95 {v['model_p95']}), gerçek {v['gercek_ortanca']} m (p95 {v['gercek_p95']})")
    print(hip)


if __name__ == "__main__":
    main()
