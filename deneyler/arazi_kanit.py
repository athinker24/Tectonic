"""Kanıt denemesi: tektonik katmanın büyük ölçekli yüzeyi + ince ızgarada (2,5 km) yükselme ve akarsu aşınması.

Kullanım: python -m deneyler.arazi_kanit [Z_NPY] [KABA_H_KM] [H_KM] [SURE_MYR] [K]

Bölge: Tibet, Tarim, Hindistan'ın kuzeyi (65 ile 105°D, 22 ile 45°K). Kaba yüzey ince ızgaraya taşınır;
yükselme her adımda 50 km ölçekte aşınmayı karşılar (büyük ölçekli yükseklik tektonik katmanınki kalır,
50 km'den küçük her şey aşınmayla oluşur). Yağış orografik ve enlemli. Gerçek veri yalnız karşılaştırma için.
"""
import sys
import time

import fastscapelib as fs
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.dunya import SINIR, gercek_yukseklik
from deneyler.dunya_ince import gercek_06, golge, izgaraya
from tektonik.lab import enlem_yagis
from tektonik.levha import Duzlem, duzlem_kur, laea_geri, laea_ileri
from tektonik.levha_model import yagis_alani
from tektonik.yazi import yazi_tipi

BOLGE = (65.0, 105.0, 22.0, 45.0)


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else "cikti/dunya_lab/dl_25km_50ma_avr1500_K5e-07_s10_z0.3_150_kk0_sh0_in5_kb1_dk0.02_z.npy"
    kaba_h = float(sys.argv[2]) if len(sys.argv) > 2 else 25.0
    h_km = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
    sure = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
    K = float(sys.argv[5]) if len(sys.argv) > 5 else 2e-6
    t0 = time.time()
    zr10, _, _ = gercek_yukseklik()
    dzk = duzlem_kur(zr10 > 0, SINIR, h_km=kaba_h, pay_km=800.0)
    # bölgenin kaba izdüşümdeki kutusu
    lo = np.array([BOLGE[0], BOLGE[1], BOLGE[0], BOLGE[1]]); la = np.array([BOLGE[2], BOLGE[2], BOLGE[3], BOLGE[3]])
    px, py = laea_ileri(lo, la, dzk.lon0, dzk.lat0)
    h = h_km * 1e3
    x = np.arange(px.min(), px.max(), h); y = np.arange(py.max(), py.min(), -h)
    X, Y = np.meshgrid(x, y)
    LO, LA = laea_geri(X, Y, dzk.lon0, dzk.lat0)
    ny, nx = X.shape
    zk = np.load(yol).astype(float)
    cc = (X - dzk.x[0]) / dzk.h; rr = (dzk.y[0] - Y) / dzk.h
    z = ndimage.map_coordinates(zk, [rr, cc], order=3, mode="nearest")
    kara = ndimage.map_coordinates(zk, [rr, cc], order=1, mode="nearest") > 0
    rng = np.random.default_rng(5)
    gur = sum(a * (lambda g: g / g.std())(ndimage.gaussian_filter(rng.standard_normal(z.shape), sg))
              for sg, a in ((1, 10.0), (3, 20.0), (8, 30.0)))
    z = np.where(kara, np.maximum(z, 1.0) + np.abs(gur), np.minimum(z, -1.0))
    z_deniz = np.where(kara, 0.0, z)
    print(f"ızgara {ny}×{nx} ({ny * nx / 1e6:.1f} milyon hücre), {h_km} km", flush=True)

    durum = {(int(i), int(j)): fs.NodeStatus.FIXED_VALUE for i, j in zip(*np.nonzero(~kara))}
    grid = fs.RasterGrid([ny, nx], [h, h], fs.NodeStatus.FIXED_VALUE, durum)
    router = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
    eroder = fs.SPLEroder(router, K, 0.5, 1.0, 1e-4)
    dt = 2e4
    n = int(round(sure * 1e6 / dt))
    zz = np.where(kara, z, 0.0)
    sig = 50.0 / h_km
    kar = kara.astype(float)
    P = None
    for i in range(n):
        if i % 25 == 0:
            P = yagis_alani(kara, zz, h, 3000.0, 1500.0, 0.15) * enlem_yagis(LA)
        zf = np.ascontiguousarray(zz, dtype=np.float64).copy()
        router.update_routes(zf)
        A = np.asarray(router.accumulate(np.ascontiguousarray(P)))
        e = np.asarray(eroder.erode(zf, A, dt)).reshape(z.shape)
        e = np.where(kara, np.clip(e, 0, None), 0.0)
        # yükselme 50 km ölçekte aşınmayı karşılar: büyük ölçek tektonik katmandan, küçük ölçek aşınmadan
        U = ndimage.gaussian_filter(e, sig) / np.maximum(ndimage.gaussian_filter(kar, sig), 1e-6)
        zz = np.where(kara, np.maximum(zz - e + U, 0.5), 0.0)
        if i % 25 == 24:
            print(f"  {i + 1}/{n} adım, {time.time() - t0:.0f} s, ortalama aşınma hızı {e[kara].mean() / dt * 1e3:.3f} mm/yıl", flush=True)
    sure_s = time.time() - t0
    zs = np.where(kara, zz, z_deniz)
    np.save(f"cikti/arazi_kanit_{h_km:g}km_z.npy", zs.astype(np.float32))
    # gerçek, aynı ızgarada
    dzi = Duzlem(dzk.lon0, dzk.lat0, h, x, y, LO, LA, kara)
    zg6, lo6, la6 = gercek_06()
    zg, _ = izgaraya(dzi, zg6, lo6, la6)
    zg = ndimage.gaussian_filter(zg, 0.6)  # 06' veri (yaklaşık 11 km) 2,5 km'ye taşınırken blok izleri
    m_im = golge(zs, kara, h); g_im = golge(zg, zg > 0, h)
    W, H = m_im.size
    s = 900 / W
    m_s = m_im.resize((900, int(H * s)), Image.LANCZOS); g_s = g_im.resize((900, int(H * s)), Image.LANCZOS)
    t = Image.new("RGB", (900, m_s.height * 2 + 70), "white")
    t.paste(m_s, (0, 32)); t.paste(g_s, (0, m_s.height + 68))
    d = ImageDraw.Draw(t)
    d.text((8, 4), f"Model: tektonik katman + {h_km:g} km'de {sure:g} milyon yıl aşınma ({sure_s / 60:.0f} dakika)", fill=(0, 0, 0), font=yazi_tipi(20))
    d.text((8, m_s.height + 40), "Gerçek (06' veri, yaklaşık 11 km)", fill=(0, 0, 0), font=yazi_tipi(20))
    t.save(f"cikti/arazi_kanit_{h_km:g}km.png")
    # yakın plan, tam çözünürlük: Tarim'in güney kenarı ve Batı Kunlun
    c0, r0 = int(nx * 0.25), int(ny * 0.25)
    m_im.crop((c0, r0, c0 + 700, r0 + 450)).save(f"cikti/arazi_kanit_{h_km:g}km_yakin.png")
    print(f"toplam {sure_s:.0f} s")


if __name__ == "__main__":
    main()
