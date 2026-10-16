"""Blog for the Costa Flooring build.
Each post is tools/blog/<nn>-<slug>.html: a JSON meta comment, then the article body (h2 with ids, paragraphs).
build.py calls pages() to get the hub + every post as (meta, body) pairs, then wraps them in the shared shell.

Placeholders inside a post body (expanded here, before the shared ones in build.py):
  {{CTA:key}}                       mid-article estimate card (keys in CTAS)
  {{FIG:img|alt|caption}}           one job photo, cropped landscape
  {{FIG2:img|alt|img|alt|caption}}  two photos side by side
  {{BA:hall}} / {{BA:stairs}}       before/after slider (same photos as the home page)
  {{DIAGRAM:key}}                   explainer drawing from tools/diagrams.py
Anywhere on the site:
  {{POSTS:slug,slug,slug}}          blog cards (home, service pages)
"""
import html, json, os, re, datetime
import diagrams

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, "tools", "blog")
BASE_URL = "https://njcostaflooring.com"
WPM = 230  # reading speed for "x min read"

CATS = {
    "care": "Refinishing &amp; care",
    "install": "Installation &amp; materials",
}

PUBLISHER = {
    "@type": "Organization", "@id": BASE_URL + "/#business", "name": "Costa Flooring LLC", "url": BASE_URL + "/",
    "logo": {"@type": "ImageObject", "url": BASE_URL + "/assets/img/logo-costa-flooring.webp", "width": 880, "height": 425},
}
AUTHOR = {"@type": "Organization", "name": "Costa Flooring LLC", "url": BASE_URL + "/about/"}

ARROW = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PLUS = '<span class="seal seal--sm" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span>'

# Mid-article estimate cards: (kicker, headline, text, button)
CTAS = {
    "refinish": ("Free on-site estimate", "Floors scratched, gray or worn through?",
                 "We check the wood, measure the rooms and give you a written price for refinishing. Most homes take 2 to 5 days.",
                 "Get a free refinishing estimate"),
    "repair": ("Free on-site estimate", "Not sure if it's a buff, a repair or a full refinish?",
               "Send a couple of photos or book a visit. We'll tell you plainly which fix your floor needs, and what it costs.",
               "Ask what your floor needs"),
    "install": ("Free in-home estimate", "Planning new hardwood or LVP?",
                "We measure, look under the carpet, check the subfloor and price the whole job in writing, removal and cleanup included.",
                "Get a free installation estimate"),
    "carpet": ("Free in-home estimate", "Ready to pull up the carpet?",
               "Tell us the rooms. We'll check what's underneath, plan the days around your family and quote it in writing.",
               "Price my carpet-to-hardwood project"),
    "compare": ("Free in-home estimate", "Still torn between LVP and hardwood?",
                "We install both, so there's nothing to push. We'll walk the house room by room and tell you what fits each space.",
                "Get an honest recommendation"),
    "dust": ("Free on-site estimate", "Want your floors done without the dust storm?",
             "Ask us how we contain dust on your job, room by room, before you book anything.",
             "Book a free refinishing estimate"),
    "final": ("Next step", "Want a straight answer about your own floor?",
              "Owner-run, from a shop on Grant Street in Linden. We come out, check the wood, measure and send you the price and the schedule in writing.",
              "Request my free estimate"),
    "holiday": ("Holiday scheduling", "Hosting this year? Book before the calendar fills up.",
                "Fall dates go fast. Get a written price and a written schedule that leaves time for the finish to cure.",
                "Check holiday availability"),
}

BA = {
    "hall": ("ba-hall-before", "Before: worn hardwood hallway with patched boards and a dull gray finish",
             "ba-hall-after", "After: the same hallway sanded and refinished, glossy oak with dark trim",
             "hallway refinish", "<strong>Same hallway, before and after.</strong> Patched boards blended in, sanded to bare wood, stained and finished by Costa Flooring."),
    "stairs": ("ba-stairs-before", "Before: staircase with damaged treads next to a front door",
               "ba-stairs-after", "After: the same staircase with new oak treads, white risers and iron balusters",
               "staircase", "<strong>Staircase rebuild and refinish.</strong> New oak treads, painted risers and a new railing, finished to match the hallway floor."),
}


def _strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def _date_long(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


def _img(name, sizes, alt, eager=False, w=960, h=1280):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="/assets/img/{name}-960.webp" srcset="/assets/img/{name}-480.webp 480w, /assets/img/{name}-960.webp 960w" '
            f'sizes="{sizes}" width="{w}" height="{h}" {load} alt="{alt}">')


def load():
    posts = []
    for fn in sorted(os.listdir(BLOG_DIR)):
        if not fn.endswith(".html"):
            continue
        src = open(os.path.join(BLOG_DIR, fn), encoding="utf-8-sig").read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", src, re.S)
        p = json.loads(m.group(1))
        p["body"] = src[m.end():].strip()
        p["url"] = f"/blog/{p['slug']}/"
        p["modified"] = p.get("modified", p["date"])
        p["words"] = len(_strip(p["body"]).split()) + sum(len(_strip(q + " " + a).split()) for q, a in p.get("faq", []))
        p["minutes"] = max(1, round(p["words"] / WPM))
        posts.append(p)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


POSTS = load()
BY_SLUG = {p["slug"]: p for p in POSTS}


# --------------------------------------------------------------------------
# Cards (hub, related posts, home, service pages)
# --------------------------------------------------------------------------
def card(p, level="h3", featured=False):
    cls = "post-card post-card--featured" if featured else "post-card"
    sizes = "(min-width: 64em) 600px, 100vw" if featured else "(min-width: 64em) 380px, (min-width: 40em) 50vw, 100vw"
    return f'''      <article class="{cls}" data-cat="{p['cat']}">
        <div class="post-card__media">{_img(p['img'], sizes, p['img_alt'])}</div>
        <div class="post-card__body">
          <p class="post-card__meta"><span class="post-card__cat">{CATS[p['cat']]}</span><span><time datetime="{p['date']}">{_date_long(p['date'])}</time> &middot; {p['minutes']} min read</span></p>
          <{level} class="post-card__title"><a href="{p['url']}">{p['headline_html']}</a></{level}>
          <p>{p['excerpt']}</p>
          <span class="link-rule" aria-hidden="true">Read the guide <span>&rarr;</span></span>
        </div>
      </article>'''


def cards(slugs):
    return "\n".join(card(BY_SLUG[s.strip()]) for s in slugs if s.strip())


def latest(n, exclude=None):
    return [p for p in POSTS if p["slug"] != exclude][:n]


def related_posts(p, n=3):
    """Hand-picked first, then same category, then newest."""
    picked = [BY_SLUG[s] for s in p.get("related", [])]
    for q in POSTS:
        if len(picked) >= n:
            break
        if q is not p and q not in picked and q["cat"] == p["cat"]:
            picked.append(q)
    for q in POSTS:
        if len(picked) >= n:
            break
        if q is not p and q not in picked:
            picked.append(q)
    return picked[:n]


# --------------------------------------------------------------------------
# Body placeholders
# --------------------------------------------------------------------------
def _cta(key):
    kicker, title, text, button = CTAS[key]
    return f'''<aside class="post-cta" aria-label="Free estimate">
  <div class="post-cta__body">
    <p class="post-cta__kicker">{kicker}</p>
    <p class="post-cta__title">{title}</p>
    <p>{text}</p>
  </div>
  <div class="post-cta__actions">
    <a class="btn btn--primary" href="/estimate/">{button}{ARROW}</a>
    <a class="post-cta__phone" href="tel:{{{{TEL}}}}">{{{{ICON_PHONE}}}}or call {{{{PHONE}}}}</a>
  </div>
</aside>'''


def _fig(spec):
    name, alt, cap = spec.split("|")
    return f'<figure class="post-fig">{_img(name, "(min-width: 64em) 720px, 100vw", alt)}<figcaption>{cap}</figcaption></figure>'


def _fig2(spec):
    a, alt_a, b, alt_b, cap = spec.split("|")
    s = "(min-width: 64em) 360px, 50vw"
    return (f'<figure class="post-fig post-fig--pair"><div class="post-fig__pair">{_img(a, s, alt_a)}{_img(b, s, alt_b)}</div>'
            f'<figcaption>{cap}</figcaption></figure>')


def _ba(key):
    b, alt_b, a, alt_a, label, cap = BA[key]
    s = "(min-width: 64em) 720px, 100vw"
    return f'''<figure class="post-fig post-ba">
  <div class="ba">
    {_img(b, s, alt_b, w=480, h=640)}
    {_img(a, s, alt_a, w=480, h=640).replace('<img ', '<img class="ba__after" ', 1)}
    <div class="ba__handle"></div>
    <span class="ba__label ba__label--before">Before</span>
    <span class="ba__label ba__label--after">After</span>
    <input type="range" min="0" max="100" value="50" aria-label="Compare before and after: {label}">
  </div>
  <figcaption>{cap} Drag the handle to compare.</figcaption>
</figure>'''


def expand(body):
    body = re.sub(r"\{\{DIAGRAM:([a-z-]+)\}\}", lambda m: diagrams.DIAGRAMS[m.group(1)](), body)
    body = re.sub(r"\{\{CTA:([a-z]+)\}\}", lambda m: _cta(m.group(1)), body)
    body = re.sub(r"\{\{FIG:([^}]+)\}\}", lambda m: _fig(m.group(1)), body)
    body = re.sub(r"\{\{FIG2:([^}]+)\}\}", lambda m: _fig2(m.group(1)), body)
    body = re.sub(r"\{\{BA:([a-z]+)\}\}", lambda m: _ba(m.group(1)), body)
    return body


# --------------------------------------------------------------------------
# Post page
# --------------------------------------------------------------------------
def _toc(body):
    items = re.findall(r'<h2 id="([^"]+)"(?: data-toc="([^"]+)")?>(.*?)</h2>', body, re.S)
    return "\n".join(f'<li><a href="#{i}">{short or _strip(full)}</a></li>' for i, short, full in items)


def _faq_html(faq):
    out = []
    for i, (q, a) in enumerate(faq, 1):
        open_ = i == 1
        out.append(f'''      <div class="faq__item{' is-open' if open_ else ''}">
        <h3><button class="faq__q" type="button" aria-expanded="{'true' if open_ else 'false'}" aria-controls="faq-a{i}" id="faq-q{i}">{q}{PLUS}</button></h3>
        <div class="faq__a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}"><div><p>{a}</p></div></div>
      </div>''')
    return "\n".join(out)


def _schema(p):
    url = BASE_URL + p["url"]
    graph = [
        {
            "@type": "BlogPosting", "@id": url + "#article", "mainEntityOfPage": url, "url": url,
            "headline": _strip(p["headline_html"]), "description": p["description"],
            "image": [BASE_URL + f"/assets/img/og-{p['slug']}.jpg", BASE_URL + f"/assets/img/{p['img']}-960.webp"],
            "datePublished": p["date"] + "T08:00:00-04:00", "dateModified": p["modified"] + "T08:00:00-04:00",
            "author": AUTHOR, "publisher": PUBLISHER, "inLanguage": "en-US",
            "articleSection": html.unescape(CATS[p["cat"]]), "keywords": p.get("keywords", []),
            "wordCount": p["words"], "isPartOf": {"@id": BASE_URL + "/blog/#blog"},
            "about": [{"@type": "Service", "name": n, "url": BASE_URL + u} for n, u in p.get("about", [])],
            "spatialCoverage": {"@type": "State", "name": "New Jersey"},
        },
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": _strip(p["headline_html"]), "item": url},
        ]},
    ]
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": _strip(q), "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}} for q, a in p["faq"]]})
    return {"@context": "https://schema.org", "@graph": graph}


def post_page(p):
    body = expand(p["body"])
    toc = _toc(body)
    hero = p["img"]
    updated = ""
    if p["modified"] != p["date"]:
        updated = f' &middot; Updated <time datetime="{p["modified"]}">{_date_long(p["modified"])}</time>'
    faq = ""
    if p.get("faq"):
        faq = f'''
<!-- ============================== FAQ ============================== -->
<section class="section section--sand section--grain" id="faq" aria-labelledby="faq-title">
  <div class="container reveal">
    <div class="section-head">
      <span class="kicker">FAQ</span>
      <h2 id="faq-title">{p.get('faq_title', 'Frequently asked questions')}</h2>
    </div>
    <div class="faq__list" data-stagger>
{_faq_html(p['faq'])}
    </div>
    <div class="section__cta">
      <a class="btn btn--primary" href="/estimate/">Ask us about your floor{ARROW}</a>
    </div>
  </div>
</section>'''
    rel = "\n".join(card(q) for q in related_posts(p))
    out = f'''<div class="read-progress" aria-hidden="true"><span></span></div>

<!-- ============================== HERO ============================== -->
<section class="hero hero--page hero--post" aria-label="Article intro">
  <div class="hero__media">{_img(hero, "100vw", p['img_alt'], eager=True)}</div>
  <div class="container hero__grid">
    <div class="hero__copy">
      <nav class="breadcrumb" aria-label="Breadcrumb"><ol>
        <li><a href="/">Home</a></li>
        <li><a href="/blog/">Blog</a></li>
      </ol></nav>
      <span class="kicker">{CATS[p['cat']]} &middot; {p['minutes']} min read</span>
      <h1>{p['h1']}</h1>
      <p class="lead">{p['excerpt']}</p>
      <p class="post-byline">By <a href="/about/">Costa Flooring</a>, Linden, NJ &middot; <time datetime="{p['date']}">{_date_long(p['date'])}</time>{updated}</p>
    </div>
  </div>
</section>

<!-- ============================== ARTICLE ============================== -->
<section class="section post-section">
  <div class="container post-layout">
    <article class="post prose" id="article">
      <details class="toc toc--inline">
        <summary>In this article</summary>
        <ol>
{toc}
        </ol>
      </details>

      <div class="answer-box">
        <p class="answer-box__label">Quick answer</p>
        <p>{p['quick']}</p>
      </div>

{body}

      {{{{CTA_END}}}}

      <footer class="author-box">
        <img src="/assets/img/logo-costa-flooring.webp" width="176" height="85" loading="lazy" alt="Costa Flooring LLC">
        <div>
          <p class="author-box__name">Written by Costa Flooring LLC</p>
          <p>An owner-run hardwood flooring company at 311 Grant St, Linden, NJ. The person who quotes your floor is the one who sands it. Refinishing, sanding, staining, repair, stairs and installation across Union County and North Jersey.</p>
          <p class="author-box__links"><a href="/about/">About us</a> &middot; <a href="/services/">Our services</a> &middot; <a href="/#reviews">Customer reviews</a></p>
        </div>
      </footer>
    </article>

    <aside class="post-aside" aria-label="Article tools">
      <nav class="toc toc--side" aria-label="Table of contents">
        <p class="toc__title">In this article</p>
        <ol>
{toc}
        </ol>
      </nav>
      <div class="side-box side-box--cta">
        <h2 class="side-box__title">Get a written price</h2>
        <p>Free on-site visit. We measure, check the wood and quote the job in writing.</p>
        <div class="call">
          <a class="phone" href="tel:{{{{TEL}}}}">{{{{PHONE}}}}</a>
          <a class="btn btn--primary btn--block" href="/estimate/">Request an estimate{ARROW}</a>
        </div>
      </div>
    </aside>
  </div>
</section>
{faq}

<!-- ============================== REVIEWS ============================== -->
<section class="section{' section--sand section--grain' if not p.get('faq') else ''}">
  <div class="container reveal">
    <div class="section-head">
      <span class="kicker">Reviews</span>
      <h2>What New Jersey homeowners say <em>after we leave.</em></h2>
    </div>
    <div class="reviews" data-stagger>
{{{{REVIEWS:{",".join(p.get("reviews", ["whitmore", "collier", "bennett"]))}}}}}
    </div>
    <div class="section__cta">
      <a class="btn btn--walnut" href="https://share.google/qCZ937u2aSv00SdK0" rel="noopener">Read our reviews on Google</a>
      <a class="btn btn--primary" href="/estimate/">Get a free estimate{ARROW}</a>
    </div>
  </div>
</section>

<!-- ============================== RELATED SERVICES ============================== -->
<section class="section{' section--sand section--grain' if p.get('faq') else ''}">
  <div class="container reveal">
    <div class="section-head">
      <span class="kicker">The services behind this guide</span>
      <h2>Need it done? <em>This is the work we do every week.</em></h2>
    </div>
    <div class="services-grid" data-stagger>
{{{{RELATED:{",".join(p["services"])}}}}}
    </div>
  </div>
</section>

<!-- ============================== KEEP READING ============================== -->
<section class="section{' section--sand section--grain' if not p.get('faq') else ''}" aria-labelledby="more-title">
  <div class="container reveal">
    <div class="section-head">
      <span class="kicker">Keep reading</span>
      <h2 id="more-title">More hardwood guides <em>for New Jersey homes.</em></h2>
    </div>
    <div class="post-grid" data-stagger>
{rel}
    </div>
    <div class="section__cta">
      <a class="btn btn--walnut" href="/blog/">See all articles</a>
    </div>
  </div>
</section>

{cta_band(p.get('band', 'Your floors, <em>done right the first time.</em>'))}
'''
    out = out.replace("{{CTA_END}}", _cta(p.get("cta_end", "final")))
    og = f"/assets/img/og-{p['slug']}.jpg"
    meta = {
        "url": p["url"], "nav": "/blog/", "title": p["title"], "description": p["description"],
        "og_image": og, "og_type": "article", "og_alt": p["img_alt"], "lastmod": p["modified"],
        "head_extra": (f'<meta property="article:published_time" content="{p["date"]}T08:00:00-04:00">\n'
                       f'<meta property="article:modified_time" content="{p["modified"]}T08:00:00-04:00">\n'
                       f'<meta property="article:section" content="{html.unescape(CATS[p["cat"]])}">\n'
                       f'<meta property="article:author" content="{BASE_URL}/about/">'),
        "preload": (f'<link rel="preload" as="image" href="/assets/img/{hero}-960.webp" imagesrcset="/assets/img/{hero}-480.webp 480w, '
                    f'/assets/img/{hero}-960.webp 960w" imagesizes="100vw" fetchpriority="high">'),
        "schema": _schema(p),
    }
    return meta, out


def cta_band(headline):
    return f'''<!-- ============================== FINAL CTA ============================== -->
<section class="section section--walnut cta-band">
  <div class="container reveal">
    <div class="section-head">
      <span class="kicker">Free on-site estimate</span>
      <h2>{headline}</h2>
      <p>Owner-run, from a shop on Grant Street in Linden. We measure, check the wood and give you a written price and a written schedule.</p>
    </div>
    <div class="section__cta">
      <a class="btn btn--primary" href="/estimate/">Get a free estimate{ARROW}</a>
      <a class="btn btn--ghost-light" href="tel:{{{{TEL}}}}">{{{{ICON_PHONE}}}}{{{{PHONE}}}}</a>
    </div>
  </div>
</section>'''


# --------------------------------------------------------------------------
# Hub page /blog/
# --------------------------------------------------------------------------
def hub_page():
    first, rest = POSTS[0], POSTS[2:]
    top = "\n".join(card(p, level="h2", featured=True) for p in POSTS[:2])
    grid = "\n".join(card(p) for p in rest)
    chips = "\n".join(f'<button class="chip" type="button" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in CATS.items())
    out = f'''<!-- ============================== HERO ============================== -->
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Blog</li></ol></nav>
    <h1>Hardwood floor guides <em>for New Jersey homeowners.</em></h1>
    <p>Straight answers on refinishing, repairs, installation and LVP from the crew that does the work, out of Linden, NJ. What it costs, how long it takes and what to expect in your house.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="/estimate/">Get a free estimate{ARROW}</a>
      <a class="btn btn--ghost-light" href="tel:{{{{TEL}}}}">{{{{ICON_PHONE}}}}{{{{PHONE}}}}</a>
    </div>
  </div>
</section>

<!-- ============================== LATEST ============================== -->
<section class="section">
  <div class="container reveal">
    <div class="section-head section-head--left">
      <span class="kicker">Latest articles</span>
    </div>
    <div class="post-grid post-grid--2" data-stagger>
{top}
    </div>
  </div>
</section>

<!-- ============================== ALL POSTS ============================== -->
<section class="section section--sand section--grain" id="articles" aria-labelledby="all-title">
  <div class="container">
    <div class="section-head">
      <span class="kicker">More articles</span>
      <h2 id="all-title">Pick a topic, <em>or read them all.</em></h2>
    </div>
    <div class="chips" role="group" aria-label="Filter articles by topic" data-filter-group hidden>
      <button class="chip" type="button" data-filter="all" aria-pressed="true">All articles</button>
{chips}
    </div>
    <span id="care" class="anchor"></span><span id="install" class="anchor"></span>
    <div class="post-grid" data-stagger data-filter-list>
{grid}
    </div>
    <p class="filter-empty" hidden>No other articles in this topic yet. The latest one is above.</p>
  </div>
</section>

<!-- ============================== TOPIC HUBS ============================== -->
<section class="section">
  <div class="container reveal">
    <div class="section-head">
      <span class="kicker">Start with the service</span>
      <h2>Know what you need? <em>Go straight to the details.</em></h2>
      <p>Every guide links back to the service it explains. These pages cover what's included, how the week goes and what it takes to get a written price.</p>
    </div>
    <div class="services-grid" data-stagger>
{{{{RELATED:refinishing,installation,repair}}}}
    </div>
    <div class="section__cta">
      <a class="btn btn--walnut" href="/services/">See all six services</a>
    </div>
  </div>
</section>

{cta_band('Rather talk it through? <em>We answer the phone.</em>')}
'''
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": BASE_URL + "/blog/#blog", "name": "Costa Flooring Blog", "url": BASE_URL + "/blog/",
         "description": "Hardwood floor refinishing, repair, installation and LVP guides for New Jersey homeowners.",
         "inLanguage": "en-US", "publisher": PUBLISHER,
         "blogPost": [{"@type": "BlogPosting", "headline": _strip(p["headline_html"]), "url": BASE_URL + p["url"],
                       "datePublished": p["date"], "dateModified": p["modified"],
                       "image": BASE_URL + f"/assets/img/{p['img']}-960.webp"} for p in POSTS]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog/"}]},
    ]}
    meta = {
        "url": "/blog/", "title": "Hardwood Floor Blog: NJ Refinishing & Installation Tips",
        "description": "Guides for New Jersey homeowners on hardwood refinishing, scratches, dust, carpet removal, LVP vs. hardwood and holiday timing. From Costa Flooring, Linden NJ.",
        "og_image": f"/assets/img/og-{first['slug']}.jpg", "lastmod": max(p["modified"] for p in POSTS), "schema": schema,
    }
    return meta, out


def pages():
    yield hub_page()
    for p in POSTS:
        yield post_page(p)


# --------------------------------------------------------------------------
# Social share images: 1200x630 JPG per post (photo crop + walnut fade + white logo)
# --------------------------------------------------------------------------
def og_images(site):
    from PIL import Image, ImageDraw
    img_dir = os.path.join(site, "assets", "img")
    logo = Image.open(os.path.join(img_dir, "logo-costa-flooring-white.webp")).convert("RGBA")
    logo = logo.resize((300, round(300 * logo.height / logo.width)), Image.LANCZOS)
    for p in POSTS:
        out = os.path.join(img_dir, f"og-{p['slug']}.jpg")
        im = Image.open(os.path.join(img_dir, f"{p['img']}-960.webp")).convert("RGB")
        w, h = im.size
        ch = round(w * 630 / 1200)
        top = max(0, min(h - ch, round(h * 0.55 - ch / 2)))
        im = im.crop((0, top, w, top + ch)).resize((1200, 630), Image.LANCZOS).convert("RGBA")
        fade = Image.new("RGBA", (1200, 630), (0, 0, 0, 0))
        d = ImageDraw.Draw(fade)
        for y in range(630):
            a = int(205 * max(0, (y - 300) / 330) ** 1.3)
            d.line([(0, y), (1200, y)], fill=(42, 24, 16, a))
        im = Image.alpha_composite(im, fade)
        im.alpha_composite(logo, (48, 630 - logo.height - 40))
        im.convert("RGB").save(out, "JPEG", quality=82, optimize=True, progressive=True)
    print("og images:", len(POSTS))


# --------------------------------------------------------------------------
# RSS feed
# --------------------------------------------------------------------------
def feed():
    def rfc(iso):
        return datetime.datetime.fromisoformat(iso + "T08:00:00-04:00").strftime("%a, %d %b %Y %H:%M:%S %z")
    items = []
    for p in POSTS:
        url = BASE_URL + p["url"]
        items.append(f'''  <item>
    <title>{html.escape(_strip(p["headline_html"]))}</title>
    <link>{url}</link>
    <guid isPermaLink="true">{url}</guid>
    <pubDate>{rfc(p["date"])}</pubDate>
    <category>{CATS[p["cat"]]}</category>
    <description>{html.escape(_strip(p["excerpt"]))}</description>
  </item>''')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Costa Flooring Blog</title>
  <link>{BASE_URL}/blog/</link>
  <atom:link href="{BASE_URL}/blog/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Hardwood floor guides for New Jersey homeowners from Costa Flooring, Linden NJ.</description>
  <language>en-us</language>
  <lastBuildDate>{rfc(POSTS[0]["modified"])}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
'''
