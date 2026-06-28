# Real GB/Pakistan tour-package prices — scraped June 2026

Source: JSON-LD schema + rendered text from non-top-5 operators and TourRadar,
captured 2026-06-29 with research/scrape.js. Excludes noise (listing-page price
bleed, one Rs 803,940 expedition outlier). Confirm before publishing — prices move.

## Domestic operators (PKR, per person, ex-Islamabad unless noted)
| Trip | Days | Price (from) | Source |
|---|---|---|---|
| Naran/Kaghan short | 2–3 d | Rs 9,500 – 16,000 | narankaghantours, pakistantravelplaces |
| Naran/Kaghan + couple | 4 d | Rs 18,500 | narankaghantours |
| Northern combo (Naran/Hunza/Khunjerab) | 5 d | ~Rs 25,000 | narankaghantours |
| Hunza (autumn / cherry blossom) | 5 d | Rs 17,500 – 23,000 | pakistantravelplaces (schema) |
| Hunza tour | 7 d | from Rs 32,000 | narankaghantours |
| Skardu/Shangrila/Khaplu/Shigar/Deosai (private/honeymoon) | 8 d | Rs 160,000 – 200,000 | pakistantravelplaces |
| Economical Pakistan tour | 3–4 d | Rs 7,500 – 15,500 | pakistantravelplaces |

## International / foreigner-facing (USD, TourRadar marketplace)
| Trip | Days | Price range | 
|---|---|---|
| Pakistan tour | 7 d | ~$1,450 – 2,000 |
| Pakistan tour | 10 d | ~$1,900 – 2,800 |
| Hiking & trekking | 5–11 d | ~$1,750 – 2,900 |
| Overall Pakistan range | — | $1,140 – $3,800 |

## Ratings (the trust signal) — NOT captured
Viator, TripAdvisor and GetYourGuide block headless scraping (403/captcha);
TourRadar exposes only listing-level data, not per-tour aggregateRating. Reliable
ways to get operator ratings: (1) 2-min manual Google/TripAdvisor lookup per
operator, or (2) a stealth scrape (puppeteer-extra-stealth) — may still fail, or
(3) Google Places API with a key. NOTE: under the lead-gen model (route inquiries
to Faisal, don't feature top-5), competitor ratings aren't needed on-page — the
trust signal is Faisal's own track record + his travelers' reviews.
