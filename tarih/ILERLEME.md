# Gece görevi ilerlemesi

Görev (13 Kasım 2026 gecesi, sahip uyurken): maskenin öncesini kuran, çok dönemli, Dünya benzeri ayrıntılı bir tektonik tarih. Çıktılar: ayrıntılı topografik harita, dönemleri anlatan PDF, hareketli görüntü. Sıra: düşün, belge, görüntü. Bitince commit, push, SendUserFile ile üç çıktı. Sahibe ara mesaj yok.

Ölçek kararı: çerçeve 8000 km × 6122 km (görüntü 2000 px genişlikte 1 px = 4 km); enlem üstte 50°K, altta yaklaşık 5°G.

## Adımlar
- [x] Notlar ve sahibin kararları: notlar/KARARLAR.md
- [x] Uyandırıcılar: 01:15 ve 01:50 UTC
- [x] olaylar.py: dönemler, olaylar, levhalar (tek kaynak)
- [~] arazi.py: yapı tamam; aşınma: `python3 arazi.py asinma 3.0`, sonra `python3 arazi.py ciz 2` (cikti/topografya.png)
- [~] animasyon.py: kod hazır ve sınandı; topografya bitince `python3 animasyon.py` (cikti/animasyon.mp4, .gif)
- [~] belge.py: kod hazır; en son `NODE_PATH=$(npm root -g) python3 belge.py` (cikti/tarih.pdf)
- [ ] commit, push, gönder
