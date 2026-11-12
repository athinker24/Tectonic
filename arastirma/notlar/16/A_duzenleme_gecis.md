# A: Kısıt tabanlı arazi düzenleme ve fizik tabanlı üretimle yumuşak geçiş

Durum: DEVAM EDİYOR (ara sürüm; bulgular geldikçe güncelleniyor)
Etiketler: [B] tam metin (PDF'den pdftotext), [B-öz] özet, [Ö] arama özeti, ERİŞİLEMEDİ

## Kaynak uyarısı (önemli)
- "Schott ve diğ. 2023 (fırça tabanlı yükselme ağacı)" ifadesi arXiv 2304.09626 ile eşleştirildiğinde bu makale aslında **StyleDEM** (Perche, Peytavie, Benes, Galin, Guérin; arXiv 2023). Başlık: "StyleDEM: a Versatile Model for Authoring Terrains" (CGF sürümü: "Authoring Terrains with Spatialised Style"). Makalede "yükselme ağacı" kavramı yok. [B] https://arxiv.org/abs/2304.09626
- Schott 2023'ün gerçek karşılığı: "Large-scale Terrain Authoring through Interactive Erosion Simulation", ACM TOG 42 (2023). Yükselme (uplift) alanında çalışır, stream power erozyonu simüle eder, kopyala-yapıştır, kıvrım/fay için warp, nokta ve eğri yükseklik kısıtları sunar. [Ö] https://h-schott.github.io/publications/uplift/publi_uplift.html — tam metin henüz indirilmedi.
- Guérin ve diğ. 2022 "Gradient Terrain Authoring" (CGF): yükseklik yerine gradyan alanında modelleme, fırça ile bölge özellikleri, nokta ve eğri kısıtları; yükseklik Poisson rekonstrüksiyonuyla geri kazanılır. [Ö] https://diglib.eg.org/handle/10.1111/cgf14460
- "Inverse erosion" ve "Schott 2023 PI düzeltme" adları arama sonuçlarında doğrulanamadı: BULUNAMADI (kullanıcı listesinde bu adlarla eşleşen makale bulunamadı; tam başlık/yer verilirse yeniden aranacak).

## Bölüm 1: Kısıt tabanlı arazi düzenleme
- **StyleDEM (Perche ve diğ. 2023)** [B-öz]: GAN (StyleGAN) tabanlı. Girdi bir eskiz veya mevcut arazi, encoder ile W+ gizli uzayına gömülür. Fırça ile düzenleme, stil karıştırma ve süper çözünürlük araçları var. Dizi/yenileme: "Four steps of a typical 5 minutes editing session" (Şekil 13). Kullanıcı çalışması: ≈5 dakikalık oturumlar.
  - Stil karıştırma etkisi: katman i = 5 (güçlü) ile i = 14 (zayıf) arası ayarlanır (Şekil 8).
  - Eğer eğitim ve ağ süresi: 5 m model 35 saat, 30 m model 75 saat (GPU 16 GB). Üretici yürütme: 13 ms (GPU).
  - Ters çevirme (GAN inversion) "up to several minutes per image" (giriş bölümü).
- **Cordonnier 2017** (bkz. Bölüm 4).
- **Schott ve diğ. 2023 (TOG, uplift)** [Ö]: kısıt ve kopyala-yapıştır araçları; tam metin indirilmedi.
- **Guérin ve diğ. 2022** [Ö]: gradyan alanında fırça ve nokta/eğri kısıtları; tam metin indirilmedi.
- **Génevaux 2013, Hnaidi 2010, Zhou 2007, Tasse ve diğ. 2014**: BEKLİYOR (henüz aranmadı/indirilmedi).

## Bölüm 2: Yumuşak geçiş (blending)
- **Pérez, Gangnet, Blake 2003 "Poisson Image Editing"** [Ö]: ACM TOG 22(3), 313-318, DOI 10.1145/1201775.882269. Gradyan alanı tabanlı enterpolasyon; tohumlu kopyalama (seamless cloning), gradyan karıştırma, doku düzleştirme ve kusursuz döşeme. Ücretsiz kopya: https://www.cs.princeton.edu/courses/archive/fall14/cos526/papers/perez03.pdf — tam metin henüz çıkarılmadı.
- **StyleDEM blend** [B-öz]: iki farklı stilize arazi, alfa maskesiyle yükseklik alanında (altitude domain) fırçayla karıştırılır (Şekil 7). Ayrıca latent uzayda doğrusal enterpolasyon: w = (1 − α) u + α v; α değişince arazi bir hedeften diğerine morfolur (Şekil 10). Makale, doğrudan yükseklik enterpolasyonuna karşı bu yöntemin avantajını vurgular.
- Laplace piramidi, mesafe tabanlı feathering: BEKLİYOR.

## Bölüm 3: Kısıtlı en iyileştirme ve ters erozyon
- "Inverse procedural modeling": BEKLİYOR.
- Ters erozyon (inverse erosion): BULUNAMADI (ad doğrulanamadı; yakın konu Schott 2023 TOG'dur).

## Bölüm 4: Hesap süresi ve ölçeklenebilirlik
- **Cordonnier ve diğ. 2017, ACM TOG 36(4), art. 134, DOI 10.1145/3072959.3073667** [B]. Kaynak: https://cs.purdue.edu/homes/bbenes/papers/Cordonnier17ToG.pdf (yerel: scratchpad/dl/cordonnier2017/paper.pdf). Bidirectional erozyon-bitki geri beslemesi; fırçalarla katman düzenleme (bölüm 3.3, "Layered data can be locally edited using interactive brushes").
  - Hücre boyutu 10×10 m; "up to 10×10 km² at interactive rates" (bölüm 7).
  - Tablo 1 [B] (ortalama, saniye/simülasyon adımı Δt, n = ızgara genişliği):
    | Olay | n=128 | n=256 | n=512 | n=1024 |
    |---|---|---|---|---|
    | Yağmur | 0.0695 | 0.43 | 3.92 | 36.5 |
    | Toplam | 0.11 | 0.59 | 4.77 | 38 |
  - "interactive control during a 15 minute editing session" (bölüm 7).
  - Simülasyon adımlarında süre sınırı: "Terminate in bounded simulation time δt" (kural 1); kullanıcı düzenlemesi "self-correct after a few simulation time steps".
- StyleDEM süre özeti: 13 ms üretim (GPU), 5 dk düzenleme oturumu; 30 m modelin eğitimi 75 saat.
- Hesap süresi karşılaştırması için tek bir ortak ölçüt yok; yukarıdaki değerler farklı donanım ve ölçeklerde, doğrudan kıyaslanamaz.

## Bulgular (özet)
1. Kullanıcının kaynak listesindeki "Schott 2023 fırça tabanlı yükselme ağacı" makalesi bulunamadı; arXiv 2304.09626 StyleDEM'dir.
2. Fırça tabanlı, kısıt destekli düzenleme için en yakın yakın konular: StyleDEM (GAN, fırça, stil), Guérin 2022 (gradyan alanı, fırça), Schott 2023 TOG (uplift, kısıt).
3. Yumuşak geçiş için yükseklik alanında alfa-maskeli karıştırma (StyleDEM) ve gradyan/Poisson karıştırma (Pérez 2003) iki ana seçenek.
4. Erozyon simülasyonunda adım başı süre 10×10 m ızgarada n=512'de ≈4.8 s, n=1024'te ≈38 s (Cordonnier 2017, Tablo 1).

## Açık işler
- Schott 2023 TOG, Guérin 2022, Pérez 2003 tam metinleri indirilip doğrulanacak.
- Génevaux 2013, Hnaidi 2010, Zhou 2007, Tasse 2014, "Inverse procedural modeling" aranacak.
- Laplace piramidi ve feathering için kaynak bulunacak.

## Erişilemeyen kaynaklar
- Yok (şu ana kadar).
