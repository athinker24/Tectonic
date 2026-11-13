# Gece görevi ilerlemesi

Görev (13 Kasım 2026 gecesi, sahip uyurken): maskenin öncesini kuran, çok dönemli, Dünya benzeri ayrıntılı bir tektonik tarih. Çıktılar: ayrıntılı topografik harita, dönemleri anlatan PDF, hareketli görüntü. Sıra: düşün, belge, görüntü. Bitince commit, push, SendUserFile ile üç çıktı. Sahibe ara mesaj yok.

Ölçek kararı: çerçeve 8000 km × 6122 km (görüntü 2000 px genişlikte 1 px = 4 km); enlem üstte 50°K, altta yaklaşık 5°G.

## Adımlar
- [x] Notlar ve sahibin kararları: notlar/KARARLAR.md
- [x] Uyandırıcılar: 01:15 ve 01:50 UTC
- [x] olaylar.py: dönemler, olaylar, levhalar (tek kaynak)
- [x] arazi.py: v1 hazır (cikti/topografya_v1.png). v2: `python3 arazi.py asinma_tam 4.0 5e-6 25` (log_tam2.txt), sonra `python3 arazi.py ciz_tam`; v2 kötüyse v1'i topografya.png olarak geri koy
- [x] animasyon.py: üretildi (v1 topografyayla); son topografyadan sonra yeniden koş
- [~] belge.py: kod hazır; en son `NODE_PATH=$(npm root -g) python3 belge.py` (cikti/tarih.pdf)
- [ ] commit, push, gönder
