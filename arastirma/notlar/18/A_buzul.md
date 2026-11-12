# A: Buzul aşındırması (düşük öncelik, kısa)

Durum: KISMİ TAMAMLANDI (düşük öncelik, kısa tutuldu). Kaynaklar İngilizce; notlar Türkçe.

Etiketler: [B] tam metin (erişilen kısım) / [B-öz] özet / [Ö] arama özeti. ERİŞİLEMEDİ: DNS hatası veren ana alan adları. BULUNAMADI: değer bulunamadı.

Ağ notu: WebFetch denemelerinde en.wikipedia.org, www.nature.com ve www.pubmed.gov DNS hatası verdi. Bunun üzerine curl (proxy) + oku.py yolu kullanıldı. pubmed.ncbi.nlm.nih.gov curl ile açıldı ama çerez duvarı nedeniyle metin çıkmadı. Nature için nature.com/articles/... adresleri curl ile açıldı (abstract ve kaynakça kısmı, yöntem bölümü yok). Wikipedia için en.wikipedia.org curl ile açıldı.

## 1. Buzul aşınma kanunu E = K_g · u_s^l

- Kanun biçimi: E = K_g · U_s^l; K_g kayaç erodibilite sabiti, l genelde 1 ile 2 arası. [Ö] "The exponent l is usually taken to be between one and two, though values up to four have appeared in models, depending on K_G." Kaynak: https://www.nature.com/articles/s41467-020-14583-8 (arama özeti, tam metin değil) [Ö]
- l = 1 (Hallet 1979 önerisi): doğrusal hal hâlâ yaygın. Kaynak: https://esurf.copernicus.org/preprints/esurf-2021-1/esurf-2021-1.pdf [Ö]
- Herman ve diğ. 2015, "Erosion by an Alpine glacier", Science 350(6257): 193-195. Özet tam metin olarak alındı [B]. Cümle: "We demonstrate that the glacial erosion rate is proportional to the ice-sliding velocity squared". Yani l = 2. Kaynak: https://resolver.caltech.edu/CaltechAUTHORS:20150929-080354449 [B]
- Herman 2015 için K_g sayısal değeri: BULUNAMADI (özette yok; tam makale erişilemedi). Bir basın özeti E = K·V² biçimini veriyor ve V'nin m/gün cinsinden olabileceğini söylüyor; bu ikincil ve birim doğrulanmadı [Ö]. Ana kaynak DOI 10.1126/science.aab2386; ek malzeme aab2386-Herman-SM.pdf (Caltech kaydında). Bu ek belge bir sonraki adımda çekilmeli.
- Herman ve Koppes ve diğ. (2015) benzer üs veriyor, K_g değerleri de birbirine yakın (ikincil kaynak). Kaynak: https://meetingorganizer.copernicus.org/EGU2016/EGU2016-14074.pdf [Ö]
- Karşı veri: 38 buzulluk bir derlemede l = 0,69 bulundu (bir aykırı değer dahil). Aynı derlemede aynı kayma hızında erozyon oranı 100 kata kadar değişiyor. Kaynak: https://pmc.ncbi.nlm.nih.gov/articles/PMC7005307 [Ö]

### Egholm ve diğ. 2009, "Glacial effects limiting mountain height", Nature 460: 884-887, doi:10.1038/nature08263 [B]

- Özet tam metin olarak alındı. Ana bulgu: maksimum dağ yüksekliği, kar çizgisi (snowline) yüksekliğindeki iklim kaynaklı gradyanlarla yakından ilişkili. Cümle: "driving elevations towards an altitude window just below the snowline". Kaynak: https://www.nature.com/articles/nature08263 [B]
- Mekanizma: kar çizgisi üstünde buzul kayması ile erozyon, buna eşlik eden izostatik yükselme. Kaynak aynı. [B]
- Model K_g ve l değerleri: BULUNAMADI (erişilen metin özet ve kaynakça; yöntem bölümü yok). Kaynakça SOSIA ve Budd ve diğ. (1979) gibi kayma yasası referanslarını içeriyor [B].
- Denge hattı (ELA) ile maksimum yükseklik ilişkisi Egholm'de kar çizgisi olarak ifade ediliyor. Sayısal bir "ELA + X m" bağıntısı: BULUNAMADI.
- Brozović, Burbank, Meigs 1997, "Climatic limits on landscape development in the northwestern Himalaya", Science 276: 571-574. Makale metni erişilmedi; bulgular ikincil kaynaklardan [Ö]. Tepe yükseklikleri ELA'nın 1 km'den fazla üstüne çıkabiliyor; ortalama ve modal yükseklikler geç Pleistosen ELA'sını izliyor. Kaynak: arama özeti, bkz. https://www.nature.com/articles/nature08263 (atıf) [Ö]
- Mitchell ve Montgomery 2005 ve Crest ve diğ. gibi sonraki testler karışık sonuç veriyor; 2003 ABD çalışması ELA-yükseklik ilişkisinin maksimum yüksekliğe daha yakın olduğunu bildiriyor [Ö].

### Glacial buzzsaw (Wikipedia) [B]

- Tanım: Sıcak tabanlı buzulların erozyonunun dağ yüksekliğini belli bir eşiğin altında tuttuğu hipotez. Büyük dağ kütlelerinin ELA'ya doğru düzleştiği ve ELA'nın "iklimsel taban seviyesi" olarak işlediği ileri sürülüyor. Kaynak: https://en.wikipedia.org/wiki/Glacial_buzzsaw [B]
- Küçük buzulların ELA altına çoğunlukla inebildiği, büyük vadi buzullarının ELA'yı aşabildiği ve buzzsaw etkisine katkı yapmadığı belirtiliyor. Patagonya buz tarlası buzzsaw olmadığı için hızlı tektonik yükselme gösteriyor. [B]
- Eleştiri: Pireneler'de ölçülen erozyon oranları genel bir seviyeye yönelim göstermiyor (Crest ve diğ. 2017). Norveç'te paleik yüzey adım adım seviyeler gösteriyor, buzzsaw ile tam uyuşmuyor (Hall ve diğ. 2013). [B]
- Wikipedia bu konuda sayısal eşik vermiyor: BULUNAMADI.

### Svalbard karşıt kanıt: Gjermundsen ve diğ. 2015, Nature Geoscience 8: 789-792, doi:10.1038/ngeo2524 [B]

- 10Be ve 26Al ile 8 zirve: en az son 1 milyon yıl korunmuş. Sonuç: buzul erozyonu Arktik'te verimsiz ve buz akıntılarıyla sınırlı; yüksek relief alpin peyzajlar "minimally erosive glacier armour" ile korunmuş. Kaynak: https://www.nature.com/articles/ngeo2524 [B]

## 2. U vadiler, sirkler, fiyortlar

- Sognefjord maksimum derinlik: 1308 m (4291 ft); en derin kısım Høyanger civarı merkezi kesimde. Norveç'in en uzun ve en derin fiyordu; uzunluk 205 km. Kaynak: https://en.wikipedia.org/wiki/Sognefjord [B]
- Sognefjord 1000 m'den derin, yaklaşık 100 km boyunca (Rutledal - Hermansverk). Ağızda ~100 m derinlikte bir eşik var. Kaynak aynı [B]
- Sayısal ayrım: bazı kaynaklar 1309 m veya 1303 m veriyor; 1200 m veren kaynak da var (ikincil, [Ö]).
- U vadi genişliği ve derinliği tipik değerleri: BULUNAMADI. Arama özetinde Graf (1970) "U-shape" tanımı ve form oranı (derinlik/genişlik) bahsediliyor, ama sayısal aralık yok. [Ö]
- Yeni Zelanda'da 37 vadi, ~400 bin yıl buzul işgali sonrası U şekli oluşuyor. Kaynak: arama özeti [Ö].
- Sirk boyutu: BULUNAMADI.

## 3. Buzul modelleri

- iSOSIA: Egholm, Knudsen, Clark, Lesemann (2011), "Modeling the flow of glaciers in steep terrains: The integrated second-order shallow ice approximation (iSOSIA)", J. Geophys. Res. 116, F02012. Derinlik-entegre, dik arazide uzunlamasına ve enine gerilmeleri içerir. [Ö] Kaynak arama sonucu: https://openpolar.no/Record/ftdatacite:10.5880%2Ffidgeo.2020.032 ve GMD 2023 karşılaştırması: https://gmd.copernicus.org/articles/16/1315/2023/gmd-16-1315-2023.html [Ö]
- OpenLEM vs iSOSIA benchmark (GMD 2023): akış desenleri benzer, kenarlarda vadi yan yüzeylerinde OpenLEM daha yüksek erozyon veriyor. [Ö]
- PISM: BULUNAMADI (bu oturumda aranmadı).
- SIA yaklaşımı: iSOSIA SIA'nın ikinci dereceden genişletmesi olarak tanımlanıyor [Ö].
- Hesap maliyeti ve GitHub Actions uyumu: BULUNAMADI (aranmadı).
- Landlab: "glacial erosion" veya buzul bileşeni arandı; sonuç yok. Landlab'ın fluvial bileşenleri (stream power, SPACE, ErosionDeposition) var. Buzul bileşeni: BULUNAMADI. Kaynak: https://landlab.readthedocs.io/en/latest/tutorials/landscape_evolution/erosion_deposition/erosion_deposition_component.html [Ö]
- Fastscapelib: buzul modülü: BULUNAMADI (aranmadı; önceki incelemelerde scratchpad içinde fastscape ile ilgili dosyalar mevcut, ama bu görevde doğrulanmadı).

## 4. Atlas verisi ilişkisi

- Bu araştırmada buzul-atlas ilişkisi yok. Atlasın buzul katmanı varsa 24. konuda ele alınacak.

## Açık kalanlar

- Herman 2015 tam metin (K_g değeri, sayısal sonuçlar): PubMed çerez duvarı nedeniyle erişilemedi.
- Egholm 2009 yöntem bölümü (K_g, l, kullanılan değerler): erişilemedi.
- Brozovic 1997 (ELA-maksimum yükseklik): henüz doğrulanmadı.
- U vadi ve fiyort sayısal boyutları (genişlik, derinlik aralıkları): henüz bulunamadı.

## Kaynak listesi

1. Herman ve diğ. 2015, Science 350(6257): 193-195. https://resolver.caltech.edu/CaltechAUTHORS:20150929-080354449 [B]
2. Egholm ve diğ. 2009, Nature 460: 884-887. https://www.nature.com/articles/nature08263 [B]
3. Gjermundsen ve diğ. 2015, Nature Geoscience 8: 789-792. https://www.nature.com/articles/ngeo2524 [B]
4. Glacial buzzsaw, Wikipedia. https://en.wikipedia.org/wiki/Glacial_buzzsaw [B]
5. Sognefjord, Wikipedia. https://en.wikipedia.org/wiki/Sognefjord [B]
6. Nature Communications 2020 (38 buzul derlemesi). https://www.nature.com/articles/s41467-020-14583-8 [Ö]
7. Koppes ve diğ. / Herman EGU 2016 özeti. https://meetingorganizer.copernicus.org/EGU2016/EGU2016-14074.pdf [Ö]
8. iSOSIA ve OpenLEM karşılaştırması, GMD 2023. https://gmd.copernicus.org/articles/16/1315/2023/gmd-16-1315-2023.html [Ö]
