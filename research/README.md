# GB Guide — tour-package scraper

Renders operator websites with your installed Google Chrome (so JavaScript runs
and prices/itineraries that plain HTTP can't see are captured), finds package
pages, and extracts structured data.

## Why a browser scraper
Most PK operator sites are JavaScript-rendered — `curl`/simple fetch returns only
the empty shell. This uses **puppeteer-core + your installed Chrome**, so it sees
exactly what a visitor sees. (Note: many operators publish *durations &
itineraries* but say "contact for price" — the scraper grabs prices only where
they actually exist.)

## Setup (one time)
```
cd research
npm install            # installs puppeteer-core (uses your Chrome, no download)
```

## Use
1. Put operator URLs in `seeds.txt`, one per line. **Best results: a `/tours`
   or `/packages` listing URL, not just the homepage.**
2. Your top-5 SERP competitors are auto-skipped — list their domains in
   `EXCLUDE` at the top of `scrape.js`.
3. Run:
```
node scrape.js
```
4. Output:
   - `packages.csv`  — open in Excel/Sheets: operator, title, durations, prices, includes, url
   - `packages.json` — same data, structured
   - `raw/*.html`    — the fully-rendered HTML of each page (so Claude can parse
     any specific package in detail later)

## Tuning (top of scrape.js)
- `maxPagesPerSeed` — safety cap per operator (default 25)
- `pkgUrl` — regex deciding which links count as package pages
- `politenessMs` — delay between page loads (be respectful)
- `EXCLUDE` — domains to skip entirely

## Then
Hand `packages.csv` (or the `raw/` files) back to Claude → real packages get
written into the `/tours/*` pages, top-5 excluded, all CTAs routed to you.
