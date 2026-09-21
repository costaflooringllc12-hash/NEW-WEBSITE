"""One-off: local-SEO titles/descriptions (≤60 / ≤160 chars). Run: python tools/seo_pass.py"""
import os, re

P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "pages")

META = {
    "00-home.html": (
        "Hardwood Floor Refinishing Linden, NJ | Costa Flooring",
        "Hardwood floor refinishing, sanding, staining, repair and installation in Linden, Union County and North Jersey. Owner-run, written prices. Free estimates."),
    "10-services.html": (
        "Hardwood Flooring Services Union County, NJ | Free Estimates",
        "Refinishing, sanding, staining, repair, stairs and new hardwood or LVP installation for Linden and North Jersey homes. Book a free on-site estimate."),
    "11-refinishing.html": (
        "Hardwood Floor Refinishing Linden, NJ | Free Estimate",
        "Worn, scratched or dated hardwood floors sanded and refinished like new in Linden, Union County and North Jersey. Dust-contained, 2–5 days. Free estimate."),
    "12-installation.html": (
        "Hardwood & LVP Floor Installation Linden, NJ | Free Quote",
        "New solid or engineered hardwood and luxury vinyl plank installed in Linden, Union County and North Jersey. Subfloor prep, finished on site. Free quote."),
    "13-sanding.html": (
        "Hardwood Floor Sanding Linden & Union County NJ | Free Quote",
        "Dust-contained hardwood floor sanding in Linden, Union County and North Jersey. Drum, edge and buffer sanding to bare wood, ready for finish. Free estimate."),
    "14-staining.html": (
        "Hardwood Floor Staining Linden, NJ | Samples on Your Floor",
        "Change your hardwood floor color in Linden, Union County or North Jersey. Stain samples tested on your sanded floor: natural, brown, gray, dark. Free estimate."),
    "15-repair.html": (
        "Hardwood Floor Repair Linden & Union County NJ | Free Quote",
        "Water damage, pet stains, gaps, squeaks and board replacement blended into your hardwood floor. Floor repair in Linden and North Jersey. Free on-site quote."),
    "16-stairs.html": (
        "Stair Refinishing & New Oak Treads Linden, NJ | Free Quote",
        "Worn stairs sanded and refinished, or rebuilt with new oak treads and painted risers, matched to your floor. Linden and Union County, NJ. Free estimate."),
    "20-service-areas.html": (
        "Service Areas | Hardwood Flooring Across North Jersey",
        "Hardwood floor refinishing and installation in Linden, Elizabeth, Union, Cranford, Westfield, Rahway, Newark, Edison, Woodbridge and more. Free estimates."),
    "30-about.html": (
        "About Costa Flooring | Hardwood Floor Company, Linden NJ",
        "Owner-run hardwood flooring company at 311 Grant St, Linden, NJ. The person who quotes your floor is the one who sands it. Free on-site estimates."),
    "40-estimate.html": (
        "Free Hardwood Flooring Estimate Linden, NJ | Costa Flooring",
        "Request a free on-site hardwood floor estimate in Linden, Union County or North Jersey. Written price, no pressure. Call (862) 452-2181 or send the form."),
    "41-thanks.html": (
        "Request Received | Costa Flooring, Linden NJ",
        "Your free estimate request was sent to Costa Flooring in Linden, NJ. We'll call or email within one business day to schedule your on-site visit."),
    "70-links.html": (
        "Costa Flooring LLC, Linden NJ | Call, Email, Follow",
        "Quick links for Costa Flooring LLC, Linden NJ: phone, email, Facebook, Instagram, Google reviews and free estimate."),
}

for fn, (t, d) in META.items():
    assert len(t) <= 62, (fn, len(t))
    assert len(d) <= 160, (fn, len(d))
    path = os.path.join(P, fn)
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'(?m)^(\s*"title":\s*)"[^"]*"', lambda m: m.group(1) + '"' + t + '"', s, count=1)
    s = re.sub(r'(?m)^(\s*"description":\s*)"[^"]*"', lambda m: m.group(1) + '"' + d + '"', s, count=1)
    open(path, "w", encoding="utf-8").write(s)
    print(f"{len(t):2} {len(d):3}  {fn}")
