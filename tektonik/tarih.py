"""Blok tarihi: aşamalı Euler dönmeleriyle geriye sürme.

Her blok için hareket aşamaları sabit bloğa (Kuzey) göre tanımlıdır:
(baslangic_ma, bitis_ma, kutup_lon, kutup_lat, hiz_derece_myr). Pozitif hız,
blok ileri zamanda kutup çevresinde saat yönünün tersine döner demektir.
Geçmişteki konum, bugünkü konumdan bu hareketlerin geri alınmasıdır; bu
yüzden son kare tanım gereği bugünkü kıyıdır.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import kure


@dataclass
class Asama:
    baslangic_ma: float
    bitis_ma: float
    kutup_lon: float
    kutup_lat: float
    hiz_derece_myr: float


@dataclass
class BlokTarihi:
    ad: str
    asamalar: list[Asama] = field(default_factory=list)

    def geri_donme(self, ma: float) -> np.ndarray:
        """Bugünkü konumdan `ma` milyon yıl önceki konuma götüren kuaterniyon."""
        q = np.array([1.0, 0.0, 0.0, 0.0])
        for a in sorted(self.asamalar, key=lambda a: a.bitis_ma):
            ust = min(ma, a.baslangic_ma)
            sure = ust - a.bitis_ma
            if sure <= 0:
                continue
            q = kure.carp(kure.donme(a.kutup_lon, a.kutup_lat, -a.hiz_derece_myr * sure), q)
        return q

    def asama(self, ma: float) -> Asama | None:
        for a in self.asamalar:
            if a.bitis_ma <= ma < a.baslangic_ma:
                return a
        return None

    def hiz_cm_yil(self, ma: float, p: np.ndarray) -> np.ndarray:
        """`ma` anında, o andaki konumu p olan noktaların sabit bloğa göre hızı."""
        # aynı anda etkin birden çok aşama (ana bloktan devralınan + kendi) toplanır
        v = np.zeros_like(np.asarray(p, float))
        for a in self.asamalar:
            if a.bitis_ma <= ma < a.baslangic_ma:
                v = v + kure.hiz_cm_yil(a.kutup_lon, a.kutup_lat, a.hiz_derece_myr, p)
        return v


def hareket_kutbu(merkez_lonlat: tuple[float, float], yon_derece: float, hiz_cm_yil: float) -> tuple[float, float, float]:
    """Bir noktayı verilen yönde (kuzeyden saat yönünde, derece) verilen hızla
    götüren Euler kutbu ve açısal hız (derece/milyon yıl)."""
    c = kure._lonlat_xyz(np.array(merkez_lonlat[0]), np.array(merkez_lonlat[1]))
    dogu = np.cross([0.0, 0.0, 1.0], c)
    dogu /= np.linalg.norm(dogu)
    kuzey = np.cross(c, dogu)
    a = np.radians(yon_derece)
    t = np.cos(a) * kuzey + np.sin(a) * dogu  # hareket yönü
    kutup = np.cross(c, t)  # v = ω × r -> ω ∥ r × v
    kutup /= np.linalg.norm(kutup)
    lon, lat = kure.xyz_lonlat(kutup)
    w = hiz_cm_yil / kure.CM_YIL * 1e6  # rad/milyon yıl
    return float(lon), float(lat), float(np.degrees(w))
