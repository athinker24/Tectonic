# C. Küre üzerinde levha hareketi: sayısal gösterim

Durum: araştırma tamamlandı (kısıtlı erişim notları en sonda).
Etiketler: [B] birincil kaynak okundu, [D] resmi belgelendirme, [Ö] özet/ikincil kaynak, [H] hesap veya çıkarım (bu notun yazarı). "BULUNAMADI" = kaynakta bulunamadı.

## 1. Euler kutbu, dönme matrisi, kuaterniyon ve üç boyutlu dönme

- Euler kutbu: dönme vektörünün (küre merkezinden radyal) yüzeyi kestiği nokta. Açı radyan; pozitif açı, dönme vektörü etrafında saat yönünün tersi. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.FiniteRotation.html
- Kutup (lat, lon) ve açı tanımı, birim vektör (x,y,z) biçimi de kabul edilir. [B] aynı sayfa
- Kuaterniyon: birim kuaterniyon q = (w, r), w = cos(θ/2), r = sin(θ/2)·u (u birim eksen). Kuaterniyondan 3×3 dönme matrisi için standart bir dönüşüm vardır. [Ö] https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation (okundu; "Quaternion-derived rotation matrix" bölümü; w, r gösterimi bu sayfada geçer). Açı/eksen biçiminin sayısal formu [H] standart tanım.
- Eksen-açı ile kuaterniyon, kütüphaneler arasında bileşen sırası bakımından farklılık gösterebilir. [Ö] https://docs.ros.org/en/kinetic/api/geometric_tools_engine/html/GteRotation_8h_source.html (arama özeti, doğrudan okunmadı)
- Rodrigues formülü (eksen birim vektörü k, açı θ, vektör v): v_dön = v cosθ + (k × v) sinθ + k (k·v)(1 − cosθ). [H] standart form; [Ö] https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula (okundu: eksene paralel/dik ayrışım ve çapraz çarpım matrisi bu formülün yapısını doğrular; formülün tam satırı çekilmedi).
- Kompozisyon (iki dönme): pygplates'te `r1 * r2` veya `pygplates.FiniteRotation.compose(r1, r2)`. Değişmeli değildir (A×B ≠ B×A). [B] https://www.gplates.org/docs/pygplates/generated/pygplates.FiniteRotation.html
- Ters dönme: `fr.get_inverse()`; `orijinal = fr.get_inverse() * döndürülmüş`. [B] aynı sayfa
- Bir poligonu (kıta bloğu) döndürmek: `fr * polygon`. Dönme rijit olduğu için köşe sayısı ve poligonun alanı değişmez. [B] (işlem desteği, aynı sayfa) + [H] (alan korunumu çıkarımı)
- Küresel poligon alanı: `PolygonOnSphere.get_area()` birim küre için steradyan döndürür; km² için R² ile çarpılır. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.PolygonOnSphere.html
- Dünya yarıçapı: `pygplates.Earth.mean_radius_in_kms` = 6371.009 km. [B] GPlately belgesindeki imza örneği: https://gplates.github.io/gplately/latest/sphinx/html/generated/gplately.PlateReconstruction.html
- s2 (R paketi) küresel alan ve işlemler: `s2_area(x, radius = s2_earth_radius_meters())`; `s2_intersection`, `s2_union`, `s2_difference`, `s2_sym_difference`. Yarıçap metre cinsinden verildiği için alan çıktısı m² olarak yorumlanır [H]. [D] https://cran.csiro.au/web/packages/s2/refman/s2.html

## 2. pyGPlates ve GPlately API

- `pygplates.FiniteRotation(pole, angle_radians)`; `get_euler_pole_and_angle()` (açı radyan); `get_lat_lon_euler_pole_and_angle_degrees()` (hepsi derece). [B] FiniteRotation sayfası
- Geometri döndürme: `fr * point`, `fr * polyline`, `fr * polygon`, `fr * multi_point`, `fr * great_circle_arc`, `fr * vector`. [B] aynı sayfa
- Küçük daire yayı: `fr.get_rotation_distance(point)` (birim küre, radyan; Dünya yüzeyi için R ile çarp). Aynı nokta veya karşı noktalar için dönme ekseni keyfi seçilir. [B] aynı sayfa
- Kimlik dönme: `FiniteRotation.create_identity_rotation()`; `represents_identity_rotation()` testi. [B] aynı sayfa
- Büyük daire dönmesi: `FiniteRotation.create_great_circle_point_rotation(from, to)` (sürüm 0.29 ve sonrası). [B] aynı sayfa
- Hız: `pygplates.calculate_velocities(domain_points, finite_rotation, time_interval_in_my[, velocity_units=pygplates.VelocityUnits.kms_per_my | cms_per_yr][, earth_radius_in_kms=pygplates.Earth.mean_radius_in_kms])`; dönüş: Vector3D listesi. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.calculate_velocities.html
- Resmi örnek: `eq = rotation_model.get_rotation(10, plaka_id, 11)`; `noktalar = geom.get_reconstructed_geometry().get_points()`; `pygplates.calculate_velocities(noktalar, eq, 1, pygplates.VelocityUnits.cms_per_yr)`. [B] aynı sayfa
- Hız vektörünü yerel büyüklük/azimut/eğim koordinatına çevirme: `pygplates.LocalCartesian.convert_from_geocentric_to_magnitude_azimuth_inclination()`. [B] aynı sayfa
- `ReconstructSnapshot.get_point_velocities(points[, velocity_delta_time=1.0][, velocity_delta_time_type=...][, velocity_units=pygplates.VelocityUnits.kms_per_my][, earth_radius_in_kms=...][, return_point_locations=False])`; hız, noktayı içeren statik poligonun dönmesinden hesaplanır; varsayılan km/My. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.ReconstructSnapshot.html
- `pygplates.RotationModel.get_rotation()`: toplam/aşamalı (total/stage) ve eşdeğer/bağıl (equivalent/relative) dönmeler; varsayılan anchor plate ID ayarlanabilir. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.RotationModel.html
- Topoloji (dinamik poligon): `pygplates.TopologicalModel(topoloji_dosyası, rotasyon_dosyası)`; `topological_snapshot(time)`; `get_resolved_topological_sections()`; `get_shared_sub_segments()`; `get_sharing_resolved_topologies()`. Eski API: `pygplates.resolve_topologies`. [B] örnek kod: https://www.gplates.org/docs/pygplates/sample-code/pygplates_detect_topology_gaps_and_overlaps.html ; API sayfası arama özetiyle doğrulandı: https://www.gplates.org/docs/pygplates/generated/pygplates.resolve_topologies.html [Ö]
- GPlately `PlateReconstruction.get_point_velocities(lons, lats, time[, delta_time=1.0, ...])`: kuzey ve doğu bileşenleri, varsayılan km/My. [B] https://gplates.github.io/gplately/latest/sphinx/html/generated/gplately.PlateReconstruction.html ; birim notu ve `velocity_units=pygplates.VelocityUnits.cms_per_yr` önerisi GPlately öğreticisinin arama özetinden [Ö] (`Points.plate_velocity()` varsayılanı cm/yıl).
- GPlately `PlateReconstruction.topological_snapshot(time, ...)` ve sonrasında `calculate_plate_boundary_statistics()`. [B] aynı sayfa (metot adları görüldü; parametre ayrıntısı tam okunmadı)
- GPlately `PlotTopologies.plot_plate_motion_vectors`: hız alanını düzgün enlem-boylam ızgarasında hesaplamak için `PlateReconstruction.get_point_velocities` kullanıyor. [Ö] https://gplates.github.io/gplately/dev-doc/04-VelocityBasics.html (arama özeti; sayfa doğrudan okunamadı; PlotTopologies ayrı API sayfası BULUNAMADI)
- GPlately öğreticisinde iki yöntem ayrılıyor: topoloji tabanlı (plaka ID'si zamana göre dinamik) ve statik poligon tabanlı `Points` (plaka ID'si sabit). [Ö] aynı öğretici özeti
- "PlateTectonicReconstruction" ve "FiniteRotation.get_velocities" adları: BULUNAMADI. Hız için resmi yol `pygplates.calculate_velocities` ve `ReconstructSnapshot.get_point_velocities`.

## 3. Bloğun toplam dönüşten hız hesabı (ω × r, cm/yıl)

- Vektör formu: v = ω × r (ω: Euler kutbu yönünde dönme vektörü, r: konum vektörü). [Ö] arama özetleri (PSU ders slaytları doğrudan açılamadı; bkz. kısıtlar)
- Büyüklük: v = Ω · R · sin δ. Ω açısal hız (radyan/yıl), R Dünya yarıçapı (6371 km), δ Euler kutbuna açısal uzaklık. [B] Carleton "Relative plate motion" ders kaynağı: "v = Ωr = Ω R sin δ"; Ω "º/Myr" olarak verilir, radyan/yıla çevrilmesi istenir; R = 6371 km. https://cdn.serc.carleton.edu/files/margins/mini_lesson_authors/reporting/relative_plate_motion_gulf_1385090255.v2.pdf
- Birim dönüşümü: Ω[°/My] × (π/180) × 10⁻⁶ = rad/yıl. [H]
- Sayısal örnek: 1 °/My için, 1.7453×10⁻⁸ rad/yıl × 6.371×10⁸ cm ≈ 11.1 cm/yıl; hız = 11.1 cm/yıl × sin δ. [H]
- Euler kutbundan uzaklıkla değişim: δ = 0 (kutup) hız sıfır; δ = 90° hız en büyük. Hız, kutba uzaklığın sinüsüyle orantılı artar. [B] (sin δ, Carleton) + [H] (sıfır/maks yorumu)
- Bir kıta bloğu katı cisim gibi döndüğünde köşeleri farklı δ'ye sahiptir; her köşenin hızı ayrı hesaplanır. [H]
- pyGPlates ile hesap: `eq = rotation_model.get_rotation(to_time, plaka_id, from_time)`; `pygplates.calculate_velocities(noktalar, eq, 1, pygplates.VelocityUnits.cms_per_yr)`. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.calculate_velocities.html
- Statik poligon yolu: `ReconstructSnapshot.get_point_velocities` (km/My varsayılan; cm/yıl için `velocity_units` verilmeli). [B] ReconstructSnapshot sayfası

## 4. Kuyruk durumu: küçük daire, büyük daire, dönüşüm fayları

Not: "kuyruk durumu" ifadesi kullanıcı tanımında belirsiz. Burada iki anlam ele alındı: (a) dönüşüm faylarının geometrisi (küçük/büyük daire), (b) Euler kutbuna yakın, hızın sıfıra yaklaştığı ve dönme ekseninin kararsız olduğu "kutup kuyruğu" durumu. Farklı bir anlam kastediliyorsa bu bölüm yeniden yazılmalı.

- Dönüşüm fayları Euler kutbu etrafında küçük daireler boyunca uzanır; hareket yönü sabittir. [Ö] Wikipedia "Leaky transform fault": "These new transforms will follow small circles centred on the new Euler Pole" (okundu) https://en.wikipedia.org/wiki/Leaky_transform_fault ; genel dönüşüm fayı sayfası: https://en.wikipedia.org/wiki/Transform_fault (okundu, bu cümle doğrudan bulunmadı)
- Küçük daireye dik çizgiler kutba geçer. [Ö] Open University "content section 4.3" (arama özeti). Sayfa doğrudan açılamadı (Cloudflare doğrulaması): https://www.open.edu/openlearn/science-maths-technology/geology/plate-tectonics/content-section-4.3
- Sırt segmentleri büyük daireye paraleldir (ideal durum). [Ö] Penn State ders slaytı (arama özeti): https://courseware.e-education.psu.edu/courses/earth540/540PlateTectonics.pdf ; PSU sayfası doğrudan açılamadı (HTML yönlendirme).
- Kutup-yakın kuyruk: hız sıfıra yaklaşır, Euler kutbu yaklaşık olarak sabit bir eksen tanımlar ama δ → 0 iken dönme yönü/ekseni hassasiyeti artar. [H] Bu, `FiniteRotation(from, to)` notundaki "aynı veya karşı noktada eksen keyfi" kuralıyla tutarlıdır. [B] https://www.gplates.org/docs/pygplates/generated/pygplates.FiniteRotation.html
- pyGPlates karşılıkları:
  - Küçük daire yayı uzunluğu (radyan): `fr.get_rotation_distance(point)`. [B]
  - Büyük daire yayı: `fr * great_circle_arc`; iki nokta için dönme: `FiniteRotation.create_great_circle_point_rotation(from, to)`. [B]
  - Yay uzunluğu: `PolygonOnSphere.get_arc_length()`. [B] PolygonOnSphere sayfası (PolylineOnSphere için aynı metot sayfada doğrulanmadı [H])

## 5. Örtüşme/boşluk denetimi, küresel Boolean işlemler, GPlately topoloji

### 5a. pyGPlates ile topoloji boşluk/örtüşme denetimi (resmi yöntem)

- Resmi örnek: "Find gaps and overlaps in global topological boundaries". [B] https://www.gplates.org/docs/pygplates/sample-code/pygplates_detect_topology_gaps_and_overlaps.html
  - Model: `topological_model = pygplates.TopologicalModel('topologies.gpml', 'rotations.rot')` (model zamandan bağımsız kurulur).
  - Her zaman adımında: `topological_snapshot(t)`; `get_resolved_topological_sections()`; her sınır bölümünün `get_shared_sub_segments()` alt-segmentleri için `len(get_sharing_resolved_topologies()) != 2` ise anomali.
  - Kural: küresel kapsama boşluksuz ve örtüşmesiz ise her alt-segment tam iki çözümlenmiş sınır tarafından paylaşılır. Bu, "iki komşu" ilkesidir. [B]
  - Boşluk: hiçbir topolojinin kapsamadığı alan. Örtüşme: iki topolojinin poligonlarının çakıştığı alan. [B]
  - Örnek aralık: 0–140 Ma, 1 My adımı; çıktı .gpml dosyası GPlates'te görüntülenir. [B]

### 5b. Küresel alan ve Boolean işlemler (Python/R)

- Planar sınır: Shapely ve GeoPandas enlem-boylam koordinatlarını düz düzlemde işler; kutuplara yakın alanlarda büyük çarpıtma olur. [Ö] https://pycon.de/archive/2025/talks/the-earth-is-no-longer-flat-introducing-support-for-spherical-geometries-in-spherely-and-geopandas/ (arama özeti)
- Antimeridyen ve kutuplar: düzlemsel gösterim kutbu çevreleyen veya antimeridyeni kesen geometrilerde zorlanır; `antimeridian` paketi bunun için düzeltme yapar, ama bazı geometrilerde düzeltme başarısız olabilir. [Ö] https://antimeridian.readthedocs.io/en/latest/failure-modes.html (arama özeti)
- Kenarlar: düzlemsel enlem-boylam kenarları büyük daire değildir; alan ve uzunluk naif hesapla yanlış olur. [Ö] (arama özeti, Elasticsearch ve sf/S2 vinyeti)
- Projeksiyon yolu (Shapely/GeoPandas): `gdf.to_crs("ESRI:54034")` veya `EPSG:3035` (Avrupa LAEA); alan = `gdf.area / 1e6` km² (CRS birimleri metre olmalı). Enlem-boylam CRS üzerinde `.area` anlamsızdır. [Ö] (GeoPandas öğreticileri, arama özeti)
- spherely: Shapely 2.0+ muadili, küresel geometri; s2geometry üzerine kurulu, s2geography ile GEOS uyumlu katman. "Erken aşama" olarak belirtilmiş. Kesişim ve alan fonksiyon adları BULUNAMADI. [D] https://spherely.readthedocs.io/en/latest/ (dokümantasyon sayfası kısa)
- s2 (R): `s2_intersection(x, y)`, `s2_union(x, y)`, `s2_difference(x, y)`, `s2_sym_difference(x, y)`, `s2_area(x, radius)`, `s2_is_valid`. [D] https://cran.csiro.au/web/packages/s2/refman/s2.html
- S2 (C++/Python): resmi kaynak, Python'a SWIG ile kısmi port olduğunu ve polyline, polygon, disc, rectangle, S2Cell covering destekler diyor. `S2BooleanOperation` C++ tarafında tanımlı; Python portunda açığa çıkıp çıkmadığı BULUNAMADI. [Ö] https://s2geometry.io/about/overview.html
- s2sphere (Python): küresel polygon Boolean işlemleri desteği BULUNAMADI.

### 5c. GPlately topoloji ve sürekli kapalı levha poligonları (Gurnis 2012)

- Gurnis vd. (2012), "Plate tectonic reconstructions with continuously closing plates", Computers & Geosciences 38(1), 35–42, doi:10.1016/j.cageo.2011.04.014. [Ö] https://www.earthbyte.org/category/reconstructions/gurnis-et-al-2012 (arama sayfası özeti)
  - Not: görev notunda dergi "G-cubed" yazıyordu; kaynakta dergi Computers & Geosciences olarak doğrulandı.
  - Yöntem özeti: her plaka poligonu, kenarları bağımsız hareket ederken geometrik olarak kapalı kalır ("continuously closed plate", CCP). Algoritma GPlates'e eklenmiştir. Model 140 My'lık bir yeniden inşaya uygulanmıştır. [Ö] aynı özet
  - Tam metin (PDF) erişilemedi: https://www.earthbyte.org/Resources/Pdf/Gurnis_cont_closing_plates_CompGeosci2012.pdf (404). Denklem ve eşikler BULUNAMADI.
- GPlately `topological_snapshot` ve `calculate_plate_boundary_statistics()` ile sınır istatistikleri alınır. [B] GPlately PlateReconstruction sayfası (metot adları)
- Boşluk/örtüşme kontrolünün resmi uygulaması, pyGPlates'in `TopologicalModel` akışıdır (5a). GPlately üzerinden aynı kontrolün nasıl yapıldığı BULUNAMADI.

## Erişim kısıtları ve bulunamayanlar

- www.gplates.org: WebFetch DNS hatası verdi; curl ile erişildi (yerel kopyalar raw08 altında). Notlardaki gplates.org kaynakları curl ile okundu.
- gplately.readthedocs.io: 404.
- gplates.github.io/gplately (sphinx/generated/PlateReconstruction) okundu; öğretici sayfası (04-VelocityBasics) curl ile 210 bayt yanıt verdi, bu yüzden arama özetine dayanıyor.
- courseware.e-education.psu.edu (PSU ders notu): HTML yönlendirme sayfası döndü; PDF içeriği alınamadı.
- open.edu (Open University): Cloudflare doğrulaması; içerik alınamadı.
- arXiv physics/0501126 PDF: metin bozuk çıktı (font kodlaması); kullanılmadı.
- earthbyte Gurnis PDF: 404.
- BULUNAMADI: "PlateTectonicReconstruction" ve "FiniteRotation.get_velocities" resmi API adları; GPlately PlotTopologies ayrı API sayfası; spherely Boolean/alan fonksiyon adları; s2sphere Boolean desteği; Gurnis 2012 tam matematiği.

## Kaynak listesi

Birincil / resmi:
- [B][D] https://www.gplates.org/docs/pygplates/generated/pygplates.FiniteRotation.html
- [B] https://www.gplates.org/docs/pygplates/generated/pygplates.calculate_velocities.html
- [B] https://www.gplates.org/docs/pygplates/generated/pygplates.ReconstructSnapshot.html
- [B] https://www.gplates.org/docs/pygplates/generated/pygplates.PolygonOnSphere.html
- [B] https://www.gplates.org/docs/pygplates/generated/pygplates.RotationModel.html
- [B] https://www.gplates.org/docs/pygplates/sample-code/pygplates_detect_topology_gaps_and_overlaps.html
- [B] https://gplates.github.io/gplately/latest/sphinx/html/generated/gplately.PlateReconstruction.html
- [B] https://cdn.serc.carleton.edu/files/margins/mini_lesson_authors/reporting/relative_plate_motion_gulf_1385090255.v2.pdf (v = Ω R sin δ)
- [D] https://cran.csiro.au/web/packages/s2/refman/s2.html
- [D] https://spherely.readthedocs.io/en/latest/

Özet / ikincil:
- [Ö] https://www.gplates.org/docs/pygplates/generated/pygplates.resolve_topologies.html (arama özeti)
- [Ö] https://gplates.github.io/gplately/dev-doc/04-VelocityBasics.html (arama özeti)
- [Ö] https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation (okundu)
- [Ö] https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula (okundu)
- [Ö] https://en.wikipedia.org/wiki/Leaky_transform_fault (okundu)
- [Ö] https://en.wikipedia.org/wiki/Transform_fault (okundu)
- [Ö] https://docs.ros.org/en/kinetic/api/geometric_tools_engine/html/GteRotation_8h_source.html (arama özeti)
- [Ö] https://www.earthbyte.org/category/reconstructions/gurnis-et-al-2012 (arama özeti)
- [Ö] https://s2geometry.io/about/overview.html (arama özeti)
- [Ö] https://pycon.de/archive/2025/talks/the-earth-is-no-longer-flat-introducing-support-for-spherical-geometries-in-spherely-and-geopandas/ (arama özeti)
- [Ö] https://antimeridian.readthedocs.io/en/latest/failure-modes.html (arama özeti)
- [Ö] https://www.open.edu/openlearn/science-maths-technology/geology/plate-tectonics/content-section-4.3 (arama özeti; sayfa açılamadı)
- [Ö] https://courseware.e-education.psu.edu/courses/earth540/540PlateTectonics.pdf (arama özeti; sayfa açılamadı)
