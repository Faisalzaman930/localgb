# Fact-check log: regions group (16 Oct 2026 pass)

I checked all 31 pages and changed all 31. Every changed page got its byline set to "Updated October 2026" and its JSON-LD `dateModified` set to `2026-10-16`. I did not touch the footer "Last updated" lines. I applied the edits as exact-match string replacements, each one asserted to match a unique string, and checked that the JSON-LD still parses afterwards. No em dashes were added.

Sources: "FACTS" means /home/claude/localgb/FACTS.md. The research files are research/fact-check-2026-10/*.md (transport, prices, places, safety). Web sources are given as URLs.

## Changed pages

### naltar/index.html
- "Pakistan's only (functioning) ski resort" (meta, og, twitter, JSON-LD, hero, body, card) → "GB's main ski resort" / "GB's only ski resort with mechanical lifts". Added a note that Malam Jabba (KP) is the other lift-served area (FACTS Places; facts-places table).
- Jeep from Nomal to Naltar was "PKR 1,500-2,500", which contradicted how-to-reach's "3,000-5,000" → now "PKR 3,000-5,000 one way". Private Gilgit-Naltar jeep "6,000-10,000" → "~PKR 8,000-15,000 for the day (2026)" (FACTS Prices, Hunza jeep/day 8,000-15,000), plus "confirm locally".
- Added a flood caveat: Aug 2026 floods in upper Naltar blocked the road and stranded tourists. Keep a buffer day in Jul-Aug (facts-places §2 Naltar, dawn.com/news/2020690).
- The PAF ski fee "PKR 500-1,500" and the homestay and Nomal guesthouse prices were unverifiable, so they became "confirm locally".

### naltar/how-to-reach/index.html
- Shared Suzuki "Rs.100" → "Rs.150-250" to match the main page, plus confirm. Nomal jeep "3,000-5,000" kept with a fuel caveat. Private jeep "7,000-10,000 return" → "~Rs.8,000-15,000 for the day".
- ISB-Gilgit flight "~50-60min, Rs.5,000-12,000" → "~1h, about Rs.19,000-28,000 one way" (FACTS Flights/Prices).
- "May-September: Road fully passable" now adds that Jul-Aug flash floods can block the road for days, as in Aug 2026 (FACTS Hazards).

### naltar/weather/index.html
- April "Road reliably open" → "usually open… confirm locally". This removes the contradiction with the main page, which says the road "may be impassable" in Mar-Apr.
- July: added a flood-season buffer-day note (Aug 2026 road block).

### gilgit/index.html
- Gilgit-Hunza confluence "2km north… walk" → "about 5km east… rickshaw or taxi". It contradicted places-to-visit, which says ~5km.
- Gilgit Manuscripts "now in Islamabad" → "mostly in New Delhi (National Archives of India), with others in Srinagar and London; found near Gilgit in 1931" (https://en.wikipedia.org/wiki/Gilgit_manuscripts).
- ISB-Gilgit flight "Rs. 8,000-18,000" → "about Rs. 19,000-28,000" (FACTS).
- NATCO "Rs. 1,200-1,500", private coaches "2,000-3,500" → "roughly Rs. 3,800-6,000 (NATCO, Faisal Movers)". Added the FCDO KKH Mansehra-Chilas advice and the Jul-Aug buffer-days caveat (FACTS Buses, Advisories, Monsoon).
- Gilgit-Skardu "~170-210km… Or fly Skardu-Gilgit (~30 min)" → "~200-210km, 4-5h + 1-2h for S-1 flood repairs. There are no Gilgit-Skardu flights." The same flight claim was removed from the "Where to go next" Skardu card (FACTS Roads, Flights).
- Hunza private car "Rs. 2,500-4,000" → "roughly Rs. 5,000-8,000, more for a jeep; confirm" (facts-prices: Gilgit car with driver 5,000-8,000).
- Budget "Rs. 1,200-2,500" → "from ~Rs. 3,500". Mid-range "3,500-7,000" → "4,000-8,000 simpler / 15,000-20,000 better ones". "Serena Gilgit is the established mid-range choice (Rs. 6,000-9,000)" → "Gilgit Serena is upper tier, from about Rs. 23,000" (FACTS Hotels; facts-prices table).
- Dhaba meals "Rs. 200-400" → "a local dish runs about Rs. 400-700" (FACTS Food).
- Fairy Meadows walk "3-4h" → "2-3h" (FACTS Roads).

### gilgit/hotels/index.html (generated)
- Meta, og, twitter and JSON-LD said "budget guesthouses Rs.1,500-3,000", but the page's own listings show Rs.3,500+ → "from about Rs.3,500".
- Serena "approx PKR 30,000-50,000" → "approx PKR 23,000-40,000" (FACTS: from ~PKR 23,000 / $84+).
- FAQ JSON-LD "1,500-3,000 / 4,000-7,000 / Rs.12,000-20,000 for the single upscale option" → "3,500-8,000 / 4,000-20,000 / ~18,000-30,000+ upper tier (Ramada, Serena)" (facts-prices table row).

### gilgit/restaurants/index.html (generated)
- The meta, og, twitter and JSON-LD description named "Sardar Restaurant", which is not on the page → now "Dera Shinwari, Dawat".

### gilgit/bagrot-valley/index.html
- Diran "7,257m" → "7,266m", in 3 places (https://en.wikipedia.org/wiki/Diran).
- Jeep "Rs.3,500-5,500 return" → "~Rs.8,000-15,000 for the day (2026)", in the body and in the FAQ JSON-LD. Guesthouse "Rs.1,000-2,000" and meals "Rs.300-500" → "budget rates, confirm locally" / "agree the price in advance", in the body and in the FAQ JSON-LD.

### gilgit/kargah-buddha/index.html
- Gilgit Manuscripts "London, Islamabad, and Srinagar" → "mostly New Delhi (National Archives of India), with others in Srinagar and London" (Wikipedia).
- Rickshaw total: added "(confirm locally)".

### gilgit/haramosh-valley/index.html
- 1957: "two climbers trapped above 7,000m and rescue partners fell into a glacier" → "Oxford University expedition… series of falls high on the mountain killed two of its four climbers" (https://en.wikipedia.org/wiki/Haramosh_Peak).
- "Turn off the KKH at Sassi (40km east of Gilgit)" → "Turn off the Jaglot-Skardu road (S-1) at Sassi". Sassi is on the S-1, not the KKH (facts-transport §6: bridge near Sassi Haramosh). Jeep "Rs.5,000-8,000" → "~Rs.8,000-15,000 a day". Added that the July 2026 floods damaged the S-1 near Sassi and the Haramosh road (facts-transport §6).

### gilgit/places-to-visit/index.html and gilgit/things-to-do/index.html
- Naltar jeep "Rs.4,000-6,000" and Bagrot "Rs.3,500-5,000" → "~Rs.8,000-15,000 (2026)", consistent with the Naltar and Bagrot pages. Things-to-do day jeep "Rs.4,000-8,000/day" → "~Rs.8,000-15,000/day".
- Nomal "34km" → "~25-30km". This matches naltar/how-to-reach, and Naltar itself is 34-40 km.
- Jaglot "25km" → "~40km" (FACTS: Gilgit-Jaglot ~35-45 km). On things-to-do, "confluence of Gilgit and Hunza rivers" at Jaglot → "Gilgit and Indus rivers". That was a factual error and also contradicted places-to-visit.
- Haramosh "40km east" → "east via the Jaglot-Skardu road (turn off at Sassi)". The peak itself is ~65 km east (Wikipedia).
- Danyore "20km south" → "~10km from the centre, across the Hunza River". This is local geography; please check (see Flags).
- Things-to-do: paragliding "Rs.5,000-8,000" and rafting "Rs.3,000-5,000" → "confirm current prices".

### gilgit/weather/index.html
- "cancellation rates of 40-60%" (unsourced) → "cancellations are frequent… often not retried the same day" (FACTS Flights).
- August: added that Jul-Aug floods closed the KKH and the Gilgit-Skardu road in 2025 and 2026, so keep buffer days (FACTS Monsoon).
- Naltar ski "February-March only" → "December-February". It contradicted all the Naltar pages.

### ghizer/index.html
- Shandur festival "Each July" / "usually first week of July" (x2) / stat "July" / seasons row "July (festival)… (first week)" → festival now in June (20-23 Jun 2025, 11-13 Jun 2026, GB beat Chitral 6-5; dates announced in spring). The July row became a flood-season note. The "Snow clears by mid-June" row → "by early June" (FACTS Places/Events; facts-transport Shandur).
- Distances: Shandur "240km" → "~210km" (https://en.wikipedia.org/wiki/Shandur_Pass: 212 km). Phander "190km" → "~170km" (https://en.wikipedia.org/wiki/Gupis_Tehsil). Gahkuch "120km" → "~72km" (GB Tourism, https://tourismdept.gbit.gov.pk/tour/id/5). Gupis "160" → "~110" and Teru "220" → "~195" are derived (see Flags).
- Private jeep to Phander "PKR 8,000-14,000" (a research-flagged row) → "roughly PKR 10,000-22,000 depending on vehicle (2026)" (facts-prices suggested replacement). Shared fares marked "pre-2026, confirm".
- Guide "PKR 1,500-2,500/day" → "agree a written rate". Rowboat, fishing permit and Phander-Shandur jeep prices → "confirm".
- Permits: "Ishkoman may require NOC" → "register at checkposts. Upper Ishkoman/Karambar near the Afghan border is restricted" (FACTS Permits).
- Road conditions: added a note on the Jul-Aug 2026 floods (Gilgit-Shandur and Ishkoman roads cut; Ghizer among the worst hit) (facts-places §5; facts-transport §3).
- NATCO Gilgit-Chitral bus softened to "has run… confirm it is running".

### ghizer/weather/index.html
- "Shandur short summer (July-September)" → "roughly June-September". June "Shandur sometimes open by late June" → "usually open by early-to-mid June; festival now in June". July "Shandur Polo Festival (mid-July)" was removed and replaced with a flood note. "Best months: June, July (for the Polo Festival)" → "June (for the Polo Festival), July…".
- August: added a flood-season note (Ghizer and Ishkoman roads cut in Aug 2026).

### ghizer/things-to-do/index.html
- "Shandur-Phander Polo Festival… mid-July" and "When: Mid-July" → "Shandur Polo Festival… now usually June (20-23 Jun 2025, 11-13 Jun 2026)".
- Handrap Lake: the page said "Above Gupis, 1-day, no guide needed, start from Gupis bazaar", which contradicted the main page ("above Handrap village, 2-day, guide required") → now "Above Handrap village… 1-2 day… guide recommended".
- Chillinji Pass "connecting Ghizer to Ishkoman" → "connecting upper Ishkoman (Karambar) with Chapursan in upper Hunza, close to the Afghan border, check permit rules". This is from local geography; see Flags. Guide "Rs.2,500-3,000/day" → "written rate".
- Tent city and shared van prices → "confirm".

### ghizer/hotels/index.html
- "Book ahead in July" / "During festival (mid-July)" / "festival dates (mid-July)" → June. Subtitle "with real prices" → "indicative prices (2026 rates are rising, so confirm)". The individual guesthouse prices are pre-2026 and were not changed (see Flags).

### ghizer/how-to-reach/index.html
- Hero and body distances: Gahkuch 120→~72km, Phander 190→~170km and 3.5h→5h, Shandur 240→~210km and 5h→7-8h. These are also updated in the summary table (sources as for ghizer/index).
- Hero "Road open year-round to Phander" → "Lower valley open year-round". It contradicted the weather page, which says Phander and above close in winter.
- Shandur "open July-October; closes November-June", "only open July to October", "Special buses in July", "NATCO… July-October" → roughly June-October, snow-dependent. The pass was open for the 11-13 Jun 2026 festival.
- "N-15 highway" for the Gilgit-Chitral road → "Gilgit-Shandur-Chitral road". The N-15 is the Mansehra-Naran-Chilas road.
- Flights "Rs.5,000-12,000" (x2) → "Rs.19,000-28,000". "Cancel 2-3 times per week on average" (unsourced) → "cancel often".
- Phander shared fare "Rs.400-500" → "Rs.800-1,200" to match the main page. Private jeep "8,000-12,000" → "~Rs.10,000-22,000". Other fares → "confirm".

### yasin/index.html
- "carved by the upper tributaries of the Yarkhun River" → "carved by the Yasin River, which joins the Ghizer near Gupis". "Predominantly Shia… speaks Khowar" → "predominantly Ismaili… Burushaski and Khowar" (https://en.wikipedia.org/wiki/Yasin_Valley).
- "220km from Gilgit" (body and stat) → "~150km" (Wikipedia: ~148 km). Hero "6h" → "4-5h". Suzuki Gupis-Yasin "3h" → "about 1h". The old figure also contradicted the page's own 30km/45min. NATCO "4h" → "3-4h".
- Darkot: "In 1895 a British-Indian garrison crossed it" → "In 1870 explorer George Hayward was killed near the pass" (https://en.wikipedia.org/wiki/Darkot_Pass). Added that the pass is close to the Afghan border, so check access with police (Wikipedia notes it as restricted; FACTS border buffer).
- Thui Pass "4,870m, connects to Punial area of Ghizer, highest of the passes" → "~4,500m (4,499m), connects to the Yarkhun valley in Chitral" (Yasin Valley Wikipedia), in the card label, the body and the stat.
- "The approach to Darkot Pass begins near Immit" → "starts further up, at Darkot village" (see Flags on Immit).
- PTDC and fares: added "confirm" / "pre-2026".

### yasin/how-to-reach/index.html
- 220km → ~150km. Waypoints "Gahkuch (120km, on paved KKH) → Gupis (70km)" → "~72km on the Gilgit-Shandur road → ~45km". "The bus follows the KKH south to Gahkuch" → "leaves Gilgit westward on the Gilgit-Shandur road". Totals: shared 6-7h → 5-6h, private 5-6h → 4-5h. Gupis-Yasin "Journey 3h" → "about 1h".
- Flight "Rs.5,000-12,000" → "Rs.19,000-28,000". Guide "Rs.2,000-3,000/day" → "written rate" plus the Afghan-border access note. Added the FCDO Mansehra-Chilas advice to the "drive from Islamabad via KKH" note. "toward Immit" → "toward Darkot".

### yasin/things-to-do/index.html
- Darkot "1895 garrison" → "1870 Hayward". Trek start "near Immit" → "Darkot village". Guide and mule prices → "written rate / confirm". Added the Afghan-border access note.
- Thui Pass "4,870m… to the Punial area of Ghizer… higher and more technically demanding than Darkot" → "~4,500m… to the Yarkhun valley in Chitral… remote and demanding".

### yasin/weather/index.html
- "Rs.3,000-5,000 per person per day is sufficient" → "about Rs.5,000-8,000 (2026)" (FACTS daily budget).

### ishkoman/index.html
- Road: added that the Aug 2026 Mayoon flood created a lake at Hasis and cut the Ghizer-Ishkoman road (facts-places §5; dawn.com/news/2020690).
- Permits: added that the upper valley toward Karambar and the Wakhan border is restricted for foreigners (FACTS Permits).

### gojal/index.html
- Shimshal "NOC required" (card tag, NOC box, transport row, trek text) → the tourist NOC was abolished in 2019. Foreigners register at checkposts. The Shimshal passes need a trekking permit and a licensed operator (FACTS Permits).
- "Karakul Lake (Chinese side) is visible from the pass" was false and has been removed.
- Khunjerab "Pass open May-October" / "opens late April/May" / "closes October" → "officially year-round since Dec 2024; practical tourist window May-Oct; Sost-Khunjerab landslides Sep 2026" (FACTS Passes).
- Shimshal jeep "PKR 8,000-14,000" (a research-flagged row) → "~PKR 10,000-22,000 return depending on vehicle (2026)". Passu glacier guide "PKR 2,000-3,500/day" (research-flagged) → "written rate".
- Added a KKH caveat (Hassanabad/Shishper Aug 2025, Juchar Nallah near Gulmit Aug 2026, keep a buffer day) and a Misgar border-zone caution.

### fairy-meadows/index.html
- Jeep "Rs. 3,000-5,000 per jeep, negotiate" (a research-flagged row) → "about Rs. 8,000+ one way / Rs. 16,000-22,500 return per jeep, union-fixed, no haggling; foreigners may not be allowed to share" (FACTS Prices). Jeep track "~10-15km, 1.5-2.5h" → "~14km, ~1.75-2h".
- "You can also walk the whole jeep section" → "Walking the jeep road is not allowed". Added registering with police at Raikot (FACTS Roads).
- Tato-FM walk "3-4h" (hero, intro, step) → "2-3h". Horse "Rs. 1,500" → "~Rs. 2,500".
- "Entry fee Rs. 500 at the Tato gate" (unsupported: facts-safety found no separate toll) → "a small local fee may be charged, confirm".
- Huts "Rs. 1,500-3,500 incl. meals" → "Rs. 3,500-10,000, meals ~Rs. 1,400 each". Own tent "Rs. 1,000" → "about Rs. 500-1,000", matching the camping page.
- Gilgit-Chilas shared van "Rs. 400-600" → "about Rs. 500" (FACTS). Added the FCDO KKH caveat for the NATCO-from-Islamabad option and a Jul-Aug flood buffer note. Beyal guide rate → "written rate".

### fairy-meadows/how-to-reach/index.html
- Hero jeep "Rs.3,000-4,500" → "Rs.8,000+ one way". Jeep row "3,000-4,500 one-way; shared 800-1,200/person" (research-flagged) → union-fixed fare, no haggling, sharing may be refused, register with police, no walking the jeep road. Track "10-15km, 1.5-2.5h" → "~14km, ~1.75-2h". Hike "3-4h" (x3) → "2-3h". Mule "1,500-2,000" → "~2,500".
- Door-to-meadow time "7-9h" → "6-8h". ISB-bridge "12-14h" → "10-14h" (FACTS ~400-480 km, 10-14 h), plus the Babusar alternative and the FCDO caveat. Coaster "Rs.300-400" → "~Rs.500".

### fairy-meadows/best-time-to-visit/index.html
- August: added the Jul-Aug 2025/2026 flood closures and buffer days.

### fairy-meadows/camping/index.html
- Site fee "Rs.400-600" (hero and table) → "Rs.500-1,000, confirm" (matching the main page). Meals "breakfast 400-600, dinner 600-900" → "~Rs.1,400 a meal" (FACTS Food). "No cities within 150km" (Gilgit is ~100 km away) → "far from any city". Tent hire → "confirm".

### deosai/index.html
- Skardu access "3-4h via Sadpara Lake and the Burji La pass" → "about 45km, 2-2.5h to Bara Pani via Sadpara Lake and the Ali Malik Mar pass (park edge ~30-35km)". The pass card was renamed from "Burji La" to "Ali Malik Mar" (FACTS Roads; facts-transport §1, skarduexplorers 2026-09-19).
- Jeep "Rs. 8,000-15,000 per day" (research-flagged) → "Rs. 15,000-30,000 round-trip day tour; Rs. 30,000-40,000 overnight" (FACTS Prices).
- Bears "over 50 today" / "Population ~50" → "78 in a 2022 count" (https://en.wikipedia.org/wiki/Deosai_National_Park).
- "Marco Polo Sheep" wildlife card → "Himalayan Marmot". Marco Polo sheep live in Khunjerab, not Deosai, and Wikipedia's Deosai species list includes the marmot. The urial card's "Smaller than Marco Polo sheep" → "Smaller than the ibex".
- Astore access "via Chilum Chowk, 3-4h… eastern plateau" → "Astore-Chilam ~55km (2h), +15km (1h) to Sheosar… western (Sheosar) side" (FACTS Roads).
- Entry fee "Rs. 500 / PKR 3,000 / USD 20-40" → "Rs. 200-500 for Pakistanis; older reports ~PKR 3,000-4,000 for foreigners" (facts-safety: USD 20-40 unsupported; LOW confidence).
- Logistics note: added the late-July 2026 floods on the Deosai and Astore roads, and buffer days.

### astore/index.html
- Minimarg was described as being on the Astore-Deosai road (intro, Deosai card, Minimarg card, overnight gem, 3-day loop, road note). It is ~36km beyond Chilam over the Burzil Pass, near the LoC (https://en.wikipedia.org/wiki/Minimarg). The Deosai approach is now "via Chilam". The NOC note and permits row were rewritten: Minimarg and the Burzil road are restricted for foreigners (10-mile LoC belt), and foreigners register at checkposts (FACTS Permits).
- Rupal: "Reinhold Messner made the first solo ascent of this face in 1978" → "Reinhold and Günther Messner made the first ascent of this face in 1970". Base camp "3,800m" → "~3,550m" (FACTS Treks).
- Skardu via Deosai "4-5h (June-October)" → "~150km, 6-7h (roughly mid-June to late Sep)". "Deosai open until mid-October" → "late September/early October" (FACTS).
- Road note: added the Khachak closure in late Jul 2026 (stranded tourists) and a buffer-day note (facts-transport §3).
- Guide rates "PKR 3,000-5,000/day" and "2,000-3,500/day" (research-flagged) → "written rate". Gilgit jeep prices → "confirm".

### naran-kaghan/index.html
- ISB-Naran "4-5h" (getting-there row, day-1 itinerary) → "~270-283km, 6-9h". Return-day arrival times softened. Lahore "7-8h" → "10-14h" (FACTS Roads).
- Babusar "open ~mid/late June to Sept/early Oct", "May: Babusar closed", "closes usually mid-October", "open June-October" → "opens ~late May (25-27 May 2026, one-way first); open roughly late May/June to Oct/Nov; daylight only, no travel after 6pm (gates ~7am-6pm)" (FACTS Passes). Naran-Babusar "2-2.5h / 65-70km" and "3h" → "~65km, 1.75-2h".
- Official July 2026 jeep fares (ProPakistani 2026-07-08): Saif-ul-Malook "PKR 2,000-3,500" (x3) → "PKR 5,500 return". Babusar "4,000-7,000" → "PKR 12,000 return". Shogran access "from Balakot 800-1,500" → "Kiwai jeep PKR 4,500 return". Chilas jeep "8,000-14,000" (research-flagged) → "agree a written price; official Naran-Babusar fare 12,000". Car hire "8,000-14,000" → "~10,000-20,000/day, confirm".
- Fairy Meadows leg: "jeep to Tatta Pani (1h)" → "register with police, then union jeep to Tato (~2h)". "Trek (3-4h) or alternative jeep road" → "2-3h; walking the jeep road is not allowed". Raikot-Gilgit "1.5h" → "~2h".
- Guide rates "PKR 2,000-3,500/day" and "2,500-4,000/day" (research-flagged) → "written rate". Trout "PKR 600-900 a fish" → "priced by weight, confirm". Coach fares → "confirm".
- Added the July monsoon caveat (2025/2026 Babusar and Kaghan closures, Mahandri Bridge weak point) and the FCDO note on the "return to Islamabad and take the KKH" fallback.

### karakoram-highway/index.html
- Raikot: "15km… ~3-4h hike" → "~14km, union-fixed fares, walking not allowed, ~2-3h hike".
- "Gilgit is also where the KKH splits from the Karakoram range road east" → "The Skardu road (S-1) leaves the KKH at Jaglot, south of Gilgit".
- NATCO "Rs. 1,200-1,500" (research-flagged) → "roughly Rs. 3,800-6,000 (2026)".
- Security: "Check FCDO advisories" → the explicit FCDO all-travel advice for Mansehra-Chilas, with Babusar or flying as alternatives, plus the Apr/Jun 2026 Chilas protest blockages (FACTS Advisories, Road works).
- Best months: "Khunjerab closed November-April" → "officially year-round since Dec 2024; tourist trips practical May-Oct". Added the Jul-Aug 2025/2026 flood closures. China crossing "Open May-October, daylight" → "Mon-Fri only (PK side ~9am-5pm), closed on PK/China holidays; tourist window May-Oct; no self-drive in China" (FACTS Passes).
- Foreigners: added "show your passport at checkposts, carry copies" (FACTS Permits).

## Checked, no change needed
None. All 31 pages had at least one correction, and the byline and dateModified were updated on each.

## Flag for Faisal
1. **Named businesses (status and prices not verifiable online):** Gilgit hotels (Ramada, Serena, Madina 2, Grand Continental, PTDC Motel, Riveria, MarcoPolo, Das-e-Basi). FACTS says Gilgit mid-range is ~15,000-20,000, but the page lists its mid-range hotels at 4,000-8,000. Also all 12 Gilgit restaurants, "Park Hotel's dining room" and "Madina Restaurant" (gilgit/index), "Sardar Restaurant" and "Ittehad Bakery" (gilgit/things-to-do), Phander Lake View Hotel, Phander Lake Resort, PTDC Phander/Gahkuch, Hotel Green Valley (Ghizer), PTDC Motel Yasin, "PTDC rest house" Gupis, Gulmit Tourist Inn, Passu Inn, PTDC Rama, Astore Inn, Pine Park Shogran, Dream Land, Lalazar Hotel, PTDC Naran/Shogran log huts.
2. **Local fares I softened ("confirm locally") rather than corrected, because there is no 2026 source:** Gilgit-Nomal/Naltar shared fares, Gilgit-Hunza shared jeep, Gilgit-Skardu shared fare, Ghizer/Gupis/Yasin shared fares and NATCO Rs.300-400, Karimabad-Gulmit/Passu/Sost/Misgar/Khunjerab jeep fares, Astore/Rama/Rupal jeep fares, Lulusar/Lalazar jeeps, all valley guesthouse prices (Naltar, Bagrot, Ghizer, Yasin, Gojal, Astore, Naran), fishing permits, Phander rowboats, Shandur tent city, Gilgit paragliding and rafting, FM tent hire. The "~Rs.8,000-15,000/day" jeep figure I used for Gilgit day trips (Naltar, Bagrot, Haramosh) comes from FACTS' Hunza jeep/day range. Please confirm it holds for Gilgit.
3. **Distances I derived and that need a local check:** Ghizer route Gupis ~110km and Teru ~195km (derived from Phander ~170 and Shandur ~212); Yasin Gahkuch-Gupis ~45km; Gilgit-Chitral via Shandur still "~450km", which looks long given Shandur is ~212km; Danyore "~10km"; Bagrot "paved to Danyore junction (20km)", since the Bagrot turn-off may be at Oshikhandas; KKH page stop distances (Gilgit "600 km" from ISB vs FACTS' low-confidence 520-560).
4. **Yasin:** "Immit Village" card and the weather/things-to-do mentions. Imit is the main village of upper Ishkoman (Karambar trek start), not Yasin, so I re-pointed only the Darkot trek-start claims. The orchard card needs a real upper-Yasin village name. "Teru Meadows" are listed in Yasin (meta + card), but Teru is the upper-Ghizer village below Shandur, so please check. The Alexander the Great claims and the "Yasin Fort changed hands in the 1890s" claim were left as is.
5. **Ghizer:** Gupis Fort is called "British-era" on the main page and "Dogra-era" on things-to-do, so the two pages contradict each other. Handrap Lake is now "1-2 day, guide recommended", but please check what is actually needed. Chillinji Pass is now "Karambar (upper Ishkoman) to Chapursan", based on local geography. Please also confirm the NATCO Gilgit-Chitral seasonal bus still runs, and the Phander Lake "5km" length.
6. **Gilgit:** Gilgit Museum "Rs. 200 entry" and whether it exists or is open; "Aga Khan Cultural Centre, free" (unverified); "mahseer" in the Gilgit/Hunza rivers; the "Sport · October" tag on the polo card; Islam arriving "9th-11th centuries" (kargah-buddha page; most sources say 14th century onward); hotels FAQ JSON-LD says "stay near the airport? Generally no", which contradicts the visible text ("Near the airport - handy").
7. **Naltar:** "traditional Burusho settlement" (Naltar is largely Shina/Gujjar-speaking, so check this); the "Taxi to Nomal Rs.5,000-8,000" row; and "November-April road closure likely" (how-to-reach) vs the main page's "public jeeps operate if snow isn't heavy" in winter.
8. **Fairy Meadows:** mobile signal "patchy, Jazz best" (main) vs "completely gone from Raikot" (how-to-reach); the July "Rs.500 premium"; Chilas rock carvings "guide on-site".
9. **Astore:** Rama Meadows 3,500m / Rama Lake 3,600m (I believe Rama is ~3,300m); the Thursday bazaar; the "Minimarg to Deosai 3-day trek" (route and permission); Rupal circuit "5-7 days via Mazeno and Fairy Meadows" (usually longer).
10. **Naran:** whether Shogran has a cable car ("PKR 400 return, 8am-6pm"); the hotel price tiers; "1.5 million tourists".
11. **KKH page:** "Swat Kohistan district" around Besham (Besham is in Shangla); Komila carvings; Sost "weekly cross-border market" (gojal).

Total flags: 11 groups (about 45 individual items).

## Needs source sync (generated pages edited)
- gilgit/hotels/index.html: hotels JSON (meta description, Serena price, FAQ JSON-LD)
- gilgit/restaurants/index.html: restaurants JSON (meta description)
