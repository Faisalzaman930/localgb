#!/usr/bin/env python3
"""
P0 SEO injector for GB Guide.

Idempotently injects into every <page>/index.html, just before </head>:
  - <link rel="canonical">
  - Open Graph + Twitter Card tags
  - JSON-LD structured data (Organization+WebSite on home, BreadcrumbList +
    TouristDestination/Article elsewhere)

Also (re)generates robots.txt and sitemap.xml at the repo root.

The injected block is wrapped in <!-- SEO:START --> ... <!-- SEO:END --> so a
re-run replaces it cleanly instead of duplicating. Hand-authored <title> and
<meta name="description"> are left untouched and reused as the source of truth.

Run:  python3 seo_inject.py
"""

import re
import json
import datetime
from pathlib import Path

DOMAIN = "https://www.gilgitbaltistanguide.com"
ROOT = Path(__file__).resolve().parent
DEFAULT_OG = f"{DOMAIN}/images/hunza-photo.webp"
TODAY = datetime.date.today().isoformat()

# Folder -> hero image used for OG/Twitter previews (falls back to DEFAULT_OG).
OG_IMAGES = {
    "": "hunza-photo.webp",
    "hunza": "hunza-photo.webp",
    "gilgit": "gilgit-photo.webp",
    "skardu": "skardu-photo.webp",
    "fairy-meadows": "fairymeadows-photo.webp",
    "naran-kaghan": "naran-kaghan-photo.webp",
    "mountains": "karakoram-photo.webp",
    "trekking": "baltoro-photo.webp",
    "things-to-do": "stargazing-photo.webp",
    "deosai": "deosai-photo.webp",
    "naltar": "naltar-photo.webp",
    "astore": "astore-photo.webp",
    "gojal": "gojal-photo.webp",
    "ghizer": "ghizer-photo.webp",
    "yasin": "yasin-photo.webp",
    "trekking/concordia": "concordia-photo.webp",
    "trekking/rakaposhi-base-camp": "rakaposhi-photo.webp",
    "mountains/rakaposhi": "rakaposhi-photo.webp",
    "hunza/attabad-lake": "attabad-photo.webp",
    "hunza/baltit-fort": "baltit-fort-photo.webp",
    "hunza/altit-fort": "altit-fort-photo.webp",
    "hunza/borith-lake": "borith-lake-photo.webp",
    "hunza/gulmit": "gulmit-photo.webp",
    "hunza/shimshal-valley": "shimshal-photo.webp",
    "mountains/spantik": "spantik-photo.webp",
    "mountains/masherbrum": "masherbrum-photo.webp",
    "mountains/k2": "k2-photo.webp",
    "trekking/k2-base-camp": "k2-photo.webp",
    "gilgit/bagrot-valley": "bagrot-valley-photo.webp",
    "gilgit/kargah-buddha": "kargah-buddha-photo.webp",
    "skardu/khaplu": "khaplu-photo.webp",
    "skardu/khaplu-palace": "khaplu-photo.webp",
    "skardu/satpara-lake": "satpara-lake-photo.webp",
    "skardu/sheosar-lake": "sheosar-lake-photo.webp",
    "skardu/shigar-valley": "shigar-valley-photo.webp",
    "mountains/nanga-parbat": "nanga-parbat-photo.webp",
    "karakoram-highway": "karakoram-highway-photo.webp",
    "trekking/nanga-parbat-base-camp": "nanga-parbat-photo.webp",
    "trekking/nanga-parbat-rupal-face": "nanga-parbat-photo.webp",
    "trekking/masherbrum-base-camp": "masherbrum-photo.webp",
    "trekking/spantik-base-camp": "spantik-photo.webp",
    "trekking/naltar-lakes": "naltar-photo.webp",
    "tours/skardu": "skardu-photo.webp",
    "updates": "karakoram-highway-photo.webp",
    "tours/naran-kaghan": "naran-kaghan-photo.webp",
    "tours/hunza": "hunza-photo.webp",
    "tours/from-islamabad": "hunza-photo.webp",
    "hunza/chapursan-valley": "chapursan-photo.webp",
    "hunza/karimabad": "karimabad-photo.webp",
    "hunza/hotels": "karimabad-photo.webp",
    "hunza/khunjerab-pass": "khunjerab-photo.webp",
    "hunza/passu-cones": "gojal-photo.webp",
    "food": "food-photo.webp",
    "hunza/food": "food-photo.webp",
    "travel/gb-food-guide": "food-photo.webp",
    "trekking/biafo-hispar-snow-lake": "snow-lake-photo.webp",
    "trekking/gondogoro-la": "gondogoro-photo.webp",
    "trekking/hushe-valley": "hushe-photo.webp",
    "trekking/karambar-lake": "karambar-photo.webp",
    "trekking/rush-lake": "rush-lake-photo.webp",
    "skardu/basho-valley": "basho-photo.webp",
    "skardu/kachura-lake": "kachura-photo.webp",
    "skardu/kharpocho-fort": "kharpocho-photo.webp",
    "skardu/manthokha-waterfall": "manthokha-photo.webp",
    "ishkoman": "ishkoman-photo.webp",
    "tours/chitral": "chitral-photo.webp",
    "mountains/laila-peak": "laila-peak-photo.webp",
    "trekking/laila-peak-base-camp": "laila-peak-photo.webp",
    "mountains/broad-peak": "broad-peak-photo.webp",
    "mountains/gasherbrum": "gasherbrum-photo.webp",
    "mountains/trango-towers": "trango-photo.webp",
    "things-to-do/rock-climbing-trango": "trango-photo.webp",
    "skardu/katpana-desert": "katpana-photo.webp",
    "skardu/sarfaranga-cold-desert": "sarfaranga-photo.webp",
    "skardu/shigar-fort": "shigar-fort-photo.webp",
    "things-to-do/shandur-polo-festival": "shandur-photo.webp",
    "things-to-do/jeep-safari-gb": "jeep-photo.webp",
    "fairy-meadows/how-to-reach": "jeep-photo.webp",
    "things-to-do/camping-in-gb": "camping-photo.webp",
    "fairy-meadows/camping": "fairymeadows-camp-photo.webp",
    "things-to-do/skiing-naltar": "naltar-ski-photo.webp",
    "hunza/in-autumn": "hunza-autumn-photo.webp",
    "hunza/in-october": "hunza-autumn-photo.webp",
    "hunza/in-november": "hunza-autumn-photo.webp",
    "updates/hunza-autumn-foliage-2026": "hunza-autumn-photo.webp",
    "hunza/in-winter": "hunza-winter-photo.webp",
    "hunza/in-december": "hunza-winter-photo.webp",
    "hunza/in-january": "hunza-winter-photo.webp",
    "hunza/in-february": "hunza-winter-photo.webp",
    "travel/gb-in-winter": "hunza-winter-photo.webp",
    "hunza/in-march": "blossom-photo.webp",
    "hunza/in-april": "blossom-photo.webp",
    "skardu/in-december": "skardu-winter-photo.webp",
    "skardu/in-january": "skardu-winter-photo.webp",
    "skardu/in-february": "skardu-winter-photo.webp",
    "travel/skardu-flights": "skardu-airport-photo.webp",
    "updates/skardu-gilgit-flights-2026": "skardu-airport-photo.webp",
    "status": "babusar-photo.webp",
    "updates/gilgit-baltistan-road-pass-status-2026": "babusar-road-photo.webp",
    "kkh-map": "karakoram-highway-photo.webp",
    "travel/karakoram-highway": "karakoram-highway-photo.webp",
    "travel/islamabad-to-hunza": "karakoram-highway-photo.webp",
    "travel": "karakoram-highway-photo.webp",
    "atm-locator": "gilgit-photo.webp",
    "agencies": "baltoro-photo.webp",
    "blog": "gojal-photo.webp",
}

# Pages that describe a place -> emit TouristDestination. Everything else that
# isn't the homepage gets Article. (Homepage gets Organization + WebSite.)
DESTINATION_DIRS = {
    "hunza", "gilgit", "skardu", "fairy-meadows", "deosai", "naltar", "astore",
    "ghizer", "gojal", "yasin", "ishkoman", "yasin-ishkoman", "naran-kaghan",
    "karakoram-highway", "destinations", "hidden-valleys", "mountains",
}

# Human-readable crumb labels for known segments.
CRUMB_LABELS = {
    "fairy-meadows": "Fairy Meadows",
    "naran-kaghan": "Naran & Kaghan",
    "karakoram-highway": "Karakoram Highway",
    "things-to-do": "Things to Do",
    "hidden-valleys": "Hidden Valleys",
    "atm-locator": "Essentials Map",
    "kkh-map": "KKH Map",
    "yasin-ishkoman": "Yasin & Ishkoman",
}

# Approx geo coordinates for place pages (lat, lon) — feeds schema.org geo.
COORDS = {
    "hunza": (36.3167, 74.65), "skardu": (35.2971, 75.6333), "gilgit": (35.9208, 74.3083),
    "fairy-meadows": (35.3897, 74.5786), "deosai": (34.9667, 75.4), "naltar": (36.1667, 74.1833),
    "astore": (35.3667, 74.8667), "ghizer": (36.1667, 73.75), "gojal": (36.4333, 74.8667),
    "yasin": (36.4, 73.3), "ishkoman": (36.45, 73.7833), "naran-kaghan": (34.9089, 73.65),
    "karakoram-highway": (35.9, 74.3),
    "mountains/k2": (35.8825, 76.5133), "mountains/nanga-parbat": (35.2375, 74.5892),
    "mountains/rakaposhi": (36.1442, 74.4894), "mountains/broad-peak": (35.81, 76.57),
    "mountains/gasherbrum": (35.7239, 76.6964), "mountains/masherbrum": (35.6411, 76.3047),
    "mountains/spantik": (36.05, 75.0), "mountains/haramosh-peak": (35.9419, 74.8994),
    "mountains/laila-peak": (35.62, 76.32), "mountains/trango-towers": (35.86, 76.31),
}

START, END = "<!-- SEO:START -->", "<!-- SEO:END -->"

GA4 = (
    '<!-- Google tag (gtag.js) -->\n'
    '<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z2Y8ZSH7FH"></script>\n'
    "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
    "gtag('js',new Date());gtag('config','G-Z2Y8ZSH7FH');</script>"
)


def label_for(seg: str) -> str:
    return CRUMB_LABELS.get(seg, seg.replace("-", " ").title())


def extract(pattern: str, html: str) -> str:
    m = re.search(pattern, html, re.I | re.S)
    return m.group(1).strip() if m else ""


def build_block(rel_dir: str, title: str, desc: str) -> str:
    seg = rel_dir.strip("/")
    url = DOMAIN if seg == "" else f"{DOMAIN}/{seg}"
    og_img = OG_IMAGES.get(seg, "")
    og_url = f"{DOMAIN}/images/{og_img}" if og_img else DEFAULT_OG

    # Clean OG title: drop the trailing brand suffix if present.
    og_title = re.sub(r"\s*[—|-]\s*GB Guide.*$", "", title).strip() or title

    tags = [
        START,
        GA4,
        '<meta name="google-site-verification" content="HHV6xWXi_fzm-W0Xq6RMXIilDC7sHeEU4yH0mpGkqAk">',
        '<link rel="icon" href="/favicon.ico" sizes="32x32">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        '<link rel="manifest" href="/site.webmanifest">',
        '<meta name="theme-color" content="#FBFAF6">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="GB Guide">',
        f'<meta property="og:title" content="{esc(og_title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{og_url}">',
        '<meta property="og:locale" content="en_US">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(og_title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{og_url}">',
    ]

    # ---- JSON-LD ----
    graph = []
    if seg == "":
        graph.append({
            "@type": "Organization",
            "@id": f"{DOMAIN}/#org",
            "name": "GB Guide",
            "url": DOMAIN,
            "logo": og_url,
            "description": "Honest, on-the-ground travel guides to Gilgit-Baltistan, "
                           "written by a local — plus a free trip planner.",
            "founder": {
                "@type": "Person",
                "@id": f"{DOMAIN}/#faisal",
                "name": "Faisal Zaman",
                "url": f"{DOMAIN}/about",
                "image": f"{DOMAIN}/images/faisal-zaman.jpg",
                "jobTitle": "Founder & local travel writer",
                "homeLocation": {"@type": "Place", "name": "Misgar, Hunza, Gilgit-Baltistan, Pakistan"},
                "sameAs": [
                    "https://www.linkedin.com/in/faisal-seo-analyst/",
                    "https://www.instagram.com/imfaysalzaman",
                    "https://www.facebook.com/share/17jDnUoeAN/",
                ],
            },
        })
        graph.append({
            "@type": "WebSite",
            "@id": f"{DOMAIN}/#website",
            "url": DOMAIN,
            "name": "GB Guide",
            "publisher": {"@id": f"{DOMAIN}/#org"},
        })
    else:
        # Breadcrumbs: Home > [segment]
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN}]
        for i, part in enumerate(seg.split("/"), start=2):
            crumbs.append({
                "@type": "ListItem", "position": i,
                "name": label_for(part), "item": url,
            })
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})

        top = seg.split("/")[0]
        if top in DESTINATION_DIRS:
            dest = {
                "@type": "TouristDestination",
                "name": og_title,
                "description": desc,
                "url": url,
                "image": og_url,
                "touristType": ["Adventure travel", "Sightseeing", "Trekking"],
                "includesAttraction": {"@type": "TouristAttraction", "name": og_title},
                "isPartOf": {"@type": "Place", "name": "Gilgit-Baltistan, Pakistan"},
                "dateModified": TODAY,
            }
            if seg in COORDS:
                lat, lon = COORDS[seg]
                dest["geo"] = {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}
            graph.append(dest)
        else:
            graph.append({
                "@type": "Article",
                "headline": og_title,
                "description": desc,
                "image": og_url,
                "author": {"@type": "Person", "name": "Faisal Zaman", "@id": f"{DOMAIN}/#faisal"},
                "publisher": {"@id": f"{DOMAIN}/#org"},
                "dateModified": TODAY,
                "mainEntityOfPage": url,
            })

    ld = {"@context": "https://schema.org", "@graph": graph}
    tags.append('<script type="application/ld+json">')
    tags.append(json.dumps(ld, ensure_ascii=False, indent=2))
    tags.append("</script>")
    tags.append(END)
    return "\n".join(tags)


def esc(s: str) -> str:
    return s.replace('"', "&quot;")


def inject(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    rel_dir = str(path.parent.relative_to(ROOT))
    rel_dir = "" if rel_dir == "." else rel_dir

    title = extract(r"<title>(.*?)</title>", html)
    # Quote-aware: capture the opening quote and match to the same closing quote,
    # so an apostrophe inside a double-quoted description doesn't truncate it.
    dm = re.search(r'<meta\s+name=["\']description["\']\s+content=(["\'])(.*?)\1', html, re.I | re.S)
    desc = dm.group(2).strip() if dm else ""
    if not desc:
        # Derive a serviceable description from the title.
        base = re.sub(r"\s*[—|-]\s*GB Guide.*$", "", title).strip() or "Gilgit-Baltistan"
        desc = f"{base} — honest local travel guide for Gilgit-Baltistan from GB Guide."

    block = build_block(rel_dir, title, desc)

    if START in html:
        html = re.sub(re.escape(START) + r".*?" + re.escape(END), block, html, flags=re.S)
    else:
        html = re.sub(r"</head>", block + "\n</head>", html, count=1, flags=re.I)

    path.write_text(html, encoding="utf-8")
    return rel_dir


def gen_robots():
    txt = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {DOMAIN}/sitemap.xml\n"
    )
    (ROOT / "robots.txt").write_text(txt, encoding="utf-8")


def gen_sitemap(dirs):
    urls = []
    for rel_dir in sorted(dirs):
        loc = DOMAIN if rel_dir == "" else f"{DOMAIN}/{rel_dir}"
        priority = "1.0" if rel_dir == "" else ("0.9" if rel_dir in DESTINATION_DIRS else "0.7")
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            f"    <priority>{priority}</priority>\n  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def main():
    pages = sorted(p for p in ROOT.rglob("index.html") if "preview" not in p.parts)
    seen_dirs = []
    for p in pages:
        rel = inject(p)
        seen_dirs.append(rel)
        print(f"  injected  /{rel}" if rel else "  injected  / (home)")
    gen_robots()
    gen_sitemap(seen_dirs)
    print(f"\n  robots.txt + sitemap.xml written ({len(seen_dirs)} URLs)")


if __name__ == "__main__":
    main()
