# 19. Yağış bağlantısı

Araştırma tarihi: 12 Kasım 2026. Belge tek bir Haiku kolunun notlarının sentezidir ve benim küçük bir denememi içerir; sentezi ben yazdım. Ham notlar `arastirma/notlar/19/A_yagis.md` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** özet ya da paket sayfası okundu, **[Ö]** arama özeti, doğrulanamadı, **[Ö-ölç]** bu oturumdaki kendi denemem, **[H]** bizim çıkarımımız, **[Y]** bulunamadı.

Dürüst durum: Smith ve Barstad (2004) JAS makalesi erişilemedi, denklemler yalnızca bir konferans özetinden alındı ve metin çıkarımında bozuk. Aracın bölgesi 7°G ile 60°K arasında olduğundan ekvator yağmur kuşağından batı rüzgârları kuşağına kadar tüm iklim bantlarını kapsıyor.

## Kısa sonuç

**1. Doğrusal orografik yağış kuramı aracın yağış katmanı için uygun ve düşük maliyetli.** Smith ve Barstad (2004, J. Atmos. Sci.): yoğunlaşmış su bütçesi; transfer fonksiyonu P̂ = C_w iσĥ / {(1 − i m H_w)(1 + iστ_c)(1 + iστ_f)}, m = sqrt[((N_m² − σ²)/σ²)(k² + l²)] [B, konferans özeti]. Örnek değerler: N_m = 0,005 1/s, rüzgâr 15 m/s, τ_c = τ_f = 1000 s [B]; sahada τ aralığı 100 ile 5000 s [Ö]. C_w ifadesi ve m'nin tam hâli metin çıkarımında bozuk; JAS makalesiyle doğrulanmalı.

**2. Hazır Python paketi var ama bu ortamda kurulmadı.** PyPI `orographic-precipitation` 1.0 (MIT, Raphael Lange; repo rlange2/orographic-precipitation): parametreler latitude, precip_base, wind_speed, wind_dir, conv_time, fall_time, nm, hw, lapse_rate, lapse_rate_m, ref_density; fonksiyon `compute_orographic_precip` [B-öz]. Ben `pip install orographic-precipitation` denedim: paket `setup.py egg_info` aşamasında metadata hatası verdi ve kurulmadı [Ö-ölç]; hata nedeni incelenmedi. Landlab'da `OrographicPrecipitator` bulunamadı, en yakın bileşen `SpatialPrecipitationDistribution` [Y].

**3. Yağış ile arazi arasında çift yönlü geri besleme var.** Roe, Montgomery ve Hallet (2003, JGR): eğime bağlı negatif, yüksekliğe bağlı pozitif geri besleme (doğru başlık "Orographic precipitation and the relief of mountain ranges"; istenen "relief-elevation relationship" başlığı bulunamadı) [B]. Whipple (2009, Nature Geoscience): erozyon tektoniği pasif değil birinci dereceden etkiliyor; Alpler ve St Elias en güçlü saha örnekleri [B, OSU kopyası].

**4. Yağış yüksekliğe sınırsız artmıyor.** Roe (2005, Annu. Rev. Earth Planet. Sci.): yağış yaklaşık 4 km (tropik) ve yaklaşık 2 km (yüksek enlem) yükseklikte H_m ölçeğine kadar; yağış yamaçta en yüksek olabilir, tepede değil [B].

## 1. Orografik yağış

| Konu | Bulgu | Etiket |
|---|---|---|
| Smith ve Barstad 2004 | transfer fonksiyonu, N_m, rüzgâr, τ_c ve τ_f; örnek N_m = 0,005 1/s, 15 m/s, τ = 1000 s | konferans özeti [B] |
| Roe 2005 | H_m ≈ 4 km tropik, ≈ 2 km yüksek enlem | [B] |
| Roe, Montgomery, Hallet 2003 | eğime bağlı negatif ve yüksekliğe bağlı pozitif geri besleme | [B] |
| Whipple 2009 | erozyon tektonik evrimi birinci dereceden etkiler | [B] |
| Willett 1999 "Orogeny and orography" | | tam metin 403, özet [Ö] |
| Whipple ve Meade 2004 | | bulunamadı; ikincil özet Roe ve diğerleri 2008 [Ö] |

## 2. Basit küresel iklim yaklaşımları

- **Köppen-Geiger (Beck ve diğerleri 2018):** 1 km çözünürlük, 5 ana sınıf, 30 alt tip, doğruluk yüzde 80,0 (eski haritalar yüzde 66 ile 71); WorldClim ve CHELSA girdileri [B]. Kuru sınıfların kara payı bulunamadı [Y].
- **Ekvator yağmur kuşağı (ITCZ), Hadley hücresi, 30° çevresi kurak kuşak, 30° ile 60° batı rüzgârları:** kavramsal kaynaklar bulundu [Ö]; Held ve Hou (1980) tam metni erişilemedi [Y].
- **Yağış eksi buharlaşma (P − E):** zonal örüntü [Ö]; Trenberth birincil kaynağı bulunamadı [Y]. North (1975) enerji dengesi modelinde yağış parametrizasyonu bulunamadı [Y].
- **Çıkarım [H]:** aracın 7°G ile 60°K bandı için yağış, enlem bandı tabanlı bir taban değer (ekvatora yakın yüksek, 20° ile 30°'de düşük, 40° ile 60°'de orta) ile doğrusal orografik katmanın toplamı olarak kurulabilir; rüzgâr yönü enlem bandına göre (tropikte doğudan, orta enlemde batıdan) seçilir. Kıta içi kuraklık için uzaklık-kıyıdan azalma terimi eklenir. Bu bir tasarım önerisidir, kaynaklı bir kural değildir.

## 3. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Orografik yağış modeli | doğrusal kuram (Smith ve Barstad) | [B] |
| N_m | 0,005 1/s (örnek) | [B] |
| Rüzgâr hızı | 15 m/s (örnek) | [B] |
| τ_c, τ_f | 1000 s (saha aralığı 100 ile 5000 s) | [B ve Ö] |
| Yağışın yükseklik sınırı H_m | yaklaşık 4 km tropik, yaklaşık 2 km yüksek enlem | [B] |
| Taban yağış | enlem bandına göre (ITCZ yüksek, 30° çevresi düşük) | [H] |
| Rüzgâr yönü | tropikte doğudan, orta enlemde batıdan | [Ö ve H] |
| Yağış → aşınma | K'nin yağışa bağımlılığı 13. belgedeki değerlerle | [B] |
| Python paketi | `orographic-precipitation` 1.0; bu ortamda kurulamadı, kaynak koddan ya da kendi uygulamamızla | [B-öz ve Ö-ölç] |

## 4. Kaynaklar arası çelişkiler

- Smith ve Barstad denklem 4 (C_w) ve m ifadesi çıkarılan metinde bozuk; birbiriyle tutarsız sürümler olabilir.
- Roe, Montgomery ve Hallet başlığı: promptumdaki "relief-elevation relationship" başlığı bulunamadı.
- Landlab: `OrographicPrecipitator` adı bulunamadı; `SpatialPrecipitationDistribution` var.

## 5. Bulunamayanlar ve doğrulanamayanlar

- Smith ve Barstad 2004 JAS tam metni (journals.ametsoc.org 403); Willett 1999 tam metni (403); Whipple ve Meade 2004; Held ve Hou 1980; Trenberth P − E kaynağı; North 1975 yağış parametrizasyonu; kuru Köppen sınıflarının kara payı.
- journals.ametsoc.org, agupubs, annualreviews ve github 403 ya da DNS hatası verdi; bot korumasını aşma girişimi yapılmadı.
- `orographic-precipitation` paketinin işlevselliği, kurulamadığı için sınanmadı.
- Whipple (2009) sayfa numaraları doğrulanmadı, DOI ile atıf yapılmalı.

## 6. Promptumdaki hatalar (düzeltildi)

- "Landlab OrographicPrecipitator" bulunamadı; en yakın bileşen `SpatialPrecipitationDistribution`.
- Roe, Montgomery ve Hallet 2003 başlığı "Orographic precipitation and the relief-elevation relationship" değil, "Orographic precipitation and the relief of mountain ranges".
- "Whipple ve Meade 2004" bu konuda bulunamadı.

## Başlıca kaynaklar

- Smith ve Barstad 2004 (konferans özeti): https://ams.confex.com/ams/pdfpapers/62756.pdf
- `orographic-precipitation` (PyPI), Lange: rlange2/orographic-precipitation
- Roe 2005, Roe ve diğerleri 2003, Whipple 2009, Beck ve diğerleri 2018: ham notlardaki bağlantılar
- Tam liste ve her bilginin kaynağı `arastirma/notlar/19/` içinde.
