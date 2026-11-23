"""Dünya ölçeğinde rastgele kıyı maskesi: 2:1 eşdikdörtgen, 5400 × 2700 (1 piksel = 1/15 derece).
Kullanım: python3 maske_dunya.py TOHUM maske.png"""
import sys
import numpy as np
from scipy import ndimage
from PIL import Image
tohum = int(sys.argv[1]); out = sys.argv[2]
rng = np.random.default_rng(tohum)
H, W = 2700, 5400
k = 4   # gürültüyü 1/4 çözünürlükte üret, sonra büyüt
h, w = H // k, W // k
def fbm():
    t = np.zeros((h, w))
    for o, a in [(160, 1), (80, .5), (40, .28), (20, .15), (10, .08), (5, .04), (2.5, .02)]:
        g = rng.standard_normal((int(h / o) + 3, int(w / o) + 3))
        t += a * ndimage.zoom(g, o, order=3)[:h, :w]
    return t / t.std()
yy, xx = np.mgrid[0:h, 0:w].astype(float)
lat = 90 - (yy + 0.5) * 180 / h
taban = np.zeros((h, w))
for _ in range(rng.integers(9, 13)):
    cx = rng.uniform(.1, .9) * w; cy = (90 - rng.uniform(-50, 60)) / 180 * h
    a, b = rng.uniform(70, 200), rng.uniform(40, 110); t = rng.uniform(0, np.pi)
    dx, dy = xx - cx, yy - cy
    u = (dx * np.cos(t) + dy * np.sin(t)) / a; v = (-dx * np.sin(t) + dy * np.cos(t)) / b
    taban = np.maximum(taban, np.exp(-(u * u + v * v)))
kenar = np.minimum(xx, w - 1 - xx)
f = taban * 1.6 + fbm() * 0.5 - np.exp(-kenar / 25) * 2 - np.clip((np.abs(lat) - 68) / 8, 0, 3)
f = ndimage.zoom(f, k, order=3)[:H, :W]
m = f > np.quantile(f, 0.70)
L, n = ndimage.label(m); s = ndimage.sum(m, L, range(1, n + 1)); m = np.isin(L, np.nonzero(s >= 60)[0] + 1)
L, n = ndimage.label(~m); s = ndimage.sum(~m, L, range(1, n + 1)); m = ~np.isin(L, np.nonzero(s >= 300)[0] + 1)
Image.fromarray((m * 255).astype(np.uint8)).save(out)
L, n = ndimage.label(m); s = ndimage.sum(m, L, range(1, n + 1))
print("kara payı", round(m.mean(), 3), "bileşen", n, "en büyükler", sorted(s.astype(int))[::-1][:8])
