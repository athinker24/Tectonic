# 13. Erozyon motorunun seçimi

Araştırma tarihi: 12 Kasım 2026. Belge üç Haiku kolunun (A Fastscapelib, B kıyı koşulu ve motor karşılaştırması, C parametre aralıkları ve sediment) ve benim yaptığım tek bir ölçümün sentezidir; sentezi ben yazdım. Ham notlar `arastirma/notlar/13/` içinde. Etiketler: **[B]** tam metin okundu, **[D]** resmi belgelendirme ya da paket meta verisi okundu, **[Ö]** arama özeti, doğrulanamadı, **[Ö-ölç]** bu oturumda kendi ölçümüm, **[H]** çıkarım, **[Y]** bulunamadı.

## Kısa sonuç

**1. Ana aday Fastscapelib, ama tek başına yetmiyor.** Sürüm 0.3.0 (25 Haziran 2025), GPL-3.0, `pip install fastscapelib`. HEALPix, raster ve profil ızgaraları var; HEALPix'te düğüm alanı 4πR²/N (eşit alan), varsayılan yarıçap Dünya yarıçapı, looped sınırı reddediliyor [D]. SPL eroder örtük, n ≠ 1 için Newton-Raphson, çok akış yalnızca n = 1'de [D]. **Çökelme modeli yok** (C++ kitaplığında; doğrulandı). Çökelme `fastscape` 0.1.0 paketinde (Fortran sarmalayıcısı), HEALPix ile birlikte kullanımı belgelenmedi [D ve Y].

**2. Ölçüm: Fastscapelib 4 çekirdekli, 15 GB makinede 1 milyon düğümde adım başına yaklaşık 0,7 s.** Tek akış yönlendirici, MST çukur çözücü, SPL (n = 1) ve ADI difüzyon, rastgele başlangıç yüzeyi. 4,2 milyon düğümde adım başına yaklaşık 3,1 s ve en yüksek bellek yaklaşık 1,5 GB [Ö-ölç]. Bu, GitHub Actions'ın 4 vCPU ve 16 GB standart çalıştırıcısı (public depo) için kabaca bir üst sınır tahminidir; Actions'ta çalıştırılmadı, CPU farklı olabilir.

**3. goSPL Actions'a sığmıyor, Landlab küresel ağ için kısıtlı.** goSPL belgelenmiş 10 km küresel ağı en az 16 MPI rank ile çalıştırıyor (12. belge). Landlab'ın `IcosphereGlobalGrid` sınıfı var ama depresyon bulucu yalnızca D8 / en dik iniş ile çalışıyor, çok akışla çalışmıyor (8. belge). 

**4. Kıyıyı sabit tutan hazır bir mekanizma bulunmadı.** Landlab, Fastscapelib ve Yuan (2019) kıyıyı sabit kotlu "açık sınır" düğümleriyle çözüyor; kıyıda yapay basamak oluşmasını önleyen yayımlanmış bir yöntem bulunamadı.

## 1. Motorların karşılaştırması

| Motor | Dil | Izgara | Sediment | Lisans | Güncel sürüm | Etiket |
|---|---|---|---|---|---|---|
| Fastscapelib | C++ ve Python | profil, raster, HEALPix (üçgen ağ başlığı çekilemedi) | C++ kitaplığında yok; `fastscape` paketinde Fortran üzerinden var | GPL-3.0 | 0.3.0, 2025-06-25 | [D] |
| Landlab | Python | raster, hex, Voronoi-Delaunay, ikosahedral küresel (`IcosphereGlobalGrid`) | SPACE (çökelme var) | MIT | 2.11.0, 2026-04-06 | [D] |
| goSPL | Python, PETSc, MPI | düzensiz üçgen / küresel ağ | var (deniz tabanı difüzyonu ve çökelme) | GPL-3.0 | 2026.7.14 | [D] |
| Badlands | Python ve Fortran | TIN, bölgesel | var | lisans kaynaklarda çelişkili (LGPL v3 bir kaynakta) | 2.3.1, 2026-05-01 | [D] |
| Pecube | Fortran | sonlu eleman | termokronoloji odaklı | GPL-3.0 | tarih yok | [D] |
| TTLEM | MATLAB | raster | | | V1.0b, 2025-03-18 | [D] |
| CHILD | | | | GPL v2 | yalnız bakım, 2020 | [D] |

Paralellik Landlab, Fastscapelib, Badlands ve Pecube için bulunamadı [Y]; Fastscapelib'de çok iş parçacıklı yolun yalnızca `single_flow_router` için doğrulandı [D].

**Fastscapelib API'sine ilişkin düzeltmeler.** `fill_sinks` ve `mst_sinks` adları kaynakta yok; doğru adlar `pflood_sink_resolver` ve `mst_sink_resolver` (varsayılan Kruskal + carve). `xsimlab-fastscape` PyPI'da yok; en yakın paket `fastscape` 0.1.0 (BSD-3-Clause, conda-forge'da var). Düğüm durumları: core, fixed_value, fixed_gradient, looped, ghost. `multi_flow_router(slope_exp)` varsayılanı C++'ta 1,0, Python `fastscape` sarmalayıcısında 0; fark doğrulanmalı [D]. `diffusion_adi_eroder` sınır durumunu yok sayıp raster kenarlarını sabit kabul ediyor [D]; kıyı için tutarsızlık riski.

## 2. Kıyının sabit tutulması

- **Landlab:** sabit kotlu sınır `BC_NODE_IS_FIXED_VALUE` ve tek çıkış düğümü; SPACE, StreamPowerEroder ve FastscapeEroder'da deniz seviyesi parametresi yok, `sea_level__elevation` yalnızca CarbonateProducer'da [B].
- **Badlands:** `sealevel = sea0 + seaFunc(time)`, dalga ve kıyı taşınımı modülü var [B].
- **goSPL:** `sealevel = seafunction(tNow)`, deniz tabanı difüzyonu (`_diffuseOcean`), deniz seviyesi altında çökelme [B].
- **Fastscapelib:** FIXED_VALUE düğümleri baz seviyesi [D].
- **Yuan ve diğerleri 2019** (JGR Earth Surface 124(6), doi 10.1029/2018JF004867): taban düğümleri açık sınır, tortu sistemden çıkıyor [B]. Gasparini, Forte ve Barnhart 2023 karşılaştırması (ESurf ön baskı): çevre düğümler açık sınır, yükseklik 0 m sabit [B].
- Kıyıda yapay basamak oluşmasının açıklaması (yükselen toprağın sabit kotlu sınıra çarpıp dik basamak üretmesi), kıyı eğim sınırlama, lagün ve kıyı ovası yaklaşımlarının hiçbiri bulunan kaynaklarda doğrulanmadı; açıklama benim çıkarımımdır [H]. Pelletier (2013) kıyı ovası makalesi bulunamadı [Y]. Cordonnier ve diğerleri "Sculpting Mountains" (IEEE TVCG 2018): tam metinde deniz seviyesi ya da kıyı sınırı yok [B].
- Düzeltmeler: Barnhart 2020 Landlab 2.0 makalesi GMD değil, Earth Surface Dynamics 8:379 ile 397 (doi 10.5194/esurf-8-379-2020); Yuan 2019 başlığı "FastScape-SPL" değil, "A New Efficient Method to Solve the Stream Power Law Model Taking Into Account Sediment Deposition"; "TTLEC" aslında TTLEM (Campforts, Schwanghart, Govers 2017, ESurf 5:47), MATLAB tabanlı.

**Aracın kıyı kuralı için çıkarım [H].** Kıyı maskesi pikselce sabit olduğundan kıyı hücreleri sabit kotlu baz düğümleri olacak; ama yükselen iç bölgenin kıyıya dik bir basamakla bitmemesi için yükselme haritası kıyıya doğru yumuşakça sıfıra gitmeli (ör. kıyıdan uzaklığa bağlı bir pencere). Bu bir tasarım önerisi; doğrulama 16. konuya ait.

## 3. Parametre aralıkları (C kolu)

| Parametre | Değer | Etiket |
|---|---|---|
| n (yalnızca advection) | yaklaşık 1,3 | Ruetenik ve diğerleri 2023, ESurf 11:865, küresel 10Be [B] |
| n (advection + difüzyon) | yaklaşık 2,3 (Q0.01: 1,59 ile 2,70) | aynı [B] |
| p (yalnızca difüzyon) | yaklaşık 2,0 | aynı [B] |
| D/K | yaklaşık 1,79e6 m^(0,9n+1) | aynı [B] |
| K aralığı | yaklaşık 1e−8 ile 1e−5 m^(1−2m)/yıl (n = 1 için) | aynı, yazarların karşılaştırdığı aralık [B] |
| D (tepe yamaç difüzyonu) | 4,4e−4 ile 3,6e−2 m²/yıl | Fernandes ve Dietrich 1997'den alıntı, aynı makale [B] |
| m/n (hesaplanmış) | çoğunlukla 0,4 ile 0,7 | Lague 2014, ESPL 39:38 [B] |
| Ourthe örneği | m = 0,75, düzeltilmiş m/n = 0,68 | aynı [B] |
| K ve yağış | E = K R^m A^m S^n, K = K_lp R^m, m = 1, n = 2,2 (Bhutan), K_lp = 2,2e−9 m^−2 | Adams ve diğerleri 2020, Sci. Adv. 6:eaaz3166 [B] |
| K ve yağış, küresel | MAP 1500 mm/yıl'ın üstünde pozitif korelasyon; yaklaşık 300 mm/yıl'da yerel tepe | Ruetenik ve diğerleri 2023 [B] |
| Deniz difüzyonu K_d | yaklaşık 300 ile 500 m²/yıl | Yuan ve diğerleri 2019 [Ö] |
| Kritik eğim | Egholm ve diğerleri 2013 (Nature 498) kritik eğim s_c kullanıyor; sayı ana metinde yok | [B] |

Doğrulanamayan: Stock ve Montgomery (1999) K aralığı "1e−7 ile 1e−2"; paper HTTP 403 verdi, atlatılmadı; araç bunu kaynaklı kullanmamalı. Egholm için 30° ile 40° kritik eğim değeri ana metinde yok. Gailleton 2019 ve Gailleton-Hergarten tartışması, Whipple 2009, Campforts 2017 (bulunan makale sayısal difüzyon konusunda), Roering ve Fernandes-Dietrich'in kalibre D/s_c değerleri bulunamadı [Y]. Davy ve Lague (2009) yalnızca özet düzeyinde (DOI 10.1029/2008JF001146); Shobe ve diğerleri 2017 (GMD 10:4577), Harel ve diğerleri 2016 (Geomorphology 268:184), Densmore, Ellis ve Anderson 1998 (JGR 103:15203), Roering ve diğerleri 1999 (WRR 35:853) arama özeti [Ö].

## 4. Hız ve kaynak ölçümü

**Ölçüm [Ö-ölç]** (4 çekirdek, 15 GB, Fastscapelib 0.3.0, Python, 10 km hücre, rastgele başlangıç yüzeyi, tek akış + MST çukur çözücü + SPL (K = 1e−5, m = 0,4, n = 1) + ADI difüzyon (0,01 m²/yıl), kıyı kenarları sabit, dt = 1e5 yıl, her adım yükselme + yönlendirme + alan birikimi + SPL + difüzyon):

| Düğüm sayısı | Adım başına süre |
|---|---|
| 65 536 (256²) | 0,028 s |
| 262 144 (512²) | 0,160 s |
| 1 048 576 (1024²) | 0,678 s |
| 4 194 304 (2048²) | 3,09 s; en yüksek bellek yaklaşık 1,5 GB |

Süre düğüm sayısıyla yaklaşık doğrusal. Bu örnekten çıkarım [H]: 1 milyon düğümde 5 000 adım (örneğin 50 milyon yıl, dt = 10 000 yıl) yaklaşık 56 dakika; 4,2 milyon düğümde aynı sayıda adım yaklaşık 4,3 saat. GitHub Actions iş başına en çok 6 saat izin veriyor, public depoda standart çalıştırıcı 4 vCPU ve 16 GB [Ö, docs doğrudan açılamadı]. Dolayısıyla Fastscapelib ile 1 milyon düğümlü simülasyon Actions'ta sığıyor; 4 milyon düğüm adım sayısına bağlı olarak sınırda. Gerçek bir yükselme haritası ve HEALPix için bu ölçüm yeniden yapılmalı; bu yalnızca raster ve D8 içindir.

Yayımlanmış kıyaslar: Barnhart 2020, Braun ve Willett 2013, Yuan 2019 tam metinlerinde çalışma süresi rakamı bulunamadı [B ve Y]; Landlab tek çekirdek hızı ve 1 ile 4 milyon düğüm süreleri bulunamadı [Y].

**Ek ölçek notu.** Kıta 87° × 67° bölgesidir (8. belge); 10 km hücreyle yaklaşık 970 × 745 = 0,72 milyon hücre, 5 km hücreyle yaklaşık 2,9 milyon hücre [H]; bu sayılar derece adımı sabit (eşdikdörtgen) ağ içindir, 60,9 milyon km²'lik bandın eşit alanlı ağda (ör. HEALPix) karşılığı 10 km'de yaklaşık 0,61 milyon, 5 km'de yaklaşık 2,44 milyon hücredir, ve kara bandın yalnızca bir kısmıdır (doğrulama notu, 12 Kasım 2026). Yani 5 ile 10 km çözünürlükte tüm kıta tek bir ağda bu ölçümün kapsamında kalıyor.

## 5. Aracın varsayılan değerleri ve öneri

| Konu | Öneri | Dayanak |
|---|---|---|
| Ana motor | Fastscapelib (raster ya da HEALPix), uyarlanmış sediment/çökelme katmanı ayrıca | [D ve H] |
| Çökelme | Fastscapelib'de yok; ya `fastscape` sediment modeli (Fortran) ya da basit çukur doldurma kuralı | [D] |
| Alternatif | Landlab SPACE (çökelmeli, Python, MIT) ama çok akış ve ikosahedral ağda depresyon bulucu kısıtı | [D ve Ö] |
| Küresel çözünürlük | tüm kıta tek ağda 5 ile 10 km | [H] |
| n | 1 (çok akış için zorunlu) ya da 1,3 ile 2,3 aralığı | [D ve B] |
| m/n | 0,4 ile 0,7 | [B] |
| K | 1e−8 ile 1e−5 | [B] |
| D | 4,4e−4 ile 3,6e−2 m²/yıl | [B] |
| Zaman adımı | 1e4 ile 1e5 yıl (örtük çözücü için); yarıya indirip yakınsama testi | [H] |
| Kıyı | sabit kotlu düğüm; yükselme kıyıda yumuşakça sıfıra | [H] |
| Süre bütçesi | 1 milyon düğüm × 5 000 adım ≈ 1 saat (4 çekirdek) | [Ö-ölç] |

## 6. Kaynaklar arası çelişkiler

- Fastscapelib çok akış varsayılanı: C++ 1,0, Python sarmalayıcısı 0 (doğrulanmadı).
- Badlands lisansı: kaynaklar çelişkili (LGPL v3 bir README'de).
- Fastscapelib SPL "implicit" deniyor ama A'ya göre kararsız olabileceği belgede yazıyor.
- Ruetenik n değeri 1,3 (yalnızca advection) ile 2,3 (advection + difüzyon) farklı; Lague 2014'ün n = 1 varsayımıyla uyumsuz.

## 7. Bulunamayanlar ve doğrulanamayanlar

- Stock ve Montgomery 1999 (HTTP 403), Whipple ve Tucker 1999 (TLS), Harel 2016 PDF (HTML döndü), Davy ve Lague 2009 PDF (HAL landing), Pelletier 2013, Gailleton 2019, Whipple 2009; fastscapelib.readthedocs.io, landlab.readthedocs.io, gospl.readthedocs.io DNS hatası verdi.
- Fastscapelib trimesh başlığı, `fastscapelib` conda paketi, çok iş parçacıklı yolun yalnızca tek akış için olduğu dışındaki paralellik; Landlab, Badlands, Pecube paralellik.
- GitHub depoları oturumda erişilemedi; kaynaklar PyPI, raw.githubusercontent.com ve doğrudan dosya indirmeleri.
- Benim ölçümüm HEALPix, çok akış ve çökelmeyi kapsamıyor; yalnızca raster, tek akış, n = 1.

## 8. Promptumdaki hatalar (düzeltildi)

- `fill_sinks`, `mst_sinks` adları yanlış; `pflood_sink_resolver`, `mst_sink_resolver`.
- `xsimlab-fastscape` paketi yok; `fastscape` 0.1.0.
- "Barnhart 2020 Landlab 2.0 GMD" yanlış; ESurf 8:379.
- "Yuan 2019 FastScape-SPL" başlığı yanlış.
- "TTLEC" yanlış; TTLEM (Campforts 2017).
- "Egholm 2013 A mechanical model of landslide" başlığı yanlış; Egholm, Knudsen, Sandiford 2013, Nature 498; kritik eğim 30° ile 40° ana metinde yok.
- "Densmore 1998" yazar listesi: Densmore, Ellis ve Anderson 1998.
- "Stock-Montgomery K aralığı 1e−7 ile 1e−2" doğrulanamadı.
- "Adams 2020 Climate-adjusted K" başlığı yanlış; "Rainfall rates set the scaling of relief and river incision in tectonically active landscapes", Sci. Adv. 6:eaaz3166.
- "par.nsf.gov/.../10471890" Stock ve Montgomery değil, Anderson ve diğerleri 2023 (ESurf 11:995).

## Başlıca kaynaklar

- Fastscapelib 0.3.0: PyPI (https://pypi.org/project/fastscapelib/) ve ham notlardaki raw.githubusercontent bağlantıları
- Ruetenik ve diğerleri 2023: https://esurf.copernicus.org/articles/11/865/2023/
- Lague 2014 (ön baskı): https://orbi.uliege.be/bitstream/2268/190050/1/preprint.pdf
- Adams ve diğerleri 2020: PMC7567587
- Barnhart ve diğerleri 2020, ESurf 8:379: https://doi.org/10.5194/esurf-8-379-2020
- Yuan ve diğerleri 2019: https://doi.org/10.1029/2018JF004867
- Egholm ve diğerleri 2013: https://doi.org/10.1038/nature12218
- Ölçüm betiği: scratchpad `bench_fs.py` (oturum sonrası silinir; kopyası `arastirma/notlar/13/bench_fs.py` olarak repoya eklendi)
- Tam liste ve her bilginin kaynağı `arastirma/notlar/13/` içinde.
