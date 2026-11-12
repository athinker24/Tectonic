"""Duvar dikişine dik ortalama kesit: python -m deneyler.kesit NSIDE Z_NPY"""
import json
import sys

import numpy as np

from tektonik.izgara import izgara_kur, maske_yukle
from tektonik.olaylar import isaretli_uzaklik_km


def main():
    nside, yol = int(sys.argv[1]), sys.argv[2]
    s = json.load(open("veri/senaryo.json", encoding="utf-8"))
    m, b = maske_yukle("veri/maske.json")
    iz = izgara_kur(m, b, nside=nside)
    z = np.load(yol)
    cep = np.array(next(d for d in s["dikisler"] if d["ad"] == "Duvar dikişi")["cizgi"])
    d = np.full(iz.n, np.nan)
    d[iz.kara] = isaretli_uzaklik_km(iz, cep, iz.kara)
    orta = iz.kara & (iz.lon > 8) & (iz.lon < 28)
    for a in range(-300, 1600, 100):
        sel = orta & (d >= a) & (d < a + 100)
        if sel.sum():
            print(f"{a:5d}..{a + 100:5d} km  z ort {z[sel].mean():6.0f}  p90 {np.percentile(z[sel], 90):6.0f}")


if __name__ == "__main__":
    main()
