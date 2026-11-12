"""Rastgele mod: sahibin işaretleri ve senaryo olmadan, kıtanın rastgele bir birleşme tarihi.

Bugün kıta tek parça olduğu için iç sınırlar geçmişte ayrılan sınırlar olamaz
(geriye sürünce bloklar üst üste biner). Bu yüzden üretilen tarih bir
birleşme tarihidir: sabit en büyük bloğa diğer bloklar sırayla gelip çarpar,
çarpışmadan sonra yavaşlayarak itmeyi sürdürür. Çarpışan her ortak sınırda,
göreli hızın sınıra dik bileşeninden bir dağ kuşağı (ve rastgele bir plato)
kurulur. Sert kısıtlar (çakışma, hız) uretici.kisitlari_denetle ile aynıdır.
"""
from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import cKDTree

from . import kure
from .bloklar import Bloklar, kara_komsuluk
from .gurultu import fbm
from .izgara import Izgara, _lonlat_xyz
from .olaylar import BlokSikismasi, SinirCarpismasi
from .tarih import Asama, BlokTarihi, hareket_kutbu
from .uretici import Aday, _merkez

YON_ADI = ["Kuzey", "Kuzeydoğu", "Doğu", "Güneydoğu", "Güney", "Güneybatı", "Batı", "Kuzeybatı"]


def tohum_sec(iz: Izgara, sayi: int, rng: np.random.Generator, en_az_km: float = 900.0) -> np.ndarray:
    """Karada birbirinden en az en_az_km uzak rastgele tohum noktaları (lon, lat)."""
    idx = np.flatnonzero(iz.kara)
    secilen: list[int] = []
    for _ in range(4000):
        i = int(rng.choice(idx))
        if all(np.arccos(np.clip(iz.xyz[i] @ iz.xyz[j], -1, 1)) * 6371.0 > en_az_km for j in secilen):
            secilen.append(i)
        if len(secilen) == sayi:
            break
    return np.c_[iz.lon[secilen], iz.lat[secilen]]


def rastgele_bloklar(iz: Izgara, tohumlar: np.ndarray, gurultu_tohum: int, en_kucuk_mkm2: float = 0.4) -> Bloklar:
    """Tohumlardan gürültülü jeodezik uzaklıkla (çok kaynaklı Dijkstra) bloklar.
    Kenar ağırlığı fBm ile oynatıldığı için sınırlar kıvrımlı olur; bloklar
    kara grafiğinde bağlıdır. Tohumsuz kara parçaları (adalar) en yakın bloğa katılır."""
    idx = np.flatnonzero(iz.kara)
    A = kara_komsuluk(iz, idx).tocoo()
    g = fbm(iz.xyz[idx], 1200.0, 60.0, tohum=gurultu_tohum)
    w = np.exp(0.6 * 0.5 * (g[A.row] + g[A.col]))
    W = sparse.csr_matrix((w, (A.row, A.col)), shape=A.shape)
    agac = cKDTree(iz.xyz[idx])
    _, kaynak = agac.query(_lonlat_xyz(tohumlar[:, 0], tohumlar[:, 1]))
    # tohumsuz büyük kara parçası (ada kıta) kendi bloğu olur
    _, bil = connected_components(A.tocsr(), directed=False)
    alan_dugum = iz.alan_m2 / 1e12
    for c in np.unique(bil):
        uye = np.flatnonzero(bil == c)
        if not np.isin(kaynak, uye).any() and uye.size * alan_dugum > 0.5:
            mer = iz.xyz[idx[uye]].mean(0)
            kaynak = np.append(kaynak, uye[np.argmax(iz.xyz[idx[uye]] @ mer)])
            tohumlar = np.vstack([tohumlar, [iz.lon[idx[kaynak[-1]]], iz.lat[idx[kaynak[-1]]]]])
    _, _, kim = dijkstra(W, directed=False, indices=kaynak, min_only=True, return_predecessors=True)
    etk = np.full(idx.size, -1)
    ulasti = kim >= 0
    etk[ulasti] = np.searchsorted(np.sort(kaynak), kim[ulasti])
    sira = np.argsort(kaynak)  # searchsorted sıralı kaynağa göre; tohum sırasına çevir
    etk[ulasti] = sira[etk[ulasti]]
    # ulaşılamayan küçük parçalar (adalar): parçanın tamamı, en yakın düğümlerinin çoğunluk bloğuna
    for c in np.unique(bil[~ulasti]):
        uye = np.flatnonzero((bil == c) & ~ulasti)
        _, j = cKDTree(iz.xyz[idx[ulasti]]).query(iz.xyz[idx[uye]])
        etk[uye] = np.bincount(etk[ulasti][j]).argmax()
    # çok küçük blokları en uzun sınırı paylaştığı komşuya kat
    alan = iz.alan_m2 / 1e12
    A = A.tocsr()
    while True:
        say = np.bincount(etk, minlength=len(tohumlar)) * alan
        kucuk = [b for b in np.unique(etk) if say[b] < en_kucuk_mkm2]
        if not kucuk or len(np.unique(etk)) <= 2:
            break
        b = kucuk[0]
        m = np.flatnonzero(etk == b)
        komsu = etk[A[m].indices]
        komsu = komsu[komsu != b]
        if komsu.size == 0:
            _, j = cKDTree(iz.xyz[idx[etk != b]]).query(iz.xyz[idx[m]])
            etk[m] = etk[etk != b][j]
        else:
            etk[m] = np.bincount(komsu).argmax()
    # yeniden numarala, alanına göre büyükten küçüğe
    kalan = [b for b in np.argsort(-np.bincount(etk)) if np.any(etk == b)]
    yeni = np.full(len(tohumlar), -1)
    for k, b in enumerate(kalan):
        yeni[b] = k
    etk = yeni[etk]
    etiket = np.full(iz.n, -1)
    etiket[idx] = etk
    # adlar: kıta merkezine göre yön
    merkez = _merkez(iz, iz.kara)
    adlar = []
    for k in range(len(kalan)):
        if k == 0:
            adlar.append("Çekirdek")
            continue
        lo, la = _merkez(iz, etiket == k)
        aci = np.degrees(np.arctan2((lo - merkez[0]) * np.cos(np.radians(la)), la - merkez[1])) % 360
        ad = YON_ADI[int(((aci + 22.5) % 360) // 45)]
        n = sum(1 for a in adlar if a.startswith(ad))
        adlar.append(ad if n == 0 else f"{ad} {n + 1}")
    return Bloklar(adlar, etiket, "Çekirdek")


def sinirlar(iz: Izgara, bloklar: Bloklar) -> dict[tuple[int, int], np.ndarray]:
    """Komşu blok çiftleri ve ortak sınır uzunluğu (km, yaklaşık)."""
    idx = np.flatnonzero(iz.kara)
    A = kara_komsuluk(iz, idx).tocoo()
    e = bloklar.etiket[idx]
    a, b = e[A.row], e[A.col]
    fark = a != b
    sonuc: dict = {}
    for i, j, r in zip(a[fark], b[fark], A.row[fark]):
        k = (min(i, j), max(i, j))
        sonuc.setdefault(k, set()).add(int(idx[r]))
    return {k: np.array(sorted(v)) for k, v in sonuc.items()}


def rastgele_aday(no: int, rng: np.random.Generator, iz: Izgara, bloklar: Bloklar) -> Aday:
    """Birleşme tarihi: her hareketli blok için geliş yönü, çarpışma zamanı, hız."""
    sin = sinirlar(iz, bloklar)
    nb = len(bloklar.adlar)
    hucre = iz.hucre_km
    tarihler: dict[str, BlokTarihi] = {}
    p: dict = {"bloklar": {}}
    anlati: list[str] = []
    # Ağaç: çekirdekten genişleyerek her bloğun ana bloğu, en uzun sınırı paylaştığı ağaçtaki komşu.
    # Blok ana bloğuna göre hareket eder ve ana bloğun hareketini devralır (aşamalar birleşir);
    # ana bloktan sonra gelir. Böylece sonradan çarpan bloklar, çarptıkları bloğun itişini taşır.
    ana = {0: None}
    zaman = {0: float(rng.uniform(60, 110))}  # çekirdek için üst sınır gibi davranır
    sira = [0]
    while len(sira) < nb:
        aday_k = []
        for (i, j), v in sin.items():
            for x, y in ((i, j), (j, i)):
                if x in ana and y not in ana:
                    aday_k.append((y, x, len(v)))
        if not aday_k:
            break
        # rastgele ama uzun sınıra ağırlıklı seçim
        w = np.array([t[2] for t in aday_k], float)
        y, x, _ = aday_k[int(rng.choice(len(aday_k), p=w / w.sum()))]
        # ana bloğu: ağaçtaki komşular arasında en uzun sınır
        komsu = [(xx, len(v)) for (i, j), v in sin.items() for xx, yy in ((i, j), (j, i)) if yy == y and xx in ana]
        x = max(komsu, key=lambda t: t[1])[0]
        ana[y] = x
        zaman[y] = float(zaman[x] * rng.uniform(0.25, 0.9)) if x != 0 else float(rng.uniform(10, 80))
        sira.append(y)
    for k in sira[1:]:
        ad = bloklar.adlar[k]
        m = bloklar.maske(ad)
        ortak = ana[k]
        s = sin[(min(k, ortak), max(k, ortak))]
        c = _merkez(iz, m)
        sv = iz.xyz[s].mean(axis=0)
        sv /= np.linalg.norm(sv)
        lo_s, la_s = kure.xyz_lonlat(sv)
        yon0 = np.degrees(np.arctan2((float(lo_s) - c[0]) * np.cos(np.radians(c[1])), float(la_s) - c[1]))
        q = {
            "carpisma_ma": zaman[k],
            "mesafe_km": float(rng.uniform(200, 1800)),
            "hiz_once": float(rng.uniform(1.5, 4.5 if ortak == 0 else 3.5)),
            "hiz_sonra": float(rng.uniform(0.3, 2.5 if ortak == 0 else 1.5)),
            "yon": float(yon0 + rng.uniform(-30, 30)),
            "ortak": bloklar.adlar[ortak],
        }
        once = q["mesafe_km"] / (q["hiz_once"] * 10.0)
        lo, la, w1 = hareket_kutbu(c, q["yon"], q["hiz_once"])
        _, _, w2 = hareket_kutbu(c, q["yon"], q["hiz_sonra"])
        devralinan = list(tarihler[bloklar.adlar[ortak]].asamalar) if ortak != 0 else []
        tarihler[ad] = BlokTarihi(ad, devralinan + [
            Asama(q["carpisma_ma"] + once, q["carpisma_ma"], lo, la, w1),
            Asama(q["carpisma_ma"], 0.0, lo, la, w2),
        ])
        p["bloklar"][ad] = q
    # birleşmiş komşu çiftler: ikisi de yerindeyken binme serbest (bkz. kisitlari_denetle)
    p["izinli_cakisma"] = {}
    for (i, j) in sin:
        ti, tj = zaman.get(i), zaman.get(j)
        if ti is None or tj is None:
            continue
        ti = np.inf if i == 0 else ti
        tj = np.inf if j == 0 else tj
        p["izinli_cakisma"][f"{bloklar.adlar[i]}|{bloklar.adlar[j]}"] = float(min(ti, tj))
    # olaylar: her ortak sınırda göreli dik yakınsama
    olaylar: list = []
    for (i, j), s in sin.items():
        if len(s) * hucre < 250:
            continue
        ai, aj = bloklar.adlar[i], bloklar.adlar[j]
        ti = p["bloklar"].get(ai, {}).get("carpisma_ma", np.inf)
        tj = p["bloklar"].get(aj, {}).get("carpisma_ma", np.inf)
        bas = float(min(ti, tj))
        if not np.isfinite(bas):
            continue
        pts = iz.xyz[s]
        vi = tarihler[ai].hiz_cm_yil(0.5, pts) if ai in tarihler else np.zeros_like(pts)
        vj = tarihler[aj].hiz_cm_yil(0.5, pts) if aj in tarihler else np.zeros_like(pts)
        n = iz.xyz[bloklar.maske(aj)].mean(0) - iz.xyz[bloklar.maske(ai)].mean(0)
        n -= pts.mean(0) * (n @ pts.mean(0))
        n /= np.linalg.norm(n)
        yakinsama = float(np.mean((vi - vj) @ n))  # + : i, j'ye doğru gidiyor
        if yakinsama < 0.3:
            continue
        # gelen blok (sonradan çarpan, daha genç zaman) alt levha olur, %25 ters
        gelen = ai if ti <= tj else aj
        ust = aj if gelen == ai else ai
        if rng.random() < 0.25:
            ust, gelen = gelen, ust
        e = {
            "kusak_km": float(rng.uniform(150, 350)), "plato_km": float(rng.choice([0.0, rng.uniform(200, 900)])),
            "plato_orani": float(rng.uniform(0.0, 0.5)), "hmax_km": float(rng.uniform(55, 70)),
        }
        olaylar.append(SinirCarpismasi(
            f"{ust} ile {gelen} çarpışması", np.zeros((2, 2)), ust_sol=True, baslangic_ma=bas,
            hiz_cm_yil=yakinsama, kusak_km=e["kusak_km"], plato_km=e["plato_km"],
            kusak_hmax_m=e["hmax_km"] * 1e3, plato_hmax_m=45_000.0, plato_orani=e["plato_orani"] if e["plato_km"] else 0.0,
            kusak_k_carpani=0.3, ust_blok=bloklar.maske(ust), alt_blok=bloklar.maske(gelen)))
        p.setdefault("olaylar", []).append(dict(ust=ust, alt=gelen, baslangic_ma=bas, yakinsama=yakinsama, **e))
        boyut = "geniş bir platoyla birlikte " if e["plato_km"] else ""
        anlati.append(
            f"{ai} ile {aj} arasındaki sınır {bas:.0f} milyon yıl önce kapandı; {gelen} altta, {ust} üstte kaldı. "
            f"Yılda {yakinsama:.1f} cm yakınsamayla {ust} tarafında {boyut}{e['kusak_km']:.0f} km genişliğinde "
            f"bir dağ kuşağı yükseldi.")
    # küçük ve sıkışan bloklar bütünüyle kalınlaşabilir
    for ad, q in p["bloklar"].items():
        m = bloklar.maske(ad)
        alan = m.sum() * iz.alan_m2 / 1e12
        if alan < 1.5 and rng.random() < 0.5:
            olaylar.append(BlokSikismasi(f"{ad} sıkışması", m, baslangic_ma=q["carpisma_ma"],
                                         hiz_cm_yil=float(rng.uniform(1.5, 4.0)), genislik_km=650.0))
            anlati.append(f"Küçük {ad} bloğu çarpıştıktan sonra iki kütle arasında sıkışıp bütünüyle kalınlaştı.")
    for ad, q in sorted(p["bloklar"].items(), key=lambda t: -t[1]["carpisma_ma"]):
        anlati.insert(0, f"{ad} bloğu {q['carpisma_ma'] + q['mesafe_km'] / (q['hiz_once'] * 10):.0f} milyon yıl önce "
                         f"{q['mesafe_km']:.0f} km uzaktaydı; yılda {q['hiz_once']:.1f} cm ile gelip "
                         f"{q['carpisma_ma']:.0f} milyon yıl önce {q['ortak']} bloğuna çarptı.")
    p["baslangic_ma"] = max([a.baslangic_ma for t in tarihler.values() for a in t.asamalar] + [1.0])
    return Aday(no, p, tarihler, olaylar, anlati)


def bloklari_tasi(iz_kaynak: Izgara, bl: Bloklar, iz_hedef: Izgara) -> Bloklar:
    """Blok etiketlerini başka çözünürlükteki ızgaraya en yakın kara düğümüyle taşı (adlar aynı kalır)."""
    ki = np.flatnonzero(iz_kaynak.kara)
    hi = np.flatnonzero(iz_hedef.kara)
    _, j = cKDTree(iz_kaynak.xyz[ki]).query(iz_hedef.xyz[hi])
    etiket = np.full(iz_hedef.n, -1)
    etiket[hi] = bl.etiket[ki[j]]
    return Bloklar(list(bl.adlar), etiket, bl.sabit)
