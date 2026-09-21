"""Contact sheets of every client photo, numbered, so we can pick the best ones.
Run: python tools/contact.py  -> tools/contact/sheet-NN.jpg + tools/contact/index.txt
"""
import os, sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "materiasi para o site")
OUT = os.path.join(ROOT, "tools", "contact")
os.makedirs(OUT, exist_ok=True)

files = []
for dp, dn, fn in os.walk(SRC):
    for f in sorted(fn):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            files.append(os.path.join(dp, f))
files.sort()

COLS, ROWS, CELL = 5, 4, 360
PER = COLS * ROWS
font = ImageFont.truetype("arial.ttf", 30) if os.path.exists(r"C:\Windows\Fonts\arial.ttf") else ImageFont.load_default()

with open(os.path.join(OUT, "index.txt"), "w", encoding="utf-8") as idx:
    for i, p in enumerate(files):
        idx.write(f"{i:03d}\t{os.path.relpath(p, SRC)}\n")

for s in range(0, len(files), PER):
    sheet = Image.new("RGB", (COLS * CELL, ROWS * CELL), "white")
    d = ImageDraw.Draw(sheet)
    for j, p in enumerate(files[s:s + PER]):
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        im.thumbnail((CELL - 8, CELL - 8))
        x, y = (j % COLS) * CELL + 4, (j // COLS) * CELL + 4
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 70, y + 40], fill="black")
        d.text((x + 6, y + 3), f"{s + j:03d}", fill="yellow", font=font)
    n = s // PER
    sheet.save(os.path.join(OUT, f"sheet-{n:02d}.jpg"), quality=82)
    print("sheet", n, len(files[s:s + PER]))
print(len(files), "photos")
