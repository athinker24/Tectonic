# Atlasta sınamak için çıktı

`python3 atlas_cikti.py /atlas/deposu/yolu` bu klasörü üretir. Atlas deposuna dokunmaz; yalnız oradan okur.

| dosya | atlas deposundaki yeri | ne |
|---|---|---|
| `dunyam_heightmap.png` | `dunya/dunyam_heightmap.png` | 4096 × 2048, 16 bit gri, tüm gezegen. Deniz pikselleri ve kıyı atlasınkiyle birebir aynı; yalnız kara değerleri yeni. |
| `heightmap_blogu.json` | `dunya/dunyam.json` → `heightmap` | Değişen alanlar: `max_elev_m`, `elev_gamma` (1.0), `elev_curve` (iki noktalı doğrusal). Diğer alanlar aynı. |
| `kabartma_kaynak.jpg` | `dunya/kabartma_kaynak.jpg` | Yeni topografyanın gölgeli görüntüsü, editör görselinin çerçevesinde (aynı `sx sy ox oy`). |
| `kontrol.png` | (yok) | Geri açılmış yükseklikler; kırmızı: maskeyle atlas kıyısının ayrıştığı pikseller. |

## Sınama

1. Atlas deposunda ayrı bir dal aç (yayındaki atlas bozulmasın; dalın önizleme adresi olur).
2. Üç dosyayı yukarıdaki yerlere koy ve `dunyam.json`'daki `heightmap` bloğunda yalnız `max_elev_m`, `elev_gamma` ve `elev_curve`'ü
   `heightmap_blogu.json`'dakilerle değiştir.
3. Push et. `atlas verisi` iş akışı `uret.py`'yi koşar. Bilgisayarda kaba deneme için: `python uret.py --res 1.0 --ozet`.

## Bilinenler

- Kayıt: maske tuvale ölçek 0,2620 / 0,2621 ve kayma (1540,9; 341,3) ile oturdu, örtüşme (IoU) 0,968. Ayrışan 14.566 tuval pikseli
  kıyı şeritleri ve birkaç koy; atlasta kara olup maskede deniz olan yerlere en yakın karanın yüksekliği verildi.
- Atlas tuvalinde bir piksel yaklaşık 10 km; dar sıralar yumuşar. En yüksek nokta bu çözünürlükte 3730 m (tam haritada 4650 m).
  Kara yükseklikleri: p10 44 m, medyan 214 m, p90 1063 m.
- Atlasın coğrafyası bu tarihin varsaydığından büyük: kıta 60°K ile 7°G arasında, yaklaşık 88° boylam. Tarihte 50°K ile 5°G ve
  8000 km genişlik varsaydım. İklim atlasın coğrafyasıyla hesaplanır.
- İş akışı yalnız `uret.py`'yi (iklim verisi ve dokular) yeniden üretir. Göller ve nehirler (`su/`), levhalar (`tektonik/`), bitki, toprak,
  tarım, yaşam ve hayvan katmanları ayrı betiklerle üretiliyor; onlar yeniden koşulmazsa eski araziye göre kalır.
