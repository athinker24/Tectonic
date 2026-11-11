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

## Açık

- Telefondan tetikleme
- Çözünürlükler ve animasyon boyutu
- Blok ayrıştırmanın otomatiklik düzeyi
