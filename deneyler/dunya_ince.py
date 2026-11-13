"""İkinci aşama: kaba simülasyonun son yüzeyi ince ızgaraya taşınır ve üzerinde akarsu aşınması koşulur.

Kullanım: python -m deneyler.dunya_ince ON_EK [H_KM] [SURE_MYR] [K] [KABA_H_KM]
  ON_EK: deneyler.dunya_lab çıktısının öneki (…_z.npy olmadan).

Kaba yüzey (ör. 25 km) aynı Lambert izdüşümünde ince ızgaraya (ör. 10 km) kübik ara değerlemeyle
taşınır; kıyı kaba modelin kıyısıdır (gerçek kıyı değil). Kanal ağının çekirdeklenmesi için 1 ile 4 hücre
ölçekli yaklaşık 40 m rastgele gürültü eklenir (fiziksel karşılığı: yüzeydeki küçük düzensizlikler). Sonra fastscapelib akarsu
aşınması (m 0,5, n 1, deniz sabit taban, çukurlar taşar), orografik yağışla ağırlıklı drenaj alanı ve
80 km ölçekli izostatik geri sıçrama (0,85); kaba modelde kabuğu kalınlaşmış (etkin) bölgelerde bu
oran 1'e çıkar: kaya yükselmesi bölgesel aşınmayı karşılar (aktif orojende yaklaşık denge), vadiler
kazılırken sırtlar yükselir. Hiçbir gerçek ya da örnek yükseklik kullanılmaz; gerçek
yükseklik yalnız yan yana karşılaştırma için çizilir.
"""
import sys
import time

import fastscapelib as fs
import h5py
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.dunya import SINIR, gercek_yukseklik
from tektonik.gorsel import _RENK
from tektonik.levha import duzlem_kur, laea_ileri
from tektonik.levha_model import yagis_alani
from tektonik.yazi import yazi_tipi

DENIZ = np.array([[-6000, 18, 45, 100], [-3500, 30, 75, 145], [-1000, 70, 125, 185], [-150, 120, 170, 215], [0, 150, 195, 225]], float)


def gercek_06():
    f = h5py.File("veri/dunya/earth_relief_06m_p.grd", "r")
    lon, lat = f["lon"][:], f["lat"][:]
    z = f["z"][:].astype(np.float32) * float(f["z"].attrs.get("scale_factor", [1.0])[0])
    if lat[0] < lat[-1]:
        lat, z = lat[::-1], z[::-1]
    b, g, d, k = SINIR
    ci = (lon >= b) & (lon < d)
    ri = (lat > g) & (lat <= k)
    return z[np.ix_(ri, ci)], lon[ci], lat[ri]


def izgaraya(dz, zr, lon_r, lat_r):
    """Lat-lon yüksekliği düzlem ızgaraya hücre ortalamasıyla (boş hücreler en yakın komşudan)."""
    ny, nx = dz.sekil
    LO, LA = np.meshgrid(lon_r, lat_r)
    px, py = laea_ileri(LO, LA, dz.lon0, dz.lat0)
    jx = np.round((px - dz.x[0]) / dz.h).astype(int)
    iy = np.round((dz.y[0] - py) / dz.h).astype(int)
    ok = (jx >= 0) & (jx < nx) & (iy >= 0) & (iy < ny)
    top = np.zeros(dz.sekil); say = np.zeros(dz.sekil)
    np.add.at(top, (iy[ok], jx[ok]), zr[ok]); np.add.at(say, (iy[ok], jx[ok]), 1)
    bos = say == 0
    z = np.where(bos, 0, top / np.maximum(say, 1))
    _, (ri, ci) = ndimage.distance_transform_edt(bos, return_indices=True)
    return z[ri, ci], ndimage.binary_erosion(~bos, iterations=2)


def golge(z, kara, h, nehir=None):
    """Hipsometrik renk + çok yönlü gölgeleme; deniz derinliği renk ölçeğiyle."""
    rgb_k = np.stack([np.interp(np.clip(z, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    rgb_d = np.stack([np.interp(np.clip(z, -6000, 0), DENIZ[:, 0], DENIZ[:, i]) for i in (1, 2, 3)], -1)
    gy, gx = np.gradient(np.where(kara, z, 0.0), h)
    ab = 2.5  # dikey abartma
    isik = 0.0
    for az, w in ((315, 0.6), (270, 0.2), (0, 0.2)):
        a = np.radians(az)
        lx, ly, lz = np.sin(a) * np.cos(np.radians(40)), np.cos(a) * np.cos(np.radians(40)), np.sin(np.radians(40))
        nx_, ny_ = -gx * ab, gy * ab  # satır aşağı = güney
        isik = isik + w * (nx_ * lx + ny_ * ly + lz) / np.sqrt(nx_ ** 2 + ny_ ** 2 + 1)
    isik = np.clip(0.35 + 0.85 * isik, 0.3, 1.25)
    rgb = np.where(kara[..., None], rgb_k * isik[..., None], rgb_d)
    if nehir is not None:
        rgb = np.where(nehir[..., None], rgb * 0.35 + np.array([40, 90, 170]) * 0.65, rgb)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def main():
    on = sys.argv[1]
    h_km = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    sure = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    K = float(sys.argv[4]) if len(sys.argv) > 4 else 5e-7
    kaba_h = float(sys.argv[5]) if len(sys.argv) > 5 else 25.0
    denge = (sys.argv[6] == "1") if len(sys.argv) > 6 else True  # etkin bölgede yükselme bölgesel aşınmayı karşılar
    cok = (sys.argv[7] == "1") if len(sys.argv) > 7 else True  # çok yönlü akış (D8'in düz paralel kanallarını önler)
    t0 = time.time()
    zr10, _, _ = gercek_yukseklik()
    dzk = duzlem_kur(zr10 > 0, SINIR, h_km=kaba_h, pay_km=800.0)
    dz = duzlem_kur(zr10 > 0, SINIR, h_km=h_km, pay_km=800.0)
    ny, nx = dz.sekil
    zk = np.load(f"{on}_z.npy").astype(float)
    X, Y = np.meshgrid(dz.x, dz.y)
    cc = (X - dzk.x[0]) / dzk.h
    rr = (dzk.y[0] - Y) / dzk.h
    z = ndimage.map_coordinates(zk, [rr, cc], order=3, mode="nearest")
    kara = ndimage.map_coordinates(zk, [rr, cc], order=1, mode="nearest") > 0
    kara = ndimage.binary_opening(kara, iterations=1) | (kara & (ndimage.uniform_filter(kara.astype(float), 3) > 0.5))
    rng = np.random.default_rng(3)
    # başlangıç düzensizliği: 1, 2 ve 4 hücre ölçekli rastgele gürültü (toplam yaklaşık 40 m); kanal ağı
    # pürüzsüz yüzeyde düz paralel çizgiler halinde çekirdekleniyordu
    gur = sum(a * (lambda g: g / g.std())(ndimage.gaussian_filter(rng.standard_normal(z.shape), sg))
              for sg, a in ((1, 15.0), (2, 20.0), (4, 25.0)))
    z = np.where(kara, np.maximum(z, 1.0) + np.abs(gur), z)
    # tektonik etkinlik: kaba modelde kalınlaşmış kabuk (S 38 ile 45 km arası geçiş)
    try:
        Sk = np.load(f"{on}_S.npy").astype(float)
        etkin = np.clip((ndimage.map_coordinates(Sk, [rr, cc], order=1, mode="nearest") - 38e3) / 7e3, 0, 1)
    except FileNotFoundError:
        etkin = np.zeros(z.shape)
    gs = 0.85 + 0.15 * etkin if denge else np.full(z.shape, 0.85)
    z_deniz = np.where(kara, 0.0, np.minimum(z, -1.0))
    print(f"ince ızgara {ny}×{nx}, {h_km} km; kara {kara.mean():.2f}", flush=True)

    durum = {(int(i), int(j)): fs.NodeStatus.FIXED_VALUE for i, j in zip(*np.nonzero(~kara))}
    grid = fs.RasterGrid([ny, nx], [dz.h, dz.h], fs.NodeStatus.FIXED_VALUE, durum)
    router = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()] + ([fs.MultiFlowRouter(1.0)] if cok else []))
    eroder = fs.SPLEroder(router, K, 0.5, 1.0, 1e-4)
    dt = 2e4
    n = int(round(sure * 1e6 / dt))
    kar = kara.astype(float)
    sig = 80.0 / h_km
    zk_ = np.where(kara, z, 0.0)
    P = yagis_alani(kara, zk_, dz.h, 3000.0, 1500.0, 0.15)
    top_e = np.zeros(dz.sekil)
    for i in range(n):
        zf = np.ascontiguousarray(zk_, dtype=np.float64).copy()
        router.update_routes(zf)
        A = np.asarray(router.accumulate(np.ascontiguousarray(P)))
        e = np.asarray(eroder.erode(zf, A, dt)).reshape(dz.sekil)
        e = np.where(kara, np.clip(e, 0, None), 0.0)
        reb = ndimage.gaussian_filter(e, sig) / np.maximum(ndimage.gaussian_filter(kar, sig), 1e-6)
        zk_ = np.where(kara, np.maximum(zk_ - e + gs * reb, 0.5), 0.0)
        top_e += e
        if i % 25 == 24:
            P = yagis_alani(kara, zk_, dz.h, 3000.0, 1500.0, 0.15)
            print(f"  {i + 1}/{n} adım, {time.time() - t0:.0f} s", flush=True)
    router.update_routes(np.ascontiguousarray(zk_, dtype=np.float64).copy())
    A = np.asarray(router.accumulate(np.ascontiguousarray(P))).reshape(dz.sekil)
    print(f"aşınma ortalama {top_e[kara].mean():.0f} m, en çok {top_e.max():.0f} m; en yüksek {zk_.max():.0f} m", flush=True)

    zs = np.where(kara, zk_, z_deniz)
    nehir = kara & (A > 1.5e11)
    son = on + f"_ince{h_km:g}km_{sure:g}my_K{K:g}_c{int(cok)}"
    np.save(f"{son}_z.npy", zs.astype(np.float32))
    m_im = golge(zs, kara, dz.h, nehir)
    # gerçek, aynı ızgarada (06' veri)
    zg6, lo6, la6 = gercek_06()
    zg, _ = izgaraya(dz, zg6, lo6, la6)
    g_im = golge(zg, zg > 0, dz.h)
    m_im.save(f"{son}.png")
    W, H = m_im.size
    tuv = Image.new("RGB", (W, H * 2 + 70), "white")
    tuv.paste(m_im, (0, 32)); tuv.paste(g_im, (0, H + 68))
    dr = ImageDraw.Draw(tuv)
    dr.text((8, 4), f"Model: 50 milyon yıl, {kaba_h:g} km simülasyon + {h_km:g} km'de {sure:g} milyon yıl akarsu aşınması", fill=(0, 0, 0), font=yazi_tipi(22))
    dr.text((8, H + 40), "Gerçek (GMT earth_relief 06', aynı izdüşüm ve renk)", fill=(0, 0, 0), font=yazi_tipi(22))
    tuv.save(f"{son}_karsilastirma.png")
    # yakın plan: Tibet, Himalaya, Tarim
    px, py = laea_ileri(np.array([70.0, 105.0]), np.array([44.0, 24.0]), dz.lon0, dz.lat0)
    c0, c1 = sorted(((px - dz.x[0]) / dz.h).astype(int)); r0, r1 = sorted(((dz.y[0] - py) / dz.h).astype(int))
    a_ = m_im.crop((c0, r0, c1, r1)); b_ = g_im.crop((c0, r0, c1, r1))
    s = 2
    a_ = a_.resize((a_.width * s, a_.height * s), Image.LANCZOS); b_ = b_.resize((b_.width * s, b_.height * s), Image.LANCZOS)
    yk = Image.new("RGB", (a_.width, a_.height * 2 + 70), "white")
    yk.paste(a_, (0, 32)); yk.paste(b_, (0, a_.height + 68))
    dr = ImageDraw.Draw(yk)
    dr.text((8, 4), "Model", fill=(0, 0, 0), font=yazi_tipi(22)); dr.text((8, a_.height + 40), "Gerçek", fill=(0, 0, 0), font=yazi_tipi(22))
    yk.save(f"{son}_yakin.png")
    print(f"toplam {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
