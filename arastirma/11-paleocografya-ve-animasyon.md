# 11. Paleocoğrafya ve animasyon kareleri

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun sentezidir (A paleotopografya haritalarının üretimi, B deniz seviyesi, kıyı çizgisi ve kare ara değerleme); sentezi ben yazdım. Ham notlar `arastirma/notlar/11/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** yalnızca özet okundu, **[Ö]** arama özeti, doğrulanamadı, **[H]** bizim çıkarımımız, **[Y]** bulunamadı.

## Kısa sonuç

**1. Hazır paleotopografya setleri yöntemce kaba ve yazarlarınca da hatalı sayılıyor.** Scotese ve Wright (2018): 117 paleo-yükseklik haritası, 5 milyon yıl aralık, son 540 milyon yıl, 1°×1° ızgara [B]. Yöntem el işi: litofasiyes haritaları ve tektonik modelle geriye düzenleme, modern topografya ve batimetri döndürülüp 256 gri tonlu haritada elle düzenleniyor, sonra yüksekliğe çevriliyor; yazarlar "çok sayıda hata" olduğunu ve dağ yüksekliklerinin büyük olasılıkla abartıldığını yazıyor, nicel hata modeli yok [B]. Bizim aracımız bu yöntemi taklit etmeyecek; kendi fiziksel yükselme-aşınma hesabını yapacak. Bu setler yalnızca karşılaştırma için kullanılabilir.

**2. Paleotopografyanın belirsizliği nicel olarak verilemiyor.** Poblete ve diğerleri (2021, Earth-Science Reviews 214:103508): Kenozoyik (60, 40, 20 milyon yıl) için altı aşamalı yöntem; modern topografya bloklara bölünüp döndürülüyor, bölge bazında doğrusal yeniden ölçekleniyor (Z' = A + m·Z) [B]. Yazarlar belirsizliği nicel vermeyi "gelecek araştırma konusu" sayıyor; Tibet için tahmini azami yükseklik 1000 ile 4500 m, Bolivya oroklini için en az 80 km, Güney Asya için en az 200 km konum belirsizliği [B].

**3. Deniz seviyesi eğrileri 100 m'yi aşan aralıkta birbirini tutmuyor.** Geç Kretase tepesi: yaklaşık +100 ± 50 m (Miller 2005 [B-öz]), +170 m (aralık 85 ile 270 m; Müller 2008 [B-öz]), 75 ile 110 m (Kominz 2008 [B-öz]); yayımlanmış tahminler yaklaşık +40 ile +250 m arasında. Kıyı çizgisini bunlardan hesaplayan araç için bu belirsizlik doğrudan kıyı belirsizliğine dönüşür.

**4. Kare ara değerleme için standart yöntem var.** Dönmeler quaternion üzerinde büyük daire ara değerlemesiyle (slerp) sabit açısal hızla ara değerlenir; ikinci türev sürekliliği için spline gerekir (Shoemake 1985, [B]). pyGPlates `FiniteRotation.interpolate` imzası doğrulandı ama algoritması belgede yok [B-öz].

## 1. Paleotopografya veri setleri

| Set | Kapsam | Yöntem | Sınırlama |
|---|---|---|---|
| Scotese ve Wright 2018 (PALEOMAP PaleoDEM) | 117 harita, 5 milyon yıl aralık, 540 milyon yıl, 1°×1° (m), yüksek çözünürlük yaklaşık 10 km ve 40 m | litofasiyes ve tektonik modelle geriye düzenleme, el işi gri ton düzenleme; Paleozoyik derin okyanus 4800 m sabit | hatalar yazarlarca kabul edilmiş, nicel hata yok; veri earthbyte.org'da (NetCDF, CSV, GPlates dosyaları), Zenodo doi 10.5281/zenodo.5460860 (0,1° NetCDF) [B] |
| Poblete ve diğerleri 2021 | 60, 40, 20 milyon yıl (Kenozoyik) | GPlates, paleobatimetri, paleokıyı, izostatik ve östatik düzeltme, paleoyükseklik; etkileşimli site map.paleoenvironment.eu | belirsizlik nicel verilmemiş [B] |
| Paleolatitude.org 3.0 (van Hinsbergen ve diğerleri 2026, PLOS ONE, doi 10.1371/journal.pone.0346817) | rijit poligon levha modeli | yalnızca paleoenlem | yükseklik çıktısı yok [B-öz] |

Promptumdaki üç hata düzeltildi: Scotese ve Wright "Earth system model" değil, elle yapılan bir yöntem; Poblete ve diğerleri Fanerozoyik değil Kenozoyik; "Utrecht paleocoğrafya hesaplayıcısı" olarak yükseklik üreten bir araç doğrulanamadı (yalnızca 2020 EGU bildirisi planlanan bir araçtan söz ediyor, yayın durumu bulunamadı [Y]). Hay (2006) paleotopografya yöntemi makalesi bulunamadı [Y]; Hay'in 1999 ve 2016/17 çalışmaları ve Markwick ve Valdes (2004, PPP 213) yalnızca özet düzeyinde [Ö]. Van Hinsbergen (2015) PDF indirmesi bağlantı sıfırlamasıyla başarısız oldu.

**Paleoyükseklik göstergeleri.** Kararlı izotop (paleotoprak ve meteorik su): Botsyun ve diğerleri (2016) özetine göre sitelerin yaklaşık yüzde 40'ı tam topografik sinyali yansıtıyor, 2,5 ‰ sapma [B-öz]; yaprak fizyonomisi ve biyotik yöntemler; termokronoloji doğrudan yüzey yüksekliği vermez [Ö]. Botsyun gövde metni (m cinsinden hata) okunmadı [Y].

## 2. Deniz seviyesi

| Kaynak | Değer | Etiket |
|---|---|---|
| Miller ve diğerleri 2005 | Kretase tepe +100 ± 50 m | [B-öz] |
| Müller ve diğerleri 2008, Science | geç Kretase +170 m (85 ile 270 m); yayımlanmış tahminler yaklaşık +40 ile +250 m | [B-öz] |
| Kominz ve diğerleri 2008 | geç Kretase yaklaşık 75 ile 110 m; erken Eosen en çok yaklaşık 150 m | [B-öz] |
| Miller ve diğerleri 2020, Sci. Adv. | Eosen sıcak sera dönemi küresel ortalama deniz seviyesi: buzsuz çizgi +66 m, Eosen'de +40 ile 50 m; Senozoyik uzun dönem düşüş 1,0 ± 0,5 m/milyon yıl | [B] |
| Wright ve diğerleri 2020 | okyanus havzası hacmi kaynaklı deniz seviyesi Jura'dan beri yaklaşık 200 m değişti; oran özette yok, ortalama yaklaşık 1 m/milyon yıl benim türetmem | [B-öz ve H] |
| Haq 1987 (+250 m değeri aslında Haq 2014 revizyonunda, Turoniyen 240 ile 250 m) | | PDF erişilemedi |
| Miller 2011 | 10 m/milyon yıl'dan az (tepe değişim oranı) | [Ö] |

Dinamik topografya: Moucha ve diğerleri (2008) New Jersey ve Batı Afrika kenarlarında son 30 milyon yılda yaklaşık 100 m dinamik topografya değişimi buldu; "kararlı" alanlardaki uzun dönem deniz seviyesi tek başına östatik okunamaz [Ö]. Flament ve diğerleri (2013): tek bir pasif kenardan küresel deniz seviyesi tahmin edilemez [Ö]. Bu sonuç doğrudan önemli: aracın kıyıları sabit olduğu için dinamik topografya ve deniz seviyesi kıyıyı oynatmaz; ama aracın içsel yükselme hesabına yansıması bu çalışmalarla uyumlu olmalı.

"Gurnis 2012 Nature Geoscience" bulunamadı [Y]; en yakın çalışma Spasojević ve Gurnis (2012, AAPG Bull.), PDF erişilemedi. Açık bir "m/milyon yıl tepe oranı" kaynağı bulunamadı [Y]. "Continental freeboard" terimi için kaynak bulunamadı [Y].

## 3. Kıyı çizgisi ve hipsometri

- Kıta kabuğu yeryüzü yüzeyinin yaklaşık yüzde 41'i, ortalama kabuk kalınlığı yaklaşık 36 km (Cogley 1984, 14 kıta) [Ö].
- Açık bir "kara-deniz" formülü doğrulanamadı. Hipsometrik eğri A(h) ile taşan alan yöntemi bir sentezdir, kaynaklı değil [H].
- Aracın bağlamında: kıyı sabit olduğundan deniz seviyesi kıyıyı kaydırmaz; kıyı kayması yalnızca paleocoğrafya karelerinde (hikaye amaçlı) hesaplanabilir. Bu hesap 6. belgedeki 120 m / eğim kuralına dayanır [H].

## 4. Animasyon kareleri

- **Quaternion slerp.** Düz quaternion ara değerlemesi ortada hızlanır; büyük daire (slerp) ara değerlemesi sabit açısal hız verir. Slerp(q1, q2; u) formülü; spline uçlarında teğet şartı birinci mertebe süreklilik sağlar (Shoemake 1985, SIGGRAPH, [B]). Kare sayısı için kaynak yok [Y].
- **pyGPlates.** `FiniteRotation.interpolate(finite_rotation1, finite_rotation2, time1, time2, target_time)` imzası doğrulandı; algoritma belgede yok (doğrulanmadı). GPlates'te 1, 5 ve 10 milyon yıllık adımların kaynağı bulunamadı [Y].
- **Zaman adımı ve kararlılık.** Braun ve Willett (2013, Geomorphology 180 ile 181:170 ile 179): Fastscape örtük şeması açık şemadan çok daha büyük adımlara dayanıklı; yalnızca kararlı durum dt'den bağımsız, geçici sonuçlar dt'ye bağlı [Ö, ikincil]. CFL benzeri dt sınır formülü bulunamadı [Y]. Pratik öneri: dt'yi yarıya indirip yakınsama testi [H].

## 5. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| Karelerin zaman adımı | 1 ile 5 milyon yıl (hikaye kareleri), hesap adımı 0,1 ile 1 milyon yıl; kaynaksız tasarım seçimi | [H] |
| Dönme ara değerleme | quaternion slerp; spline ile C1 süreklilik | [B] |
| Paleotopografya kaynağı | aracın kendi hesabı; Scotese-Wright yalnızca karşılaştırma için | [B] |
| Deniz seviyesi | kıyı sabit; hikaye karelerinde ±100 m bandında senaryo, uzun dönem eğilim 1 m/milyon yıl'dan az | [Ö ve B] |
| Deniz seviyesi belirsizliği | Kretase tepesinde ±100 m civarı | [B-öz] |
| Dinamik topografya | ±0,5 km (5. belge) | [B] |
| Yakınsama testi | dt'yi yarıya indirip sonuç farkını ölç | [H] |

## 6. Kaynaklar arası çelişkiler

- Kretase deniz seviyesi tepe: +100, +170, +75 ile 110 ve +250 m (Haq 2014).
- Haq 1987 ile Haq 2014 değerleri karışık anılıyor; +250 m Haq 2014'e ait.
- Scotese'in kendi hata kabulü ile haritaların yaygın kullanımı arasında bir uyumsuzluk: yazarlar hata ve abartı uyarısı yapıyor ama harita bir referans olarak kullanılıyor.

## 7. Bulunamayanlar ve doğrulanamayanlar

- Haq 1987 PDF (TLS hatası, atlatılmadı); Müller 2008 tam metni (ResearchGate kullanılamadı); Miller 2020 science.org (Cloudflare, Europe PMC kullanıldı); landlab.readthedocs.io (DNS).
- Hay 2006; Markwick ve Valdes 2004; van Hinsbergen 2015; Botsyun 2016 gövde metni; Baatsen ve diğerleri iş akışı; Scotese 2018 lisans dosyası.
- Kretase deniz seviyesi için açık "m/milyon yıl" tepe oranı; "continental freeboard"; GPlates zaman adımı örnekleri; Fastscape dt sınırı.
- Wright (2020) için tahmin ettiğim DOI yanlış bir makaleye gitti; notlara eklenmedi.

## 8. Promptumdaki hatalar (düzeltildi)

- "Scotese ve Wright 2018, Earth system model" yanlış: elle yapılan bir yöntem.
- "Poblete ve diğerleri 2021, Phanerozoik" yanlış: Kenozoyik (60, 40, 20 milyon yıl).
- "Utrecht paleogeography calculator" yükseklik üreten bir araç olarak doğrulanamadı.
- "Kretase +250 m" Haq 1987'ye değil Haq 2014 revizyonuna ait.
- "Gurnis 2012 Nature Geoscience" bulunamadı.

## Başlıca kaynaklar

- Scotese ve Wright 2018: earthbyte.org kaynak sayfası ve https://doi.org/10.5281/zenodo.5460860
- Poblete ve diğerleri 2021, Earth-Sci. Rev. 214:103508 ve map.paleoenvironment.eu
- Miller ve diğerleri 2020, Science Advances (Europe PMC PMC7228749)
- Shoemake 1985, SIGGRAPH, "Animating rotation with quaternion curves"
- Müller ve diğerleri 2008, Kominz ve diğerleri 2008, Moucha ve diğerleri 2008, Flament ve diğerleri 2013, Braun ve Willett 2013: ham notlardaki bağlantılar
- Tam liste ve her bilginin kaynağı `arastirma/notlar/11/` içinde.
