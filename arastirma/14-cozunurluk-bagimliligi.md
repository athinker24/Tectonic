# 14. Erozyonun çözünürlük bağımlılığı

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun (A akarsu güç yasasının ızgara boyutuna bağımlılığı, B DEM çözünürlüğü ve ölçüm) ve benim yaptığım küçük bir sayısal denemenin sentezidir; sentezi ben yazdım. Ham notlar `arastirma/notlar/14/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** yalnızca özet ya da kısmi metin, **[Ö]** arama özeti, doğrulanamadı, **[Ö-ölç]** bu oturumdaki kendi ölçümüm, **[T]** tek makalenin türetimi, **[H]** çıkarım, **[Y]** bulunamadı.

## Kısa sonuç

**1. Kaba bir ızgarada akarsu güç yasası, ince ızgaradan çok daha düşük rölyef verir; bunu düzeltmeyen bir 20 km önizleme ile 5 km hesabı tutmaz.** Bu belgenin en önemli bulgusu, benim ölçümüm: aynı 400 km'lik alanda aynı K, m, n ve yükselme ile hücre boyu 20 km'den 2,5 km'ye indirildiğinde ortalama yükseklik her yarıya inişte 1,8 ile 2,4 kat arttı (m = 0,5, n = 1 için 2,3 ile 2,4 kat: 1,0 → 2,3 → 5,5 → 12,6 m) [Ö-ölç]. 20 km'den 5 km'ye geçişte dört ayarda ortalama yükseklik 3,6 ile 5,5 kat arttı (m = 0,5: 5,5; m = 0,45: 5,4; m = 0,4: 4,7; n = 1,5: 3,6). Eşik drenaj alanı (A_c) olmayan ve difüzyonsuz bu en yalın düzenekte sorun beklenen bir sorun; ama büyüklüğü, önizleme ile ana hesap arasındaki fark ayara bağlı olarak 3,6 ile 5,5 kat olabileceğini gösteriyor. (Doğrulama notu: önceki sürümde burada "2,2 ile 2,4 kat" ve "5,4 ile 5,9 kat" yazıyordu; tabloyla yeniden hesaplanınca yalnızca m = 0,5 ve 0,45 satırları için doğruydu.)

**2. Literatürde bu sorun için kuralı olan iki makale var, ve birbirleriyle tam uyuşmuyorlar.** Hergarten (2020): eşik alanı A_c fiziksel alan olarak yazılırsa kanal erozyon terimi δ^(−2β) ile ölçekleniyor, β = 0,5'te δ^(−1) [B]. Hergarten ve Pietrek (2023): yalnızca SPIM için K'nın yeniden ölçeklenmesi α = δx^(n−2m) L^(1−n) T^(−1) (Eş. 16), m/n = 0,5'te δx'ten bağımsız; difüzyon eklenince ölçekleme bozuluyor [B]. Kargère ve diğerleri (2025): kanal başı alanı çözünürlükten bağımsız olacak şekilde fraktal bir çerçeve [B].

**3. 20 km önizleme ile 5 km ana hesabın sonuçları birebir tutmayacak, bu tasarımda kabul edilmeli.** Hergarten 2020 ile Hergarten ve Pietrek 2023 aynı çözünürlük sıçraması için erozyon terimini 4 kat, difüzyonlu durumda A_h'yi 16 kat değiştirmeyi öneriyor [T, A kolunun türetimi]; iki yaklaşım uyuşmuyor.

**4. Gerçek DEM'lerde çözünürlük ölçülen rölyefi de değiştiriyor, ama sayı tablosu bulunamadı.** 5, 10, 20, 90 m ve 1 km hücreler için yerel rölyef oranlarına ve 5 km'den 20 km'ye kaba taneleme etkisine dair kaynaklı bir tablo bulunamadı [Y]. Aracın gerçekçilik ölçümü (20. konu) bu yüzden gerçek bir DEM'i kendisi kaba tanelemeli.

## 1. Akarsu güç yasasında ızgara boyutu bağımlılığı

| Kaynak | Bulgu | Etiket |
|---|---|---|
| Hergarten 2020a, "Rivers as linear elements", ESurf 8:367 ile 377 (doi 10.5194/esurf-8-367-2020) | Eşik kanal alanı A_c tanımlanınca etkin alan A_e ≈ α A_c^β (θ = 0,5 kafes: α = 1,360, β = 0,465; OCN: α = 1,508, β = 0,478). A_c fiziksel alan olarak yazılırsa kanal erozyon terimi δ^(−2β) ile ölçeklenir; β = 0,5'te δ^(−1), Perron ve diğerleri (2008) ile temelde aynı. Kalıntı bağımlılık var: N = 1e5 ile 1e7 arasında k_s 1,6 ile 2,0 | [B] |
| Hergarten ve Pietrek 2023, ESurf 11:741 ile 755 | Yalnızca SPIM için K yeniden ölçeklenmesi α = δx^(n−2m) L^(1−n) T^(−1); m/n = 0,5'te δx'ten bağımsız. Difüzyon eklenince ölçekleme bozulur; gerçek A_h ∝ δx², sabit erodibilitede boyutsuz A_h ∝ δx^(−2). Kanal oluşturan alan D^0,8 ile artar (D × 10 → × 6,5) | [B, PDF] |
| Hergarten 2020b, taşıma sınırlı, ESurf 8:841 ile 854 | Taşıma terimi için piksel boyutuna bağlı ek yeniden ölçekleme faktörü gerekir; tek evrensel formül verilmiyor | [B] |
| Kargère ve diğerleri 2025, ESurf 13:403 ile 415 ("A fractal framework for channel–hillslope coupling") | Eğim değişim noktasında drenaj alanı δ ile bir faktör ölçeklenir; kanal başı alanı δ'dan bağımsız. K ya da m için açık bir δ kuralı yok | [B] |
| Lague 2014, ESPL 39:38 ile 61 | SPIM yalnızca yaklaşık 0,1 ile 5 km² üstündeki kritik alanın üstünde geçerli; Δx kuralı yok | [B] |
| Armitage 2019, ESurf 7:67 | Akış dağıtımı ızgara bağımlılığını etkiler; uyarlanabilir ağ iki çözünürlükte benzer dalga boyu veriyor | [B] |

Düzeltme: "Hergarten 2025, Resolution dependence of the stream power law" diye bir makale bulunamadı. Çözünürlük ve SPL konulu 2025 makalesi Kargère, Constantine, Hales, Grieve ve Johnson'ındır; Hergarten yalnızca atıf. Whipple ve Tucker (1999) PDF'i TLS hatasıyla, Perron ve diğerleri (2008) tam metni erişim nedeniyle okunamadı [Y]. Cordonnier 2016'da K ile hücre alanı ilişkisi, Gailleton 2019 çoklu çözünürlük, Braun ve Willett 2013 ızgara kuralı ve m(Δx), n(Δx) için açık kural bulunamadı [Y].

## 2. Kendi ölçümüm

Düzenek [Ö-ölç]: Fastscapelib 0.3.0 (Python), tek akış yönlendirici + MST çukur çözücü + SPL; 400 × 400 km alan, tüm kenarlar sabit kotlu (0 m), düzgün yükselme U = 1e−3 m/yıl iç düğümlerde, toplam süre 4e7 yıl, dt = 1e5 yıl (örtük çözücü), rastgele başlangıç gürültüsü, difüzyon yok, eşik alan yok, K = 1e−7. Hücre boyu 20, 10, 5, 2,5 km; ortalama yükseklik ve en büyük yükseklik:

| m, n | 20 km | 10 km | 5 km | 2,5 km |
|---|---|---|---|---|
| 0,5; 1 | 1,0 m (en çok 2,3) | 2,3 (5,6) | 5,5 (13,5) | 12,6 (31,7) |
| 0,45; 1 | 6,0 (16,8) | 14,2 (37,4) | 32,4 (86,1) | 69,8 (172,9) |
| 0,4; 1 | 43,4 (129,3) | 96,6 (262,5) | 203,6 (554,4) | 412,2 (1087,1) |
| 0,5; 1,5 | 31,2 (98,4) | 62,0 (171,7) | 113,0 (303,4) | 200,7 (518,3) |

Her hücre yarılanışında ortalama yükseklik 1,8 ile 2,4 kat artıyor (m = 0,5, n = 1 için 2,3 ile 2,4); 20 km'den 5 km'ye (4 kat ince) 3,6 ile 5,5 kat (en büyük yükseklikte 3,1 ile 5,9 kat). Bu, A_c ve difüzyon olmayan, düzgün yükselmeli ve fiziksel olarak sığ bir düzenek (rölyef çok düşük, çünkü K = 1e−7 ile bile 400 km alanda büyük akarsular çok düz); kesin sayılar aracın nihai ayarlarına taşınamaz. Yönü ve büyüklük mertebesi kullanılabilir. Daha büyük bir K ile (1e−5, ilk deneme) m = 0,5 ve n = 1 için tüm çözünürlüklerde rölyef yaklaşık 1 m ve çözünürlükten bağımsız çıktı; yani bu düzenekte sonuç K'ya ve rölyefin küçüklüğüne duyarlı. Betik `arastirma/notlar/14/res_test.py`.

Yorum [H]: ince ızgarada kaynak hücresinin alanı (δx²) küçük olduğundan kaynak yakınındaki eğim, U / (K A^m), kaba ızgaraya göre dikleşiyor ve yükseklik farkı bu yüzden artıyor; Hergarten'in eşik alan (A_c) düzeltmesi ya da Kargère ve diğerlerinin çözünürlükten bağımsız kanal başı alanı tam olarak bu etkiyi hedefliyor. Ölçüm, bu düzeltmelerin gerekli olduğunu destekliyor ama etkinliğini sınamıyor.

## 3. DEM çözünürlüğü ve ölçülen rölyef

- **Zhang ve Montgomery 1994 (WRR 30:1019 ile 1028).** 2, 4, 10, 30, 90 m ızgaralar; 10 m büyük kazanç, 2 ile 4 m marjinal; çözünürlük arttıkça topografik indeksin ortalaması artıyor [Ö]. Sayısal tablo bulunamadı [Y]. Yorumcu: 10 m sonucu girdi verisine bağlı.
- **Grohmann 2013.** Kaba ızgara eğimi düzleştirir ve eğim dağılımını bozar [Ö]. Eğim ızgara boyuyla ters orantılı düşer; fraktal ya da variogram düzeltmesi önerilmiş; eğim uzunluğu ızgara kabalaştıkça yaklaşık doğrusal artar (Guo ve diğerleri 2013, [Ö]).
- **Grieve ve diğerleri 2016 (ESurf Discussions esurf-2016-28).** 20 çözünürlük karşılaştırması: Santa Cruz Adası'nda rölyef yaklaşık 10 m hücreye kadar sabit, sonra artıyor; Gabilan Mesa'da ortalama rölyef en kaba ve en ince çözünürlük arasında yaklaşık 20 m artıyor; eğrilik geniş tepelerde çözünürlükten az etkileniyor [B].
- **Lin ve Oguchi 2004.** 1 m DEM, 88 alt havza, drenaj yoğunluğu ve eğim ilişkisi iki tip [Ö]; eşik alan bilgisi bulunamadı.
- **Nyquist.** f_N = 1/(2 Res) [Ö].
- **Tarboton ve diğerleri 1991 (Hydrol. Proc. 5:81 ile 100).** Ölçek yasalarını sağlayan en yüksek çözünürlüklü ağı seçme ölçütü, 21 ABD DEM'i; örnek eşikler 50 piksel (30 m) ve 20 piksel; kırılma yaklaşık 20 ile 50 piksel arasında (cümle kesik, doğrulanmalı) [B]. Helmlinger ve diğerleri 1993 (WRR 29): drenaj yoğunluğu A_th ve çözünürlüğe güçlü bağlı [Ö]. Montgomery ve Dietrich 1992: kanal başı eşiği A·|∇z|² ve ters alan eğim ilişkisi [Ö]; sayısal A_c değerleri bulunamadı [Y].
- **Perron, Kirchner ve Dietrich 2008, JGR 113 (doi 10.1029/2007JF000866).** Arazi tek fraktal değil [Ö]; özet ve ana sonuçlar okunamadı.
- **Guérin ve diğerleri 2017 (ACM TOG 36(4):228).** Koşullu GAN ile örnek tabanlı arazi sentezi [Ö]. Schott 2024 bu çözünürlük ajanı tarafından bulunamadı; sonradan 17. konuda doğrulandı: Schott ve diğerleri 2024, "Terrain Amplification using Multi-Scale Erosion", ACM TOG 43(4):145 (yalnızca özet okundu). Huftier, Schott ve diğerleri CGF 45 (2026) ayrı bir makale.

**GMBA (Global Mountain Biodiversity Assessment) rölyef ölçütü.** Pürüzlülük: 3×3 = 9 noktada (30 yay saniyesi veri, 2,5 yay dakikası piksel) en büyük yükseklik farkı 200 m'yi aşarsa piksel "engebeli" sayılır [B-öz, gmba.unibe.ch]. Promptumdaki 300 m değeri bu sayfayla uyuşmuyor; Körner ve diğerleri 2011 PDF'i açılamadığı için 1,8 km pencere ve çok pencereli formül doğrulanmadı. Kapsam yüzde 12,3 (511 milyon kişi, GMBA) ile yaklaşık yüzde 22 (1,27 milyar kişi, Kapos ve diğerleri) arasında çelişiyor [Ö].

## 4. Aracın varsayılan değerleri ve tasarım sonuçları

| Konu | Öneri | Dayanak |
|---|---|---|
| Çözünürlük geçişi | önizleme (20 km) ve ana hesap (5 ile 10 km) aynı rölyefi vermez; K, A_c ve D çözünürlükle yeniden ayarlanmalı | [B ve Ö-ölç] |
| K yeniden ölçekleme | m/n = 0,5 ve yalnızca SPIM için K sabit; difüzyonlu durumda ölçekleme bozuluyor | [B] |
| Eşik alan A_c | fiziksel alan (km²) olarak tanımla, hücre sayısı olarak değil; kanal başı alanı çözünürlükten bağımsız seçilsin | [B] |
| Önizleme | niteliksel önizleme (konum, kuşak biçimi); rölyef büyüklüğü için kesin sayı verme | [H] |
| Ana hesap | tek çözünürlük (5 ile 10 km) ve tüm olaylar için aynı | [H] |
| Gerçekçilik ölçümü | gerçek DEM'i 5 ile 10 km'ye kaba tanele (20. konu); rölyef ve eğimi aynı çözünürlükte karşılaştır | [H] |
| Rölyef ölçütü | GMBA 3×3 pencere / 200 m, ya da araç hücresine göre ölçeklenmiş pencere | [B-öz] |
| Zaman adımı ve çözünürlük | dt örtük çözücü için büyük olabilir; yakınsama testi (13. belge) | [H] |

## 5. Kaynaklar arası çelişkiler

- Hergarten (2020) δ^(−2β) ile ölçeklenme, Hergarten ve Pietrek (2023) m/n = 0,5'te δx'ten bağımsız K; difüzyonlu durumda A_h için ayrıca 16 kat; iki yaklaşım uyuşmuyor.
- GMBA eşiği: 200 m (GMBA sayfası) ile 300 m (Alpine Botany 2021 özeti); pencere 3×3 ile yaklaşık 1,8 km ile 6 km yarıçap.
- GMBA kapsamı: yüzde 12,3 ile yüzde 22.
- Benim ilk deneyimde K = 1e−5, m = 0,5 çözünürlükten bağımsız çıktı; K = 1e−7 ile aynı m ve n için rölyef çözünürlükle arttı. Fark, rölyefin ilk durumda kaynak hücre sorunundan ayrı olarak çok küçük kalmasından.

## 6. Bulunamayanlar ve doğrulanamayanlar

- 5, 10, 20, 90 m ve 1 km hücrelerde yerel rölyef oranları; 5 km'den 20 km'ye kaba taneleme etkisi; nehir ağı uzunluğu için kıyı çizgisi benzeri formül; Montgomery ve Dietrich 1992 sayısal A_c; Zhang ve Montgomery sayısal tablo.
- Körner ve diğerleri 2011 tam metni, Grohmann 2007 ve 2013 tam metinleri, Perron 2008, Pelletier spektral, Whipple ve Tucker 1999, Cordonnier 2016 K-alan ilişkisi, Gailleton 2019, Braun ve Willett 2013 ızgara kuralı.
- www.doi.org 403, efi.eng.uci.edu sertifika zinciri güvenilmez, www.geomorphometry.org DNS hatası; atlatılmadı.
- Benim ölçümüm A_c, difüzyon, çok akış ve HEALPix'i kapsamıyor; yalnızca raster, tek akış, düzgün yükselme.
- Tarboton 1997 D∞ drenaj yoğunluğu iddiası doğrulanamadı. (Schott 2024 makalesi 17. konuda bulundu; tam metni okunamadı.)

## 7. Promptumdaki hatalar (düzeltildi)

- "Hergarten 2025, Earth Surface Dynamics" yanlış atıf; 2025 makalesi Kargère ve diğerleri (ESurf 13:403).
- "Körner 2011 GMBA eşik 300 m" doğrulanmadı; GMBA sayfası 200 m diyor.
- "Schott 2024" bu konuda bulunamadı; 17. konuda var olduğu doğrulandı (ACM TOG 43(4):145).
- "Perron 2008 Spectral" ve "Pelletier spektral" ifadeleri karışık; Perron, Kirchner ve Dietrich 2008, JGR 113.

## Başlıca kaynaklar

- Hergarten 2020a: https://esurf.copernicus.org/articles/8/367/2020/
- Hergarten ve Pietrek 2023: https://esurf.copernicus.org/articles/11/741/2023/
- Hergarten 2020b: https://esurf.copernicus.org/articles/8/841/2020/
- Kargère ve diğerleri 2025: https://esurf.copernicus.org/articles/13/403/2025/
- Lague 2014: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf
- Armitage 2019: https://esurf.copernicus.org/articles/7/67/2019/
- Grieve ve diğerleri 2016: esurf-2016-28 (ESurf Discussions)
- GMBA: https://www.gmba.unibe.ch/tools/definitions/mountain_definition/index_eng.html
- Ölçüm betiği: `arastirma/notlar/14/res_test.py`
- Tam liste ve her bilginin kaynağı `arastirma/notlar/14/` içinde.
