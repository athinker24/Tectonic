import numpy as np

from tektonik import kure
from tektonik.izgara import _lonlat_xyz


def nokta(lon, lat):
    return _lonlat_xyz(np.array(float(lon)), np.array(float(lat)))


def test_donme_kuzey_kutbu():
    q = kure.donme(0, 90, 90)  # kuzey kutbu çevresinde 90° saat yönünün tersi
    lon, lat = kure.xyz_lonlat(kure.uygula(q, nokta(10, 20)))
    assert abs(lon - 100) < 1e-9 and abs(lat - 20) < 1e-9


def test_ters_ve_bileske():
    q1, q2 = kure.donme(30, 40, 25), kure.donme(-70, 10, -60)
    p = nokta(5, 5)
    ileri = kure.uygula(kure.carp(q1, q2), p)
    assert np.allclose(ileri, kure.uygula(q1, kure.uygula(q2, p)))
    assert np.allclose(kure.uygula(kure.ters(kure.carp(q1, q2)), ileri), p)
    # değişmeli değil
    assert not np.allclose(kure.uygula(kure.carp(q2, q1), p), ileri)


def test_ara_sabit_hiz():
    q0, q1 = kure.donme(0, 90, 0), kure.donme(0, 90, 60)
    lon, _ = kure.xyz_lonlat(kure.uygula(kure.ara(q0, q1, 0.25), nokta(0, 0)))
    assert abs(lon - 15) < 1e-6


def test_hiz():
    # 1°/milyon yıl, kutuptan 90° uzakta: 2*pi*6371 km / 360 = 111,19 km/Myr = 11,12 cm/yıl
    v = kure.hiz_cm_yil(0, 90, 1.0, nokta(0, 0))
    assert abs(np.linalg.norm(v) - 11.119) < 0.01
    assert np.linalg.norm(kure.hiz_cm_yil(0, 90, 1.0, nokta(0, 90))) < 1e-9
    v60 = kure.hiz_cm_yil(0, 90, 1.0, nokta(0, 60))
    assert abs(np.linalg.norm(v60) - 11.119 * 0.5) < 0.01


def test_cokgen():
    kare = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=float)
    p = np.stack([nokta(5, 5), nokta(15, 5), nokta(5, -1), nokta(9.9, 9.9), nokta(-175, 0)])
    assert kure.cokgen_ici(p, kare).tolist() == [True, False, False, True, False]
    # 10°x10° ekvator karesi: R² * dlon * (sin10 - sin0)
    beklenen = 6371.0**2 * np.radians(10) * np.sin(np.radians(10))
    assert abs(kure.cokgen_alani_km2(kare) - beklenen) / beklenen < 0.01
    assert abs(kure.cokgen_alani_km2(kare[::-1]) - beklenen) / beklenen < 0.01
