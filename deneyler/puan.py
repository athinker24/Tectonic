"""Gerçek dünya koşularının çok bölgeli şekil puanı (yükseklik eşiği üstündeki alanların örtüşmesi, IoU).

Kullanım: python -m deneyler.puan ON_EK [ON_EK ...]   (… _z.npy ve _gercek.npy olmadan; 50 km koşular)

Bölgeler ve eşikler (aynı ağırlık):
  Tibet ve Himalaya (68 ile 105°D, 24 ile 42°K): 1500 ve 3000 m
  İran, Zagros, Anadolu, Kafkas (30 ile 66°D, 24 ile 44°K): 1000 ve 2000 m
  Tien Şan ve Tarim (66 ile 96°D, 36 ile 46°K): 1500 m
Puan = beş IoU'nun ortalaması. Tek bölgeye göre ayar yapılmasın diye bütün koşular bu puanla karşılaştırılır.
"""
import sys

import numpy as np

from deneyler.dunya import SINIR, gercek_yukseklik
from tektonik.levha import duzlem_kur

BOLGELER = [
    ("Tibet 1500", (68, 105, 24, 42), 1500), ("Tibet 3000", (68, 105, 24, 42), 3000),
    ("İran 1000", (30, 66, 24, 44), 1000), ("İran 2000", (30, 66, 24, 44), 2000),
    ("TienŞan 1500", (66, 96, 36, 46), 1500),
]


def puan(on, dz, g):
    z = np.load(f"{on}_z.npy")
    out = {}
    for ad, (a0, a1, b0, b1), e in BOLGELER:
        k = (dz.lon > a0) & (dz.lon < a1) & (dz.lat > b0) & (dz.lat < b1)
        m = (z > e) & k; r = (g > e) & k
        out[ad] = (m & r).sum() / max((m | r).sum(), 1)
    return out, float(np.mean(list(out.values())))


def main():
    zr, _, _ = gercek_yukseklik()
    dz = duzlem_kur(zr > 0, SINIR, h_km=50.0, pay_km=800.0)
    g = None
    for on in sys.argv[1:]:
        if g is None:
            g = np.load(f"{on}_gercek.npy")
        o, p = puan(on, dz, g)
        print(f"{p:.3f}  " + "  ".join(f"{k} {v:.2f}" for k, v in o.items()) + f"  {on[-45:]}")


if __name__ == "__main__":
    main()
