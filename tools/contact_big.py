"""Bigger contact sheets for a shortlist of indexes (from tools/contact/index.txt).
Run: python tools/contact_big.py 3 12 45 ...
"""
import os, sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "materiasi para o site")
OUT = os.path.join(ROOT, "tools", "contact")
idx = {int(l.split("\t")[0]): l.split("\t")[1].strip() for l in open(os.path.join(OUT, "index.txt"), encoding="utf-8")}
want = [int(a) for a in sys.argv[1:]]
COLS, ROWS, CELL = 4, 3, 480
font = ImageFont.truetype("arial.ttf", 34)
for s in range(0, len(want), COLS * ROWS):
    chunk = want[s:s + COLS * ROWS]
    sheet = Image.new("RGB", (COLS * CELL, ROWS * CELL), "white")
    d = ImageDraw.Draw(sheet)
    for j, i in enumerate(chunk):
        im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, idx[i]))).convert("RGB")
        im.thumbnail((CELL - 8, CELL - 8))
        x, y = (j % COLS) * CELL + 4, (j // COLS) * CELL + 4
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 80, y + 44], fill="black")
        d.text((x + 6, y + 3), f"{i:03d}", fill="yellow", font=font)
    n = s // (COLS * ROWS)
    sheet.save(os.path.join(OUT, f"big-{n:02d}.jpg"), quality=85)
    print("big", n, chunk)
