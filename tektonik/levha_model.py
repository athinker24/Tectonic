"""İnce viskoz levha + aşınma zaman döngüsü (kalıpsız). Gerçek dünya ve sahibin kıtası aynı kodu kullanır."""
from __future__ import annotations

from dataclasses import dataclass, field

import fastscapelib as fs
import numpy as np
from scipy import ndimage

from .izgara import _lonlat_xyz
from .levha import SANIYE_YIL, Duzlem, LevhaCozucu, laea_ileri

AIRY = 1 - 2800 / 3300


@dataclass
class LevhaAyar:
    eta0: float = 1e22  # Pa s, 1e-15 /s'deki referans viskozite
    n: float = 3.0  # üstel yasa
    okyanus: float = 1.0  # okyanus viskozite çarpanı
    cekirdek_km: float = 700.0  # blok çekirdeği: başka bloğun karasına uzaklık
    cekirdek_ozel: dict = field(default_factory=dict)  # blok adı -> çekirdek uzaklığı (km)
    k: float = 4e-9  # akarsu aşınma katsayısı
    m: float = 1.0
    nsp: float = 2.0
    s_ref_km: float = 33.0  # deniz seviyesindeki kabuk kalınlığı
    bukulme_km: float = 80.0
    dt_myr: float = 0.5
    alt_adim: int = 5
    kare_myr: float = 2.0
    tohum: int = 3
    yagis: bool = False  # orografik yağış: aşınma yağışla toplanan suya bağlı
    yagis_L_km: float = 3000.0  # düz karada nemin yağarak tükenme uzunluğu
    yagis_Hc_m: float = 1500.0  # bu kadar yükselen hava neminin çoğunu bırakır
    yagis_taban: float = 0.15  # buharlaşmayla yeniden dolaşan nem (iç kesimler hiç kurumasın)


@dataclass
class LevhaSonuc:
    z: np.ndarray
    S: np.ndarray
    kareler: list = field(default_factory=list)
    gunluk: list = field(default_factory=list)
    yagis: np.ndarray | None = None


def yerel_eksenler(dz: Duzlem, lon, lat):
    e = 0.01
    x0, y0 = laea_ileri(lon, lat, dz.lon0, dz.lat0)
    xe, ye = laea_ileri(lon + e / np.cos(np.radians(lat)), lat, dz.lon0, dz.lat0)
    xn, yn = laea_ileri(lon, lat + e, dz.lon0, dz.lat0)
    de = np.stack([xe - x0, ye - y0]); de /= np.linalg.norm(de, axis=0)
    dn = np.stack([xn - x0, yn - y0]); dn /= np.linalg.norm(dn, axis=0)
    return de, dn


def yagis_alani(kara: np.ndarray, z: np.ndarray, h_m: float, L_km: float, Hc_m: float, taban: float) -> np.ndarray:
    """Dört yönden (batı, doğu, güney, kuzey) esen nemli havanın bıraktığı yağış, eşit ağırlıklı.
    Nem q denizde 1; karada her hücrede p = q (h/L + max(0, Δz)/Hc) yağar ve q'dan düşer.
    Dönüş: ortalaması kara üzerinde 1 olacak biçimde ölçeklenmiş yağış (iç kesimde en az `taban`)."""
    ny, nx = kara.shape
    top = np.zeros(kara.shape)
    a = h_m / (L_km * 1e3)
    for eksen, ters in ((1, False), (1, True), (0, False), (0, True)):
        K, Z = (kara, z) if eksen == 1 else (kara.T, z.T)
        if ters:
            K, Z = K[:, ::-1], Z[:, ::-1]
        q = np.ones(K.shape[0])
        P = np.zeros(K.shape)
        zonce = np.zeros(K.shape[0])
        for j in range(K.shape[1]):
            k = K[:, j]
            zz = np.where(k, Z[:, j], 0.0)
            # denizden karaya ilk hücre: kıyıdaki yükseklik sıçraması yamaç sayılmaz
            zonce = np.where(k & (j > 0) & ~K[:, max(j - 1, 0)], zz, zonce)
            oran = np.clip(a + np.maximum(zz - zonce, 0) / Hc_m, 0, 1)
            p = np.where(k, q * oran, 0.0)
            P[:, j] = p
            q = np.where(k, q - p, 1.0)
            zonce = zz
        if ters:
            P = P[:, ::-1]
        top += P if eksen == 1 else P.T
    top = np.where(kara, top, 0.0)
    ort = top[kara].mean() if kara.any() else 1.0
    return np.where(kara, np.maximum(top / ort, taban), 0.0)


def kos_levha(dz: Duzlem, blok: np.ndarray, adlar: list[str], tarihler: dict, bas_ma: float,
              ayar: LevhaAyar | None = None, gunluk_yaz=print, eta_carpan: np.ndarray | None = None) -> LevhaSonuc:
    """blok: [ny,nx] blok sırası (deniz −1). tarihler: ad -> BlokTarihi (sabit blokta yok)."""
    a = ayar or LevhaAyar()
    h_km = dz.h / 1e3
    ny, nx = dz.sekil
    kara = dz.kara
    # levhalar (deniz en yakın bloğa) ve çekirdekler
    _, (ri, ci) = ndimage.distance_transform_edt(blok < 0, return_indices=True)
    levha = blok[ri, ci]
    cekirdek = {}
    for b, ad in enumerate(adlar):
        diger = kara & (blok != b) & (blok >= 0)
        d = ndimage.distance_transform_edt(~diger) * h_km if diger.any() else np.full(dz.sekil, np.inf)
        dl = ndimage.distance_transform_edt(levha == b) * h_km
        ck_km = a.cekirdek_ozel.get(ad, a.cekirdek_km)
        cekirdek[ad] = (levha == b) & (d > ck_km) & (dl > 0.5 * min(ck_km, a.cekirdek_km))
    eta_taban = np.where(kara, a.eta0, a.eta0 * a.okyanus)
    if eta_carpan is not None:
        eta_taban = eta_taban * eta_carpan  # dayanım farkları (sert çekirdekler)

    rng = np.random.default_rng(a.tohum)
    kiyi = ndimage.distance_transform_edt(kara) * h_km
    S = np.full(dz.sekil, 35e3)
    g = ndimage.gaussian_filter(rng.standard_normal(dz.sekil), 3); g /= g.std()
    z = np.where(kara, np.clip(AIRY * (35e3 - a.s_ref_km * 1e3) + 40 * g, 0, None) * np.clip(kiyi / 150, 0, 1), 0)

    durum = {(int(i), int(j)): fs.NodeStatus.FIXED_VALUE for i, j in zip(*np.nonzero(~kara))}
    grid = fs.RasterGrid([ny, nx], [dz.h, dz.h], fs.NodeStatus.FIXED_VALUE, durum)
    router = fs.FlowGraph(grid, [fs.SingleFlowRouter(), fs.MSTSinkResolver()])
    klit = a.k * np.exp(0.5 * ndimage.gaussian_filter(rng.standard_normal(dz.sekil), 2) * 2)
    eroder = fs.SPLEroder(router, klit, a.m, a.nsp, 1e-4)

    coz = LevhaCozucu(dz)
    de, dn = yerel_eksenler(dz, dz.lon, dz.lat)
    _, (rk, ck) = ndimage.distance_transform_edt(~kara, return_indices=True)
    kar = kara.astype(float)
    sig = a.bukulme_km / h_km

    def gk(x):
        return ndimage.gaussian_filter(x * kar, sig) / np.maximum(ndimage.gaussian_filter(kar, sig), 1e-6)

    sonuc = LevhaSonuc(z, S)
    u = v = np.zeros(dz.sekil)
    ma = float(bas_ma)
    dt = a.dt_myr
    e = np.zeros(dz.sekil)
    while ma > 1e-6:
        sabit = np.zeros(dz.sekil, bool)
        u0 = np.zeros(dz.sekil); v0 = np.zeros(dz.sekil)
        sabit[[0, -1], :] = True; sabit[:, [0, -1]] = True
        for ad in adlar:
            mm = cekirdek[ad]
            if not mm.any():
                continue
            sabit |= mm
            if ad in tarihler:
                xyz = _lonlat_xyz(dz.lon[mm], dz.lat[mm])
                vel = tarihler[ad].hiz_cm_yil(ma - 0.25 * dt, xyz) / 100 / SANIYE_YIL
                lo, la = np.radians(dz.lon[mm]), np.radians(dz.lat[mm])
                ev = np.stack([-np.sin(lo), np.cos(lo), np.zeros_like(lo)], 1)
                nv = np.stack([-np.sin(la) * np.cos(lo), -np.sin(la) * np.sin(lo), np.cos(la)], 1)
                ve, vn = (vel * ev).sum(1), (vel * nv).sum(1)
                u0[mm] = ve * de[0][mm] + vn * dn[0][mm]
                v0[mm] = ve * de[1][mm] + vn * dn[1][mm]
        Sg = S[rk, ck]
        eta = eta_taban.copy()
        for _ in range(4):
            u, v = coz.coz(eta, Sg, sabit, u0, v0)
            ekk, eE = coz.gerinim(u, v)
            eta = np.clip(eta_taban * (np.maximum(eE, 1e-18) / 1e-15) ** (1 / a.n - 1), 1e20, 1e25)
        dS = np.where(kara, -S * ekk * dt * 1e6 * SANIYE_YIL, 0.0)
        dS = np.clip(dS, -0.2 * S, 30e3)
        S = np.where(kara, np.clip(S + dS, 20e3, 90e3), 35e3)
        z = np.where(kara, (z - gk(z)) + AIRY * (gk(S) - a.s_ref_km * 1e3) * np.clip(kiyi / 60, 0, 1), 0.0)
        z = np.where(kara, np.maximum(z, 0.0), 0.0)
        top_e = 0.0
        P = yagis_alani(kara, z, dz.h, a.yagis_L_km, a.yagis_Hc_m, a.yagis_taban) if a.yagis else None
        for _ in range(a.alt_adim):
            zf = z.copy()
            router.update_routes(zf)
            A = np.asarray(router.accumulate(P if P is not None else 1.0))
            e = np.asarray(eroder.erode(zf, A, dt / a.alt_adim * 1e6)).reshape(dz.sekil)
            z = np.where(kara, np.maximum(z - e, 0.0), 0.0)
            S = S - np.where(kara, e, 0)
            top_e += float(e[kara].sum())
        ma = round(ma - dt, 6)
        if abs(ma / a.kare_myr - round(ma / a.kare_myr)) < 1e-6:
            sonuc.kareler.append((ma, z.astype(np.float32).copy()))
            sonuc.yagis = P
            alan = dz.h ** 2
            gun = dict(ma=ma, zmax=float(z.max()), zort=float(z[kara].mean()), Smax_km=float(S[kara].max() / 1e3),
                       kalinlasma_km3_yil=float(np.sum(-ekk[kara] * Sg[kara]) * alan * SANIYE_YIL / 1e9),
                       asinma_km3_yil=float(top_e * alan / (dt * 1e6) / 1e9))
            sonuc.gunluk.append(gun)
            if gunluk_yaz:
                gunluk_yaz(gun)
    sonuc.z, sonuc.S = z, S
    sonuc.yagis = yagis_alani(kara, z, dz.h, a.yagis_L_km, a.yagis_Hc_m, a.yagis_taban)
    return sonuc
