# B: Jeolojik bilginin sade dille anlatımı, belirsizlik görselleştirmesi ve karşılaştırma/seçim arayüzleri

Durum: TAMAMLANDI (ana bulgular; eksikler bölüm sonlarında işaretli)
Etiketler: [B] tam metin okundu, [B-öz] özet okundu, [Ö] arama sonucu özeti, BULUNAMADI / ERİŞİLEMEDİ

## 0. Özet (sade dilde)
- Jeolojik anlatıda kısa paragraf, soru-cevap ve benzetme (ör. 'iki dev konveyör bandı') USGS'te ana yöntemdir [B].
- Belirsizlik için sayıları değil 'olası sonuçları' göstermek (HOP) daha doğru yargı sağlıyor [B].
- Karşılaştırmada üç yöntem: yan yana, üst üste, doğrudan kodlama (Gleicher) [B-sunum].
- Seçim arayüzünde çok seçenekli yöntem daha fazla tercih üretiyor, ama bilişsel yükü artırıyor [B].
- Mobilde yan yana yerine dönüşümlü/kaydırmalı gösterim ve küçük seçim kümeleri daha uygun görünüyor, ama doğrudan telefon çalışması bulunamadı [Ö].

## 1. Jeolojik bilginin kamuya anlatımı ve paleocoğrafya görselleştirme
- [B] USGS "This Dynamic Earth" (Smith, Gerald; Baker & Russell; USGS GIP 1996; çevrimiçi)
  URL: https://pubs.usgs.gov/gip/dynamic/dynamic.html (+ alt sayfalar: /preface.html, /historical.html, /developing.html, /understanding.html, /hotspots.html, /unanswered.html)
  - Sade dil örneği (preface, [B]): "Plate tectonics is a relatively new scientific concept, introduced some 30 years ago" ve ardından kısa, somut tanımlar.
  - Benzetme (understanding.html, [B]): "Picture two giant conveyor belts, facing each other but slowly moving in opposite directions" - okurun zihninde bir mekanizma kurmak için kullanılan ortak bir kalıp.
  - Yapı: kısa paragraflar, her bölüm bir soruyla açılıyor (hotspots: "How do the Hawaiian Islands ... fit into the plate-tectonics picture?") [B].
  - Tarihsel anlatı (historical.html, [B]): Wegener'in 'kıta kayması' fikri, Pangaea'nın 225-200 My önce parçalanmaya başladığı ifadesiyle zaman çizgisi olarak sunulur. Sayılar kesin ve kısa tutulur.
  - Görselleştirme: Pangaea parçalanma diyagramları, "Note the curvature of the Earth" gibi fotoğraf açıklamaları. Harita yerine adım adım diyagram dizisi.
- [ERİŞİLEMEDİ] Scotese PALEOMAP (https://www.scotese.com/): TLS hatası (sertifika alan adı uyuşmuyor: "no alternative certificate subject name matches target host name 'www.scotese.com'"). Sertifika hatası atlatılmadı.
- [ERİŞİLEMEDİ] Ron Blakey / deep-time.org: HTTP 503 (sunucu kullanılamıyor).
- [Ö] Ron Blakey / Deep Time Maps (https://deeptimemaps.com/): Blakey paleocoğrafya haritaları (Kuzey Amerika, Batı İç Denizi, Avrupa, Arktik vb.) ticari lisanslı. Arama özetine göre harita kullanımı satın alma/lisans gerektiriyor; ücretsiz kullanım sınırlı. [Ö]
- [Ö] GSA Geologic Time Scale (https://www.geosociety.org/timescale): sayfa ana sayfa olarak zaman çizelgesi sunuyor; güncel v6.0 posteri satılık. Ücretsiz PDF'lerin çoğu eski sürüm (v5.0 gibi). Sayfa tam metni boş döndü (JS ağırlıklı); etkileşimli olup olmadığı doğrulanamadı. [Ö]
- Scotese PALEOMAP için alternatif alan adı denenmedi (bilinen tek resmi alan adı sertifika hatası veriyor).

## 2. Belirsizlik görselleştirmesi
- [Ö] Görev 'Padilla, Kay, Hullman 2021' olarak verildi; arama bu isimle 2021 çalışması döndürmedi. Bulunan en yakın ve doğrulanabilen çalışma: Correll, Hullman, Qiao, Kale, Kay, "In Pursuit of Error: A Survey of Uncertainty Visualization Evaluation", IEEE InfoVis 2018. 86 kullanıcı çalışmasını bir taksonomiyle inceliyor; değerlendirmenin çoğunlukla performans ve memnuniyet ölçülerine odaklandığını söylüyor.
  URL (özet sayfası): https://www.tableau.com/research/publications/pursuit-error-survey-uncertainty-visualization-evaluation  [Ö]
  -> Padilla 2021 çalışması için: BULUNAMADI (yazar/başlık doğrulanamadı; kullanıcıdan başlık ya da bağlantı istenmeli).
- [B] Tam makale PDF (2018-UncertaintyEvalSurvey-InfoVis.pdf, Northwestern MU Collective): https://mucollective.northwestern.edu/files/2018-UncertaintyEvalSurvey-InfoVis.pdf
  - Özet [B]: "372 evaluation paths ... 86 publications", altı karar düzeyi (davranışsal hedefler, beklenen etkiler, değerlendirme hedefleri, ölçüler, elicitation teknikleri, analiz yaklaşımları).
  - Öneri R1 [B]: "Consider Explaining As An End Goal" - kullanıcının neden öyle davrandığını sormak.
  - Öneri R2 [B]: "Use Decision Frameworks for Realism & Control" - yalnızca olasılığı okuyabilmek yetmez, karar kalitesi de ölçülmeli.
  - Öneri R3 [B]: "Account for the Ambiguity of Confidence" - 'hard-easy effect': zor işte aşırı güven, kolay işte eksik güven raporlanır.
  - Kavramlar [B]: "hypothetical choice action", "heuristic use", "prospect theory". Kaynak listesinde Hullman, Resnick, Adar 2015 "Hypothetical outcome plots outperform error bars and violin plots..." ve Kale ve ark. 2015 "animated hypothetical outcome plots" anılıyor [B, kaynakça]. Bu iki makalenin tam metni henüz alınmadı.
- [B] Hullman, Resnick, Adar 2015, "Hypothetical Outcome Plots Outperform Error Bars and Violin Plots for Inferences about Reliability of Variable Ordering", PLOS ONE 10(11), DOI 10.1371/journal.pone.0142444. Tam PDF: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0142444&type=printable
  - Özet [B]: "HOPs ... animates a finite set of individual draws. ... require relatively little background knowledge ... enables viewers to infer properties of the distribution using mental processes like counting and integration." "With HOPs, people made much more accurate judgments about plots of two and three quantities."
  - Uygulama notu: belirsizlik, tek tek 'olası sonuç' çerçeveleriyle gösterilir; sade dil için en çok öne çıkan yöntem bu.
- [Ö] Belirsizlik yardımcı notu: Padilla 2021 bulunamadı; yukarıdaki anket ve HOP, bu konudaki doğrulanmış tam metinli kaynaklar.

## 3. Küçük çoklu (small multiples) ve harita karşılaştırma arayüzleri
- [B] Gleicher, Michael, "Considerations for Visualizing Comparison" (2017 konuşma slaytları; PDF). URL: https://graphics.cs.wisc.edu/GleicherAssets/Talks/2017_10_VisComp-given.pdf
  - Karşılaştırmanın 4 soruya bölünmesi: Neyi karşılaştırıyorsun (hedefler/eylemler)? Neden zor (hedef sayısı, büyük/karmaşık hedefler, karmaşık ilişkiler)? Zorluklarla nasıl başa çıkılır (ölçekleme stratejileri)? Hangi görsel tasarım?
  - Ölçekleme stratejileri [B]: "Scan Sequentially", "Select Subset", "Summarize Somehow".
  - Karşılaştırma tasarımları [B]: "Juxtapose" (yan yana), "Superpose" (üst üste bindirme), "Explicit Encoding" (farkı doğrudan kodlama).
  - Örtük ve açık karşılaştırma [B]: "Explicit Comparisons – the system has the set of targets" / "Implicit Comparisons – the system may not know all the targets". Örneğin: kullanıcının kendisi grupları seçer ("make explicit").
- [Ö] Gleicher, Albers, Walker, Jusufi, Hansen, Roberts, "Visual Comparison for Information Visualization", Information Visualization 10(4), 289-309, 2011, DOI 10.1177/1473871611416549. Üç tasarım: juxtaposition, superposition, explicit encoding. (Makalenin tam metni henüz alınmadı; alan: https://journals.sagepub.com/doi/10.1177/1473871611416549)
- Not: arama sonucunda çıkan arXiv 2009.00192 bu makale değil; kullanılmayacak.

## 4. Kullanıcıdan seçim alma arayüzü tasarımı
- [Ö] Takagi, Hideyuki, "Interactive Evolutionary Computation: Fusion of the Capabilities of EC Optimization and Human Evaluation", Proc. IEEE 89(9), 1275-1296, 2001, DOI 10.1109/5.949485. Kapsam: yaklaşık 250 IEC çalışması; "uygunluk fonksiyonu" yerine insan değerlendirmesi. Arayüz araştırması ve insan yorgunluğu ana konu olarak öne çıkıyor. Tam metin: Kyushu Üniversitesi deposu (henüz çekilmedi). Özet kaynağı: https://gpbib.cs.ucl.ac.uk/gp-html/takagi_2001_ieee.html  [Ö]
- [ERİŞİLEMEDİ] IEEE Xplore (ieeexplore.ieee.org/document/4011444) HTTP 202; bot koruması gibi davrandı, içerik alınamadı.
- [B] Kompatscher, Shi, Varni, Weinkauf, Oulasvirta, "Interactive Groupwise Comparison for Reinforcement Learning from Human Feedback", Computer Graphics Forum (2025). arXiv: https://arxiv.org/pdf/2507.04340
  - Tasarım [B]: 'Pairwise' (A/B) arayüzü ile 'interactive groupwise' (birden çok seçenek, kullanıcı hangi karşılaştırmayı yapacağını seçer) karşılaştırıldı.
  - Sayılar [B]: 10 uzman; her oturum 7 tur x 3 dakika = 21 dakika. Aynı sürede kullanıcılar Interactive arayüzde pairwise'a göre ortalama %86.7 daha fazla tercih verdi. Ödül: 1043'e karşı 648 (küçük örneklem, istatistiksel anlamlılık iddia edilmiyor). 7/10 oturumda daha iyi politika.
  - Kullanıcı yorumları [B]: pairwise için "It is simple but not helpful in exploring the behaviours" (kontrol eksikliği); interactive için "more control over similar cases". Hata oranı interactive'de daha düşük yorumlanmış.
  - Maliyet [B]: çoklu seçenek daha fazla bilişsel çaba gerektirir (Sec. özeti). Sonuç: görev karmaşıklığı ve bilişsel yük tasarımı yönlendirmeli.
- [Ö] Qomariyah, Kazakov, Petrie 2019 (ILP, araba satışı): pairwise arayüzü liste aramasına göre tercih edildi. Tam metin alınmadı.
- [Ö] Pairwise ve A/B tasarımında tek seçim, iki kart yan yana, 'I prefer this one' düğmesi (Quadratic Metric Elicitation / Lin et al. çalışmaları) [Ö].
- [Ö] Takagi tabanlı IEC bulguları: insan yorgunluğu ana sorun [Ö]. Turnuva (tournament) tipi seçim için doğrudan kaynak BULUNAMADI.
- Oturum: A/B yerine bir turda birden çok seçenek sunmak tercih sayısını artırıyor ama bilişsel yük getiriyor; mobil için tek seferde az seçenek daha uygun olabilir (çıkarım, [Ö]).

## 5. Mobil ekranda harita karşılaştırma ve seçim kısıtları
- [Ö] Swipe (kaydırma/örtme) ile yan yana (side-by-side) karşılaştırma: 25 katılımcılı çalışmada, dört harita için yan yana daha iyi; swipe yalnızca karmaşık iki haritalık görevde öne çıktı; swipe ayarları sezgisel bulunmadı. ÇALIŞMA MASAÜSTÜ/WEB GIS üzerinde, telefon değil. Yayın künyesi: BULUNAMADI (arama özetinden doğrulanamadı).
- [Ö] MobileHCI 2016 (MFocus): büyük ekranda genel bakış, tablette bölünmüş 1, 2 veya 4 ayrıntı görünümü. Yan yana tasarımı destekliyor. URL: https://www.irit.fr/~Marcos.Serrano/pubs/2016-MobileHCI-MFocus.pdf [Ö]
- [Ö] Küçük ekran tez çalışması: tablet dokunmatik ekranı akıllı telefondan daha çok tercih edildi (telefonda kullanım kolaylığı düşük). URL: https://essay.utwente.nl/essays/93967 [Ö]
- [Ö] Telefon için doğrudan swipe-vs-yan-yana çalışması BULUNAMADI.
- Çıkarım (tasarım önerisi, [Ö] bulgularına dayanır): telefonda iki harita için kaydırma/örtme ya da dönüşümlü gösterim; dört harita için küçük çoklu (small multiples) yerine sıralı tarama ya da seçilmiş alt küme (Gleicher: Scan Sequentially / Select Subset).

## 6. Eksikler ve doğrulanamayanlar
- Scotese PALEOMAP: ERİŞİLEMEDİ (TLS).
- Blakey: sunucu 503; lisans kısıtı var (ticari).
- GSA: sayfa tam metni boş; etkileşimlilik doğrulanamadı.
- Tufte "Envisioning Information" bölüm metni alınamadı; küçük çoklu tanımı yalnızca ikincil kaynaklardan [Ö].
- Story map: arama özetleri [Ö]; akademik bir değerlendirme yok.
- Takagi 2001 tam metni alınamadı (IEEE 202).
- Gleicher 2011 makalesinin tam metni alınamadı; 2017 sunumu [B].

## Erişim günlüğü
- hullmanlab / plos (HOP PDF): 200, tam metin.
- arxiv.org/pdf/2507.04340: tam metin.
- Tufte, Takagi, Qomariyah: yalnız arama özeti.
- mucollective.northwestern.edu (anket sayfası + PDF): 200, pdftotext ile tam metin.
- geosociety.org/timescale: tam metin boş (0 karakter).
- deeptimemaps.com: kısmi metin alındı (arama özetiyle birlikte).
- pubs.usgs.gov ana sayfa ve alt sayfalar: 200, curl + oku.py ile metin alındı.
- scotese.com: TLS sertifika uyuşmazlığı; atlatılmadı.
- deep-time.org: 503.
- ieeexplore.ieee.org (Takagi 2001): HTTP 202, içerik alınamadı.
- graphics.cs.wisc.edu Gleicher 2017 sunumu: 200, pdftotext ile metne çevrildi.
- design.kyushu-u.ac.jp indirilebilir dosya sayfası: bağlantı bulunamadı.
