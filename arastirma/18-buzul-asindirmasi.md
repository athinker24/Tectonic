# 18. Buzul aşındırması (düşük öncelik)

Araştırma tarihi: 12 Kasım 2026. Belge tek bir Haiku kolunun notlarının sentezidir; sentezi ben yazdım. Ham notlar `arastirma/notlar/18/A_buzul.md` içinde. Etiketler: **[B]** tam metin ya da tam özet okundu, **[Ö]** arama özeti, doğrulanamadı, **[H]** bizim çıkarımımız, **[Y]** bulunamadı. Bu konu düşük öncelikli olduğu için kısa tutuldu; kaynak sayısı az ve sayılar eksik.

## Kısa sonuç

**1. Buzul aşınma kanununda üs kaynaklarda tutarsız.** E = K_g · u_s^l biçiminde yazılıyor; Herman ve diğerleri (2015, Science 350(6257):193 ile 195) erozyon oranının kayma hızının karesiyle orantılı olduğunu bildirdi (l = 2) [B, özet]. 38 buzulluk bir derleme ise l = 0,69 buldu ve aynı kayma hızında erozyonun 100 kata kadar değiştiğini yazıyor [Ö]. Yaygın modelleme aralığı 1 ile 2, bazı modellerde 4'e kadar [Ö]. K_g değeri bulunamadı [Y].

**2. "Buzul testeresi" (glacial buzzsaw) tartışmalı.** Egholm ve diğerleri (2009, Nature 460:884 ile 887, doi 10.1038/nature08263): en yüksek dağ yüksekliği kar çizgisi gradyanıyla ilişkili; model kayma erozyonu ve izostatik yükselmeyle yüksekliği kar çizgisinin hemen altına çekiyor [B]. Pireneler ve Norveç'te eleştiri var, sayısal eşik yok [B, ansiklopedi]. Brozović ve diğerleri (1997): tepe yükseklikleri denge hattı irtifasının 1 km'den fazla üstüne çıkabiliyor [Ö, ikincil]. Gjermundsen ve diğerleri (2015, Nature Geoscience 8:789 ile 792): Svalbard'da zirveler en az 1 milyon yıl korunmuş, buzul erozyonu kısıtlı [B].

**3. Aracın bu sürümde buzul aşındırmasını modellememesi tutarlı bir tercih.** Landlab'da buzul erozyon bileşeni yok, Fastscapelib'de buzul modülü bulunamadı [Ö ve Y]. iSOSIA (Egholm ve diğerleri 2011, JGR 116:F02012) dik arazi için derinlik-entegre ikinci derece buzul modeli; GMD 2023 OpenLEM ile karşılaştırması mevcut [Ö]. PISM maliyeti ve Actions uyumu aranmadı [Y]. Bu sürümde buzul etkisi, yüksek enlemde ve yüksek tepelerde bir tavan ve U vadi biçimi olarak sonradan eklenebilir [H].

## 1. Biçimler: fiyort, U vadi, sirk

- Sognefjord: en büyük derinlik 1308 m (kaynaklar 1303 ile 1309 arasında), 1000 m'den derin kısım yaklaşık 100 km, uzunluk 205 km [B, ansiklopedi].
- U vadi genişlik ve derinliği ile sirk boyutları için sayısal aralık bulunamadı [Y]; Graf (1970) form oranı tanımı var ama aralık yok [Ö].

## 2. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Buzul aşınma üssü l | 1 ile 2 (Herman 2015: 2); 38 buzulluk derleme (Cook ve diğerleri 2020, tam metin): l = 0,69 yalnızca Meserve buzulu dahilken, hariçken l = 0,65 | [B] |
| Aşınma hızı belirsizliği | aynı kayma hızında 100 kata kadar | [Ö] |
| Maksimum yükseklik | denge hattı irtifasının hemen altı, ama zirveler denge hattının 1 km üstüne çıkabilir (Brozović 1997 ikincil alıntı; Egholm 2009 basın yazısı yaklaşık 1500 m diyor, tam metin okunamadı) | [B ve Ö] |
| Fiyort derinliği | Sognefjord örneği 1308 m, uzunluk 205 km | [B] |
| Model | bu sürümde yok; sonradan işlenir | [H] |

## 3. Bulunamayanlar ve doğrulanamayanlar

- Herman 2015 K_g ve ek malzemesi (aab2386-Herman-SM.pdf); Egholm 2009 yöntem bölümü ve model K_g, l değerleri; buzul testeresi sayısal eşiği; U vadi ve sirk boyut aralıkları; PISM maliyeti ve Actions uyumu; Landlab / Fastscapelib buzul modülü.
- WebFetch en.wikipedia.org, www.nature.com, www.pubmed.gov için DNS hatası verdi; curl ile devam edildi, bot korumasına müdahale edilmedi. pubmed.ncbi.nlm.nih.gov çerez duvarı nedeniyle metin vermedi.
- Atlasın buzul katmanıyla ilişki bu araştırmada ele alınmadı (24. konu).

## Başlıca kaynaklar

- Herman ve diğerleri 2015: https://resolver.caltech.edu/CaltechAUTHORS:20150929-080354449
- Egholm ve diğerleri 2009: https://www.nature.com/articles/nature08263
- Gjermundsen ve diğerleri 2015: https://www.nature.com/articles/ngeo2524
- Glacial buzzsaw: https://en.wikipedia.org/wiki/Glacial_buzzsaw ; Sognefjord: https://en.wikipedia.org/wiki/Sognefjord
- 38 buzulluk derleme: https://pmc.ncbi.nlm.nih.gov/articles/PMC7005307
- Tam liste ve her bilginin kaynağı `arastirma/notlar/18/` içinde.
