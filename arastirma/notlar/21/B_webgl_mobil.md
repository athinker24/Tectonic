# B: Kabartma gösteriminin mobil tarayıcıda WebGL ile çizimi

Durum: TAMAMLANDI (son tur). Etiketler: [B] tam metin okundu, [D] resmi belgelendirme/spesifikasyon, [Ö] arama özeti veya ikincil kaynak (tam metin okunmadı), [TAHMİN] kaynaksız hesap.

## Özet
- WebGL2, iOS Safari 15'ten itibaren [Ö]; Android Chrome için WebGL2 desteği bu turda ayrıca doğrulanmadı.
- Terrain-RGB ve Terrarium kodlama formülleri resmi/ikincil kaynaklarla doğrulandı [D/B].
- MapLibre hillshade paint varsayılanları spesifikasyondan doğrulandı [D].
- Mobilde piksel başına komşu örnekleme pahalı olabilir; ön hesaplama (normal/eğim karosu) önerilir [Ö].
- WebGPU, MDN'e göre henüz Baseline değil [D]; Safari 26 varsayılan açıklaması yalnızca ikincil kaynakta [Ö].
- Ölçüm verileri (kare hızı, 1-3 milyon hücre süresi, PNG boyutu) bulunamadı: hedef cihazda ölçüm gerekir.

## 1. WebGL1/WebGL2 destek durumu, doku sınırları, kodlama
- WebGL2 iOS Safari'de sürüm 15'ten itibaren destekli. Değer: "iOS 15"; kaynak: https://web-platform-dx.github.io/web-features-explorer/features/webgl2 [Ö]. caniuse ile aynı yönde ama caniuse doğrudan ERİŞİLEMEDİ.
- WebGL en iyi uygulamalar: "The only errors a well-formed page generates are OUT_OF_MEMORY and CONTEXT_LOST_WEBGL." ve "Handle webglcontextlost events, which can be emitted when the GPU runs out of memory, among other reasons." [B] https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
- MAX_TEXTURE_SIZE: MDN sayfasındaki örnek çıktı "MAX_TEXTURE_SIZE: 4096" [B, yalnızca örnek; cihaz değeri değil]. Kaynak: aynı MDN sayfası. Genel aralık 4096-16384 bilgisi bu turda kaynakla doğrulanmadı.
- NPOT dokular: WebGL1'de mipmap ve wrap kapatılmadan NPOT doku "fail by returning transparent black" [B] (https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial/Using_textures_in_WebGL). WebGL2 için NPOT davranışı bu turda ayrıca doğrulanmadı.
- EXT_color_buffer_float: "Baseline Widely available", Eylül 2021'den beri; "available to WebGL 2 contexts only" [B] (https://developer.mozilla.org/en-US/docs/Web/API/EXT_color_buffer_float). Bu uzantı R16F gibi formatları render hedefi yapar [Ö].
- Chrome Android'de EXT_color_buffer_float sürüm 56'dan itibaren; Firefox Android 51 [Ö, MDN uyumluluk verisi arama özetinde].
- iOS: bir WebKit bug thread'ine göre iOS 16.4'te EXT_color_buffer_float raporlanıyor; ayrıca EXT_color_buffer_half_float iOS'ta WebGL1 ve WebGL2'de açıklanmış [Ö].
- OES_texture_float_linear: anket verisi Android %74,19, iOS %45,95 [Ö, anket, cihaz garantisi değil]. Kaynak: https://web3dsurvey.com/webgl2/extensions/OES_texture_float_linear (arama özeti).
- R16F'nin mobilde filtrelenebilirliği: BULUNAMADI (kesin kaynak yok). Çalışma zamanı özelliği tespiti önerilir [TAHMİN/öneri].
- Terrain-RGB (Mapbox) [D]: "encoding each color channel as a position in a base-256 numbering system ... 16,777,216 unique values ... 0.1 meter height increments"; formül `height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)`. https://docs.mapbox.com/data/tilesets/reference/mapbox-terrain-rgb-v1/ . Veri zoom 15 çözünürlüğüne kadar.
- Terrarium (Mapzen/Tilezen) [B, crate kaynak kodu]: `elevation = (R * 256 + G + B / 256) - 32768` metre; atıf: joerd formats.md#terrarium. Kaynak: https://docs.rs/crate/terrain-codec/0.2.1/source/src/heightmap/mod.rs . joerd birincil sayfası ERİŞİLEMEDİ.
- Bir QGIS listesi (2020) farklı bir Terrarium şeması öneriyor; standart formülle uyuşmadığı için dikkatle okunmalı [Ö].

## 2. Fragment shader'da hillshade maliyeti ve kare hızı
- Piksel başına 8 komşu okuması mobilde çok yavaş olabilir: "Per fragment, we need to look at 8 surrounding pixels • Too slow for many mobile devices." [Ö, Speaker Deck "dynamic terrain visualization"]. Aynı sunumda 8 yön, 32 piksel yarıçaplı sürümde 256+ okuma ve CPU ön işleme 250+ ms/karo [Ö].
- Terrain Viewer, normalleri WebGL2 tek geçişiyle GPU'da önceden hesaplıyor; WebGL2 yoksa CPU geri dönüşü var [Ö] (https://terrain-viewer.iconem.com/docs/dev/lighting-effects/).
- Karo kenarları için komşu veri gerekir; Mapbox GL JS komşu karolardan doldurur; alternatif padded karo (ör. 260/516 px) [Ö].
- Kare hızı: bir Three.js forum iletisinde telefonda 60 fps'ten 20 fps'e düşüş bildiriliyor (ölçüm kaynağı değil, anekdot) [Ö].
- 1-3 milyon hücrelik harita için çizim süresi ve kare hızı: BULUNAMADI (ölçülmüş veri yok). Cihaz üzerinde ölçüm gerekir.
- dFdx/dFdy türev tabanlı hillshade maliyeti: BULUNAMADI (kaynak taranmadı).

## 3. MapLibre GL JS terrain / hillshade katmanı
- Hillshade paint özellikleri [D] (https://maplibre.org/maplibre-style-spec/layers/ , tam metin okundu):
  - hillshade-illumination-direction: sayı dizisi, [0,359], varsayılan 335; çoklu ışık yalnızca hillshade-method multidirectional iken.
  - hillshade-illumination-altitude: [0,90], varsayılan 45.
  - hillshade-exaggeration: [0,1], varsayılan 0.5; "Intensity of the hillshade".
  - hillshade-shadow-color: varsayılan "#000000"; gölge alanlar.
  - hillshade-accent-color: varsayılan "#000000"; "accentuate rugged terrain like sharp cliffs and gorges".
  - hillshade-highlight-color: arama özetinde #FFFFFF örneği; sayfada varsayılan doğrulanmadı (özellik adı ve tipi için spec sayfası tam okunmalı).
- Resmi "add a hillshade layer" örneğinde direction 315, shadow #000000, highlight #FFFFFF, accent #000000 [B] (https://maplibre.org/maplibre-gl-js/docs/examples/add-a-hillshade-layer/). Yani örnek değeri ile spec varsayılanı farklı.
- raster-dem kaynağı [D] (https://maplibre.org/maplibre-style-spec/sources/): "Only supports Mapbox Terrain RGB and Mapzen Terrarium tiles." encoding: terrarium | mapbox (varsayılan) | custom. custom için redFactor, greenFactor, blueFactor, baseShift parametreleri; custom 3.4.0'dan, mapbox/terrarium 0.43.0'dan destekli (tablo). Örneklerde tileSize 256 ve maxzoom 19 görülüyor [B].
- Exaggeration 0 iken hillshade offscreen pass yapmıyor [Ö, eski MapLibre kaynağı arama özeti].
- Spec sayfasında hillshade'ın 3D terrain ile ilişkisi ve flat/ light modu ayrıntısı: [B, 3d-terrain örneği] "A global directional light source which is only applied on 3D and hillshade layers."

## 4. Bellek, pil, iOS bağlam kaybı, canvas boyut sınırı
- Canvas alanı sınırı: eski iOS Safari'de 16.777.216 piksel (örn. 4096x4096) [Ö, blog ve WebKit bug]. Bir blog iOS 18'de 8192x8192 / 67.108.864 piksel olduğunu söylüyor, ancak Apple notlarında doğrulanmadı [Ö].
- WebKit bug 271002: "[iOS] Increase the limit on the canvas size to 8192x8192" (2024) [Ö] (https://lists.webkit.org/pipermail/webkit-unassigned/2024-March/1154963.html).
- WebGL bağlamı için 2017 WebKit bug'ı Safari'nin WebGL'i yatay/dikey 4096 ile sınırladığını söylüyor [Ö].
- iOS Safari WebGL bağlam kaybı: bellek baskısında, uygulama değiştirme/arka plan sonrası ve canvas yeniden boyutlandırmada olabilir; bazı iOS 18.2-18.3 raporlarında yeniden oluşturulamayan bağlam [Ö, WebKit bug, Apple forum, Cesium topluluğu].
- Önerilen kod: webglcontextlost olayında preventDefault() ve yeniden kurma; iOS'ta geri yüklemenin güvenilirliği doğrulanmadı [Ö].
- Pil tüketimi (sürekli render, GPU süresi): BULUNAMADI.

## 5. WebGPU durumu
- MDN WebGPU API [D]: "Limited availability"; "This feature is not Baseline because it does not work in some of the most widely-used browsers." ; secure context (HTTPS) gerekir. https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API
- Safari 26: WWDC25 duyurusuna göre WebGPU Safari 26 beta'da iOS/iPadOS için geldi [Ö, Privacy Guides forum aktarımı]; bir ikincil kaynak Safari 26'da varsayılan olarak etkin diyor [Ö]. Apple'ın Safari 26 sürüm notları JavaScript gerektirdiği için ERİŞİLEMEDİ, bu yüzden resmi doğrulama yok.
- Chrome Android'de WebGPU durumu: BULUNAMADI (bu turda doğrulanmadı; webgpureport.org ERİŞİLEMEDİ).
- Güvenli kullanım önerisi: WebGPU'yu birincil yol değil, özellik tespiti ile isteğe bağlı iyileştirme olarak kullanmak; WebGL2 yedek olarak kalmalı [TAHMİN/öneri].

## 6. Alternatif: önceden üretilmiş kabartma karoları ve boyut bütçesi
- Önceden hesaplanmış karo fikri, Ön hesaplamanın kare süresini düşürdüğünü destekleyen kaynaklarla uyumlu [Ö, bkz. 2].
- MapTiler Terrain RGB v2 [D] (https://docs.maptiler.com/schema-raster/terrain-rgb/): dataset-id terrain-rgb-v2, zoom 0-14, format webp, çözünürlük 30 m (bazı alanlarda 5 m), dikey çözünürlük 6 m. Bu bir hazır veri ürünü; kendi ürününüz için kodlama kararını etkiler.
- Mapbox Terrain-RGB'nin 0.1 m artımı [D] ile MapTiler'ın 6 m dikey çözünürlüğü farklı hassasiyet anlamına gelir.
- 16-bit PNG boyut bütçesi (örn. ~3 MB): BULUNAMADI. Kaynaklı ölçüm yok. [TAHMİN] 256x256 karo ham 16-bit gri ölçek = 128 KB; sıkıştırılmış boyut arazi karmaşıklığına göre değişir. Gerçek ölçüm gerekir.
- Cloudflare Pages / R2 dağıtım limitleri ve maliyetleri: BULUNAMADI (bu turda aranmadı).
- Actions'ta karo üretimi (CI) ve sunum için ayrıca kaynak aranmadı: BULUNAMADI.

## Erişilemeyen / sorunlu kaynaklar
- https://caniuse.com/webgl2 : HTTP 406 (curl), WebFetch DNS hatası. ERİŞİLEMEDİ. Bot koruması olası; atlatılmadı.
- https://wikis.khronos.org/webgl/Implementations/SafariiOS : JavaScript doğrulama sayfası. ERİŞİLEMEDİ.
- https://developer.apple.com/documentation/safari-release-notes/safari-26-release-notes ve safari-26_1 : JavaScript gerektiriyor. ERİŞİLEMEDİ.
- https://webgpureport.org/ : WebFetch DNS hatası. ERİŞİLEMEDİ.
- https://github.com/tilezen/joerd/blob/master/docs/formats.md : metin çıkarılamadı. ERİŞİLEMEDİ.
- https://klokantech.com/labs/dem-color-encoding : metin çıkarılamadı (boş). ERİŞİLEMEDİ.
- https://medium.com/@frederic.rodrigo/... (karo optimizasyonu): metin çıkarılamadı. ERİŞİLEMEDİ.
- WebFetch ile maplibre.org ve docs.mapbox.com DNS hatası verdi; curl (proxy) ile erişildi.
- Hiçbir kaynakta bulunamadı: R16F mobil filtrelenebilirlik kesin durumu, mobil GPU MAX_TEXTURE_SIZE cihaz verileri, 1-3 milyon hücre çizim süresi, kare hızı ölçümleri, 16-bit PNG boyut ölçümü, Cloudflare dağıtım limitleri.
