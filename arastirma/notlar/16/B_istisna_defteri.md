# B: İstisna (Conflict) Defteri - Kısıt Tutarlılığı ve Çelişki Açıklaması

Durum: TAMAMLANDI (ilk tur). Etiketler: [B] tam metin okundu; [B-öz] sayfa/özet metni okundu (tam makale değil); [Ö] yalnızca arama özeti.

Not: Bu turda hiçbir makalenin tam PDF metni okunmadı. En güçlü kanıtlar [B-öz] düzeyinde (özet ya da sayfa metni, bazıları grep ile seçilmiş bölümler). Junker 2004 ve Felfernig/Jannach makalelerinin tam metni sonraki turda okunmalı.

Amaç: Kullanıcı isteklerinin (kısıtlarının) tutarlılığını denetlemek; çelişkileri sessizce düzeltmeden göstermek için yöntem bulmak.

## 1. Kısıt tatmin / çelişki çıkarımı (MUS, IIS, gevşetme)

- Junker, U. (2004). "QUICKXPLAIN: Preferred Explanations and Relaxations for Over-Constrained Problems." AAAI 2004, s. 167-172. [B-öz]
  - Özet: aşırı kısıtlı problemlerde hem çok sayıda çelişki (conflict/explanation) hem de çok sayıda gevşetme (relaxation) olabilir. Kullanıcı tercihlerine (kısıtlar arası öncelik) dayalı "tercih edilen açıklama" ve "tercih edilen gevşetme" tanımlanır. Hesap, CP, SAT veya DL çözücüleriyle çalışan genel bir yöntemle yapılır; böl-ve-yönet stratejisiyle hızlandırılır.
  - Yöntem (ikincil kaynak, [Ö]): tercih edilen çelişki için en tercihli kısıtlar eklenip hata oluşana kadar ilerlenir, sonra en az tercihli olanlar çıkarılır. Gevşetme bunun ikilisi olarak başlar.
  - Kaynak: https://mlanthology.org/aaai/2004/junker2004aaai-quickxplain/ (özet ve BibTeX, [B-öz])
  - Değer: Metin "configuration applications" ve bir endüstriyel CP aracının açıklama olanağının temeli olduğunu belirtir.
- MUS / IIS kavramı ve deletion filter (Liffiton ve diğerleri; Bendík ve diğerleri). [Ö]
  - Tanım (arama özeti): MUS, çıkarıldığında tatmin edilebilir hâle gelen ama kendisi tatmin edilemez olan küme. OR literatüründe bunun karşılığı IIS (Irreducible Inconsistent Subsystem).
  - Algoritma: "deletion filter" (shrink); her kısıt sırayla çıkarılıp tatmin edilemezlik korunuyorsa kalıcı olarak atılır. Bir sistemde birden çok MUS olabilir.
  - Kaynak: https://arxiv.org/abs/1708.00400 (Bendík ve diğerleri, "Recursive Online Enumeration of All Minimal Unsatisfiable Subsets", [B-öz]); tam MUS/IIS tartışması için https://sun.iwu.edu/~mliffito/publications/jar_liffiton_CAMUS.pdf [Ö]
  - Özet metin: MUS'ları tanımlamak için tatmin testleri gerekir; test karmaşıklığı özellikle temporal mantık, model checking veya SMT'de çok yüksek olabilir. Tüm MUS'ları sıralamak genelde üstel sayıda olabileceği için zordur.
- MaxSAT / minimal düzeltme kümesi (MCS): [Ö] "computing minimal correction subset" aramasında ilgili literatür bulundu; ayrıntı alınmadı.
  - Kaynak: https://aitopics.org/tag/computing minimal correction subset [Ö]
- Gevşetme (relaxation) için Jannach ve Liegl 2006 önerisi (conflict-directed relaxation, içerik tabanlı öneri): [BULUNAMADI] (kaynak doğrulanamadı; aramada yalnızca bir kaynakça satırı olarak görüldü).
- Counterfactual açıklama, kısıt gevşetme yoluyla (Gupta, Genc, O'Sullivan; ICTAI 2024; arXiv 2022, 2204.03429): [Ö]
  - Düşünce: kısıtları tamamen atmak yerine kullanıcının kısıtlarında hangi değişikliğin çelişkiyi çözeceğini önermek daha bilgilendirici.
  - Kaynak: https://arxiv.org/abs/2204.03429 ; https://cora.ucc.ie/items/80af6e2d-83d6-4eff-ae14-e513a1982d39 [Ö]

## 2. Kullanıcıya çelişki açıklaması (konfigüratörler, XAI)

- Felfernig, Friedrich, Jannach, Stumptner: "Consistency-based diagnosis of configuration knowledge bases" (2004 civarı). [Ö]
  - Özet (arama): konfigürasyon bilgi tabanlarının teşhisi için tanım ve çelişki (conflict) tabanlı algoritma; prototip ticari kısıt-tabanlı konfigüratör kütüphaneleriyle etkileşimli hata ayıklama süresinde çalışıyor.
  - Kaynak: https://digital.library.adelaide.edu.au/items/d6b059e5-632b-4702-aa73-d2fb832fb581 [Ö]
- Hierarchical Diagnosis (Felfernig/Jannach): teşhis verimliliği çelişki kümelerinin minimalliğine bağlı; hiyerarşik yapı ile farklı ayrıntı düzeylerinde teşhis. [Ö]
  - Kaynak: https://web-ainf.aau.at/pub/jannach/files/Hierarchical_Diagnosis.pdf
- PERSDIAG (Felfernig ve diğerleri, 2011): tutarsız kullanıcı gereksinimleri için kişiselleştirilmiş teşhisler; kullanıcının kabul edeceği teşhisler için en iyi-ilk arama. [Ö]
  - Kaynak: https://ase.ist.tugraz.at/wp-content/uploads/sites/34/2023/05/2011-Felfernig-Personalized-diagnoses-for-inconsistent-user-requirements.pdf
- Açıklanabilir yapay zeka (XAI) ilkeleri: Miller, T. (2019). "Explanation in Artificial Intelligence: Insights from the Social Sciences." Artificial Intelligence. [B-öz]
  - Özet metin (arXiv 1706.07269): açıklamalar karşıtlık (contrastive) içerir; insanlar "neden P?" sorusunu çoğunlukla "neden Q yerine P?" olarak sorar. Sistemlerin karşıtlık açıklaması üretmesi, kullanıcının önyargılarını hesaba katması ve sosyal etkileşim yapabilmesi önerilir.
  - Kaynak: https://arxiv.org/abs/1706.07269
  - Uygulama notu: "Kullanıcının isteği neden çelişiyor?" yerine "Hangi iki istek birlikte olamaz?" biçiminde karşıtlık sunmak bu ilkeye uyar. Yorum: bu bir çıkarım, kaynağın doğrudan söylediği değil.
- Etkileşimli gevşetme (interactive constraint relaxation) ilkesi: [Ö] Junker'in tercih tabanlı yaklaşımı (yukarıda) ve counterfactual gevşetme çalışmaları bu yönde; ayrı bir "etkileşimli gevşetme" standardı bulunamadı.

## 3. Değişiklik defteri ve izlenebilirlik

- Architecture Decision Records (ADR): Michael Nygard 2011 blog yazısı ("Documenting Architecture Decisions") ile popülerleşti. [B-öz]
  - Tanım (adr.github.io): bir ADR tek bir mimari kararı ve gerekçesini kaydeder; ödünleşimler (trade-offs) ve sonuçlar da anlaşılır hâle gelir. Projede tutulan ADR'lerin toplamı "decision log" (karar defteri) olarak adlandırılır.
  - Kaynak: https://adr.github.io/ ; Zdun ve diğerleri "Sustainable Architectural Decisions" tabanlı Y-statement biçimi. [B-öz]
- W3C PROV-DM (Moreau, Missier ve diğerleri; W3C Recommendation, 30 Nisan 2013). [B-öz]
  - Tanım (spec metni): provenance, bir veri veya nesnenin üretiminde yer alan varlıklar (entity), etkinlikler (activity) ve kişiler (agent) hakkında bilgi; kalite ve güvenilirlik değerlendirmesi için kullanılır.
  - Anahtar ilişki: türetme (derivation, WasDerivedFrom), "bir varlığın başka bir varlıktan dönüşümü, güncellenmesi ya da yeni bir varlığın temel alınarak oluşturulması". Revizyon bir türetme türüdür.
  - Kısıt tarafı: değişebilen varlıklar için ayrı bir tamamlayıcı spec, PROV-CONSTRAINTS. [B-öz]
  - Kaynak: https://www.w3.org/TR/prov-dm/
  - Uygulama notu: bir kararın hangi önceki kararlardan türediğini izlemek için PROV-DM'deki "türetme" kavramı kullanılabilir (çıkarım).
- "Audit trail" (denetim izi): [BULUNAMADI] (bu turda ayrı bir birincil kaynak aranmadı).

## 4. Jeoloji: paleocoğrafik ihlal ve misfit ölçütleri

- Clennett, Holt, Tetley, Becker, Faccenna (2023). "Assessing plate reconstruction models using plate driving force consistency tests." Scientific Reports 13, 10191. DOI 10.1038/s41598-023-37117-w. [B-öz]
  - Yöntem: slab pull, ridge push (GPE) ve mantle drag hesaplanır; kapalı bir yeniden kurguda, kuvvetlerin dengelenmesi için gereken artık (residual) kuvvet/tork (residual torque) değerlendirilir. Araç pyGPlates üzerine kurulu.
  - Metin: "residual torque — the missing forces required for plate motion to be in dynamic equilibrium" (anlam çevirisi: plaka hareketinin dinamik dengede olması için gereken eksik kuvvetler).
  - Sayısal örnek: 60-90 Ma'da Pasifik plakasında artık kuvvet toplam sürüş kuvvetinin iki katı olarak bulunmuş; yazarlar bunu bu yeniden kurgunun fiziksel olarak tutarsız olduğunun işareti olarak yorumlamış.
  - Kaynak: https://pmc.ncbi.nlm.nih.gov/articles/PMC10290141 (tam metin, grep ile seçilmiş bölümler [B-öz])
  - Değer/ölçüt: artık tork ve artık kuvvet büyüklüğü, bir "ihlal/uyumsuzluk" göstergesi olarak kullanılabilir.
- Tectonic Rules Model (Tetley ve diğerleri 2019; Müller ve diğerleri 2022 genişletme): üç kural (hotspot misfit'in en aza indirilmesi, mutlak çukur (trench) göçünün en aza indirilmesi, net litosfer dönüşünün sınırlandırılması), sonra dördüncü kural olarak kıta hızının en aza indirilmesi. Kurallar ağırlıklandırılıp eş zamanlı uyumlandırılır. [Ö]
  - Kaynak: https://www.geologist.nl/wp-content/uploads/2024/10/2024_Wagenaar_ESSOAR.pdf (Wagenaar ve diğerleri, ESSOAR ön baskı 2024; arama snippet'i)
  - Tutarsızlık notu: arama sonuçları aynı çalışmayı bir yerde "2024 JGR: Solid Earth", başka yerde "2025, cilt 130, doi 10.1029/2024JB030430" olarak veriyor; kesin atıf yayınlanmış makaleden doğrulanmalı.
  - Eleştiri: bir Solid Earth tartışma yorumu bu "kuralların" aslında varsayım ya da jeodinamik modellerin genel sonuçları olabileceğini savunuyor. [Ö]
- GPlates: masaüstü etkileşimli yeniden kurgu aracı; GPL v2; pyGPlates ve GPlately Python paketleri. [B-öz]
  - Kaynak: https://www.gplates.org/
  - GPlates'te yerleşik bir "kural ihlali" raporu veya paleocoğrafik misfit metriği BULUNAMADI. Plaka kuralları (tectonic rules) için yerleşik bir GPlates özelliği doğrulanamadı; Clennett aracı harici (pyGPlates tabanlı) bir analiz olarak görünüyor. [Ö]
- Hotspot misfit (sıcak nokta izleri) ölçütü: bir maliyet fonksiyonuyla tanımlanır (arXiv 2603.03366 ve arama özeti). [Ö]
  - Kaynak: https://arxiv.org/html/2603.03366v1
- Continuously Closing Plates (CCP): Gurnis ve diğerleri (2012); GPlates'e dahil edilmiş; yeniden kurgu kurallarına uyumu test etmek için kullanılabilir. [Ö]
  - Kaynak: https://www.earthbyte.org/Resources/Pdf/Gurnis_cont_closing_plates_CompGeosci2012.pdf

## Kaynak günlüğü

| # | URL | Etiket | Not |
|---|-----|--------|-----|
| 1 | https://mlanthology.org/aaai/2004/junker2004aaai-quickxplain/ | B-öz | Junker 2004 özet ve BibTeX |
| 2 | https://arxiv.org/abs/1708.00400 | B-öz | MUS enumerasyonu özet |
| 3 | https://arxiv.org/abs/1706.07269 | B-öz | Miller XAI özet |
| 4 | https://www.w3.org/TR/prov-dm/ | B-öz | PROV-DM spec (grep) |
| 5 | https://adr.github.io/ | B-öz | ADR tanım ve kaynaklar |
| 6 | https://www.gplates.org/ | B-öz | GPlates tanımı |
| 7 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10290141 | B-öz | Clennett 2023 (grep) |
| 8 | https://arxiv.org/abs/2204.03429 | Ö | Counterfactual relaxation |
| 9 | https://web-ainf.aau.at/pub/jannach/files/Hierarchical_Diagnosis.pdf | Ö | Felfernig/Jannach |
| 10 | https://www.geologist.nl/wp-content/uploads/2024/10/2024_Wagenaar_ESSOAR.pdf | Ö | Tectonic Rules Model |
| 11 | https://sun.iwu.edu/~mliffito/publications/jar_liffiton_CAMUS.pdf | Ö | MUS/IIS (Liffiton) |
| 12 | Jannach & Liegl 2006 | BULUNAMADI | Doğrulanamadı |
| 13 | Audit trail birincil kaynağı | BULUNAMADI | Aranmadı |

## Sonuç

- Kısıt çelişkisi için en sağlam çerçeve: MUS/IIS (deletion filter ile hesaplanır) ve Junker'in tercih tabanlı açıklama/gevşetme yöntemi (QuickXplain). Kullanıcıya gösterim için ilk öneri: önce minimal çelişki kümesini (MUS) göster, sonra tercihe dayalı gevşetme önerileri sun, hiçbirini sessizce uygulama.
- Açıklama ilkesi: Miller'in karşıtlık ilkesi; "hangi iki istek birlikte olamaz" biçimi.
- Defter/izlenebilirlik: ADR (karar gerekçesi, ödünleşimler) ve PROV-DM'deki türetme ilişkisi, her çelişki çözümünün kaydını tutmak için uygun.
- Jeoloji karşılığı: Clennett 2023'teki artık kuvvet/tork ölçütü bir "ihlal büyüklüğü" olarak kullanılabilir; GPlates'te yerleşik bir ihlal raporu yok.
- Eksikler: Junker ve Felfernig makalelerinin tam metni okunmadı; Jannach & Liegl doğrulanamadı; Tectonic Rules Model atfı tutarsız. Sonraki turda bunlar öncelikli.
