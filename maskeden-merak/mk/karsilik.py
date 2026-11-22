"""Gerçek dünya karşılıklarıyla topografya.

karsiliklar.json: liste; her öğe bir bölgeye bir gerçek yerin yükseklik modelini döndürüp ölçekleyip bükerek yerleştirir.
  ad            : benzersiz ad
  kutu          : [boylam0, boylam1, enlem0, enlem1] kaynak kutusu (karo indirilecek alan)
  parca         : bu karşılığın uygulanabileceği parça adları (parcalar.json), ör. ["1", "2"]
  bolge         : hedef çokgen (maske pikseli); karşılık bu çokgen ∩ izinli parçalarda etkilidir
  nokta         : denetim noktaları [[x, y, boylam, enlem], ...]; en az 2. Hedef pikselin kaynakta nereye düştüğü.
                  Benzerlik dönüşümü (döndürme + ölçek) bu noktalardan en küçük karelerle bulunur, sonra ince levha eğrisiyle bükülür.
  ayna          : true ise doğu batı aynalanır (doğrudan kopya olmasın)
  carpan        : yükseklik çarpanı (varsayılan 1)
  yukseklik_egri: [[kaynak_m, hedef_m], ...] parçalı doğrusal yeniden eşleme (ör. Himalaya'yı Kafkas ölçeğine indirmek)
  oncelik       : ağırlık çarpanı (üstte kalması gereken karşılık için 2 ile 3)
  yumusak_km    : bölge kenarının yumuşaklığı (varsayılan 80)
  bukme_kat     : genel alan bükmesinin bu karşılıktaki katı (varsayılan 1)
  z             : karo zoom düzeyi (varsayılan 6; dar sıralar için 7)
  kes           : kaynakta istenmeyen kısımlar [[[boylam, enlem], ...], ...]; deniz sayılır ve ayna dolgusuyla dolar
  capa_bolge    : bükmenin yerel kalması için çapa çokgeni (varsayılan bolge)
Kaynaktaki deniz, aynalanmış komşu karayla doldurulur; hedefin kıyısı her zaman maskedir.
"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.interpolate import RBFInterpolator

from . import dem
from .maske import parcalar
from .proje import log


def benzerlik(k, km_px):
    """Hedef piksel (x, y) → kaynak (boylam, enlem) benzerlik dönüşümü ve (açı°, ölçek)."""
    n = np.array(k["nokta"], float)
    lo0, la0 = n[:, 2].mean(), n[:, 3].mean(); tx, ty = n[:, 0].mean(), n[:, 1].mean()
    ayna = k.get("ayna", False)
    X = (n[:, 2] - lo0) * 111.32 * np.cos(np.radians(la0)) * (-1 if ayna else 1); Y = (n[:, 3] - la0) * 110.6
    u = (n[:, 0] - tx) * km_px; v = -(n[:, 1] - ty) * km_px
    zs = X + 1j * Y; zt = u + 1j * v
    c = (np.conj(zs) @ zt) / (np.conj(zs) @ zs) if len(n) > 1 else 1.0 + 0j
    aci, olc = np.degrees(np.angle(c)), abs(c)
    r = np.radians(aci); cl = np.cos(np.radians(la0))

    def f(xy):
        u = (xy[:, 0] - tx) * km_px / olc; v = -(xy[:, 1] - ty) * km_px / olc
        X = u * np.cos(-r) - v * np.sin(-r); Y = u * np.sin(-r) + v * np.cos(-r)
        if ayna:
            X = -X
        return np.stack([lo0 + X / (111.32 * cl), la0 + Y / 110.6], 1)
    return f, (aci, olc)


def _kure_x(k, xy):
    """Küresel proje (proje.json "kure": true): maske pikseli her yerde aynı derece olduğu için doğu batı yönünde gerçek uzaklık
    cos(enlem) ile kısalır. Hedef x, karşılığın orta noktası çevresinde cos(enlem) ile sıkıştırılır ki kaynak gerçek km ölçeğinde
    otursun (yerel sinüzoidal izdüşüm)."""
    ust, dp = k["_kure"]
    xy = np.asarray(xy, float)
    tx = float(np.mean([q[0] for q in k["nokta"]]))
    c = np.cos(np.radians(np.clip(ust - (xy[:, 1] + 0.5) * dp, -89.0, 89.0)))
    return np.stack([tx + (xy[:, 0] - tx) * c, xy[:, 1]], 1)


def esleme(k, km_px):
    """Hedef piksel → kaynak (boylam, enlem): benzerlik + denetim noktalarında ince levha bükmesi; çevreye çapa noktaları."""
    if "_kure" in k:
        n = np.array(k["nokta"], float).reshape(-1, 4)
        kk = {key: v for key, v in k.items() if key != "_kure"}
        kk["nokta"] = np.hstack([_kure_x(k, n[:, :2]), n[:, 2:]]).tolist()
        for a in ("bolge", "capa_bolge"):
            if a in k:
                kk[a] = _kure_x(k, np.array(k[a], float)).tolist()
        ic = esleme(kk, km_px)
        return lambda xy: ic(_kure_x(k, xy))
    f, _ = benzerlik(k, km_px)
    cb = k.get("capa_bolge", k["bolge"])
    xs = [q[0] for q in cb]; ys = [q[1] for q in cb]
    pay = 400 * 4.0 / km_px
    x0, x1, y0, y1 = min(xs) - pay, max(xs) + pay, min(ys) - pay, max(ys) + pay
    capa = np.array([(x, y) for x in np.linspace(x0, x1, 5) for y in np.linspace(y0, y1, 5) if x in (x0, x1) or y in (y0, y1)], float)
    n = np.array(k["nokta"], float).reshape(-1, 4)
    hed = np.vstack([capa, n[:, :2]]); kay = np.vstack([f(capa), n[:, 2:]])
    return RBFInterpolator(hed, kay, kernel="thin_plate_spline", degree=1)


def agirlik(k, lab, adlar, km_px):
    ny, nx = lab.shape
    im = Image.new("L", (nx, ny), 0)
    ImageDraw.Draw(im).polygon([tuple(q) for q in k["bolge"]], fill=255)
    pol = np.asarray(im) > 0
    izin = np.isin(lab, [adlar.index(str(a)) + 1 for a in k.get("parca", adlar)])
    sig = k.get("yumusak_km", 80) / km_px
    w = ndimage.gaussian_filter((pol & izin).astype(np.float32), sig)
    izin_g = ndimage.binary_dilation(izin, iterations=max(1, int(2 * sig)), mask=lab > 0)   # boğaz ötesine taşma yok
    return w * ndimage.gaussian_filter(izin_g.astype(np.float32), 2.0)


def kaynak_yukle(k, kaynaklar):
    if k["ad"] not in kaynaklar:
        kaynaklar[k["ad"]] = dem.Kaynak(*k["kutu"], z=k.get("z", 6)).doldur(kutu=k["kutu"], kes=k.get("kes"))
    return kaynaklar[k["ad"]]


def ornekle(k, km_px, w, kaynaklar, bukme=None):
    """w > 0 olan hücrelerde kaynak yüksekliği (m); (yükseklik, kaynakta deniz payı)."""
    ileri = esleme(k, km_px)
    K = kaynak_yukle(k, kaynaklar)
    ny, nx = w.shape
    out = np.zeros((ny, nx), np.float32); deniz = np.zeros((ny, nx), np.float32)
    ii, jj = np.nonzero(w > 1e-3)
    lo0, lo1, la0, la1 = k["kutu"]; disari = 0; aralik = [np.inf, -np.inf, np.inf, -np.inf]
    for a in range(0, len(ii), 400000):
        i, j = ii[a:a + 400000], jj[a:a + 400000]
        x, y = j.astype(float), i.astype(float)
        if bukme is not None:
            kb = k.get("bukme_kat", 1.0)
            x = x + kb * bukme[0][i, j]; y = y + kb * bukme[1][i, j]
        ll = ileri(np.stack([x, y], 1))
        agir = w[i, j] > 0.2
        disari += int((agir & ((ll[:, 0] < lo0) | (ll[:, 0] > lo1) | (ll[:, 1] < la0) | (ll[:, 1] > la1))).sum())
        if agir.any():
            aralik = [min(aralik[0], ll[agir, 0].min()), max(aralik[1], ll[agir, 0].max()), min(aralik[2], ll[agir, 1].min()), max(aralik[3], ll[agir, 1].max())]
        h = K.ornek(ll[:, 0], ll[:, 1]) * k.get("carpan", 1.0)
        if k.get("yukseklik_egri"):
            e = np.array(k["yukseklik_egri"], float); h = np.interp(h, e[:, 0], e[:, 1])
        out[i, j] = h
        deniz[i, j] = K.deniz_ornek(ll[:, 0], ll[:, 1])
    n = int((w > 0.2).sum())
    dp = float((deniz[w > 0.2] > 0.5).mean()) if n else 0.0
    if dp > 0.1:
        log(f"UYARI {k['ad']}: ağırlıklı alanın %{100 * dp:.0f}'i kaynakta denize düşüyor; orası aynalanmış karayla dolar ve düz, "
            f"yapay görünür. Noktaları kaynaktaki kara üstüne kaydır ya da ölçeği küçült.")
    if n and disari / n > 0.02:
        log(f"UYARI {k['ad']}: ağırlıklı alanın %{100 * disari / n:.0f}'i kaynak kutusunun dışına düşüyor (aynalanmış kenar, düz dikişler). "
            f"Kullanılan aralık boylam {aralik[0]:.1f}..{aralik[1]:.1f}, enlem {aralik[2]:.1f}..{aralik[3]:.1f}: kutuyu genişlet ya da noktaları sıklaştır.")
    return out, deniz


def gurultu(shape, km, km_px, kok):
    ny, nx = shape
    g = ndimage.gaussian_filter(np.random.default_rng(kok).standard_normal((ny // 4 + 1, nx // 4 + 1)), km / km_px / 4, mode="wrap")
    return ndimage.zoom(g / (g.std() + 1e-9), (ny / g.shape[0], nx / g.shape[1]), order=1)[:ny, :nx]


class Bant:
    """Çok bantlı karışım (proje.json "bant": {"km": [12, 45, 180], "us": [6, 3, 1.5, 1]}).

    Her karşılık yalnız karada normalleştirilmiş Gauss süzgeçleriyle bantlara ayrılır: ince doku (< 12 km), orta (12 ile 45 km),
    kaba (45 ile 180 km), taban (> 180 km). Her bandın ağırlığı w^us: ince dokuda üs büyük, sınırda bir karşılığın dokusu baskın
    olur (iki doku üst üste binip bulanmaz); tabanda üs küçük, yükseklik geniş ve yumuşak geçer. Doku bantlarında karışımın
    genliği korunur (ilintisiz iki dokunun ortalaması sönükleşmesin). Karşılıktaki "bant": [i, o, k, t] bant başına çarpandır;
    ör. [1, 1, 0, 0] karşılığı yalnız doku veren bir katman yapar (başka bir karşılığın üstüne doku karıştırmak için)."""

    def __init__(self, ayar, shape, kp):
        self.km = ayar.get("km", [12.0, 45.0, 180.0]); self.us = ayar.get("us", [6.0, 3.0, 1.5, 1.0])
        self.kp = kp; n = len(self.km) + 1
        self.acc = [np.zeros(shape, np.float32) for _ in range(n)]
        self.wacc = [np.zeros(shape, np.float32) for _ in range(n)]
        self.wsq = [np.zeros(shape, np.float32) for _ in range(n)]

    def ekle(self, k, w, z):
        m = (w > 1e-3).astype(np.float32)
        if not m.any():
            return
        g = [z]
        for s in self.km:
            g.append(ndimage.gaussian_filter(z * m, s / self.kp) / np.maximum(ndimage.gaussian_filter(m, s / self.kp), 1e-4))
        bantlar = [g[i] - g[i + 1] for i in range(len(self.km))] + [g[-1]]
        carp = k.get("bant", [1.0] * len(bantlar))
        for i, b in enumerate(bantlar):
            if carp[i] <= 0:
                continue
            wi = (np.clip(w, 0, None) ** self.us[i]) * carp[i] * m
            self.acc[i] += wi * b; self.wacc[i] += wi; self.wsq[i] += wi * wi

    def sonuc(self):
        z = self.acc[-1] / np.maximum(self.wacc[-1], 1e-12)
        for i in range(len(self.acc) - 1):
            ort = self.acc[i] / np.maximum(self.wacc[i], 1e-12)
            gen = np.clip(self.wacc[i] / np.sqrt(np.maximum(self.wsq[i], 1e-24)), 1.0, 1.6)   # genlik düzeltmesi
            z += np.where(self.wacc[i] > 0, ort * gen, 0)
        return z.astype(np.float32)


def bilesik(p, kaynaklar=None):
    """Bütün karşılıkların ağırlıklı birleşimi, tam maske çözünürlüğünde. cikti/karsilik_z.npy."""
    kara = p.kara(); ny, nx = kara.shape; kp = p.km_px
    lab, adlar = parcalar(p)
    liste = p.json("karsiliklar.json", [])
    if p.ayar.get("kure"):
        liste = [dict(k, _kure=[p.ayar["ust_enlem"], p.der_px]) for k in liste]
    if not liste:
        raise SystemExit("karsiliklar.json boş")
    kaynaklar = {} if kaynaklar is None else kaynaklar
    t = p.ayar["tohum"]
    g = lambda km, k: gurultu((ny, nx), km, kp, t * 100 + k)
    bukme = ((g(500, 1) * 32 + g(150, 2) * 12) / kp, (g(500, 3) * 32 + g(150, 4) * 12) / kp)    # yaklaşık 40 km: kopya olmasın
    II, JJ = np.indices((ny, nx), dtype=np.float32)
    kd = ((g(350, 5) * 88 + g(90, 6) * 28) / kp, (g(350, 7) * 88 + g(90, 8) * 28) / kp)       # sınırlar ±70 km kıvrılır
    toplam = np.zeros((ny, nx), np.float32); wtop = np.zeros((ny, nx), np.float32); genis = []
    bant = Bant(p.ayar["bant"], (ny, nx), kp) if p.ayar.get("bant") else None
    for k in liste:
        w = agirlik(k, lab, adlar, kp)
        w = ndimage.map_coordinates(w, [II + kd[1], JJ + kd[0]], order=1, mode="nearest").astype(np.float32) * kara * k.get("oncelik", 1.0)
        z, _ = ornekle(k, kp, w, kaynaklar, bukme)
        if bant:
            bant.ekle(k, w, z)
        else:
            toplam += w * z
        wtop += w; genis.append((k, w))
        log(f"karşılık {k['ad']}: en yüksek {z[w > 1e-3].max() if (w > 1e-3).any() else 0:.0f} m")
    bos = kara & (wtop < 0.05)
    if bos.any():
        log(f"karşılıksız kara {bos.sum()} piksel: en yakın karşılıklarla dolduruluyor")
        for k, w in genis:
            if k.get("bant") and k["bant"][-1] <= 0:      # yalnız doku veren karşılık boşluk doldurmaz
                continue
            wb = ndimage.gaussian_filter(w, 160 / kp) * bos
            z, _ = ornekle(k, kp, wb, kaynaklar, bukme)
            if bant:
                bant.ekle(k, wb, z)
            else:
                toplam += wb * z
            wtop += wb
    z = bant.sonuc() if bant else toplam / np.maximum(wtop, 1e-6)
    dk = ndimage.distance_transform_edt(kara) * kp
    u = np.clip(dk / p.ayar["kiyi_rampa_km"], 0, 1)
    z = np.where(kara, np.maximum(z * (0.3 + 0.7 * u * u * (3 - 2 * u)), 1.0), 0.0).astype(np.float32)
    np.save(p.cikti("karsilik_z.npy"), z)
    log(f"birleşim: en yüksek {z.max():.0f} m, kara ortancası {np.median(z[kara]):.0f} m")
    return z


def onizle(p, secili=None):
    """Her karşılığı tek başına, bölgesinin çevresinde gösterir (cikti/oniz_AD.png): sarı çokgen, camgöbeği denetim noktaları."""
    from .ciz import renklendir
    kara = p.kara(); kp = p.km_px
    s = min(1.0, 1600 / max(kara.shape))
    ny, nx = int(kara.shape[0] * s), int(kara.shape[1] * s)
    kara_k = np.asarray(Image.fromarray(kara.astype(np.uint8) * 255).resize((nx, ny), Image.BOX)) > 127
    kaynaklar = {}
    for k in p.json("karsiliklar.json", []):
        if secili and k["ad"] not in secili:
            continue
        if p.ayar.get("kure"):
            k = dict(k, _kure=[p.ayar["ust_enlem"], p.der_px / s])
        ks = dict(k, bolge=[[x * s, y * s] for x, y in k["bolge"]], nokta=[[a * s, b * s, c, d] for a, b, c, d in k["nokta"]])
        if "capa_bolge" in k:
            ks["capa_bolge"] = [[x * s, y * s] for x, y in k["capa_bolge"]]
        im = Image.new("L", (nx, ny), 0); ImageDraw.Draw(im).polygon([tuple(q) for q in ks["bolge"]], fill=255)
        alan = ndimage.binary_dilation(np.asarray(im) > 0, iterations=int(240 / (kp / s)))
        z, deniz = ornekle(ks, kp / s, alan.astype(np.float32), kaynaklar)
        rgb = renklendir(np.where(deniz > 0.5, -200, z), kp / s)
        rgb[~alan] = 30
        kenar = kara_k ^ ndimage.binary_erosion(kara_k); rgb[kenar] = [255, 40, 40]
        img = Image.fromarray(rgb); d = ImageDraw.Draw(img)
        d.line([tuple(q) for q in ks["bolge"] + ks["bolge"][:1]], fill=(255, 255, 0), width=1)
        for a, b, _, _ in ks["nokta"]:
            d.ellipse([a - 4, b - 4, a + 4, b + 4], outline=(0, 255, 255), width=2)
        xs = [q[0] for q in ks["bolge"]]; ys = [q[1] for q in ks["bolge"]]
        img.crop((max(0, min(xs) - 80), max(0, min(ys) - 80), min(nx, max(xs) + 80), min(ny, max(ys) + 80))).save(p.cikti(f"oniz_{k['ad']}.png"))
        log(f"önizleme {k['ad']}")
