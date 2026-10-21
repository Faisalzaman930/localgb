#!/usr/bin/env python3
"""
"Trip cost from <city>" sections on /tours/from-lahore, /tours/from-karachi and
/tours/from-islamabad - one heading per destination, so searches like
"skardu trip cost from karachi" land on a clear answer.

Fares and times follow FACTS.md (Oct 2026); package "from" prices follow the
live-checked comparisons in research/tours/. All-in estimates reuse each page's
existing figures so the page stays consistent. Idempotent (CITY-COSTS markers).

Run after editing:  python3 city_costs.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START, END = "<!-- CITY-COSTS:START -->", "<!-- CITY-COSTS:END -->"

CITIES = {
  "lahore": {
    "anchor": "<h2>When to go",
    "intro": "Here's what each trip costs from Lahore in 2026, per person, with the fastest way to get there. Prices are published \"from\" prices - always confirm what's included.",
    "dests": [
      ("Hunza trip cost from Lahore",
       "Coaches run from Lahore to Hunza for about PKR 6,900-8,400 each way (18-22 hours, best split over two or three days). The cheapest published package, a 5-day Hunza and Khunjerab trip via Babusar, starts at about Rs 17,500 and departs from Lahore. Private Hunza trips run about Rs 29,500-69,500 for 3-7 days, plus the connection.",
       "/tours/hunza", "Hunza tour packages compared"),
      ("Skardu trip cost from Lahore",
       "By road it's about 970 km and 18-22 hours; coaches cost about PKR 6,900-8,400 each way. PIA lists a nonstop Lahore-Skardu flight (check how often it runs), or connect through Islamabad, where flights to Skardu cost about PKR 18,000-30,000 one way. An 8-day group trip by road starts at about Rs 25,500 and ends back in Lahore.",
       "/tours/skardu", "Skardu tour packages compared"),
      ("Naran Kaghan trip cost from Lahore",
       "Many 3-day group trips pick up in Lahore, from about Rs 11,500 per person, and get back around midnight on the last day. Joining from Islamabad instead, it comes to roughly Rs 13,000-15,000 all-in. Couples' packages are about Rs 40,000-60,000.",
       "/tours/naran-kaghan", "Naran Kaghan tour packages and prices"),
      ("Fairy Meadows trip cost from Lahore",
       "Karakoram Backpackers' 5-day Fairy Meadows trip departs from Lahore or Islamabad, from about US$500 per person with the jeep included. Doing it yourself, the Raikot-Tato jeep alone is about PKR 16,000-22,500 return per jeep.",
       "/tours/fairy-meadows", "Fairy Meadows tour packages and trip cost"),
    ],
    "extra": "<h3>From Faisalabad, Sialkot, Gujranwala or Multan</h3><p>There are few departures from these cities, so most people join a trip in Lahore or Islamabad. Ask the operator about pick-up points before you book.</p>",
  },
  "karachi": {
    "anchor": "<h2>When to go",
    "intro": "Here's what each trip costs from Karachi in 2026, per person, including how to get north. The flights are the biggest part of the budget, so book them early.",
    "dests": [
      ("Skardu trip cost from Karachi",
       "PIA flies direct from Karachi to Skardu about 3-4 times a week (around 2 h 20) - the quickest way north. Otherwise fly to Islamabad and connect (Islamabad-Skardu flights are about PKR 18,000-30,000 one way). A 7-9 day Skardu trip comes to roughly Rs 70,000-85,000 all-in with return flights; Skardu group packages from Islamabad start at about Rs 25,500-39,500 before flights.",
       "/tours/skardu", "Skardu tour packages compared"),
      ("Hunza trip cost from Karachi",
       "Fly to Islamabad, then either fly on to Gilgit (about an hour, PIA only, often cancelled) or join a road trip. A 7-9 day Hunza trip comes to roughly Rs 70,000-85,000 all-in with flights; packages from Islamabad and Lahore start at about Rs 17,500 before flights.",
       "/tours/hunza", "Hunza tour packages compared"),
      ("Hunza and Skardu together from Karachi",
       "The best use of the long journey: fly into Skardu, drive to Hunza (Skardu-Gilgit is about 4-5 hours), and fly home from Gilgit or Islamabad. The full circuit comes to roughly Rs 85,000-100,000+ all-in.",
       "/tours/gilgit", "Gilgit-Baltistan tour packages and prices"),
      ("Naran Kaghan trip cost from Karachi",
       "Fly to Islamabad and join a 3-day trip there, from about Rs 11,500 per person - so the total is mostly your return flights. Naran is 6-9 hours by road from Islamabad.",
       "/tours/naran-kaghan", "Naran Kaghan tour packages and prices"),
      ("Fairy Meadows trip cost from Karachi",
       "Fly to Islamabad, then take a 5-6 day trip (from about US$500 per person, jeep included, with Karakoram Backpackers) or combine it with Hunza.",
       "/tours/fairy-meadows", "Fairy Meadows tour packages and trip cost"),
    ],
    "extra": "",
  },
  "islamabad": {
    "anchor": "<h2>When to go in 2026</h2>",
    "intro": "Here's what each trip costs from Islamabad and Rawalpindi in 2026, per person, by road and by air.",
    "dests": [
      ("Hunza trip cost from Islamabad",
       "By road it's 14-20 hours (often two days); coaches from Rawalpindi cost about PKR 4,850-6,100 each way. By air, Islamabad-Gilgit is about an hour on PIA (PKR 19,000-28,000 one way, often cancelled), then 2-3.5 hours by road. Packages start at about Rs 17,500 for 5 days by road.",
       "/tours/hunza", "Hunza tour packages compared"),
      ("Skardu trip cost from Islamabad - by air or by road",
       "By air: about an hour on PIA, Airblue or AirSial jets, PKR 18,000-30,000 one way. By road: 16-18 hours; coaches cost about PKR 5,500-6,200. Group trips by road run about Rs 25,500-39,500 for 7-8 days; trips by air run about Rs 63,000-145,000 for 4-6 days.",
       "/tours/skardu", "Skardu tour packages compared"),
      ("Fairy Meadows trip cost from Islamabad",
       "It's 10-14 hours to Raikot Bridge (Babusar is shorter in summer), then the Raikot-Tato jeep (about PKR 16,000-22,500 return per jeep) and a 2-3 hour walk. Packages start at about US$500 per person for 5 days.",
       "/tours/fairy-meadows", "Fairy Meadows tour packages and trip cost"),
      ("Naran Kaghan trip cost from Islamabad",
       "Naran is 6-9 hours by road. 3-day group trips start at about Rs 11,500 per person; couples' packages are about Rs 40,000-60,000.",
       "/tours/naran-kaghan", "Naran Kaghan tour packages and prices"),
    ],
    "extra": "",
  },
}


def block(c):
    secs = "".join(f'<h3>{h}</h3><p>{t} See <a href="{u}">{a}</a>.</p>' for h, t, u, a in c["dests"])
    return (f'{START}\n<section class="city-costs"><h2>Trip cost from {c["name"]}, by destination</h2>'
            f'<p>{c["intro"]}</p>{secs}{c["extra"]}'
            '<p>Worried about safety or road closures? Read <a href="/travel/is-gilgit-baltistan-safe">is Gilgit-Baltistan safe?</a> and '
            '<a href="/updates/is-gilgit-baltistan-open-for-tourists-2026">what\'s open in 2026</a>.</p></section>\n{END}\n')


def main():
    for city, c in CITIES.items():
        c["name"] = city.capitalize()
        path = ROOT / "tours" / f"from-{city}" / "index.html"
        s = path.read_text(encoding="utf-8")
        new = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
        if c["anchor"] not in new:
            raise SystemExit(f"anchor missing on from-{city}: {c['anchor']}")
        new = new.replace(c["anchor"], block(c) + c["anchor"], 1)
        if new != s:
            path.write_text(new, encoding="utf-8")
        print(f"from-{city}: {len(c['dests'])} destination sections")


if __name__ == "__main__":
    main()
