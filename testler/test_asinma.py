import numpy as np
import pytest

from tektonik.asinma import AsinmaAyar, asindir
from tektonik.izgara import SABIT, izgara_kur, maske_oku


@pytest.fixture(scope="module")
def iz():
    return izgara_kur(maske_oku("veri/test_maske.png"), nside=64)


def test_izgara_kiyi(iz):
    assert iz.kara.sum() > 2000
    assert iz.kiyi.sum() > 100
    assert not (iz.kara & iz.kiyi).any()
    assert (iz.durum[iz.kiyi] == SABIT).all()
    # ölçülen kıta sınırları (KARARLAR 7), bir hücre payıyla
    pay = iz.hucre_km / 111.0 * 1.5
    assert abs(iz.lat[iz.kara].max() - 59.99) < pay
    assert abs(iz.lat[iz.kara].min() + 7.08) < pay
    assert abs(iz.lon[iz.kara].min() + 44.43) < pay
    assert abs(iz.lon[iz.kara].max() - 43.11) < pay
    # kara alanı: atlas maskesinden ~35 milyon km²
    assert 30e6 < iz.kara.sum() * iz.alan_m2 / 1e6 < 40e6


def test_asinma_birimi(iz):
    """Eğimli düzlemde tek küçük adım: aşınma ≈ K · A^m · S · dt."""
    z0 = np.zeros(iz.n)
    z0[iz.kara] = iz.kiyiya_km[iz.kara] * 10.0  # eğim 0,01
    k, dt = 1e-7, 1.0
    son = asindir(iz, np.zeros(iz.n), dt, AsinmaAyar(k=k, dt_yil=dt, tolerans=1e-7), z0=z0)
    ic = iz.kara & (iz.kiyiya_km > 300)
    beklenen = k * np.sqrt(son.drenaj_m2[ic]) * 0.01 * dt
    oran = np.median((z0[ic] - son.z[ic]) / beklenen)
    assert 0.8 < oran < 1.1


def test_kiyi_sabit(iz):
    u = np.where(iz.kara, 1e-3, 0.0)
    son = asindir(iz, u, 2e6, AsinmaAyar(k=2e-6))
    assert (son.z[~iz.kara] == 0).all()
    assert son.z[iz.kara].max() > 1.0
    assert np.isfinite(son.z).all()
