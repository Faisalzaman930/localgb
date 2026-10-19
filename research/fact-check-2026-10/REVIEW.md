# GB Guide fact-check — October 2026: your review list

Everything below is in the local copy only (branch `content/fact-check-oct-2026`). Nothing is committed or pushed.

## What changed
- 174 of 190 pages corrected (about 1,040 fixes), each logged with old → new and a source in `logs/`.
- `FACTS.md` re-verified against sources as of 16–19 Oct 2026; source evidence in `facts-*.md`.
- Generator scripts and data in `research/` updated, so rebuilding hotels, restaurants, month, honeymoon and trek pages reproduces the fixes.
- `byline_inject.py` now keeps each page's own "Updated" date instead of resetting everything to June 2026.
- Footer "Last updated October 2026" sitewide; sitemap `lastmod` refreshed for the 174 changed pages.
- Checks passed: all structured data (JSON-LD) parses, all inline scripts compile (incl. planner), no em dashes added.

## Decisions only you can make
1. **"I'm from Hunza"** on the Hunza tour pages and the Hunza hotels/food intros. An agent changed it to "Gilgit-Baltistan" on tours/hunza only. Which is right for you?
2. **Agencies:** agencies/index lists 6 "personally vetted" agencies, but the Hunza/Skardu/Islamabad/K2 agency pages say "we don't have a vetted list yet". Keep the 6, or soften the index?
3. **Raikot anecdote:** homepage/About say you "haggled" a jeep at Raikot Bridge; fares are now union-fixed. Keep as a past story or reword?
4. **Month page titles** ("Hunza/Skardu in January 2026"…): Jan–Sep are now in the past. Roll to 2027?
5. **Homepage "169 honest guides"** counter: keep, update, or drop?
6. **Planner cost tiers** (Rs 6,500 / 12,000 / 15,000 / 18,000 / 20,000 / 45,000+ per day) were interpolated from the fact sheet bands. Sanity-check.

## Needs local confirmation (no reliable online source)
- **Are these open in 2026?** Glacier Breeze (Passu), Jahaan (Gulmit), and the named hotels/restaurants/cafes on the Hunza, Skardu, Gilgit, Ghizer, Astore and Naran pages; Hunza Embassy tier and "new pool/spa"; PTDC motels; Gilgit Museum; Phander hotels.
- **Local fares** (softened to "confirm locally"): Attabad boats, shared jeeps/Suzukis, NATCO valley fares, Gilgit–Skardu shared/private car, Gilgit–Karimabad, Eagle's Nest jeep, Naltar/Kargah taxis, homestays (Chapursan/Shimshal), fort fees for Pakistanis, guide day rate, paragliding/rafting.
- **Roads after the 2026 floods:** are Naltar, Haramosh, Hushe, Astore (Khachak), Hisper/Nagar and the Jaglot–Skardu road fully restored? If yes, the flood caveats can be removed.
- **Status page:** override check dates are still 27 June 2026; Babusar/Deosai live status for late October.
- **Local details:** Khunjerab NP camping rules; Karambar/Darkot permits; Naltar winter road; Fairy Meadows phone signal; Shigar "Rock Bridge"; Manthokha facilities/fee; Sarfaranga distance; Serena forts open in winter; Upper Kachura route; tumuro tea and diram phitti wording; "Hunza water" (mulberry) wording; Ganish carvings age.
- **Distances derived, not sourced:** Chilas–Raikot, Lulusar, Gupis/Teru/Danyore/Bagrot, and kkh-map markers (Gilgit at km 545 on the map vs 575 on the KKH route page).
- **Trek operator data:** prices, ratings, licence numbers and a few internal mismatches (Trango, Skardu Trekkers, Chogori, TripMaker, Hunza Guides, Chogho Lingsa) need a fresh pull from the operators' sites.

Full per-page detail: `logs/log-*.md` (each has a "Flag for Faisal" section) and `logs/log-resolve.md`.
