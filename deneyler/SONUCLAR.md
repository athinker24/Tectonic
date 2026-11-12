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

## 12 Kasım 2026: aşama 3, tek çarpışmadan yükselme ve animasyon

Senaryo: 31,2°K boyunca 37°B ile 41°D arasında dikiş hattı, kuzey üst levha, 50 milyon yıl önce başlayıp süren çarpışma, 4 cm/yıl. Kuşak 280 km, arkasında 700 km plato bölgesi; kabuk üst sınırı kuşakta 70 km, platoda 44 km (Zagros ve İran tipi, karar 6). Kayaç sertliği ln K'de 0,5 standart sapmalı rastgele alan; yükselmeye boyuna yüzde 35 düzensizlik.

**Yeni fizik:**
- Kütle korunumu: kuşağa giren hacim hız × 35 km kabuk; kalınlığı sınıra varan düğüm fazlasını platoya devrediyor (düğüm başına en çok 5 mm/yıl).
- Airy: yüzey yükselmesi kalınlaşmanın 0,152 katı.
- Bölgesel izostazi: aşınan yükün 0,85'i geri sıçrıyor, 80 km bükülme ölçeğinde yayılarak (ölçülen yayılma genişliği 83 km, korunum binde 2 sapma).

**n = 1'in kusuru:** tüm kıta deniz seviyesine aşındı (kara medyanı 3 m), çünkü büyük ve düz akarsular sınırsız kazıyor. n = 2, m = 1 (Ruetenik 2023 küresel uyumu n ≈ 2,3) ile kara medyanı 102 ile 126 m.

**Sonuçlar (50 milyon yıl, bugün):**

| Nside | Hücre | K (n = 2) | En yüksek | Kara medyanı | Kuşak ortalama / %95 | Kuşak eğimi ortanca / %90 | Plato ortalama (%10 ile %90) | Süre |
|---|---|---|---|---|---|---|---|---|
| 256 | 25,5 km | 4e-9 | 4117 m | 102 m | 1624 / 2759 m | 0,92° / 1,58° | 1169 (560 ile 1834) m | 83 s |
| 256 | 25,5 km | 1,5e-8 | 2317 m | 59 m | 910 / 1590 m | 0,50° / 0,87° | 667 m | 83 s |
| 512 | 12,7 km | 4e-9 | 4562 m | 110 m | 1773 / 3032 m | 1,69° / 2,92° | 1269 (620 ile 2002) m | 412 s |
| 512 | 12,7 km | 2e-9 | 7861 m | 126 m | 2492 / 4500 m | 2,45° / 4,54° | 1707 m | 414 s |

Gerçek veri hedefi (arastirma/20, hücre ortalamaları arası eğim): 20 km'de Himalaya ve Alpler ortanca 0,9°; 10 km'de Alpler 1,24° / 3,7°, Himalaya 1,6° / 4,7°. K = 4e-9 ortancayı tutuyor ama %90'lık dilim gerçekten düşük (eğim dağılımı dar). K = 2e-9 %90'ı tutuyor, ortancayı aşıyor. Varsayılan K = 4e-9; plato 1269 m ile seçilen 1000 ile 1500 m aralığında.

**Hata ve düzeltme:** K = 2e-9 koşusunda kabuk 197 km'ye fırladı; plato dolunca fazla hacim birkaç boş düğüme yığılıyordu. Düğüm başına üst sınır eklendi ve teste bağlandı. K = 2e-9 satırı bu düzeltmeden önce koşuldu; yeniden koşulmalı.

**Açık:** eğim dağılımının dar olması (gerçekte daha çok dik yamaç var); kıyı sönümlemesinin kıyı türüne göre ayarlanması; ova yüksekliği gerçek iç ovalardan (100 ile 300 m) biraz düşük.
