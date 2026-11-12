"""Zaman döngüsü: olaylar -> kabuk kalınlaşması -> yükselme -> aşınma -> izostazi."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .asinma import AsinmaAyar, Asindirici
from .gurultu import fbm
from .izgara import Izgara
from .izostazi import Duzlestirici, geri_sicrama
from .olaylar import AIRY, H0_M


@dataclass
class ModelAyar:
    k: float = 4e-9
    m: float = 1.0  # m/n = 0,5
    n: float = 2.0  # Ruetenik ve diğ. 2023 küresel uyum n ≈ 2,3 (arastirma/13)
    k_degiskenlik: float = 0.5  # ln K standart sapması (kayaç sertliği farkı)
    dt_yil: float = 1e5
    bukulme_km: float = 80.0
    kiyi_sonum_km: float = 60.0  # yükselmenin kıyıya doğru sönüm uzunluğu
    kare_myr: float = 2.0
    tohum: int = 1


@dataclass
class ModelSonuc:
    z: np.ndarray
    h: np.ndarray
    kareler: list[tuple[float, np.ndarray]] = field(default_factory=list)
    gunluk: list[dict] = field(default_factory=list)


def kos(iz: Izgara, olaylar: list, baslangic_ma: float, ayar: ModelAyar | None = None) -> ModelSonuc:
    ayar = ayar or ModelAyar()
    kara = iz.kara
    g_lit = fbm(iz.xyz, 2000.0, 60.0, tohum=ayar.tohum)
    g_tek = fbm(iz.xyz, 1500.0, 80.0, tohum=ayar.tohum + 7)
    k_alan = ayar.k * np.exp(ayar.k_degiskenlik * g_lit)
    for o in olaylar:
        o.hazirla(iz, g_tek)
        if hasattr(o, "k_carpani"):
            k_alan = k_alan * o.k_carpani(iz)
    asin = Asindirici(iz, AsinmaAyar(k=k_alan, m=ayar.m, n=ayar.n, dt_yil=ayar.dt_yil))
    duz = Duzlestirici(iz, ayar.bukulme_km)

    # başlangıç: alçak, hafif engebeli kıta; kıyıya doğru sıfıra iner
    s = np.clip(iz.kiyiya_km / 150.0, 0, 1)
    z = np.zeros(iz.n)
    z[kara] = (120.0 + 60.0 * fbm(iz.xyz, 1500.0, 100.0, tohum=ayar.tohum + 3)[kara]) * (s * s * (3 - 2 * s))[kara]
    z = np.clip(z, 0, None)
    h = np.full(iz.n, H0_M)
    h[kara] += z[kara] / AIRY

    ks = np.clip(iz.kiyiya_km / max(ayar.kiyi_sonum_km, 1e-9), 0, 1)
    kiyi_sonum = ks * ks * (3 - 2 * ks)

    sonuc = ModelSonuc(z=z, h=h)
    adim = int(round(baslangic_ma * 1e6 / ayar.dt_yil))
    sonraki = baslangic_ma
    idx = np.flatnonzero(kara)
    for i in range(adim + 1):
        ma = baslangic_ma - i * ayar.dt_yil / 1e6
        if ma <= sonraki + 1e-9:
            sonuc.kareler.append((round(ma, 3), z.astype(np.float32).copy()))
            sonraki -= ayar.kare_myr
        if i == adim:
            break
        r = np.zeros(idx.size)
        for o in olaylar:
            r += o.kalinlasma(ma, h)
        r *= kiyi_sonum[idx]
        h[idx] += r * ayar.dt_yil
        z[idx] += AIRY * r * ayar.dt_yil
        e = asin.adim(z)
        h -= e
        z[kara] += geri_sicrama(duz, e)[kara]
        z[~kara] = 0.0
        if i % 50 == 0:
            sonuc.gunluk.append(dict(ma=round(ma, 2), zmax=float(z.max()), zort=float(z[kara].mean()),
                                     hmax=float(h[kara].max()), asinma_ort_mm_yil=float(e[kara].mean() / ayar.dt_yil * 1e3)))
    sonuc.z, sonuc.h = z, h
    return sonuc
