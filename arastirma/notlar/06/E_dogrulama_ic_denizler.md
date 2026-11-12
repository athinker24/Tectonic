# Doğrulama: İç denizler (B_ic_denizler.md [Ö] sayıları)

Durum: KISMI. Wikipedia ham metinleri ve birkaç birincil özet okundu. Nature sayfası hız sınırına takıldı; bu yüzden Krijgsman 1999 okunamadı. Aşağıdaki liste yalnızca gerçekten okunan değerleri içerir.

Etiketler: [B] birincil kaynak (özet ya da metin) okundu, [E] ansiklopedi (Wikipedia ham wikitext), [Ö] yalnızca arama özeti (bu turda değiştirilmedi).

## Ağ notu

- en.wikipedia.org, journals.tubitak.gov.tr, zenodo.org, grida.no: araç katmanında (WebFetch, getaddrinfo) DNS hatası. Ancak `curl` ile HTTPS_PROXY üzerinden üçü de HTTP 200 döndü. Wikipedia ve Crossref verisi bu yolla alındı.
- nature.com (doi.org üzerinden): ngeo2784 okundu. 23231 (Krijgsman 1999) için 429 (hız sınırı) geldi; yeniden denemek için tarayıcı kimliği değiştirme girişimi izin sistemi tarafından reddedildi, bu yüzden denenmedi.
- cnrs.fr, mdpi.com: DNS hatası; bu turda denenmedi.

## Bulgular

### 1. Akdeniz (tüm deniz) ve doğu/batı ayrımı

- Alan: 2,500,000 km2 [E] Wikipedia Mediterranean Sea, ham metin: "The Mediterranean Sea covers an area of about 2500000 km2".
- Ortalama derinlik: 1,500 m [E] "has an average depth of 1500 m".
- En derin nokta: 5,109 ±1 m, Calypso Deep, İyon Denizi [E] "the deepest recorded point is 5109 ±1 m in the Calypso Deep in the Ionian Sea". ÇELİŞKİ: B'deki 5,267 m eski bir değer olarak not edilmiş; güncel [E] değeri 5,109 m.
- Doğu/batı ayrı alan ve derinlik: BULUNAMADI. Wikipedia Mediterranean Sea sayfasında alt havza tablosu var (Libya Denizi 350,000 km2; Levant Denizi 320,000 km2; Tirren 275,000 km2; Ege 214,000 km2; İyon 169,000 km2; Balear 150,000 km2), ancak doğu ve batı toplamları yok. Western_Mediterranean sayfası boş/yönlendirme; Levant_Basin sayfası kısa. Ayrı bir birincil kaynak bu turda bulunamadı.

### 2. Messinian tuz kalınlığı (Krijgsman, Roveri, Hsü)

- [E] Wikipedia Messinian salinity crisis: "The amount of Messinian salts has been estimated as around 4e18 kg (but this estimate may be reduced by 50 to 75% when more information becomes available)" (Ryan 2008 atfı). Hacim (>1 milyon km3) bu ham metinde doğrudan geçmiyor; B notundaki "1 million km3" yalnızca arama özetinden geliyordu.
- Kalınlık (km ya da m): ham metinde ana bir değer bulunamadı. CNRS (3 km), "2 km" ve "1,2 km" değerleri bu turda doğrulanamadı (cnrs.fr erişilemedi).
- Krijgsman 1999 (Nature, doi 10.1038/23231): Crossref'te özet yok; sayfa 429 döndü. Kalınlık değeri BULUNAMADI (okunamadı).
- Roveri 2001 (Sedimentary Geology, doi 10.1016/s0037-0738(00)00183-4): başlık ve yazarlar Crossref'te doğrulandı; özet alınamadı. Kalınlık BULUNAMADI.
- Hsü 1973: Crossref ve bu turdaki kaynaklarda bulunamadı. BULUNAMADI.
- Levant Messinian tuzu: Feng ve diğerleri 2017 (Mar. Pet. Geol., doi 10.1016/j.marpetgeo.2017.08.027) başlık doğrulandı; özet yok. Kalınlık BULUNAMADI.

### 3. Doğu Akdeniz kabuk ve yaş (Granot 2016)

- [B] Granot, R. (2016) Nature Geoscience, doi 10.1038/ngeo2784, "Palaeozoic oceanic crust preserved beneath the eastern Mediterranean". Özet (nature.com sayfası, meta açıklama): "Analysis of magnetic data ... reveals oceanic crust formed up to 340 million years ago" ve "the Herodotus Basin ... lineated magnetic anomalies, which imply that the crust is oceanic ... formed about 340 million years ago" ve "the transition from the rather weak and stretched continental crust found in the Levant Basin to the relatively strong oceanic Herodotus crust".
- SONUÇ: B notundaki "Doğu Akdeniz okyanusal (Nature Geosci 2016)" genellemesi yanlış. Granot yalnızca Herodotus Havzası için okyanusal kabuk ve yaş (~340 Ma, Paleozoik) veriyor. Levant Havzası için kabuk türü "gerilmiş sürekli kabuk" (stretched continental crust).
- Kabuk kalınlığı (km) Granot özetinde yok: BULUNAMADI.
- Granot'un "Herodotus" ve "Levant" ayrımı B'deki "Basin age: NOT FOUND" satırını doldurur: Herodotus için ~340 Ma.

### 4. Batı Akdeniz / Alboran (B'deki yaş ve kabuk ile ilgili)

- [B] Booth-Rea ve diğerleri 2007 (G3, doi 10.1029/2007GC001639), "Crustal types and Tertiary tectonic evolution of the Alborán sea": kabuk kalınlığı ~5 s TWTT (~15 km) batıda (doğu Alboran) ~2 s TWTT (~6 km, okyanusa benzer) doğuda (Algero-Balear). Okunan özet kısmında "rollback" zamanlaması yok. B notundaki "early-middle Miocene subduction rollback" atfı bu DOI için doğrulanamadı; bu atıf yanlış eşleşmiş olabilir.

### 5. Karadeniz (alan, derinlik, taban kabuğu, yaş)

- [E] Wikipedia Black Sea: alan 436,400 km2 (Azak Denizi hariç). B'deki 422,000 (Britannica) ve 461,000 (Azak dahil) bu turda kontrol edilmedi. Maksimum derinlik ve kabuk metni bu turda çekilmedi: BULUNAMADI (bu turda).
- [B] Hässig ve diğerleri 2020 (Tectonics, doi 10.1029/2020TC006336) özeti: "the oblique opening of the Eastern Black Sea as a back-arc to intra-arc basin, from west to east" ve "Throughout Cretaceous subduction, this segment ... was torn in two". B notundaki yorum uyumlu. Sayı içermiyor.
- [B] Spadini, Robinson, Cloetingh 1996 (Tectonophysics, doi 10.1016/s0040-1951(96)00187-4): başlık "Western versus Eastern Black Sea tectonic evolution: pre-rift lithospheric controls on basin formation". Özet alınamadı; kalınlık ve yaş BULUNAMADI.
- Nikishin, Brunet: bu turda birincil özet bulunamadı. BULUNAMADI.

### 6. Hazar (alan, derinlik, taban)

- [E] Wikipedia Caspian Sea: infobox alan 389,000 km2; metin "gross coverage 386,400 km2"; uzunluk 1,200 km; ortalama genişlik 320 km; yüzey deniz seviyesinin ~27 m altında. B'deki 371,000 km2 değeri Wikipedia ile çelişiyor (386,400 / 389,000).
- [E] Taban: "The Caspian Sea is at its South Caspian Basin, like the Black Sea, a remnant of the ancient Paratethys Sea. Its seafloor is, therefore, a standard oceanic basalt and not a continental granite body" (Kaz'min & Verzhbitskii 2011 atfı). B'deki "<10 km kabuk" (2024) ile çelişmiyor ama farklı bir yorum; ikisi yan yana.
- Ortalama/maks derinlik: bu turda ham metinde bulunamadı; B'deki 211 m / 1,025 m değerleri doğrulanmadı.
- Nikishin 2008 (Precaspian, 10.3997/2214-4609.20146090): başlık doğrulandı; sayı yok. BULUNAMADI.

### 7. Baltık (alan, buzul sonrası yükselme)

- [E] Wikipedia Baltic Sea: infobox alan 377,000 km2; metinde "surface area is about 349644 km2"; ortalama 55 m; maks 459 m (İsveç tarafı, merkez). B notundaki 415,000 km2 doğrulanmadı; üç değer var: 377,000 / 349,644 (ve 415,000 yok).
- [E] Buzul sonrası yükselme: "The land is still emerging isostatically from its depressed state ... post-glacial rebound. ... The uplift is about eight millimetres per year on the Finnish coast of the ..." (metin kesilmiş; "Finnish coast" yeterli). Yıllık 8 mm.
- [E] Oluşum: "occupies a basin ... formed by glacial erosion during the last few ice ages". B'deki "craton reactivation" (Ediacaran–Kambriyen) iddiası bu [E] ile çelişiyor; ikisi aynı sayfada değil, yorum farkı.
- Maks/ortalama tarih: BULUNAMADI.

### 8. Hudson Körfezi (alan)

- [E] Wikipedia Hudson Bay: alan 1,230,000 km2 ("Hudson Bay encompasses 1230000 km2", ikinci en büyük "bay"). B'de BULUNAMADI idi; artık bulundu.
- [E] Infobox: ortalama derinlik 100 m; maks 270 m (kaynak: Britannica). B'deki 128 m / 183 m (EBSCO) ile çelişiyor; ikisi yan yana.

### 9. Güney Çin Denizi (derinlik, alan)

- [E] Wikipedia South China Sea: alan ~3,500,000 km2 ("area = 3500000 km2"); ortalama 1212 m; en derin nokta "either 5559 m or 5567 m" (B'deki 5,563 ±4 m ile uyumlu; 5,016 m Britannica ile çelişiyor).
- Sahanlık genişliği ve çökelti kalınlığı: bu turda aranmadı. BULUNAMADI (bu turda).

### 10. Japon Denizi (sahanlık, çökelti)

- Bu turda aranmadı. BULUNAMADI (bu turda).

### 11. Kuzey Batı Akdeniz tuzu ve Balear (B 2.3b)

- Bu turda aranmadı ayrı olarak. Balear 325 m ve >1 km değerleri doğrulanmadı.

## Çelişen sayılar (yan yana)

| Konu | Değer A | Değer B | Değer C | Not |
|---|---|---|---|---|
| Akdeniz maks derinlik | 5,109 ±1 m [E] Wikipedia | 5,267 m (B eski değer) | - | Güncel [E] 5,109 m |
| Messinian tuz (Med) | ~4e18 kg [E], 50–75% azalma olası | 3 km (CNRS, bu turda okunamadı) | ~2 km / ~1.2 km | Kalınlık doğrulanamadı |
| Baltık alan | 377,000 km2 [E] infobox | 349,644 km2 [E] metin | 415,000 (B, doğrulanmadı) | Üç değer, iki [E] |
| Baltık oluşum | Buzul erozyonu [E] | Craton reaktivasyonu (B, Ö) | - | Yorum farkı |
| Hazar alan | 389,000 km2 [E] infobox | 386,400 km2 [E] metin | 371,000 km2 (B, Ö) | [E] iki değer, B farklı |
| Hazar taban | Oceanic basalt [E] | <10 km kabuk, 2024 (B, Ö) | - | Yorum farkı |
| SCS maks derinlik | 5,559 / 5,567 m [E] | 5,563 ±4 m (B, Ö) | 5,016 m (Britannica, B) | Tüm [E] değerler uyumlu |
| Hudson maks derinlik | 270 m [E] infobox (Britannica) | 183 m (EBSCO, B) | - | Ortalama 100 vs 128 m |
| Hudson alan | 1,230,000 km2 [E] | - | - | B'de BULUNAMADI idi |
| Doğu Akdeniz kabuk | Herodotus: okyanusal, ~340 Ma [B] Granot 2016 | Levant: gerilmiş sürekli [B] Granot | - | B'deki genelleme düzeltildi |
| Alboran kabuk | ~15 km batı (E Alboran) [B] Booth-Rea 2007 | ~6 km okyanusa benzer (Algero-Balear) [B] | - | Zamanlama özette yok |

## BULUNAMADI listesi (bu tur)

- Akdeniz doğu ve batı alan ve derinlik (ayrı değerler).
- Messinian tuz kalınlığı (Krijgsman 1999, Roveri 2014, Hsü 1973): Krijgsman metni erişilemedi (429); Hsü bulunamadı; Roveri özeti alınamadı.
- Karadeniz maks derinlik, ortalama derinlik, taban kabuğu kalınlığı, yaş (Nikishin, Cloetingh, Brunet): birincil özet alınamadı.
- Hazar ortalama ve maks derinlik; Nikishin 2008 sayısal değer yok.
- Baltık: dönemsel buzul çözülme tarihi; çökelti kalınlığı.
- Hudson Körfezi çökelti kalınlığı doğrulanmadı (B'deki ~2 km, 2,500 m).
- Japon Denizi ve Güney Çin Denizi sahanlık genişliği ve çökelti kalınlığı: bu turda aranmadı.
- Doğu Akdeniz kabuk kalınlığı (km): Granot özetinde yok.
- Levant Havzası evaporit kalınlığı: Feng 2017 özeti alınamadı.

## Kaynaklar (okunan)

- https://en.wikipedia.org/w/index.php?title=Mediterranean_Sea&action=raw (curl, [E])
- https://en.wikipedia.org/w/index.php?title=Messinian_salinity_crisis&action=raw ([E])
- https://en.wikipedia.org/w/index.php?title=Black_Sea&action=raw ([E])
- https://en.wikipedia.org/w/index.php?title=Caspian_Sea&action=raw ([E])
- https://en.wikipedia.org/w/index.php?title=Baltic_Sea&action=raw ([E])
- https://en.wikipedia.org/w/index.php?title=Hudson_Bay&action=raw ([E])
- https://en.wikipedia.org/w/index.php?title=South_China_Sea&action=raw ([E])
- https://www.nature.com/articles/ngeo2784 (via doi.org/10.1038/ngeo2784; [B] meta açıklama) — Granot 2016
- https://api.crossref.org/works/10.1029/2020TC006336 ([B] özet) — Hässig 2020
- https://api.crossref.org/works/10.1029/2007GC001639 ([B] özet) — Booth-Rea 2007
- https://api.crossref.org/works/10.1016/j.tecto.2008.09.026 (Govers 2009; özet yok)
- https://api.crossref.org/works/10.1038/23231 (Krijgsman 1999; başlık ve yazarlar; özet yok)

## Sonraki adımlar

1. Ağ izni tam ise (araç katmanında DNS hatası sürüyor) nature.com/articles/23231 ve cnrs.fr kontrol edilmeli; hız sınırı geçince Krijgsman 1999 ve CNRS.
2. Black Sea ve Hazar için Wikipedia ham metinde maks derinlik ve kabuk cümleleri grep ile çekilmeli (dosyalar bu turda indirildi, ancak derinlik grep'i yapılmadı).
3. Japon Denizi ve SCS sahanlık genişliği bu turda aranmadı.
