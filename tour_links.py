#!/usr/bin/env python3
"""
Descriptive internal links to the tour pages from high-traffic guides.

Adds one short "rather book a tour?" line (between TOUR-LINKS markers) just
above the related-guides block on each page in LINKS. Idempotent.

Run after page changes:  python3 tour_links.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START, END = "<!-- TOUR-LINKS:START -->", "<!-- TOUR-LINKS:END -->"

HUNZA = ("/tours/hunza", "Hunza tour packages compared")
SKARDU = ("/tours/skardu", "Skardu tour packages")
FAIRY = ("/tours/fairy-meadows", "Fairy Meadows tour packages and trip cost")
GILGIT = ("/tours/gilgit", "Gilgit tour packages")
ISB = ("/tours/from-islamabad", "tours from Islamabad")
LHR = ("/tours/from-lahore", "tours from Lahore")
GB = ("/tours", "all Gilgit-Baltistan tours")
H5 = ("/tours/hunza/5-days", "a 5-day Hunza tour")
HFAM = ("/tours/hunza/family", "Hunza with the family")
HBUD = ("/tours/hunza/budget", "cheap Hunza tours")
HMOON = ("/tours/hunza/honeymoon", "Hunza honeymoon packages")

LINKS = {
    "tours": ("Planning Hunza?", [HUNZA, H5, HFAM, HBUD, HMOON]),
    "tours/hunza/honeymoon": ("Other ways to do Hunza:", [HUNZA, H5, HFAM]),
    "tours/hunza/5-days": ("Other ways to do Hunza:", [HUNZA, HBUD, HFAM]),
    "tours/hunza/family": ("Other ways to do Hunza:", [HUNZA, H5, HMOON]),
    "tours/hunza/budget": ("Other ways to do Hunza:", [HUNZA, H5, HFAM]),
    "hunza": ("Rather have your trip organised?", [HUNZA, H5, HFAM, HBUD]),
    "hunza/places-to-visit": ("Want these sights in a ready-made trip?", [HUNZA, ISB]),
    "hunza/things-to-do": ("Prefer a guided trip that covers these?", [HUNZA, HFAM, FAIRY]),
    "hunza/karimabad": ("Planning a trip to Hunza?", [HUNZA, ISB]),
    "hunza/food": ("Planning the rest of your Hunza trip?", [HUNZA]),
    "hunza/weather": ("Picked your month?", [HUNZA, FAIRY]),
    "skardu": ("Rather have your trip organised?", [SKARDU, ISB, LHR]),
    "skardu/restaurants": ("Planning the rest of your trip?", [SKARDU, HUNZA]),
    "gilgit/restaurants": ("Planning the rest of your trip?", [GILGIT, HUNZA, FAIRY]),
    "travel/best-time-to-visit-gb": ("Know when you're going?", [HUNZA, SKARDU, FAIRY, GB]),
    "travel/7-day-itinerary": ("Prefer a ready-made version of this itinerary?", [HUNZA, H5, SKARDU]),
    "travel/14-day-itinerary": ("Prefer a ready-made trip?", [HUNZA, SKARDU, FAIRY]),
    "travel/budget-gb-itinerary": ("Comparing against a package?", [HBUD, HUNZA, LHR]),
    "fairy-meadows/how-to-reach": ("Rather not arrange the jeep and hike yourself?", [FAIRY]),
    "fairy-meadows/best-time-to-visit": ("Know when you're going?", [FAIRY, HUNZA]),
}


def block(lead, links):
    a = [f'<a href="{u}">{t}</a>' for u, t in links]
    joined = a[0] if len(a) == 1 else ", ".join(a[:-1]) + " or " + a[-1]
    return (f'{START}\n<div class="callout" style="max-width:820px;margin:2rem auto;"><p>'
            f'<strong>{lead}</strong> See {joined} - real itineraries side by side, from a local.</p></div>\n{END}\n')


def main():
    done = 0
    for rel, (lead, links) in LINKS.items():
        path = ROOT / rel / "index.html"
        s = path.read_text(encoding="utf-8")
        new = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
        anchor = next((a for a in ("<!-- RELATED:START -->", "<!-- WA-HELP:START -->", "<!-- PHOTO-CREDITS:START -->", "<footer>") if a in new), None)
        new = new.replace(anchor, block(lead, links) + anchor, 1)
        if new != s:
            path.write_text(new, encoding="utf-8")
        done += 1
    print(f"tour links on {done} pages")


if __name__ == "__main__":
    main()
