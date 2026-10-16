"""Explainer diagrams for blog posts: {{DIAGRAM:key}}.
Drawings are inline SVG (aria-hidden, no text inside, so nothing shrinks to unreadable on a phone);
every label lives in HTML next to the drawing. Colors are the site palette: oak, walnut, sand, stone.
"""
import shell

OAK, OAK_L, OAK_D, GRAIN = "#C98B4A", "#E2B27A", "#8A5526", "#A86B32"
WALNUT, STAIN, STONE, BG = "#3B2314", "#5E3219", "#8C857D", "#FBF8F4"


def _svg(vb, inner):
    return f'<svg viewBox="{vb}" aria-hidden="true" focusable="false">{inner}</svg>'


def _wood(x, y, w, h, joint=True):
    """Board cross-section: oak body, three grain lines, one joint."""
    g = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{OAK}"/>'
         f'<path d="M{x} {y + h * .25} C{x + w * .3} {y + h * .18} {x + w * .6} {y + h * .36} {x + w} {y + h * .26}" stroke="{GRAIN}" stroke-width="2" fill="none" opacity=".55"/>'
         f'<path d="M{x} {y + h * .55} C{x + w * .35} {y + h * .62} {x + w * .65} {y + h * .46} {x + w} {y + h * .56}" stroke="{GRAIN}" stroke-width="2" fill="none" opacity=".45"/>'
         f'<path d="M{x} {y + h * .82} C{x + w * .25} {y + h * .76} {x + w * .7} {y + h * .9} {x + w} {y + h * .8}" stroke="{GRAIN}" stroke-width="2" fill="none" opacity=".4"/>')
    if joint:
        g += f'<line x1="{x + w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y + h}" stroke="{OAK_D}" stroke-width="2"/>'
    return g


def _planks(x, y, w, h, rows, fill, grain, seed=0):
    """Top view of a plank floor: rows of boards with staggered end joints."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>']
    rh = h / rows
    offsets = (0.62, 0.28, 0.81, 0.45, 0.12, 0.7)
    for r in range(rows):
        yy = y + r * rh
        if r:
            out.append(f'<line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{grain}" stroke-width="1.6"/>')
        jx = x + w * offsets[(r + seed) % 6]
        out.append(f'<line x1="{jx}" y1="{yy}" x2="{jx}" y2="{yy + rh}" stroke="{grain}" stroke-width="1.6"/>')
        out.append(f'<path d="M{x + 6} {yy + rh * .5} C{x + w * .3} {yy + rh * .3} {x + w * .55} {yy + rh * .75} {x + w - 6} {yy + rh * .45}" stroke="{grain}" stroke-width="1" fill="none" opacity=".55"/>')
    return "".join(out)


def _item(svg, num, title, text=""):
    t = f"<span>{text}</span>" if text else ""
    return (f'<div class="diagram__item"><div class="diagram__art">{svg}</div>'
            f'<p class="diagram__label"><span class="diagram__num">{num}</span><strong>{title}</strong>{t}</p></div>')


def _figure(items, caption, cols, cls=""):
    return (f'<figure class="diagram diagram--{cols} {cls}"><div class="diagram__grid">{"".join(items)}</div>'
            f'<figcaption>{caption}</figcaption></figure>')


# ---------------------------------------------------------------- post: refinishing restores old floors
def refinish_stages():
    vb = "0 0 200 120"
    base = _wood(10, 50, 180, 60)
    worn = base + (f'<rect x="10" y="38" width="180" height="12" fill="#B9AE9F"/>'
                   + "".join(f'<path d="M{x} 38 l5 9 l5 -9" fill="{BG}" stroke="{STONE}" stroke-width="1.4"/>' for x in (34, 78, 128, 160))
                   + f'<rect x="96" y="40" width="26" height="8" fill="#8F8577" opacity=".6"/>')
    sanded = base + (f'<rect x="10" y="50" width="180" height="6" fill="{OAK_L}"/>'
                     f'<rect x="10" y="38" width="180" height="12" fill="none" stroke="{STONE}" stroke-width="1.4" stroke-dasharray="5 4"/>'
                     + "".join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="{OAK_L}"/>' for x, y in ((40, 28), (52, 20), (70, 30), (118, 24), (135, 14), (150, 28), (95, 18))))
    stained = base + f'<rect x="10" y="50" width="180" height="8" fill="{STAIN}" opacity=".85"/>'
    sealed = stained + (f'<rect x="10" y="41" width="180" height="9" fill="#F6E6D0" opacity=".75"/>'
                        f'<line x1="30" y1="44" x2="96" y2="44" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
                        f'<path d="M160 22 l3 8 l8 3 l-8 3 l-3 8 l-3 -8 l-8 -3 l8 -3 z" fill="{OAK}"/>')
    items = [
        _item(_svg(vb, worn), "01", "Worn finish", "Scratches and graying sit in the top layer."),
        _item(_svg(vb, sanded), "02", "Sanded", "The old finish and the damaged top come off."),
        _item(_svg(vb, stained), "03", "Stained (optional)", "Even color across the fresh wood."),
        _item(_svg(vb, sealed), "04", "Sealed", "New protective coats of finish."),
    ]
    return _figure(items, "What refinishing does to the top of a hardwood board, step by step.", 4)


# ---------------------------------------------------------------- post: scratched floors
def scratch_depth():
    vb = "0 0 260 140"
    def panel(deep):
        notch = "M106 44 L128 82 L150 44 Z" if deep else "M112 44 L128 57 L144 44 Z"
        sand = (f'<line x1="14" y1="90" x2="246" y2="90" stroke="{WALNUT}" stroke-width="1.6" stroke-dasharray="6 4"/>'
                f'<path d="M232 66 v18 m-5 -6 l5 6 l5 -6" stroke="{WALNUT}" stroke-width="1.6" fill="none"/>') if deep else \
               (f'<line x1="14" y1="44" x2="246" y2="44" stroke="{WALNUT}" stroke-width="1.6" stroke-dasharray="6 4"/>')
        return _svg(vb, f'<rect width="260" height="140" fill="{BG}"/>' + _wood(14, 58, 232, 70)
                    + f'<rect x="14" y="44" width="232" height="14" fill="#EAD8BC"/>'
                    + f'<path d="{notch}" fill="{BG}" stroke="{STONE}" stroke-width="1.5"/>' + sand)
    items = [
        _item(panel(False), "A", "Light scratch: in the finish only", "Usually fixed by buffing and a fresh coat (recoat)."),
        _item(panel(True), "B", "Deep scratch: into the wood", "Sanded below the scratch (dashed line), then refinished."),
    ]
    return _figure(items, "Scratch depth decides the fix. The pale band is the finish; the oak below is the wood itself.", 2)


# ---------------------------------------------------------------- post: 2026 trends
def trend_swatches():
    vb = "0 0 200 130"
    gloss = (_planks(0, 0, 200, 130, 5, "#C69A62", "#A87B45", 2)
             + '<rect x="100" y="0" width="100" height="130" fill="#fff" opacity=".0"/>'
             + '<path d="M118 0 L150 0 L104 130 L72 130 Z" fill="#fff" opacity=".28"/>'
             + '<path d="M160 0 L172 0 L126 130 L114 130 Z" fill="#fff" opacity=".22"/>'
             + f'<rect x="0" y="0" width="100" height="130" fill="{BG}" opacity=".12"/>'
             + f'<line x1="100" y1="0" x2="100" y2="130" stroke="{WALNUT}" stroke-width="2" stroke-dasharray="5 4"/>')
    items = [
        _item(_svg(vb, _planks(0, 0, 200, 130, 5, "#E6D1AE", "#C9AE85")), "01", "Light white oak", "Bright, natural and timeless."),
        _item(_svg(vb, _planks(0, 0, 200, 130, 5, "#9A6334", "#7A4A24", 3)), "02", "Warm medium brown", "Rich without going dark."),
        _item(_svg(vb, gloss), "03", "Matte and low-gloss", "Left: matte. Right: gloss reflects every light."),
        _item(_svg(vb, _planks(0, 0, 200, 130, 3, "#D6B285", "#B48D5C", 1)), "04", "Wide plank", "Fewer seams, a calmer, larger-looking room."),
    ]
    return _figure(items, "The four hardwood looks Westfield and Summit homeowners ask for most in 2026.", 4, "diagram--swatches")


# ---------------------------------------------------------------- post: carpet vs hardwood benefits
def lifespan():
    carpet = "".join(f'<span class="life__seg" style="--from:{a};--to:{b}"><em>Replace</em></span>' for a, b in ((0, 32), (33, 65), (66, 98)))
    wood = '<span class="life__seg life__seg--wood" style="--from:0;--to:100"></span>' + "".join(
        f'<span class="life__mark" style="--at:{x}"><em>Refinish</em></span>' for x in (36, 70))
    return f'''<figure class="diagram life">
  <div class="life__chart">
    <div class="life__row"><p class="life__name"><strong>Carpet</strong><span>Replaced every 7 to 10 years</span></p><div class="life__track">{carpet}</div></div>
    <div class="life__row"><p class="life__name"><strong>Hardwood</strong><span>Sanded and refinished, not replaced</span></p><div class="life__track">{wood}</div></div>
    <div class="life__axis" aria-hidden="true"><span>Install</span><span>~10 yrs</span><span>~20 yrs</span><span>~30 yrs</span></div>
  </div>
  <figcaption>Three decades of flooring: carpet gets torn out and bought again; hardwood gets a new surface. Illustration, not a schedule.</figcaption>
</figure>'''


# ---------------------------------------------------------------- shared: numbered steps
def _steps(items, caption, cls=""):
    lis = "".join(f'<li class="steps__item"><span class="steps__node" aria-hidden="true">{shell.ICONS[icon]}</span>'
                  f'<div><p class="steps__when">{when}</p><p class="steps__title">{title}</p><p>{text}</p></div></li>'
                  for icon, when, title, text in items)
    return f'<figure class="diagram steps {cls}"><ol>{lis}</ol><figcaption>{caption}</figcaption></figure>'


def carpet_timeline():
    return _steps([
        ("search", "Step 1", "In-home estimate", "Measurements, a look at the existing flooring and a check for squeaks, damaged plywood or uneven transitions."),
        ("swatch", "Step 2", "Material and scheduling", "In-stock flooring moves faster; special orders can shift the start date."),
        ("trash", "Step 3", "Carpet and debris removal", "Carpet, padding, tack strips and staples come out and leave the house."),
        ("wrench", "Step 4", "Subfloor repair, if needed", "Water damage, squeaks or unevenness get fixed before any wood goes down."),
        ("layers", "Step 5", "Installation", "A few days for a smaller project; longer for a full main floor, stairs or several rooms."),
        ("check", "Step 6", "Cleanup and walk-through", "Clear timing on when you can walk on the floor and move furniture back."),
    ], "How a carpet-to-hardwood project usually runs, from the estimate to the walk-through.")


def cost_factors():
    f = [("ruler", "Square footage", "More area, more material, labor and time."),
         ("swatch", "Hardwood type", "Species, plank width, finish and stain color."),
         ("trash", "Carpet removal", "Stapled, glued or layered carpet takes longer."),
         ("layers", "Subfloor condition", "Repairs change the budget before install."),
         ("stairs", "Stairs", "Matching stairs to the new floor adds detail work."),
         ("home", "Baseboards and trim", "Optional, but often what makes it look finished."),
         ("shield", "Labor quality", "Rushed work costs more later.")]
    cards = "".join(f'<li class="factor"><span class="factor__icon" aria-hidden="true">{shell.ICONS[i]}</span><strong>{t}</strong><span>{d}</span></li>' for i, t, d in f)
    return f'<figure class="diagram factors"><ul class="factor-grid" role="list">{cards}</ul><figcaption>The seven things that move the price of replacing carpet with hardwood.</figcaption></figure>'


# ---------------------------------------------------------------- post: LVP vs hardwood
def seasons():
    vb = "0 0 220 110"
    def boards(gap, cup):
        out, n, x = [], 4, 8
        w = (204 - gap * (n - 1)) / n
        for i in range(n):
            bx = x + i * (w + gap)
            if cup:
                out.append(f'<path d="M{bx} 40 Q{bx + w / 2} 52 {bx + w} 40 L{bx + w} 92 L{bx} 92 Z" fill="{OAK}"/>')
            else:
                out.append(f'<rect x="{bx}" y="44" width="{w}" height="48" fill="{OAK}"/>')
            out.append(f'<path d="M{bx + 4} 64 C{bx + w * .4} 58 {bx + w * .6} 72 {bx + w - 4} 66" stroke="{GRAIN}" stroke-width="1.6" fill="none" opacity=".5"/>')
        out.append(f'<rect x="4" y="92" width="212" height="10" fill="{STONE}" opacity=".35"/>')
        return "".join(out)
    def lvp():
        return (f'<rect x="8" y="58" width="204" height="18" fill="#B98A57"/>'
                + "".join(f'<line x1="{x}" y1="58" x2="{x}" y2="76" stroke="#8E6538" stroke-width="1.5"/>' for x in (59, 110, 161))
                + f'<rect x="8" y="76" width="204" height="6" fill="#6E6861" opacity=".55"/><rect x="4" y="92" width="212" height="10" fill="{STONE}" opacity=".35"/>')
    snow = f'<g stroke="{WALNUT}" stroke-width="2" stroke-linecap="round"><path d="M196 10v20M186 15l20 10M186 25l20-10"/></g>'
    sun = f'<g stroke="{OAK_D}" stroke-width="2" stroke-linecap="round"><circle cx="196" cy="20" r="6" fill="none"/><path d="M196 6v3M196 31v3M182 20h3M207 20h3"/></g>'
    items = [
        _item(_svg(vb, boards(7, False) + snow), "W", "Hardwood in winter", "Dry heated air: boards give up moisture and shrink. Small gaps can show."),
        _item(_svg(vb, boards(0, True) + sun), "S", "Hardwood in summer", "Humid air: boards take on moisture and swell. Too much can cup the edges."),
        _item(_svg(vb, lvp() + snow), "W", "LVP in winter", "Manufactured core: little change with indoor humidity."),
        _item(_svg(vb, lvp() + sun), "S", "LVP in summer", "Same floor, same seams, much less seasonal movement."),
    ]
    return _figure(items, "Why New Jersey's seasons matter: wood moves with humidity, LVP mostly doesn't. Proper acclimation, expansion space and indoor humidity control keep hardwood in check.", 2, "diagram--seasons")


# ---------------------------------------------------------------- post: dustless refinishing
def dust_paths():
    vb = "0 0 300 170"
    room = (f'<rect width="300" height="170" fill="{BG}"/><rect x="10" y="10" width="200" height="140" fill="none" stroke="{STONE}" stroke-width="2"/>'
            f'<rect x="10" y="140" width="200" height="10" fill="{OAK}"/>'
            f'<g stroke="{STONE}" stroke-width="1.6"><rect x="150" y="26" width="44" height="26" fill="#fff"/><path d="M154 32h36M154 38h36M154 44h36"/></g>')
    sander = f'<rect x="44" y="114" width="40" height="26" rx="4" fill="{WALNUT}"/><rect x="40" y="136" width="48" height="5" fill="#1E1613"/><path d="M64 114 L58 86" stroke="{WALNUT}" stroke-width="4" stroke-linecap="round"/>'
    dots_all = ((96, 110), (110, 96), (126, 84), (104, 74), (140, 64), (160, 58), (172, 44), (120, 50), (90, 60), (60, 70), (150, 92), (176, 74), (184, 36), (40, 40), (70, 36), (130, 30), (100, 30), (190, 110), (170, 120), (30, 90))
    trad = room + sander + f'<ellipse cx="100" cy="122" rx="14" ry="10" fill="#D9CFC2" stroke="{STONE}" stroke-width="1.4"/>' \
        + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{OAK_D}" opacity=".55"/>' for x, y in dots_all) \
        + f'<path d="M168 40 l-6 4 l6 4" stroke="{OAK_D}" stroke-width="2" fill="none"/>'
    cont = room.replace('x="10" y="10" width="200" height="140" fill="none" stroke="#8C857D" stroke-width="2"',
                        'x="10" y="10" width="200" height="140" fill="none" stroke="#8C857D" stroke-width="2" stroke-dasharray="275 30 400"') \
        + sander + f'<path d="M84 124 C140 124 170 100 212 100 L246 100" stroke="{WALNUT}" stroke-width="5" fill="none" stroke-linecap="round"/>' \
        + f'<rect x="242" y="78" width="46" height="62" rx="5" fill="{WALNUT}"/><rect x="250" y="88" width="30" height="20" rx="2" fill="{OAK_L}"/>' \
        + f'<g stroke="{WALNUT}" stroke-width="1" opacity=".7"><path d="M254 92h22M254 96h22M254 100h22M254 104h22"/></g>' \
        + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{OAK_D}" opacity=".55"/>' for x, y in ((98, 108), (112, 102)))
    items = [
        _item(_svg(vb, trad), "A", "Traditional sanding", "A cloth bag on the sander. Fine dust passes through, floats around the room and gets pulled into the HVAC return."),
        _item(_svg(vb, cont), "B", "High-containment sanding", "Suction at the sanding pad, a hose out of the room and a sealed HEPA-filtered collector. Up to 95–99% captured."),
    ]
    return _figure(items, "Where the dust goes: the same sander, two very different houses afterward.", 2)


# ---------------------------------------------------------------- post: holiday countdown
def holiday_countdown():
    return _steps([
        ("doc", "6 to 8 weeks out", "Request a free in-home estimate", "Assess the wood, flag repairs, talk stain colors and get the expected schedule."),
        ("clock", "4 to 6 weeks out", "Confirm, choose the finish, plan the move-out", "Arrange furniture removal and a place for kids and pets away from the work."),
        ("sander", "2 to 3 weeks out", "Sanding, staining and finishing done", "Leaves time for drying and curing before anyone sets a table."),
        ("shield", "1 to 2 weeks out", "Protect the cure", "The floor may feel dry, but heavy furniture and rugs may still need to wait."),
        ("home", "Holiday", "Host on finished floors", "No rushed finish, no fresh coating under the dining chairs."),
    ], "Working backward from Thanksgiving: the refinishing countdown.", "steps--countdown")


def cure_timeline():
    marks = [("0", "Last coat", "Finish applied"), ("10", "~24 hours", "Light foot traffic, in socks*"),
             ("38", "Several days", "Furniture back, carefully*"), ("72", "7 to 14 days", "Area rugs back down*")]
    pts = "".join(f'<li style="--at:{a}"><strong>{w}</strong><span>{t}</span></li>' for a, w, t in marks)
    return f'''<figure class="diagram cure">
  <div class="cure__bar" aria-hidden="true"><span></span></div>
  <ol class="cure__marks">{pts}</ol>
  <figcaption>Drying is not curing. *Typical ranges; the exact times depend on the finish product, temperature, humidity and ventilation.</figcaption>
</figure>'''


DIAGRAMS = {
    "refinish-stages": refinish_stages, "scratch-depth": scratch_depth, "trend-swatches": trend_swatches,
    "lifespan": lifespan, "carpet-timeline": carpet_timeline, "cost-factors": cost_factors, "seasons": seasons,
    "dust-paths": dust_paths, "holiday-countdown": holiday_countdown, "cure-timeline": cure_timeline,
}
