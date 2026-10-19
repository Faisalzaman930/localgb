# Resolve pass: "Flag for Faisal" items (19 Oct 2026)

Scope: flags that do not need local knowledge, meaning (a) internal contradictions between pages and (b) facts checkable from reliable web sources. Every changed page has byline "Updated October 2026" and dateModified 2026-10-16. All JSON-LD on the 38 changed HTML pages parses (0 errors). The edited JSON data and .py generators also parse/compile. No em dashes were introduced, and no git or build commands were run.

## RESOLVED

1. **Passu Cones "five" vs "six"** (log-hunza 14). `hunza/index.html` "five shark-fin peaks" → "six shark-fin spires". This matches passu-cones, places-to-visit, things-to-do, karakoram-highway and planner. It is a site-consistency fix only: no independent count was found.
2. **Hussaini old bridge abandoned vs crossable** (hunza 15).
   - `hunza/index.html`: "old bridge (now abandoned) ... cross the old one, use the newer one to come back" → "broken cables of the original bridge still hang alongside it - photogenic, but not crossable".
   - `hunza/passu-cones/index.html`: "both are still standing and crossable" / "new bridge is stable" → "only the current plank bridge is crossable" / "hold both side cables".
   - Source: https://urbanduniya.com/?p=9385 ("broken and buckled cables ... remains of the original bridge"). Wikipedia says the bridge was rebuilt after 2010.
3. **Gupis Fort British- vs Dogra-era** (regions 5).
   - `ghizer/index.html` → "British-era fort built in the 1890s (later used by the Gilgit Scouts and NLI, with a restoration agreed in 2025)".
   - `ghizer/things-to-do/index.html` "ruined Dogra-era fort" → "crumbling British-era fort (built 1890s)".
   - Sources: AKDN/Serena 6 Aug 2025 (https://the.akdn/en/resources-media/whats-new/in-the-media/serena-hotels-partners-with-nli-for-restoration-of-gupis-fort-in-gilgitbaltistan, "built in 1894") and Pamir Times 2017 (Gilgit Scouts/NLI use, deserted).
4. **Gilgit hotels FAQ JSON-LD contradicting visible text** (regions 6). In `gilgit/hotels/index.html`, the JSON-LD answer to "Should I stay near the airport?" was "Generally no ... far from everything". It now matches the visible guidance ("Only if you are flying ... handy when a PIA flight shifts; Jutial/Chinar Bagh quieter; bazaar for budget"). NOTE: this second FAQPage block is hand-added. build_hotels.py does not produce it, so a rebuild would drop it.
5. **Besham "Swat Kohistan district"** (regions 11).
   - `karakoram-highway/index.html` → "Besham is in Shangla district; just north the road enters the Indus gorge of Kohistan". Source: https://en.wikipedia.org/wiki/Besham.
   - "Komila, just north, has Buddhist rock carvings" was unsourced and Komila is ~75-80 km north (opposite Dasu, Upper Kohistan per Wikipedia Dasu). It now reads "Past Komila and Dasu (roughly 75-80km further), the Shatial and Chilas rock-art sites hold Buddhist-era carvings".
6. **KKH page stop distances vs FACTS** (regions 3, 11; travel 4).
   - `karakoram-highway/index.html` km markers changed: Besham 310→250, Chilas 500→445, Raikot 540→490, Gilgit 600→575, Karimabad 660→675, Passu 700→720, Sost 790→755. Khunjerab stays 840.
   - The old markers were internally inconsistent: Gilgit→Karimabad was only 60 km, against FACTS 95-110.
   - `hunza/how-to-reach/index.html`: Besham ~310km → ~250km; Chilas ~500km → ~430-450km.
   - `travel/karakoram-highway/index.html`: Besham→Chilas "~140-180 km" (derived by subtraction) → "~195 km".
   - Sources: Wikipedia Besham (~250 km from Rawalpindi-Islamabad); distancesfrom.com (ISB-Besham 264 km, Besham-Chilas 196-197 km, Besham-Gilgit via Chilas 333 km); Wikipedia Khunjerab Pass (870 km from Islamabad, 270 km from Gilgit, 75 km from Sost); GB Tourism (Sost 184 km from Gilgit).
   - **FACTS.md note:** these sources put ISB→Gilgit at ~575-600 km, above FACTS' LOW-confidence 520-560 km. FACTS' Hunza↔Khunjerab 120-135 km also looks short: Karimabad-Passu ~46 + Passu-Sost ~35-40 + Sost-pass 75-86 ≈ 155-170 km. Recommend widening both FACTS ranges. The FACTS-based "~520-560km" figures elsewhere were not changed, and `kkh-map` (Gilgit at km 545) was left as is.
7. **Islam's arrival in Gilgit** (regions 6). `gilgit/kargah-buddha/index.html` "9th-11th centuries" (x2) → "from around the 13th-14th centuries". Source: https://en.wikipedia.org/wiki/History_of_Gilgit-Baltistan (13th-century Islamic influence; 14th century via Sufi preachers in Baltistan and Tarkhan rulers in Gilgit).
8. **Gilgit-Chitral via Shandur "~450km"** (regions 3). `ghizer/how-to-reach/index.html` → "approximately 385-390km". Sources: Wikipedia Gilgit-Shandur Road (216 km) / Shandur Pass (212 km from Gilgit) + Wikipedia Chitral-Shandur Road (172 km).
9. **Rama Meadows 3,500 m / Rama Lake 3,600 m** (regions 9). `astore/index.html`: Rama Meadows (3,500m) → (~3,300m); Rama Lake "approximately 3,600m" → 3,500m; camp "~3,600m" → "~3,500m". Sources: Wikipedia Rama Lake (valley ~3,300 m); GB Tourism Dept https://tourismdept.gbit.gov.pk/tour/id/16 (lake ~3,507 m).
10. **Naltar "traditional Burusho settlement"** (regions 7). `naltar/index.html`: tag "traditional Burusho culture" → "Shina and Gujjar culture"; body → "traditional mountain settlement of Shina-speaking and Gujjar families". Source: Friday Times, "Where the Gujjars rest" (2019): "Shins, Yeskhuns and Gujars are the main tribes ... speak both Shina and Gujri".
11. **Shogran cable car "PKR 400 return, 8am-6pm"** (regions 10). No source shows a cable car to or at Shogran: Graana says only jeeps go up to Siri Paye, and Zameen's list of Pakistani chairlifts has none at Shogran. All 5 cable-car mentions in `naran-kaghan/index.html` were removed or replaced ("Jeep up from Kiwai or drive"; "Jeeps also run on from Shogran to Siri Paye (confirm the fare locally)").
12. **Teru and Imit placed in Yasin** (regions 4).
    - `yasin/index.html` (meta/og/twitter/JSON-LD descriptions x4, two gem cards), `yasin/things-to-do/index.html` and `yasin/weather/index.html` were edited.
    - "Teru Meadows" → "Upper Yasin (Summer) Pastures" in side valleys such as Thui and Qorqolti. "Immit Village" → "Upper Yasin (Orchard) Villages" such as Sandi and Barkulti.
    - Source: https://en.wikipedia.org/wiki/Yasin_Tehsil (village/union-council lists, which do not include Teru or Imit). Teru is in upper Ghizer and Imit in Ishkoman.
13. **Luxus Hunza "Aliabad"** (tours 9).
    - `tours/hunza/honeymoon/index.html` Aliabad → "Ainabad, Attabad Lake". `hunza/hotels/index.html` (table and card) "Gulmit" → same.
    - Source: Booking.com listing address "Luxus Hunza, Ainabad, Hunza" (Expedia lists it under Aina Abad).
    - Source sync: `research/build_honeymoon.py` STAY_OVERRIDES area and `research/hotels/hunza.json` area.
14. **Eagle's Nest rating 3.0 vs 4.0** (task list; tours 10).
    - Tripadvisor shows 4.0/5, 142 reviews, #3 of 18 in Hunza (https://www.tripadvisor.co.uk/Hotel_Review-g469409-d1027139-Reviews-Eagle_s_Nest_Hotel-Hunza_Gilgit_Baltistan.html, read 19 Oct 2026).
    - Honeymoon "3.0 Tripadvisor (139)" → "4.0 (142)", and "#3 of 17 ... notably mixed reviews" → "#3 of 18 ... (4.0/5), though reviews are mixed on service".
    - hunza/hotels: (141) → (142), "#3 of 17" → "#3 of 18", and type "Mid-range" → "Upper tier" so it matches the honeymoon page and its PKR 23,000-25,000 price.
    - Source sync: build_honeymoon.py STAY_OVERRIDES and research/hotels/hunza.json (type, reviews, pros).
15. **"Shangrila Mountain Resort dining room" in Gilgit** (core). Shangrila Resort is at Lower Kachura, Skardu (FACTS). In `planner/index.html`, the Gilgit luxury food line now reads "Serena Gilgit restaurant or the Ramada Gilgit restaurant". Ramada is the site's own #1 Gilgit hotel.
16. **Islamabad-Chitral PIA flights** (tours 13). In `tours/chitral/index.html` the FAQ now leads with the road via the Lowari Tunnel, and adds "PIA's Islamabad-Chitral flights were reported suspended in December 2025 (too few ATR aircraft), so check whether they have resumed". Sources: Chitral Today 2 Dec 2025 (Senate reply: flights suspended, only 2 ATRs, load 41%); Dawn 19 Mar 2025 (weekly resumption planned from 5 Apr 2025). No 2026 resumption found.
17. **Trekking hub "Season: Apr - Oct" vs Baltoro Jun-Sep** (treks 11). `trekking/index.html` → "Season: May - Oct (Baltoro Jun - Sep)" (FACTS seasons). The hero is outside the TREKCMP markers, so no source sync is needed.
18. **Stray Chitral FAQPage JSON-LD** (travel 8). The same invisible "Is Chitral part of Gilgit-Baltistan?" FAQPage block was removed from `updates/index.html` and all 5 updates posts (best-time-to-visit, road-pass-status, hunza-autumn-foliage, is-gb-open, skardu-gilgit-flights). No generator script contains it. It also remains on tours/chitral, where it is on-topic; it was not touched there.
19. **Tripako Naltar package price** (treks 4).
    - The operator page (fetched 19 Oct 2026) is a 2021 listing: departure 2 Apr 2021, registration deadline 1 Mar 2021, dateModified 2021-03-26, Rs 14,500.
    - `trekking/naltar-lakes/index.html` (table, standouts, card header and meta, pros, FAQ HTML + JSON-LD) and the `trekking/index.html` hub row now show "Rs 14,500 (2021 listing)". The FAQ range is now "PKR 28,000-30,000 (Tripako's PKR 14,500 is a 2021 listing)".
    - Source sync: new `"price_note": "2021 listing"` in research/treks/naltar-lakes.json. price_str() in build_trek_articles.py and build_treks.py now appends price_note. The JSON good/pros and the build_trek_articles.py FAQ text were updated.
20. **Ian Taylor Trekking HQ "Dublin"** (treks 10). Already fixed before this pass: _ratings.json origin is "Colorado, USA" and the K2 page shows Colorado. No change.
21. **K2 stats freshness** (treks 9). `mountains/k2/index.html` "(around 96 deaths and some 800 summits by August 2023)" + ", with five more deaths in the 2024 and 2025 seasons". Source: Wikipedia List of deaths on eight-thousanders (2024: Ser Muhammad, Hiraide, Nakajima; 2025: Iftikhar Hussain, Guan Jing). No reliable 2024 summit total was found, so the summit figure was not extended.
22. **Chaqchan Mosque date** (skardu 16). The site said "600 years" (skardu x2) and "700 years old" (planner). Both now read "traditionally dated to 1370", and "the oldest" → "one of the oldest" in skardu/index.html and planner. Source: Wikipedia Chaqchan Mosque ("Dating from 1370 ... one of the oldest in the region", date disputed).
23. **Rakaposhi BC altitude** (treks 1; FACTS now ~3,300-3,500 m).
    - `trekking/rakaposhi-base-camp/index.html`: meta/og/twitter/JSON-LD desc x4 changed; "about" → "~3,300-3,500m, with Kacheli Lake around 4,000m above it"; trek-facts → 3,300-3,500m; 2nd FAQPage answer → "Tagaphari ... 3,300-3,500m; Kacheli Lake about 4,000m".
    - `trekking/index.html` card 3,800-4,150m → 3,300-3,500m.
    - Source sync: research/treks/_pagemeta.json (desc + hero_meta) and build_trek_articles.py about. The 2nd FAQPage block is not in any generator.
24. **Rush Lake altitude**: checked. Every mention is 4,694 m or "around 4,700m", which is consistent with FACTS. No change.
25. **"Mahseer" in the Gilgit/Hunza rivers** (regions 6). `gilgit/things-to-do/index.html` → "brown trout and native snow trout (mahseer never established up here)". Source: FAO https://www.fao.org/4/x2614e/x2614e07.htm ("introduction of mahseer into the River Gilgit was not successful"; Northern Areas species list).
26. **Gilgit polo "Sport · October" tag** (regions 6). Confirmed: the Jashan-e-Azadi tournament runs 15 Oct to 1 Nov at the Shahi Polo Ground (https://e-tourism.gbit.gov.pk/festivals-and-events/jashan-e-azadi-gilgit-baltistan-polo-tournament). The tag was kept and one clause was added to the `gilgit/index.html` card.
27. **Rupal circuit "5-7 days via Mazeno and Fairy Meadows"** (regions 9). `astore/index.html` → "A long trek (usually 8-10+ trekking days, roughly 2.5-3 weeks from Islamabad) ... and the Diamir side toward Fairy Meadows". Sources: ATP Mazeno itinerary (8-10 trekking days Tarashing → Diamir BC/Sair); Hunza Guides "Around Nanga Parbat" 19-23 days.
28. **Khaplu → Hushe "30km"** (skardu 7). `skardu/khaplu/index.html` → "Roughly 2.5-3.5h by jeep via Kande". Source: zewanderingfrogs.com (Khaplu-Kande 2-3h + Kande-Hushe 30-45 min). An operator itinerary on trekking/hushe-valley gives Skardu-Hushe as 120 km.
29. **Shimshal facts** (hunza 21). In `hunza/shimshal-valley/index.html`: road "65km" (x7, incl. FAQ JSON-LD) → 56km; population "about 1,200" (x2) → "more than 2,000" / "roughly 2,000-3,000". Shimshal Pass 4,735 m is confirmed. Source: https://en.wikipedia.org/wiki/Shimshal (56 km from Passu; >2,000 / ~3,000 inhabitants; pass 4,735 m).
30. **Deosai bear count** (core). `deosai/index.html` "78 in a 2022 count" → "an estimated 66 (range 58-77) in the 2022 GB Forest and Wildlife survey". `planner/index.html` "only a few dozen" → "a 2022 survey estimated around 66". Sources: GB FWP Brown Bear Survey 2022 PDF (fwegb.gov.pk, "We estimated 66 ... 58 to 77"); Express Tribune 5 Oct 2026.
31. **Borith Lake facilities** (hunza 18). `hunza/borith-lake/index.html`: "no facilities beyond a seasonal chai stall" (x2) → "...and a small hotel or two listed online near the lake (confirm they are open)". Source: Expedia listings "Arcadian Borith Lake Hunza" and "Borith Inn". The byline and dateModified were also brought up to date (they were June / 2026-07-09).
32. **Hunza autumn foliage window** (tours 8). The honeymoon page said "mid-October to early November". The rest of the site (in-autumn "peak Oct 10-25", in-october, best-time) and FACTS say October, so `tours/hunza/honeymoon/index.html` (x4 incl. FAQ JSON-LD) now says "October (peak usually mid-to-late October)". Source sync: build_honeymoon.py (autumn='October' + 2 strings).
33. **PakVoyager Rush Lake 13 vs "12-day" verdict** (treks 3, one item). The operator URL is "13-days-rush-lake-trek...". Verdict → "13-day" in `trekking/rush-lake/index.html` + research/treks/rush-lake.json.
34. **Karimabad ~2,500 m** (hunza 16). Matches FACTS (Towns: Karimabad ~2,500). No change.
35. **Shangrila DC-3 "at the water's edge"** (skardu 3, wording only). Confirmed on land by the lake as a coffee shop (https://www.ruudleeuw.com/off-airport-meast.htm). No change. The fee stays as in FACTS.
36. **Upper Kachura distance** (skardu 5). FACTS: Kachura/Shangrila ~20 km, NOT 35 km. The hike wording used is consistent. No change.
37. **1974 Pattan earthquake / Hazara Motorway E-35 on kkh-map** (core). Both are factual (the 28 Dec 1974 quake devastated Pattan; E-35 runs from Burhan/Hasan Abdal toward Mansehra). No change.

## LEFT FOR FAISAL
- **Named businesses' open status, prices or tiers (all logs):** Gilgit/Hunza/Skardu/Naran hotels, restaurants and cafes, Glacier Breeze, Jahaan, PTDC motels, Hunza Embassy (Splurge vs Mid-range tier and "new pool/spa"), Arish Luxury Suites rating, Café de Hunza in Gilgit, agencies' status/vetting/ratings (incl. Baltistan Tours 4.4 vs 4.3 and Nature Adventure Club being Lahore-based), PTP Kalash availability, K2 Museum fee and whether it is the K2 Hotel museum, Gilgit Museum, AKCC "free". Local knowledge is needed.
- **Local fares with no online source (all logs):** Attabad boats, shared jeeps/Suzukis, NATCO valley fares, Gilgit-Skardu shared/private, Eagle's Nest jeep, Naltar taxi, Kargah taxi, Satpara/Katpana/fishing permits, homestays (Chapursan/Shimshal), Gulmit Museum fee/hours, Baltit Pakistani fee/hours, Ganish tour, Fairy Meadows July premium and camping, NP BC "Rs 500", dorm beds, paragliding/rafting, guide day rate, Lahore-Islamabad coach, Karachi airfare, ISB-Hunza car, Shandur "free to watch", Shigar Fort cafe, Shangrila restaurant.
- **Editorial / voice items (excluded by brief):** "I'm from Hunza" wording; agencies "personally vetted" contradiction; haggling anecdote at Raikot; planner style tiers; month-page "2026" titles; related-link anchor refresh; status-page check dates; "169 honest guides" (sitemap has 189 URLs, but which pages count as "guides" is an editorial definition).
- **Not resolvable from reliable web sources in this pass:**
  - Khunjerab NP overnight camping rules: no published rule found; the current cautious wording stays. KNP fee collection point: Wikipedia names a park station at Dih, but not where the fee is charged.
  - Karambar/Darkot permit practice and the Karambar distance to the Wakhan.
  - Naltar winter road (how-to-reach "closure likely" vs main "public jeeps if snow isn't heavy").
  - Fairy Meadows mobile signal ("patchy, Jazz best" vs "gone from Raikot").
  - Astore Thursday bazaar; Minimarg-Deosai trek; Handrap Lake requirements; Phander Lake "5km"; NATCO Gilgit-Chitral bus.
  - Chilas-Raikot km (sources 28-50); Lulusar km; Gupis/Teru/Danyore/Bagrot derived km; Sarfaranga distance; Shigar Rock Bridge; Manthokha facilities/fee; Deosai NP fee.
  - Kharpocho "K2 visible": removed earlier on geographic grounds, not re-sourced.
  - Upper Kachura vs GB Tourism "35-40 km" (FACTS already decides this).
  - Serena winter opening; Yasin Fort/Alexander legends; Sost "weekly cross-border market"; "1.5 million tourists" in Naran; Chillinji Pass routing (consistent with geography but not sourced here).
  - Tumuro = wild thyme / diram phitti = sprouted wheat: wording kept, not re-sourced.
  - Month-page temperature source label; Hopper/Eagle's Nest hike time vs jeep road; winter guesthouse openness; Lahore-Skardu frequency; mid-Oct Babusar/Deosai live status; flood caveats (Haramosh, Naltar, Hushe, Astore, Hisper) and whether the roads are restored; permit office and fee; Mulberry "Hunza water" wording; Ganish carvings age.
- **Operator data inconsistencies on trek pages** (treks 2-3, except PakVoyager): Trango porter 18 vs 20 kg and $2,055 vs $1,790; Skardu Trekkers Masherbrum tiers and Rakaposhi "domestic flights included"; Chogori Laila $1,500 vs $1,300; TripMaker NP; Chogori Snow Lake porter; Hunza Guides Rupal routing; Chogho Lingsa CKNP fee; licence numbers and "years operating". Each needs a fresh pull from the operator sites.

## Source sync done (generated pages)
- research/build_honeymoon.py: Eagle's Nest rating/reviews/take, Luxus area, autumn window (3 strings).
- research/hotels/hunza.json: Eagle's Nest type/reviews/pros; Luxus area.
- research/treks/naltar-lakes.json: price_note, good, pros. research/treks/rush-lake.json: PakVoyager verdict. research/treks/_pagemeta.json: Rakaposhi desc + hero_meta.
- research/build_trek_articles.py: price_str price_note, Naltar FAQ, Rakaposhi about. research/build_treks.py: price_str price_note.
- Not reproducible by generators, because the blocks are hand-added: the gilgit/hotels 2nd FAQPage and the trekking/rakaposhi-base-camp 2nd FAQPage. Both were edited in HTML only.

## Counts
Resolved: 37 flag items (31 with page edits, 6 verified with no change needed). Left for Faisal: ~85 individual items across 6 groups (named businesses, fares, editorial, unsourced facts, operator data).
