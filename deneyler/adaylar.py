"""Aşama 4: aday tarihler üret, denetle, seç, anlat.

Kullanım: python -m deneyler.adaylar NSIDE SAYI
"""
import json
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

from tektonik.bloklar import bloklara_ayir
from tektonik.izgara import izgara_kur, maske_oku
from tektonik.paleo import paleo_harita
from tektonik.uretici import celiskiler, cesitli_sec, evrimlestir


def main():
    nside, sayi = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    senaryo = json.load(open("veri/test_senaryo.json", encoding="utf-8"))
    iz = izgara_kur(maske_oku("veri/test_maske.png"), nside=nside)
    bloklar = bloklara_ayir(iz, senaryo)
    adaylar = evrimlestir(iz, bloklar, senaryo, tohum_sayisi=sayi, nesil=6, nesil_boyu=sayi // 2)
    sayi = len(adaylar)
    gecerli = [a for a in adaylar if a.gecerli]
    nedenler = {}
    for a in adaylar:
        for x in a.ihlaller:
            nedenler[x.split(":")[0]] = nedenler.get(x.split(":")[0], 0) + 1
    istek_no = [i["no"] for i in senaryo["istekler"]]
    cel = celiskiler(adaylar, istek_no)
    secilen = cesitli_sec(gecerli, 5)
    print(f"{sayi} aday, {len(gecerli)} geçerli; ihlal türleri {nedenler}; süre {time.time()-t0:.0f} s")
    print("çelişki:", cel)
    rapor = {"aday_sayisi": sayi, "gecerli": len(gecerli), "ihlal_turleri": nedenler, "celiski": cel, "secilen": []}
    for a in secilen:
        print(f"-- aday {a.no}: istekler {a.istek_sonuc}")
        for c in a.anlati:
            print("   ", c)
        rapor["secilen"].append({"no": a.no, "parametre": a.parametre, "istekler": {str(k): v for k, v in a.istek_sonuc.items()}, "anlati": a.anlati})
        kareler = []
        bas = a.parametre["baslangic_ma"]
        for ma in (round(bas), round(a.parametre["carpisma_ma"]), round(a.parametre["ta_ma"]), 0):
            im = paleo_harita(iz, bloklar, a.tarihler, float(ma), derece=0.25)
            ImageDraw.Draw(im).text((8, 8), f"{ma} milyon yıl önce", fill=(0, 0, 0))
            kareler.append(im)
        w, h = kareler[0].size
        serit = Image.new("RGB", (w * 4, h), (255, 255, 255))
        for n, im in enumerate(kareler):
            serit.paste(im, (n * w, 0))
        serit.save(f"cikti/aday_{a.no}.png")
    json.dump(rapor, open("cikti/adaylar.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
