"""Rastgele mod: senaryo ve sahip işaretleri olmadan rastgele birleşme tarihi ve kabartma.

Kullanım: python -m deneyler.rastgele TOHUM [NSIDE_SON] [BLOK_SAYISI]
Tarama Nside 128'de yapılır; geçerli ilk aday son çözünürlükte yeniden kurulur,
yeniden denetlenir ve aşınmalı tam modelle koşulur. Çıktı: cikti/rastgele/<tohum>_*.
"""
import json
import os
import sys
import time

import numpy as np
from PIL import ImageDraw

from tektonik.gorsel import kabartma, tuval_kur, yukseklik_png
from tektonik.izgara import izgara_kur, maske_yukle
from tektonik.model import ModelAyar, kos
from tektonik.paleo import paleo_harita
from tektonik.rastgele import rastgele_aday, rastgele_bloklar, tohum_sec
from tektonik.uretici import kisitlari_denetle
from tektonik.yazi import yazi_tipi


def kur(nside, maske, sinir, tohumlar, tohum):
    iz = izgara_kur(maske, sinir, nside=nside)
    return iz, rastgele_bloklar(iz, tohumlar, gurultu_tohum=tohum)


def main():
    tohum = int(sys.argv[1])
    nside = int(sys.argv[2]) if len(sys.argv) > 2 else 256
    rng = np.random.default_rng(tohum)
    sayi = int(sys.argv[3]) if len(sys.argv) > 3 else int(rng.integers(4, 9))
    os.makedirs("cikti/rastgele", exist_ok=True)
    on = f"cikti/rastgele/{tohum}_{nside}"
    t0 = time.time()
    maske, sinir = maske_yukle("veri/maske.json")
    iz_t = izgara_kur(maske, sinir, nside=128)
    tohumlar = tohum_sec(iz_t, sayi, rng)
    bl_t = rastgele_bloklar(iz_t, tohumlar, gurultu_tohum=tohum)
    print(f"{len(bl_t.adlar)} blok: {bl_t.adlar}")

    iz, bl = (iz_t, bl_t) if nside == 128 else kur(nside, maske, sinir, tohumlar, tohum)
    if bl.adlar != bl_t.adlar:
        print("uyarı: son çözünürlükte blok sırası farklı; tarama son çözünürlükte yapılacak")
        iz_t, bl_t = iz, bl
    denenen, aday = 0, None
    nedenler: dict = {}
    for no in range(400):
        denenen += 1
        a = rastgele_aday(no, np.random.default_rng([tohum, no]), iz_t, bl_t)
        if len(a.olaylar) == 0:
            nedenler["olay yok"] = nedenler.get("olay yok", 0) + 1
            continue
        kisitlari_denetle(a, iz_t, bl_t, {})
        if a.gecerli:
            if iz is not iz_t:
                a = rastgele_aday(no, np.random.default_rng([tohum, no]), iz, bl)
                kisitlari_denetle(a, iz, bl, {})
                if not a.gecerli:
                    nedenler["son çözünürlükte geçersiz"] = nedenler.get("son çözünürlükte geçersiz", 0) + 1
                    continue
            aday = a
            break
        for x in a.ihlaller:
            k = x.split(":")[0]
            nedenler[k] = nedenler.get(k, 0) + 1
    print(f"{denenen} aday denendi; elenme nedenleri {nedenler}")
    if aday is None:
        print("geçerli aday bulunamadı")
        return
    for c in aday.anlati:
        print("  ", c)
    bas = float(np.ceil(max(o.baslangic_ma for o in aday.olaylar) + 2))
    son = kos(iz, aday.olaylar, bas, ModelAyar(kare_myr=2.0, tohum=tohum))
    tv = tuval_kur(iz, derece=0.08 if nside >= 512 else 0.16)
    kabartma(iz, son.z, tv).save(f"{on}_son.png")
    yukseklik_png(son.z, tv).save(f"{on}_yukseklik16.png")
    s = (sinir[0] - 25, sinir[1] - 15, sinir[2] + 25, sinir[3] + 8)
    der = 0.25 if nside < 512 else 0.15
    f = yazi_tipi(18)
    harita = paleo_harita(iz, bl, {}, 0.0, sinir=(sinir[0] - 3, sinir[1] - 3, sinir[2] + 3, sinir[3] + 3), derece=0.1)
    d = ImageDraw.Draw(harita)
    for k, ad in enumerate(bl.adlar):
        lo = iz.lon[bl.etiket == k].mean()
        la = iz.lat[bl.etiket == k].mean()
        d.text(((lo - sinir[0] + 3) / 0.1, (sinir[3] + 3 - la) / 0.1), ad, fill=(0, 0, 0), font=yazi_tipi(16))
    harita.save(f"{on}_bloklar.png")
    kareler = []
    for ma, z in son.kareler:
        im = paleo_harita(iz, bl, aday.tarihler, float(ma), z=z.astype(float), sinir=s, derece=der)
        ImageDraw.Draw(im).text((10, 8), f"{ma:.0f} milyon yıl önce", fill=(0, 0, 0), font=f)
        kareler.append(im)
    kareler[0].save(f"{on}.gif", save_all=True, append_images=kareler[1:] + [kareler[-1]] * 8,
                    duration=220, loop=0, optimize=True)
    z = son.z
    r = dict(tohum=tohum, nside=nside, blok=bl.adlar, denenen=denenen, elenme=nedenler, baslangic_ma=bas,
             zmax_m=float(z.max()), kara_ortanca_m=float(np.median(z[iz.kara])),
             kara_p90_m=float(np.percentile(z[iz.kara], 90)), sure_s=round(time.time() - t0),
             parametre=aday.parametre, anlati=aday.anlati)
    json.dump(r, open(f"{on}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)
    print(json.dumps({k: v for k, v in r.items() if k not in ("parametre", "anlati")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
