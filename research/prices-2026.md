# Real GB/Pakistan tour-package prices — scraped June 2026 (v2, sitemap-fed)

Source: JSON-LD schema from operator tour-detail pages (via sitemaps) + TourRadar,
captured 2026-06-29 with research/scrape.js. PKR, per person, ex-Islamabad unless noted.

## ⚠️ Accuracy caveats (read before publishing)
- Schema `offer.price` is **not always the headline price** — it can be a deposit/
  teaser. Confirmed anomaly: pakistantravelplaces lists "8 Days Skardu & Deosai" with
  a schema price of Rs 25,500 but a page headline of Rs 160k–190k. **Always cross-check
  one number against the page before quoting it.**
- Treat everything below as *real but indicative ranges*, not fixed quotes.

## Domestic operator packages (clean schema, pakistantravelplaces.com)
| Trip | Days | Price | 
|---|---|---|
| 1-day local (Soon Valley, Khanpur, Mukshpuri) | 1 d | Rs 3,500 – 4,500 |
| Murree / Tolipeer / Shogran short | 2 d | Rs 7,000 – 7,500 |
| Neelum / Naran / Swat / Kumrat | 3 d | Rs 10,500 – 12,500 |
| Kalash & Chitral | 4 d | Rs 14,500 |
| Saral–Dudipatsar trek | — | Rs 16,500 |
| Hunza + Khunjerab | 5 d | Rs 17,500 |
| Hunza + Naltar | 6 d | Rs 19,500 |
| Luxury Autumn Hunza | 5 d | Rs 22,000 |
| **Hunza honeymoon (luxury/private)** | 5 d | **Rs 160,000** |
| **Skardu honeymoon (luxury/private)** | 8 d | **Rs 190,000** |
| Skardu + Deosai (group; see caveat) | 8 d | headline Rs 160k–175k (schema showed 25.5k = likely deposit) |

## Cross-checked banding (use these on pages)
- **Budget group, by road:** short trips Rs 3.5k–16k; multi-day northern (Naran/Hunza) Rs 17k–25k.
- **Mid Hunza/Naran:** Rs 17k–25k (5–6 d).
- **Premium / private / honeymoon:** Rs 160,000–200,000 (5–8 d, Hunza or Skardu).

## International / foreigner-facing (USD, TourRadar)
7-day ~$1,450–2,000 · 10-day ~$1,900–2,800 · trekking ~$1,750–2,900 · overall $1,140–3,800.

## Ratings — NOT available via scraping
Pakistan tours carry too few reviews for `aggregateRating` schema; Viator/TripAdvisor
block headless. Reliable options: Google Places API (needs key) or 2-min manual lookup.
Under the lead-gen model, competitor ratings aren't needed on-page anyway.
