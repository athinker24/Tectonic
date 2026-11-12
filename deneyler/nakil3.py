"""Taban + gerçek doku: tekrarsız, kenarsız örnek tabanlı kabartma.

Kullanım: python -m deneyler.nakil3 [TOHUM]

Taban: yumuşak bölgesel yükseklik (sıradağ kuşağı profili, çanak düzeyi, ova düzeyi), sahibin
dikişi ve sarı alanından. Doku: gerçek yükseklik verisinin 120 km'lik Gauss'la süzülmüş yüksek
geçiren kısmı (ortalaması sıfır, 300 km'den küçük şekiller); sınıfa göre (dağ, plato, ova) çok
sayıda gerçek bölgeden 640 km'lik parçalar; parçalar kendi sırt yönü x eksenine çevrilip
saklanır, hedefte dikiş boyuna çevrilir; varyansı koruyan Hann harmanlama. Aynalama yok.
"""
import json
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.ayrinti import kuresel, ornekle
from deneyler.nakil import HEDEF, duzlem_cizgi, sd
from tektonik.gorsel import _DENIZ, _RENK
from tektonik.izgara import _lonlat_xyz, maske_yukle
from tektonik.kure import cokgen_ici
from tektonik.levha import laea_geri, laea_ileri
from tektonik.yazi import yazi_tipi

KAYNAK = {
    "dag": {"Himalaya": (76, 95, 27, 31), "Orta And": (-72, -64, -25, -15), "Alpler": (5, 15, 44, 47.5),
            "Kayalık Dağlar": (-116, -105, 37, 48), "Zagros": (47, 57, 27, 34), "Tien Şan": (72, 88, 40, 44),
            "Kafkas": (40, 48, 41.5, 44), "Elburz": (50, 60, 35.5, 38.5)},
    "plato": {"İran": (52, 60, 29, 35), "Anadolu": (30, 40, 37.5, 40.5), "Moğolistan": (95, 110, 44, 49),
              "Colorado": (-112, -106, 35, 39), "Meksika": (-104, -99, 19, 25), "Etiyopya": (36, 41, 6, 13),
              "İspanya": (-6, -2, 38.5, 42)},
    "ova": {"Sahra": (-8, 28, 12, 27), "Kongo": (15, 33, -15, 3), "Brezilya": (-58, -42, -20, -6),
            "Avustralya": (120, 145, -32, -20), "Batı Sibirya": (65, 88, 55, 66), "Doğu Avrupa": (27, 52, 48, 58),
            "Kuzey Amerika": (-104, -88, 38, 52)},
}
H_KM = 10.0
P = 40          # parça: 400 km
PB = 58         # döndürme için büyük pencere
SIGMA = 12.0    # yüksek geçiren süzgeç (hücre), yaklaşık 120 km
DER = 0.1


def bolge_izgara(G, sinir):
    b, d, g, k = sinir
    lon0, lat0 = 0.5 * (b + d), 0.5 * (g + k)
    lo = np.r_[np.linspace(b, d, 40), np.linspace(b, d, 40), np.full(40, b), np.full(40, d)]
    la = np.r_[np.full(40, g), np.full(40, k), np.linspace(g, k, 40), np.linspace(g, k, 40)]
    px, py = laea_ileri(lo, la, lon0, lat0)
    x = np.arange(px.min(), px.max(), H_KM * 1e3)
    y = np.arange(py.max(), py.min(), -H_KM * 1e3)
    X, Y = np.meshgrid(x, y)
    LO, LA = laea_geri(X, Y, lon0, lat0)
    return ornekle(G, LO, LA)


def yon(a):
    """Yapı tensörüyle baskın sırt yönü (derece, x ekseninden, satır aşağı görüntü koordinatı)."""
    gy, gx = np.gradient(a)
    jxx, jyy, jxy = (gx * gx).mean(), (gy * gy).mean(), (gx * gy).mean()
    egim_aci = 0.5 * np.degrees(np.arctan2(2 * jxy, jxx - jyy))  # eğimin baskın yönü
    return egim_aci + 90.0  # sırt eğime dik


def kutuphane(G):
    lib = {}
    for sinif, bolgeler in KAYNAK.items():
        parcalar = []
        for ad, s in bolgeler.items():
            pay = 0.0 if sinif == "ova" else 2.5  # dar kuşaklar: çevresiyle birlikte al
            z = bolge_izgara(G, (s[0] - pay, s[1] + pay, s[2] - pay, s[3] + pay))
            kara = z > 0
            zz = np.where(kara, z, 0.0)
            hp = zz - ndimage.gaussian_filter(zz, SIGMA)
            ny, nx = z.shape
            for i in range(0, ny - PB, 12):
                for j in range(0, nx - PB, 12):
                    if kara[i:i + PB, j:j + PB].mean() < (0.85 if sinif != "ova" else 0.97):
                        continue
                    buyuk = hp[i:i + PB, j:j + PB]
                    a = yon(buyuk) if sinif != "ova" else 0.0
                    dd = ndimage.rotate(buyuk, a, reshape=False, order=1, mode="reflect")
                    o = (PB - P) // 2
                    parcalar.append((ad, dd[o:o + P, o:o + P].astype(np.float32)))
        lib[sinif] = parcalar
        print(f"{sinif}: {len(parcalar)} parça ({', '.join(sorted({p[0] for p in parcalar}))})", flush=True)
    return lib


def doku(lib_sinif, sekil, aci_alan, rng, adim=P // 3):
    """Varyansı koruyan Hann harmanlamayla parça yorganı; her parça hedef sırt yönüne döndürülür."""
    ny, nx = sekil
    top = np.zeros(sekil); agr = np.zeros(sekil)
    w = np.outer(np.hanning(P), np.hanning(P))
    son = []
    for i in range(-P // 2, ny, adim):
        for j in range(-P // 2, nx, adim):
            i0, j0, i1, j1 = max(i, 0), max(j, 0), min(i + P, ny), min(j + P, nx)
            if i1 <= i0 or j1 <= j0:
                continue
            # aynı parçanın yakında tekrar etmemesi için son 30 seçimden kaçın
            for _ in range(10):
                q = int(rng.integers(len(lib_sinif)))
                if q not in son:
                    break
            son = (son + [q])[-30:]
            p = lib_sinif[q][1]
            if rng.random() < 0.5:
                p = p[::-1, :]  # sırt boyunca ters çevirmek yönü bozmaz, çeşit katar
            a = aci_alan[(i0 + i1) // 2, (j0 + j1) // 2]
            dd = ndimage.rotate(p, -a, reshape=False, order=1, mode="reflect")
            ww = w[i0 - i:i1 - i, j0 - j:j1 - j]
            top[i0:i1, j0:j1] += ww * dd[i0 - i:i1 - i, j0 - j:j1 - j]
            agr[i0:i1, j0:j1] += ww * ww
    return top / np.sqrt(np.maximum(agr, 1e-9))


def main():
    tohum = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rng = np.random.default_rng(tohum)
    t0 = time.time()
    G = kuresel()
    lib = kutuphane(G)
    print(f"kütüphane {time.time() - t0:.0f} s", flush=True)

    maske, sinir = maske_yukle("veri/maske.json")
    b, g, d_, k = sinir
    lon = np.arange(b, d_, DER) + DER / 2
    lat = np.arange(k, g, -DER) - DER / 2
    LO, LA = np.meshgrid(lon, lat)
    Hh, Ww = maske.shape
    kara = maske[np.clip(((k - LA) / (k - g) * Hh).astype(int), 0, Hh - 1), np.clip(((LO - b) / (d_ - b) * Ww).astype(int), 0, Ww - 1)]
    sen = json.load(open("veri/senaryo.json", encoding="utf-8"))
    sari = np.array(next(i for i in sen["istekler"] if i["no"] == 2)["bolge"], float)
    kirmizi = np.array(next(i for i in sen["istekler"] if i["no"] == 1)["bolge"], float)
    xyz = _lonlat_xyz(LO.ravel(), LA.ravel())
    m_sari = cokgen_ici(xyz, sari).reshape(LO.shape)
    m_kir = cokgen_ici(xyz, kirmizi).reshape(LO.shape) & kara

    # dikiş koordinatları ve hedef sırt yönü (dikiş boyunca)
    Pt, tl0, tla0 = duzlem_cizgi(HEDEF)
    tx, ty = laea_ileri(LO, LA, tl0, tla0)
    s_t, d_t, uc_t, Lt = sd(tx / 1e3, ty / 1e3, Pt)
    gk = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 15); gk /= gk.std()
    gk2 = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 5); gk2 /= gk2.std()
    dp, ucp = d_t + 120 * gk + 40 * gk2, uc_t + 120 * gk + 40 * gk2
    # dikişin yerel doğrultusu: s alanının eğimi (görüntü koordinatında açı)
    sy_, sx_ = np.gradient(ndimage.gaussian_filter(s_t, 4))
    aci_dikis = np.degrees(np.arctan2(sy_, sx_))

    # taban
    def yum(x):
        return x * x * (3 - 2 * x)
    uc_w = yum(np.clip(1 - ucp / 450.0, 0, 1))
    w_dag = yum(np.clip(1 - np.abs(dp + 40) / 380.0, 0, 1)) * uc_w
    # çanak kenarı: çokgene işaretli uzaklık, büyük ve küçük ölçekli gürültüyle bozulmuş
    ic_km = ndimage.distance_transform_edt(m_sari) * 11.0 - ndimage.distance_transform_edt(~m_sari) * 11.0
    g3 = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 25); g3 /= g3.std()
    ic_km = ic_km + 180 * g3 + 60 * gk2
    w_plato = yum(np.clip((ic_km + 150) / 300.0, 0, 1)) * yum(np.clip((dp - 80) / 220.0, 0, 1))
    ova = 250 + 180 * ndimage.gaussian_filter(rng.standard_normal(LO.shape), 40) / 0.02
    ova = 250 + 180 * (ova - ova.mean()) / ova.std()
    kiyi = ndimage.distance_transform_edt(kara) * 11.0
    ova *= np.clip(kiyi / 150, 0.15, 1)
    tepe = (3000 * np.exp(-((dp + 50) / 210.0) ** 2) + 900 * np.exp(-((dp + 220) / 120.0) ** 2)) * uc_w
    taban = ova + w_plato * (1250 - ova)
    taban = np.maximum(taban, ova + tepe)

    # doku: sınıf ağırlıklarıyla
    sekil = LO.shape
    d_dag = doku(lib["dag"], sekil, aci_dikis, rng)
    d_pla = doku(lib["plato"], sekil, aci_dikis, rng)
    d_ova = doku(lib["ova"], sekil, rng.uniform(0, 180, sekil) * 0 + ndimage.gaussian_filter(rng.uniform(0, 180, sekil), 30), rng)
    w_ova = np.clip(1 - w_dag - w_plato, 0, 1)
    top_w = w_dag + w_plato + w_ova
    d_dag = d_dag * 1.4  # kuşak dokusu: gerçek kuşakların yüksek geçiren genliği kaynakta dar şeritte seyreliyor
    dk = (w_dag * d_dag + w_plato * d_pla + w_ova * d_ova) / np.sqrt(np.maximum(w_dag ** 2 + w_plato ** 2 + w_ova ** 2, 1e-9)) * np.minimum(top_w, 1)
    z = np.where(kara, np.maximum(taban + dk, 0) * np.clip(kiyi / 30, 0, 1), 0.0)
    print(f"sentez {time.time() - t0:.0f} s", flush=True)

    rgb = np.stack([np.interp(np.clip(z, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    dyy = DER * 111.19e3
    gy, gx = np.gradient(z * 3, dyy)
    gx = gx / np.cos(np.radians(LA))
    rgb = rgb * np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9, 0.3, 1.3)[..., None]
    rgb = np.where(kara[..., None], rgb, _DENIZ)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    ImageDraw.Draw(im).text((8, 6), "Taban + gerçek doku (22 bölgeden, aynalama yok)", fill=(0, 0, 0), font=yazi_tipi(16))
    im.save(f"cikti/nakil3_{tohum}.png")
    np.save(f"cikti/nakil3_{tohum}_z.npy", z.astype(np.float32))
    ic = m_sari & kara & (w_plato > 0.9)
    print(f"çanak iç ortanca {np.median(z[ic]):.0f} m (p10 {np.percentile(z[ic], 10):.0f}, p90 {np.percentile(z[ic], 90):.0f}); "
          f"sıradağ p95 {np.percentile(z[m_kir], 95):.0f} m; en yüksek {z.max():.0f} m; kara ortanca {np.median(z[kara]):.0f} m")


if __name__ == "__main__":
    main()
