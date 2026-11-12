"""Senaryonun blok ayrımını çiz: python -m deneyler.bloklari_ciz MASKE_JSON SENARYO NSIDE CIKTI"""
import json
import sys

import numpy as np
from PIL import ImageDraw

from tektonik.bloklar import bloklara_ayir
from tektonik.izgara import izgara_kur, maske_yukle
from tektonik.paleo import paleo_harita
from tektonik.yazi import yazi_tipi


def main():
    mj, sj, nside, cikti = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    maske, sinir = maske_yukle(mj)
    iz = izgara_kur(maske, sinir, nside=nside)
    sen = json.load(open(sj, encoding="utf-8"))
    bl = bloklara_ayir(iz, sen)
    alan = iz.alan_m2 / 1e6
    for i, ad in enumerate(bl.adlar):
        print(f"{ad}: {(bl.etiket == i).sum() * alan / 1e6:.2f} milyon km²")
    print(f"toplam kara {iz.kara.sum() * alan / 1e6:.2f} milyon km², hücre {iz.hucre_km:.1f} km")
    s = (sinir[0] - 3, sinir[1] - 3, sinir[2] + 3, sinir[3] + 3)
    der = 0.1
    im = paleo_harita(iz, bl, {}, 0.0, sinir=s, derece=der)
    d = ImageDraw.Draw(im)
    f = yazi_tipi(14)
    px = lambda lo, la: ((lo - s[0]) / der, (s[3] - la) / der)
    for x in range(-40, 50, 10):
        d.text(px(x + 0.3, s[3] - 0.3), f"{x}°", fill=(0, 0, 0), font=f)
    for y in range(-0, 61, 10):
        d.text(px(s[0] + 0.3, y - 0.3), f"{y}°", fill=(0, 0, 0), font=f)
    for dk in sen.get("dikisler", []):
        d.line([px(*p) for p in dk["cizgi"]], fill=(0, 0, 0), width=3)
    renk = {1: (220, 30, 20), 2: (230, 180, 0), 3: (30, 110, 240), 4: (60, 190, 60)}
    for ist in sen.get("istekler", []):
        c = ist.get("bolge") if isinstance(ist.get("bolge"), list) and len(ist.get("bolge")) > 2 else ist.get("isaret")
        if c:
            d.line([px(*q) for q in c + c[:1]], fill=renk.get(ist["no"], (0, 0, 0)), width=2)
    for ad, b in sen["bloklar"].items():
        x, y = px(*b["tohum"])
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(0, 0, 0))
        d.text((x + 6, y - 8), ad, fill=(0, 0, 0), font=f)
    im.save(cikti)


if __name__ == "__main__":
    main()
