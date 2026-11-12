# A: Kısıt tabanlı arazi düzenleme ve fizik tabanlı üretimle yumuşak geçiş

Durum: BÜYÜK ÖLÇÜDE TAMAM (kalan açıklar aşağıda)
Etiketler: [B] tam metin (PDF, pdftotext ile okundu), [B-öz] tam metinden özet, [Ö] yalnız arama özeti, ERİŞİLEMEDİ

## Kaynak uyarıları
- **Schott 2023 doğrulandı (düzeltme):** Makalenin tam metni (HAL önbaskı hal-04049125, ACM TOG 2023) "Uplift Tree" (yükselme ağacı), "Procedural Brushes" (fırça), "Interactive Blend", "Correction control" ve "Inverse procedural modeling" bölümleri içeriyor. Kullanıcının tarifi bu makaleyle örtüşüyor. [B] https://hal.science/hal-04049125v1
- **arXiv 2304.09626 Schott ile karıştırılmamalı:** Bu numara StyleDEM (Perche, Peytavie, Benes, Galin, Guérin, 2023) makalesine ait; "yükselme ağacı" içermiyor. [B] https://arxiv.org/abs/2304.09626
- **Schott 2023 sayfası:** h-schott.github.io için WebFetch DNS hatası verdi (ENOTFOUND); curl ile sayfa 404 döndü. Alternatif sayfa (aparis69.github.io) özeti verdi. Yine de tam metin HAL'dan okundu.
- **Tasse 2014 (Computers & Graphics 45, 101-115):** core.ac.uk PDF'i Cloudflare bot koruması ("Just a moment...") döndürdü. Bot korumasını aşmadım. Bilgi yalnızca arama özetinden: **ERİŞİLEMEDİ (tam metin)**, [Ö].
- **"Inverse erosion" (Cordonnier) ve "Schott 2023 PI düzeltme" adları:** "Inverse erosion" tek başına bir makale olarak BULUNAMADI. Schott 2023'te PI düzeltme **var** (aşağıda, denklem 10); "inverse erosion" yerine ilgili konular: Unerosion (Yang ve diğ. 2024, CGF) [Ö] ve ters erozyon modelleme (Petit ve diğ., adjoint) [Ö].

## Bölüm 1: Kısıt tabanlı arazi düzenleme

### Schott, Paris, Fournier, Guérin, Galin 2023 — "Large-scale terrain authoring through interactive erosion simulation" (ACM TOG 42) [B]
- Arazi yükseklik değil **yükselme (uplift)** alanında tanımlanır: u = u0 + ũ.
  - u0: statik kısım, Uplift Tree (hiyerarşik vektör tabanlı yapı) veya fırçalarla (brushes) üretilir.
  - ũ: dinamik düzeltme terimi; kesin yükseklik kısıtlarını (sparse elevation constraints) sağlar.
- Kullanıcı işlemleri: kopyala-yapıştır, kıvrım/fay için warp, nokta ve eğri yükseklik kısıtları, fırça, enterpolasyon.
- Yükselme alanında enterpolasyon ve warp "hidrolojik tutarlılığı" korur (bölüm 5.2): yükseklik üzerinde karıştırma "unrealistic results" üretir.
- Özet [B-öz]: "We set aside modeling in the elevation domain in favour of the uplift domain and compute emerging reliefs by simulating the stream power erosion."
- Kullanıcının "dağ sırası" isteği: bu makalede Uplift Tree ile dağ sıraları ve vadiler kontrol edilir (bölüm 5, 7).
- **PI düzeltme (denklem 10, bölüm 6.4)** [B]:
  - ũ(k+1) = Kp·e(k) + Ki·Σ_{j=0..k} e(j) + Kd·(e(k) − e(k−1)), e(k) = h0 − h(k, q), h0 = hedef yükseklik.
  - Kazançlar: Kp = 0.01, Kd = 0.01, Ki = 0.001; güncelleme her 10 iterasyonda.
  - Yazar not: "controlling the altitude of specific points ... remains difficult" (non-lineerlik nedeniyle). Yani belirli bir noktanın yüksekliği ancak geri besleme ile ayarlanır.
- Ters prosedürel modelleme (bölüm 5, 7): Uplift Tree, bir DEM'den çıkarılan sırt ve nehir ağlarından (Argudo ve diğ. 2019) üretilebilir. Eksik bilgi: "The only information needed ... is the compact Uplift Tree."
- Kullanıcı süresi: "completed in less than 10 minutes by an experienced user" (bölüm 7).

### Guérin, Peytavie, Masnou, Digne, Sauvage, Gain, Galin 2022 — "Gradient Terrain Authoring" (CGF 41(2), 85-95) [B]
- Modelleme gradyan alanında yapılır; yükseklik Poisson rekonstrüksiyonuyla geri kazanılır.
- Kısıtlar: yükseklik kısıtı Dirichlet koşuluyla gradyan alanının içine girer.
- **Çakışma kuralı [B]:** "This approach has the benefit of enforcing hard elevation constraints over soft gradient constraints if there is a conflict between the two forms."
  - Bu, kullanıcının "belirli yükseklik" isteği için doğrudan yararlı: sert kısıt, yumuşak gradyan kısıtından önce gelir.
- Araçlar [B]: kopyala-yapıştır (warp destekli), fırça (bölge özelliklerini değiştirme: düzleştirme, pürüzlendirme, hizalama), nokta/eğri kısıtları.
- Süre [B]: "constrained reconstruction is GPU optimized and executes in real-time"; "real-time updates for terrain resolutions up to 1024 × 1024".
- Not: aynı makale, örnek tabanlı rakip yöntemlerin "pre-processing step that can take several minutes" süresi olduğunu belirtiyor (rakip yöntemler için karşılaştırma, kendi yöntemi için değil).

### StyleDEM: Perche, Peytavie, Benes, Galin, Guérin 2023 (arXiv 2304.09626; CGF "Authoring Terrains with Spatialised Style") [B-öz]
- GAN tabanlı (StyleGAN). Girdi eskiz veya mevcut arazi, encoder W+ uzayına gömer.
- Fırça ile yükseklik ve stil düzenleme; stil karıştırma (katman i = 5 güçlü, 14 zayıf etki, Şekil 8).
- Süre: "Four steps of a typical 5 minutes editing session"; üretim 13 ms (GPU); GAN inversion "up to several minutes per image"; eğitim 5 m model 35 saat, 30 m model 75 saat (16 GB GPU).
- Kullanıcı süresi: "after a ≈5 minutes editing session only" (eşleşme Şekil 14).

### Hnaidi, Guérin, Akkouche, Peytavie, Galin 2010 — "Feature based terrain generation using diffusion equation" (CGF 29(7), 2179-2186) [B]
- Eğriler (sırt, nehir yatağı, uçurum) üzerinde parametrik kısıtlar: yükseklik, eğim, pürüzlülük; kısıtlar iki uç noktada ve aralarında doğrusal enterpolasyonla tanımlanır.
- Kısıtlar rasterleştirilip çok ızgaralı (multigrid) difüzyonla yayılır. Ayrıntı gürültü ile eklenir.
- GPU'da etkileşimli çalışır (özet). Makalede saniye düzeyinde süre değeri bulunamadı: **süre BULUNAMADI (metinde açık değer yok)**.

### Génevaux, Galin, Guérin, Peytavie, Benes 2013 — "Terrain generation using procedural models based on hydrology" (ACM TOG 32(4), 143) [B-öz]
- Basit bir eskizden hidroloji kavramlarıyla arazi; hiyerarşik drenaj ağı ile nehir ağı tutarlı. Tam metin indirildi, ayrıntılı okuma tamamlanmadı.
- Kısıt tabanlı düzenleme bağlamında: kontrol edilebilirlik düşük olan yöntemlere alternatif (özet).

### Zhou, Sun, Turk, Rehg 2007 — "Terrain Synthesis from Digital Elevation Models" (IEEE TVCG 13(4), 834-848) [Ö]
- Örnek tabanlı: örnek DEM yamaları, kullanıcı çizimli özellik haritasına göre yerleştirilir; graph cut ve Poisson düzenleme ile birleştirilir; yerleştirme sırası özellik ağacında genişlik öncelikli (BFS) geçişle belirlenir. Tam metin indirilmedi.

### Tasse, Emilien, Cani, Hahmann, Dodgson 2014 — "Feature-based terrain editing from complex sketches" (Computers & Graphics 45, 101-115) [Ö]
- Birinci şahıs eskizine göre mevcut arazinin deformasyonu; siluetler ve sırtlar eşleştirilir; çok görünümlü genişleme.
- **ERİŞİLEMEDİ (tam metin):** core.ac.uk Cloudflare bot koruması.

### Cordonnier, Galin, Gain, Benes, Guérin, Peytavie, Cani 2017 — "Authoring landscapes by combining ecosystem and terrain erosion simulation" (ACM TOG 36(4), 134) [B]
- Bitki ve erozyon simülasyonu arasında iki yönlü geri besleme; fırçalarla katman düzenleme ("Layered data can be locally edited using interactive brushes").
- Kullanıcı oturumu: "interactive control during a 15 minute editing session".
- Kaynak: https://cs.purdue.edu/homes/bbenes/papers/Cordonnier17ToG.pdf

### Emilien, Vimont, Cani, Poulin, Benes 2015 — WorldBrush (ACM TOG) [B, kısmi]
- Örnek tabanlı, eğime bağlı dağılımlar (ağaç, çimen, kaya). Tam metin indirildi; yalnızca şekil yazısı okundu: kısıt "constrained by the terrain's slope". Ayrıntı okunmadı.

## Bölüm 2: Yumuşak geçiş (blending)

### Pérez, Gangnet, Blake 2003 — "Poisson Image Editing" (ACM TOG 22(3), 313-318) [B-öz]
- Kılavuz vektör alanı v ile Dirichlet koşullu Poisson denklemi: kaynak gradyanı hedef sınırına bağlanır. Denklem (özet): Δf = div v içte, f = f* sınırda. Sıfır sağ taraflı durumda Laplace denklemine iner ("amounts to solving a Laplace equation").
- Gradyan karıştırma: gradyan bölgede maksimum/karıştırma işlemiyle seçilir (makale: "to include maximum operations").
- Laplace piramidi: Pérez, sınır etkisini hızlandırmak için çok çözünürlüklü (Laplacian pyramid) yaklaşım kullanır; ayrıca tam Poisson çözümüyle karşılaştırır (makale bölüm 3.1).
- Kopya: https://www.cs.princeton.edu/courses/archive/fall14/cos526/papers/perez03.pdf
- Not: denklem gösterimi pdftotext ile bozulduğu için sembolik ayrıntı yalnızca metin özetinden alındı.

### StyleDEM blend [B-öz]
- Alfa maskesi (fırça ile) iki stilize arazi arasında yükseklik alanında karıştırır (Şekil 7).
- Latent uzayda doğrusal enterpolasyon: w = (1 − α)·u + α·v; α değişince arazi bir hedeften diğerine morfoloj yapar (Şekil 10). Makale bunu doğrudan yükseklik enterpolasyonuna karşı önerir.

### Schott 2023 blend [B]
- Yükselme alanında "hydrologically consistent blending between terrain patches" (giriş); yükselme alanında enterpolasyon ve warp, yükseklik enterpolasyonuna göre hidrolojik tutarlılığı korur (bölüm 5.2).

### Guérin 2022 blend [B]
- Gradyan alanında "seamless blending of disparate landforms" (giriş): yükseklik değil gradyan alanı karıştırılır; yükseklik Poisson ile geri elde edilir.

### Laplace piramidi, mesafe tabanlı feathering
- Laplace piramidi: Pérez 2003 üzerinden doğrulandı (hızlandırma yolu). Ayrı bir feathering kaynağı BULUNAMADI (ek arama yapılmadı).

## Bölüm 3: Kısıtlı en iyileştirme ve ters erozyon

### Inverse procedural modeling
- **Talton ve diğ. 2011 "Metropolis Procedural Modeling" (TOG 30(2))** [Ö]: Reversible Jump MCMC ile prosedürel model parametrelerinin kısıtlara uydurulması. Makalenin örnekleri ağaç, şehir, bina; **terrain sonucu BULUNAMADI** (arama özetine göre).
- Schott 2023 [B]: Uplift Tree'nin DEM'den (Argudo ve diğ. 2019) kurulması; "inverse procedural modeling" bölümü (5, 7.1). Eksik bilgi hâlâ sadece Uplift Tree'dir.
- WorldBrush (Emilien 2015) [B kısmi]: örnek tabanlı istatistik, "inverse procedural modeling" yaklaşımlarının bir örneği olarak anılır (Talton 2011 ile birlikte).

### Ters erozyon
- Schott 2023 PI düzeltme: denklem 10 (bkz. Bölüm 1). Erozyon denklemi ters çözülmez; hedef yükseklik için u düzeltilir.
- Adjoint tabanlı ters modelleme (Petit ve diğ., 2025, ESurf 13) [Ö]: jeomorfoloji, sertleşme ve parametre hassasiyeti.
- Unerosion (Yang ve diğ. 2024, CGF) [Ö]: arazi evrimini geriye doğru simüle eder.
- Wasserstein mesafesiyle ters modelleme (Morris ve diğ. 2023, GRL) [Ö].
- "Cordonnier inverse erosion" adıyla bir makale BULUNAMADI.

## Bölüm 4: Hesap süresi ve ölçeklenebilirlik

### Schott 2023 — Tablo 1 [B]
Ortalama adım süresi t_s (ms) ve toplam yakınsama süresi t_c (s); sabit tekdüze uplift, GPU (GTX 1080 Ti, makale bölüm 7):

| Izgara | Adım sayısı | t_s (ms) | t_c (s) |
|---|---|---|---|
| 256 | 5k | 0.1 | 0.5 |
| 512 | 5k | 0.3 | 1.3 |
| 1024 | 11k | 0.8 | 9.1 |
| 2048 | 39k | 3.3 | 128 |
| 4096 | 81k | 12.5 | 1036 |

- Karşılaştırma (makale): 400×400 grid, Cordonnier 2016 yöntemi ≈200 adım, adım başı 1.3 s, toplam 252 s; Schott ≈5000 adım, 512×512 grid, 1.3 s toplam. Yazarlar "up to two orders of magnitude faster" der.
- Hedef ölçek (giriş [B]): "large-scale terrains ranging from 100×100 km² to 1000×1000 km²".
- Kullanıcı deneyimi: "completed in less than 10 minutes by an experienced user" (bölüm 7).

### Cordonnier 2017 — Tablo 1 [B]
Ortalama adım süresi, saniye/adım Δt, ızgara genişliği n:

| Olay | n=128 | n=256 | n=512 | n=1024 |
|---|---|---|---|---|
| Yağmur | 0.0695 | 0.43 | 3.92 | 36.5 |
| Toplam | 0.11 | 0.59 | 4.77 | 38 |

- Hücre 10×10 m; "up to 10×10 km² at interactive rates" (bölüm 7); 15 dk düzenleme oturumu.
- Donanım bu incelemede doğrulanmadı.

### StyleDEM [B-öz]
- Üretici çalıştırma 13 ms (GPU); düzenleme oturumu ≈5 dk; GAN inversion "several minutes per image"; eğitim 35-75 saat.

### Guérin 2022 [B]
- Gerçek zamanlı kısıtlı yeniden yapılandırma, 1024×1024 çözünürlüğe kadar.

### Hnaidi 2010 [B]
- GPU'da etkileşimli; saniye değeri BULUNAMADI.

### Karşılaştırma notu
- Üç makalenin süre ölçütleri farklı ızgara boyutları, donanımlar ve birimlerle (Schott ms/adım ve s toplam; Cordonnier s/adım; StyleDEM ms üretim) verildiği için doğrudan kıyaslanamaz. Bu notta değerler yalnızca kendi makalelerinin verdiği biçimde listelenmiştir.

## Bulgular (özet)
1. **Schott 2023** (Uplift Tree, fırça, PI kısıtı, ms/adım tablosu) kullanıcının tarif ettiği yöntemin en yakın karşılığı. Kaynak doğrulandı, arXiv 2304.09626 yanlış eşleşmeydi (StyleDEM).
2. **Sert kısıt önceliği** (Guérin 2022): çakışan yükseklik ve gradyan kısıtlarında sert yükseklik kısıtı kazanır. Belirli bir yerde belirli yükseklik için bu kural doğrudan kullanılabilir.
3. **Yumuşak geçiş için iki temel yol:** (a) yükselme (uplift) alanında enterpolasyon/warp (Schott 2023; hidrolojik tutarlılığı korur), (b) gradyan alanında Poisson karıştırma (Pérez 2003; Guérin 2022). Yükseklik alanında doğrudan karıştırma, Schott ve Guérin'e göre gerçekçi olmayan sonuçlar verebilir.
4. **Kısıtlı düzeltme (PI):** Schott denklem 10 ile yükseklik hedefine ulaşmak için geri besleme kullanır: Kp = 0.01, Ki = 0.001, Kd = 0.01, her 10 iterasyonda bir güncelleme.
5. **Süre:** Schott 512×512 grid için toplam 1.3 s; 1024×1024 için 9.1 s (Tablo 1). Cordonnier 1024 için 38 s (adım başı, yağmur dahil). Guérin 2022 1024×1024 çözünürlükte gerçek zamanlı.
6. **Ters prosedürel modelleme:** Schott Uplift Tree üzerinden; Talton 2011 terrain için değil.

## Erişilemeyen veya eksik kaynaklar
- **ERİŞİLEMEDİ:** Tasse 2014 tam metin (core.ac.uk, bot koruması).
- **Adı doğrulanamadı:** "Cordonnier inverse erosion"; "Schott 2023 brush-based elevation tree" adı tam olarak (Uplift Tree ile) eşleşti, ancak "brush-based" ibaresi arXiv numarasıyla karıştı.
- **Eksik:** Génevaux 2013 ve Zhou 2007'nin ayrıntılı okuması; Laplace piramidi/feathering için ayrı kaynak; Hnaidi 2010 için saniye düzeyinde süre.
- **Açık iş:** Guérin 2022 ve Schott 2023 karşılaştırmalı süre tablosu için aynı donanımda ölçüm yok.
