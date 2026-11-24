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
- Dikkat: 6000 m üstü 123 tek piksellik tepe var (v2'de 2), 17'si 8000 m'de (beyaz, doymuş); yalnız 15'i bozkır düzenlemesinin
  içinde, geri kalanı sıradağların tepelerine dağılmış. Çevreleri 3000 ile 5000 m. Kaynağı bilinmiyor (fırça izi ya da Merak'ın
  içe/dışa aktarması). Dokunulmadı.
