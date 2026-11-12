# 24. Atlas ve Merak ile veri alışverişi

Araştırma tarihi: 12 Kasım 2026. Bu konu dışarıdan kaynak taramasıyla değil, atlas deposunun (`dunyam-atlas-mobil`) salt okunur incelenmesiyle yazıldı; depoda hiçbir dosyayı değiştirmedim ve hiçbir betiği çalıştırmadım. Merak için tek bir web araması yaptım: "MerakMapMaker" adına dair açık bir kaynak bulunamadı [Y]. Etiketler: **[A]** atlas deposundaki dosyadan okundu (dosya adı yanında), **[K]** `KARARLAR.md`, **[H]** bizim çıkarımımız, **[Y]** bulunamadı.

## Kısa sonuç

**1. Atlas zincirine giriş kapısı bir yükseklik haritası: 16 bit gri PNG ya da `.glb`.** Atlas notu (`CLAUDE.md` §9): sahip araziyi MerakMapMaker'da düzenleyip yeni bir `.glb` verdiğinde asıl projedeki `_mk_heightmap.py`, `worldinfo/` içindeki en yeni arazi dosyasından (`.glb` varsa o, yoksa 16 bit PNG) gezegen tuvalini üretir. Kaynak tercihen `.glb`: orada z gerçek yüksekliktir. 16 bit PNG de desteklenir [A].

**2. Atlasın yükseklik eğrisi sahibin çapalarından kurulu ve gri tonu doğrudan metreye çevirmiyor.** `dunya/dunyam.json` → `heightmap`: dosya `dunya/dunyam_heightmap.png` 4096 × 2048, 16 bit gri (`I;16`), küresel eşdikdörtgen (sınırlar −180, −90, 180, 90), `sea_level_value` 11934, en yüksek 7000 m, en derin −1492 m, `elev_gamma` 1,0; `elev_curve` 37 noktalı, monoton (PCHIP) gri tondan metreye eğri: örneğin normalize gri 0,20939 → 250 m, 0,38616 → 800 m, 0,4735 → 1000 m, 0,83125 → 6000 m, 1,0 → 7000 m [A]. Yani aracın ürettiği gerçek yükseklikler eğrinin tersinden gri tona çevrilmeli ya da `.glb` ile verilmeli; yoksa atlas yükseklikleri kendi eğrisinden geçirip değiştirir [H].

**3. Kıta boylamda sabitleniyor.** `KARA_MERKEZ_LON = −0,7`; her yeni arazi sürümünde kıta kaymasın diye (akıntılar, işaretli bölge, notlardaki boylamlar sessizce yanlış olmasın) [A, CLAUDE.md §9 ve dunyam.json]. Yeni araç çıktısı aynı yerleşimle gelmeli [H].

**4. Atlasın tektonik katmanı bu araçla değişecek.** Atlas bugün levha hikâyesini araziden geriye doğru okuyor (`tektonik/uygulama.py`, `data/tektonik.json`: 13 levha, 202 sınır, 35 kuşak, 7 yarık); "Motor levha bilmez, iklimi etkilemez" [A]. Bu araç bunu ters çevirecek: önce blok tarihi, sonra arazi. Şema (levha, sınır türü, kuşak) yeniden üretilebilir ama bu bir tasarım işi [H].

## 1. Atlasın bugünkü yükseklik zinciri [A]

Sırayla (`CLAUDE.md` §9, "Arazi değişince ne yapılır"):

1. `python _mk_heightmap.py`: `worldinfo/` içindeki en yeni arazi dosyasından gezegen tuvalini üretir, `data/work/` altına yazar. `file`, `sea_level_value`, `max_depth_m` alanlarını kendisi yazar; elle taşınmaz.
2. `elev_curve` artık sahibin çapalarıyla kurulu; eski yöntem (`_egri_kur.py --yaz`: karanın alan ağırlıklı gri ton dağılımı ETOPO'dan ölçülmüş gerçek Dünya buzsuz kara hipsometrisine nicelik eşlemesiyle oturtulur) çapaları siler, "ŞU AN KOŞMA".
3. `_akinti_kur.py`: yalnız kıyı değiştiyse akıntıları yeniden türetir.
3b. Kabartma görseli: editörden aynı çerçevede yeni renkli görsel (konturlar kapalı); `kabartma_kaydet.py <görsel>` koşulur. Görsel yenilenmezse uygulamadaki gölge eski dağları gösterir; `uret.py` görselin karaya oturmasını her koşuda ölçer, yüzde 95'in altındaysa uyarır. Kayıt: `kabartma` alanında `sx`, `sy`, `ox`, `oy`, IoU 0,9859.
4. 0,26° çözünürlüklü koşu, `export_viewer.py --res 0.26`, `_atlas.py`, `_denetim.py`, `node _atlas_test.js`, `_repo_senkron.py --yaz`. Uyarı: `_atlas.py` mobil `data/atlas.json`'u eski biçimde yazar; mobil veri yalnızca bu repodaki `uret.py`'den üretilir.
5. Commit ve push; iş akışı (workflow) veriyi yeniden üretir.

**Sert sıra kuralı:** eğri düzelmeden nem düğmeleri (`convective_c`, `rh_ocean`, `blocking_*`) ayarlanmaz; bayat bir eşlemeyle ayarlanan düğme, eğri düzelince yanlış kalır ve yanlışlığı arazi kusuru gibi gösterir [A].

**Zincirin tüketicileri (mobil depodaki dosyalar) [A]:** yükseklik eğrisi (`dunyam.json`), `data/yukseklik.png` (1992 × 1680, 8 bit gri, harita dokusu), `data/kabartma*.jpg` (üç kabartma), iklim, su (`su.json`), buzul (`BUZUL.md`), toprak, bitki, yaşanabilirlik, tarım, hayvan, tektonik (`tektonik.json`, `levha.png` 1495 × 1262 8 bit) ve `data/atlas.json` (yaklaşık 2,8 MB).

## 2. Aracın çıktısı için gereken biçim [H]

| Atlas girdisi | Araç çıktısı | Not |
|---|---|---|
| Yükseklik haritası | tercihen `.glb` (z = metre) ya da 16 bit gri PNG, 4096 × 2048 küresel eşdikdörtgen tuval | tuval yaklaşık 9,8 km/piksel (ekvatorda), aracın 5 ile 10 km hücresiyle aynı mertebe |
| Gri ton eşlemesi | PNG verilirse `elev_curve` tersiyle gri tona çevrilmeli (sea_level_value 11934, en yüksek 7000 m, en derin −1492 m) | `_mk_heightmap.py` ve `_egri_kur.py` bu depoda yok, tam eşleme bilinemez [Y] |
| Kıyı | atlas maskesiyle birebir; ölçek 0,754, kayma 1511,9 / 162,7 [K] | maske aynı dışa aktarımdan gelirse |
| Boylam | `KARA_MERKEZ_LON = −0,7` ile sabit | yeni çıktı aynı yerleşimle |
| Kabartma görseli | konturlu olmayan renkli kabartma, atlasla aynı çerçeve, karaya oturma ≥ %95 | 21. belgedeki gölgeleme çıktısı bu rolü görebilir [H] |
| Tektonik | levha, sınır türü (Bird 2003, PB2002, göreli hız sınıra 20°'den yakınsa yanal), kuşak, yarık | `tektonik/uygulama.py` şeması; yeni blok modeliyle yeniden türetilmeli |

## 3. Çatışmalar ve açık noktalar

- **Yükseklik çapaları ile gerçek Dünya.** Atlas kıtasını bilerek Dünya'dan yüksek tutuyor: ova 250 ile 300 m, plato çanağı 800 ile 1000 m, Büyük Duvar zirveleri 6000 m, en yüksek 7000 m, kara medyanı yaklaşık 950 m (Dünya 377 m) [A, CLAUDE.md]. Aracın ürettiği yükseklikler bu çapalardan geçmeli; 20. belgedeki gerçekçilik ölçütü bu yüzden bağıl olmalı.
- **Plato çanağı.** Atlas iklimi çanak içini 800 ile 1000 m alıyor [K]; sahibin isteği 1000 ile 2000 m step. Bu aralığa yakın kalmak atlası bozmaz, 2000 m'ye çıkmak iklim ayarlarının yeniden denenmesini gerektirir [K ve H].
- **Boylam sınırı tutarsızlığı.** Atlas `tektonik/OZET.md` kıtayı "47°B ile 43°D" yazıyor; `KARARLAR.md` "44°B ile 43°D" diyor [A ve K]. Hangisinin doğru olduğunu atlas verisinden (`dunyam.json`) ya da maskeden ölçmek gerekir; şimdilik doğrulanmadı [Y].
- **Eski yöntem uyarısı.** `_egri_kur.py --yaz` çapaları siler; yeni araçla bu betik çalıştırılmamalı [A].
- **Küresel tuval çözünürlüğü.** Atlas çalışma çözünürlüğü 0,26° (yaklaşık 29 km); aracın 5 ile 10 km hücreli çıktısı bunun üzerinde, tuvale indirgeme (alan ağırlıklı) gerekecek [A ve H].
- **Merak.** MerakMapMaker'a dair açık bir kaynak bulunamadı (tek web araması); `.glb` ve 16 bit PNG ihracı yalnızca atlasın kendi notundan [A ve Y]. Merak "History" sekmesi hakkında yalnızca önceki oturumdan bilgi var (bu dosyada doğrulanmadı).
- **Zincir uyumu.** Aracın çıktısı atlas zincirine girdiğinde nem düğmeleri yeniden ayarlanmak zorunda kalabilir; sıra kuralına uyulmalı (eğri önce) [A].

## 4. Aracın varsayılan değerleri

| Parametre | Öneri | Etiket |
|---|---|---|
| Çıktı biçimi | `.glb` (z metre) ve 16 bit PNG, ikisi birlikte | [A ve H] |
| Tuval | 4096 × 2048 küresel eşdikdörtgen, ölçek 0,754, kayma 1511,9 / 162,7 (maske uyumu) | [A ve K] |
| Boylam | `KARA_MERKEZ_LON = −0,7` | [A] |
| Yükseklik üst sınırı | 7000 m; ova 250 ile 300 m, çanak 800 ile 1000 m (veya sahip kararıyla 1000 ile 2000 m), Duvar 6000 m | [A ve K] |
| Gri ton eşlemesi | `elev_curve` tersi, deniz seviyesi değeri 11934 | [A] |
| Kabartma | konturlu olmayan renkli görsel, atlas çerçevesinde, IoU ≥ 0,95 | [A] |
| Tektonik şema | 13 levha tipi şema; sınır türü Bird 2003 / PB2002, 20° | [A] |
| Atlasa dokunma | araç atlas deposunu değiştirmez; çıktıyı `worldinfo/` benzeri girdi klasörüne yazar | [H] |

## 5. Bulunamayanlar ve doğrulanamayanlar

- MerakMapMaker belgeleri ve `.glb` / PNG dışa aktarım ayrıntıları (web aramasında hiçbir sonuç); atlasın `_mk_heightmap.py`, `_egri_kur.py` kaynakları (mobil depoda yok).
- Gri ton ile metre eşlemesinin tam semantiği (normalizasyon aralığı, deniz tabanı kolu).
- Kıtanın batı sınırının 44°B mi 47°B mi olduğu.
- `data/work/dunyam_heightmap.png` mobil depoda yok; yalnızca `dunya/dunyam_heightmap.png` var.

## 6. Promptumdaki hatalar (düzeltildi)

- Karar günlüğündeki "44°B" ifadesi atlasın kendi özetiyle (47°B) çelişiyor; doğrulanmalı.
- "Merak'ın içe aktarım biçimi bilinmiyor" notu doğru kaldı; dışa aktarım biçimi `.glb` ve 16 bit PNG olarak atlas notundan öğrenildi.

## Kaynaklar

- `dunyam-atlas-mobil/CLAUDE.md` §9 ve yükseklik eğrisi tablosu, `dunya/dunyam.json`, `tektonik/OZET.md`, `data/tektonik.json`, `DURUM.md` (salt okunur)
- `KARARLAR.md` 2. bölüm (ölçek ve projeksiyon)
- MerakMapMaker için: web araması sonuçsuz.
