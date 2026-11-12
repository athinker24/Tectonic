# B: Levha yakınsamasından yüzey yükselmesi: fiziksel yollar

Durum: TAMAMLANDI (taslak sınırları içinde). Tüm kaynaklar İngilizce; notlar Türkçe.

Etiketler: [B] tam metin okundu / [B-öz] kısmi metin ya da özet okundu / [Ö] arama özeti / [T] kaynaksız türetme (kontrol edilmeli) / ERİŞİLEMEDİ / BULUNAMADI

Özet: Sayısal yükselme hızı (mm/yıl) ve kuşak genişliği (km) değerleri bu taramada hiçbir tam metinden alınamadı. Denklemler ve boyutsuz sayılar (Argand, Ne, kritik eğim) için değerler bulundu. Sayısal kıyaslar için model çıktıları gereklidir.

## Kaynak listesi

| No | Kaynak | Erişim | Etiket |
|----|--------|--------|--------|
| K1 | England & McKenzie 1982, GJI 70(2):295-321 | libmast / scilit kaydı (özet) | [Ö] |
| K2 | England & McKenzie 1983 (düzeltme), GJRAS 73:523-532 | arama özeti | [Ö] |
| K3 | Houseman & England 1986, JGR 91(B3):3651-3664 (Bölüm 1) | arama özeti | [Ö] |
| K4 | England & Houseman 1986, JGR 91(B3):3664-3676 (Bölüm 2) | arama özeti | [Ö] |
| K5 | Davis, Suppe & Dahlen 1983, JGR 88(B2):1153-1172 | özet + atıf sayfaları; tam metin ERİŞİLEMEDİ (Scribd kısmi tarama) | [Ö] |
| K6 | Dahlen, Suppe & Davis 1984 (kohesyonlu Coulomb kama) | arama özeti | [Ö] |
| K7 | Dahlen 1990, Annual Rev. Earth Planet. Sci. 18:55-99 | sunucu TLS sertifika hatası: ERİŞİLEMEDİ (TLS); arama özeti | [Ö] |
| K8 | Willett 1999, "Orogeny and orography", JGR 104(B12):28957-28981, doi:10.1029/1999JB900248 | Caltech dergi kulübü PDF'i (kısmi, sayfa seçimi), https://www.tectonics.caltech.edu/meetings/journal_club/session4/Willett1999JGR.pdf | [B-öz] |
| K9 | Whipple & Meade 2004, JGR 109 (F01011), doi:10.1029/2003JF000019 | özet (arama) | [Ö] |
| K10 | Salles, Mallard & Zahirovic 2020, goSPL, JOSS 5(56):2804, https://joss.theoj.org/papers/10.21105/joss.02804.pdf | PDF tam okundu | [B] |
| K11 | Roe & Brandon, "Critical form and feedbacks in mountain-belt dynamics: the role of rheology as a tectonic governor" (el yazması, 27 Nisan 2009; yayın bilgisi doğrulanmadı), https://earthweb.ess.washington.edu/roe/GerardWeb/Publications_files/RoeBrandon_ViscWedge08.pdf | PDF tam okundu | [B] |
| K12 | Garthwaite 2011, Leeds doktora tezi (TVS ile Asya), https://etheses.whiterose.ac.uk/2611/ | PDF tam okundu | [B] |
| K13 | Glerum et al. 2018, Solid Earth 9:267, https://se.copernicus.org/articles/9/267/2018/ | arama özeti; sayfa çekildi, ayrıntılı okunmadı | [Ö] |
| K14 | Thieulot & Bangerth 2022, Solid Earth | arama özeti | [Ö] |
| K15 | MIT OCW 12.002 (2008), ders 26, isostasi, https://ocw.mit.edu/courses/12-002-physics-and-chemistry-of-the-terrestrial-planets-fall-2008/74fb28dc068682451773d2616e914ff2_MIT12_002f08_lec26.pdf | PDF tam okundu | [B] |

## Bulgular

### 1. İnce viskoz levha (TVS) modeli: England & McKenzie 1982; England & Houseman 1986

- **Denklem ve boyutsuz sayı [B, K12 bölüm 5.2]**: Model sürekli bir ince levhayı güç yasası reolojisiyle tanımlar.
  Yanal tek tip akış varsayılır; deformasyon iki parametreyle belirlenir: güç yasası üssü n ve Argand sayısı Ar.
  Argand sayısı, yerçekimsel potansiyel enerji (GPE) kuvvetlerinin sınır kuvvetlerine oranıdır.
  Tanım (K12 eşitlik 5.24, metin kopyasından yeniden yazıldı; üsler kontrol edilmeli):
  Ar = g·ρc·L·(1 − ρc/ρm) / (B·ε̇0^n), burada ρc kabuk, ρm manto yoğunluğu, L ölçek, B malzeme sabiti.
- **Artan Ar etkisi [B, K12]**: Ar arttıkça GPE farkları daha etkili olur; sınırda kalın kabuk plato oluşmaz,
  litosfer kalınlaşmaya karşı daha çok akar. Ar küçük ve erozyon yoksa çok kalın kabuk oluşabilir.
- **Yatay deformasyon ölçeği [B, K12, England ve diğerleri 1985'e atıfla]**: Deformasyon ölçeği n ile azalır;
  yakınsak rejimde bozunma uzunluğu yaklaşık √(1/n) × sınır dalga boyudur (kaynak: England ve diğerleri 1985).
- **Düzeltme [Ö, K2]**: 1983 düzeltmesi, yönetici denklemde basınç gradyanı teriminin eksik olduğunu;
  doğru sonuçların daha yayılmış deformasyon verdiğini; nicel farklar olsa da sonuçların değişmediğini belirtir.
  En büyük farklar düşük Ar'de görülür [Ö, K12 özeti].
- **Güç üssü n**: Kıtasal TVS çalışmalarında en uygun n değeri çoğunlukla ≈3 bulunmuştur; ≈10 de öne sürülmüştür [Ö, K12 atfı].
- **Tibet/Asya uyumu [B, K12 özet]**: Gözlenen hız alanını en iyi tahmin eden modeller n = 2–5, Ar = 1–4 kullanır;
  Tibet platosu ve Tien Shan, önlük bölgelerinden 3–8 kat zayıf bulunmuştur.
  Himalaya yayının düşey integre yatay itme kuvveti FL ≈ 7–15 × 10^12 N/m olarak verilir.
- **Gerinim hızları [B, K12]**: Litosferin tek bir güç yasasıyla temsil edilebildiği gerinim hızı aralığı 10^-13 – 10^-17 s^-1.
- **Houseman & England 1986 [Ö, K3/K4]**: Sonlu eleman yöntemi, dizilen sınır ile. Tibet'in gerinim hızı,
  Tien Shan ve Ningxia-Gansu'nun yaklaşık dörtte biri. Model, platonun önündeki doğu-batı gerilmesini üretmez.
- Yükselme hızı (mm/yıl) değeri: BULUNAMADI (özet düzeyinde).

### 2. Kısalma, kabuk kalınlığı ve yüzey yüksekliği (kütle korunumu, Airy izostazisi)

- **Airy dengesi [B, K15 MIT dersi]**: Yüksek topografya, ek kök kalınlığıyla dengelenir.
  Denge: d_v = d_t × ρc / (ρm − ρc) (d_t topografya yüksekliği, d_v kök derinliği ilave).
  Örnek (MIT): d_t = 5 km, ρc = 2800, ρm = 3300 kg/m³ → d_v ≈ 28 km; toplam kabuk farkı ≈ 33 km.
  Aynı derste deniz seviyesindeki sürekli kabuk için ayrı bir örnek vardır; toplam Tibet kabuğu ≈ 61 km.
- **Kısalma-kalınlık bağıntısı [T]**: Alansal (kütle) korunumu ile yatay kısalma S (oran) için kalınlık h1 = h0 / (1 − S).
  Bu, kaynaktan doğrulanmamış bir türetmedir; kaynak arama kaynağı bulunamadı.
  Yükselme için Airy bağıntısıyla birleştirilebilir, ancak sayısal sonuç burada uygulanmadı.
- **Sınırlar [Ö]**: Basit Airy bağıntısı tek başına yeterli değildir; yakınsak sınırlarda dinamik yatay gerilmeler
  de yüzey yüksekliğine katkı sağlar. Kabuk kalınlığı ile yüzey yüksekliği arasında global bir basit ilişki yoktur (USGS derlemesi, arama özeti).
- Kısalma yüzdesi ile yükseklik (km) için hazır bir kaynak tablo: BULUNAMADI.

### 3. Sayısal geodinamik kodlar ve yüzey yükselmesi girdisi

- **goSPL [B, K10]**: Küresel ölçekli ileri model; "deforming plate tectonics" ile sürülür.
  Düşey ve yatay yer değiştirme alanları zamanla değişebilen girdi olarak verilir.
  Akarsu aşındırması için akım gücü yasası, hillslope difüzyonu, ikili litoloji sedimantasyonu.
  Model, Badlands'ten yöntem alır; Badlands yerel-kıtasal, goSPL küresel ölçek için uygundur.
  Sayısal yükselme hızı verilmez.
- **Pecube ile bağlantı**: BULUNAMADI. **GPlates + goSPL doğrudan iş akışı**: BULUNAMADI.
  (Arama özetinde: GPlates → CitcomS ile dinamik topografya → Badlands bir çalışmada vardır [Ö]; goSPL ile değil.)
- **ASPECT [Ö, K13]**: Doğrusal olmayan viskoplastisite; dört 2B karşılaştırma (indentor, brick, sandbox, slab detachment)
  ve 3B termomekanik dalma modeli.
- **SOPALE, UnderWorld [Ö, K14]**: ASPECT ile aynı eleman ailesini (piecewise bilinear/trilinear) kullanır.
- **I2ELVIS / I3ELVIS [Ö]**: Gerya & Yuen 2D işaretleyici-hücre yöntemi (2007, PEPI 163) ve 3D halefi I3ELVIS.
  Not: Aranan "I2VIS" adına kaynak BULUNAMADI; kodun adı büyük olasılıkla I2ELVIS'tir.
- **Dört kodun doğrudan kıyası (subduksiyon benchmark'ı)**: BULUNAMADI.
- **Doğrudan hesap maliyeti (CPU-saat, bellek)**: BULUNAMADI.

### 4. Kinematik yükselme, kritik kama, aşınma bağlaşımı

- **Kararlı hal aşınma-yükselme dengesi [B, K11]**: Akarsu aşınması ė = K Q^m (dz/dx)^n, Q = P ka x^h.
  Kararlı hal denklemi: U = K ka^m P^m x^(hm) (dz/dx)^n (K11 denklem 6).
  Yükselme U düzgün alınıp kama ucundan bölenlere integre edilir; sonuç kama ölçeğine bağlı.
  Metin, kama açısının ve yükselmenin kama ölçeğine ve aşınma parametrelerine bağlı olduğunu gösterir.
  "Tectonic governor" kavramı: kritik topografik form, yükselme/aşınma değişikliklerini sönümler [B, K11].
- **Willett 1999 [B-öz, K8]**: Aşınma sayısı Ne = k·L/u (k: aşınma katsayısı ~ 1/zaman; L: yarı genişlik; u: yükselme hızı).
  Ne, aşınma ile tektonik yükselme oranıdır. Kararlı hal yüksekliği h* = −(1/Ne) ln(x*) (kısmi PDF'ten; eşitlik numaraları sayfa kopyasında bozuk).
  Kuşak; Ne büyüdükçe daha hızlı kararlı hale ulaşır. Yağış tabanlı asimetri (Southern Alps örneği) [Ö özet].
- **Whipple & Meade 2004 [Ö, K9]**: İki taraflı sürtünmeli kama, kararlı akı. Kararlı hal kuşak genişliği,
  tepe yüksekliği ve kabuk kalınlığı; kabuk akısının aşınma verimliliğine oranına (bir kuvvetine) bağlıdır.
  Sayısal değerler (mm/yıl, km): BULUNAMADI (yalnızca özet okundu).
- **Willett 1999 başlığı**: "Doubly vergent critical orogens" başlıklı bir Willett 1999 makalesi BULUNAMADI;
  bu sorgunun karşılığı büyük olasılıkla "Orogeny and orography" (K8)'dır.
- **"Plate-driven uplift in landscape evolution models" ve "kinematic thrust uplift"**: Doğrudan eşleşen kaynak BULUNAMADI.
  Arama özetindeki sayısal örnekler (başka çalışmalardan, eşleşen kaynaklar doğrulanmadı) [Ö, kullanılmadı]:
  Calabrian ön yay: >1 mm/yıl (30–25 Ma), <0,4 mm/yıl (15 Ma); Meksika ve Batı Kuzey Amerika: 0,15–0,2 mm/yıl (25–10 Ma);
  Peru kısalma: 0,25–0,6 mm/yıl (10 Ma'dan bugüne). Bunlar bu notta yalnızca bağlam içindir.

### 5. Kuşak genişliği ve yükseklik ölçeklemesi (Davis, Suppe & Dahlen 1983)

- **Kritik kama [Ö, K5]**: Kama kritik eğime ulaşana kadar iç deformasyonla şekillenir; sonra sabit eğimde kararlı kayarak büyür.
  Kritikten küçük eğimli kama itildiğinde kaymaz; yüzey eğimini artırır.
  Batı Tayvan'dan çıkarılan etkin iç sürtünme katsayısı μ = 1,03 (Byerlee ile tutarlı).
- **Kritik eğim tanımı [Ö, K7 Dahlen 1990]**: Kritik eğim = yüzey eğimi α + taban (dekolman) eğimi β.
  Kritik eğim, iç deformasyon ile taban boyunca kaymanın eşit kolaylıkta olduğu denge durumudur.
- **Kohesyonlu Coulomb kama [Ö, K6]**: Eğimin, kama mukavemeti ve taban sürtünmesi ile ilişkisi.
- **Kritik eğim açısı (derece) ve kuşak genişliği (km)**: BULUNAMADI (tam metin ERİŞİLEMEDİ; Dahlen 1990 TLS hatası nedeniyle).
- **Kritik kama, boyuttan bağımsız eğim [B, K11]**: Coulomb kama, kritik eğimin kama büyüklüğünden bağımsız olduğunu verir.

## Açık sorular ve eksikler

1. Sayısal yükselme hızı (mm/yıl) ve kuşak genişliği (km) için tam metin kaynak yok: England & McKenzie 1982,
   Houseman & England 1986, Davis 1983, Whipple & Meade 2004 tam metinleri ERİŞİLEMEDİ (ücretli / AGU).
2. Dahlen 1990 sunucusu TLS sertifika hatası veriyor (planetarygeoscience.uchicago.edu). TLS doğrulaması atlanmadı.
3. Argand sayısının tanımı K12'den doğrulandı, ancak eşitlik 5.24'ün üsleri metin kopyasından okundu; kontrol gerekli.
4. Kısalma-kalınlık-yükseklik bağıntısı [T] türetmedir; kaynak bulunmadı.
5. Dört kodun doğrudan karşılaştırması ve hesap maliyetleri BULUNAMADI.
6. Sonraki adımlar: Willett 1999 tam makale (AGU erişimi), Whipple & Meade 2004 tam metin, Glerum 2018 ayrıntılı okuma.
