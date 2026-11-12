# Prosedürel arazi üretimi: tektonik yükselme ve akarsu erozyonu (araştırma notları)

Durum: 2/5 kaynak tam/özet olarak okundu (Cordonnier 2016 [B], Schott 2023 [B]); Cortial 2019 yalnızca özet [B-öz]. Tzathas 2024 ve Génevaux/Guérin için arama devam ediyor.

Etiketler: [B] tam metin okundu, [B-öz] özet okundu, [Ö] yalnızca arama özeti.

## Kaynak durumu

| # | Makale | Etiket | Not |
|---|---|---|---|
| 1 | Cordonnier ve diğ. 2016, Eurographics (CGF 35(2)) | [B] | PDF curl ile indirildi, pdftotext ile okundu |
| 2 | Cortial ve diğ. 2019, Eurographics (CGF 38(2)) | [B-öz] | Tam PDF giriş (DSpace Login) gerektiriyor: ERİŞİLEMEDİ; yalnızca DL özeti okundu |
| 3 | Schott ve diğ. 2023, ACM TOG 42(5) | [B] | HAL preprint (hal-04049125) curl ile indirildi, 16 sayfa |
| 4 | Tzathas ve diğ. 2024 | bekliyor | |
| 5 | Génevaux ve diğ. 2013; Guérin ve diğ. 2022 (STAR) | bekliyor | |

## 1. Cordonnier ve diğ. 2016 [B]

Künye: Cordonnier, Braun, Cani, Benes, Galin, Peytavie, Guérin. "Large Scale Terrain Generation from Tectonic Uplift and Fluvial Erosion". Computer Graphics Forum 35(2), Eurographics 2016. DOI 10.1111/cgf.12820.

- **Girdi:** Gri tonlamalı yükselme haritası U. Kullanıcı bu haritayla simülasyon alanını ve dağların büyüme hızını belirler. Harita, Ω üzerinde parçalı sabit (piecewise uniform) dağılım olarak alınır.
- **Model denklemi (1):** dh/dt = u(p) − k·A(p)^m·s(p)^n. h yükseklik, u yükselme, k erozyon katsayısı, A drenaj alanı, s yerel eğim (s = ∇h).
- **Parametreler:** n = 1 ve m = 0,5 ("as in most geomorphological studies"). m/n ≈ 0,5 jeolojik kısıt olarak verilmiş.
- **Deneysel değerler (Bölüm 6):** Arazi boyutu 50 × 50 km². Maksimum yükselme U = 5,0·10⁻⁴ m/yıl (dünya dağlarının ortalaması). Erozyon oranı k = 5,61·10⁻⁷ 1/yıl, dağların yaklaşık 2000 m'de zirve yapması için seçilmiş. Zaman adımı δt = 2,5·10⁵ yıl.
- **Yükseklik ilişkisi (Bölüm 6.4):** Deneylerle doğrusal bulunan kural hmax = 2,244·u/k (km cinsinden). Tepe yüksekliği tek bir oran (u/k) ile belirleniyor.
- **Çözünürlük:** Vektör temsil: Poisson örneklemeyle üretilen rastgele noktalar ve Delaunay üçgenlemesi üzerinde drenaj grafiği. Örnek sayısı 10.000 ile 160.000 arasında. Son yükseklik haritası Gauss çekirdekleriyle üretiliyor.
- **Süre (Tablo 1, Intel i7 3 GHz, 16 GB RAM, C++/OpenGL):**
  - 10.000 örnek: adım 0,031 s, yakınsama 6,4 s
  - 40.000 örnek: adım 0,177 s, yakınsama 35,4 s
  - 90.000 örnek: adım 0,401 s, yakınsama 78,0 s
  - 160.000 örnek: adım 1,273 s, yakınsama 252,0 s
  - Yakınsama yaklaşık 100-300 adımda.
- **Çözücü:** Örtük (implicit) şema, büyük zaman adımları. Drenaj ağı bağlantısı değiştikçe yineleme gerekiyor. Eğim üst sınırı 30° olarak uygulanıyor.
- **Sınırlamalar (makalenin kendi belirtimi):** Doğrulama yalnızca görsel gözleme dayanıyor; insan denek testi yok. Parametrelerin jeolojik anlamı tam bilinmiyor. Tortul birikimi ihmal ediliyor. Yalnızca akarsu erozyonu modelleniyor (buzul, yamaç, alüvyal erozyon yok). Uplift haritasının tektonik simülasyonla otomatik üretimi gelecek iş. Uygulama optimize edilmemiş.
- **Kod/veri:** Makalede kod veya veri erişim beyanı bulunmadı. Bir video referansı var. Açık kod olup olmadığı **BULUNAMADI**.
- **Gerçek veri:** Gerçek arazi veri setleriyle karşılaştırma yapılmış (Bölüm 6.1, "Real dataset").

## 2. Cortial ve diğ. 2019 [B-öz]

Künye: Cortial, Peytavie, Galin, Guérin. "Procedural Tectonic Planets". CGF 38(2), 2019. DOI 10.1111/cgf.13614.

- **Özet (DL sayfasından):** Fiziksel tabanlı simülasyon yerine, levha hareketi ve çarpışmasının büyük ölçekli gezegen özelliklerini yeniden üreten prosedürel yöntem. Dalma (subduction) ve çarpışma yaklaşıklaştırılarak litosfer (kıta ve okyanus kabuğu) deforme ediliyor. Kullanıcı levha hareketini kontrol ediyor; kıtalar, okyanus sırtları, büyük dağ kuşakları, ada yayları üretiliyor. Büyük ölçekli gezegen modeli prosedürel veya gerçek yükseklik verisiyle detaylandırılıyor. Levha yarılması (rifting) gibi olaylar etkileşimli tetiklenebiliyor.
- **Girdi:** Levha hareket parametreleri ve etkileşimli yönlendirme (uplift haritası değil, levha tabanlı).
- **Denklem, parametre değerleri, çözünürlük, süre, sınırlama, kod:** Tam PDF giriş gerektiriyor (DSpace Login): **ERİŞİLEMEDİ**. Bu alanlar doğrulanamadı.
- Açık PDF/kaynak kodu: bulunamadı (HAL preprint araması sonuç vermedi).

## 3. Schott ve diğ. 2023 [B]

Künye: Schott, Paris, Fournier, Guérin, Galin. "Large-scale Terrain Authoring through Interactive Erosion Simulation". ACM Trans. Graph. 42(5), makale 162, SIGGRAPH 2023. DOI 10.1145/3592787.

- **Girdi:** Yükselme alanı u = u₀ + ũ. u₀ statik kısım: "Uplift Tree" adı verilen, fırçalar (iskelet ilkel şekiller ve operatörler) ile kurulan hiyerarşik vektör yapısı. ũ dinamik düzeltme: yükseklik kısıtlarını (tepe, sırt, vadi noktası ve eğrileri) sağlamak için PI benzeri bir denetleyici (Kp = 0,01, Kd = 0,01, Ki = 0,001; her 10 yinelemede bir güncelleme).
- **Model denklemi (1):** ∂h/∂t = u − s^n·a^m + Δh. Burada a drenaj alanı, Δh yamaç difüzyonu (Laplasyen). K katsayısı açıkça yazılmamış (K = 1 gibi davranıyor). Yalnızca m/n oranı önemli, ≈ 1/2 seçilmiş.
- **Drenaj alanı yaklaşımı:** Hücre sıralamasına dayanmayan, paralelleştirilebilir artımlı yaklaşım. Hücreler arası akış yönlendirmesi (p = ∞ ile en dik eğim dağılımı) ve 5×5 hücrelik yerel pencere kullanılıyor. Her yinelemede bir kez güncelleniyor.
- **Çözünürlük:** Düzenli ızgara, açık (explicit) entegrasyon. Hücre boyutu 80 ile 600 m arasında. Test araziler 100 × 100 km² ile 1000 × 1000 km² arasında. Yüksek çözünürlük için sparse amplification (×8) ile ayrıntılandırılıyor.
- **Süre (Tablo 1, Intel i7 4 GHz, 16 GB RAM, GTX 1080 Ti, GLSL compute shader):**
  - 256²: 5k adım, adım 0,1 ms, toplam 0,5 s
  - 512²: 5k adım, 0,3 ms, 1,3 s
  - 1024²: 11k adım, 0,8 ms, 9,1 s
  - 2048²: 39k adım, 3,3 ms, 128 s
  - 4096²: 81k adım, 12,5 ms, 1036 s
  - Yazarlara göre Cordonnier 2016 ile karşılaştırma: 160k nokta (≈400×400 ızgara) için onlar 252 s, bu yöntem 512×512 için 1,3 s. Not: donanımlar farklı (CPU 3 GHz/GPU yok vs. 4 GHz + GTX 1080 Ti), doğrudan karşılaştırma tam adil değil.
- **Zaman adımı uyarlaması:** Pit-hücre sayısına göre Δt, azalırsa %1 artırılıyor, belirgin artışta 0,75 ile çarpılıyor.
- **Sınırlamalar (makalenin belirtimi):** Birden fazla yakın tepe kısıtı uyumsuz yükseklikle üst üste binerse kararsızlık. Kısıt güncellemesi CPU'da hesaplanıyor, yavaşlatıyor (GPU'ya taşımak gelecek iş). Çözünürlük 1024²'nin üstünde yakınsama yavaşlıyor. Sediment birikimi modelde yok: Bölüm 6.1'de ters prosedürel modellemede vadilerde çeşitlilik eksikliği gösteriliyor. Ayrıca yazarlar, Cordonnier 2018'in (tektonik katlanma yaklaşımı) yönlendirilemez olduğunu, bu yüzden yazar aracı olmadığını belirtiyor.
- **Kod/veri:** Erozyon simülasyon kodu açık: github.com/HSchott/StreamPowerErosion (makale metni ve yazar sayfası aynı bağlantıyı veriyor). Ancak bu oturumda GitHub erişimi kapalı, kod içeriği **doğrulanamadı**. Proje sayfasında video ve PDF bağlantıları da var.
- **Erişim notu:** h-schott.github.io ve aparis69.github.io (curl ile) erişilebildi, yalnızca yazar sayfası HTML. Ana PDF'i hal.science üzerinden alındı.

## 4. Tzathas ve diğ. 2024 [bekliyor]

## 5. Génevaux ve diğ. 2013; Guérin ve diğ. 2022 [bekliyor]

## Ağ ve erişim notları

- www.cs.purdue.edu ve h-schott.github.io: WebFetch DNS hatası (getaddrinfo ENOTFOUND). curl ile indirme başarılı.
- diglib.eg.org bitstream 25c92629… MP4 video (makale değil). 493f9706… DSpace giriş sayfası: Cortial PDF'i erişilemedi.
- github.com/H-Schott/StreamPowerErosion: proxy yanıtı "GitHub access not enabled" (bu oturumda GitHub erişimi kapalı).
- Proxy durum sorgusu bir izin reddi aldı; denemedi ve geçici yolla aşmaya çalışmadı.
- PDF metni için `pdftotext` kullanıldı; `oku.py` yalnızca HTML için (trafilatura) çalışır.
- İndirilen dosyalar: /tmp/claude-0/-home-user-Tectonic/1cb340b3-df7d-519b-96f4-5170b8cfb37a/scratchpad/dl_cordonnier/ ve .../dl_schott/
