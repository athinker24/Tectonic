# Mimari

Tarih: 12 Kasım 2026. Bu belge aracın nasıl kurulacağını belirler. Dayanağı `arastirma/` altındaki 24 belge ve `KARARLAR.md`. Her seçimin yanında hangi belgeye dayandığı yazılı. Atlas ile veri alışverişi şimdilik kapsam dışı (sahibin kararı, 12 Kasım 2026).

## Dürüst başlangıç notu

Benzer sistemlerin hiçbiri bu işin tamamını yapmıyor (1. belge). Parçalar var:

- Levha hareketinden arazi: goSPL, Cortial 2019, Cordonnier 2018. Hepsi ileri yönde çalışır: önce levhalar, sonra arazi. Kıyı sonuç olarak çıkar, girdi olarak verilmez.
- Yükselme haritasından aşınmış arazi: Cordonnier 2016, Schott 2023, Fastscapelib. Olgun ve hızlı.
- Sabit kıyı: Fastscapelib'in sabit değerli düğümleri. Hazır.

"Kıyı sabit, geçmişi bul" biçimindeki ters problem için yayımlanmış bir yöntem bulunamadı (9. belge). Aracın özgün ve en riskli parçası bu. Mimari bu yüzden riskli parçayı yalıtacak biçimde katmanlı kuruldu: her katman bir öncekinin çıktısını dosya olarak alır ve tek başına sınanabilir.

## Genel akış

```
maske PNG ──► [0 Kayıt] ──► küre ızgarası + kıyı düğümleri
                               │
istekler + istisna defteri ──► [1 Tarih üretici] ──► 4 ile 6 aday tarih (olay listeleri)
                               │        (telefonda seçim)
seçilen tarih ──► [2 Olaydan yükselmeye] ──► zaman dilimi başına yükselme alanı + kayaç sertliği
                               │
                             [3 Aşınma] ──► zaman dilimi başına yükseklik
                               │
                             [4 Çıktı] ──► kareler, kabartma, hikaye metni, ölçüm raporu
                               │
                  Cloudflare (R2 + Pages + Worker) ──► telefon (PWA)
```

Katman 0 ile 4 GitHub Actions'ta Python ile koşar (karar 4). Telefon yalnızca gösterir, seçtirir ve erozyonsuz kaba önizleme yapar.

## Katman 0: maske kaydı ve ızgara

- Girdi: sahibin Photoshop siyah beyaz PNG'si. Küreye kayıt atlas kıyısıyla örtüşme (IoU) ölçülerek yapılır; ölçülen kıta sınırları 7,08°G ile 59,99°K, 44,43°B ile 43,11°D (karar 7).
- Hesap ızgarası: **HEALPix, Nside 512 (hücre 12,7 km, küre geneli 3,1 milyon düğüm)**. Gerekçe: eşit alanlı, kutup sorunu yok, Fastscapelib doğrudan destekliyor ve kendi gezegen örneği tam bu düzeni kullanıyor: kıyı düğümleri sabit, okyanus maskeli (1, 8 ve 13. belgeler). Kıta dışındaki düğümler hesaba girmez.
- Kıyı: maskenin kıyı hücreleri sabit yükseklikli (0 m) taban düğümleridir. Maske her adımda yeniden dayatılmaz, çünkü taban düğümleri zaten oynamaz; kıyı piksel piksel korunur.
- **Sınanmamış varsayım:** hız ölçümüm düz ızgarada yapıldı (1 milyon düğümde adım başına 0,7 s). HEALPix'te hız ölçülmedi. İlk iş bu ölçümdür. Yedek plan: kıta merkezli eşit alanlı düzlem ızgara (Lambert azimutal); kıta kenarında yaklaşık yüzde 17 biçim bozulması getirir, bu yüzden ikinci tercih.

## Katman 1: tarih üretici (özgün parça)

**Temsil.** Bir tarih, zaman sıralı bir olay listesidir. Olay türleri: ayrılma (rift), sürüklenme, dalma, çarpışma, yanal kayma, uzak alan yeniden etkinleşmesi, sıcak nokta. Her olayın blokları, zamanı, hızı ve kenarı vardır. Bloklar küre üzerinde çokgenlerdir; hareketleri Euler dönmeleriyle, saf numpy ve kuaterniyonla hesaplanır (8. belge). pyGPlates bağımlılık yapılmaz; gerekirse yalnızca denetim için kullanılır.

**Geriye sürme.** Bugünkü kıta bloklara bölünür, bloklar bugünkü konumlarından geriye döndürülür. Böylece bugünkü kıyı tanım gereği korunur: tarih hangi yoldan gelirse gelsin son kare maskedir.

**Sert kısıtlar (ihlal edilirse aday atılır):**
- Geçmişte bloklar üst üste binmez (küresel çokgen kesişimi).
- Kıtasal hız üst sınırı 60 mm/yıl (9. belge, Müller 2022 kuralı).
- Verilen kararlar: batıda kara köprüsü, güney geçidi hep açık, güneybatı ayrı kıta, 1 numaralı sıranın uzunluğu çarpışma cephesi kadar (kararlar 1 ile 3).
- İstisna defterindeki sahip istekleri.

**Dört bölge isteği** birer hedef olarak girer: (1) kuzeydoğunun güneyinde doğu batı sıradağı, (2) arkasında 1000 ile 1500 m Zagros tipi çanak, (3) yarımada çarpışması, Apenin ve Alp tarzı ayrı adaylar olarak, (4) iç denizde tümüyle dağlık mikro kıta.

**Arama ve seçim.** Adaylar kalite ve çeşitlilik aramasıyla (MAP-Elites) üretilir, sunulacak 4 ile 6 aday çeşitlilik gözeten seçimle (k-DPP) ayrılır (10. belge). İki tarih arasındaki uzaklık üç şeyden hesaplanır: olay dizisi farkı, blok yolları farkı, sonuç haritası farkı. Bu uzaklık tanımı ve aday sayısı benim tasarımım; kaynağı yok.

**Çelişkiler.** İstekler birlikte sağlanamıyorsa araç hiçbirini sessizce gevşetmez. En küçük çelişen istek kümesini bulur, gösterir, hangi isteğin ne kadar gevşetilmesi gerektiğini seçenek olarak sunar. Seçim deftere yazılır (16. belge).

**Sade dil.** Her olay kısa bir soru ve yanıt olarak anlatılır, her adayın yanında küçük haritası durur (10. belge).

**Risk.** Bu katmanın yayımlanmış bir örneği yok. Arama uzayı büyük çıkarsa ilk sürümde blok bölünmesini yarı otomatik yaparım: araç önerir, siz telefonda düzeltirsiniz. Bu, `KARARLAR.md`'deki açık "blok ayrıştırmanın otomatiklik düzeyi" maddesinin yanıtı olur; şimdiden karar vermiyorum, prototip gösterecek.

## Katman 2: olaydan yükselmeye

Tam geodinamik simülasyon yapılmaz; Actions'a sığmaz ve gereksizdir (12. belge). Kural tabanlı üretici kullanılır:

- Çarpışma: yükselme, cepheye uzaklığın, göreli hızın ve geçen sürenin işlevi (Cortial tarzı). Kuşak genişlikleri ve yükseklikleri 2. belgenin değerlerinden.
- Kabuk hesabı: Airy izostazisi, toplam kalınlaşmanın yaklaşık yüzde 15'i yüzey yükselmesi; önülkede bükülme çukuru, aşırı dolu varsayılır (3. belge).
- Dalma, rift, yanal fay, sıcak nokta şablonları 5. belgenin değerlerinden. Uzak alan etkisi 1500 ile 2500 km, 10 ile 30 milyon yıl gecikmeyle (2. belge).
- Sahip istisnaları yükselme alanında fırça olarak eklenir; hedef yükseklik oransal-integral düzeltmeyle tutturulur (Schott 2023, 16. belge).
- Yükselme kıyıya doğru yumuşakça sıfıra iner. Aksi halde sabit kıyıda yapay basamak oluşur (1 ve 13. belgeler). Sönümleme biçimi sınanmadı; katman 3 prototipinin ilk deneyi bu.
- Kayaç sertliği haritası (çökel, magmatik, metamorfik) blok tarihinden türetilir ve aşınma katsayısını belirler (17. belge).

## Katman 3: aşınma

- Motor: Fastscapelib 0.3.0 (conda-forge derlemesi; pip tekerleğinde HEALPix yok). Akarsu güç yasası n = 2, m = 1 (m/n = 0,5); n = 1 tüm ovaları deniz seviyesine aşındırdığı için değiştirildi (deneyler/SONUCLAR.md). Yamaç difüzyonu bu hücre boyunda etkisiz, kullanılmıyor. Bölgesel izostazi: aşınan yükün 0,85'i 80 km ölçeğinde geri sıçrar.
- Zaman: tarihin dilimleri boyunca yürür; her dilimde katman 2'nin yükselmesi eklenir. Böylece dağlar yükselirken aşınır, olay bitince yaşlanır (4. belge).
- Çökelme: Fastscapelib'de yok. İlk sürümde basit kural: kapalı çukurlar dolup taşar (göl), önülke çukurları dolu varsayılır, kıyıya ulaşan tortu sistemden çıkar (15. belge). Gerçek tortu taşınımı ancak ilk sonuçlar yetersiz çıkarsa eklenir.
- **Ayar, literatürden değil ölçümden.** Aşınma katsayısı, aynı hücre boyunda gerçek dağlardan ölçtüğüm rölyef hedeflerine göre ayarlanır: 10 km hücrede genç yüksek dağ 1100 ile 1450 m, eski dağ yaklaşık 460 m, Zagros tipi yaklaşık 840 m yerel rölyef (20. belge). Tek çözünürlükte koşulur; çözünürlük değişirse yeniden ayar gerekir, çünkü aynı katsayı 20 km ile 5 km arasında 3,6 ile 5,5 kat farklı yükseklik verdi (14. belge).
- Yağış ilk sürümde enlem bandına bağlı basit bir alandır; dağ yağışı modeli sonraki aşama (19. belge). Buzul yok (18. belge).
- Süre bütçesi: düz ızgara ölçümüne göre 1 milyon düğüm ve 5000 adım yaklaşık 1 saat; Actions iş sınırı 6 saat (13 ve 23. belgeler).

## Katman 4: çıktı ve ölçüm

- Her zaman dilimi için 16 bit yükseklik PNG'si ve önceden gölgelenmiş kabartma görüntüsü (çok yönlü gölgeleme, yükseklik renkleri; 21. belge). Ölçülen boyut 1 milyon hücrede kare başına yaklaşık 1,5 MB.
- Hikaye metni, istisna defteri ve gerçekçilik raporu. Rapor bağıl ölçülerle yapılır: rölyefin yüksekliğe oranı, eğim dağılımı, akarsu ağı ölçeklemesi (Hack üssü yaklaşık 0,6), genç ve eski dağ farkı (20. belge).
- Kareler Cloudflare R2'ye yazılır; Actions'ın kendi depolaması 60 ile 600 MB'lık kare dizisine yetmez (23. belge).

## Uygulama ve altyapı

- Telefon uygulaması: ana ekrana eklenen PWA, Cloudflare Pages'te, Cloudflare Access arkasında (karar 5; 22 ve 23. belgeler).
- Tetikleme: uygulama senaryoyu bir Worker'a yollar; Worker kimliği doğrular, günlük koşu sayısını denetler, GitHub'da iş akışını başlatır. GitHub anahtarı yalnızca Worker'da gizli değer olarak durur.
- Durum: uygulama açıkken Worker üzerinden yoklama. Bildirim (Web Push) ilk sürümde yok.
- Zaman çubuğu: kareler önceden yüklenir, kaydırıcı kareler arasında gezer. Aday karşılaştırma: küçük haritalar yan yana, seçilen iki aday arasında kaydırma.
- Telefonda anlık önizleme yalnızca erozyonsuz yükselme alanıdır ve "kaba taslak" diye etiketlenir; rölyef büyüklüğü için sayı göstermez (karar 4, 14. belge).

## Kurulum sırası

Her aşamanın sonunda size telefonda bakılabilir bir çıktı verilir; bir aşama sınanmadan sonrakine geçilmez.

1. **İskelet ve kayıt.** Maske küreye oturur, HEALPix ızgarası ve kıyı düğümleri kurulur, HEALPix hız ölçümü yapılır. Çıktı: kıyı örtüşme raporu.
2. **Aşınma çekirdeği.** Elle çizilmiş bir yükselme alanıyla aşınma koşar; kıyı basamağı deneyi ve rölyef ayarı burada yapılır. Çıktı: ilk kabartma haritası.
3. **Olaydan yükselmeye.** Elle yazılmış tek bir tarihten (örneğin yalnızca büyük çarpışma) yükselme ve zaman kareleri. Çıktı: ilk animasyon.
4. **Tarih üretici.** Aday tarihler, çelişki gösterimi, sade dil.
5. **Uygulama ve altyapı.** PWA, Worker, R2; `KURULUM.md` rehberiyle Cloudflare ve GitHub kurulumu birlikte yapılır.
6. **İnce işler.** Dağ yağışı, ayrıntı ekleme, gerekirse gerçek tortu taşınımı.

En riskli parça 4. aşamadır ama çıktısı ancak 2 ve 3 çalışıyorsa anlamlıdır; sıra bu yüzden böyle.

## Açık kalanlar

- HEALPix hızı ve kıyı sönümleme biçimi: 1 ve 2. aşamada ölçülecek.
- Blok bölünmesinin otomatiklik düzeyi: 4. aşama prototipi gösterecek.
- Animasyon kare sayısı ve zaman adımı: 3. aşamada, dosya boyutu ölçülerek.
- Maske henüz verilmedi. 1. aşama maskeyi bekler; 2. aşamanın çekirdeği sentetik bir test maskesiyle başlayabilir.
