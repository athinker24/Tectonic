"""Gerçek yükseklik verisi: AWS Terrain Tiles (terrarium kodlaması), Web Mercator karoları.

yukseklik = R * 256 + G + B / 256 - 32768 (m). Karolar kaynak/karolar/ altında önbelleğe alınır.
"""
import io
import math
import os
import urllib.request

import numpy as np
from PIL import Image
from scipy import ndimage

URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
ONBELLEK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kaynak", "karolar")


def _karo(z, x, y):
    yol = os.path.join(ONBELLEK, str(z), str(x), f"{y}.png")
    if not os.path.exists(yol):
        os.makedirs(os.path.dirname(yol), exist_ok=True)
        for deneme in range(4):
            try:
                with urllib.request.urlopen(URL.format(z=z, x=x, y=y), timeout=60) as r:
                    veri = r.read()
                break
            except Exception:
                if deneme == 3:
                    raise
        with open(yol, "wb") as f:
            f.write(veri)
    a = np.asarray(Image.open(yol).convert("RGB"), float)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def merc(lon, lat, z):
    n = 2 ** z * 256
    x = (np.asarray(lon) + 180.0) / 360.0 * n
    la = np.radians(np.clip(lat, -85, 85))
    y = (1 - np.log(np.tan(la) + 1 / np.cos(la)) / math.pi) / 2 * n
    return x, y


class Kaynak:
    """Bir enlem boylam kutusunun mozaiği; (boylam, enlem) noktalarında örnekleme."""

    def __init__(self, lon0, lon1, lat0, lat1, z=6):
        self.z = z
        x0, y1 = merc(lon0, lat0, z); x1, y0 = merc(lon1, lat1, z)
        self.tx0, self.tx1 = int(x0 // 256), int(x1 // 256)
        self.ty0, self.ty1 = int(y0 // 256), int(y1 // 256)
        satirlar = []
        for ty in range(self.ty0, self.ty1 + 1):
            satirlar.append(np.hstack([_karo(z, tx % 2 ** z, ty) for tx in range(self.tx0, self.tx1 + 1)]))
        self.h = np.vstack(satirlar).astype(np.float32)
        self.dolu = None

    def doldur(self, s_px=25, kutu=None):
        """Deniz hücrelerini (≤ 0) ve kutu dışını yansıyan karayla alçak ova olarak doldurur."""
        k = self.h > 0
        if kutu is not None:
            ii, jj = np.indices(k.shape)
            n = 2 ** self.z * 256
            lon = (jj + self.tx0 * 256) / n * 360 - 180
            lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * (ii + self.ty0 * 256) / n))))
            k &= (lon >= kutu[0]) & (lon <= kutu[1]) & (lat >= kutu[2]) & (lat <= kutu[3])
        w = ndimage.gaussian_filter(k.astype(float), s_px)
        v = ndimage.gaussian_filter(np.where(k, self.h, 0.0), s_px)
        ort = v / np.maximum(w, 1e-6)
        # uzak denizde ortalama anlamsızlaşır: daha geniş ölçekle tamamla
        w2 = ndimage.gaussian_filter(k.astype(float), s_px * 4)
        v2 = ndimage.gaussian_filter(np.where(k, self.h, 0.0), s_px * 4)
        ort2 = v2 / np.maximum(w2, 1e-6)
        ort = np.where(w > 0.05, ort, ort2)
        # ayna dolgusu: deniz hücresine en yakın kıyı noktasına göre yansıyan karanın değeri, uzaklıkla söner
        d, (qi, qj) = ndimage.distance_transform_edt(~k, return_indices=True)
        ii, jj = np.indices(k.shape)
        mi = np.clip(2 * qi - ii, 0, k.shape[0] - 1); mj = np.clip(2 * qj - jj, 0, k.shape[1] - 1)
        ayna = self.h[mi, mj]
        sonum = 0.45 + 0.55 * np.exp(-d / 80.0)
        dol = np.where(k[mi, mj], ayna * sonum, np.clip(0.35 * ort, 15, 250))
        dol = 0.75 * dol + 0.25 * np.clip(0.35 * ort, 15, 250)
        dol = np.maximum(ndimage.gaussian_filter(dol, 1.0), 8)
        self.dolu = np.where(k, self.h, dol).astype(np.float32)
        self.deniz = (~k).astype(np.float32)
        return self

    def ornek(self, lon, lat, dolu=True, order=1):
        x, y = merc(lon, lat, self.z)
        x = x - self.tx0 * 256; y = y - self.ty0 * 256
        a = self.dolu if (dolu and self.dolu is not None) else self.h
        return ndimage.map_coordinates(a, [y, x], order=order, mode="mirror")

    def deniz_ornek(self, lon, lat):
        x, y = merc(lon, lat, self.z)
        return ndimage.map_coordinates(self.deniz, [y - self.ty0 * 256, x - self.tx0 * 256], order=1, mode="mirror")
