"""Maskenin temizlenmesi ve parçalara ayrılması.

parcalar.json:
  {"cizgiler": [[[x, y], [x, y], ...], ...],     # parçaları ayıran kesme çizgileri (maske pikseli)
   "tohumlar": {"1": [x, y], "2": [x, y], ...}}  # her parçanın içinde bir nokta; ad = parça adı
Kesme çizgileriyle bölünen kara bileşenleri tohumlarına göre adlandırılır; tohumsuz bileşenler (adalar) en yakın parçaya katılır.
"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from .proje import log


def temizle(p, en_az_px=6):
    """Eşikle, en_az_px'ten küçük kara ve deniz parçalarını sil, cikti/maske_temiz.png yaz. Kenar yumuşatma kalmaz."""
    a = np.asarray(Image.open(p.yol(p.ayar["maske"])).convert("L")) > 127
    L, n = ndimage.label(a); s = ndimage.sum(a, L, range(1, n + 1)); a = np.isin(L, np.nonzero(s >= en_az_px)[0] + 1)
    L, n = ndimage.label(~a); s = ndimage.sum(~a, L, range(1, n + 1)); a = ~np.isin(L, np.nonzero(s >= en_az_px)[0] + 1)
    Image.fromarray((a * 255).astype(np.uint8)).save(p.cikti("maske_temiz.png"))
    p._kara = a
    log(f"maske {a.shape[1]} × {a.shape[0]}, kara payı {a.mean():.3f}, km/piksel {p.km_px:.3f}")
    return a


def parcalar(p, boyut=None):
    """(etiket dizisi int16, adlar listesi). Etiket 0 deniz, k parça adlar[k-1]. boyut=(ny, nx) verilirse en yakın komşuyla ölçeklenir."""
    tanim = p.json("parcalar.json")
    kara = p.kara()
    ny, nx = kara.shape
    if not tanim:
        lab = kara.astype(np.int16); adlar = ["1"]
    else:
        im = Image.fromarray(kara.astype(np.uint8) * 255)
        d = ImageDraw.Draw(im)
        for c in tanim.get("cizgiler", []):
            d.line([tuple(q) for q in c], fill=0, width=3)
        k = np.asarray(im) > 0
        L, n = ndimage.label(k)
        adlar = list(tanim["tohumlar"].keys())
        lab = np.zeros((ny, nx), np.int16)
        for i, ad in enumerate(adlar, 1):
            x, y = tanim["tohumlar"][ad]
            b = L[int(y), int(x)]
            if b == 0:
                raise ValueError(f"tohum {ad} ({x}, {y}) karada değil ya da kesme çizgisinin üstünde")
            lab[L == b] = i
        bos = kara & (lab == 0)
        if bos.any():
            _, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
            lab = np.where(bos, lab[iy, ix], lab)
    if boyut is not None and tuple(boyut) != (ny, nx):
        lab = np.asarray(Image.fromarray(lab.astype(np.uint8)).resize((boyut[1], boyut[0]), Image.NEAREST)).astype(np.int16)
    return lab, adlar


def parca_resmi(p):
    """Parçaları renkli gösteren denetim görüntüsü (cikti/parcalar.png)."""
    lab, adlar = parcalar(p)
    rng = np.random.default_rng(3)
    pal = np.vstack([[20, 30, 60], rng.integers(70, 255, (len(adlar), 3))]).astype(np.uint8)
    im = Image.fromarray(pal[lab]); d = ImageDraw.Draw(im)
    tanim = p.json("parcalar.json") or {}
    for ad, (x, y) in tanim.get("tohumlar", {}).items():
        d.text((x, y), ad, fill=(0, 0, 0), stroke_width=3, stroke_fill=(255, 255, 255))
    for c in tanim.get("cizgiler", []):
        d.line([tuple(q) for q in c], fill=(255, 0, 0), width=3)
    im.save(p.cikti("parcalar.png"))
    log(f"parçalar: {adlar}")
