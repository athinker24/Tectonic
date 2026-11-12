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

### F3 — Hergarten & Pietrek (2023), ESurf 11, 741 [B-öz]
- Kaynak: https://esurf.copernicus.org/articles/11/741/2023/ [B-öz, yalnızca arama özeti]
- Kargère et al. 2025 bunu, "Hergarten and Pietrek (2023)" olarak paralel akış/yakınsak akış tartışmasında anıyor [B, satır 29]. Tam metni henüz okumadım — TAMAMLANACAK.

### F4 — Hergarten (2020a), "Rivers as linear elements", ESurf 8, 367–377 [B-öz]
- URL: https://esurf.copernicus.org/articles/8/367/2020/ [B-öz, arama özeti]
- Arama özeti: çözünürlüğe bağlı ölçek sorununa dair güç-yasası ölçeklemesi (eşik kataleti boyutu ve ağ genişliği içeren) tartışılır [Ö]. Tam metin için TAMAMLANACAK.
