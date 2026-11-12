# C. Küre üzerinde levha hareketi: sayısal gösterim (taslak)

Durum: araştırma devam ediyor. Bu dosya bulgu geldikçe güncellenir.
Etiketler: [B] birincil kaynak okundu, [D] resmi belgelendirme, [Ö] özet/ikincil. Bulunamayan konular "BULUNAMADI" ile işaretlenir.

## 1. Euler kutbu, dönme matrisi, kuaterniyon

_Henüz bulgu yok._

## 2. pyGPlates ve GPlately API

- `pygplates.FiniteRotation(pole, angle_radians)`: Euler kutbu (nokta, (lat,lon) derece veya (x,y,z)) ve açı RADYAN cinsinden. Pozitif açı, dönme vektörü etrafında saat yönünün tersi (anti-clockwise). [B] https://www.gplates.org/docs/pygplates/generated/pygplates.FiniteRotation.html (yerel metin: raw08/3aa5260145.txt)
- Kutup ve açı: `get_euler_pole_and_angle()` (açı radyan) ve `get_lat_lon_euler_pole_and_angle_degrees()` (hepsi derece). [B] aynı sayfa
- Geometri döndürme: `fr * point`, `fr * polyline`, `fr * polygon`, `fr * multi_point`, `fr * great_circle_arc`, `fr * vector`. [B] aynı sayfa
- Kompozisyon: `r1 * r2` veya `pygplates.FiniteRotation.compose(r1, r2)`; değişmeli değildir (A×B ≠ B×A). [B] aynı sayfa
- Ters dönme: `fr.get_inverse()`; `orijinal = fr.get_inverse() * döndürülmüş`. [B] aynı sayfa
- Dönme mesafesi (küçük daire yayı, birim küre üzerinde radyan): `fr.get_rotation_distance(point)`; Dünya yüzeyinde mesafe için Earth yarıçapıyla çarpılır. [B] aynı sayfa
- Kimlik dönme: `FiniteRotation.create_identity_rotation()`; ya da herhangi bir kutup ve açı=0. `represents_identity_rotation()` testi var. [B] aynı sayfa
- İki nokta arasındaki dönme: `FiniteRotation(from_point, to_point)`; aynı veya karşı noktalarda rastgele eksen seçilir. `create_great_circle_point_rotation` sürümü 0.29'dan beri. [B] aynı sayfa
- Hız hesabı: `pygplates.calculate_velocities(domain_points, finite_rotation, time_interval_in_my[, velocity_units=pygplates.VelocityUnits.kms_per_my | cms_per_yr][, earth_radius_in_kms=pygplates.Earth.mean_radius_in_kms])`; `time_interval_in_my` milyon yıl; dönüş: Vector3D listesi. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.calculate_velocities.html (raw08/c63f21f6b8.txt)
- Örnek kullanım (resmi): `eq = rotation_model.get_rotation(10, plaka_id, 11)`; `noktalar = geom.get_reconstructed_geometry().get_points()`; `pygplates.calculate_velocities(noktalar, eq, 1, pygplates.VelocityUnits.cms_per_yr)`; 1 My aralığında cm/yıl. [B] aynı sayfa
- Yerel koordinatlara çevirme: `pygplates.LocalCartesian.convert_from_geocentric_to_magnitude_azimuth_inclination()`. [B] aynı sayfa
- ReconstructSnapshot üzerinde `get_point_velocities(points[, velocity_delta_time=1.0])` [Ö] (arama özeti, sayfa raw08/5daada439b.txt'de doğrulanacak)
- Kaynak notu: "PlateTectonicReconstruction" ve "FiniteRotation.get_velocities" adları arama sonuçlarında BULUNAMADI; bu adlar resmi API olarak doğrulanamadı. Hız için resmi yol `pygplates.calculate_velocities` ve `ReconstructSnapshot`/`ReconstructModel` üzerinden.
- `pygplates.PolygonOnSphere`: `get_area()` (birim küre için steradyan; km² için R² ile çarp), `get_arc_length()`, `get_centroid()`, `is_point_in_polygon(point)`. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.PolygonOnSphere.html (raw08/6afaa1e2a7.txt). Uyarı: `get_area` yerine "p in polygon" yalnızca sınır üzerindeki çakışmayı kontrol eder; iç bölge testi için `is_point_in_polygon()` kullanılır (aynı sayfa).
- `pygplates.ReconstructSnapshot.get_point_velocities(points[, velocity_delta_time=1.0][, velocity_delta_time_type=pygplates.VelocityDeltaTimeType.t_plus_delta_t_to_t][, velocity_units=pygplates.VelocityUnits.kms_per_my][, earth_radius_in_kms=pygplates.Earth.mean_radius_in_kms][, sort_reconstructed_static_polygons=...][, return_point_locations=False])`; hızlar, noktayı içeren statik poligonun dönmesinden hesaplanır. Varsayılan birim km/My, cm/yıl değil. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.ReconstructSnapshot.html (raw08/5daada439b.txt)
- `pygplates.RotationModel`: `get_rotation()` ile toplam/aşamalı (total/stage) ve eşdeğer/bağıl (equivalent/relative) dönmeler; varsayılan anchor plate ID ayarlanabilir. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.RotationModel.html (raw08/f9c8a8bf5e.txt)
- Topoloji (dinamik poligon): `pygplates.TopologicalModel(topoloji_dosyası, rotasyon_dosyası)`; `topological_snapshot(time)`; `get_resolved_topological_sections()`; `get_shared_sub_segments()`; `get_sharing_resolved_topologies()`. Eski API `pygplates.resolve_topologies` (dosyaya veya listeye). [B] https://www.gplates.org/docs/pygplates/generated/pygplates.resolve_topologies.html (arama özeti; sayfa doğrudan çekilmedi), örnek kod aşağıda.
- GPlately `PlateReconstruction.get_point_velocities(lons, lats, time[, delta_time=1.0, ...])`: kuzey ve doğu bileşenleri, km/Myr. Varsayılan km/My; `Points.plate_velocity()` varsayılanı cm/yıl. Öğretici, birim farkından dolayı `velocity_units=pygplates.VelocityUnits.cms_per_yr` açıkça verilmesini öneriyor. [B] https://gplates.github.io/gplately/latest/sphinx/html/generated/gplately.PlateReconstruction.html (raw08/c64c61335c.txt). Metot `reconstruct(feature, to_time[, from_time, ...])` de listelenmiş.
- GPlately `PlotTopologies.plot_plate_motion_vectors`: hız vektör alanını düzgün enlem-boylam ızgarasında hesaplamak için `PlateReconstruction.get_point_velocities` kullanıyor [Ö] (arama özeti; https://gplates.github.io/gplately/dev-doc/04-VelocityBasics.html doğrudan çekilemedi, BULUNAMADI olarak kalan kısım: PlotTopologies ayrı API sayfası).
- Gözlem: GPlately öğreticisi iki yöntemi ayırıyor: topoloji tabanlı (plaka ID'si zamana göre dinamik) ve statik poligon tabanlı `Points` (plaka ID'si sabit). [Ö] aynı öğretici özeti.
- Yer yarıçapı: `pygplates.Earth.mean_radius_in_kms` (fonksiyon imzalarında varsayılan). Değer henüz doğrulanmadı (sonraki adım).

## 5. Örtüşme/boşluk denetimi (kısmi)

- Resmi pyGPlates örneği "Find gaps and overlaps in global topological boundaries": [B] https://www.gplates.org/docs/pygplates/sample-code/pygplates_detect_topology_gaps_and_overlaps.html (raw08/e946aceb3f.txt).
  - Yöntem: `topological_model = pygplates.TopologicalModel('topologies.gpml','rotations.rot')`; her zaman adımında `topological_snapshot(t)`; `get_resolved_topological_sections()`; her `get_shared_sub_segments()` için `len(get_sharing_resolved_topologies()) != 2` ise anomali.
  - Kural: küresel kapsama tam ve boşluksuz/örtüşmesiz ise her alt-segment tam iki çözümlenmiş sınır tarafından paylaşılır. Bu, iki-komşu ilkesidir.
  - Örnek zaman aralığı: 0–140 Ma, 1 My adımı.
  - Çıktı: anomali özelliklerini GPlates'te görüntülemek için .gpml dosyası.
- Gurnis vd. (2012), "Plate tectonic reconstructions with continuously closing plates", Computers & Geosciences 38(1), 35–42, doi:10.1016/j.cageo.2011.04.014. Not: görev notunda "G-cubed" yazıyordu; kaynak dergi Computers & Geosciences olarak doğrulandı. [B-özet] https://www.earthbyte.org/category/reconstructions/gurnis-et-al-2012 (arama sayfası özeti). Yöntem: her plaka poligonu, kenarları bağımsız hareket ederken geometrik olarak kapalı kalır ("continuously closed plate", CCP). Algoritma GPlates'e eklenmiş. Makalenin tam metni erişilemedi (earthbyte PDF 404) — tam metin BULUNAMADI.
- spherely (Shapely 2.0+ muadili, küresel geometri): "erken aşamada" geliştirme; s2geometry üzerine kurulu, s2geography aracılığıyla GEOS uyumlu katman. [D] https://spherely.readthedocs.io/en/latest/ . Kesişim ve alan API'si doğrulanmadı — BULUNAMADI.

## 3. Bloğun hız hesabı (ω × r)

_Henüz bulgu yok._

## 4. Kuyruk durumu: küçük daire, büyük daire, dönüşüm fayları

_Henüz bulgu yok._

## 5. Örtüşme/boşluk denetimi, küresel Boolean işlemler, GPlately topoloji (Gurnis 2012)

_Henüz bulgu yok._

## Kaynak listesi

_Henüz kaynak yok._
