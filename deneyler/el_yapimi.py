"""Aşama 2 deneyi: elle çizilmiş yükselmeyle aşınma, kıyı sönümlemesi ve ayar.

Kullanım: python -m deneyler.el_yapimi NSIDE K SONUM_KM SURE_MYR ETIKET
"""
import json
import sys
import time

import numpy as np

from tektonik.asinma import AsinmaAyar, asindir
from tektonik.gorsel import kabartma, tuval_kur, yukseklik_png
from tektonik.izgara import izgara_kur, maske_oku


def el_yapimi_yukselme(iz, sonum_km):
    """Doğu batı sıradağ (33°K, 35°B..40°D), arkasında plato, zemin yükselmesi."""
    lat, lon = iz.lat, iz.lon
    # sıradağ: enlem 33 çevresinde Gauss, yarı genişlik ~150 km (1,35°)
    boy = 1.0 / (1.0 + np.exp(-(lon + 35) / 2.0)) * 1.0 / (1.0 + np.exp((lon - 40) / 2.0))
    sira = 4.0e-3 * np.exp(-((lat - 33.0) / 1.35) ** 2) * boy
    # plato: 36..44°K arası geniş, zayıf yükselme
    plato = 0.25e-3 * np.exp(-((lat - 40.0) / 4.0) ** 2) * boy
    zemin = 0.03e-3
    u = sira + plato + zemin
    if sonum_km > 0:
        d = iz.kiyiya_km
        s = np.clip(d / sonum_km, 0, 1)
        u = u * (s * s * (3 - 2 * s))  # yumuşak basamak
    return np.where(iz.kara, u, 0.0)


def egim_olc(iz, tv, z):
    """Hücre ortalamaları arasındaki eğim (derece): ortanca ve %90, bölgeye göre."""
    zi = np.where(tv.kara, z[tv.dugum], np.nan)
    dy = tv.derece * 111.19e3
    dx = dy * np.cos(np.radians(tv.lat))[:, None]
    gy, gx = np.gradient(zi)
    e = np.degrees(np.arctan(np.hypot(gx / dx, gy / dy)))
    LA = np.broadcast_to(tv.lat[:, None], zi.shape)
    sira = np.isfinite(e) & (np.abs(LA - 33.0) < 1.5)
    return {
        "sira_egim_ortanca": float(np.nanmedian(e[sira])),
        "sira_egim_p90": float(np.nanpercentile(e[sira], 90)),
        "tum_egim_ortanca": float(np.nanmedian(e)),
    }


def main():
    nside, k, sonum, sure, etiket = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    t0 = time.time()
    iz = izgara_kur(maske_oku("veri/test_maske.png"), nside=nside)
    u = el_yapimi_yukselme(iz, sonum)
    son = asindir(iz, u, sure * 1e6, AsinmaAyar(k=k))
    z = son.z
    tv = tuval_kur(iz, derece=0.08 if nside >= 512 else 0.16)
    kabartma(iz, z, tv).save(f"cikti/{etiket}.png")
    kiyi1 = iz.kara & (iz.kiyiya_km < 1.2 * iz.hucre_km)
    kiyi3 = iz.kara & (iz.kiyiya_km < 3.5 * iz.hucre_km)
    sira = iz.kara & (np.abs(iz.lat - 33.0) < 1.0) & (iz.lon > -30) & (iz.lon < 35)
    plato = iz.kara & (np.abs(iz.lat - 40.0) < 2.0) & (iz.lon > -20) & (iz.lon < 30) & (iz.kiyiya_km > 300)
    r = {
        "etiket": etiket, "nside": nside, "hucre_km": round(iz.hucre_km, 1), "k": k, "sonum_km": sonum, "sure_myr": sure,
        "kara_dugum": int(iz.kara.sum()), "zmax": float(z.max()), "kara_ort": float(z[iz.kara].mean()),
        "kara_medyan": float(np.median(z[iz.kara])),
        "sira_ort": float(z[sira].mean()), "sira_p95": float(np.percentile(z[sira], 95)),
        "plato_ort": float(z[plato].mean()) if plato.any() else None,
        "kiyi_ilk_hucre_ort_m": float(z[kiyi1].mean()), "kiyi_ilk_hucre_p95_m": float(np.percentile(z[kiyi1], 95)),
        "kiyi_ilk_hucre_maks_m": float(z[kiyi1].max()),
        "kiyi_3hucre_p95_m": float(np.percentile(z[kiyi3], 95)),
        "sure_s": round(time.time() - t0, 1),
    }
    r.update(egim_olc(iz, tv, z))
    json.dump(r, open(f"cikti/{etiket}.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
