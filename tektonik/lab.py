"""Çarpışma laboratuvarı: ileri zamanlı, kıyısı serbest, etki tepkili harita görünümü simülasyonu.

Tek bir ilerleyen alan var: kabuk kalınlığı S (kıta yaklaşık 35 km, okyanus 7 km; çökeller de S'ye
katılır). Her adımda:
  1. Hız: ince viskoz levha (levha.LevhaCozucu). Gelen bloğun iç kısmı sabit hızla sürülür, karşı
     bloğun iç kısmı durur; arada kıta kendi dayanımıyla akar. Okyanus zayıftır: okyanusta yakınsama
     dalma demektir, kabuk yok olur, kalınlaşma olmaz.
  2. Taşıma: S ve levha etiketi hız alanıyla yarı Lagrange taşınır; kıyılar S'den doğar.
  3. Kalınlaşma: kıtada dS = −S ∇·u.
  4. Alt kabuk akışı: kalın ve sıcak kabukta doğrusal olmayan yayılma ∇·(κ(S)∇S); κ, S eşiği aşınca
     büyür. Platonun düz tepesi ve dik kenarı buradan doğar (Clark ve Royden 2000).
  5. Yüzey: elastik levha bükülmesiyle izostazi (FFT). Fazla kabuk yük; levha geniş bölgeye eğilir,
     yükün önünde çökme havzası ve ötesinde kabarma kendiliğinden çıkar.
  6. Aşınma: fastscapelib akarsu aşınması (m 0,5, n 1); deniz taban düzeyi 0. Aşınan kabuk S'den düşer.
  7. Çökelme: karadaki kapalı çukurlar o adımda aşınan hacimle (orantılı) dolar; ön havza düz ovaya döner.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import fastscapelib as fs
import numpy as np
from scipy import ndimage
from skimage.morphology import reconstruction

from .levha import BUY, SANIYE_YIL, Duzlem, LevhaCozucu

RHO_C, RHO_M, G = 2800.0, 3300.0, 9.81


@dataclass
class LabAyar:
    h_km: float = 15.0
    dt_myr: float = 0.25
    eta0: float = 3e22
    sert_gelen: float = 3.0  # gelen blok kalkan gibi daha dayanıklı (Hindistan benzeri)
    okyanus: float = 0.2
    n: float = 3.0
    cek_gelen_km: float = 500.0
    cek_sabit_km: float = 450.0
    S_ref_km: float = 35.0
    serbest_bord_m: float = 300.0  # S_ref'teki kıtanın yüksekliği
    okyanus_derin_m: float = -4000.0
    Te_km: float = 40.0
    kappa_max: float = 8e3  # m²/yıl, sıcak kalın kabukta
    kappa_min: float = 30.0
    S_akis_km: float = 55.0  # alt kabuk akışının açıldığı kalınlık
    S_ust_km: float = 80.0
    K: float = 2e-7
    m: float = 0.5
    nsp: float = 1.0
    cokelme: float = 0.7  # aşınan hacmin karadaki çukurlara giden payı
    tohum: int = 1
    carpisma_sonrasi_hiz: float = 0.5  # temas sonrası hız çarpanı (Hindistan çarpışmadan sonra yavaşladı)


@dataclass
class LabDurum:
    S: np.ndarray
    etiket: np.ndarray  # 1 gelen levha, 0 sabit levha
    z: np.ndarray
    u: np.ndarray
    v: np.ndarray
    ma: float
    gunluk: list = field(default_factory=list)


def acik_okyanus(z):
    """Alan kenarına bağlı deniz altı bölge (açık okyanus); iç göller hariç."""
    deniz = z < 0
    et, n = ndimage.label(deniz)
    kenar = np.unique(np.r_[et[0, :], et[-1, :], et[:, 0], et[:, -1]])
    kenar = kenar[kenar > 0]
    return np.isin(et, kenar)


def bukulme_suzgeci(ny, nx, h, Te_km):
    E, nu = 1e11, 0.25
    D = E * (Te_km * 1e3) ** 3 / (12 * (1 - nu ** 2))
    ky = 2 * np.pi * np.fft.fftfreq(ny, h)
    kx = 2 * np.pi * np.fft.rfftfreq(nx, h)
    k4 = (kx[None, :] ** 2 + ky[:, None] ** 2) ** 2
    return RHO_C / (RHO_M + D * k4 / G)  # w_k / S'_k


def yuzey(S, kita, suzgec, a: LabAyar):
    """Bükülmeli izostazi: S' = S − S_ref yükü; çökme w; yükselti S' − w + serbest bord. Okyanus sabit derinlik."""
    Sp = np.where(kita, S - a.S_ref_km * 1e3, 0.0)
    w_f = np.fft.irfft2(np.fft.rfft2(Sp) * suzgec, s=S.shape)  # elastik levha çökmesi
    w_a = RHO_C / RHO_M * Sp  # yerel (Airy) kök
    # Kalınlaşma yerel olarak Airy dengesinde; bükülme yalnız bölgesel farkı (ön havza çukuru ve
    # yükün altındaki eksik kök) uzun dalga boyunda ekler. Kısa dalga boyunda elastik destek, dar
    # kalınlaşmayı onlarca km yükseğe çıkarıyordu (fiziksel değil: kalınlaşma yüzeye konan yük değil).
    fark = ndimage.gaussian_filter(w_a - w_f, 60.0 / a.h_km)
    z_k = Sp - w_a + fark + a.serbest_bord_m
    w = w_f
    # okyanus: kıta kenarından uzaklaştıkça derinleşir (kıta yamacı yaklaşık 100 km)
    d = ndimage.distance_transform_edt(~kita) * a.h_km
    z_o = a.okyanus_derin_m * np.clip(d / 100.0, 0, 1) - w * 0.0
    return np.where(kita, z_k, np.minimum(z_o, z_k))


class Lab:
    def __init__(self, S0: np.ndarray, etiket0: np.ndarray, hiz_gelen: tuple[float, float], bas_ma: float,
                 ayar: LabAyar | None = None):
        self.a = a = ayar or LabAyar()
        ny, nx = S0.shape
        self.ny, self.nx = ny, nx
        h = a.h_km * 1e3
        self.h = h
        self.dz = Duzlem(0.0, 0.0, h, np.arange(nx) * h, -np.arange(ny) * h, np.zeros((ny, nx)), np.zeros((ny, nx)),
                         np.ones((ny, nx), bool))
        self.coz = LevhaCozucu(self.dz)
        self.suzgec = bukulme_suzgeci(ny, nx, h, a.Te_km)
        self.v_gelen = np.array(hiz_gelen) / 100 / SANIYE_YIL  # (doğu, kuzey) m/s
        # ızgara nesnesi saklanmalı: yalnız akış grafiği tutarsa çöp toplanıp çöküyor
        self.grid = fs.RasterGrid([ny, nx], [h, h], fs.NodeStatus.FIXED_VALUE)
        self.router = fs.FlowGraph(self.grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
        self.eroder = fs.SPLEroder(self.router, a.K, a.m, a.nsp, 1e-4)
        kita = S0 > 20e3
        self.temas_ma = None
        self.kenar_S = (S0[0, :].astype(float).copy(), S0[-1, :].astype(float).copy(), S0[:, 0].astype(float).copy(), S0[:, -1].astype(float).copy())
        self.kenar_L = (etiket0[0, :].astype(float).copy(), etiket0[-1, :].astype(float).copy(), etiket0[:, 0].astype(float).copy(), etiket0[:, -1].astype(float).copy())
        self.durum = LabDurum(S0.astype(float).copy(), etiket0.astype(float).copy(),
                              yuzey(S0, kita, self.suzgec, a), np.zeros((ny, nx)), np.zeros((ny, nx)), bas_ma)

    def adim(self):
        a, d = self.a, self.durum
        S, L = d.S, d.etiket
        ny, nx, h = self.ny, self.nx, self.h
        dt_s = a.dt_myr * 1e6 * SANIYE_YIL
        kita = S > 20e3
        gelen = L > 0.5
        # --- hız ---
        dis_sabit_kita = ndimage.distance_transform_edt(~(kita & ~gelen)) * a.h_km
        dis_gelen_kita = ndimage.distance_transform_edt(~(kita & gelen)) * a.h_km
        cek_g = kita & gelen & (dis_sabit_kita > a.cek_gelen_km)
        cek_s = kita & ~gelen & (dis_gelen_kita > a.cek_sabit_km)
        sabit = cek_g | cek_s
        sabit[[0, -1], :] = True; sabit[:, [0, -1]] = True
        # kıtalar temas edince (aradaki en kısa uzaklık iki hücreden az) gelen yavaşlar
        gk = kita & gelen
        et_g, n_g = ndimage.label(gk)
        if n_g > 1:  # temas yalnız gelen kıtanın ana gövdesi için
            gk = et_g == (1 + np.argmax(ndimage.sum(gk, et_g, range(1, n_g + 1))))
        if self.temas_ma is None and gk.any() and dis_sabit_kita[gk].min() < 2.5 * a.h_km:
            self.temas_ma = d.ma
        carp = a.carpisma_sonrasi_hiz if self.temas_ma is not None else 1.0
        u0 = np.where(gelen, self.v_gelen[0] * carp, 0.0)
        v0 = np.where(gelen, self.v_gelen[1] * carp, 0.0)
        eta_t = np.where(kita, a.eta0 * np.where(gelen, a.sert_gelen, 1.0), a.eta0 * a.okyanus)
        # kalın sıcak kabuk zayıflar
        eta_t = eta_t * np.exp(-np.clip(S - a.S_ref_km * 1e3, 0, None) / 15e3)
        _, (rk, ck) = ndimage.distance_transform_edt(~kita, return_indices=True)
        Sg = S[rk, ck] if kita.any() else S
        eta = eta_t.copy()
        for _ in range(3):
            u, v = self.coz.coz(eta, Sg, sabit, u0, v0)
            ekk, eE = self.coz.gerinim(u, v)
            eta = np.clip(eta_t * (np.maximum(eE, 1e-18) / 1e-15) ** (1 / a.n - 1), 1e19, 1e25)
        # --- taşıma ---
        sn = dt_s / h
        rr, cc = np.mgrid[0:ny, 0:nx].astype(float)
        r0, c0 = rr + v * sn, cc - u * sn
        S = ndimage.map_coordinates(S, [r0, c0], order=1, mode="nearest")
        L = ndimage.map_coordinates(L, [r0, c0], order=1, mode="nearest")
        # kenarlar: alandan giren malzeme başlangıçtaki kenar değerini taşır (sivrilik birikmesin)
        S[0, :], S[-1, :], S[:, 0], S[:, -1] = self.kenar_S
        L[0, :], L[-1, :], L[:, 0], L[:, -1] = self.kenar_L
        kita = S > 20e3
        # --- kalınlaşma (yalnız kıtada; okyanusta dalma) ---
        dS = np.where(kita, -S * ekk * dt_s, 0.0)
        S = S + np.clip(dS, -0.2 * S, 15e3)
        # --- alt kabuk akışı (alt adımlı, açık) ---
        kap = a.kappa_min + a.kappa_max / (1 + np.exp(-(S - a.S_akis_km * 1e3) / 4e3))
        kap = np.where(kita, kap, 0.0)
        dt_yil = a.dt_myr * 1e6
        alt = int(np.ceil(dt_yil * kap.max() * 4 / (h * h))) + 1
        dta = dt_yil / alt
        for _ in range(alt):
            kx = 0.5 * (kap[:, 1:] + kap[:, :-1]); ky = 0.5 * (kap[1:, :] + kap[:-1, :])
            fx = kx * (S[:, 1:] - S[:, :-1]) / h; fy = ky * (S[1:, :] - S[:-1, :]) / h
            dv = np.zeros_like(S)
            dv[:, :-1] += fx; dv[:, 1:] -= fx; dv[:-1, :] += fy; dv[1:, :] -= fy
            S = S + dta * dv / h
        S = np.clip(S, 5e3, a.S_ust_km * 1e3)
        kita = S > 20e3
        # --- yüzey ve aşınma ---
        z = yuzey(S, kita, self.suzgec, a)
        kara = ~acik_okyanus(z)  # iç göller de karanın parçası: nehirler onlara akar, dolarlar
        zr = np.ascontiguousarray(np.where(kara, z, 0.0), dtype=np.float64).copy()  # deniz taban düzeyi 0
        self.router.update_routes(zr)
        A = np.asarray(self.router.accumulate(1.0))
        e = np.asarray(self.eroder.erode(zr, A, dt_yil)).reshape(S.shape)
        e = np.where(kara, np.clip(e, 0, None), 0.0)
        S = S - e
        hacim = float(e.sum())
        # --- çökelme: açık okyanusa bağlı olmayan bütün çukurlar (iç göller dahil) dolar ---
        z = yuzey(S, S > 20e3, self.suzgec, a)
        acik = acik_okyanus(z)
        tohum = np.where(acik, np.maximum(z, 0.0), z.max() + 1.0)
        maske = np.where(acik, np.maximum(z, 0.0), z)
        dolu = reconstruction(tohum, maske, method="erosion")
        cukur = np.where(~acik & (S > 15e3), np.clip(dolu - z, 0, None), 0.0)  # okyanus kabuğunda çökelme yok
        if cukur.sum() > 0 and hacim > 0:
            # çukurun izostatik derinleşmesi için yaklaşık 1/(1−ρc/ρm) kat malzeme gerekir; payı sınırlı
            gerek = cukur.sum() / (1 - RHO_C / RHO_M)
            oran = min(1.0, a.cokelme * hacim / gerek)
            S = S + cukur * oran / (1 - RHO_C / RHO_M)
        d.S, d.etiket, d.u, d.v = S, L, u, v
        d.z = yuzey(S, S > 20e3, self.suzgec, a)
        d.ma = round(d.ma - a.dt_myr, 6)
        kara = ~acik_okyanus(d.z)
        d.gunluk.append(dict(ma=d.ma, zmax=float(d.z.max()), Smax_km=float(S.max() / 1e3),
                             kara_orani=float(kara.mean()), asinma_km3=float(hacim * h * h / 1e9),
                             vmax_cm=float(np.hypot(u, v).max() * SANIYE_YIL * 100), temas_ma=self.temas_ma))
        return d
