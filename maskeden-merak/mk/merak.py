"""Merak (merakmapmaker.com) için çıktı ve Merak dışa aktarımlarıyla çalışma.

Kodlama (bir Merak 16 bit dışa aktarımından test platolarıyla ölçüldü; sürüm değişebilir, `plato` komutuyla yeniden ölç):
  S = deniz seviyesi gri değeri; kara: gri = S + (65535 − S) · sqrt(m / ZM); deniz: gri = S · (1 − (−m / DD) ^ DP)
Merak dünyası: dışa aktarım boyutu (ör. 16000 × 7719, oran 2,073). "Fill world" görüntüyü oranını koruyarak sığdırır;
dışa aktarımla aynı boyuttaki görüntü birebir oturur. Bu modülün bütün çıktıları o boyuttadır.
Dünyaya yerleşim: 2:1 eşdikdörtgen dünya (enlem 90..−90, boylam −180..180) Merak çerçevesine yükseklikten sığdırılıp ortalanır
(2:1 görüntüyle Fill world'ün yaptığı); kıta, maskenin enlem ve boylamına düz (bükmeden) konur.
"""
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage, optimize

from .ciz import deniz_profili, renklendir
from .maske import parcalar
from .proje import log

Image.MAX_IMAGE_PIXELS = None
KODLAMA = {"S": 14642.0, "ZM": 8000.0, "DD": 6840.0, "DP": 0.607, "kaynak": "2026-11 Merak 16 bit dışa aktarımı, 6 plato"}


def kodlama(p):
    k = p.json("merak_kodlama.json")
    return {**KODLAMA, **(k or {})}


def coz(g, K):
    g = np.asarray(g, np.float32); S = K["S"]
    return np.where(g > S, K["ZM"] * np.clip((g - S) / (65535 - S), 0, None) ** 2,
                    -K["DD"] * np.clip(1 - g / S, 0, None) ** (1 / K["DP"]))


def kodla(m, K):
    m = np.asarray(m, np.float32); S = K["S"]
    kara = S + 1 + (65534 - S) * np.sqrt(np.clip(m, 0, K["ZM"]) / K["ZM"])
    deniz = S * (1 - np.clip(-m / K["DD"], 0, 1) ** K["DP"])
    return np.round(np.where(m > 0, kara, np.minimum(deniz, S))).clip(0, 65535).astype(np.uint16)


def oku(yol):
    return np.asarray(Image.open(yol)).astype(np.int32)


def yaz(yol, g):
    Image.fromarray(np.asarray(g).astype(np.uint16)).save(yol)


# ------------------------------------------------------------------ kodlamayı ölç
def plato(p, disa, yukseklikler):
    """Merak dışa aktarımındaki düz test platolarından kodlamayı ölçer → merak_kodlama.json.
    yukseklikler: platolara Flatten ile verilen metreler (en az 2 kara, en az 2 deniz önerilir). Platolar açık okyanusta olmalı."""
    g = oku(disa)
    taban = np.bincount(g.ravel() // 16).argmax() * 16
    duz = np.zeros(g.shape, bool)
    duz[:-1, :-1] = (np.diff(g, axis=0)[:, :-1] == 0) & (np.diff(g, axis=1)[:-1, :] == 0)
    # kıta ve çevresi (en büyük taban dışı bileşenler) dışarıda: platolar açık okyanusta ayrık yükseltilerdir
    yapi = np.abs(g - taban) > 32
    Ly, ny_ = ndimage.label(yapi); sy_ = ndimage.sum(yapi, Ly, range(1, ny_ + 1))
    kita = np.isin(Ly, np.nonzero(sy_ > 0.2 * sy_.max())[0] + 1)
    duz &= yapi & ~kita
    L, n = ndimage.label(duz); s = ndimage.sum(duz, L, range(1, n + 1))
    adaylar = []
    for k in np.argsort(-s):
        if s[k] < 100:
            break
        v = int(np.bincount(g[L == k + 1]).argmax())
        if all(abs(v - a) > 8 for a in adaylar):
            adaylar.append(v)
    adaylar = sorted(adaylar)[:len(yukseklikler)] if len(adaylar) >= len(yukseklikler) else adaylar
    if len(adaylar) != len(yukseklikler):
        raise SystemExit(f"{len(yukseklikler)} plato bekleniyordu, {len(adaylar)} düz alan bulundu: {adaylar}")
    hm = np.array(sorted(yukseklikler), float); gv = np.array(sorted(adaylar), float)
    kara = hm > 0; deniz = hm < 0
    if kara.sum() < 2:
        raise SystemExit("en az iki kara platosu gerekli")
    A = np.c_[np.ones(kara.sum()), np.sqrt(hm[kara])]
    S, k = np.linalg.lstsq(A, gv[kara], rcond=None)[0]
    ZM = ((65535 - S) / k) ** 2
    K = {"S": float(S), "ZM": float(ZM), "DD": KODLAMA["DD"], "DP": KODLAMA["DP"]}
    if deniz.sum() >= 2:
        y = np.log(1 - gv[deniz] / S); x = np.log(-hm[deniz])
        DP, b = np.polyfit(x, y, 1); K["DD"] = float(np.exp(-b / DP)); K["DP"] = float(DP)
    K["taban_gri"] = int(taban); K["taban_m"] = float(coz(taban, K))
    K["olcum"] = [[float(a), int(b), round(float(coz(b, K)), 1)] for a, b in zip(hm, gv)]
    K["kaynak"] = os.path.basename(disa)
    json.dump(K, open(p.yol("merak_kodlama.json"), "w"), ensure_ascii=False, indent=1)
    log(f"kodlama: S {S:.0f}, beyaz {ZM:.0f} m, deniz D {K['DD']:.0f} p {K['DP']:.3f}; denetim (m, gri, geri çözüm): {K['olcum']}")
    return K


# ------------------------------------------------------------------ Merak çerçevesine yerleşim
def _cerceve(p):
    W, H = p.ayar["merak_boyut"]
    ox = (W - 2 * H) / 2.0                         # 2:1 dünyanın Merak çerçevesindeki yatay kayması
    return W, H, ox


def merak_to_maske(p, y, x):
    """Merak pikseli → maske pikseli (satır, sütun)."""
    W, H, ox = _cerceve(p)
    lat = 90 - (np.asarray(y, float) + 0.5) * 180 / H
    lon = -180 + (np.asarray(x, float) - ox + 0.5) * 360 / (2 * H)
    my = (p.ayar["ust_enlem"] - lat) / p.der_px - 0.5
    mx = (lon - p.ayar["merkez_boylam"]) / p.der_px + p.boyut[1] / 2 - 0.5
    return my, mx


def maske_to_merak(p, my, mx):
    W, H, ox = _cerceve(p)
    lat = p.ayar["ust_enlem"] - (np.asarray(my, float) + 0.5) * p.der_px
    lon = p.ayar["merkez_boylam"] + (np.asarray(mx, float) + 0.5 - p.boyut[1] / 2) * p.der_px
    return (90 - lat) * H / 180 - 0.5, (lon + 180) * 2 * H / 360 + ox - 0.5


def kita_kutusu(p, pay=300):
    ny, nx = p.boyut
    ys, xs = maske_to_merak(p, np.array([0, ny, 0, ny]), np.array([0, 0, nx, nx]))
    W, H, _ = _cerceve(p)
    return max(int(ys.min()) - pay, 0), min(int(ys.max()) + pay, H), max(int(xs.min()) - pay, 0), min(int(xs.max()) + pay, W)


def cikti(p, kaynak="z.npy", ad="merak"):
    """cikti/z.npy (ya da verilen dizi) → Merak çerçevesinde 16 bit yükseklik + siyah beyaz maske + ölçek bilgisi."""
    K = kodlama(p)
    z = np.load(p.cikti(kaynak)).astype(np.float32) if isinstance(kaynak, str) else kaynak
    kara = p.kara()
    W, H, _ = _cerceve(p)
    y0, y1, x0, x1 = kita_kutusu(p)
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    my, mx = merak_to_maske(p, yy, xx)
    icerde = (my >= 0) & (my <= kara.shape[0] - 1) & (mx >= 0) & (mx <= kara.shape[1] - 1)
    zk = ndimage.map_coordinates(z, [my, mx], order=1, cval=0)
    kk = ndimage.map_coordinates(kara.astype(np.float32), [my, mx], order=1, cval=0) > 0.5
    kk &= icerde
    L, n = ndimage.label(kk); s = ndimage.sum(kk, L, range(1, n + 1)); kk = np.isin(L, np.nonzero(s >= 30)[0] + 1)  # benek yok
    km_px_m = 40030.0 / (2 * H)                                              # Merak pikseli (ekvatorda) km
    deniz = deniz_profili(kk, km_px_m, p.ayar["deniz"])
    h = np.where(kk, np.maximum(zk, 2.0), deniz)
    g = np.full((H, W), kodla(np.array(p.ayar["deniz"]["derin_m"]), K), np.uint16)
    g[y0:y1, x0:x1] = kodla(h, K)
    yaz(p.cikti(f"{ad}_{W}.png"), g)
    mk = np.zeros((H, W), np.uint8); mk[y0:y1, x0:x1] = kk * 255
    Image.fromarray(mk).save(p.cikti(f"{ad}_maske_{W}.png"))
    on = Image.fromarray(renklendir(h, km_px_m)); on.thumbnail((2000, 2000)); on.save(p.cikti(f"{ad}_onizleme.jpg"), quality=88)
    olc = {"boyut": [W, H], "kodlama": K, "kita_kutusu": [x0, y0, x1, y1],
           "enlem": [float(p.enlem(p.boyut[0] - 1)), p.ayar["ust_enlem"]],
           "boylam": [float(p.boylam(0)), float(p.boylam(p.boyut[1] - 1))],
           "ice_aktarma": "Import image → terrain, sekme 'Heightmap / mask (auto)', düğme 'Fill world'"}
    json.dump(olc, open(p.cikti(f"{ad}_olcek.json"), "w"), ensure_ascii=False, indent=1)
    log(f"Merak çıktısı {W} × {H}: {ad}_{W}.png; kara en yüksek {h[kk].max():.0f} m")
    return g


# ------------------------------------------------------------------ sahibin dışa aktarımıyla çalışma
def kayit(a_kara, b_kara, kutu):
    """İki kara maskesi arasında b = a·(sy, sx) + (oy, ox); IoU en büyüklenir. Aynı boyutlu dosyalarda (1, 1, 0, 0) çıkmalı."""
    y0, y1, x0, x1 = kutu; f = 2
    Y, X = np.mgrid[y0:y1:f, x0:x1:f].astype(np.float32); A = a_kara[y0:y1:f, x0:x1:f]
    def m(q):
        sy, sx, oy, ox = q
        b = ndimage.map_coordinates(b_kara.astype(np.float32), [Y * sy + oy, X * sx + ox], order=1) > 0.5
        return -(A & b).sum() / max((A | b).sum(), 1)
    r = optimize.minimize(m, [1, 1, 0, 0], method="Nelder-Mead", options={"xatol": 1e-4, "fatol": 1e-6, "maxiter": 400,
                          "initial_simplex": [[1, 1, 0, 0], [1.01, 1, 0, 0], [1, 1.01, 0, 0], [1, 1, 5, 0], [1, 1, 0, 5]]})
    return r.x, -r.fun


def temizle(g, K, en_az=30, sig_m=-40.0):
    """Denizdeki küçük kara beneklerini siler, deniz seviyesine çok yakın sığlığı sig_m'ye indirir. (g, silinen parça, sığlaşan piksel)"""
    S = K["S"]; kara = g > S
    L, n = ndimage.label(kara); s = ndimage.sum(kara, L, range(1, n + 1))
    kucuk = np.isin(L, np.nonzero(s < en_az)[0] + 1)
    sinir = int(kodla(np.array(sig_m), K))
    out = g.copy(); out[kucuk] = sinir
    deniz = out <= S; say = int((deniz & (out > sinir)).sum())
    out[deniz] = np.minimum(out[deniz], sinir)
    return out, int((s < en_az).sum()), say


def kiyi_rampa(h, kara, km_px, kok=11):
    """Yalnız karada: kıyıdan içeri alçalma (kıyıda yaklaşık 20 m, 7 ile 31 km arası gürültülü genişlik), kıyıdaki kabarık şerit bastırılır."""
    rng = np.random.default_rng(kok)
    n = ndimage.gaussian_filter(rng.standard_normal(h.shape).astype(np.float32), 40); n /= n.std() + 1e-6
    dk = ndimage.distance_transform_edt(kara) * km_px
    gen = 18 * (1 + 0.6 * np.clip(n, -1.2, 1.2))
    t = np.clip(dk / gen, 0, 1); t = t * t * (3 - 2 * t)
    tavan = 3 + 25 * np.clip(dk / 4, 0, 1)
    hl = np.maximum(h * (0.12 + 0.88 * t), np.minimum(h, tavan))
    ic = ndimage.uniform_filter(np.where(kara, hl, 0), 25) / np.maximum(ndimage.uniform_filter(kara.astype(np.float32), 25), 1e-3)
    hl = np.where(t < 1, np.minimum(hl, np.maximum(ic * (0.4 + 0.6 * t) + 30, hl * t)), hl)
    return np.where(kara, np.maximum(hl, 2), h)


def birlestir(p, disa, bizim=None, tolerans_m=15.0, kiyi=False):
    """Sahibin Merak'ta elle işlediği dışa aktarım ile bizim çıktıyı birleştirir.
    Kural: kıyı çizgisi ve deniz sahibin dosyasından aynen; sahibin değiştirdiği kara (bizimkinden tolerans_m'den fazla farklı) aynen;
    bölge listesi (merak_bolgeler.json: [[[x, y], ...], ...], Merak pikseli) içindeki kara bizim yükseklikle değiştirilir.
    Çıktı: cikti/birlesik_W.png, cikti/dokunulmamis.npy (sahibin dokunmadığı kara maskesi, üslup için)."""
    K = kodlama(p); W, H, _ = _cerceve(p)
    E = oku(disa)
    if E.shape != (H, W):
        raise SystemExit(f"dışa aktarım {E.shape[::-1]}, proje merak_boyut {W} × {H}: proje.json'u düzelt")
    B = oku(bizim or p.cikti(f"merak_{W}.png"))
    y0, y1, x0, x1 = kita_kutusu(p)
    q, iou = kayit(E > K["S"], B > K["S"], (y0, y1, x0, x1))
    log(f"kayıt sahip→bizim: {np.round(q, 4).tolist()}, IoU {iou:.4f} (beklenen 1, 1, 0, 0)")
    e = coz(E[y0:y1, x0:x1], K); b = coz(B[y0:y1, x0:x1], K); kara = e > 0
    dok = kara & (np.abs(e - b) > tolerans_m)
    dok = ndimage.binary_closing(ndimage.binary_opening(dok, iterations=2), iterations=4)
    dokunulmamis = kara & ~dok
    out = E.copy()
    bolgeler = p.json("merak_bolgeler.json", [])
    if bolgeler:
        from matplotlib.path import Path
        yy, xx = np.mgrid[y0:y1, x0:x1]
        ic = np.zeros(kara.shape, bool)
        for c in bolgeler:
            ic |= Path(c).contains_points(np.c_[xx.ravel(), yy.ravel()]).reshape(kara.shape)
        w = np.clip(ndimage.distance_transform_edt(ic) / 30, 0, 1)
        yeni = np.where(kara, w * np.maximum(b, 2) + (1 - w) * e, e)
        e = yeni
    if kiyi:
        e = kiyi_rampa(e, kara, 40030.0 / (2 * H))
    blok = out[y0:y1, x0:x1]; blok[kara] = kodla(np.maximum(e[kara], 0.5), K); out[y0:y1, x0:x1] = blok
    out, nb, ns = temizle(out, K)
    yaz(p.cikti(f"birlesik_{W}.png"), out)
    np.save(p.cikti("dokunulmamis.npy"), dokunulmamis)
    log(f"birleşim: sahibin değiştirdiği kara payı {dok.sum() / max(kara.sum(), 1):.3f}; silinen benek {nb}, sığlaşan deniz {ns}")
    return out


def uslup(p, girdi=None, sig=6, yama=128, kok=23):
    """Sahibin dokunmadığı karayı sahibin üslubuna yaklaştırır (genel hat korunur, ince doku sahibin işlediği yerden yamalarla).
    Eğitim: sahibin değiştirdiği kara (en az birkaç bin km²). Çıktı: cikti/uslup_W.png. Kıyı ve deniz değişmez."""
    K = kodlama(p); W, H, _ = _cerceve(p)
    g = oku(girdi or p.cikti(f"birlesik_{W}.png"))
    y0, y1, x0, x1 = kita_kutusu(p)
    A = coz(g[y0:y1, x0:x1], K); kara = A > 0
    dokun = np.load(p.cikti("dokunulmamis.npy")) & kara
    kd = ndimage.distance_transform_edt(kara)
    kaynak = kara & ~dokun & (kd > 25)
    if kaynak.sum() < yama * yama * 2:
        raise SystemExit("sahibin elle işlediği alan doku örneği için az")
    def suz(z, s):
        return ndimage.gaussian_filter(np.where(kara, z, 0), s) / np.maximum(ndimage.gaussian_filter(kara.astype(np.float32), s), 1e-3)
    gA = suz(A, sig); hp = A - gA
    kut = [0, 300, 700, 1200, 2000, 3000, 9000]; xo, so = [], []
    for lo, hi in zip(kut[:-1], kut[1:]):
        m = kaynak & (gA >= lo) & (gA < hi)
        if m.sum() > 500:
            xo.append(float(np.median(gA[m]))); so.append(float(hp[m].std()))
    xo, so = np.array(xo), np.array(so)
    t = np.clip(hp / np.interp(gA, xo, so), -4, 4)
    kk = ndimage.uniform_filter(kaynak.astype(np.float32), yama) > 0.97
    ys, xs = np.nonzero(kk[yama // 2:-yama // 2:8, yama // 2:-yama // 2:8]); ys = ys * 8; xs = xs * 8
    rng = np.random.default_rng(kok); adim = yama // 2
    han = np.hanning(yama + 1)[:-1]; pen = np.outer(han, han)
    hh, ww = A.shape
    doku = np.zeros((hh + 2 * yama, ww + 2 * yama), np.float32); top = np.zeros_like(doku)
    for y in range(-adim, hh, adim):
        for x in range(-adim, ww, adim):
            k = rng.integers(len(ys)); q = np.rot90(t[ys[k]:ys[k] + yama, xs[k]:xs[k] + yama], rng.integers(4))
            if rng.random() < 0.5:
                q = q[:, ::-1]
            doku[y + adim:y + adim + yama, x + adim:x + adim + yama] += q * pen; top[y + adim:y + adim + yama, x + adim:x + adim + yama] += pen
    doku = (doku / np.maximum(top, 1e-3))[adim:adim + hh, adim:adim + ww]; doku /= doku[kara].std() + 1e-6
    g6, g2 = suz(A, sig), suz(A, 2)
    sd = np.sqrt(np.maximum(suz(A ** 2, 20) - suz(A, 20) ** 2, 0)); k = np.clip((sd - 80) / 250, 0, 1)
    taban = (1 - k) * g6 + k * g2
    bant = taban - suz(taban, 20); taban = taban + np.where(bant > 0, 0.25 * bant, 0.05 * bant)
    yeni = taban + doku * np.interp(taban, xo, so) * (1 - 0.6 * k)
    yeni = np.where(kd < 4, np.minimum(yeni, A + 20), yeni)
    Wd = np.where(dokun, np.clip(ndimage.distance_transform_edt(~(kara & ~dokun)) / 30, 0, 1), 0)
    R = np.where(kara, Wd * np.maximum(yeni, 2) + (1 - Wd) * A, A)
    out = g.copy(); blok = out[y0:y1, x0:x1]; blok[kara] = kodla(np.maximum(R[kara], 0.5), K); out[y0:y1, x0:x1] = blok
    yaz(p.cikti(f"uslup_{W}.png"), out)
    log(f"üslup: doku genliği {dict(zip(np.round(xo).astype(int).tolist(), np.round(so).astype(int).tolist()))}; kıyı farkı {int(((out > K['S']) != (g > K['S'])).sum())}")
    return out


def rehber(p, girdi=None, seviyeler=(100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000)):
    """Elle işleme rehberi: Merak çerçevesinde saydam katman (eş yükseklik eğrileri, nokta yükseklikleri, adlar). cikti/rehber_W.png"""
    from PIL import ImageDraw, ImageFont
    K = kodlama(p); W, H, _ = _cerceve(p)
    g = oku(girdi or p.cikti(f"merak_{W}.png"))
    y0, y1, x0, x1 = kita_kutusu(p)
    Z = coz(g[y0:y1, x0:x1], K); kara = Z > 0
    f = max(1, W // 8000)
    Zs = ndimage.gaussian_filter(np.where(kara, Z, 0), 1.2 * f)
    sv = np.digitize(Zs, seviyeler)
    renk = [(120, 200, 120), (180, 220, 100), (240, 230, 90), (245, 190, 70), (240, 140, 50), (225, 80, 60), (200, 60, 150), (150, 80, 220), (255, 255, 255)]
    kat = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    for ax in (0, 1):
        fark = sv != np.roll(sv, 1, ax); ust = np.maximum(sv, np.roll(sv, 1, ax))
        for i in range(len(seviyeler)):
            m = fark & kara & (ust == i + 1)
            m = ndimage.binary_dilation(m, iterations=f - 1) if f > 1 else m
            kat[m, :3] = renk[i % len(renk)]; kat[m, 3] = 255
    im = Image.fromarray(kat, "RGBA"); d = ImageDraw.Draw(im)
    yazi = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    fk = ImageFont.truetype(yazi, 9 * f); fa = ImageFont.truetype(yazi, 13 * f)
    Zt = ndimage.gaussian_filter(np.where(kara, Z, 0), 2 * f)
    tepe = (Zt == ndimage.maximum_filter(Zt, 45 * f)) & kara & (Zt > 700)
    ys, xs = np.nonzero(tepe)
    for k in np.argsort(-Zt[ys, xs])[:80]:
        x, y = xs[k], ys[k]
        d.ellipse([x - 2 * f, y - 2 * f, x + 2 * f, y + 2 * f], fill=(255, 0, 0, 255))
        d.text((x + 3 * f, y - 5 * f), str(int(round(Z[y, x], -1))), font=fk, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    for e in p.json("etiketler.json", []):
        my, mx = maske_to_merak(p, e["y"], e["x"])
        d.text((mx - x0, my - y0), e["ad"], font=fa, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255), anchor="mm")
    tam = Image.new("RGBA", (W, H), (0, 0, 0, 0)); tam.paste(im, (x0, y0))
    tam.save(p.cikti(f"rehber_{W}.png"))
    log(f"rehber: {p.cikti(f'rehber_{W}.png')}")


def fark(p, disa, bizim=None):
    """Sahibin dışa aktarımı ile bizim çıktı arasındaki fark haritası (kırmızı: sahibinki yüksek, mavi: bizimki) ve parça özetleri."""
    K = kodlama(p); W, H, _ = _cerceve(p)
    E = oku(disa); B = oku(bizim or p.cikti(f"merak_{W}.png"))
    y0, y1, x0, x1 = kita_kutusu(p)
    e = coz(E[y0:y1, x0:x1], K); b = coz(B[y0:y1, x0:x1], K); kara = e > 0
    d = np.clip((e - b) / 1000, -1, 1)
    rgb = np.zeros(d.shape + (3,)); rgb[..., 0] = np.where(d > 0, 1, 1 + d); rgb[..., 1] = 1 - np.abs(d); rgb[..., 2] = np.where(d < 0, 1, 1 - d)
    rgb[~kara] = 0.15
    im = Image.fromarray((rgb * 255).astype(np.uint8)); im.save(p.cikti("fark.png"))
    lab, adlar = parcalar(p)
    yy, xx = np.mgrid[y0:y1, x0:x1]; my, mx = merak_to_maske(p, yy, xx)
    L = ndimage.map_coordinates(lab.astype(np.float32), [my, mx], order=0, cval=0).astype(int)
    for i, ad in enumerate(adlar, 1):
        m = kara & (L == i)
        if m.sum() > 100:
            print(f"parça {ad}: sahip %50/%90/en yüksek {np.percentile(e[m], [50, 90]).round().astype(int).tolist()} {e[m].max():.0f}; "
                  f"bizim {np.percentile(b[m], [50, 90]).round().astype(int).tolist()} {b[m].max():.0f}; 200 m'den çok sapan pay {(np.abs(e[m] - b[m]) > 200).mean():.2f}")
