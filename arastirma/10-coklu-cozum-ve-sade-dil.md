# 10. Çoklu çözüm üretimi, seçim ve sade dil

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun sentezidir (A çoklu çözüm üretimi, B sade dil, belirsizlik görselleştirme, karşılaştırma ve seçim arayüzü); sentezi ben yazdım. Ham notlar `arastirma/notlar/10/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** yalnızca özet ya da sunum okundu, **[Ö]** arama özeti, doğrulanamadı, **[H]** bizim çıkarımımız, **[Y]** bulunamadı. Bu konu fiziksel sayı değil yöntem konusudur; bu yüzden varsayılanlar sayı yerine tasarım kararları olarak verildi.

## Kısa sonuç

**1. Çözümlerin "anlamlı biçimde farklı" olması üç ayrı iştir: çeşitlilik ölçüsü seçmek, çeşitli aday üretmek ve çeşitli altküme seçmek.** Her biri için tam metni okunmuş bir yöntem var: kalite-çeşitlilik (MAP-Elites), yenilik araması (novelty search) ve determinantal nokta süreci (DPP).

**2. Ters problemde "kabul edilen örnekler kümesi" çoklu çözümün doğal tanımı.** Schaaf ve diğerleri (2021, GemPy): olabilirlik yerine bir mesafe fonksiyonu kullanılıyor (ABC), eşik ε; topoloji grafları için Jaccard indeksi mesafe olarak kullanılmış [B]. Araç için en doğrudan model bu: geçerlilik kısıtlarını sağlayan tüm tarihler kümesinden çeşitli bir altküme sun.

**3. Belirsizliği göstermenin en iyi kanıtlanmış yolu olası sonuçları animasyonla göstermek.** Hullman, Resnick ve Adar (2015): animasyonlu olası sonuçlar hata çubuklarından ve keman grafiklerinden daha doğru yargı sağladı [B]. Bu, aracın zaman kaydırıcısında çoklu tarih gösterimiyle örtüşüyor.

**4. Kullanıcıdan seçim almak için çok seçenekli (groupwise) arayüz daha verimli ama daha yorucu.** On uzmanla yapılan küçük bir çalışmada çok seçenekli arayüz 21 dakikada ortalama yüzde 86,7 daha fazla tercih verdirdi, bilişsel yük daha yüksekti; istatistiksel anlamlılık iddia edilmiyor (Kompatscher ve diğerleri 2025, arXiv 2507.04340, [B]). Bu, kanıt değil ipucu.

**5. Telefonda harita karşılaştırmaya özel çalışma bulunamadı.** Mevcut çalışmalar masaüstü ve web GIS üzerinde [Ö]; telefon için çıkarımlar benim yorumum [H].

## 1. Çoklu çözüm: yöntemler

| Yöntem | Ne yapar | Kaynak ve etiket |
|---|---|---|
| MAP-Elites | Özellik uzayını (N boyutlu, ayrıklaştırılmış) hücrelere böler; her hücrede en iyi "elit" tutulur; yavru ya yeni hücreye yerleşir ya mevcut sakinin yerini alır. Yazarlar "MAP-Elites is an illumination algorithm" diyor | Mouret ve Clune 2015, arXiv 1504.04909 [B] |
| Yenilik araması | Uygunluk yerine yeniliği ödüllendirir: ρ(x) = (1/k) Σ dist(x, μᵢ), μᵢ en yakın k komşu; yenilik ağırlıklı arşiv | Lehman ve Stanley 2011, Evol. Comput. 19(2):189 ile 223, doi 10.1162/EVCO_a_00025 [B, üçüncü taraf kopya] |
| Determinantal nokta süreci (DPP) | Kalite ve çeşitlilik ayrı terimler: L_ij = q_i φ_iᵀ φ_j q_j (Eşitlik 85); P_L(Y) ∝ (Π q_i²) det(S_Y) (Eşitlik 87); k-DPP sabit boyutlu altküme seçer | Kulesza ve Taskar 2012, arXiv 1207.6083 [B] |
| Kısıt çözme ile üretim | WaveFunctionCollapse: çıktı yalnızca girdi örüntülerini içerir; en düşük entropili hücre çöktürülür, kısıtlar yayılır; kısıt çözme NP-zor, çelişki nadir; "kolay" tile setleri ilginç çeşitlilik üretmez | mxgmn/WaveFunctionCollapse README [B] |
| ASP ile çeşitli çözümler | k-çeşitli küme: Δ(S) ≥ k, Δ Hamming tabanlı olabilir; dört yöntem, çevrimiçi çözücü değişikliği en iyi sonucu verdi | Eiter ve diğerleri, arXiv 1108.3260 [B] |
| ABC ile ters problem | Olabilirlik yerine mesafe fonksiyonu; ABC-REJ, tolerans ε; topoloji için Jaccard J(A,B) = \|A∩B\|/\|A∪B\| | Schaaf ve diğerleri 2021, GMD 14:3899 [B] |
| Bayes ters problem kuramı | Çözüm, posterior ile ağırlıklı tüm modellerin kümesi | Tarantola (2005) [Ö, denklemler doğrulanamadı] |

Okunamayanlar: Sambridge ve Mosegaard (2002), Buffan ve diğerleri (2023, DOAJ sayfası) ve Lehman ve Stanley'nin yayıncı sayfası bot doğrulamasına takıldı, atlatılmadı. Tarantola kitabı ücretli, ipgp.fr DNS/403 hatası verdi. Wasserstein / EMD mesafesi (Villani 2009, Peyré ve Cuturi 2019) yalnızca arama özetinde [Ö]. ASP ile prosedürel içerik üretimi kaynakları (Smith ve Mateas, Togelius ve Justinussen, Wang ve Kreminski 2024) tam okunmadı.

Bulunamayan: "olay tabanlı" üretim, paleocoğrafya ve Bayes senaryo ağacını birleştiren tek bir kaynak [Y]. Komşu çalışmalar: Skauvold ve Eidsvik (EnKF, havza modeli, arXiv 1711.07763); 2025 GSA özeti (deprem senaryoları, dört senaryo, Monte Carlo); EGU 2020 parçacık filtresi [Ö]. Buffan ve diğerleri (2023): beş açık levha modeli, paleo-enlem sapması ve ortalama jeodezik mesafe ile karşılaştırılmış [Ö]. GPlates tartışmalarında kovaryans, bootstrap ve rotasyon karşılaştırması öneriliyor [Ö].

**Çözümler arası mesafe için öneri (bizim tasarımımız [H], kaynaklı bir kural değil).** Tarih bir blok yörüngesi kümesi olarak tanımlandığından üç mesafe birleştirilebilir: (a) blok konumlarının ortalama jeodezik farkı, (b) haritalar arası piksel farkı ya da alan ağırlıklı Wasserstein, (c) olay dizisinin Jaccard / Hamming mesafesi (hangi çarpışma, hangi rift, hangi sırayla). Çeşitlilik ölçüsü yalnızca piksel farkı olursa araç benzer hikayeleri farklı sayabilir; bu yüzden olay dizisi mesafesi gerekli görünüyor.

## 2. Jeolojinin sade anlatımı

- USGS "This Dynamic Earth" (pubs.usgs.gov/gip/dynamic) okundu [B]: kısa paragraflar, her bölüm bir soruyla açılıyor, "iki dev konveyör bandı" gibi benzetmeler, tarih için zaman çizgisi (Pangea 225 ile 200 milyon yıl önce). Bu, aracın hikaye dili için en kullanışlı model.
- Scotese PALEOMAP (TLS sertifika uyuşmazlığı, atlatılmadı) ve Blakey Deep Time Maps (HTTP 503; haritalar ticari lisanslı [Ö]) okunamadı. GSA Geologic Time Scale v6.0 posteri satılık, ücretsiz PDF'ler eski sürüm; etkileşimlilik doğrulanamadı [Ö].
- Story map için akademik değerlendirme bulunamadı [Y].

**Aracın hikaye dili için çıkarım [H]:** her olay tek cümlelik bir soru ve yanıt biçiminde ("Bu kıta neden yükseldi? Çünkü güneyden gelen blok kuzeye çarptı"), sayılar parantez içinde ve yalnızca ilgili tarihte, teknik terimler ilk geçtiği yerde açıklanmış. Bu USGS yöntemine dayanıyor ama araç için doğrulanmış bir kural değil.

## 3. Belirsizlik ve karşılaştırma arayüzü

- Correll, Hullman ve diğerleri (2018), "In Pursuit of Error", InfoVis: 86 çalışma, 372 değerlendirme yolu; öneriler: açıklamayı hedef yap, karar çerçevesi kullan, güven raporunun belirsizliğini hesaba kat [B]. Promptumdaki "Padilla, Kay, Hullman 2021" çalışması bulunamadı [Y].
- Hullman, Resnick ve Adar (2015), "Hypothetical Outcome Plots", PLOS ONE, doi 10.1371/journal.pone.0142444: animasyonlu olası sonuçlar hata çubuklarından ve keman grafiklerinden daha doğru yargı sağlıyor; "sayma ve bütünleştirme" ile okunabiliyor [B].
- Gleicher (2017 konuşma slaytları): karşılaştırma için üç tasarım (yan yana koyma, üst üste koyma, açık kodlama) ve üç ölçekleme stratejisi (sırayla tara, altküme seç, özetle) [B-öz]. Gleicher (2011) makalesi alınamadı [Ö]. Tufte'nin small multiples tanımı yalnızca ikincil kaynaklardan [Ö].
- Takagi (2001), Proc. IEEE, interaktif evrimsel hesaplama: insan değerlendirmesi uygunluk değerinin yerine geçiyor; insan yorgunluğu ana sorun [Ö, tam metin yok]. Turnuva seçimi için doğrudan kaynak bulunamadı [Y].
- Mobil: swipe ile yan yana karşılaştırma çalışması (25 katılımcı) masaüstü / web GIS üzerinde; yan yana dört haritada daha iyi, swipe ayarları sezgisel değil. Tablet telefondan daha çok tercih edildi [Ö]. Telefonda doğrudan karşılaştırma bulunamadı [Y].

## 4. Aracın tasarım varsayılanları

| Konu | Öneri | Dayanak |
|---|---|---|
| Aday üretimi | MAP-Elites ya da yenilik araması ile çeşitli, kısıtları sağlayan tarihler | [B] |
| Altküme seçimi | k-DPP ile 4 ile 6 aday seçilsin (kalite ve çeşitlilik ayrı ayarlanır) | [B], sayı tasarım seçimi [H] |
| Geçerlilik | önce sert kısıtlar (maske, istisna defteri, fiziksel sınırlar); sonra çeşitlilik | [B] ve [H] |
| Mesafe | blok konumu farkı, alan ağırlıklı harita farkı, olay dizisi Jaccard'ı birleşimi | [H] |
| Gösterim | aday başına küçük harita, ortak zaman kaydırıcısı | [Ö ve H] |
| Belirsizlik | tek tarih yerine animasyonlu olası sonuçlar (HOP) | [B] |
| Seçim arayüzü | önce çok seçenekli seçim, ardından yakınlaştırma; kullanıcıya yorgunluk sınırı | [B, küçük örneklem] |
| Hikaye dili | her olay için soruyla açılan kısa paragraf | [B] ve [H] |
| Telefon | iki harita için kaydırma ya da örtme; çok harita için seçilmiş alt küme | [H] |

## 5. Kaynaklar arası çelişkiler

- Çoklu çözüm literatürü fiziksel bir çelişki üretmiyor; ancak "çeşitlilik" tanımı kaynaktan kaynağa değişiyor: özellik uzayı hücreleri (MAP-Elites), en yakın komşu uzaklığı (novelty), determinant (DPP) ve Hamming (ASP). Hiçbiri doğrudan paleocoğrafi tarihler için doğrulanmadı.
- Kompatscher ve diğerleri (2025) çok seçenekli arayüzü daha verimli buldu ama bilişsel yükün de arttığını yazıyor; sonuç küçük örneklemde ve anlamlılık iddiası yok.
- Wilson (iletişim araştırması) ile bu konunun çelişkisi yok; sade dil önerileri tek bir kamusal kaynaktan (USGS).

## 6. Bulunamayanlar ve doğrulanamayanlar

- Sambridge ve Mosegaard (2002); Tarantola (2005) denklemleri; Takagi (2001) ve Gleicher (2011) tam metni; Tufte kitabı; Buffan (2023) tam metni; ASP-PCG kaynakları.
- Scotese PALEOMAP ve Blakey haritaları (erişilemedi); GSA zaman çizelgesi etkileşimliliği; story map akademik değerlendirmesi.
- Olay tabanlı üretim + paleocoğrafya + Bayes senaryo ağacı için tek bir kaynak.
- Turnuva seçimi ve telefonda harita karşılaştırması için doğrudan kaynak.
- Hiçbir kaynakta "5 ile 6 aday" gibi bir sayı yok; bu benim tasarım önerim.

## 7. Promptumdaki hatalar (düzeltildi)

- "Padilla, Kay, Hullman 2021" bulunamadı; en yakın doğrulanmış kaynak Correll ve diğerleri 2018.
- Gleicher 2011 makalesi alınamadı; yalnızca 2017 sunumu okundu.
- "Takagi 2001 interaktif evrimsel hesaplama" atfı arama özetinden; tam metin okunmadı.
- "Visual comparison techniques Gleicher 2011" ifadesi kitap adı olarak belirsiz; makale "Visual comparison for information visualization" (Information Visualization 10(4)).

## Başlıca kaynaklar

- Mouret ve Clune 2015: https://arxiv.org/abs/1504.04909
- Kulesza ve Taskar 2012: https://arxiv.org/abs/1207.6083
- Lehman ve Stanley 2011: https://doi.org/10.1162/EVCO_a_00025
- Schaaf ve diğerleri 2021, GMD 14:3899: https://gmd.copernicus.org/articles/14/3899/2021/gmd-14-3899-2021.html
- Eiter ve diğerleri: https://arxiv.org/abs/1108.3260
- Hullman, Resnick, Adar 2015: https://doi.org/10.1371/journal.pone.0142444
- Correll ve diğerleri 2018: https://mucollective.northwestern.edu/files/2018-UncertaintyEvalSurvey-InfoVis.pdf
- Kompatscher ve diğerleri 2025: https://arxiv.org/abs/2507.04340
- USGS This Dynamic Earth: https://pubs.usgs.gov/gip/dynamic/dynamic.html
- Tam liste ve her bilginin kaynağı `arastirma/notlar/10/` içinde.
