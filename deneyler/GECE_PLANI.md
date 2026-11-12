# Gece planı: gerçek çarpışma simülasyonu (12 ile 13 Kasım 2026 gecesi)

Sahibin isteği: kopyala yapıştır değil, etki tepki. Blok okyanusu geçip gelir, çarpar; dağ yükselir,
arkasında plato büyür, önünde çökme havzası (ova) oluşur; nehirler ve aşınma bunlara tepki verir.

## Yaklaşım (`deneyler/carpisma_lab.py`, `tektonik/lab.py`)

İleri zamanlı, kıyısı serbest bir harita görünümü simülasyonu (sahibin maskesinden bağımsız ilk sürüm):
1. Kabuk kalınlığı alanı S (kıta 35 km, okyanus 7 km), düzenli kartezyen ızgara (10 ile 20 km).
2. Hız: ince viskoz levha çözücüsü (tektonik/levha.py); gelen bloğun çekirdeği hızla sürülür,
   sabit bloğun çekirdeği durur. Okyanus zayıf ve dalabilir: okyanusta yakınsama kabuğu yok eder
   (dalma), kalınlaştırmaz.
3. Taşıma: S hız alanıyla yarı Lagrange taşınır; kıyılar S'den çıkar (S > 20 km kara/sığ).
4. Alt kabuk akışı: kalın ve sıcak kabukta (S > ~55 km) doğrusal olmayan yayılma κ(S); bu düz tepeli,
   dik kenarlı platoyu kendiliğinden doğurur (Clark ve Royden 2000, 2. belge).
5. Bükülmeli izostazi: elastik levha (Te 30 ile 50 km) FFT ile; yükün önünde çökme havzası ve
   ötesinde kabarma kendiliğinden çıkar.
6. Aşınma: fastscapelib akarsu aşınması; çökelme: kapalı çukurlar aşınan malzemeyle dolar
   (havzalar düz ovaya döner).
7. Çıktı: zamanla animasyon (blok gelir, çarpar, dağ yükselir), kesit (ön havza, kuşak, plato).

## Durum
- [ ] Çekirdek simülasyon (kartezyen, iki blok)
- [ ] Bükülme + ön havza
- [ ] Alt kabuk akışı + plato
- [ ] Aşınma + çökelme
- [ ] Animasyon ve kesit
- [ ] Sahibin güneydoğu bloğu ile kuzeye uygulama

## İlerleme kaydı
- Koşu 1 (10 milyon yıl, 30 km): okyanus boşluğu çok dar kurulmuş.
- Koşu 2 (50 milyon yıl, 20 km): gelen kıta karşı kıtayı bütünüyle itti (sabit çekirdek 900 km uzaktaydı); bükülme dar kalınlaşmayı 21 km yükseltti (elastik destek kısa dalga boyunda fiziksel değil).
- Düzeltmeler: sabit çekirdek 450 km; kısa dalga boyunda yerel izostazi, bükülme yalnız bölgesel farkı ekler; temas sonrası hız yarıya; sabit kenar değerleri.
- Koşu 3: temas hemen algılandı (kuzey kıtasının gürültü adacıkları gelen levhada); iç göller doldurulmuyordu.
- Düzeltmeler: en büyük parça, delik doldurma; açık okyanusa bağlı olmayan her çukur dolar; temas yalnız ana gövdeyle.
- Koşu 4: temas 31 Ma; 20 Ma 3,5 km asimetrik dağ; 10 Ma düz tepeli plato; 0 Ma yaklaşık 4,5 km, 300 km genişlikte plato; iki yanda bükülme havzası (denizle dolu).
- Düzeltme: kalan tortu kıta üstündeki sığ denize (kıyıya yakın önce) dolar; çöküntü havzaları ovaya dönmeli.
