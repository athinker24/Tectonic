"""Ayrıntı katmanı denemesi: gerçek yükseklik verisinden bağlama uygun orta ölçek ayrıntı.

Kullanım: python -m deneyler.ayrinti [MODEL_Z_NPY]

Kütüphane: Amerika, Afrika ve Avrupa'nın 10 km'lik gerçek yüksekliği (GMT earth_relief 06'),
50 km'lik kaba hâli ve aradaki fark (ayrıntı). Her 480 km'lik parça, kaba yüksekliği ve kaba
eğimi ile etiketlenir; ayrıntı, kaba eğim +x yönüne bakacak biçimde döndürülüp saklanır.
Hedef: kalıpsız levha modelinin Asya'sı (50 km). Her pencereye bağlamı en yakın parçalardan
biri, hedefin eğim yönüne döndürülerek eklenir; pencereler Hann ağırlığıyla harmanlanır.
Asya kütüphanede yok (kendi şekillerini geri koymamak için).
"""
import json
import sys
import time

import h5py
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree

from deneyler.dunya import SINIR, gercek_yukseklik
from tektonik.gorsel import _DENIZ, _RENK
from tektonik.levha import duzlem_kur, laea_geri, laea_ileri
from tektonik.yazi import yazi_tipi

H = 10.0  # km, ince ızgara
OLCEK = 5  # kaba = 50 km
P = 48  # parça (480 km)
PB = 68  # döndürme için büyük pencere
ADIM = 16

KUTUPHANE = {
    "Güney Amerika": (-82, -56, -34, 13),
    "Kuzey Amerika": (-130, 15, -60, 62),
    "Afrika": (-18, -35, 52, 37),
    "Avrupa": (-10, 36, 40, 62),
}


def kuresel():
    f = h5py.File("veri/dunya/earth_relief_06m_p.grd", "r")
    lon, lat = f["lon"][:], f["lat"][:]
    z = f["z"][:].astype(np.float32) * float(f["z"].attrs.get("scale_factor", [1.0])[0])
    if lat[0] > lat[-1]:
        lat, z = lat[::-1], z[::-1]
    return lon, lat, z


def ornekle(G, LO, LA):
    lon, lat, z = G
    c = (np.mod(LO - lon[0], 360.0)) / (lon[1] - lon[0])
    r = (LA - lat[0]) / (lat[1] - lat[0])
    return ndimage.map_coordinates(z, [r, c], order=1, mode="nearest")


def bolge(G, sinir, h_km=H):
    b, g, d, k = sinir
    lon0, lat0 = 0.5 * (b + d), 0.5 * (g + k)
    lo = np.concatenate([np.linspace(b, d, 50), np.linspace(b, d, 50), np.full(50, b), np.full(50, d)])
    la = np.concatenate([np.full(50, g), np.full(50, k), np.linspace(g, k, 50), np.linspace(g, k, 50)])
    px, py = laea_ileri(lo, la, lon0, lat0)
    x = np.arange(px.min(), px.max(), h_km * 1e3)
    y = np.arange(py.max(), py.min(), -h_km * 1e3)
    n = (len(y) // OLCEK) * OLCEK, (len(x) // OLCEK) * OLCEK
    X, Y = np.meshgrid(x[: n[1]], y[: n[0]])
    LO, LA = laea_geri(X, Y, lon0, lat0)
    return ornekle(G, LO, LA)


def kaba(z):
    ny, nx = z.shape
    k = z.reshape(ny // OLCEK, OLCEK, nx // OLCEK, OLCEK).mean(axis=(1, 3))
    return k, ndimage.zoom(k, OLCEK, order=1)[:ny, :nx]


def egim(kz):
    gy, gx = np.gradient(kz, H * OLCEK)  # m/km, satır güneye
    return gx, -gy


def kutuphane_kur(G):
    oz, parcalar = [], []
    for ad, s in KUTUPHANE.items():
        z = bolge(G, s)
        kara = z > 0
        _, up = kaba(np.where(kara, z, 0))
        art = np.where(kara, z - up, 0.0)
        gx, gy = egim(ndimage.gaussian_filter(up, 2))
        ny, nx = z.shape
        sayi = 0
        for i in range(0, ny - PB, ADIM):
            for j in range(0, nx - PB, ADIM):
                if kara[i:i + PB, j:j + PB].mean() < 0.97:
                    continue
                ci, cj = i + PB // 2, j + PB // 2
                ex, ey = gx[ci - 8:ci + 8, cj - 8:cj + 8].mean(), gy[ci - 8:ci + 8, cj - 8:cj + 8].mean()
                aci = np.degrees(np.arctan2(ey, ex))
                buyuk = art[i:i + PB, j:j + PB]
                # eğim yönünü +x'e çevir (görüntü koordinatında y aşağı: açıyı ters işaretle döndür)
                d = ndimage.rotate(buyuk, -aci, reshape=False, order=1, mode="reflect")
                o = (PB - P) // 2
                parcalar.append(d[o:o + P, o:o + P].astype(np.float32))
                oz.append((up[ci, cj] / 500.0, np.hypot(ex, ey) / 2.0, up[i:i + PB, j:j + PB].std() / 300.0))
                sayi += 1
        print(f"{ad}: {sayi} parça", flush=True)
    return np.array(oz), np.array(parcalar)


def sentez(up, kara, oz, parcalar, rng, k=6):
    ny, nx = up.shape
    gx, gy = egim(ndimage.gaussian_filter(up, 2))
    agac = cKDTree(oz)
    top = np.zeros(up.shape); agr = np.zeros(up.shape)
    w = np.outer(np.hanning(P), np.hanning(P))
    o = P // 2
    for i in range(0, ny - P, P // 3):
        for j in range(0, nx - P, P // 3):
            if kara[i:i + P, j:j + P].mean() < 0.3:
                continue
            ci, cj = i + o, j + o
            ex, ey = gx[ci - 8:ci + 8, cj - 8:cj + 8].mean(), gy[ci - 8:ci + 8, cj - 8:cj + 8].mean()
            q = (up[ci, cj] / 500.0, np.hypot(ex, ey) / 2.0, up[i:i + P, j:j + P].std() / 300.0)
            _, idx = agac.query(q, k=k)
            p = parcalar[rng.choice(np.atleast_1d(idx))]
            aci = np.degrees(np.arctan2(ey, ex))
            d = ndimage.rotate(p, aci, reshape=False, order=1, mode="reflect")
            top[i:i + P, j:j + P] += w * d
            agr[i:i + P, j:j + P] += w * w
    # varyansı koruyan harmanlama: bağımsız parçaların ortalaması genliği söndürmesin
    art = np.where(agr > 1e-6, top / np.sqrt(np.maximum(agr, 1e-6)), 0.0)
    kiyi = ndimage.distance_transform_edt(kara) * H
    return np.where(kara, np.maximum(up + art * np.clip(kiyi / 30.0, 0, 1), 0.0), 0.0)


def kabartma(z, kara):
    zz = np.where(kara, z, 0.0)
    rgb = np.stack([np.interp(np.clip(zz, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    gy, gx = np.gradient(zz * 3, H * 1e3)
    rgb = rgb * np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9, 0.3, 1.3)[..., None]
    rgb = np.where(kara[..., None], rgb, _DENIZ)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def spek(a, kara):
    a = np.where(kara, a, 0.0); a = a - a.mean()
    w = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1]))
    F = np.abs(np.fft.fftshift(np.fft.fft2(a * w))) ** 2
    yy, xx = np.indices(F.shape)
    rr = np.hypot((yy - F.shape[0] / 2) / F.shape[0], (xx - F.shape[1] / 2) / F.shape[1])
    return F, rr


def main():
    yol = sys.argv[1] if len(sys.argv) > 1 else "cikti/dunya/dunya_50km_eta3e+22_k5e-10_o1_avr2500_s10_y1_t1_kn50_d0_h0_s11_b80_z.npy"
    t0 = time.time()
    G = kuresel()
    oz, parcalar = kutuphane_kur(G)
    print(f"kütüphane {len(parcalar)} parça, {time.time() - t0:.0f} s", flush=True)

    # hedef: dünya deneyinin 50 km ızgarası, 10 km'ye
    zr, lo_r, la_r = gercek_yukseklik()
    dz = duzlem_kur(zr > 0, SINIR, h_km=50.0, pay_km=500.0)
    m50 = np.load(yol).astype(float)
    # Asya kutusu
    kut = (dz.lon > 55) & (dz.lon < 125) & (dz.lat > 18) & (dz.lat < 56)
    r, c = np.nonzero(kut)
    r0, r1, c0, c1 = r.min(), r.max() + 1, c.min(), c.max() + 1
    m = m50[r0:r1, c0:c1]
    x = dz.x[c0] + (np.arange((c1 - c0) * OLCEK) - (OLCEK // 2)) * H * 1e3
    y = dz.y[r0] - (np.arange((r1 - r0) * OLCEK) - (OLCEK // 2)) * H * 1e3
    X, Y = np.meshgrid(x, y)
    LO, LA = laea_geri(X, Y, dz.lon0, dz.lat0)
    gercek = ornekle(G, LO, LA)
    kara = gercek > 0
    up = ndimage.zoom(m, OLCEK, order=1)[: len(y), : len(x)]
    up = np.where(kara, np.maximum(up, 0), 0)
    rng = np.random.default_rng(1)
    t1 = time.time()
    ince = sentez(up, kara, oz, parcalar, rng)
    print(f"sentez {time.time() - t1:.0f} s, ızgara {ince.shape}", flush=True)

    # ölçüm: dalga boyuna göre güç oranı (model / gerçek), yalnız model ve ayrıntılı
    Fg, rr = spek(gercek, kara)
    Fu, _ = spek(up, kara)
    Fi, _ = spek(ince, kara)
    sonuc = {}
    for lam in (400, 250, 160, 100, 60, 40, 25):
        f = H / lam  # döngü / hücre
        b = (rr > f / 1.25) & (rr < f * 1.25)
        sonuc[f"{lam} km"] = dict(yalniz_model=round(float(Fu[b].mean() / Fg[b].mean()), 2),
                                  ayrintili=round(float(Fi[b].mean() / Fg[b].mean()), 2))

    def pur(a, n):
        mu = ndimage.uniform_filter(a, n); sq = ndimage.uniform_filter(a * a, n)
        return np.sqrt(np.maximum(sq - mu * mu, 0))
    yuksek = kara & (gercek > 1500)
    for n in (3, 9):
        sonuc[f"yerel engebe {n * H:.0f} km (yüksek kesim)"] = dict(
            yalniz_model=round(float(np.median(pur(up, n)[yuksek]))), ayrintili=round(float(np.median(pur(ince, n)[yuksek]))),
            gercek=round(float(np.median(pur(gercek, n)[yuksek]))))
    print(json.dumps(sonuc, ensure_ascii=False, indent=1))
    json.dump(sonuc, open("cikti/dunya/ayrinti_olcum.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    ims = [kabartma(up, kara), kabartma(ince, kara), kabartma(np.where(kara, gercek, 0), kara)]
    adl = ["Model (50 km)", "Model + gerçek veriden ayrıntı", "Gerçek (10 km)"]
    W, Hh = ims[0].size
    tuv = Image.new("RGB", (W, Hh * 3 + 90), "white")
    for i, (im, ad) in enumerate(zip(ims, adl)):
        tuv.paste(im, (0, 30 + i * (Hh + 30)))
        ImageDraw.Draw(tuv).text((6, 5 + i * (Hh + 30)), ad, fill=(0, 0, 0), font=yazi_tipi(20))
    tuv.save("cikti/dunya/ayrinti_karsilastirma.png")
    np.save("cikti/dunya/ayrinti_z.npy", ince.astype(np.float32))
    print(f"toplam {time.time() - t0:.0f} s")




def yonlu_sirtlar(up, kara, rng, uzun_km=180.0, kisa_km=22.0, yon_sayisi=12):
    """Kaba yüksekliğin eş yükselti çizgilerine paralel, uzun ve dar sırtlar (yönlü gürültü).

    Sıkışan kuşaklarda sıralar sıkışmaya dik, yani kaba eğime dik uzanır. Her yön için beyaz
    gürültü o yönde uzun, dik yönde dar bir Gauss çekirdeğiyle süzülür; her hücre kendi sırt
    yönüne en yakın iki yönün sonucunu alır. Genlik kaba eğim ve yükseklikle büyür."""
    gx, gy = egim(ndimage.gaussian_filter(up, 3))
    sirt_aci = (np.degrees(np.arctan2(gy, gx)) + 90.0) % 180.0  # eş yükselti yönü
    ny, nx = up.shape
    n = rng.standard_normal((ny, nx))
    alanlar = []
    for k in range(yon_sayisi):
        a = 180.0 * k / yon_sayisi
        d = ndimage.rotate(n, -a, reshape=True, order=1, mode="wrap")
        d = ndimage.gaussian_filter(d, (kisa_km / H, uzun_km / H))  # satır yönü dar, sütun yönü uzun
        d = ndimage.rotate(d, a, reshape=True, order=1)
        oy, ox = (d.shape[0] - ny) // 2, (d.shape[1] - nx) // 2
        d = d[oy:oy + ny, ox:ox + nx]
        alanlar.append(d / (d.std() + 1e-9))
    alanlar = np.array(alanlar)
    t = sirt_aci / (180.0 / yon_sayisi)
    i0 = np.floor(t).astype(int) % yon_sayisi
    i1 = (i0 + 1) % yon_sayisi
    f = t - np.floor(t)
    r = np.take_along_axis(alanlar, i0[None], 0)[0] * np.cos(f * np.pi / 2) + np.take_along_axis(alanlar, i1[None], 0)[0] * np.sin(f * np.pi / 2)
    # sırt biçimi: tepeler keskin, vadiler geniş (|gürültü| tersine çevrilmiş)
    r = 1.0 - 2.0 * np.abs(np.tanh(r))
    egm = np.hypot(gx, gy)  # m/km
    genlik = 120.0 * np.clip(egm / 4.0, 0, 3) + 0.12 * np.clip(up - 500, 0, None)
    return r * genlik


def main_yonlu():
    yol = sys.argv[2]
    G = kuresel()
    oz, parcalar = kutuphane_kur(G)
    zr, lo_r, la_r = gercek_yukseklik()
    dz = duzlem_kur(zr > 0, SINIR, h_km=50.0, pay_km=500.0)
    m50 = np.load(yol).astype(float)
    kut = (dz.lon > 55) & (dz.lon < 125) & (dz.lat > 18) & (dz.lat < 56)
    r, c = np.nonzero(kut)
    r0, r1, c0, c1 = r.min(), r.max() + 1, c.min(), c.max() + 1
    m = m50[r0:r1, c0:c1]
    x = dz.x[c0] + (np.arange((c1 - c0) * OLCEK) - (OLCEK // 2)) * H * 1e3
    y = dz.y[r0] - (np.arange((r1 - r0) * OLCEK) - (OLCEK // 2)) * H * 1e3
    X, Y = np.meshgrid(x, y)
    LO, LA = laea_geri(X, Y, dz.lon0, dz.lat0)
    gercek = ornekle(G, LO, LA)
    kara = gercek > 0
    up = np.where(kara, np.maximum(ndimage.zoom(m, OLCEK, order=1)[: len(y), : len(x)], 0), 0)
    rng = np.random.default_rng(1)
    t0 = time.time()
    sirt = yonlu_sirtlar(up, kara, rng)
    ince_doku = sentez(up, kara, oz, parcalar, rng) - up
    kiyi = ndimage.distance_transform_edt(kara) * H
    ince = np.where(kara, np.maximum(up + (sirt + 0.5 * ince_doku) * np.clip(kiyi / 30, 0, 1), 0), 0)
    print(f"yönlü sentez {time.time() - t0:.0f} s")
    Fg, rr = spek(gercek, kara); Fi, _ = spek(ince, kara)
    sonuc = {}
    for lam in (400, 250, 160, 100, 60, 40, 25):
        f = H / lam; b = (rr > f / 1.25) & (rr < f * 1.25)
        sonuc[f"{lam} km"] = round(float(Fi[b].mean() / Fg[b].mean()), 2)

    def pur(a, n):
        mu = ndimage.uniform_filter(a, n); sq = ndimage.uniform_filter(a * a, n)
        return np.sqrt(np.maximum(sq - mu * mu, 0))
    yuksek = kara & (gercek > 1500)
    for n in (3, 9):
        sonuc[f"engebe {n * H:.0f} km"] = [round(float(np.median(pur(ince, n)[yuksek]))), round(float(np.median(pur(gercek, n)[yuksek])))]
    print(json.dumps(sonuc, ensure_ascii=False))
    ims = [kabartma(ince, kara), kabartma(np.where(kara, gercek, 0), kara)]
    W, Hh = ims[0].size
    tuv = Image.new("RGB", (W, Hh * 2 + 60), "white")
    for i, (im, ad) in enumerate(zip(ims, ["Model + yönlü sırtlar + gerçek doku", "Gerçek (10 km)"])):
        tuv.paste(im, (0, 30 + i * (Hh + 30)))
        ImageDraw.Draw(tuv).text((6, 5 + i * (Hh + 30)), ad, fill=(0, 0, 0), font=yazi_tipi(20))
    tuv.save("cikti/dunya/ayrinti_yonlu.png")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "yonlu":
        main_yonlu()
    else:
        main()
