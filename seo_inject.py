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
DEFAULT_OG = f"{DOMAIN}/images/hunza-hero.webp"
TODAY = datetime.date.today().isoformat()

# Folder -> hero image used for OG/Twitter previews (falls back to DEFAULT_OG).
OG_IMAGES = {
    "": "hunza-hero.webp",
    "hunza": "hunza-hero.webp",
    "gilgit": "gilgit-hero.webp",
    "skardu": "skardu-hero.webp",
    "fairy-meadows": "fairymeadows-hero.webp",
    "naran-kaghan": "naran-kaghan-hero.webp",
    "mountains": "hero-nanga-parbat.jpg",
    "trekking": "hero-k2.jpg",
    "things-to-do": "hero-stargazing.jpg",
    "deosai": "deosai-hero.webp",
    "naltar": "naltar-hero.webp",
    "astore": "astore-hero.webp",
    "gojal": "gojal-hero.webp",
    "ghizer": "ghizer-hero.webp",
    "yasin": "yasin-hero.webp",
    "trekking/concordia": "concordia-hero.webp",
    "trekking/rakaposhi-base-camp": "rakaposhi-hero.webp",
    "mountains/rakaposhi": "rakaposhi-hero.webp",
    "hunza/attabad-lake": "attabad-hero.webp",
    "hunza/baltit-fort": "baltit-fort-hero.webp",
    "hunza/altit-fort": "altit-fort-hero.webp",
    "hunza/borith-lake": "borith-lake-hero.webp",
    "hunza/gulmit": "gulmit-hero.webp",
    "hunza/shimshal-valley": "shimshal-hero.webp",
    "mountains/spantik": "spantik-hero.webp",
    "mountains/masherbrum": "masherbrum-hero.webp",
    "mountains/k2": "k2-hero.webp",
    "trekking/k2-base-camp": "k2-hero.webp",
    "gilgit/bagrot-valley": "bagrot-valley-hero.webp",
    "gilgit/kargah-buddha": "kargah-buddha-hero.webp",
    "skardu/khaplu": "khaplu-hero.webp",
    "skardu/khaplu-palace": "khaplu-hero.webp",
    "skardu/satpara-lake": "satpara-lake-hero.webp",
    "skardu/sheosar-lake": "sheosar-lake-hero.webp",
    "skardu/shigar-valley": "shigar-valley-hero.webp",
    "mountains/nanga-parbat": "nanga-parbat-hero.webp",
    "mountains/masherbrum": "masherbrum-hero.webp",
    "mountains/spantik": "spantik-hero.webp",
    "karakoram-highway": "karakoram-highway-hero.webp",
    "trekking/nanga-parbat-base-camp": "nanga-parbat-hero.webp",
    "trekking/nanga-parbat-rupal-face": "nanga-parbat-hero.webp",
    "trekking/masherbrum-base-camp": "masherbrum-hero.webp",
    "trekking/spantik-base-camp": "spantik-hero.webp",
    "trekking/naltar-lakes": "naltar-hero.webp",
    "tours/skardu": "skardu-hero.webp",
    "tours/naran-kaghan": "naran-kaghan-hero.webp",
    "tours/hunza": "hunza-hero.webp",
    "tours/gilgit-baltistan": "hunza-hero.webp",
    "tours/from-islamabad": "hunza-hero.webp",
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
