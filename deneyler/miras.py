"""Miras: sahibin kıtasında ana evreden (60 Ma) önceki eski tarih; eski kuşaklar, havzalar, kabuk farkları.

Kullanım: python -m deneyler.miras [TOHUM] [H_KM]

Bugünkü kıta biçimi üzerinde (eski kıyılar bilinmediği için yaklaşık) sırayla:
  360-344 Ma  eski çarpışma A: rastgele yönlü, kıvrımlı bir dikişin küçük yanı 2,5 cm/yıl yaklaşır (400 km)
  344-280 Ma  aşınma ve gevşeme (hız yok; K 1,5e-7, eski kayaç dayanıklı)
  280-264 Ma  eski çarpışma B: başka yön ve yerde
  264-200 Ma  aşınma ve gevşeme
  200-190 Ma  yarılma: küçük yan 1,5 cm/yıl uzaklaşır (150 km; incelen kabuk, sonra çöküntü havzası)
  190-60 Ma   aşınma ve gevşeme
Her evre laboratuvarın aynı süreçleriyle (ince levha, kalınlaşma, alt kabuk akışı, izostazi, yağışlı
aşınma, çökelme) koşulur. Kalıp yok; dikişlerin yeri ve yönü yalnız tohumdan.
Çıktı: veri/miras_{TOHUM}.npz (hücre boylam, enlem, kabuk kalınlığı S) ve cikti/miras/ görselleri.
Kara ortancası tek bir sabitle 35 km'ye taşınır (uzun vadeli serbest bord); bugünkü karada S en az
33,5 km tutulur (sahibin kıyısı kara kalsın).
"""
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.carpisma_lab import resim
from tektonik.izgara import maske_yukle
from tektonik.lab import Lab, LabAyar
from tektonik.levha import duzlem_kur
from tektonik.yazi import yazi_tipi


def dikis_etiketi(dz, rng, kita, kivrim_km=400.0):
    """Kıtanın içinden geçen rastgele yönlü, kıvrımlı bir hat; bir yanı 1 (hareketli), öbür yanı 0.
    Dönüş: etiket, hareket yönü birim vektörü (doğu, kuzey; hatta dik, hatta doğru)."""
    ny, nx = dz.sekil
    r, c = np.nonzero(kita)
    i = rng.integers(len(r))
    r0, c0 = r[i], c[i]
    th = rng.uniform(0, np.pi)
    n = np.array([np.cos(th), np.sin(th)])  # hattın normali (doğu, kuzey)
    yy, xx = np.mgrid[0:ny, 0:nx]
    dxe = (xx - c0) * dz.h; dyn = -(yy - r0) * dz.h
    g = ndimage.gaussian_filter(rng.standard_normal((ny, nx)), kivrim_km * 1e3 / dz.h / 2); g /= g.std()
    d = dxe * n[0] + dyn * n[1] + 150e3 * g  # kıvrımlı hat
    et = (d > 0).astype(float)
    if (et * kita).sum() > ((1 - et) * kita).sum():  # hareketli taraf kıtanın küçük parçası olsun
        return 1.0 - et, n
    return et, -n  # hareketli taraf (d > 0) hatta doğru (−n yönünde) gelir


def main():
    tohum = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    h_km = float(sys.argv[2]) if len(sys.argv) > 2 else 45.0
    t0 = time.time()
    os.makedirs("cikti/miras", exist_ok=True)
    maske, sinir = maske_yukle("veri/maske.json")
    dz = duzlem_kur(maske, sinir, h_km=h_km, pay_km=900.0)
    kara0 = dz.kara.copy()
    rng = np.random.default_rng(tohum)
    S = np.where(kara0, 35e3, 7e3)
    a = LabAyar(h_km=h_km, dt_myr=1.0, kappa_max=3000.0, K=5e-7, cek_gelen_km=400.0, cek_sabit_km=450.0,
                carpisma_sonrasi_hiz=1.0)
    # (ad, başlangıç Ma, bitiş Ma, hız cm/yıl, K): sakin evrelerde eski, aşınmış kayaç daha dayanıklı
    # (ad, başlangıç Ma, bitiş Ma, hız cm/yıl, K); kısalma yaklaşık 400 km, yarılma 150 km.
    # Sakin evrelerde eski, aşınmış kayaç daha dayanıklı (K düşük).
    evreler = [("çarpışma A", 360, 344, 2.5, 5e-7), ("aşınma", 344, 280, 0.0, 1.5e-7), ("çarpışma B", 280, 264, 2.5, 5e-7),
               ("aşınma", 264, 200, 0.0, 1.5e-7), ("yarılma", 200, 190, -1.5, 3e-7), ("aşınma", 190, 60, 0.0, 1.5e-7)]
    kareler = []
    from dataclasses import replace
    for ad, b0, b1, v, Kf in evreler:
        a = replace(a, K=Kf)
        kita = S > 20e3
        if v != 0:
            et, yon = dikis_etiketi(dz, rng, kita)
            hiz = (yon[0] * v, yon[1] * v)
        else:
            et, hiz = np.zeros(S.shape), (0.0, 0.0)
        lab = Lab(S, et, hiz, float(b0), a)
        n = int(round((b0 - b1) / a.dt_myr))
        for i in range(n):
            d = lab.adim()
            if i % 5 == 4 or i == n - 1:
                im = resim(d.z, h_km, 2)
                ImageDraw.Draw(im).text((8, 6), f"{d.ma:.0f} milyon yıl önce ({ad})", fill=(255, 255, 255), font=yazi_tipi(16))
                kareler.append(im)
        S = lab.durum.S
        g = d.gunluk[-1]
        print(f"{ad} {b0}-{b1} Ma: zmax {g['zmax']:.0f} m, Smax {g['Smax_km']:.1f} km, {time.time() - t0:.0f} s", flush=True)
    # bugünkü kara: en az 33,5 km (kıyı sahibin maskesi), deniz: okyanus
    # kıtanın uzun vadeli serbest bordu korunur (deniz düzeyi ve manto dengesi): kara ortancası 35 km'ye
    # tek bir sabitle taşınır; eski kökler ve havzalar arasındaki göreli fark aynen kalır
    print(f"ham kara S: %5 {np.percentile(S[kara0], 5) / 1e3:.1f}, ortanca {np.median(S[kara0]) / 1e3:.1f}, "
          f"%95 {np.percentile(S[kara0], 95) / 1e3:.1f} km", flush=True)
    S = S + (35e3 - np.median(S[kara0]))
    Sk = np.where(kara0, np.maximum(S, 33.5e3), 7e3)
    on = f"cikti/miras/miras_{tohum}_{h_km:g}km"
    kareler[0].save(f"{on}.gif", save_all=True, append_images=kareler[1:] + [kareler[-1]] * 6, duration=150, loop=0)
    kareler[-1].save(f"{on}_son.png")
    os.makedirs("veri", exist_ok=True)
    np.savez_compressed(f"veri/miras_{tohum}.npz", lon=dz.lon[kara0], lat=dz.lat[kara0], S=Sk[kara0])
    print(f"kara S: ortanca {np.median(Sk[kara0]) / 1e3:.1f} km, %5 {np.percentile(Sk[kara0], 5) / 1e3:.1f}, "
          f"%95 {np.percentile(Sk[kara0], 95) / 1e3:.1f} km; son yüzey en yüksek {g['zmax']:.0f} m; toplam {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
