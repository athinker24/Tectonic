"""Proje dosyası (proje.json) ve maske çerçevesinin ölçeği.

Bir proje klasörü: proje.json, maske (PNG), parcalar.json, karsiliklar.json, ozellikler.json, etiketler.json, cikti/.
Koordinatlar her yerde MASKE PİKSELİ (x sütun, y satır, sol üst 0,0) olarak yazılır.
"""
import json
import os
import time

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
T0 = time.time()
VARSAYILAN = {
    "genislik_km": 8000.0,       # maskenin tüm genişliği
    "ust_enlem": 50.0,           # maskenin üst kenarının enlemi
    "merkez_boylam": 0.0,        # maskenin yatay ortasının boylamı
    "merak_boyut": [16000, 7719],  # Merak 16 bit dışa aktarımının boyutu (Merak'ta ölç; bkz. YOL.md)
    "kiyi_rampa_km": 45.0,       # karşılık birleşiminden sonra kıyıya doğru alçalma
    "deniz": {"kiyi_m": -60.0, "derin_m": -4000.0, "egim_km": 300.0, "en_sig_m": -40.0},
    "tohum": 7,
}


def log(s):
    print(f"[{time.time() - T0:6.0f} s] {s}", flush=True)


class Proje:
    def __init__(self, klasor):
        self.klasor = os.path.abspath(klasor)
        with open(self.yol("proje.json"), encoding="utf-8") as f:
            ayar = json.load(f)
        self.ayar = {**VARSAYILAN, **ayar}
        self.ayar["deniz"] = {**VARSAYILAN["deniz"], **ayar.get("deniz", {})}
        os.makedirs(self.cikti(), exist_ok=True)
        self._kara = None

    # yollar
    def yol(self, *a):
        return os.path.join(self.klasor, *a)

    def cikti(self, *a):
        return os.path.join(self.klasor, "cikti", *a)

    def json(self, ad, bos=None):
        p = self.yol(ad)
        if not os.path.exists(p):
            return bos
        with open(p, encoding="utf-8") as f:
            return json.load(f)

    # maske ve ölçek
    def kara(self):
        if self._kara is None:
            temiz = self.cikti("maske_temiz.png")
            p = temiz if os.path.exists(temiz) else self.yol(self.ayar["maske"])
            self._kara = np.asarray(Image.open(p).convert("L")) > 127
        return self._kara

    @property
    def boyut(self):
        ny, nx = self.kara().shape
        return ny, nx

    @property
    def km_px(self):
        return self.ayar["genislik_km"] / self.boyut[1]

    @property
    def der_px(self):
        """Düz yerleşim: bir maske pikseli enlemde ve boylamda aynı derece (sahibin tercihi: bükmeden, oran korunarak)."""
        return self.km_px / 111.2

    def enlem(self, y):
        return self.ayar["ust_enlem"] - (np.asarray(y, float) + 0.5) * self.der_px

    def boylam(self, x):
        return self.ayar["merkez_boylam"] + (np.asarray(x, float) + 0.5 - self.boyut[1] / 2) * self.der_px
