# Deney sonuçları

## 12 Kasım 2026: HEALPix hızı, birim hatası, kıyı sönümlemesi, ilk ayar

Test maskesi: atlas yükseklik haritasının kara/deniz ayrımı (`veri/test_maske.png`), sahibin Photoshop maskesi gelene kadar yer tutucu. Makine: 4 çekirdek, 15 GB.

**HEALPix hızı (gerçek kıyı, yalnız akarsu aşınması):**

| Nside | Hücre | Toplam düğüm | Kara düğümü | Adım süresi | Bellek |
|---|---|---|---|---|---|
| 128 | 50,9 km | 196 608 | 13 659 | 0,03 s | 0,2 GB |
| 256 | 25,5 km | 786 432 | 54 677 | 0,10 s | 0,5 GB |
| 512 | 12,7 km | 3 145 728 | 218 846 | 0,47 s | 1,9 GB |

30 milyon yıllık koşu (300 adım, Nside 512) ızgara kurulumu ve görüntü dahil yaklaşık 140 s sürdü; üç koşu aynı anda. Mimarideki HEALPix seçimi tuttu.

**Kurulum:** pip tekerleğindeki Fastscapelib'de HEALPix yok (`HealpixGrid` boş). conda-forge derlemesi gerekiyor (`environment.yml`).

**Fastscapelib birim hatası:** HEALPix ızgarasında komşu uzaklıkları radyan, düğüm alanları m² dönüyor. Eğim R = 6,371e6 kat büyük hesaplanıyor; düzeltilmezse arazi ilk adımda sıfıra aşınıyor. Düzeltme `K / R^n`; eğimli düzlem deneyinde ölçülen aşınma beklenenin 0,97 katı (`testler/test_asinma.py`).

**Kıyı sönümlemesi** (elle çizilmiş yükselme: 33°K boyunca sıradağ 4 mm/yıl, arkasında zayıf plato; 30 milyon yıl; K = 2e-6):

| Sönümleme | Kıyıdaki ilk kara hücresi: ortalama / %95 / en yüksek |
|---|---|
| yok | 44 / 84 / 3049 m |
| 150 km yumuşak basamak | 1 / 1 / 63 m |

Sönümleme olmadan sıradağın denize vardığı yerde 3 km'lik basamak oluşuyor. 150 km'lik sönümleme bunu gideriyor ama kıyı ovalarını her yerde neredeyse sıfır metreye çekiyor; bu da gerçekçi değil (gerçek kıyıların bir kısmı diktir). Sönümleme uzunluğu yerel olmalı: pasif kıyıda uzun, etkin kıyıda kısa. Açık iş.

**İlk ayar** (hücre ortalamaları arası eğim, sıradağ kuşağında; gerçek veri hedefi 10 km hücrede ortanca 1,2 ile 1,6°, arastirma/20):

| K | Sıradağ eğimi ortanca / %90 | Sıradağ ortalama / %95 yükseklik | En yüksek |
|---|---|---|---|
| 2e-6 | 3,2° / 8,1° | 4468 / 8311 m | 9813 m |
| 5e-6 | 1,3° / 3,2° | 1797 / 3358 m | 3924 m |

K = 5e-6 eğim hedefini tutuyor ama 4 mm/yıl yükselmeyle zirve 3,9 km'de kalıyor. 6 ile 7 km'lik zirve ve gerçekçi eğim birlikte isteniyorsa kuşak daha geniş olmalı (gerçek Himalaya yaklaşık 250 ile 350 km); bu elle çizilmiş sıradağ 150 km yarı genişlikte. Kesin ayar, gerçek yükselme alanı (aşama 3) gelince yapılacak.

**Görülen kusur:** düz ve tekdüze yükselmede vadiler tarak dişi gibi düzenli çıkıyor (tek yönlü akışın ızgara izi). Gerçek yükselme alanı düzensiz olacak; ayrıca yükselmeye ve kayaç sertliğine düzensizlik eklenmeli.
