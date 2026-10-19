#!/usr/bin/env python3
"""
Photo credits for Wikimedia Commons images (CC BY / CC BY-SA need author,
licence and source shown wherever the photo is used).

Reads photo_credits.json and, idempotently:
  - adds a small credit line just above <footer> on every page whose <body>
    shows one of the credited photos (between PHOTO-CREDITS markers, so
    nav_footer.py, which rewrites <footer>, never touches it)
  - rebuilds the full list on /photo-credits (between PHOTO-LIST markers)

Run after adding/changing photos or pages:  python3 photo_credits.py
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CREDITS = json.loads((ROOT / "photo_credits.json").read_text(encoding="utf-8"))

START, END = "<!-- PHOTO-CREDITS:START -->", "<!-- PHOTO-CREDITS:END -->"
LIST_START, LIST_END = "<!-- PHOTO-LIST:START -->", "<!-- PHOTO-LIST:END -->"
LINK = 'style="color:inherit;text-decoration:underline;text-underline-offset:2px"'


def credit(name: str) -> str:
    c = CREDITS[name]
    e = html.escape
    lic = (f'<a href="{e(c["license_url"])}" rel="license noopener" target="_blank" {LINK}>{e(c["license"])}</a>'
           if c["license_url"] else e(c["license"]))
    return (f'<a href="{e(c["source"])}" rel="noopener" target="_blank" {LINK}>{e(c["title"])}</a>'
            f' by {e(c["artist"])}, {lic}')


def page_block(names: list) -> str:
    items = " · ".join(credit(n) for n in names)
    label = "Photo" if len(names) == 1 else "Photos"
    return (f'{START}\n<div class="photo-credit" style="max-width:1100px;margin:2.5rem auto 1.5rem;'
            f'padding:0 1.5rem;font-size:0.72rem;line-height:1.7;color:var(--cream-2,#6B6458);text-align:center">'
            f'{label}: {items}, via Wikimedia Commons (resized). '
            f'<a href="/photo-credits" {LINK}>All photo credits</a></div>\n{END}\n')


def photos_shown(doc: str) -> list:
    body = doc.split("</head>", 1)[-1]
    body = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", body, flags=re.S)
    seen = []
    for name in re.findall(r"/images/([\w.-]+)", body):
        if name in CREDITS and name not in seen:
            seen.append(name)
    return seen


def main():
    pages = 0
    for path in sorted(ROOT.rglob("index.html")):
        if any(p in path.parts for p in (".git", "research", "node_modules", "preview")):
            continue
        doc = path.read_text(encoding="utf-8")
        new = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", doc, flags=re.S)
        names = photos_shown(new)
        if names and "<footer>" in new:
            new = new.replace("<footer>", page_block(names) + "<footer>", 1)
            pages += 1
        if path.parent.name == "photo-credits" and LIST_START in new:
            rows = "\n".join(
                f'<li><strong>{html.escape(n)}</strong> - {credit(n)}</li>' for n in sorted(CREDITS))
            new = re.sub(re.escape(LIST_START) + r".*?" + re.escape(LIST_END),
                         f"{LIST_START}\n<ul class=\"credit-list\">\n{rows}\n</ul>\n{LIST_END}", new, flags=re.S)
        if new != doc:
            path.write_text(new, encoding="utf-8")
    print(f"photo credits on {pages} pages; {len(CREDITS)} photos listed")


if __name__ == "__main__":
    main()
