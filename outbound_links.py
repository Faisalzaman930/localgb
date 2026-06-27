#!/usr/bin/env python3
"""Inject a curated 'Official sources & further reading' block (idempotent)
on pages where authoritative outbound links add real E-E-A-T / GEO value.
Only confident, long-lived URLs (Wikipedia, PIA, NHA, CKNP, PMD)."""
import re, os, glob

W = "https://en.wikipedia.org/wiki/"
PIA = ("Pakistan International Airlines (PIA)", "https://www.piac.com.pk")
NHA = ("National Highway Authority — road updates", "https://nha.gov.pk")
CKNP = ("Central Karakoram National Park (permits)", "https://www.cknp.org")
PMD = ("Pakistan Meteorological Department", "https://www.pmd.gov.pk")
GB = ("Gilgit-Baltistan — overview", W + "Gilgit-Baltistan")

OUTBOUND = {
    "mountains": [("Highest mountains of Pakistan", W + "List_of_mountains_in_Pakistan"), ("Karakoram", W + "Karakoram")],
    "mountains/k2": [("K2 — Wikipedia", W + "K2")],
    "mountains/nanga-parbat": [("Nanga Parbat — Wikipedia", W + "Nanga_Parbat")],
    "mountains/broad-peak": [("Broad Peak — Wikipedia", W + "Broad_Peak")],
    "mountains/gasherbrum": [("Gasherbrum I — Wikipedia", W + "Gasherbrum_I"), ("Gasherbrum II", W + "Gasherbrum_II")],
    "mountains/rakaposhi": [("Rakaposhi — Wikipedia", W + "Rakaposhi")],
    "mountains/masherbrum": [("Masherbrum — Wikipedia", W + "Masherbrum")],
    "mountains/spantik": [("Spantik — Wikipedia", W + "Spantik")],
    "mountains/haramosh-peak": [("Haramosh — Wikipedia", W + "Haramosh")],
    "mountains/laila-peak": [("Laila Peak — Wikipedia", W + "Laila_Peak")],
    "mountains/trango-towers": [("Trango Towers — Wikipedia", W + "Trango_Towers")],
    "travel/skardu-flights": [PIA, ("Skardu International Airport", W + "Skardu_International_Airport")],
    "travel/gilgit-airport": [PIA, ("Gilgit Airport", W + "Gilgit_Airport")],
    "travel/islamabad-to-skardu": [PIA],
    "travel/lahore-to-skardu": [PIA],
    "travel/karakoram-highway": [NHA, ("Karakoram Highway — Wikipedia", W + "Karakoram_Highway")],
    "karakoram-highway": [NHA, ("Karakoram Highway — Wikipedia", W + "Karakoram_Highway")],
    "kkh-map": [NHA, ("Karakoram Highway — Wikipedia", W + "Karakoram_Highway")],
    "travel/noc-permits-gb": [GB, CKNP],
    "trekking/k2-base-camp": [CKNP],
    "trekking/k2-base-camp/permits": [CKNP],
    "trekking/k2-base-camp/cost": [CKNP],
    "trekking/k2-base-camp/itinerary": [CKNP],
    "trekking/k2-base-camp/best-time": [CKNP],
    "trekking/concordia": [CKNP],
    "trekking/gondogoro-la": [CKNP],
    "trekking/biafo-hispar-snow-lake": [CKNP],
    "status": [NHA, PMD],
    "weather": [PMD],
    "deosai": [("Deosai National Park — Wikipedia", W + "Deosai_National_Park")],
    "khunjerab": [],
    "hunza/khunjerab-pass": [("Khunjerab Pass — Wikipedia", W + "Khunjerab_Pass")],
    "things-to-do/shandur-polo-festival": [("Shandur — Wikipedia", W + "Shandur_Top")],
}

START, END = "<!-- SOURCES:START -->", "<!-- SOURCES:END -->"

def main():
    n = 0
    for page, links in OUTBOUND.items():
        if not links: continue
        f = page + "/index.html"
        if not os.path.exists(f): continue
        items = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t} ↗</a></li>' for t, u in links)
        block = (f'{START}\n<div class="sources"><div class="sources-title">Official sources &amp; further reading</div>'
                 f'<ul>{items}</ul></div>\n{END}')
        h = open(f, encoding="utf-8").read()
        if START in h:
            h = re.sub(re.escape(START) + r".*?" + re.escape(END), block, h, flags=re.S)
        elif "<footer>" in h:
            h = h.replace("<footer>", block + "\n<footer>", 1)
        else:
            continue
        open(f, "w", encoding="utf-8").write(h); n += 1
    print(f"outbound sources injected on {n} pages")

if __name__ == "__main__":
    main()
