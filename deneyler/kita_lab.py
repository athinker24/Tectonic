"""Sahibin kıtasında çarpışma laboratuvarı: bloklar geçmiş konumlarından başlayıp ileri zamanda gelir.

Kullanım: python -m deneyler.kita_lab [ADAY_NO] [H_KM] [BAS_MA] [PAY] [BUYUK] [YAY_M] [MIRAS_NPZ]

Başlangıç: her blok, aday tarihinin geri sürmesiyle BAS_MA anındaki konumuna yerleştirilir
(Kuzey sabit). Sonra hiçbir kalıp olmadan: bloklar tarihlerindeki hızlarla sürülür, ince viskoz levha
akar, kabuk kalınlaşır ve taşınır, alt kabuk akışı, bükülmeli izostazi, yağışlı aşınma ve çökelme.
Kıyılar serbesttir; son durum sahibin maskesiyle karşılaştırılır (örtüşme oranı raporlanır).
"""
import json
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree

from deneyler.carpisma_lab import resim
from tektonik import kure
from tektonik.bloklar import bloklara_ayir
from tektonik.izgara import _lonlat_xyz, izgara_kur, maske_yukle
from tektonik.lab import LabAyar, LabCok
from tektonik.levha import duzlem_kur, laea_ileri
from tektonik.levha_model import yerel_eksenler
from tektonik.uretici import aday_kur
from tektonik.yazi import yazi_tipi


def main():
    no = int(sys.argv[1]) if len(sys.argv) > 1 else 1029
    h_km = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
    bas = float(sys.argv[3]) if len(sys.argv) > 3 else 70.0
    t0 = time.time()
    os.makedirs("cikti/kita_lab", exist_ok=True)
    on = f"cikti/kita_lab/kita_{no}_{h_km:g}km_{bas:g}ma" + ("_buyuk" if (len(sys.argv) <= 5 or sys.argv[5] == "1") else "")
    maske, sinir = maske_yukle("veri/maske.json")
    sen = json.load(open("veri/senaryo.json", encoding="utf-8"))
    pay = float(sys.argv[4]) if len(sys.argv) > 4 else 1800.0
    buyuk = (sys.argv[5] == "1") if len(sys.argv) > 5 else True
    dz = duzlem_kur(maske, sinir, h_km=h_km, pay_km=pay)
    ny, nx = dz.sekil
    iz = izgara_kur(maske, sinir, nside=128)
    bl = bloklara_ayir(iz, sen)
    rapor = json.load(open("cikti/gercek/adaylar.json", encoding="utf-8"))
    p = dict(next(a["parametre"] for a in rapor["secilen"] if a["no"] == no))
    aday = aday_kur(no, np.random.default_rng(0), iz, bl, sen, p)

    # bugünkü blok etiketleri ızgarada
    ki = np.flatnonzero(iz.kara)
    _, j = cKDTree(iz.xyz[ki]).query(_lonlat_xyz(dz.lon[dz.kara], dz.lat[dz.kara]))
    blok_bugun = np.full(dz.sekil, -1)
    blok_bugun[dz.kara] = bl.etiket[ki[j]]
    # başlangıç: her bloğun kara hücrelerini BAS_MA anına geri sür, ızgaraya yerleştir
    # miras (deneyler.miras): bugünkü konumda eski tarihten kalan kabuk kalınlığı; yoksa her yer 35 km
    miras = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7] != "0" else None
    if miras:
        mv = np.load(miras)
        _, jm = cKDTree(_lonlat_xyz(mv["lon"], mv["lat"])).query(_lonlat_xyz(dz.lon, dz.lat))
        S_miras = mv["S"][jm].reshape(dz.sekil)
        on += "_miras" + os.path.basename(miras).replace("miras_", "").replace(".npz", "")
    else:
        S_miras = np.full(dz.sekil, 35e3)
    S0 = np.full(dz.sekil, 7e3)
    L0 = np.full(dz.sekil, -1.0)
    for b, ad in enumerate(bl.adlar):
        m = blok_bugun == b
        if not m.any():
            continue
        xyz = _lonlat_xyz(dz.lon[m], dz.lat[m])
        sv = S_miras[m]
        if ad in aday.tarihler:
            tr = aday.tarihler[ad]
            p0 = xyz
            xyz = kure.uygula(tr.geri_donme(bas), p0)
            # "Büyük" blok: çarpışmadan sonraki itmenin tüketeceği kıta uzantısı. Katı geri sürmede bu
            # itme çarpışma anında bir boşluk olarak görünür; o boşluk aslında bloğun dağa itilip yok
            # olan önüdür (Büyük Hindistan). Çarpışma anı: sıfırdan büyük en geç aşama sonu.
            tc = max([a.bitis_ma for a in tr.asamalar if 0 < a.bitis_ma < bas], default=0.0)
            if buyuk and tc > 0:
                q = kure.carp(tr.geri_donme(bas), kure.ters(tr.geri_donme(tc)))
                kor = np.vstack([kure.uygula(tr.geri_donme(t), p0) for t in np.linspace(0, tc, 24)])
                # yalnız çarpışmada tükenecek kısım: katı ileri hareketle bugün başka bir bloğun
                # karasına denk gelen koridor hücreleri (iç denize bakan yanın önü kara olarak kalmasın)
                bugun = kure.uygula(kure.ters(tr.geri_donme(tc)), kor)
                diger = (blok_bugun >= 0) & (blok_bugun != b)
                agac = cKDTree(_lonlat_xyz(dz.lon[diger], dz.lat[diger]))
                dd, _ = agac.query(bugun, distance_upper_bound=1.5 * dz.h / 6.371e6)
                kor = kor[np.isfinite(dd)]
                ek = kure.uygula(q, kor)
                xyz = np.vstack([xyz, ek])
                sv = np.r_[sv, np.full(len(ek), 35e3)]
                print(f"{ad}: çarpışma {tc:.1f} Ma, Büyük {ad} uzantısı {len(kor)} nokta")
        lo, la = kure.xyz_lonlat(xyz)
        px, py = laea_ileri(np.asarray(lo), np.asarray(la), dz.lon0, dz.lat0)
        c = np.round((px - dz.x[0]) / dz.h).astype(int)
        r = np.round((dz.y[0] - py) / dz.h).astype(int)
        ok = (r >= 0) & (r < ny) & (c >= 0) & (c < nx)
        if (~ok).any():
            print(f"uyarı: {ad} bloğunun {(~ok).sum()} hücresi alan dışında")
        yer = np.zeros(dz.sekil, bool)
        yer[r[ok], c[ok]] = True
        deg = np.zeros(dz.sekil)
        np.maximum.at(deg, (r[ok], c[ok]), sv[ok])
        kapa = ndimage.binary_closing(yer, iterations=1) & ~yer
        deg = np.where(kapa, ndimage.maximum_filter(deg, 3), deg)
        yer |= kapa
        S0[yer] = deg[yer]
        L0[yer] = b
    # okyanus hücreleri: en yakın bloğun etiketi (levha)
    kita0 = S0 > 20e3
    _, (ri, ci) = ndimage.distance_transform_edt(~kita0, return_indices=True)
    L0 = L0[ri, ci]

    yay = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0  # yay magmatizması üretimi (m)
    a = LabAyar(h_km=h_km, dt_myr=0.5, kappa_max=3000.0, K=5e-7, cek_gelen_km=400.0, cek_sabit_km=450.0, yay_uretim_m=yay)
    if yay > 0:
        on += f"_yay{yay:g}"
    lab = LabCok(S0, L0, bas, a, dz.lon, dz.lat, aday.tarihler, bl.adlar, bl.sabit, yerel_eksenler(dz, dz.lon, dz.lat))
    kareler = []
    adim = int(round(bas / a.dt_myr))
    for i in range(adim):
        d = lab.adim()
        if i % 4 == 3 or i == adim - 1:
            im = resim(d.z, h_km, 2)
            ImageDraw.Draw(im).text((8, 6), f"{d.ma:.0f} milyon yıl önce", fill=(255, 255, 255), font=yazi_tipi(16))
            kareler.append(im)
        if i % 20 == 19 or i == adim - 1:
            g = d.gunluk[-1]
            print(f"{d.ma:5.1f} Ma  zmax {g['zmax']:5.0f} m  Smax {g['Smax_km']:4.1f} km  kara %{100 * g['kara_orani']:.0f}  "
                  f"vmax {g['vmax_cm']:.1f} cm/yıl  {time.time() - t0:.0f} s", flush=True)
    kareler[0].save(f"{on}.gif", save_all=True, append_images=kareler[1:] + [kareler[-1]] * 8, duration=150, loop=0)
    kareler[-1].save(f"{on}_son.png")
    z = lab.durum.z
    kara_son = z > 0
    ort = (kara_son & dz.kara).sum() / max((kara_son | dz.kara).sum(), 1)
    # maskeye göre kesilmiş: kıyı sahibin maskesi, yükseklik simülasyondan
    zm = np.where(dz.kara, np.maximum(z, 1.0), np.minimum(z, -1.0))
    resim(zm, h_km, 2).save(f"{on}_maskeli.png")
    np.save(f"{on}_z.npy", z.astype(np.float32))
    print(f"maske örtüşmesi (IoU) {ort:.2f}; en yüksek {z.max():.0f} m; toplam {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
