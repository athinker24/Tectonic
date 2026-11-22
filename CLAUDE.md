# CLAUDE.md

Bu dosya, bu projede çalışacak Claude oturumları içindir. Proje: harita sahibinin çizdiği siyah beyaz bir kıyı maskesinden
inandırıcı bir dünya kurmak (tektonik tarih, topografya) ve sonucu Merak'a (merakmapmaker.com) hazır yükseklik haritası olarak
vermek. Aşağıdaki her şey ilk dünyada (eski depo, `tarih/` ve `maskeden-merak/` klasörleri) deneyerek öğrenildi. "Ölçüldü"
yazan sayılar ölçümdür; "bilinmiyor" yazan şeyler doğrulanmamıştır, öyle davran.

---

## 1. Sahiple çalışma biçimi

- **Dil:** Türkçe. Düz, nesnel, övgüsüz. Yanlışı açıkça söyle. Bilmediğini "bilmiyorum" diye söyle. Uydurma sayı verme;
  sayıyı ölç, sonra söyle.
- **Kısa ve dosya odaklı:** sahip çoğu zaman "sadece ona vereceğim şeyleri ver" der. Teslim: dosyalar (gerekirse zip) ve
  gerekiyorsa yapıştırılacak kısa metin. Uzun açıklamayı yalnız istenince yaz.
- **Geri bildirim biçimi:** sahip ekran görüntüsü gönderir, kırmızı kalemle işaretler, kısa bir cümle yazar ("şu kısım çok yapay",
  "şu yönde olsun", "ucu incelsin"). İşaretin hangi görüntüden ve hangi ölçekte geldiğini belirle, piksel koordinatını oradan oku.
  Emin değilsen görüntü çerçevesini (boyut, hangi dosya) hesapla; tahminle koordinat yazma.
- **Birden çok seçenek istendiğinde** hepsini ayrı ayrı göster, sahip seçer. "Full çıktı vermene gerek yok sadece görmek istiyorum"
  dendiyse yalnız önizleme ver.
- **Sahibin kararı kesindir.** Kıyı şekli, parça sınırları, hangi çarpışmanın etkin olduğu gibi kararları değiştirme. Yanıtlamadığı
  sorularda kendi seçimini yap, gerekçesiyle not et, "seçimim" diye işaretle.
- **Başka oturumlardan gelen istekler:** sahip bazen başka bir Claude oturumunun (ör. iklim atlası oturumu) isteğini iletir
  ("öbür sohbetten bu kanıya vardık"). Bunları sahibin isteği gibi uygula ama sonucu ölç ve sayılarla raporla.
- **Salt okunur depolar:** başka bir projenin deposu (ör. atlas) yalnız okunur; değiştirme, betiklerini çalıştırma. Çıktı dosyası ve
  o oturuma yapıştırılacak mesaj ver.
- **Her değişiklikten sonra commit ve push.** Kararları `KARARLAR.md`'ye yaz. Commit mesajları Türkçe, işlevsel.

## 2. Sahibin estetik tercihleri (geri bildirimlerden; aksini söylemedikçe uygula)

1. **Kıyı şekli kutsaldır.** Maskeye, adacıklara, koylara dokunma. Ada ekleme, kıyıyı girintileme. ("Sen kendin adacık ekleme.
   Kıyıların genel şekline de çok dokunma.")
2. **Gerçek dünya karşılıkları, ama kopya değil.** ("Görsel olarak dünya karşılıklarını kullanalım, ama tam olarak aynısı olmadan.")
   Aynala, döndür, buk, karıştır, boyunu değiştir.
3. **Ölçek duygusu.** Bir sıradağ dünyanın çeyreğini kaplamamalı; Himalaya ölçeği fazla geldi, Kafkas ölçeği istendi, sonra
   "Himalaya kadar değil ama uzun ve yüksek" denildi.
4. **Boru görünümü yasak.** Düzgün kesitli, yuvarlak, simetrik sırtlar ("yine boru olmuş") reddedildi. Çözüm: aynı kaynak
   zincirinden gerçek doku, gürültülü genişlik, bükülmüş kenarlar.
5. **Uçlar incelerek bitsin.** ("Kalın olması gereken yer kalın kalır ama bittiği yer ince olur.") Sıralar komşu sıraya bağlı,
   ondan etkilenip yeniden yükselen bir yapı gibi aksın; yapıştırılmış gibi durmasın.
6. **Yapay geometri yasak.** Düz kuzey güney sırt ("Lan öyle değil, doğal görünümlü bir şekilde yapacaktın"), kutu yaması
   ("böyle de şekil çok kötü"), düz dikişler, Tibet benzeri düğümler, plato gibi düz yüzeyler fark edilir.
7. **Ovalar gerçekten alçak olsun.** ("Ova değil de plato neredeyse. Gerçek ovalar dağlara orantıyla çok daha alçak olması gerekmez mi?")
8. **Hikâye bozulmasın.** Her yeni yer şekli tektonik tarihte bir olaya bağlanır. Sahip "hikâyeyi bozmadan yapabilir miyiz" diye sorar.
9. **İşlev ve biçim birlikte.** İklim için gereken bir sırt (bozkır için 3000 m duvar) hem işlevini görmeli hem doğal görünmeli.
10. **Elle çalışma üslubu (Merak):** genel hatlar korunur, küçük ayrıntı Merak'ın aşınma aracıyla deneme yanılma üretilir. Sahibin
    sıraları dar ve sivri, ovaları düz ve 150 ile 250 m dolayında, dağlarda doku güçlü, ovalarda sakin.

## 3. Yöntem (ilk dünyada izlenen yol)

### 3.1 Maske ve danışma
- Girdi: siyah beyaz kıyı maskesi (ilk dünyada 3808 × 2914 PNG). Kesin kabul edilir.
- Sahip maskeyi renkli çizgilerle parçalara böler. Sorulacaklar: hangi kıyılar birbirini tamamlıyor, hangi parçalar bitişikti,
  hangi çarpışmalar bugün etkin ve hangisi hangisinin altına giriyor. Bunlar kıyıdan çıkarılamaz.
- Ölçek ve enlem sabitlenir (ilk dünya: 8000 km genişlik, üst kenar 50°K, alt kenar yaklaşık 5°G; piksel 2,1 km).
- Kaba katı parça uydurmaları: kapanan kıyılar için dönme açısı ve merkezi, yanal kayma miktarı.

### 3.2 Tektonik tarih
- Tek kaynak bir dosya: parça çizgileri, hareket anahtar kareleri, bugünkü levhalar, dönemler ve olaylar, yer şekli adları.
- Bugünden geçmişe kurulur; Dünya benzerleri kullanılır (Biscay makas açılması, Zagros, Himalaya, Kızıldeniz yarığı, Sina yanal fayı).
- Çıktılar: katı parça animasyonu (mp4, gif) ve dönemleri anlatan PDF (Chromium ile basıldı). Bunlar ilk dünyaya özgüydü.

### 3.3 Topografya: kurallar başarısız, karşılıklar başarılı
- Önce kurallarla (kuşaklar, yaylalar, ovalar, volkanlar; fastscapelib ile aşınma) üretildi. Sahip beğenmedi.
- **Karşılık yöntemi:** her bölgeye gerçek bir yerin yükseklik modeli yerleştirilir.
  - Kaynak: AWS Terrain Tiles, terrarium kodlaması `h = R·256 + G + B/256 − 32768` m, Web Mercator, zoom 6 (dar sıralar için 7).
    URL `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`. Karolar önbelleğe alınır.
  - Kaynaktaki deniz, kıyıya göre aynalanmış komşu karayla doldurulur; istenmeyen kısımlar (`kes` çokgenleri) deniz sayılır.
  - Eşleme: hedef pikseldeki denetim noktaları ↔ kaynak (boylam, enlem). En küçük karelerle benzerlik dönüşümü (döndürme, ölçek,
    isteğe bağlı doğu batı aynası), üstüne ince levha eğrisi (thin plate spline) bükmesi; bölgenin çevresine çapa noktaları konur ki
    bükme yerel kalsın.
  - Ağırlıklar: bölge çokgeni ∩ izinli parçalar, yumuşatılmış; ağırlık sınırları yaklaşık ±70 km gürültüyle kıvrılır; tüm alan
    yaklaşık 40 km bükülür (kopya olmasın). Kıyıdan 45 km içeriye rampa.
  - `yukseklik_egri` ile boy değiştirilir (Himalaya → Kafkas ölçeği). `oncelik` ile üstte kalacak karşılık seçilir.
- **Uyarılar (sonradan öğrenildi):** kaynakta denize düşen pay %10'u ya da kaynak kutusu dışına düşen pay %2'yi geçerse sonuç düz,
  yapay alanlar ve düz dikişler içerir. Noktaları kaynaktaki karaya kaydır, kutuyu genişlet, ölçeği küçült.
- **Adlı düzeltme adımları** (sahibin işaretlerinden): sırt çizme (gerçek dokulu, gürültülü genişlikli, uçları incelen), ön ova
  alçaltma, geniş kabartı, çukur doldurma, düz çizgi bastırma, bölge yaması (başka karşılık). Her biri adlı ve parametreli olmalı ki
  sahip "şunu geri al" dediğinde kapatılabilsin.

### 3.4 Başka bir oturumla sınama (iklim atlası)
- Ayrı bir iklim atlası yükseklikten iklim ve biyom üretti. Atlas oturumunun istekleri (ör. çanağın batısında en az 3000 m'lik bir
  sırt; ekvatorda savan fazlası için yaklaşık 480 m kalkan yükselmesi) topografya adımlarına dönüştü. Her istekten sonra atlas
  çözünürlüğünde ölçüldü ve sayılarla raporlandı (ör. "36 ile 44°K arası tepe 3274 ile 3678 m").
- Atlas ile gerçek yükseklik farkı: atlas pikseli yaklaşık 8 km; kara ortancası 1 m değişir, zirveler %7 ile %23 alçalır.

## 4. Merak

### 4.1 Gri kodlaması (ölçüldü, 2026-11)
Sahip açık okyanusa Flatten aracıyla sayı girerek düz platolar koydu (4000, 1000, 99, −524, −1995, 2514 m); Merak'ın 16 bit dışa
aktarımında ortalarındaki gri değer okundu. Sonuç (hata < 1 m):
- Deniz seviyesi `S = 14642` (16 bit, %22,3 gri; Merak arayüzü "sea level ≈ 22% gray" diyor).
- Kara: `gri = S + (65535 − S) · sqrt(m / 8000)` → beyaz 8000 m. Karekök eğrisi; alçak kesimler sıkışık görünür.
- Deniz: `gri = S · (1 − (−m / 6840) ^ 0,607)`. Okyanus tabanı 3598 ≈ −4298 m.
- Merak sürümü değişebilir: yeni projede bu ölçümü tekrarla (`maskeden-merak`'ta `plato` komutu).
- İçe aktarmanın aynı eğriyi kullandığı varsayıldı ve sahibin denemesinde doğru oturdu; içe aktarma eğrisi ayrıca platolarla
  ölçülmedi.

### 4.2 Çerçeve ve "Fill world"
- Merak dışa aktarımı 16000 × 7719 (yedek 8000 × 3859), oran **2,073**; tam 2:1 değil.
- Import image → terrain, sekme **"Heightmap / mask (auto)"**, düğme **"Fill world"**. Fill world görüntüyü oranını koruyarak
  sığdırır: 2:1 bir görüntü yükseklikten sığar ve yatayda ortalanır (8k'da ölçek 0,965, kayma yaklaşık 141 piksel).
- **Dışa aktarımla aynı boyutta dosya ver**: birebir oturur (ölçek 1, kayma 0). Bütün son dosyalar böyle verildi.
- Kıta yerleşimi düzdür (sahibin isteği: "şekli Mercator şekline getirmene gerek yok, düz ver"): bir maske pikseli enlemde ve
  boylamda aynı derece; enlem satırdan, boylam orta boylamdan.
- "Place on existing" sekmesinin varsayılan kutusu dünyayı doldurmaz; saydamlığı nasıl okuduğu bilinmiyor. Tam harita için kullanma.
- "Colour map (assign colours)" sekmesi her pikseli en yakın renge bağlar, ara değer yok; gri yükseklik haritası bu sekmede bozulur.

### 4.3 Merak ile döngü (sahip elle işlerken)
1. Bizim dosya içe aktarılır. Sahip bölgeleri elle işler.
2. Sahipten 16 bit dışa aktarım alınır (ekran görüntüsü değil; ekran görüntüsü 1600 piksel, JPEG, kenarlı ve ölçüme uygun değil).
3. **Birleştirme:** sahibin elle işlediği her piksel, kıyı çizgisi ve deniz aynen kalır; dokunulmamış yerler ve sahibin işaretlediği
   bölgeler bizim yükseklikle doldurulur, sınırda 15 ile 30 piksel geçiş.
4. **Denetim, her çıktıda:** kıyı çizgisi farkı 0 piksel; deniz pikselleri değişmedi.
5. **Temizleme:** Merak dışa aktarımında kıyı önünde 1 ile 30 piksellik kara benekleri olur (16k'da 152 parça ölçüldü) ve deniz
   seviyesine çok yakın sığ deniz (−1 ile −40 m) Merak'ta benek benek kara çıkar. Küçük kara parçaları denize çevrilir, −40 m'den
   sığ deniz −40 m'ye indirilir.
6. **Deniz derinliğini sahip Merak'ta kendisi ayarlar.** Bizim eklediğimiz kıta sahanlığı (−12 ile −150 m) bazı yerlerde kara gibi
   çıktığı için geri alındı. Denize dokunma.
7. **Kıyı rampası yalnız karada:** Merak'ın kıyısında kara 2,5 ile 10 km içeride iç kesimden yüksekti (350 ile 430 m, iç 260 m);
   kıyıdan içeri alçalan rampa (kıyıda yaklaşık 20 m, 7 ile 31 km arası gürültülü genişlik) bunu düzeltti.
8. **Fark haritası:** sahibin sürümü ile bizimki parça parça karşılaştırılır (ortanca, %90, en yüksek, 200 m'den fazla sapan pay).
   İlk dünyada sahibin Mor Sıradağları bizimkinin yaklaşık yarısı genişlikte, 500 ile 600 m daha yüksek ve 50 ile 125 km güneydeydi.
9. **Üslup aktarımı:** sahibin dokunmadığı kara, onun üslubuna yaklaştırılır. İlk deneme (yükseklik eşleme + sırt keskinleştirme +
   gürültü) sahibe göre yetersizdi. İkincisi kabul edildi: taban bizim veriden yalnız karada süzülür (yaklaşık 15 km; dağlıkta daha
   az), ince doku sahibin elle işlediği bölgeden 128 piksellik yamalarla kopyalanır (Hann pencereli, yarı örtüşmeli yamalı doku
   sentezi), genliği sahibin dokusunun yüksekliğe göre ölçülen genliğine ayarlanır.
10. **Rehber:** elle işleme için Merak çerçevesinde saydam katman (eş yükseklik eğrileri 100 ile 3000 m, nokta yükseklikleri,
    adlar); Merak'a referans olarak Fill world ile konur. Elle işleme önerileri: tabanı Flatten ile sayıyla kur, sırtları dar fırçayla
    tutarlı yönde çiz, Smooth az, Erode çok, zirveleri aşınma payı için %5 ile %10 fazla kur, her bölgeden sonra kaydet.

### 4.4 Geography Lab (levhalar)
- Yön pusula açısıdır (0 kuzey, 90 doğu); Merak'taki bir okun 59°'de kuzeydoğuyu göstermesinden doğrulandı. Hız cm/yıl.
- Edilgen kıyılarda kıta ile önündeki okyanus aynı levhadır; okyanus sırtlarını kıyıdan uzağa koy. Sınır türünü ("Regime":
  Subduction, Continental collision, Transform, Divergent) "auto" bırakma.
- "Run 200 million years" araziyi yeniden hesaplar; elle işlenmiş haritada çalıştırma ya da önce kaydet. Ne kadar değiştirdiği bilinmiyor.

## 5. Teknik dersler ve tuzaklar

- **Kenar yumuşatma yok.** Maskeler saf siyah beyaz. Ölçeklerken en yakın komşu ya da "yumuşak büyüt, sonra eşikle".
- **JPEG yok.** Ovalarda gri adımlarını oynatır. Ölçüm her zaman dışa aktarılan PNG'den.
- **Süzgeçte denizi hesaba katma:** kıyıyı aşağı çeker ve kıyıya paralel yapay bir sırt bırakır. Yalnız karada normalleştirilmiş
  süzgeç: `gauss(z·kara) / gauss(kara)`.
- **Ölçek değiştirirken etiketler:** 8k etiketini 16k'ya en yakın komşuyla taşıyınca kıyı pikselleri etiketsiz kalır; en yakın
  etiketle doldur.
- **Doldurulacak bölge listesinde parça unutmak** (ilk dünyada Uzun Yarımada unutuldu). Her listeyi parça görüntüsü üstünde gözle denetle.
- **Kaynak verideki dikişler** (karşılıklar arası çokgen kenarları) birleştirilmemiş sürümde görünür; ağırlık sınırlarını bük.
- **Bellek:** 16000 × 7719 float32 dizi 494 MB. Kıta kutusuna kırp ya da satır blokları halinde çalış.
- **Gönderim:** sohbet aracı 8000 pikselden geniş görüntüyü göndermez; zip'le. Büyük ikili dosyaları git'e koyma (zip ve 16k PNG
  `.gitignore`'da), betikler ve küçük sürümler depoda.
- **Kayıt (iki maskeyi eşleme):** ölçek ve kaymayı kara maskelerinin örtüşmesini (IoU) en büyükleyerek bul (Nelder-Mead).
  Aynı boyutlu Merak dosyalarında (1, 1, 0, 0) çıkmalı.
- **Batimetri formülü hatası (ilk dünya):** iç deniz katsayısı tabanı sığlaştırmak yerine derinleştirdi (−7,4 km). Formül yazarken
  işaretleri denetle; sonuçları ölç.
- **Görüntü üzerinde koordinat:** sahibin işaretlediği görüntü küçültülmüşse oranı hesapla; ne olduğunu bilmediğin görüntüden
  koordinat okuma.

## 6. Ortam

- Python 3: numpy, scipy, Pillow, matplotlib (isteğe bağlı fastscapelib, imageio). Chromium ve Playwright önceden kurulu olabilir
  (PDF ve ekran görüntüsü için).
- Ağ: `s3.amazonaws.com` (karolar). Bulut oturumunda ağ politikası engellerse ortam belgesine bak; TLS doğrulamasını kapatma.
- Üslup ve doğrulama sırasında ara diziler geçici klasöre yazıldı; kalıcı olması gerekenler depoya ya da yeniden üretilebilir
  betiklere konmalı.

## 7. Mevcut kod

- `maskeden-merak/`: haritadan bağımsız araç takımı (`python3 -m mk PROJE KOMUT`). Komutlar: `maske`, `parcalar`, `onizle`,
  `karsilik`, `ozellik`, `ciz`, `olcum`, `hepsi`, `merak`, `plato`, `birlestir`, `uslup`, `rehber`, `fark`. Ayrıntılı yol `YOL.md`,
  kaynak kataloğu `KATALOG.md`, tarih şablonu `TARIH_SABLONU.md`, örnek proje `projeler/ornek`, sınama `testler/test_merak.py`.
- `belgeler/ilk_dunya/`: ilk dünyadan belgeler: `YONTEM.md` (aşamalar), `MERAK.md` (Merak hattının bütün sayıları; içindeki
  betik adları eski depoya aittir), `KARARLAR.md` (sahibin kararları). İlk dünyanın kodu ve verisi (`tarih/`) eski depoda,
  `athinker24/Merakproject`'te duruyor; bu depoya taşınmadı.

## 8. Web sitesine taşırken akılda tutulacaklar

Ağır bir simülasyon yok; işlerin hepsi görüntü ve dizi işlemi. Tarayıcıda yapılabilecekler ile sunucu ya da önceden hesaplama
gerektirenler ayrılmalı:
- Tarayıcıda rahat: maske yükleme ve temizleme, parça çizgisi çizme ve tohum koyma, önizleme ve gölgeli kabartma, Merak kodlaması
  (gidiş dönüş formülleri), kıyı ve deniz denetimleri, rehber katmanı, fark haritası.
- Dikkat isteyen: 16k çıktılar (123 milyon piksel; tarayıcı belleği ve PNG kodlama süresi), ince levha eğrisi (nokta sayısı az olduğu
  için hızlı), uzaklık dönüşümleri ve Gauss süzgeçleri (WebGL ya da Web Worker).
- Dış veri: AWS Terrain Tiles doğrudan tarayıcıdan çekilebilir (açık veri, CORS durumunu doğrula); önbellek gerekir.
- Sahibin akışı korunmalı: işaretle, yorum yaz, sayıyla geri dönüş al; her adım adlı, geri alınabilir ve tarihte bir olaya bağlı.
