import json

import numpy as np
import pytest

from tektonik import kure
from tektonik.bloklar import bloklara_ayir
from tektonik.izgara import _lonlat_xyz, izgara_kur, maske_oku
from tektonik.tarih import Asama, BlokTarihi, hareket_kutbu


@pytest.fixture(scope="module")
def iz():
    return izgara_kur(maske_oku("veri/test_maske.png"), nside=64)


def test_bloklar(iz):
    s = json.load(open("veri/test_senaryo.json", encoding="utf-8"))
    b = bloklara_ayir(iz, s)
    assert (b.etiket[iz.kara] >= 0).all() and (b.etiket[~iz.kara] == -1).all()
    for ad in b.adlar:
        assert b.maske(ad).sum() > 10, ad
    # Güneydoğu bloğu dikişin güneyinde
    assert np.median(iz.lat[b.maske("Güneydoğu")]) < 25
    assert np.median(iz.lat[b.maske("Kuzey")]) > 35


def test_hareket_kutbu():
    lon, lat, w = hareket_kutbu((15.0, 10.0), 0.0, 5.0)  # kuzeye 5 cm/yıl
    v = kure.hiz_cm_yil(lon, lat, w, _lonlat_xyz(np.array(15.0), np.array(10.0)))
    assert abs(np.linalg.norm(v) - 5.0) < 1e-6
    assert v[2] > 0  # kuzeye (z artıyor)


def test_geri_surme():
    # 10 milyon yıl boyunca kuzeye 5 cm/yıl: 500 km; geriye sürünce 500 km güneyde olmalı
    lon, lat, w = hareket_kutbu((15.0, 10.0), 0.0, 5.0)
    t = BlokTarihi("x", [Asama(10.0, 0.0, lon, lat, w)])
    p = _lonlat_xyz(np.array(15.0), np.array(10.0))
    q = kure.uygula(t.geri_donme(10.0), p)
    km = np.degrees(np.arccos(np.clip(q @ p, -1, 1))) * 111.19
    assert abs(km - 500.0) < 1.0
    _, enlem = kure.xyz_lonlat(q)
    assert enlem < 10.0
    # şimdi ve aşama öncesi
    assert np.allclose(t.geri_donme(0.0), [1, 0, 0, 0])
    assert np.allclose(t.geri_donme(20.0), t.geri_donme(10.0))
