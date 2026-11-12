# 21. Gerçekçi kabartma gösterimi

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun (A haritacılıkta gölgeleme ve renklendirme, B telefonda WebGL ile çizim) ve benim küçük bir boyut ölçümümün sentezidir; sentezi ben yazdım. Ham notlar `arastirma/notlar/21/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** özet ya da belge sayfası okundu, **[D]** resmi belgelendirme okundu, **[Ö]** arama özeti, doğrulanamadı, **[Ö-ölç]** bu oturumdaki kendi ölçümüm, **[H]** çıkarım, **[Y]** bulunamadı.

Dürüst durum: bu konu araca özgü ölçümler gerektiriyor (telefonda kare hızı, belirli bir cihazda çizim süresi). Bulunan kaynaklar belge ve rehber düzeyinde; kare hızı ve çizim süresi hiçbir kaynakta bulunamadı ve ben de bir telefonda ölçemedim.

## Kısa sonuç

**1. Aracın 5 ile 10 km hücreli çıktısı için en uygun gösterim çok yönlü gölgeleme ile hafif yükseklik renklendirmesinin birleşimi.** Esri'nin çok yönlü gölgelemesi altı yönden ışık birleştiriyor ve aşırı pozlanma ile gölge arasındaki dengeyi düzeltiyor [B-öz]. Patterson ve Jenny (2011, Cartographic Perspectives 69:31 ile 45, doi 10.14714/CP69.20): çapraz karışımlı yükseklik renkleri; çevre renkleri yalnızca 1000 m altında; düz alanlarda gri olmayan hafif gölgeli kabartma; küçük ve orta ölçekler için [B-öz]. Bu, aracın telefonda gösterimi için doğrudan uygulanabilir bir tarif.

**2. 5 ile 10 km hücre kabaca 1:10 milyon ile 1:20 milyon ölçekli harita ayrıntısı.** Ajanın hesabına göre bu ölçekte kabartma çok ayrıntılı gelir; Leonowicz, Jenny ve Hurni (2010, Cartographica 45(1):64 ile 74): SRTM gölgelemesi 1:1.000.000 ölçekte fazla ayrıntılı, gölgelemeden önce eğrilik tabanlı genelleme öneriliyor [B-öz]. Aracın çıktısı zaten kaba hücreli olduğundan bu bir sorun değil, bir yarar: ek genelleme gerekmeyebilir [H].

**3. Telefon çizimi için yükseklik haritasını önceden hesaplanmış gölgelenmiş görüntü olarak sunmak, yükseklik dokusunu cihazda işlemekten daha güvenli.** Mobil GPU'da piksel başına 8 komşu okuma "birçok mobil cihaz için çok yavaş" ve eğim / normal önceden hesaplanmalı [Ö]. İlk sürüm için Actions'ta kabartmayı üretip PNG olarak sunmak yeterli; WebGL canlı gölgeleme sonraki aşama [H].

**4. 16 bit yükseklik haritası dosya boyutu kontrol edildi: 1 milyon hücre için 1,5 MB.** Aşağıda ayrıntı [Ö-ölç].

## 1. Gölgeleme ve renklendirme (A kolu)

| Konu | Bulgu | Etiket |
|---|---|---|
| Klasik tek yönlü gölgeleme | Esri varsayılan azimut 315°, yükseklik 45°, zenit = 90 − yükseklik, eğim ve bakı için 3×3 pencere; formül görüntü olarak verilmiş, Burrough ve McDonell 1998'e atıf | [B-öz] |
| Çok yönlü gölgeleme | Esri güncel çok yönlü mod altı yönden ışık birleştirir; Mark (1992, USGS OFR 92-422): dört azimut (225/270/315/360) 30° yükseklikte, bakıya göre ağırlıklı | [B-öz ve Ö] |
| RVT (Relief Visualization Toolbox, Kokalj ve diğerleri) | gökyüzü görünürlüğü (SVF) yaygın ışık yerine geçiyor; varsayılan 8 yön (16 en iyi), arama yarıçapı 10 piksel, küçük özellikler için 5 ile 10 m (5 ile 20 piksel); açıklık (openness) Yokoyama ve diğerleri 2002'ye göre; çok yönlü gölgeleme RGB 315/15/75; 16 yön yararlı üst sınır | [B-öz] |
| Swiss tarzı renk | Jenny ve Hurni 2006: gri değer ve yükseklikten renk arama tablosu; Hobbs üç yönlü RGB gölgeleme | [B-öz] |
| Çapraz karışımlı yükseklik renkleri | Patterson ve Jenny 2011: çevre renkleri yalnızca 1000 m altında; düz alanlarda gri olmayan hafif kabartma; küçük ve orta ölçek; SRTM30Plus tabanı | [B-öz] |
| Eğrilik tabanlı genelleme | Leonowicz, Jenny, Hurni 2010: SRTM gölgelemesi 1:1.000.000'da fazla ayrıntılı | [B-öz] |
| Eğrilik ve gölgeleme | Kennelly 2008 (Geomorphology, s. 567 ile 577); Kennelly ve Stewart 2014 (IJGIS 28(2), gökyüzü modelleri) | [Ö] |
| Deniz renklendirmesi | Natural Earth 10m okyanus tabanı CleanTOPO2'den, Blue Earth batimetrisi GEBCO'dan | [Ö] |
| Çözünürlük kuralı | çözünürlük (m) = ölçek paydası / 2000 (Farmakis-Serebryakova ve diğerleri) | [Ö] |

Bulunamayanlar: Mark 1992 tam metni, Jenny 2001 denklemleri, Horn 1981 (aranmadı), Imhof tam metni, Veronesi ve Hurni 2014, düşey abartma çarpanı ve küçük ölçekte eğim ağırlığı için kaynak [Y]. "Kennelly 2014 Geomorphology" ifadesi yanlıştı: 2008 Geomorphology (Kennelly) ve 2014 IJGIS (Kennelly ve Stewart) iki ayrı makale. Yokoyama makalesinin yazar adları promptumda yanlıştı (Yokoyama, Shirasawa ve Pike 2002, PE&RS 68(3):257 ile 265).

**Hücre sayısı aritmetiği (ajanın hesabı, kaynak değil) [H].** Küresel 5 km hücre yaklaşık 20 milyon hücre, 10 km yaklaşık 5 milyon; yalnızca kara için 5 km'de yaklaşık 6 milyon, 10 km'de yaklaşık 1,5 milyon. Aracın kıtası (87° × 67°) 8. belgedeki hesapla (derece adımı sabit ağ) 10 km'de yaklaşık 0,72 milyon, 5 km'de yaklaşık 2,9 milyon hücre; eşit alanlı ağda 0,61 ve 2,44 milyon. 1 ile 3 milyon hücre yani tüm kıtayı 5 ile 10 km arasında kapsıyor.

## 2. Telefonda WebGL ile çizim (B kolu)

| Konu | Bulgu | Etiket |
|---|---|---|
| WebGL2 desteği | iOS Safari 15 ve sonrası; caniuse HTTP 406 verdi | [Ö] |
| Kayan nokta doku | `EXT_color_buffer_float` yalnızca WebGL2'de; Baseline, Eylül 2021 | [B] (MDN) |
| MAX_TEXTURE_SIZE | MDN örnek çıktısında 4096 (yalnızca örnek); gerçek sınır cihaza göre | [B, örnek] |
| Mapbox Terrain-RGB | yükseklik = −10000 + ((R·65536 + G·256 + B) · 0,1), 0,1 m artım | [D] |
| Terrarium | (R·256 + G + B/256) − 32768 (terrain-codec kaynağı, joerd'a atıf; birincil joerd sayfası açılamadı) | [B] |
| MapTiler Terrain RGB v2 | zoom 0 ile 14, webp, 6 m dikey çözünürlük | [D] |
| MapLibre hillshade | varsayılan ışık yönü 335, yükseklik 45, abartma 0,5, gölge ve vurgu rengi #000000; highlight varsayılanı doğrulanmadı; raster-dem kodlaması terrarium / mapbox (varsayılan) / custom | [D] |
| Piksel başına komşu okuma | 8 komşu okuma "birçok mobil cihaz için çok yavaş"; normal / eğim önceden hesaplanmalı | [Ö] |
| WebGPU | MDN "Limited availability", Baseline değil; Safari 26'da varsayılan açık iddiası yalnızca ikincil kaynakta | [D ve Ö] |
| iOS canvas alanı | eski sınır 16 777 216 piksel; iOS 18 için 8192 × 8192 iddiası blog kaynaklı | [Ö] |
| WebGL bağlam kaybı | bellek baskısı ve arka plana geçişte | [Ö] |

Bulunamayanlar: R16F'in mobilde kesin filtrelenebilirlik durumu, kare hızı ve 1 ile 3 milyon hücre çizim süresi ölçümleri, dFdx tabanlı gölgelemenin maliyeti, Cloudflare Pages / R2 sınırları [Y]. Apple Safari 26 sürüm notları JavaScript gerektirdiği için okunamadı. WebFetch maplibre.org ve docs.mapbox.com için DNS hatası verdi; curl ile erişildi, bot koruması atlatılmadı.

## 3. Önceden hesaplanmış yükseklik haritası boyutu [Ö-ölç]

Himalaya bloğunun (Nepal, 3°×3°, en engebeli örnek) SRTM verisini ortalayıp 16 bit gri PNG'ye çevirdim (0,15 m adım, optimize edilmiş): 1000 × 1000 piksel (1 milyon hücre) için 1,53 MB; 2000 × 2000 piksel (4 milyon hücre) için 5,75 MB. Aynı bloğun 900 × 900 8 bit gri hâli 0,28 MB [Ö-ölç]. Bu, en engebeli örnekle yapıldı, yani üst sınır kabul edilebilir: genel dünyada daha düz bölgeler daha küçük dosya verir. Aracın çıktısı da yumuşak olduğundan (5 ile 10 km hücre ortalaması) benzer ya da daha küçük olması beklenir [H]. "16 bit PNG yaklaşık 3 MB" iddiası (promptumdaki) bu ölçümle kabaca tutarlı (1 ile 5 MB aralığı).

## 4. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Gölgeleme | çok yönlü (altı yön), azimut 315° civarı ana yön, yükseklik 45° | [B-öz] |
| Renklendirme | çapraz karışımlı yükseklik renkleri, çevre renkleri 1000 m altında, düz alanda gri değil | [B-öz] |
| Gökyüzü görünürlüğü | 8 ile 16 yön, arama yarıçapı 10 piksel (isteğe bağlı) | [B-öz] |
| Yükseklik kodlaması | 16 bit PNG, 0,1 ile 0,15 m adım (Terrain-RGB / Terrarium benzeri) | [D ve Ö-ölç] |
| Dosya boyutu | 10 km hücre kıta için yaklaşık 1,5 MB, 5 km için yaklaşık 5,8 MB (en engebeli örnekle) | [Ö-ölç] |
| Telefonda çizim, ilk sürüm | Actions'ta önceden gölgelenmiş PNG; canlı WebGL gölgeleme sonraki aşama | [H] |
| WebGL | WebGL2 (iOS Safari 15+), WebGPU güvenle kullanılmıyor (Baseline değil) | [D] |
| Düşey abartma | kaynak bulunamadı; MapLibre varsayılanı 0,5 hillshade abartması ayrı şey | [D ve Y] |
| Genelleme | kaba hücre zaten genelleştirilmiş; ek genelleme gerekmeyebilir | [H] |

## 5. Kaynaklar arası çelişkiler

- MapLibre gölgeleme ışık yönü varsayılanı 335 ile Esri ve klasik 315.
- Mark 1992 azimutları (225 / 270 / 315 / 360, 30° yükseklik) ile Esri'nin güncel çok yönlü modu (altı yön).
- iOS canvas sınırı: eski 16 777 216 piksel ile iOS 18 için 8192 × 8192 iddiası.
- WebGPU: MDN "Limited availability" ile Safari 26 varsayılan açık iddiası (ikincil).

## 6. Bulunamayanlar ve doğrulanamayanlar

- Kare hızı ve çizim süresi, R16F filtrelenebilirliği, dFdx maliyeti, düşey abartma kuralı, küçük ölçek eğim ağırlığı.
- Mark 1992, Jenny 2001, Horn 1981, Imhof, Veronesi ve Hurni 2014 tam metinleri; Zakšek ve diğerleri 2011, Kennelly 2008 yalnızca arama özeti.
- caniuse (HTTP 406), Apple sürüm notları (JavaScript gerekiyor), joerd birincil sayfası, Cloudflare Pages / R2 sınırları.
- Kendi boyut ölçümüm yalnızca Himalaya bloğuyla, gerçek bir çıktıyla değil; aracın nihai çıktısı farklı olabilir.

## 7. Promptumdaki hatalar (düzeltildi)

- "Yokoyama ve diğerleri 2002" yazar adları yanlıştı; Yokoyama, Shirasawa, Pike.
- "Kennelly 2014 Geomorphology" yok; 2008 Geomorphology ve 2014 IJGIS iki ayrı makale.
- "iOS canvas 4096×4096" doğru değil; eski sınır 16 777 216 piksel (ikincil).
- "16 bit PNG yaklaşık 3 MB" iddiası ölçümle 1,5 ile 5,8 MB aralığında doğrulandı (hücre sayısına bağlı).

## Başlıca kaynaklar

- Esri "How Hillshade Works" ve çok yönlü gölgeleme sayfaları (ham notlarda)
- RVT kılavuzu v2.2.1 (Kokalj, Zakšek ve diğerleri)
- Patterson ve Jenny 2011: https://doi.org/10.14714/CP69.20
- Leonowicz, Jenny, Hurni 2010, Cartographica 45(1):64 ile 74
- MapLibre style spec (hillshade), MDN (EXT_color_buffer_float, WebGPU)
- Mapbox Terrain-RGB belgesi, Terrarium (terrain-codec)
- Tam liste ve her bilginin kaynağı `arastirma/notlar/21/` içinde.
