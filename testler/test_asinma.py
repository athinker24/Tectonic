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


def test_carpisma_kutle_ve_sinir(iz):
    from tektonik.olaylar import H0_M, Carpisma
    from tektonik.gurultu import fbm
    cephe = np.array([[x, 31.2] for x in np.linspace(-37, 41, 30)])
    c = Carpisma("t", cephe, ust_sol=True, baslangic_ma=10.0, hiz_cm_yil=4.0, plato_km=500.0)
    c.hazirla(iz, fbm(iz.xyz, 1500.0, 200.0))
    h = np.full(iz.n, H0_M)
    r = c.kalinlasma(5.0, h)
    # kuşak üst levha tarafında (kuzey) olmalı
    lat = iz.lat[iz.kara]
    assert r[lat > 31.2].sum() > 5 * r[lat < 31.2].sum()
    # kütle: toplam hacim akısı ≈ hız × H0 × cephenin karadaki boyu mertebesinde, pozitif ve sonlu
    assert np.isfinite(r).all() and (r >= 0).all()
    # doygunluk: kalınlık sınırdaysa kuşak kabul etmez, plato düğüm sınırı aşılmaz
    h[:] = 80_000.0
    r2 = c.kalinlasma(5.0, h)
    assert r2.max() <= c.plato_azami_m_yil + 1e-12
