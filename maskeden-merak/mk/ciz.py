"""Gölgeli, renkli topografya görüntüsü ve etiketler.

etiketler.json: [{"ad": "MOR SIRADAĞLARI", "x": 1200, "y": 640, "boyut": 18}, ...] (maske pikseli; boyut tam görüntüde punto).
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

from .proje import log

YAZI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
KARA_RENK = ([0, 200, 600, 1200, 2000, 3000, 4500, 6500],
             [(86, 140, 76), (132, 168, 92), (196, 190, 120), (196, 156, 100), (160, 120, 86), (140, 120, 110), (200, 196, 190), (250, 250, 250)])
DENIZ_RENK = ([-6000, -3000, -1000, -200, 0], [(14, 32, 70), (24, 56, 110), (44, 90, 150), (90, 150, 200), (140, 190, 220)])


def _tablo(z, esik, renk):
    r = np.array(renk, float)
    return np.stack([np.interp(z, esik, r[:, i]) for i in range(3)], -1)


def golge(z, km_px):
    gy, gx = np.gradient(ndimage.gaussian_filter(z, 0.6), km_px * 1000)
    a, e = np.radians(315), np.radians(40)
    lx, ly, lz = np.sin(a) * np.cos(e), np.cos(a) * np.cos(e), np.sin(e)
    nx_, ny_ = -gx * 3, gy * 3
    return np.clip(0.45 + 0.7 * (nx_ * lx + ny_ * ly + lz) / np.sqrt(nx_ ** 2 + ny_ ** 2 + 1), 0.25, 1.1)


def renklendir(z, km_px):
    g = golge(np.where(z > 0, z, 0), km_px)
    rgb = np.where((z > 0)[..., None], _tablo(z, *KARA_RENK) * g[..., None], _tablo(z, *DENIZ_RENK))
    return np.clip(rgb, 0, 255).astype(np.uint8)


def deniz_profili(kara, km_px, d_ayar):
    """Kıyıdan uzaklığa bağlı basit deniz tabanı (görüntü ve Merak için yer tutucu; derinliği sahip Merak'ta ayarlar)."""
    d = ndimage.distance_transform_edt(~kara) * km_px
    t = np.clip(d / d_ayar["egim_km"], 0, 1); t = t * t * (3 - 2 * t)
    return np.minimum(d_ayar["kiyi_m"] + (d_ayar["derin_m"] - d_ayar["kiyi_m"]) * t, d_ayar["en_sig_m"])


def ciz(p):
    z = np.load(p.cikti("z.npy")).astype(np.float32)
    kara = p.kara(); kp = p.km_px
    tam = np.where(kara, z, deniz_profili(kara, kp, p.ayar["deniz"]))
    rgb = renklendir(tam, kp)
    kenar = kara ^ ndimage.binary_erosion(kara); rgb[kenar] = (40, 40, 40)
    im = Image.fromarray(rgb); im.save(p.cikti("topografya.png"))
    d = ImageDraw.Draw(im); s = im.size[0] / 2000
    f = lambda n: ImageFont.truetype(YAZI, max(8, int(n * s)))
    for la in range(-90, 91, 5):
        y = (p.ayar["ust_enlem"] - la) / p.der_px
        if 0 < y < im.size[1]:
            for x in range(0, im.size[0], int(24 * s)):
                d.line([(x, y), (x + 10 * s, y)], fill=(255, 255, 255), width=max(1, int(s)))
            d.text((6 * s, y + 2 * s), f"{abs(la)}°{'K' if la >= 0 else 'G'}", fill=(255, 255, 255), font=f(13))
    for e in p.json("etiketler.json", []):
        d.text((e["x"], e["y"]), e["ad"], font=f(e.get("boyut", 16)), fill=(255, 255, 255), anchor="mm",
               stroke_width=max(1, int(2 * s)), stroke_fill=(0, 0, 0))
    km = 1000 / kp
    d.rectangle([20 * s, im.size[1] - 40 * s, 20 * s + km, im.size[1] - 32 * s], fill=(255, 255, 255))
    d.text((24 * s + km, im.size[1] - 46 * s), "1000 km", font=f(14), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(p.cikti("topografya_etiketli.png"))
    log(f"çizim: kara en yüksek {z[kara].max():.0f} m; %10/%50/%90 {np.percentile(z[kara], [10, 50, 90]).round().astype(int).tolist()}")


def olcum(p):
    """Parça başına yükseklik özeti ve etiketlerin çevresindeki en yüksek nokta (cikti/olcum.txt)."""
    from .maske import parcalar
    z = np.load(p.cikti("z.npy")); kara = p.kara(); lab, adlar = parcalar(p)
    satir = []
    for i, ad in enumerate(adlar, 1):
        m = kara & (lab == i)
        if m.any():
            q = np.percentile(z[m], [10, 50, 90]).round().astype(int).tolist()
            satir.append(f"parça {ad}: %10/%50/%90 {q}, en yüksek {z[m].max():.0f} m")
    zs = ndimage.maximum_filter(z, int(60 / p.km_px))
    for e in p.json("etiketler.json", []):
        x, y = int(e["x"]), int(e["y"])
        if 0 <= y < z.shape[0] and 0 <= x < z.shape[1]:
            satir.append(f"{e['ad']}: 60 km içinde en yüksek {zs[y, x]:.0f} m")
    open(p.cikti("olcum.txt"), "w", encoding="utf-8").write("\n".join(satir) + "\n")
    print("\n".join(satir))
