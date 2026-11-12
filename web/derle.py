"""web/anlik_sablon.html + web/veri_anlik.json -> web/anlik.html"""
import json

v = json.load(open("web/veri_anlik.json"))
s = open("web/anlik_sablon.html", encoding="utf-8").read().replace("/*VERI*/null", json.dumps(v, separators=(",", ":")))
open("web/anlik.html", "w", encoding="utf-8").write(s)
print(len(s))
