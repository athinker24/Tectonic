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
