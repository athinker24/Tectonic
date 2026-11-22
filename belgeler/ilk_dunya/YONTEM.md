# Siyah beyaz maskeden Merak haritasına: yöntem ve başka haritada uygulama

Bu belge, bu depoda bir kıyı maskesinden başlayıp tektonik tarihi, topografyayı ve Merak'a aktarılan yükseklik haritasını nasıl
ürettiğimizi aşama aşama anlatır; ardından aynı işi başka bir maskeyle yapmak için gerekenleri listeler. Merak'a aktarımın
teknik ayrıntıları (gri kodlama, çerçeve, kayıt) `merak/MERAK.md`'dedir; bu belge onu tamamlar.

---

## A. Aşamalar (yaptığımız sırayla)

### 0. Girdi: siyah beyaz kıyı maskesi
- `maske.png`, 3808 × 2914, beyaz kara, siyah deniz. Sahibin çizdiği kıyı şekli; kesin ve değişmez kabul edildi.
- Sonradan sahip maskenin elle düzeltilmiş bir sürümünü verdi (1024 × 1024 kare JPEG, "v2"). Merak'taki kıyı bu v2'dir; tarih ve
  topografya ise ilk maske üzerinde üretildi. İkisi %97,7 örtüşür (IoU); aradaki fark kıyı şeritleri ve küçük koylar.

### 1. Danışma: maskenin parçaları ve sahibin kararları (`notlar/KARARLAR.md`)
- Sahip maskeyi renkli çizgilerle 7 parçaya böldü (mavi 1|2, mor 2|3, sarı 4|5, yeşil 5|7) ve hangi kıyıların birbirini tamamladığını,
  hangi parçaların bitişik olduğunu, hangi çarpışmaların bugün etkin olduğunu söyledi.
- Bu kararlardan kaba katı parça uydurmaları yapıldı (dönme açıları, dönme merkezleri, kayma miktarları).
- Sahibin yanıtlamadığı sorularda seçim yapıldı ve not edildi (ölçek, sıradağın en yüksek ucu, çarpışma yaşları).

### 2. Ölçek ve enlem
- Çerçeve 8000 km genişlik, yaklaşık 6100 km yükseklik; üst kenar 50°K, alt kenar yaklaşık 5°G. 2000 piksellik çizim çerçevesinde
  1 piksel = 4 km (`olaylar.KM_PX`, `GEN = 2000`, `YUK = 1530`); tam maskede 1 piksel ≈ 2,1 km.
- Enlem iklim (kar çizgisi, yağış) ve sonra atlas ile Merak yerleşimi için gerekli.

### 3. Tektonik tarih (`olaylar.py`, tek kaynak)
- Parça sınır çizgileri (`CIZGI`), parça başına hareket anahtar kareleri (`HAREKET`: zaman, açı, dx, dy), bugünkü levhalar (`LEVHALAR`),
  dönemler ve olaylar (`DONEMLER`), yer şekilleri ve adları.
- Mantık: bugünkü kıyılardan geri gidilir; birbirini tamamlayan kıyılar kapatılır, aradaki okyanuslar ve çarpışmalar zamanlanır,
  her sıradağ ya da havza bir olaya bağlanır. Dünya'dan benzer örnekler kullanıldı (Biscay makas açılması, Zagros, Himalaya, Kızıldeniz).
- `animasyon.py`: 340 milyon yıldan bugüne katı parça animasyonu (mp4, gif) ve dönem kareleri.
- `belge.py`: dönemleri anlatan PDF (Chromium ile basılır).

### 4. Topografya, birinci yol: kurallarla (`arazi.py`, eski)
- Olaylardan yapı katmanı: kuşaklar, yaylalar, ovalar, volkanlar; yağış; fastscapelib ile akarsu aşınması; gölgeli harita.
- Sahip beğenmedi ("bu bölgelerin her birinin ne olduğu belli zaten, dünya karşılıklarını kullanalım ama aynısı olmadan").
  Çıktı `cikti/topografya_kural.png` olarak saklı.

### 5. Topografya, ikinci yol: gerçek dünya karşılıkları (`benzer.py`, `dem.py`) — ana yöntem
- `dem.py`: AWS Terrain Tiles (terrarium kodlaması `h = R·256 + G + B/256 − 32768`), zoom 6 (yer yer 7). Karolar
  `kaynak/karolar/`'da önbelleğe alınır. `Kaynak(lon0, lon1, lat0, lat1, z)`; kaynaktaki deniz, aynalanmış komşu karayla doldurulur
  (`doldur`), istenmeyen kısımlar `kes` çokgenleriyle deniz sayılır.
- `benzer.py` `KARSILIK` listesi: her bölge için bir gerçek yer (ör. 2 → aynalı Tarım, Tanrı Dağları, Himalaya ön kuşağı;
  4 → aynalı İberya, Fransa, İran). Her karşılık:
  - benzerlik dönüşümü (döndürme, ölçek, ayna) ve ince levha eğrisi (thin plate spline) kontrol noktaları (`nokta`: hedef piksel ↔
    kaynak boylam/enlem) ile hedefe bükülür;
  - seçenekler: `ayna`, `carpan` (yükseklik çarpanı), `yukseklik_egri`, `oncelik`, `yumusak_km`, `bukme_kat`, `kes`, `capa_bolge`;
  - parça etiketlerine göre ağırlıklarla karıştırılır; ağırlık sınırları ±70 km gürültüyle bükülür, tüm harita yaklaşık 40 km
    bükülür; kıyıya rampa.
- `bilesik()` içindeki son işlemler, sahibin geri bildirimleriyle eklendi (her biri adlı bir adım): çanak sırtları ve tabanı,
  ön ova alçaltma, sırt tabanı yükseltme, çukur doldurma, düz çizgileri bastırma, sırt uçlarını inceltme, ekvator kubbesi,
  doğu kıvrımı, yarımada rift omzu. Bunların hepsi bu haritaya özgü piksel koordinatlarıyla yazılmıştır.
- Çıktılar: `cikti/benzer_z.npy` (kara, 2914 × 3808), `cikti/son_z_tam.npy` (batimetriyle), `cikti/topografya*.png`.

### 6. Atlas sınaması (`atlas_cikti.py`)
- Ayrı bir iklim atlası deposu bu yüksekliği kullanarak iklim ve biyom üretti. Atlas oturumu belirli istekler gönderdi (ör. çanağın
  batısında bozkır için en az 3000 m'lik bir sırt, ekvatorda savan fazlası için kalkan yükselmesi); bunlar `bilesik()` adımlarına
  dönüştü ve atlas girdileri yeniden üretildi. Atlas deposu salt okunurdu; yalnız çıktı dosyaları ve atlasa yapıştırılacak mesaj verildi.

### 7. Merak'a aktarım (`merak_*.py`, ayrıntılar `merak/MERAK.md`)
1. Doğrusal kodlamalı tüm dünya dosyaları ve renk haritası denemeleri (Merak'ın kodlaması henüz bilinmiyordu).
2. Sahibin v2 maskesine oturtulmuş yükseklik (`merak_v2.py`).
3. Sahip Merak'ta doğu yarıyı elle işledi; Merak dışa aktarımı ve altı test platosuyla Merak'ın gri kodlaması çözüldü.
4. Sahibin dışa aktarımı ile bizim verinin birleştirilmesi: elle dokunulmamış düz alanlar bizim veriyle doldu (`merak_birlestir.py`),
   işaretli yapay alanlar düzeltildi (`merak_duzelt.py`), yalnız karada kıyı rampası (`merak_kiyi.py`), benekler temizlendi
   (`merak_temizle.py`).
5. Karşılaştırma için katkısız sürüm (`merak_saf.py`), sahibin üslubuna yaklaştırma (`merak_uslup.py`, `merak_uslup2.py`),
   elle işleme rehberleri (`merak_rehber.py`), Geography Lab levha şeması (`merak_levha.py`).

---

## B. Sahibin tercihleri (geri bildirimlerden çıkan kurallar)

Başka bir haritada da büyük olasılıkla geçerli; yeni işe başlamadan okunmalı.

- Kıyı şekli kutsaldır: maskeye, adacıklara, kıyı girintilerine dokunulmaz; ekleme yapılmaz.
- Dünya karşılıkları kullanılır ama **doğrudan kopya olmaz**: aynalanır, döndürülür, bükülür, karıştırılır.
- Ölçek duygusu: bir sıradağ dünyanın çeyreğini kaplamamalı (Mor için Himalaya fazla geldi, Kafkas ölçeği istendi).
- **Boru görünümü istenmez**: düzgün kesitli, yuvarlak, yapay sırtlar reddedildi. Çözüm: aynı kaynak zincirinden gerçek doku,
  gürültülü genişlik, bükülmüş kenarlar, sivrilen uçlar.
- Sıralar **uçlarda incelerek** bitmeli; "bağlantılı" ve "doğal akan" görünmeli; komşu sıradan ayrı, yapıştırılmış gibi durmamalı.
- Düz çizgiler, kutu kenarları, dikişler, yapay platolar hemen fark edilir ve reddedilir (kutu yaması, düz kuzey güney sırt).
- Ovalar dağlara oranla gerçekten alçak olmalı (ön ova "plato gibi" eleştirisi).
- Hikâye bozulmadan değişiklik: her topografya değişikliği `olaylar.py`'de bir olayla gerekçelendirildi.
- İletişim: kısa, yalnız teslim edilecek dosyalar; sahip ekran görüntüsünü kırmızıyla işaretleyip gönderir, koordinat bu işaretten
  okunur (görüntü çerçevesi bilinmeli).
- Merak'ta sahibin elle yöntemi: genel hatlar korunur, küçük ayrıntı aşınma aracıyla deneme yanılma üretilir.

---

## C. Başka bir haritada denemek için gerekenler

### C.1 Girdiler
1. **Siyah beyaz kıyı maskesi** (PNG, kenar yumuşatmasız). Yüksek çözünürlük iyidir; bizde 3808 × 2914.
2. **Ölçek ve konum**: genişlik (km) ve üst kenar enlemi (ya da iki enlem). Bunlar olmadan iklim ve dünya karşılık ölçekleri anlamsız.
3. **Parça çizgileri ve sahip kararları**: hangi kıyılar birbirini tamamlıyor, hangi parçalar bitişikti, bugün hangi sınırlar etkin.
   Bunlar sahipten alınmalı; kıyı şeklinden tek başına çıkarılamaz (ör. 5'in dönüş yönü belirsiz kaldı).
4. **Her parça için gerçek dünya karşılığı** (hangi bölge neye benzemeli). Sahibin onayı alınmalı.
5. **Merak için**: hedef dünyada kıtanın yeri (enlem, boylam) ve Merak'ın kendi dışa aktarım boyutu.

### C.2 Ortam
- Python 3, numpy, scipy, Pillow, matplotlib, imageio; isteğe bağlı fastscapelib (kurallı aşınma için) ve Chromium (PDF için).
- **Ağ erişimi**: `s3.amazonaws.com` (AWS Terrain Tiles, `elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`). Bir karşılık için
  z=6'da birkaç düzine karo yeter. Karo önbelleği git dışıdır.
- Bellek: 16k Merak dosyası float32 olarak 494 MB; 16 GB yeter, ama kıta kutusuna kırparak çalışmak gerekir.

### C.3 Neyin yeniden yazılması, neyin aynen kullanılabileceği

Haritadan bağımsız (aynen kullanılır):
- `dem.py` (karo indirme, terrarium çözme, aynalı doldurma, örnekleme).
- `benzer.py` içindeki makine: `esleme` (benzerlik + ince levha eğrisi), karıştırma, ağırlık sınırı bükme, kıyı rampası, çizim
  (`arazi.ciz`).
- Merak kodlaması ve araçları: `coz`/`kodla` (`merak_birlestir.py`), `merak_temizle.py`, `merak_kiyi.py`, `merak_uslup2.py`'nin
  yamalı doku sentezi, `merak_rehber.py`'nin eğri ve nokta yükseklik çizimi. Bunlar yalnız dosya yollarını ve kırpma kutularını
  değiştirmeyi gerektirir.
- Kayıt yöntemi: iki kara maskesi arasında ölçek ve kaymayı IoU en büyükleyerek bulmak (Nelder-Mead).

Haritaya özgü (yeniden yazılır):
- `olaylar.py`: `CIZGI`, `HAREKET`, `BAGLI_3`, `LEVHALAR`, `DONEMLER` tamamen bu dünyanın hikâyesidir.
- `animasyon.py`: `TOHUM` (parça tohum noktaları) ve kesme çizgileri.
- `benzer.py`: `KARSILIK` listesindeki her kaynak kutusu ve kontrol noktası (`nokta`, piksel koordinatlarıyla); `bilesik()`'teki
  bütün adlı adımlar (`SIRT_TABAN`, `SIRT_GUNEY`, `CUKUR`, `EKVATOR`, `MAVI`, `URAL`, `SARI`, `MOR_SIRT`, `dogu_mor`, `YARIMADA`)
  ve etiket konumları.
- Merak tarafı: v2 kıta kutusu, kayıt sayıları (`v2_olcek.json`, `birlesik_olcek.json`), `merak_duzelt.BOLGE` çokgenleri,
  `merak_levha.py`'deki levha çokgenleri ve hendek çizgisi, rehberdeki yakın plan kutuları, kıta kırpma kutusu.

### C.4 Önerilen sıra (yeni harita için)
1. Maskeyi al; parça çizgilerini ve kararları sahiple netleştir; `notlar/KARARLAR.md`'ye yaz.
2. Ölçek ve enlemi sabitle.
3. Tarihi kur (`olaylar.py`), animasyonla tutarlılığı sına (kapanan kıyılar gerçekten oturuyor mu).
4. Her parça için karşılık seç, `benzer.py onizle` ile tek tek önizle; kontrol noktalarını sahibin geri bildirimiyle ayarla.
5. `benzer.py bilesik` ve `ciz`; sahibin işaretlediği sorunları adlı adımlar olarak ekle; her adımda olay listesini güncelle.
6. Merak'ta önce **tek bir test**: açık okyanusa en az üç ayrı yükseklikte (biri deniz altında) düz plato koy, 16 bit dışa aktar,
   kodlamayı yeniden ölç. Merak sürümü değişmiş olabilir; 1. bölümdeki sabitler varsayılmamalı.
7. Merak'ın dışa aktarım boyutunda dosya üret, "Heightmap / mask (auto)" + "Fill world" ile içe aktar, `_platolu` sürümle
   içe aktarma eğrisini denetle.
8. Sahip elle işledikçe dışa aktarımı al, birleştir, temizle; kıyı çizgisi ve deniz farkı 0 denetimini her çıktıda çalıştır.

### C.5 Sık yapılan hatalar
- Ekran görüntüsünü ölçüm kaynağı sanmak: ekran görüntüleri ölçekli, JPEG ve kenarlı olur; yalnız dışa aktarılan PNG ölçülür.
- 8k etiketini 16k'ya en yakın komşuyla taşıyınca kıyı piksellerinin etiketsiz (0) kalması; etiketsizler en yakın etiketle doldurulmalı.
- Süzgeçte denizi hesaba katmak: kıyıyı aşağı çeker ve kıyıya paralel yapay bir sırt bırakır; yalnız karada normalleştirilmiş süzgeç
  kullanılmalı.
- Sığ denizi deniz seviyesine çok yakın bırakmak: Merak'ta benek benek kara çıkar.
- Doldurulacak bölge listesine bir parçayı unutmak (bizde Uzun Yarımada); etiket listesi her seferinde haritada görsel olarak denetlenmeli.
- Kaynak verideki dikişler (karşılıklar arası çokgen kenarları) "saf" sürümde görünür; birleştirmeden önce ya kaynakta giderilmeli ya da
  ağırlık sınırları bükülmeli.
