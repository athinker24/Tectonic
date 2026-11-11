# 1. Mevcut araçlar ve dünya kurgucuların yöntemleri

Araştırma tarihi: 11 Kasım 2026. Bu belge beş ayrı araştırma kolunun birleşimidir. Kollar yaklaşık 230 web sayfası, 25 makale ve 20 kod deposu okudu. Her bilginin kaynağı ham notlarda, bilginin hemen yanında duruyor: `arastirma/notlar/01/` (İngilizce; A Merak ve GPlates, B hobi ve profesyonel araçlar, C kurgusal dünyalarda yöntemler, D bilimsel araçlar, E grafik araştırmaları). Bu belge o notların Türkçe özeti ve bu araca çıkan sonuçlardır. "Doğrulanamadı" yazan bir bilgi birincil kaynaktan teyit edilemedi.

Sorulan soru: kıyı çizgisi sabit bir kıtadan tutarlı bir tektonik tarih çıkarıp buna uyan gerçekçi, aşınmış bir rölyef üreten bir araç zaten var mı; yoksa hangi parçalar yeniden kullanılabilir, hangi dersler alınmalı?

## Kısa sonuç

Bu işin tamamını yapan bir araç yok. Hiçbir araç bugünkü bir kara maskesini alıp kıyıyı sabit tutarak bir levha tarihi önermiyor ve o tarihten aşınmış bir rölyef üretmiyor. Bu bulgu beş kolun beşinde de bağımsız olarak çıktı.

En yakın üç aday şunlar:

- **Merak'ın yeni "History" sekmesi.** 1 Kasım 2026'da eklendi. Bugünkü karadan levhaları ve hareketlerini çıkarıp 250 milyon yıl geriye sarıyor; bugünkü haritaya dokunmuyor. Ama rölyef üretmiyor, yalnızca hareketi gösteriyor.
- **Gleba.** Ücretsiz bir masaüstü simülatörü. Kıta taslağı içe aktarıp levha yönü verilebiliyor; dağ, plato ve erozyon üretiyor. Kıyının koşudan sonra sabit kalıp kalmadığı doğrulanamadı. Kapalı kaynak, yalnızca grafik arayüzlü bir uygulama.
- **GPlates.** Bilimsel standart. Bugünü sabit alıp geriye doğru çalışmak, yerleşik çalışma biçimi. Ama yalnızca katı dönmeleri hesaplıyor; çarpışma, dağ oluşumu, erozyon ve yükseklik tamamen elle yapılıyor.

Kendi aracımızı yapmak bu yüzden gerekçeli. Ama sıfırdan yazılması gereken kısım sanıldığından küçük: blok kinematiği (pyGPlates ya da düz numpy), kıyıyı sabit tutan erozyon (Fastscapelib ya da Landlab) ve gerçekçilik ölçütleri (yayınlanmış ve kodu açık yöntemler) hazır. Asıl yazılması gereken iki parça kalıyor: blok tarihinden yükseltme haritası üreten kurallar ve kıyıdan geriye tarih çıkaran çıkarım katmanı.

## 1. Merak Map Maker: brief'ten sonra değişti

Brief'te Merak'ın tektonik aracının ihtiyacı karşılamadığı yazıyor: ileriye dönük mod kıyıyı bozuyor, geriye dönük mod hazır bir rölyef istiyor. Bu değerlendirme Kasım 2026 güncellemelerinden önce yapılmış. Merak'ın sitesinde metin içeren bir belge yok; bilgiler sitenin kendi uygulama kodundaki tarihli değişiklik günlüğünden, arayüz yazılarından ve fiyat tablosundan okundu. Sürüm numarası kullanılmıyor, yalnızca tarihli sürümler var.

**History sekmesi (1 Kasım 2026).** Bugünkü dünyanın karasından levhaları ve Euler hareketlerini çıkarıyor ("Plates from the land") ve 250 milyon yıl geriye, 50 milyon yıl ileriye oynatıyor. GIF olarak kaydediliyor. Bugünkü harita "Today" olarak değişmeden kalıyor; bu sekmede haritayı değiştiren bir "uygula" düğmesi yok. Yani kıyı fiilen korunuyor. Levha çıkarımının ne kadar sağlam olduğu, sıkıştırılmış koddan değerlendirilemedi. Girdi olarak karanın yükseklik alanını da kullanıyor; yalnızca siyah beyaz bir maskeyle ne kadar iyi çalıştığı doğrulanamadı.

**Tectonics sekmesi (8 Kasım 2026).** Bugünkü araziden başlayıp 200 milyon yıl ileriye çalışıyor. Levhalar karadan okunuyor ya da elle çiziliyor, bölünüyor, birleştiriliyor. Her levhaya yön ve hız veriliyor (0 ile 15 cm/yıl; arayüzdeki ipucu: "Dünya'da 1 ile 10"). Her sınıra tür (dalma, çarpışma, yanal, açılma), hangi levhanın dalacağı, 0 ile 3 arası yükselme çarpanı ve volkanizma seçimi veriliyor. Kıtasal riftleşme, akarsu erozyonu ve manto sorgucu açılıp kapatılabiliyor. "Apply this moment" haritayı o anın durumuyla değiştiriyor; bu modda kıyı korunmuyor. Bu, brief'te anlatılan ileriye dönük modun gelişmiş hali.

**Diğer ilgili özellikler.** Sculpt araç çubuğunda bir "Coastline lock" var (28 Eylül 2026); tam olarak ne yaptığı doğrulanamadı. "Apply bathymetry" levhalardan sırtlı ve hendekli bir deniz tabanı üretiyor (1 Kasım 2026). Merak'ın jeoloji haritası şu sınıfları kullanıyor: tortul platform, önülke havzası, kıvrım dağları, volkanik yay, aşınmış dağlar, pasif kenar.

**Yükseklik haritası biçimi.** Brief'te ve 24. konuda "bilinmiyor" diye geçen soru cevaplandı. Merak'ın iç ızgarası 4096 × 1976. Dışa aktarım 16 bitlik gri PNG, en fazla 16384 piksel. Dosyanın içine en düşük ve en yüksek metre değeri ile deniz seviyesinin gri değeri yazılıyor. İçe aktarım gri yükseklik haritası (deniz seviyesi yaklaşık %22 gri), saf siyah beyaz kara maskesi (açık renk kara), renkli harita, GeoJSON ve Merak'ın kendi `.warmap` dosyalarını kabul ediyor. Varsayılan projeksiyon **Natural Earth**, eşdikdörtgen değil. Dışa aktarılan dosya kendi projeksiyonunu taşıyor. Bu, atlastaki küre kaydı için önemli bir ayrıntı (24. konu).

**Fiyat.** Ücretsiz sürüm 2K dışa aktarım ve filigranla sınırlı, projeksiyon yok. Premium aylık 6 dolar (16K dışa aktarım). Founder's Lifetime tek seferlik 49,99 dolar, yalnızca ilk 300 kişi için. Merak'ın betik arayüzü ya da komut satırı yok; Actions'ta otomatik çalıştırılamaz.

**Bu araca etkisi.** Merak'ın History sekmesi zaman çubuğu fikrinin bir benzerini yapıyor ama rölyef üretmiyor. Tectonics sekmesi rölyef üretiyor ama kıyıyı koruyamıyor. İkisinin arasındaki boşluk, brief'te tanımlanan ihtiyacın ta kendisi ve hâlâ boş. Yine de denemesi ucuz bir şey var: maske gelince Merak'a içe aktarıp History sekmesinin bu kıtadan hangi levhaları çıkardığına bakmak. Bu, bizim çıkarım katmanımız için bağımsız bir karşılaştırma noktası verir. Merak'ın yeni özellikleri haftalık geldiği için bu bölüm hızla eskiyebilir.

## 2. GPlates ve levha kinematiği araçları

**Sürümler.** GPlates masaüstü son kararlı sürüm 2.5 (15 Nisan 2024). 3.0 yayımlanmadı; OpenGL'den Vulkan'a geçiş için ayrı bir dalda geliştiriliyor. pyGPlates 1.0.0 Mart 2025'te çıktı ve pip ile kuruluyor (Linux, macOS, Windows için hazır paket; Python 3.8 ile 3.13). GPlately 2.0.0 Temmuz 2025'te çıktı ve deposu çok aktif. Lisanslar GPL v2. Ağustos 2026'da dünya kurgucular için resmi olmayan bir çatal çıktı ("2.6.0-dev8-SR1": levha bölme, çokgen birleştirme, dönme dosyası düzenleyici); GPlates ekibi bunu onaylamıyor.

**Ne yapıyor.** Levhaları Euler kutupları etrafında katı dönmelerle hareket ettiriyor, bir rasteri statik çokgenlerle kesip geçmişe taşıyabiliyor, levha topolojilerini ve hızları hesaplıyor. Fizik yok.

**Ne yapmıyor.** Çarpışma, dağ oluşumu, erozyon ve yükseklik üretimi tamamen elle yapılıyor. Geliştirici John Cannon forumda deformasyon desteğinin bu kullanım için "tam yararlı olmayabileceğini" ve gezegenin içeride birim yarıçaplı bir küre olarak tutulduğunu söylüyor. Bir kullanıcı da yöntemin özelliklere "katı monolitler gibi" davrandığından şikâyet ediyor. GPlately'de de geçmiş yükseklik haritası üreten bir modül yok.

**Bizim için önemli olan.** GPlates'in dönme dosyası bugünden geriye okunuyor: 0 milyon yıl satırı her zaman bugünkü konum. Yani "bugünkü harita sabit, geçmiş uydurulur" GPlates'in doğal çalışma biçimi. Worldbuilding Pasta ileriye doğru çalıştığı için "sürüklenme düzeltmesi" denen bir yamaya ihtiyaç duyuyor; geriye doğru çalışınca bu gerekmiyor. Forumda en az üç kullanıcı tam olarak bunu yapmış: bugünkü kıtadan başlayıp geriye gitmiş.

**Bu araca etkisi.** Blok hareketlerini pyGPlates ile tutmak hazır ve doğrulanmış bir altyapı verir: sonlu dönmeler, yeniden kurgu, hız alanları. Ayrıca çıktıyı GPlates'in kendi biçimlerinde (`.rot` dönme dosyası, GPML ya da GeoJSON çokgenler) yazmak, uydurduğumuz tarihin GPlates'te açılıp incelenebilmesini sağlar. Ama aynı iş birkaç yüz satır numpy ile de yapılabilir; pyGPlates'e bağımlılık zorunlu değil. Bu seçim 8. ve 9. konularda verilecek.

## 3. Kurgusal haritalardan tektonik tarih: bilim insanları ve topluluk

### Bilim insanlarının örnekleri

**Game of Thrones (2019).** Sabin Zahirovic (Sydney Üniversitesi) ve Jo Condon (Melbourne Üniversitesi), üç araştırma asistanıyla birlikte, bir Cartographers' Guild kullanıcısının yaptığı GIS kıyı haritasını GPlates'te geriye doğru kurdu. Volkanizmayı ve dağ oluşumunu yaklaşmanın kanıtı saydılar ve bugünkü dalma zonlarını haritaya çizdiler. En önemli kuralları şuydu: "Tektonik yeniden kurgunun en kolay kısmı, okyanus tabanı açılmasını geriye sararak yapılır." Yani önce en genç okyanuslar kapatılıyor. Dar Deniz'in 25 milyon yıl önce açıldığını, aynı yaştaki Doğu Afrika Riftini örnek alarak varsaydılar. Belirsizliğin yaşla büyüdüğünü açıkça yazdılar: 250 milyon yıla kadar oldukça doğru, daha öncesi çok zor. Önceki bir mesajımda Ben Mather'ı da yazarlar arasında saymıştım; hiçbir kaynakta adı geçmiyor, bu bilgi yanlıştı.

**Orta Dünya.** Reynolds (1974) dört levha, Sarjeant (1990'lar) altı levha önerdi. Çıkarım biçimleri öğretici: dağ sıraları sütur, sıraların birleştiği yerler üçlü kavşak, uzun düz bir nehir rift, düz ve sakin ovalar kraton sayılıyor. Jeolog Alex Acks (2017) Mordor'un dik açılı kutu biçimli dağlarını reddediyor ("dağlar köşe yapmaz") ve Hüküm Dağı gibi tek başına bir volkanın bir sıcak nokta izi gerektirdiğini hatırlatıyor. EGU'nun 2023 ve 2025 blog yazıları, genç ve yaşlı dağların yükseklik ve pürüzlülükten ayırt edildiği aynı mantığı kullanıyor.

**Lunt'un Orta Dünya iklim modeli (2013).** Çizilmiş bir haritayı modele çevirmek için açık kurallar koymuş: dağ 4000 m, etek tepeleri 2000 m, diğer kara 300 m, nehir 100 m, okyanus kıyıdan uzaklaştıkça 4000 m'ye derinleşiyor. Aldığı serbestlikleri tek tek yazmış. Bu şeffaflık bizim istisna defterimiz için iyi bir örnek.

### Dünya kurgucu topluluğunun yöntemleri

**Worldbuilding Pasta** bu alanın en ayrıntılı kaynağı. Yazar hazır bir haritaya sonradan tarih giydirmeyi önermiyor ve bunu bilardo masasına benzetiyor: topların dağılımından oyunu geri kurmaya çalışmak. Gerçek Dünya'da jeologlar bir çözümün var olduğunu biliyor; kurgusal bir dünyada böyle bir garanti yok. Yine de bir yol tarif ediyor:

1. Kıtaların bir süper kıtadan gelmiş olabileceğini, bir iki parça dışarıda kalabilir diyerek denetle.
2. Bugünkü levha yönleri genelde eski süper kıtanın merkezinden dışarı doğrudur.
3. Hareketin önündeki kıyılara aktif kenarları ve bugünkü dağ oluşumunu koy.
4. Genç iç okyanusa bakan kıyılar pasif kenardır.
5. Eski dağları sanatsal tercihle yerleştir.

Bir de uygulanabilirlik testi veriyor: hiçbir dalma zonundan uzakta okyanus ortasında aniden beliren bir kara parçası olmamalı ve hareketin önündeki her kıyının aktif bir kenarı olmalı.

Sayısal kuralları:

- Levha hızları: dalan okyanus 10 ile 20, yeni çarpışma 5 ile 10, aktif kenarlı kıta 2 ile 5, pasif kenarlı kıta 1 cm/yıl'ın altında. Aynı yazarın GPlates yazısında değerler biraz farklı: 8 ile 20 / 6 / 3 / 1'in altı.
- 1 cm/yıl, Dünya'da 10 milyon yılda yaklaşık 0,9 derece hareket demek.
- Dağların ortalama yüksekliği yaklaşık 2500 m'den başlar ve milyon yılda yaklaşık 5 m düşer; zirveler yaklaşık 4000 m'den başlar ve milyon yılda yaklaşık 8 m düşer. Yazar üstel bir azalmanın daha iyi bir model olabileceğini de belirtiyor.
- Bir çarpışma kuşağı çarpışma bittikten sonra yaklaşık 50 milyon yıl etkin kalır; 450 milyon yıl sonra yalnızca kökleri kalır.
- Okyanus kabuğu yaklaşık 250 milyon yılda tamamen yenilenir. Bu yüzden 200 ile 250 milyon yıldan eski okyanus tarihi kayıt bırakmaz ve serbestçe uydurulabilir.

Kıyı biçimi ile kenar türü arasındaki kuralları:

- Hareketin önündeki aktif kenar: düzgün kıyı, yüksek kıyı sırası.
- Arkaya çekilen dalma kenarı: girintili kıyı, açıkta ada yayı.
- Pasif kenar: ya uzun haliç girintileri ve alçak kıyı ovasıyla girintili, ya da manto yükselmesiyle düzgün bir kıyı.

En önemli uyarısı, bizim brief'teki sorunla doğrudan ilgili: deneyimsiz harita çizerlerin ve basit üreteçlerin kıtaları "yüksek bir iç kısımdan kıyılara doğru alçalan" biçimde yapmasına karşın, gerçekte daha yaygın olan "çeşitli yaşlarda kıyı sıralarıyla çevrili alçak iç havzalar"dır. Fraktal ve gürültü üreteçleri bu yüzden yoğunlaşmış yer şekilleri üretemez.

**Worldbuilding Stack Exchange**'in topluluk kuralları (soru 247575) yararlı ama dikkatli okunmalı. Önemli kurallar şunlar: levhalar dört yönlü kavşakta buluşmaz; sınırlar yaklaşık 120 derecelik üçlü kavşaklar ve düzgün dalma yaylarıdır; levhalar karaların ortasından nadiren geçer, geçiyorsa ortadan bir dağ sırası kesmelidir; çoğu levha hem okyanus hem kara içerir. Aynı sayfada çelişkiler ("asla T" ile "dik açılı T") ve yanlışlar ("yanal faylar volkan yapar") da var. Bu kuralları jeologların kaynaklarıyla (Worldbuilding Pasta, Acks, EGU) süzmek gerekiyor.

**Artifexian**'ın GPlates dizisi Worldbuilding Pasta yöntemini izliyor ve ileriye doğru çalışıyor; hazır haritaya uygulanan bir yöntem değil. **Azgaar** kıyıyı sabit tutabiliyor ("Keep" modu ve yalnızca karada çalışan fırçalar) ama tektonik mantığı yok. **Cartographers' Guild**'de geriye doğru çalışmayı deneyip vazgeçen kullanıcılar var; konular giriş istediği için yalnızca arama özetlerinden okundu.

## 4. Hobi ve dünya kurgucu simülatörleri

| Araç | Zamanla hareket | Çarpışmadan dağ ve plato | Erozyon | Verilen kıyıyı kullanma | Son güncelleme |
|---|---|---|---|---|---|
| Gleba | Var; levha yönü verilebiliyor | Var (Himalaya tipi plato dahil) | Akarsu ve buzul | Taslak içe aktarımı yerleşimi yönlendiriyor; sabit kalıp kalmadığı doğrulanamadı | v0.3.6, 2 Eylül 2026 |
| GeoChronicler | Elle anahtar kareler | Yok (yükseklik modeli yok) | Yok | 0 milyon yılda elle çizip geriye gidilebiliyor | Doğrulanamadı |
| Cartogenesis | Var | Sıralar, yaylar, platolar, riftler | Akarsu, çökelme, buzul | Yok | Doğrulanamadı |
| WorldEngine | Var (PlaTec ile) | Var | Var | Yok | v0.20.0, Kasım 2026 |
| PlaTec (PyPlatec) | Var (2B) | Var | Basit | Yok | v1.4.4, Kasım 2025 |
| Tectonics.js | Var (kendiliğinden oluşan dalma) | Var | Var | Yok | Ağustos 2020'den beri durgun |
| Red Blob, Experilous | Yok (anlık) | Sınır kurallarıyla | Yok | Yok | 2016 ile 2026 arası |
| Azgaar FMG | Yok | Şablonlarla | Yalnızca nehirler | Görüntüden yükseklik içe aktarımı, kıyıyı koruyan düzenleme | Kasım 2026 |

GitHub Actions'ta Linux üzerinde başsız çalışabilen yalnızca iki açık kaynak seçenek var: PyPlatec (LGPL-3.0) ve WorldEngine (MIT). İkisi de başlangıç kara maskesi almıyor. GeoChronicler'ın JSON şeması (levha, kıta, kraton, orojen, sıcak nokta, anlık görüntüler) uydurulan bir tarihi kaydetmek için iyi bir örnek veri modeli.

İki yöntem doğrudan işe yarıyor. Andy Gainey'in (Experilous, 2016) yaklaşımı sınırdaki göreli hareketi sınıra dik bileşen (basınç) ve teğet bileşen (kesme) olarak ayırıp her birini bir yükselti profiline çeviriyor. Red Blob bunun üstüne bir çarpışma eşiği (0,75) ekleyerek her sınırda dağ oluşmasını engelliyor. Frozenfractal (2023) levhaları mevcut kıtaların etrafında büyütüyor; "önce kıtalar, sonra levhalar" yaklaşımının yordamsal bir örneği.

## 5. Profesyonel arazi yazılımları

| Yazılım | Son sürüm | Linux | Actions'ta başsız | Tektonik | Not |
|---|---|---|---|---|---|
| Gaea | 2.3.1.0 (24 Eylül 2026); Gaea 3 erken erişimde | Yok | Yok (Windows; otomasyon Pro sürümde) | Yok; Uplift ve Fold yalnızca biçim filtresi | Ücretsiz sürüm 1K dışa aktarım; Indie 99, Pro 199 dolar |
| World Machine | Build 4069 (30 Ekim 2026) | Var (Temmuz 2026'dan beri) | Mümkün olabilir (Pro, 299 dolar, XML betik); ekransız çalışma ve lisans doğrulanamadı | Yok | En makul ticari aday |
| World Creator | 4 erken erişim (Kasım 2026) | "Yakında" | Yok | Yok | Bütün gezegen desteği |
| Houdini | 22 (Temmuz 2026) | Var | Mümkün; büyük kurulum ve lisans sorunu | Yok (betikle yazılabilir) | Ücretsiz Apprentice ticari olmayan kullanım için |
| Wilbur | 1.89 (2019, yalnızca arama özetinden) | Yok | Yok | Yok | Ücretsiz; kıta ölçeği erozyonda tercih ediliyor |
| Instant Terra | 2.5 (Mart 2022) | Yok | Yok | Yok | Durgun görünüyor |

Profesyonel yazılımların hiçbirinde levha tektoniği yok. "Tektonik" görünen düğümleri (Gaea'nın Uplift, Fold, Shear düğümleri) yalnızca biçim filtreleri. Kıyıyı sabit tutmak hepsinde maskelerle yapılıyor.

**Kıta ölçeği iddiası.** Kilroy's Kartography (Ekim 2025), Gaea'nın en büyük ölçeğini 2400 × 2400 km olarak veriyor ve topluluklarının görüşünü aktarıyor: büyük ölçekli erozyonda Wilbur daha iyi sonuç veriyor. Bu sınır QuadSpinner'ın kendi belgelerinde geçmiyor; resmi bir sınır olarak doğrulanamadı. Bizim kıtamız 7000 km'yi aştığı için bu ayrım önemli.

**Wilbur'un tarifi** (yazarı Joe Slayton, ProFantasy forumu, 2020) doğrudan Python'a aktarılabilir. Sıra şöyle:

1. Çukurları doldur.
2. En yüksek yüksekliğin yaklaşık %5'i kadar mutlak gürültü ekle. Yüzdesel gürültü kullanma; dağları ovalardan daha gürültülü yapar.
3. Çukurları yeniden doldur. Gürültünün parçaladığı nehirleri bu ikinci doldurma yeniden birleştirir.
4. Akış birikimine dayalı oyma uygula (akarsu güç yasasına benzer).
5. Hafif bir parçacık erozyonu geçişi yap.

Yazarın uyarısı: ham akış oyması "hidrolojik olarak akla yatkın olmayan" şeyler yapar, sonraki geçişler bunun için gerekli.

**Bu araca etkisi.** Ticari yazılımlar ağır hesabın parçası olamaz: ya Windows'a bağlılar ya da lisans ve kurulum sorunları var. World Machine ve Houdini teknik olarak Linux'ta çalışıyor ama bağımlılık olarak değil, istenirse elle yapılacak isteğe bağlı bir son işlem olarak düşünülebilirler. Yükseklik haritası çıktısını kare bir karo olarak da verebilmek, ince işi Gaea'da yapmak isteyenlere yardım eder.

## 6. Bilimsel arazi evrimi araçları

**goSPL.** Bu işin bilimsel karşılığına en yakın araç: küresel, levha hareketiyle sürülen, çökelme, deniz dibi birikimi ve küresel bükülme hesaplayan bir arazi evrimi modeli. Çok aktif; son sürüm 2026.7.14 ve depoya Kasım 2026'da commit geliyor. GPL-3. Ama ağır: MPI, PETSc ve paralel HDF5 istiyor. PyPI'da yalnızca kaynak paket var; pratikte `geodels` conda kanalından ya da Docker imajından kuruluyor. Bellek asıl sınır: 10 km'lik küresel ağ en az 16 işlemci ve işlemci başına yaklaşık 6,6 GB istiyor, yani Actions makinesine sığmaz. Salles ve arkadaşlarının 2023 Science makalesi 10 km'de, süper bilgisayarlarda, 128 işlemciyle koşmuş ve modeli elle hazırlanmış geçmiş yükseklik haritalarına doğru "dürtmüş". Kıyıyı sabit tutmak yerleşik değil; yalnızca belgelenmemiş bir `zfit` ayarı ya da sınırları sabit bir 2B bölge buna yaklaşıyor. Dağ yağışı yalnızca 2B ağlarda çalışıyor, küresel ağda çalışmıyor.

**Fastscapelib.** Sürüm 0.3.0 (Haziran 2025), GPL-3. O tarihten beri yeni commit yok. Kıyıyı sabit tutmak için en uygun araç: her düğüme "sabit değer" durumu verilebiliyor ve bu düğümler taban seviyesi oluyor. Kendi gezegen örneği tam olarak bunu yapıyor: kıyı şeridi sabit, okyanus maskeli. HEALPix küre ızgarası pip paketlerinde yok, yalnızca conda-forge'da. Raster ve üçgen ağ ızgaraları her yerde var. Yalnızca akarsu güç yasası ve raster üzerinde doğrusal difüzyon içeriyor; çökelme, bükülme ve levha hareketi yok. Yayınlanmış performans ölçümü yok.

**Landlab.** Sürüm 2.11.0 (Nisan 2026), MIT lisanslı, pip ile kuruluyor, aktif. Kıyıyı sabit tutmak sınır düğümü durumuyla kolay. SPACE bileşeni çökelmeyle birlikte erozyon yapıyor; bükülme ve deniz dibi taşınımı bileşenleri de var. Küresel ikosahedral ızgarası genç ve çukur bulma algoritmasının belgelerinde "iyi ölçeklenmiyor" uyarısı var. Erozyon bileşenlerinin küresel ızgarada sınandığına dair test bulunamadı.

**Badlands.** Bakım sürümleri dışında gelişmiyor, numpy 2'yi desteklemiyor. Önerilmiyor.

**Geçmiş yükseklik haritası üreten araçlar.** Levha tarihinden yükseklik haritası üreten, başsız çalışan, pip ile kurulan bir araç yok. Utrecht'in "paleogeography calculator"ı (yükseklik kabuk kalınlığı ve izostaziden, okyanus derinliği taban yaşından) 2020'de duyuruldu ama kodu yayımlanmadı. TopoChronia ve Terra Antiqua QGIS eklentileri ve belirli modellere bağlı. Scotese'in geçmiş yükseklik haritaları elle yorumlanarak yapılmış. Aktarılabilir olan bu araçların kendisi değil kural setleri: okyanus derinliği taban yaşından (Stein ve Stein), kıta yüksekliği kabuk kalınlığı ve Airy izostazisinden, yay, orojen, rift ve kenar için ayrı şablonlar.

## 7. Bilgisayar grafiği araştırmaları

Grafik literatürü tam bizim problemimizin parçalarını çözmüş, ama hiçbir makale hepsini birleştirmemiş.

**Tektonikten yükseltmeye.**

- **Cordonnier ve diğerleri (2018).** Levha hareketinden kabuk kalınlaşma hızını hesaplayıp onu yükseltmeye çeviriyor: u = α · dq/dt. Ortalama yükseltmeyi yılda yaklaşık 0,5 mm'ye ölçekliyor ve sabit tarafta yükseltmeyi sıfırlayan yordamsal bir fay ekliyor.
- **Cortial ve diğerleri (2019).** Daha ucuz bir tarif veriyor: yükseltme, çarpışma cephesine uzaklığın, göreli levha hızının ve yüksekliğin çarpımı. Kullanıcı çalışmasında tektonik gezegenler fraktal gezegenlere karşı 97'ye 47 oy aldı.
- Bu makalelerin hiçbiri izostaziyi modellemiyor.

**Kıyıyı sabit tutmak.** Bu bir son işlem değil, bir sınır koşulu. Bunu destekleyen dört kaynak var:

- **Tzathas ve diğerleri (2024)** doğrudan bir sınır maskesi alıyor ve maskelenen hücrelerin yüksekliği sabit kalıyor.
- **FastFlow (2024)** çıkış hücrelerini "deniz kıyılarında, alanın içinde" kabul ediyor.
- **Fastscapelib** her düğümde sabit değer durumunu destekliyor.
- **Cordonnier ve diğerleri (2016)** yalnızca alan kenarını deniz seviyesinde sabitliyor.

İki ek koşul var. Tzathas'a göre problemin iyi tanımlı olması için yükseltme sınırda sıfıra inmeli. Cordonnier 2016 da sonucu en çok kıyıya yakın yükseltme eğiminin belirlediğini bulmuş. Yani blok tarihinden gelen yükseltme kıyıya doğru sönümlenmeli. 13. konuya eklenen "kıyı kısıtı yapay basamak üretmesin" sorusunun cevabı da bu.

**Çözücü.** Braun ve Willett'in (2013) örtük, O(n) yöntemi koşulsuz kararlı. Büyük zaman adımlarına (250.000 yıl) izin veriyor ve 100 ile 300 adımda yakınsıyor. Bu, işlemcili bir Actions makinesinde numpy ya da numba için doğal seçim. Schott'un ekran kartı yöntemi binlerce adım istiyor ve çukur yönlendirmesi yok. Tzathas'ın analitik yöntemi Python ile hızlı (1024² ızgara 8,2 saniye) ama kodu yalnızca ticari olmayan araştırma lisanslı; kopyalanamaz, makaleden yeniden yazılabilir. Çukurlar her adımda yönlendirilmeli; yoksa su kara içinde hapsolur.

**Ayrıntı ekleme.** Schott ve diğerleri (2024) düşük çözünürlüklü bir araziyi 32 katına kadar büyütüp hidrolojik olarak tutarlı ayrıntı ekliyor. Kodu MIT lisanslı.

**Gerçekçiliğin ölçülmesi.** Otomatik sınanabilen ölçütler yayımlanmış:

- Hack yasası uyumu: katsayı 1 ile 6, üs 0,45 ile 0,7 arasında olmalı (Schott 2023).
- Sıfır kırma hacmi, yani her yerden suyun dışarı akabilmesi (Schott 2024).
- Referansa karşı hipsometri (Tzathas 2024).
- Zirve ve boyun istatistikleri (Argudo 2019).
- Geomorfon dağılımları (Argudo 2025; kodu MIT lisanslı).

Galin'in 2019 derlemesi, otomatik doğrulamanın genellikle "tutarlı drenaj testiyle sınırlı" kaldığını söylüyor. Bu ölçütler 20. konunun temelini oluşturacak.

**Geriye dönük modelleme.** Schott ve diğerleri (2023) var olan bir araziden sırt ve vadi ağacını çıkarıp ondan yükseltme haritası kuruyor. Bizim ihtiyacımız bundan farklı (bizde rölyef yok, yalnızca kıyı var), ama yükseltme alanını düzenlenebilir ilkel parçalarla temsil etme fikri istisna karıştırma için doğrudan kullanılabilir.

## 8. GitHub Actions makine sınırları

GitHub'ın kendi belgelerine göre açık repolarda `ubuntu-latest` makinesi 4 işlemci ve 16 GB bellek veriyor; gizli repolarda 2 işlemci ve 8 GB. Her iş en fazla 6 saat sürebilir. Atlas reposu açık olduğu için oradaki süre ölçümleri 4 işlemcili makineden geliyor. Tectonic reposu gizli kalırsa koşular aşağı yukarı iki kat uzun sürer ve bellek yarıya düşer. Bu bir karar konusu ve 23. konuda ele alınacak.

## 9. Bu araca çıkan sonuçlar

**Mimari sonuçlar.** Pratik yığın şu şekilde ortaya çıkıyor:

- Blok hareketleri: pyGPlates ya da düz numpy ile Euler dönmeleri.
- Yükseltme ve kabuk kalınlığı: kendi kural tabanlı üreticimiz, maskenin içinde.
- Erozyon: kıyıyı sabit değer düğümleriyle tutan Fastscapelib ya da Landlab.

goSPL, deniz dibi birikimi ya da bükülme gerekirse ve kaba (25 ile 35 km) bir küresel koşu yeterliyse isteğe bağlı bir eklenti olabilir. Ticari yazılımlar bağımlılık olamaz. Kesin seçimler 8, 12 ve 13. konuların işi.

**Kodlanmaya değer çıkarım kuralları.**

- En genç okyanusları önce kapat: yapboz gibi oturan, birbirinin aynası pasif kenarlar en genç rifttir.
- Kıtaların bir süper kıtaya toplanıp toplanamadığını sına.
- Her kıyı parçasını kenar türüne göre sınıflandır: önde aktif, arkada geri çekilen, genç okyanusa bakan pasif.
- Dağları süs değil kanıt say. Kıyı sırası dalmadır, iç kuşak sütürdür, geniş plato çoklu çarpışma ya da düz dalma ister, ada yayı olmadan kısa ve kırık kıyı sırası eski bir orojendir. Yaşı yükseklik ve pürüzlülükten oku.
- Sınır topolojisini denetle: yalnızca üçlü kavşak, dört yönlü kavşak yok, dalma için düzgün yaylar, levhaların çoğu hem kara hem okyanus içerir, Dünya büyüklüğünde bir gezegende yaklaşık 12 ile 18 levha.
- Hız ve zaman ölçeklerini akla yatkınlık denetimi olarak kullan.
- Tek başına volkanlar ve adalar bir sıcak nokta izine ya da bir dalma zonuna oturmalı.

**Tuzaklar.**

- **Çözüm tek değil ve hiç olmayabilir.** Gerçek Dünya'da bir çözümün var olduğu bilinir, kurgusal bir haritada bilinmez. Araç birden çok aday tarih sunmalı, çelişkileri zorla oturtmak yerine göstermeli ve okyanus tarihinde geniş bir hata payını kabul etmeli. Bu, brief'teki "çelişki sessizce düzeltilmez" şartıyla ve 10. konuyla örtüşüyor.
- **Kıyı çizgisi kabuk sınırı değil.** Sahanlık ve kıta kabuğu kıyının ötesine uzanır. Blok sınırlarını kıyıya değil kabuk kenarına koymak gerekebilir.
- **Gürültüyle üretilmiş kıyıların tektonik bilgisi azdır.** Merak'ta yapılmış kıyıların ne kadar bilgi taşıdığı bu yüzden belirsiz. Brief'teki "kıyı geometrisi tarihe ipucu verir" ilkesi bu sınırla birlikte uygulanmalı.
- **Bazı istekler gerçekçi olmayabilir.** Böyle istekler için nadir gerçek örnekler sunulmalı (Tarım havzası, Anadolu mikro levhası, antesedan nehirler) ya da istisna defterine yazılmalı. Lunt'un ve Game of Thrones ekibinin serbestliklerini açıkça yazması bunun iyi örnekleri.
- **Topluluk kuralları birbiriyle çelişiyor ve yanlış içeriyor.** Yalnızca jeologların doğruladığı kurallar kodlanmalı.

**Senin için iki somut öneri.**

1. Maske gelince Merak'a içe aktarıp History sekmesinin bu kıtadan hangi levhaları çıkardığına bakmak. Ücretsiz sürümde de çalışıyor olmalı; bu doğrulanamadı. Sonucu bizim çıkarımımızla karşılaştırmak için bağımsız bir referans olur.
2. Tectonic reposunun açık mı gizli mi kalacağı. Bu karar Actions makinesinin gücünü iki kat değiştiriyor. Kararı 23. konuda vereceğiz.

## 10. Doğrulanamayanlar ve boşluklar

- Merak History sekmesinin levha çıkarım kalitesi ve yalnızca kara maskesiyle nasıl davrandığı; "Coastline lock"ın tam işlevi.
- Gleba'da içe aktarılan kıyının koşudan sonra korunup korunmadığı.
- World Machine'in ekransız bir Linux makinesinde çalışıp çalışmadığı ve lisansının bulut makinelerine izin verip vermediği.
- Wilbur'un güncel sürümü (sitesine erişilemedi, yalnızca arama özeti var).
- Gaea'nın 2400 km sınırının resmi olup olmadığı.
- Worldbuilding Pasta'nın dört dağ türü için verdiği kesit profilleri yalnızca görsel olarak var; sayılar çıkarılamadı.
- Reddit erişimi engelledi, Cartographers' Guild giriş istedi, YouTube video sayfaları doğrulama istedi. Bu kaynaklar yalnızca arama özetleri ve başlıklar üzerinden görüldü.
- 2025 ve 2026 grafik araştırmaları büyük ölçüde Fransız laboratuvarlarının arşivi (HAL) üzerinden tarandı. Başka grupların çalışmaları eksik kalmış olabilir.

## Başlıca kaynaklar

Tam liste ve her bilginin tek tek kaynağı `arastirma/notlar/01/` içindeki beş dosyada.

- Merak Map Maker: https://merakmapmaker.com (uygulama kodu, değişiklik günlüğü, fiyat tablosu)
- GPlates indirme sayfası: https://www.gplates.org/download/
- GPlates kullanım kılavuzu: https://www.gplates.org/docs/user-manual/
- pyGPlates 1.0.0 duyurusu: https://discourse.gplates.org/t/pygplates-1-0-0-released/1020
- GPlates forumu, dünya kurgu bölümü: https://discourse.gplates.org/t/about-the-worldbuilding-category/764
- Worldbuilding Pasta, tektonik: https://worldbuildingpasta.blogspot.com/2020/01/an-apple-pie-from-scratch-part-va.html
- Worldbuilding Pasta, GPlates rehberi: https://worldbuildingpasta.blogspot.com/2020/06/an-apple-pie-from-scratch-part-v.html
- Worldbuilding Pasta, yer şekilleri: https://worldbuildingpasta.blogspot.com/2021/07/an-apple-pie-from-scratch-part-viia.html
- Worldbuilding Pasta, arazi iş akışı: https://worldbuildingpasta.blogspot.com/2023/03/an-apple-pie-from-scratch-part-viic.html
- Game of Thrones tektonik haritası: https://www.auscope.org.au/media-1/got
- Orta Dünya jeolojisi, EGU 2025: https://blogs.egu.eu/divisions/gd/2025/08/13/one-ring-to-rule-them-all-the-geology-of-middle-earth/
- Acks, Orta Dünya dağları: https://reactormag.com/tolkiens-map-and-the-messed-up-mountains-of-middle-earth/
- Lunt, Orta Dünya iklimi: https://www.paleo.bristol.ac.uk/~ggdjl/reports/middle_earth_1.4.pdf
- Worldbuilding Stack Exchange, levha kuralları: https://worldbuilding.stackexchange.com/questions/247575
- Gleba: https://calandiel.itch.io/gleba
- GeoChronicler: https://geochronicler.netlify.app/instructions.md
- WorldEngine: https://github.com/Mindwerks/worldengine
- PlaTec: https://github.com/Mindwerks/plate-tectonics
- Gaea indirme sayfası: https://quadspinner.com/download
- World Machine Build 4069: https://help.world-machine.com/topic/build-4069-dragontail-peak/
- Kilroy's Kartography: https://kilroys-kartography.com/realistic-fantasy-maps-an-overview/
- Wilbur erozyonu, yazarın tavsiyesi: https://forum.profantasy.com/discussion/9770/wilbur-erosion
- goSPL HPC ölçekleme: https://gospl.readthedocs.io/en/latest/user_guide/hpc_scaling.html
- Salles ve diğerleri 2023: https://hal.science/hal-04880511/document
- Fastscapelib gezegen örneği: https://fastscapelib.readthedocs.io/en/latest/examples/planetary_py.html
- Landlab: https://github.com/landlab/landlab
- Utrecht paleogeography calculator: https://meetingorganizer.copernicus.org/EGU2020/EGU2020-2402.html
- Cordonnier ve diğerleri 2016: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf
- Cordonnier ve diğerleri 2018: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonnier18TVCG.pdf
- Cortial ve diğerleri 2019: https://hal.science/hal-02136820/file/2019-Procedural-Tectonic-Planets.pdf
- Schott ve diğerleri 2023: https://hal.science/hal-04049125/file/2022-uplift-author.pdf
- Schott ve diğerleri 2024: https://hal.science/hal-04565030/file/2024-MultiScaleHydro-Author.pdf
- Tzathas ve diğerleri 2024: https://hal.science/hal-04525371/file/Analytical_Terrains_EG.pdf
- FastFlow 2024: https://hal.science/hal-04684270/file/FastFlowPG2024_Author_Version.pdf
- Argudo ve diğerleri 2025: https://hal.science/hal-05246144/file/2024-metrics-author.pdf
- GitHub makine özellikleri: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
