"""Convert the selected client photos (by contact-sheet index) to site/assets/img/job-NNN-{480,960}.webp.
Run: python tools/pick.py  -> prints a manifest line per photo with its aspect ratio (w/h)
"""
import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "materiasi para o site")
OUT = os.path.join(ROOT, "site", "assets", "img")
idx = {int(l.split("\t")[0]): l.split("\t")[1].strip() for l in open(os.path.join(ROOT, "tools", "contact", "index.txt"), encoding="utf-8")}

PICK = [0, 2, 4, 11, 12, 19, 21, 24, 25, 27, 29, 31, 33, 35, 36, 37, 47, 49, 63, 70, 81, 83, 87, 91, 97, 103, 109, 110, 122, 126, 165, 166,
        50, 51, 154, 155, 164, 107,
        8, 10, 53, 55, 56, 62, 67, 69, 88, 108, 111, 113, 139, 140, 145, 146, 151, 152,
        118]

for i in PICK:
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, idx[i]))).convert("RGB")
    w, h = im.size
    for W in (480, 960):
        r = im.resize((W, round(h * W / w)), Image.LANCZOS)
        r.save(os.path.join(OUT, f"job-{i:03d}-{W}.webp"), "WEBP", quality=80 if W == 960 else 78, method=6)
    print(f"job-{i:03d}\t{w}x{h}\tar={w / h:.4f}")
