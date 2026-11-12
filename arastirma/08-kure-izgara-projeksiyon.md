# 8. Küre geometrisi, ızgaralar ve projeksiyonlar

Araştırma tarihi: 12 Kasım 2026. Belge üç Haiku kolunun sentezidir (A ızgaralar ve akış yönlendirme, B projeksiyon ve alan ölçümü, C kürede dönme ve topoloji); sentezi ben yazdım. Ham notlar `arastirma/notlar/08/` içinde. Etiketler: **[B]** birincil metin okundu, **[D]** resmi belgelendirme okundu, **[Ö]** arama özeti, **[E]** ansiklopedi, **[H]** hesap (bizim ya da ajanın; yöntem yazılı), **[Y]** bulunamadı.

Önemli düzeltme: B kolu kıtanın enlem bandını yanlış varsaydı (10K ile 77K). Karar günlüğündeki gerçek kutu 7G ile 60K, 44B ile 43D (67° enlem, 87° boylam, kuzey güney yaklaşık 7450 km). B kolunun enleme bağlı bozulma sayıları (ör. Mercator 60K'da 4) bu yüzden başka bir banda ait; aşağıda yalnızca formüller ve doğru banda göre yeniden hesapladığım değerler kullanıldı. Albers önerisi B'nin hesabından geliyor ve yeni banda göre yeniden doğrulanmadı.

## Kısa sonuç

**1. Hesap ızgarası için HEALPix ya da ikosahedral ağ, gösterim için eşdikdörtgen ızgara.** HEALPix tüm hücreleri eşit alanlı yapar: Npix = 12 Nside², hücre alanı π/(3 Nside²) steradyan (Górski ve diğerleri 2005, [B]). Fastscapelib HEALPix ızgarasını destekliyor ve varsayılan yarıçapı 6,371e6 m [D]. Landlab'ın küresel ızgarası ikosahedral (`IcosphereGlobalGrid`); HEALPix ve enlem boylam ızgarası yok [B kaynak kodu].

**2. Aracın kıtası kutuptan uzak olduğundan eşdikdörtgen ızgara kabul edilebilir.** 60K'de eşdikdörtgen hücre ekvatora göre yarı genişlikte (cos 60° = 0,5); yani 5 km derece-başı ızgara kuzey kenarında doğu batı yönünde yaklaşık 2,5 km'ye iner [H]. Bu, akış yönlendirmede yön sapması ve zaman adımı sınırı yaratır; HEALPix bunu ortadan kaldırır.

**3. Alan ölçümü her zaman enlem ağırlıklı yapılmalı.** Hücre alanı R² Δλ (sin φ2 − sin φ1) [B]; piksel sayısı kullanılırsa gerçek alan oranı yanlış çıkar. Bizim 7G ile 60K bandında kıtanın küresel alanı yaklaşık 60,9 milyon km², satır başı ortalama cos ağırlığı 0,845 [H].

**4. Gerçek hesap pyGPlates / GPlately ile.** Dönme açıları radyan, pozitif saat yönünün tersi; hız v = Ω R sin δ; çakışma ve boşluk denetimi için resmi topoloji örneği var [B].

## 1. Izgara seçenekleri

| Izgara | Özellik | Not | Etiket |
|---|---|---|---|
| Eşdikdörtgen | hücre alanı R² Δλ (sin φ2 − sin φ1) | 5 km derece-başı ızgarada küre geneli yaklaşık 32 milyon hücre; kutup hücresi çok dar ve uzun, sorun alandan çok en-boy oranı | [B ve H] |
| HEALPix | tüm hücreler eşit alan, 12 Nside² hücre, 12 taban piksel | kenarlar jeodezik değil. R = 6371 km için Nside 256 yaklaşık 25,5 km, 512 yaklaşık 12,7 km, 1024 yaklaşık 6,4 km (ajanın hesabı); 5 ve 20 km tam tutmuyor | [B ve H] |
| İkosahedral (Landlab) | 4'lü bölme, hücre sayısı 10·4ⁿ + 2 | seviye 9 yaklaşık 2,6 milyon hücre, yaklaşık 14 km; seviye 10 yaklaşık 10,5 milyon, yaklaşık 7 km (Euler formülü, kod çalıştırılmadı) | [B ve H] |
| Küp küre | | Putman ve Lin (2007) yalnızca arama özetinde, düzgünlük sayısı bulunamadı | [Ö] |

**Landlab** ızgara türleri: FramedVoronoiGrid, HexModelGrid, IcosphereGlobalGrid, NetworkModelGrid, RadialModelGrid, RasterModelGrid, VoronoiDelaunayGrid [B]. Sınıf adı `IcosphereGlobalGrid`, ajanın ilk yazdığı `IcosphereGrid` değil.

**Fastscapelib** ızgara türleri: profil, raster (8 komşu), üçgen ağ, HEALPix [Ö ve D].

**goSPL** (Salles 2020, JOSS, doi 10.21105/joss.02804): yapısal olmayan küresel ağ; çok yönlü akış yönlendirme, 1 ile 6 yön, ağırlıklar toplamı 1 [B]. Makale "Voronoi ya da Delaunay" demiyor [B].

**Akış yönlendirme.** goSPL belgesi tek yönlü yönlendirmenin ağ geometrisine çok duyarlı olduğunu yazıyor [D]. Landlab FlowDirectorMFD hem raster hem düzensiz ızgarada çalışıyor [Ö]; Landlab depresyon bulucu yalnızca SteepestDescent ve D8 ile çalışıyor, MFD ile çalışmıyor [Ö]. Bu, 13. konuda (erozyon motoru) önemli bir kısıt.

## 2. Projeksiyon ve bozulma

Snyder (USGS PP 1395, 1987) [B]: bozulma ölçüleri h (meridyen ölçeği), k (paralel ölçeği); alan ölçeği h × k; en büyük açısal bozulma ω için sin(ω/2) = |a − b| / (a + b). Bölgesel, doğu batı yönünde uzanan orta enlem kıtası için Snyder Albers eşalan koniği öneriyor [B].

Gerçek banda (7G ile 60K) göre değerler [H]:

| Projeksiyon | Alan ölçeği |
|---|---|
| Eşdikdörtgen | 1/cos φ: 7G'de 1,01; 30K'de 1,15; 45K'de 1,41; 60K'de 2,00 |
| Mercator | 1/cos² φ: 30K'de 1,33; 45K'de 2,00; 60K'de 4,00 |
| Lambert eşalan silindirik | alan korunur, ama şekil bozulur |
| Albers eşalan konik | alan korunur; B kolu 10K ile 77K bandı için en büyük açısal bozulmayı 31,7° buldu. Gerçek band için yeniden hesaplanmadı |
| Lambert konform konik | açı korunur; B kolunun bandında en büyük alan sapması 0,357 |

Robinson, Winkel tripel ve Mollweide formüllerinin birincil metni doğrulanmadı [Y].

**Telefon gösterimi.** Web Mercator (EPSG:3857, "Pseudo-Mercator"): küre yerine R = a = 6378137 m yarıçaplı, konform değil, 88°'nin üstünde kullanılmamalı, enlem sınırı 85,0511° [D]. Hayali gezegenimizde (R = 6371 km) bu yarıçap farkı yalnızca ölçek, şekil değişmez. Mercator'un 60K'deki alan ölçeği 4; yani kuzey kenarında alanlar 4 kat büyük görünür. MapLibre stil belgesinde `projection` varsayılanı "mercator" [B]; MapLibre GL JS 5'te küre desteği yalnızca arama özetinde [Ö]. deck.gl GlobeView deneysel, zoom 12'nin üstünde yüksek hassasiyetli değil [B]. Leaflet özel CRS arayüzü var ama hazır Mercator dışı projeksiyon bulunamadı [Y]. Tuval (canvas) ile elle çizim aranmadı [Y].

## 3. Alan ve mesafe ölçümü

- Kürede hücre alanı R² Δλ (sin φ2 − sin φ1) [H, B kolunun hesabı]; 1°×1° hücre ekvatorda 12 363,7 km², 60K'de 6 088,4 km²; tüm hücrelerin toplamı 4πR² ile tam örtüştü [H].
- Piksel sayısına göre yüzde ile alana göre yüzde farklı: ajanın yanlış bandında bu fark yüzde 37,22 ile yüzde 40,04; yani piksel sayımı alanı eksik tahmin eder. Bizim bantta satır ağırlığı ortalaması 0,845 [H].
- Mesafe: haversine (R = 6371 km) pyproj'un küre üzerindeki kesin jeodezik sonucuyla aynı; WGS84 elipsoidine göre fark yüzde −0,36 ile yüzde +0,56 [H]. Meridyen boyunca 67° = 7450,1 km (R = 6371), karar günlüğündeki değerle tutarlı. Hayali gezegenimiz küre olduğundan elipsoid düzeltmesi gerekmez.
- Maske alanı için iki yol: (a) satır satır R² Δλ (sin farkı) toplamı; (b) maskeyi eşalan CRS'ye gdalwarp ile yeniden projekte edip piksel sayısı çarpı piksel alanı [B ve D]. Her iki yol da maskenin georeferansını (piksel → enlem boylam) gerektirir; GDAL ve rasterio bu ortamda kurulu değil, çalıştırılmadı.

## 4. Kürede dönme, hız ve topoloji

- `pygplates.FiniteRotation(pole, angle_radians)`: açı radyan, pozitif saat yönünün tersi; bileşke r1 * r2 ya da `compose(r1, r2)`, değişmeli değil; ters için `get_inverse()`; poligonu döndürmek için `fr * polygon` [B].
- Poligon alanı `PolygonOnSphere.get_area()` steradyan; km² = alan × R². `pygplates.Earth.mean_radius_in_kms` = 6371,009 km [B]. Bizim gezegende 6371 kullanılacak (karar günlüğü).
- Kuaterniyon w = cos(θ/2), vektör kısmı sin(θ/2) u; Rodrigues formülü standart [H, E].
- Hız: v = Ω R sin δ (δ Euler kutbuna açısal uzaklık, Carleton ders notu, [B]); 1°/milyon yıl için v ≈ 11,1 cm/yıl × sin δ [H]. Kutupta hız sıfır, δ = 90°'de en büyük.
- `pygplates.calculate_velocities(domain_points, finite_rotation, time_interval_in_my, velocity_units=...)` [B]; `ReconstructSnapshot.get_point_velocities` varsayılan km/milyon yıl; cm/yıl için `velocity_units` verilmeli [B]; GPlately `PlateReconstruction.get_point_velocities(lons, lats, time)` varsayılan km/milyon yıl [B]. "PlateTectonicReconstruction" ve "FiniteRotation.get_velocities" resmi API olarak bulunamadı [Y].
- Dönüşüm fayları Euler kutbu çevresinde küçük daireler boyunca uzanır, sırt segmentleri büyük dairedir [Ö, Wikipedia ve arama özeti]. pyGPlates'te küçük daire yayı için `get_rotation_distance`, büyük daire için `create_great_circle_point_rotation` ve `great_circle_arc` [B].
- **Çakışma ve boşluk denetimi.** Resmi pyGPlates yöntemi: `TopologicalModel`, `topological_snapshot(t)`, `get_shared_sub_segments()`; her alt segment tam iki çözümlenmiş topoloji tarafından paylaşılmalı, aksi halde boşluk ya da örtüşme var [B]. Shapely düzlemsel; kutup ve antimeridyen sorunları, projeksiyona geçmek gerekir [Ö]. R `s2` paketinde küresel kesişim, birleşim, fark ve alan var [D]. `spherely` erken aşamada, fonksiyon adları bulunamadı; `s2sphere` için Boolean desteği doğrulanamadı [Y].
- Gurnis ve diğerleri (2012), Computers & Geosciences 38(1), 35 ile 42, doi 10.1016/j.cageo.2011.04.014 (sürekli kapalı levha poligonları). Önceki promptumdaki "G-cubed" yanlıştı; tam metin ve denklemler okunamadı (PDF 404) [Y].

## 5. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Gezegen yarıçapı | 6371 km | karar günlüğü |
| Hesap ızgarası | HEALPix Nside 512 (12,7 km) ile 1024 (6,4 km) ya da ikosahedral seviye 9 ile 10; 5 ile 20 km istenirse Nside 256 ile 2048 | [H] |
| Gösterim ızgarası | eşdikdörtgen, mask çözünürlüğüne bağlı | karar günlüğü |
| Alan ağırlığı | R² Δλ (sin φ2 − sin φ1), ya da HEALPix'te sabit | [B] |
| Mobil gösterim | eşdikdörtgen ya da Albers eşalan koniği, Web Mercator değil (60K'de alan 4 kat) | [H] |
| Dönme açıları | radyan, saat yönünün tersi pozitif | [B] |
| Hız hesabı | v = Ω R sin δ; 1°/milyon yıl yaklaşık 11,1 cm/yıl × sin δ | [B ve H] |
| Çakışma denetimi | pyGPlates topolojik snapshot; bağımsız denetim için s2 | [B ve D] |

## 6. Kaynaklar arası çelişkiler

- Izgara adı: Landlab'ın küresel ızgarasının adı `IcosphereGlobalGrid`, `IcosphereGrid` değil (ajan düzeltti).
- HEALPix çözünürlüğü 5 ve 20 km ile tam örtüşmüyor; Nside 256/512/1024 = 25,5/12,7/6,4 km.
- Gurnis 2012 yayın yeri: Computers & Geosciences (doğru), G-cubed (promptumdaki yanlış).
- Wikipedia Mollweide sayfası 429, Esri 403 verdi; bu iki kaynakta doğrulama yapılamadı.

## 7. Bulunamayanlar ve doğrulanamayanlar

- O'Callaghan ve Mark (1984) D8 ve Freeman (1991) metinleri; mesh çok yönlü akış yönlendirme (Qin 2007); küp küre düzgünlük sayısı; Landlab `VoronoiDelaunayGrid` ile D8/MFD birleşiminin belgelerde doğrulanması.
- Robinson, Winkel tripel ve Mollweide birincil formülleri; Leaflet özel CRS ve MapLibre küre desteği birincil sayfada; GDAL'e özgü raster alan tarifi.
- Gurnis 2012 tam metni ve denklemleri; `spherely` ve `s2sphere` Boolean desteği; "kuyruk durumu" ifadesi (benim promptumdaki belirsiz ifade; kutup yakını sıfır hız durumu olarak yorumlandı).
- gplately.readthedocs.io 404; courseware.e-education.psu.edu ve open.edu yalnızca arama özetiyle; WebFetch bazı sitelerde DNS hatası verdi, curl ile erişildi.
- GDAL CLI ve rasterio ortamda kurulu değil; ajanın hesapları pyproj ile yapıldı, GDAL tarifi çalıştırılmadı.

## 8. Promptumdaki hatalar (düzeltildi)

- B kolunun promptunda kıta bandını 10K ile 77K olarak varsayması ajanın değil benim eksiğimdi: gerçek banda ait kodları ("60K-7G, 44B-43D") koordinata çevirmedim. Karar günlüğündeki değer 7G ile 60K, 44B ile 43D.
- "IcosphereGrid" adı yanlış; sınıf `IcosphereGlobalGrid`.
- "PlateTectonicReconstruction" adlı pyGPlates sınıfı yok; GPlately'de `PlateReconstruction` var.
- Gurnis ve diğerleri (2012) G-cubed'de değil, Computers & Geosciences'ta.

## Başlıca kaynaklar

- Górski ve diğerleri 2005, HEALPix: https://arxiv.org/abs/astro-ph/0409513
- Salles ve diğerleri 2020, goSPL, JOSS: https://doi.org/10.21105/joss.02804
- Snyder 1987, USGS PP 1395: https://pubs.usgs.gov/pp/1395/report.pdf
- pyGPlates FiniteRotation: https://www.gplates.org/docs/pygplates/generated/pygplates.FiniteRotation.html
- pyGPlates boşluk ve örtüşme örneği: https://www.gplates.org/docs/pygplates/sample-code/pygplates_detect_topology_gaps_and_overlaps.html
- Gurnis ve diğerleri 2012: https://doi.org/10.1016/j.cageo.2011.04.014
- Tam liste ve her bilginin kaynağı `arastirma/notlar/08/` içinde.
