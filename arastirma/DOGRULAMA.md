# Doğrulama kaydı

Tarih: 12 Kasım 2026. Bu belge, 24 araştırma belgesine uygulanan doğrulama turunun ne yaptığını, neyi bulduğunu ve neyi kapsamadığını kaydeder. Ham sonuç dosyaları `notlar/dogrulama/` içinde (`girdi_1..5.md`, `sonuc_1..5.md`); mekanik denetimlerin betikleri ve çıktıları aynı klasörde ve `notlar/20/` ile `notlar/13/`, `notlar/14/` altındaki ölçüm betikleriyle birlikte duruyor.

## Kapsam: "hepsi" değil

Belgelerde yaklaşık 1400 kanıt etiketi var. Bunların yaklaşık 480'i zayıf düzeyde ([Ö] arama özeti, [E] ansiklopedi, [T] tek makale iddiası, [B-öz] yalnızca özet). Hepsini yeniden kaynağa gidip okumak bu kotayla ve Haiku ajanlarıyla mümkün değildi ve ajanların hata riskini artırırdı. Bu yüzden doğrulama katmanlı yapıldı:

| Katman | Ne yapıldı | Kapsam |
|---|---|---|
| 1. Atıf denetimi (mekanik) | Belgelerdeki her DOI Crossref ve DataCite'a soruldu; DOI'siz atıflar (yazar, yıl, dergi, cilt, sayfa) Crossref'te aranıp karşılaştırıldı | 44 DOI, 39 DOI'siz atıf, 10 el ile başlık sorgusu |
| 2. Hesap denetimi | Belgelerde [H] ve [Ö-ölç] etiketli türetilmiş sayılar koddan yeniden üretildi | HEALPix pikselleri, bant alanı, Airy kök oranları, süre bütçeleri, 14. ve 20. belge oranları |
| 3. Örnekleme | "Tam metin okundu" ([B]) ve ansiklopedi ([E]) iddialarından örnek kaynak sayfaları ben çektim | 6 makale iddiası, 18 ansiklopedi sayısı, 4 paket meta verisi |
| 4. Hedefli iddia doğrulaması | "Aracın varsayılan değerleri" tablolarındaki zayıf etiketli 63 satır ve 1. belgedeki 13 etiketsiz iddia, bağımsız doğrulama isteyen 5 ajana bölünüp kaynaklarına gönderildi; her ajan kararını ben okuyup denetledim | 76 iddia |
| 5. Belgeler arası tutarlılık | Aynı büyüklüğün farklı belgelerde farklı geçip geçmediği arandı | 10 anahtar büyüklük |

Kapsanmayan: belgelerin ana bölümlerindeki ve tablolarındaki zayıf etiketli yaklaşık 400 iddia (varsayılan tablolar dışında), [B]/[D] etiketli yaklaşık 700 iddianın büyük çoğunluğu ve 2 ile 4. belgelerin ham not dosyalarına dayanan sayılar. Bu iddialar yeniden okunmadı.

## Sonuçlar

**Atıflar.** 44 DOI'nin hepsi çözüldü ve yazar, yıl, dergi ve başlıkla uyuştu. Uydurma ya da yanlış yazılmış bir DOI bulunmadı. DOI'siz atıfların hiçbiri uydurma çıkmadı. Bulunan atıf hatası tek bir yerde: 9. belgede Tonga ve Lau hız sayıları Schellart (2008) GSA Bulletin satırına bağlanmıştı; makale yalnızca korelasyon veriyor (hız sayıları Schellart ve diğerleri 2007 Nature'ın özetinden). Düzeltildi.

**Hesaplar.** Doğru çıkanlar: HEALPix piksel boyları (Nside 256: 25,5 km; 512: 12,7; 1024: 6,4), 7°G ile 60°K bandının alanı (60,89 milyon km²), Airy kök oranları (5 km topografya için 28 km kök, 33 km toplam, yüzey kazancı 0,152), süre bütçeleri (1 milyon düğüm × 5000 adım ≈ 57 dakika; 4,2 milyon düğüm ≈ 4,3 saat). Yanlış çıkanlar ve düzeltmeler: 14. belgede "yarılanışta 2,2 ile 2,4 kat" ve "20 km'den 5 km'ye 5,4 ile 5,9 kat" ifadeleri yalnızca iki ayarda doğruydu, doğrusu 1,8 ile 2,4 kat ve 3,6 ile 5,5 kat; 20. belgede rölyef oranı 1,8 ile 2,1 değil 1,8 ile 2,3, eğim düşüşü 2 ile 3 değil 2,2 ile 3,7 kat; 13. ve 21. belgede 0,72 ve 2,9 milyon hücre sayıları yalnızca derece adımı sabit ağ için, eşit alanlı ağda 0,61 ve 2,44 milyon. Hepsi düzeltildi.

**Örnekleme.** Tam metin okundu etiketli 6 iddianın 6'sı kaynakta aynen çıktı (Hack L = 1,4 A^0,6; Ruetenik n ≈ 1,3 ve 2,3, D/K ≈ 1,79e6; Messager 1,42 milyon göl; Kargère yazarları; Fastscapelib 0.3.0, GPL-3.0, 25 Haziran 2025; Map-Elites "illumination algorithm"). Stern (2002) hem 124 ± 38 km hem 166 ± 60 km değerlerini birebir veriyor. Ansiklopedi etiketli 18 sayının 18'i sayfada çıktı (Great Basin'in 541 730 km²'si 209 162 mi²'nin dönüşümü). Landlab lisansı MIT (LICENSE.md ve PyPI).

**Hedefli iddia doğrulaması (76 iddia).** Ajanların kararları: DOĞRULANDI 26, KISMEN 29, ÇELİŞKİLİ 1, DOĞRULANAMADI 17, HESAP (yöntem denetimi) 3. Ajan kararlarını doğrudan işlemedim; ilk ikisinde yanlış yorum yakaladım (bir satırın birden çok fayı kapsadığını görmemiş; bir değeri yanlış sayfada aramış; kaynak göstermeden DOĞRULANDI demiş) ve yalnızca kendi kontrolümden geçenleri belgelere işledim. DOĞRULANDI kararlarının yaklaşık yarısı yalnızca arama özetine dayanıyordu; bunlar belgelerde zayıf düzeyde kaldı.

## Belgelere işlenen düzeltmeler

| Belge | Düzeltme |
|---|---|
| 01 | Etiketsiz belgenin başına doğrulama durumu bölümü eklendi; Cordonnier 2018, FastFlow, Cordonnier 2016, otomatik ölçütler ve paketler için KISMEN/DOĞRULANAMADI ayrımı |
| 02 | Montgomery ve Brandon aşınma aralığının yeniden doğrulanamadığı notu |
| 05 | Hotspot hızı: 5,7 cm/yıl yalnızca 57 ile 25 milyon yıl önce için; son ~15 milyon yılda Hawaii çok daha hızlı. Yanal fay hız aralığının kaynağı (Kuzey Anadolu Neojen 6,5 ile San Andreas tarihsel 35). LIP ana evre tanım farkı |
| 06 | Sahanlık kırılma derinliği 133 ile 140 m; Parsons-Sclater geçerlilik sınırı (70/80/90 Ma) ve asimptot; hendek tipik derinliği için "6 ile 8 km" ifadesi tek kaynakta yok |
| 07 | Çarpışma adası yükselme hızı üst sınırı 14 mm/yıl'ın üstü; mikro kıta "ömrü" yerine "oluşum süresi" |
| 09 | Schellart 2008 atfı ayrıldı; hendek geri çekilmesi 6 ile 16 cm/yıl (slab kenarında); Hindistan yavaşlaması üçte bir ve %40'tan fazla; "130 milyon yıl" hız değişimi olarak kaldırıldı; Arabistan %30 birincil kaynakta bulunamadı |
| 11 | Deniz seviyesi belirsizliği: çalışmalar arası yayılım +40 ile +270 m, tek çalışma ±50 m |
| 13 | Landlab lisansı doğrulandı; hücre sayısı notu |
| 14 | Çözünürlük oranları yeniden hesaplandı; Schott 2024 "bulunamadı" notu düzeltildi |
| 17 | Spektral eğim: β ≈ 2 yalnızca 1B, 2B yüzeyde β = 2H + 2; hogback/cuesta ayrımı kaynakta ikili değil; GPU gereksinimi standart çalıştırıcı için doğru, ücretli GPU'lu çalıştırıcılar var |
| 18 | Buzul üssü: 0,69 yalnızca Meserve buzulu dahilken, hariçken 0,65; zirve yüksekliği "1 km" Brozović ikincil alıntısı |
| 19 | Smith ve Barstad zaman sabiti aralığı 200 ile 5000 s |
| 20 | Rölyef ve eğim oranları; θ için Whipple ve Tucker 0,35 ile 0,6 |
| 21 | Hücre sayısı eşit alanlı ağda |

## Hâlâ doğrulanmamış olan önemli iddialar

- **Hesaba doğrudan giren ama yalnızca arama özetine dayanan sayılar:** Parsons-Sclater katsayıları (2500, 350, 6400 m, 62,8); Stock ve Montgomery K aralıkları (1e-7 ile 1e-2); GDH1 katsayıları (hiç bulunamadı); Smith ve Barstad transfer fonksiyonunun C_w ve m ifadesi (konferans özetinden, metin çıkarımında bozuk); Mark ve Aronson D ≈ 2,2 (bulunamadı); Burbank 30 ile 40° eşik eğim (özette yok).
- **Birincil kaynağı okunamadı:** Montgomery ve Brandon 2002 (0,2 ile 6 mm/yıl), Syvitski ve Milliman 2007, Zahirovic 2015, Cortial 2019, Tzathas 2024, Hergarten 2020 denklemleri 7 ile 11 (metnin okunan kısmında üs yok), Schott 2024 tam metni, Egholm 2009 yöntem bölümü.
- **Kaynağı bulunamayanlar:** Wilson döngüsü süresi, kıta bloğu tipik hızı, boyut dağılımı, U vadi ve sirk boyutları, abartma çarpanı, telefonda kare hızı ve çizim süresi, MerakMapMaker belgeleri.
- **Kaynaksız ama kullanılan çıkarımlar ([H]):** blok sayısı aralığı (5 ile 30), mesafe tanımı (çeşitlilik için), kıyıda yükselmenin sönümlenmesi, günlük koşu sayacı tasarımı, Web Push ile bildirim. Bunlar tasarım önerisi, olgu değil.
- **Bilinen çelişkiler çözülmedi:** kıtanın batı sınırı 44°B (karar günlüğü) ile 47°B (atlas özeti); Messiniyen tuz kalınlığı 1,2, 2 ya da 3 km; Panama kapanması 3 ile 15 milyon yıl önce; Kretase deniz seviyesi tepesi +40 ile +270 m.

## Yöntemin sınırları

- Doğrulama ajanlarının çoğu yine Haiku'ydu ve arama özetlerinden, ansiklopediden çıkan değerleri sık sık "doğrulandı" olarak işaretledi. Bu etiket tek başına güvenilir değil.
- Atlatma yapılmadı: bot koruması, TLS sertifika hatası ya da erişim reddi veren kaynaklar "erişilemedi" olarak bırakıldı.
- Kendi ölçümlerim (Fastscapelib hızı ve çözünürlük bağımlılığı, SRTM rölyef istatistikleri, PNG boyutları) bu ortamda tek koşuyla alındı; farklı donanımda ve gerçek verilerle tekrarlanmadı.
