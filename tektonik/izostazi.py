"""Bölgesel izostazi: aşınan yükün geri sıçraması, bükülme ölçeğinde yayılır.

Aşınma e kadar kaya kaldırdığında Airy dengesinde yüzey (ρc/ρm)·e kadar geri
yükselir. Litosfer bunu yerel değil bükülme uzunluğu ölçeğinde (kıtada
yaklaşık 50 ile 150 km, arastirma/03) yaydığı için aşınma alanı önce
düzleştirilir. Düzleştirme, komşu ortalamasının tekrarı (yayılma) ile.
"""
from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.spatial import cKDTree

from .izgara import Izgara

RHO_C = 2800.0
RHO_M = 3300.0


class Duzlestirici:
    def __init__(self, iz: Izgara, sigma_km: float = 80.0):
        idx = np.flatnonzero(iz.kara)
        agac = cKDTree(iz.xyz[idx])
        hucre = iz.hucre_km / 6371.0
        k, j = agac.query(iz.xyz[idx], k=9, distance_upper_bound=1.7 * hucre)
        n = idx.size
        satir, sutun = [], []
        for c in range(1, 9):
            ok = np.isfinite(k[:, c])
            satir.append(np.flatnonzero(ok))
            sutun.append(j[ok, c])
        satir, sutun = np.concatenate(satir), np.concatenate(sutun)
        A = sparse.csr_matrix((np.ones(satir.size), (satir, sutun)), shape=(n, n))
        derece = np.asarray(A.sum(axis=1)).ravel()
        derece[derece == 0] = 1
        # x <- 0,5 x + 0,5 komşu ortalaması. Kenarda (kıyıda) komşu az; denize sızma yok.
        self.M = (0.5 * sparse.identity(n) + 0.5 * sparse.diags(1 / derece) @ A).tocsr()
        self.idx = idx
        # adım başına varyans artışı ~0,5·(ortalama komşu uzaklığı²)/2 (2B, eksen başına)
        komsu_km2 = np.nanmean(np.where(np.isfinite(k[:, 1:]), k[:, 1:], np.nan) ** 2) * 6371.0**2
        self.tekrar = max(1, int(round(sigma_km**2 / (0.25 * komsu_km2))))

    def uygula(self, alan: np.ndarray) -> np.ndarray:
        x = alan[self.idx]
        for _ in range(self.tekrar):
            x = self.M @ x
        sonuc = np.zeros_like(alan)
        sonuc[self.idx] = x
        return sonuc


def geri_sicrama(duz: Duzlestirici, asinma_m: np.ndarray) -> np.ndarray:
    return (RHO_C / RHO_M) * duz.uygula(asinma_m)
