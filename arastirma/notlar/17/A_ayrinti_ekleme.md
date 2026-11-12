# A: Kaba arazi sonucuna ince çözünürlükte ayrıntı ekleme (araştırma notları)

Durum: TAMAMLANDI (bölüm 5 ve tabloya kadar). Açık: Schott 2024 tam metni, kütle korunumu denklemi, CPU süreleri.

Etiketler: [B] tam metin okundu, [B-öz] özet okundu, [Ö] arama özeti, BULUNAMADI, ERİŞİLEMEDİ.

## 1. Arazi süperçözünürlüğü (örnek tabanlı / öğrenmeye dayalı)

- Guérin ve diğ. 2017, "Interactive Example-Based Terrain Authoring with Conditional GANs", ACM TOG 36(6), art. 228, DOI 10.1145/3130800.3130804. Her sentezleyici, eskiz-arazi çiftleriyle eğitilmiş bir cGAN. Kullanıcı nehir/vadi/sırt eskizi çizer, sentezleyici arazi üretir. Erozyon sentezleyicisi düşük maliyetli erozyon üretir. Tam metin okunmadı. [Ö]
  - URL: https://hal-udl.archives-ouvertes.fr/hal-01583706/ ve https://perso.liris.cnrs.fr/eguerin/new/blog/interactive-example-based-terrain-authoring-with-conditional-generative-adversarial-networks/
  - Not: SIGGRAPH history sayfası (history.siggraph.org/?p=210667) yazar listesi uyuşmuyor; atıf için kullanılmamalı.
- Perche ve diğ. 2023, "StyleDEM: a Versatile Model for Authoring Terrains", arXiv:2304.09626. StyleGAN mimarisi DEM üzerinde. İki model (30 m ve 5 m) kademeli çalışır; büyük girdi yamalara bölünür. Süperçözünürlük ve stil karıştırma birlikte kullanılabilir. Kod yayını doğrulanmadı. [Ö]
  - URL: https://arxiv.org/abs/2304.09626
- Argudo ve diğ. 2019, "Orometry-based Terrain Analysis and Synthesis", ACM TOG 38(6), art. 199, DOI 10.1145/3355089.3356535. Zirve ve eyer noktalarından graf kurulur; kaba yükseklik haritasından bu grafla sürekli yükseklik fonksiyonu üretilir, nehir ağı türetilip vadi yamaçları şekillendirilir. [Ö]
  - URL: https://people.cs.uct.ac.za/~jgain/wp-content/papercite-data/pdf/argudo2019.pdf
- Cordonnier ve diğ. 2016, "Large Scale Terrain Generation from Tectonic Uplift and Fluvial Erosion", CGF 35(2), DOI 10.1111/cgf.12820. Yükselme haritasından akış grafı; stream power denklemi. Vektör temsili üzerinde erozyon, sonra DEM'e dönüşüm. [Ö]
  - URL: https://diglib.eg.org/handle/10.1111/cgf12820
- Diffusion ile arazi: Goslin, "Terrain Diffusion" / InfiniteDiffusion, arXiv:2512.08309 (Aralık 2025; v3 Ocak 2026). [B-öz: tam metin 78 bin karakter, yalnız hedefli okuma yapıldı]
  - Hiyerarşik modeller: kaba gezegen modeli kıtaları kurar; ince modeller dağ/vadi/yerel rölyef ekler. Çekirdek latent diffusion 512x512 yama, 90 m çözünürlük, 46 km karo (signed-sqrt uzayında). Yama başına üç kanal: ortalama yükseklik, yüzde 5 yükseklik, veri maskesi. Ayrıntıyı diffusion dekoderi artık (residual) olarak üretir.
  - Eğitimsiz sonsuz örnekleme (MultiDiffusion genellemesi); tutarlılık için komşu karoların paylaşılan bağlamı; seed tutarlılığı.
  - Süre: gecikme ölçümleri tek NVIDIA RTX 3090 Ti üzerinde; "gezegen hızının 9 katı" iddiası tüketici GPU'su için.
  - Bu, 2024 değil. 2024 için Hu ve diğ. "Terrain Diffusion Network" listede görüldü, doğrulanmadı.
  - URL: https://arxiv.org/html/2512.08309v3

- Zhou ve diğ. 2007, "Terrain Synthesis from Digital Elevation Models", IEEE TVCG 13(4), 834-848, DOI 10.1109/TVCG.2007.1027. Örnek DEM'den yama (patch) kopyalama, kullanıcı özellik haritasıyla yönlendirme, graph cut + Poisson editing ile birleştirme. Büyük ölçekli sırt/vadiye odaklı. [Ö]
  - URL: https://faculty.cc.gatech.edu/~turk/my_papers/terrain_synth_tvcg.pdf (arama sonucunda listelendi)
- Gain ve diğ. 2009, "Terrain Sketching", ACM I3D 2009, s. 31-38: eskiz arayüzüyle yordamsal arazi. [Ö]
  - Gain 2015 eşleşmesi: "Parallel, Realistic and Controllable Terrain Synthesis", CGF 34 (2015), DOI 10.1111/cgf12545; karma arayüz (eskiz, boyama, manipülatör). [Ö]
  - WorldBrush: Emilien ve diğ., SIGGRAPH 2015 / ACM TOG 34(4); örnek tabanlı yordamsal dünya. [Ö]
  - Not: Cordonnier'in 2015 Gain/WorldBrush çalışmasında yer aldığı doğrulanamadı (BULUNAMADI bağlantısı).
- Argudo 2016 "Image-based Terrain Synthesis": BULUNAMADI. En yakın: Argudo ve diğ. 2017, "Coherent multi-layer landscape synthesis", The Visual Computer 33, 1005-1015. Sözlük (dictionary) tabanlı, düşük çözünürlük girdiden yüksek çözünürlük arazi. [Ö]
- Grenier, Guérin, Galin, Sauvage 2024, "Real-time Terrain Enhancement with Controlled Procedural Patterns", CGF 43(1), DOI 10.1111/cgf.14992. Örnek tabanlı değil; mevcut araziye yordamsal desenlerle detay ekler, GPU'da gerçek zamanlı; kontrol haritaları paleti. Bu, ince çözünürlük ayrıntı eklemeyle doğrudan ilgili. [Ö]
  - URL: https://diglib.eg.org/handle/10.1111/cgf14992

## 2. Fizik tabanlı detay (akarsu ağı sabit, erozyon ince çözünürlükte)

- Génevaux ve diğ. 2013, "Terrain Generation Using Procedural Models Based on Hydrology", ACM TOG 32(4), art. 143, DOI 10.1145/2461912.2461996. Hidrolojiye dayalı analitik ve sürekli model; kullanıcı kaba eskiz verir, nehir ağı tutarlı yerleşir. Topluluk uygulaması: github.com/wattzhikang/terrainHydrology. [Ö]
  - URL: https://www.cs.purdue.edu/homes/bbenes/papers/Genevaux13ToG.pdf
- Schott ve diğ. 2023, "Large-scale terrain authoring through interactive erosion simulation", ACM TOG 42(5). Erozyon yükselme (uplift) alanında stream power ile simüle; hızlı drenaj alanı yaklaşımı; kopyala-yapıştır, warp, yükseklik kısıtları; nehir ağı oyulabilir. Vektör nehir ağı açıkça geçmiyor. [Ö]
- Schott ve diğ. 2024, "Terrain Amplification using Multi-Scale Erosion", ACM TOG 43(4) (SIGGRAPH 2024). Düşük çözünürlük girdiyi yüksek çözünürlüğe hidrolojik tutarlılıkla çıkarır; termal, stream power ve yamaç erozyonu yaklaşımları çok ölçekli. [B-öz] Sayfa özeti okundu (https://h-schott.github.io/p/mserosion): "düşük çözünürlük girdiyi yüksek çözünürlüğe hidrolojik tutarlılıkla" çıkarır; termal, stream power erozyonu ve biriktirme, farklı ölçeklerde yaklaşık hızlı simülasyonlar. DOI 10.1145/3658200, ACM TOG 43(4), art. 145, 12 sayfa. Tam PDF ve kütle korunumu koşulu HENÜZ ALINAMADI.
- Cordonnier ve diğ. 2016 (bkz. bölüm 1): yükselme ve erozyon vektör gösterim üzerinde; sonra DEM. Bu, "kaba ağı sabit tutup ince çözünürlükte erozyon" fikrinin doğrudan öncülü. [Ö]

## 3. Gürültü tabanlı ayrıntı (fBm, ridged multifractal, domain warping; spektrum)

- Musgrave ridged multifractal: Blender belgesi, mutlak değer alıp yüzeyi ters çevirerek "kanyon" görünümü. Kaynak olarak Musgrave, "Texturing and Modeling: A Procedural Approach", 3. baskı, bölüm 16. [Ö]
  - URL: https://docs.blender.org/manual/en/2.80/render/shader_nodes/textures/musgrave.html
- fBm: oktav toplama (frekans artar, genlik azalır). [Ö] URL: https://thebookofshaders.com/13/
- Domain warping: f(p) = fbm(p + fbm(p + fbm(p))) (Inigo Quilez). Makale metni alınamadı; yalnız ikincil kaynaktan. [Ö, doğrulanmadı]
- Simplex noise: BULUNAMADI (aramada bulunmadı).
- Spektrum: Dünya topografyası güç spektrumunda β ≈ 2 geniş ölçek aralığında; fBm için β = 2H + 1, dolayısıyla H ≈ 0,5 (bu basit eşleme). Eşik: 2B izotropik yüzeyde 2B PSD ~ q^(-2-2H), D = 3 − H. Tahmin tuzakları: pencere sızıntısı, açı ortalaması konvansiyonu (1B β ≈ 2; açı ortalamalı β + D − 1). Bazı veri setlerinde iki rejim (kırılma). [Ö] URL: https://arxiv.org/pdf/1504.02898 ; https://arxiv.org/pdf/1607.03040 ; https://npg.copernicus.org/articles/13/541/2006/npg-13-541-2006.pdf

## 1 ek. StyleDEM tam metin [B] (https://arxiv.org/html/2304.09626)

- Süperçözünürlük (bölüm 4): büyük girdi, ağ girişi 1024x1024 olduğu için s boyutlu yamalara bölünür; yamalar ayrı üretilir, çıktı için histogram eşleştirme ile yükseklik aralığı orijinal yamaya geri taşınır. Sınırda süreksizlik, yamaların s/2 örtüşmeli ara yamalarla harmanlanmasıyla giderilir ((2k-1)^2 yama). Örnek: çözünürlük 3 katına çıkarıldı.
- Önceki (Guérin 2017'deki) yöntem için: "birkaç dakika/görüntü", etkileşim için engelleyici. [B]

## 4. Tutarlılık (kütle korunumu, kaba ortalama, akarsu ağı)

- Terrain Diffusion [B-öz, hedefli okuma]: Laplace kodlama. Düşük frekans L, kaba çözünürlük (blur + downsample), yüksek frekans H = orijinal − yükseltilmiş L. Üretimden sonra (L+H) provizyonel yükseklik haritasına decode edilip blur + downsample ile L̂ yeniden çıkarılır; yüksek frekans gürültüsü Ĥ'ye yönlendirilir. Nihai çıktı L̂ + H. Yani kaba (düşük frekans) hata yok olur, ince detay korunur. Bu, "kaba ortalamayı koruma" koşulu için doğrudan bir şablon: kaba ortalamayı ayrı bir kanal olarak koşullandır, ince detayı ortalaması sıfır (H) olarak ekle.
- Koşullandırma kanalları: yama başına ortalama yükseklik, yüzde 5 yükseklik, veri maskesi (Terrain Diffusion). Bu kanallar kaba ortalamaya uyumu kolaylaştırır.
- Akarsu ağı korunumu: Schott 2024 (hidrolojik tutarlılık) ve Génevaux 2013 (nehir ağının tutarlı yerleşimi) ilgili; ancak kütle korunumu için açık bir denklem tam metinden alınamadı. BULUNAMADI (tam metin erişilemedi).
- Argudo 2019 [Ö]: kaba yükseklik haritası zirve/eyer grafına dönüşüp sürekli yüzeye çevrilir; yani kaba yapı kısıt olarak kullanılır.
- Schott 2024 ACM sayfası: ERİŞİLEMEDİ (dl.acm.org JavaScript/çerez duvarı; bot koruması atlatılmadı). h-schott.github.io üzerinden yalnız özet alındı.

## 5. Süre ve çıktı boyutu (Python / CPU uyumu)

- Terrain Diffusion [B-öz]: gecikme ölçümü tek NVIDIA RTX 3090 Ti; "9 kat gezegen hızı" iddiası tüketici GPU'su. Çekirdek 512x512 yama, 90 m, 46 km karo. CPU süresi BULUNAMADI.
- StyleDEM [B]: süperçözünürlük 1024x1024 ağ girişine göre yama; süre ölçümü raporlanmadı (bu metinde). BULUNAMADI (süre). Ağın GPU'da çalışması beklenir; açık doğrulama yok.
- Guérin 2017 [Ö]: "erozyon sentezleyicisi düşük maliyetli". Sayı verilmedi.
- Grenier 2024 [Ö]: GPU'da (grafik donanımı) gerçek zamanlı; CPU süresi BULUNAMADI.
- Python/CPU uyumu sonucu: yukarıdaki yöntemlerin çoğu GPU'ya bağlı (GAN, diffusion). Kaba-ince ayrıntı için Python/CPU dostu yol: Laplace L+H ayrıştırması ile gürültü tabanlı H (fBm / ridged) eklemek; bu CPU'da NumPy ile yapılabilir (süre tahmini doğrulanmadı).

## Özet bulgu tablosu

| Konu | Kaynak | Etiket | Not |
|---|---|---|---|
| cGAN eskiz-arazi | Guérin 2017 | Ö | ACM TOG 36(6) |
| StyleDEM süperçözünürlük | Perche 2023 | B | yama + s/2 örtüşme |
| Orometri | Argudo 2019 | Ö | zirve/eyer grafı |
| Akış/erozyon vektör | Cordonnier 2016 | Ö | stream power |
| Hidrolojik yordamsal | Génevaux 2013 | Ö | nehir ağı tutarlı |
| Çok ölçekli erozyon | Schott 2024 | B-öz | tam metin ERİŞİLEMEDİ |
| Gerçek zamanlı detay | Grenier 2024 | Ö | yordamsal desen |
| Diffusion arazi | Goslin 2025 | B-öz | L+H, 90 m, RTX 3090 Ti |
| Argudo 2016 | — | BULUNAMADI | en yakın 2017 |
| Simplex noise | — | BULUNAMADI | aramada yok |
| Kütle korunumu denklemi | — | BULUNAMADI | tam metin yok |

Ağ notu: h-schott.github.io ilk WebFetch'te DNS hatası verdi; curl ile sayfa alındı. dl.acm.org erişilemedi (JS/çerez duvarı). Bot koruması aşılmadı.

## 2. Fizik tabanlı detay (akarsu ağı sabit, erozyon ince çözünürlükte)

_Bekliyor._

## 3. Gürültü tabanlı ayrıntı (fBm, ridged multifractal, domain warping; spektrum β, Hurst)

_Bekliyor._

## 4. Tutarlılık (kütle korunumu, kaba ortalama ve akarsu ağının korunması)

_Bekliyor._

## 5. Süre ve çıktı boyutu (Python / CPU uyumu)

_Bekliyor._
