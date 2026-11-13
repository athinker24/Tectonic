"""Kanıt denemesi 2: tektonik katman + kurala dayalı yapı katmanı + ince ızgarada aşınma.

Kullanım: python -m deneyler.yapi_kanit [ON_EK] [KABA_H_KM] [H_KM] [SURE_MYR] [K] [GENLIK_M]

Yapı katmanı (kural; kopya değil, her parametresi tektonik katmandan):
  doğrultu: kalınlaşmış kabuğun eş kalınlık çizgileri (S'nin 100 km düzgünleştirilmiş eğiminin yapı
            tensörü, 250 km ortalama); kuşaklar sıkışmaya dik uzanır.
  şiddet:   kabuk kalınlaşması (S 40 km'den 55 km'ye 0'dan 1'e) ve kalınlaşmış yerde eğim (kenar
            kuşakları güçlü); deforme olmamış ovada sıfır; sert çekirdeklerde (Tarim, Junggar, Sichuan,
            Ordos, kalkanlar) 60 km yumuşak geçişle 0,15 kat.
  desen:    rastgele gürültü doğrultu boyunca çizgi tümlevi ile uzatılır (iki ölçek: ana kuşaklar
            yaklaşık 140 km aralık ve 600 km boy, ikincil sırtlar 45 km ve 140 km), 150 km ölçekte 45 km
            bükülür (kıvrım, dallanma); sırtlar yalnız desen tepelerinde (düzensiz aralık, sönen uçlar),
            arası düz tabanlı havza; ikincil sırtlar ana kuşak üstünde güçlü.
Hedef yüzey = kaba yüzey + genlik × şiddet × desen. Aşınma katmanı: 15 km'den büyük ölçek hedefe
0,5 milyon yıl sürede yaklaşır (yükselme), küçük ölçek (vadiler) aşınmayla serbest oluşur.
"""
import sys
import time

import fastscapelib as fs
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.arazi_kanit import BOLGE
from deneyler.dunya import SERT, SINIR, cokgen_ici, gercek_yukseklik
from deneyler.dunya_ince import gercek_06, golge, izgaraya
from tektonik.lab import enlem_yagis
from tektonik.levha import Duzlem, duzlem_kur, laea_geri, laea_ileri
from tektonik.levha_model import yagis_alani
from tektonik.yazi import yazi_tipi


def cizgi_tumlevi(N, tx, ty, adim):
    """Gürültüyü (tx, ty) doğrultu alanı boyunca her iki yönde `adim` hücre ortalar (LIC)."""
    ny, nx = N.shape
    rr, cc = np.mgrid[0:ny, 0:nx].astype(float)
    top = N.copy(); say = 1.0
    for yon in (1.0, -1.0):
        r, c = rr.copy(), cc.copy()
        for k in range(adim):
            ii = np.clip(np.rint(r).astype(int), 0, ny - 1); jj = np.clip(np.rint(c).astype(int), 0, nx - 1)
            dx, dy = tx[ii, jj], ty[ii, jj]
            # doğrultu işareti sürekli kalsın (çizgi alanı yönsüz)
            if k > 0:
                ters = dx * px + dy * py < 0
                dx = np.where(ters, -dx, dx); dy = np.where(ters, -dy, dy)
            px, py = dx, dy
            c = c + yon * dx; r = r - yon * dy
            w = np.exp(-(k / (0.8 * adim)) ** 2)
            top += w * ndimage.map_coordinates(N, [r, c], order=1, mode="reflect"); say += w
    return top / say


def desen(ny, nx, h_km, tx, ty, aralik_km, boy_km, rng):
    """Doğrultu boyunca uzamış, belirli aralıklı sırt deseni; kaba ızgarada üretilip büyütülür."""
    f = max(1, int(round(aralik_km / 8 / h_km)))  # hücre aralığın yaklaşık 1/8'i
    nyc, nxc = ny // f + 1, nx // f + 1
    hc = h_km * f
    N = ndimage.gaussian_filter(rng.standard_normal((nyc, nxc)), aralik_km / 4 / hc)
    txc, tyc = tx[::f, ::f][:nyc, :nxc], ty[::f, ::f][:nyc, :nxc]
    L = cizgi_tumlevi(N, txc, tyc, int(boy_km / 2 / hc))
    L = L - ndimage.gaussian_filter(L, aralik_km / hc)  # aralıktan büyük ölçeği at (bant geçiren)
    L /= L.std() + 1e-12
    up = ndimage.zoom(L, f, order=3)[:ny, :nx]
    if up.shape != (ny, nx):
        up = np.pad(up, ((0, ny - up.shape[0]), (0, nx - up.shape[1])), mode="edge")
    return np.clip(up / 2.0, -1, 1)


def main():
    on = sys.argv[1] if len(sys.argv) > 1 else "cikti/dunya_lab/dl_50km_50ma_avr1500_K5e-07_s10_z0.3_150_kk0_sh0_in5_kb1_dk0.02_yay2000_iklim"
    kaba_h = float(sys.argv[2]) if len(sys.argv) > 2 else 50.0
    h_km = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
    sure = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
    K = float(sys.argv[5]) if len(sys.argv) > 5 else 2e-6
    genlik = float(sys.argv[6]) if len(sys.argv) > 6 else 1800.0
    t0 = time.time()
    zr10, _, _ = gercek_yukseklik()
    dzk = duzlem_kur(zr10 > 0, SINIR, h_km=kaba_h, pay_km=800.0)
    lo = np.array([BOLGE[0], BOLGE[1], BOLGE[0], BOLGE[1]]); la = np.array([BOLGE[2], BOLGE[2], BOLGE[3], BOLGE[3]])
    px, py = laea_ileri(lo, la, dzk.lon0, dzk.lat0)
    h = h_km * 1e3
    x = np.arange(px.min(), px.max(), h); y = np.arange(py.max(), py.min(), -h)
    X, Y = np.meshgrid(x, y)
    LO, LA = laea_geri(X, Y, dzk.lon0, dzk.lat0)
    ny, nx = X.shape
    cc = (X - dzk.x[0]) / dzk.h; rr = (dzk.y[0] - Y) / dzk.h
    zk = np.load(f"{on}_z.npy").astype(float); Sk = np.load(f"{on}_S.npy").astype(float)
    z = ndimage.map_coordinates(zk, [rr, cc], order=3, mode="nearest")
    S = ndimage.map_coordinates(Sk, [rr, cc], order=1, mode="nearest")
    kara = ndimage.map_coordinates(zk, [rr, cc], order=1, mode="nearest") > 0
    print(f"ızgara {ny}×{nx}, {h_km} km", flush=True)

    # --- yapı katmanı ---
    Sd = ndimage.gaussian_filter(S, 100.0 / h_km)
    gy, gx = np.gradient(Sd)
    gx, gy = gx, -gy  # doğu, kuzey
    jxx = ndimage.gaussian_filter(gx * gx, 250.0 / h_km); jyy = ndimage.gaussian_filter(gy * gy, 250.0 / h_km)
    jxy = ndimage.gaussian_filter(gx * gy, 250.0 / h_km)
    th = 0.5 * np.arctan2(2 * jxy, jxx - jyy)  # eğim doğrultusu
    tx, ty = -np.sin(th), np.cos(th)  # doğrultu (kuşak uzanımı) eğime dik
    rng = np.random.default_rng(11)
    ana = desen(ny, nx, h_km, tx, ty, 140.0, 600.0, rng)
    ikincil = desen(ny, nx, h_km, tx, ty, 45.0, 140.0, rng)
    # büyük ölçekli bükme: kuşaklar kıvrılır, dallanır, kavislenir (genlik 45 km, ölçek 150 km)
    wx = ndimage.gaussian_filter(rng.standard_normal(z.shape), 150.0 / h_km); wx *= (45.0 / h_km) / (wx.std() + 1e-12)
    wy = ndimage.gaussian_filter(rng.standard_normal(z.shape), 150.0 / h_km); wy *= (45.0 / h_km) / (wy.std() + 1e-12)
    ri_, ci_ = np.mgrid[0:ny, 0:nx].astype(float)
    bük = lambda f: ndimage.map_coordinates(f, [ri_ + wy, ci_ + wx], order=1, mode="reflect")
    ana, ikincil = bük(ana), bük(ikincil)
    # sırt yalnız desenin tepelerinde: düzensiz aralık, uçlarda doğal sönme; arası düz havza
    tepe = lambda n: np.clip(n, 0, 1) ** 1.2
    d = 1.5 * tepe(ana) + 0.45 * tepe(ikincil) * (0.3 + 0.7 * np.clip(ana + 0.5, 0, 1)) - 0.3
    egim = np.hypot(gx, gy) * 1e3 / h_km  # m kabuk / km
    # yalnız deforme kabukta: kalınlaşma 40 km'den 55 km'ye; kenar kuşağı terimi yalnız kalınlaşmış yerde
    kalin = np.clip((S - 40e3) / 15e3, 0, 1)
    siddet = np.clip(kalin * 0.75 + np.clip(egim / 40.0, 0, 1) * np.clip((S - 37e3) / 3e3, 0, 1) * 0.5, 0, 1)
    sert = np.zeros(z.shape, bool)
    for c_ in SERT.values():
        sert |= cokgen_ici(LO, LA, c_)
    w_sert = ndimage.gaussian_filter(sert.astype(float), 60.0 / h_km)  # yumuşak geçiş, çokgen izi kalmasın
    siddet = siddet * (1.0 - 0.85 * np.clip(w_sert * 1.5, 0, 1))
    hedef = np.where(kara, z + genlik * siddet * d, z)
    print(f"yapı katmanı {time.time() - t0:.0f} s", flush=True)

    # --- aşınma katmanı ---
    gur = sum(a * (lambda g: g / g.std())(ndimage.gaussian_filter(rng.standard_normal(z.shape), sg)) for sg, a in ((1, 10.0), (3, 20.0)))
    zz = np.where(kara, np.maximum(hedef, 1.0) + np.abs(gur), 0.0)
    z_deniz = np.where(kara, 0.0, np.minimum(z, -1.0))
    durum = {(int(i), int(j)): fs.NodeStatus.FIXED_VALUE for i, j in zip(*np.nonzero(~kara))}
    grid = fs.RasterGrid([ny, nx], [h, h], fs.NodeStatus.FIXED_VALUE, durum)
    router = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver(), fs.MultiFlowRouter(1.0)])  # çok yönlü: düz paralel oluklar olmasın
    eroder = fs.SPLEroder(router, K, 0.5, 1.0, 1e-4)
    dt = 2e4; n = int(round(sure * 1e6 / dt))
    s15 = 15.0 / h_km
    hedef_d = ndimage.gaussian_filter(np.where(kara, hedef, 0.0), s15)
    P = None
    for i in range(n):
        if i % 25 == 0:
            P = yagis_alani(kara, zz, h, 3000.0, 1500.0, 0.15) * enlem_yagis(LA)
        zf = np.ascontiguousarray(zz, dtype=np.float64).copy()
        router.update_routes(zf)
        A = np.asarray(router.accumulate(np.ascontiguousarray(P)))
        e = np.where(kara, np.clip(np.asarray(eroder.erode(zf, A, dt)).reshape(z.shape), 0, None), 0.0)
        zz = zz - e
        # yükselme: 15 km düzgünleştirilmiş yüzey 0,5 milyon yılda hedefe yaklaşır
        U = (hedef_d - ndimage.gaussian_filter(zz, s15)) * min(1.0, dt / 5e5)
        zz = np.where(kara, np.maximum(zz + U, 0.5), 0.0)
        if i % 50 == 49:
            print(f"  {i + 1}/{n} adım, {time.time() - t0:.0f} s", flush=True)
    sure_s = time.time() - t0
    zs = np.where(kara, zz, z_deniz)
    np.save(f"cikti/yapi_kanit_{h_km:g}km_{sure:g}my_K{K:g}_c_z.npy", zs.astype(np.float32))
    dzi = Duzlem(dzk.lon0, dzk.lat0, h, x, y, LO, LA, kara)
    zg6, lo6, la6 = gercek_06()
    zg, _ = izgaraya(dzi, zg6, lo6, la6)
    zg = ndimage.gaussian_filter(zg, 0.6)
    m_im = golge(zs, kara, h); g_im = golge(zg, zg > 0, h)
    W, H = m_im.size; s = 900 / W
    m_s = m_im.resize((900, int(H * s)), Image.LANCZOS); g_s = g_im.resize((900, int(H * s)), Image.LANCZOS)
    t = Image.new("RGB", (900, m_s.height * 2 + 70), "white")
    t.paste(m_s, (0, 32)); t.paste(g_s, (0, m_s.height + 68))
    dr = ImageDraw.Draw(t)
    dr.text((8, 4), f"Model: tektonik + yapı katmanı + {h_km:g} km'de {sure:g} milyon yıl aşınma ({sure_s / 60:.0f} dakika)", fill=(0, 0, 0), font=yazi_tipi(20))
    dr.text((8, m_s.height + 40), "Gerçek (06' veri, yaklaşık 11 km)", fill=(0, 0, 0), font=yazi_tipi(20))
    t.save(f"cikti/yapi_kanit_{h_km:g}km_{sure:g}my_K{K:g}_c.png")
    c0, r0 = int(nx * 0.25), int(ny * 0.25)
    m_im.crop((c0, r0, c0 + 700, r0 + 450)).save(f"cikti/yapi_kanit_{h_km:g}km_{sure:g}my_K{K:g}_c_yakin.png")
    # yapı katmanının kendisi (aşınmadan önce), tanı için
    golge(np.where(kara, hedef, z_deniz), kara, h).resize((900, int(H * s)), Image.LANCZOS).save(f"cikti/yapi_kanit_{h_km:g}km_{sure:g}my_K{K:g}_c_hedef.png")
    print(f"toplam {sure_s:.0f} s")


if __name__ == "__main__":
    main()
