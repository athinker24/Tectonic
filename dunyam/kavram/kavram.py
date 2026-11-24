"""Earth Platform kavram denemesi (sahip, 2026-11-24): Dünyam'ın bir bölgesini 30 m'ye indirmek.

Bölge: Kaynak Sırası'nın güneybatı eteği ve iç deniz kıyısı; v3 merkezi (7755, 2520), 5120 × 5120 piksel, 30 m (yaklaşık
154 km). Dağ kaynağı seçimi: döndürülmüş kutunun dağ bölgesine düşen kesiminde 3 km'lik doku genliği 40 m'nin altında kalan
pay ölçüldü; Toubkal çevresi %37 (düz ova lekeleri), Orta Yüksek Atlas %0. Koordinat: atlasın kaydı (tuval = v3/4 · s + o; IoU 0,982), yani nehirler ve iklim atlasla aynı yerde.

Adımlar (hepsi adlı, AYAR'dan kapatılabilir):
1. taban: v3 (yaklaşık 3 km) bikübik büyütülür; kıyı sıfır eş eğrisinden çıkar (piksel basamağı yok).
2. doku: gerçek yükseklik (AWS z12, yaklaşık 30 m) iki kaynaktan; yüksek geçiren süzgeçle yalnız 1,5 km'den kısa dalga
   boyları alınır, kaynak doğal yönünden en az 35° döndürülür, aynalanır. Genlik, hedefin taban kabartısının kaynağın kendi
   kabartısına oranıyla ayarlanır (ova sakin, dağ güçlü). Kaynaklar yüksekliğe göre yumuşak geçişle karışır.
3. nehir: atlasın `su.json` nehirleri (debi ≥ 50 m³/s) araziye kazınır: yatak boyuna profili kaynaktan ağıza azalan,
   vadi tabanı genişliği ve derinliği debiyle artar. Önce büyük kollar, kollar ana yatağa iner.
Çıktılar `cikti/` altında (git dışında büyük olanlar): `z30.npy` (float32 m), kabartma görüntüleri."""
import json
import math
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image
from scipy import ndimage

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(KOK, "..", "..", "maskeden-merak"))
from mk import dem  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
S = 14642
R_DUNYA = 6371000.0
KAYIT = dict(sx=1.29056, sy=1.29348, ox=-541.80, oy=-213.45)   # tuval (4096 × 2048) = (v3 + 0,5)/4 · s + o
ATLAS = "/home/user/athinker24/dunyam-atlas-mobil"

AYAR = dict(
    merkez_v3=(7755, 2520), n=5120, adim_m=30.0,
    doku=True, nehir=True,
    # kaynaklar: ad, merkez (boylam, enlem), dönme (°), ayna, büyütme, hikâye bağı
    kaynaklar=[
        dict(ad="Orta Yüksek Atlas", merkez=(-6.30, 31.60), aci=57.0, ayna=False, kat=1.15,
             olay="iç deniz kıyısındaki genç yükselim (sahibin +689 m'lik düzenlemesi): ters dönmüş eski yarık kenarı"),
        dict(ad="Massif Central (Aubrac ve Margeride)", merkez=(3.05, 44.75), aci=-112.0, ayna=True, kat=1.0,
             olay="Kuzey Levhası'nın sabit iç kesimi: aşınmış eski kalkan yaylası, akarsularla yarılmış"),
    ],
    dag_esik=(1800.0, 2700.0),   # bu aralıkta Atlas dokusunun ağırlığı 0'dan 1'e çıkar
    yuksek_gecir_m=1500.0,       # dokudan alınan en uzun dalga boyu ölçeği (Gauss σ)
    kabarti_m=6000.0,            # kabartı (yerel std) penceresi
    oran_sinir=(0.25, 1.6),
    kiyi_rampa_m=600.0,          # doku kıyıdan bu uzaklığa kadar sıfırdan tama çıkar
)


def v3_ll(x, y):
    c = (np.asarray(x) + 0.5) / 4 * KAYIT["sx"] + KAYIT["ox"]; r = (np.asarray(y) + 0.5) / 4 * KAYIT["sy"] + KAYIT["oy"]
    return c / 4096 * 360 - 180, 90 - r / 2048 * 180


def ll_v3(lon, lat):
    c = (np.asarray(lon) + 180) / 360 * 4096; r = (90 - np.asarray(lat)) / 180 * 2048
    return (c - KAYIT["ox"]) / KAYIT["sx"] * 4 - 0.5, (r - KAYIT["oy"]) / KAYIT["sy"] * 4 - 0.5


class Izgara:
    """Bölgenin yerel metrik ızgarası: u doğu, v kuzey (m); satır 0 kuzey."""

    def __init__(self, a):
        self.n, self.d = a["n"], a["adim_m"]
        self.lon0, self.lat0 = (float(t) for t in v3_ll(*a["merkez_v3"]))
        k = (np.arange(self.n) - (self.n - 1) / 2) * self.d
        self.u = k[None, :]; self.v = -k[:, None]

    def ll(self, u, v):
        return (self.lon0 + np.degrees(u / (R_DUNYA * math.cos(math.radians(self.lat0)))),
                self.lat0 + np.degrees(v / R_DUNYA))

    def uv(self, lon, lat):
        return (np.radians(np.asarray(lon) - self.lon0) * R_DUNYA * math.cos(math.radians(self.lat0)),
                np.radians(np.asarray(lat) - self.lat0) * R_DUNYA)

    def px(self, lon, lat):
        u, v = self.uv(lon, lat)
        return u / self.d + (self.n - 1) / 2, -v / self.d + (self.n - 1) / 2   # (sütun, satır)


def coz(g):
    g = g.astype(np.float32)
    return np.where(g > S, 8000 * ((g - S) / (65535 - S)) ** 2, -6840 * np.clip(1 - g / S, 0, None) ** (1 / 0.607)).astype(np.float32)


def taban(iz):
    lon, lat = iz.ll(np.broadcast_to(iz.u, (iz.n, iz.n)), np.broadcast_to(iz.v, (iz.n, iz.n)))
    x, y = ll_v3(lon, lat)
    x0, y0 = int(x.min()) - 4, int(y.min()) - 4; x1, y1 = int(x.max()) + 5, int(y.max()) + 5
    G = np.asarray(Image.open(os.path.join(KOK, "..", "kaynak", "ana_v3_16k.png")))[y0:y1, x0:x1]
    z = coz(G)
    # kıyıda bikübik aşmasın diye denizi kıyıdan uzaklaştıkça derinleşen sığ bir yüzey sayarız (kıyı = sıfır eş eğrisi)
    B = ndimage.map_coordinates(z, [y - y0, x - x0], order=3, mode="nearest").astype(np.float32)
    kara_v3 = ndimage.map_coordinates((G > S).astype(np.float32), [y - y0, x - x0], order=1) > 0.5
    return B, kara_v3, (x0, y0, x1, y1)


def kaynak_doku(iz, k):
    """Kaynağı hedef ızgaraya döndürüp aynalayarak örnekler; yüksek geçiren doku ve kaynağın kabartısı."""
    a = math.radians(k["aci"]); c, s = math.cos(a), math.sin(a)
    U = np.broadcast_to(iz.u, (iz.n, iz.n)) * (-1 if k["ayna"] else 1); V = np.broadcast_to(iz.v, (iz.n, iz.n))
    ue = k["kat"] * (c * U - s * V); ve = k["kat"] * (s * U + c * V)
    lonc, latc = k["merkez"]
    lon = lonc + np.degrees(ue / (R_DUNYA * math.cos(math.radians(latc)))); lat = latc + np.degrees(ve / R_DUNYA)
    z = 12
    lo0, lo1, la0, la1 = float(lon.min()), float(lon.max()), float(lat.min()), float(lat.max())
    X0, Y1 = dem.merc(lo0, la0, z); X1, Y0 = dem.merc(lo1, la1, z)
    tx = range(int(X0 // 256), int(X1 // 256) + 1); ty = range(int(Y0 // 256), int(Y1 // 256) + 1)
    with ThreadPoolExecutor(16) as ex:
        karolar = {(i, j): t for (i, j), t in zip([(i, j) for j in ty for i in tx],
                                                  ex.map(lambda ij: dem._karo(z, ij[0], ij[1]), [(i, j) for j in ty for i in tx]))}
    M = np.vstack([np.hstack([karolar[(i, j)] for i in tx]) for j in ty]).astype(np.float32)
    mx, my = dem.merc(lon, lat, z)
    E = ndimage.map_coordinates(M, [my - ty[0] * 256 - 0.5, mx - tx[0] * 256 - 0.5], order=1).astype(np.float32)
    s_hp = AYAR["yuksek_gecir_m"] / iz.d
    L = ndimage.gaussian_filter(E, s_hp)
    d = E - L
    return d, yerel_kabarti(L, iz), E


def yerel_kabarti(L, iz):
    s = AYAR["kabarti_m"] / iz.d
    m = ndimage.gaussian_filter(L, s); m2 = ndimage.gaussian_filter(L * L, s)
    return np.sqrt(np.maximum(m2 - m * m, 1.0))


def doku_ekle(iz, B, kara):
    rB = yerel_kabarti(ndimage.gaussian_filter(B, AYAR["yuksek_gecir_m"] / iz.d), iz)
    Bs = ndimage.gaussian_filter(B, 3000 / iz.d)
    e0, e1 = AYAR["dag_esik"]
    t = np.clip((Bs - e0) / (e1 - e0), 0, 1); w_dag = t * t * (3 - 2 * t)
    toplam = np.zeros_like(B); bilgi = []
    for k, w in zip(AYAR["kaynaklar"], (w_dag, 1 - w_dag)):
        d, rK, _ = kaynak_doku(iz, k)
        # yüksek yerde taban düz kalsa bile doku sönmesin (Merak'ta düzleşmiş 3000 m üstü platolar)
        tt = np.clip((Bs - 1500) / 1500, 0, 1); alt = AYAR["oran_sinir"][0] + 0.75 * tt * tt * (3 - 2 * tt)
        oran = np.clip(rB / rK, alt, AYAR["oran_sinir"][1])
        toplam += w * oran * d
        bilgi.append((k["ad"], float(np.percentile(np.abs(d), 90)), float(np.median(oran))))
    toplam /= np.sqrt(w_dag ** 2 + (1 - w_dag) ** 2)        # iki ilgisiz dokunun karışımı genliği düşürmesin
    uz = ndimage.distance_transform_edt(kara) * iz.d
    rampa = np.clip(uz / AYAR["kiyi_rampa_m"], 0, 1)
    Z = np.where(kara, np.maximum(B + rampa * toplam, 1.0 + 0.02 * np.minimum(uz, 500)), np.minimum(B, -1.0))
    return Z.astype(np.float32), bilgi, w_dag


def nehirler(iz, Z, kara):
    """Atlas nehirlerini kazır. Döner: yeni Z, nehir maskesi, özet."""
    su = json.load(open(os.path.join(ATLAS, "data", "su.json")))
    liste = []
    for n in su["nehirler"]:
        p = np.cumsum(np.array(n["p"], float).reshape(-1, 2), 0) / 100       # ağızdan kaynağa
        q = 10 ** (np.array(n["q"], float) / 10)
        c, r = iz.px(p[:, 0], p[:, 1])
        icinde = (c > -50) & (c < iz.n + 50) & (r > -50) & (r < iz.n + 50)
        if icinde.sum() >= 2:
            liste.append((n["k"], c, r, q))
    liste.sort(key=lambda t: t[0])                          # büyük kollar önce
    yatak = np.full(Z.shape, np.nan, np.float32); genis = np.zeros(Z.shape, np.float32)
    Zs = ndimage.gaussian_filter(Z, 2)
    puruz = Z - ndimage.gaussian_filter(Z, 10)                  # 300 m'den kısa doku; vadi tabanına kısmen geri konur
    rng = np.random.default_rng(7)
    ozet = []
    for kd, c, r, q in liste:
        # 30 m adımla sıkılaştır (ağızdan kaynağa)
        seg = np.hypot(np.diff(c), np.diff(r)); t = np.concatenate([[0], np.cumsum(seg)])
        tt = np.arange(0, t[-1], 1.0)
        cc = np.interp(tt, t, c); rr = np.interp(tt, t, r); qq = np.interp(tt, t, q)
        ic = (cc >= 0) & (cc < iz.n - 1) & (rr >= 0) & (rr < iz.n - 1)
        if ic.sum() < 30:
            continue
        cc, rr, qq = cc[ic], rr[ic], qq[ic]
        # atlas çizgisi 30 m'de düz parçalı: yatak, dalga boyu yaklaşık 4 km, genliği debiyle artan kıvrımlarla oynatılır
        tc = np.gradient(ndimage.gaussian_filter1d(cc, 20)); tr = np.gradient(ndimage.gaussian_filter1d(rr, 20))
        nb = np.hypot(tc, tr) + 1e-9
        gen = (4 + 4 * np.log10(np.maximum(qq, 50) / 50))
        kay = ndimage.gaussian_filter1d(rng.standard_normal(len(cc)), 25); kay /= kay.std() + 1e-9
        kay *= np.minimum(np.minimum(np.arange(len(cc)), np.arange(len(cc))[::-1]) / 60, 1)   # uçlar yerinde kalsın
        cc = np.clip(cc + kay * gen * (-tr / nb), 0, iz.n - 1.001); rr = np.clip(rr + kay * gen * (tc / nb), 0, iz.n - 1.001)
        h = ndimage.map_coordinates(Zs, [rr, cc], order=1)
        var = ~np.isnan(yatak[rr.astype(int), cc.astype(int)])     # daha önce kazınmış yatak (ana kol)
        h = np.where(var, yatak[rr.astype(int), cc.astype(int)], h)
        h = ndimage.gaussian_filter1d(h, 100)                    # yaklaşık 3 km boyunca yumuşat
        # kaynaktan ağıza azalan profil: tersinden birikimli en küçük
        prof = np.minimum.accumulate(h[::-1])[::-1]
        derin = 3 + 2.5 * np.log10(np.maximum(qq, 50) / 50)       # yatak derinliği, m
        b = np.maximum(prof - derin, 0.5)
        b = np.where(var, np.minimum(b, yatak[rr.astype(int), cc.astype(int)]), b)
        ii, jj = np.round(rr).astype(int), np.round(cc).astype(int)
        mev = yatak[ii, jj]
        yatak[ii, jj] = np.where(np.isnan(mev), b, np.minimum(mev, b))
        gur = 1 + 0.45 * ndimage.gaussian_filter1d(rng.standard_normal(len(qq)), 60) * 6   # genişlik boyunca değişsin
        genis[ii, jj] = np.maximum(genis[ii, jj], np.clip(gur, 0.4, 1.8) * (40 + 120 * np.log10(np.maximum(qq, 50) / 50) ** 1.3))
        ozet.append(dict(kademe=kd, boy_km=round(len(cc) * iz.d / 1000, 1), debi=int(qq.max()),
                         kazi_m_ortanca=round(float(np.median(np.maximum(ndimage.map_coordinates(Z, [rr, cc], order=1) - b, 0))), 1)))
    maske = ~np.isnan(yatak)
    if not maske.any():
        return Z, maske, ozet
    dist, (iy, ix) = ndimage.distance_transform_edt(~maske, return_indices=True)
    dm = dist * iz.d
    by = yatak[iy, ix]; w = genis[iy, ix]
    # vadi: taban yarı genişliği w, sonra ~6° duvar, 2 km ötede araziye katılır
    vadi = by + np.where(dm <= w, 0.0, (dm - w) * 0.10 + ((dm - w) / 800) ** 2 * 40)
    vadi = vadi + puruz * (0.15 + 0.85 * np.clip((dm - w) / 300, 0, 1))
    kk = 40.0                                                    # yumuşak en küçük: vadi kenarı kırılmasın
    hh = np.maximum(kk - np.abs(Z - vadi), 0) / kk
    yumin = np.minimum(Z, vadi) - hh * hh * kk / 4
    yeni = np.where(kara & (dm < 4000), np.maximum(yumin, 0.5), Z)
    return yeni.astype(np.float32), maske, ozet


def golge(z, d, azim=315, alt=40, abart=1.0):
    gy, gx = np.gradient(z * abart, d)
    a, e = math.radians(azim), math.radians(alt)
    nx, ny = -gx, gy
    nz = np.ones_like(z)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    lx, ly, lz = math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)
    return np.clip((nx * lx + ny * ly + nz * lz) / n, 0, 1)


def renk(z, d, nehir=None):
    sh = golge(z, d)
    t = np.clip(z / 4000, 0, 1)[..., None]
    alcak = np.array([0.42, 0.55, 0.33]); orta = np.array([0.72, 0.66, 0.50]); yuksek = np.array([0.95, 0.95, 0.95])
    c = np.where(t < 0.5, alcak + (orta - alcak) * (t / 0.5), orta + (yuksek - orta) * ((t - 0.5) / 0.5))
    rgb = c * (0.35 + 0.75 * sh[..., None])
    rgb[z <= 0] = [0.22, 0.38, 0.58]
    if nehir is not None:
        rgb[nehir] = [0.15, 0.35, 0.75]
    return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)


def main():
    out = os.path.join(KOK, "cikti"); os.makedirs(out, exist_ok=True)
    iz = Izgara(AYAR)
    B, kara, kutu = taban(iz)
    kara = B > 0
    print(f"merkez {iz.lon0:.3f}, {iz.lat0:.3f}; taban v3 kutusu {kutu}; kara payı {kara.mean():.2f}; "
          f"taban yükseklik %5/50/95 {np.percentile(B[kara], [5, 50, 95]).round()}")
    Z = B.copy(); w_dag = None
    if AYAR["doku"]:
        Z, bilgi, w_dag = doku_ekle(iz, B, kara)
        for b in bilgi:
            print(f"doku {b[0]}: |yüksek geçiren| %90 {b[1]:.0f} m, genlik oranı ortanca {b[2]:.2f}")
    nm = None
    if AYAR["nehir"]:
        Z, nm, ozet = nehirler(iz, Z, kara)
        print(f"nehir {len(ozet)} kol:", ozet)
    np.save(os.path.join(out, "z30.npy"), Z)
    np.save(os.path.join(out, "taban30.npy"), B)
    print(f"sonuç %5/50/95/en çok {np.percentile(Z[kara], [5, 50, 95]).round()} {Z.max():.0f}; "
          f"taban ile kıyı farkı {int(((Z > 0) != kara).sum())} piksel")
    # görüntüler: genel (1/2), taban ile karşılaştırma, üç yakın plan (tam çözünürlük, 1024 piksel = 30 km)
    Image.fromarray(renk(Z, iz.d, nm)[::2, ::2]).save(os.path.join(out, "genel.png"))
    yan = np.hstack([renk(B, iz.d)[::4, ::4], np.full((iz.n // 4, 8, 3), 255, np.uint8), renk(Z, iz.d, nm)[::4, ::4]])
    Image.fromarray(yan).save(os.path.join(out, "taban_sonuc.png"))
    return iz, B, Z, nm


if __name__ == "__main__":
    main()
