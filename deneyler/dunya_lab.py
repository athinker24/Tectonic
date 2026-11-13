"""Gerçek dünyada çarpışma laboratuvarı: Hindistan, Arabistan, Afrika bugünkü kıyılarından geçmişe
geri sürülür, sonra ileri zamanda Avrasya'ya (sabit) karşı sürülür. Kalıp yok; başlangıçta kabuk her
yerde 35 km (bugünkü dağlar başlangıçta yok). Sonuç gerçek yükseklikle (GMT earth_relief 10') karşılaştırılır.

Kullanım: python -m deneyler.dunya_lab [H_KM] [BAS_MA] [AVR_CEKIRDEK_KM] [K] [SERT] [ZAYIF] [ZAYIF_KM]
          [SIZINTI] [SAHANLIK] [INCELME_KM] [KUBIK] [DIKIS_ESIK]  (varsayılanlar en iyi bilinen ayar)

Hızlar (Avrasya'ya göre, yuvarlanmış):
  Hindistan: 50 ile 20 Ma 5 cm/yıl N20°D, 20 ile 0 Ma 4 cm/yıl N15°D; çarpışma 50 Ma
             (Molnar ve Stock 2009 ile Zahirovic ve diğ. 2012 çarpışma sonrası yavaşlama).
  Arabistan: 25 Ma'ya dek Afrika ile birlikte; sonra Euler kutbu 27,5°K 17,6°D 0,404°/My
             (ArRajehi ve diğ. 2010); çarpışma 27 Ma
             (McQuarrie ve diğ. 2003; McQuarrie ve van Hinsbergen 2013).
  Afrika: 50 ile 25 Ma 2 cm/yıl kuzeye, sonra Euler kutbu 0,95°G 21,8°B 0,06°/My (McClusky ve diğ. 2003).
"""
import json
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.carpisma_lab import resim
from deneyler.dunya import ARABISTAN, SERT, BOLGELER, HINDISTAN, SINIR, cokgen_ici, gercek_yukseklik, kutu
from tektonik import kure
from tektonik.izgara import _lonlat_xyz
from tektonik.lab import LabAyar, LabCok
from tektonik.levha import duzlem_kur, laea_ileri
from tektonik.levha_model import yerel_eksenler
from tektonik.tarih import Asama, BlokTarihi, hareket_kutbu
from tektonik.yazi import yazi_tipi
from scipy.spatial import cKDTree

CARPISMA = {"Hindistan": 50.0, "Arabistan": 27.0}


def main():
    h_km = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0
    bas = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0
    avr = float(sys.argv[3]) if len(sys.argv) > 3 else 1500.0
    K = float(sys.argv[4]) if len(sys.argv) > 4 else 5e-7
    sert = float(sys.argv[5]) if len(sys.argv) > 5 else 10.0  # kratonların viskozite çarpanı (1 = yok)
    zay = float(sys.argv[6]) if len(sys.argv) > 6 else 0.3  # levha sınırı fay kuşağı viskozite çarpanı
    zay_km = float(sys.argv[7]) if len(sys.argv) > 7 else 150.0
    sizinti = (sys.argv[8] == "1") if len(sys.argv) > 8 else False
    sahan = (sys.argv[9] == "1") if len(sys.argv) > 9 else False  # sığ denizler (−200 m'den sığ) deniz altı kıta kabuğu
    incel = float(sys.argv[10]) if len(sys.argv) > 10 else 5.0  # incelen kıtanın zayıflaması (km), 0 kapalı
    kubik = (sys.argv[11] == "1") if len(sys.argv) > 11 else True
    dikis = float(sys.argv[12]) if len(sys.argv) > 12 else 0.02  # dar şerit kapanma eşiği (adım başına kısalma)
    t0 = time.time()
    os.makedirs("cikti/dunya_lab", exist_ok=True)
    on = f"cikti/dunya_lab/dl_{h_km:g}km_{bas:g}ma_avr{avr:g}_K{K:g}_s{sert:g}_z{zay:g}_{zay_km:g}_kk{int(sizinti)}_sh{int(sahan)}_in{incel:g}_kb{int(kubik)}_dk{dikis:g}"

    zr, lon_r, lat_r = gercek_yukseklik()
    dz = duzlem_kur(zr > 0, SINIR, h_km=h_km, pay_km=800.0)
    ny, nx = dz.sekil
    # gerçek yükseklik aynı ızgaraya (hücre ortalaması)
    LO, LA = np.meshgrid(lon_r, lat_r)
    px, py = laea_ileri(LO, LA, dz.lon0, dz.lat0)
    jx = np.clip(np.round((px - dz.x[0]) / dz.h).astype(int), 0, nx - 1)
    iy = np.clip(np.round((dz.y[0] - py) / dz.h).astype(int), 0, ny - 1)
    top = np.zeros(dz.sekil); say = np.zeros(dz.sekil)
    np.add.at(top, (iy, jx), zr); np.add.at(say, (iy, jx), 1)
    gercek = np.where(say > 0, top / np.maximum(say, 1), -4000.0)
    print(f"ızgara {ny}×{nx}, hücre {h_km} km", flush=True)

    blok = np.where(dz.kara, 0, -1)
    adlar = ["Avrasya", "Afrika", "Arabistan", "Hindistan"]
    hin = dz.kara & cokgen_ici(dz.lon, dz.lat, HINDISTAN)
    ara = dz.kara & cokgen_ici(dz.lon, dz.lat, ARABISTAN)
    afr = dz.kara & ~ara & ((dz.lat < 35.95) & ((dz.lon < 33.0) | (dz.lat < 29.5)) & (dz.lon < 52))
    afr &= ~((dz.lon > 22) & (dz.lon < 36) & (dz.lat > 34.4))
    blok[afr] = 1; blok[ara] = 2; blok[hin] = 3

    def tarih(ad, m, asamalar):
        c = (float(dz.lon[m].mean()), float(dz.lat[m].mean()))
        return BlokTarihi(ad, [Asama(b0, b1, *hareket_kutbu(c, yon, v)) for b0, b1, yon, v in asamalar])

    # Arabistan 25 milyon yıl öncesine dek Afrika ile tek levha (Kızıldeniz sonra açıldı); o dönemde
    # Afrika Avrasya'ya 2 cm/yıl yaklaşıyordu, 25 Ma'dan sonra 1 cm/yılın altına yavaşladı (McQuarrie ve diğ. 2003)
    # 25 Ma'dan bugüne GPS Euler kutupları (Avrasya'ya göre, saat yönünün tersine pozitif):
    # Arabistan 27,5°K 17,6°D 0,404°/My (ArRajehi ve diğ. 2010; erken Miyosen'den beri tutarlı),
    # Nubia 0,95°G 21,8°B 0,06°/My (McClusky ve diğ. 2003). Yakın kutup Arabistan'ı Afrika'dan döndürerek
    # ayırır: Kızıldeniz güneyde daha hızlı açılır.
    afr_t = tarih("Afrika", afr, [(80, 25, 0, 2.0)])
    afr_t.asamalar.append(Asama(25, 0, -21.8, -0.95, 0.06))
    ara_t = BlokTarihi("Arabistan", [Asama(25, 0, 17.6, 27.5, 0.404)])
    ara_t.asamalar.insert(0, Asama(80, 25, *[getattr(afr_t.asamalar[0], k) for k in ("kutup_lon", "kutup_lat", "hiz_derece_myr")]))
    tarihler = {
        "Hindistan": tarih("Hindistan", hin, [(80, 20, 20, 5.0), (20, 0, 15, 4.0)]),
        "Arabistan": ara_t,
        "Afrika": afr_t,
    }

    # başlangıç kabuğu: kara 35 km; sahanlık (istenirse) bugünkü derinliğe izostatik denk kalınlıkta kıta
    # kabuğu, en yakın kara bloğuna ait. z = (S − S_ref)(1 − ρc/ρm) + serbest bord.
    Sdeg = np.where(dz.kara, 35e3, 0.0)
    if sahan:
        sh = ~dz.kara & (gercek > -200)
        sh &= ndimage.distance_transform_edt(~dz.kara) * h_km <= 600  # kıtaya bağlı sahanlıklar
        _, (rb, cb) = ndimage.distance_transform_edt(blok < 0, return_indices=True)
        blok = np.where(sh, blok[rb, cb], blok)
        Sdeg = np.where(sh, 35e3 + (np.clip(gercek, -200, 0) - 300.0) / (1 - 2800.0 / 3300.0), Sdeg)
        print(f"sahanlık {sh.sum()} hücre", flush=True)
    S0 = np.full(dz.sekil, 7e3)
    L0 = np.full(dz.sekil, -1.0)
    for b, ad in enumerate(adlar):
        m = blok == b
        p0 = _lonlat_xyz(dz.lon[m], dz.lat[m])
        sv = Sdeg[m]
        xyz = p0
        if ad in tarihler:
            tr = tarihler[ad]
            xyz = kure.uygula(tr.geri_donme(bas), p0)
            tc = CARPISMA.get(ad, 0.0)
            if tc > 0:
                # Büyük uzantı: çarpışmadan bugüne itmenin süpürdüğü, bugün Avrasya karasına denk gelen koridor
                tc = min(tc, bas)
                kor = np.vstack([kure.uygula(tr.geri_donme(t), p0) for t in np.linspace(0, tc, 40)])
                bugun = kure.uygula(kure.ters(tr.geri_donme(tc)), kor)
                diger = blok == 0
                dd, _ = cKDTree(_lonlat_xyz(dz.lon[diger], dz.lat[diger])).query(bugun, distance_upper_bound=1.5 * dz.h / 6.371e6)
                kor = kor[np.isfinite(dd)]
                q = kure.carp(tr.geri_donme(bas), kure.ters(tr.geri_donme(tc)))
                xyz = np.vstack([xyz, kure.uygula(q, kor)])
                sv = np.r_[sv, np.full(len(kor), 35e3)]
                print(f"{ad}: çarpışma {tc:g} Ma, Büyük {ad} uzantısı {len(kor)} nokta", flush=True)
        lo, la = kure.xyz_lonlat(xyz)
        qx, qy = laea_ileri(np.asarray(lo), np.asarray(la), dz.lon0, dz.lat0)
        c = np.round((qx - dz.x[0]) / dz.h).astype(int)
        r = np.round((dz.y[0] - qy) / dz.h).astype(int)
        ok = (r >= 0) & (r < ny) & (c >= 0) & (c < nx)
        yer = np.zeros(dz.sekil, bool)
        yer[r[ok], c[ok]] = True
        deg = np.zeros(dz.sekil)
        np.maximum.at(deg, (r[ok], c[ok]), sv[ok])
        kapa = ndimage.binary_closing(yer, iterations=1) & ~yer  # döndürmede açılan tek hücrelik delikler
        deg = np.where(kapa, ndimage.maximum_filter(deg, 3), deg)
        yer |= kapa
        S0[yer] = deg[yer]
        L0[yer] = b
    kita0 = S0 > 20e3
    _, (ri, ci) = ndimage.distance_transform_edt(~kita0, return_indices=True)
    L0 = L0[ri, ci]

    a = LabAyar(h_km=h_km, dt_myr=0.5, kappa_max=3000.0, K=K, cek_gelen_km=400.0, cek_sabit_km=avr,
                 sinir_zayif=zay, sinir_km=zay_km, kiyi_sizinti=sizinti, incelme_km=incel, tasima_kubik=kubik, dikis_esik=dikis)
    lab = LabCok(S0, L0, bas, a, dz.lon, dz.lat, tarihler, adlar, "Avrasya", yerel_eksenler(dz, dz.lon, dz.lat))
    if sert != 1.0:
        # sert bölgeler bugünkü yerlerinde (Avrasya sabit olduğundan geri sürülmez); 50 km kenar yumuşatması
        ms = np.zeros(dz.sekil, bool)
        for cg in SERT.values():
            ms |= cokgen_ici(dz.lon, dz.lat, cg)
        w = ndimage.gaussian_filter(ms.astype(float), 50.0 / h_km)
        lab.eta_carpan = np.exp(np.log(sert) * np.clip(w * 2, 0, 1))
    kareler = []
    adim = int(round(bas / a.dt_myr))
    for i in range(adim):
        d = lab.adim()
        if i % 4 == 3 or i == adim - 1:
            im = resim(d.z, h_km, 2)
            ImageDraw.Draw(im).text((8, 6), f"{d.ma:.0f} milyon yıl önce", fill=(255, 255, 255), font=yazi_tipi(16))
            kareler.append(im)
        if i % 10 == 9 or i == adim - 1:
            g = d.gunluk[-1]
            print(f"{d.ma:5.1f} Ma  zmax {g['zmax']:5.0f} m  Smax {g['Smax_km']:4.1f} km  vmax {g['vmax_cm']:.1f} cm/yıl  "
                  f"{time.time() - t0:.0f} s", flush=True)
    kareler[0].save(f"{on}.gif", save_all=True, append_images=kareler[1:] + [kareler[-1]] * 8, duration=150, loop=0)
    z = lab.durum.z
    # model | gerçek yan yana, aynı izdüşüm ve renk
    a_im, b_im = resim(z, h_km, 2), resim(gercek, h_km, 2)
    W = a_im.width
    tuv = Image.new("RGB", (W * 2 + 12, a_im.height + 30), "white")
    tuv.paste(a_im, (0, 30)); tuv.paste(b_im, (W + 12, 30))
    dr = ImageDraw.Draw(tuv)
    dr.text((6, 5), f"Model: {bas:g} milyon yıllık çarpışma, kalıpsız", fill=(0, 0, 0), font=yazi_tipi(18))
    dr.text((W + 18, 5), "Gerçek (GMT earth_relief)", fill=(0, 0, 0), font=yazi_tipi(18))
    tuv.save(f"{on}_karsilastirma.png")
    np.save(f"{on}_z.npy", z.astype(np.float32))
    np.save(f"{on}_S.npy", lab.durum.S.astype(np.float32)); np.save(f"{on}_S0.npy", S0.astype(np.float32))
    np.save(f"{on}_gercek.npy", gercek.astype(np.float32)); np.save(f"{on}_L.npy", lab.durum.etiket.astype(np.float32))
    kara_g = gercek > 0
    olc = {}
    for ad, (a0, a1, b0, b1) in BOLGELER.items():
        m = kutu(dz, a0, a1, b0, b1) & kara_g
        if m.sum() < 3:
            continue
        olc[ad] = dict(model_ortanca=round(float(np.median(z[m]))), gercek_ortanca=round(float(np.median(gercek[m]))),
                       model_p95=round(float(np.percentile(z[m], 95))), gercek_p95=round(float(np.percentile(gercek[m], 95))))
        v = olc[ad]
        print(f"{ad}: model {v['model_ortanca']} m (p95 {v['model_p95']}), gerçek {v['gercek_ortanca']} m (p95 {v['gercek_p95']})")
    hip = {}
    for esik in (1000, 2000, 3000, 4000):
        hip[f">{esik} m"] = [round(float((z > esik).sum() * h_km ** 2 / 1e6), 2), round(float((gercek > esik).sum() * h_km ** 2 / 1e6), 2)]
    print("alan Mkm² (model, gerçek):", hip)
    ort = ((z > 0) & kara_g).sum() / max(((z > 0) | kara_g).sum(), 1)
    print(f"kıyı örtüşmesi (IoU) {ort:.2f}; en yüksek {z.max():.0f} m; toplam {time.time() - t0:.0f} s")
    json.dump(dict(bolgeler=olc, alan=hip, iou=round(float(ort), 3), sure_s=round(time.time() - t0)),
              open(f"{on}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
