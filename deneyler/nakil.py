"""Gerçek bir dağ sistemini sahibin dikişine bükerek taşıma (örnek tabanlı sıradağ).

Kullanım: python -m deneyler.nakil [ORNEK]   ORNEK: zagros | himalaya

Kaynak dağ sistemi kendi dikiş çizgisine göre (boyuna konum s, dikişe işaretli uzaklık d)
koordinatlanır; hedefte sahibin duvar dikişi için aynı koordinatlar hesaplanır ve her hedef
noktası kaynaktaki karşılığından yükseklik alır. Boyuna yönde kaynak hedef uzunluğuna
esnetilir; plato tarafında (d > 300 km) uzaklık, sahibin sarı çanağının derinliği kaynağın
platosuna sığacak biçimde ölçeklenir. Kaynakta deniz olan yerler alçak ova sayılır.
Kenarlar 250 km'de arka plana yumuşakça geçer. Aşınma ve izostazi bu denemede yok.
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from deneyler.ayrinti import kuresel, ornekle
from tektonik.gorsel import _DENIZ, _RENK
from tektonik.izgara import maske_yukle
from tektonik.levha import laea_geri, laea_ileri
from tektonik.yazi import yazi_tipi

ORNEKLER = {
    # dikiş çizgisi (batıdan doğuya; plato çizginin solunda), plato derinliği (km)
    "zagros": dict(ad="Zagros ve İran platosu", cizgi=[(44.5, 36.8), (46, 35.3), (47.5, 34.2), (49, 33), (50.5, 32),
                                                       (52, 30.8), (53.5, 29.8), (55.2, 28.8), (57, 28.2), (58.5, 27.8)],
                   plato_km=620.0),
    "himalaya": dict(ad="Himalaya ve Tibet", cizgi=[(73, 35), (77, 33.5), (80, 31.5), (83, 30), (86, 29.3), (89, 29.2),
                                                     (92, 29.3), (95, 29.5)], plato_km=900.0),
}
HEDEF = [(5.1, 37.5), (10.4, 35.8), (15.7, 34.1), (21.0, 32.5), (26.3, 30.8), (31.66, 29.09), (34.5, 28.2)]
D_ARKA_KM = 300.0  # bu uzaklığa kadar dikiş çevresi birebir taşınır
GECIS_KM = 400.0


def duzlem_cizgi(cizgi):
    c = np.array(cizgi, float)
    lon0, lat0 = c[:, 0].mean(), c[:, 1].mean()
    x, y = laea_ileri(c[:, 0], c[:, 1], lon0, lat0)
    return np.c_[x, y] / 1e3, lon0, lat0


def sd(px, py, P):
    """Noktaların kırık çizgiye göre (s boyuna km, d işaretli uzaklık km, uç dışı uzaklık)."""
    seg = P[1:] - P[:-1]
    L = np.hypot(seg[:, 0], seg[:, 1])
    s0 = np.concatenate([[0], np.cumsum(L)])
    en = np.full(px.shape, np.inf); s = np.zeros(px.shape); d = np.zeros(px.shape); uc = np.zeros(px.shape)
    for i in range(len(seg)):
        t = ((px - P[i, 0]) * seg[i, 0] + (py - P[i, 1]) * seg[i, 1]) / L[i] ** 2
        tc = np.clip(t, 0, 1)
        qx, qy = P[i, 0] + tc * seg[i, 0], P[i, 1] + tc * seg[i, 1]
        dist = np.hypot(px - qx, py - qy)
        isaret = np.sign(seg[i, 0] * (py - P[i, 1]) - seg[i, 1] * (px - P[i, 0]))
        yeni = dist < en
        en = np.where(yeni, dist, en)
        s = np.where(yeni, s0[i] + t * L[i], s)  # uçlarda t sınırsız: çizginin uzantısı
        d = np.where(yeni, isaret * dist if False else isaret * np.abs(
            (px - P[i, 0]) * seg[i, 1] - (py - P[i, 1]) * seg[i, 0]) / L[i], d)
        disari = np.where(t < 0, -t * L[i], np.where(t > 1, (t - 1) * L[i], 0.0))
        uc = np.where(yeni, disari if (i == 0 or i == len(seg) - 1) else 0.0, uc)
    return s, d, uc, s0[-1]


def noktaya(s, d, P):
    """(s, d) -> düzlem noktası: çizgi üzerinde s'deki nokta + d × yumuşatılmış normal."""
    seg = P[1:] - P[:-1]
    L = np.hypot(seg[:, 0], seg[:, 1])
    s0 = np.concatenate([[0], np.cumsum(L)])
    nrm = np.c_[-seg[:, 1], seg[:, 0]] / L[:, None]  # sola dik
    # köşelerde ortalama normal; s boyunca doğrusal ara değer
    kn = np.vstack([nrm[0], 0.5 * (nrm[:-1] + nrm[1:]), nrm[-1]])
    kn /= np.linalg.norm(kn, axis=1)[:, None]
    sc = np.clip(s, 0, s0[-1])
    i = np.clip(np.searchsorted(s0, sc) - 1, 0, len(seg) - 1)
    f = (sc - s0[i]) / L[i]
    bx = P[i, 0] + f * seg[i, 0] + (s - sc) * seg[i, 0] / L[i]
    by = P[i, 1] + f * seg[i, 1] + (s - sc) * seg[i, 1] / L[i]
    nx_ = kn[i, 0] * (1 - f) + kn[i + 1, 0] * f
    ny_ = kn[i, 1] * (1 - f) + kn[i + 1, 1] * f
    nn = np.hypot(nx_, ny_)
    return bx + d * nx_ / nn, by + d * ny_ / nn


def main():
    ad = sys.argv[1] if len(sys.argv) > 1 else "zagros"
    o = ORNEKLER[ad]
    G = kuresel()
    maske, sinir = maske_yukle("veri/maske.json")
    b, g, d_, k = sinir
    der = 0.1
    lon = np.arange(b, d_, der) + der / 2
    lat = np.arange(k, g, -der) - der / 2
    LO, LA = np.meshgrid(lon, lat)
    H, W = maske.shape
    kara = maske[np.clip(((k - LA) / (k - g) * H).astype(int), 0, H - 1), np.clip(((LO - b) / (d_ - b) * W).astype(int), 0, W - 1)]

    Pt, tl0, tla0 = duzlem_cizgi(HEDEF)
    tx, ty = laea_ileri(LO, LA, tl0, tla0)
    s_t, d_t, uc_t, Lt = sd(tx / 1e3, ty / 1e3, Pt)
    Ps, sl0, sla0 = duzlem_cizgi(o["cizgi"])
    _, _, _, Ls = sd(np.zeros(1), np.zeros(1), Ps)

    # sarı çanağın dikişe en uzak noktası: plato tarafı bu derinlikten kaynağın platosuna ölçeklenir
    sen = json.load(open("veri/senaryo.json", encoding="utf-8"))
    sari = np.array(next(i for i in sen["istekler"] if i["no"] == 2)["bolge"], float)
    sx, sy = laea_ileri(sari[:, 0], sari[:, 1], tl0, tla0)
    _, d_sari, _, _ = sd(sx / 1e3, sy / 1e3, Pt)
    derinlik = max(float(d_sari.max()), D_ARKA_KM + 100)
    olcek = (o["plato_km"] - D_ARKA_KM) / (derinlik - D_ARKA_KM)

    # boyuna: en çok 1,2 kat esnet, kalan uzunluğu kaynağı aynalayarak doldur (üçgen dalga)
    esne = max(Lt / Ls, 1.0) ** 0.3 if Lt > Ls else 1.0
    u = s_t / esne
    donem = 2 * Ls
    u = np.mod(u, donem)
    s_s = np.where(u <= Ls, u, donem - u)
    # plato tarafı: ölçek değiştirmeden, kaynağın plato şeridini (D_ARKA ile plato_km arası) aynalayarak tekrarla
    pk = o["plato_km"]
    v = np.maximum(d_t - D_ARKA_KM, 0.0)
    gen = pk - D_ARKA_KM
    v = np.mod(v, 2 * gen)
    v = np.where(v <= gen, v, 2 * gen - v)
    d_s = np.where(d_t > D_ARKA_KM, D_ARKA_KM + v, d_t)
    olcek = 1.0
    qx, qy = noktaya(s_s, d_s, Ps)
    qlo, qla = laea_geri(qx * 1e3, qy * 1e3, sl0, sla0)
    z_k = ornekle(G, qlo, qla)
    z_k = np.where(z_k > 0, z_k, 80.0)  # kaynaktaki deniz: alçak ova

    # ağırlık: dikiş çevresinde 1, plato tarafında çanak derinliğine, ön tarafta 350 km'ye, uçlarda yumuşak.
    # Kenar düzensizliği uzaklıkların gürültüyle bozulmasından gelir (uzakta yeni leke doğmaz).
    rng = np.random.default_rng(4)
    gk = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 15); gk /= gk.std()
    gk2 = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 5); gk2 /= gk2.std()
    bozma = 160 * gk + 50 * gk2
    dp, ucp = d_t + bozma, uc_t + bozma
    ust = derinlik
    w = np.clip((ust + GECIS_KM - dp) / GECIS_KM, 0, 1) * np.clip((dp + 350 + GECIS_KM) / GECIS_KM, 0, 1)
    w *= np.clip(1 - ucp / GECIS_KM, 0, 1)
    w = w * w * (3 - 2 * w)
    arka = ndimage.gaussian_filter(rng.standard_normal(LO.shape), 25)
    arka = 200 + 120 * arka / arka.std()
    kiyi = ndimage.distance_transform_edt(kara) * 11.0
    z = np.where(kara, (w * z_k + (1 - w) * arka) * np.clip(kiyi / 40, 0, 1), 0.0)

    rgb = np.stack([np.interp(np.clip(z, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], -1)
    dy = der * 111.19e3
    gy, gx = np.gradient(z * 3, dy)
    gx = gx / np.cos(np.radians(LA))
    rgb = rgb * np.clip(0.85 + (-gx * 0.7 + gy * 0.7) * 0.9, 0.3, 1.3)[..., None]
    rgb = np.where(kara[..., None], rgb, _DENIZ)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    dr = ImageDraw.Draw(im)
    dr.text((8, 6), f"Örnek: {o['ad']} (boyuna esneme × {esne:.2f} ve aynalama, plato şeridi aynalı)", fill=(0, 0, 0), font=yazi_tipi(16))
    im.save(f"cikti/nakil_{ad}.png")
    # ölçüm: sarı çanak ve kırmızı kuşak
    from tektonik.kure import cokgen_ici as _ci
    from tektonik.izgara import _lonlat_xyz
    xyz = _lonlat_xyz(LO.ravel(), LA.ravel())
    m_sari = _ci(xyz, sari).reshape(LO.shape) & kara
    kirmizi = np.array(next(i for i in sen["istekler"] if i["no"] == 1)["bolge"], float)
    m_kir = _ci(xyz, kirmizi).reshape(LO.shape) & kara
    print(f"{o['ad']}: çanak ortanca {np.median(z[m_sari]):.0f} m (p10 {np.percentile(z[m_sari], 10):.0f}, p90 {np.percentile(z[m_sari], 90):.0f}); "
          f"sıradağ p95 {np.percentile(z[m_kir], 95):.0f} m, en yüksek {z.max():.0f} m; boyuna esneme {esne:.2f}, plato ölçeği {olcek:.2f}")


if __name__ == "__main__":
    main()
