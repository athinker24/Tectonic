# Merak (merakmapmaker.com) için yükseklik haritası hattı

Bu belge, bu depodaki dünyanın (tarih/) yükseklik verisinin Merak'a nasıl aktarıldığını, Merak'ın gri değerleri nasıl
okuduğunu, görüntülerin Merak dünyasına nasıl oturtulduğunu ve hangi betiğin ne ürettiğini anlatır. Başka bir insanın ya da
yapay zekanın bu işi sıfırdan sürdürebilmesi için yazıldı. Bütün sayılar ölçülmüş değerlerdir; ölçülmeyen ya da bilinmeyen
şeyler "bilinmiyor" diye işaretlenmiştir.

Çalışma dizini: `tarih/`. Bütün betikler oradan `python3 BETIK.py` ile çalışır. Python paketleri: numpy, scipy, Pillow, matplotlib.
Büyük görüntüler için her betikte `Image.MAX_IMAGE_PIXELS = None` vardır.

---

## 1. Kısa özet (yapay zeka için)

- Merak'a verilen son dosyalar **16 bit gri PNG**, boyutu **16000 × 7719** (yedek: 8000 × 3859). Bu boyut Merak'ın kendi
  16 bit dışa aktarımıyla aynıdır; Merak'ta "Import image → terrain", sekme **"Heightmap / mask (auto)"**, düğme **"Fill world"**
  ile içe aktarılınca her piksel dışa aktarımdaki pikselin tam üstüne gelir (ölçek 1, kayma 0).
- Gri kodlama (Merak'ın dışa aktarımından altı test platosuyla çözüldü, hata < 1 m):
  - Deniz seviyesi gri değeri `S = 14642` (16 bit; 0,2234 oranı).
  - Kara (m ≥ 0): `gri = S + 50893 · sqrt(m / 8000)` → beyaz (65535) = 8000 m.
  - Deniz (m < 0): `gri = S · (1 − (−m / 6840) ^ 0,607)`.
  - Okyanus tabanının dışa aktarımdaki değeri 3598 ≈ −4298 m.
- Kara/deniz ayrımı: `gri > S` kara. Kıyı çizgisi sahibin maskesidir (v2) ve hiçbir adımda değiştirilmez.
- İçe aktarmanın da aynı eğriyi kullandığı varsayılır ve sahibin denemesinde doğru oturduğu görüldü; içe aktarma eğrisi ayrıca
  platolarla ölçülmedi (bkz. 9. bölüm).

```python
import numpy as np
S, KA, ZM, DD, DP = 14642.0, 50893.0, 8000.0, 6840.0, 0.607

def coz(g):            # 16 bit gri -> metre
    g = g.astype(np.float32)
    return np.where(g >= S, ZM * np.clip((g - S) / KA, 0, None) ** 2,
                    -DD * np.clip(1 - g / S, 0, None) ** (1 / DP))

def kodla_kara(m):     # metre (>= 0) -> gri
    return np.round(S + KA * np.sqrt(np.clip(m, 0, ZM) / ZM)).clip(0, 65535)

def kodla_deniz(m):    # metre (< 0) -> gri
    return np.round(S * (1 - np.clip(-m / DD, 0, 1) ** DP)).clip(0, S - 1)
```

Bu işlevler `merak_birlestir.py` (`coz`, `kodla`) ve `merak_kiyi.py` (`deniz_kodla`) içinde tanımlıdır.

---

## 2. Merak'ın kodlaması nasıl bulundu

1. Sahip Merak'ta açık okyanusa, Flatten aracıyla sayı girerek, düz tepeli altı plato koydu: 4000, 1000, −1995, 2514, 99, −524 m.
2. Merak'tan 16 bit dışa aktarım alındı (`The-Greatest-Them-Of-All-heightmap-16bit.png`, 16000 × 7719, ve `_8k` sürümü 8000 × 3859).
3. Her platonun ortasındaki sabit gri değer okundu:

| metre | gri (16 bit) |
|---|---|
| −1995 | 7710 |
| −524 | 11565 |
| 99 | 20303 |
| 1000 | 32639 |
| 2514 | 43176 |
| 4000 | 50629 |
| okyanus tabanı | 3598 |

4. Karada `gri − S` ile `sqrt(m)` arasındaki oran üç aralıkta da 569'dur (568,5 ile 569) → karekök eğrisi. `S = 20303 − 569·sqrt(99)
   = 14642`. `(65535 − 14642) / 569 = 89,4` → beyaz = 89,4² ≈ 8000 m. Sonuçta `KA = 65535 − S = 50893`.
5. Denizde iki noktadan üs ve ölçek çözüldü: `p = 0,607`, `D = 6840 m`. Bu eğri −1995 ve −524'ü 1 m içinde verir; tabanı (3598)
   −4298 m'ye çevirir. Deniz eğrisi yalnız iki nokta ve tabanla belirlendi; ara derinliklerde birkaç on metrelik hata olabilir.
6. Merak arayüzünde yazan açıklama: "Grayscale = heightmap (black sea floor → white peaks, sea level ≈ 22% gray). Pure black & white =
   land mask". Ölçülen 0,2234 bu %22 ile uyumludur.

Önemli: daha önceki dosyalarda (`dunya_*`, `v2_*`) **doğrusal** bir kodlama kullanılmıştı (`gri = 0,22 + 0,78·m/zmax`). Merak bunları
da okudu ama metreler doğru çıkmaz. Son dosyalar (birlesik, kiyi, son, saf, temiz, uslup) Merak'ın kendi karekök kodlamasındadır.

---

## 3. Çerçeveler ve "Fill world" ile oturtma

### 3.1 Merak'ın dünya çerçevesi
- Merak dışa aktarımı 8000 × 3859 ya da 16000 × 7719'dur, yani oran **2,073 : 1** (tam 2:1 değil). Bu, Merak dünyasının kendisidir.
- "Fill world" görüntüyü dünya kutusuna **oranını koruyarak** sığdırır ("never stretched"). Ölçüm: 8000 × 4000 (2:1) bir görüntü
  yükseklikten sığdırılmış ve yatayda ortalanmıştır; ölçek 3859/4000 = 0,965 ve yatay kayma yaklaşık 144 piksel (8k).
- Sonuç: Merak'ın dışa aktarımıyla **aynı boyutta** bir görüntü verilirse Fill world birebir oturur. Son dosyaların hepsi böyledir.
- "Place on existing" sekmesinde varsayılan kutu dünyayı doldurmaz; o sekme kullanılırsa önce "Fill world"e basılmalıdır. Bu
  sekmenin saydamlığı (alfa) ya da siyahı "dokunma" olarak okuyup okumadığı **bilinmiyor**; tam harita için kullanılmamalıdır.

### 3.2 Zincir: bizim harita → v2 → Merak
Dört koordinat sistemi vardır:

1. **Bizim tam harita** (`maske.png`, `cikti/benzer_z.npy`): 3808 × 2914 piksel (genişlik × yükseklik), piksel ≈ 2,1 km.
   Kuzey kenarı 50°K; harita 8000 km genişliğinde. `olaylar.py`: `KM_PX = 4.0` (2000 piksellik çizim çerçevesinde), `GEN = 2000`,
   `YUK = 1530`. Bizim çizim çerçevesinden maskeye çarpan 3808/2000 = 1,904.
2. **v2 kıta kutusu**: sahibin kare maskesi (1024 × 1024 JPEG, `c7048a42`/`0ad7dd57` yüklemesi). Temizlenir (6 pikselden küçük
   kara ve deniz parçaları silinir), sınır kutusuna kırpılır ve bizim enlem aralığına (50°K ile 5,053°G) ölçeklenir.
   8000 × 4000 dünyada kutu: `x = 3200, y = 889, genişlik 1601, yükseklik 1223`; boylam −36° ile +36,045°.
3. **v2 dünyası**: 8000 × 4000, eşdikdörtgen, `dunya_maske_v2.png`.
4. **Merak dünyası**: 8000 × 3859 (ya da 16000 × 7719).

Dönüşümler (hepsi satır `y`, sütun `x`):

- Merak 8k → v2 dünyası (`birlesik_olcek.json`, kara örtüşmesi IoU 0,9932):
  `y_v2 = y · 1,0364 + 0,198`, `x_v2 = x · 1,0361 − 144,33`.
- v2 dünyası → v2 kıta kutusu: `ky = y_v2 − 889`, `kx = x_v2 − 3200`.
- v2 kıta kutusu → bizim maske (`v2_olcek.json`, IoU 0,9768): `my = ky · 2,3786 + 1,8795`, `mx = kx · 2,376 + 1,4061`.
- Merak 16k → Merak 8k: `y8 = (y + 0,5) · 3859/7719 − 0,5`, `x8 = (x + 0,5) · 8000/16000 − 0,5`.

Kayıtların hepsi Nelder-Mead ile kara maskelerinin IoU'sunu en büyükleyerek bulundu (`merak_v2.py`, `merak_birlestir.py`).
Bizim yüksekliği Merak pikseline getiren hazır işlev: `merak_duzelt.bizim(y8, x8)`. Bizim maskede deniz olan ama v2'de kara olan
yerlerde `merak/v2_kita_kara_16bit.png` (v2 kıta kutusunda, `gri/65535 · 5693` m) yedeği kullanılır.

### 3.3 Parça etiketleri
`animasyon.parcalar()` bizim parçaları verir (değerler 1..8 = parça 1, 2, şerit, 3, 4, 5, 6, 7). Bunlar v2 kıta kutusuna
(`merak/v2_parca.npy`) ve Merak 8k çerçevesine taşınır. Etiket eşlemesi:

| etiket | parça | ad |
|---|---|---|
| 1 | 1 | kuzeybatı (Ulu Dağlar, Ak Kalkan, Mavi Dağlar) |
| 2 | 2 | kuzey (Çanak Sıraları, Uzak Sıra, Tuzak Çanağı) |
| 3 | şerit | 2'nin güney kuşağı (Mor Sıradağları) |
| 4 | 3 | doğu dil (Kızıl Basamaklar, Doğu Yay Dağları) |
| 5 | 4 | güneybatı (Köprü Dağları, Köz Yaylası, Köz Masifleri) |
| 6 | 5 | Sarı Sıradağları'nın doğu şeridi, Sarı Ön Havzası |
| 7 | 6 | iç denizdeki ada |
| 8 | 7 | Uzun Yarımada |

---

## 4. Kesinlikle dikkat edilecekler (öğrenilmiş dersler)

1. **Kenar yumuşatma yok.** Maskede ara gri istenmez; maske saf siyah beyaz verilir. Ölçek değiştirirken en yakın komşu ya da
   "yumuşak büyüt sonra eşikle" kullanılır.
2. **JPEG yok.** Merak dışa aktarımı ve bizim dosyalar PNG'dir. JPEG ovalarda birkaç gri adımı oynatır.
3. **Denizde kara benekleri.** Merak dışa aktarımında kıyı önünde 1 ile 30 piksellik çok sayıda kara beneği vardı (16k'da 152 parça)
   ve deniz seviyesine çok yakın sığlıklar (−1 ile −40 m) Merak'ta benek benek kara olarak çıkıyordu. `merak_temizle.py`:
   16k'da 30 pikselden (8k'da 8) küçük kara parçaları denize çevrilir, −40 m'den sığ deniz −40 m'ye indirilir. Sahibin maskesindeki
   gerçek adacıklar (en küçüğü yaklaşık 37 piksel, 16k) kalır.
4. **Denize dokunma.** Sahip deniz derinliğini Merak'ta kendisi ayarlıyor. Bir ara eklenen kıta sahanlığı (−12 ile −150 m) bazı
   yerlerde kara gibi göründüğü için geri alındı. Son dosyalarda deniz pikselleri Merak dışa aktarımındakiyle (temizleme dışında)
   gri değerine kadar aynıdır.
5. **Kıyı çizgisine dokunma.** Adacık ekleme ve kıyıyı girintileme denendi, sahip istemedi. Her betik sonunda
   `((yeni > S) != (eski > S)).sum() == 0` denetlenir.
6. **Elle işlenmiş piksellere dokunma.** Sahibin Merak'ta elle yaptığı yerler korunur; değişiklik yalnız "bizim" bölgelerde yapılır
   (bkz. 5.2).
7. **Gönderim sınırı.** Sohbet aracı 8000 pikselden geniş görüntüleri göndermez; 16k dosyalar zip içinde verilir. Zip ve 16k PNG'ler
   `.gitignore`'dadır; 8k sürümleri ve betikler depodadır.
8. **Görüntü boyutu.** 16000 × 7719 dizi float32 olarak 494 MB tutar. Betikler kıta çevresini kırparak ya da satır blokları halinde
   (1024 satır) çalışır. Kıta kırpma kutusu (16k): `y 1600..4200, x 6300..9700`.

---

## 5. Hat: hangi betik ne yapar (sırayla)

### 5.1 Hazırlık (eski, doğrusal kodlama)
| betik | girdi | çıktı | not |
|---|---|---|---|
| `merak_cikti.py` | Merak ekran görüntüsü | `merak_yukseklik_16bit.png`, `merak_maske.png` | ilk deneme, ekran görüntüsüne kayıt |
| `merak_dunya.py [GEN]` | bizim veri | `dunya_yukseklik_16bit.png`, `dunya_maske.png`, `dunya_olcek.json` | 2:1 tüm dünya, düz yerleşim (50°K ile 5°G, boylam ±36°), doğrusal kodlama |
| `merak_renk.py` | `dunya_yukseklik_16bit.png` | `dunya_renk_haritasi.png`, `dunya_renk_listesi.json` | "Colour map" sekmesi için 13 basamaklı renk haritası |
| `merak_v2.py MASKE.jpg` | sahibin kare maskesi | `v2_*` (8000 × 4000), `v2_olcek.json` | v2 maskesine oturmuş yükseklik, doğrusal kodlama |
| `merak_kalan.py`, `merak_yerlestir.py` | v2 | `kalan_*`, `yerlestir_*` | elle işleme referansları; Place on existing denemeleri |

### 5.2 Merak kodlamasıyla son hat
1. `merak_birlestir.py DISA_8K.png DISA_16K.png` → `birlesik_8k.png`, `birlesik_16k.png`, `*_platolu.png`, `birlesik_olcek.json`.
   - Kayıt: v2 → Merak (3.2).
   - "Elle dokunulmamış" kara: Merak'ın varsayılan düz arazisi, yani `E < 330 m` ve 9 piksellik pencerede standart sapma `< 25 m`,
     morfolojik açma/kapama, 400 pikselden küçük parçalar atılır; yalnız etiket 1, 5, 6, 7.
   - Bu kara bizim yükseklikle doldurulur; sınırda 15 pikselde (8k) karışır; kıyıda (denize karşı) geçiş yoktur.
   - Kıtadan 120 pikselden (8k) uzak okyanus tabana (3598) indirilir → test platoları ve lekeler silinir. `_platolu` sürümlerde
     platolar geri konur (içe aktarma denetimi için).
   - Bilinen eksik: etiket 8 (Uzun Yarımada) bu listede unutulmuştu; `merak_duzelt.py` ile kapatıldı.
2. `merak_duzelt.py GIRDI_16k OUT_16k` → sahibin işaretlediği iki bölgeyi (Mavi Dağlar'ın batısındaki düz şerit; Sarı Ön Havzası ve
   Uzun Yarımada) bizim yükseklikle değiştirir. Bölge çokgenleri 8k koordinatında (`BOLGE`), 15 piksel geçiş.
3. `merak_kiyi.py GIRDI_16k ONEK` → yalnız karada kıyı rampası: kıyıdan içeri `t = smoothstep(d / g)`, `g` 7 ile 31 km arası gürültülü
   genişlik; `h = max(h · (0,12 + 0,88 t), min(h, 3 + 25·min(d/4 km, 1)))`; kıyıdaki kabarık şerit iç ortalamaya göre bastırılır.
   Ölçüm öncesi: kıyıdan 2,5 ile 10 km içeride ortanca 350 ile 430 m (iç kesim 260). Sonrası: 2,5 km 85 m, 10 km 210 m.
   Deniz ve kıyı çizgisi aynen kalır. Çıktı `ONEK_16k.png`, `ONEK_8k.png` (8k: 16k'dan kutu ortalamasıyla, 8k maskesi
   `birlesik_8k`'dan zorlanır).
4. `merak_temizle.py ONEK...` → benekler ve sığlık (4. bölüm, madde 3). Çıktı `ONEK_temiz_16k.png`, `ONEK_temiz_8k.png`.
5. `merak_saf.py` → sahibin hiçbir katkısı olmadan, yalnız bizim yükseklik; kıyı ve deniz `birlesik_*`'tan. Çıktı `saf_16k.png`,
   `saf_8k.png` (sonra `merak_temizle.py merak/saf`).
6. `merak_uslup.py` ve `merak_uslup2.py` → "bizim" karayı sahibin üslubuna yaklaştırır (5.3). Çıktı `uslup_16k.png`, `uslup2_16k.png`
   ve ölçüm dosyaları `uslup_olcum.json`, `uslup2_olcum.json`. Bu iki betik `/tmp/.../scratchpad/` altındaki ara dizilere
   (`A16.npy` sahibin sürümü, `B16.npy` bizim sürüm, `O16.npy` ilk dışa aktarım, `LB16.npy` etiket) dayanır; yeniden üretmek için
   bu dizileri önce `son_temiz_16k`, `saf_temiz_16k`, Merak dışa aktarımı ve `LB8` etiketlerinden kıta kutusunu kırparak oluşturmak
   gerekir (`Y0, Y1, X0, X1 = 1600, 4200, 6300, 9700`).
7. `merak_levha.py` → Geography Lab için levha şeması (`levha_semasi.png`).
8. `merak_rehber.py` → elle işleme rehberleri (`rehber_dunya.png` saydam, 8000 × 3859; `rehber_kuzeybati/guneybati/ada.png`).

Son teslim edilen dosyalar ve anlamları:

| dosya (16k) | içerik |
|---|---|
| `son_temiz_16k.png` | sahibin elle işlediği + bizim dolgu + kıyı rampası + temizleme |
| `saf_temiz_16k.png` | yalnız bizim yükseklik, sahibin kıyısı ve denizi |
| `uslup2_16k.png` | `son_temiz` üstünde bizim bölgeler sahibin üslubuna göre yeniden yapılmış (en son sürüm) |

### 5.3 Üslup aktarımı (uslup2)
Sahibin yöntemi: genel hatlar korunur, küçük ayrıntı Merak'ın aşınma aracıyla deneme yanılma üretilir. Aktarım:

1. **Yükseklik eşleme.** Sahibin elle işlediği bölgede (etiket 2, 3, 4) iki sürümün 80 niceliği eşlenir; bizim yükseklik bu eğriyle
   dönüştürülür. Ölçüm: sahibin %10/%50/%99,5 dilimleri 206/919/4425 m, bizimkiler 114/748/3896 m.
2. **Taban.** Yalnız karada (deniz hesaba katılmaz) 6 piksellik (16k, yaklaşık 15 km) Gauss süzgeci. Dağlık yerde
   (20 piksellik pencerede standart sapma 80 ile 330 m arası) süzgeç 2 piksele kayar, sıraların biçimi korunur.
   50 km bandında sırt keskinleştirme: pozitif bant ×1,25, negatif ×1,05.
3. **Doku.** Sahibin elle işlediği bölgeden (kıyıdan 25 piksel içeride) `A − gauss(A, 6)` alınır, yüksekliğe göre genliğe bölünerek
   normalleştirilir. 128 × 128 piksellik yamalar rastgele seçilir, döndürülür, aynalanır ve Hann pencereleriyle yarı örtüşerek döşenir
   (yamalı doku sentezi). Genlik tablosu (taban yüksekliği → doku standart sapması): 207 m → 12 m, 503 → 51, 974 → 74,
   1500 → 170, 2448 → 321, 3389 → 268. Dağlık yerde doku ×(1 − 0,6k).
4. **Karışım.** Bizim bölge ağırlığı `W`: ilk dışa aktarımdaki düz kara + işaretli bölgeler + bunlara komşu kıyı bandı;
   sahibin karasına karşı 30 piksellik geçiş, denize karşı geçiş yok.

---

## 6. Doğrulama denetimleri (her çıktıda)

```python
a = np.asarray(Image.open(yeni)).astype(np.int32)
b = np.asarray(Image.open(referans)).astype(np.int32)
assert ((a > S) != (b > S)).sum() == 0          # kıyı çizgisi aynı
assert (a[b <= S] != b[b <= S]).sum() == 0      # deniz aynı (temizleme hariç)
```

Ek olarak gölgeli kabartma ile yan yana önizleme alınır (8k, kıta kutusu `y 800..2100, x 3150..4850`).

---

## 7. Sahibin sürümü ile bizim sürümün ölçülmüş farkları (8k, piksel ≈ 5 km)

- Mor Sıradağları: sahibinde yarı yükseklik genişliği 13 ile 45 piksel, bizde 40 ile 105; tepe hattı sahibinde 4000 ile 4700 m,
  bizde 2700 ile 4100 m (10 km ölçeğinde); orta kesimde tepe hattı sahibinde 10 ile 25 piksel güneyde.
- Mor Ön Ovası ortancası sahibinde 204 m, bizde 100 m. Tuzak Çanağı tabanı 964 m ile 801 m.
- 3'ün güney yarımadası: ortanca 404 ile 286 m, en yüksek 4618 ile 3267 m.
- Şerit kuşağında en yüksek 5979 m (sahip) ile 5636 m (biz).
- Kara alanının %21'i (sahip) ile %26'sı (biz) 200 m altında; %2,6 ile %1,5'i 3000 m üstünde; eğimi 5°'yi aşan %1,9 ile %1,4.

---

## 8. Kaynak veri hakkında bilinen sorunlar

- `arazi.batimetri` iç denizi sığlaştırmak yerine derinleştiriyor (`z*(1−0,35·ic) + ic·min(0, z)`): İç Deniz ve Güneydoğu Kanalı
  yaklaşık −7,4 km. Merak dosyalarında deniz Merak'tan geldiği için etkisi yok.
- `benzer.py`'de Avrupa ile Tarım dokuları arasındaki çokgen sınırı Mavi Dağlar'ın doğusunda kuzey güney düz bir dikiş bırakıyor
  (`saf` sürümünde görünür).
- Bizim haritada 3'ün güneydoğusunda bir deniz girintisi var; sahibin maskesinde orası kara. `saf` sürümünde orası v2 yedeğiyle
  doldurulduğu için pürüzsüz bir çukur gibi görünür.

---

## 9. Bilinmeyenler

- Merak'ın **içe aktarma** eğrisi platolarla ayrıca ölçülmedi. Dışa aktarma eğrisiyle aynı olduğu varsayıldı; `*_platolu.png` dosyaları
  bunu denetlemek için var (içe aktarıp platolardan birinin yüksekliğine bakmak yeterli: 2514 m olmalı).
- "Place on existing" sekmesinin saydamlığı ya da siyahı nasıl yorumladığı.
- Merak'ın içe aktarmada ince bir ayrıntı gürültüsü ekleyip eklemediği (sığ denizde benek çıkmasının olası sebebi).
- Merak aşınma aracının zirveleri ne kadar indirdiği.
- Geography Lab'de "Run 200 million years"ın mevcut araziyi ne kadar değiştirdiği.

---

## 10. Levhalar (Geography Lab için, `merak_levha.py`)

Yön pusula açısıdır (0 kuzey, 90 doğu); Merak'taki P5 = 59° okunun kuzeydoğuyu göstermesinden doğrulandı. Hızlar Kuzey Levhası
sabit kabul edilerek verildi (kaynak: `olaylar.LEVHALAR`).

| levha | kapsam | yön | cm/yıl |
|---|---|---|---|
| Kuzey | 1, 2, 4, iç denizin batısı, kuzey/batı/güney sahanlıkları | sabit | 0 |
| Doğu Dil | 3 ve doğu hendeğine kadar | 0° | 1,8 |
| Orta Blok | 5 | 270° | 2,8 |
| Uzun Yarımada | 7 | 315° | 4,6 |
| Ada | 6 | 180° | 0,7 |
| Doğu Havza | iç denizin doğusu ve güneyi | 315° | 0,8 |
| Doğu Okyanusu | doğu hendeğinin dışı | 270° | 6,5 |
| Batı Okyanusu | batıda, uzakta | 270° | 2,4 |
| Kutup | kuzeyde, uzakta | 0° | 0,6 |
| Güney Okyanusu | güneyde, uzakta (hız öneridir) | 180° | 1,5 |

Sınırlar: Kuzey–Doğu Dil ve Kuzey–Orta "Continental collision"; Doğu Dil–Uzun ve Doğu Dil–Orta "Divergent"; Orta–Uzun "Transform";
Kuzey–Ada "Divergent"; Doğu Havza–Ada "Subduction"; Doğu Havza'nın diğer kenarları "Transform"; Doğu Okyanusu–Doğu Dil "Subduction";
Doğu Okyanusu–Kuzey "Transform"; uzak okyanus sırtları "Divergent".
