# Kararlar

Sahibiyle adım adım verilen kararlar. Gerekçe ve kaynak brief: `tektonik-araci-brief.md` (sohbetle verildi).

## 1. Haritanın okunuşu (11 Kasım 2026)

- Üç kara parçası: kuzey kara (iki loblu, 1 ve 2 doğu lobunda), güneydoğu kara (kuzey karaya doğudan bağlı yarımada, 1'in nedeni), güneybatı kara (ayrı kıta, 3 onun doğu kolu). Ortada iç deniz ve 4.
- Kara bağlantısı batı geçidinde. Atlas maskesinde zaten 1 ile 2 piksellik bir kara boynu olarak var. Güney geçidi her zaman açık; iç deniz okyanusa yalnızca güneyden bağlanıyor.
- Batı lobundaki halka plato ile güneybatı karadaki geniş düzlük korunmayacak; yeniden üretilecek.

## 2. Ölçek ve projeksiyon (11 Kasım 2026)

- Atlasla aynı gezegen ve konum: yarıçap 6371 km, kıta 60°K ile 7°G, 44°B ile 43°D arası (`dunyam-atlas-mobil/dunya/dunyam.json`). Kuzey-güney yaklaşık 7450 km, doğu-batı yaklaşık 6300 km (50°K) ile 9600 km (10°K).
- Kıta atlasla aynı kıta; maskeler görsel olarak eşleşti.
- Küre geometrisi zorunlu: kıta 67 enlem derecesine yayılıyor.
- Merak çıktısının küreye kaydı atlastaki dönüşümle yapılabilir (kare tuval, ölçek 0.754, kayma 1511.9 / 162.7), maske aynı dışa aktarımdan gelirse.

## 3. Bölge isteklerinin yorumu (11 Kasım 2026)

- Dört bölge isteğindeki gerçek dünya benzetmeleri (Himalaya, Tibet, İtalya, Alp ve Apenin) örnektir, şart değildir.
- 1 numaralı sıranın uzunluğu: güneydoğu bloğun çarpışma cephesi ne kadar uzun çıkarıyorsa o kadar. Kuşağı batıya doğru uzatmak için ek bir olay ya da dalma kuşağı uydurulmayacak.
- Plato çanağı (2) için iklim notu: atlasın iklimi çanak içi 800 ile 1000 m alınarak ayarlandı; bu aralığa yakın kalmak atlası bozmaz.

## 4. Ağır hesabın yeri (11 Kasım 2026)

- Tektonik yükseltme ve hidrolik erozyon GitHub Actions'ta Python ile koşar (atlas düzeni). Erozyon için Fastscapelib 0.3.0 adayı.
- Telefonda yalnızca anında kaba önizleme (erozyonsuz yükseltme alanı) hesaplanır.
- Cloudflare Containers ve tarayıcıda WebGPU elendi: kalite farkı yok ya da düşük, ek maliyet ve iş var.

## 5. Telefondan tetikleme (11 Kasım 2026)

- Uygulamadaki "Gönder" senaryoyu bir Cloudflare Worker'a yollar; Worker GitHub'a yazar ve Actions koşusunu başlatır. Koşu durumu da aynı Worker üzerinden okunur.
- GitHub anahtarı yalnızca Cloudflare'da gizli değer olarak durur; telefonda ya da repoda durmaz. Yalnızca bu repoya yetkili, kısıtlı bir anahtar olur.
- Site ve Worker Cloudflare Access arkasında, yalnızca sahibin e-postasıyla açılır.
- Sahibi Cloudflare ve GitHub tarafındaki kurulumu kendisi yapacak: adım adım, ekran ekran bir kurulum rehberi (`KURULUM.md`) yazılacak ve kurulum sırasında birlikte gidilecek.

## 6. Bölge ve altyapı kararları (12 Kasım 2026)

- **Bölge 2 (bozkır çanağı):** Zagros ve İran benzeri. Çarpışmanın hemen arkasında, Tibet gibi aşırı kalınlaşmamış, orta yükseklikte bir plato. Tibet benzeri 4 ile 5 km'lik plato seçilmedi.
- **Çanak yüksekliği:** 1000 ile 1500 m. Atlas iklimi çanak içini 800 ile 1000 m alıyor; bu yüzden araç çıktısı atlasa girince atlasın nem ayarları yeniden denenmeli, sıra kuralı gereği önce yükseklik eğrisi, sonra nem ayarları.
- **Bölge 3 (yarımada çarpışması):** Araç hem Apenin tarzını (dalan levha geri çekiliyor, arkada açılan havza) hem Alp tarzını (doğrudan kıta çarpışması) tutarlı tarih seçenekleri olarak üretecek; seçim haritalara bakılarak yapılacak.
- **Depo:** herkese açık olacak (Actions'ta 4 işlemci, 16 GB, ücretsiz ve sınırsız dakika). Kod, çıktılar ve araştırma belgeleri herkese görünür olur. Görünürlüğü sahibi GitHub ayarlarından kendisi değiştirecek.

**Not (doğrulanmadı):** Zagros bloğu için ölçtüğüm ortalama yükseklik (10 km hücrede yaklaşık 1900 m) kıvrım kuşağının kendisine ait. Seçilen 1000 ile 1500 m'lik çanak, bu kuşağın arkasındaki iç havzalara karşılık gelir; İran platosu iç havzalarının gerçek yüksekliği bu turda kaynakla doğrulanmadı.

## 7. Kıtanın sınırları ölçüldü (12 Kasım 2026)

Atlasın yükseklik haritasından (`dunya/dunyam_heightmap.png`, 4096 × 2048, deniz seviyesi değeri 11934) ölçüldü: ana kıta 7,08°G ile 59,99°K, 44,43°B ile 43,11°D arasında. Bu, 2. bölümdeki 44°B ile 43°D değerini doğruluyor; atlasın `tektonik/OZET.md` dosyasındaki "47°B" ifadesi yanlış (atlas deposuna dokunulmadı). Ana kıtanın dışında 18 kara parçası var; en büyüğü yaklaşık 9100 piksel (kabaca 790 000 km²), 18°B ile 4°B, 20,5°K ile 30,5°K arasında.

## Açık

- Çözünürlükler ve animasyon boyutu
- Blok ayrıştırmanın otomatiklik düzeyi
