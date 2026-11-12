# 22. Mobil arayüz

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun sentezidir (A PWA, depolama, çevrimdışı çalışma ve arka plan; B parmakla çizim, zaman çubuğu, yerleşim ve erişilebilirlik); sentezi ben yazdım. Ham notlar `arastirma/notlar/22/` içinde. Etiketler: **[B]** tam metin okundu, **[D]** resmi belge ya da uyumluluk verisi okundu, **[Ö]** arama özeti, doğrulanamadı, **[K]** kullanıcı raporu, **[H]** bizim çıkarımımız, **[Y]** bulunamadı.

Dürüst durum: iOS Safari'nin dokunma davranışı bu ortamda sınanamadı (cihaz testi gerekli). Apple'ın insan arayüzü yönergeleri (HIG) sayfaları yalnızca JavaScript kabuğu döndürdü, bu yüzden Apple'ın 44 pt kuralı ve Pencil metinleri okunamadı. Bu belge bu yüzden "okunan kaynak" ile "cihazda sınanması gereken" ayrımını açıkça tutuyor.

## Kısa sonuç

**1. Ana ekrana eklenmiş PWA kullanılabilir; depolama kotası sorun değil, bellek sorun.** Safari'de bir kaynağın (origin) kotası diskin en çok yüzde 60'ı (tarayıcı uygulaması), yüzde 15'i (diğer uygulamalar); ana ekran uygulaması tarayıcıyla aynı kotada [B, WebKit blog 14403]. 30 kare × 2 MB = 60 MB kota açısından sorun değil [H]. Asıl kısıt bellek: Apple sayısal bir sınır yayımlamıyor; uzun sayfada sekme çökmesi için bir kullanıcı raporu var (WebKit hatası 312727, [K]).

**2. Uzun Actions koşusunun bittiğini bildirmenin tek yolu Web Push.** Web Push ve rozet (Badging) iOS 16.4'ten beri, yalnızca ana ekrana eklenmiş uygulamada ve kullanıcı etkileşimiyle [B, WebKit blog 13878]. Arka plan senkronizasyonu ve periyodik arka plan senkronizasyonu Safari ve iOS'ta yok [D]. Bildirimi gönderecek bir sunucu gerekir; bu, 23. konudaki Cloudflare Worker ile örtüşür [H].

**3. Parmakla çizim için Pointer Events yeterli ama iki parmak yakınlaştırmayı uygulama kendisi yapmalı.** `touch-action: none` tarayıcı kaydırma ve yakınlaştırmayı kapatır; `pinch-zoom` ayrı bir değer olduğundan iki parmak yakınlaştırmayı kod kendisi yönetmeli (çıkarım). iOS Safari'de kesin kaynak yok, 2018-2019 raporları var [Ö].

**4. Zaman çubuğu için hedef küçük ama kaynaklı: 24 × 24 CSS px alt sınırı (WCAG 2.5.8), pratikte 44 pt (Apple) ve 48 dp (Material).** Apple ve Material değerleri arama özetinden [Ö]; WCAG 2.5.8 okundu [B].

## 1. PWA, depolama ve çevrimdışı (A kolu)

| Konu | Bulgu | Etiket |
|---|---|---|
| Ana ekran uygulaması | manifest ile Safari dışında açılır | [B] |
| Web Push, rozet | iOS 16.4 ve sonrası, yalnızca ana ekrana eklenmiş uygulama, kullanıcı etkileşimi şart | [B] (webkit.org/blog/13878) |
| Depolama kotası | origin kotası diskin en çok %60'ı (tarayıcı uygulaması) ve %15'i (diğer uygulamalar); toplam kota diskin %80'i ve %20'si | [B] (webkit.org/blog/14403) |
| 7 günlük silme | Akıllı İzleme Önleme (ITP) kuralı doğrulandı; ana ekran uygulamalarının kendi kullanım sayacı var | [B] (webkit.org/blog/10218) |
| Kalıcı depolama | `navigator.storage.persist()` Safari 15.2+, `estimate()` Safari 17+; karar WebKit sezgilerine bağlı, ana ekran uygulaması öne çıkıyor | [D, B] |
| Cache API, OPFS | Cache API Safari 11.1, OPFS Safari 15.2 | [D] |
| Çevrimdışı strateji | Workbox StaleWhileRevalidate her zaman yeniden doğrular; `ExpirationPlugin` ile `maxEntries` sınırlanır | [B] |
| Güncelleme | yeni service worker, eski kontrol eden istemciler kalmayınca etkinleşir; `skipWaiting()` kullanıcı onayından sonra çağrılmalı; `clients.claim()` dikkatle | [B] (web.dev) |
| Paylaşım, dosya | Web Share Safari 12.1 ve iOS destekli; File System Access seçicileri (`showOpenFilePicker` vb.) Safari ve iOS'ta yok | [D] |
| Arka plan | Background Sync ve Periodic Background Sync Safari ve iOS'ta yok | [D] |
| Bellek | Apple sayısal limit yayımlamıyor; WebKit hatası 312727 [K]: uzun sayfada iPhone'da sekme çöküp yeniden yükleniyor, aynı sayfa Android Chrome'da çalışıyor; tuval, WebGL ve bitmap tetikleyici olarak arama özetlerinde geçiyor | [K ve Ö] |

Düzeltme: promptumdaki "Safari kotası toplam origin kotasının yaklaşık yüzde 60'ı" ifadesi yanlıştı; doğrusu origin kotası diskin en çok yüzde 60'ı. web.dev'de geçen "Safari yaklaşık 1 GB" ifadesi kaynaksız, kullanılmamalı. Chrome'un depolama sayıları web.dev'den dolaylı [Ö], Chrome'un kendi belgesi çekilmedi.

**Bildirim tasarımı [H].** Koşu bitince Cloudflare Worker (ya da Actions'ın webhook'u) kullanıcıya Web Push gönderebilir; iOS'ta bunun çalışması için uygulamanın ana ekrana eklenmiş olması gerekir. Alternatif olarak uygulama açılınca durumu sorgulamak (yoklama) her cihazda çalışır, bildirim gecikmeli olur.

## 2. Dokunma, çizim ve zaman çubuğu (B kolu)

| Konu | Bulgu | Etiket |
|---|---|---|
| Giriş modeli | Pointer Events tek giriş modeli; `getCoalescedEvents` (çizim uygulamaları için birleştirilmemiş konumlar), `getPredictedEvents` (Baseline 2024, öngörü tarayıcıya bağlı) | [D] (MDN) |
| Kaydırma çakışması | `touch-action: none` tarayıcı kaydırmasını ve yakınlaştırmasını kapatır; iki parmak yakınlaştırma için kod gerekir | [D, çıkarım] |
| Apple Pencil | `pointerType` "pen", `pressure`, `tiltX`; Safari'de doğrulama yok | [Ö] |
| Avuç reddi | resmi mekanizma bulunamadı | [Y] |
| Tuval performansı | MDN "Optimizing canvas": çevrimdışı ön çizim, tam sayı koordinat, `alpha: false`, `requestAnimationFrame`; `OffscreenCanvas` ve `transferControlToOffscreen` ile worker'a taşıma; `devicePixelRatio` ile keskinlik ölçekleme | [D] |
| Zaman çubuğu | `input range step=1` ile kare seçimi; `aria-valuetext` ile okunur değer | [D] |
| Dokunma hedefi | WCAG 2.5.8 = 24 × 24 CSS px; Apple 44 × 44 pt; Material 48 × 48 dp | [B ve Ö] |
| Kare ön yükleme | `createImageBitmap` ile önceden çözülmüş kare penceresi, `close()` ile bellek yönetimi | [D] |
| Kare hızı hedefi | 30 ile 60 kare/s hedefi kaynaksız, tasarım hedefi | [H] |
| Güvenli alan, görünüm | `env(safe-area-inset-*)`, dinamik görünüm birimleri (`dvh`; `vh` = `lvh`) | [D] |
| Tek el | Hoober (2013): %49 tek el, %36 kucaklama, %15 iki el; sağ baş parmak %67 | [Ö] |
| Alt sayfa kalıbı | doğrulanmış kaynak bulunamadı | [Y] |
| Erişilebilirlik | WCAG 1.4.3 kontrast 4,5:1 (büyük metin 3:1); 1.4.11 sayfasının 3:1 metni tam doğrulanmadı; `prefers-reduced-motion`; çizim tuvali ekran okuyucuya kapalı, yazılı alternatif gerekir | [B ve D] |

## 3. Aracın tasarım varsayılanları

| Parametre | Öneri | Etiket |
|---|---|---|
| Uygulama biçimi | PWA, ana ekrana eklenmiş | [B] |
| Çevrimdışı | service worker, StaleWhileRevalidate, kare önbelleği `maxEntries` ile sınırlı | [B] |
| Güncelleme | yeni sürümde kullanıcı onayıyla `skipWaiting()` | [B] |
| Koşu bildirimi | Web Push (ana ekrana eklenmiş), yedek olarak açılışta yoklama | [B ve H] |
| Arka plan senkronizasyonu | kullanılmasın (iOS'ta yok) | [D] |
| Depolama | Cache API + IndexedDB / OPFS; kalıcılık için `persist()` isteği | [D] |
| Bellek | aynı anda yalnızca birkaç karenin `ImageBitmap`'i; `close()` ile bırakma | [D ve H] |
| Çizim girişi | Pointer Events, `touch-action: none` yalnızca çizim tuvalinde, yakınlaştırma uygulama kodunda | [D] |
| Zaman çubuğu | `input range`, `step=1`, 44 pt hedef, `aria-valuetext` ile tarih etiketi | [D ve Ö] |
| Yerleşim | `dvh`, `env(safe-area-inset-*)`, ana kontroller alt yarıda (tek el) | [D ve Ö] |
| Hareket | `prefers-reduced-motion` altında animasyon yerine adım adım | [D] |
| Karşılaştırma | iki harita için kaydırma ya da örtme, çok harita için seçilmiş alt küme (10. belge) | [H] |
| Cihaz testi | iOS Safari'de dokunma, Pencil, bellek davranışı için gerçek cihaz testi şart | [H] |

## 4. Kaynaklar arası çelişkiler

- Dokunma hedefi: WCAG 24 CSS px (alt sınır) ile Apple 44 pt ve Material 48 dp (öneri).
- Kota ifadeleri: web.dev'de "Safari yaklaşık 1 GB" ile WebKit'in yüzde 60 / yüzde 15 kuralı; WebKit blogu birincil.
- iOS Safari dokunma davranışı: 2018-2019 raporları ile güncel sürüm arasında fark olabilir; cihazda sınanmadı.

## 5. Bulunamayanlar ve doğrulanamayanlar

- Apple HIG (44 pt, Pencil metinleri) ve Apple Safari 15.1 özellik sayfası (boş döndü); Hoober 2013 birincil metni (uxmatters DNS'te çözülmedi); Chrome'un kendi depolama belgesi.
- Avuç reddi için resmi mekanizma; alt sayfa kalıbı için doğrulanmış kaynak; iOS Safari'de WebCodecs desteği; `ImageBitmap` bellek bütçesi.
- iOS Safari dokunma davranışı ve Pencil (cihaz testi gerekli); iOS sekme bellek sınırı (Apple yayımlamıyor).
- WCAG 1.4.11 3:1 ifadesi tam doğrulanmadı.
- developer.mozilla.org, www.w3.org, www.lukew.com WebFetch'te DNS hatası verdi; curl ile erişildi. Esri kılavuzu ve community.esri.com DNS hatası verdi.

## 6. Promptumdaki hatalar (düzeltildi)

- "Safari: toplam origin kotasının yaklaşık yüzde 60'ı" yanlış; origin kotası diskin en çok yüzde 60'ı.
- "Chrome: disk alanının yüzde 60'ı" doğrulanmadı (web.dev özetinden dolaylı).
- "Safari yaklaşık 1 GB" web.dev'de kaynaksız ifade.
- "iOS Safari WebGPU" bu konuda ele alınmadı; 21. belgede Baseline olmadığı belirtildi.

## Başlıca kaynaklar

- WebKit blog: https://webkit.org/blog/14403/ (depolama), https://webkit.org/blog/13878/ (Web Push), https://webkit.org/blog/10218/ (ITP)
- MDN: Pointer Events, `getCoalescedEvents`, Optimizing canvas, OffscreenCanvas, `createImageBitmap`, `touch-action`
- W3C WCAG 2.2: 2.5.8, 1.4.3, 1.4.11
- web.dev (service worker yaşam döngüsü), Workbox belgeleri
- Tam liste ve her bilginin kaynağı `arastirma/notlar/22/` içinde.
