"""Build a clean deploy folder (only files the site actually uses) + zip for Hostinger.
Run: python tools/deploy.py  ->  deploy/  and  deploy-costaflooring.zip
"""
import os, re, shutil, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "deploy")
ZIP = os.path.join(ROOT, "deploy-costaflooring.zip")

# 1. site files only (html, css, js, sitemap, robots, favicon, .htaccess) — never raw client material
WEB = (".html", ".css", ".js", ".xml", ".txt", ".svg", ".ico", ".webmanifest", ".woff2")
keep = set()
for dp, dn, fn in os.walk(SITE):
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), SITE).replace("\\", "/")
        if rel.startswith("assets/img/"):
            continue
        if f == ".htaccess" or f.lower().endswith(WEB):
            keep.add(rel)

# 2. images: only the ones referenced from html/css/js
refs = set()
for rel in list(keep):
    if rel.endswith((".html", ".css", ".js")):
        txt = open(os.path.join(SITE, rel), encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r"assets/img/([A-Za-z0-9._-]+\.(?:webp|png|jpg|svg))", txt):
            refs.add("assets/img/" + m.group(1))
keep |= refs

# 3. copy
if os.path.exists(OUT):
    shutil.rmtree(OUT)
for rel in sorted(keep):
    src = os.path.join(SITE, rel)
    dst = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

# 4. .htaccess comes from site/.htaccess (already in keep)

# 5. zip
if os.path.exists(ZIP):
    os.remove(ZIP)
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, dn, fn in os.walk(OUT):
        for f in fn:
            full = os.path.join(dp, f)
            z.write(full, os.path.relpath(full, OUT))

total = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(OUT) for f in fn)
unused = len([f for f in os.listdir(os.path.join(SITE, "assets/img")) if "assets/img/" + f not in refs])
print(f"deploy/: {len(keep)+1} files, {total/1024/1024:.1f} MB  (skipped {unused} unused images)")
print("zip:", os.path.basename(ZIP), f"{os.path.getsize(ZIP)/1024/1024:.1f} MB")
