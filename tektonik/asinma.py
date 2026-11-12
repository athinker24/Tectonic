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
    """Yükselme alanını (m/yıl) sure_yil boyunca uygula ve aşındır.

    yukselme: sabit dizi ya da zaman (yıl) -> dizi işlevi. Yalnız kara
    düğümlerinde etkilidir; kıyı ve deniz düğümleri 0 m kalır.
    yagis: göreli akış ağırlığı (1 = ortalama); None ise her yerde 1.
    """
    ayar = ayar or AsinmaAyar()
    fg = fs.FlowGraph(iz.grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
    # Fastscapelib 0.3.0 HEALPix ızgarasında komşu uzaklıkları metre değil
    # radyan (birim küre) dönüyor; düğüm alanları ise m². Eğim bu yüzden R kat
    # büyük hesaplanıyor. Düzeltme: K_etkin = K / R^n. 12 Kasım 2026'da eğimli
    # düzlem deneyiyle doğrulandı (testler/test_asinma.py).
    k_etkin = np.asarray(ayar.k, dtype=float) / YARICAP_M**ayar.n
    k_etkin = float(k_etkin) if k_etkin.ndim == 0 else k_etkin
    spl = fs.SPLEroder(fg, k_etkin, ayar.m, ayar.n, ayar.tolerans)

    z = np.zeros(iz.n) if z0 is None else z0.astype(float).copy()
    if z0 is None:
        # düz yüzeyde akış yönü tanımsız kalmasın diye çok küçük pürüz
        z[iz.kara] = np.random.default_rng(0).random(int(iz.kara.sum()))
    z[~iz.kara] = 0.0
    kaynak = 1.0 if yagis is None else yagis.astype(float)

    sonuc = AsinmaSonuc(z=z, drenaj_m2=np.zeros(iz.n))
    adim = int(round(sure_yil / ayar.dt_yil))
    sonraki_kare = 0.0
    A = None
    for i in range(adim):
        t = i * ayar.dt_yil
        u = yukselme(t) if callable(yukselme) else yukselme
        z[iz.kara] += u[iz.kara] * ayar.dt_yil
        fg.update_routes(z)
        A = fg.accumulate(kaynak)
        z -= spl.erode(z, A, ayar.dt_yil)
        z[~iz.kara] = 0.0
        if kare_araligi_yil is not None and t + ayar.dt_yil >= sonraki_kare:
            sonuc.kareler.append(z.astype(np.float32).copy())
            sonuc.kare_zamani_yil.append(t + ayar.dt_yil)
            sonraki_kare += kare_araligi_yil
    sonuc.z = z
    sonuc.drenaj_m2 = np.asarray(A) if A is not None else sonuc.drenaj_m2
    return sonuc
