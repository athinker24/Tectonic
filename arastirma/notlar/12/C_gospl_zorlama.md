# goSPL: Tektonik Zorlama (Levha Hareketi ve Yükselme Girdisi) Araştırma Notları

Durum: DEVAM EDİYOR. Bölüm 1, 4 ve 5 kısmen dolu; bölüm 2 ve 3 için kaynaklar taranıyor.

Etiketler: [B] tam metin, [B-öz] özet, [D] resmi belgelendirme, [Ö] arama özeti.
Erişim notu: WebFetch gospl.readthedocs.io için ENOTFOUND verdi; curl ile indirme başarılı (HTTP 200) ve metin oku.py ile çıkarıldı. github.com için curl 403 döndü (GitHub kaynak kodu okunamadı; ayrıca bkz. bölüm 5).

## Kaynak listesi

- K1 [D]: goSPL, Tectonic forcing (dev): https://gospl.readthedocs.io/en/dev/tech_guide/tecto.html
- K2 [D]: goSPL, Tectonic related parameters (kullanıcı kılavuzu): https://gospl.readthedocs.io/en/latest/user_guide/optfile2.html
- K3 [D]: goSPL, Required input file parameters: https://gospl.readthedocs.io/en/latest/user_guide/inputfile.html
- K4 [D]: goSPL, HPC scaling & performance: https://gospl.readthedocs.io/en/latest/user_guide/hpc_scaling.html
- K5 [D]: goSPL, Installation via Conda: https://gospl.readthedocs.io/en/latest/getting_started/installConda.html
- K6 [D]: goSPL kök sayfa (örnek araştırma listesi ve kaynak linkleri): https://gospl.readthedocs.io/en/latest/
- K7 [Ö]: Arama özeti, PyPI: https://pypi.org/project/gospl (sürümler 2026.6.12 / 2026.6.13 görüldü)
- K8 [B-öz]: JOSS makalesi (Salles 2020): https://joss.theoj.org/papers/10.21105/joss.02804.pdf (henüz okunmadı)

## Bulgular

### 1. Tektonik zorlama (yatay ve düşey)

- [D] Tektonik zorlama kullanıcı tanımlıdır; goSPL'in süreci (litosferik ya da manto kaynaklı) bilmediği ve sıkışma ile kabuk/tortu sıkışmasını hesaba katmadığı belirtiliyor. K1.
- [D] Zorlama, `tectonics:` bloğunda `start` ve `end` (yıl) ile tanımlanan olaylar dizisidir. Her olay ya `upsub` (yalnızca düşey), ya da `hdisp` (3B yer değiştirme hızı) içerir. K2.
- [D] Düşey girdi: `upsub: ['data/uplift20Ma','t']` gibi, anahtarı `t` olan bir `.npz` dosyası. Birim m/yıl. Düşey değer her düğüm için 1B vektör. K2, K1.
- [D] Yatay girdi: `hdisp: ['data/hdisp18Ma', 'hxyz']`, anahtarı `hxyz`, 3B dizi; x, y, z yönünde hız bileşenleri m/yıl. 2B ağlarda z bileşeni 0.0 verilir. K2.
- [D] Dosya formatı: TÜM girdi dosyaları numpy zip (`.npz`) olmak zorunda; netCDF ya da HDF5 değil. Bu, başlatmada hızlı yükleme sağlar. K3, K2. (Not: çıktılar HDF5 + XDMF'tir; girdi değil. Bkz. bölüm 3.)
- [D] Zaman adımı: düşey yer değiştirme her `dt` adımında uygulanır. `interp` yatay şeması DIŞINDAKİ yatay advection da her `dt` adımında yapılır. K2.
- [D] Zaman adımı (model): `time:` bloğunda `start`, `end` (yıl), `dt` (iç adım, örtük), `tout` (çıktı aralığı), `strat` (stratigrafi aralığı) ve `rstep` (yeniden başlatma). K3.
- [D] Advection şeması, `domain: advect:` anahtarında `upwind`, `iioe1`, `iioe2` veya `interp` olarak seçilir. K1, K3.
- [D] `interp` şeması (küresel ağ için, levha hareketi için): yatay hareket yalnızca tektonik aralığın SONUNDA (`end` zamanında) uygulanır. Aralık "birkaç bin ila milyon yıl" olabilir. K1, K2.
- [D] `upwind` ve `iioe1/2` şemaları 2B ağlar için tasarlandı; global (küresel) yüzey advection'ı "doğrulanmamış" (not edilmiş). K1.
- [D] Küresel `interp` yönteminde ağ yeniden üretilmez (remeshing yok); bunun yerine yer değiştirmiş noktalardan en yakın üç noktaya ters uzaklık ağırlıklı enterpolasyon yapılır (SciPy cKDTree). Tam eşleşen düğüm değerini aynen alır. "Verimli ama en doğru olmayabilir" diye not düşülmüş. K1.
- [D] Düğüm yoğunluğu advection ile zamanla değişir (seyrekleşme/yığılma); dokümantasyon bunu açıkça belirtiyor ve yine de ağı yeniden kurmadan ilerliyor. K1.
- [D] Stratigrafik kayıt: katmanlar tek tek advect edilmez; her zaman adımında yüzeyden sonra yarı-Lagrange ile taşınır. Uyarı: ters uzaklık enterpolasyonu kütle korumaz; uzun ve güçlü yatay hareketlerde toplam katman kalınlığı ile yüzey yüksekliği hafifçe ayrışabilir. K1.
- [D] Stratigrafi maliyeti: 1M düğümlü ağda her adımda bir katman kaydedilirse, katman taşıma çalışma süresinin yaklaşık %3'ü. K1.
- [D] Bir sınırlama: döngüsel (periodik, silindirik) 2B modeller yalnızca tek MPI süreci ile çalışır. K1.
- [D] Kaynak tanımı: yatay advection için levha hareketleri "plate-tectonic reconstruction software" çıktısından alınabilir (K1). Bu bağlamda GPlates adı sayfada geçmiyor (bkz. bölüm 2).

### 2. Levha hareketinin ızgaraya uygulanması, GPlates bağlantısı

- [B-öz] Hangi yazılım arandığında: pyGPlates/gospl-pygplates örneği için henüz tam metin bulunmadı. Arama özeti (K7 ya da [Ö]): "horizontal advection ... can be obtained from plate-tectonic reconstruction software". Doğrudan GPlates bağlantısı için kaynak bulunamadı: BULUNAMADI (henüz). Sonraki adım: goSPL-examples deposu ya da kılavuzun örnek bölümü.

### 3. Örnek kullanımlar, ızgara boyutu, süre, çekirdek, bellek

- [D] HPC ölçek testi (K4): üç küresel ağ, Gadi (48 çekirdekli düğümler):
  - 10 km ağ: 5.9 milyon düğüm, 11.8 milyon yüzey; en küçük çalışan çekirdek sayısı 16; düğüm başına RSS ~6.6 GB. Adım sayısı sabit (ölçüm: sabit sayıda model adımı, I/O kapalı). 16 çekirdek: 521.3 s; 240 çekirdek: 46.9 s (hızlanma 11.1x, verim 0.74); 288: 44.4 s (verim 0.65).
  - 8 km ağ: 9.2 milyon düğüm; en küçük 24 çekirdek; RSS ~9.9 GB; 24 çekirdek 800.7 s; 96 çekirdek 194.7 s.
  - 5 km ağ: 23.7 milyon düğüm; en küçük 96 çekirdek; RSS ~24 GB (rank 0'da yoğunlaşıyor; ortalama ~3 GB). 48 çekirdek tek 192 GB düğümde OOM ile öldürülüyor. K4.
- [D] "Bir global ağ çok düşük çekirdek sayısında bellekten sığmaz; 10 km ağ 16 çekirdekten az başlatılamaz." K4.
- [D] Bu ölçekler yalnızca çekirdek/bellek ölçekleme tanımı; tam simülasyon süresi (ör. Kenozoyik, 65 Ma) ve bu yayınlardaki sonuçlar BULUNAMADI (henüz). Sonraki adım: kök sayfadaki Salles 2023/2024 ve PNAS 2025 makale bağlantılarını (K6) okumak.
- [D] Kök sayfa (K6) örnek araştırmalar listesi bağlantıları: Nature 2023 (10.1038/s41586-023-06777-z), Nature Communications 2024 (10.1038/s41467-024-47662-1), Science 2023 (10.1126/science.add2541), PNAS 2025 (10.1073/pnas.2516468122), ESurf 2025 (esurf.copernicus.org/articles/13/683/2025/), JGR Earth Surface 2025 (10.1029/2025JF008473), PLOS ONE 2025 (10.1371/journal.pone.0332766), Scientific Reports 2022 (s41598-022-23206-9). Bu makalelerin içeriği henüz okunmadı; hangisinin "Kenozoyik küresel" ya da "paleo-erozyon" olduğu doğrulanmadı.

### 4. Badlands ve Pecube ile fark

- BULUNAMADI (henüz). Sonraki adım: Badlands ve Pecube kılavuzu ya da makalesi.

### 5. Lisans, kurulum, GitHub Actions uygunluğu

- [Ö] Lisans: GPL (kaynak: arama özeti, K7). Resmî metin ve dosya henüz doğrulanmadı.
- [D] Kurulum (conda, K5): `mamba create -n gospl -c geodels -c conda-forge gospl`. `-c conda-forge` zorunlu; aksi halde petsc4py, mpi4py, pyshtools, vtk gibi bağımlılıklar conda-forge'dan çözülmez. Güncel sürüm kayıtlarında v2026.7.14 listelenmiş. K5.
- [D] HPC kurulumu: Intel MPI, HDF5, PETSc 3.21.3, netCDF, MKL, Python 3.11 modülleri; h5py ve hdf5 MPI bağlantılı olmalı (paralel HDF5 yazımı için; nompi varyantı sessizce hata verir). K5, kılavuzun HPC sayfası (dl2/74e352fe88 metni).
- [D] Bağımlılıklar (kılavuz): mpi4py, petsc4py, h5py (MPI bağlantılı), netCDF4. K-doc (dl2/dda28dbd5a).
- [D] Çıktılar: HDF5 + XDMF; bu nedenle girdi NetCDF değildir, ama çıktı için netCDF4 kullanılır (CF-NetCDF ara dönüşüm aracı var). K-doc.
- Bellek varsayımı (16 GB, 2-4 çekirdek) İLE benchmark değerleri: 10 km ağ 16 çekirdekte düğüm başına ~6.6 GB; 16 GB'lık bir çalışma ortamında 2-4 çekirdek bu ağ için BAŞLATILAMAZ (K4'e göre en az 16 çekirdek gerekir). 8 ve 5 km ağlar daha da fazlasını ister. Sonuç: GitHub Actions ortamı (2-4 çekirdek, 16 GB) küresel ağ için yeterli değil; yalnızca çok kaba (dolayısıyla bu benchmark'tan farklı, küçük) ağlarla ya da 2B/yerel modelle ileri test yapılabilir. Bu kaba ağ için bellek/süre ölçümü BULUNAMADI.
- [D] Sınırlama: döngüsel 2B modeller yalnızca seri çalışır (K1).

## Açık sorular (sonraki turda)

1. goSPL-examples deposundaki gospl-pygplates örneğinin tam metni (Bölüm 2).
2. Kök sayfadaki makalelerin (özellikle Salles 2023/2024 ve PNAS 2025) süre ve ızgara ayrıntıları (Bölüm 3).
3. Badlands ve Pecube karşılaştırması (Bölüm 4).
4. Resmi lisans dosyası (Bölüm 5).
5. GitHub kaynağı github.com üzerinden curl ile 403 aldı; alternatif kaynak (PyPI sayfası, conda paket meta verisi) gerekebilir.
