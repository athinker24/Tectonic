# 16. Kurgusal istisnaların doğal karıştırılması

Araştırma tarihi: 12 Kasım 2026. Belge iki Haiku kolunun sentezidir (A arazi düzenleme ve yumuşak geçiş, B istisna defteri ve çelişki gösterimi); sentezi ben yazdım. Ham notlar `arastirma/notlar/16/` içinde. Etiketler: **[B]** tam metin okundu, **[B-öz]** özet, sayfa metni ya da seçilmiş bölümler okundu, **[Ö]** arama özeti, doğrulanamadı, **[H]** bizim çıkarımımız, **[Y]** bulunamadı.

Dürüst durum: B kolunda hiçbir makalenin tam metni okunmadı (yalnızca özet düzeyi). A kolunda Schott 2023, Guérin 2022, Cordonnier 2017, Hnaidi 2010 ve Pérez 2003 okundu. Bu konu fiziksel sayı değil yöntem konusu; varsayılanlar tasarım önerisidir.

## Kısa sonuç

**1. Kullanıcının tarif ettiği mekanizma (bir bölgede belirli yükseklik, belli bir yerde dağ sırası, yumuşak karışım) Schott ve diğerlerinin 2023 makalesiyle örtüşüyor.** "Large-scale terrain authoring through interactive erosion simulation" (ACM TOG, HAL hal-04049125) tam metinde "Uplift Tree" (yükselme ağacı), "Procedural Brushes" ve PI (oransal-integral) tabanlı yükseklik kısıtı içeriyor [B]. Arazi yükseklik alanında değil yükselme alanında düzenleniyor; hidrolojik tutarlılığı korumak için bu tercih edilmiş [B].

**2. Sert yükseklik istekleri için PI düzeltmesi var.** Schott 2023, Eş. 10: ũ(k+1) = Kp·e(k) + Ki·Σe(j) + Kd·(e(k) − e(k−1)); Kp = 0,01, Ki = 0,001, Kd = 0,01, her 10 iterasyonda güncelleme [B]. Yani hedef yüksekliğe ulaşana kadar yükselme alanı döngü içinde düzeltiliyor.

**3. Yükseklik alanında doğrudan karıştırma gerçekçi olmayan sonuç verebilir.** Schott: yükselme alanında enterpolasyon ya da warp tercih edilir [B]. Gradyan alanında Poisson karıştırma (Pérez 2003) ve Guérin 2022'nin gradyan arazi düzenlemesi alternatif [B].

**4. Çelişki tespiti bilinen kısıt çözme yöntemleriyle yapılabilir; hiçbir çelişkiyi sessizce düzeltmemek ilkesi mevcut yöntemlerle uygulanabilir.** Önce minimal çelişki kümesi (MUS, IIS) bulunur ve gösterilir, sonra Junker (2004) tercih tabanlı gevşetme önerileri sunulur, hiçbiri kullanıcı onayı olmadan uygulanmaz [B-öz ve H].

## 1. Kısıtlı arazi düzenleme

| Yöntem | Ne yapar | Etiket |
|---|---|---|
| Schott ve diğerleri 2023, ACM TOG ("Large-scale terrain authoring through interactive erosion simulation") | Yükselme ağacı, prosedürel fırçalar; yükselme alanı u = u0 + ũ; PI düzeltmesi yükseklik hedefini tutar | [B] |
| Guérin ve diğerleri 2022, CGF 41(2) ("Gradient Terrain Authoring") | Eğim alanı üzerinden Poisson yeniden yapılandırma; çakışmada sert yükseklik kısıtı, yumuşak gradyan kısıtından önce gelir | [B] |
| Cordonnier ve diğerleri 2017 ("Authoring landscapes by combining ecosystem and terrain erosion simulation") | Ekosistem ve arazi aşınmasının birleşik simülasyonu | [B] |
| Hnaidi ve diğerleri 2010, "Feature based terrain generation using diffusion equation" | Özellik tabanlı arazi üretimi, difüzyon denklemi | [B]; saniye düzeyinde süre metinde yok |
| Pérez ve diğerleri 2003, "Poisson Image Editing" | Gradyan alanında karıştırma; Laplace piramidi hızlandırma olarak geçiyor | [B]; ayrı bir kenar yumuşatma (feathering) kaynağı bulunamadı |
| Génevaux 2013, Zhou 2007, WorldBrush 2015 | | yalnızca kısmen okundu |
| Tasse ve diğerleri 2014, "Feature-based terrain editing from complex sketches" | | [Ö] (core.ac.uk Cloudflare bot koruması, aşılmadı) |

Ters erozyon ve ters prosedürel modelleme: "Cordonnier inverse erosion" adlı makale bulunamadı [Y]; Talton 2011 arazi içermiyor (ağaç, şehir, bina). İlgili çalışmalar: Unerosion (Yang 2024, CGF), adjoint tabanlı Petit ve diğerleri (2025), Wasserstein ters modelleme (Morris 2023) [Ö].

Kaynak eşleşmesi düzeltmesi: arXiv 2304.09626 "Schott 2023" değil, StyleDEM (Perche, Peytavie, Benes, Galin, Guérin 2023). Gerçek Schott 2023 makalesi HAL'da (hal-04049125) tam metin olarak okundu [B].

**Hesap süreleri (kıyaslanamaz; donanımlar ve birimler farklı).** Schott 2023, Tablo 1, GTX 1080 Ti: 512 × 512 toplam 1,3 s; 1024 × 1024 toplam 9,1 s [B]. Cordonnier 2017, Tablo 1: n = 1024 için toplam 38 s [B]. Guérin 2022: 1024 × 1024 gerçek zamanlı [B]. Hepsi GPU'da; aracın Python / CPU ortamında (13. belge: 1 milyon düğüm adım başına yaklaşık 0,7 s) aynı süreler beklenmemeli [H].

## 2. Aracın kısıt gösterimi: yumuşak karışım

- **Sert yükseklik isteği** (bir bölgede belirli yükseklik): Schott PI düzeltmesiyle yükselme alanında hedef tutturulur [B]. Çakışırsa Guérin 2022 önceliği: sert yükseklik kısıtı, yumuşak gradyan kısıtından önce gelir [B].
- **Yumuşak istek** (bir yerde dağ sırası olsun): yükselme alanında fırça bileşimi, düşmeye bağlı karıştırma [B ve H].
- **Çevreye geçiş:** yükselme alanında interpolasyon ya da warp, hidrolojiyi bozmaz (Schott) [B]. Mesafeye bağlı sönümleme (kenar yumuşatma) için ayrı kaynak bulunamadı; bu bir tasarım seçimidir [H].
- **Kıyı sabit kısıtı ile birleşme (13. belge):** istisna bölgesinde yükselme kıyıda sıfıra gitmeli; aksi halde kıyıda basamak oluşur [H].

## 3. Çelişkilerin gösterilmesi ve istisna defteri

| Konu | Yöntem | Etiket |
|---|---|---|
| En küçük çelişki kümesi | MUS / IIS: tatmin edilemez küme, tek kısıt çıkarılınca tatmin edilebilir; birden çok MUS olabilir. Silme filtresi yaygın | arXiv 1708.00400 [B-öz]; Liffiton CAMUS [Ö] |
| Tercih tabanlı gevşetme | Junker 2004, "QuickXplain: Preferred Explanations and Relaxations for Over-Constrained Problems", AAAI 2004, 167 ile 172: kullanıcı tercihine dayalı tercih edilen açıklama ve gevşetme; böl-ve-yönet ile hızlandırma | [B-öz] |
| Karşıolgusal gevşetme | Gupta, Genc, O'Sullivan (ICTAI 2024): kısıt atmak yerine hangi değişikliğin çelişkiyi çözeceğini önerir | arXiv 2204.03429 [Ö] |
| Konfigüratör teşhisi | Felfernig ve diğerleri: çelişki tabanlı teşhis; PERSDIAG (2011): tutarsız kullanıcı gereksinimleri için kabul edilebilir teşhisler | [Ö] |
| Açıklama ilkesi | Miller 2019, "Explanation in AI: Insights from the Social Sciences": açıklamalar karşıtlıktır ("neden P, Q yerine?") | arXiv 1706.07269 [B-öz] |
| Karar kaydı | Architecture Decision Records (tek karar ve gerekçesi, ödünleşimler; proje ADR toplamı "decision log") | adr.github.io [B-öz] |
| İzlenebilirlik | W3C PROV-DM (30 Nisan 2013): entity / activity / agent; "derivation" (WasDerivedFrom) ve revizyon | [B-öz] |
| Jeolojik ihlal ölçüsü | Clennett ve diğerleri 2023, Sci. Rep. 13:10191 (doi 10.1038/s41598-023-37117-w): slab çekişi, sırt itişi, manto sürtünmesi; artık kuvvet / tork = dinamik denge için eksik kuvvetler; 60 ile 90 milyon yıl önce Pasifik plakasında artık kuvvet toplam sürüş kuvvetinin iki katı | [B-öz] |
| Tektonik kurallar modeli | Tetley 2019; Müller 2022 genişletme: hotspot uyumsuzluğu, hendek göçü, net dönme, kıta hızı kuralları (atıf tutarsız: "2024 JGR" ve "2025, cilt 130") | [Ö] |

Bulunamayan / doğrulanamayan: Jannach ve Liegl 2006 (conflict-directed relaxation); "audit trail" için birincil kaynak aranmadı; GPlates'te yerleşik "kural ihlali" raporu ya da paleocoğrafi uyumsuzluk metriği [Y].

**Öneri [H] (kaynaklı bir kural değil).** Her kullanıcı isteği bir kısıt olarak kaydedilir (defter satırı: kim, ne, ne zaman, neden, hangi etkinliklere bağlı). Çözücü başarısızsa: (1) MUS bulunur ve kullanıcıya olduğu gibi gösterilir; (2) Junker biçiminde "hangi isteği ne kadar gevşetirsen çözülür" seçenekleri sunulur; (3) hiçbiri otomatik uygulanmaz; (4) kullanıcı seçimi yeni bir defter satırı olarak kaydedilir ve türetme ilişkisi (PROV benzeri) saklanır. Bu, "çelişki sessizce düzeltilmeyecek" kuralını doğrudan karşılıyor.

## 4. Aracın varsayılan değerleri

| Parametre | Değer | Etiket |
|---|---|---|
| İstek temsili | yükselme alanında fırça / kısıt (Uplift Tree benzeri) | [B] |
| Yükseklik hedefi | PI düzeltmesi: Kp = 0,01, Ki = 0,001, Kd = 0,01; her 10 iterasyonda güncelleme | [B] |
| Çakışma önceliği | sert yükseklik kısıtı > yumuşak gradyan kısıtı | [B] |
| Geçiş | yükselme alanında enterpolasyon / warp; yükseklik alanında doğrudan karıştırma yok | [B] |
| Çelişki bulma | MUS / deletion filter | [B-öz ve Ö] |
| Gevşetme önerisi | Junker tercih tabanlı; hiçbiri otomatik uygulanmaz | [B-öz] |
| Açıklama biçimi | karşıtlık: "neden P, Q yerine?" | [B-öz] |
| Defter | ADR + PROV-DM türetme ilişkisi | [B-öz] |
| Kıyı | istisna yükselmesi kıyıda sıfıra gider | [H] |

## 5. Kaynaklar arası çelişkiler

- Tectonic Rules Model atfı: "2024 JGR" ile "2025, cilt 130".
- Hesap süreleri üç makalede farklı birim ve donanımda; doğrudan karşılaştırılamaz.
- Schott 2023 arXiv numarası yanlış makaleye gidiyor (StyleDEM).

## 6. Bulunamayanlar ve doğrulanamayanlar

- Tasse 2014 tam metni (core.ac.uk Cloudflare, aşılmadı); Hnaidi 2010 süre; Génevaux 2013, Zhou 2007, WorldBrush 2015 kısmen okundu; h-schott.github.io DNS hatası, HAL ön baskısı kullanıldı.
- Junker 2004 ve Felfernig makalelerinin tam metni; Jannach ve Liegl 2006; audit trail kaynağı; GPlates misfit metriği; Tectonic Rules Model yayımlanmış atfı.
- "Cordonnier inverse erosion" ve arazi için ters prosedürel modelleme (Talton 2011 arazi içermiyor).
- Kenar yumuşatma (feathering) için ayrı kaynak.

## 7. Promptumdaki hatalar (düzeltildi)

- "Schott 2023" arXiv 2304.09626 yanlış; o StyleDEM'dir. Schott 2023'ün kaynağı HAL hal-04049125.
- "Cordonnier inverse erosion" adlı makale yok.
- "Hnaidi 2010" ve "Zhou 2007" başlıkları doğrulandı ama süre metinde yok.
- "Laplace pyramid" Pérez 2003'te hızlandırma olarak geçiyor; ayrı feathering kaynağı yok.

## Başlıca kaynaklar

- Schott ve diğerleri 2023: HAL hal-04049125
- Guérin ve diğerleri 2022: people.cs.uct.ac.za/~Jgain/wp-content/papercite-data/pdf/guerin2022.pdf
- Cordonnier ve diğerleri 2017: cs.purdue.edu/homes/bbenes/papers/Cordonnier17ToG.pdf
- Hnaidi 2010: perso.liris.cnrs.fr/egalin/Articles/2010-terrain.pdf
- Pérez 2003: cs.princeton.edu/.../perez03.pdf
- Junker 2004: https://mlanthology.org/aaai/2004/junker2004aaai-quickxplain/
- Miller 2019: https://arxiv.org/abs/1706.07269
- ADR: https://adr.github.io/ ; W3C PROV-DM: https://www.w3.org/TR/prov-dm/
- Clennett ve diğerleri 2023: https://pmc.ncbi.nlm.nih.gov/articles/PMC10290141
- Tam liste ve her bilginin kaynağı `arastirma/notlar/16/` içinde.
