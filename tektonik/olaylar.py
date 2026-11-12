"""Katman 2: olaydan kalınlaşmaya ve yükselmeye.

Kural tabanlı, kütle korunumlu. Bir çarpışmada birim boy başına kuşağa giren
kabuk hacmi = yakınsama hızı × kabuk kalınlığı (m²/yıl). Bu hacim bir profil
boyunca dağıtılır; kalınlığı üst sınıra varan düğüm fazlasını arkadaki
platoya devreder. Yüzey yükselmesi Airy ile kalınlaşmanın (1 − ρc/ρm)
katıdır (arastirma/02, 03). Bugünkü konumlarda çalışır; blokların geriye
sürülmesi aşama 4'ün işi.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .izgara import YARICAP_M, Izgara, _lonlat_xyz

RHO_C = 2800.0
RHO_M = 3300.0
AIRY = 1.0 - RHO_C / RHO_M  # 0,152: birim kalınlaşma başına yüzey yükselmesi
H0_M = 35_000.0  # normal kıta kabuğu


def isaretli_uzaklik_km(iz: Izgara, cizgi_lonlat: np.ndarray, secim: np.ndarray) -> np.ndarray:
    """Seçili düğümlerin kırık büyük daire çizgisine işaretli uzaklığı (km).

    Pozitif: çizgi yönüne bakınca sol taraf.
    """
    p = iz.xyz[secim]
    v = _lonlat_xyz(cizgi_lonlat[:, 0], cizgi_lonlat[:, 1])
    en_iyi = np.full(p.shape[0], np.inf)
    isaret = np.ones(p.shape[0])
    for a, b in zip(v[:-1], v[1:]):
        nrm = np.cross(a, b)
        nrm /= np.linalg.norm(nrm)
        s = p @ nrm  # sin(daireye açısal uzaklık), sol taraf pozitif
        ayak = p - np.outer(s, nrm)
        ayak /= np.linalg.norm(ayak, axis=1, keepdims=True)
        # ayak a..b yayında mı
        ab = np.arccos(np.clip(a @ b, -1, 1))
        ia = np.arccos(np.clip(ayak @ a, -1, 1))
        ib = np.arccos(np.clip(ayak @ b, -1, 1))
        icinde = np.abs(ia + ib - ab) < 1e-9 + 1e-6 * ab
        d = np.where(
            icinde,
            np.abs(np.arcsin(np.clip(s, -1, 1))),
            np.minimum(np.arccos(np.clip(p @ a, -1, 1)), np.arccos(np.clip(p @ b, -1, 1))),
        )
        daha = d < en_iyi
        en_iyi = np.where(daha, d, en_iyi)
        isaret = np.where(daha, np.sign(s + 1e-15), isaret)
    return en_iyi * isaret * YARICAP_M / 1e3


@dataclass
class Carpisma:
    ad: str
    cephe: np.ndarray  # [K, 2] lon, lat; dikiş hattı
    ust_sol: bool  # True: çizgi yönüne göre sol taraf üst levha (yükselen)
    baslangic_ma: float  # kaç milyon yıl önce başladı
    bitis_ma: float = 0.0  # 0 = sürüyor
    hiz_cm_yil: float = 4.0
    kusak_km: float = 250.0  # ana kuşak genişliği (üst levha tarafı)
    on_kusak_km: float = 60.0  # alt levha tarafındaki kıvrım bindirme kuşağı
    plato_km: float = 600.0  # kuşağın arkasında plato bölgesi
    yan_sonum_km: float = 300.0  # cephe uçlarında sönüm
    kusak_hmax_m: float = 65_000.0
    plato_hmax_m: float = 45_000.0
    plato_azami_m_yil: float = 5e-3  # platoda düğüm başına en büyük kalınlaşma hızı
    uzak_km: tuple[float, float] = (1500.0, 2500.0)
    uzak_orani: float = 0.0
    uzak_gecikme_myr: float = 15.0
    plato_maske: np.ndarray | None = None  # [N] bool ya da 0..1 ağırlık; verilirse plato bölgesi uzaklık bandı yerine bu
    plato_orani: float = 0.0  # yaklaşmanın doğrudan platoda dağılan payı (yaygın kısalma)
    kusak_k_carpani: float = 1.0  # kuşak çekirdeğinde aşınabilirlik çarpanı (metamorfik çekirdek daha sert)
    _geo: dict = field(default_factory=dict, repr=False)

    def _uzaklik(self, iz: Izgara) -> tuple[np.ndarray, np.ndarray]:
        """Kara düğümleri için cepheye işaretli uzaklık (üst levha +) ve boyuna sönüm."""
        sec = iz.kara
        d = isaretli_uzaklik_km(iz, self.cephe, sec)
        if not self.ust_sol:
            d = -d
        # cephe uçlarından uzaklık (boyuna sönüm)
        uc = _lonlat_xyz(self.cephe[[0, -1], 0], self.cephe[[0, -1], 1])
        p = iz.xyz[sec]
        # cephe boyunca konum: uçlara uzaklık yerine çizgiye en yakın noktanın uca uzaklığı
        # yaklaşım: uçlara düz uzaklık, kuşak genişliği ölçeğinde
        d_uc = np.minimum(np.arccos(np.clip(p @ uc[0], -1, 1)), np.arccos(np.clip(p @ uc[1], -1, 1))) * YARICAP_M / 1e3
        boy = np.ones_like(d)
        # uçların dışına taşan bölge: uca uzaklık > |d| ise uç ötesindedir
        disari = d_uc < np.abs(d) * 0.999
        boy = np.where(disari, np.exp(-((d_uc / self.yan_sonum_km) ** 2)), 1.0)
        return d, boy

    def hazirla(self, iz: Izgara, gurultu: np.ndarray | None = None) -> None:
        sec = iz.kara
        d, boy = self._uzaklik(iz)

        # ana kuşak profili: alt levha tarafında dar ön kuşak, üst tarafta tepe ~0,35 W'da
        W, F = self.kusak_km, self.on_kusak_km
        x = d
        kusak = np.where(
            x >= 0,
            np.exp(-0.5 * ((x - 0.35 * W) / (0.3 * W)) ** 2),
            np.exp(-0.5 * ((x - 0.35 * W) / (0.3 * W)) ** 2) * np.exp(-((-x / F) ** 2)),
        )
        kusak = np.where(x > 1.2 * W, kusak * np.exp(-((x - 1.2 * W) / (0.2 * W)) ** 2), kusak)
        if gurultu is not None:
            kusak = kusak * np.clip(1.0 + 0.35 * gurultu[sec], 0.3, 2.0)
        plato = ((x > 0.6 * W) & (x < W + self.plato_km)).astype(float)
        if self.plato_km > 0:
            plato *= np.clip((W + self.plato_km - x) / (0.25 * self.plato_km), 0, 1)
        if self.plato_maske is not None:
            # sahibin çizdiği plato: çokgen içi, kuşağın kendisi hariç
            plato = self.plato_maske[sec].astype(float) * (np.abs(x) > 0.6 * W)
        uzak = ((x > self.uzak_km[0]) & (x < self.uzak_km[1])).astype(float)
        if gurultu is not None:
            uzak *= np.clip(gurultu[sec], 0, None)

        alan = iz.alan_m2
        # birim boy başına normalize: kuşak profili integrali (m) = 1 kabul edilir
        # profil x yönünde tepe genişliği ~0,3W*sqrt(2pi); düğüm alanı / ortalama boy ile
        integral_m = 0.3 * W * 1e3 * np.sqrt(2 * np.pi)
        self._geo = dict(
            idx=np.flatnonzero(sec), d=d, boy=boy, kusak=kusak / integral_m,
            plato=plato, uzak=uzak, alan=alan,
        )

    def k_carpani(self, iz: Izgara) -> np.ndarray:
        """Aşınabilirlik çarpanı alanı: kuşak çekirdeğinde kusak_k_carpani, dışında 1."""
        c = np.ones(iz.n)
        if self.kusak_k_carpani == 1.0 or not self._geo:
            return c
        g = self._geo
        w = g["kusak"] / max(g["kusak"].max(), 1e-30) * g["boy"]
        c[g["idx"]] = 1.0 - (1.0 - self.kusak_k_carpani) * np.clip(w, 0, 1)
        return c

    def etkin(self, ma: float) -> float:
        """0..1: olayın bu andaki şiddeti (başta 2 milyon yılda açılır, sonda 2 milyon yılda söner)."""
        if ma > self.baslangic_ma or ma < self.bitis_ma - 2.0:
            return 0.0
        a = np.clip((self.baslangic_ma - ma) / 2.0, 0, 1)
        b = np.clip((ma - (self.bitis_ma - 2.0)) / 2.0, 0, 1) if self.bitis_ma > 0 else 1.0
        return float(min(a, b))

    def kalinlasma(self, ma: float, h: np.ndarray) -> np.ndarray:
        """Bu anda kalınlaşma hızı (m/yıl), seçili düğümler için. h: tüm düğümlerin kabuk kalınlığı."""
        g = self._geo
        e = self.etkin(ma)
        r = np.zeros(g["idx"].size)
        if e == 0.0:
            return r
        akı = self.hiz_cm_yil / 100.0 * H0_M * e  # m²/yıl, birim boy başına
        hh = h[g["idx"]]
        tum = akı * g["kusak"] * g["boy"]
        istek = (1.0 - self.plato_orani) * tum
        # kuşakta doygunluk: kalınlık üst sınıra yaklaştıkça kabul azalır
        kabul = np.clip((self.kusak_hmax_m - hh) / 5000.0, 0, 1)
        r = istek * kabul
        fazla_hacim = float(np.sum(istek * (1 - kabul)) * g["alan"])  # m³/yıl
        fazla_hacim += self.plato_orani * float(np.sum(tum) * g["alan"])
        if fazla_hacim > 0 and (self.plato_km > 0 or self.plato_maske is not None):
            pk = g["plato"] * np.clip((self.plato_hmax_m - hh) / 3000.0, 0, 1)
            if self.plato_maske is None:
                pk = pk * g["boy"]
            top = float(pk.sum() * g["alan"])
            if top > 0:
                # düğüm başına üst sınır: plato dolunca fazla malzeme birkaç boş
                # düğüme yığılmasın (yanal kaçış / dalma ile sistemden çıkar)
                ek = np.minimum(fazla_hacim * pk / top, self.plato_azami_m_yil)
                r = r + ek
        if self.uzak_orani > 0 and (self.baslangic_ma - ma) > self.uzak_gecikme_myr:
            uz = g["uzak"] * g["boy"]
            top = float(uz.sum() * g["alan"])
            if top > 0:
                # uzak etki: toplam akının küçük bir payı, kuşaktan bağımsız ek
                toplam_akı = float(np.sum(istek) * g["alan"])
                r = r + self.uzak_orani * toplam_akı * uz / top
        return r


@dataclass
class BlokSikismasi:
    """Bir blok iki levha arasında sıkışıp bütünüyle kalınlaşıyor (Yeni Gine,
    Tayvan benzeri; arastirma/07). Kalınlaşma hızı = hız × H0 / blok genişliği,
    blok içinde düzensiz dağılır, kıyıya doğru söner."""

    ad: str
    blok_maske: np.ndarray  # [N] bool
    baslangic_ma: float
    bitis_ma: float = 0.0
    hiz_cm_yil: float = 3.0
    genislik_km: float = 600.0
    hmax_m: float = 62_000.0
    _geo: dict = field(default_factory=dict, repr=False)

    def hazirla(self, iz: Izgara, gurultu: np.ndarray | None = None) -> None:
        sec = iz.kara
        m = self.blok_maske[sec].astype(float)
        if gurultu is not None:
            m *= np.clip(1.0 + 0.4 * gurultu[sec], 0.3, 2.0)
        self._geo = dict(idx=np.flatnonzero(sec), m=m)

    def etkin(self, ma: float) -> float:
        return Carpisma.etkin(self, ma)  # aynı açılma ve sönme kuralı

    def kalinlasma(self, ma: float, h: np.ndarray) -> np.ndarray:
        g = self._geo
        e = self.etkin(ma)
        if e == 0.0:
            return np.zeros(g["idx"].size)
        hiz = self.hiz_cm_yil / 100.0 * H0_M / (self.genislik_km * 1e3) * e
        kabul = np.clip((self.hmax_m - h[g["idx"]]) / 5000.0, 0, 1)
        return hiz * g["m"] * kabul


@dataclass
class SinirCarpismasi(Carpisma):
    """Çizgi yerine iki bloğun ortak sınırından tanımlanan çarpışma (rastgele mod).

    ust_blok, alt_blok: [N] bool. Uzaklık: üst blok düğümlerinde alt bloğa (+),
    diğer kara düğümlerinde üst bloğa (−). Temas noktalarından uzaklaşan sınır
    uçlarında kuşak yan_sonum_km ölçeğinde söner."""

    ust_blok: np.ndarray | None = None
    alt_blok: np.ndarray | None = None

    def _uzaklik(self, iz: Izgara) -> tuple[np.ndarray, np.ndarray]:
        from scipy.spatial import cKDTree

        sec = iz.kara
        p = iz.xyz[sec]
        km = YARICAP_M / 1e3
        d_alt, _ = cKDTree(iz.xyz[self.alt_blok]).query(p)
        d_ust, _ = cKDTree(iz.xyz[self.ust_blok]).query(p)
        ust = self.ust_blok[sec]
        d = np.where(ust, d_alt, -d_ust) * km
        # temas: alt bloğa bir buçuk hücreden yakın üst düğümler
        h = iz.hucre_km * 1.6
        temas = np.flatnonzero(sec)[ust & (d_alt * km < h)]
        if temas.size == 0:
            return d, np.zeros_like(d)
        d_t, _ = cKDTree(iz.xyz[temas]).query(p)
        fark = np.clip(d_t * km - np.abs(d) - h, 0, None)
        boy = np.exp(-((fark / self.yan_sonum_km) ** 2))
        return d, boy
