"""Yeni topografyayı Dünyam Atlası'nın (dunyam-atlas-mobil) girdi biçimine çevirir; atlas deposuna dokunmaz.

Atlas tüm gezegeni kaplayan 4096 × 2048, 16 bit gri bir PNG okur (satır 0 kuzey, equirectangular).
Kara: değer ≥ sea_level_value. Yükseklik: oran = (v − deniz) / (vmax − deniz), metre = egri(oran).
Burada kıyı ATLASIN tuvalinden korunur (akıntılar, nehirler ona göre kurulu); kara hücrelerine bu tarihin
yükseklikleri, maskeyi tuvaldeki kıtaya en iyi oturtan ölçek ve kaymayla taşınır. Eğri doğrusal yazılır
(metre doğrudan), deniz pikselleri değişmez.

Kullanım: python3 atlas_cikti.py /atlas/deposu/yolu
Çıktı: atlas/dunyam_heightmap.png, atlas/heightmap_blogu.json, atlas/kabartma_kaynak.jpg, atlas/kontrol.png
"""
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage, optimize

Image.MAX_IMAGE_PIXELS = None
ATLAS = sys.argv[1] if len(sys.argv) > 1 else "/home/user/athinker24/dunyam-atlas-mobil"


def main():
    w = json.load(open(f"{ATLAS}/dunya/dunyam.json"))
    hm = w["heightmap"]
    tuval = np.asarray(Image.open(f"{ATLAS}/dunya/dunyam_heightmap.png")).astype(np.float64)
    deniz = float(hm["sea_level_value"])
    kara_t = tuval >= deniz
    maske = np.asarray(Image.open("maske.png").convert("L")) > 127
    z = np.load("cikti/son_z_tam.npy").astype(np.float64)
    my, mx = maske.shape

    # kayıt: tuval (satır, sütun) → maske (y, x) = ((satır − oy) / sy, (sütun − ox) / sx)
    rr, cc = np.nonzero(kara_t); yy, xx = np.nonzero(maske)
    sy = (rr.max() - rr.min()) / (yy.max() - yy.min()); sx = (cc.max() - cc.min()) / (xx.max() - xx.min())
    p0 = np.array([sx, sy, cc.min() - xx.min() * sx, rr.min() - yy.min() * sy])
    r0, r1, c0, c1 = rr.min() - 20, rr.max() + 20, cc.min() - 20, cc.max() + 20
    R, C = np.mgrid[r0:r1, c0:c1].astype(np.float64)
    kt = kara_t[r0:r1, c0:c1]
    mf = maske.astype(np.float32)

    def iou_eksi(p):
        sx_, sy_, ox, oy = p
        m = ndimage.map_coordinates(mf, [(R - oy) / sy_, (C - ox) / sx_], order=1, cval=0) > 0.5
        return -(m & kt).sum() / max((m | kt).sum(), 1)

    print("başlangıç IoU", -iou_eksi(p0))
    son = optimize.minimize(iou_eksi, p0, method="Nelder-Mead",
                            options={"xatol": 1e-4, "fatol": 1e-6, "maxiter": 600, "initial_simplex": None})
    sx, sy, ox, oy = son.x
    iou = -son.fun
    print("kayıt", son.x, "IoU", iou)

    # tuvaldeki kara hücrelerine yükseklik: maskede kara olmayan kıyı şeritleri en yakın karadan
    _, (ii, jj) = ndimage.distance_transform_edt(~maske, return_indices=True)
    zk = np.where(maske, z, z[ii, jj])
    zk = np.maximum(zk, 1.0)
    # örtüşme önleme: tuval pikseli ~ 1/sx maske pikseli; örneklemeden önce o ölçekte yumuşat
    zk = np.maximum(ndimage.gaussian_filter(zk, 0.45 / sx), 1.0)
    h = ndimage.map_coordinates(zk, [(R - oy) / sy, (C - ox) / sx], order=1, mode="nearest")
    yuk = np.zeros_like(tuval); yuk[r0:r1, c0:c1] = h
    kara_disi = kara_t.copy(); kara_disi[r0:r1, c0:c1] = False
    if kara_disi.any():
        print("uyarı: kayıt kutusu dışında kara", kara_disi.sum())
    en = float(yuk[kara_t].max())
    max_m = float(np.ceil(en / 10) * 10)
    yeni = tuval.copy()
    v = deniz + np.clip(yuk / max_m, 0, 1) * (65535 - deniz)
    yeni[kara_t] = np.maximum(np.round(v[kara_t]), deniz)
    # vmax = 65535 olmalı (oran onunla ölçülür): en yüksek kara pikseli tam 65535
    i = np.unravel_index(np.where(kara_t, yuk, -1).argmax(), yuk.shape)
    yeni[i] = 65535
    out = yeni.astype(np.uint16)
    Image.fromarray(out).save("atlas/dunyam_heightmap.png")

    blok = {k: v for k, v in hm.items() if k != "kabartma"}
    blok["file"] = "dunya/dunyam_heightmap.png"  # uret.py bu alanı zaten dunya/ yoluna çevirir
    blok.update({"max_elev_m": max_m, "elev_gamma": 1.0, "elev_curve": [[0.0, 0.0], [1.0, max_m]]})
    blok["kabartma"] = {k: hm["kabartma"][k] for k in ("file", "sx", "sy", "ox", "oy")} | {"iou": hm["kabartma"].get("iou")}
    json.dump({"heightmap": blok,
               "_not": ("Tektonik tarih denemesi (Tectonic deposu, tarih/): kara yükseklikleri Dünya karşılıklarından. "
                        f"Kıyı atlas tuvalinden korundu; maske tuvale ölçek sx {sx:.5f} sy {sy:.5f}, kayma x {ox:.2f} y {oy:.2f} "
                        f"ile oturtuldu (IoU {iou:.4f}). Eğri doğrusal: değer metreyi doğrudan taşır.")},
              open("atlas/heightmap_blogu.json", "w"), ensure_ascii=False, indent=1)

    # kabartma kaynağı: atlasın editör görseli çerçevesinde (tuval → görsel: ((satır − oy)/sy, (sütun − ox)/sx))
    kb = hm["kabartma"]
    ky, kx = Image.open(f"{ATLAS}/{kb['file']}").size[::-1]
    gy, gx = np.mgrid[0:ky, 0:kx].astype(np.float64)
    tr = gy * kb["sy"] + kb["oy"]; tc = gx * kb["sx"] + kb["ox"]
    topo = ndimage.gaussian_filter(np.asarray(Image.open("cikti/topografya.png").convert("RGB")).astype(np.float32),
                                   (0.45 * kb["sx"] / sx, 0.45 * kb["sx"] / sx, 0))
    kab = np.stack([ndimage.map_coordinates(topo[..., k], [(tr - oy) / sy, (tc - ox) / sx], order=1, mode="nearest")
                    for k in range(3)], -1)
    Image.fromarray(np.clip(kab, 0, 255).astype(np.uint8)).save("atlas/kabartma_kaynak.jpg", quality=92)

    # kontrol: geri açılmış yükseklik ve kıyı farkı
    oran = np.maximum(out.astype(float) - deniz, 0) / (65535 - deniz)
    m_ac = np.where(out >= deniz, oran * max_m, -1)
    m_kayit = ndimage.map_coordinates(mf, [(R - oy) / sy, (C - ox) / sx], order=1) > 0.5
    fark = m_kayit ^ kt
    kes = m_ac[r0:r1, c0:c1]
    rgb = np.stack([np.interp(kes, [-1, 0, 500, 1500, 3000, 5000], c) for c in
                    ([30, 90, 170, 200, 160, 245], [50, 140, 170, 160, 130, 245], [90, 80, 100, 110, 110, 245])], -1)
    rgb[fark] = [255, 0, 0]
    Image.fromarray(rgb.astype(np.uint8)).save("atlas/kontrol.png")
    print("kara hücresi", int(kara_t.sum()), "kıyı farkı", int(fark.sum()), "en yüksek", max_m,
          "geri açılan en yüksek", round(float(m_ac.max())), "medyan kara", round(float(np.median(m_ac[out >= deniz]))))


if __name__ == "__main__":
    main()
