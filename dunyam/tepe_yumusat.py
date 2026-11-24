"""Ana kalıp v3'teki iğne tepeleri çevrelerine göre yumuşatır (sahip, 2026-11-24: "tek piksellik tepeleri çevrelerine uygun
şekilde yumuşat").

İğne: 5 × 5 içinde en yüksek kara pikseli; 8 piksel (yaklaşık 20 km) yarıçaplı halkanın ortancasından ASIM_M'den fazla, 8 komşusunun
ortalamasından KESKIN_M'den fazla yüksek. Merak'ın fırça izleri 1 ile 13 piksellik koni kümeleri bırakıyor; tek piksel ölçütü
bunları kaçırıyordu (6000 m üstü piksellerin komşu en yükseğini aşma ortancası −21 m: kümeli).

Düzeltme: halka ortancası taban; tabanın üstündeki aşım e, e' = E0 · tanh(e / E0) ile sıkıştırılır (küçük aşım neredeyse aynı
kalır, büyük aşım E0'a yaklaşır). Sıkıştırma tepeden R/2'ye kadar tam, R'ye kadar kosinüsle sıfıra iner; tepenin biçimi
korunur, yalnız boyu kısalır. Yalnız karada; kıyı ve deniz değişmez. Girdi temizlenmiş Merak dışa aktarımıdır (`temizle_v3.py`
çıktısı); betik onu yerinde günceller, yeniden çalıştırmadan önce `temizle_v3.py` yeniden çalıştırılmalı."""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None
S = 14642
KOK = os.path.dirname(os.path.abspath(__file__))
R = 8            # halka yarıçapı, piksel
ASIM_M = 1000    # halka ortancasını aşma
KESKIN_M = 400   # 8 komşu ortalamasını aşma
E0 = 1500        # sıkıştırılmış aşımın üst sınırı, m


def coz(g):
    g = g.astype(np.float32)
    return np.where(g > S, 8000 * ((g - S) / (65535 - S)) ** 2, 0).astype(np.float32)


def kodla(m):
    return np.round(S + 1 + (65534 - S) * np.sqrt(np.clip(m, 1, 8000) / 8000)).astype(np.uint16)


def main():
    yol = os.path.join(KOK, "kaynak", "ana_v3_16k.png")
    G = np.array(Image.open(yol)); kara0 = G > S
    ys, xs = np.where(kara0)
    y0, y1, x0, x1 = ys.min() - R, ys.max() + R + 1, xs.min() - R, xs.max() + R + 1
    g = G[y0:y1, x0:x1]; k = g > S; z = coz(g)

    tepe = k & (z == ndimage.maximum_filter(z, size=5)) & (z > 800)
    cy, cx = np.where(tepe)
    dy, dx = np.mgrid[-R:R + 1, -R:R + 1]; d = np.hypot(dy, dx)
    halka = np.argwhere((d >= R - 1.5) & (d <= R)) - R
    taban = np.median(np.stack([z[cy + oy, cx + ox] for oy, ox in halka], 1), 1)
    m8 = (ndimage.uniform_filter(z, 3) * 9 - z) / 8
    e = z[cy, cx] - taban
    sec = (e > ASIM_M) & ((z - m8)[cy, cx] > KESKIN_M)
    cy, cx, taban, e = cy[sec], cx[sec], taban[sec], e[sec]
    q = E0 * np.tanh(e / E0) / e                       # aşımın kalacak payı

    w_cekirdek = np.where(d <= R / 2, 1.0, np.where(d <= R, 0.5 * (1 + np.cos(np.pi * (d - R / 2) / (R / 2))), 0.0))
    # her piksel için en güçlü sıkıştırma (en küçük çarpan) ve onun tabanı
    carpan = np.ones_like(z); tb = np.zeros_like(z)
    for y, x, t, qq in zip(cy, cx, taban, q):
        sl = (slice(y - R, y + R + 1), slice(x - R, x + R + 1))
        c = 1 - w_cekirdek * (1 - qq)
        daha = c < carpan[sl]
        carpan[sl] = np.where(daha, c, carpan[sl]); tb[sl] = np.where(daha, t, tb[sl])
    ust = k & (carpan < 1) & (z > tb)
    yeni = z.copy(); yeni[ust] = tb[ust] + (z[ust] - tb[ust]) * carpan[ust]

    degisen = ust & (kodla(yeni) != g)
    g2 = g.copy(); g2[degisen] = kodla(yeni[degisen]); G[y0:y1, x0:x1] = g2
    Image.fromarray(G).save(yol)
    z2 = coz(g2)
    dus = (z - yeni)[degisen]
    print(f"iğne {len(cy)}; değişen piksel {int(degisen.sum())}; en yüksek {z[k].max():.0f} → {z2[k].max():.0f} m; "
          f"6000 m üstü piksel {int((z > 6000).sum())} → {int((z2 > 6000).sum())}; kıyı farkı {int(((G > S) != kara0).sum())}")
    print("tepe noktası düşüşü m (ortanca, %90, en çok):", np.percentile(z[cy, cx] - yeni[cy, cx], [50, 90]).round(),
          round(float((z[cy, cx] - yeni[cy, cx]).max())), "| tüm değişen pikseller ortanca", round(float(np.median(dus))))
    np.savez_compressed(os.path.join(KOK, "kaynak", "igneler.npz"), y=cy + y0, x=cx + x0, taban=taban, asim=e)


if __name__ == "__main__":
    main()
