# B. Hipsometri, Hack yasası, Horton oranları, drenaj yoğunluğu, eğim-alan ilişkisi

Durum: Tarama tamamlandı (kaynakların bir kısmına erişim engelli). Bulgular aşağıda.

Etiketler: [B] tam metin okundu; [B-öz] yalnızca özet/kayıt sayfası okundu; [Ö] arama sonucu özeti (birincil metin okunmadı); BULUNAMADI: bu tarama turunda değer/kaynak bulunamadı; ERİŞİLEMEDİ: kaynağa erişilemedi.

## Ağ durumu (özet)

- WebFetch: pubs.usgs.gov, pure.psu.edu, www.scribd.com, en.wikipedia.org için DNS hatası (ENOTFOUND).
- curl -sSL (proxy üzerinden) ile pubs.usgs.gov, en.wikipedia.org, pure.psu.edu, esurf.copernicus.org, pdodds.w3.uvm.edu, cukerala.ac.in 200 ile açıldı; metin için oku.py (trafilatura) ve pdftotext kullanıldı.
- ERİŞİLEMEDİ (bot koruması, 403 / "Just a moment"): doi.org üzerinden AGU/GSA yayınları (Rigon 1996 doi:10.1029/96WR02397; Strahler 1952 doi:10.1130/0016-7606(1952)63[1117:HAAOET]2.0.CO;2; Pike & Wilson 1971 doi:10.1130/0016-7606(1971)82[1079:ERHIAG]2.0.CO;2); core.ac.uk tezi (Wobus 2005, core.ac.uk/download/4399269.pdf); Columbia Academic Commons (Melton 1957).
- ERİŞİLEMEDİ (TLS): escholarship.org (Harrison ve diğ. 1983 tam metin) sertifika zinciri hatası verdi; atlatılmadı.
- ERİŞİLEMEDİ (erişim reddi): repository.library.noaa.gov (ETOPO1 NGDC-24 PDF) "Access Denied" HTML döndü.
- Not: Görev notundaki iki Wobus/Kirby/ETOPO dosyası için yalnızca özet ve kayıt sayfaları elde edildi.

## 1. Hipsometrik integral (HI)

- [Ö] Strahler 1952, "Hypsometric (area-altitude) analysis of erosional topography", GSA Bull. 63(11), 1117-1142, doi:10.1130/0016-7606(1952)63[1117:HAAOET]2.0.CO;2. Birincil metin ERİŞİLEMEDİ. Arama özeti: youth/mature/old evresi çerçevesi var; mature ve old eğrilerin monadnock yoksa aynı görünmesi nedeniyle terminoloji "inequilibrium / equilibrium / monadnock" olarak önerilmiş. Etiket: [Ö].
- [Ö] Strahler 1952'nin youth > 0.6, mature 0.35-0.6, old < 0.35 eşikleri: arama ile DOĞRULANAMADI. Bu eşikler yaygın olarak ikincil kaynaklarda tekrar edilir; birincil kaynakla teyit edilmedi. Etiket: BULUNAMADI (birincil).
- [B-öz] Wikipedia Hypsometry (https://en.wikipedia.org/wiki/Hypsometry, curl ile alındı): Strahler 1952'yi kaynak gösterir ve üç parametreli eğri önerdiğini yazar; HI'yi "summary measure of the shape of the hypsometric curve" olarak tanımlar. Sayısal HI aralığı ve evre eşikleri vermez. Etiket: [B-öz].
- [Ö] Pike & Wilson 1971, Bull. GSA 82, 1079-1084: HI ile elevasyon-rölyef oranının matematiksel olarak özdeş olduğunu gösterir (arama özeti). Evre eşikleri aramada BULUNAMADI. Etiket: [Ö].
- [Ö] İkincil: Chorley & Kennedy (1971) HI ≤ 0.60 olduğunda integral kendini stabilize eder; Carson & Kirkby (1972) olgunlukta integralin ~%50 civarına yerleştiğini belirtir (arama özeti, birincil değil). Etiket: [Ö].
- [B] Uygulama örneği (ikincil): Kerala, Meenachil havzası (EREM 73/4, 2017, s. 41-57, https://cukerala.ac.in/cukpdfs/IQAC/3.4.5/3.4.5.GEO.027.pdf): alt havzaların çoğu Ea >= 0.30 "mature", Ea < 0.30 "old" olarak sınıflanır. Bu, bir uygulamanın kullandığı eşiktir; Strahler'in eşiği değildir. Etiket: [B] (uygulama, birincil değil).

## 2. Dünya karasının hipsometrisi

- [Ö] Ortalama ve medyan değerler için sayılar bulunamadı; bulunan değerler kaynaklarla uyuşmuyor:
  - arXiv 1810.08658 ("Estimating Atmospheric Mass Using Air Density", https://arxiv.org/pdf/1810.08658) tarihsel ortalama kara yüksekliklerini listeler: 700 m (1895), 840 m (1921), 871 m (1931), 797 m (2012). Yani 840 m, Cogley 1984 ile değil 1921 tahminiyle ilişkilendirilmiş; bu makalede medyan değerleri 466 m (Kossinna 1931) ve 420.5 m (2012). Etiket: [Ö].
  - PMC (30 arc-saniye yükseklik çalışması, arama özeti): kara alanı medyanı 408 m. Etiket: [Ö].
  - "Medyan 377 m": hiçbir kaynakta bulunamadı. Etiket: BULUNAMADI.
- Cogley 1984: arama ile kaynak bulunamadı (dergi/cilt/sayfa doğrulanamadı). Etiket: BULUNAMADI.
- Harrison, Miskell, Brass, Saltzman, Sloan 1983, "Continental hypsography", Tectonics 2(4), 357-377 (arama özeti, Ö): açık erişim eScholarship kopyası TLS hatası nedeniyle ERİŞİLEMEDİ. 840 m / 377 m değerleri bu makalede doğrulanamadı. Etiket: [Ö] + ERİŞİLEMEDİ.
- Amante & Eakins 2009, ETOPO1, NOAA Tech. Memo NESDIS NGDC-24 (DOI 10.7289/V5C8276M; arama özeti, Ö). PDF ERİŞİM REDDİ; ortalama kara yüksekliği istatistiği içerip içermediği doğrulanamadı. Etiket: [Ö] + ERİŞİLEMEDİ.
- Eakins ve diğ. 2022, ETOPO 2022 (15 arc-saniye; DOI 10.25921/fd45-gt74; arama özeti, Ö). Kara ortalama yüksekliği bu kayıtta bulunamadı. Etiket: [Ö], BULUNAMADI (istatistik).

## 3. Hack yasası

- [B] Hack 1957, USGS PP 294-B, "Studies of longitudinal stream profiles in Virginia and Maryland", s. 45-97, doi:10.3133/pp294B. URL: https://pubs.usgs.gov/pp/0294b/report.pdf. Denklem (3): L = 1.4 A^0.6 (L mil, A mil²). Metin (İng.): "The coefficient of the equation relating length and area averages around 1.4 but ranges between 1 and 2.5"; kumtaşı alanlarında katsayı ~2.0. Ölçüm aralığı: 0.12-375 mil². Etiket: [B].
- [B] Hack 1957, Hack'in 0.6 üssünü havza şeklinin değişimiyle açıklar: şekil sabit kalsaydı üs 0.5 olurdu (W_a = A/L türetmesi). Etiket: [B].
- [B-öz] Wikipedia Hack's law (https://en.wikipedia.org/wiki/Hack%27s_law, curl ile alındı): "the exponent h is slightly less than 0.6 in most basins", büyük havzalarda (>8000 mil²) hafifçe azalır. Etiket: [B-öz].
- [Ö] Rigon ve diğ. 1996, "On Hack's law", WRR 32(11), 3367-3374 (doi:10.1029/96WR02397, ERİŞİLEMEDİ). Arama özeti: DEM ile deneysel test; Hack üssü, uzama ve fraktal karakter ilişkisi; ölçek argümanlarıyla açıklama. Etiket: [Ö].
- Ayrım: Willemin 2000, "Hack's law: sinuosity, convexity, elongation", WRR 36(11), 3365-3374 (doi:10.1029/2000WR900229). Rigon 1996 ile karıştırılmamalı. Etiket: [B-öz] (Wikipedia kaynakça).

## 4. Horton oranları

- [B] Horton 1945, "Erosional development of streams and their drainage basins", GSA Bull. 56, 275-370 (kopya: https://pdodds.w3.uvm.edu/research/papers/others/1945/horton1945a.pdf, pdftotext ile okundu; OCR bozuk olabilir).
  - Bifürkasyon oranı R_B: "ranges from about 2 for flat or rolling drainage basins up to 3 or 4 for mountainous or highly dissected drainage basins". Etiket: [B].
  - Uzunluk oranı R_L: "range from about 2 to about 3; the average is 2.32". Etiket: [B].
  - Alan oranı R_A: Horton metninde bulunamadı. Etiket: BULUNAMADI.
- Yorum: Görev notundaki aralıklar (R_B 3-5; R_L 1.5-3.5; R_A 3-6) Horton 1945'in kendi değerleriyle tam örtüşmüyor (R_B üst sınırı 4). Görev notundaki aralıklar Strahler 1957 / Schumm 1956'dan geliyor olabilir; bu iki makale doğrulanamadı.
- [Ö] Strahler 1957 ve Schumm 1956 (GSA Bull. 67, 597-646, doi:10.1130/0016-7606(1956)67[597:EODSAS]2.0.CO;2): kayıt doğrulandı; tam metin açık değil. Arama özeti: Schumm Perth Amboy badlands'ta beşinci dereceli sistemi inceler, hipsometrik analizle maksimum erozyon noktasının kanal yukarısına göç ettiğini bildirir. R_B/R_L/R_A değerleri BULUNAMADI. Etiket: [Ö].

## 5. Drenaj yoğunluğu ve eşik alanı

- [Ö] Melton 1957, "An analysis of the relations among elements of climate, surface properties, and geomorphology", Columbia Univ., ONR Tech. Rep. 11, proje NR 389-042. Tam metin ERİŞİLEMEDİ (Columbia bot koruması). Arama özeti: drenaj yoğunluğu ile toprak ve iklim ilişkisi. Değer aralığı BULUNAMADI. Etiket: [Ö].
- [B] Horton 1945: drenaj yoğunluğu / eşik alanı için sayısal kriter bu metinde ayrıca çıkarılmadı (metinde "drainage density" tanımlanır ama bu turda sayısal aralık aranmadı). Etiket: BULUNAMADI (bu turda).
- Horton 1932 (Trans. AGU 13): doi:10.1029/TR013i001p00350 DOI yanıtı 403 verdi; metin ERİŞİLEMEDİ. Etiket: ERİŞİLEMEDİ.
- Eşik alanı (hillslope-channel geçişi): Wobus ve diğ. 2006 özetinde hillslope-channel geçişi tartışması BULUNAMADI; yalnızca "channel-based" yaklaşımın tektonik sinyali taşıdığı belirtilir. Etiket: BULUNAMADI.

## 6. Eğim-alan yasası

- [B-öz] Kirby & Whipple 2012, "Expression of active tectonics in erosional landscapes", J. Struct. Geol. 44, 54-75, doi:10.1016/j.jsg.2012.07.009. Kaynak: https://pure.psu.edu/en/publications/expression-of-active-tectonics-in-erosional-landscapes/ (kayıt sayfası, özet okundu). Tür: "Review article". Özet (İng.): "existing data support theoretical expectations of positive, monotonic relationships between channel steepness index, a measure of channel gradient normalized for downstream increases in drainage area, and erosion rate at equilibrium". Etiket: [B-öz]. Tam metin açık değil.
- Kirby & Whipple 2012'de θ_ref = 0.45 veya "θ = 0.45 ± 0.2" ifadesi: BULUNAMADI (özet ve kayıt sayfasında yok). Arama özetinde "0.4 < θ < 0.6" aralığı Kirby & Whipple'a atfedildi ama tam metinle doğrulanmadı. Etiket: [Ö] (ikincil), BULUNAMADI (birincil).
- [B] Mudd, Clubb, Gailleton, Hurst 2018, "How concave are river channels?", Earth Surf. Dynam. 6, 505-523, doi:10.5194/esurf-6-505-2018. Tam metin: https://esurf.copernicus.org/articles/6/505/2018/esurf-6-505-2018.pdf (pdftotext ile okundu). Denklem (1): S = k_s A^(-θ), θ "concavity index", k_s "steepness index". Referans konkavitesi θ_ref ile normalize edilmiş k_sn tanımlanır (denklem 6, Wobus ve diğ. 2006a'ya atfen). Etiket: [B].
  - Bu makalede "θ ≈ 0.45" değeri, belirli bir havza için en olası konkavite olarak geçer (bootstrap/disorder yöntemleri); Loess Plateau çalışmasında referans konkavite 0.4-0.5 önerilir. Bu, Kirby & Whipple'ın 0.45 değeri değildir. "±0.2" ifadesi bu makalede BULUNAMADI. Etiket: [B].
  - Ayrıca bu makale tüm kanalların tek bir θ_ref ile normalize edilmesinin (k_sn) sonuçları değiştirdiğini gösterir; yani θ_ref seçimi kritiktir. Etiket: [B].
- [Ö] Wobus, Whipple, Kirby, Snyder, Johnson, Spyropolou, Crosby, Sheehan 2006, "Tectonics from topography: procedures, promise, and pitfalls", GSA SP 398, s. 55-74, doi:10.1130/2006.2398(04). Metin ERİŞİLEMEDİ (Scribd ve core.ac.uk tezi erişim hatası/bot koruması). Arama özeti: profil eğrisi indeksleri; eğim-alan güç yasası; kırılma (scaling break) tektonik sınıra karşılık gelebilir. Eşik alanı ve θ_ref sayıları BULUNAMADI. Etiket: [Ö].

## Açık sorular / sonraki adımlar

- Strahler 1952 ve Pike & Wilson 1971 evre eşikleri için birincil metin: GSA erişimi (bot koruması) gerekli. Mevcut yalnızca ikincil doğrulama.
- Rigon 1996 tam metin: AGU erişimi gerekli.
- Kirby & Whipple 2012 tam metin: θ_ref ve "0.45 ± 0.2" ifadesi için gerekli.
- Harrison ve diğ. 1983 (840 m / 377 m): escholarship TLS hatası; sertifika sorunu çözülmeden doğrulanamaz.
- ETOPO1 NGDC-24: repository.library.noaa.gov erişim reddi; ortalama kara istatistiği doğrulanamadı.
- Görev notundaki R_B 3-5, R_L 1.5-3.5, R_A 3-6 aralıkları ve "0.45 ± 0.2" ifadesi, bu turda incelenen birincil metinlerde doğrulanamadı.
- Cogley 1984: kaynak bulunamadı.
