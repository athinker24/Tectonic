# 12. Tektonik olaylardan yükselme haritasına

Araştırma tarihi: 12 Kasım 2026. Belge üç Haiku kolunun sentezidir (A bilgisayar grafiğinde yükselme haritasından arazi üretimi, B yakınsamadan yükselmeye fiziksel yollar, C goSPL ve levha zorlaması); sentezi ben yazdım. Ham notlar `arastirma/notlar/12/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** yalnızca özet okundu, **[D]** resmi belgelendirme okundu, **[Ö]** arama özeti, doğrulanamadı, **[H]** bizim çıkarımımız, **[Y]** bulunamadı.

Dürüst durum: bu konunun en önemli boşluğu şu ki, kuşak genişliği ve yükselme hızı için tam metinden kaynaklı sayı çıkmadı (B kolu); yalnızca denklemler ve boyutsuz sayılar var. Bu belge bu yüzden aracın girdi biçimini ve denklemlerini verir, bu sayıları ise 2. ve 4. belgedeki değerlerle tamamlamak gerekir.

## Kısa sonuç

**1. Bilgisayar grafiğinin yükselme tabanlı arazi modeli kısa ve kullanılabilir.** Cordonnier ve diğerleri (2016): girdi gri tonlamalı yükselme haritası; denklem dh/dt = u − k A^m s^n, n = 1, m = 0,5; hızlı, 6,4 ile 252 s [B]. Schott ve diğerleri (2023): ∂h/∂t = u − s^n a^m + Δh, m/n yaklaşık 1/2; fırça tabanlı yükselme düzenleme [B]. Bu, aracın "olaydan yükselme haritasına" katmanının çıktı biçimi olarak uygun.

**2. Fiziksel kısa yol: kritik kama veya ince viskoz levha, ikisi de doğrulanmış sayı vermedi.** Argand sayısı Ar = g ρc L (1 − ρc/ρm) / (B ε̇0^n) (bir tezden, üsler kontrol edilmeli); Tibet için n = 2 ile 5 ve Ar = 1 ile 4 en iyi uyum, plato Tien Shan ve önlüğünden 3 ile 8 kat zayıf [B, tez atfı]. Bu, 2. belgedeki "uzak alan 1500 ile 2500 km" kuralı için fiziksel gerekçe sağlıyor, ama doğrudan bir yükselme hızı değil.

**3. goSPL levha hareketini zorlama olarak alıyor, ama ücretsiz Actions ortamına sığmıyor.** `upsub` düşey yükselme ve `hdisp` 3B yatay hız, m/yıl, `.npz` dosyasından [D]. Belgelenmiş küresel ağlar 5,9 milyon düğümden başlıyor ve en az 16 MPI rank gerektiriyor [D]. Bu çıkarım benim: 2 ile 4 çekirdek ve 16 GB bu ağları başlatamaz [H].

**4. Bu araç için yükselme haritası olay tabanlı üretilmeli, simülasyonla değil.** Bu bir tasarım önerisi; kanıtı yok, ama Schott ve diğerlerinin "Uplift Tree" fikriyle (fırça tabanlı yükselme bileşimi) örtüşüyor [H].

## 1. Yükselme haritasından arazi: bilgisayar grafiği

| Makale | Girdi | Model ve değerler | Çözünürlük ve süre | Etiket |
|---|---|---|---|---|
| Cordonnier ve diğerleri 2016, CGF 35(2) | gri tonlamalı yükselme haritası | dh/dt = u − k A^m s^n, n = 1, m = 0,5; 50×50 km² alan, U = 5,0e−4 m/yıl, k = 5,61e−7 1/yıl, δt = 2,5e5 yıl; tepe yüksekliği hmax = 2,244 u/k (km; birim doğrulanmadı) | vektör gösterim, 10 000 ile 160 000 örnek; 6,4 ile 252 s yakınsama (i7 3 GHz) | [B]; açık kod beyanı yok |
| Schott ve diğerleri 2023, ACM TOG 42(5) | fırça tabanlı yükselme ağacı + PI düzeltme: u = u0 + ũ | ∂h/∂t = u − s^n a^m + Δh, m/n yaklaşık 1/2; drenaj alanı yaklaşımı paralelleştirilebilir | 80 ile 600 m hücre; 512² ızgara için 1,3 s (GTX 1080 Ti); tortu yok, 1024²'nin üstünde yakınsama yavaşlar | [B, HAL ön baskı]; kod github.com/H-Schott/StreamPowerErosion (makaleye göre; oturumda erişilemedi) |
| Guérin ve diğerleri 2022, CGF 41(2) "Gradient Terrain Authoring" | eğim alanı | Poisson yeniden yapılandırma, GPU multigrid | 513² için 27 ms, 8193² için 7,67 s | [B]; kod beyanı var, açılmadı |
| Génevaux ve diğerleri 2013, ACM TOG 32(4) | kontur, nehir kroki, eğim haritası | hidroloji kuralları (Horton-Strahler, Rosgen); yükselme/aşınma PDE'si yok | 3368 km² adada toplam yaklaşık 12 s; delta ve menderes yok, yapay tepe sorunu | [B] |
| Cortial ve diğerleri 2019, CGF 38(2) "Procedural Tectonic Planets" | levha tabanlı, yükselme haritası değil | | | [B-öz]; tam metin giriş istiyor, denklem ve sayı doğrulanamadı |
| Tzathas ve diğerleri 2024, CGF 43(2) "Physically-based Analytical Erosion for fast Terrain Generation" | | | | [Ö]; tam metin giriş istiyor |

Düzeltme: promptumdaki "Orometry-based terrain analysis" Argudo 2019'a ait, Tzathas'a değil; "orogenic sketching" başlığı bulunamadı. Guérin ve diğerleri (2022) STAR "Procedural terrain" olarak bulunamadı; yakın olan 2019 STAR Galin ve diğerleri "A Review of Digital Terrain Modeling" (CGF 38(2)) [Ö].

## 2. Yakınsamadan yükselmeye: fiziksel yollar

- **İnce viskoz levha (England ve McKenzie 1982; Houseman ve England 1986).** Argand sayısı Ar = g ρc L (1 − ρc/ρm) / (B ε̇0^n) (Garthwaite 2011 tezi, Eşitlik 5.24; üsler kontrol edilmeli) [B]. Tibet için en iyi uyum n = 2 ile 5, Ar = 1 ile 4; plato Tien Shan ve önlük bölgelerinden 3 ile 8 kat zayıf [B]. Gerinim hızı aralığı 1e−13 ile 1e−17 1/s [B]. Deformasyon bozunma uzunluğu yaklaşık (1/n)^0,5 × sınır dalga boyu [B, tez atfı]; kıtasal modeller için n çoğunlukla yaklaşık 3 [Ö]. Orijinal makalelerin tam metni ücretli, özet düzeyinde kaldı.
- **Airy dengesi.** d_v = d_t ρc / (ρm − ρc); MIT örneği: 5 km topografya yaklaşık 28 km kök, toplam yaklaşık 33 km kabuk farkı [B, MIT OCW]. Bu, 2. belgede düzeltilen doğru hesapla uyumlu (toplam kalınlaşma = h + r).
- **Kısalma kalınlaşma ilişkisi.** h1 = h0 / (1 − S) türetmesi kaynaksız [H]; kontrol edilmeli.
- **Kararlı hal aşınma ve yükselme.** U = K ka^m P^m x^(hm) (dz/dx)^n (Roe ve Brandon el yazması, Eşitlik 6, [B]). Willett'in aşınma sayısı Ne = kL/u [B-öz].
- **Kritik kama.** Davis, Suppe ve Dahlen (1983): μ = 1,03 (Batı Tayvan) [Ö]; kritik eğim = yüzey eğimi + taban eğimi (Dahlen 1990 özeti, [Ö]). Whipple ve Meade (2004) kama-aşınma bağlaşımı ve Willett (1999) için tam metin alınamadı. "Doubly vergent critical orogens" başlıklı Willett 1999 makalesi bulunamadı; büyük olasılıkla "Orogeny and orography" (JGR 104, doi 10.1029/1999JB900248) [Y].
- **Sayısal geodinamik kodlar.** ASPECT, Underworld, I2ELVIS/I3ELVIS, SOPALE: dört kodlu dalma karşılaştırması ve hesap maliyetleri bulunamadı [Y]; "I2VIS" adına kaynak yok, büyük olasılıkla I2ELVIS.

## 3. goSPL ve benzer araçlarda levha zorlaması

- **Girdi biçimi [D]:** `tectonics:` olayları: start/end (yıl), `upsub` (yalnızca düşey) ya da `hdisp` (3B yatay hız), m/yıl. Düşey: `upsub: ['data/uplift20Ma','t']`, düğüm başına 1B vektör. Yatay: `hdisp: ['data/hdisp18Ma','hxyz']`, 3B dizi, 2B ağda z = 0. Tüm girdi dosyaları `.npz`; netCDF/HDF5 girdi değil, çıktı HDF5 + XDMF.
- **Zaman [D]:** start, end, dt (örtük adım), tout, strat, rstep (yıl). Yatay yer değiştirme için seçenekler: upwind, iioe1, iioe2, interp.
- **`interp` seçeneği (küresel levha hareketi) [D]:** yatay yer değiştirme yalnızca olay sonunda uygulanır, düşey yer değiştirme her dt'de; olay süresi tipik birkaç bin ile milyon yıl. Yeniden ağ üretimi yok; sabit ağa ters uzaklık ara değerlemesi (en yakın 3 nokta, cKDTree); belgeler "en doğru olmayabilir" diyor. upwind ve iioe 2B için tasarlanmış, küresel yüzey için doğrulanmamış. Stratigrafi her adımda yarı-Lagrange ile taşınır, kütle korunmaz, 1 milyon düğümde yaklaşık yüzde 3 ek süre.
- **GPlates bağlantısı [D]:** "Horizontal advection often corresponds to plate motions and can be obtained from plate-tectonic reconstruction software"; GPlates/pyGPlates adı belgede geçmiyor. Örnek depo `plate_mvt` ("global landscape evolution driven by horizontal plate motion ... together with vertical tectonics") dosyaları okunamadı. gospl-pygplates örneği bulunamadı [Y].
- **HPC ölçeği [D] (hpc_scaling):**

| Ağ | Düğüm | En az MPI rank | Bellek | Süre |
|---|---|---|---|---|
| 10 km | 5,9 milyon | 16 | yaklaşık 6,6 GB/rank | 16 rank 521 s; 240 rank 46,9 s (verim 0,74) |
| 8 km | 9,2 milyon | 24 | yaklaşık 9,9 GB/rank | |
| 5 km | 23,7 milyon | 96 | rank 0'da yaklaşık 24 GB; 48 rank tek 192 GB düğümde bellek yetersiz | |

- **Yayınlar.** Salles ve diğerleri 2023, Nature 624:115: 10 milyon düğümün üstü, 21 milyon hücre, yaklaşık 5 km; dilim başına 168 CPU; 2 milyon yıl ön simülasyon [B]; süre ve bellek raporlanmamış. Salles ve diğerleri 2024, Nat. Commun. 15:3430 (Sahul): yaklaşık 1 km bölgesel, 80 CPU, 75'ten 35 bin yıla [B]. Salles ve diğerleri 2023, Science 379:918: yaklaşık 10 km, 1 milyon yıl kareleri, "birkaç yüz işlemci", simülasyon başına "birkaç gün" [Ö]; tam metin erişilemedi. Promptumdaki "Salles 2023 Earth system" ve "2024 paleo-erosion" başlıkları yanlıştı; gospl yazılım makalesi 2020 JOSS (2023 Computers & Geosciences bulunamadı).
- **Lisans ve kurulum.** goSPL GPLv3, sürüm 2026.7.14; kurulum `mamba create -n gospl -c geodels -c conda-forge gospl`; paralel HDF5 ve h5py gerekli [D ve B].
- **Badlands ve PECUBE.** Badlands LGPL v3, Python, bölgesel TIN, girdi XML (`<tectonic>`, `<disp3d>`, ASCII/CSV), 3B yatay yer değiştirmede düğüm yeniden üretimi var [D]. PECUBE (Braun 2012, Tectonophysics) 3B termo-kinematik sonlu eleman kodu, termokronoloji odaklı, yükselme yüzey evrimden ayrı [B-öz]; lisansı bulunamadı. Fark: goSPL küresel ve sediment yönlendirmeli; Badlands bölgesel; PECUBE termokronoloji odaklı.

## 4. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Yükselme girdisi | yükselme haritası (m/yıl), olay tabanlı fırça bileşimi | [B ve H] |
| Akarsu güç yasası | n = 1, m = 0,5 (m/n yaklaşık 0,5) | [B] |
| K ve U örnek aralığı | k = 5,61e−7 1/yıl, U = 5e−4 m/yıl (Cordonnier) | [B] |
| Argand sayısı aralığı | Ar = 1 ile 4, n = 2 ile 5 (Tibet en iyi uyum) | [B] |
| Plato / önlük zayıflık oranı | 3 ile 8 | [B] |
| Airy toplam kalınlaşma | topografya h için yaklaşık 0,15 oranı (2. belge) | [B] |
| Zorlama biçimi | düşey: her adımda; yatay: olay sonunda (goSPL `interp` mantığı) | [D] |
| Ağ boyutu (Actions) | 10 km küresel ağ başlatılamaz (16 rank gerekir); alt ağ ve kaba ızgara ayrı tasarlanmalı | [D ve H] |
| Yatay yer değiştirme ara değerlemesi | ters uzaklık (en yakın 3 nokta) yerine alan korunumlu yöntem aranmalı | [D ve H] |

## 5. Kaynaklar arası çelişkiler

- Willett 1999: "Doubly vergent critical orogens" (promptumdaki başlık) bulunamadı; "Orogeny and orography" olabilir.
- Cortial 2019 ve Tzathas 2024 sayıları doğrulanamadı; aynı açık ortamda tam metin giriş istedi.
- goSPL örnekleri: Salles (2023, Science) "birkaç yüz işlemci" ile Nature 2023 "dilim başına 168 CPU" tutarlı, ama ilki yalnızca özet.

## 6. Bulunamayanlar ve doğrulanamayanlar

- Tam metinden kaynaklı yükselme hızı (mm/yıl) ve kuşak genişliği (km) değeri bulunamadı; 2. ve 4. belgedeki değerler kullanılacak.
- England ve McKenzie 1982, Houseman ve England 1986, Davis 1983, Whipple ve Meade 2004, Dahlen 1990 tam metinleri (ücretli ya da TLS hatası, atlatılmadı).
- Cortial 2019 ve Tzathas 2024 tam metinleri; Cordonnier 2016 açık kodu.
- goSPL `plate_mvt` dosyaları, gospl-pygplates örneği, Science 2023 tam metni, Nature 2023 süre ve bellek ek verisi, PECUBE lisansı; GitHub depoları oturumda erişilemedi, add_repo çağrılmadı.
- Dört kodlu geodinamik karşılaştırma ve hesap maliyetleri.
- Kısalma kalınlaşma bağıntısı h1 = h0/(1 − S) kaynaksız.

## 7. Promptumdaki hatalar (düzeltildi)

- "Salles 2023 Earth system" ve "2024 paleo-erosion" başlıkları yanlıştı; gerçek yayınlar: Nature 624:115, Nat. Commun. 15:3430 (Sahul), Science 379:918.
- "Tzathas 2024: orogenic sketching" yanlış; Tzathas 2024 "Physically-based Analytical Erosion for fast Terrain Generation".
- "Orometry-based terrain analysis" Argudo 2019'a aittir.
- "Guérin 2022 STAR Procedural terrain" bulunamadı; 2019 STAR Galin ve diğerleri var.
- "I2VIS" adı muhtemelen I2ELVIS.
- "Doubly vergent critical orogens" Willett 1999 başlığı doğrulanamadı.

## Başlıca kaynaklar

- Cordonnier ve diğerleri 2016, Computer Graphics Forum 35(2) (Large Scale Terrain Generation from Tectonic Uplift and Fluvial Erosion)
- Schott ve diğerleri 2023, ACM TOG 42(5): ham notlardaki HAL bağlantısı
- Génevaux ve diğerleri 2013, ACM TOG 32(4); Guérin ve diğerleri 2022, CGF 41(2)
- goSPL belgeleri: https://gospl.readthedocs.io
- Salles ve diğerleri 2023, Nature 624:115: https://doi.org/10.1038/s41586-023-06777-z
- Salles ve diğerleri 2024, Nat. Commun. 15:3430: https://doi.org/10.1038/s41467-024-47662-1
- Garthwaite 2011 tezi (Argand sayısı), MIT OCW (Airy), Roe ve Brandon el yazması: ham notlardaki bağlantılar
- Tam liste ve her bilginin kaynağı `arastirma/notlar/12/` içinde.
