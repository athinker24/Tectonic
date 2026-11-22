"""Kullanım: python3 -m mk PROJE_KLASORU KOMUT [argümanlar]

Komutlar (sırasıyla; ayrıntılar YOL.md):
  maske                 maskeyi temizle (benek ve delik), cikti/maske_temiz.png; ölçeği yaz
  parcalar              parçaları ayır ve göster, cikti/parcalar.png
  onizle [AD ...]       karşılıkları tek tek önizle, cikti/oniz_AD.png
  karsilik              karşılıkları birleştir, cikti/karsilik_z.npy
  ozellik               ozellikler.json adımlarını uygula, cikti/z.npy
  ciz                   cikti/topografya.png, cikti/topografya_etiketli.png
  olcum                 parça ve etiket yükseklikleri, cikti/olcum.txt
  hepsi                 karsilik + ozellik + ciz + olcum + merak
  merak                 Merak çerçevesinde 16 bit yükseklik + maske, cikti/merak_W.png
  plato DISA M1 M2 ...  Merak dışa aktarımındaki test platolarından kodlamayı ölç, merak_kodlama.json
  birlestir DISA [--kiyi] sahibin elle işlediği dışa aktarımla birleştir, cikti/birlesik_W.png
  uslup [GIRDI]         dokunulmamış karayı sahibin üslubuna yaklaştır, cikti/uslup_W.png
  rehber [GIRDI]        elle işleme rehberi (saydam katman), cikti/rehber_W.png
  fark DISA [BIZIM]     sahip ile bizim arasındaki fark haritası ve özet
"""
import sys

from . import ciz, karsilik, maske, merak, ozellik
from .proje import Proje


def main(a):
    if len(a) < 2:
        print(__doc__); return
    p = Proje(a[0]); k = a[1]; r = a[2:]
    if k == "maske":
        maske.temizle(p)
    elif k == "parcalar":
        maske.parca_resmi(p)
    elif k == "onizle":
        karsilik.onizle(p, r or None)
    elif k == "karsilik":
        karsilik.bilesik(p)
    elif k == "ozellik":
        ozellik.uygula(p)
    elif k == "ciz":
        ciz.ciz(p)
    elif k == "olcum":
        ciz.olcum(p)
    elif k == "hepsi":
        kay = {}
        karsilik.bilesik(p, kay); ozellik.uygula(p, kay); ciz.ciz(p); ciz.olcum(p); merak.cikti(p)
    elif k == "merak":
        merak.cikti(p)
    elif k == "plato":
        merak.plato(p, r[0], [float(v) for v in r[1:]])
    elif k == "birlestir":
        merak.birlestir(p, r[0], kiyi="--kiyi" in r)
    elif k == "uslup":
        merak.uslup(p, r[0] if r else None)
    elif k == "rehber":
        merak.rehber(p, r[0] if r else None)
    elif k == "fark":
        merak.fark(p, r[0], r[1] if len(r) > 1 else None)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
