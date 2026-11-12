"""Birleşik örnek: Himalaya sıradağı + İran platosu çanağı + gerçek ova ve kalkanlardan arka plan.

Kullanım: python -m deneyler.nakil2 [TOHUM]

1. Sıradağ şeridi (dikişin önünde 350 km ile arkasında 120 km arası): Himalaya'dan, dikişe bükülerek.
2. Çanak (dikişin 250 km gerisinden sarı alanın sonuna): İran platosunun iç şeridinden (Ana Zagros
   bindirmesinin 300 ile 620 km kuzeydoğusu), aynalanarak; ortancası sahibin istediği 1000 ile
   1500 m aralığının ortasına (1250 m) sabit yükseltmeyle getirilir.
3. Kıtanın geri kalanı: dağsız gerçek bölgelerden (Sahra, Kongo, Brezilya, Avustralya, Batı Sibirya,
   Doğu Avrupa, Kuzey Amerika düzlükleri) 1200 km'lik rastgele döndürülmüş parçalar; ortalama
   düzeyi ağırlıklı ortalamayla, ayrıntı varyansı koruyan harmanlamayla.
Aşınma ve izostazi yok; dikiş izlerini birleştirecek aşınma koşusu sonraki adım.
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.ayrinti import kuresel, ornekle
from deneyler.nakil import D_ARKA_KM, HEDEF, ORNEKLER, duzlem_cizgi, noktaya, sd
from tektonik.gorsel import _DENIZ, _RENK
from tektonik.izgara import _lonlat_xyz, maske_yukle
from tektonik.kure import cokgen_ici
from tektonik.levha import laea_geri, laea_ileri
from tektonik.yazi import yazi_tipi

ARKA_KAYNAK = {
    "Sahra": (-8, 28, 12, 27), "Kongo": (15, 33, -15, 3), "Brezilya": (-58, -42, -20, -6),
    "Avustralya": (120, 145, -32, -20), "Batı Sibirya": (65, 88, 55, 66), "Doğu Avrupa": (27, 52, 48, 58),
    "Kuzey Amerika düzlükleri": (-104, -88, 38, 52),
}
DER = 0.1


def tasinan(G, LO, LA, cizgi_kaynak, d_kaynak_fonk, s_esne_ust=1.2):
    """Hedef ızgaranın her noktası için kaynaktan yükseklik (boyuna aynalı, d dönüşümü verilen)."""
    Pt, tl0, tla0 = duzlem_cizgi(HEDEF)
    tx, ty = laea_ileri(LO, LA, tl0, tla0)
    s_t, d_t, uc_t, Lt = sd(tx / 1e3, ty / 1e3, Pt)
    Ps, sl0, sla0 = duzlem_cizgi(cizgi_kaynak)
    _, _, _, Ls = sd(np.zeros(1), np.zeros(1), Ps)
    esne = min(max(Lt / Ls, 1.0) ** 0.3, s_esne_ust)
    u = np.mod(s_t / esne, 2 * Ls)
    s_s = np.where(u <= Ls, u, 2 * Ls - u)
    qx, qy = noktaya(s_s, d_kaynak_fonk(d_t), Ps)
    qlo, qla = laea_geri(qx * 1e3, qy * 1e3, sl0, sla0)
    return ornekle(G, qlo, qla), d_t, uc_t


def aynali(d, a, b):
    """d'yi [a, b] aralığında aynalayarak tekrarla."""
    gen = b - a
    v = np.mod(np.maximum(d - a, 0.0), 2 * gen)
    return a + np.where(v <= gen, v, 2 * gen - v)


def arka_plan(G, LO, LA, kara, rng, P=120, adim=60):
    ny, nx = LO.shape
    kaynaklar = []
    for ad, (b, d, g, k) in ARKA_KAYNAK.items():
        kaynaklar.append((ad, 0.5 * (b + d), 0.5 * (g + k), (d - b) * 111 * np.cos(np.radians(0.5 * (g + k))), (k - g) * 111))
    ort_top = np.zeros(LO.shape); ort_agr = np.zeros(LO.shape)
    ay_top = np.zeros(LO.shape); ay_agr = np.zeros(LO.shape)
    w = np.outer(np.hanning(P), np.hanning(P))
    for i in range(-P // 2, ny, adim):
        for j in range(-P // 2, nx, adim):
            i0, j0 = max(i, 0), max(j, 0)
            i1, j1 = min(i + P, ny), min(j + P, nx)
            if i1 <= i0 or j1 <= j0 or not kara[i0:i1, j0:j1].any():
                continue
            ad, clo, cla, gx_km, gy_km = kaynaklar[rng.integers(len(kaynaklar))]
            lc, ac = LO[(i0 + i1) // 2, (j0 + j1) // 2], LA[(i0 + i1) // 2, (j0 + j1) // 2]
            dx = (LO[i0:i1, j0:j1] - lc) * 111.19 * np.cos(np.radians(ac))
            dy = (LA[i0:i1, j0:j1] - ac) * 111.19
            a = rng.uniform(0, 2 * np.pi)
            rx, ry = dx * np.cos(a) - dy * np.sin(a), dx * np.sin(a) + dy * np.cos(a)
            ox = rng.uniform(-0.3, 0.3) * gx_km; oy = rng.uniform(-0.3, 0.3) * gy_km
            slo, sla = laea_geri((rx + ox) * 1e3, (ry + oy) * 1e3, clo, cla)
            z = ornekle(G, slo, sla)
            z = np.where(z > 0, z, np.nan)
            m = np.nanmedian(z) if np.isfinite(z).any() else 200.0
            z = np.where(np.isfinite(z), z, m)
            ww = w[i0 - i:i1 - i, j0 - j:j1 - j]
            ort_top[i0:i1, j0:j1] += ww * m; ort_agr[i0:i1, j0:j1] += ww
            ay_top[i0:i1, j0:j1] += ww * (z - m); ay_agr[i0:i1, j0:j1] += ww * ww
    ort = ort_top / np.maximum(ort_agr, 1e-9)
    ay = ay_top / np.sqrt(np.maximum(ay_agr, 1e-9))
    return ort + ay


def main():
    tohum = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    rng = np.random.default_rng(tohum)
    G = kuresel()
    maske, sinir = maske_yukle("veri/maske.json")
    b, g, d_, k = sinir
    lon = np.arange(b, d_, DER) + DER / 2
    lat = np.arange(k, g, -DER) - DER / 2
    LO, LA = np.meshgrid(lon, lat)
    H, W = maske.shape
    kara = maske[np.clip(((k - LA) / (k - g) * H).astype(int), 0, H - 1), np.clip(((LO - b) / (d_ - b) * W).astype(int), 0, W - 1)]
    sen = json.load(open("veri/senaryo.json", encoding="utf-8"))
    sari = np.array(next(i for i in sen["istekler"] if i["no"] == 2)["bolge"], float)
    kirmizi = np.array(next(i for i in sen["istekler"] if i["no"] == 1)["bolge"], float)
    xyz = _lonlat_xyz(LO.ravel(), LA.ravel())
    m_sari = cokgen_ici(xyz, sari).reshape(LO.shape) & kara
    m_kir = cokgen_ici(xyz, kirmizi).reshape(LO.shape) & kara

    # 1. sıradağ: Himalaya, d birebir (dikişin güneyinde yüksek Himalaya, kuzeyinde Tibet kenarı)
    z_him, d_t, uc_t = tasinan(G, LO, LA, ORNEKLER["himalaya"]["cizgi"], lambda d: aynali(d + 400.0, 0.0, 750.0) - 400.0)
    z_him = np.where(z_him > 0, z_him, 80.0)
    # 2. çanak: İran platosu iç şeridi, aynalı
    z_ir, _, _ = tasinan(G, LO, LA, ORNEKLER["zagros"]["cizgi"], lambda d: aynali(d, 300.0, 620.0))
    z_ir = np.where(z_ir > 0, z_ir, 80.0)
    # sıradağdan çanağa geçiş (dikişin 120 ile 300 km gerisi), düzensiz
    gk = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 15); gk /= gk.std()
    gk2 = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 5); gk2 /= gk2.std()
    dp, ucp = d_t + 160 * gk + 50 * gk2, uc_t + 160 * gk + 50 * gk2
    t = np.clip((dp - 120.0) / 180.0, 0, 1); t = t * t * (3 - 2 * t)
    # çanak ölçeği: sarı alanın içinde kalan çanak noktalarının ortancası 1250 m olsun
    ic = m_sari & (t > 0.9)
    # dikey germe yerine sabit yükseltme (havzalar da kalkar, dağların sertliği değişmez)
    olcek = 1250.0 - float(np.median(z_ir[ic])) if ic.any() else 0.0
    z_dag = (1 - t) * z_him + t * (z_ir + olcek)

    # 3. ağırlık: çanak sarı alanın sonuna kadar, ön tarafta 350 km, uçlarda yumuşak
    Pt, tl0, tla0 = duzlem_cizgi(HEDEF)
    sx, sy = laea_ileri(sari[:, 0], sari[:, 1], tl0, tla0)
    _, d_sari, _, _ = sd(sx / 1e3, sy / 1e3, Pt)
    derinlik = float(d_sari.max())
    G_ = 400.0
    w = np.clip((derinlik + G_ - dp) / G_, 0, 1) * np.clip((dp + 350 + G_) / G_, 0, 1) * np.clip(1 - ucp / G_, 0, 1)
    w = w * w * (3 - 2 * w)

    arka = arka_plan(G, LO, LA, kara, rng)
    kiyi = ndimage.distance_transform_edt(kara) * 11.0
    z = np.where(kara, np.maximum(w * z_dag + (1 - w) * arka, 0) * np.clip(kiyi / 40, 0, 1), 0.0)

    rgb = np.stack([np.interp(np.clip(z, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    dy = DER * 111.19e3
    gy, gx = np.gradient(z * 3, dy)
    gx = gx / np.cos(np.radians(LA))
    rgb = rgb * np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9, 0.3, 1.3)[..., None]
    rgb = np.where(kara[..., None], rgb, _DENIZ)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    ImageDraw.Draw(im).text((8, 6), "Himalaya sıradağı + İran platosu çanağı + gerçek ova ve kalkan arka planı", fill=(0, 0, 0), font=yazi_tipi(16))
    im.save("cikti/nakil_birlesik.png")
    np.save("cikti/nakil_birlesik_z.npy", z.astype(np.float32))
    print(f"çanak (sarı) ortanca {np.median(z[m_sari]):.0f} m (p10 {np.percentile(z[m_sari], 10):.0f}, p90 {np.percentile(z[m_sari], 90):.0f}); "
          f"sıradağ (kırmızı) p95 {np.percentile(z[m_kir], 95):.0f} m; en yüksek {z.max():.0f} m; "
          f"kara ortanca {np.median(z[kara]):.0f} m; çanak yükseltmesi {olcek:+.0f} m")


if __name__ == "__main__":
    main()
