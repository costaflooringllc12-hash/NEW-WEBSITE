"""Static site builder for Costa Flooring.
Reads tools/pages/*.html (content fragment with a JSON meta comment at top),
wraps each in the shared shell (tools/shell.py) and writes to site/<url>/index.html.
Run: python tools/build.py
"""
import json, os, re, datetime, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "tools", "pages")
SITE = os.path.join(ROOT, "site")
BASE_URL = "https://njcostaflooring.com"
GTM_ID = "GTM-XXXXXXX"  # TODO: replace with the client's real container ID

BIZ = {
    "name": "Costa Flooring LLC",
    "phone_display": "(862) 452-2181",
    "phone_tel": "+18624522181",
    "email": "contact@njcostaflooring.com",
    "street": "311 Grant St",
    "city": "Linden",
    "state": "NJ",
    "zip": "07036",
}

NAV = [
    ("Home", "/"),
    ("Services", "/services/"),
    ("Before & After", "/#before-after"),
    ("Service Areas", "/service-areas/"),
    ("About", "/about/"),
    ("Contact", "/estimate/"),
]
SERVICES = [
    ("Hardwood Floor Refinishing", "/services/hardwood-floor-refinishing/"),
    ("Hardwood & LVP Installation", "/services/hardwood-floor-installation/"),
    ("Floor Sanding", "/services/floor-sanding/"),
    ("Floor Staining", "/services/floor-staining/"),
    ("Floor Repair", "/services/floor-repair/"),
    ("Stair Refinishing", "/services/stair-refinishing/"),
]


def head(meta):
    url = BASE_URL + meta["url"]
    og_img = BASE_URL + meta.get("og_image", "/assets/img/hero-refinished-oak-living-room-960.webp")
    robots = '<meta name="robots" content="noindex, follow">' if meta.get("noindex") else ""
    schema = ""
    if meta.get("schema"):
        schema = '<script type="application/ld+json">' + json.dumps(meta["schema"], ensure_ascii=False) + "</script>"
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta["title"]}</title>
<meta name="description" content="{meta["description"]}">
<link rel="canonical" href="{url}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Costa Flooring LLC">
<meta property="og:title" content="{meta["title"]}">
<meta property="og:description" content="{meta["description"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2A1810">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/poppins-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
{meta.get("preload", "")}
{schema}
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
<a class="skip-link" href="#main">Skip to content</a>
"""


def build():
    urls = []
    year = datetime.date.today().year
    for fn in sorted(os.listdir(PAGES)):
        if not fn.endswith(".html"):
            continue
        src = open(os.path.join(PAGES, fn), encoding="utf-8-sig").read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", src, re.S)
        meta = json.loads(m.group(1))
        body = src[m.end():]
        body = (body.replace("{{PHONE}}", BIZ["phone_display"]).replace("{{TEL}}", BIZ["phone_tel"])
                .replace("{{EMAIL}}", BIZ["email"])
                .replace("{{ICON_PHONE}}", shell.ICON_PHONE).replace("{{ICON_ARROW}}", shell.ICON_ARROW)
                .replace("{{SIDEBAR}}", shell.sidebar(BIZ, SERVICES, meta["url"])))
        body = re.sub(r"\{\{ICON:([a-z]+)\}\}", lambda mm: shell.ICONS[mm.group(1)], body)
        body = re.sub(r"\{\{RELATED:([a-z, ]+)\}\}", lambda mm: shell.related(mm.group(1).split(",")), body)
        body = re.sub(r"\{\{REVIEWS:([a-z, ]+)\}\}", lambda mm: shell.reviews(mm.group(1).split(",")), body)
        body = re.sub(r"\{\{WALL:([a-z0-9, |-]+)\}\}", lambda mm: shell.wall(mm.group(1)), body)
        if meta.get("bare"):  # standalone page (link-in-bio / QR landing): no header, footer or JS
            html = head(meta) + body + "</body>\n</html>\n"
        else:
            html = head(meta) + shell.header(BIZ, NAV, SERVICES, meta.get("nav", meta["url"])) + body + shell.footer(BIZ, SERVICES, year)
        out_path = meta.get("file") or os.path.join(meta["url"].strip("/"), "index.html")
        # Root-relative -> relative paths, so the site works from any folder (Live Server, subdir, file://)
        depth = out_path.replace("\\", "/").count("/")
        prefix = "../" * depth if depth else "./"
        html = re.sub(r'(href|src|srcset|imagesrcset)="/', lambda mm: f'{mm.group(1)}="{prefix}', html)
        html = html.replace(", /assets/", f", {prefix}assets/")
        out = os.path.join(SITE, out_path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(html)
        if not meta.get("noindex"):
            urls.append(meta["url"])
        print("built", out_path)

    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{BASE_URL}{u}</loc><lastmod>{today}</lastmod></url>")
    sm.append("</urlset>")
    open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))
    open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    print("sitemap + robots written")


if __name__ == "__main__":
    build()
