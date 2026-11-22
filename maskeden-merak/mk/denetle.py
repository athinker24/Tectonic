"""Karşılıkların hızlı denetimi: küçültülmüş maskede her karşılığın kaynakta denize ve kutu dışına düşen payı, kapsanmayan kara.
Kullanım: python3 -m mk.denetle PROJE [AD ...]"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

from .karsilik import agirlik, ornekle
from .maske import parcalar
from .proje import Proje


def denetle(p, secili=None, s=3):
    kara = p.kara(); kp = p.km_px * s
    lab, adlar = parcalar(p)
    lab = lab[::s, ::s]; kara = kara[::s, ::s]
    kaynaklar = {}; wtop = np.zeros(kara.shape, np.float32)
    for k in p.json("karsiliklar.json", []):
        ks = dict(k, bolge=[[x / s, y / s] for x, y in k["bolge"]], nokta=[[a / s, b / s, c, d] for a, b, c, d in k["nokta"]])
        if "capa_bolge" in k:
            ks["capa_bolge"] = [[x / s, y / s] for x, y in k["capa_bolge"]]
        if p.ayar.get("kure"):
            ks["_kure"] = [p.ayar["ust_enlem"], p.der_px * s]
        w = agirlik(ks, lab, adlar, kp) * kara * k.get("oncelik", 1.0)
        wtop += w
        if secili and k["ad"] not in secili:
            continue
        z, deniz = ornekle(ks, kp, w, kaynaklar)
        a = w > 0.2
        print(f"{k['ad']:<20} alan {a.sum():>7}  denizde %{100 * (deniz[a] > 0.5).mean() if a.any() else 0:4.1f}  "
              f"en yüksek {z[a].max() if a.any() else 0:5.0f} m  ortanca {np.median(z[a]) if a.any() else 0:5.0f} m", flush=True)
    bos = kara & (wtop < 0.05)
    print(f"kapsanmayan kara %{100 * bos.sum() / kara.sum():.1f}")
    if bos.any():
        L, n = ndimage.label(bos); sz = ndimage.sum(bos, L, range(1, n + 1))
        for i in np.argsort(sz)[::-1][:6]:
            ys, xs = np.nonzero(L == i + 1)
            print(f"  boşluk {int(sz[i]) * s * s} piksel, merkez x {int(xs.mean()) * s} y {int(ys.mean()) * s}")




def oturt(p, giris="karsiliklar_taslak.json", cikis="karsiliklar.json", s=4):
    """Her karşılığın kaynaktaki yerini, kaynakta denize ve kutu dışına düşen payı en aza indirecek biçimde ince ayarlar.

    Hedefteki ağırlıklı alan (bölge ∩ izinli parçalar ∩ kara) kaynağa eşlenir; kaynak tarafında küçük bir dönme, ölçek ve kayma
    taranır (karşılıktaki "oturt": {"km": 400, "aci": 25, "olcek": 0.25}; false ise dokunulmaz). En iyisi denetim noktalarının kaynak
    koordinatlarına uygulanır ve kutu kayma payı kadar genişletilir. Sonuç ve eski/yeni deniz payı yazdırılır."""
    import json
    from .karsilik import esleme, kaynak_yukle
    kara = p.kara()[::s, ::s]; kp = p.km_px * s
    lab, adlar = parcalar(p); lab = lab[::s, ::s]
    liste = p.json(giris, [])
    kaynaklar = {}; out = []
    rng = np.random.default_rng(5)
    for k in liste:
        ayar = k.get("oturt", {})
        if ayar is False:
            out.append({kk: v for kk, v in k.items() if kk != "oturt"}); continue
        tkm = ayar.get("km", 400.0); taci = ayar.get("aci", 25.0); tol = ayar.get("olcek", 0.25)
        pay = tkm / 111.0 * 1.6 + 1.0
        kutu = [k["kutu"][0] - pay, k["kutu"][1] + pay, max(k["kutu"][2] - pay, -84.0), min(k["kutu"][3] + pay, 84.0)]
        kb = dict(k, kutu=kutu, ad=k["ad"] + "#genis")
        ks = dict(kb, bolge=[[x / s, y / s] for x, y in k["bolge"]], nokta=[[a / s, b / s, c, d] for a, b, c, d in k["nokta"]])
        if p.ayar.get("kure"):
            ks["_kure"] = [p.ayar["ust_enlem"], p.der_px * s]
        w = agirlik(ks, lab, adlar, kp) * kara
        ii, jj = np.nonzero(w > 0.3)
        if len(ii) == 0:
            print(f"{k['ad']}: hedefte alan yok"); out.append(k); continue
        if len(ii) > 5000:
            sec = rng.choice(len(ii), 5000, replace=False); ii, jj = ii[sec], jj[sec]
        ll = esleme(ks, kp)(np.stack([jj.astype(float), ii.astype(float)], 1))
        K = kaynak_yukle(kb, kaynaklar)
        c0, c1 = ll[:, 0].mean(), ll[:, 1].mean(); cl = np.cos(np.radians(c1))
        X = (ll[:, 0] - c0) * 111.32 * cl; Y = (ll[:, 1] - c1) * 110.6

        def puan(a, o, tx, ty, ayrinti=False):
            r = np.radians(a)
            x = o * (X * np.cos(r) - Y * np.sin(r)) + tx; y = o * (X * np.sin(r) + Y * np.cos(r)) + ty
            lo = c0 + x / (111.32 * cl); la = c1 + y / 110.6
            dz = float((K.deniz_ornek(lo, la) > 0.5).mean())
            ceza = 0.02 * (np.hypot(tx, ty) / max(tkm, 1) + abs(a) / max(taci, 1) + abs(np.log(o)) / max(np.log(1 + tol), 1e-3))
            return (dz, dz + ceza) if ayrinti else dz + ceza

        eski = puan(0, 1, 0, 0, True)[0]
        en = (puan(0, 1, 0, 0), 0.0, 1.0, 0.0, 0.0)
        for a in np.linspace(-taci, taci, 5) if taci > 0 else [0.0]:
            for o in np.exp(np.linspace(-np.log(1 + tol), np.log(1 + tol), 5)) if tol > 0 else [1.0]:
                for tx in np.linspace(-tkm, tkm, 9):
                    for ty in np.linspace(-tkm, tkm, 9):
                        v = puan(a, o, tx, ty)
                        if v < en[0]:
                            en = (v, a, o, tx, ty)
        _, a, o, tx, ty = en
        yeni = puan(a, o, tx, ty, True)[0]
        r = np.radians(a); nk = []
        for q in k["nokta"]:
            x = (q[2] - c0) * 111.32 * cl; y = (q[3] - c1) * 110.6
            x2 = o * (x * np.cos(r) - y * np.sin(r)) + tx; y2 = o * (x * np.sin(r) + y * np.cos(r)) + ty
            nk.append([q[0], q[1], round(c0 + x2 / (111.32 * cl), 3), round(c1 + y2 / 110.6, 3)])
        k2 = {kk: v for kk, v in k.items() if kk != "oturt"}
        k2["nokta"] = nk; k2["kutu"] = [round(v, 2) for v in kutu]
        out.append(k2)
        print(f"{k['ad']:<22} deniz %{100 * eski:4.1f} → %{100 * yeni:4.1f}  dönme {a:+5.1f}°  ölçek {o:4.2f}  kayma {tx:+5.0f},{ty:+5.0f} km", flush=True)
    with open(p.yol(cikis), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "oturt":
        oturt(Proje(sys.argv[1]))
    else:
        denetle(Proje(sys.argv[1]), sys.argv[2:] or None)
