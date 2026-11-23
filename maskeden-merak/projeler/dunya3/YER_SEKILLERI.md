# Yer şekilleri ve karşılıkları

`kur.py` üretir. Tepe: yükseklik eğrisinin üst ucu (m).

| ad | parça | sebebi (olay) | karşılık | tepe |
|---|---|---|---|---|
| KolDaglari | bati | Batı'nın iki kalkanının çarpışması (320 MYÖ): kol boyunca eski kıvrımlar (Apalaş benzeri) | kutu [-91, -69, 30, 46] | 2100 |
| BatiKuzeyKalkan | bati | Kuzey kalkanı; buzul aşındırması, göller (Kanada kalkanının kuzeybatısı benzeri) | kutu [np.float64(-125.88), -95, 54, np.float64(70.21)] | 1100 |
| KuzeyYarikOmzuBati | bati | Kuzey Yarığı'nın açılması (20 MYÖ'den beri): batı omzu (Baykal benzeri) | kutu [98, 117, 46, 61] | 2100 |
| BatiIcKalkanKuzey | bati | Batı Kalkanı: aşınmış düzlükler ve kum denizi | kutu [118, 139, -36, -21] | 1100 |
| BatiIcKalkanGuney | bati | Batı Kalkanı'nın güneyi: yaşlı kalkan, demirli sıralar | kutu [110, 128, -34, -16] | 1000 |
| BatiKiyiKuzey | bati | Büyük Okyanus kıyısı: edilgen kıyı basamağı | kutu [22, 37, -36, -20], aynalı | 2100 |
| BatiKiyiGuney | bati | Büyük Okyanus kıyısı güneyi: edilgen kıyı basamağı | kutu [-53, -36, -30, -16], aynalı | 2100 |
| GuneyYarikHavzalari | bati | Güney kıyısında başarısız yarık kolları (Kenya yarığı benzeri), yanardağlı | kutu [30, 43, -7, 6] | 2900 |
| KorfezOvasi | bati | Kol Dağları önünde batan önülke; körfez kıyısı ovası | kutu [-99, -81, 26, 40.5] | 1500 |
| BatiDoguKiyi | bati | Orta Okyanus kıyısı: kumtaşı yaylaları ve kuesta basamakları | kutu [-18, -1, np.float64(4.2), np.float64(24.3)] | 1100 |
| KuzeyKalkan | kuzey | Kuzey Kalkanı; buzul aşındırması, göl düzlükleri | kutu [-106, -82, 56, 70] | 1100 |
| OrtaSira | kuzey | Kuzey'in iki kalkanının çarpışması (400 MYÖ): aşınmış orta sıra (Kafkas dokusu, alçaltılmış) | kutu [33, 54, 36.5, 48] | 2700 |
| KuzeyIcOva | kuzey | Kuzey platformu: geniş, alçak tortul ova | kutu [-69, -53, -42, -26] | 1500 |
| BatiKiyiYarikOmzu | kuzey | Kuzey Yarığı'nın doğu omzu (Baykal yarığının kuzeydoğu kolu benzeri) | kutu [103, 124, 49, 62] | 2100 |
| DoguKiyiDaglari | kuzey | Doğu Okyanusu açılırken ters dönen eski yarık havzası dağları (Atlas benzeri) | kutu [-13, 8, 25, 39] | 4100 |
| GuneyKivrimKusagi | kuzey | Orta Kıta'nın Kuzey'e yaklaşması: genç kıvrım yayı (Karpat benzeri) | kutu [12, 32, 40, 54], aynalı | 3600 |
| GuneyBatiOva | kuzey | Kuzey'in güneybatısı: alçak, düz kuru ova | kutu [-68, -53, -30, -15] | 1500 |
| GuneyDoguYayla | kuzey | Kuzey'in güneydoğusu: yatay katmanlı yayla, kanyonlar | kutu [-118, -102, 30, 43.5] | 1800 |
| OrtaKalkan | orta | Orta Kıta: batıda kalkan, doğuda tortul örtü; kuzeyi Kuzey'e dalan önülke (Arabistan benzeri) | kutu [np.float64(32.25), np.float64(58.08), 11, np.float64(34.74)] | 2900 |
| GuneyMeseta | guney | Güney Kıtası: bazalt mesetaları, rüzgâr aşındırması | kutu [-75, -61, -54, np.float64(-40.42)] | 1500 |
| GuneyBuzulDaglari | guney | Kutup yakınında eski yığışım kuşağı, buzul vadili (Doğu Sayan benzeri) | kutu [np.float64(90.68), 107, np.float64(46.85), np.float64(57.65)] | 2100 |
| GuneyKuzeyKiyi | guney | Orta Kıta'dan kopma (80 MYÖ): kopma kenarında yükselmiş yaylalar (Zimbabve doğu yaylaları benzeri) | kutu [np.float64(24.77), np.float64(39.03), -26, np.float64(-13.04)] | 2900 |
| BatiKalkanKuzeyD | dogu | Doğu Kıtası'nın batı kalkanı: kumtaşı yaylaları ve çöl havzası | kutu [12, 30, 8, 23] | 1000 |
| BatiKalkanGuneyD | dogu | Doğu Kıtası'nın batı kalkanı güneyi: kuru havza ve kenar yaylaları | kutu [11, 31, -32, -13] | 1600 |
| GuneyBatiKiyiD | dogu | Doğu Okyanusu kıyısında eski kıvrım kuşağı (Kap kıvrımları benzeri) | kutu [14, 31, -38, -28.5] | 2100 |
| BoynuzKuzey | dogu | Boynuz: eklenmiş yay parçalarının kıvrım kuşağı (Çerski benzeri) | kutu [133, 159, np.float64(57.25), np.float64(72.25)] | 2100 |
| BoynuzGuney | dogu | Boynuzun güneyi: havza ve sıra (Transbaykal benzeri) | kutu [np.float64(103.89), 131, np.float64(45.7), np.float64(61.3)] | 2100 |
| KavusmaDaglari | dogu | Kuzeydoğu parçasının ana kıtaya çarpması (30 MYÖ'den beri): kıvrım kuşağı (Zagros dokusu, aynalı) | kutu [41, 63, 22, 40], aynalı | 4100 |
| KuzeydoguYay | dogu | Büyük Okyanus'un dalması: kuzeydoğu kıyısında yanardağ sırası (Barisan benzeri) | kutu [91, 110, -10, 10], aynalı | 4100 |
| KuzeydoguIc | dogu | Kuzeydoğu parçasının içi: yay ardı ovası ve sıralar (Mançurya benzeri) | kutu [114, 134, 38, 54] | 1500 |
| OrtaKalkanDogu | dogu | Ana kalkanın ortası: masa yaylaları | kutu [-66, -48, -20, -6] | 950 |
| OrtaKalkanGuneyD | dogu | Ana kalkanın güneyi: yatay katmanlar, dolerit masaları (Karoo benzeri) | kutu [16, 32, -37, -25] | 1500 |
| DoguIcHavza | dogu | Dalma ardında kırık önülke: sıralar ve tuzlu havzalar | kutu [-72, -58, -37, -23] | 2900 |
| GuneyDoguAnd | dogu | Büyük Okyanus'un dalması: güneydoğu kıyısında And benzeri sıra | kutu [-84, -65, -20, 0], aynalı | 4100 |
| GuneyKutupBati | dogu | Kutup yakınında eski kubbe yaylası (Hangay benzeri) | kutu [91, 108, 41, 54] | 2100 |
| GuneyKutupDogu | dogu | Kutup yakınında buzul aşındırmalı kalkan (Västerbotten benzeri) | kutu [10, 26, 59, 70] | 1100 |
| AdaKuzeybati | adaKB | Büyük Okyanus'ta sıcak nokta adası (İzlanda) | kutu [-25, np.float64(-12.2), np.float64(62.31), np.float64(67.08)] | 2500 |
| AdaGuneydogu | adaGD | Kutup bölgesinde kopmuş kalkan parçası, buzul dağlı (Baffin) | kutu [np.float64(-82.98), -57, 63, np.float64(74.04)] | 2500 |
| AdaOrtaOkyanus | adaOrta | Orta Okyanus sırtına yakın sıcak nokta (Sicilya) | kutu [np.float64(11.99), np.float64(16.2), np.float64(35.7), np.float64(39.04)] | 2500 |
