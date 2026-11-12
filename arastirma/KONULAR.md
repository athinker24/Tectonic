# Araştırma konuları

Sahibiyle 11 Kasım 2026'da belirlendi; üç kez brief, kararlar ve atlas reposuyla karşılaştırılarak tamamlandı. Her konu bu klasörde numaralı ayrı bir belge olacak. Her belgede bulunanlar, kaynak bağlantıları (erişim tarihiyle) ve bu araca çıkan sonuç yer alır. Kaynaklar güncel olmalı; eğitim bilgisine dayanılmaz.

**Araştırma ölçütü (sahibi, 11 Kasım 2026):** Araştırmalar üstünkörü ve hızlı olmayacak. Tamamen ayrıntılı ve özenli olacak; olabildiğince çok ve geçerli kaynağa bakılacak. Birincil kaynaklar (resmi belgeler, makaleler, sürüm notları) ikincil özetlere tercih edilir. Doğrulanamayan bilgi doğrulanamadı diye yazılır.

**Durum (12 Kasım 2026):** 1. konu `01-mevcut-araclar.md`, 2. konu `02-carpisma-kusaklari.md`, 3. konu `03-izostazi-ve-bukulme.md`, 4. konu `04-daglarin-yaslanmasi.md`, 5. konu `05-diger-sinir-turleri.md`, 6. konu `06-kiyi-ic-denizler-deniz-tabani.md` olarak tamamlandı. Ham notlar `notlar/01/` ile `notlar/06/` altında. Sonraki: 7. konu.

Sıra bağımlılık sırasıdır: önce ne üretileceği, sonra geriye dönük kurgu, sonra arazi modeli, görsel ve altyapı.

## 0. Önceki çalışmalar

1. **Mevcut araçlar ve dünya kurgucuların yöntemleri.** GPlates ile kurgusal dünya modelleme (Worldbuilding Pasta, Artifexian, GPlates forumunun worldbuilding bölümü, Game of Thrones tektonik haritası), GeoChronicler, Gaea 2, World Machine, Wilbur, Merak'ın kendi tektonik aracı. Neyi yeniden kullanabiliriz, nerede yetersiz kalıyorlar.

## A. Jeoloji: ne üreteceğiz

2. **Çarpışma kuşaklarının anatomisi.** Kesit (önülke ovası, kıvrım ve bindirme kuşağı, ana sıra, plato), genişlik ve yükseklikler, çentik (indenter) köşeleri ve düğümler (Pamir, Assam), uzak etkiler ve eski kuşakların yeniden canlanması (Tien Shan, Altay), plato yüksekliklerini belirleyen etkenler (Tibet, Moğolistan, Tarım, İran); litosfer dayanımı, sert kratonlar ve zayıf zonlar (deformasyonun nerede yoğunlaştığını ve uzak etkileri belirler; 2 numaralı çanak için temel). Varsayılan değerlerin kaynağı.
3. **İzostazi ve bükülme.** Kabuk kalınlığından yüksekliğe, önülke havzasının bükülmeyle oluşumu, aşınmaya karşı izostatik yükselme.
4. **Dağların yaşlanması.** Kuşakların aşınma hızları, genç keskin ve yaşlı yuvarlak kuşakların sayısal karşılığı (Appalachian, Ural).
5. **Diğer sınır türlerinin yer şekilleri.** Volkanik yaylar, sıcak noktalar, yanal faylar (Kuzey Anadolu, San Andreas), gerilme alanları (Ege, Basin and Range), rift vadileri.
6. **Kıyı geometrisinden tarih okuma, iç denizler ve deniz tabanı.** Pasif ve aktif kenar sahanlıkları, başarısız riftler, yay ardı havzalar; iç denizlerin tabanı (Akdeniz, Karadeniz, Hazar); alçak kara köprüleri (Süveyş, Panama); sahanlık, yamaç, derin havza ve hendekten oluşan batimetrinin üretimi.
7. **Tamamen dağlık adalar ve mikro kıtalar.** Tayvan, Yeni Zelanda, Yeni Gine, Korsika ve Sardunya, Girit.

## B. Ters problem ve zaman

8. **Küre geometrisi, ızgaralar ve projeksiyonlar.** Blokların, erozyonun ve gösterimin ortak koordinat yapısı: eşdikdörtgen, HEALPix, küp küre, ikosahedral ızgaralar; akış yönlendirmenin bu ızgaralarda çalışması; telefonda gösterim projeksiyonu; alan ağırlıklı ölçüm (atlas tuzağı 7.1).

9. **Blok ayrıştırma ve geriye sürme.** Euler kutupları, kıyı oturtma, sütur hatları, çakışma denetimi; pyGPlates ve GPlately; levha hızları ve zaman ölçekleri; isteklerin tektonik maliyetinin ölçülmesi.
10. **Çoklu çözüm üretimi, seçim ve sade dil.** Birbirinden anlamlı biçimde farklı tutarlı tarihlerin üretilmesi; seçeneklerin harita olarak karşılaştırılması; jeolojinin hikaye ve harita diline çevrilmesi.
11. **Paleocoğrafya ve animasyon kareleri.** Geçmiş kıyılar ve deniz seviyesi, levha hareketlerinden geçmiş yükseklik haritası (Utrecht paleogeography calculator), sürekli kapalı levhalar (Gurnis 2012), dönmelerin ara değerlemesi.

## C. Arazi modeli

12. **Tektonik olaylardan yükseltme haritasına.** Cordonnier 2016, Cortial 2019, Schott 2023, Tzathas 2024; goSPL'in levha zorlamalı yaklaşımı.
13. **Erozyon motorunun seçimi.** Fastscapelib (HealpixGrid), goSPL, Landlab; kıyıyı sabit tutma ve kıyı kısıtının kıyıda yapay basamak üretmeden uygulanması; Actions'ta süre ve bellek; gerçek parametre aralıkları; lisanslar.
14. **Erozyonun çözünürlük bağımlılığı.** Akarsu güç yasasının ızgara boyuna bağlılığı (Hergarten 2020, Earth Surface Dynamics 2025); 20 km önizleme, ana hesap ve detay geçişinin tutarlı kalması.
15. **Çökelme, kapalı havzalar ve göller.** Önülke ovaları, deltalar, sahanlık dolgusu; denize akmayan havzalar (Tarım, Moğolistan); atlasın göl ve nehir katmanıyla uyum.
16. **Kurgusal istisnaların doğal karıştırılması.** Yükseltme tabanlı düzenleme (Schott 2023) ve çevreye yumuşak geçiş.
17. **Ayrıntı ekleme ve doğallık.** Çok ölçekli ayrıntı ekleme (Schott 2024), kayaç farklılıkları, gürültü.
18. **Buzul aşındırması (düşük öncelik).** U vadiler, sirkler, fiyortlar; atlasın buzul katmanıyla ilişkisi.
19. **Yağışla bağ.** Smith ve Barstad dağ yağışı modeli (orographic_precipitation paketi), LFPM; atlas rüzgarlarıyla bağlantı.
20. **Gerçekçiliğin ölçülmesi.** Alan ağırlıklı hipsometri, eğim dağılımı, akarsu ağı yoğunluğu, boyuna profiller, sırt sürekliliği; GEBCO ve Copernicus ile karşılaştırma; atlasın yükseklik çapalarıyla (kıta bilerek Dünya'dan yüksek) gerçekçilik ölçütünün çatışması.

## D. Görsel

21. **Gerçekçi rölyef gösterimi.** Çok yönlü gölgeleme, İsviçre kabartması, ortam gölgesi, yükseklik renklendirmesi; telefonda WebGL ile çizim.

## E. Altyapı

22. **Mobil arayüz.** PWA, WebGL ve WebGPU'nun telefonlardaki güncel durumu, parmakla çizimde yapışma, zaman çubuğunun akıcılığı, çevrimdışı depolama sınırları.
23. **Cloudflare Worker, Access ve GitHub.** Kısıtlı anahtar ya da GitHub App, koşu başlatma ve durum okuma, Actions makine sınırları, animasyon karelerinin depolanması. Sahibine yazılacak kurulum rehberinin temeli.
24. **Atlas ve Merak ile veri alışverişi.** Photoshop maskesinin küreye kaydı, projeksiyonlar, 16 bitlik yükseklik haritası biçimi (Merak'ın içe aktarım biçimi bilinmiyor), yeni arazinin atlas zincirine girişi (yükseklik eğrisi, iklim, su, buzul, toprak, bitki, yaşanabilirlik, tarım, hayvan) ve atlasın levha katmanının yeni blok modeliyle değişmesi.
