# 20. Gerçekçiliğin ölçülmesi

Araştırma tarihi: 12 Kasım 2026. Belge üç şeyin sentezidir: iki Haiku kolunun literatür taraması (B hipsometri ve akarsu ağı ölçeklemesi, C fraktal ölçütler, eğim, algısal gerçekçilik ve DEM özellikleri; ilk kol kota nedeniyle yarım kalmış, A notu), benim gerçek yükseklik verisi üzerinde yaptığım ölçümler ve atlas deposundaki yükseklik çapaları (salt okunur inceleme). Sentezi ben yazdım. Ham notlar ve betikler `arastirma/notlar/20/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** özet ya da ikincil tam metin, **[Ö]** arama özeti, doğrulanamadı, **[Ö-ölç]** bu oturumdaki kendi ölçümüm, **[H]** çıkarım, **[Y]** bulunamadı.

## Kısa sonuç

**1. Aracın gerçekçiliğini ölçmek için gerçek DEM'i aynı hücre boyuna kaba tanelemek gerekiyor; yayımlanmış rölyef tablosu yok, ben ölçtüm.** Altı dağ kuşağında 30 m SRTM verisini (AWS terrain tiles) 5, 10 ve 20 km hücrelere kaba taneleyerek yerel rölyef (hücre içi en yüksek eksi en düşük) hesapladım [Ö-ölç]. Aşağıdaki tablo araç için gerçekçilik hedefleri veriyor, ama kurgusal kıta bilerek Dünya'dan yüksek (atlas çapaları, bkz. 4. bölüm).

**2. Algısal gerçekçilik için kullanılabilir bir yöntem var: iki seçenekten zorunlu seçim (2AFC) deneyi.** Rajasekaran ve diğerleri (2022, arXiv 1909.04610): 128 Mechanical Turk katılımcısı; gerçek arazi yaklaşık yüzde 77, prosedürel arazi yaklaşık yüzde 51 gerçekçi bulundu; geomorfon regresyonu açıklanan varyansın yüzde 72'sini veriyor [B]. Argudo ve diğerleri (2019): orometrik sınıflandırma doğruluğu yüzde 75,3 (R = 50 km); algısal çalışmalarda gerçek ile sentetik arasındaki fark sürüyor [B].

**3. Yayımlanmış ölçütlerin bir kısmı araca uymuyor.** FID (Fréchet) mesafesi arazi yüksekliğinde standart ölçüt olarak bulunamadı, yalnızca görüntü uzayında kullanılıyor [Y]. Sırt sürekliliği için yayımlanmış standart ölçüt bulunamadı [Y]; prominence ve zirve-eyer grafı var ama süreklilik ölçüsü değil [B-öz].

## 1. Kendi ölçümüm: gerçek DEM'i kaba tanelemek

**Veri ve yöntem [Ö-ölç].** AWS terrain tiles (`skadi`, SRTM kaynaklı, 1 yay-saniye ≈ 30 m); altı bölge × 3°×3° (54 karo): Alpler (45–48°K, 7–10°D), Nepal Himalayası (27–30°K, 84–87°D), Appalachian (35–38°K, 84–81°B), İskandinav dağları (60–63°K, 6–9°D), Zagros (30–33°K, 50–53°D), Orta And (19–16°G, 70–67°B). Hücre = 162, 324, 648 piksel (0,045°, 0,09°, 0,18° ≈ 5, 10, 20 km kuzey-güney); %90'dan az geçerli hücre atıldı. Betikler: `dem_fetch.py`, `dem_stats.py`, `dem_hydro.py`; sonuçlar `dem_stats.json`, `dem_hydro.json`.

**Yerel rölyef (hücre içi en yüksek eksi en düşük, m): ortalama / ortanca / yüzde 90**

| Bölge | 5 km | 10 km | 20 km |
|---|---|---|---|
| Alpler | 792 / 641 / 1692 | 1104 / 947 / 2275 | 1471 / 1291 / 2796 |
| Nepal Himalayası | 1006 / 848 / 1975 | 1456 / 1171 / 2828 | 2078 / 1536 / 4180 |
| Appalachian | 345 / 314 / 630 | 460 / 416 / 823 | 625 / 572 / 1074 |
| İskandinav dağları | 688 / 662 / 1202 | 980 / 977 / 1574 | 1316 / 1348 / 1856 |
| Zagros | 554 / 488 / 1126 | 838 / 764 / 1601 | 1229 / 1106 / 2198 |
| Orta And | 497 / 326 / 1299 | 756 / 556 / 1861 | 1129 / 842 / 2490 |

**Hücre ortalamalarından hesaplanan eğim (derece): ortanca / yüzde 90**

| Bölge | 5 km | 10 km | 20 km |
|---|---|---|---|
| Alpler | 2,0 / 7,4 | 1,2 / 3,7 | 0,9 / 2,2 |
| Nepal Himalayası | 2,7 / 7,5 | 1,6 / 4,7 | 0,9 / 3,4 |
| Appalachian | 0,6 / 2,2 | 0,4 / 1,4 | 0,3 / 0,8 |
| İskandinav dağları | 2,6 / 6,6 | 1,3 / 3,0 | 0,7 / 1,5 |
| Zagros | 1,6 / 4,8 | 1,0 / 2,7 | 0,6 / 1,6 |
| Orta And | 1,2 / 4,9 | 0,8 / 3,4 | 0,5 / 2,3 |

**İnce ölçekli eğim ve yükseklik (yaklaşık 120 m, ortanca / yüzde 90, derece):** Alpler 11,3 / 35,7; Himalaya 17,2 / 35,7; Appalachian 10,5 / 24,2; İskandinav 10,7 / 31,1; Zagros 5,6 / 25,8; Orta And 4,4 / 25,8. Bölge ortalama yüksekliği: Alpler 1026 m, Himalaya 3630, Appalachian 569, İskandinav 884, Zagros 1915, Orta And 3810 m [Ö-ölç].

**Okuma [H].**
- Yerel rölyef hücre boyuyla yaklaşık doğrusal büyüyor: 5 km'den 20 km'ye 1,8 ile 2,3 kat (Appalachian 1,81, Alpler 1,86, İskandinav 1,91, Himalaya 2,07, Zagros 2,22, Orta And 2,27). Hücre ortalamalarından hesaplanan eğimin ortancası ise 20 km'de 5 km'ye göre 2,2 ile 3,7 kat düşüyor (Alpler 2,2, Appalachian 2,3, Orta And 2,3, Zagros 2,5, Himalaya 2,9, İskandinav 3,7) (kaba taneleme eğimi düzleştirir). Bu, 14. belgedeki "çözünürlük rölyefi ve eğimi değiştirir" bulgusunun gerçek veride karşılığı.
- Genç yüksek dağlarda (Himalaya, Alpler) 10 km hücre ortalama rölyefi 1100 ile 1450 m; eski dağlarda (Appalachian) 460 m. Oran yaklaşık 2,4 ile 3,2 kat; bu, 4. belgedeki eski ve genç dağ ayrımı için ölçülebilir bir gerçekçilik işareti.
- Zagros, 10 km'de 838 m ortalama rölyef ve yaklaşık 1900 m ortalama yükseklikle, 2. konudaki "Zagros benzeri plato" seçeneğinin ölçülebilir bir referansı.

**Hipsometrik integral ve eğim-alan ilişkisi [Ö-ölç], 185 m hücre (6×6 ortalama), 3°×3° blok.**

| Bölge | HI | θ (A > 10 km², ham D8 yerel eğim, ortanca) | En büyük drenaj alanı (km²) |
|---|---|---|---|
| Alpler | 0,22 | 0,26 | 30 318 |
| Nepal Himalayası | 0,41 | 0,27 | 22 838 |
| Appalachian | 0,23 | 0,19 | 23 946 |
| İskandinav dağları | 0,39 | 0,29 | 9 731 |
| Zagros | 0,44 | 0,11 | 31 933 |
| Orta And | 0,54 | 0,21 | 40 286 |

Uyarılar: HI blok boyutu 3°×3° (üst sınır olarak denizi de içeren İskandinav bloğu dahil); bu Strahler'in havza ölçekli HI'sinden farklı bir ölçü olduğu için eşik karşılaştırması yapılmamalı. θ değerleri kaba: 185 m hücrede ham D8 eğimle, A'ya göre ortanca değerlerin 10 km² üstü 8 ile 9 kutusuna uydurulmuş doğru; literatürdeki yaklaşık 0,45'ten (Kirby ve Whipple) düşük çıktı, çünkü blok kenarlarında havzalar kesik, gürültülü yerel eğim kullanıldı, bitki ve bina etkisi ve SRTM yüzey modeli sorunları var. Bu θ değerleri aracın hedefi olarak kullanılmamalı. İlk çalıştırmada drenaj alanını hücre alanıyla fazla çarpma hatası yapmıştım; düzeltilmiş sonuçlar yukarıda.

## 2. Literatürden hedef değerler

| Ölçüt | Değer | Etiket |
|---|---|---|
| Hack yasası | L = 1,4 A^0,6 (L mil, A mil²), katsayı 1 ile 2,5 (kumtaşında yaklaşık 2,0); Hack (1957), USGS PP 294-B, Eş. 3. Ansiklopedide üs "0,6'dan biraz küçük" | [B ve B-öz] |
| Horton oranları | bifurkasyon R_B yaklaşık 2 (düz arazi) ile 3 ile 4 (dağlık); uzunluk R_L yaklaşık 2 ile 3, ortalama 2,32 (Horton 1945); R_A metinde yok | [B] |
| Eğim-alan yasası | S = k_s A^−θ; k_sn θ_ref ile normalize (Mudd ve diğerleri 2018, ESurf 6:505); θ ≈ 0,45 tek havzada tepe değer; Loess Platosu için θ_ref 0,4 ile 0,5 öneriliyor. "±0,2" ifadesi bu makalede yok; Kirby ve Whipple 2012'de doğrulanamadı (ikincil "0,4 < θ < 0,6" [Ö]) | [B ve Ö] |
| Hipsometrik integral eşikleri | Strahler (1952) genç / olgun / yaşlı eşikleri (0,6 / 0,35) birincil kaynakla doğrulanamadı; ikincil bir uygulamada 0,30 altı "yaşlı" | [Ö ve B-öz] |
| Dünya karası hipsometrisi | ortalama kara yüksekliği 840 m (1921 tahmini olarak ikincil kaynakta); medyan 377 m hiçbir kaynakta bulunamadı | [Ö ve Y] |
| Fraktal / spektral | küresel topografya güç spektrumunun çok-fraktal modeli fBm / fLm'den iyi (Gagnon ve diğerleri 2006, NPG 13:541), spektral üs yaklaşık 2 | [B-öz ve Ö] |
| Eşik yamaç | Burbank ve diğerleri 1996, Nature 379:505 ile 510 (doi 10.1038/379505a0): Indus kesiminde aşınma 2 ile 12 mm/yıl, yamaç açıları aşınma hızından bağımsız, ortak eşik süreci; 30 ile 40° değeri özette yok | [B-öz] |
| Eğim dağılımı | Montgomery (2001): normal ya da üstel eğim histogramları, eşik yamaçlar; ortanca ve yüzde 90 değeri bulunamadı | [Ö] |

## 3. DEM kaynakları ve algısal ölçütler

- **GEBCO:** güncel sürüm GEBCO_2026, 15 yay-saniye ızgara, kamu malı, ücretsiz [B]. Dikey doğruluk bulunamadı [Y].
- **Copernicus DEM:** GLO-30 (1") ve GLO-90 (3"); ESA lisansıyla ücretsiz (atıf zorunlu); mutlak dikey hata yüzde 90 olasılıkla 4 m'den az, göreli hata 2 m'den az (eğim yüzde 20 ve altı); bir yüzey modeli, bina ve bitki içerir [B]. SRTM karşılaştırması: Avrupa rüzgâr sahalarında RMSE 1,91 m (Copernicus) ve 2,82 m (SRTM) [Ö]. FABDEM yaklaşık 30 m, GLO-30'dan türetilmiş, ticari olmayan kullanım [B-öz].
- **Algısal değerlendirme:** Rajasekaran ve diğerleri (2022, PTRM): 2AFC, 128 katılımcı, gerçek yaklaşık %77, prosedürel yaklaşık %51 gerçekçi; geomorfon regresyonu açıklanan varyans %72, SE 0,13 [B]. Argudo ve diğerleri (2019): orometrik sınıflandırma doğruluğu %75,3 (R = 50 km), alt deneyde %86; altı arazinin algısal çalışması [B]. Perche ve diğerleri (2023): nicel değerlendirme drenaj hesabıyla, nitel kullanıcı istemi [B]. "Turing testi" ifadesi bulunamadı; PTRM 2AFC eşdeğeri [Y].
- **Sırt sürekliliği:** prominence tanımı (anahtar boyun, eşikler 15 m, 150 m, 300 ft, 2000 ft) [B-öz]; Reeb grafı kontur ağacıdır, süreklilik ölçüsü değil [B-öz]. Yayımlanmış sırt sürekliliği ölçütü bulunamadı [Y]; araç kendi ölçütünü tanımlamalı (örneğin 3. belgedeki sırt çizgisi uzunluğu / doğrusal uzaklık oranı) [H].

## 4. Atlas çapalarıyla çatışma

Atlas deposunun (`dunyam-atlas-mobil`) yükseklik eğrisi sahibin çapalarından kurulu: ova 250 ile 300 m, plato çanağı 800 ile 1000 m, Büyük Duvar zirveleri 6000 m, en yüksek 7000 m, aralar PCHIP; kıta bilerek Dünya'dan yüksek, kara medyanı yaklaşık 950 m (Dünya'da yaklaşık 377 m) [atlas notu, salt okunur].

**Çatışma [H].**
- Gerçek dünya referansları yukarıdaki tabloda: Himalaya 8748 m maksimum, 20 km hücre ortalama rölyefi 2078 m; Alpler 4543 m maksimum, 1471 m. Atlas en yüksek noktası 7000 m: Himalaya'dan düşük, Alpler'den yüksek. Büyük Duvar 6000 m zirveli, yani yükseklik olarak And (6577 m maksimum) ile Alpler arası.
- Kara medyanı 950 m (atlas) ile 377 m (Dünya) arasındaki fark, kıtanın genel olarak yüksek olduğunu söylüyor. Mutlak yüksekliği doğrudan Dünya DEM'iyle karşılaştıran bir gerçekçilik ölçütü bu yüzden yanlış sinyal verir (kıta "çok yüksek" görünür).
- Plato çanağı (800 ile 1000 m) 2. konudaki "1000 ile 2000 m step" ile çakışıyor: atlas iklimi çanak içini 800 ile 1000 m alıyor, istek 1000 ile 2000 m. Karar günlüğünde zaten not var; burada sayısal olarak da belirtilmeli.

**Öneri [H].** Gerçekçilik ölçütü mutlak yükseklikle değil, yükseklikle ölçeklenmiş ya da bağıl bir biçimle karşılaştırmalı: (a) yerel rölyef / yerel ortalama yükseklik oranı, (b) eğim dağılımı, (c) yerel rölyefin hücre boyuna bağımlılığı (5, 10, 20 km), (d) Hack üssü ve akarsu ağı yoğunluğu, (e) genç ve eski dağlar arasındaki rölyef oranı. Mutlak çapa çatışması istisna defterine (16. konu) yazılmalı: "yükseklik eğrisi atlas çapalarına göre Dünya'dan bilerek yüksek".

## 5. Aracın varsayılan ölçüt seti

| Ölçüt | Hedef | Etiket |
|---|---|---|
| 10 km hücre yerel rölyef, genç yüksek dağ | yaklaşık 1100 ile 1450 m ortalama | [Ö-ölç] |
| 10 km hücre yerel rölyef, eski dağ | yaklaşık 460 m ortalama | [Ö-ölç] |
| 10 km hücre yerel rölyef, plato / kıvrım kuşağı (Zagros benzeri) | yaklaşık 840 m ortalama | [Ö-ölç] |
| Rölyefin hücre boyuna bağımlılığı | 5 km'den 20 km'ye yaklaşık 1,8 ile 2,3 kat | [Ö-ölç] |
| Hücre eğiminin ortancası, 10 km | 1,2 ile 1,6° (genç dağ), 0,4° (eski dağ) | [Ö-ölç] |
| Hack üssü | h ≈ 0,6 (L = 1,4 A^0,6) | [B] |
| Horton bifurkasyon / uzunluk oranı | R_B 3 ile 4 (dağlık), R_L 2 ile 3 | [B] |
| Akarsu içbükeyliği θ | 0,4 ile 0,6 (ikincil) | [Ö] |
| Algısal gerçekçilik | 2AFC deneyi, hedef gerçek araziyle karıştırılabilirlik | [B] |
| Mutlak yükseklik | atlas çapalarıyla (ova 250 ile 300 m, çanak 800 ile 1000 m, zirve 6000 ile 7000 m); Dünya DEM'iyle karşılaştırma | atlas |
| Karşılaştırma yöntemi | gerçek DEM'i aracın hücre boyuna kaba tanele, alan ağırlıklı ölçüm (8. belge) | [H] |

## 6. Kaynaklar arası çelişkiler

- Horton oranları: görev notundaki R_B 3 ile 5, R_L 1,5 ile 3,5 ile Horton 1945 metni (R_B 2 ile 4, R_L 2,32 ortalama) örtüşmüyor.
- θ ≈ 0,45 ± 0,2: Mudd ve diğerleri 2018'de "± 0,2" ifadesi yok.
- Hack üssü: 0,6 ile "0,6'dan biraz küçük".
- Burbank 1996: Nature'da; "JGR" atfı yanlıştı. Roering 1999 başlığı "Evidence for nonlinear, diffusive sediment transport..." (WRR 35(3):853 ile 870); "creep and landsliding" başlığı Roering ve diğerleri 2001 Geology'ye ait. Perron 2008 JGR 113 (F04003) doğrulandı; "2008 Nature" yanlış, Nature makalesi 2009 (460:468).
- Atlas medyanı 950 m ile Dünya 377 m (Dünya değeri doğrulanamadı).

## 7. Bulunamayanlar ve doğrulanamayanlar

- Strahler 1952 ve Pike ve Wilson 1971 birincil metinleri; Cogley 1984; Harrison 1983; Rigon 1996; Kirby ve Whipple 2012 tam metni; Wobus 2006; Melton 1957; Horton 1932; Mark ve Aronson 1984 (D ≈ 2,2); Montgomery 2001 sayıları; Burbank 1996 tam metni (30–40° özet dışı).
- Dünya karası ortalama yüksekliği 840 m ve medyan 377 m için birincil kaynak; GEBCO dikey doğruluğu.
- FID arazi için, sırt sürekliliği için standart ölçüt.
- AGU, GSA DOI sayfaları, core.ac.uk tezi, escholarship.org (TLS sertifika hatası, atlatılmadı), NOAA NGDC-24 PDF (erişim reddi) açılamadı.
- Kendi ölçümüm: 6 bölge × 3°×3° ile sınırlı; deniz içeren bloklar (İskandinav) sıfır yükseklikli deniz pikselleri içeriyor olabilir; SRTM bir yüzey modeli (bitki ve yapı); θ ve HI kaba.

## 8. Promptumdaki hatalar (düzeltildi)

- "Burbank 1996 JGR" yanlış; Nature 379:505 ile 510.
- "Roering 1999: creep and landsliding" başlığı yanlış (2001 Geology'ye ait).
- "Perron 2008 Nature" yanlış; JGR 113 (F04003), Nature 2009.
- "Cogley, Harrison ve Sinclair" ortalama ve medyan çifti doğrulanamadı.
- "Horton oranları R_B 3 ile 5, R_L 1,5 ile 3,5" Horton 1945'le tam örtüşmüyor.
- "GEBCO 2024" yerine güncel sürüm GEBCO_2026.
- "Schott 2023 evaluation" bölümü bulunamadı; en yakın eşleşme Argudo, Guérin, Schott, Galin (2025) CGF raporu.
- "θ ≈ 0,45 ± 0,2" Mudd ve diğerleri 2018'de "± 0,2" olmadan.

## Başlıca kaynaklar

- Hack 1957, USGS PP 294-B: https://pubs.usgs.gov/pp/0294b/report.pdf
- Horton 1945 (kopya): pdodds.w3.uvm.edu
- Mudd ve diğerleri 2018, ESurf 6:505: https://esurf.copernicus.org/articles/6/505/2018/
- Rajasekaran ve diğerleri 2022 (PTRM): https://arxiv.org/abs/1909.04610
- Argudo ve diğerleri 2019, ACM TOG 38(6):199; Perche ve diğerleri 2023: https://arxiv.org/abs/2304.09626
- Burbank ve diğerleri 1996: https://doi.org/10.1038/379505a0
- Copernicus DEM ve GEBCO: kurum sayfaları, ham notlarda
- SRTM karo kaynağı: https://s3.amazonaws.com/elevation-tiles-prod/skadi/
- Ölçüm betikleri ve sonuçları: `arastirma/notlar/20/`
- Tam liste ve her bilginin kaynağı `arastirma/notlar/20/` içinde.
