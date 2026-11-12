"""İnce viskoz levha (England ve McKenzie 1982; Houseman ve England 1986).

Kıta litosferi, kalınlığı boyunca ortalanmış, düzlemde akan bir viskoz tabaka
gibi ele alınır. Hız alanı u = (u, v) kuvvet dengesinden çözülür:

    ∂j τij = ∂i Γ / L,   τij = 2η (ε̇ij + δij ε̇kk),
    Γ = ½ g ρc (1 − ρc/ρm) S²   (Airy dengesindeki kabuğun potansiyel enerjisi)

S kabuk kalınlığı, L litosfer kalınlığı. δij ε̇kk terimi düşey gerinimden gelir
(ε̇zz = −ε̇kk): sıkışan yerde kabuk kalınlaşır, dS/dt = −S ∇·u. Etkin viskozite
üstel yasayla gerinim hızına bağlıdır: η = η0 (ε̇E / ε̇0)^(1/n − 1).

Bloklar katı çekirdeklerine hız dayatılarak sürülür; aradaki kıta kendi
dayanımına ve kalın kabuğun yayılma eğilimine (Argand sayısı) göre deforme
olur. Dağların ve platoların yeri ve biçimi buradan doğar; kalıp basılmaz.

Izgara: kıtanın ortasına yerleştirilmiş Lambert eşit alanlı azimutal izdüşüm,
düzenli kare hücreler. Bilinen basitleştirme: hesap bugünkü harita
çerçevesindedir, kabuk yatayda taşınmaz (Euler çerçevesi, kıyı sabit).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu

YARICAP = 6.371e6
G = 9.81
RHO_C, RHO_M = 2800.0, 3300.0
BUY = 0.5 * G * RHO_C * (1 - RHO_C / RHO_M)  # Γ = BUY · S²
SANIYE_YIL = 3.15576e7


@dataclass
class Duzlem:
    """Lambert eşit alanlı azimutal izdüşümde düzenli ızgara (satır 0 kuzey)."""
    lon0: float
    lat0: float
    h: float  # hücre boyu, m
    x: np.ndarray  # [nx] m
    y: np.ndarray  # [ny] m, azalan (kuzeyden güneye)
    lon: np.ndarray  # [ny, nx]
    lat: np.ndarray
    kara: np.ndarray  # [ny, nx] bool

    @property
    def sekil(self):
        return self.lon.shape


def laea_ileri(lon, lat, lon0, lat0):
    l, p = np.radians(lon), np.radians(lat)
    l0, p0 = np.radians(lon0), np.radians(lat0)
    k = np.sqrt(2.0 / (1 + np.sin(p0) * np.sin(p) + np.cos(p0) * np.cos(p) * np.cos(l - l0)))
    x = YARICAP * k * np.cos(p) * np.sin(l - l0)
    y = YARICAP * k * (np.cos(p0) * np.sin(p) - np.sin(p0) * np.cos(p) * np.cos(l - l0))
    return x, y


def laea_geri(x, y, lon0, lat0):
    p0 = np.radians(lat0)
    r = np.hypot(x, y)
    c = 2 * np.arcsin(np.clip(r / (2 * YARICAP), -1, 1))
    with np.errstate(invalid="ignore", divide="ignore"):
        p = np.arcsin(np.cos(c) * np.sin(p0) + np.where(r > 0, y * np.sin(c) * np.cos(p0) / r, 0))
        l = np.radians(lon0) + np.arctan2(x * np.sin(c), r * np.cos(p0) * np.cos(c) - y * np.sin(p0) * np.sin(c))
    return np.degrees(l), np.degrees(p)


def duzlem_kur(maske: np.ndarray, sinir, h_km: float = 50.0, pay_km: float = 600.0) -> Duzlem:
    b, g, d, k = sinir
    lon0, lat0 = 0.5 * (b + d), 0.5 * (g + k)
    H, W = maske.shape
    # maskenin karasının izdüşümdeki kapsamı
    yy, xx = np.nonzero(maske[::8, ::8])
    lo = b + (xx * 8 + 0.5) / W * (d - b)
    la = k - (yy * 8 + 0.5) / H * (k - g)
    px, py = laea_ileri(lo, la, lon0, lat0)
    h = h_km * 1e3
    x = np.arange(px.min() - pay_km * 1e3, px.max() + pay_km * 1e3, h)
    y = np.arange(py.max() + pay_km * 1e3, py.min() - pay_km * 1e3, -h)
    X, Y = np.meshgrid(x, y)
    LO, LA = laea_geri(X, Y, lon0, lat0)
    r = np.clip(((k - LA) / (k - g) * H).astype(int), 0, H - 1)
    c = np.clip(((LO - b) / (d - b) * W).astype(int), 0, W - 1)
    ic = (LO >= b) & (LO < d) & (LA > g) & (LA <= k)
    kara = np.zeros(X.shape, bool)
    kara[ic] = maske[r[ic], c[ic]]
    return Duzlem(lon0, lat0, h, x, y, LO, LA, kara)


class LevhaCozucu:
    """Değişken viskoziteli ince levha denklemlerinin sonlu farklarla çözümü.

    Bilinmeyenler hücre merkezlerinde (u, v). Dirichlet hücreleri (blok
    çekirdekleri ve alan kenarı) dayatılmış hızı taşır."""

    def __init__(self, dz: Duzlem, L_m: float = 100e3):
        self.dz = dz
        self.L = L_m
        ny, nx = dz.sekil
        self.ny, self.nx, self.n = ny, nx, ny * nx

    def coz(self, eta: np.ndarray, S: np.ndarray, sabit: np.ndarray, u0: np.ndarray, v0: np.ndarray):
        """eta [ny,nx] Pa s; S kabuk kalınlığı m; sabit bool [ny,nx]; u0,v0 dayatılan hız (m/s).
        Dönüş u, v (m/s), x doğuya, y kuzeye."""
        ny, nx, n, h = self.ny, self.nx, self.n, self.dz.h
        idx = np.arange(n).reshape(ny, nx)
        # satır kuzeyden güneye: y ekseni satırla ters; ∂y = -(∂/∂satır)/h
        e = eta
        def yuz(a, b):  # yüz değerleri: geometrik ortalama
            return np.sqrt(a * b)
        rows, cols, vals = [], [], []
        rhs = np.zeros(2 * n)
        G2 = BUY * S ** 2 / self.L
        # Γ gradyanı (merkezi fark), y kuzeye pozitif
        gx = np.zeros_like(S); gy = np.zeros_like(S)
        gx[:, 1:-1] = (G2[:, 2:] - G2[:, :-2]) / (2 * h)
        gy[1:-1, :] = -(G2[2:, :] - G2[:-2, :]) / (2 * h)

        def ekle(r, c, v):
            rows.append(r); cols.append(c); vals.append(v)

        ic = ~sabit.copy()
        ic[0, :] = ic[-1, :] = ic[:, 0] = ic[:, -1] = False
        I, J = np.nonzero(ic)
        p = idx[I, J]
        # komşu indisleri
        pE, pW_, pN, pS = idx[I, J + 1], idx[I, J - 1], idx[I - 1, J], idx[I + 1, J]
        eE, eW = yuz(e[I, J], e[I, J + 1]), yuz(e[I, J], e[I, J - 1])
        eN, eS = yuz(e[I, J], e[I - 1, J]), yuz(e[I, J], e[I + 1, J])
        h2 = h * h
        # u denklemi: ∂x[4η ∂x u] + ∂y[η ∂y u] + ∂x[2η ∂y v] + ∂y[η ∂x v] = ∂x Γ/L
        ru = p
        ekle(ru, pE, 4 * eE / h2); ekle(ru, pW_, 4 * eW / h2)
        ekle(ru, pN, eN / h2); ekle(ru, pS, eS / h2)
        ekle(ru, p, -(4 * eE + 4 * eW + eN + eS) / h2)
        # karışık terimler: ∂x[2η ∂y v] ≈ (2η_E ∂y v_E − 2η_W ∂y v_W)/(2h), ∂y v_k = (v_N − v_S)/(2h)
        c4 = 1.0 / (4 * h2)
        eJE, eJW = e[I, J + 1], e[I, J - 1]
        ekle(ru, n + idx[I - 1, J + 1], 2 * eJE * c4); ekle(ru, n + idx[I + 1, J + 1], -2 * eJE * c4)
        ekle(ru, n + idx[I - 1, J - 1], -2 * eJW * c4); ekle(ru, n + idx[I + 1, J - 1], 2 * eJW * c4)
        # ∂y[η ∂x v] ≈ (η_N ∂x v_N − η_S ∂x v_S)/(2h)
        eIN, eIS = e[I - 1, J], e[I + 1, J]
        ekle(ru, n + idx[I - 1, J + 1], eIN * c4); ekle(ru, n + idx[I - 1, J - 1], -eIN * c4)
        ekle(ru, n + idx[I + 1, J + 1], -eIS * c4); ekle(ru, n + idx[I + 1, J - 1], eIS * c4)
        rhs[ru] = gx[I, J]
        # v denklemi: ∂x[η ∂x v] + ∂y[4η ∂y v] + ∂x[η ∂y u] + ∂y[2η ∂x u] = ∂y Γ/L
        rv = n + p
        ekle(rv, n + pE, eE / h2); ekle(rv, n + pW_, eW / h2)
        ekle(rv, n + pN, 4 * eN / h2); ekle(rv, n + pS, 4 * eS / h2)
        ekle(rv, rv, -(eE + eW + 4 * eN + 4 * eS) / h2)
        # ∂x[η ∂y u] ≈ (η_E ∂y u_E − η_W ∂y u_W)/(2h)
        ekle(rv, idx[I - 1, J + 1], eJE * c4); ekle(rv, idx[I + 1, J + 1], -eJE * c4)
        ekle(rv, idx[I - 1, J - 1], -eJW * c4); ekle(rv, idx[I + 1, J - 1], eJW * c4)
        # ∂y[2η ∂x u] ≈ (2η_N ∂x u_N − 2η_S ∂x u_S)/(2h)
        ekle(rv, idx[I - 1, J + 1], 2 * eIN * c4); ekle(rv, idx[I - 1, J - 1], -2 * eIN * c4)
        ekle(rv, idx[I + 1, J + 1], -2 * eIS * c4); ekle(rv, idx[I + 1, J - 1], 2 * eIS * c4)
        rhs[rv] = gy[I, J]
        # Dirichlet
        D = idx[~ic]
        for kaydir, deger in ((0, u0[~ic]), (n, v0[~ic])):
            ekle(D + kaydir, D + kaydir, np.ones(D.size))
            rhs[D + kaydir] = deger
        A = sparse.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(2 * n, 2 * n))
        # ölçekleme: satırları köşegene böl (koşul sayısı)
        dg = np.abs(A.diagonal()); dg[dg == 0] = 1
        Dm = sparse.diags(1.0 / dg)
        x = splu((Dm @ A).tocsc()).solve(Dm @ rhs)
        return x[:n].reshape(ny, nx), x[n:].reshape(ny, nx)

    def gerinim(self, u, v):
        h = self.dz.h
        ux = np.gradient(u, h, axis=1); vy = -np.gradient(v, h, axis=0)
        uy = -np.gradient(u, h, axis=0); vx = np.gradient(v, h, axis=1)
        exy = 0.5 * (uy + vx)
        ekk = ux + vy
        # ikinci değişmez (düşey dahil): ε̇E² = ε̇xx² + ε̇yy² + ε̇zz² ... /2 + ε̇xy²
        eE = np.sqrt(0.5 * (ux ** 2 + vy ** 2 + ekk ** 2) + exy ** 2)
        return ekk, eE


def dayanim_dokusu(dz: Duzlem, sapma: float, hat: float, tohum: int = 0) -> np.ndarray:
    """Kıtanın her ölçekte düzensiz dayanımı için viskozite çarpanı.

    sapma: çok ölçekli (yaklaşık 150 ile 1000 km) gürültünün ln η standart sapması.
    hat: eski zayıf hatlar (fay ve sütur ağı); ikinci bir gürültünün sıfır geçişleri
    boyunca yaklaşık 60 km genişliğinde şeritlerde ln η bu kadar düşer.
    Gerçek Dünya'da bu dokunun yeri bilinmez; istatistiksel bir temsil."""
    from scipy import ndimage
    rng = np.random.default_rng(tohum)
    h_km = dz.h / 1e3
    n = np.zeros(dz.sekil)
    for olcek_km, agirlik in ((1000, 1.0), (500, 0.7), (250, 0.5), (150, 0.35)):
        a = ndimage.gaussian_filter(rng.standard_normal(dz.sekil), olcek_km / h_km / 2.5)
        n += agirlik * a / (a.std() + 1e-12)
    n /= n.std()
    b = np.zeros(dz.sekil)
    for olcek_km, agirlik in ((600, 1.0), (300, 0.6)):
        a = ndimage.gaussian_filter(rng.standard_normal(dz.sekil), olcek_km / h_km / 2.5)
        b += agirlik * a / (a.std() + 1e-12)
    b /= b.std()
    # sıfır geçişine uzaklığın kabaca karşılığı: |b| / |∇b|
    gy, gx = np.gradient(b)
    d_km = np.abs(b) / (np.hypot(gx, gy) + 1e-9) * h_km
    serit = np.exp(-(d_km / 30.0) ** 2)
    return np.exp(sapma * n - hat * serit)
