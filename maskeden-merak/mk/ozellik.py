"""Karşılık birleşiminin üstüne adlı düzeltme adımları (ozellikler.json, sırayla uygulanır). Hepsi yalnız karada çalışır.

Ortak alanlar: "ad" (açıklama), "tur", koordinatlar maske pikseli, uzunluklar km, yükseklikler m.

tur "sirt"   : bir çizgi boyunca sıradağ. Boru görünmesin diye: genişlik gürültülü, çizgi bükülür, uçlar incelerek alçalır,
               doku gerçek bir yerden (doku: karşılık sözlüğü, nokta'lar çizgi boyunca) ya da yoksa sırt gürültüsünden.
               alanlar: cizgi, yukseklik (sayı ya da her köşe için liste; sırtın tepe yüksekliği), yari_km (sayı ya da liste),
               incel [baş_payı, son_payı] (0..1, varsayılan [0.1, 0.3]), doku (isteğe bağlı), doku_kat (1), ust (yumuşak tavan)
tur "alcalt" : bölgede ya da çizgi çevresinde taban üstünü bastırır (ön ova, alçak ova, düz Ural izi silme).
               alanlar: bolge ya da (cizgi + yari_km), taban, kat (taban üstünde kalan pay, 0..1), yumusak_km
tur "kabart" : geniş ve alçak kabartı. alanlar: bolge ya da (cizgi + yari_km), m (sayı ya da çizgi köşelerine liste), yumusak_km
tur "cukur_doldur": bölgedeki derin çukurları çevre düzeyine yaklaştırır. alanlar: bolge, olcek_km (90), pay (150)
tur "yama"   : bölgeyi başka bir karşılıkla değiştirir (karsiliklar.json biçiminde sözlük, bolge dahil); kıyı rampası korunur.
"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree

from .karsilik import gurultu, ornekle
from .proje import log


def _cokgen(shape, pts):
    im = Image.new("F", (shape[1], shape[0]), 0.0)
    ImageDraw.Draw(im).polygon([tuple(q) for q in pts], fill=1.0)
    return np.asarray(im)


def _yogun(c, n=60):
    c = np.asarray(c, float)
    return np.vstack([c[i] + (c[i + 1] - c[i]) * t for i in range(len(c) - 1) for t in np.linspace(0, 1, n)[:, None]])


def _boyunca(v, nkose, n=60):
    v = np.broadcast_to(np.asarray(v, float), (nkose,)) if np.ndim(v) == 0 else np.asarray(v, float)
    return np.concatenate([v[i] + (v[i + 1] - v[i]) * np.linspace(0, 1, n) for i in range(len(v) - 1)])


def _cizgi_alan(shape, cizgi, km_px, pay_km, bukme=None, adim=2):
    """Çizginin çevresindeki kutuda (uzaklık km, çizgi boyunca t 0..1, kutu dilimi); adim'lık seyrek ızgarada sorgu."""
    pts = _yogun(cizgi)
    ny, nx = shape; pay = pay_km / km_px
    r0, r1 = max(int(pts[:, 1].min() - pay), 0), min(int(pts[:, 1].max() + pay) + 1, ny)
    c0, c1 = max(int(pts[:, 0].min() - pay), 0), min(int(pts[:, 0].max() + pay) + 1, nx)
    yy, xx = np.mgrid[r0:r1:adim, c0:c1:adim].astype(np.float32)
    if bukme is not None:
        xx = xx + bukme[0][r0:r1:adim, c0:c1:adim]; yy = yy + bukme[1][r0:r1:adim, c0:c1:adim]
    d, i = cKDTree(pts).query(np.stack([xx.ravel(), yy.ravel()], 1))
    sh = ((r1 - r0) / xx.shape[0], (c1 - c0) / xx.shape[1])
    d = ndimage.zoom(d.reshape(xx.shape) * km_px, sh, order=1)[:r1 - r0, :c1 - c0]
    t = ndimage.zoom((i / (len(pts) - 1)).reshape(xx.shape), sh, order=1)[:r1 - r0, :c1 - c0]
    return d, t, (slice(r0, r1), slice(c0, c1)), len(pts)


def _agirlik(z, o, km_px):
    if "bolge" in o:
        return ndimage.gaussian_filter(_cokgen(z.shape, o["bolge"]), o.get("yumusak_km", 50) / km_px)
    d, t, sl, _ = _cizgi_alan(z.shape, o["cizgi"], km_px, o["yari_km"] * 2.5)
    W = np.zeros(z.shape, np.float32)
    W[sl] = np.exp(-(d / o["yari_km"]) ** 2)
    return W


def sirt(z, kara, km_px, o, kok, kaynaklar):
    ny, nx = z.shape
    g = lambda km, k: gurultu((ny, nx), km, km_px, kok * 10 + k)
    bukme = ((g(300, 1) * 25 + g(80, 2) * 10) / km_px, (g(300, 3) * 25 + g(80, 4) * 10) / km_px)
    yari = np.max(np.atleast_1d(o["yari_km"]))
    d, t, sl, n = _cizgi_alan(z.shape, o["cizgi"], km_px, yari * 3, bukme)
    nk = len(o["cizgi"])
    H = np.interp(t, np.linspace(0, 1, (nk - 1) * 60), _boyunca(o["yukseklik"], nk))
    Y = np.interp(t, np.linspace(0, 1, (nk - 1) * 60), _boyunca(o["yari_km"], nk))
    b0, b1 = o.get("incel", [0.1, 0.3])
    uc = np.clip(t / max(b0, 1e-3), 0, 1) * np.clip((1 - t) / max(b1, 1e-3), 0, 1)
    uc = uc * uc * (3 - 2 * uc)
    Y = Y * (1 + 0.3 * np.clip(g(220, 5)[sl], -1.5, 1.5)) * (0.15 + 0.85 * uc)
    P = np.exp(-(d / np.maximum(Y, 1e-3)) ** 2)
    if o.get("doku"):
        k = dict(o["doku"]); k.setdefault("bolge", o["cizgi"])
        alan = np.zeros((ny, nx), np.float32); alan[sl] = P > 0.01
        tex, _ = ornekle(k, km_px, alan, kaynaklar, None)
        tex = tex[sl]
        rel = tex - ndimage.gaussian_filter(tex, 15 / km_px)
    else:
        n1 = g(25, 6)[sl]; n2 = g(9, 7)[sl]
        rel = (1 - np.abs(n1)) ** 2 * 0.6 + (1 - np.abs(n2)) ** 2 * 0.4 - 0.45
        rel = rel / (rel.std() + 1e-6) * 0.18 * H
    hedef = H * (0.25 + 0.75 * uc) * P + o.get("doku_kat", 1.0) * rel * np.sqrt(P)
    alt = z[sl]
    yeni = np.maximum(alt, alt * (1 - P) + hedef)
    if o.get("ust"):
        u = o["ust"] - 300
        yeni = np.where(yeni > u, u + 300 * np.tanh((yeni - u) / 300), yeni)
    z = z.copy(); z[sl] = np.where(kara[sl] & (P > 0.005), yeni, alt)
    return z


def alcalt(z, kara, km_px, o):
    W = _agirlik(z, o, km_px)
    b = o.get("taban", 100.0); kat = o.get("kat", 0.2)
    return np.where(kara & (z > b), b + (z - b) * (1 - W * (1 - kat)), z)


def kabart(z, kara, km_px, o):
    if "bolge" in o:
        A = _agirlik(z, o, km_px) * o["m"]
    else:
        d, t, sl, _ = _cizgi_alan(z.shape, o["cizgi"], km_px, o["yari_km"] * 2.5)
        nk = len(o["cizgi"])
        m = np.interp(t, np.linspace(0, 1, (nk - 1) * 60), _boyunca(o["m"], nk))
        A = np.zeros(z.shape, np.float32); A[sl] = m * np.exp(-(d / o["yari_km"]) ** 2)
    return np.where(kara, z + A, z)


def cukur_doldur(z, kara, km_px, o):
    W = _agirlik(z, dict(o, yumusak_km=o.get("yumusak_km", 40)), km_px)
    s = o.get("olcek_km", 90) / km_px
    duz = ndimage.gaussian_filter(np.where(kara, z, 0.0), s) / np.maximum(ndimage.gaussian_filter(kara.astype(float), s), 1e-3)
    taban = duz - o.get("pay", 150)
    yeni = np.where(z < taban, taban - 0.3 * np.maximum(taban - z, 0) ** 0.8, z)
    return np.where(kara, z * (1 - W) + np.maximum(yeni, z) * W, z)


def yama(z, kara, km_px, o, kaynaklar):
    W = ndimage.gaussian_filter(_cokgen(z.shape, o["bolge"]), o.get("yumusak_km", 45) / km_px) * kara
    A, _ = ornekle(o, km_px, (W > 1e-3).astype(np.float32), kaynaklar)
    dk = ndimage.distance_transform_edt(kara) * km_px
    u = np.clip(dk / 30.0, 0, 1); rampa = 0.35 + 0.65 * u * u * (3 - 2 * u)
    return np.where(kara, z * (1 - W) + np.maximum(A * rampa, 5) * W, z)


def uygula(p, kaynaklar=None):
    """cikti/karsilik_z.npy + ozellikler.json → cikti/z.npy."""
    z = np.load(p.cikti("karsilik_z.npy")).astype(np.float32)
    kara = p.kara(); kp = p.km_px; kaynaklar = {} if kaynaklar is None else kaynaklar
    for i, o in enumerate(p.json("ozellikler.json", [])):
        tur = o["tur"]
        if tur == "sirt":
            z = sirt(z, kara, kp, o, p.ayar["tohum"] * 100 + i, kaynaklar)
        elif tur == "alcalt":
            z = alcalt(z, kara, kp, o)
        elif tur == "kabart":
            z = kabart(z, kara, kp, o)
        elif tur == "cukur_doldur":
            z = cukur_doldur(z, kara, kp, o)
        elif tur == "yama":
            z = yama(z, kara, kp, o, kaynaklar)
        else:
            raise ValueError(f"bilinmeyen özellik türü: {tur}")
        log(f"özellik {i}: {tur} {o.get('ad', '')} (en yüksek {z[kara].max():.0f} m)")
    z = np.where(kara, np.maximum(z, 1.0), 0.0).astype(np.float32)
    np.save(p.cikti("z.npy"), z)
    return z
