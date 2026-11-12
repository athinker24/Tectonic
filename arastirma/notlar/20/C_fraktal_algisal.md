# C: Fraktal ve algısal arazi ölçütleri — araştırma notları

Durum: TAMAMLANDI (son güncelleme 2026-11-12)

Etiketler: [B] tam metin okundu / [B-öz] özet okundu (tam metin erişilemedi) / [Ö] arama özeti / ERİŞİLEMEDİ (ücretli/engelli, yalnız atıf doğrulandı) / BULUNAMADI

Yöntem notu: WebFetch yerine ağ proxy'si üzerinden curl + oku.py (trafilatura) ve pdftotext kullanıldı. Springer, AGU (Wiley), Elsevier tam metinleri proxy üzerinden alınamadı (doi.org yönlendirmesi 41 karakter döndürdü; link.springer.com DNS hatası). Bu nedenle o kaynaklardaki sayısal değerler ikincil kaynaklardan veya arama özetlerinden alındı ve etiketlendi. Bot korumasını aşmaya çalışılmadı.

## 1. Fraktal ve spektral arazi ölçütleri

**1.1 Mark & Aronson (1984)** — "Scale-dependent fractal dimensions of topographic surfaces: an empirical investigation, with applications in geomorphology and computer mapping", Mathematical Geology 16(7): 671-683, DOI 10.1007/BF01033029.
- Durum: ERİŞİLEMEDİ (tam metin yok; özet yok).
- [Ö] Atıf: https://www.scilit.net/publications/20d83bb46d5617151a41122e8ab0dd03
- [Ö] İkincil aktarım (inceleme): https://rjes.wdcb.ru/v19/2019ES000678/refsdir-678/Mark84.html — yöntem: DEM üzerinde varyogram; D'nin ölçekle keskin değiştiği, arazinin iç içe yapılardan oluştuğu yorumu.
- [Ö] Ölçek kırılması: çoğu karasal arazinin fraktal grafiğinde, karakteristik arazi uzunluklarına karşılık gelen eğim değişimleri görüldüğü aktarılıyor.
- D≈2.2 değeri: BULUNAMADI. Görevdeki bu değer doğrulanamadı; kaynak olarak kullanılmadan önce makalenin tam metninden teyit edilmeli.

**1.2 Perron, Kirchner & Dietrich (2008)** — "Spectral signatures of characteristic spatial scales and nonfractal structure in landscapes", JGR Earth Surface 113, F04003, DOI 10.1029/2007JF000866.
- Durum: ERİŞİLEMEDİ (doi.org ve Wiley 41 karakter; yalnız atıf).
- [Ö] Atıf doğrulandı: https://earthref.org/ERR/119557/
- [Ö] Aynı grubun ilgili çalışması: Perron, Dietrich & Kirchner (2008), "Controls on the spacing of first-order valleys", JGR 113, F04016, DOI 10.1029/2007JF000977.
- [Ö] Perron, Kirchner & Dietrich (2009), Nature 460: 468, "Formation of evenly spaced ridges and valleys": vadi aralığının karakteristik uzunluk ölçeği Lc ile orantılı olduğu öngörüsü, beş sahada test. https://www.nature.com/articles/460468a
- Güç spektrumu "nonfractal" ölçütünün sayısal tanımı: BULUNAMADI. Arama, özet/tam metin döndürmedi. (Arama sonucundaki "2008 Nature" bilgisi yanlıştır; Nature makalesi 2009'dur.)

**1.3 Gagnon, Lovejoy & Schertzer (2006)** — "Multifractal earth topography", Nonlinear Processes in Geophysics 13: 541-570, DOI (npg) https://npg.copernicus.org/articles/13/541/2006/
- Durum: [B-öz] (özet tam okundu).
- Dört DEM'den (gezegensel ölçekten 50 cm'ye, >2x10^8 piksel) topografi transektleri; güç spektrumu ve çoklu ölçekleme (multiscaling) araçları.
- Özet: fBm, fLm ve çoklu-fraktal FIF modelleri ayırt edici biçimde ele alınmış; "gerçekçi modellerin anizotropik tekillikler gerektirdiği" ve değişken istatistikli anizotropik tekilliklerin "ölçek kırılması" hakkında yanıltıcı sonuçlara yol açabileceği belirtilmiş.
- [Ö] Arama özeti: kompozit spektrum yaklaşık dört büyüklük mertebesinde ölçekleniyor, spektral üs ~2; evrensel parametreler α≈1.79, C1≈0.12; bathymetri/kıta/kıta kenarı için H değerleri 0.46/0.66/0.77 (bu değerler tam sayfada doğrulanmadı, [Ö]).
- Yorum: Ölçek kırılması sorusunda Gagnon 2006, tek bir kırılma yerine çoklu-ölçek ve anizotropi tartışmasını öne çıkarıyor.

**1.4 Huang & Turcotte (1989)** — "Fractal mapping of digitized images: Application to the topography of Arizona and comparisons with synthetic images", JGR 94(B6), DOI 10.1029/88JB03908.
- Durum: [Ö] (tam metin erişilemedi; EarthRef kaydı https://earthref.org/ERR/37880 ve arama özeti).
- [Ö] Arizona topografyası (7 nokta/km) için fraktal boyut ve pürüzlülük genliği haritaları; 1B veya 2B Fourier dönüşümünden sonra genliklerin dalga sayısının kuvvet yasasına uyduğu.
- [Ö] Bir kaynak, 1B fraktal boyutun 2B değerden 1 çıkarılarak elde edilmemesi gerektiğini tartışıyor.

**1.5 Gagnon ve diğ. ile Huang-Turcotte arasında ek bulgu**: Sayısal "D≈2.2" ile tutarlı bir spektral üs için bu makaleler dolaylı destek veriyor ancak kesin D değeri BULUNAMADI.

**1.6 Roering, Kirchner & Dietrich (1999)** — DÜZELTME: Görev metnindeki "Water Resources Research" başlığı doğru değil. WRR 1999 makalesi: "Evidence for nonlinear, diffusive sediment transport on hillslopes and implications for landscape morphology", WRR 35(3): 853-870, DOI 10.1029/1998WR900090.
- Durum: [Ö] (arama özeti; https://zendy.io/title/10.1029/1998wr900090 ve EarthRef https://earthref.org/ERR/43301). Tam metin erişilemedi (doi.org 41 karakter).
- [Ö] Doğrusal difüzyon yerine doğrusal olmayan difüzyon; beş küçük havza verisi; eğim arttıkça yamaç eğriliğinin sıfıra yaklaşması.
- [Ö] "Creep ve landsliding" başlığı ise Roering, Sklar, Kirchner & Dietrich (2001), Geology 29: 143-146, "Hillslope evolution by nonlinear creep and landsliding: An experimental study". Deneysel granüler yamaç.

**1.7 Burbank ve diğ. (1996) — ATIF DÜZELTMESİ**: Görevdeki "Burbank 1996 (JGR)" yanlış. Doğru: Burbank ve diğ. (1996), "Bedrock incision, rock uplift and threshold hillslopes in the northwestern Himalayas", **Nature 379: 505-510**, DOI 10.1038/379505a0. Bu makale bölüm 2'de incelenmiştir.

## 2. Yamaç eğimi dağılımı

**2.1 Burbank ve diğ. (1996) (Nature)** — [B-öz] Özet tam okundu (https://doi.org/10.1038/379505a0):
- Indus, kaya tabanını 2–12 mm/yıl hızla kesiyor.
- Çevre dağlardaki ortalama yamaç açıları dik ve "erozyon hızından esasen bağımsız"; ortak bir eşik süreci kontrolü öneriliyor.
- Kaya yükselmesi ve nehir kesimi arasında denge; heyelanlar yamaçların hızlı nehir kesimine verimli uyum sağlamasına izin veriyor.
- Eşik eğim "30–40°" değeri: ÖZETTE YOK; BULUNAMADI (tam metin paywall, şekiller okunamadı). Bu değer, kaynak doğrulanana kadar kullanılmamalı.

**2.2 Montgomery (2001)** — "Slope distributions, threshold hillslopes, and steady-state topography", American Journal of Science 301(4-5): 432-454, DOI 10.2475/ajs.301.4-5.432.
- Durum: [Ö] (ajsonline sayfası https://ajsonline.org/article/88259 yalnız künye/TOC döndürdü; özet bilgisi arama özetinden). Tam metin: ERİŞİLEMEDİ.
- [Ö] Olimpik Dağları ve Oregon Kıyı Sıradağları'nın DEM'leri, "steady-state" iki dağ kuşağı.
- [Ö] Drenaj alanı–eğim grafiklerinde belirgin saçılma; yoğunluk konturlarında hillslope→kanal geçişinde bir "attractor" (çekici).
- [Ö] 100 km² eğim histogramları: aktif yükselen alanlarda yaklaşık normal, birikim (depositional) topografyada üstel dağılım. Oregon'da çoğunlukla normal, düşük eğimli alanlarda sola çarpık.
- [Ö] Eğim dağılımları eşik kaya ve toprak örtülü yamaçların steady-state topografya ile ilişkisini yansıtıyor.
- Sayısal "ortanca eğim" ve "yüzde 90 eğim" ölçütleri: BULUNAMADI (özet düzeyinde tanımlanmamış).

**2.3 Eğim histogramı ortanca/%90 değerleri için genel**: BULUNAMADI (ayrı bir kaynak tanımı yok; yalnızca Montgomery'nin dağılım şekli tartışması var).

## 3. GEBCO ve Copernicus DEM teknik özellikleri

**3.1 GEBCO** — [B] https://www.gebco.net/data-products/gridded-bathymetry-data/ (sayfa okundu)
- Güncel sürüm: **GEBCO_2026 Grid** (görevde 2025 istenmişti; GEBCO_2025 hâlâ arşivde).
- Izgara: **15 yay-saniyesi** aralık; kara ve okyanusu kapsayan global arazi modeli; netCDF ve GeoTIFF (ayrıca Esri ASCII). Dosya boyutları ~4 GB (sıkıştırılmış).
- Ek ürünler: TID (Type Identifier) ızgarası; sub-ice ve ice-surface versiyonları (Grönland/Antarktika); çok çözünürlüklü test ürünü.
- Lisans: "The GEBCO Grid is placed in the public domain and may be used free of charge." (kamu malı). Atıf biçimi: "GEBCO Bathymetric Compilation Group 2026 ... doi:10.5285/4f68d5c7-45eb-f999-e063-7086abc036fa".
- Dikey datum notu: veriler ortalama deniz seviyesine atıfla birleştirilmiş; sığ sularda farklı datumlu veriler var.
- Dikey doğruluk (m): BULUNAMADI (sayfada sayısal dikey hata belirtilmemiş).

**3.2 Copernicus DEM (GLO-30 / GLO-90)** — [B] https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM
- Önemli: Copernicus DEM bir **DSM (yüzey modeli)**; binalar, altyapı ve bitki örtüsünü içerir (DTM değil).
- Çözünürlük: GLO-30 = 1.0 yay-saniyesi (~30 m); GLO-90 = 3.0 yay-saniyesi (~90 m). EEA-10 (Avrupa, 10 m) kısıtlı erişimli.
- Dikey doğruluk: mutlak < 4 m (90% doğrusal hata); göreli < 2 m (eğim ≤%20), < 4 m (eğim >%20) (1°x1° alanda, 90% nokta-nokta).
- Yatay mutlak doğruluk: < 6 m (90% dairesel hata).
- Lisans: GLO-30 ve GLO-90 dünya çapında **ücretsiz** lisans; ESA kullanıcı lisansı ve CCM erişim koşulları; kaynak bildirimi zorunlu ("COP-DEM" atfı; değiştirilmişse ayrı bildirim).
- Dağlık arazi ölçütü: sayfada yok.

**3.3 SRTM karşılaştırması** — [Ö] (ikincil):
- EMD bellek notu (https://help.emd.dk/mediawiki/images/a/ae/20210920_AccuracyCopernicusDEM.pdf): ~3.600 Avrupa rüzgar türbini sahası; Copernicus-30 RMSE 1.91 m, MAE 1.36 m; SRTM-30 RMSE 2.82 m, MAE 2.26 m. Dağlık-özel değil.
- Helmy ve diğ. (2025) (LiDAR ile üç morfolojik alan; SRTM 30, ALOS, Copernicus 30, FABDEM): Copernicus 30 ve FABDEM genel olarak daha iyi. Dağlık alt-sonuçları arama özetinde yok.
- Tehran ve Jam (ISPRS Annals 2023): Copernicus daha doğru (RMSE 5.72 ve 2.19 m iki alan). [Ö]
- Uyarı: bitki örtüsü/kanopi sıralamayı değiştirebilir; SRTM kanopiye daha az nüfuz eder ama dağlık bölgelerde sıralama değişebilir. [Ö]
- SRTM'nin 30 m dağlık-özel karşılaştırması: BULUNAMADI (kesin yayın doğrulanamadı).

## 4. Arazi sentezinde gerçekçilik değerlendirmesi

**4.1 PTRM — Rajasekaran, Kang, Čadík, Galin, Guérin, Peytavie, Slavík, Benes (2022), ACM TAP; arXiv 1909.04610** — [B] (tam metin https://ar5iv.labs.arxiv.org/html/1909.04610)
- Kullanıcı çalışması: Mechanical Turk, **2AFC** ("Which terrain looks more realistic (left or right)?"); E1: 70 katılımcı; E2: 128 katılımcı, 22.500 görüntü çifti görüntülemesi; yalnızca "Mechanical Turk Masters".
- Gerçek arazi (SRTM tabanlı, beş sınıf: aeolian, coastal, fluvial, glacial, slope) gerçekçilik oyu ~%77; prosedürel arazi ~%51 (örnek Fig. 1).
- Geomorfon özellikleri (10 sınıf: flat, peak, ridge, shoulder, spur, slope, pit, valley, footslope, hollow). Pearson korelasyonları (algı skoru ile): Valley 0.66, Ridge 0.64, Summit 0.44, Depression 0.42, Spur 0.33, Hollow 0.22, Flat -0.10, Footslope -0.15, Shoulder -0.17, Slope -0.65.
- **PTRM regresyonu** (denklem 2): açıklanan varyans %72, standart hata 0.13 (5 kat bölme, %80/%20 doğrulama). Katsayılar Depression 3.61, Summit 1.77, Flat 25.40, Valley 9.71, Ridge 7.65, Hollow 6.77, Spur 9.14, Shoulder 7.40, Slope 29.26 (bölen 69.22, sabit -38.44).
- Sentetik arazilerde depresyon, zirve, düzlük, vadi, sırt, çukur ve sırt uzantısı (spur) geomorfonları genelde eksik.
- Sınırlılıklar (yazarların kendi): geomorfonlar küçük alanlarla sınırlı; büyük ölçekli nehir/vadi dağılımını yansıtmıyor; ölçek bağımlılığı; kamera/aydınlatma sabit.
- Bu ölçüt, görevin "eğim-yükseklik histogram uyumu" ve "orometri" ölçütlerinden farklı olarak yerel geomorfon dağılımına dayanıyor.

**4.2 Argudo, Galin, Paris, Gain, Guérin (2019), "Orometry-based terrain analysis and synthesis", ACM TOG 38(6): 199 (SIGGRAPH Asia)** — [B] (PDF: https://people.cs.uct.ac.za/~jgain/wp-content/papercite-data/pdf/argudo2019.pdf, pdftotext)
- Orometrik tanımlayıcı: tepe ve eyerlerden (peaks & saddles) oluşan seyrek betimleyici; 50 bölge sınıflandırma (Random Forest). Doğruluk: R=50 km'de ortalama %75.3; alt-deney %86 ortalama doğruluk.
- Prominence (önem), dominance, isolation, relevance gibi orometrik istatistikler; prominence/yükseklik oranının algısal olarak daha önemli olduğu tartışılıyor.
- **Algısal çalışma (7.4)**: 6 terrain (T1 gerçek SRTM Alp DEM 1 arcsec; T2/T3 yöntem; T4 Cordonnier 2016 erozyon; T5 Perlin+gradyan; T6 ridged fBm). Tüm arazi 90x90 km, 30 m. Aerial perspektif görüntüleme. Sonuç: gerçek ile sentetik arasında hâlâ "algısal fark" var (Fig. 22). Sayısal yüzdeler metinden tam çıkarılamadı.
- Yazarlar, eğrilik/yerel profil (ridge & valley profilleri) ve ağaç topolojisinin hâlâ eksik olduğunu belirtiyor.

**4.3 Perche ve diğ. (2023), "Authoring Terrains with Spatialised Style", Computer Graphics Forum (Pacific Graphics 2023)** — [B] (PDF: https://www.cs.purdue.edu/homes/bbenes/papers/Perche23CGF.pdf, pdftotext)
- Yöntem: StyleGAN2 tabanlı; 1024x1024 kare yamalar (IGN RGE ALTI 5 km, 5 m çözünürlük; SRTM 30 m, 344 DEM'den 3.096 yama).
- Nicel değerlendirme: **drenaj hesabı** ile diğer tekniklere karşı (hidrolojik tutarlılık). Nitel değerlendirme: kullanıcılardan istem ile arazi oluşturma.
- Elevasyon histogramları ile sınıf dengesi (eşitlenmiş temsilciler). Geriye dönük FID/Fréchet kullanımı: BULUNAMADI bu makalede.

**4.4 Guérin ve diğ. (2017)** — "Interactive example-based terrain authoring with conditional GANs", ACM TOG. [Ö] (arama özeti: taslak çizimden cGAN ile arazi sentezi). Tam metin okunmadı (https://www.cs.purdue.edu/homes/bbenes/papers/Guerin17ToG.pdf erişimi denenmedi; yalnız arama sonucunda listelendi).

**4.5 "Schott 2023"**: BULUNAMADI. Arama, 2023 tarihli Schott makalesi döndürmedi. Yakın eşleşme: Argudo, Guérin, Schott, Galin (2025), "Terrain Descriptors for Landscape Synthesis, Analysis and Simulation", Computer Graphics Forum (STAR) — https://diglib.eg.org/handle/10.1111/cgf70080 (tam metin ERİŞİLEMEDİ; ayrıntı [Ö]). Bu, jeomorfoloji tanımlayıcılarını ve sanatçı geri bildirimlerini inceliyor. Görev metnindeki "Schott 2023" muhtemelen bu 2025 raporuna karışmıştır.

**4.6 FID/Fréchet mesafesi**: [Ö] Arazi (DEM) için değil, çoğunlukla görüntü uzayında kullanılıyor (ör. GAN eğitim seti benzerliği; 3D Earth modeli renderlar; D2-CDIG: SSIM, FID, PSNR, RMSE, LPIPS). Arazi-yükseklik üzerinde standart bir FID ölçütü BULUNAMADI.

**4.7 Hidrolojik tutarlılık**: Perche 2023 (drenaj hesabı ile nicel değerlendirme) [B]. Ek kaynak BULUNAMADI.

**4.8 Eğim-yükseklik histogram uyumu ve orometri**: Argudo 2019 orometrik istatistik [B]; eğim histogram uyumu (KS/Wasserstein gibi) için kaynak BULUNAMADI.

**4.9 Turing testi**: PTRM 2AFC (4.1) [B] Turing benzeri. Doğrudan "Turing testi" ifadesi BULUNAMADI.

## 5. Dağ sırası sürekliliği ölçütleri

**5.1 Topographic prominence** — [B] https://en.wikipedia.org/wiki/Topographic_prominence (ikincil ama ayrıntılı)
- Tanım: zirvenin, daha yüksek araziye herhangi bir yoldan ulaşmak için inmesi gereken en az yükseklik düşüşü; anahtar eyer ("key col") bu yolların en yüksek minimumu.
- Eşikler: Nuttall 15 m, Dawson Marilyn 150 m, ABD'de 14'lü 300 ft (91 m), gayriresmi 2000 ft (610 m).
- Kaynak ayrıca "prominence" ve "dominance" orometrik istatistiklerle Argudo 2019 [B] tarafından kullanılıyor.

**5.2 Reeb graf / kontur ağacı** — [B] https://en.wikipedia.org/wiki/Reeb_graph
- Reeb grafı: bir fonksiyonun seviye kümelerinin evrimini yansıtan bölüm uzayı; iki boyutlu düz alanda polytree ve "contour tree" adını alır. Arazide zirve/eyer/çukur bağlantılarının topolojik özeti için doğal yapı. Eşik değeri ya da "süreklilik" ölçüsü tanımlamıyor.

**5.3 Zirve-eyer grafı (peak-saddle graph)** — [B] Argudo 2019 (4.2): sentez yöntemi, eyer ve zirvelerden grafik kuruyor; tepe-tepe bağlantılarının >%95 oranında (sayfada "more than 95% of the peak to peak connections") bir kriterle uyumlu olduğu belirtiliyor (kriterin tam tanımı okunmadı, [B-kısmi]).

**5.4 "Ridge continuity" ölçüsü**: BULUNAMADI. Yayınlanmış standart bir ölçüt bulunamadı. PTRM'de sırt (ridge) yalnızca geomorfon kategorisi, süreklilik ölçüsü değil [B]. Önerilen yaklaşım (kaynak değil, öneri): sırt çizgisi çıkarımı ve kırılma sayısı/bağlantılılık, PTRM tarzı insan değerlendirmesiyle doğrulama.

## 6. Eksikler ve doğrulanamayanlar (özet)

- Perron 2008 tam metin ve güç spektrumu kriteri: ERİŞİLEMEDİ.
- Mark & Aronson 1984 tam metin ve D≈2.2: ERİŞİLEMEDİ / BULUNAMADI.
- Burbank 1996'da 30–40° eşik eğim: BULUNAMADI (özette yok).
- Huang & Turcotte 1989 spektral ayrıntı: tam metin ERİŞİLEMEDİ.
- Gagnon 2006 spektral üs ve H değerleri: özet doğrulandı, sayılar [Ö].
- Roering ve diğ. "creep and landsliding": doğru atıf Roering, Sklar, Kirchner & Dietrich (2001) Geology; WRR 1999 başlığı farklı (1.6).
- Montgomery 2001: tam metin ERİŞİLEMEDİ; özet [Ö].
- GEBCO dikey doğruluk: BULUNAMADI.
- Copernicus GLO-30 mutlak dikey doğruluk: [B] (<4 m, 90%).
- Dağlık-özel SRTM vs Copernicus karşılaştırması: [Ö] (Helmy 2025; tam metin yok).
- Guérin 2017 ve Schott 2023: ayrıntı ya da Schott 2023 BULUNAMADI.
- FID/Fréchet arazi üzerinde: BULUNAMADI (görüntü uzayında kullanım var).
- Ridge continuity standart ölçüsü: BULUNAMADI.
- Gerçekçilik için Turing testi ifadesi: BULUNAMADI (PTRM 2AFC [B] ile eşdeğer).

## 7. Kaynak listesi (URL)
- https://doi.org/10.1038/379505a0 (Burbank 1996, Nature)
- https://www.scilit.net/publications/20d83bb46d5617151a41122e8ab0dd03 (Mark & Aronson 1984)
- https://rjes.wdcb.ru/v19/2019ES000678/refsdir-678/Mark84.html
- https://earthref.org/ERR/119557/ (Perron 2008 künye)
- https://www.nature.com/articles/460468a (Perron 2009)
- https://npg.copernicus.org/articles/13/541/2006/ (Gagnon 2006)
- https://earthref.org/ERR/37880 (Huang & Turcotte 1989)
- https://zendy.io/title/10.1029/1998wr900090 (Roering 1999 WRR künye)
- https://ajsonline.org/article/88259 (Montgomery 2001 künye)
- https://www.gebco.net/data-products/gridded-bathymetry-data/ (GEBCO)
- https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM (Copernicus DEM)
- https://help.emd.dk/mediawiki/images/a/ae/20210920_AccuracyCopernicusDEM.pdf (SRTM vs Copernicus, [Ö])
- https://arxiv.org/abs/1909.04610 ve https://ar5iv.labs.arxiv.org/html/1909.04610 (PTRM)
- https://people.cs.uct.ac.za/~jgain/wp-content/papercite-data/pdf/argudo2019.pdf (Argudo 2019)
- https://www.cs.purdue.edu/homes/bbenes/papers/Perche23CGF.pdf (Perche 2023)
- https://diglib.eg.org/handle/10.1111/cgf70080 (Argudo, Guérin, Schott, Galin 2025)
- https://en.wikipedia.org/wiki/Topographic_prominence
- https://en.wikipedia.org/wiki/Reeb_graph
