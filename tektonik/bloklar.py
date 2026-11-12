"""Bugünkü kıtayı bloklara ayırma.

Dikiş hatları (kırık büyük daire çizgileri) kara grafiğini keser; kalan
bağlı bileşenler tohum noktalarıyla adlandırılır. Tohumsuz küçük parçalar
(adalar) en yakın adlı bloğa katılır.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

from .izgara import Izgara, _lonlat_xyz
from .olaylar import isaretli_uzaklik_km


def kara_komsuluk(iz: Izgara, idx: np.ndarray) -> sparse.csr_matrix:
    agac = cKDTree(iz.xyz[idx])
    k, j = agac.query(iz.xyz[idx], k=9, distance_upper_bound=1.7 * iz.hucre_km / 6371.0)
    satir, sutun = [], []
    for c in range(1, 9):
        ok = np.isfinite(k[:, c])
        satir.append(np.flatnonzero(ok))
        sutun.append(j[ok, c])
    satir, sutun = np.concatenate(satir), np.concatenate(sutun)
    n = idx.size
    return sparse.csr_matrix((np.ones(satir.size, dtype=np.int8), (satir, sutun)), shape=(n, n))


@dataclass
class Bloklar:
    adlar: list[str]
    etiket: np.ndarray  # [N] blok sırası, kara dışı -1
    sabit: str

    def maske(self, ad: str) -> np.ndarray:
        return self.etiket == self.adlar.index(ad)


def bloklara_ayir(iz: Izgara, senaryo: dict) -> Bloklar:
    idx = np.flatnonzero(iz.kara)
    A = kara_komsuluk(iz, idx)
    kesik = np.zeros(idx.size, bool)
    for d in senaryo.get("dikisler", []):
        u = isaretli_uzaklik_km(iz, np.array(d["cizgi"], float), iz.kara)
        kesik |= np.abs(u) < 0.8 * iz.hucre_km
    tut = ~kesik
    A2 = A[tut][:, tut]
    nb, lab = connected_components(A2, directed=False)
    tam = np.full(idx.size, -1)
    tam[tut] = lab
    # kesik düğümler: kesilmemiş en yakın komşunun bileşeni (aynı tarafta kalır)
    agac = cKDTree(iz.xyz[idx[tut]])
    _, j = agac.query(iz.xyz[idx[kesik]])
    tam[kesik] = lab[j]

    adlar = list(senaryo["bloklar"].keys())
    bilesen_ad = {}
    for ad, b in senaryo["bloklar"].items():
        p = _lonlat_xyz(np.array(float(b["tohum"][0])), np.array(float(b["tohum"][1])))
        i = int(np.argmax(iz.xyz[idx] @ p))
        bilesen_ad[tam[i]] = adlar.index(ad)
    etiket_k = np.array([bilesen_ad.get(c, -1) for c in tam])
    # adsız parçalar: en yakın adlı düğümün bloğu
    adsiz = etiket_k < 0
    if adsiz.any():
        agac = cKDTree(iz.xyz[idx[~adsiz]])
        _, j = agac.query(iz.xyz[idx[adsiz]])
        etiket_k[adsiz] = etiket_k[~adsiz][j]
    etiket = np.full(iz.n, -1)
    etiket[idx] = etiket_k
    sabit = next(ad for ad, b in senaryo["bloklar"].items() if b.get("sabit"))
    return Bloklar(adlar, etiket, sabit)
