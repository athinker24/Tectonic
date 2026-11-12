# 3. İzostazi ve bükülme

Araştırma tarihi: 11 ve 12 Kasım 2026. Bu belge dört Haiku kolunun (esneme kuramı, aşınma ve çökelmeye izostatik tepki, hesap kodları, Airy sınaması) sentezidir; sentezi ben yazdım. Ham notlar `arastirma/notlar/03/` klasöründe, her bilginin kaynağı yanında. Dört notu baştan sona okudum. Esneme formüllerini kendim sayısal olarak denetledim: Te = 30 km için 1B sonlu fark çözümü, sürekli levha formüllerini tuttu (w0 oranı 1,0000; ön çıkıntı 330,2 km ve π α = 330,4 km; çöküntü derinliği oranı −0,0432; sıfır geçişi 248,2 km ve 3π α / 4 = 247,8 km). Kırık levha ve sürekli levha ön katsayılarını sınır koşullarından elle türetip kontrol ettim. Etiketler 2. belgedekiyle aynı:

- **[B]** Birincil makale ya da yetkili kaynak okundu, sayı orada.
- **[T]** Tek makalenin iddiası.
- **[Ö]** Arama özetinden alındı, doğrulanamadı.
- **[H]** Bizim hesabımız ya da türetmemiz.
- **[E]** Ansiklopedi düzeyi.
- **[Y]** Bulunamadı.

## Kısa sonuç

Dört bulgu, aracın izostazi katmanının biçimini belirliyor.

**1. Kabuk kalınlığına dayanan Airy kuralı tek başına yetmiyor.** Zoback ve Mooney (2003) 1700'den fazla sismik kabuk modelinde, deniz seviyesine yakın yerlerde kabuk kalınlığının 25 ile 55 km arasında değiştiğini ve yükseklikle basit bir ilişki olmadığını buldu [B]. Yalnızca kabuğa bakan model yükseklikleri yerlerin yüzde 97'sinde ortalama 1,73 ± 0,95 km fazla tahmin ediyor [B]. Litosfer mantosu terimi gerekli. Ama Airy artış olarak (kabuk kalınlaşınca yüzey ne kadar yükselir) işe yarıyor ve Tibet'i iyi tutturuyor. Alpler'i tutturmuyor.

**2. Düzeltilmiş Airy sayıları.** Kabuk kalınlaşması ΔT yüzeyi ΔT × (ρm − ρc) / ρm kadar, yani yaklaşık 0,15 ΔT yükseltir. Aynı çarpan aşınmada da geçerli: aşınan her km kaya, ortalama yüzeyi yaklaşık 0,15 km alçaltır, kayanın kendisi ise yaklaşık 0,85 km yükselir [B]. 2. belgede bu oran 0,18 olarak yazılmıştı; düzeltildi.

**3. Ön çukur, sabit kıyıda çökeltiyle dolu olmak zorunda.** Himalaya ön ülkesinde Hint tabanı yaklaşık 5 km bükülüyor ve bu çukur 1 ile 5 km çökeltiyle dolu [B]; Gang ovasının yüzeyinin deniz seviyesine yakın olması genel coğrafya bilgisi, bu turda kaynakla denetlenmedi. Kıyı sabit olduğu için karadaki her ön çukur "aşırı dolu" olmalı. Bu bir tasarım kısıtı ve erozyon motorunda çökelme gerektiriyor.

**4. Bükülmeyi hesaplamak ucuz, ama sürekli levha bu işe tam uymuyor.** Sabit Te'li FFT çözümü 2 milyon hücre için yaklaşık 0,1 saniye sürer [H, ekstrapolasyon]. Ama Lin ve Watts (2002) sürekli bir elastik levhanın Batı Tayvan havzasının hem genişliğini hem derinliğini birlikte açıklayamadığını gösterdi [B]. Gerçek ön çukurlar çoğunlukla "kırık levha" ya da gömülü yük modelleriyle daha iyi uyuyor [B]. Aracın hem sürekli hem kırık levha seçeneği olmalı.

## 1. Airy ve litosfer mantosu

### Temel bağıntılar

Airy dengesi (ρc = 2800, ρm = 3300 kg/m³): kök r = h × ρc / (ρm − ρc) = 5,6 h; toplam kalınlaşma h + r = 6,6 h; yüzey yükselmesi toplam kalınlaşmanın yaklaşık 0,15'i [B, MIT ders notu; Molnar ve England 1990; [H] hesap]. 2. belge Airy muhasebesini bu yönde düzeltti.

### Küresel sınama

Zoback ve Mooney (2003), Lachenbruch ve Morgan (1990) modeliyle [B]:

- Litosfer kolonu: kabuk (Lc, ρc) ve manto kapağı (Lm, ρm) astenosfer (ρa = 3300) üstünde yüzer. Kara yüksekliği ε = (ρa − ρL) / ρa × L − H0. H0 = 2,78 ± 0,35 km, orta okyanus sırtı kolonundan kalibre.
- Kabuk payı Hc = (ρa − ρc) / ρa × Lc − H0, manto payı Hm = (ρa − ρm) / ρa × Lm. ρc = 2800 ile yalnızca kabuk terimi için sıfır yükseklik kalınlığı 18,3 km çıkıyor ([H] türetme; bu fiziksel bir referans kalınlık değil, yalnızca kabuk terimi için sıfır noktası).
- Veri: ETOPO5'ten 50 km yarıçapında ortalanmış yükseklikler.
- Sonuçlar: "yükseklik ile kabuk kalınlığı arasında basit bir ilişki yok"; Airy tipi korelasyon yalnızca uçlarda (55 km'den kalın ya da 20 km'den ince kabuk). Kabuğun yoğunluğu kalınlıkla artıyor: 25 km'de 2764, 50 km'de 2947 kg/m³ (55 km'den kalınlarda tersine).
- Kraton manto kapağı sismik 200 ile 350 km kalınlığı ancak yaklaşık yüzde 1 daha hafif bir kapakla tutuyor [B].

Lamb ve diğerleri (2020) litosfer kalınlığının kıtasal yüksekliğin birinci dereceden denetleyicisi olduğunu söylüyor; sayıları arama özetinden [Ö].

### Tibet tutuyor, Alpler tutmuyor

| Bölge | Yükseklik | Gözlenen kabuk | Düzeltilmiş Airy (T0 = 35) | Etiket |
|---|---|---|---|---|
| Tibet | yaklaşık 5 km | yaklaşık 70 km (Himalaya'da yaklaşık 50, Qiangtang'da 90'a kadar) | yaklaşık 68 km | [B] |
| İran platosu | yaklaşık 1,5 km | 42 ile 50 km | yaklaşık 45 km | [B] |
| Alpler | yaklaşık 2 km | yaklaşık 55 ile 60 km | yaklaşık 48 km | [Ö] |

Alpler'in fazla kalın kökü dalan levha ve eklojit yoğunlaşmasıyla açıklanıyor; eklojitleşmenin 300 ile 600 kg/m³'e varan yoğunlaşma yapabileceği bir ikincil kaynaktan [Ö, üst sınır]. Bu yüzden aracın izostazi katmanı kökü yükseklikten türetmemeli; kökün yoğunluğu ve kalınlığı birer parametre olmalı.

### Varsayılan yoğunluklar

- Astenosfer ve manto kapağı: 3300 kg/m³ [B, Zoback ve Mooney].
- Kabuk: 2800 kg/m³ ve kalınlıkla artan (2764'ten 2947'ye) seçenek [B]. Küresel ortalama kabuk yoğunluğu 2830 [Ö].
- Su: 1030 kg/m³.
- Çökelti: 1700 ile 2500 kg/m³. Deniz çökeltisi için bir ikincil kaynak 1700 ile 1950 veriyor [Ö]; Lin ve Watts ön ülke dolgusu için 2500 kullanıyor [B]; gözenekliliğin derinlikle azalması (Sclater ve Christie 1980) çözümü olabilir [Ö]. Araştırma görevime yazdığım 2000 ile 2500 aralığı yerine bu geniş aralık daha doğru görünüyor.
- Ortalama kıta kabuğu kalınlığı 39 ile 41 km [Ö]. 2. belgedeki 35 km referans bir ders notundan, birincil bir kaynak değil.

### Dinamik topografya ve kratonlar

Dinamik topografya modellerde ± 2 km çıkıyor; gözlemlerde yaklaşık ± 1 km (yaklaşık 1000 km dalga boyunda) ve yaklaşık ± 500 m (10 000 km dalga boyunda) [B, Hoggard ve diğerleri 2016; Steinberger ve diğerleri 2019]. En uzun dalga boyunda model genliği gözlemin iki katından fazla. Araçta isteğe bağlı, varsayılan olarak kapalı bir terim; açılırsa en çok ± 0,5 km. Güney Afrika kratonları diğerlerinden 500 ile 700 m yüksek [Ö].

## 2. Esneme kuramı

### Formüller (uygulanabilir)

Varsayımlar: ince elastik levha, 2B silindirik eğilme (yük şerit boyunca sonsuz), doğrusal elastisite, küçük sapmalar, Winkler temeli (akışkan manto, viskoz gevşeme yok) [B].

- Esneklik sertliği D = E Te³ / (12 (1 − ν²)); E = 10^11 Pa, ν = 0,25 (Stewart ve Watts 1997 ile Lin ve Watts 2002 tablosu) [B].
- Esneklik parametresi α = [4D / ((ρm − ρdolgu) g)]^(1/4) [B, MIT 12.520].
- **Sürekli levha**, toplam çizgi yükü V0 (her yana yarısı): w(x) = w0 e^(−x/α) [cos(x/α) + sin(x/α)], w0 = V0 α³ / (8D). Sıfır geçişi 3π α / 4, ön çıkıntı konumu π α, çıkıntı genliği −0,0432 w0 [B; [H] sayısal denetim tuttu].
- **Kırık levha** (yük ucunda eğilme momenti sıfır), toplam yük V0 her yana yarısı: w(x) = w0 e^(−x/α) cos(x/α), w0 = V0 α³ / (4D). Sıfır geçişi π α / 2, ön çıkıntı konumu 3π α / 4, çıkıntı genliği −0,067 w0 [B; ön katsayılar [H] türetme].
- Genel ön katsayı (her yana uygulanan kesme kuvveti Vb): sürekli w0 = Vb α³ / (4D), kırık w0 = Vb α³ / (2D) [H].
- Yön: MIT'in gösteriminde aşağı doğru sapma negatif; araç elevasyona yazarken işareti çevirmeli.
- Toplam çöküntü hacmi: bütün x üzerinden w'nin integrali V0 / ((ρm − ρdolgu) g) [H, çizgi yükü için kütle dengesi]. Bu, aracın çökelti ihtiyacını kontrol etmek için kullanılabilir.

**Dikkat, üç kaynak karışıklığı:**

- "Ön çıkıntı 3π α / 4'te" sözü kırık levha için doğru; sürekli levhada 3π α / 4 sıfır geçişi, ön çıkıntı π α. Literatürdeki kısaltma belirsiz [B].
- NCU ders notundaki kırık levha ön katsayısı sürekli levhadakinin dört katı görünüyor, MIT ve bizim türetmemiz iki kat veriyor. Fark yük tanımından: NCU'da sürekli levha için P toplam yük, kırık levha için P her yarının ucundaki yük. Aynı toplam yük için iki kat çıkıyor ([H], çözüldü).
- α'nın tanımı kodlar arasında farklı. gFlex 2B için α = (D / (Δρ g))^(1/4) kullanıyor; yukarıdaki 1B tanımın 4^(1/4) = 1,41 katı kadar küçük. Te = 30 km için gFlex α yaklaşık 47 km (E = 65 GPa ile; [B], C notları), bizim 1B α yaklaşık 105 km (E = 10^11 ile). Farkın bir kısmı E'den, bir kısmı tanımdan.

### Te, α ve ön çıkıntı konumu

E = 10^11, ν = 0,25, ρm = 3300, ρdolgu = 2500 [H]:

| Te (km) | D (N m) | α (km) | sürekli sıfır geçişi (km) | sürekli ön çıkıntı (km) |
|---|---|---|---|---|
| 5 | 1,1 × 10^21 | 27,4 | 64,6 | 86,2 |
| 10 | 8,9 × 10^21 | 46,1 | 108,7 | 144,9 |
| 20 | 7,1 × 10^22 | 77,6 | 182,8 | 243,8 |
| 30 | 2,4 × 10^23 | 105,2 | 247,8 | 330,4 |
| 40 | 5,7 × 10^23 | 130,5 | 307,5 | 410,0 |
| 60 | 1,9 × 10^24 | 176,9 | 416,7 | 555,6 |
| 80 | 4,6 × 10^24 | 219,5 | 517,1 | 689,5 |

Dolgu yoğunluğu etkisi (Te = 30 km): dolgu 2000 için α 93,1 km, 2500 için 105,2, 3000 için 134,4. α, (ρm − ρdolgu)^(−1/4) ile ölçekleniyor; dalga boyu üzerinde zayıf, derinlik üzerinde (α³ ile) güçlü bir kaldıraç [H].

### Gözlenen ön çukurlar ve sürekli levhanın sınırı

- İsviçre Molasse havzası: özgün dalga boyu yaklaşık 120 km, genlik 5 ile 7 km. Subhercynian havzası (kırık levha, levha içi): dalga boyu yaklaşık 25 ile 40 km, genlik yaklaşık 2500 m (Hindle ve Kley 2021, atıfla [B]). Sürekli levha ile Molasse ön çıkıntısını 120 km'de bulmak için Te yaklaşık 8 km gerekir [H]; Te = 30 km 330 km verir, yani çok geniş.
- Himalaya ön ülkesi: yaklaşık 5 km derinlik, yaklaşık 200 km boyunca (Duvall ve diğerleri 2021, [B]); Hint levhasının etkin elastik kalınlığı kuzeye doğru 60 ile 80 km'den 20 ile 30 km'ye düşüyor (Hetenyi ve diğerleri 2006, [B]).
- Zagros ön ülkesi: derinlik kuşak boyunca 1 ile 6 km, Arap levhasının etkin elastik kalınlığı yaklaşık 50 km (Pirouz ve diğerleri 2017, [B]).
- Lin ve Watts (2002), Batı Tayvan: düşük Te (5 km) için havza fazla dar; yüksek Te (20 km) için genişlik tutuyor ama derinlik fazla az. Yüzey yüküne maruz sürekli elastik levha bu şekli tam açıklayamıyor. Kırık levha modelleri Appalach, Orta And ve Himalaya havzalarını başarıyla açıklıyor [B]. Batı Tayvan Te 13 km, dolgu 10 km'ye kadar [B].
- Ön çıkıntının zaman içinde sabit hızla göç etmesi olası değil; sıçramalı ilerliyor (Horton 2022, [B]). Daha sert levha daha geniş ön çıkıntı demek [B].

### Etkin elastik kalınlık (Te) değerleri

| Bölge | Te | Kaynak ve etiket |
|---|---|---|
| Kıtalar genel | 5 ile 110 km, iki tepeli: 10 ile 30 ve 70 ile 90 km | Tesauro ve diğerleri 2009, [B] |
| Küresel en iyi uyum | 34 ± 4 km | Watts ve Moore 2017 özeti, [Ö] |
| Himalaya ön ülkesi | 40 ile 90 km'den fazla, ön ülkede 70 km'nin üstü; Tibet içinde 10 km'nin altı | Stewart ve Watts 1997, [B] |
| Zagros | ön ülkede 60 km'nin üstü, yüksek Zagros altında sıfıra yakın | Stewart ve Watts 1997, [B] |
| Umman ofiyolit yükü | 30 km | Stewart ve Watts 1997, [B] |
| Batı Tayvan | 13 km | Lin ve Watts 2002, [B] |
| And | 5 ile 85 km, orojen genişliğiyle ilişkili | Stewart ve Watts 1997 özeti, [B] |
| Alpler | 20 ile 34 km (güç tabanlı), yaş tabanlı tahmin 13 ile 18 km | Tesauro ve diğerleri 2009, [B] |
| Apenin ve Pannonya | 20 ile 35 km | Tesauro ve diğerleri 2009, [B] |
| Adriyatik ve Po | 5 ile 15 km | Kruse ve Royden 1994, [B] |
| Tarım | 66 ile 110 km | 2. belge, yöntem farkı |

Kıtalarda Te ile termal yaş arasında basit bir ilişki yok (Tesauro ve diğerleri 2009, [B]). Okyanuslarda bir model sonucu olarak Te yaklaşık 450 °C izotermini izliyor; 20 ile 130 milyon yıllık taban için 10 ile 40 km (Bellas ve diğerleri 2022, [B], model sonucu). Mekanik anizotropi Kalnins ve diğerlerine (2015) göre anlamlı değil [B]. "Jöle sandviç" ve "krem brüle" tartışması bu turda çözülmedi [Y].

## 3. Ön ülke havzası ve sabit kıyı

Brief'in şartı kıyının hiç değişmemesi; karadaki bir ön çukur deniz seviyesinin altına inemez.

- Foreland havzaları "az dolu" (derin deniz), "dolu" (sığ deniz) ve "aşırı dolu" (akarsu) evrelerinden geçer; havzanın taban seviyesi deniz seviyesidir (Catuneanu 2004, [B]). Aşırı dolu havzanın yüzeyi taban seviyesine yakın kalır.
- Himalaya: yaklaşık 5 km bükülmüş taban, 1 ile 5 km dolgu [B]. Po: Pliyo-Kuvaterner dolgu 8 km'ye kadar (Ricci Lucchi 1986'ya atıfla, [B, ikincil]). Batı Tayvan: 10 km'ye kadar [B]. Kafkaslar (Rioni): 7 km'den fazla [B].
- Tasarım sonucu [H]: Sabit kıyıyla her kara ön çukuru aşırı dolu olmalı. Bükülme yükü, kuşağın yükü artı çökelti yükü. Dolgu, Δρ = ρm − ρçökelti ile α'yı da değiştirir (dolgu yoğunluğu 2500 iken Δρ = 800 kg/m³). Çökeltinin hacmi yaklaşık çöküntü hacmi kadar (yukarıdaki integral) ve kaynağı aşınan dağ olmalı; yani çökelme zorunlu bir kütle dengesi.
- Fastscapelib'de çökelme yok (yalnızca akarsu güç yasası ve raster üzerinde difüzyon) [B, 1. belge ve D notu]. Landlab'in ErosionDeposition ve SPACE bileşenleri ya da goSPL çökelmeyi destekliyor. Fastscapelib kullanılacaksa ön çukuru "taban seviyesine kadar doldurma" kuralıyla temsil etmek ve çökelti kütlesini ayrıca hesaplamak gerekir. Bu bir varsayım [H].
- Doluluk oranı: Sinclair ve Allen (1992) F oranı (bindirme cephesinin ilerleme hızı bölü cephedeki çöküntü hızı) arama özetinden [Ö], birincil metin okunmadı.

## 4. Aşınmanın geri yükselmesi

- **Yerel Airy sınırı.** Molnar ve England (1990): aşınan dT kalınlığındaki kaya için yüzey dT × (ρm − ρc) / ρm kadar, yaklaşık dT/6 alçalır; kaya (Moho dahil) yaklaşık 5/6 dT yükselir; kaya yükselmesi = yüzey yükselmesi + aşınma [B]. Champagnac ve diğerleri (2009): ρc = 2,8, ρm = 3,25 ile kaya yükselmesi dT × 0,86, yüzey alçalması 0,14 [B]. Braun ve Robert (2005): ρc = 2600, ρa = 3200 ile bir km rölyef azalması için 5,3 km kabuk aşınmalı (yüzey alçalma oranı 0,19) [B, denklem çıkarımı kısmen belirsiz]. Farklar yoğunluk seçiminden. Araç ρc ve ρm'yi parametre yapmalı.
- **Esnek tepki yayılır ve yumuşar.** Champagnac ve diğerleri (2009): Te = 10 km, E = 10^11 Pa, ν = 0,25, 100 km sınır genişletmesi, anlık elastik tepkiyle merkezi Alpler'deki ölçülmüş kaya yükselmesinin yüzde 75'ini tutturuyor, çekirdekte en çok yaklaşık 0,8 mm/yıl [B]. Kaya yükselmesi ile aşınma arasındaki regresyon eğimi 0,88 ± 0,14 [B]. Te → 0 sınırında yerel Airy elde edilir.
- **Zaman tepkisi.** Viskoelastik gevşeme zamanı τ = 2η / E (Sternai ve diğerleri 2019, [B]). Alpler için gecikme büyüklüğü doğrulanmadı; 10 000 ile 100 000 yıl gibi bir rakam [Y]. Champagnac anlık elastik bir model. On milyonlarca yıllık bir benzetimde anlık tepki ilk yaklaşım olarak kullanılabilir; gevşeme gecikmesi ayrı bir seçenek olmalı [H].
- **Buzul kalkması payı.** Alpler'de gözlenen yaklaşık 1 ile 2,5 mm/yıl yükselmenin Batı ve Orta Alpler'de yüzde 10 ile 30'u, Doğu Alpler'de yüzde 50'ye kadarı buzulların çekilmesiyle açıklanıyor; aşınma payı da yüzde 50'ye kadar [B ve Ö] (Sternai ve diğerleri 2019).
- **Çökeltinin depolanması.** Vadide depolanan çökelti izostatik tepkiyi azaltıyor (Sternai ve diğerleri 2019, [B]).
- **Tepe yüksekliği.** Montgomery (1994) vadi oyulmasıyla tepelerin yüksekliğinde en çok yaklaşık yüzde 25 artış olduğunu gösterdi (Roe ve diğerleri 2003 aracılığıyla, [B, ikincil]); arama özetleri Sierra ve Tibet için yüzde 5 ile 10, Himalaya için yüzde 20 ile 30 veriyor [Ö]. Birincil metin okunmadı.
- **Orojenik bozunma.** Wolf ve diğerleri (2022, Nature): Beaumont sayısı Bm kuşakları üç tipe ayırıyor; Himalaya, Tibet ve Orta And tip 1 (kararsız, dayanım denetimli), Tayvan tip 2, Güney Alpler tip 3 (aşınma denetimli) [B, özet ve giriş]. Bozunmanın iki evresi var [B].
- **Kaya yükselmesi, yüzey yükselmesi ve aşınma ayrı alanlar olmalı** (England ve Molnar 1990): kaya yükselmesi = yüzey yükselmesi + aşınma. Hiçbiri diğerinin yerine kullanılmamalı [B].

## 5. Okyanus tabanı (kısa)

Tabanın tam ele alınışı 6. konuya ait; burada izostazi açısından bulunanlar.

- Orta okyanus sırtı derinliği genelde 2500 ile 2600 m; küresel ortalama 2,85 ± 0,5 km (Gale ve diğerleri 2014, Richards ve diğerleri 2018 aracılığıyla); plaka modeli uyumu 2,22 km [B].
- Plaka modeli: Parsons ve Sclater T = 1350 ± 275 °C, kalınlık 125 ± 10 km; Stein ve Stein T = 1450 °C, kalınlık 90 km (Richards ve diğerleri 2018'in aktardığı biçimde, [B]).
- Genç taban için batma hızı yaklaşık 320 ile 350 m / (milyon yıl)^(1/2) (Korenaga ve diğerleri; Stein ve Stein arama özeti) [Ö]; yaşlı taban yaklaşık 5,5 ile 6,4 km'de düzleşiyor (Vikipedi, [E]).
- Korenaga referans modelinin denklemi (d0 = 2600 m, d1 = 409 m/Ma^0,5, d2 = 930 m) çıkarılan metinde d2'nin işareti belirsiz: artı işaretle 200 milyon yılda 9,3 km çıkıyor, bu gerçekçi değil. Basılı denklem kontrol edilmeden kullanılmamalı [Y]. Parsons ve Sclater (1977) ile Stein ve Stein (1992) tam metinleri okunamadı.

## 6. Hesap: kodlar, maliyet, düzlem ve küre

| Kod | Yöntem | Te değişken | Küre | Sürüm | Lisans |
|---|---|---|---|---|---|
| gFlex (awickert) | FD (seyrek LU), FFT, SAS | yalnızca FD | hayır (SAS_NG'de büyük daire mesafesi, çözüm hâlâ düzlem) | PyPI 1.3.0 (27 Mayıs 2026); 2.0.0b2 (1 Temmuz 2026); CHANGES'te 1.4.0 (29 Mayıs 2026) | GPL-3.0 |
| Landlab Flexure | Green fonksiyonu doğrudan toplam | hayır | hayır | 2.11.0 | MIT |
| goSPL | düz: FV iki harmonik, PETSc; küre: pyshtools ile spektral kabuk | evet (ikisi de) | evet | 2026.7.14 | GPL-3.0 |
| Fastscapelib (Python) | esneme yok | | | 0.3.0 | GPL-3.0 |
| TISC | 2B planform, EET ızgarası | evet | hayır | Kasım 2026 | GPL-3.0 |
| GMT grdflexure | FFT | hayır | hayır | | |

Hepsi [B], gFlex 1.3.0 ile 1.4.0 uyuşmazlığı ve TISC çözücü ayrıntıları hariç. gFlex 2.0 beta, `te` yerine `T_e`, `PlateSolutionType` kaldırıldı gibi API kırılmalarıyla geliyor; conda-forge'da yalnızca 1.1.0 var.

**Maliyet, 2000 × 1000 ızgara (2 milyon hücre).** Ölçülmüş tek veri gFlex belgelerinden: FFT 1000 × 1000 için yaklaşık 40 ms, FD 400 × 400 için yaklaşık 5 s (N^1,5 gibi ölçekleniyor), SAS 300 × 300 için yaklaşık 0,2 s [B]. Ekstrapolasyonlar [H, doğrulanmadı]: sabit Te FFT yaklaşık 0,1 s; SAS yaklaşık 5 s; FD seyrek LU yaklaşık 4 dakika çarpanlara ayırma ve büyük bellek; önbellekli çözüm çok daha ucuz (7 ile 12 kat). Landlab doğrudan toplamı 2 milyon yüklü hücre için 4 × 10^12 çekirdek değerlendirmesi: pratik değil. goSPL küresel spektral çözümü 5,9 milyon düğümlü ağda yaklaşık 4 saniye (seri) [B, HPC belgesi]. Yerel bir ölçüm yapılmadı; ilk koşuda ölçülmeli.

**Düzlem mi küre mi?** Te = 30 km için küresel esneme parametresi yaklaşık 50 km; eğrilik yalnızca en düşük derecelerde (binlerce km dalga boyunda) önemli görünüyor [H, tahmin]. Kıta kuzey güney yaklaşık 6700 km, yarım küreye yakın bir kısım. Boylam yönündeki hücre aralığı enleme göre cos(enlem) ile küçülüyor (60°K'de yarıya iniyor). Pratik yol: bölgeyi düzlem bir izdüşüme alıp düzlem çözücü kullanmak ve en düşük derece hatasını belgelemek. Tek küresel çözücü goSPL'in pyshtools tabanlı spektral kabuğu; yalnızca eğilme terimli bir operatör ve kendi ölçütüne göre Turcotte 1981 ve Wieczorek 2007'den derece 2'de yüzde 12, derece 4'te yüzde 4, derece 9 ve üstünde yüzde 1'in altında sapıyor [T, depo iddiası]. Brotchie ve Silvester (1969) okunamadı [Y]; düzlem ve küre eşiği için kaynaklı bir sayı bulunamadı.

**Erozyon motoruna bağlama.** goSPL ve Landlab'in kullandığı kalıp: yüklerin son çözümden bu yana değişimi (aşınma ve çökelme), belirli bir aralıkla toplanıp esneme çözümü yapılır ve sapma yüksekliğe eklenir; Landlab'de her çağrıda duraylı durum çözümü. Deniz seviyesinin altındaki yükler için iteratif doldurma gerekir (gFlex README) [B]. Kıyı maskesi her adımda yeniden uygulanmalı (1. belgedeki kural) [H].

**Önerim** [H]:

1. Varsayılan: sabit Te'li FFT (kendi numpy gerçeklemesi, birkaç satır: w(k) = q(k) / (D k⁴ + Δρ g)). Hızlı ve basit.
2. Değişken Te ya da kırık levha gerektiğinde: önbellekli seyrek FD çözümü (gFlex 1.x'i çağırmak ya da 13 noktalı yıldızı kendimiz yazmak). Kırık levha, sütur boyunca Te'yi sıfıra indirerek temsil edilebilir.
3. Küre için düzlem izdüşüm; goSPL küresel çözümü yalnızca doğrulama için.
4. Lisans: gFlex ve Fastscapelib GPL; kodu kopyalamak yerine formülden yeniden yazmak lisansı serbest bırakır.

## 7. Aracın varsayılan değerleri

| Parametre | Varsayılan ya da aralık | Etiket |
|---|---|---|
| E, ν | 10^11 Pa, 0,25 | [B] |
| ρm, ρc, ρsu | 3300, 2800, 1030 kg/m³ | [B] |
| Kabuk yoğunluğu kalınlıkla artışı (isteğe bağlı) | 2764 (25 km) ile 2947 (50 km) | [B] |
| Çökelti yoğunluğu | 1700 ile 2500; ön ülke dolgusu için 2500 | [B] ve [Ö] |
| Yüzey yükselmesi / toplam kabuk kalınlaşması | 0,15 (ρm − ρc) / ρm; litosfer mantosu kalınlaşırsa daha az | [H] |
| Aşınmada yüzey alçalması / aşınan kalınlık | 0,14 ile 0,19 (yoğunluğa bağlı); kaya yükselmesi 0,81 ile 0,86 | [B] |
| Te (kıta genel aralığı) | 5 ile 110 km; çoğu kuşak için 5 ile 40, kraton ön ülkeleri için 60 ile 80 km | [B] |
| Te ile termal yaş | kıtalarda bağlama; yalnızca okyanuslarda ve isteğe bağlı | [B] |
| Anizotropi | yok | [B] |
| Esneme türü | sürekli levha (varsayılan), kırık levha (anahtar) | [B] |
| Dinamik topografya | kapalı; açılırsa en çok ± 0,5 km | [B] |
| Esneme çözücü | FFT sabit Te; değişken Te için önbellekli FD | [H] |
| Düzlem / küre | düzlem izdüşüm | [H] |
| Tepki zamanı | anlık elastik; gevşeme isteğe bağlı, τ = 2η / E | [B] ve [Y] |
| Ön ülke dolgusu | kıyı sabitken aşırı dolu, yüzey taban seviyesine yakın | [H] |

## 8. Kaynaklar arası çelişkiler

- Airy ve kabuk kalınlığı: Tibet tutuyor, Alpler tutmuyor, Zoback ve Mooney küresel olarak tutmuyor diyor [B ve Ö]. Kabuk yoğunluğunun kalınlıkla arttığı bulgusu da Airy'nin sabit yoğunluk varsayımına ters.
- Aşınmada yüzey alçalması: 0,14 (Champagnac yoğunlukları), 0,17 (Molnar ve England), 0,19 (Braun ve Robert) [B]; fark yoğunluk seçimi.
- Whipple (2009) Airy için c ≈ 1/5 yazıyor; bu 1/6'dan farklı bir tanım olabilir, denkliği doğrulanmadı [B].
- Montgomery (1994) tepe yükselmesi: en çok yüzde 25 mi, yüzde 5 ile 30 mu [B ve Ö].
- Alpler'de geri yükselmenin payı: Sternai ve diğerleri (2019) yüzde 10 ile 30 (buzul kalkması, Batı ve Orta Alpler) ve Champagnac'ın aşınma payı yüzde 50'ye kadar [B ve Ö]. Farklı mekanizmaların payları.
- Te tanımı: güç tabanlı, yaş tabanlı, tutarlılık (coherence) tabanlı farklı sayılar veriyor; jöle sandviç ve krem brüle tartışması çözülmedi [B ve Y].
- Sürekli ve kırık levha: düşük Te ile havza fazla dar, yüksek Te ile fazla sığ; kırık levha daha iyi uyuyor [B].
- Yoğunluk değerleri: ρm 3200 ile 3330 (kaynağa göre); çökelti 1700 ile 2500; kabuk yoğunluğu 2764 ile 2947.
- Okyanus batma hızı: 320 (Korenaga) ve 350 (Stein ve Stein) [Ö]; Korenaga denklemi işaret belirsizliği [Y].
- Kıta ortalama kabuk kalınlığı: 41,1 km (Christensen ve Mooney 1995) ile 39,2 km (Chulick ve Mooney 2002) [Ö].
- Dinamik topografya genliği: model ± 2 km, gözlem ± 0,5 ile 1 km [B].

## 9. Bulunamayanlar ve doğrulanamayanlar

- Parsons ve Sclater (1977), Stein ve Stein (1992) tam metinleri; Crosby ve McKenzie (2009); Levandowski (2014); Afonso (2022); Hasterok ve Chapman (2007) tam metni; Conrad (2013).
- Burov ve Watts (2006), Audet ve Burgmann (2011), Tesauro ve diğerleri (2012) tam metinleri; Jordan (1981), Beaumont (1981), Watts (2001) kitabı, Turcotte ve Schubert (2002).
- Montgomery (1994), Champagnac ve diğerleri (2007), Burbank (1992), Garcia-Castellanos (2002), Gilchrist ve Summerfield (1990), Stephenson ve Lambeck (1985) birincil metinleri.
- Önceki promptumdaki bazı atıflar benim hatamdı: Champagnac 2007 Geology'de (Nature Geoscience'ta değil); Whipple 2009 Nature Geoscience; Montgomery 1994 JGR'de (American Journal of Science'ta değil); Stephenson ve Lambeck 1985 Geophysical Journal'da (Nature'da değil). "Braun ve Yamato 2010" ve "Wolf 2022 EPSL" bulunamadı; bu adlarla yayın bulunamadığı için kullanılmadı. Wolf ve diğerleri (2022) Nature'da.
- Ön çukur derinliği ve genişliğinin levha yaşına göre kaynaklı bir tablosu; esneme dalga boyu ve yük ilişkileri için yalnızca Molasse ve Subhercynian örnekleri var.
- Zagros ve Mezopotamya için Te'nin 20 milyon yılda 20 ile 55 km'ye yükselmesi, Ganj için 15 ile 25 km, Bengal'de 2 ile 4 mm/yıl çökme, Po için 10 ile 25 km³ / milyon yıl dolgu: yalnızca arama özetinde [Ö].
- "Apenin çökmesi 1,5 mm/yıl" iddiası atfedildiği makalede (Stefani ve diğerleri 2019) yok; reddedildi.
- Düzlem ve küre eşiği için kaynaklı sayı; goSPL kabuk operatörünün doğruluğu için tek kaynak deponun kendi ölçütü [T].
- Haiku koşularında iki makalenin dışındaki sayılar bu belgeyi yazarken yeniden denetlenmedi; bu turda yalnızca formüller sayısal olarak sınandı.

## Başlıca kaynaklar

Tam liste ve her bilginin tek tek kaynağı `arastirma/notlar/03/` içindeki dört dosyada.

- Zoback ve Mooney 2003, litosfer kaldırma kuvveti: https://escweb.wr.usgs.gov/share/mooney/2003_IGR_LithoBuoyancy.pdf
- Lachenbruch ve Morgan 1990 (özet): https://pubs.usgs.gov/publication/70016328
- MIT 12.520 ders 20, esneme: https://ocw.mit.edu/courses/12-520-geodynamics-fall-2006/353f42887f4ee449a0bd1602660dd0ae_lecture20.pdf
- Stewart ve Watts 1997: https://ora.ox.ac.uk/objects/uuid:9f803b42-522e-442b-9849-bb8e6c2a5494/files/m88d0e5b84c28370abf6d7b84438cc52d
- Lin ve Watts 2002, Batı Tayvan: https://basin.earth.ncu.edu.tw/publications/papers/Lin&Watts_2002.pdf
- Hindle ve Kley 2021: https://se.copernicus.org/articles/12/2425/2021/
- Tesauro, Kaban ve Cloetingh 2009: https://research.vu.nl/ws/files/2522156/227389.pdf
- Bellas, Zhong ve Watts 2022: https://par.nsf.gov/servlets/purl/10391238
- Horton 2022: https://par.nsf.gov/servlets/purl/10329923
- Kalnins ve diğerleri 2015: https://geoweb.princeton.edu/people/simons/PDF/reprints/EPSL-2015b.pdf
- Hetenyi ve diğerleri 2006 (özet): https://real.mtak.hu/5945/
- Duvall ve diğerleri 2021: https://eprints.lancs.ac.uk/155586/1/Duvall_al2021BRE_006_2021.R2_Proof_hi.pdf
- Pirouz ve diğerleri 2017 (özet): https://authors.library.caltech.edu/records/1bgnp-74m19
- Kruse ve Royden 1994 (özet): https://digitalcommons.usf.edu/geo_facpub/942
- Molnar ve England 1990: https://www.tectonics.caltech.edu/meetings/journal_club/session2/Molnar_and_England1990Nature.pdf
- Champagnac ve diğerleri 2009: https://gfzpublic.gfz-potsdam.de/pubman/item/item_238796_1/component/file_238795/13194.pdf
- Braun ve Robert 2005: https://www.isterre.fr/IMG/pdf/Braun-and-Robert-ESPL2005.pdf
- Whipple 2009: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2009_Whipple.pdf
- Sternai ve diğerleri 2019: https://boa.unimib.it/bitstream/10281/229017/2/Sternai%20et%20al.%2c%202019.pdf
- Roe, Montgomery ve Hallet 2003: https://earthweb.ess.washington.edu/roe/Web/GerardWeb/Publications_files/RoeEtal_Relief_JGR03.pdf
- Wolf ve diğerleri 2022 (Nature): https://gfzpublic.gfz-potsdam.de/pubman/item/item_5011946_3/component/file_5012394/5011946.pdf
- Catuneanu 2004: https://www.eas.ualberta.ca/catuneanu/files/Papers_PDF%20files/2004_Catuneanu_Forelands_JAES.pdf
- Hoggard, White ve Al-Attar 2016 (özet): https://researchportalplus.anu.edu.au/en/publications/global-dynamic-topography-observations-reveal-limited-influence-o/
- Steinberger ve diğerleri 2019: https://gfzpublic.gfz-potsdam.de/pubman/item/item_4381899_3/component/file_4384888/4381899.pdf
- Richards ve diğerleri 2018: https://freddrichards.github.io/documents/papers/richards_etal_2018_jgr.pdf
- Murodov ve diğerleri 2022, Tibet: https://www.frontiersin.org/articles/10.3389/feart.2022.821497/pdf
- gFlex (Wickert 2016): https://gmd.copernicus.org/articles/9/997/2016/gmd-9-997-2016.pdf
- gFlex deposu ve belgeleri: https://github.com/awickert/gFlex
- Landlab: https://github.com/landlab/landlab
- goSPL: https://github.com/Geodels/gospl
- Beuthe 2007, kabuk eğilmesi: https://arxiv.org/pdf/0704.1627
