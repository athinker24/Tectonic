"""Dönemleri anlatan PDF: HTML üretir, Chromium ile PDF'e basar.

Kullanım: python belge.py
Çıktı: cikti/tarih.pdf (ve cikti/tarih.html)
"""
import base64
import io
import os

import numpy as np
from PIL import Image

import olaylar as O

NEDEN = {
    "Mor Sıradağları": "3'ün 2'nin altına girdiği etkin çarpışma (50 milyon yıldır). Kabuk iki katına kalınlaştı. Doğuya doğru yükselir, çünkü 3 dönerek geliyor ve doğu ucu daha hızlı sıkışıyor.",
    "Kuzey Kenar Sırası": "Mor Yaylası'nın kuzey kenarı; yayla kabuğu kuzeydeki sert 2 kabuğunun üzerine itiliyor.",
    "Şerit Sırtları": "210 milyon yıl önceki İnce Şerit dikişlerinin Mor çarpışmasıyla yeniden sıkışması.",
    "Uzak Sıra": "Çarpışmanın 1000 km kuzeyde yeniden canlandırdığı eski dikişler; yaklaşık 28 milyon yıldır yükseliyor.",
    "Mavi Dağlar": "430 milyon yıl önceki 1 ile 2 çarpışmasının aşınmış kökü; sonraki dönemlerde hafifçe yeniden yükseldi.",
    "Ulu Dağlar": "1,1 milyar yıl önceki İlk Birlik çarpışmasının kalıntısı; çok yaşlı, yuvarlak sırtlar.",
    "Köprü Dağları": "4'ün makas biçiminde dönerek açılmasıyla sıkışan kara köprüsü (95 ile 40 milyon yıl önce, Pireneler benzeri).",
    "Köz Masifleri": "320 milyon yıl önceki Köz orojeninin granit kökleri; 4'ün içinde alçak, yuvarlak masifler.",
    "Sarı Sıradağları": "5'in 4'ün altına girdiği genç ve etkin çarpışma (8 milyon yıldır). En yüksek güney orta kesimde, çünkü 5'in güney ucu önce çarptı. Hızla yükselip hızla aşınıyor.",
    "Kanal Omzu (3)": "Güneydoğu kanalının yarılmasıyla 3'ün batı kenarında yükselen omuz; kanala dik bir basamak.",
    "Kanal Omzu (5)": "Aynı yarığın 5 tarafındaki daha alçak omuz.",
    "Uzun Yarımada Sırtı": "7, kanal fayı boyunca kuzeybatıya kayarken 5'e bastırıyor; sıkışmalı yanal kayma dar ve dik bir sırt yükseltti (Sina benzeri).",
    "Doğu Yay Dağları": "Doğu Okyanusu'nun 3'ün altına dalmasıyla oluşan volkanik yay (60 milyon yıldır, And benzeri).",
    "Kanca Yayı": "Doğu yayının kıvrılan kuzey ucu; genç volkan adaları ve yarımada.",
    "Güneydoğu Yay Dağları": "Doğu yayının güney ucu; volkanlar ve deniz basmış vadiler.",
    "Ada Omurgası": "6'nın yay ardı gerilmesinde kalan sırtı; güneye uzanan parmaklar yükselmiş bloklar, aralarındaki körfezler çöküntüler.",
    "1 İç Deniz Omzu": "Makas açılmasında 1'in iç denize bakan kenarında yükselen yarık omzu.",
    "Doğu Düğümü": "Mor çarpışmasının doğu köşesi; sıkışma en büyük, kıyıya kadar inen yüksek ve dik dağlar.",
}
PLATO_NEDEN = {
    "Mor Yaylası": "İnce Şerit kabuğunun Mor çarpışmasıyla kalınlaşması; ortalama yaklaşık 4,3 km, içinde kapalı havzalar ve tuz gölleri.",
    "Kum Havzası": "Uzak Sıra ile Mor Yaylası arasında sıkışan sert blok; çevresindeki dağlar üzerine bindirdiği için çöken, denize akışı olmayan çöl havzası.",
    "Kızıl Basamaklar": "66 milyon yıl önce sıcak nokta üzerinden geçerken 3'ün ortasını örten taşkın bazaltları; basamaklı yamaçlar.",
    "Kuzey Tuzakları": "252 milyon yıl önceki büyük bazalt püskürmesi; aşınmış, derin vadili bazalt yaylası.",
    "Köz Yaylası": "Köz orojeninin aşınmış ve düzleşmiş yüzeyi; 4'ün iç yaylası.",
}


BOLGELER = [
    ("1 (kuzeybatı)", "Kıtanın en eski ve en sakin parçası. Kuzeyinde Ak Kalkan: alçak, buzulların kazıdığı, sayısız gölle kaplı bir ova; "
     "kuzey kıyısı fiyortlu. Batı kıyısı boyunca Ulu Dağlar'ın yuvarlak sırtları uzanır. Doğu sınırı Mavi Dağlar: 430 milyon yıllık "
     "dikişin üzerindeki yaylalar, kuzey ucunda dikiş hattını izleyen uzun fiyort. Güneydoğuda iç denize bakan kıyı, makas açılmasının "
     "yarık omzudur; dik bir basamakla denize iner. Batı rüzgârları batı kıyısını nemli tutar, iç kesimler daha kuru ve karasaldır."),
    ("2 (kuzeydoğu)", "Kıtanın en büyük parçası; iki ayrı dünyayı birleştirir. Kuzeyi Boz Kalkan ve Kır Çekirdeği: düz, göllü, ormanlık "
     "ovalar; ortasında Kuzey Tuzakları'nın basamaklı bazalt yaylası. Güney kuşağı İnce Şerit'tir ve bugün Mor Yaylası olarak 4 km'nin "
     "üstündedir. Yaylanın kuzeyinde Kum Havzası çölü ve daha kuzeyde Uzak Sıra; doğusunda Derin Göl yarığı ve doğuya kaçan blok. "
     "Bu güney kuşağı kıtanın deprem ve dağ oluşumu bakımından en etkin bölgesidir."),
    ("3 (doğu dil)", "Güney Kıtası'ndan kopup 150 milyon yılda yaklaşık 5600 km yol alan parça. Kuzey kenarı 2'nin altına dalıyor ve önünde "
     "Mor Ön Ovası uzanıyor; ovanın ana nehri batıya akıp üçgen koyda delta kurar. Ortası Kızıl Basamaklar bazaltlarıyla örtülü, kurak ve "
     "basamaklı bir yayla. Doğu kıyısı etkin bir volkan yayı: Doğu Yay Dağları, Kanca Yayı ve güneydoğu yarımadası; açığında 7 km'yi "
     "aşan Doğu Hendeği. Batı kıyısı güneydoğu kanalının yarık omzu."),
    ("4 (güneybatı)", "Kuzey Kıtası'na 370 ile 320 milyon yıl önce eklenen parçaların toplamı; Köz orojeninin aşınmış masifleri ve yaylası. "
     "130 ile 85 milyon yıl önce makas gibi dönerek 1'den ayrıldı; batıda kara köprüsü sıkışıp Köprü Dağları oldu. Doğu kenarında genç "
     "Sarı Sıradağları yükseliyor. Güney kıyısı ekvatora yakın; son buzul çağından sonra yükselen denizin boğduğu dallı nehir vadileri "
     "bugünkü girintili kıyıyı oluşturur."),
    ("5 (güney orta)", "3'ten 22 milyon yıl önce kopan ve batıya sürüklenerek 4'ün altına dalan mikro levha. Batı yarısı Sarı Sıradağları'nın "
     "önündeki çöküntü havzası, doğu kenarı kanal yarığının alçak omzu. Yer şekilleri kıtanın en genci; depremler ve hızlı aşınma sürüyor."),
    ("6 (iç deniz adası)", "Bir zamanlar 1'in güneydoğu kıyısına bitişik olan, 4 ile birlikte dönen ve 25 milyon yıldır altındaki levhanın "
     "geri çekilmesiyle gerilen blok. Güneye uzanan parmak biçimli yarımadalar yükselmiş bloklar, aralarındaki derin körfezler "
     "çöküntülerdir. Güney açığındaki küçük adalar etkin volkanlardır."),
    ("7 (güneydoğu yarımadası)", "5'in güney ucundan kesilip kanal fayı boyunca yaklaşık 980 km kuzeybatıya taşınan dar parça. 5'e bastırdığı için "
     "ortasında dar ve dik bir sırt var. Kuzeyindeki dar girinti ilerlemeden kalmış bir yarık kolu, doğusundaki kanal ise düz ve dik "
     "kıyılı bir yanal fay vadisidir."),
]


def img64(yol, gen=None, kalite=82):
    im = Image.open(yol).convert("RGB")
    if gen and im.width > gen:
        im = im.resize((gen, int(im.height * gen / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=kalite)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def profiller():
    """Bugünkü yüzeyden iki kesit: Mor çarpışmasını kuzey güney, Sarı çarpışmasını doğu batı keser."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    z = np.load("cikti/son_z.npy").astype(float)
    ny, nx = z.shape; g = nx / O.GEN; hk = O.KM_PX / g
    fig, ax = plt.subplots(2, 1, figsize=(9, 5.2), dpi=150)
    for a, (ad, p0, p1, etiket) in zip(ax, [
        ("Kesit A: kuzeyden güneye, x = 1450 (2, Kum Havzası, Mor Yaylası, Mor Sıradağları, 3)", (1450, 150), (1450, 1150),
         [(230, "Uzak Sıra"), (370, "Kum Havzası"), (470, "Kuzey Kenar Sırası"), (540, "Mor Yaylası"), (615, "Mor Sıradağları"), (700, "Mor Ön Ovası"), (950, "Kızıl Basamaklar")]),
        ("Kesit B: batıdan doğuya, y = 1180 (4, Sarı Sıradağları, 5, kanal, 3)", (400, 1180), (1500, 1180),
         [(560, "Köz Yaylası"), (728, "Sarı Sıradağları"), (820, "Sarı Ön Havzası"), (960, "kanal"), (1060, "Kanal Omzu"), (1250, "Kızıl Basamaklar"), (1480, "Doğu Yay")])]):
        n = 600
        xs = np.linspace(p0[0], p1[0], n) * g; ys = np.linspace(p0[1], p1[1], n) * g
        from scipy import ndimage
        zz = ndimage.map_coordinates(z, [ys, xs], order=1)
        d = np.linspace(0, np.hypot(p1[0] - p0[0], p1[1] - p0[1]) * O.KM_PX, n)
        a.fill_between(d, -6000, zz, where=zz >= 0, color="#b49a74", lw=0)
        a.fill_between(d, zz, 0, where=zz < 0, color="#7aa6cf", lw=0)
        a.fill_between(d, -6000, zz, where=zz < 0, color="#8a8a8a", lw=0)
        a.plot(d, zz, color="#3a2a20", lw=0.8)
        a.set_ylim(-4500, 8000); a.set_xlim(0, d[-1])
        a.set_title(ad, fontsize=8.5, loc="left")
        a.set_ylabel("m", fontsize=8); a.tick_params(labelsize=7)
        for k, t in etiket:
            q = (k - (p0[1] if p0[0] == p1[0] else p0[0])) * O.KM_PX
            a.annotate(t, (q, 7300), fontsize=6.5, ha="center", color="#5a2a1a")
    ax[1].set_xlabel("km (düşey abartma çok büyük)", fontsize=8)
    fig.tight_layout(); fig.savefig("cikti/kesitler.png"); plt.close(fig)


def zaman_cizelgesi():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=150)
    renk = ["#8c6d5a", "#9b7b63", "#a98a6c", "#7d93a8", "#6d8bb0", "#9a8f6a", "#b08a5a", "#7aa07a", "#a0b46a", "#c99a5a", "#c86e4e", "#d28c3c", "#8fb8d8"]
    f = lambda t: np.log10(t + 1)
    for i, D in enumerate(O.DONEMLER):
        a, b = D["aralik"]
        ax.barh(0, f(a) - f(b), left=f(b), color=renk[i % len(renk)], edgecolor="white", height=0.6)
        ax.text((f(a) + f(b)) / 2, 0.36, D["ad"], ha="left", va="bottom", fontsize=6.3, rotation=35, rotation_mode="anchor")
    for D in O.DONEMLER:
        for ty, bas, ac in D["olaylar"]:
            ax.plot([f(ty)], [-0.42], marker="|", color="#5a2a1a", ms=7)
    tik = [0, 1, 3, 10, 30, 100, 300, 1000, 3000]
    ax.set_xticks([f(t) for t in tik]); ax.set_xticklabels([str(t) for t in tik], fontsize=7)
    ax.set_xlim(f(3500), f(0) - 0.02); ax.set_ylim(-0.7, 2.6); ax.set_yticks([])
    ax.set_xlabel("milyon yıl önce (logaritmik ölçek; çentikler olaylar)", fontsize=7.5)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig("cikti/zaman.png"); plt.close(fig)


def hiz_tablosu():
    """Anahtar karelerden hız: parça ağırlık merkezinin yer değiştirmesi (km / milyon yıl = mm/yıl)."""
    satir = []
    for ad, ad_tr in (("3", "3 (Doğu Dil)"), ("serit", "İnce Şerit"), ("4", "4 (makas dönüşü)"), ("6", "6 (ada)")):
        kf = O.HAREKET[ad]
        for (t0, a0, x0, y0), (t1, a1, x1, y1) in zip(kf[:-1], kf[1:]):
            if t1 > 340 or (x0 == x1 and y0 == y1 and a0 == a1):
                continue
            km = np.hypot(x1 - x0, y1 - y0) * O.KM_PX
            v = km / (t1 - t0) / 10.0  # cm/yıl
            don = abs(a1 - a0) / (t1 - t0)
            satir.append((ad_tr, f"{t1:g} ile {t0:g}", f"{km:,.0f}".replace(",", "."), f"{v:.1f}".replace(".", ","), f"{don:.2f}".replace(".", ",")))
    return satir


def html():
    st = """
    <style>
    @page { size: A4; margin: 16mm 15mm 16mm 15mm; }
    body { font-family: 'DejaVu Serif', Georgia, serif; font-size: 10.5pt; line-height: 1.45; color: #222; }
    h1 { font-family: 'DejaVu Sans', sans-serif; font-size: 26pt; margin: 0 0 4mm 0; color: #3a2a20; }
    h2 { font-family: 'DejaVu Sans', sans-serif; font-size: 15pt; color: #6a2e1e; border-bottom: 1px solid #c9b8a8; padding-bottom: 1mm; margin-top: 7mm; }
    h3 { font-family: 'DejaVu Sans', sans-serif; font-size: 11.5pt; color: #444; margin-bottom: 1mm; }
    .alt { color: #777; font-size: 9pt; }
    table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 2mm 0 4mm 0; }
    th, td { border-bottom: 1px solid #ddd; padding: 1.2mm 1.5mm; text-align: left; vertical-align: top; }
    th { background: #f1ebe4; font-family: 'DejaVu Sans', sans-serif; }
    img.tam { width: 100%; border: 1px solid #ccc; }
    .yan { display: flex; gap: 4mm; align-items: flex-start; }
    .yan img { width: 48%; border: 1px solid #ccc; }
    .sayfa { page-break-before: always; }
    .kutu { background: #f7f3ee; border-left: 3px solid #b07a5a; padding: 2mm 3mm; margin: 3mm 0; }
    </style>"""
    p = ["<html><head><meta charset='utf-8'>", st, "</head><body>"]
    p.append("<h1>Dünyam: kıtanın tektonik tarihi</h1>")
    p.append("<p class='alt'>Kıyı şekli sahibin maskesidir ve değişmez; bu belge o kıyının öncesini kurar. "
             f"3,4 milyar yıldan bugüne {len(O.DONEMLER)} dönem, {sum(len(D['olaylar']) for D in O.DONEMLER)} olay, bugün {len(O.LEVHALAR)} levha.</p>")
    if os.path.exists("cikti/topografya_etiketli.png"):
        p.append(f"<img class='tam' src='{img64('cikti/topografya_etiketli.png', 1800)}'>")
        p.append("<p class='alt'>Bugünkü topografya: tarihten türetilen yapı (kuşaklar, yaylalar, havzalar, volkanlar) ve "
                 "üzerinde 3 milyon yıllık akarsu ve yamaç aşınması. Kar çizgisi enleme bağlı; kurak bölgeler sarımsı.</p>")
    # varsayımlar
    p.append("<h2>Çerçeve ve varsayımlar</h2>")
    p.append("<p>Harita çerçevesi doğu batı yönünde 8000 km, kuzey güney yönünde yaklaşık 6100 km kabul edildi; kara yaklaşık "
             "28 milyon km² eder, Afrika'dan biraz küçük. Çerçevenin üst kenarı 50°K, alt kenarı yaklaşık 5°G. Bu seçimle Mor "
             "Sıradağları 28 ile 33°K arasına, Mor Yaylası 30 ile 35°K arasına düşer; bu enlemler Himalaya ve Tibet'inkine yakındır, "
             "kar çizgisi ve iklim kuşakları da buna göre davranır. Kuzey kıyıları 45°K'nin üstünde, buzul çağlarında buzla "
             "örtülmüş; güney kıyıları ekvatorda.</p>")
    p.append("<div class='kutu'><b>Sahibin kararları</b> (danışmada verildi): kıyı sabit; parçalar 1 ile 7 ve çizgileri; batı ve merkezdeki "
             "karşılıklı kıyılar birbirini tamamlar; 1, 4 ve 6 bitişikti; 5, 3'ün batısına bitişikti ve sonra batıya gitti; "
             "etkin çarpışmalar 3 ile 2 (3 altta) ve 5 ile 4 (5 altta); 7 ayrı bir parça.<br><b>Benim seçimlerim</b> (sahip yanıt "
             "vermedi): Sarı Sıradağları en yüksek güney orta kesimde; 7 ile 5 arası sıkışmalı yanal kayma; Mor çarpışması uzun "
             "(50 milyon yıl), Sarı çarpışması yeni (8 milyon yıl); ölçek ve enlemler; bütün olayların zamanları, hızları ve adları.</div>")
    zaman_cizelgesi()
    p.append("<h2>Zaman çizelgesi</h2>")
    p.append(f"<img class='tam' src='{img64('cikti/zaman.png', 1500)}'>")
    # levhalar
    p.append("<h2>Bugünkü levhalar</h2><table><tr><th>Levha</th><th>Tür</th><th>Kapsadığı</th><th>Hareket (Kuzey Levhası'na göre)</th></tr>")
    for a, b, c, d in O.LEVHALAR:
        p.append(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>")
    p.append("</table>")
    if os.path.exists("cikti/donem/t000.png"):
        p.append(f"<img class='tam' style='width:70%;margin-left:15%' src='{img64('cikti/donem/t000.png', 1000)}'>")
    # dönemler
    kare = {"Köz orojeni ve Büyük Birlik": [340, 300], "Mor kaması ve İnce Şerit": [250, 210], "Büyük Birlik'in parçalanması": [170, 130],
            "Makas açılması": [100, 85], "Kuzeye koşu": [66, 50], "Mor çarpışması": [50, 35], "İç deniz evresi": [22, 10]}
    p.append("<h2 class='sayfa'>Dönemler</h2>")
    p.append("<p>Aşağıdaki dönemler en eskiden en yeniye sıralı. Her dönemin sonunda o dönemin olayları ve, 340 milyon yıldan "
             "sonrası için, levha haritaları var. Haritalarda kırmızı dişli çizgiler dalma zonları (dişler üstteki levhada), beyaz "
             "çift çizgiler okyanus sırtları, turuncu çizgi yarık. Kahverengi Güney Kıtası çerçevenin dışına uzanır ve şematiktir.</p>")
    for i, D in enumerate(O.DONEMLER, 1):
        a, b = D["aralik"]
        p.append(f"<h3>{i}. {D['ad']} <span class='alt'>({a:g} ile {b:g} milyon yıl önce)</span></h3>")
        p.append(f"<p>{D['ozet']}</p>")
        p.append("<table><tr><th style='width:16%'>Zaman (MYÖ)</th><th style='width:26%'>Olay</th><th>Açıklama</th></tr>")
        for ty, bas, ac in D["olaylar"]:
            p.append(f"<tr><td>{ty:g}</td><td>{bas}</td><td>{ac}</td></tr>")
        p.append("</table>")
        if D["ad"] in kare:
            ims = [f"cikti/donem/t{t:03d}.png" for t in kare[D["ad"]] if os.path.exists(f"cikti/donem/t{t:03d}.png")]
            if ims:
                p.append("<div class='yan'>" + "".join(f"<img src='{img64(q, 700)}'>" for q in ims) + "</div>")
    if os.path.exists("cikti/kesitler.png"):
        p.append("<h2 class='sayfa'>İki kesit</h2><p>Bugünkü yüzeyden alınmış iki kesit. A kesiti Mor çarpışmasının bütün "
                 "basamaklarını gösterir: kuzeyde sert 2 kabuğu ve Uzak Sıra, arada Kum Havzası, yaylanın dik kuzey kenarı, "
                 "4 km'yi aşan yayla, en yüksek sıradağ ve önünde alçak ön ova. B kesiti genç Sarı çarpışmasını ve güneydoğu kanalının "
                 "yarık omzunu keser.</p>")
        p.append(f"<img class='tam' src='{img64('cikti/kesitler.png', 1600)}'>")
    # hızlar
    p.append("<h2 class='sayfa'>Hızlar</h2><p>Hızlar parçaların ağırlık merkezlerinin geri kurgudaki yer değiştirmesinden "
             "hesaplandı (Kuzey Levhası sabit). Dünya'daki karşılaştırma için: Hindistan'ın en hızlı dönemi yılda 15 cm'nin üstü, "
             "bugünkü Hindistan Avrasya yakınlaşması yılda yaklaşık 4 ile 5 cm, Arabistan yılda 2 cm civarı.</p>")
    p.append("<table><tr><th>Parça</th><th>Aralık (MYÖ)</th><th>Yol (km)</th><th>Ortalama hız (cm/yıl)</th><th>Dönüş (°/milyon yıl)</th></tr>")
    for r in hiz_tablosu():
        p.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    p.append("</table>")
    p.append("<p>5 ve 7 için: 5, 22 milyon yılda yaklaşık 700 km batıya gitti (yılda ortalama 3,2 cm) ve yaklaşık 24° saat yönünde döndü. "
             "7, 3'e göre kanal fayı boyunca yaklaşık 980 km kuzeybatıya kaydı (yılda ortalama 4,5 cm); bu büyük bir yanal fay "
             "hızıdır, Yeni Zelanda Alp Fayı'nın yılda yaklaşık 3 ile 4 cm'lik hızına yakın.</p>")
    p.append("<h2 class='sayfa'>Parça parça bugünkü coğrafya</h2>")
    for ad, metin in BOLGELER:
        p.append(f"<h3>{ad}</h3><p>{metin}</p>")
    # yer şekilleri
    p.append("<h2>Bugünkü yer şekilleri ve nedenleri</h2><table><tr><th style='width:22%'>Yer şekli</th><th style='width:13%'>En yüksek (m)</th><th>Neden</th></tr>")
    for ad, c, deger, yari, yas, dik in O.KUSAKLAR:
        p.append(f"<tr><td><b>{ad}</b></td><td>{max(deger):,}".replace(",", ".") + f"</td><td>{NEDEN.get(ad, '')}</td></tr>")
    for ad, pol, (y0, y1), _ in O.PLATOLAR:
        p.append(f"<tr><td><b>{ad}</b></td><td>{y0:,} ile {y1:,}".replace(",", ".") + f" (ortalama)</td><td>{PLATO_NEDEN.get(ad, '')}</td></tr>")
    p.append("</table>")
    p.append("<p>Ovalar: Mor Ön Ovası (3'ün kuzeyinde, Mor Sıradağları'nın önünde, ana nehri batıya üçgen koya akar ve orada delta "
             "kurar; koy, çarpışmanın yavaş kapanan batı ucunda kalmış deniz koludur), Sarı Ön Havzası (5'in batısı), 1'in batı kıyı "
             "ovası. Göller: Derin Göl (2'deki yarık gölü, Baykal benzeri), Kum Gölü (Kum Havzası'nın kapalı gölü), Mor Yaylası'nın "
             "tuz gölleri ve kuzeydeki buzul gölleri. Deniz tabanı: 3'ün doğusunda Doğu Hendeği (7 km'yi aşar), 6'nın güneyinde Ada "
             "Hendeği, doğu iç denizde eski okyanus tabanı (3 km), batı iç denizde incelmiş kıta kabuğu.</p>")
    p.append("<h2>Sınırlar</h2><p>Geri kurgu katı parçalarla yapıldı: parçaların bugünkü şekli geçmişe taşındı, oysa çarpışmalarda kabuk "
             "kısalır ve kıvrılır. Bu yüzden 2'nin altına dalan kıta kenarı haritalarda ayrı bir kuşak olarak gösterildi. 340 milyon "
             "yıldan eski olaylar yalnız metinde var; o dönemlerin kıyıları bilinemeyecek kadar silinmiştir, bu Dünya için de böyledir. "
             "Topografya fiziksel bir levha benzetimi değil: tarihten çıkarılan kurallarla kurulan yapı katmanı ve üzerinde gerçek "
             "bir akarsu aşınması modelidir (fastscapelib). Rakamlar tutarlı ama yaklaşık; her biri değiştirilebilir.</p>")
    p.append("</body></html>")
    return "\n".join(p)


def main():
    if os.path.exists("cikti/son_z.npy"):
        profiller()
    h = html()
    open("cikti/tarih.html", "w").write(h)
    import subprocess
    subprocess.run(["node", "pdf_bas.js", os.path.abspath("cikti/tarih.html"), os.path.abspath("cikti/tarih.pdf")], check=True)
    print("PDF tamam")


if __name__ == "__main__":
    main()
