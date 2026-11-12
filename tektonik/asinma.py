"""Katman 3: aşınma çekirdeği.

Akarsu güç yasası (E = K A^m S^n), Fastscapelib'in örtük çözücüsüyle.
Kıyı düğümleri sabit (0 m) taban seviyesidir.

Yamaç difüzyonu bilerek yok: 12,7 km hücrede, literatürdeki en büyük
difüzyon katsayısıyla (0,036 m²/yıl) bile D·dt/dx² ≈ 2e-5 kalıyor, yani
bu ölçekte etkisiz (arastirma/13, 14).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import fastscapelib as fs
import numpy as np

from .izgara import YARICAP_M, Izgara


@dataclass
class AsinmaAyar:
    k: float | np.ndarray = 2e-6  # aşınma katsayısı (m = 0,5 için 1/yıl)
    m: float = 0.5
    n: float = 1.0
    dt_yil: float = 1e5
    tolerans: float = 1e-4


class Asindirici:
    """Adım adım aşınma. Her adımda akış yeniden yönlendirilir."""

    def __init__(self, iz: Izgara, ayar: AsinmaAyar | None = None, yagis: np.ndarray | None = None):
        self.iz = iz
        self.ayar = ayar or AsinmaAyar()
        self.fg = fs.FlowGraph(iz.grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
        # Fastscapelib 0.3.0 HEALPix ızgarasında komşu uzaklıkları metre değil
        # radyan (birim küre) dönüyor; düğüm alanları ise m². Eğim bu yüzden R kat
        # büyük hesaplanıyor. Düzeltme: K_etkin = K / R^n. 12 Kasım 2026'da eğimli
        # düzlem deneyiyle doğrulandı (testler/test_asinma.py).
        k = np.asarray(self.ayar.k, dtype=float) / YARICAP_M ** self.ayar.n
        self.spl = fs.SPLEroder(self.fg, float(k) if k.ndim == 0 else k, self.ayar.m, self.ayar.n, self.ayar.tolerans)
        self.kaynak = 1.0 if yagis is None else yagis.astype(float)
        self.drenaj_m2 = np.zeros(iz.n)

    def adim(self, z: np.ndarray, dt: float | None = None) -> np.ndarray:
        """z'yi yerinde aşındırır, aşınma miktarını (m) döner."""
        dt = self.ayar.dt_yil if dt is None else dt
        self.fg.update_routes(z)
        self.drenaj_m2 = np.asarray(self.fg.accumulate(self.kaynak))
        e = np.asarray(self.spl.erode(z, self.drenaj_m2, dt))
        z -= e
        z[~self.iz.kara] = 0.0
        e = e.copy()
        e[~self.iz.kara] = 0.0
        return e


@dataclass
class AsinmaSonuc:
    z: np.ndarray
    drenaj_m2: np.ndarray
    kareler: list[np.ndarray] = field(default_factory=list)
    kare_zamani_yil: list[float] = field(default_factory=list)


def asindir(
    iz: Izgara,
    yukselme: Callable[[float], np.ndarray] | np.ndarray,
    sure_yil: float,
    ayar: AsinmaAyar | None = None,
    z0: np.ndarray | None = None,
    yagis: np.ndarray | None = None,
    kare_araligi_yil: float | None = None,
) -> AsinmaSonuc:
    """Yükselme alanını (m/yıl) sure_yil boyunca uygula ve aşındır (izostazisiz basit yol)."""
    ayar = ayar or AsinmaAyar()
    a = Asindirici(iz, ayar, yagis)
    z = np.zeros(iz.n) if z0 is None else z0.astype(float).copy()
    if z0 is None:
        z[iz.kara] = np.random.default_rng(0).random(int(iz.kara.sum()))
    z[~iz.kara] = 0.0
    sonuc = AsinmaSonuc(z=z, drenaj_m2=np.zeros(iz.n))
    adim = int(round(sure_yil / ayar.dt_yil))
    sonraki = 0.0
    for i in range(adim):
        t = i * ayar.dt_yil
        u = yukselme(t) if callable(yukselme) else yukselme
        z[iz.kara] += u[iz.kara] * ayar.dt_yil
        a.adim(z)
        if kare_araligi_yil is not None and t + ayar.dt_yil >= sonraki:
            sonuc.kareler.append(z.astype(np.float32).copy())
            sonuc.kare_zamani_yil.append(t + ayar.dt_yil)
            sonraki += kare_araligi_yil
    sonuc.z = z
    sonuc.drenaj_m2 = a.drenaj_m2
    return sonuc
