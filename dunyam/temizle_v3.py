"""Ana kalıp v3 = sahibin 24 Kasım Merak dışa aktarımı (kaynak/merak_disa_2026-11-24.png), yalnız kurallı temizlikle
(CLAUDE.md §4.3 madde 5): 30 pikselden küçük kara parçaları deniz, −40 m'den sığ deniz −40 m. Arazi ve kıyı aynen.
v2 ile birleştirme denendi ve bırakıldı: sahibin alçalttığı kesim tam yakalanamadı, geçişte dalgalı iz kaldı."""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
S = 14642
KOK = os.path.dirname(os.path.abspath(__file__))


def coz(g):
    g = g.astype(np.float64)
    return np.where(g > S, 8000 * np.clip((g - S) / (65535 - S), 0, None) ** 2, -6840 * np.clip(1 - g / S, 0, None) ** (1 / 0.607))


def main():
    n = np.asarray(Image.open(os.path.join(KOK, "kaynak", "merak_disa_2026-11-24.png")))
    kara = n > S
    L, nk = ndimage.label(kara); sz = ndimage.sum(kara, L, range(1, nk + 1))
    benek = np.isin(L, np.nonzero(sz < 30)[0] + 1)
    z = coz(n); sig = (~kara) & (z > -40)
    deniz40 = np.uint16(round(S * (1 - (40 / 6840) ** 0.607)))
    G = n.copy(); G[benek | sig] = deniz40
    Image.fromarray(G).save(os.path.join(KOK, "kaynak", "ana_v3_16k.png"))
    k3 = G > S; z3 = coz(G)
    print(f"kara beneği → deniz {int(benek.sum())} piksel ({int((sz < 30).sum())} parça), sığ deniz → −40 m {int(sig.sum())} piksel")
    print("kara payı %.4f, kara %%10/50/90 %s, en yüksek %.0f, 6000 m üstü %d piksel, 8000 m (beyaz) %d" %
          (k3.mean(), np.percentile(z3[k3], [10, 50, 90]).round(), z3[k3].max(), int((z3 > 6000).sum()), int((G == 65535).sum())))
    print("değişen kara piksel (benek dışında):", int(((G != n) & kara & ~benek).sum()))


if __name__ == "__main__":
    main()
