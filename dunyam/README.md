# Dünyam (sahibin dünyası): Minecraft hazırlığı

Kaynak dosyalar `kaynak/` altında, git'te değil (16k PNG; `.gitignore`). Sahip 2026-11-23'te verdi (`merak_son_saf_16k.zip`).

| dosya | ne | ölçüm |
|---|---|---|
| `kaynak/son_temiz_16k.png` | son hâl: doğu yarısı sahibin Merak'ta elle işlediği, batı yarısı gerçek dokular | 16000 × 7719, 16 bit; kara %3,38; kara %10/%50/%90 = 113/598/1636 m, en yüksek 6759 m |
| `kaynak/saf_temiz_16k.png` | yalnız gerçek dokular (karşılık yöntemi) | aynı boyut; kara %10/%50/%90 = 79/554/1596 m, en yüksek 5690 m |

- İki dosyanın kıyısı birebir aynı (fark 0 piksel). Yükseklik farkı doğuda büyük (|fark| ortancası 160 ile 365 m), batıda küçük
  (3 ile 7 m; %5 ile %15'inde 100 m'den çok).
- Merak kodlaması (`S = 14642`, beyaz 8000 m) ile okundu. Kara 36°B ile 36°D, 5°G ile 50°K arası (Merak çerçevesinde).
- İklim atlasının arazisi (`dunyam-atlas-mobil/dunya/dunyam_heightmap.png`) bu kıtanın büyütülmüş ve kaydırılmış hâli: boylamda
  1,217, enlemde 1,218 kat, IoU 0,953 (atlas ızgarasında, Nelder-Mead). Atlasta kara 44,5°B ile 43,1°D, 7°G ile 60°K.
  Kıyı farkı: atlas ızgarasında 21 379 piksel (atlas karasının %4,7'si); çoğu kıyı boyunca ince şerit (çözünürlük), birkaç gerçek
  fark var (doğu kıyısında yaklaşık 1700 piksellik parça). Görüntü: `atlas_merak_kiyi.png` (gri ortak, kırmızı yalnız atlasta kara,
  mavi yalnız Merak'ta kara).
