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

## 12 Kasım 2026: aşama 4, aday tarih üretici (ilk sürüm)

Test maskesi dört bloğa ayrıldı (Kuzey sabit, Güneydoğu, Güneybatı, Takımada) ve dikişler senaryo dosyasında (`veri/test_senaryo.json`). Batı kara köprüsü test maskesinde yaklaşık 31°B ile 27°B, 25°K'de 1 ile 2 piksellik bir boyun; dikiş oraya çizildi.

**Kısıtlar:** blokların geçmişte üst üste binmemesi, kıtasal hızın 6 cm/yıl'ı geçmemesi, güney geçidinin hiç kapanmaması (ölçüm eşiği 60 km, 50 km hücreyle). Güney geçidi bugün yaklaşık 205 km genişliğinde (100 km hücreyle ölçüldü); ilk denemedeki 150 km eşiği benim koyduğum ve neredeyse her adayı eleyen bir sayıydı, düşürüldü.

**İstekler** kabuk kalınlığından ölçülüyor (aşınmasız hızlı tarama): sıradağ kuşağında kabuğun %95'lik dilimi ≥ 60 km; çanakta izostatik yükseklik ortancası 1000 ile 1500 m; mikro kıtanın en az %60'ında kabuk ≥ 45 km.

**Arama:** 300 rastgele tohumdan yalnızca 4'ü geçerli çıktı. Geçerli adaylardan mutasyonla 6 nesil sonra 1200 adaydan 572'si geçerli, arşivde 11 farklı hücre. Süre 50 km hücreyle 19 dakika.

**Coğrafyanın dayattığı sonuçlar (bu maske için):**
- Güneydoğu bloğu yalnızca güneydoğudan, kuzeybatıya doğru hareket ederek gelebiliyor (seçilen adaylarda yön kuzeyden 15° ile 25° batıya). Tam kuzeye ya da kuzeydoğuya gelen her aday güneybatı kıtasıyla çakıştı ya da güney geçidini kapattı.
- Güneybatı kıtası yerinde durmuş olamıyor: geçerli adayların hepsinde kuzeydoğuya kayıyor, geriye sürünce güneybatıya çekilip güneydoğu bloğuna yol açıyor.
- Mikro kıta hiçbir geçerli adayda güneydoğu bloğuna doğru sıkışmadı; kuzey kıyısına ya da güneybatı kıtasına sıkışıyor.

**Seçilen beş aday** (dört isteğin üçü de her birinde sağlanıyor; çelişki yok): çarpışma 25, 42, 47, 65 ve 65 milyon yıl önce; kapanan okyanus 600 ile 1187 km; mikro kıta 11 ile 16 milyon yıl önce kuzey kıyısına ya da güneybatı kıtasına sıkışıyor. Görsel: `cikti/ornek_adaylar.png`.

**Eksikler:**
- Olay şablonları test maskesine özgü yazıldı (`aday_kur`); sahibin maskesi için senaryo dosyasından okunacak biçimde genelleştirilmeli.
- 3. istek (yarımada çarpışması, Apenin ve Alp tarzı) henüz yok; test maskesinde yarımadanın yeri belirsiz.
- İstekler aşınmasız kabuk tahmininden ölçülüyor; seçilen aday tam modelle (aşınmalı) yeniden ölçülmeli.
- Çeşitlilik özellikleri ve aday sayısı (5) benim tasarımım.

## Aşama 4, sahibin maskesiyle (12 Kasım 2026)

Maske `veri/maske.png` (3808 × 2914, eşdikdörtgen, sınır kutusu 44,43°B ile 43,11°D, 7,08°G ile 59,99°K). Test maskesinin aynı kutuya kırpılmasıyla örtüşme (IoU) 0,966, en iyi kayma sıfır: sınırlar doğru. Kenar yumuşatmalı 15 545 gri piksel 128 eşiğiyle ikilendi; güneydoğu körfezindeki iki gri leke (yaklaşık 2650 ile 2800 x, 2150 ile 2300 y piksel) kara sayıldı.

Batı köprüsü test maskesinden geniş: 40,3°B ile 37,6°B arasında, yaklaşık 28,2°K, genişlik yaklaşık 250 km. Dikiş buraya taşındı (`veri/senaryo.json`). Blok alanları (Nside 512): Kuzey 17,53, Güneybatı 9,73, Güneydoğu 6,62, Takımada 0,90 milyon km², toplam kara 34,78 milyon km².

Üretici (Nside 128, 300 tohum, 6 nesil): 1200 aday, 480 geçerli (tohumda 5). İhlaller: çakışma 733, geçit 534, hız 108. Çelişki yok. Seçilen beş aday: çarpışma 40, 55, 64, 63, 65 milyon yıl önce; güneydoğu yönü −16° ile −24° (yine güneydoğudan geliyor); güneybatı her adayda yaklaşıyor (yön 20° ile 62°). Test maskesinden farklı olarak mikro kıtanın güneydoğu bloğuna sıkıştığı geçerli bir aday çıktı (1145).

## Sahibin bölge işaretleriyle (12 Kasım 2026)

İşaretler `veri/sahip_isaretleri.png`; renkler çokgene çevrildi (`veri/senaryo.json`). Kırmızı sıradağ alanı 1,39, sarı çanak 3,55 milyon km² (İran platosu yaklaşık 3,7 milyon km²). Kırmızı alanın ekseni 0,2°D 40,1°K ile 32,1°D 30,0°K arasında, yaklaşık 3000 km. Eksenin batı ucu karada bittiği için duvar dikişi 5°D yakınında güneye kırılıp iç denizin kuzeydoğu körfezine bağlandı (bizim kararımız). Mavi çizginin kara üzerindeki batı kenarı yeni Yarımada dikişi; Yarımada 2,69 milyon km², güney geçidinin batı kıyısı artık bu blok.

Yeni kod: plato çokgenle verilebilir (Carpisma.plato_maske); istek 3 iki türlü: Alp (Yarımada doğudan yaklaşıp kökünden çarpar, kökte kuşak, kabuk %95 ≥ 55 km), Apenin (Güneybatı ile birlikte gider, omurga şeridinde kalınlaşma, kabuk %90 42 ile 52 km).

Üretici (Nside 128): 300 rastgele tohumun hiçbiri geçerli değil; mutasyonla 1200 adayda 329 geçerli. İhlal: çakışma 1040, geçit 665, hız 151. 80 adaylık ayrı örnekte en sık çakışan çift Güneydoğu ile Yarımada (65), sonra Güneybatı ile Takımada (30). Çelişki yok; seçilen beşin hepsi dört isteği sağlıyor (2 Apenin, 3 Alp). Seçilenlerin bir kısmı aralık sınırında: güneydoğu yönü −25° (aralığın ucu), çarpışma 65 milyon yıl (aralığın ucu). Aralık genişletilince daha kuzeybatıdan gelen ve daha eski çarpışmalar da geçerli çıkabilir. Apenin türünde ölçülen 50,0 km kabuğun üst sınırı (hmax); omurga ölçüsü bu sınırla belirleniyor.
