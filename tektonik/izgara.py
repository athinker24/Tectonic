"""Katman 0: küre ızgarası ve kıyı.

HEALPix ızgarası (eşit alanlı). Kara düğümleri hesaba girer, karaya komşu
deniz düğümleri sabit yükseklikli taban düğümüdür (kıyı), geri kalan deniz
hesap dışıdır. Kıyı bu yüzden hiçbir adımda oynamaz.
"""
from __future__ import annotations

from dataclasses import dataclass

import fastscapelib as fs
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree

YARICAP_M = 6.371e6  # KARARLAR.md 2

CORE = int(fs.NodeStatus.CORE.value)
SABIT = int(fs.NodeStatus.FIXED_VALUE.value)
DISARI = int(fs.NodeStatus.GHOST.value)


def maske_oku(yol: str, esik: int = 128) -> np.ndarray:
    """Siyah beyaz maske PNG'sini oku. True = kara (açık renk)."""
    a = np.array(Image.open(yol).convert("L"))
    return a >= esik


@dataclass
class Izgara:
    nside: int
    grid: "fs.HealpixGrid"
    lon: np.ndarray  # derece, -180..180
    lat: np.ndarray  # derece
    xyz: np.ndarray  # birim küre, [N, 3]
    durum: np.ndarray  # CORE / SABIT / DISARI
    kara: np.ndarray  # bool
    kiyi: np.ndarray  # bool (sabit taban düğümleri)
    alan_m2: float
    kiyiya_km: np.ndarray  # kara düğümleri için kıyıya uzaklık, diğerleri 0

    @property
    def n(self) -> int:
        return self.durum.size

    @property
    def hucre_km(self) -> float:
        return float(np.sqrt(self.alan_m2) / 1e3)


def _lonlat_xyz(lon_d: np.ndarray, lat_d: np.ndarray) -> np.ndarray:
    lo, la = np.radians(lon_d), np.radians(lat_d)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], axis=-1)


def izgara_kur(
    maske: np.ndarray,
    sinir: tuple[float, float, float, float] = (-180.0, -90.0, 180.0, 90.0),
    nside: int = 512,
) -> Izgara:
    """Eşdikdörtgen kara maskesinden HEALPix ızgarası kur.

    maske: [H, W] bool, satır 0 kuzey. sinir: (batı, güney, doğu, kuzey) derece.
    """
    n = 12 * nside * nside
    g0 = fs.HealpixGrid(nside, np.zeros(n, dtype=np.uint8), YARICAP_M)
    lon_r, lat_r = np.asarray(g0.nodes_lonlat())
    lon = np.degrees(lon_r)
    lon = np.where(lon > 180.0, lon - 360.0, lon)
    lat = np.degrees(lat_r)

    b, gy, d, k = sinir
    H, W = maske.shape
    ic = (lon >= b) & (lon < d) & (lat > gy) & (lat <= k)
    r = np.clip(((k - lat) / (k - gy) * H).astype(int), 0, H - 1)
    c = np.clip(((lon - b) / (d - b) * W).astype(int), 0, W - 1)
    kara = np.zeros(n, bool)
    kara[ic] = maske[r[ic], c[ic]]

    xyz = _lonlat_xyz(lon, lat)
    alan = 4.0 * np.pi * YARICAP_M**2 / n
    hucre = np.sqrt(alan)

    # Kıyı: karaya 1,6 hücreden yakın deniz düğümleri (8 komşuluk dahil).
    agac_kara = cKDTree(xyz[kara])
    deniz_i = np.flatnonzero(~kara)
    # yalnız karanın yakınındaki denize bak (hız için kaba kutu)
    yakin = deniz_i[
        (lon[deniz_i] > lon[kara].min() - 2)
        & (lon[deniz_i] < lon[kara].max() + 2)
        & (lat[deniz_i] > lat[kara].min() - 2)
        & (lat[deniz_i] < lat[kara].max() + 2)
    ]
    kiris, _ = agac_kara.query(xyz[yakin])
    kiyi = np.zeros(n, bool)
    kiyi[yakin[kiris * YARICAP_M < 1.6 * hucre]] = True

    durum = np.full(n, DISARI, dtype=np.uint8)
    durum[kara] = CORE
    durum[kiyi] = SABIT

    kiyiya = np.zeros(n)
    agac_kiyi = cKDTree(xyz[kiyi])
    kir, _ = agac_kiyi.query(xyz[kara])
    kiyiya[kara] = 2.0 * np.arcsin(np.clip(kir / 2.0, 0, 1)) * YARICAP_M / 1e3

    grid = fs.HealpixGrid(nside, durum, YARICAP_M)
    return Izgara(nside, grid, lon, lat, xyz, durum, kara, kiyi, alan, kiyiya)


def buyuk_daire_km(iz: Izgara, lon0: float, lat0: float) -> np.ndarray:
    """Her düğümün (lon0, lat0) noktasına büyük daire uzaklığı, km."""
    p = _lonlat_xyz(np.array(lon0), np.array(lat0))
    return np.arccos(np.clip(iz.xyz @ p, -1, 1)) * YARICAP_M / 1e3
