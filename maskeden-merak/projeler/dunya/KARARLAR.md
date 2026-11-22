# Dünya ölçeğinde deneme: kararlar

Sahip "dünya boyutlarında bir şey dene" dedi; aşağıdakilerin hepsi seçimim.

- Maske: `maske_dunya.py 30218 maske.png`, 5400 × 2700, 1 piksel = 1/15 derece (ekvatorda 7,4 km), tüm gezegen
  (90°K ile 90°G, 180°B ile 180°D). Kara payı 0,290. Kara, kutuplardan (68° ötesi) ve tarih değiştirme çizgisinden uzak tutuldu
  (Merak çerçevesinin iki yanındaki 281 piksellik şeritte kara yok).
- `"kure": true`: maske pikseli her yerde aynı derece; karşılıklar doğu batı yönünde cos(enlem) ile düzeltilir (yerel
  sinüzoidal izdüşüm, `karsilik._kure_x`). Özellik adımlarına (sırt dokusu, yama) bu düzeltme uygulanmıyor; bu projede özellik yok.
- Parçalar: bati, kuzey, dogu, guney, gb (güneybatı), adalar, gada (güneydeki ada).
- Karşılıklar: bati = Afrika (aynalı), kuzey = Avrasya, dogu = Güney Amerika (aynalı; And benzeri sıra doğu kıyısında),
  guney = Kuzey Amerika (180° döndürülmüş), gb = Moğolistan, adalar = Kayalık Dağlar parçası, gada = İzlanda.
  Büyük karşılıklarda 5 ile 8 denetim noktası kıyı uçlarını kaynağın kıyı uçlarına bağlar (kaynakta denize düşen pay
  Afrika %23 → 0, Avrasya %18 → 0).
- Avrasya'nın Tibet'i güney kıyısında geniş, düz bir yayla düğümü yaptı (sahibin yasakladığı biçim). Üstüne İran ve Anadolu
  karşılığı (öncelik 3) kondu; düğüm kalktı, yerine havzalı sıralar geldi.
- Ovalar için yükseklik eğrilerinin alt ucu korunur (200 m → 150 m, 600 m → 320 m); dağlar Kafkas ile Alp ölçeğine indirildi.
