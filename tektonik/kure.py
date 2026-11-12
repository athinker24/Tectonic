"""Küre üzerinde blok hareketi: Euler dönmeleri, hız, çokgen içi sınaması.

Saf numpy. Dönmeler birim kuaterniyonla tutulur (w, x, y, z); pozitif açı
kutup ekseni çevresinde saat yönünün tersidir (pyGPlates ile aynı kural,
arastirma/08).
"""
from __future__ import annotations

import numpy as np

from .izgara import YARICAP_M, _lonlat_xyz

CM_YIL = YARICAP_M * 100.0  # rad/yıl -> cm/yıl çarpanı (ekvatorda)


def xyz_lonlat(p: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(p, dtype=float)
    return np.degrees(np.arctan2(p[..., 1], p[..., 0])), np.degrees(np.arcsin(np.clip(p[..., 2], -1, 1)))


def donme(kutup_lon: float, kutup_lat: float, aci_derece: float) -> np.ndarray:
    """Euler kutbu ve açıdan birim kuaterniyon."""
    u = _lonlat_xyz(np.array(kutup_lon), np.array(kutup_lat))
    h = np.radians(aci_derece) / 2.0
    return np.concatenate([[np.cos(h)], np.sin(h) * u])


def carp(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """Bileşke: önce q2, sonra q1 uygulanır (değişmeli değildir)."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ]
    )


def ters(q: np.ndarray) -> np.ndarray:
    return q * np.array([1.0, -1.0, -1.0, -1.0])


def uygula(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Birim vektör(ler)i döndür. p: [..., 3]."""
    w, v = q[0], q[1:]
    p = np.asarray(p, dtype=float)
    t = 2.0 * np.cross(v, p)
    return p + w * t + np.cross(v, t)


def ara(q1: np.ndarray, q2: np.ndarray, s: float) -> np.ndarray:
    """Büyük daire ara değerlemesi (slerp): sabit açısal hız."""
    d = float(np.dot(q1, q2))
    if d < 0:
        q2, d = -q2, -d
    if d > 0.9995:
        q = q1 + s * (q2 - q1)
        return q / np.linalg.norm(q)
    th = np.arccos(d)
    return (np.sin((1 - s) * th) * q1 + np.sin(s * th) * q2) / np.sin(th)


def hiz_cm_yil(kutup_lon: float, kutup_lat: float, derece_myr: float, p: np.ndarray) -> np.ndarray:
    """Noktalardaki hız vektörü (cm/yıl), birim küre teğet düzleminde [..., 3].

    v = omega x r. 1°/milyon yıl, kutuptan 90° uzakta yaklaşık 11,1 cm/yıl.
    """
    w = _lonlat_xyz(np.array(kutup_lon), np.array(kutup_lat)) * np.radians(derece_myr) / 1e6
    return np.cross(w, np.asarray(p, dtype=float)) * CM_YIL


def cokgen_ici(p: np.ndarray, kose_lonlat: np.ndarray) -> np.ndarray:
    """Noktalar küresel çokgenin içinde mi (sarım sayısı, çokgen yarım küreden küçük).

    kose_lonlat: [K, 2] derece, sıralı köşeler (kapatma gerekmez).
    """
    v = _lonlat_xyz(kose_lonlat[:, 0], kose_lonlat[:, 1])
    m = v.mean(axis=0)
    m /= np.linalg.norm(m)
    # merkeze teğet düzleme gnomonik izdüşüm: büyük daireler doğru olur
    e1 = np.cross([0.0, 0.0, 1.0], m)
    if np.linalg.norm(e1) < 1e-9:
        e1 = np.array([1.0, 0.0, 0.0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(m, e1)

    def izdusur(q):
        c = q @ m
        return (q @ e1) / c, (q @ e2) / c, c

    vx, vy, vc = izdusur(v)
    if (vc <= 0.05).any():
        raise ValueError("çokgen yarım küreye yakın ya da büyük; parçalara bölün")
    p = np.asarray(p, dtype=float)
    px, py, pc = izdusur(p)
    ic = np.zeros(p.shape[:-1], dtype=bool)
    K = len(vx)
    for i in range(K):
        j = (i + 1) % K
        kesisir = (vy[i] > py) != (vy[j] > py)
        with np.errstate(divide="ignore", invalid="ignore"):
            xk = (vx[j] - vx[i]) * (py - vy[i]) / (vy[j] - vy[i]) + vx[i]
        ic ^= kesisir & (px < xk)
    return ic & (pc > 0)


def cokgen_alani_km2(kose_lonlat: np.ndarray) -> float:
    """Küresel çokgen alanı (küresel fazlalık), km²."""
    v = _lonlat_xyz(kose_lonlat[:, 0], kose_lonlat[:, 1])
    K = len(v)
    toplam = 0.0
    for i in range(K):
        a, b, c = v[i - 1], v[i], v[(i + 1) % K]
        t1 = np.cross(b, a)
        t2 = np.cross(b, c)
        t1 /= np.linalg.norm(t1)
        t2 /= np.linalg.norm(t2)
        aci = np.arctan2(np.dot(b, np.cross(t1, t2)), np.dot(t1, t2))
        toplam += aci % (2 * np.pi)
    fazla = toplam - (K - 2) * np.pi
    if fazla < 0 or fazla > 2 * np.pi:
        fazla = 4 * np.pi - abs(fazla) if fazla > 2 * np.pi else abs(fazla)
    return float(min(fazla, 4 * np.pi - fazla) * (YARICAP_M / 1e3) ** 2)
