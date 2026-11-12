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

## Tam model, gerçek maske ve sahibin bölgeleri (12 Kasım 2026)

Adaylar 1029 (Alp) ve 443 (Apenin), Nside 512, K = 4e-9, n = 2. Koşu süresi 10 ile 12 dakika.

İlk koşuda sıradağ (dikişten 200 ile 300 km'de ortalama 1530 m) platodan (yaklaşık 1250 ile 1500 m) yalnızca yaklaşık 300 m yüksek çıktı. Neden: kabuk kalınlığı h yerel olarak birikiyor, aşınmanın geri sıçraması ise 80 km bükülmeyle bölgesel; kuşakta h doyuma (70 km) ulaşıp kabul sıfırlanırken yüzey alçakta kalıyordu. Plato yalnızca bu yapay doygunluk fazlasıyla besleniyordu. Kuşak sertliği (K çarpanı 0,3 ve 0,15) ve yakınsama hızı (3,5, 5 cm/yıl) bunu değiştirmedi; bu, sınırın aşınma değil doygunluk olduğunu gösterdi.

Düzeltme: her adımda h = H0 + düz(z) / AIRY (ModelAyar.kabuk_yuzeyden). Bununla sıradağ yükseldi (Nside 256, dikişten 0 ile 100 km ortalama 2445 m) ama plato 120 m'ye düştü. Ek: yaklaşmanın bir payı (plato_orani) doğrudan çizilen plato bölgesine yayılır (yaygın kısalma; Zagros Arabistan ile Avrasya yaklaşmasının yalnızca bir kısmını karşılar). Nside 256'da pay 0,4: plato ortancası 983 m; 0,6: 1137 m. Seçim 0,5, kuşak K çarpanı 0,3. Çizilen plato sınırı arazide basamak bıraktığı için 200 km'lik yumuşak geçiş eklendi.

Sonuç (Nside 512, pay 0,5, çarpan 0,3):

| | 1029 Alp | 443 Apenin |
|---|---|---|
| en yüksek nokta | 5153 m | 5466 m |
| sıradağ bölgesi p95 | 3361 m | 3421 m |
| dikişten 100 ile 200 km ortalama | 2156 m | 2444 m |
| çanak ortancası (hedef 1000 ile 1500) | 1220 m | 1280 m |
| çanak p10 ile p90 | 714 ile 1613 m | 1017 ile 1638 m |
| yarımada | kök p95 3423 m | omurga p90 2591 m |
| mikro kıta ortancası, 500 m üstü pay | 1147 m, 0,88 | 832 m, 0,75 |
| kara ortancası | yaklaşık 100 m | yaklaşık 96 m |

Bilinen sınırlar: aşınma bugünkü kıyı çizgisiyle bugünkü ızgarada hesaplanır, paleo karelerde yükseklik bloklarla taşınır. Adaylar eski (aşınmasız, plato payı yok) ölçümle seçildi; aday araması yeni fizikle yeniden yapılmalı. Ovalar alçak (kara ortancası yaklaşık 100 m).

## Rastgele mod (12 Kasım 2026)

`python -m deneyler.rastgele TOHUM [NSIDE] [BLOK_SAYISI]`. Senaryo ve sahip işaretleri kullanılmaz. Kıta 4 ile 8 tohumdan gürültülü jeodezik uzaklıkla bloklara ayrılır; 0,5 milyon km²'den büyük tohumsuz kara parçası kendi bloğu olur. Tarih bir birleşme tarihidir: çekirdekten genişleyen bir ağaçta her blok ana bloğuna göre hareket eder ve onun hareketini devralır. Ortak sınırda göreli dik yakınsama 0,3 cm/yıl'ı geçerse sınır çarpışması kurulur (gelen blok altta, %25 ters). Birleşmiş komşular arasındaki üst üste binme serbest bırakıldı (sınırdaki kısalmanın katı çizimdeki karşılığı); birleşmeden önceki binme ve 6 cm/yıl hız sınırı sert.

İlk sürüm (bağımsız bloklar): 400 adayda geçerli yok. Ağaçla ve birleşme sonrası binme serbest: tohum 1 için 284, tohum 2 için 14, tohum 3 için 36 aday denendi. Nside 256 sonuçları: en yüksek nokta 6167, 4877, 4785 m; kara ortancası 110, 90, 93 m. Bilinen eksik: başka bloğa sınırı olmayan ada blokları (iç denizdeki mikro kıta) hareketsiz ve olaysız kalıyor.

## İnce viskoz levha, kalıpsız (12 Kasım 2026)

`tektonik/levha.py`, `deneyler/levha_deneme.py`. Kıta Lambert eşit alanlı izdüşümde 50 km'lik düzenli ızgarada (173 × 190) ince viskoz levha; blok çekirdeklerine aday 443'ün hızları dayatılır, aradaki kıta üstel yasayla (n = 3) akar; kalınlaşma −S ∇·u; Γ = ½ g ρc (1 − ρc/ρm) S² yayılmaya iter. Aşınma fastscapelib RasterGrid (K = 4e-9, m = 1, n = 2). Uzun dalga boyu yükseklik kabuktan (80 km bükülme, S_ref 33 km), kısa dalga boyu aşınma kabartısı. Koşu 50 milyon yıl, 75 ile 230 s.

Denemeler (en yüksek nokta, en kalın kabuk):
- okyanus zayıf (0,1 η0): okyanusta 10 m/yıl'a varan yapay akış, karada eksi yükseklik; atıldı.
- okyanus dayanıklı (10 η0), çekirdek 700 km: deformasyon geniş, yer yer kıyıda 85 km sivri kabuk (kıyı itme yapaylığı).
- Voronoi levhalar (deniz bloğuyla gider), kıyıda Γ için en yakın karanın kalınlığı, η0 1e22: kuzeydoğuda geniş sıkışma bölgesi, batı köprüsünde ve yarımada çevresinde kuşak; en yüksek 1614 m, kabuk 55 km.
- gerinim zayıflaması (0,1 ve 0,3): deformasyon fay ağına yerelleşti ama kalınlaşma azaldı (kabuk 40 ile 46 km).

Hacim dengesi (Voronoi, zayıflamasız): karada kalınlaşma yaklaşık 4 km³/yıl, deniz hücrelerinde (dalma ile tüketilen) yaklaşık 3 km³/yıl, aşınma yaklaşık 3,6 km³/yıl. Dağlar alçak çünkü aşınma gelen kabuğun neredeyse tamamını götürüyor ve kısalma 1500 km genişliğe yayılıyor. Sırada: bilinen bir örnekle ayar (Hindistan büyüklüğünde katı itici, England ve Houseman deneyleri) ve aşınmanın çözünürlükten bağımsız hâle getirilmesi.

## Gerçek dünya deneyi (12 Kasım 2026)

`deneyler/dunya.py`, `tektonik/levha_model.py`. Bugünkü kıyılar GMT earth_relief 10' (SRTM15+ türevi) verisinden; Avrasya sabit, Hindistan 50 ile 20 milyon yıl 5 cm/yıl K20°D sonra 4 cm/yıl K15°D, Arabistan 25 milyon yıldır 2 cm/yıl K15°B, Afrika 0,6 cm/yıl K30°B (GPS ve levha modellerinden yuvarlandı: Hindistan 33 ile 52 mm/yıl, Arabistan 17 ile 30 mm/yıl, Afrika yaklaşık 5 mm/yıl). Başlangıçta kabuk her yerde 35 km. 50 km, 270 × 350 ızgara, koşu yaklaşık 2 dakika. Gerçek yükseklik aynı ızgaraya hücre ortalamasıyla örneklendi (ilk koşuda veri ölçek katsayısı 0,5 atlanmıştı, düzeltildi).

Hücre ortalaması ortancaları (m), model / gerçek:

| ayar | Tibet | Himalaya | Zagros | İran | Alpler | Tien Şan | Moğolistan | Sibirya |
|---|---|---|---|---|---|---|---|---|
| η0 1e22, K 4e-9, Avrasya çekirdeği 700 km | 442 / 4986 | 1328 / 3228 | 515 / 1287 | 454 / 1084 | 73 / 1064 | 149 / 1776 | 158 / 1521 | 135 / 222 |
| η0 1e22, K 1e-10, 700 km | 4417 | 6359 | 1911 | 1975 | 298 | 303 | 303 | 303 |
| η0 1e22, K 2e-10, 2500 km | 2674 | 3271 | 1207 | 1249 | 772 | 2155 | 1608 | 303 |
| η0 3e22, K 2e-10, 2500 km | 3135 | 4327 | 1080 | 1159 | 743 | 2227 | 1447 | 303 |
| η0 1e22, K 2e-10, 3500 km | 2310 | 2942 | 956 | 995 | 692 | 1732 | 1334 | 1059 |

Bulgular: (1) K = 4e-9 ile aşınma (yaklaşık 6 km³/yıl) tektonik girdiyi (yaklaşık 4,6 km³/yıl) aşıyor, dağ oluşmuyor; gerçekçi bölge ortalamaları K ≈ 1e-10 ile 2e-10'da. (2) Avrasya'nın katı çekirdeği Hindistan'a 700 km'de başlayınca Tien Şan ve Moğolistan oluşmuyor; 2500 km'de oluşuyor. (3) En iyi ayarda Himalaya, Zagros, İran, Tien Şan, Moğolistan yüzde 25 içinde; Tibet yaklaşık yarısı (2674 / 4986), Alpler düşük (Adriya mikro levhası yok). (4) Görünüm gerçekçi değil: yükseklik Orta Asya'ya yayılmış düzgün bir kubbe; Tarim, Junggar, Sichuan gibi katı havzalar ve keskin plato kenarı yok. Eksik fizik: dayanım farkları (kratonlar), orografik yağış (dar ıslak cephe, kurak iç), kabuğun yatay taşınması (Hindistan'ın kuzeye ilerleyişi Euler çerçevesinde yok).

### Sert çekirdekler ve yağış

Sert bölgeler (Tarim, Junggar, Sichuan, Ordos, Kuzey Çin, Sibirya ve Doğu Avrupa kalkanları; elle kabaca çizildi) viskozite çarpanı 10 (ya da 5), 150 km yumuşak kenar. Yağış: dört yönden eşit esen nemli hava; karada her hücrede q (h/L + yükselme/Hc) yağar (L 3000 km, Hc 1500 m, taban 0,15); kıyıdaki ilk sıçrama yamaç sayılmaz. Aşınma yağışla toplanan suya bağlı (fastscapelib accumulate ağırlıklı).

| ayar | Tibet | Himalaya | Zagros | İran | Alpler | Tien Şan | Moğolistan |
|---|---|---|---|---|---|---|---|
| gerçek | 4986 | 3228 | 1287 | 1084 | 1064 | 1776 | 1521 |
| sert yok, yağış yok, K 2e-10 | 2674 | 3271 | 1207 | 1249 | 772 | 2155 | 1608 |
| sert 10, yağış yok, K 2e-10 | 2776 | 3920 | 1462 | 1581 | 675 | 755 | 1353 |
| sert 10, yağış, K 5e-10 | 2875 | 4044 | 979 | 1433 | 461 | 770 | 1259 |
| sert 10, yağış, K 1e-9 | 2570 | 3746 | 722 | 1214 | 325 | 707 | 1038 |
| sert 5, yağış, K 1e-9 | 2591 | 3638 | 715 | 1167 | 335 | 979 | 1115 |

Görünüm: katı havzalar (Tarim, Junggar, Sichuan) alçak kaldı, plato kenarı keskinleşti. Sayılar karışık: Tien Şan Tarim katılaşınca düştü (sert çokgen ve 150 km yumuşatma Tien Şan kutusuna taşıyor olabilir), Tibet hâlâ yarı. Yağış kıyıda yoğun, içeride kurak; Himalaya önü belirgin ıslanmıyor (güney rüzgârı Hindistan'ı geçerken nemini kaybediyor; muson yok). En büyük kalan eksik: kabuğun yatay taşınması.

### Kabuk taşıma

Yarı Lagrange taşıma (`LevhaAyar.tasima`): her adımda kabuk kalınlığı ve aşınma kabartısı hız alanıyla taşınır (doğrusal ara değer), kalkış noktası denizdeyse gelen kabuk 35 km; kıyı sabit. Sonra −S ∇·u kalınlaşması. Sert bölge kenar yumuşatması 150 km'den 50 km'ye indirilince Tien Şan geri geldi (Tarim sertliği Tien Şan'a taşıyordu).

| ayar | Tibet | Himalaya | Zagros | İran | Alpler | Tien Şan | Moğolistan |
|---|---|---|---|---|---|---|---|
| gerçek | 4986 | 3228 | 1287 | 1084 | 1064 | 1776 | 1521 |
| taşıma, η0 1e22, sert 10, yağış, K 5e-10 | 3028 | 3332 | 946 | 1255 | 420 | 566 | 1129 |
| taşıma, η0 3e22, sert 10, yağış, K 5e-10 | 4175 | 4093 | 847 | 1220 | 418 | 475 | 1043 |
| aynı, kenar 50 km | 4671 | 4075 | 762 | 1112 | 418 | 1543 | 1540 |
| η0 2e22, kenar 50 km | 3480 | 3298 | 835 | 1158 | 421 | 2591 | 1451 |
| η0 3e22, sert 5, kenar 50 km | 4089 | 3594 | 772 | 1126 | 422 | 1004 | 1161 |

Seçilen ayar (η0 3e22, sert 10, kenar 50 km, yağış, K 5e-10, taşıma): Tibet %94, Himalaya %126, İran %103, Tien Şan %87, Moğolistan %101, Zagros %59, Alpler %39 (Adriya yok). Bilinen görsel kusurlar: 50 km'de akarsular düz ışınsal çizgiler; Kazakistan ve Turan alçak düzlükleri modelde fazla yüksek; Tibet'in düz tepesi yok.

### Orta ölçek (160 ile 270 km) denemeleri

Ölçüt: Orta Asya kutusunda (60 ile 110°D, 25 ile 50°K) dalga boyuna göre güç oranı model / gerçek ve 150 km yerel engebe ortancası (gerçek 272 m). Taban ayar: η0 3e22, sert 10, kenar 50 km, yağış, K 5e-10, taşıma.

| deneme | 271 km | 203 km | 162 km | engebe |
|---|---|---|---|---|
| taban (bükülme 80 km) | 0,63 | 0,39 | 0,36 | 132 |
| dayanım dokusu σ 0,5 ve 0,7 (iki tohum) | 0,15 ile 0,35 | 0,13 ile 0,26 | 0,16 ile 0,38 | 152 ile 194 |
| doku σ 1 | 1,61 | 0,72 | 1,23 | 260 (Himalaya 722 m'ye düştü) |
| doku σ 1 + zayıf hatlar | 0,12 | 0,22 | 0,31 | 183 |
| bükülme 40 km | 0,70 | 0,47 | 0,27 | 117 |
| bükülme 25 km | 0,65 | 0,42 | 0,24 | 114 |

Sonuç: ne dayanım dokusu ne kısa bükülme orta ölçeği sistemli biçimde getirdi; doku sonucu tohuma göre savuruyor. 25 km çözünürlük koşusu yarıda durduruldu (50 milyon yılın yarısı 24 dakika). Karar: fizik 50 km'de yalnızca 300 km üstü düzen için; orta ve küçük ölçek gerçek yükseklik verisinden bağlama uygun ayrıntı katmanıyla.

## Ayrıntı katmanı denemeleri (12 Kasım 2026)

`deneyler/ayrinti.py`. Kütüphane: Güney ve Kuzey Amerika, Afrika, Avrupa (GMT earth_relief 06', 10 km LAEA); 480 km'lik 1769 parça, kaba yükseklik, kaba eğim ve kaba engebeyle etiketli, eğime göre döndürülmüş. Hedef: levha modelinin Asya'sı (50 km'den 10 km'ye). Asya kütüphanede yok.

- Ağırlıklı ortalama harmanlama: bağımsız parçalar birbirini söndürdü (60 km'de güç oranı 0,06).
- Varyansı koruyan harmanlama: 100 km'de 0,63, 60 km'de 0,73; 30 km engebe 89 m (gerçek 137), 90 km engebe 185 m (gerçek 278). Görünüm: her yere serpilmiş pürüz, kesintisiz sıra yok.
- Eş yükselti yönüne hizalı yönlü sırtlar + parçalar: 100 km 0,46, 60 km 0,51, 25 km 0,92; engebe 85 / 137 ve 193 / 278 m. Sırtlar oluştu ama Tibet'in yerine ve biçimine göre değil, modelin kubbesine göre.

Önemli düzeltme: önceki "400 km üstünde model doğru" yargısı güç spektrumuna dayanıyordu; güç spektrumu biçimi (faz) ölçmez. Görsel karşılaştırmada büyük biçimler de farklı: model Tarim çevresinde sarmal bir halka, Orta Asya'da kubbe üretiyor; gerçek Tibet doğu batı uzanan, keskin kenarlı bir plato ve Tarim düz bir havza. Spektrum ölçütü biçim için yetersiz.

## Örnek tabanlı sıradağ: gerçek dağ sistemini dikişe bükme (12 Kasım 2026)

`deneyler/nakil.py`. Kaynak dağ sistemi kendi dikişine göre (boyuna s, işaretli uzaklık d) koordinatlanır, sahibin duvar dikişine taşınır. Boyuna en çok 1,2 kat esneme, kalan uzunluk kaynağı aynalayarak; plato tarafı (d > 300 km) kaynağın plato şeridini aynalayarak tekrarlar (ölçek değişmez). Kenarlar 400 km geçiş, uzaklıklar 160 + 50 m genlikli gürültüyle bozulur (yalnız uzaklık; doğrudan ağırlığa eklenen gürültü uzakta rastgele dağ lekeleri doğurmuştu). Arka plan şimdilik gürültülü düz ova. Aşınma ve izostazi yok. 0,1° ızgara, koşu birkaç saniye.

- Zagros ve İran platosu: sıradağ p95 2324 m, en yüksek 3345 m; çanak ortancası 197 m (çizilen sarı alanın bir kısmı geçiş bölgesinde ve arka planda kalıyor).
- Himalaya ve Tibet: sıradağ p95 5435 m, en yüksek 6188 m; çanak ortancası 1185 m, p90 4980 m (Tibet istenen 1000 ile 1500 m'den çok yüksek).

Görünüm: taşınan bölgenin içi gerçek dağ dokusunda; kenarlar düzensiz. Kusurlar: aynalama yer yer simetrik tekrar olarak görünüyor; çevredeki düz arka plan taşınan bölgeyi yapıştırılmış gösteriyor; tek bir kaynak isteklere tam uymuyor (Zagros sıradağı küçük, Tibet çok yüksek).

### Birleşik örnek (Himalaya sıradağı + İran çanağı + gerçek arka plan)

`deneyler/nakil2.py`, koşu yaklaşık 2 saniye. Sıradağ şeridi Himalaya'dan (dikişin 400 km önünden 350 km gerisine, aynalı), çanak İran platosunun iç şeridinden (Ana Zagros bindirmesinin 300 ile 620 km kuzeydoğusu, aynalı) sabit yükseltmeyle (+536 m); geçiş dikişin 120 ile 300 km gerisinde, düzensiz. Kıtanın geri kalanı yedi dağsız gerçek bölgeden 1200 km'lik rastgele döndürülmüş parçalar (ortalama düzey ağırlıklı ortalama, ayrıntı varyansı koruyan).

Sonuç: sıradağ (kırmızı) p95 5417 m, en yüksek 5889 m; sarı alanın ortancası 648 m (p10 353, p90 1831), çünkü sarı çokgenin bir kısmı geçiş ve arka planda kalıyor; çanak iç bölgesinin ortancası tanım gereği 1250 m; kara ortancası 434 m.

Hatalar ve düzeltmeler: Himalaya d'si 150 km'de kesilince ötesi aynı çizginin tekrarıyla doldu (düz çizgiler); aynalamaya çevrildi. Çanağı dikey germek (× 1,75) dağları sertleştirdi; sabit yükseltmeye çevrildi.

Kalan kusurlar: sıradağın arkasında Tibet'in güney kenarı 5 km'lik beyaz bir şerit olarak taşınıyor; aynalama yer yer tekrar gösteriyor; çanağın batı kenarı arka plana sert geçiyor; nehir ağı parçalar arasında kopuk (aşınma koşusu yok).

### Taban + gerçek doku (tekrarsız)

`deneyler/nakil3.py`, koşu yaklaşık 3 saniye. Sahibin geri bildirimi: birleşik örnekte tekrar eden kalıp ve "sonradan konmuş" görünüm. Nedenleri: aynalama ve gerçek parçanın tüm yüksekliğiyle (kendi bölgesel eğimi ve ova düzeyiyle) yapıştırılması. Yeni yöntem: yumuşak taban (sıradağ profili, çanak 1250 m, ova 250 ± 180 m) + ortalaması sıfır doku (gerçek verinin 120 km Gauss'la yüksek geçiren kısmı). Kütüphane: dağ 294 parça (8 kuşak), plato 174 (7 plato), ova 786 (7 bölge); 400 km'lik parçalar sırt yönüne göre döndürülmüş, hedefte dikiş boyuna çevrilir; son 30 seçim tekrar edilmez; varyansı koruyan harmanlama. Aynalama yok. Çanak kenarı çokgene uzaklığın gürültüyle bozulmasıyla düzensiz.

Sonuç: çanak iç ortanca 1369 m (p10 957, p90 1887), sıradağ p95 4291 m, en yüksek 6088 m, kara ortancası 221 m. Görünüm: kenar basamağı ve tekrar yok; doku gerçek kuşaklara göre daha yuvarlak ve benekli (keskin uzun sırtlar az); nehir ağı yok.

### Aşınma koşusu (örnek tabanlı kabartmanın üstünde)

`deneyler/asindir_son.py`. Lat-lon kabartma 10 km Lambert eşit alanlı ızgaraya taşındı (yaklaşık 920 × 720), fastscapelib akarsu aşınması m 0,5, n 1, K 1e-6, 2 milyon yıl (100 adım × 20 000 yıl), 80 km bükülmeyle geri sıçrama 0,85; sonra lat-lon'a geri. Süre 20 s (adım başına 0,2 s). Ortalama aşınma 211 m, en çok 4354 m; en yüksek nokta 6148 m, kara ortancası 191 m. Görünüm: ağaç dallanmalı vadiler, sıradağda yan sırtlar, nehir ağı kıyılara bağlı; çanaktan çıkan nehirler sıradağı yararak denize iniyor (çanak dışa akışlı oldu; İran platosu gerçekte büyük ölçüde iç akışlı). 0,4 milyon yıl ile K 5e-7: ortalama aşınma 18 m, etkisi az.
