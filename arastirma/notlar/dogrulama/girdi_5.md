# Doğrulama girdisi, parça 5 (1. belge, etiketsiz araç taraması)

Her satır 1. belgedeki bir iddiadır (`01:satır`). Hepsi etiketsizdi, yani kanıt düzeyi bilinmiyor.

- `01:162` Cordonnier ve diğerleri (2018): levha hareketinden kabuk kalınlaşma hızını hesaplayıp yükseltmeye çeviriyor, u = α · dq/dt; ortalama yükseltmeyi yılda yaklaşık 0,5 mm'ye ölçekliyor; sabit tarafta yükseltmeyi sıfırlayan yordamsal bir fay ekliyor. (Hangi makale olduğunu da doğrula: "Sculpting Mountains" TVCG 2018 olabilir; değilse gerçek makaleyi bul.)
- `01:163` Cortial ve diğerleri (2019, "Procedural Tectonic Planets"): yükseltme = çarpışma cephesine uzaklık, göreli levha hızı ve yüksekliğin çarpımı; kullanıcı çalışmasında tektonik gezegenler fraktal gezegenlere karşı 97'ye 47 oy aldı.
- `01:168` Tzathas ve diğerleri (2024): doğrudan bir sınır maskesi alıyor, maskelenen hücrelerin yüksekliği sabit kalıyor; problemin iyi tanımlı olması için yükseltme sınırda sıfıra inmeli.
- `01:169` FastFlow (2024): çıkış hücrelerini "deniz kıyılarında, alanın içinde" kabul ediyor.
- `01:171` Cordonnier ve diğerleri (2016): yalnızca alan kenarını deniz seviyesinde sabitliyor; sonucu en çok kıyıya yakın yükseltme eğimi belirliyor.
- `01:174` Braun ve Willett (2013): örtük, O(n) yöntem, koşulsuz kararlı; büyük zaman adımlarına (250 000 yıl) izin veriyor, 100 ile 300 adımda yakınsıyor.
- `01:176` Schott ve diğerleri (2024): düşük çözünürlüklü araziyi 32 katına kadar büyütüp hidrolojik olarak tutarlı ayrıntı ekliyor; kodu MIT lisanslı.
- `01:180` Otomatik ölçütler: Hack yasası uyumu için katsayı 1 ile 6, üs 0,45 ile 0,7 (Schott 2023); sıfır kırma hacmi (Schott 2024); referansa karşı hipsometri (Tzathas 2024); zirve ve boyun istatistikleri (Argudo 2019); geomorfon dağılımları (Argudo 2025, kodu MIT).
- `01:185` Galin ve diğerleri 2019 derlemesi: otomatik doğrulamanın genellikle "tutarlı drenaj testiyle sınırlı" kaldığını söylüyor.
- `01:120` Wilbur'un tarifi (Joe Slayton, ProFantasy forumu, 2020): çukur doldur; en yüksek yüksekliğin yaklaşık %5'i kadar mutlak gürültü ekle; yeniden doldur; akış birikimine dayalı oyma; hafif parçacık erozyonu.
- `01:128` goSPL son sürüm 2026.7.14, depoya Kasım 2026'da commit geliyor, GPL-3; Landlab 2.11.0 (Nisan 2026) MIT, pip; Badlands numpy 2'yi desteklemiyor ve yalnız bakım sürümleri alıyor; Fastscapelib 0.3.0'dan beri (Haziran 2025) yeni commit yok.
- `01:135` Utrecht "paleogeography calculator" (yükseklik kabuk kalınlığı ve izostaziden, okyanus derinliği taban yaşından) 2020'de duyuruldu ama kodu yayımlanmadı.
- `01:196` Gizli repoda `ubuntu-latest` 2 işlemci ve 8 GB; açık repoda 4 işlemci ve 16 GB; iş başına 6 saat.
