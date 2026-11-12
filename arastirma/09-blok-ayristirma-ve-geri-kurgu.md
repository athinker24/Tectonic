# 9. Blok ayrıştırma ve geriye sürme

Araştırma tarihi: 12 Kasım 2026. Belge üç Haiku kolunun sentezidir (A geri kurgu yöntemleri, B hızlar ve zaman ölçekleri, C blok ayrıştırma ve maliyet); sentezi ben yazdım. Ham notlar `arastirma/notlar/09/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** yalnızca özet okundu, **[Ö]** arama özeti ya da ikincil kaynak, doğrulanamadı, **[E]** ansiklopedi, **[H]** bizim hesabımız ya da çıkarımımız, **[Y]** bulunamadı.

Dürüst durum: bu konuda tam metin okunan kaynak çok az. Okunanlar: Müller ve diğerleri 2019 (Tectonics), Müller ve diğerleri 2022 (Solid Earth), Torsvik ve diğerleri 2012 (Earth-Science Reviews), Gurnis ve Yang 2018. Hız ve zaman ölçekleri (B kolu) tamamen özet düzeyinde kaldı. Aracın en kritik ihtiyacı olan "bu blok boyutu, bu hız ve bu süre makul mü" sorusunun kaynaklı yanıtı bu nedenle sınırlı; aşağıdaki varsayılanlar aralıktır.

## Kısa sonuç

**1. Kıtalar rijit değil, ve rijit model örtüşme ve boşluk üretir.** Müller ve diğerleri (2019): rijit levha modeli kıta içi deformasyonu yok sayar; dağıtılmış deformasyon alanı tepe değerinde yaklaşık 30 milyon km² (geç Jura, yaklaşık 160 ile 155 milyon yıl önce) ve yaklaşık 48 milyon km² (geç Eosen, yaklaşık 35 milyon yıl önce), orta Kretase'de yaklaşık 10 milyon km² [B]. Pangea parçalanmadan önce (240 milyon yıl) kıta alanı yaklaşık 198, bugün yaklaşık 220 milyon km² (yüzde 10 artış) [B]. Gordon (1998): dağınık deformasyon yeryüzü yüzeyinin yaklaşık yüzde 15'i [Ö]. Aracın kıtasal blokları bu yüzden rijit ama aralarında deformasyon bantları (sütur) olmalı.

**2. Geri kurgunun standart girdileri var, ters problem formülü yok.** Euler kutbu ve dönme açısı zamana bağlı; kıyılar ya da kontur (Bullard, Everett ve Smith 1965: 500 kulaç konturu en iyi uyumu verdi, kıyı çizgisi değil [Ö]); en küçük kareler (Hellinger 1981 [Ö]). "Kıyılar sabit, geçmiş blokları bul" biçiminde bir ters problem için yayımlanmış bir yöntem bulunamadı [Y]; araç bunu kendi tasarlamak zorunda.

**3. Levha hızları geniş bir aralıkta ve ani değişebilir.** Okyanusal levhalar kıtasallardan 2 ile 3 kat hızlı (Zahirovic ve diğerleri 2015, özet, [Ö]). Hindistan 18 cm/yıl'ın üstündeki hızdan çarpışmada yaklaşık üçte bire düştü (yaklaşık 50 milyon yıl önce, NGEO725 özeti, [Ö]). Müller ve diğerleri (2022) kıtasal hızı 60 mm/yıl ile sınırlıyor [B].

**4. Mutlak referans çerçevesi seçimi belirsizliği artırır.** Hibrit çerçeve: 100 milyon yıldan gençte sıcak nokta, 200 ile 100 milyon yılda paleomanyetizma (Müller ve diğerleri 2016, özet [Ö], 2019 güncellemesi [B]). Aracın kendi hayali gezegeninde gerçek bir mutlak çerçeve yok; göreli hareket yeterli.

## 1. Geri kurgu yöntemleri ve modeller

| Model | Kapsam | Not | Etiket |
|---|---|---|---|
| Müller ve diğerleri 2016, Annu. Rev. Earth Planet. Sci. 44:107 ile 138 ("Ocean Basin Evolution and Global-Scale Plate Reorganization Events Since Pangea Breakup", doi 10.1146/annurev-earth-060115-012211) | Trias'tan bugüne, sürekli kapanan levha poligonları | mutlak çerçeve hibrit | [B-öz] |
| Müller ve diğerleri 2019, Tectonics 38:1884 ile 1907 (doi 10.1029/2018TC005462) | yaklaşık 240 milyon yıl, rift ve orojenlerde deforme litosfer | v2.0 çerçeve ağırlıkları yaşa göre değişiyor (0 ile 80 milyon yılda TR = NR = HS = 1; 170 ile 250 milyon yılda NR = 0,2) | [B ve Ö] |
| Müller ve diğerleri 2022, Solid Earth 13:1127 ("tectonic-rules-based mantle reference frame") | | net dönme 0,25 °/milyon yıldan az; kıtasal hız 60 mm/yıl'dan az | [B] |
| Matthews ve diğerleri 2016, Global Planet. Change 146:226 ile 250 | 410 milyon yıldan bugüne | tepe levha hızı 365 milyon yıl önce | [Ö] |
| Merdith ve diğerleri 2021, Earth-Sci. Rev. 214:103477 | 1000 milyon yıldan bugüne, paleomanyetik çerçeve | | [Ö] |
| Gurnis ve diğerleri 2012, Comput. Geosci. 38:35 ile 42 | sürekli kapanan levha (CCP) poligonları: poligon zaman içinde geometrik olarak kapalı kalır, 140 milyon yıldan bugüne küresel örnek | GPlates boşlukları otomatik çizgilerle dolduruyor (Gurnis ve Yang 2018 [B]) | [B-öz ve B] |

Müller 2016 için promptumdaki "Annual Review 2022" ve "Müller 2019 Annual Review" ifadeleri yanlıştı: 2016 makalesi Annual Review'da, 2019 makalesi Tectonics'te, 2022 makalesi Solid Earth'te.

Hellinger (1981, JGR 86:9312 ile 9318): ağırlıklı en küçük kareler ile Euler kutbu belirsizlik bölgesi [Ö]. Güven bölgesi formülleri ve TPW (gerçek kutup gezinmesi) düzeltmesi bulunamadı [Y]. Buffan ve diğerleri (2023): beş küresel model karşılaştırması, model seçimi yaşla birlikte belirsizliği artırıyor [Ö].

## 2. Hızlar ve zaman ölçekleri

| Konu | Değer | Etiket |
|---|---|---|
| Okyanusal levha / kıtasal levha hız oranı | 2 ile 3 kat | [Ö] |
| Küresel levha hızı | medyan yaklaşık 4 cm/yıl, en hızlı yaklaşık 8,5 cm/yıl (15 cm/yıl üstü yaklaşık 10 milyon yıl için model artefaktı) | [Ö] |
| Hindistan | 18 cm/yıl'ın üstü, çarpışmada (yaklaşık 50 milyon yıl önce) yaklaşık üçte bire düştü; 1978 paleomanyetik ortalama 14,9 cm/yıl (70 ile 40 milyon yıl) sonra 5,2 cm/yıl; kısa hızlanmalar yaklaşık 130, 80, 65 milyon yıl önce | [Ö] |
| Arabistan | yaklaşık 5 milyon yıldan beri yaklaşık yüzde 30 yavaşlama (Austermann ve Iaffaldano 2013, Zagros nedeni); ArRajehi (2010) buna karşı; bugün yaklaşık 18 mm/yıl | [Ö] |
| Slab çekişi | levha itkisinin yaklaşık yarısı (Conrad ve Lithgow-Bertelloni 2002, Science 298:207) | [Ö] |
| Hendek geri çekilmesi | Tonga yaklaşık 16 cm/yıl, Lau açılması yaklaşık 15 cm/yıl; İzu-Bonin kuzeyi 2 ile 6; Mariana birkaç cm/yıl (bu hız sayıları arama özetlerinden; kaynağı doğrulanamadı, Schellart 2008'e ait değil). Schellart 2008, GSA Bull. 120:1441 yalnızca korelasyon veriyor: hendek hızı korelasyonu 0,33 ile 0,68; geri çekilme genellikle genişlemeyle, sabit ya da ilerleyen hendek kısalmayla ilişkili (üst levha kısalması ve genişlemesi, And parametrik çalışması; hız sayısı yok) | [Ö] |
| Atlantik açılma örnekleri | Orta Atlantik yaklaşık 134 ile 126 milyon yıl, Güney Atlantik yaklaşık 112 milyon yıl; Pangea kırılması Jura başı (200 ile 175 milyon yıl) | [Ö] |
| Hindistan kat ettiği yol | 70 milyon yılda yaklaşık 8,6 cm/yıl, 130 milyon yılda yaklaşık 4,6 cm/yıl (varsayımsal çıkarım, kendi hesabım) | [H] |

Wilson döngüsü süresi için tek bir kaynaklı değer bulunamadı [Y]. Wilson (1966, Nature 211:676 ile 681) kavramsal, sayısal süre yok; adlandırma yılı 1973, 1974 ve 1975 olarak farklı yerlerde geçiyor. Gerya'nın 2014 Gondwana Research makalesi (25:442 ile 463) Wilson döngüsünden söz etmiyor; promptumdaki bu atıf yanlıştı.

## 3. Kıtanın bloklara bölünmesi

**Gerçek örnekler.**

- Metcalfe (2013), J. Asian Earth Sci. 66:1 ile 33: üç Tetis faz: Paleo-Tetis (Devoniyen ile Trias), Meso-Tetis (geç erken Permiyen ile geç Kretase), Ceno-Tetis (geç Trias ile geç Kretase) [B-öz]. Ayrılan bloklar: Devoniyen'de Kuzey Çin, Tarim, Güney Çin, Hindiçin; Permiyen sonunda Cimmeriyen bloklar; geç Trias ile geç Jura'da Lhasa; Kretase'de Sundaland [Ö]. Tam metin okunmadı.
- Torsvik ve diğerleri (2012), Earth-Sci. Rev. 114:325 ile 368: Kaledoniyen orojenezinden (430 ile 420 milyon yıl önce) sonra Laurentia ve Baltica'nın görünür kutup gezinti yolları Laurussia yolu olarak birleşir; Laurussia ile Sibirya verisi geç Permiyen'den itibaren Laurasia'da birleşir [B].
- Hindistan Asya çarpışması yaklaşık 70 milyon yıl önce (Yin ve Harrison 2000, ikincil özet [Ö]); Baltica ile Avalonia yaklaşık 443 milyon yıl önce (Cocks ve Torsvik 2005 [Ö]).
- Bulunamayanlar: Qiangtang ile Lhasa kenet yaşı, Tarim ile Kuzey Çin birleşme tarihi, Kazakhstania çarpışma zamanı [Y].

**Blok sayısı ve boyutu.** Kıta kabuğu alanı yaklaşık 150 ile 220 milyon km² (kaynaklar çelişiyor: 198 ve 220, Müller 2019; 150 ile 210 diğer kaynaklarda). Kraton alanları için ve "10^5 ile 10^7 km²" blok boyutu aralığı için kaynak bulunamadı [Y]. Blok sayısı (yaklaşık 15 ile 2200) yalnızca bölme aritmetiğidir (alan bölü blok boyutu); literatür iddiası değil, modelleme varsayımıdır [H].

**Sütur ve geçmiş okyanus genişliği.** Erzincan kuşağı yaklaşık 40 km kalınlıkta bir bindirme kuşağı, okyanus genişliği değil; mélanj genişliği okyanus genişliğinin zayıf bir vekili [Ö]. Vardar için 3000 km'yi aşan tomografi tahmini yalnızca özet düzeyinde ve doğrulanmadı [Ö]. Van der Meer ve diğerleri (2018, Atlas of the Underworld): 94 slab kalıntısı, "dalma bölgesi uzunluğu karşı derinlik" hesabı; okyanus genişliği formülü bulunamadı [B-öz ve Y].

**Yazılım ve segmentasyon.** pyGPlates, GPlately, paleo-yaş ızgaraları ve gptools bulundu [Ö]. "paleoplate", "BEST-FIT" ve "Reconstruction Tool" adlı doğrulanmış yazılım bulunamadı [Y]. Otomatik blok bölme: ADOPT (su bölümü, watershed), Platerecipy (Random Walker ile Euler vektörü rijitlik testi), GNSS hızlarının Euler vektör uzayında kümelenmesi [Ö]. Voronoi ve jeolojik harita segmentasyonu için kaynak bulunamadı [Y].

## 4. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Blok modeli | rijit bloklar, aralarında deformasyon bantları | [B] |
| Kıtasal hız üst sınırı | 60 mm/yıl (Müller 2022 kuralı) | [B] |
| Tipik kıtasal levha hızı | 1 ile 8 cm/yıl; okyanusal levhalar 2 ile 3 kat hızlı | [Ö] |
| Çarpışma sonrası yavaşlama | hızın yaklaşık üçte birine düşmesi (Hindistan), %30 (Arabistan) | [Ö] |
| Hız değişimi | ani değişimler olası (Hindistan 130, 80, 65 milyon yıl önce); ivme kısıtı kaynaksız | [Ö ve Y] |
| Hendek geri çekilmesi | 2 ile 16 cm/yıl | [Ö] |
| Blok sayısı | tasarım seçimi; 5 ile 30 başlangıç aralığı önerilir | [H] |
| Referans çerçeve | göreli hareket yeterli (hayali gezegende mutlak çerçeve gereksiz) | [H] |
| Kıta alanı kaybı/kazancı | geri kurgu sırasında alan korunmalı; model kıta alanını bugünkü %10 aralığında tutsun | [B] |
| Çakışma/boşluk | sürekli kapanan poligonlar; deformasyon bantları boşluğu doldursun | [B] |

Not: 60 mm/yıl üst sınırı gerçek Dünya'nın kıtasal levhaları için; hayali gezegende aynı fiziksel hız ölçeğini kullanmak bir tasarım seçimi ve karar günlüğünde belirtilmeli.

## 5. Kaynaklar arası çelişkiler

- Hindistan yavaşlama zamanı: 50, 44, 55 ile 40 milyon yıl önce. Kretase tepe hızı: 18 cm/yıl ile yaklaşık 20 cm/yıl.
- Arabistan yavaşlamasının nedeni: Zagros orojenezi (Austermann ve Iaffaldano) ile çarpışma direncinin etkisiz olduğu (ArRajehi).
- Pangea kırılma tarihi: 200 ile 175 milyon yıl önce, Güney Atlantik 140 ile 130 ya da 120 milyon yıl önce (eğitim siteleri).
- Kıta alanı: 150, 198, 210, 220 milyon km².
- Wilson döngüsü adlandırma yılı: 1973, 1974, 1975.
- Forsyth ve Uyeda (1975) ile Hager (1983) levha itkisi katkıları.

## 6. Bulunamayanlar ve doğrulanamayanlar

- Alan korunumlu yeniden kurgu tanımı; TPW düzeltme formülü; Hellinger ve Chang güven bölgesi formülleri; Merdith 2021 ve Matthews 2016 model hata payları; "ters problem" çerçevesi.
- Zahirovic ve diğerleri (2015) ve Gibbons (2015) tam metinleri (earthbyte PDF 404, ScienceDirect bot koruması; atlatılmadı); Forsyth ve Uyeda (1975) tablosu; Burke (1976); Cocks ve Torsvik 2005 ve 2011, Torsvik ve Cocks 2017 (indirilmedi).
- Qiangtang-Lhasa, Tarim-Kuzey Çin, Kazakhstania yaşları; kraton alanları ve blok boyutu dağılımı; ofiyolit ve mélanj genişlikleri; Voronoi ve harita segmentasyonu.
- Müller 2016 ve Metcalfe 2013 tam metinleri okunamadı (DOI 403); Van der Meer 2018 dergi makalesi sayısal içerik vermedi.
- Hız ve zaman ölçekleri bölümü tümüyle özet düzeyinde.

## 7. Promptumdaki hatalar (düzeltildi)

- "Müller 2016 closed plate polygons, Annual Review" doğru: Annu. Rev. Earth Planet. Sci. 44:107. "Müller 2019 Annual Review" yanlış (Tectonics). "Müller 2022 Annual Review" yanlış (Solid Earth 13:1127).
- "Gerya 2014 Wilson döngüsü" atfı doğrulanamadı; bulunan makale Wilson döngüsünden söz etmiyor.
- "Tectonic Reconstruction Software 'Reconstruction Tool'", "paleoplate", "BEST-FIT" doğrulanmış yazılım olarak bulunamadı.
- "10^5 ile 10^7 km² tipik blok boyutu" kaynaksız, benim varsayımım.
- "Burke 1976" Wilson döngüsü atfı bulunamadı.

## Başlıca kaynaklar

- Müller ve diğerleri 2019, Tectonics: https://doi.org/10.1029/2018TC005462
- Müller ve diğerleri 2016, Annu. Rev.: https://doi.org/10.1146/annurev-earth-060115-012211 (özet: https://www.earthbyte.org/?p=4306)
- Müller ve diğerleri 2022, Solid Earth 13:1127: ham notlardaki bağlantı
- Gurnis ve diğerleri 2012: https://doi.org/10.1016/j.cageo.2011.04.014
- Torsvik ve diğerleri 2012, Earth-Sci. Rev. 114:325: ham notlardaki bağlantı
- Metcalfe 2013, JAES 66:1 (özet)
- Tam liste ve her bilginin kaynağı `arastirma/notlar/09/` içinde.
