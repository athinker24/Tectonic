# A: Akarsu güç yasası (E = K A^m S^n) — ızgara çözünürlüğüne (Δx) bağımlılık

Durum: Araştırma başladı. Bulgular aşağıya eklenecek.

Etiketler: [B] tam metin okundu, [B-öz] özet/arama sonucu üzerinden, [Ö] yalnızca arama özeti, ERİŞİLEMEDİ, BULUNAMADI.

## Kaynak listesi (hedef)

1. Hergarten (2020) — Transport-limited fluvial erosion (ESurf/ESD?)
2. Hergarten (2025) — Earth Surface Dynamics, K ve m ızgara çözünürlüğü ölçeklemesi / Resolution dependence of the stream power law
3. Braun & Willett (2013) — FastScape / ızgara ve drenaj alanı
4. Schwanghart & Scherler (2017) — TopoToolbox / ölçek
5. Perron (2008) — Ardından gelen "Perron 2008" difüzyon/çözünürlük
6. Cordonnier et al. (2016/2019) — K'nin hücre alanına bağımlılığı
7. Whipple & Tucker (1999)
8. Lague (2014) — Δx ve eğim ölçeği
9. Stock & Montgomery (1996/1999)
10. Gailleton et al. (2019) — çok çözünürlüklü/uyarlamalı ağ

## Önemli düzeltme (kaynak atfı)

- "Hergarten 2025, Earth Surface Dynamics, 'Resolution dependence of the stream power law'" biçiminde bir makale BULUNAMADI. ESurf 13, 403–415 (2025), URL https://esurf.copernicus.org/articles/13/403/2025/ , başlığı "A fractal framework for channel–hillslope coupling", yazarları Kargère, Constantine, Hales, Grieve, Johnson [B]. Hergarten bu makalede atıf olarak geçiyor (satır: "As noted by Pelletier (2010), Hergarten (2020), and Hergarten and Pietrek (2023)...") ama yazar değil [B].
- Sonuç: Kullanıcının verdiği "Hergarten 2025 K ve m ızgara ölçekleme" başlığı doğrulanamadı; bu konu için en yakın 2025 kaynak Kargère et al. (2025).

## Bulgular

### F1 — Hergarten (2020), transport-limited, ESurf 8, 841–854 [B]
- Kaynak: https://esurf.copernicus.org/articles/8/841/2020/ , DOI 10.5194/esurf-8-841-2020 [B]
- Etiket: [B]
- Bulgu: Taşıma sınırlı modelde (transport-limited) düğüm alanı s_i "regular mesh için piksel boyutu" olarak tanımlanıyor; toplam sediment akısı Q_i ile hesaplanıyor (sediment dengesi, akı/birim genişlik değil) [B].
- Bulgu (ölçek sorunu): Q, toplam akıya dayalı ifadede eğer Γ (kazı fonksiyonu) doğrudan detachment-limited K gibi alınırsa "rivers linear nesneler olarak ele alındığında ölçek sorunu" çıkar; sonuçların çözünürlüğe yapay bağımlılığını önlemek için Γ'da piksel boyutuna bağlı ek bir yeniden ölçekleme faktörü tanıtılmalı [B, cümle: "an additional rescaling factor depending on the pixel size must be introduced in the definition of Γ in order to avoid an artificial dependence of the results on the spatial resolution"]. Metin, bu ölçekleme için Howard 1994, Perron et al. 2008, Pelletier 2010, Hergarten 2020a'ya atıf yapar ve "farklı yaklaşımlar" bunlarda tartışıldığını belirtir [B]. Makale kendi yaklaşımının formülünü tam vermez; "uniform K ölçekleme kuralı" tanımlamadığı için bu konuda BULUNAMADI (tek bir sabit kural).
- Bulgu (difüzyon): Taşıma sınırlı model difüzyon tipi denklemdir; difüzivite "catchment size" ile değişir, birkaç büyüklük mertebesi [B, satır 30].
- Bulgu (lineer hibrit): Lineer model (n=1) için iterasyonsuz çözüm, δt büyük değerlerle de çalışır; δt=1'de hata "birkaç yüzde", bu bir zaman gecikmesi (time lag) olarak yorumlanır [B, satır 91].
- Örnek domain: 5000×5000 düğüm; m=0.5 kullanılmış, lengths piksel birimi [B, satır 78].

### F2 — Kargère et al. (2025), ESurf 13, 403 — ızgara çözünürlüğü ve drenaj alanı [B]
- Etiket: [B]
- Bulgu (Eq. 1-2 bağlamı): 2D'de katkı drenaj alanı, ızgara çözünürlüğüyle tutarsız ölçeklenir; hillslope'lar paralel akış, kanallar yakınsak akış gösterir. Paralel akışlı bölgelerin alanı δ (ızgara boyutu) tarafından belirlenir; yakınsak akış alanları δ'ya karşı etkilenmez [B, satır 29].
- Bulgu (hipotez 1): Eğim değişim noktasında (inflection point) drenaj alanı δ'nın bir faktörü ile ölçeklenir (1 faktör δ) [B, satır 61, 63: "varies by a factor of δ across resolutions"].
- Bulgu (hipotez 2): Kanal başı (channel head) drenaj alanı çözünürlükten bağımsızdır ve inflection-point özgül alanının karesine karşılık gelir [B, satır 61].
- Bulgu (özgül drenaj alanı): a = A/δ tanımı; a'nın δ'ya örtük bağımlılığı olduğu belirtilir (Litwin et al. 2022b; Costa-Cabral & Burges 1994) [B, satır 39]. D∞ akış yönlendirmesi kullanılır [B].
- Bulgu (eğim eğrisi): Piksel genişliğinden büyük kanal genişliği varsayımında kanal eğimi konkavitesi, Pelletier (2010) yaklaşımından farklı çıkar; yazarlar kanal genişliğinin piksel genişliğini aştığını varsayar, piksel genişliği kanal başı genişliğine eşit alınır (Litwin et al. 2022b'ye atıf) [B, satır 67].
- Not: Bu makale K ve m için açık "δ'ya göre K ölçekleme kuralı" vermiyor (taramada bulunamadı) — yalnızca A ve eşik ölçeğinin δ ile ilişkisini veriyor. K için: "K difficult to estimate from topography" [B, satır 64].

### F3 — Hergarten & Pietrek (2023), "Self-organization of channels and hillslopes...", ESurf 11, 741–755 [B]
- Kaynak: https://esurf.copernicus.org/articles/11/741/2023/ , DOI 10.5194/esurf-11-741-2023 [B]
- Etiket: [B]
- Bulgu (K'nın δx'e yeniden ölçeklenmesi): Boyutsuz K (ve U) birim ızgara aralığı δx (m), dikey ölçek L, zaman ölçeği T ile tanımlanıyor; K için boyut analizinden bir yeniden ölçekleme faktörü veriliyor (formül PDF metninde bozuk geldi, faktör [Ö]); U da ayrıca ölçekleniyor [B, satır 68-69]. Sonuç: birim δx'te yapılan boyutsuz simülasyonu başka δx'e aktarmak için, sabit K ve U'da α ve β sabit olmalı [B, satır 69]. Ayrıca bu ölçekleme "L ve T'nin δx'ten bağımsız" olmasını sağlar (yalnızca SPIM / shared stream-power, hillslope eklenmeden) [B, satır 70].
- Bulgu (difüzyon ile kırılma): Hillslope süreçleri (difüzyon) eklenince bu ölçekleme kayboluyor; K_d ve K_t, Eq. 16 (m=0) ile farklı ölçeklenir ve yatay bir karakteristik uzunluk oluşturur; gerçek dünyadaki A_h değeri δx² ile ölçeklenir [B, satır 71]. Sabit erodibilite (ve sabit gerçek A_h) için boyutsuz A_h'nin de δx'e göre ayarlanması gerekir [B, satır 71].
- Bulgu (kalıntı bağımlılık): Hergarten (2020a, Fig. 10) "rescaling parametrelerden sonra bile" ızgara aralığına kalıntı bağımlılık gözlemlemiş; bu, hillslope–fluvial geçiş bölgesinde paralel akış desenlerinden kaynaklanıyor [B, satır 29]. Yazarlar, eşik-tabanlı modellerde Ac'nin "süreçlere bağlı" olduğunu ve evrensel bir değeri olmadığını, Ac'nin difüzivite ile artması gerektiğini belirtiyor [B, satır 32].
- Bulgu (difüzivite duyarlılığı): Aynı topografyada D 10 kat artınca kanal oluşturan alan yaklaşık 6.5 kat artıyor, yani ~D^0.8 [B, satır 42].
- Bulgu (m=0 seçimi): Hillslope modeli için m=0 seçilmesi, "A'nın unchannelized akış için ızgara aralığına bağlı olması" nedeniyle tercih ediliyor [B, satır 51]. Bu, m'nin ızgara ile ilişkisine doğrudan bir ipucu.

### F4 — Hergarten (2020a), "Rivers as linear elements in landform evolution models", ESurf 8, 367–377 [B]
- Kaynak: https://esurf.copernicus.org/articles/8/367/2020/ , DOI 10.5194/esurf-8-367-2020 [B]
- Etiket: [B]
- Bulgu (ölçek sorunu): Ölçek sorunu ızgara genişliği δ ile: "canyon-like topography" ve yalnızca yerel taşıma yoksa vadi genişliğinin δ ile azalması; yerel taşıma (difüzyon) eklenince kanal eğimi δ'ya bağlı artıyor [B, satır 20-23]. Örnek: δ=0.01 ve δ=0.002 (100×100 ve 500×500), m=0.5, θ=0.5 [B, satır 20].
- Bulgu (Howard 1994 / Perron 2008 / Pelletier 2010): Ölçek sorununa iki yaklaşım önerilmiş — Howard (1994) alt-piksel temsili, Perron et al. (2008) bunu detachment-limited'a aktarmış (δ-faktörü; kanal genişliği w sabit varsayılır), Pelletier (2010) ise taşıma terimini ters faktörle yeniden ölçeklemiş [B, satır 27-30]. Hergarten bu yaklaşımların ikisinin de kanal genişliğine bağlı kaldığını ve w'nın tutarsız olduğunu belirtiyor [B, satır 29-32].
- Bulgu (çözüm, ana sonuç): Eşik kataleti A_c tanımlanır (A ≥ A_c kanal, aksi halde hillslope) [B, satır 36]. Ölçekleme ilişkisi: A_e ≈ α A_c^β (Eq. 14); θ=0.5 kafes (lattice) için α=1.360, β=0.465 [B, satır 48]; OCN (optimal channel networks, θ=0.5, L=4096) referansı α=1.508, β=0.478 [B, satır 53]. A_e: kanal bölgesine akan hillslope alanının ortalaması (piksel sayısı) [B, satır 38-39].
- Bulgu (fiziksel alan ile δ bağı): A_c fiziksel alan olarak yazılınca bölgesel erozyon terimi δ^(−2β) ile ölçeklenir [B, satır 53-54]. β=0.5 alınırsa terim yaklaşık δ^(−1) olur; bu, Perron et al. (2008)'in varsayımıyla "temelde aynı" [B, satır 54]. Fark: Perron'daki w sabit ve fiziksel anlamını yitiriyor [B, satır 54].
- Bulgu (kalıntı bağımlılık, sayısal): Yeniden ölçeklenmiş ortalama k_s, N=10^5'ten 10^7'ye 1.6–2.0 arasında değişiyor (kalıntı bağımlılık, yakınsama belirsiz) [B, satır 59, 62]. Ölçeklenmemiş (dashed) durumda k_s, N arttıkça (δ küçüldükçe) belirgin artıyor [B, satır 59].
- Bulgu (kanal + difüzyon): Kalıntı bağımlılığın nedeni ağ yeniden düzenlenmesi (network reorganization); difüzyon dendritik topolojiyi paralel akışa doğru bozuyor [B, satır 62].
- Formüller (Eq. 11-16) PDF metin çıkarımında bozuk; bu notta yalnızca metindeki sayısal ve sözel ifadeler kullanıldı.

### F5 — Hergarten (2020), transport-limited: ölçek faktörü ile F1 bağlantısı
- F1'deki "piksel boyutuna bağlı yeniden ölçekleme faktörü" ifadesi [B], F4'teki A_c tabanlı yeniden ölçekleme ile birlikte okunmalı; F1 bu faktörün tam formunu vermiyor, F4 bunu veriyor (A_c, β). [B-öz, çapraz okuma]

### F6 — Kargère et al. (2025): "BULUNAMADI" olan K/m ölçekleme kuralı
- Tam metinde K ve m için açık, δ'ya göre bir K ölçekleme kuralı bulunamadı [B, tarama]; yalnızca A_inflection ∝ δ ve A_channel_head ∝ δ⁰ hipotezleri (F2).

### Arama özetleri (henüz tam metin yok)
- Braun & Willett (2013), Geomorphology 180–181, 170–179, DOI 10.1016/j.geomorph.2012.10.008 [Ö]: O(n) implicit yöntem; Landlab notu, transient çözümün zaman adımından bağımsız olmadığını ve Appendix B'de doğruluk tartışıldığını söylüyor [Ö]. Izgara aralığı etkisi arama özetinde BULUNAMADI.
- Schwanghart & Scherler (2017), ESurf 5, 821–839, https://esurf.copernicus.org/articles/5/821/2017/ [Ö]: DEM kaynaklı profil hatası ve kantil regresyonla düzeltme; K/m çözünürlük ölçekleme ile DOĞRUDAN ilgisi yok (ölçüm/DEM hatası tarafı). Bu nedenle ızgara ölçeklemesi için BULUNAMADI, tangential.
- Cordonnier 2016: arama BULUNAMADI (makale bulunamadı). Kaynak "Cordonnier, Davy..." için tekrar aranacak.
- Gailleton et al. 2019 ESurf 7, 549: Gailleton, Malatesta, Cordonnier, Braun'un makalesi arama sonucunda görüldü (90 m topografya, drenaj havzaları); "multiresolution/adaptive mesh" konusu DOĞRULANAMADI [Ö]. Adaptif-ağ konusu için BULUNAMADI (henüz).
- Armitage (2019), ESurf kısa iletişim: akış yönlendirmesi ve kenar tabanlı dağıtımın LEM çözünürlük bağımlılığını önemli ölçüde azalttığı [Ö].
- Perron, Dietrich & Kirchner (2008), JGR 113, F04016, DOI 10.1029/2007JF000977: Hergarten (2020a) ve Hergarten (2020) tarafından anılıyor; kendi metni henüz okunmadı [B-öz, atıf].
