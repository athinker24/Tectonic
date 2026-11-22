"""Merak araçlarının sentetik sınaması (ağ gerekmez): kodlama gidiş dönüş, plato ölçümü, birleştirme, üslup, rehber, fark.
Önce örnek projede `python3 -m mk projeler/ornek hepsi` çalışmış olmalı (cikti/merak_16000.png). Kullanım: python3 testler/test_merak.py
"""
import json
import os
import shutil
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mk import merak  # noqa: E402
from mk.proje import Proje  # noqa: E402

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = Proje(os.path.join(KOK, "projeler", "ornek"))
K = merak.KODLAMA
W, H = p.ayar["merak_boyut"]

# 1) gidiş dönüş
m = np.array([-4000, -1995, -524, -40, -1, 1, 99, 1000, 2514, 4000, 7900], float)
geri = merak.coz(merak.kodla(m, K), K)
assert np.all(np.abs(geri - m) < np.maximum(2.0, 0.002 * np.abs(m))), geri
print("kodlama gidiş dönüş tamam")

# 2) sahte "Merak dışa aktarımı": bizim çıktı + açık okyanusta altı düz plato + sahibin bir bölgede yükselttiği kara
B = merak.oku(p.cikti(f"merak_{W}.png"))
E = B.copy()
plato_m = [4000, 1000, -1995, 2514, 99, -524]
for i, h in enumerate(plato_m):
    y, x = 600 + (i % 3) * 300, 1000 + (i // 3) * 300
    E[y:y + 120, x:x + 120] = merak.kodla(np.array(h, float), K)
y0, y1, x0, x1 = merak.kita_kutusu(p)
e = merak.coz(E[y0:y1, x0:x1], K)
blok = e.copy(); ys, xs = np.nonzero(e > 0); cy, cx = int(np.median(ys)), int(np.median(xs))
blok[cy - 200:cy + 200, cx - 200:cx + 200] = np.where(e[cy - 200:cy + 200, cx - 200:cx + 200] > 0,
                                                       e[cy - 200:cy + 200, cx - 200:cx + 200] * 1.4 + 300, e[cy - 200:cy + 200, cx - 200:cx + 200])
E[y0:y1, x0:x1] = merak.kodla(blok, K)
sahte = p.cikti("test_disa.png"); merak.yaz(sahte, E)

# 3) plato ölçümü sabitleri geri bulmalı
kaydet = p.yol("merak_kodlama.json"); eski = open(kaydet).read() if os.path.exists(kaydet) else None
try:
    K2 = merak.plato(p, sahte, plato_m)
finally:
    if eski is None:
        os.path.exists(kaydet) and os.remove(kaydet)
    else:
        open(kaydet, "w").write(eski)
assert abs(K2["S"] - K["S"]) < 30 and abs(K2["ZM"] - K["ZM"]) / K["ZM"] < 0.02, K2
assert abs(K2["DP"] - K["DP"]) < 0.02 and abs(K2["DD"] - K["DD"]) / K["DD"] < 0.05, K2
print("plato ölçümü tamam:", {k: round(v, 3) for k, v in K2.items() if isinstance(v, float)})

# 4) birleştir, üslup, rehber, fark
out = merak.birlestir(p, sahte)
assert ((out > K["S"]) != (E > K["S"]))[y0:y1, x0:x1].sum() < 0.001 * (E > K["S"]).sum()   # yalnız benek temizliği
merak.uslup(p)
merak.rehber(p)
merak.fark(p, sahte)
os.remove(sahte)
print("Merak araçları tamam")
