"""Küre üzerinde düzgün, çok ölçekli rastgele alan (fBm benzeri).

Rastgele düzlem dalgalarının toplamı; birim küredeki xyz konumları
üzerinde hesaplanır, kutup ya da ızgara izi bırakmaz.
"""
from __future__ import annotations

import numpy as np

from .izgara import YARICAP_M


def fbm(xyz: np.ndarray, en_buyuk_km: float, en_kucuk_km: float, tohum: int = 0,
        hurst: float = 0.5, dalga_sayisi: int = 48) -> np.ndarray:
    """Ortalama 0, standart sapma ~1 olan alan. Dalga boyları en_buyuk..en_kucuk km."""
    rng = np.random.default_rng(tohum)
    R = YARICAP_M / 1e3
    sonuc = np.zeros(xyz.shape[0])
    L = en_buyuk_km
    toplam_w = 0.0
    while L >= en_kucuk_km:
        k = 2 * np.pi * R / L  # birim küre üzerinde dalga sayısı
        yon = rng.normal(size=(dalga_sayisi, 3))
        yon /= np.linalg.norm(yon, axis=1, keepdims=True)
        faz = rng.uniform(0, 2 * np.pi, dalga_sayisi)
        w = (L / en_buyuk_km) ** hurst
        sonuc += w * np.cos(xyz @ (yon.T * k) + faz).sum(axis=1) / np.sqrt(dalga_sayisi / 2)
        toplam_w += w * w
        L /= 2.0
    return sonuc / np.sqrt(toplam_w)
