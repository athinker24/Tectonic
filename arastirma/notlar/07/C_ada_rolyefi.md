# Küçük dağlık adalarda rölyef ve aşınma: notlar

Durum: DEVAM EDİYOR (iskelet, bulgular eklenecek)
Etiketler: [B] birincil kaynak okundu, [Ö] özet/ikincil, [E] ansiklopedi. BULUNAMADI = kaynak bulunamadı.

## 1. Ada alanı ile en yüksek nokta ve rölyef
Kaynak: İngilizce Wikipedia sayfaları, [E], curl + oku.py ile alındı (en.wikipedia.org/wiki/<Ad>).
- Korsika: "Monte Cinto as the highest peak at 2,706 m"; metinde "total surface area of 8,680 km2" [E]. Aynı sayfanın infobox'ı "Total 8,722 km2" veriyor. Çelişki: 8 680 vs 8 722 (kullanıcı değeri 8 680 metinle uyumlu).
- Sardunya: "area of 24,100 km2"; "The highest peak is Punta La Marmora ... (1,834 m)" [E]. Kullanıcı 24 090 km2 yazmış; ansiklopedi 24 100 km2 (yuvarlama farkı).
- Tayvan: ana ada "35,808 square kilometers"; 168 adalı toplam "36,193 square kilometers"; "highest being Yu Shan at 3,952 m" [E]. Kullanıcı 36 000 km2 ve 3 952 m: yükseklik teyit, alan yuvarlama.
- Girit: infobox ve metin "8,450 km2", "Highest elevation 2,456 m (Mount Ida / Psiloritis)" [E]. Kullanıcı 8 336 km2 yazmış: Wikipedia'da 8 336 BULUNAMADI. Çelişki: 8 336 vs 8 450 (yükseklik teyit).
- Yeni Gine: "area of 785,753 km2"; "Highest elevation 4,884 m (Puncak Jaya)" [E]. Kullanıcı 786 000 km2 ve 4 884 m: teyit.
- Güney Adası: "Area 150,437 km2"; "Highest elevation 3,724 m (Aoraki / Mount Cook)" [E]. Kullanıcı 151 000 km2: yuvarlama farkı; yükseklik teyit.
- Ortalama rölyef / ortalama yükseklik (ada başına): bu sayfalarda BULUNAMADI; ada alanı ile ortalama rölyef ilişkisi için sayısal veri henüz yok.
- Not: Milliman & Syvitski 1992 [B] "a small island with elevations of 800-900 m probably should be considered mountainous" (bkz. bölüm 3).

## 2. Kıyı havzaları, nehir kısalığı, Hack yasası
- Hack 1957 [B], USGS Professional Paper 294-B, https://pubs.usgs.gov/pp/0294b/report.pdf (curl ile PDF alındı, pdftotext ile metne çevrildi): özette "length (measured ... along the longest channel above the locality) increases directly as the 0.6 power of the drainage area. This rate of increase is not affected, except locally and for short distances, by the geology of the basin." Çalışma alanı: "between 0.12 and 375 square miles" (yaklaşık 0,3 ile 970 km2) — yani küçük havzalar dahil; Virginia ve Maryland akarsuları.
- Hack yasası için Wikipedia [E] (arama özeti, tam sayfa okunmadı): üs "slightly less than 0.6 in most basins", büyük havzada (yaklaşık 20 720 km2 üstü) azalır. Birincil Hack metni ile uyumlu.
- Küçük ada kıyı havzaları ve Hack üssünün adalarda değişimi: BULUNAMADI (aramada ilgili kaynak çıkmadı). Hack'in "short distances" şerhi kısa kıyı nehirleri için sınırlayıcı not.
- Ada genişliğine bağlı havza alanı (geometrik tahmin): henüz kaynaklı değil; kaynak aranacak.

## 4. Güney Alpleri batı-doğu yağış gradyanı (ek: NIWA West Coast)
- NIWA West Coast Climatology [B-ish: resmi kurum raporu, PDF], https://www.niwa.co.nz/sites/default/files/West_Coast_Climatology_NIWA_web.pdf (curl + pdftotext -layout): özet: "Annual rainfall totals at relatively high elevations regularly exceed 10,000 mm, with low elevation coastal locations typically recording between 2,000 and 3,000 mm of rainfall annually." (1981-2010 normalleri, Tablo 6, mm/yıl): Cropp River 11 400; Tuke River 10 558; Lake Paringa 5 588; Franz Josef 5 751; Lake Moeraki 4 301; Kopara 2 995; Hokitika 2 732; Seddonville 2 813; Greymouth 2 452; Westport 2 046; Inangahua 2 433; Reefton 1 943; Karamea 1 868. Not: Tablo satırları istasyon yüksekliği içermiyor (bu çıkarımda kontrol edilmedi); bazı istasyonlar yüksek dağ eteğinde olabilir.
- Doğu tarafı: NIWA Canterbury Climatology [B-ish, resmi PDF], https://niwa.co.nz/sites/default/files/Canterbury%20climate%20FINAL%20WEB_0.pdf (curl + pdftotext -layout; Tablo 6, 1981-2010 yıllık normal, mm/yıl): Arthur's Pass 4 642; Mt Cook Village 4 285; Methven 895; Akaroa 969; Castle Hill Village 967; Darfield 756; Culverden 576; Christchurch 618; Ashburton 681; Rangiora 688; Kaikoura 721; Waipara 620; Lake Tekapo 591; Tara Hills (Omarama) 506; Waimate 536; Timaru 550. Yerleşim satırı tablo düzenine göre (yıllık satır, sonra istasyon adı) eşlendi; el ile tekrar kontrol önerilir.
- Okuma: Batı (Franz Josef 5 751; Hokitika 2 732) ile doğu (Lake Tekapo 591; Christchurch 618; Omarama 506) arasında ~8-10 kat fark. Ama Mt Cook Village (Canterbury tarafı, ana sırtın doğusunda) 4 285 mm: gradyan yalnız batı-doğu değil, sırta ve yüksekliğe yakınlığa bağlı. Kesin mm/km gradyanı için istasyon mesafeleri gerekir; kaynaklı mesafe BULUNAMADI, bu yüzden hesaplanmadı.
- NIWA Canterbury ulusal özet (metin): "rainfall is highest along the main divide which has both high elevation and western exposure ... orographic enhancement."
- Milliman/Taiwan dışı: Te Ara/NIWA "Milford Sound almost 7 metres a year" (NIWA ders sayfası, arama özeti, sayfa okunmadı).

## 3. Denudasyon hızları (Taiwan, Yeni Zelanda, Yeni Gine; Milliman & Syvitski 1992)
- Milliman & Syvitski 1992 [B], J. Geol. 100:525-544 (NAP yeniden basımı, https://nap.nationalacademies.org/read/1992/chapter/7 — curl ile alındı, oku.py ile metne çevrildi): "Analysis of data from 280 rivers ... sediment loads/yields are log-linear function of basin area and maximum elevation." Küçük dağlık nehirler: "greatly underestimated in previous global sediment budgets, perhaps by as much as a factor of three." Yüksek adalar (Oceania) için: "yields for rivers draining Oceania are probably ≥3000 t/km2/yr" (metin, Milliman & Meade 1983'ün 1000 t/km2/yr varsayımına karşı).
- Milliman & Syvitski 1992 [B], aynı metin: "mountainous rivers with basin areas of about 10,000 km2 have sediment yields between 140 and 1700 t/km2/yr." Dağlık: "high mountain (headwaters >3000 m), mountain (1000-3000 m)" sınıfları. Küçük ada için: "a small island with elevations of 800-900 m probably should be considered mountainous."
- Milliman & Syvitski 1992 [B], aynı metin: alan <4000 km2'de artış trendi "less pronounced"; "Some very small rivers in New Zealand and Taiwan ... have yields much lower than expected, while others have much higher yields." (Taiwan/NZ'de saçılma var.)
- Dadson et al. 2003, Nature 426:648-651 [B], https://www.nature.com/articles/nature02150 (curl+oku.py): "Estimated erosion rates within the actively deforming mountains are high (3-6 mm yr-1) on all timescales." Aynı özette: "The highest erosion rates are found where rapid deformation, high storm frequency and weak substrates coincide, despite low topographic relief." (Relief ile aşınma ilişkisinin zayıf olduğunu gösterir.)
- Yeni Zelanda ve Yeni Gine denudasyon hızları: henüz BULUNAMADI (bkz. arama notları).

## 4. Orografik yağış ve yağmur gölgesi (Güney Alpleri)
- (bekliyor)

## 5. Adaların kıyı ova oranı
- (bekliyor)

## Çelişkiler
- (henüz yok)

## Kaynak listesi
- (bekliyor)
