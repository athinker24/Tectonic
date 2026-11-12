# 17. Ayrıntı ekleme ve doğallık

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun sentezidir (A kaba sonuca çok ölçekli ayrıntı ekleme, B litolojinin arazi biçimine etkisi); sentezi ben yazdım. Ham notlar `arastirma/notlar/17/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** özet ya da ansiklopedi sayfası okundu, **[Ö]** arama özeti, doğrulanamadı, **[H]** bizim çıkarımımız, **[Y]** bulunamadı.

Dürüst durum: bu konuda birincil kaynak çok az okunabildi. Tam metin okunanlar: StyleDEM (Perche ve diğerleri 2023) ve Portenga'nın tezi. Geri kalanlar özet düzeyinde ya da ansiklopedi; Stock ve Montgomery 1999, Sklar ve Dietrich 2001, Kirby ve Whipple 2012, Hartmann ve Moosdorf 2012 gibi temel makaleler erişilemedi.

## Kısa sonuç

**1. Kaba fiziksel sonuca ayrıntı eklemenin yayımlanmış yöntemlerinin çoğu GPU'ya bağlı.** StyleDEM, Terrain Diffusion ve Guérin 2017 GPU kullanıyor; hiçbirinin CPU süresi raporlanmadı [B ve Ö]. Aracın Python / CPU ortamında (13. belge) pratik yol, kaba sonucu Laplace ayrışımıyla düşük frekanslı kısım olarak sabitleyip üzerine fBm / ridged çok-fraktallı gürültü eklemek; bu benim çıkarımım, doğrulanmadı [H].

**2. Kaba ortalamayı koruma koşulunun şablonu var.** Terrain Diffusion: Laplace ayrışımı L + H; üretim sonrası L̂ yeniden çıkarılır, nihai çıktı L̂ + H; kaba hata yok olur, detay korunur; koşullandırma yama ortalaması, yüzde 5 yükseklik ve maske ile yapılıyor [B-öz]. Bu, 14. belgede çözünürlük bağımlılığı sorununu hafifletmenin bir yolu.

**3. Litoloji arazi biçimini ciddi biçimde değiştiriyor, ama K katsayısının litolojiye göre değişimi için doğrulanmış sayı yok.** Stock ve Montgomery 1999 değerleri yalnızca arama özetinden: granit ve metamorfik 1e−7 ile 1e−6, volkanoklastik 1e−5 ile 1e−4, çamurtaşı 1e−4 ile 1e−2 (m = 0,4 için) [Ö]; makale erişilemediği için 13. belgedeki "K aralığı doğrulanamadı" uyarısı geçerli kalıyor. Litoloji ile erodibilite yaklaşık iki büyüklük mertebesi değişiyor (Zondervan ve diğerleri, GSA 2022 özeti, [Ö]).

**4. Küresel aşınma hızında kayaç türü farkı küçük ama ölçülü.** Portenga'nın tezi (tam metin): çıkıntılarda ortalama aşınma 12 ± 1,3 m/milyon yıl; tortul 19 ± 1,9, metamorfik 13 ± 1,7, magmatik 8,6 ± 0,9 [B]. Havza ortalaması 209 ± 33 m/milyon yıl, medyan 53 (n = 1110) [B]. Promptumdaki "218 mm/bin yıl" değeri tezde bulunamadı.

## 1. Ayrıntı ekleme yöntemleri

| Yöntem | Ne yapar | Etiket |
|---|---|---|
| Perche ve diğerleri 2023, StyleDEM (arXiv 2304.09626) | Süperçözünürlük: girdi 1024 × 1024 ağ boyutuna göre yamalara bölünür, histogram eşleştirmesiyle yükseklik aralığı geri taşınır, s/2 örtüşmeyle harmanlanır ((2k − 1)² yama); örnekte 3 kat büyütme | [B] |
| Guérin ve diğerleri 2017, ACM TOG 36(6):228 (doi 10.1145/3130800.3130804) | Eskiz tabanlı koşullu GAN; süre sayısı raporlanmadı ("düşük maliyetli") | [Ö] |
| Argudo ve diğerleri 2019, ACM TOG 38(6):199 (doi 10.1145/3355089.3356535) | Oro-metri: zirve ve eyer grafı, sürekli yüzey | [Ö] |
| Zhou ve diğerleri 2007, IEEE TVCG 13(4):834 ile 848 | Yama kopyalama, graph cut ve Poisson | [Ö] |
| Gain ve diğerleri 2009 "Terrain Sketching"; Gain, Merry, Marais 2015 (CGF 34); Emilien ve diğerleri 2015 WorldBrush | Eskizle düzenleme | [Ö] |
| Grenier ve diğerleri 2024, CGF 43(1) (doi 10.1111/cgf.14992) | Kontrollü yordamsal desenlerle gerçek zamanlı geliştirme, GPU | [Ö] |
| Schott ve diğerleri 2024, "Terrain Amplification using Multi-Scale Erosion", ACM TOG 43(4):145 (doi 10.1145/3658200) | Çok ölçekli erozyonla büyütme; yalnızca özet okundu (ACM sitesi tam metni engelledi, atlatılmadı) | [B-öz] |
| Génevaux ve diğerleri 2013, ACM TOG 32(4):143 | Hidroloji tabanlı; nehir ağı tutarlı | [Ö] |
| Cordonnier ve diğerleri 2016, CGF 35(2) | Yükselme ve erozyon vektör gösterimde, sonra DEM | [Ö] |
| "Terrain Diffusion" / InfiniteDiffusion (arXiv 2512.08309, Aralık 2025) | Laplace ayrışımı L + H; RTX 3090 Ti; çekirdek 512 × 512 yama, 90 m, 46 km karo | [B-öz] |

Düzeltmeler: "Terrain Diffusion" 2024 değil, Aralık 2025; "Argudo 2016 Image-based Terrain Synthesis" bulunamadı, en yakın makale Argudo ve diğerleri 2017, "Coherent multi-layer landscape synthesis", The Visual Computer 33 [Ö]. "Schott 2024" gerçekten var (ACM TOG 43(4):145, "Terrain Amplification using Multi-Scale Erosion"); önceki belgelerde onu bulunamadı olarak not etmiştim, o not yanlıştı. Kütle korunumu denklemi ve nehir ağı koşulu bulunamadı (Schott 2024 tam metni yok) [Y].

**Gürültü ve spektrum.** Musgrave ridged multifractal: mutlak değer ve ters çevirme ("kanyon"), kaynak Musgrave, Texturing and Modeling, 3. baskı, 16. bölüm [Ö]. fBm: oktav toplamı. Domain warping: f(p) = fbm(p + fbm(p + fbm(p))) (Quilez, ikincil kaynak, doğrulanmadı). Simplex gürültü için kaynak bulunamadı [Y]. Yeryüzü topografyasında güç spektrumu eğimi β yaklaşık 2; fBm için β = 2H + 1, basit eşlemeyle H yaklaşık 0,5; 2B izotropik: D = 3 − H [Ö]. Konvansiyon ve pencere sızıntısı tuzakları var (arXiv 1504.02898).

## 2. Litoloji ve arazi biçimi

| Konu | Bulgu | Etiket |
|---|---|---|
| K ve litoloji (m = 0,4) | granit / metamorfik 1e−7 ile 1e−6; volkanoklastik 1e−5 ile 1e−4; çamurtaşı 1e−4 ile 1e−2 (Stock ve Montgomery 1999). "K oranı 10 ile 100" ifadesi makalede doğrudan bulunamadı; aralıklardan hesaplanan fark yaklaşık 1e2 ile 1e5 (benim hesabım) | [Ö ve H] |
| Erodibilite | yaklaşık iki büyüklük mertebesi değişiyor (Zondervan ve diğerleri, GSA 2022 özeti) | [Ö] |
| Direnç | aşınma direnci çekme dayanımının karesiyle orantılı (Sklar ve Dietrich 2001) | [Ö] |
| Kirby ve Whipple 2012 | litoloji profil yorumunu karmaşıklaştırır; "litolojik knickpoint" tanımı bulunamadı | [B-öz] |
| Tabakalı kayaç | hogback: eğim 30° ile 40°'nin üstünde, sert ve yumuşak ardalanma; cuesta: düşük eğim; ikisi bir süreklilik. Mesa, bazalt kapak ve ters topografya | [B-öz ve Ö] |
| Landlab / Fastscapelib | Landlab `LithoLayers` (K_sp, katman / kimlik) ve Fastscapelib `SPLEroder` k_coef dizisi ile K haritası üretilebilir; hazır örnek iş akışı bulunamadı | [Ö] |
| Granit / volkanik | tor ve inselberg için model tartışması; batolit ölçeğinde rölyef kontrastı ve aşınma hızı için nicel çalışma bulunamadı; lav akıntısı ters topografyası | [Ö ve Y] |
| Karst | karbonat çözünmesi, doline, polye, yüzey akışı az olabilir; kireçtaşında ve kırığın sık olduğu yerde en güçlü gelişir | [B-öz] |
| GLiM (Hartmann ve Moosdorf 2012) | 16 birincil sınıf, 12 + 14 alt sınıf, yaklaşık 1 235 400 poligon; alan payı: tortul yaklaşık %64 (üçte biri karbonat), metamorfik yaklaşık %13, plütonik yaklaşık %7, volkanik yaklaşık %6, su ve buz yaklaşık %10 | [Ö] |
| GLHYMPS (Gleeson 2014) | ortalama poligon yaklaşık 100 km²; ortalama geçirgenlik yaklaşık 1e−15 m² (donmuş zemin) ve 1e−14 m²; gözeneklilik %14 | [Ö] |
| Kayaç ve aşınma hızı (Portenga'nın tezi, tam metin) | havza ortalaması 209 ± 33 m/milyon yıl, medyan 53 (n = 1110); çıkıntı ortalaması 12 ± 1,3, medyan 5,2 (n = 418); çıkıntıda tortul 19 ± 1,9 (n = 106), metamorfik 13 ± 1,7 (n = 82), magmatik 8,6 ± 0,9 (n = 230) | [B] |

Promptumdaki "218 mm/bin yıl" değeri tezde yok (1 m/milyon yıl = 1 mm/bin yıl; tezdeki havza ortalaması 209). GSA Today (Portenga ve Bierman 2011) metni erişilemediği için 218 doğrulanamadı.

**Aracın litoloji katmanı için çıkarım [H].** Araç bir kayaç haritası üretmeli (kaba katmanlar: çökel, magmatik, metamorfik; sertlik indisi) ve K haritasını bu sertlikten türetmeli. Kullanıcının istisna isteklerinde (ör. platoda yumuşak çökel, sıradağda sert magmatik) bu harita mantıklı bir kurgusal özgürlük sağlıyor. K oranı için kaynaklı bir değer yerine kullanıcıya gösterilen bir aralık (10 ile 100 kat) önerilir; yeni çalışmalarla doğrulanmadığı belirtilmeli.

## 3. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Detay ekleme yöntemi | kaba sonucu Laplace ayrışımıyla düşük frekans olarak sabitle, üstüne fBm ya da ridged ekle | [B-öz ve H] |
| Güç spektrumu eğimi | β ≈ 2 yalnızca 1B profil için (β = 2H + 1, H ≈ 0,5); 2B yüzeyin radyal spektrumunda β = 2H + 2 olduğundan aynı H için β ≈ 3 (doğrulama ajanı, yöntem denetimi); araç hangi boyutu kullandığını belirtmeli | [Ö ve H] |
| Kaba ortalamayı koruma | L̂ yeniden çıkar, L̂ + H | [B-öz] |
| Nehir ağı | kaba çözünürlükte bulunan ağ ince çözünürlükte sabit tutulsun (koşul), kaynak bulunamadı | [H] |
| K ve litoloji | sertliğe göre değişken K haritası; aralık 10 ile 100 kat (kullanıcıya belirtilen) | [Ö ve H] |
| Hogback / cuesta | eğim 30° ile 40°'nin üstü hogback, altı cuesta; kaynak ayrım açısını keyfi sayıyor ve arada homoklinal sırtlar olduğunu belirtiyor, ikili ayrım kaynakta yok | [B-öz] |
| Kayaç türü ve çıkıntı aşınma hızı | tortul 19, metamorfik 13, magmatik 8,6 m/milyon yıl | [B] |
| GPU gereksinimi | StyleDEM, Terrain Diffusion ve Guérin 2017'nin GPU'ya bağlı olduğu kaynakta doğrulanamadı (yayımlanan hız sayıları GPU'da); GitHub'ın standart çalıştırıcılarında GPU yok, ücretli "GPU-powered" büyük çalıştırıcılar var | [B-öz, Ö ve D] |

## 4. Kaynaklar arası çelişkiler

- Stock ve Montgomery K aralıkları: 13. belgede doğrulanamadı olarak işaretlenmişti; burada arama özetinde litolojiye göre alt aralıklar çıktı. İkisi de [Ö]; makaleye erişilince kontrol edilmeli.
- Portenga: promptumdaki 218 ile tezdeki 209 m/milyon yıl.
- Hogback eğim eşiği: "30° ile 40°'nin üstü" ansiklopedi tanımı; jeoloji ders kitaplarında farklı olabilir.

## 5. Bulunamayanlar ve doğrulanamayanlar

- Stock ve Montgomery 1999, Sklar ve Dietrich 2001, Kirby ve Whipple 2012, Hartmann ve Moosdorf 2012, Gleeson 2014, Portenga ve Bierman 2011 (GSA Today) tam metinleri (doi.org 403 / DNS; bot koruması, atlatılmadı).
- Schott 2024 tam metni, kütle korunumu denklemi, nehir ağı koşulu; CPU süreleri; simplex gürültü; Argudo 2016.
- Litolojik knickpoint tanımı; hogback / Appalachian değerleri; batolit ölçekli nicel çalışma; karstta yüzey akışı eksikliğinin nicel değeri; GLiM sınıf bazında tam tablo.
- hazır LEM K haritası iş akışı örneği.

## 6. Promptumdaki hatalar (düzeltildi)

- "Schott 2024" gerçekten var (ACM TOG 43(4)); önceki bulunamadı notu yanlıştı.
- "Terrain Diffusion 2024" Aralık 2025.
- "Argudo 2016 Image-based Terrain Synthesis" doğrulanamadı.
- "Portenga 2011 ortalama 218 mm/bin yıl" tezde 209 m/milyon yıl.
- "K oranı 10 ile 100" makaleden doğrulanamadı; hesaplanan fark çok daha büyük (1e2 ile 1e5).

## Başlıca kaynaklar

- Perche ve diğerleri 2023, StyleDEM: https://arxiv.org/abs/2304.09626
- Schott ve diğerleri 2024: https://h-schott.github.io/p/mserosion
- Terrain Diffusion: https://arxiv.org/html/2512.08309v3
- Grenier ve diğerleri 2024: https://diglib.eg.org/handle/10.1111/cgf14992
- Portenga'nın tezi (uvm.edu): ham notlardaki bağlantı
- Wikipedia sayfaları (hogback, cuesta, karst): ham notlarda
- Tam liste ve her bilginin kaynağı `arastirma/notlar/17/` içinde.
