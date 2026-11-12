"""Katman 1: aday tarih üretici.

Her aday, blokların aşamalı hareketleri ve bunlardan türeyen olaylardan
oluşur. Sert kısıtları (çakışma, hız, geçit) bozan aday atılır. Kalanlar
istekleri ne kadar sağladıklarına ve birbirlerinden ne kadar farklı
olduklarına göre seçilir (kalite ve çeşitlilik: MAP-Elites benzeri arşiv,
ardından en uzak noktalarla açgözlü seçim; arastirma/10).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

import numpy as np
from scipy.spatial import cKDTree

from . import kure
from .bloklar import Bloklar
from .izgara import Izgara, _lonlat_xyz, buyuk_daire_km
from .olaylar import AIRY, H0_M, BlokSikismasi, Carpisma
from .paleo import konumlar
from .tarih import Asama, BlokTarihi, hareket_kutbu

HIZ_SINIRI_CM_YIL = 6.0  # Müller 2022 kıtasal hız kuralı (arastirma/09)


@dataclass
class Aday:
    no: int
    parametre: dict
    tarihler: dict[str, BlokTarihi]
    olaylar: list
    anlati: list[str] = field(default_factory=list)
    ihlaller: list[str] = field(default_factory=list)
    istek_sonuc: dict = field(default_factory=dict)  # istek no -> (sağlandı mı, ölçülen, hedef metni)
    h: np.ndarray | None = None

    @property
    def gecerli(self) -> bool:
        return not self.ihlaller

    def saglanan(self) -> set[int]:
        return {k for k, v in self.istek_sonuc.items() if v[0]}


def _merkez(iz: Izgara, maske: np.ndarray) -> tuple[float, float]:
    v = iz.xyz[maske].mean(axis=0)
    v /= np.linalg.norm(v)
    lon, lat = kure.xyz_lonlat(v)
    return float(lon), float(lat)


ARALIK = {
    "carpisma_ma": (25, 65), "okyanus_km": (600, 2500), "hiz_once": (3.5, 7.0), "hiz_sonra": (2.0, 5.0),
    "yon": (-25, 25), "plato_km": (400, 900), "plato_hmax_km": (42.0, 46.0),
    "gb_hiz": (0.5, 2.0), "gb_yon": (-10, 70), "gb_baslangic_ma": (30, 80),
    "ta_ma": (6, 25), "ta_hiz": (1.5, 4.5), "ta_sapma": (-20, 20),
    "ya_ma": (5, 40), "ya_hiz": (1.0, 4.0), "ya_yon": (-130, -50), "ya_mesafe_km": (100, 800),
}
TURLER = {"gb_tur": ["sabit", "yaklasan"], "ta_tur": ["kuzeye", "doguya", "batiya"], "ya_tur": ["alp", "apenin"]}


def bolge_maske(iz: Izgara, bolge) -> np.ndarray:
    """İstek bölgesi: iki köşeli kutu [[b, g], [d, k]] ya da çokgen [[lon, lat], ...]."""
    if len(bolge) == 2:
        (b, g), (d, k) = bolge
        return iz.kara & (iz.lon >= b) & (iz.lon <= d) & (iz.lat >= g) & (iz.lat <= k)
    return iz.kara & kure.cokgen_ici(iz.xyz, np.asarray(bolge, float))


def omurga_maske(iz: Izgara, blok: np.ndarray, yari_km: float = 130.0) -> tuple[np.ndarray, np.ndarray]:
    """Bloğun uzun ekseni (teğet düzlemde temel bileşen) ve çevresindeki şerit."""
    from .olaylar import isaretli_uzaklik_km
    v = iz.xyz[blok]
    m = v.mean(axis=0); m /= np.linalg.norm(m)
    e1 = np.cross([0.0, 0.0, 1.0], m); e1 /= np.linalg.norm(e1); e2 = np.cross(m, e1)
    q = np.c_[v @ e1, v @ e2]
    _, _, vt = np.linalg.svd(q - q.mean(0), full_matrices=False)
    t = (q - q.mean(0)) @ vt[0]
    uc = [q.mean(0) + a * vt[0] for a in (np.percentile(t, 3), np.percentile(t, 97))]
    cizgi = []
    for u in uc:
        w = m + u[0] * e1 + u[1] * e2; w /= np.linalg.norm(w)
        cizgi.append(kure.xyz_lonlat(w))
    cizgi = np.array([[float(a), float(b)] for a, b in cizgi])
    d = np.full(iz.n, np.inf)
    d[iz.kara] = np.abs(isaretli_uzaklik_km(iz, cizgi, iz.kara))
    return blok & (d < yari_km), cizgi


def parametre_ornekle(rng: np.random.Generator) -> dict:
    p = {k: float(rng.uniform(*v)) for k, v in ARALIK.items()}
    p.update({k: str(rng.choice(v)) for k, v in TURLER.items()})
    return p


def mutasyon(p: dict, rng: np.random.Generator, olcek: float = 0.12) -> dict:
    """Sürekli değerlere aralığın %12'si kadar gürültü; arada bir tür değişimi."""
    q = dict(p)
    for k, (a, b) in ARALIK.items():
        q[k] = float(np.clip(q[k] + rng.normal(0, olcek * (b - a)), a, b))
    for k, v in TURLER.items():
        if rng.random() < 0.15:
            q[k] = str(rng.choice(v))
    return q


def aday_kur(no: int, rng: np.random.Generator, iz: Izgara, bloklar: Bloklar, senaryo: dict,
             p: dict | None = None) -> Aday:
    """Test senaryosuna özgü olay şablonları. Sahibin maskesi gelince bu şablon
    senaryo dosyasından okunacak biçimde genelleştirilecek."""
    p = dict(p) if p is not None else parametre_ornekle(rng)
    tarihler: dict[str, BlokTarihi] = {}
    olaylar: list = []
    anlati: list[str] = []
    gd = bloklar.maske("Güneydoğu")
    gd_m = _merkez(iz, gd)

    # Güneydoğu: okyanus kapanır, sonra çarpışır ve kuzeye itmeyi sürdürür.
    once_myr = p["okyanus_km"] / (p["hiz_once"] * 10.0)
    p["baslangic_ma"] = p["carpisma_ma"] + once_myr
    lo, la, w1 = hareket_kutbu(gd_m, p["yon"], p["hiz_once"])
    _, _, w2 = hareket_kutbu(gd_m, p["yon"], p["hiz_sonra"])
    tarihler["Güneydoğu"] = BlokTarihi("Güneydoğu", [
        Asama(p["baslangic_ma"], p["carpisma_ma"], lo, la, w1),
        Asama(p["carpisma_ma"], 0.0, lo, la, w2),
    ])
    dikis = next(d for d in senaryo["dikisler"] if d["ad"] == "Duvar dikişi")
    cephe = np.array(dikis["cizgi"], float)
    plato_istek = next((i for i in senaryo.get("istekler", []) if i["tur"] == "plato" and len(i["bolge"]) > 2), None)
    plato_m = bolge_maske(iz, plato_istek["bolge"]) if plato_istek else None
    # dikişe dik yakınsama: hızın kuzey bileşeni
    yakinsama = p["hiz_sonra"] * np.cos(np.radians(p["yon"]))
    olaylar.append(Carpisma("Büyük çarpışma", cephe, ust_sol=True, baslangic_ma=p["carpisma_ma"],
                            hiz_cm_yil=yakinsama, kusak_km=280.0, plato_km=p["plato_km"],
                            kusak_hmax_m=70_000.0, plato_hmax_m=p["plato_hmax_km"] * 1e3,
                            plato_maske=plato_m, kusak_k_carpani=p.get("kusak_sertlik", 1.0)))
    anlati.append(
        f"Güneydoğu bloğu neden kuzeye dayandı? Yaklaşık {p['baslangic_ma']:.0f} milyon yıl önce aradaki "
        f"{p['okyanus_km']:.0f} km'lik okyanusu yılda {p['hiz_once']:.1f} cm ile kapatmaya başladı; "
        f"{p['carpisma_ma']:.0f} milyon yıl önce kuzeydeki ana karaya çarptı."
    )
    anlati.append(
        f"Büyük doğu batı sıradağı nereden geldi? Çarpışmadan beri blok yılda {p['hiz_sonra']:.1f} cm ile "
        f"itmeyi sürdürüyor; dikiş hattında kabuk kalınlaştı, sıradağ ve arkasında "
        + ("sahibin çizdiği çanak bölgesine yayılan bir plato yükseldi." if plato_m is not None
           else f"{p['plato_km']:.0f} km genişliğe kadar yayılan bir plato yükseldi.")
    )

    # Güneybatı: ya yerinde kalır ya da yavaşça yaklaşır.
    if p["gb_tur"] == "yaklasan":
        gbm = _merkez(iz, bloklar.maske("Güneybatı"))
        lo, la, w = hareket_kutbu(gbm, p["gb_yon"], p["gb_hiz"])
        tarihler["Güneybatı"] = BlokTarihi("Güneybatı", [Asama(p["gb_baslangic_ma"], 0.0, lo, la, w)])
        anlati.append(
            f"Güneybatı kıtası? {p['gb_baslangic_ma']:.0f} milyon yıldır yılda {p['gb_hiz']:.1f} cm ile "
            f"kuzeydoğuya kayıyor; batıdaki kara köprüsü bu yaklaşmanın sonucu."
        )
    else:
        anlati.append("Güneybatı kıtası? Bu tarihte kuzeye göre yerinde; batıdaki kara köprüsü eski bir bağlantı.")

    # Yarımada: Güneybatı ile birlikte gider; Alp türünde önce doğudan yaklaşıp kökünden çarpar,
    # Apenin türünde omurgası boyunca dar ve orta yükseklikte bir kuşak gelişir.
    if "Yarımada" in bloklar.adlar:
        ya = bloklar.maske("Yarımada")
        ortak = list(tarihler["Güneybatı"].asamalar) if "Güneybatı" in tarihler else []
        if p["ya_tur"] == "alp":
            yd = next(d for d in senaryo["dikisler"] if d["ad"] == "Yarımada dikişi")
            once = p["ya_mesafe_km"] / (p["ya_hiz"] * 10.0)
            lo, la, w1 = hareket_kutbu(_merkez(iz, ya), p["ya_yon"], p["ya_hiz"])
            tarihler["Yarımada"] = BlokTarihi("Yarımada", ortak + [
                Asama(p["ya_ma"] + once, p["ya_ma"], lo, la, w1),
                Asama(p["ya_ma"], 0.0, lo, la, 0.4 * w1),
            ])
            olaylar.append(Carpisma("Yarımada çarpışması (Alp türü)", np.array(yd["cizgi"], float), ust_sol=True,
                                    baslangic_ma=p["ya_ma"], hiz_cm_yil=0.4 * p["ya_hiz"] + 0.6, kusak_km=200.0,
                                    plato_km=0.0, kusak_hmax_m=62_000.0))
            anlati.append(
                f"Yarımada nasıl oluştu (Alp türü)? {p['ya_ma'] + once:.0f} milyon yıl önce ayrı bir kıta parçasıydı; "
                f"aradaki {p['ya_mesafe_km']:.0f} km'lik denizi yılda {p['ya_hiz']:.1f} cm ile kapatıp "
                f"{p['ya_ma']:.0f} milyon yıl önce güneybatı kıtasına kökünden çarptı; kökte yüksek ve geniş bir sıradağ yükseldi.")
        else:
            om, _ = omurga_maske(iz, ya)
            if ortak:
                tarihler["Yarımada"] = BlokTarihi("Yarımada", ortak)
            olaylar.append(BlokSikismasi("Yarımada omurgası (Apenin türü)", om, baslangic_ma=p["ya_ma"],
                                         hiz_cm_yil=p["ya_hiz"], genislik_km=400.0, hmax_m=50_000.0))
            anlati.append(
                f"Yarımada nasıl oluştu (Apenin türü)? Güneybatı kıtasının bir uzantısı; {p['ya_ma']:.0f} milyon yıldır "
                f"kenarındaki dalan levha geri çekiliyor ve omurgası boyunca yılda {p['ya_hiz']:.1f} cm'lik kısalmayla "
                f"dar, orta yükseklikte bir sıradağ büyüyor.")

    # Takımada: iki levha arasında sıkışan mikro kıta.
    ta = bloklar.maske("Takımada")
    yon = {"kuzeye": 0.0, "doguya": 90.0, "batiya": -90.0}[p["ta_tur"]] + p["ta_sapma"]
    tam = _merkez(iz, ta)
    lo, la, w = hareket_kutbu(tam, yon, p["ta_hiz"])
    tarihler["Takımada"] = BlokTarihi("Takımada", [Asama(p["ta_ma"] + 8.0, 0.0, lo, la, w)])
    olaylar.append(BlokSikismasi("Mikro kıta sıkışması", ta, baslangic_ma=p["ta_ma"],
                                 hiz_cm_yil=p["ta_hiz"], genislik_km=650.0))
    kime = {"kuzeye": "kuzeydeki ana karanın kıyısına", "doguya": "güneydoğu bloğunun batı kıyısına",
            "batiya": "güneybatı kıtasının kıyısına"}[p["ta_tur"]]
    anlati.append(
        f"İç denizdeki mikro kıta neden baştan sona dağlık? {p['ta_ma']:.0f} milyon yıl önce {kime} "
        f"sıkıştı; yılda {p['ta_hiz']:.1f} cm'lik itmeyle bütün blok kalınlaştı (Yeni Gine ve Tayvan benzeri)."
    )
    return Aday(no, p, tarihler, olaylar, anlati)


def kisitlari_denetle(aday: Aday, iz: Izgara, bloklar: Bloklar, senaryo: dict, adim_myr: float = 2.0) -> None:
    ihlal = []
    kara = iz.kara
    hucre = iz.hucre_km / 6371.0
    # hız
    for ad, t in aday.tarihler.items():
        m = bloklar.maske(ad)
        for a in t.asamalar:
            v = np.linalg.norm(kure.hiz_cm_yil(a.kutup_lon, a.kutup_lat, a.hiz_derece_myr, iz.xyz[m]), axis=1)
            if v.max() > HIZ_SINIRI_CM_YIL + 1e-6:
                ihlal.append(f"hız: {ad} {v.max():.1f} cm/yıl (sınır {HIZ_SINIRI_CM_YIL})")
                break
    # çakışma ve geçitler
    en_eski = max(a.baslangic_ma for t in aday.tarihler.values() for a in t.asamalar)
    zamanlar = np.arange(0.0, en_eski + adim_myr, adim_myr)
    gecitler = senaryo.get("gecitler", [])
    for ma in zamanlar[1:]:
        p = konumlar(iz, bloklar, aday.tarihler, ma)
        agaclar = {ad: cKDTree(p[bloklar.maske(ad)]) for ad in bloklar.adlar}
        for a, b in combinations(bloklar.adlar, 2):
            d, _ = agaclar[b].query(p[bloklar.maske(a)], distance_upper_bound=0.5 * hucre)
            binen = int(np.isfinite(d).sum())
            if binen > 3:
                ihlal.append(f"çakışma: {ma:.0f} milyon yıl önce {a} ile {b} üst üste ({binen} düğüm)")
        for g in gecitler:
            a, b = g["bloklar"]
            merkez = _lonlat_xyz(np.array(float(g["nokta"][0])), np.array(float(g["nokta"][1])))
            r = g["yaricap_km"] / 6371.0
            pa = p[bloklar.maske(a)]
            pb = p[bloklar.maske(b)]
            pa = pa[np.linalg.norm(pa - merkez, axis=1) < r]
            pb = pb[np.linalg.norm(pb - merkez, axis=1) < r]
            if len(pa) and len(pb):
                d, _ = cKDTree(pb).query(pa)
                en_az = float(d.min() * 6371.0)
                if en_az < g["en_az_km"]:
                    ihlal.append(f"geçit: {g['ad']} {ma:.0f} milyon yıl önce {en_az:.0f} km'ye daraldı (en az {g['en_az_km']})")
        if len(ihlal) > 6:
            break
    # aynı türden ihlalleri tekrarlama
    goruldu, sade = set(), []
    for x in ihlal:
        k = x.split(" ")[0] + x.split(" ")[-1] if x.startswith("hız") else " ".join(x.split()[:1] + x.split()[4:7])
        if k not in goruldu:
            goruldu.add(k)
            sade.append(x)
    aday.ihlaller = sade


def kabuk_tahmini(aday: Aday, iz: Izgara, dt_myr: float = 0.5, asinma_kabuk_m_myr: float = 0.0) -> np.ndarray:
    """Aşınmasız hızlı tarama: olayların bugüne kadar biriktirdiği kabuk kalınlığı."""
    from .gurultu import fbm
    g = fbm(iz.xyz, 1500.0, 200.0, tohum=aday.no)
    for o in aday.olaylar:
        o.hazirla(iz, g)
    en_eski = max(o.baslangic_ma for o in aday.olaylar)
    h = np.full(iz.n, H0_M)
    idx = np.flatnonzero(iz.kara)
    for ma in np.arange(en_eski, 0.0, -dt_myr):
        r = sum(o.kalinlasma(ma, h) for o in aday.olaylar)
        h[idx] += r * dt_myr * 1e6
    return h


def istekleri_olc(aday: Aday, iz: Izgara, bloklar: Bloklar, senaryo: dict) -> None:
    h = aday.h
    sonuc = {}
    for ist in senaryo.get("istekler", []):
        if ist["tur"] in ("kusak", "plato"):
            m = bolge_maske(iz, ist["bolge"])
        if ist["tur"] == "kusak":
            olc = float(np.percentile(h[m], 95) / 1e3)
            sonuc[ist["no"]] = (olc >= ist["kabuk_km_en_az"], round(olc, 1), f"kabuk %95 ≥ {ist['kabuk_km_en_az']} km")
        elif ist["tur"] == "plato":
            z = float(np.median((h[m] - H0_M) * AIRY))
            lo, hi = ist["yukseklik_m"]
            sonuc[ist["no"]] = (lo <= z <= hi, round(z), f"izostatik yükseklik ortancası {lo} ile {hi} m")
        elif ist["tur"] == "yarimada":
            ya = bloklar.maske(ist["blok"])
            if aday.parametre.get("ya_tur") == "alp":
                from .olaylar import isaretli_uzaklik_km
                yd = next(d for d in senaryo["dikisler"] if d["ad"] == "Yarımada dikişi")
                u = np.full(iz.n, np.inf)
                u[iz.kara] = np.abs(isaretli_uzaklik_km(iz, np.array(yd["cizgi"], float), iz.kara))
                olc = float(np.percentile(h[ya & (u < 300)], 95) / 1e3)
                sonuc[ist["no"]] = (olc >= 55, round(olc, 1), "Alp türü: kökte kabuk %95 ≥ 55 km")
            else:
                om, _ = omurga_maske(iz, ya)
                olc = float(np.percentile(h[om], 90) / 1e3)
                sonuc[ist["no"]] = (42 <= olc <= 52, round(olc, 1), "Apenin türü: omurgada kabuk %90 42 ile 52 km")
        elif ist["tur"] == "dagli_blok":
            m = bloklar.maske(ist["blok"])
            pay = float(np.mean(h[m] >= ist["kabuk_km_en_az"] * 1e3))
            sonuc[ist["no"]] = (pay >= ist["pay_en_az"], round(pay, 2), f"kabuğu ≥ {ist['kabuk_km_en_az']} km olan pay ≥ {ist['pay_en_az']}")
    aday.istek_sonuc = sonuc


def _ozellik(a: Aday) -> np.ndarray:
    p = a.parametre
    return np.array([
        p["carpisma_ma"] / 40.0, p["hiz_sonra"] / 3.0, p["yon"] / 25.0, p["plato_km"] / 500.0,
        p["ta_ma"] / 20.0, {"kuzeye": 0, "doguya": 1, "batiya": 2}[p["ta_tur"]] * 1.0,
        1.0 if p["gb_tur"] == "yaklasan" else 0.0,
        2.0 if p.get("ya_tur") == "alp" else 0.0, p.get("ya_ma", 0.0) / 20.0,
    ])


def cesitli_sec(adaylar: list[Aday], k: int = 5) -> list[Aday]:
    """Önce MAP-Elites benzeri arşiv: (çarpışma zamanı dilimi, mikro kıta türü,
    güneybatı türü) hücresi başına en çok isteği sağlayan aday. Sonra arşivden
    en uzak noktalarla açgözlü seçim (k-DPP'ye basit yaklaşım)."""
    arsiv: dict = {}
    for a in adaylar:
        p = a.parametre
        hucre = (int((p["carpisma_ma"] - 25) // 10), p["ta_tur"], p["gb_tur"], p.get("ya_tur"))
        puan = len(a.saglanan())
        if hucre not in arsiv or puan > len(arsiv[hucre].saglanan()):
            arsiv[hucre] = a
    havuz = list(arsiv.values())
    if not havuz:
        return []
    en_iyi = max(len(a.saglanan()) for a in havuz)
    havuz = [a for a in havuz if len(a.saglanan()) == en_iyi] or havuz
    F = np.array([_ozellik(a) for a in havuz])
    secilen = [int(np.argmax([len(a.saglanan()) for a in havuz]))]
    while len(secilen) < min(k, len(havuz)):
        d = np.min(np.linalg.norm(F[:, None, :] - F[secilen][None, :, :], axis=2), axis=1)
        d[secilen] = -1
        secilen.append(int(np.argmax(d)))
    return [havuz[i] for i in secilen]


def celiskiler(adaylar: list[Aday], istek_nolari: list[int]) -> dict:
    """İstekler geçerli adaylarla birlikte sağlanabiliyor mu; değilse en küçük
    çelişen kümeyi (silme süzgeci, arastirma/16) ve her isteğin en iyi
    ulaşılan değerini döner. Hiçbir isteği kendiliğinden gevşetmez."""
    gecerli = [a for a in adaylar if a.gecerli]

    def saglanir(kume) -> bool:
        return any(set(kume) <= a.saglanan() for a in gecerli)

    if saglanir(istek_nolari):
        return {"celiski": False}
    kume = list(istek_nolari)
    for x in list(kume):
        dene = [y for y in kume if y != x]
        if dene and not saglanir(dene):
            kume = dene
    en_iyi = {}
    for no in istek_nolari:
        degerler = [a.istek_sonuc[no][1] for a in gecerli if no in a.istek_sonuc]
        if degerler:
            en_iyi[no] = (min(degerler), max(degerler))
    return {"celiski": True, "en_kucuk_celisen_kume": kume, "ulasilan_aralik": en_iyi}


def evrimlestir(iz: Izgara, bloklar: Bloklar, senaryo: dict, tohum_sayisi: int = 200,
                nesil: int = 6, nesil_boyu: int = 100, tohum: int = 42, gunluk=print) -> list[Aday]:
    """Rastgele tohumlar, sonra geçerli adaylardan mutasyonla yeni adaylar
    (MAP-Elites benzeri: ebeveynler arşiv hücrelerinden eşit seçilir)."""
    rng = np.random.default_rng(tohum)
    tum: list[Aday] = []

    def degerlendir(p):
        a = aday_kur(len(tum), rng, iz, bloklar, senaryo, p)
        kisitlari_denetle(a, iz, bloklar, senaryo)
        if a.gecerli:
            a.h = kabuk_tahmini(a, iz)
            istekleri_olc(a, iz, bloklar, senaryo)
        tum.append(a)

    for _ in range(tohum_sayisi):
        degerlendir(None)
    gunluk(f"tohum: {tohum_sayisi} aday, {sum(a.gecerli for a in tum)} geçerli")
    for g in range(nesil):
        gecerli = [a for a in tum if a.gecerli]
        if not gecerli:
            for _ in range(nesil_boyu):
                degerlendir(None)
            continue
        hucreler: dict = {}
        for a in gecerli:
            p = a.parametre
            hucreler.setdefault((int((p["carpisma_ma"] - 25) // 10), p["ta_tur"], p["gb_tur"], p.get("ya_tur")), []).append(a)
        anahtarlar = list(hucreler)
        for _ in range(nesil_boyu):
            h = hucreler[anahtarlar[rng.integers(len(anahtarlar))]]
            ebeveyn = h[rng.integers(len(h))]
            degerlendir(mutasyon(ebeveyn.parametre, rng))
        gunluk(f"nesil {g + 1}: toplam {len(tum)}, geçerli {sum(a.gecerli for a in tum)}, arşiv hücresi {len(hucreler)}")
    return tum
