"""İnce viskoz levha ile kalıpsız dağ oluşumu (sahibin maskesi ve blokları).

Kullanım: python -m deneyler.levha_deneme [ETA0] [H_KM] [ADAY]
ETA0: 1e-15 /s gerinim hızındaki referans viskozite (Pa s), varsayılan 2e22.
Bloklar ve hızları cikti/gercek/adaylar.json içindeki adaydan (varsayılan 443) gelir;
çarpışma kalıpları KULLANILMAZ. Dağlar blok çekirdeklerine dayatılan hızlardan,
levhanın akışıyla doğar.
"""
import json
import os
import sys
import time

import fastscapelib as fs
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree

from tektonik.bloklar import bloklara_ayir
from tektonik.gorsel import _DENIZ, _RENK
from tektonik.izgara import _lonlat_xyz, izgara_kur, maske_yukle
from tektonik.levha import SANIYE_YIL, LevhaCozucu, duzlem_kur, laea_ileri
from tektonik.uretici import aday_kur
from tektonik.yazi import yazi_tipi

AIRY = 1 - 2800 / 3300


def yerel_eksenler(dz, lon, lat):
    """Coğrafi doğu ve kuzey birim yönlerinin ızgaradaki karşılığı."""
    e = 0.01
    x0, y0 = laea_ileri(lon, lat, dz.lon0, dz.lat0)
    xe, ye = laea_ileri(lon + e / np.cos(np.radians(lat)), lat, dz.lon0, dz.lat0)
    xn, yn = laea_ileri(lon, lat + e, dz.lon0, dz.lat0)
    de = np.stack([xe - x0, ye - y0]); de /= np.linalg.norm(de, axis=0)
    dn = np.stack([xn - x0, yn - y0]); dn /= np.linalg.norm(dn, axis=0)
    return de, dn


def kabartma(dz, z, olcek=2):
    zz = np.where(dz.kara, z, 0.0)
    rgb = np.stack([np.interp(np.clip(zz, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    gy, gx = np.gradient(zz * 4, dz.h)
    isik = np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9 * 1.0, 0.3, 1.3)
    rgb = rgb * isik[..., None]
    rgb = np.where(dz.kara[..., None], rgb, _DENIZ)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    return im.resize((im.width * olcek, im.height * olcek), Image.LANCZOS)


def renkli(a, lo, hi, cmap=((40, 60, 140), (240, 240, 240), (170, 40, 30))):
    t = np.clip((a - lo) / (hi - lo), 0, 1)
    c = np.array(cmap, float)
    s = t * (len(c) - 1); i = np.clip(s.astype(int), 0, len(c) - 2); f = (s - i)[..., None]
    return (c[i] * (1 - f) + c[i + 1] * f).astype(np.uint8)


def main():
    eta0 = float(sys.argv[1]) if len(sys.argv) > 1 else 2e22
    h_km = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0
    no = int(sys.argv[3]) if len(sys.argv) > 3 else 443
    zayif_min = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
    cek_km = float(sys.argv[5]) if len(sys.argv) > 5 else 400.0
    okyanus = float(sys.argv[6]) if len(sys.argv) > 6 else 0.1
    zay_ger = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0  # gerinim zayıflaması ölçeği (0 = yok)
    t0 = time.time()
    etiket = f"levha_{no}_{h_km:g}km_eta{eta0:.0e}_z{zayif_min:g}_c{cek_km:g}_o{okyanus:g}_g{zay_ger:g}"
    os.makedirs("cikti/levha", exist_ok=True)
    on = f"cikti/levha/{etiket}"

    maske, sinir = maske_yukle("veri/maske.json")
    sen = json.load(open("veri/senaryo.json", encoding="utf-8"))
    dz = duzlem_kur(maske, sinir, h_km=h_km)
    ny, nx = dz.sekil
    print(f"ızgara {ny}×{nx}, hücre {h_km} km, kara {dz.kara.sum()}")

    # bloklar ve kinematik: HEALPix'teki blok etiketleri ve aday tarihi
    iz = izgara_kur(maske, sinir, nside=128)
    bl = bloklara_ayir(iz, sen)
    rapor = json.load(open("cikti/gercek/adaylar.json", encoding="utf-8"))
    p = next(a["parametre"] for a in rapor["secilen"] if a["no"] == no)
    aday = aday_kur(no, np.random.default_rng(0), iz, bl, sen, p)
    ki = np.flatnonzero(iz.kara)
    _, j = cKDTree(iz.xyz[ki]).query(_lonlat_xyz(dz.lon[dz.kara], dz.lat[dz.kara]))
    blok = np.full(dz.sekil, -1)
    blok[dz.kara] = bl.etiket[ki[j]]

    # blok çekirdekleri: başka bloğun karasına 400 km'den uzak hücreler
    cekirdek = {}
    sinira = np.full(dz.sekil, np.inf)
    # levhalar: her hücre (kara ya da deniz) en yakın bloğun levhasına ait (Voronoi);
    # denizdeki hücreler bloklarıyla birlikte hareket eder, yalnızca levha sınırları deforme olur
    _, (ri, ci) = ndimage.distance_transform_edt(blok < 0, return_indices=True)
    levha = blok[ri, ci]
    for b, ad in enumerate(bl.adlar):
        diger = dz.kara & (blok != b) & (blok >= 0)
        d = ndimage.distance_transform_edt(~diger) * h_km
        dl = ndimage.distance_transform_edt(levha == b) * h_km  # levha sınırına uzaklık
        cekirdek[ad] = (levha == b) & (d > cek_km) & (dl > 0.5 * cek_km)
        sinira = np.where(blok == b, np.minimum(sinira, d), sinira)

    # reoloji: kıta η0, okyanus çok zayıf (iletmez), genç blok sınırları zayıf
    zayif = np.where(dz.kara, np.clip(sinira / 150.0, zayif_min, 1.0), 1.0)
    eta_taban = np.where(dz.kara, eta0 * zayif, eta0 * okyanus)

    S = np.full(dz.sekil, 35e3)
    z = np.zeros(dz.sekil)
    g = np.random.default_rng(3).standard_normal(dz.sekil)
    g = ndimage.gaussian_filter(g, 3) ; g /= g.std()
    kiyi = ndimage.distance_transform_edt(dz.kara) * h_km
    z = np.where(dz.kara, np.clip(100 + 40 * g, 0, None) * np.clip(kiyi / 150, 0, 1), 0)

    # aşınma: fastscapelib düzenli ızgarası, deniz sabit taban
    durum = {(int(a), int(b)): fs.NodeStatus.FIXED_VALUE for a, b in zip(*np.nonzero(~dz.kara))}
    grid = fs.RasterGrid([ny, nx], [dz.h, dz.h], fs.NodeStatus.FIXED_VALUE, durum)
    router = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
    klit = 4e-9 * np.exp(0.5 * ndimage.gaussian_filter(np.random.default_rng(5).standard_normal(dz.sekil), 2) * 2)
    eroder = fs.SPLEroder(router, klit, 1.0, 2.0, 1e-4)

    coz = LevhaCozucu(dz)
    _, (rk, ck) = ndimage.distance_transform_edt(~dz.kara, return_indices=True)
    de, dn = yerel_eksenler(dz, dz.lon, dz.lat)
    bas = float(np.ceil(max(a.baslangic_ma for t in aday.tarihler.values() for a in t.asamalar)))
    bas = min(bas, 60.0)
    dt_myr, alt = 0.5, 5
    kareler, gunluk = [], []
    u = v = np.zeros(dz.sekil)
    gerinim = np.zeros(dz.sekil)  # biriken gerinim (boyutsuz)
    ma = bas
    while ma > 1e-6:
        # dayatılan hızlar: her blok çekirdeği o andaki (sabit bloğa göre) hızıyla
        sabit = np.zeros(dz.sekil, bool)
        u0 = np.zeros(dz.sekil); v0 = np.zeros(dz.sekil)
        sabit[[0, -1], :] = True; sabit[:, [0, -1]] = True
        for ad in bl.adlar:
            m = cekirdek[ad]
            if not m.any():
                continue
            sabit |= m
            if ad in aday.tarihler:
                xyz = _lonlat_xyz(dz.lon[m], dz.lat[m])
                vel = aday.tarihler[ad].hiz_cm_yil(ma - 0.25 * dt_myr, xyz) / 100 / SANIYE_YIL  # m/s, 3B
                lo, la = np.radians(dz.lon[m]), np.radians(dz.lat[m])
                ev = np.stack([-np.sin(lo), np.cos(lo), np.zeros_like(lo)], 1)
                nv = np.stack([-np.sin(la) * np.cos(lo), -np.sin(la) * np.sin(lo), np.cos(la)], 1)
                ve, vn = (vel * ev).sum(1), (vel * nv).sum(1)
                u0[m] = ve * de[0][m] + vn * dn[0][m]
                v0[m] = ve * de[1][m] + vn * dn[1][m]
        # kıyıda yapay itme olmasın: denizdeki hücrelere en yakın karanın kalınlığı (Γ için)
        Sg = S[rk, ck]
        # üstel yasa: Picard yinelemesi
        # gerinim zayıflaması: kırılan, ısınan kuşak zayıflar ve deformasyonu üzerine çeker
        zay = np.maximum(0.05, np.exp(-gerinim / zay_ger)) if zay_ger > 0 else 1.0
        eta_t = eta_taban * zay
        eta = eta_t.copy()
        for _ in range(4):
            u, v = coz.coz(eta, Sg, sabit, u0, v0)
            ekk, eE = coz.gerinim(u, v)
            eta = np.clip(eta_t * (np.maximum(eE, 1e-18) / 1e-15) ** (1 / 3 - 1), 1e20, 1e25)
        gerinim = gerinim + eE * dt_myr * 1e6 * SANIYE_YIL
        dS = np.where(dz.kara, -S * ekk * dt_myr * 1e6 * SANIYE_YIL, 0.0)
        dS = np.clip(dS, -0.2 * S, 30e3)
        S = np.where(dz.kara, np.clip(S + dS, 20e3, 85e3), 35e3)
        # bölgesel izostazi: uzun dalga boyu kabuktan (80 km bükülme), kısa dalga boyu aşınma kabartısı
        kar = dz.kara.astype(float)
        def gk(a):
            return ndimage.gaussian_filter(a * kar, 80 / h_km) / np.maximum(ndimage.gaussian_filter(kar, 80 / h_km), 1e-6)
        z = np.where(dz.kara, (z - gk(z)) + AIRY * (gk(S) - 33e3) * np.clip(kiyi / 60, 0, 1), 0.0)
        z = np.where(dz.kara, np.maximum(z, 0.0), 0.0)
        for _ in range(alt):
            zf = z.copy()
            router.update_routes(zf)
            A = np.asarray(router.accumulate(1.0))
            e = np.asarray(eroder.erode(zf, A, dt_myr / alt * 1e6)).reshape(dz.sekil)
            z = z - e
            S = S - np.where(dz.kara, e, 0)
            z = np.where(dz.kara, np.maximum(z, 0.0), 0.0)
        ma = round(ma - dt_myr, 6)
        if abs(ma / 2 - round(ma / 2)) < 1e-6:
            kareler.append((ma, z.copy(), S.copy(), eE.copy()))
            gunluk.append(dict(ma=ma, zmax=float(z.max()), Smax_km=float(S[dz.kara].max() / 1e3),
                               vmax_cm=float(np.hypot(u, v)[dz.kara].max() * SANIYE_YIL * 100),
                               zort=float(z[dz.kara].mean()),
                               kara_hacim_km3_yil=float(np.sum(-ekk[dz.kara] * Sg[dz.kara]) * dz.h ** 2 * SANIYE_YIL / 1e9),
                               deniz_hacim_km3_yil=float(np.sum(-ekk[~dz.kara] * Sg[~dz.kara]) * dz.h ** 2 * SANIYE_YIL / 1e9),
                               asinma_km3_yil=float(np.sum(e[dz.kara]) * dz.h ** 2 / (dt_myr / alt * 1e6) / 1e9)))
            print(gunluk[-1], f"{time.time() - t0:.0f} s", flush=True)

    kabartma(dz, z).save(f"{on}_son.png")
    # üçlü: kabartma, kabuk kalınlığı, gerinim hızı
    k = kabartma(dz, z, 2)
    kb = Image.fromarray(np.where(dz.kara[..., None], renkli(S / 1e3, 30, 70), 200).astype(np.uint8))
    gr = Image.fromarray(np.where(dz.kara[..., None], renkli(np.log10(np.maximum(kareler[-1][3], 1e-18)), -17, -14.5), 200).astype(np.uint8))
    kb = kb.resize(k.size, Image.NEAREST); gr = gr.resize(k.size, Image.NEAREST)
    uc = Image.new("RGB", (k.width * 3 + 20, k.height + 26), "white")
    for i, (im, ad) in enumerate([(k, "kabartma"), (kb, "kabuk kalınlığı 30 ile 70 km"), (gr, "gerinim hızı (log)")]):
        uc.paste(im, (i * (k.width + 10), 26))
        ImageDraw.Draw(uc).text((i * (k.width + 10) + 4, 4), ad, fill=(0, 0, 0), font=yazi_tipi(16))
    uc.save(f"{on}_uclu.png")
    ims = []
    for ma, zz, SS, _ in kareler:
        im = kabartma(dz, zz, 1)
        ImageDraw.Draw(im).text((6, 4), f"{ma:.0f} milyon yıl önce", fill=(0, 0, 0), font=yazi_tipi(14))
        ims.append(im)
    ims[0].save(f"{on}.gif", save_all=True, append_images=ims[1:] + [ims[-1]] * 6, duration=200, loop=0)
    np.save(f"{on}_z.npy", z.astype(np.float32))
    r = dict(eta0=eta0, h_km=h_km, aday=no, sure_s=round(time.time() - t0), zmax=float(z.max()),
             kara_ortanca=float(np.median(z[dz.kara])), kara_p90=float(np.percentile(z[dz.kara], 90)),
             Smax_km=float(S[dz.kara].max() / 1e3), gunluk=gunluk)
    json.dump(r, open(f"{on}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print({k: v for k, v in r.items() if k != "gunluk"})


if __name__ == "__main__":
    main()
