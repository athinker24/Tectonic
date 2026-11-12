# 15. Çökelme, kapalı havzalar ve göller

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun sentezidir (A önülke havzaları, delta ve sahanlık dolgusu, B kapalı havzalar ve göller); sentezi ben yazdım. Ham notlar `arastirma/notlar/15/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** yalnızca özet ya da ansiklopedi, **[Ö]** arama özeti, doğrulanamadı, **[H]** çıkarım, **[Y]** bulunamadı.

Dürüst durum: önülke havzaları ve deltalar için nicel sayı neredeyse hiç bulunamadı. Kaynaklı sayılar çoğunlukla küresel çökelti hacmi (GlobSed) ve göl veri tabanlarından geliyor. Atlas reposundaki göl ve nehir katmanıyla uyum bu belgede ele alınmadı (24. konuya ait).

## Kısa sonuç

**1. Çökelti kalınlığı kıta kenarlarında büyük.** GlobSed (Straume ve diğerleri 2019, Geochemistry, Geophysics, Geosystems 20:1756 ile 1772, doi 10.1029/2018GC008115) [B]: okyanus çökelti hacmi yaklaşık 3,37e8 km³, ortalama 927 m; kıta kenarlarında hacim yaklaşık 1,43e8 km³ (yaklaşık yüzde 42), alan yaklaşık 4,69e7 km², ortalama 3044 m; derin okyanusta (kıta okyanus sınırından 200 km ötesi) ortalama 404 m. Makalenin "yüzde 29,7 artış" ifadesi tablodaki Whittaker 2013 değeriyle (2,37e8 km³) tutarlı değil; yalnızca metin ifadesi olarak aktarılıyor.

**2. Kapalı havzalar kıtaların yaklaşık beşte biri.** Küresel endoreik alan yaklaşık yüzde 18 (ansiklopedi, [B-öz]) ile yaklaşık yüzde 20 (Scientific Data s41597-023-02875-9, [B]; kaynağı Lehner ve Döll olarak doğrulanamadı). Avustralya'da yüzde 21, Kuzey Amerika'da yüzde 5 [B-öz]. Aracın denize akmayan havzası (Tarım ya da Moğolistan benzeri) için bu orana göre bir kapalı havza yüzdesi aralığı verilebilir.

**3. Göller küçük bir alanı kaplıyor ve küçükleri çok.** HydroLAKES (Messager ve diğerleri 2016): 10 hektar ve üstü 1,42 milyon göl, 2,67 milyon km² (kara alanının yüzde 1,8), hacim 181,9 bin km³ [B]. Downing ve diğerleri (2006): 304 milyon göl ve gölcük, 4,2 milyon km²; Pareto üssü c = 1,06; doğal göller 0,001 km² ve üstü için kara alanının yüzde 2,8'i [B].

**4. Çukur doldurma (priority-flood) ve taşma için standart algoritma var.** Barnes ve diğerleri: Priority-Flood, depresyonsuz yüzey, her hücre drene oluyor; tamsayı için O(n), kayan nokta için O(n lg n) [B]. Landlab `LakeMapperBarnes` göl alanını çıktı olarak veriyor [Ö]; Fastscapelib `PFloodSinkResolver` yüksekliği değiştiriyor, akış grafiğini değiştirmiyor [Ö].

## 1. Önülke havzaları, deltalar ve çökelti hacmi

| Konu | Değer | Etiket |
|---|---|---|
| Küresel okyanus çökelti hacmi | 3,37e8 km³; ortalama 927 m | GlobSed [B] |
| Kıta kenarı çökeltisi | 1,43e8 km³ (yaklaşık %42); alan 4,69e7 km²; ortalama 3044 m | GlobSed Tablo 3 [B] |
| Derin okyanus çökeltisi | ortalama 404 m (kıta okyanus sınırından 200 km ötesi) | GlobSed [B] |
| Küresel nehir tortu yükü | askıda yaklaşık 20e9 t/yıl | Milliman ve Syvitski 1992 [Ö] |
| BQART modeli | 488 nehir, yanlılık yaklaşık %3; jeoloji %65, iklim +%14, insan +%16, buzul yaklaşık %1; uzun dönem ortalamayı tahmin eder, olay bazlı değil | Syvitski ve Milliman 2007 [B-öz] |
| Önülke sistemi | dört depozon: wedge-top, foredeep, forebulge, back-bulge | DeCelles ve Giles 1996 [B-öz] |
| Doluluk oranı | F = tortu arzı / accommodation; F > 1 aşırı dolu, F < 1 eksik dolu eğilimi; Alp erken fazında F < 1 | Sinclair ve Allen 1992, Basin Research 4:215 [Ö] |
| Ganj-Brahmaputra | yaklaşık 1e9 t/yıl, delta yaklaşık 110 000 km², toplam kalınlık 16 km'yi aşıyor (yalnızca Wikipedia türevi; birincil kaynakla doğrulanmadı) | [Ö] |
| Derin okyanus tortu derlemesi | son 5 milyon yıl artışı deniz seviyesi düşüşüne bağlanmış, sonraki derleme iklimi öneriyor | Hay 1988 [Ö] |

Düzeltmeler: GlobSed Straume 2019 "Scientific Data"da değil, G-cubed'de; Watts ve Ryan 1976 "Marine and Petroleum Geology" değil, Tectonophysics 36:25 ile 44 (ikincil kaynaklar, birincil kopya yok); Jordan 1981 "Tectonics" değil, AAPG Bulletin 65(12):2506 ile 2520, "Thrust loads and foreland basin evolution, Cretaceous, western United States"; "Sinclair 1992" Sinclair ve Allen 1992.

Backstripping (Watts ve Ryan yöntemi) Airy 1B modeliyle ve 2B esneme ile farklı sonuç verir [Ö]. "Tortu yükü başına yaklaşık yüzde 50 ek çökme" ifadesi için kaynaklı bir yüzde bulunamadı [Y]; doğrulanmadan kullanılmamalı. Airy ile yüklenen çökmeyi ρ_çökelti ve ρ_manto oranıyla hesaplamak [H] mümkündür (3. belgedeki kütle dengesi), ama bu kaynaklı bir sayı değil bir hesap.

**Bulunamayanlar:** Ganj, Indus, Po, Ebro, Alp molası ve Appalachian önülkeleri için genişlik, kalınlık ve dolgu hızı (m/milyon yıl); aşırı ve eksik dolu için nicel eşik; Mississippi, Nil ve Yangtze deltası için alan, ilerleme hızı ve hacim; dağ kuşağı aşınma hacmi ile havza dolgu hacminin karşılaştırması [Y].

## 2. Kapalı havzalar

| Havza | Alan ve diğer | Etiket |
|---|---|---|
| Tarım | yaklaşık 888 000 km²; tortul dolgu yerel olarak 15 km'yi aşıyor (benim tahminim olan 5 ile 15 km yerel maksimumun altında kalıyor); ortalama kalınlık için birincil kaynak bulunamadı | [B-öz] |
| Gobi | 1 295 000 km² | [B-öz] |
| Büyük Havza | 541 730 km² | [B-öz] |
| Aral | 68 000 km² (1960) → 17 160 km² (2004) | [B-öz] |
| Balkaş | 16 400 km², derinlik yaklaşık 341 m (bu değer tutarsız görünüyor) | [B-öz] |
| Altiplano | taban yaklaşık 3750 m | [B-öz] |

Kapalı havzanın oluşum nedenleri: tektonik izolasyon ve yağmur gölgesi; Tien Shan ve Kunlun yükselmesi Tarım'ı kapalı yaptı ve Tien Shan yağmur gölgesi oluşturdu (zaman aralığı tartışmalı: Oligosen ile Miyosen) [Ö]. Altiplano ile Tibet karşılaştırması [B-öz]. Tibet yağış sayıları bulunamadı [Y].

**Taşma örnekleri.** Hazar erken Khvalynian maksimumu +48 ile +50 m (geleneksel), HESS 2024: Manych üzerinden Karadeniz'e batıya akış [B]; taşma eşiği tartışması: 2026 modeli 31 m, eski çalışma 45 ile 50 m [Ö]. Bonneville Gölü: Red Rock Pass'tan taşma, sel göl seviyesini yaklaşık 125 m düşürdü [B-öz]. Karadeniz ve Bonneville'in eski endoreik göller olduğu ansiklopedide yazıyor [B-öz]. Göl alanı ve hacim ilişkisi ile Hazar'ın kalıcı çökelti kalınlığı bulunamadı [Y].

## 3. Göl modelleme ve veri tabanları

- **Priority-Flood** (Barnes ve diğerleri, arXiv 1511.04463): depresyonsuz, her hücre drene oluyor [B]. Landlab `LakeMapperBarnes`: "fill sinks to the brim", `lake_areas` çıktısı [Ö]; Fastscapelib `PFloodSinkResolver` yüksekliği değiştirir, akış grafiğini değiştirmez [Ö] (Fastscapelib akış kılavuzu 0 karakter döndü, doğrulanmadı).
- **Su dengesi.** Yağış eksi buharlaşma formülü için sayısal örnek bulunamadı [Y].
- **HydroLAKES** (Messager ve diğerleri 2016): ortalama bekleme süresi 1834 gün (medyan 456); hacim doğrulamada yüzde 16,5 düşük tahmin; derinliğin en güçlü yordayıcısı arazi eğimi [B]. Derinlik alan güç yasası açık katsayılarla (Messager Model 5) bulunamadı [Y].
- **Downing ve diğerleri 2006:** 304 milyon göl ve gölcük, 4,2 milyon km², Pareto c = 1,06, doğal göller 0,001 km² ve üstü için kara alanının yüzde 2,8'i [B].
- **Lehner ve Döll 2004:** Seviye 1 için 3067 göl (50 km² ve üstü) ve 654 rezervuar [Ö]; PDF bağlantı sıfırlamasıyla okunamadı.

## 4. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Kıta kenarı çökeltisi ortalama kalınlığı | yaklaşık 3 km | [B] |
| Derin havza çökeltisi | ortalama yaklaşık 0,4 km | [B] |
| Kapalı havza kara oranı | yaklaşık %18 ile 20 | [B-öz ve B] |
| Göl alanı kara oranı | yaklaşık %1,8 (≥10 ha) ile %2,8 (≥0,001 km²) | [B] |
| Göl boyut dağılımı | Pareto c ≈ 1,06 | [B] |
| Çukur doldurma | Priority-Flood, depresyonsuz yüzey, göl çıktısı | [B] |
| Taşma | göl seviyesi eşik yüksekliğine ulaşınca dışarı akış; Hazar ve Bonneville örnekleri | [B ve B-öz] |
| Önülke dolgusu | aşırı dolu varsayım (F > 1), kıyı sabit olduğundan | [H] |
| Tortu yükü çökmesi | Airy ile ρ oranından hesaplanır; "%50 ek" kuralı kullanılmasın | [H] |
| Kapalı havza çökelti kalınlığı | Tarım yerel maksimum 15 km'yi aşıyor; ortalama için değer yok | [B-öz] |

Aracın fixed-coast kısıtı açısından [H]: önülke havzalarının dolgusu kıyı sabit olduğundan deniz yönünde aşırı dolu varsayılıp çökelti kıyıdan çıkış kabul edilebilir (13. belgedeki açık sınır yaklaşımı). Gerçek kıyı ilerlemesi (delta) maskeye yansımayacak; bu istisna defterinde belirtilmeli.

## 5. Kaynaklar arası çelişkiler

- Endoreik alan oranı: yaklaşık %18 (ansiklopedi) ile %20 (Scientific Data, kaynağı doğrulanamadı).
- Hazar taşma eşiği: 31 m (2026 modeli) ile 45 ile 50 m (eski çalışma); erken Khvalynian maksimumu +48 ile +50 m.
- GlobSed metin ("%29,7 artış") ile Tablo 3 (Whittaker 2013 değeri 2,37e8 km³) tutarsız.
- Tien Shan yükselmesi ve yağmur gölgesi zamanı: Oligosen ile Miyosen, tartışmalı.
- Tarım dolgu kalınlığı: yerel olarak 15 km'nin üstü ile promptumdaki 5 ile 15 km.

## 6. Bulunamayanlar ve doğrulanamayanlar

- Önülke ve delta nicel sayıları (yukarıda); aşırı/eksik dolu eşiği; "tortu yükü başına yüzde 50" oranı; Ganj 16 km kalınlık iddiası.
- Syvitski ve Milliman 2007 tam metni (WHOI sunucusu "self-signed certificate in chain", doi.org/10.1086/509246 HTTP 403, core.ac.uk 403; atlatılmadı); Lehner ve Döll 2004 PDF (bağlantı sıfırlaması); Milliman ve Farnsworth 2011 tabloları; Sinclair 1997 GSA Bulletin; Bartolini 1996; Sclater ve Christie 1980.
- Hazar çökelti kalınlığı; Tibet yağış sayıları; yağış eksi buharlaşma formülü; göl alan ve hacim ilişkisi; Messager derinlik güç yasası katsayıları; Scientific Data'daki %20'nin kaynağı.
- Atlas göl ve nehir katmanıyla uyum bu belgede ele alınmadı.

## 7. Promptumdaki hatalar (düzeltildi)

- GlobSed Straume 2019: Scientific Data değil, G-cubed.
- Watts ve Ryan 1976: Tectonophysics 36:25 ile 44, Marine and Petroleum Geology değil.
- Jordan 1981: AAPG Bulletin 65(12), Tectonics değil.
- "Sinclair 1992" Sinclair ve Allen 1992, Basin Research 4:215.
- "Tarım havzası 5 ile 15 km" yerel maksimumu (15 km'yi aşıyor) olarak düzeltildi.
- "Tortu yükü başına yaklaşık %50 çökme" kaynaksız.
- "Hay 1988?" Hay 1988 DSDP / ODP derlemesi olarak doğrulandı (özet).

## Başlıca kaynaklar

- Straume ve diğerleri 2019, GlobSed: https://doi.org/10.1029/2018GC008115 (epic.awi.de kopyası)
- Messager ve diğerleri 2016 (HydroLAKES): ham notlardaki bağlantı
- Downing ve diğerleri 2006
- Barnes ve diğerleri, Priority-Flood: https://arxiv.org/abs/1511.04463
- Sinclair ve Allen 1992; DeCelles ve Giles 1996; Syvitski ve Milliman 2007 (özet)
- Tam liste ve her bilginin kaynağı `arastirma/notlar/15/` içinde.
