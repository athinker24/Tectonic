# Minecraft dünyasına çevirme: ön araştırma (2026-11-23)

Amaç: bu depoda üretilen rastgele dünyaları gerçekçi araziyle Minecraft dünyası olarak kullanmak; istenince Merak çıktısı da
verilmeye devam edilsin. Bu belge yalnız araştırmadır; kod yazılmadı. Kaynaklar sonda. "Tahminim" yazan sayılar ölçüm değildir.

## 1. Asıl sorun: ölçek

Bizim dünyalar tüm gezegen: 40 032 km × 20 016 km. Merak çıktısında bir piksel ekvatorda 2,5 km, iç modelde 7,4 km.
En yüksek tepe 4662 m (dunya2).

Minecraft'ın sınırları:
- Yatay: dünya sınırının yarıçapı yaklaşık 30 milyon blok, yani 1 blok = 1 m ile gezegen yatayda sığar. Ama dosya boyutu sığmaz.
  Bir bölge dosyası 32 × 32 yığın (512 × 512 blok) tutar; bir hesaplayıcı sitesi yığın başına yaklaşık 45 KB veriyor.
- Dikey: varsayılan −64 ile 320 arası, 384 blok. Veri paketiyle (dimension_type) en çok 4064 blok (−2032 ile 2031); min_y + height − 1
  2031'i geçemez.

Ölçek seçenekleri (dosya boyutları tahminim, 45 KB/yığın ile, tamamı önceden üretilirse):

| ölçek | dünya boyu (blok) | 4662 m dağ | önceden üretilirse | not |
|---|---|---|---|---|
| 1:1000 (tüm gezegen) | 40 000 × 20 000 | 4,7 blok | yaklaşık 140 GB | Yotan'ın Dünya haritası bu ölçekte; Everest 10 yerine 70 blok yapılmış, yani dikey yaklaşık 7 kat abartılmış |
| 1:100 (tek kıta, 4000 km) | 40 000 × 40 000 | 47 blok | yaklaşık 280 GB | 1 blok = 100 m; bizim modelin 74 katı ayrıntı gerekir |
| 1:25 (bir bölge, 1000 km) | 40 000 × 40 000 | 186 blok | aynı | yürünebilir, "gerçek" boyutlu dağlar ancak burada başlar |
| 1:1 (bir bölge, 40 km) | 40 000 × 40 000 | 4662 blok (sığmaz, 4064 sınırı) | aynı | Terra++/Tellus gerçek Dünya'yı böyle yapıyor |

Sonuç: tüm gezegen Minecraft'ta ancak 1:1000 dolayında ve dikey abartıyla olur; o ölçekte dağlar oyunda tepecik kalır, gerçekçilik
haritada görünür, yürürken görünmez. Oyunda gerçekçi arazi istenirse dünyanın bir parçası 1:25 ile 1:100 arasında verilmelidir.
İki kullanım ayrı tutulmalı: "gezegen haritası" (1:500 ile 1:2000) ve "oynanır bölge" (1:10 ile 1:100).

## 2. Bizim yöntemin Minecraft için en büyük avantajı

Merak için 7,4 km'lik modelde yetiniyoruz. Minecraft'ta 1:25 ile 1:100 arası 25 ile 100 m ayrıntı ister. Bunu bulanık büyütme ya da
gürültüyle uydurmak gerekmiyor: karşılık yöntemi zaten her bölgeye gerçek bir yerin yükseklik modelini yerleştiriyor. AWS Terrain
Tiles daha yüksek yakınlıkta (zoom 10 ile 12; yaklaşık 150 ile 40 m) aynı kaynaklardan örneklenebilir. Yani seçilen bölge için gerçek
vadiler, gerçek sırtlar o ölçekte üretilebilir. Döndürme, aynalama, bükme ve çok bantlı karışım aynı kalır; yalnız çözünürlük artar.
Arnis da (OpenStreetMap'ten Minecraft'a) yüksekliği aynı AWS karolarından alıyor; yöntem kanıtlanmış.

Gereken yeni işler:
- **Bölge seçimi ve yerel çözünürlük:** dünya haritasından bir kutu seçilir; o kutuda karşılıklar yüksek yakınlıkta yeniden örneklenir.
- **Biyom haritası:** Minecraft her sütun için biyom ister. Bizde iklim yok (ilk dünyada ayrı bir iklim atlası oturumu vardı). Enlem,
  yükseklik, denize uzaklık, egemen rüzgâr ve dağ gölgesinden basit bir iklim, ondan Minecraft biyomlarına eşleme gerekir.
- **Akarsular:** karışım dokuları drenajı bozar (kaynaktan gelen vadiler birbirine bağlanmaz, çukurlar kalır). Oyunda bu kapalı göller
  ve kopuk vadiler olarak görünür. Çukur doldurma (priority flood) ve akış yönü (D8) ile akarsu ve göl üretmek gerekir. Merak çıktısı
  da bundan yararlanır.
- **Dikey eşleme:** deniz seviyesi, dikey abartı ve üst sınır (384 ya da veri paketiyle 4064) seçilir; ovaların "ova" kalması için
  doğrusal olmayan bir eğri (Merak'ın karekök eğrisine benzer) düşünülmeli.

## 3. Minecraft'a yazmanın yolları

### A. NovoAtlas (Fabric/NeoForge modu, görüntüden dünya üretimi)
Yükseklik haritası (gri PNG) ve biyom haritası (her renk bir biyom, 8 bit RGBA, kayıpsız) bir veri paketine konur; mod Minecraft'ın
arazi biçimini ve biyom yerleşimini bu görüntülerden alır, gerisini (mağaralar, cevher, ağaçlar, yapılar) oyun kendisi üretir.
Mağara biyomları için katman başına ayrı harita, isteğe bağlı sıvı yükseklik haritası var (1.4.0). Fabric 1.21.10 sürümü listelenmiş.
- Artı: dünya önceden üretilmez, oynandıkça üretilir; yüzlerce GB dosya yok. Bizden yalnız birkaç PNG ve veri paketi çıkar.
- Eksi: sunucuda (ya da tek oyunculuda) mod gerekir. Yatay ölçek ayarının nasıl çalıştığı bulunamadı (sürüm notunda "Horizontal
  Scaling" başlığı var, ayrıntı wikide). Tectonic gibi gürültü tabanlı modlarla uyumsuz olduğu yazılıyor. Bilmiyorum: çok büyük
  görüntülerde (40 000 piksel) bellek davranışı.

### B. WorldPainter (masaüstü, Java)
16 bit yükseklik haritası alır, katmanlar (mağara, tünel, ağaç, biyom maskeleri), Java dünyası olarak dışa aktarır. 2.24.0 sürümünün
1.20.5 ve 1.21'i desteklediği bir topluluk gönderisinde yazıyor (resmî sürüm notu görmedim). `wpscript` ile JavaScript betikleri
komut satırından çalışır (`wp.getWorld().fromFile(...)`, `wp.exportWorld(world).toDirectory(...)`). Dünya haritası projeleri
(DerMattinger/MinecraftEarthMap) tam olarak bizim iş akışımızı WorldPainter betiğiyle yapıyor: NASA yükseklik ve batimetri, ESA
arazi örtüsünden biyom maskeleri; 1:1000 Dünya için 62 dakika ve 19,1 GB bellek bildiriyorlar.
- Artı: olgun, yaygın; mağara ve süsleme katmanları hazır; sonuç modsuz oynanan düz bir dünya.
- Eksi: tüm alan önceden üretilir (dosya boyutu, süre, bellek). Eski belgeye göre dışa aktarma ayarları betikten değiştirilemiyor,
  `.world` dosyasına önceden kaydedilmeli (sekiz yıllık bilgi, güncelliği doğrulanmadı). Bedrock dışa aktarımı doğrulanamadı.
  Biyom maskesinde kenar yumuşatma olmamalı (renk birebir biyoma eşlenir).

### C. Bölge dosyalarını (Anvil, .mca) Python'dan doğrudan yazmak
- amulet-core: kararlı 1.9.26, 2.0 alfa (2025); Amulet Map Editor'ün çekirdeği. 1.21 desteği arama sonuçlarında doğrulanmadı.
- anvil-parser-modern (bakımı süren çatal; denemeleri 1.14 ile 1.15), mcworldlib (nbtlib üstünde; 2021 sürümü), NBT kitaplıkları.
- Artı: her şey bizim elimizde, tek dil (Python), harici program yok.
- Eksi: yüzey kuralları, biyom, mağara, ağaç, su, ışık gibi her şeyi bizim yazmamız gerekir; Minecraft sürümleriyle blok durumu ve veri
  sürümü değişir; Python büyük alanlarda yavaştır. Arnis aynı işi bu yüzden Python'dan Rust'a taşımış.

### D. Başkalarının yolları (yöntem için örnek)
- **Arnis** (Rust): OpenStreetMap ve yükseklik verisinden Java ve Bedrock dünyası yazar; yükseklik için AWS Terrain Tiles (bir kaynakta
  Overture Maps). Doğrudan dosya yazma yolunun çalışan örneği.
- **Terra++ / Terra 1-to-1 / Tellus / Terrarium**: gerçek Dünya'yı oyun içinde, oynandıkça 1:1 üretir; eskileri dikey sınır için
  Cubic Chunks'a dayanıyor. Bizim karşılık örneklemesinin oyun içi akrabası.
- **Dünya haritaları** (Yotan 1:1000, Earth Tiles, MinecraftEarthMap): WorldPainter + yükseklik + biyom maskesi.
- **GDMC HTTP + gdpc**: oyun açıkken HTTP ile blok okuyup yazma; küçük alanlar ve yapı yerleştirme için, arazi üretimi için değil.

## 4. Değerlendirme (seçimim, gerekçeli)

1. Depo iki çıktılı olmalı: aynı iç dünya modelinden "merak" (bugünkü) ve "minecraft". İç model (maske, tarih, karşılıklar, bant
   karışımı) ortak kalır; Minecraft için ek olarak iklim ve biyom, akarsu, yerel yüksek çözünürlük gelir.
2. Minecraft çıktısının ilk hedefi **NovoAtlas veri paketi** olmalı: bizden yalnız yükseklik ve biyom PNG'si çıkar, Minecraft
   ayrıntıyı ve mağaraları kendisi üretir, yüzlerce GB önceden üretme yoktur. İkinci hedef **WorldPainter betiği** (modsuz dağıtılacak
   hazır harita gerekirse). Doğrudan .mca yazmak en çok iş, en az kazanç; şimdilik değil.
3. İlk deneme küçük tutulmalı: bir dünyadan 1:50 ölçekte 1000 × 1000 km'lik bir bölge (20 000 × 20 000 blok), dikey 384 blok.
   Ölçülecekler: oyunda ovaların ve dağların görünüşü, NovoAtlas'ın bu boyuttaki görüntüyle bellek ve hızı, sınırda dikiş olup olmadığı.

## 5. Bilinmeyenler (doğrulanmadı)
- NovoAtlas'ın yatay ölçek ayarı, en büyük görüntü boyutu ve özel biyom (veri paketi biyomu) desteği.
- WorldPainter'ın güncel sürümde betikten dışa aktarma ayarlarını değiştirip değiştiremediği; Bedrock desteği.
- amulet-core'un 1.21 yazma desteği.
- Gerçek yığın başına dosya boyutu (45 KB bir hesaplayıcı sitesinin kaba değeri; okyanus yığınları daha küçük olabilir).
- Adla ilgili not: Minecraft'ta "Tectonic" adlı çok bilinen bir dünya üretimi veri paketi ve modu var (Apollo; kıta ölçeğinde kara,
  uzun sıradağlar). Depo bu adla yayımlanırsa karışır; NovoAtlas'ın Tectonic ile birlikte çalışmadığı da yazılıyor.

## Kaynaklar
- Minecraft boyut sınırları: https://minecraft.wiki/w/Tutorial:Adding_a_new_dimension , https://bugs-legacy.mojang.com/browse/MC-278998 ,
  https://modrinth.com/datapack/higher-heights-datapack/version/4-4064
- Bölge dosyası: https://minecraft.fandom.com/wiki/Region_file_format ; yığın boyutu tahmini: https://west-games.com/minecraft-world-file-size-calculator/
- NovoAtlas: https://modrinth.com/mod/novoatlas , https://www.curseforge.com/minecraft/mc-mods/novoatlas
- WorldPainter betik ve komut satırı: https://worldpainter.net/trac/wiki/Scripting , https://www.worldpainter.net/trac/wiki/ExportingFromCommandLine?version=1 ,
  https://github.com/Captain-Chaos/WorldPainter/wiki/Scripting-API , https://www.worldpainter.net/doc/faq
- Dünya haritaları: https://github.com/DerMattinger/MinecraftEarthMap , https://github.com/MattiBorchers/MinecraftEarthMap ,
  https://www.planetminecraft.com/project/earth-11000/ , https://evanthebearge.gitbook.io/minecraft-earth-map/minecraft-earth-tiles/configuring-earth-tiles/map-features
- Arnis: https://wiki.openstreetmap.org/wiki/Arnis , https://github.blog/open-source/maintainers/arnis-turns-any-place-on-earth-into-a-minecraft-world
- Terra++ ve benzerleri: https://github.com/BuildTheEarth/terraplusplus , https://github.com/orangeadam3/terra121 , https://modrinth.com/mod/tellus ,
  https://modrinth.com/mod/terrarium-earth , https://pcgamer.com/a-11-scale-model-of-earth-is-possible-in-minecraft-with-mods-and-your-help
- Python kitaplıkları: https://pypi.org/project/amulet-core , https://pypi.org/project/anvil-parser-modern/ , https://pypi.org/project/mcworldlib/0.2021.10
- GDMC: https://pypi.org/project/gdpc , https://www.github.com/Niels-NTG/gdmc_http_interface
- Tectonic (Minecraft): https://github.com/Apollounknowndev/tectonic , https://modrinth.com/mod/tectonic

## 6. Earth Platform incelemesi (2026-11-23; pirut/earth-platform, son işleme dd31a85, 22 Kasım 2026)

Sahibin gönderdiği mod ve tanıtım videosu. Kaynak kodu okunarak incelendi (`ROADMAP.md`, `docs/FLAGS.md`, `CubicSettings`,
`EarthSettings`, `EarthGenerator`, `TerrariumTileSource`, `Drainage`, `ElevationLayer`). Çalıştırılmadı.

### Yükseklik ve boyut sorununu nasıl çözüyor
- **Kendi küp motoru:** dünya Y −16384 ile 16383 arası (32 768 blok). Vanilla'da her yığın dipten tepeye tek sütun olduğu için
  bu yükseklikte her yığın yaklaşık 85 kat büyüyordu; dünyayı 16 blokluk küplere bölmüşler, yalnız oyuncunun yakınındaki küpler
  yükleniyor. Madencilik, yaratıklar, kızıltaş, Nether ve End çalışıyor. Bizim en yüksek tepe 4662 m, en derin deniz 4000 m:
  1 blok = 1 m'de sığar.
- **Önceden üretme yok:** bir yere ilk gidildiğinde o yerin verisi indirilir, diskte saklanır (varsayılan 8 GB), sonra çevrimdışı
  çalışır. Gezegenin tamamı için yüzlerce GB dosya sorunu yok.
- **Uzak görüş:** kendi uzak arazi çizicisi (Voxy ve Distant Horizons'tan esinli), varsayılan 94 km, en çok 397 km. Gerçek ölçekte
  dağları görebilmek için bu şart.
- **Yatay ölçek ayarı var:** her dünyanın ayar dosyasına `earth.metresPerBlock` yazılıyor (Mercator'da varsayılan 1/cos(enlem)).
  Dikey her zaman metredir. Bu değer büyütülürse (ör. 10 m/blok) dünya alanı küçülür, dikey abartı kendiliğinden gelir.
  Arayüzde değiştirilebildiği görülmedi; ayar dosyası elle değiştirilebilir. Denenmedi.

### Bizim dünyalarımız buna nasıl bağlanabilir
- **Biçim aynı:** yükseklik, AWS Terrain Tiles'tan terrarium PNG karoları olarak okunuyor (Web Mercator, zoom 0 ile 15), bizim
  kaynaklarımızla aynı biçim ve aynı adres. Disk önbelleği de `z/x/y.png` düzeninde.
- **Gezegen boyu aynı:** bizim dünyalar 40 032 km çevreli; Dünya ile aynı. Kendi gezegenimiz onların ızgarasına 1:1 oturur;
  bizim eşdikdörtgen enlem boylam modelimiz Web Mercator karolarına çevrilir (±85° ötesi kaybolur; karalarımız ±75° içinde).
- **Çatallamadan deneme yolu (denenmedi):** önbelleği bizim karolarımızla önceden doldurmak ve oyunu
  `-Dearthplatform.earth.offline=true` ile açmak ("yalnız önbellekteki yerler üretilir"); Copernicus, 3DEP, HRDEM, REMA, IGN, GSI
  katmanları bayraklarla kapatılır. Önbellek LRU ile kırpılıyor; oturumda okunan dosyalar silinmiyor.
- **Çatallayarak yol:** karo adresi koda gömülü (`TerrariumTileSource.AWS_TERRAIN_TILES`); bir sistem özelliğiyle değiştirilebilir
  hale getirilirse bizim bir karo sunucumuz (yerel HTTP) doğrudan kullanılır. Lisans LGPL-3.0: çatal serbest, kod değişiklikleri açık
  kalmalı.
- **Asıl engel, Dünya'ya özgü öteki veriler:** biyomları CHELSA iklimi, ESA WorldCover arazi örtüsü, JRC yüzey suyu, RESOLVE
  ekobölgeleri, ağaç boyu ve kayaç haritaları belirliyor. Bunlar gerçek Dünya'nın koordinatlarıyla gelir; bizim gezegene
  uygulanırsa ormanlar, göller, çöller yanlış yere düşer. İki çıkış var:
  1. Eski dünya kipi: ayar dosyasında `earth.cover` boşsa "arazi örtüsünden önce yapılmış dünyalar gibi" üretiyor: sıcaklık enlem ve
     yükseklikten, nem geniş gürültüden, iç su yok. Yeni dünyada bu alanı boşaltmak ayar dosyasını elle değiştirmeyi gerektirir;
     denenmedi.
  2. Kendi iklim ve arazi örtüsü rasterlerimizi onların biçiminde (bulut uyumlu GeoTIFF) üretmek ve kaynak adreslerini çatalda
     değiştirmek. Bizde iklim modeli henüz yok; zaten Minecraft için gerekecekti.
- **Akarsular:** `Drainage` akarsuları yalnız yükseklikten çıkarıyor (zoom 10'da çukurları doldurup akış biriktiriyor, vadide ve
  yeterli havzada akarsu). Bu bizim karolarımızda da çalışır ve bizim kopuk vadiler sorununa da örnek bir çözüm.

### Ayrıntı sorunu (bizim tarafımızdaki asıl iş)
1 blok = 1 m'de oyun 30 m ve daha ince yükseklik ister (onlar zoom 13 ile 15 okuyor; ince kabartıyı gürültüyle ekliyor). Bizim iç
model 7,4 km. Bütün gezegen için zoom 13 karoları önceden üretmek olanaksız (yaklaşık 67 milyon karo, tahminim birkaç TB). Gereken:
istenen karoyu o anda üreten bir karo sunucusu. Yöntemimiz buna uygun: çok bantlı karışımın kaba bantları ve ağırlıklar küresel
modelden, ince bantlar her karşılığın kaynağından (aynı AWS karoları, yüksek zoomda) eşleme ile anında örneklenir. Eşleme (benzerlik
ve ince levha eğrisi), sınır gürültüleri ve bükme küresel ve belirlenimci olduğundan komşu karolar arasında dikiş çıkmaz. Merak çıktısı
aynı iç modelden kalır.

### Riskler
- Alfa sürüm; Minecraft 1.21.1, NeoForge ya da Fabric; 4 GB (gölgelendiriciyle 6 GB) bellek.
- Küp motoru vanilla kayıt biçimi değil; yüksekliği kendisi denetleyen modlar ayrı düzeltme istiyor.
- Önbellek yolu, ayar dosyası alanları ve bayraklar sürümden sürüme değişebilir; çatalsız yol bunlara bağımlı.
- Karo sunucusunun hızı: bir ilk ziyaret yüzlerce karo istiyor; her karo için eşleme ve birkaç kaynağın örneklenmesi gerekir.

### Kaynaklar (bu bölüm)
- https://github.com/pirut/earth-platform (README, ROADMAP.md, docs/FLAGS.md, CHANGELOG.md, kaynak kodu)
- https://github.com/pirut/earth-platform/releases
- Tanıtım videosunun dökümü (sahibin iletisi).
