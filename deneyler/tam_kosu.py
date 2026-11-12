"""Seçilen adayı aşınmalı tam modelle koş: kabartma, paleo animasyon, istek ölçümleri.

Kullanım: python -m deneyler.tam_kosu NSIDE ADAY_NO [K]
Aday parametreleri cikti/gercek/adaylar.json içinden okunur.

Not: aşınma ve yükselme bugünkü kıyı çizgisiyle bugünkü ızgarada hesaplanır;
paleo karelerde bu yükseklik blokların geçmiş konumlarına taşınır. Yani
çarpışma öncesi blokların kıyıları da bugünkü gibidir (bilinen basitleştirme).
"""
import json
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

from tektonik.bloklar import bloklara_ayir
from tektonik.gorsel import kabartma, tuval_kur, yukseklik_png
from tektonik.izgara import izgara_kur, maske_yukle
from tektonik.model import ModelAyar, kos
from tektonik.olaylar import isaretli_uzaklik_km
from tektonik.paleo import paleo_harita
from tektonik.uretici import aday_kur, bolge_maske, omurga_maske
from tektonik.yazi import yazi_tipi


def olc(iz, bl, sen, p, z):
    r = {"kara_ortanca_m": float(np.median(z[iz.kara])), "zmax_m": float(z.max())}
    for ist in sen["istekler"]:
        if ist["tur"] == "kusak":
            m = bolge_maske(iz, ist["bolge"])
            r["sıradağ_z_p95_m"] = float(np.percentile(z[m], 95))
            r["sıradağ_z_ort_m"] = float(z[m].mean())
        elif ist["tur"] == "plato":
            m = bolge_maske(iz, ist["bolge"])
            r["çanak_z_ortanca_m"] = float(np.median(z[m]))
            r["çanak_z_p10_p90_m"] = [float(np.percentile(z[m], 10)), float(np.percentile(z[m], 90))]
        elif ist["tur"] == "yarimada":
            ya = bl.maske(ist["blok"])
            if p["ya_tur"] == "alp":
                yd = next(d for d in sen["dikisler"] if d["ad"] == "Yarımada dikişi")
                u = np.full(iz.n, np.inf)
                u[iz.kara] = np.abs(isaretli_uzaklik_km(iz, np.array(yd["cizgi"], float), iz.kara))
                m = ya & (u < 300)
                r["yarımada_kök_z_p95_m"] = float(np.percentile(z[m], 95))
            else:
                om, _ = omurga_maske(iz, ya)
                r["yarımada_omurga_z_p90_m"] = float(np.percentile(z[om], 90))
            r["yarımada_z_ortanca_m"] = float(np.median(z[ya]))
        elif ist["tur"] == "dagli_blok":
            m = bl.maske(ist["blok"])
            r["mikro_kıta_z_ortanca_m"] = float(np.median(z[m]))
            r["mikro_kıta_500m_üstü_pay"] = float(np.mean(z[m] > 500))
    return r


def main():
    nside, no = int(sys.argv[1]), int(sys.argv[2])
    k = float(sys.argv[3]) if len(sys.argv) > 3 else 4e-9
    sert = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    t0 = time.time()
    sen = json.load(open("veri/senaryo.json", encoding="utf-8"))
    rapor = json.load(open("cikti/gercek/adaylar.json", encoding="utf-8"))
    p = dict(next(a["parametre"] for a in rapor["secilen"] if a["no"] == no))
    p["kusak_sertlik"] = sert
    if len(sys.argv) > 5:
        p["plato_orani"] = float(sys.argv[5])
    maske, sinir = maske_yukle("veri/maske.json")
    iz = izgara_kur(maske, sinir, nside=nside)
    bl = bloklara_ayir(iz, sen)
    a = aday_kur(no, np.random.default_rng(0), iz, bl, sen, p)
    bas = float(np.ceil(max(o.baslangic_ma for o in a.olaylar) + 2))
    son = kos(iz, a.olaylar, bas, ModelAyar(k=k, kare_myr=2.0, tohum=no))
    on = f"cikti/gercek/tam_{no}_{nside}" + (f"_s{sert:g}" if sert != 1.0 else "") + (f"_p{p['plato_orani']:g}" if len(sys.argv) > 5 else "")
    tv = tuval_kur(iz, derece=0.08 if nside >= 512 else 0.16)
    kabartma(iz, son.z, tv).save(f"{on}_son.png")
    yukseklik_png(son.z, tv).save(f"{on}_yukseklik16.png")
    # paleo animasyon: blokların geçmiş konumunda o anki yükseklik
    s = (sinir[0] - 25, sinir[1] - 15, sinir[2] + 25, sinir[3] + 8)
    der = 0.25 if nside < 512 else 0.15
    f = yazi_tipi(18)
    kareler = []
    for ma, z in son.kareler:
        im = paleo_harita(iz, bl, a.tarihler, float(ma), z=z.astype(float), sinir=s, derece=der)
        ImageDraw.Draw(im).text((10, 8), f"{ma:.0f} milyon yıl önce", fill=(0, 0, 0), font=f)
        kareler.append(im)
    kareler[0].save(f"{on}.gif", save_all=True, append_images=kareler[1:] + [kareler[-1]] * 8,
                    duration=220, loop=0, optimize=True)
    np.save(f"{on}_z.npy", son.z.astype(np.float32))
    r = dict(no=no, nside=nside, kusak_sertlik=sert, plato_orani=p.get("plato_orani", 0.0), hucre_km=round(iz.hucre_km, 1), k=k, baslangic_ma=bas, tur=p.get("ya_tur"),
             sure_s=round(time.time() - t0), **olc(iz, bl, sen, p, son.z), anlati=a.anlati, gunluk=son.gunluk)
    json.dump(r, open(f"{on}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({x: v for x, v in r.items() if x not in ("gunluk", "anlati")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
