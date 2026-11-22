# Yol: siyah beyaz maskeden Merak'a hazır yükseklik haritası

Bu belge, işi yürütecek yapay zeka (ya da kişi) içindir. Her aşamada ne yapılacağı, harita sahibine ne sorulacağı, hangi komutun
çalışacağı ve neyin denetleneceği yazılıdır. Aşamalar sırayla yapılır; bir aşama sahibin onayı olmadan kapanmaz.

Komutların hepsi depo kökünden: `python3 -m mk projeler/AD KOMUT`. Koordinatlar her dosyada **maske pikseli** (x sütun, y satır,
sol üst 0,0); Merak'la ilgili bölge dosyaları (`merak_bolgeler.json`) Merak pikselidir.

---

## 0. Kurulum
- `pip install -r requirements.txt`. Ağ: `s3.amazonaws.com` (AWS Terrain Tiles) erişilebilir olmalı. Karolar `karolar/`'a
  önbelleğe alınır (git dışı); başka bir önbellek için `MK_KAROLAR=/yol`.
- Örnekle sına: `python3 -m mk projeler/ornek hepsi` (yaklaşık yarım dakika) ve `python3 testler/test_merak.py`.

## 1. Maske
**Sahipten iste:** siyah beyaz kıyı maskesi (PNG, beyaz kara). Kenar yumuşatması olmasın. JPEG gelirse eşiklenir ama kıyıda
basamak kalabilir; mümkünse PNG iste.

**Yap:** `projeler/AD/` klasörü aç, maskeyi koy, `proje.json` yaz (şablon: `projeler/ornek/proje.json`), `maske` komutunu çalıştır.

**Sahibe sor ve proje.json'a yaz:**
- Kıtanın genişliği (km) → `genislik_km`. Bilmiyorsa birkaç seçenek öner (ör. Avustralya genişliği 4000 km, Avrasya 10000 km).
- Üst kenarın enlemi → `ust_enlem`; isterse orta boylam → `merkez_boylam`.
- Merak'ta yükseklik haritasını kaç boyutta dışa aktardığı → `merak_boyut` (bkz. 7. aşama). Bilinmiyorsa 16000 × 7719 yaz ve 7. aşamada doğrula.

**Denetle:** komutun yazdığı km/piksel değeri makul mü (bizim ilk haritada 2,1 km)? Kıta çerçeveye sığıyor mu?

## 2. Parçalar
**Sahipten iste:** maskenin üstüne renkli çizgilerle parça sınırları ve her parçaya bir numara. Şunları sor (kıyıdan
çıkarılamaz, sahibin kararıdır):
- Hangi kıyılar birbirini tamamlıyor (bir zamanlar bitişikti)?
- Hangi parçalar bugün birbirine çarpıyor, hangisi hangisinin altına giriyor?
- Hangi parça neye benzemeli (dağlık, düz, kalkan, yayla, volkanik)?

**Yap:** çizimden kesme çizgilerini ve her parçanın içinden bir tohum noktasını maske pikseli olarak oku → `parcalar.json`.
`parcalar` komutu → `cikti/parcalar.png`. Sahibin çizimiyle yan yana göster.

**Not:** kararları ve sahibin sözlerini `projeler/AD/KARARLAR.md`'ye yaz. Sahibin yanıtlamadığı sorularda kendi seçimini yaz ve
"seçimim" diye işaretle.

## 3. Tarih (isteğe bağlı ama önerilir)
Her sıradağın, havzanın ve yarığın bir sebebi olursa hem harita tutarlı olur hem sahip değişiklik isterken hikâyeye bağlayabilir.
`TARIH_SABLONU.md`'yi `projeler/AD/tarih.md` olarak doldur: dönemler, olaylar, bugünkü levhalar, yer şekli adları. Dünya'dan benzer
örnekler kullan (Biscay makas açılması, Zagros, Himalaya, Kızıldeniz). Sahibe özetle, onay al. Haritaya her yeni yer şekli eklerken
tarihte karşılığı olsun.

## 4. Karşılıklar
**Yap:**
1. Her parça (ya da parça içindeki bölge) için `KATALOG.md`'den bir gerçek yer seç. Sahibe hangi parçaya neyin karşılık geldiğini
   söyle ve onay al.
2. `karsiliklar.json`'a yaz (alanlar `mk/karsilik.py` başında). En az iki denetim noktası: hedef pikseldeki önemli bir yer ↔ kaynaktaki
   boylam ve enlem. İki nokta yön ve ölçeği belirler; fazlası bükerek uydurur.
3. `onizle AD` → `cikti/oniz_AD.png`: kırmızı kıyı, sarı çokgen, camgöbeği noktalar. Kaynağın kıyıları hedefin kıyısına benzemek
   zorunda değil; hedefin kıyısı her zaman maskedir.
4. Uyarıları oku: **kaynakta denize düşen pay** %10'u, **kutu dışına düşen pay** %2'yi geçiyorsa düzelt (kutuyu genişlet, noktaları
   kaynaktaki karaya kaydır, ölçeği küçült). Aksi halde düz, yapay alanlar ve düz dikişler çıkar.
5. Yükseklik ölçeğini dünyaya uydur: büyük sıradağlar için `yukseklik_egri` ile indir (ör. Himalaya → Kafkas ölçeği).

## 5. Birleşim, özellikler, sahiple döngü
**Yap:** `karsilik` → `ozellik` → `ciz` → `olcum`. `cikti/topografya_etiketli.png`'yi sahibe gönder.

**Döngü:** sahip ekran görüntüsünde kırmızıyla işaretleyip yorum yazar. Görüntünün hangi çerçeve olduğunu bil (topografya.png
maske boyutunda; küçültülmüşse oranı hesapla), işaretten maske pikseli koordinat oku, `ozellikler.json`'a adlı bir adım ekle:
- "Buraya sıradağ / şu yönde aksın / ucu incelsin" → `sirt` (cizgi sahibin çizdiği yön; `doku` ile gerçek bir sıranın dokusu;
  `incel` uçlar; `yukseklik` köşe başına liste).
- "Ova çok yüksek / plato gibi" → `alcalt` (taban 40 ile 200 m, kat 0,2).
- "Biraz kabarsın / çarpışmadan etkilensin" → `kabart`.
- "Büyük çukurlar var" → `cukur_doldur`.
- "Bu bölgenin hikâyesi/şekli değişsin" → `yama` (başka bir karşılık).
Her değişiklikten sonra `olcum` ile sayıları denetle ve sahibe sayılarla bildir (ör. "tepe 2900 m, geçit 1800 m").

**Sahibin tercihleri (ilk haritada öğrenildi; aksini söylemedikçe uygula):**
- Kıyı şekli kutsaldır: maskeye, adacıklara, koylara dokunma; ada ekleme.
- Doğrudan kopya olmasın: aynala, döndür, buk, karıştır.
- Ölçek duygusu: bir sıradağ dünyanın çeyreğini kaplamasın.
- **Boru görünümü olmasın**: düzgün kesitli yuvarlak sırtlar reddedilir. Gerçek doku, gürültülü genişlik, bükülmüş kenar.
- Sıralar uçlarda **incelerek** bitsin; komşu sıraya **bağlı** ve doğal aksın; yapıştırılmış gibi durmasın.
- Düz çizgi, kutu kenarı, dikiş, yapay plato hemen fark edilir.
- Ovalar dağlara oranla gerçekten alçak olsun.
- Kısa iletişim: yalnız teslim edilecek dosyalar ve gerekirse yapıştırılacak kısa metin.

## 6. Son görüntü ve teslim
`hepsi` komutu tüm hattı çalıştırır ve Merak dosyasını üretir. Sahibe: etiketli topografya, ölçüm özeti, Merak dosyası.

## 7. Merak
### 7.1 Kodlamayı ölç (her yeni Merak sürümü ya da yeni proje için bir kez)
Merak'ın gri ↔ metre eşlemesi belgelenmemiştir; ölçülür:
1. Sahipten iste: Merak'ta herhangi bir haritada açık okyanusa, **Flatten** aracına sayı girerek düz tepeli en az dört plato
   (iki kara, iki deniz; ör. 4000, 1000, 99, −524, −1995 m), birbirinden ve kıtadan uzak.
2. Merak'tan **16 bit** dışa aktarım (PNG; JPEG ya da ekran görüntüsü olmaz). Boyutunu `proje.json` `merak_boyut`'a yaz.
3. `plato DISA.png 4000 1000 99 -524 -1995` → `merak_kodlama.json`. Denetim satırında her plato kendi metresine 1 ile 2 m içinde
   dönmeli. İlk ölçüm (2026-11): S 14642, beyaz 8000 m, deniz D 6840, p 0,607 (karada karekök, deniz seviyesi %22,3 gri).

### 7.2 Dosyayı üret ve içe aktar
- `merak` → `cikti/merak_W.png` (16 bit, Merak dışa aktarımıyla aynı boyut), `cikti/merak_maske_W.png` (saf siyah beyaz),
  `merak_olcek.json`, önizleme.
- Merak'ta: Import image → terrain, sekme **"Heightmap / mask (auto)"**, **"Fill world"**, içe aktar. "Place on existing" kullanma
  (kutusu dünyayı doldurmaz; saydamlığı nasıl okuduğu bilinmiyor).
- Sohbet aracı 8000 pikselden geniş görüntü göndermiyorsa zip'le.
- Denetim: içe aktardıktan sonra Merak'ta birkaç noktanın yüksekliğine bak (Hover info), `rehber` çıktısındaki nokta yükseklikleriyle karşılaştır.
- Deniz tabanı yer tutucudur (kıyıda −60 m, 300 km'de −4000 m, hiçbir yer −40 m'den sığ değil). Derinliği sahip Merak'ta ayarlar.

### 7.3 Sahip elle işledikçe
Sahip Merak'ta bölgeleri elle işler (genel hatları koruyup küçük ayrıntıyı Merak aşınma aracıyla deneme yanılma üretir). Her turda
sahipten 16 bit dışa aktarım al ve:
- `fark DISA` → `cikti/fark.png` ve parça özetleri (kırmızı: sahibinki yüksek, mavi: bizimki). Sahibe "nerede ne kadar saptı" diye
  sayılarla göster.
- `birlestir DISA` → sahibin işi, kıyısı ve denizi aynen; `merak_bolgeler.json`'daki çokgenler (Merak pikseli) bizim yükseklikle
  değiştirilir; benekler temizlenir. `--kiyi` ile karada kıyı rampası (kıyıdaki kabarık şeridi bastırır).
- `uslup` → sahibin dokunmadığı karayı onun üslubuna yaklaştırır: genel hat bizden, ince doku sahibin işlediği yerden yamalarla.
- `rehber` → `cikti/rehber_W.png`: Merak'a referans katmanı olarak Fill world ile konacak saydam eş yükseklik ve nokta yüksekliği
  katmanı. Sahibe elle işlerken: tabanı Flatten ile sayıyla kur, sırtları dar fırçayla çiz, Smooth'u az, Erode'u çok kullan,
  zirveleri aşınma payı için %5 ile %10 fazla kur.

**Her Merak çıktısında denetim:** kıyı çizgisi farkı 0 (`(yeni > S) != (eski > S)`), deniz değişmedi (temizlik dışında).

## 8. Sık yapılan hatalar
- Ekran görüntüsünden ölçmek (ölçekli, JPEG, kenarlı). Yalnız dışa aktarılan PNG ölçülür.
- Kaynakta deniz olan yerleri hedefin karasına düşürmek: düz, yapay alanlar. Uyarıya bak.
- Süzgeçte denizi hesaba katmak: kıyıyı aşağı çeker, kıyıya paralel yapay sırt bırakır (araçlar yalnız karada süzer).
- Sığ denizi deniz seviyesine çok yakın bırakmak: Merak'ta benek benek kara çıkar (araçlar −40 m'den sığ deniz bırakmaz).
- Etiket ya da bölge listesinde bir parçayı unutmak: her listeyi `parcalar.png` üstünde gözle denetle.
- Sahibin işaretini yanlış çerçevede okumak: işaretli görüntünün boyutunu ve hangi dosyadan geldiğini her seferinde sor ya da çıkar.

## 9. Kayıt
Her aşamanın sonunda: kararlar `KARARLAR.md`'ye, değişiklikler commit'e. Sahibe yalnız değişeni ve sayıları söyle.
