# B: Projeksiyon ve alan ölçümü notları

Durum: ARA SÜRÜM. Kalan kaynaklar (Leaflet, MapLibre, deck.gl, GDAL, USGS PDF, Vincenty) henüz okunmadı.

Etiketler: [B] birincil metin okundu (doğrudan sayfa/PDF), [D] resmi belgelendirme (EPSG, pyproj API), [Ö] özet/arama sonucu, [E] ansiklopedi (Wikipedia), [H] benim hesabım (kod ve sayılar aşağıda; kaynak bağımsız, yeniden üretilebilir).

Erişim notu: Doğrudan WebFetch pubs.usgs.gov, esri.com, epsg.org, pyproj4.github.io, geo.hunter.cuny.edu için DNS hatası verdi. curl ile pubs.usgs.gov, epsg.org ve pyproj4.github.io indirildi (200); esri.com 403 döndü. en.wikipedia.org sayfaları curl ile indi (Mollweide sayfası 429 hız sınırı verdi).

Hesap betikleri (proje dışında, scratchpad): tissot_calc.py ve dist_calc.py. pyproj 3.8.0 geçici dizine kuruldu (scratchpad/pylib).

## 1. Bozulma (distorsiyon) ölçüleri ve projeksiyon seçimi

### 1a. Ölçüt tanımları
- [E] Tissot göstergesi: bir noktadaki küçük dairenin projeksiyondaki elipsi; a = en büyük, b = en küçük ölçek faktörü. Alan bozulması a·b; açısal bozulma en çok ω = 2·asin((a−b)/(a+b)). Konforman projeksiyonda elips daire olur (a = b). Eşalanlı projeksiyonda a·b = 1 (her yerde). [E] Wikipedia "Tissot's indicatrix"; ω formülü [D] EPSG 1024 sayfasında da aynı biçimde geçer.
- [D] EPSG Guidance: ω = 2 asin(|h−k|/(h+k)) (h meridyen, k paralel ölçeği).
- Snyder USGS PP 1395 (kitabın kendisi): [B] pubs.usgs.gov kaydı okundu: "Snyder, J., 1987, Map projections: A working manual: U.S. Geological Survey Professional Paper 1395, ix, 385 p., doi 10.3133/pp1395", yayıncı US GPO, Washington. Kayıtta "Document: Report (pdf)" bağlantısı var; PDF'in kendisi bu oturumda okunmadı, Tissot bölümünün tam metni BULUNAMADI. [Ö] arama sonuçları Tissot bölümünün 20. sayfa civarında "Scale variation and angular distortion" başlığı altında olduğunu söylüyor; bu sayfa numarası doğrulanmadı.

### 1b. Sayısal karşılaştırma [H]
Hesap: R = 6371 km küre; Tissot Jacobian'ı pyproj 3.8.0 ile sonlu farkla. Varsayılan bölge: 10°K–77°K enlem bandı (67° yayılım, R=6371'de ≈7450 km). Boylam ofsetleri 0°, 15°, 30°. Konik projeksiyonlar için standart paralel = band'in 1/6 ve 5/6'ı (21,2° ve 65,8°), lat0 = 43,5°.

| Projeksiyon | Band'da en büyük \|a·b−1\| | Alan-ağırlıklı ortalama \|a·b−1\| | En büyük ω (°) |
|---|---|---|---|
| Eşdikdörtgen (equidistant cyl., std 0) | 3,445 | 0,463 | 78,5 |
| Mercator | 18,76 | 1,521 | 0 (konform) |
| Lambert eşalanlı silindirik (cea) | 0 | 0 | 129,3 |
| Mollweide | 0 | 0 | 54,8 |
| Robinson | 0,782 | 0,143 | 66,8 |
| Winkel Tripel | 1,912 | 0,280 | 59,0 |
| Albers eşalanlı konik (aea) | 0 | 0 | 31,7 |
| Lambert konform konik (lcc) | 0,357 | 0,102 | 0 (konform) |

Nokta değerleri (boylam ofseti 0): 
- Mercator: 45°'de a=b=1,414, a·b=2,000; 60°'de a·b=4,000; 75°'de a·b=14,93.
- Eşdikdörtgen: 60°'de a=2,000, b=1,000 (a·b=2,000); 75°'de a·b=3,864 (=1/cos75°).
- cea: a·b=1 her enlemde; ama 60°'de a=2,000, b=0,500, ω=73,7°.
- Mollweide: 45°'de a=1,026, b=0,975, ω=3,0°; 75°'de ω=43,2°.
- Winkel Tripel: 45°'de a·b=1,262; 60°'de 1,605.
- Robinson: ekvatorda a·b=0,815; 45°'de 0,944; 60°'de 1,238.

Yorum [H]: Bu bant için alan bozulmasını ve açısal bozulmayı birlikte en düşük tutan seçenek, konik projeksiyonlar (Albers veya LCC) oldu; Albers alanı korur, açıyı en çok 31,7° bozar; LCC açıyı korur, alanı en çok ~%36 değiştirir. Mercator ve eşdikdörtgen bu bant için uygun değil. Bu bulgu sadece varsayılan bant içindir; gerçek kıtanın enlem/boylam kutusu bilinmediği için sonuç yeniden hesaplanmalı.

Robinson tablosu [E] Wikipedia "Robinson projection" (5° aralıklı PLEN/PDFE tablosu) okundu: 0°: 1,0000/0,0000; 45°: 0,8962/0,5571; 90°: 0,5322/1,0000. Robinson "ne eşalanlı ne konform" diye tanımlanıyor [E]. Robinson'ın tam ölçek sabitleri bu oturumda doğrulanmadı.

Winkel Tripel: [E] sayfa okundu ama formül/tablo bu metinden çıkmadı; pyproj hesabı [H] kullanıldı.

Mollweide: [E] sayfası 429 (hız sınırı) verdi; Mollweide için değerler [H] pyproj ile hesaplandı (eşalanlılık kontrolü: a·b=1,000).

Açık kalan: Snyder'in PP 1395 metnindeki Tissot ve bozulma formüllerinin doğrudan okunması ve Snyder'ın önerdiği konik seçimi kuralı [B] olarak doğrulanmadı.

## 2. Alan ağırlıklı ölçüm: R² cos φ dλ dφ
- [H] Küre üzerinde 1°×1° hücre alanı (R=6371 km), A = R²·Δλ·(sin φ2 − sin φ1):
  - 0–1°: 12 363,7 km²; 30–31°: 10 653,3 km²; 45–46°: 8 666,2 km²; 60–61°: 6 088,4 km²; 75–76°: 3 095,7 km².
  - Kapalı formül R²(π/180)²cos(orta enlem) ile fark 0,1 km² (yuvarlama).
- [H] Tüm 1°×1° hücrelerin toplamı = 510 064 472 km² = 4πR² (tam eşleşme).
- [H] Enlem bandı 10–77°: gerçek alan oranı %40,04; satır sayımına göre (naif) %37,22. Eşdikdörtgen ızgarada piksel saymak alanı yanlış verir; her satır cos φ ile ağırlıklandırılmalı (ya da sin farkı kullanılmalı).
- [D] pyproj Geod.polygon_area_perimeter (pyproj API, pyproj4.github.io/pyproj/stable/api/geod.html, curl ile okundu): "Area (meters^2) and perimeter (meters) of a geodesic polygon", lons/lats derece (radians=False), sonuç tuple (alan, çevre). Pozitif alan saat yönünün tersi, negatif saat yönü.

## 3. Küresel mesafe (R = 6371 km): haversine, Vincenty, küresel yaklaşım
- [H] Haversine (R=6371 km) ile küre üzerindeki kesin jeodezik (pyproj Geod(a=R,b=R)) birebir aynı çıktı verdi (6 örnekte fark 0). Yani haversine bu küre modelinde doğru.
- [H] Haversine ile WGS84 elipsoid jeodezik arasındaki fark (%):
  - 1° meridyen, ekvator: +0,561 (111,195 vs 110,574 km)
  - 100 km civarı, 45°: +0,049
  - 1000 km doğu-batı, 45°: −0,279
  - 67° kuzey-güney (10→77°, 30° boylam): +0,077 (7450,06 vs 7444,34 km)
  - 30° doğu-batı, 60°: −0,363
  - Neredeyse antipodal: +0,001
- [H] Kuzey-güney 67° yayılım: küre (R=6371) 7450,1 km; WGS84 meridyen yayı 7444,3 km. Yani "yaklaşık 7450 km" ifadesi R=6371 ile tutarlı.
- Vincenty: [Ö] arama sonuçları Vincenty'nin elipsoid için ters formülü olduğunu, haversine'in küre varsayımı yaptığını söylüyor; [E] Wikipedia Vincenty sayfası indi (10 KB metin) ama hata/doğruluk cümlesi henüz taranmadı. pyproj ise Karney yöntemi kullanır, Vincenty değil; bu nedenle "Vincenty ile" karşılaştırması bu oturumda yapılmadı, sadece "pyproj/Karney ile" karşılaştırıldı. Vincenty'nin sayısal doğruluğu BULUNAMADI (bu oturumda doğrulanmadı).
- Kararlılık: [Ö] küçük mesafelerde küresel kosinüs yasası sayısal olarak kötü koşullanır; haversine bunu düzeltir. Antipodal yakınında haversine'de de büyük hata olabilir [Ö].

## 4. Telefon (mobil web) gösterimi
- [D] EPSG 1024 "Popular Visualisation Pseudo Mercator" (epsg.org, curl ile okundu): "applies standard Mercator (Spherical) formulas ... to ellipsoidal coordinates and the sphere radius is taken to be the semi-major axis"; R = a = 6378137 m; "this method is not conformal: scale factor varies as a function of azimuth"; "should not be used poleward of 88°".
- [D] EPSG 1024 formüller: h = R/(ρ cos φ) (meridyen), k = R/(ν cos φ) (paralel); ρ, ν WGS84 eğrilik yarıçapları.
- [E] Wikipedia "Web Mercator projection": "uses the equatorial radius of the WGS 84 spheroid"; "projected as if defined on a sphere". EPSG:3857 bunu 2011'den beri referans olarak kullanır.
- [Ö] ArcGIS ve diğer kaynaklar uç enlemi ~85°03'04" olarak verir; Web Mercator'da 85,0511° sınırı yaygın. (Bu değer [E]/[Ö] düzeyinde; bu oturumda doğrudan doğrulanmadı.)
- [H] Eşdikdörtgen ve Mercator için nokta ölçekleri: Mercator sphere: 60°'de a·b=4; EPSG 3857 hesabı için ayrı sayısal tablo henüz üretilmedi (EPSG formülünden hesaplanabilir; sonraki adım).
- Özel küresel projeksiyonlar (MapLibre, deck.gl, Leaflet):
  - [Ö] MapLibre GL JS 5.0.0 (Ocak 2025) "globe" projeksiyonunu ekledi; `setProjection` ile etkinleşir. MapLibre Native'de henüz yok [Ö, arama sonucu].
  - [Ö] deck.gl GlobeView, MapLibre'ın kamerasını MapboxOverlay üzerinden izler; deck.gl belgelerine göre MapLibre globe tam destekli. Kutuplara yakın veri için en iyi seçenek olarak tanımlandı [Ö, Development Seed Aralık 2024 değerlendirmesi, sürüm 5 öncesi].
  - Leaflet özel CRS: BULUNAMADI (arama sonucu yetersiz; leafletjs.com okunmadı).
  - MapLibre'da keyfi (Mercator dışı, globe dışı) özel projeksiyon: BULUNAMADI (bu oturumda doğrulanmadı).
- Canvas ile elle çizim: henüz araştırılmadı.

## 5. Eşdikdörtgen PNG maskesinin gerçek alana çevrilmesi
- [H] Maske bir eşdikdörtgen (plate carrée) ızgarada ise her piksel satırının alanı R²·Δλ·(sin φ2 − sin φ1). Maske alanı = piksellerin bu alanlarının toplamı (1. bölüm ile aynı formül).
- [D] pyproj: Geod(a=R,b=R) ile sferik poligon alanı; Geod(ellps='WGS84') ile elipsoid. Tüm maske kenarlarını enlem/boylam halkası olarak verip polygon_area_perimeter ile toplamak bir yöntemdir ([Ö] çıkarım; pyproj belgesi bunu tek poligon için tanımlar).
- GDAL / rasterio: BULUNAMADI. Bu oturumda "rasterio" ve "gdalinfo" kurulu değil; GDAL belgelerine erişim henüz denenmedi.
- Uyarı [Ö]: pyproj issue #1399 (dependabot mirror üzerinden) global poligonda geometry_area_perimeter'in 0 döndürdüğünü bildiriyor; tam küre maskesi için kontrol gerekli.

## Açık sorular / sonraki adımlar
1. Kullanıcı bölgenin gerçek koordinat kutusunu doğrulasın: "60K-7G, 44B-43D" kodları hangi koordinat sistemine ait (ör. MGRS/UTM hücresi ya da başka bir ızgara)? Çözülemedi; hesap varsayılan 10–77°K bandıyla yapıldı. Bu kodlar gerçek enlem/boylam sınırına çevrilirse sonuçlar yeniden hesaplanır.
2. Snyder PP 1395 PDF'i (pubs.usgs.gov/pp/1395 benzeri) curl ile indirilip Tissot bölümü ve konik seçim önerisi [B] doğrulanacak.
3. Leaflet CRS, MapLibre projection, deck.gl globe belgeleri ve GDAL/pyproj raster alan yöntemi birincil kaynaktan okunacak.
4. Vincenty doğruluğu (Wikipedia sayfası + Vincenty orijinal kaynağı) doğrulanacak.
