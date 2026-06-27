#!/usr/bin/env python3
"""Inject a 'By Faisal Zaman' author byline (idempotent) after the breadcrumb
on content/guide pages. Links to /about; reinforces the author E-E-A-T signal
on every article, matching the Person author in each page's schema."""
import re, os, glob

START, END = "<!-- BYLINE:START -->", "<!-- BYLINE:END -->"
SKIP = {"about", "explore", "kkh-map", "atm-locator", "status"}  # self/tool pages

def main():
    n = 0
    for f in glob.glob("**/index.html", recursive=True):
        d = os.path.dirname(f)
        if d in SKIP or d == "":  # skip homepage + tool/self pages
            continue
        h = open(f, encoding="utf-8").read()
        if "byline" in h and START not in h:
            pass
        byline = (f'{START}\n<div class="byline">By <a href="/about">Faisal Zaman</a>'
                  f'<span class="sep">·</span>Local from Gilgit-Baltistan'
                  f'<span class="sep">·</span>Updated June 2026</div>\n{END}')
        if START in h:
            h2 = re.sub(re.escape(START) + r".*?" + re.escape(END), byline, h, flags=re.S)
        else:
            m = re.search(r'<div class="breadcrumb">.*?</div>\s*</div>', h, re.S)
            if not m:
                continue  # no breadcrumb -> skip (not an article-type page)
            h2 = h[:m.end()] + "\n" + byline + h[m.end():]
        if h2 != h:
            open(f, "w", encoding="utf-8").write(h2); n += 1
    print(f"byline injected on {n} pages")

if __name__ == "__main__":
    main()
