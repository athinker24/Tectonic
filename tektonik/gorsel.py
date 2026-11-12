"""Katman 4: HEALPix alanını haritaya çevir, kabartma ve 16 bit yükseklik yaz."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image
from scipy.spatial import cKDTree

from .izgara import Izgara, _lonlat_xyz

# Yükseklik renkleri (m, RGB). Ova yeşili, plato sarısı, dağ kahvesi, zirve beyazı.
_RENK = np.array(
    [
        (0, 112, 153, 108),
        (300, 150, 178, 120),
        (800, 196, 196, 136),
        (1500, 200, 170, 120),
        (2500, 172, 136, 106),
        (4000, 150, 124, 112),
        (5500, 214, 208, 204),
        (7000, 255, 255, 255),
    ],
    dtype=float,
)
_DENIZ = np.array([168, 198, 214], dtype=float)


@dataclass
class Tuval:
    """Kıtayı kaplayan eşdikdörtgen görüntü ızgarası."""

    sinir: tuple[float, float, float, float]  # batı, güney, doğu, kuzey
    derece: float
    dugum: np.ndarray  # [H, W] en yakın ızgara düğümü
    kara: np.ndarray  # [H, W] bool
    lat: np.ndarray  # [H]

    @property
    def boyut(self) -> tuple[int, int]:
        return self.kara.shape


def tuval_kur(iz: Izgara, derece: float = 0.08, pay: float = 1.5) -> Tuval:
    b, d = iz.lon[iz.kara].min() - pay, iz.lon[iz.kara].max() + pay
    g, k = iz.lat[iz.kara].min() - pay, iz.lat[iz.kara].max() + pay
    lon = np.arange(b, d, derece) + derece / 2
    lat = np.arange(k, g, -derece) - derece / 2
    LO, LA = np.meshgrid(lon, lat)
    secili = np.flatnonzero(iz.kara | iz.kiyi)
    agac = cKDTree(iz.xyz[secili])
    kir, j = agac.query(_lonlat_xyz(LO.ravel(), LA.ravel()))
    dugum = secili[j].reshape(LO.shape)
    yakin = (kir.reshape(LO.shape) * 6371.0) < iz.hucre_km * 0.75
    kara = iz.kara[dugum] & yakin
    return Tuval((b, g, d, k), derece, dugum, kara, lat)


def golgele(z: np.ndarray, tv: Tuval, abarti: float = 12.0) -> np.ndarray:
    """Çok yönlü gölgeleme (4 yön, ağırlıklı). Dönüş 0..1."""
    dy = tv.derece * 111.19e3
    dx = dy * np.cos(np.radians(tv.lat))[:, None]
    gy, gx = np.gradient(z * abarti)
    gy /= -dy  # satır güneye artar
    gx /= dx
    egim = np.arctan(np.hypot(gx, gy))
    baki = np.arctan2(-gx, gy)
    yuk = np.radians(45.0)
    toplam = np.zeros_like(z)
    for az, w in ((315, 0.5), (270, 0.2), (360, 0.2), (225, 0.1)):
        a = np.radians(az)
        toplam += w * (np.sin(yuk) * np.cos(egim) + np.cos(yuk) * np.sin(egim) * np.cos(a - baki))
    return np.clip(toplam, 0, 1)


def kabartma(iz: Izgara, z: np.ndarray, tv: Tuval, zmax: float | None = None) -> Image.Image:
    zi = np.where(tv.kara, z[tv.dugum], 0.0)
    olcek = 1.0 if zmax is None else 7000.0 / max(zmax, 1.0)
    zr = np.clip(zi * olcek, 0, 7000)
    rgb = np.stack([np.interp(zr, _RENK[:, 0], _RENK[:, i]) for i in (1, 2, 3)], axis=-1)
    g = golgele(zi, tv)
    duz = np.sin(np.radians(45.0))
    rgb = rgb * (0.55 + 0.75 * (g - duz) / duz * 0.6 + 0.45)[..., None]
    rgb = np.where(tv.kara[..., None], rgb, _DENIZ)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def yukseklik_png(z: np.ndarray, tv: Tuval, zmax: float = 9000.0) -> Image.Image:
    """16 bit gri yükseklik haritası: 0 = deniz, 65535 = zmax metre."""
    zi = np.where(tv.kara, z[tv.dugum], 0.0)
    return Image.fromarray(np.clip(zi / zmax * 65535.0, 0, 65535).astype(np.uint16))
