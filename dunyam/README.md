# Dünyam (sahibin dünyası): Minecraft hazırlığı

Kaynak dosyalar `kaynak/` altında, git'te değil (16k PNG; `.gitignore`). Sahip 2026-11-23'te verdi (`merak_son_saf_16k.zip`).

| dosya | ne | ölçüm |
|---|---|---|
| `kaynak/son_temiz_16k.png` | son hâl: doğu yarısı sahibin Merak'ta elle işlediği, batı yarısı gerçek dokular | 16000 × 7719, 16 bit; kara %3,38; kara %10/%50/%90 = 113/598/1636 m, en yüksek 6759 m |
| `kaynak/saf_temiz_16k.png` | yalnız gerçek dokular (karşılık yöntemi) | aynı boyut; kara %10/%50/%90 = 79/554/1596 m, en yüksek 5690 m |

- İki dosyanın kıyısı birebir aynı (fark 0 piksel). Yükseklik farkı doğuda büyük (|fark| ortancası 160 ile 365 m), batıda küçük
  (3 ile 7 m; %5 ile %15'inde 100 m'den çok).
- Merak kodlaması (`S = 14642`, beyaz 8000 m) ile okundu. Kara 36°B ile 36°D, 5°G ile 50°K arası (Merak çerçevesinde).
- İklim atlasının arazisi (`dunyam-atlas-mobil/dunya/dunyam_heightmap.png`) bu kıtanın büyütülmüş ve kaydırılmış hâli: boylamda
  1,217, enlemde 1,218 kat, IoU 0,953 (atlas ızgarasında, Nelder-Mead). Atlasta kara 44,5°B ile 43,1°D, 7°G ile 60°K.
  Kıyı farkı: atlas ızgarasında 21 379 piksel (atlas karasının %4,7'si); çoğu kıyı boyunca ince şerit (çözünürlük), birkaç gerçek
  fark var (doğu kıyısında yaklaşık 1700 piksellik parça). Görüntü: `atlas_merak_kiyi.png` (gri ortak, kırmızı yalnız atlasta kara,
  mavi yalnız Merak'ta kara).

## Ana kalıp (2026-11-23, sahibin kararı)
- Sahip: "Asıl kalıp bu son verdiğim zipteki; sadece bir bağlantı eklenmesi gerekiyor batı kısmında." Atlastaki öteki kıyı farkları
  Merak'ta yanlışlıkla değişmiş şeyler. Atlastaki bağlantının şekli rastgeleydi; tek önemli olan batı okyanusunun kapanması,
  olabildiğince doğal biçimde (dış şekil ve arazi).
- `kaynak/ana_16k.png` = `son_temiz_16k.png` + `bagla2.py` ile batıdaki kara köprüsü. Ayarlar `bagla_ayar.json`.
- Yöntem (seçimim): köprü, kuzey kıyısındaki sıranın güneye uzanan kolu (Orta Amerika'nın Kordilyera'nın devamı olması gibi).
  Arazi: iki kütlenin kıyı yüksekliklerinden harmonik taban + eksen boyunca sırt (800 m, kıvrılmış) + aynı haritanın komşu dağından
  alınan ince doku; eksenden uzaklaştıkça deniz tabanına iner. Kıyı bu arazinin 0 m eğrisi, elle çizilmedi.
- Ölçüm: denizden karaya 3256 piksel (yaklaşık 20 000 km²), karadan denize 0; yeni kara %10/%50/%90 = 52/216/481 m, en yüksek
  1018 m. Eski kıyının yeni karaya 7 piksel içindeki şeridinde 1277 kara pikselinin yalnız yüksekliği değişti (Merak'ın kıyı rampası
  eski kıyıyı alçak bırakmıştı, koyu çizgi kalıyordu); kıyı çizgisi aynı. Kara bileşeni (30 piksel üstü) 22 → 21.
- Denenip bırakılanlar: atlastaki kıstağı taşımak (düz, yama gibi); Tehuantepec kıstağının gerçek arazisi (90° döndürülmüş;
  dağlık ucu yapıştırılmış yumru gibi, ova parçaları kopuk, doku çevreden keskin). Üç ayar seçeneği: `bagla_secenekler.png`
  (sol üst önce; sol alttaki seçildi). Önce ve sonra: `bagla_once_sonra.png`.

## Dikiş düzeltmesi (2026-11-23, sahibin işareti: "kıtaların asıl şekilleri kenarlarda hâlâ belli")
- Sebep: Merak'ın dışa aktarımı kıyıyı birkaç piksel alçak ve benekli bırakıyor; birleşince eski kıyı çizgisi yeni karanın içinde
  ince koyu çizgi olarak kalıyordu. Ayrıca eski kıyı ile yeni kara arasında bir iki piksellik deniz aralıkları ve ince bir oluk vardı.
- Düzeltme (`bagla2.py`): köprüye bitişik bir iki piksellik deniz aralıkları kapatılır; eski kıyının yeni karaya değen kesiminin
  25 piksel çevresinde kaba yükseklik birleşik araziden yeniden kurulur (Gauss 8 piksel, yalnız karada); eski kıyının 5 piksellik
  benekli şeridinin ve birleşme çizgisinin 8 piksel içinin ince dokusu atılır; yeni karanın tabanı eski kıyıya yakın yerde eski
  karayla aynı düzeyde başlar.
- Ölçüm: denizden karaya 3330 piksel, karadan denize 0; yalnız yüksekliği değişen eski kara 6199 piksel (kıyı çizgisi aynı).
  Güney birleşme yerinde çok hafif bir ton kaldı.

## Ana kalıp v3 (2026-11-24): sahibin Merak dışa aktarımı
- Kaynak: `kaynak/merak_disa_2026-11-24.png` (sahip, "Custom-World-heightmap-16bit", 16000 × 7719). Atlasın son arazisi bundan
  üretildi (atlas notundaki yeni kayıt ölçeği bununla tutuyor).
- v2'ye göre: Merak'ın içe ve dışa aktarması bütün haritayı yaklaşık 3 piksel sağa ve aşağı kaydırmış ve biraz ölçeklemiş
  (sx 1,00015, sy 1,00067; kara maskesi IoU 0,9916). Kaydırma düzeltilince ortak karada |fark| ortancası 15 m. Sahibin iki tutarlı
  düzenlemesi: Kaynak Sırası'nın güney ucunda iç deniz kıyısı (x 7699..8079, y 2474..2624) ortalama +689 m; onun kuzeybatısında
  bir şerit (x 7785..7947, y 2190..2339) ortalama −115 m. Görüntü `v3_fark.png` (kırmızı yükselen, mavi alçalan, sarı yeni kara,
  yeşil kaybolan kara; kaydırma düzeltilmiş).
- Karar (seçimim): v3 = dışa aktarımın kendisi + kurallı temizlik (`temizle_v3.py`): 700 piksellik kara beneği (445 parça) deniz,
  129 582 sığ deniz pikseli −40 m. Kara ve kıyı aynen; Merak ve atlasla birebir. v2 ile birleştirme denendi, bırakıldı.
- İğne tepeler (sahip: "tek piksellik tepeleri çevrelerine uygun şekilde yumuşat"): v3'te 6000 m üstü 123 piksel vardı (v2'de 2),
  17'si 8000 m'de (doymuş). Tek piksel değil, 1 ile 13 piksellik koni kümeleri (fırça izi); komşu en yükseğini aşma ortancaları
  −21 m, komşu ortalamasını aşma ortancaları 1523 m. Ölçüt (`tepe_yumusat.py`): 5 × 5'te en yüksek, 20 km'lik halkanın
  ortancasından 1000 m'den, 8 komşu ortalamasından 400 m'den yüksek tepe: 1364 iğne. Halka ortancası üstündeki aşım
  1500·tanh(aşım/1500) ile sıkıştırılır, tepeden 10 km'de tam, 20 km'de sıfır; biçim kalır, boy kısalır. Sonuç: 113 070 piksel
  değişti (ortanca 50 m düşüş), tepe noktası düşüşü ortanca 391 m, %90 1372 m, en çok 6500 m; en yüksek 8000 → 6183 m;
  6000 m üstü 123 → 3 piksel; kıyı farkı 0. Önce/sonra: `tepe_once_sonra.png` (sol önce). Yeniden üretmek için
  `temizle_v3.py` sonra `tepe_yumusat.py`.

## Earth Platform kavram denemesi (2026-11-24; `kavram/kavram.py`)
- Bölge: Kaynak Sırası'nın güneybatı eteği ve iç deniz kıyısı; v3 merkezi (7755, 2520), atlas kaydıyla 7,696°B 37,125°K;
  5120 × 5120 piksel, 30 m (154 km). Kara payı 0,80, taban yüksekliği %5/50/95: 477, 1234, 3240 m.
- Taban: v3 bikübik; kıyı sıfır eş eğrisi. Kıyı farkı (tabana göre) 0 piksel.
- Doku (AWS z12, yalnız 1,5 km'den kısa dalga boyları), yüksekliğe göre 1800 ile 2700 m arasında yumuşak geçişle:
  - dağ: Orta Yüksek Atlas, 57° döndürülmüş, 1,15 kat. Toubkal çevresi elendi: dağ bölgesinin %37'sine düz ova düşüyordu.
  - yayla: Massif Central (Aubrac ve Margeride), aynalı, −112° döndürülmüş.
  - Genlik: hedef kabartısının kaynak kabartısına oranı (0,25 ile 1,6); 1500 ile 3000 m arasında alt sınır 1'e çıkar ki Merak'ta
    düzleşmiş yüksek platolar düz kalmasın.
- Nehir: bölgeye atlasın tek nehri giriyor (821, kademe 1, 6309 m³/s, 58,5 km). Yatak kaynaktan ağıza azalan profil, yaklaşık
  4 km dalga boylu kıvrım, debiyle genişleyen gürültülü taban, dokulu yamaçlar. Kazı ortancası 151 m: atlas nehri v3'te vadisi
  olmayan bir yayladan geçiyor, sonuç bir kanyon.
- Yapılmadı: çukur doldurma (Earth Platform kendi akaçlamasını z10'da çukur doldurarak yapıyor); terrarium karoları.
- Earth Platform yakın araziyi z15'e kadar okuyor (`EarthGenerator.zoom`, en kaba 9). Çevrimdışı kipte önbellekte olmayan karo
  üretilmiyor (`earthplatform/cache/terrarium-v1/z/x/y.png`). Bu bölgenin z9 ile z15 piramidi yaklaşık 34 bin karo (z15 tek başına 25 281; hesap: 154 km, 37°K).
  Önbelleği doldurmak ya da çatalda yerel karo sunucusu, ikisinden biri gerekiyor.
- Görüntüler: `kavram/genel_kucuk.png` (kırmızı kutular yakın planlar), `kavram/yakin.png` (30 km'lik üç kesit, tam çözünürlük),
  `kavram/taban_sonuc.png` (solda yalnız taban, sağda sonuç).

### Oyuna hazırlık (2026-11-24; `kavram/karolar.py`, `kavram/paket/`)
- Karolar: 36 373 terrarium PNG (z9 100, z10 400, z11 1600, z12 992, z13 1600, z14 6400, z15 25 281), 0,95 GB. Bölge z9 ile z15;
  çevresi yalnız v3 ile z12'de 120 km'ye, z9 ile z11'de 300 km'ye kadar. Bölge kenarında son 3 km'de doku tabana iner.
  z10'dan ince karolarda açık deniz tam 0 m (Earth Platform derinliği z10'dan alır), yükseklik 1/8 m'ye yuvarlı.
- Dünya ayar dosyası `kavram/paket/generator.properties`: `earth.cover` boş (eski dünya kipi). Bu kipte mod arazi örtüsü, iklim,
  uydu, nehir verisi istemez; yalnız yükseklik okur (`CubicSettings.open`).
- Sınama (mod dd31a85 bu makinede derlendi, alpha.76):
  - modun okuyucusu (`TerrariumTileSource`, onarım süzgeçleri dahil) 200 karodan 198'ini hiç değiştirmedi, 2'sinde kıyıda 0,5 m;
  - `GlobalElevation` ile 300 noktada oyunun okuduğu yükseklik ile 30 m model farkı: z15 en çok 0,1 m, z12 en çok 1,0 m;
    deniz noktalarında derinlik z10'dan doğru doldu;
  - çevrimdışı açılan sunucu bu ayar dosyasıyla başlangıç noktasının verisini bizim karolardan hatasız hazırladı (uyarı yok).
  - Sahip 2026-11-24 akşamı kendi bilgisayarında kurdu; dünya açıldı ve yüklendi.
- Teslim: `teslim/dunyam_ep_1..5.zip` (git dışında; gönderim sınırı yüzünden 190 MB'lık beş parça). Kurulum `kavram/paket/KURULUM.txt`.
- Sürüm 2 (aynı akşam, sahibin ilk oyun görüntülerinden sonra; zirve yuvarlak ve pürüzsüz, yamaçlar düzgün basamaklı):
  30 m altına gerçek ince doku (z14 ve z15; ABD NED 10 m: dağda San Juan Dağları, ovada Gila Wilderness; 53° ve 131°
  döndürülmüş iki kat, döşenebilir), genlik eğimle 1 ile 15 m; z13-15 bikübik ve σ 0,8 piksel (30 m kare yüzeyler ve tek
  piksellik çapraz sırtların zikzakları); dağ kaynağında 31,656°K'deki kayık SRTM birleşmesinde doku güveni sıfıra iner.
  Appalachian yaylası ova kaynağı olarak denendi, bırakıldı (yol yarmaları düz çizgi bıraktı). Karolar 1,15 GB, yedi parça.
  Mod okuyucusu 200 karodan 198'ini değiştirmedi. Drive'a yükleme denendi: bağlayıcı çağrı başına yaklaşık 3 MB taşıyor, olmadı.
- Shader: Iris 1.8 en çok 16 render hedefi destekliyor; daha fazlasını isteyen paketler (Complementary r5.9.3, sahibin
  denediği sürüm) "Render target with index 19" hatası veriyor. Photon v1.3b colortex16'ya kadar kullanıyor (ölçüldü).
