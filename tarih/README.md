# Dünyam tektonik tarihi

Sahibin sabit kıyı maskesinin (`maske.png`) öncesini kuran tarih ve ondan türetilen topografya.

- `olaylar.py`: tek kaynak. Ölçek ve enlem, parça sınırları, hareket anahtar kareleri, bugünkü levhalar, dönemler ve olaylar, yer şekilleri.
- `arazi.py`: yapı katmanı (kuşaklar, yaylalar, ovalar, volkanlar) + yağış + fastscapelib aşınması + gölgeli topografik harita.
  Sıra: `python3 arazi.py yapi`, `python3 arazi.py asinma 3.0`, `python3 arazi.py ciz 2`.
- `benzer.py` ve `dem.py`: Dünya karşılıklarıyla topografya (bugünkü ana harita). Her bölgeye gerçek bir yerin yükseklik modeli
  (AWS Terrain Tiles) döndürülüp ölçeklenerek, aynalanıp bükülerek yerleştirilir. Sıra: `python3 benzer.py bilesik`, `python3 benzer.py ciz`;
  karşılıkların tek tek önizlemesi `python3 benzer.py onizle`. Karolar `kaynak/karolar/` altında önbelleğe alınır (git dışı).
  Kurallarla kurulan önceki harita `cikti/topografya_kural.png` olarak duruyor.
- `animasyon.py`: 340 milyon yıldan bugüne katı parça geri kurgusu; `cikti/animasyon.mp4`, `cikti/animasyon.gif`, `cikti/donem/`.
- `belge.py`: dönemleri anlatan PDF (`cikti/tarih.pdf`); Chromium ile basılır: `NODE_PATH=$(npm root -g) python3 belge.py`.
- `notlar/`: danışmadaki kararlar ve ölçümler.

Ölçek: çerçeve 8000 km × yaklaşık 6100 km; üst kenar 50°K, alt kenar yaklaşık 5°G.
