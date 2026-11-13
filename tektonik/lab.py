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
    yagis: bool = True  # orografik yağış (levha_model.yagis_alani): ıslak cephe, kurak iç
    k_degiskenlik: float = 0.6  # ln K sapması (kayaç sertliği farkı)
    carpisma_sonrasi_hiz: float = 0.5  # temas sonrası hız çarpanı (Hindistan çarpışmadan sonra yavaşladı)
    sinir_zayif: float = 1.0  # levha sınırı fay kuşağının viskozite çarpanı (1 = yok); bindirme kuşağı
    sinir_km: float = 200.0  # fay kuşağının sınırdan iki yana genişliği
    gelen_sert: float = 1.0  # çok bloklu: hareketli blokların kıtası bu kat viskoz (Hindistan, Arabistan kalkanları)
    kita_dalma: float = 0.0  # kıta kabuğu dalması: kalınlaşmanın bu payı mantoya gider (Hindistan Asya için yaklaşık 0,5)
    sinir_tek_yan: bool = False  # True: fay kuşağı yalnız üstteki (sabit) levhada; gelen kıtanın önü kalınlaşmasın
    dikis_esik: float = 0.0  # dar okyanus şeridinin kapanması için adım başına en az kısalma (0,02: %2); 0 her yakınsamada
    yumusama_e0: float = 0.0  # >0: gerinim yumuşaması; birikmiş gerinim ε ile viskozite exp(−ε/e0) (fay yerelleşmesi)
    yumusama_min: float = 0.1  # yumuşamanın alt sınırı (viskozite çarpanı)
    iyilesme_myr: float = 20.0  # birikmiş gerinimin iyileşme süresi
    yay_uretim_m: float = 0.0  # >0: dalma batma magmatizması; tüketilen okyanus alanı başına eklenen kabuk (m), ör. 800
    yay_uzaklik_km: float = 200.0  # yayın hendekten (ilk kıta hücresinden) içeri uzaklığı
    yay_zayif: float = 1.0  # <1: etkin yayın altındaki sıcak kabuk zayıflar (en düşük viskozite çarpanı)
    iklim: bool = False  # enlem kuşakları (yağış çarpanı) ve kar çizgisi üstünde buzul aşınması; enlem gerekir
    buzul_k: float = 1.33e-6  # 1/yıl: kar çizgisinin 1500 m üstünde yaklaşık 2 mm/yıl aşınma (buzul testeresi)
    plastik_mpa: float = 0.0  # >0: derinlik ortalamalı akma gerilimi (MPa); η ≤ τy / (2 ε̇E) (fay davranışı)
    plastik_e: float = 1.0  # akma geriliminin yarıya indiği birikmiş gerinim (yumuşama yalnız akmada)
    plastik_min: float = 0.4  # akma geriliminin en düşük oranı
    tasima_kubik: bool = True  # sınırlı kübik taşıma (False: eski doğrusal, kıyıyı yayar)
    incelme_km: float = 0.0  # >0: incelen kıtada viskozite exp(−(S_ref−S)/incelme) düşer (yırtılma, Kızıldeniz); 0 kapalı
    kiyi_sizinti: bool = True  # alt kabuk akışı kıyıdan okyanusa geçebilir mi (False: kıta kenarında akı yok)


@dataclass
class LabDurum:
    S: np.ndarray
    etiket: np.ndarray  # 1 gelen levha, 0 sabit levha
    z: np.ndarray
    u: np.ndarray
    v: np.ndarray
    ma: float
    gunluk: list = field(default_factory=list)


def enlem_yagis(lat):
    """Enlemsel ortalama yağış çarpanı (yaklaşık): ekvator ıslak, dönence altı kurak (Hadley hücresi),
    orta enlem ıslak (kutup cephesi), kutuplar kurak. Kıta içi kuruma yagis_alani'nde ayrıca var."""
    e = np.abs(lat)
    return np.interp(e, [0, 10, 20, 27, 35, 45, 55, 65, 80, 90], [1.8, 1.6, 0.9, 0.35, 0.6, 1.1, 1.1, 0.7, 0.35, 0.3])


def kar_cizgisi(lat):
    """Buzul denge hattı yüksekliği (m), enleme göre yaklaşık: dönence altı kurak kuşakta en yüksek."""
    e = np.abs(lat)
    return np.interp(e, [0, 20, 30, 45, 60, 70, 90], [4800, 5500, 5000, 3000, 1200, 300, 0])


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
        self.eta_carpan = None  # sert bölgeler (kratonlar): kıtada viskozite çarpanı, ızgarada sabit
        # birikmiş gerinim; başlangıçta küçük rastgele miras zayıflıklar (yerelleşmenin çekirdekleri)
        _r = np.random.default_rng(a.tohum + 7)
        _e0 = a.yumusama_e0 if a.yumusama_e0 > 0 else 0.5 * a.plastik_e
        self.Eps = 0.2 * _e0 * np.abs(ndimage.gaussian_filter(_r.standard_normal(S0.shape), 1.5)) / 0.2
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
        rng = np.random.default_rng(a.tohum)
        g = ndimage.gaussian_filter(rng.standard_normal((ny, nx)), 60.0 / a.h_km); g /= g.std()
        g2 = ndimage.gaussian_filter(rng.standard_normal((ny, nx)), 15.0 / a.h_km); g2 /= g2.std()
        self.k_alan = a.K * np.exp(a.k_degiskenlik * (0.8 * g + 0.6 * g2))
        self.eroder = fs.SPLEroder(self.router, self.k_alan, a.m, a.nsp, 1e-4)
        kita = S0 > 20e3
        self.temas_ma = None
        self.etiket_derece = 1
        self.kenar_S = (S0[0, :].astype(float).copy(), S0[-1, :].astype(float).copy(), S0[:, 0].astype(float).copy(), S0[:, -1].astype(float).copy())
        self.kenar_L = (etiket0[0, :].astype(float).copy(), etiket0[-1, :].astype(float).copy(), etiket0[:, 0].astype(float).copy(), etiket0[:, -1].astype(float).copy())
        self.durum = LabDurum(S0.astype(float).copy(), etiket0.astype(float).copy(),
                              yuzey(S0, kita, self.suzgec, a), np.zeros((ny, nx)), np.zeros((ny, nx)), bas_ma)

    def _hiz(self, S, L, kita, d):
        a = self.a
        gelen = L > 0.5
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
        if self.eta_carpan is not None:
            eta_t = eta_t * np.where(kita, self.eta_carpan, 1.0)
        return sabit, u0, v0, eta_t

    def _yay(self, kita, ekk, u, v, dt_s):
        """Dalma batma magmatizması. İnce levhada okyanus zayıf olduğu için yakınsama hendekte değil okyanus
        şeridine yayılmış olarak görünür; bu yüzden yakınsayan her okyanus hücresinde tüketilen alan
        (−ε̇kk dt h²) dalıyor sayılır. Hücreden hareket yönünde (m) ilerlenir; ilk kıta hücresine göre okyanus
        yaklaşıyorsa ((u_okyanus − u_kıta)·m > 0) o kıta üstteki levhadır ve dalan alan × yay_uretim_m hacminde
        kabuk kıyıdan yay_uzaklik_km içeri eklenir (σ 30 km). Kıtayla birlikte giden okyanus yay doğurmaz.
        Okyanus içi yaylar şimdilik yok."""
        a = self.a
        ny, nx = kita.shape
        ek = np.zeros(kita.shape)
        hz = np.hypot(u, v)
        kay = ~kita & (ekk * dt_s < -1e-3) & (hz > 1.0 / 100 / SANIYE_YIL)
        if not kay.any():
            return ek
        ri, ci = np.nonzero(kay)
        hacim = -ekk[ri, ci] * dt_s * a.yay_uretim_m  # hücre alanına yayılmış kalınlık (m)
        dc, dr = u[ri, ci] / hz[ri, ci], -v[ri, ci] / hz[ri, ci]
        r, c = ri.astype(float), ci.astype(float)
        bulundu = np.zeros(len(ri), bool); gecerli = np.zeros(len(ri), bool)
        hr = np.zeros(len(ri)); hc = np.zeros(len(ri))
        for _ in range(int(3000.0 / a.h_km)):
            r += dr; c += dc
            ii = np.clip(np.rint(r).astype(int), 0, ny - 1); jj = np.clip(np.rint(c).astype(int), 0, nx - 1)
            yeni = ~bulundu & kita[ii, jj]
            if yeni.any():
                w = (u[ri, ci] - u[ii, jj]) * dc - (v[ri, ci] - v[ii, jj]) * dr
                gecerli |= yeni & (w > 1.0 / 100 / SANIYE_YIL)  # en az 1 cm/yıl yaklaşma (pasif kıyıda yay yok)
                hr[yeni] = r[yeni] + dr[yeni] * a.yay_uzaklik_km / a.h_km
                hc[yeni] = c[yeni] + dc[yeni] * a.yay_uzaklik_km / a.h_km
                bulundu |= yeni
            if bulundu.all():
                break
        if not gecerli.any():
            return ek
        ii = np.clip(np.rint(hr[gecerli]).astype(int), 0, ny - 1)
        jj = np.clip(np.rint(hc[gecerli]).astype(int), 0, nx - 1)
        np.add.at(ek, (ii, jj), hacim[gecerli])
        ek = ndimage.gaussian_filter(ek, max(30.0 / a.h_km, 0.5))
        ek = np.where(kita, ek, 0.0)
        # ısı: eklenen kalınlığın 5 milyon yıllık sönümlü toplamı
        isi = getattr(self, "yay_isi", None)
        self.yay_isi = (np.zeros(ek.shape) if isi is None else isi * np.exp(-a.dt_myr / 5.0)) + ek
        self.yay_top = getattr(self, "yay_top", 0.0) + ek  # birikmiş yay kabuğu (ızgarada; taşınmaz, tanı için)
        self.yay_hacim = getattr(self, "yay_hacim", 0.0) + float(ek.sum()) * self.h * self.h / 1e9
        return ek

    def adim(self):
        a, d = self.a, self.durum
        S, L = d.S, d.etiket
        ny, nx, h = self.ny, self.nx, self.h
        dt_s = a.dt_myr * 1e6 * SANIYE_YIL
        kita = S > 20e3
        gelen = L > 0.5
        # --- hız ---
        sabit, u0, v0, eta_t = self._hiz(S, L, kita, d)
        if a.yumusama_e0 > 0:
            eta_t = eta_t * np.where(kita, np.maximum(a.yumusama_min, np.exp(-self.Eps / a.yumusama_e0)), 1.0)
        if a.yay_zayif < 1.0 and getattr(self, "yay_isi", None) is not None:
            # son birkaç milyon yılda magma eklenen kabuk sıcak ve zayıf (500 m eklemede e kat)
            eta_t = eta_t * np.maximum(a.yay_zayif, np.exp(-self.yay_isi / 500.0))
        _, (rk, ck) = ndimage.distance_transform_edt(~kita, return_indices=True)
        Sg = S[rk, ck] if kita.any() else S
        eta = eta_t.copy()
        for _ in range(3):
            u, v = self.coz.coz(eta, Sg, sabit, u0, v0)
            ekk, eE = self.coz.gerinim(u, v)
            eta = np.clip(eta_t * (np.maximum(eE, 1e-18) / 1e-15) ** (1 / a.n - 1), 1e19, 1e25)
            if a.plastik_mpa > 0:
                # plastik akma: gerilim akma sınırını aşamaz; sınır birikmiş gerinimle düşer (fay zayıflaması)
                ty = a.plastik_mpa * 1e6 * np.maximum(a.plastik_min, 1.0 - 0.5 * self.Eps / a.plastik_e)
                if self.eta_carpan is not None:  # kratonların akma sınırı da yüksek (viskozite çarpanının karekökü)
                    ty = ty * np.sqrt(self.eta_carpan)
                eta = np.where(kita, np.maximum(np.minimum(eta, ty / (2 * np.maximum(eE, 1e-18))), 1e19), eta)
        # --- taşıma ---
        sn = dt_s / h
        rr, cc = np.mgrid[0:ny, 0:nx].astype(float)
        r0, c0 = rr + v * sn, cc - u * sn
        if a.tasima_kubik:
            # kübik yarı Lagrange + yerel sınırlama (Bermejo ve Staniforth 1992): doğrusal ara değerleme
            # hareket eden kıyıyı her adımda yayıyordu (100 adımda 20 ile 36 hücre); kıyı S 33 km'nin
            # altına inince deniz oluyordu. Sınırlama, kalkış noktasını çevreleyen 4 düğümün aralığı.
            Sy = ndimage.map_coordinates(S, [r0, c0], order=3, mode="nearest")
            i0 = np.clip(np.floor(r0).astype(int), 0, ny - 1); j0 = np.clip(np.floor(c0).astype(int), 0, nx - 1)
            i1 = np.clip(i0 + 1, 0, ny - 1); j1 = np.clip(j0 + 1, 0, nx - 1)
            q = (S[i0, j0], S[i0, j1], S[i1, j0], S[i1, j1])
            S = np.clip(Sy, np.minimum(np.minimum(q[0], q[1]), np.minimum(q[2], q[3])),
                        np.maximum(np.maximum(q[0], q[1]), np.maximum(q[2], q[3])))
        else:
            S = ndimage.map_coordinates(S, [r0, c0], order=1, mode="nearest")
        L = ndimage.map_coordinates(L, [r0, c0], order=self.etiket_derece, mode="nearest")
        if a.yumusama_e0 > 0 or a.plastik_mpa > 0:
            Eps = np.where(kita, self.Eps + eE * dt_s, self.Eps) * np.exp(-a.dt_myr / a.iyilesme_myr)
            self.Eps = ndimage.map_coordinates(Eps, [r0, c0], order=1, mode="nearest")
        # kenarlar: alandan giren malzeme başlangıçtaki kenar değerini taşır (sivrilik birikmesin)
        S[0, :], S[-1, :], S[:, 0], S[:, -1] = self.kenar_S
        L[0, :], L[-1, :], L[:, 0], L[:, -1] = self.kenar_L
        kita = S > 20e3
        # --- dikişin kapanması: iki kıta arasında sıkışan dar okyanus şeridi dalarak yok olur ---
        # sabit ızgarada hücre yok olamadığı için: yakınsayan ve iki yanı kıta olan, 3 hücreden dar
        # okyanus hücreleri komşu kıta kabuğunu alır (kalan okyanus litosferi dalmış sayılır)
        # yalnız gerçekten dar şeritler (yaklaşık 60 km'ye kadar); iç denizler ve boğazlar kapanmasın
        yineleme = max(1, int(round(30.0 / a.h_km)))
        kapali = ndimage.binary_closing(kita, structure=np.ones((3, 3)), iterations=yineleme)
        sikisan = kapali & ~kita & (ekk * dt_s < -a.dikis_esik)
        if sikisan.any():
            Sk = np.where(kita, S, 0.0)
            say = ndimage.uniform_filter(kita.astype(float), 5)
            ort = ndimage.uniform_filter(Sk, 5) / np.maximum(say, 1e-6)
            S = np.where(sikisan, np.maximum(ort, 30e3), S)
            kita = S > 20e3
        # --- kalınlaşma (yalnız kıtada; okyanusta dalma) ---
        dS = np.where(kita, -S * ekk * dt_s, 0.0)
        if a.kita_dalma > 0:
            # çarpışmada kıta kabuğunun bir kısmı manto içine dalar (Ingalls ve diğ. 2016: Hindistan Asya
            # çarpışmasında çarpışma öncesi kabuk kütlesinin yaklaşık %50'si yüzeyde yok)
            dS = np.where(dS > 0, dS * (1.0 - a.kita_dalma), dS)
        S = S + np.clip(dS, -0.2 * S, 15e3)
        if a.yay_uretim_m > 0:
            S = S + self._yay(kita, ekk, u, v, dt_s)
        # --- alt kabuk akışı (alt adımlı, açık) ---
        kap = a.kappa_min + a.kappa_max / (1 + np.exp(-(S - a.S_akis_km * 1e3) / 4e3))
        kap = np.where(kita, kap, 0.0)
        dt_yil = a.dt_myr * 1e6
        alt = int(np.ceil(dt_yil * kap.max() * 4 / (h * h))) + 1
        dta = dt_yil / alt
        for _ in range(alt):
            kx = 0.5 * (kap[:, 1:] + kap[:, :-1]); ky = 0.5 * (kap[1:, :] + kap[:-1, :])
            if not a.kiyi_sizinti:  # kıta kabuğu okyanus litosferinin altına akmaz
                kx = np.where(kita[:, 1:] & kita[:, :-1], kx, 0.0); ky = np.where(kita[1:, :] & kita[:-1, :], ky, 0.0)
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
        if a.yagis:
            from .levha_model import yagis_alani
            self.P = yagis_alani(kara, np.where(kara, z, 0.0), h, 3000.0, 1500.0, 0.15)
            if a.iklim and getattr(self, "lat", None) is not None:
                self.P = self.P * enlem_yagis(self.lat)
            A = np.asarray(self.router.accumulate(np.ascontiguousarray(self.P)))
        else:
            A = np.asarray(self.router.accumulate(1.0))
        e = np.asarray(self.eroder.erode(zr, A, dt_yil)).reshape(S.shape)
        e = np.where(kara, np.clip(e, 0, None), 0.0)
        if a.iklim and getattr(self, "lat", None) is not None:
            # buzul aşınması: kar çizgisinin üstündeki yükseklik zamanla kırpılır (buzul testeresi)
            # buz akısı yağışla orantılı: kurak plato içinde buzul testeresi zayıf
            Pb = self.P if (a.yagis and getattr(self, "P", None) is not None) else 1.0
            eg = np.where(kara, a.buzul_k * dt_yil * Pb * np.clip(z - e - kar_cizgisi(self.lat), 0, None), 0.0)
            e = e + np.minimum(eg, np.clip(z - e, 0, None))
        S = S - e
        hacim = float(e.sum())
        # --- çökelme: açık okyanusa bağlı olmayan bütün çukurlar (iç göller dahil) dolar ---
        z = yuzey(S, S > 20e3, self.suzgec, a)
        acik = acik_okyanus(z)
        tohum = np.where(acik, np.maximum(z, 0.0), z.max() + 1.0)
        maske = np.where(acik, np.maximum(z, 0.0), z)
        dolu = reconstruction(tohum, maske, method="erosion")
        cukur = np.where(~acik & (S > 15e3), np.clip(dolu - z, 0, None), 0.0)  # okyanus kabuğunda çökelme yok
        butce = a.cokelme * hacim
        if cukur.sum() > 0 and butce > 0:
            # çukurun izostatik derinleşmesi için yaklaşık 1/(1−ρc/ρm) kat malzeme gerekir; payı sınırlı
            gerek = cukur.sum() / (1 - RHO_C / RHO_M)
            oran = min(1.0, butce / gerek)
            S = S + cukur * oran / (1 - RHO_C / RHO_M)
            butce -= oran * gerek
        # kalan tortu: kıta kabuğu üstündeki sığ deniz (çöküntü havzası, şelf) deniz seviyesine doğru dolar;
        # önce kıyıya yakın olanlar (nehir ağızları) dolsun diye kıyı uzaklığıyla ağırlıklı
        if butce > 0:
            deniz_kita = acik & (S > 20e3) & (z < 0)
            if deniz_kita.any():
                kiyi_uz = ndimage.distance_transform_edt(acik) * a.h_km
                w = np.where(deniz_kita, np.exp(-kiyi_uz / 150.0), 0.0)
                gerek_h = np.where(deniz_kita, -z / (1 - RHO_C / RHO_M), 0.0)
                pay = np.minimum(gerek_h, butce * w / max(w.sum(), 1e-9))
                S = S + pay
        d.S, d.etiket, d.u, d.v = S, L, u, v
        d.z = yuzey(S, S > 20e3, self.suzgec, a)
        d.ma = round(d.ma - a.dt_myr, 6)
        kara = ~acik_okyanus(d.z)
        d.gunluk.append(dict(ma=d.ma, zmax=float(d.z.max()), Smax_km=float(S.max() / 1e3),
                             kara_orani=float(kara.mean()), asinma_km3=float(hacim * h * h / 1e9),
                             vmax_cm=float(np.hypot(u, v).max() * SANIYE_YIL * 100), temas_ma=self.temas_ma))
        return d


class LabCok(Lab):
    """Çok bloklu laboratuvar: her blok kendi tarihinin (BlokTarihi, sabit bloğa göre) hızıyla sürülür.

    etiket: blok sırası (−1 okyanus başlangıçta; okyanus hücreleri en yakın bloğun levhasına sayılır).
    Konumlar düzlemde; hız Euler kutbundan hücrenin coğrafi konumunda hesaplanıp ızgaraya çevrilir."""

    def __init__(self, S0, etiket0, bas_ma, ayar, lon, lat, tarihler: dict, adlar: list, sabit_ad: str, eksen):
        super().__init__(S0, etiket0, (0.0, 0.0), bas_ma, ayar)
        self.etiket_derece = 0
        # kenardan giren her şey okyanus (kıta kenara çakılıp sonsuz kaynak olmasın)
        self.kenar_S = tuple(np.full_like(k, 7e3) for k in self.kenar_S)
        self.lon, self.lat = lon, lat
        self.tarihler, self.adlar, self.sabit_ad = tarihler, adlar, sabit_ad
        self.de, self.dn = eksen

    def _hiz(self, S, L, kita, d):
        from .izgara import _lonlat_xyz
        a = self.a
        Li = np.rint(L).astype(int)
        # levha: her hücre en yakın kıta hücresinin bloğu
        _, (ri, ci) = ndimage.distance_transform_edt(~kita, return_indices=True)
        lev = Li[ri, ci]
        sabit = np.zeros(S.shape, bool)
        u0 = np.zeros(S.shape); v0 = np.zeros(S.shape)
        for b, ad in enumerate(self.adlar):
            kb = kita & (lev == b)
            if not kb.any():
                continue
            diger = kita & (lev != b)
            dis = ndimage.distance_transform_edt(~diger) * a.h_km if diger.any() else np.full(S.shape, 1e9)
            cek_km = a.cek_sabit_km if ad == self.sabit_ad else a.cek_gelen_km
            # komşularla çevrili bloklarda bu uzaklıkta iç kısım kalmayabilir: o zaman bloğun
            # komşulardan en uzak %40'ı sürülür (yoksa blok sürülmeden pasif kalıyordu)
            esik = min(cek_km, float(np.percentile(dis[kb], 60)))
            cek = kb & (dis >= esik)
            sabit |= cek
            if ad in self.tarihler:
                m = lev == b
                xyz = _lonlat_xyz(self.lon[m], self.lat[m])
                vel = self.tarihler[ad].hiz_cm_yil(d.ma - 0.5 * a.dt_myr, xyz) / 100 / SANIYE_YIL
                lo, la = np.radians(self.lon[m]), np.radians(self.lat[m])
                ev = np.stack([-np.sin(lo), np.cos(lo), np.zeros_like(lo)], 1)
                nv = np.stack([-np.sin(la) * np.cos(lo), -np.sin(la) * np.sin(lo), np.cos(la)], 1)
                ve, vn = (vel * ev).sum(1), (vel * nv).sum(1)
                u0[m] = ve * self.de[0][m] + vn * self.dn[0][m]
                v0[m] = ve * self.de[1][m] + vn * self.dn[1][m]
        sabit[[0, -1], :] = True; sabit[:, [0, -1]] = True
        eta_t = np.where(kita, a.eta0, a.eta0 * a.okyanus)
        if a.gelen_sert != 1.0:
            # gelen bloklar (kalkanlar) sağlam: deformasyon üstteki levhanın içine taşınır
            eta_t = eta_t * np.where(kita & (lev != self.adlar.index(self.sabit_ad)), a.gelen_sert, 1.0)
        eta_t = eta_t * np.exp(-np.clip(S - a.S_ref_km * 1e3, 0, None) / 15e3)
        if self.eta_carpan is not None:
            eta_t = eta_t * np.where(kita, self.eta_carpan, 1.0)
        if a.incelme_km > 0:
            eta_t = eta_t * np.where(kita, np.exp(-np.clip(a.S_ref_km * 1e3 - S, 0, None) / (a.incelme_km * 1e3)), 1.0)
        if a.sinir_zayif != 1.0:
            # yalnız sabit blok ile gelen bloklar arasındaki dikiş: iki yandan da sınıra yakın kıta
            sb = kita & (lev == self.adlar.index(self.sabit_ad))
            gb = kita & ~sb
            if sb.any() and gb.any():
                d_s = ndimage.distance_transform_edt(~sb) * a.h_km
                d_g = ndimage.distance_transform_edt(~gb) * a.h_km
                zayif = kita & (d_s < a.sinir_km) & (d_g < a.sinir_km)
                if a.sinir_tek_yan:
                    zayif &= sb
            # bindirme kuşağı: iki levhanın kıtaları arasındaki sınırda fay zonu zayıftır (gerinim orada
            # yoğunlaşır; Himalaya cephesi gibi). Kenar yumuşatması bir hücre.
                w = ndimage.gaussian_filter(zayif.astype(float), 1.0)
                eta_t = eta_t * np.exp(np.log(a.sinir_zayif) * np.clip(w * 1.5, 0, 1))
        return sabit, u0, v0, eta_t
