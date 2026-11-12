"""Geçmiş anın haritası: blokları geriye sürüp yeniden çizer."""
from __future__ import annotations

import numpy as np
from PIL import Image
from scipy.spatial import cKDTree

from . import kure
from .bloklar import Bloklar
from .gorsel import _DENIZ, _RENK, golgele
from .izgara import Izgara, _lonlat_xyz
from .tarih import BlokTarihi

BLOK_RENK = [(196, 180, 140), (150, 180, 120), (200, 150, 120), (160, 150, 200), (120, 170, 190), (210, 190, 110),
             (170, 130, 160), (130, 150, 110), (220, 160, 160), (140, 190, 170)]


def konumlar(iz: Izgara, bloklar: Bloklar, tarihler: dict[str, BlokTarihi], ma: float) -> np.ndarray:
    """Her kara düğümünün `ma` anındaki birim vektörü (sabit blok yerinde)."""
    p = iz.xyz.copy()
    for i, ad in enumerate(bloklar.adlar):
        if ad not in tarihler:
            continue
        m = bloklar.etiket == i
        p[m] = kure.uygula(tarihler[ad].geri_donme(ma), iz.xyz[m])
    return p


def paleo_harita(iz: Izgara, bloklar: Bloklar, tarihler: dict[str, BlokTarihi], ma: float,
                 z: np.ndarray | None = None, sinir=(-70.0, -40.0, 70.0, 72.0), derece: float = 0.15) -> Image.Image:
    b, g, d, k = sinir
    lon = np.arange(b, d, derece) + derece / 2
    lat = np.arange(k, g, -derece) - derece / 2
    LO, LA = np.meshgrid(lon, lat)
    kara = np.flatnonzero(iz.kara)
    p = konumlar(iz, bloklar, tarihler, ma)[kara]
    agac = cKDTree(p)
    kir, j = agac.query(_lonlat_xyz(LO.ravel(), LA.ravel()))
    yakin = (kir * 6371.0 < iz.hucre_km * 0.8).reshape(LO.shape)
    dugum = kara[j].reshape(LO.shape)
    if z is None:
        rgb = np.array(BLOK_RENK, float)[np.clip(bloklar.etiket[dugum], 0, len(BLOK_RENK) - 1)]
    else:
        zi = np.where(yakin, z[dugum], 0.0)
        rgb = np.stack([np.interp(np.clip(zi, 0, 7000), _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], axis=-1)

        class _T:
            pass
        t = _T(); t.derece = derece; t.lat = lat
        gl = golgele(zi, t)
        duz = np.sin(np.radians(45.0))
        rgb = rgb * (0.55 + 0.75 * (gl - duz) / duz * 0.6 + 0.45)[..., None]
    rgb = np.where(yakin[..., None], rgb, _DENIZ)
    # 10 derecelik enlem boylam çizgileri
    H, W = rgb.shape[:2]
    for x in np.arange(np.ceil(b / 10) * 10, d, 10):
        c = int((x - b) / derece)
        if 0 <= c < W:
            rgb[:, c] = rgb[:, c] * 0.85
    for y in np.arange(np.ceil(g / 10) * 10, k, 10):
        r = int((k - y) / derece)
        if 0 <= r < H:
            rgb[r] = rgb[r] * 0.85
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
