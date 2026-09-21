"""Shared header / footer / sidebar markup for the Costa Flooring build."""

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L8 9.7a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.7.6 2.6.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_ARROW = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 12-9 12S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/></svg>'
ICON_IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/></svg>'
ICON_FB = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>'

def _svg(paths, sw="2"):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{paths}</svg>')

# Small line icons used in timelines / option cards on inner pages: {{ICON:name}}
ICONS = {
    "phone": ICON_PHONE, "mail": ICON_MAIL, "pin": ICON_PIN, "clock": ICON_CLOCK, "doc": ICON_DOC,
    "home": _svg('<path d="M3 21h18M5 21V10l7-6 7 6v11"/><path d="M9 21v-6h6v6"/>'),
    "sander": _svg('<rect x="3" y="8" width="18" height="8" rx="2"/><path d="M7 8V5M17 8V5M3 12h18"/>'),
    "drop": _svg('<path d="M12 2.5c3 4 7 8 7 12a7 7 0 0 1-14 0c0-4 4-8 7-12z"/>'),
    "check": _svg('<path d="M20 6L9 17l-5-5"/>'),
    "shield": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
    "layers": _svg('<path d="M12 2l9 5-9 5-9-5 9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/>'),
    "ruler": _svg('<path d="M3 17L17 3l4 4L7 21l-4-4z"/><path d="M8 12l2 2M11 9l2 2M14 6l2 2"/>'),
    "search": _svg('<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>'),
    "cut": _svg('<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/>'),
    "brush": _svg('<path d="M9.06 11.9l8.07-8.06a2.85 2.85 0 1 1 4.03 4.03l-8.06 8.08"/><path d="M7.07 14.94c-1.66 0-3 1.35-3 3.02 0 1.33-2.5 1.52-2 2.02 1.08 1.1 2.49 2.02 4 2.02 2.2 0 4-1.8 4-4.04a3.01 3.01 0 0 0-3-3.02z"/>'),
    "sun": _svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>'),
    "stairs": _svg('<path d="M3 20h4v-4h4v-4h4V8h4V4"/><path d="M3 20v-2M21 4h-2"/>'),
    "wrench": _svg('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'),
    "wind": _svg('<path d="M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2"/>'),
    "trash": _svg('<path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/>'),
    "eye": _svg('<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
    "swatch": _svg('<rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/>'),
}

# Service cards for "other services" rows on the service pages: {{RELATED:refinishing,sanding,stairs}}
SERVICE_CARDS = {
    "refinishing": ("01", "/services/hardwood-floor-refinishing/", "svc-refinishing", "Hardwood floor refinishing: refinished red oak bedroom floor with dark walnut trim, Union County NJ",
                    "Hardwood floor refinishing", "Sand to bare wood, optional stain, two or three coats of finish. The job that changes a house the most.", "Refinishing details"),
    "installation": ("02", "/services/hardwood-floor-installation/", "svc-installation", "Hardwood floor installation: new white oak plank floor in a New Jersey home",
                     "Hardwood &amp; LVP installation", "Solid and engineered hardwood, or luxury vinyl plank. Old floor removal and subfloor prep included.", "Installation details"),
    "sanding": ("03", "/services/floor-sanding/", "svc-sanding", "Hardwood floor sanding: oak living room floor sanded to bare wood, Linden NJ",
                "Floor sanding", "Drum, edge and buffer sanding with dust containment. The step everything else depends on.", "Sanding details"),
    "staining": ("04", "/services/floor-staining/", "svc-staining", "Hardwood floor staining: oak floor stained a deep red-brown, glossy finish, New Jersey",
                 "Floor staining", "Natural, brown, gray or dark. Samples tested on your sanded floor so you choose from the real thing.", "Staining details"),
    "repair": ("05", "/services/floor-repair/", "svc-repair", "Hardwood floor repair: old hallway with patched boards before refinishing, Union County NJ",
               "Floor repair", "Board replacement, pet and water damage, gaps, squeaks, and patching where a wall or vent came out.", "Repair details"),
    "stairs": ("06", "/services/stair-refinishing/", "svc-stairs", "Stair refinishing: refinished oak treads with white painted risers, Linden NJ",
               "Stair refinishing", "Treads and risers sanded, stained to match the floor and finished, or new oak treads over old steps.", "Stair details"),
}

# Real Google reviews (same set as the home page): {{REVIEWS:whitmore,collier,mcallister}}
REVIEWS = {
    "whitmore": ("J", "J. Whitmore", "Hardwood floor refinishing", "My floors look beautiful! Costa was very detailed in helping me find the right color and gloss. Everything came out even better than I had hoped."),
    "collier": ("A", "A. Collier", "Sanding, staining and refinishing", "Renato arrived even earlier than scheduled. He did a fantastic job sanding, staining, and refinishing multiple rooms and stairs. Great to work with!"),
    "bennett": ("T", "T. Bennett", "Installation and correction", "They fixed a mess left by another installer. Costa Flooring leveled and installed the floor perfectly. Great attention to detail!"),
    "dorsey": ("K", "K. Dorsey", "Hardwood floor installation", "Costa Flooring exceeded all expectations with flawless hardwood flooring and exceptional craftsmanship. Their team was punctual, clean, and used premium materials. Highly recommended!"),
    "hargrove": ("L", "L. Hargrove", "Hardwood sales and installation", "Everything went excellent. Renato was very professional and fast. Great quality flooring job from start to finish."),
    "mcallister": ("S", "S. McAllister", "Whole-home flooring renovation", "Excellent renovation of our home flooring. The team was friendly, responsive, and highly organized. Impeccable, clean work throughout."),
}


# Alt text for every job photo used in the portfolio walls: {{WALL:img,img,...|img,img,...}} (top row | bottom row)
ALT = {
    "gal-01": "Refinished oak hallway with dark stained trim",
    "gal-02": "Bedroom with refinished red oak floor and black window frames",
    "gal-04": "Glossy refinished oak floor under a window with baseboard heat",
    "gal-06": "Refinished floor reflecting light from two windows",
    "gal-08": "Living room oak floor with dark inlay border and fireplace",
    "gal-09": "Bay window room with refinished oak and dark border inlay",
    "gal-10": "Refinished oak floor in a bedroom with natural light",
    "gal-11": "Oak floor refinished with a rich brown stain, high gloss",
    "gal-12": "Living room oak floor refinished in a medium brown stain",
    "gal-13": "Natural oak stair treads with black balusters",
    "gal-14": "Curved staircase with refinished oak treads and white balusters",
    "gal-17": "Oak floor refinished with glossy finish in a room with dark gray walls",
    "gal-18": "Straight staircase with refinished treads and white risers",
    "hero-alt-living-room-fireplace": "Open living room with fireplace and newly refinished light oak floor",
    "ba-install-after": "New red oak floor installed and finished on site in an open kitchen and living area",
    "ba-room-after": "New white oak floor with a dark inlay border in a room with wainscoting",
    "ba-hall-after": "Hallway sanded and refinished, glossy oak with dark trim",
    "ba-hall-before": "Before: worn hardwood hallway with patched boards and a dull gray finish",
    "job-000": "Bedroom with a refinished oak floor and tan walls, glossy finish",
    "job-002": "Refinished oak floor in a room with French doors",
    "job-004": "Large sunlit room with a natural-finish oak floor and a wall of windows",
    "job-011": "Refinished red oak floor seen through a bedroom doorway",
    "job-012": "Bedroom with dark blue walls and a freshly finished light oak floor",
    "job-019": "Corner bedroom with black window frames and a refinished oak floor",
    "job-021": "Small bedroom with a refinished red oak floor and a double window",
    "job-024": "Living room with French doors and a glossy refinished oak floor",
    "job-025": "Hallway toward the front door with a refinished oak floor",
    "job-027": "Bedroom with a refinished oak floor reflecting the window",
    "job-029": "Living room with ceiling fan and a refinished oak floor",
    "job-031": "Open living room with stone fireplace and a glossy refinished oak floor",
    "job-033": "Living room with front door and a refinished oak floor, satin sheen",
    "job-035": "Bedroom seen through the doorway, refinished oak with varied grain",
    "job-036": "Room with a refinished oak floor and a large window",
    "job-037": "Long hallway with a refinished oak floor and white doors",
    "job-047": "Close-up of a refinished red oak floor with a satin finish",
    "job-049": "Open kitchen and living area with a glossy refinished oak floor",
    "job-063": "Room with dark window trim and a deep brown stained oak floor",
    "job-070": "Sunlight across a refinished oak floor with a brown stain",
    "job-081": "Refinished oak floor with a glossy finish beside a baseboard radiator",
    "job-083": "Living room with a bay window, fireplace and a dark inlay border in the oak floor",
    "job-087": "Blue bedroom with a refinished pine floor, glossy finish",
    "job-091": "Refinished oak floor with a contrasting threshold between rooms",
    "job-097": "Older home with a radiator and a refinished red oak floor with a dark border",
    "job-103": "Living room with a wall of windows and a medium brown stained oak floor",
    "job-109": "Dining room with a dark stained oak floor, satin finish",
    "job-110": "Sunlight on a refinished oak floor with a warm brown stain",
    "job-122": "Living room with French doors and a brown stained oak floor",
    "job-126": "Bedroom with dark trim and a glossy refinished oak floor",
    "job-165": "Bedroom with a refinished oak floor, natural tone",
    "job-166": "Living room with a fireplace and a refinished oak floor in a light natural finish",
    "job-050": "Natural white oak floor, matte finish, at a corner wall",
    "job-051": "Bedroom with a new natural white oak floor and recessed lights",
    "job-154": "Room with built-in shelves and a natural white oak floor",
    "job-155": "Step-up into a room with a natural white oak floor",
    "job-164": "Open living room with fireplace and a natural finish white oak floor",
    "job-107": "Dark stained hardwood meeting a tile floor at a doorway",
    "job-008": "Foyer staircase with refinished oak treads and white balusters",
    "job-010": "Staircase with refinished oak treads and rails, white spindles",
    "job-053": "Straight staircase with new oak treads, white risers and iron balusters",
    "job-055": "Oak staircase with iron balusters, seen from the living room",
    "job-056": "Looking down a staircase with wide-plank oak treads",
    "job-062": "View down a foyer staircase with refinished oak handrail and white balusters",
    "job-067": "Refinished oak staircase leading up to a landing",
    "job-069": "Short stair run with refinished oak treads and white risers",
    "job-088": "Staircase with natural oak treads and white risers, blue wall",
    "job-108": "L-shaped staircase with refinished oak treads and white balusters",
    "job-111": "Staircase with dark stained oak treads leading to a landing",
    "job-113": "Staircase with natural oak treads seen from the top",
    "job-139": "Three-step landing with refinished oak treads and white risers",
    "job-140": "Straight staircase with refinished oak treads and white risers",
    "job-145": "Two-story foyer with an arched window and refinished oak stairs",
    "job-146": "Natural oak staircase with iron balusters seen from the landing",
    "job-151": "Winder staircase with natural oak treads and white risers",
    "job-152": "Staircase with light oak treads and black balusters, white wainscoting",
    "job-118": "Before: worn hardwood floor with scratches and a patched strip",
}
# Widths in the wall alternate so the rows don't look like a grid (photos are all 3:4; --ar crops them)
_AR = ("1.3333", "0.75", "1", "0.75")


def _wall_track(names, hidden):
    out = []
    for j, n in enumerate(names):
        n = n.strip()
        alt = "" if hidden else ALT[n]
        tab = ' tabindex="-1"' if hidden else ""
        out.append(f'        <figure class="wall__item" style="--ar:{_AR[j % 4]}"><a href="/assets/img/{n}-960.webp" data-lb{tab}><img src="/assets/img/{n}-480.webp" width="480" height="640" loading="lazy" alt="{alt}"></a></figure>')
    return "\n".join(out)


def wall(spec):
    top, bottom = (s.split(",") for s in spec.split("|"))
    rows = []
    for cls, names in (("left", top), ("right", bottom)):
        rows.append(f'''    <div class="wall__row wall__row--{cls}">
      <div class="wall__track">
{_wall_track(names, False)}
      </div>
      <div class="wall__track" aria-hidden="true">
{_wall_track(names, True)}
      </div>
    </div>''')
    return '  <div class="wall reveal" data-wall>\n' + "\n".join(rows) + "\n  </div>"


def related(keys):
    cards = []
    for k in keys:
        num, href, img, alt, title, desc, link = SERVICE_CARDS[k.strip()]
        cards.append(f'''      <a class="svc-card" href="{href}">
        <div class="svc-card__media"><img src="/assets/img/{img}-480.webp" srcset="/assets/img/{img}-480.webp 480w, /assets/img/{img}-960.webp 960w" sizes="(min-width: 64em) 380px, (min-width: 40em) 50vw, 100vw" width="480" height="640" loading="lazy" alt="{alt}"></div>
        <div class="svc-card__content"><span class="svc-card__num" aria-hidden="true">{num}</span>
          <h3>{title}</h3>
          <p>{desc}</p>
          <span class="link-rule">{link} <span aria-hidden="true">&rarr;</span></span>
        </div>
      </a>''')
    return "\n".join(cards)


def reviews(keys):
    out = []
    for k in keys:
        initial, name, job, text = REVIEWS[k.strip()]
        out.append(f'''      <figure class="review">
        <div class="review__stars" aria-label="5 out of 5 stars">★★★★★</div>
        <blockquote>{text}</blockquote>
        <figcaption><span class="review__avatar" aria-hidden="true">{initial}</span><span><strong>{name}</strong>{job}</span></figcaption>
      </figure>''')
    return "\n".join(out)


SOCIAL = {
    "facebook": "https://www.facebook.com/costaflooringllc/",
    "instagram": "https://www.instagram.com/costaflooring_llc/",
    "google": "https://share.google/qCZ937u2aSv00SdK0",
}


def header(biz, nav, services, current):
    drawer_links = "\n".join(f'<a href="{h}">{l}</a>' for l, h in nav)
    drawer_sub = "\n".join(f'<a class="nav-drawer__sub" href="{h}">{l}</a>' for l, h in services)
    sub = "\n".join(f'<li><a href="{h}">{l}</a></li>' for l, h in services)
    def link(l, h):
        cur = ' aria-current="page"' if h == current else ""
        if h == "/services/":
            return (f'<div class="nav__item nav__item--has-sub"><a href="{h}"{cur}>{l}<svg class="caret" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 10l5 5 5-5z"/></svg></a>'
                    f'<ul class="nav__sub" role="list">{sub}</ul></div>')
        return f'<a href="{h}"{cur}>{l}</a>'
    links = "\n".join(link(l, h) for l, h in nav)
    return f"""<header class="site-header" id="header">
  <div class="container header__top">
    <a class="header__contact" href="tel:{biz['phone_tel']}">{ICON_PHONE}{biz['phone_display']}</a>
    <a class="header__contact header__contact--center" href="mailto:{biz['email']}">{ICON_MAIL}{biz['email']}</a>
    <span class="header__social">
      <a href="{SOCIAL['facebook']}" aria-label="Facebook" rel="noopener">{ICON_FB}</a>
      <a href="{SOCIAL['instagram']}" aria-label="Instagram" rel="noopener">{ICON_IG}</a>
    </span>
  </div>
  <div class="container nav">
    <a class="brand" href="/" aria-label="Costa Flooring LLC, home">
      <img class="brand__logo brand__logo--light" src="/assets/img/logo-costa-flooring-white.webp" alt="Costa Flooring LLC" width="176" height="85">
      <img class="brand__logo brand__logo--dark" src="/assets/img/logo-costa-flooring.webp" alt="Costa Flooring LLC" width="176" height="85">
    </a>
    <nav class="nav__links" aria-label="Primary">
{links}
    </nav>
    <div class="nav__right">
      <a class="btn btn--primary nav__cta" href="/estimate/">Get a free estimate</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu"><span></span></button>
    </div>
  </div>
</header>

<div class="nav-drawer" id="drawer">
{drawer_links}
{drawer_sub}
  <a class="nav-drawer__phone" href="tel:{biz['phone_tel']}">Call {biz['phone_display']}</a>
  <a class="btn btn--primary" href="/estimate/">Get a free estimate{ICON_ARROW}</a>
</div>

<main id="main">
"""


def footer(biz, services, year):
    svc = "\n".join(f'<li><a href="{h}">{l}</a></li>' for l, h in services)
    return f"""</main>

<footer class="site-footer">
  <img class="footer__watermark" src="/assets/img/logo-costa-flooring-white.webp" alt="" width="880" height="425" loading="lazy" aria-hidden="true">
  <div class="container footer">
    <div class="footer__brand">
      <img src="/assets/img/logo-costa-flooring-white.webp" alt="Costa Flooring LLC" width="176" height="85" loading="lazy">
      <p class="footer__tagline">Hardwood floors <em>brought back to life.</em></p>
      <p>Refinishing, sanding, staining, repair and installation for homes and businesses across Union County and North Jersey.</p>
      <a class="btn btn--primary" href="/estimate/" style="margin-top:var(--s-5)">Get a free estimate{ICON_ARROW}</a>
      <div class="footer__social">
        <a href="{SOCIAL['instagram']}" aria-label="Instagram" rel="noopener">{ICON_IG}</a>
        <a href="{SOCIAL['facebook']}" aria-label="Facebook" rel="noopener">{ICON_FB}</a>
        <a href="{SOCIAL['google']}" aria-label="Google Business Profile" rel="noopener">{ICON_PIN}</a>
      </div>
    </div>
    <div>
      <h4>Explore</h4>
      <ul role="list">
        <li><a href="/">Home</a></li>
        <li><a href="/services/">Services</a></li>
        <li><a href="/#before-after">Before &amp; after</a></li>
        <li><a href="/#reviews">Reviews</a></li>
        <li><a href="/service-areas/">Service areas</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/estimate/">Free estimate</a></li>
      </ul>
    </div>
    <div>
      <h4>Services</h4>
      <ul role="list">
{svc}
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <div class="footer__nap">
        <div class="footer__row">{ICON_PIN}<span><strong>Costa Flooring LLC</strong><br>{biz['street']}, {biz['city']}, {biz['state']} {biz['zip']}</span></div>
        <div class="footer__row">{ICON_PHONE}<a href="tel:{biz['phone_tel']}">{biz['phone_display']}</a></div>
        <div class="footer__row">{ICON_MAIL}<a href="mailto:{biz['email']}">{biz['email']}</a></div>
        <div class="footer__hours"><strong>Hours</strong>Mon–Fri 7 AM–7 PM<br>Sat 8 AM–7 PM &middot; Sun closed</div>
        <div class="footer__meta">Serving Linden, Elizabeth, Union, Cranford, Westfield, Rahway, Newark, Jersey City, Edison, Woodbridge and towns across North &amp; Central New Jersey.</div>
      </div>
    </div>
  </div>

  <div class="footer__bottom">
    <div class="container footer__bottom-in">
      <span>&copy; <span id="year">{year}</span> Costa Flooring LLC. All rights reserved.</span>
      <span><a href="/privacy-policy/">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="/terms/">Terms of service</a></span>
      <span>Site by <a href="https://eusouts.com" rel="noopener">Eu sou TS</a></span>
    </div>
  </div>
</footer>

<div class="lb" id="lightbox" hidden aria-modal="true" role="dialog" aria-label="Photo">
  <button class="lb__close" type="button" data-lb-close aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <figure class="lb__figure"><img class="lb__img" src="" alt=""></figure>
</div>

<div class="mobile-bar">
  <a href="tel:{biz['phone_tel']}">{ICON_PHONE} Call now</a>
  <a href="/estimate/">Free estimate {ICON_ARROW}</a>
</div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def sidebar(biz, services, current):
    items = "\n".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a></li>' for l, h in services)
    return f"""<aside class="sidebar">
  <div class="side-box">
    <h3>Get a written price</h3>
    <p>Free on-site visit. We measure, check the wood and quote the job in writing.</p>
    <div class="call">
      <a class="phone" href="tel:{biz['phone_tel']}">{biz['phone_display']}</a>
      <a class="btn btn--primary btn--block" href="/estimate/">Request an estimate{ICON_ARROW}</a>
    </div>
  </div>
  <div class="side-box">
    <h3>All services</h3>
    <ul>
{items}
    </ul>
  </div>
</aside>"""
