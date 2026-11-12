"""Türkçe harfleri gösteren yazı tipi (PIL'in varsayılanı ı, ş, ğ çizemiyor)."""
from functools import lru_cache

from PIL import ImageFont

ADAYLAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


@lru_cache(maxsize=8)
def yazi_tipi(boy: int = 14):
    for y in ADAYLAR:
        try:
            return ImageFont.truetype(y, boy)
        except OSError:
            continue
    return ImageFont.load_default()
