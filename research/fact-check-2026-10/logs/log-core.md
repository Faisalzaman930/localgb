# Fact-check log - GROUP core (16-19 Oct 2026)

## Changed pages

`index.html`
- Sample "Your 7-Day Hunza ≈ Rs 9k/day" → "≈ Rs 15k/day" (matches the planner's new Culture tier; FACTS.md Prices: mid-range 15,000-22,000/day)

`status/index.html` (seasonal-norm data in the JS; owner override values left untouched)
- KKH note: added protests at Chilas (2026) + "UK FCDO advises against all travel on the Mansehra-Chilas section"; monsoon "Jul-Aug" → "late Jul-Aug" (FACTS.md Road works; Advisories)
- Babusar: openMonths 7-10 / marginal 6,11 → open 6-10 / marginal 5,11; "Closed by snow roughly Nov-May" → "Open roughly late May/June to Oct/Nov (opened ~25-27 May 2026, one-way at first, then shut again for snow in early June)" (FACTS.md Passes)
- Khunjerab: "Officially Apr/May-Nov; the gate and border services close for winter" → "Officially open year-round since Dec 2024 (for trade); practical tourist window May-Oct; winter access can be suspended; Sost border Mon-Fri only, closed on PK/China holidays". openMonths 5-11 / marginal 4 → open 5-10 / marginal 11-4 (winter now shows "Conditional", not "Closed") (FACTS.md Passes)
- Deosai: "reliably open only roughly mid-June/July to September" → "roughly mid-June to late September/early October (best Jun-Aug)" (FACTS.md Passes)
- Fairy Meadows: "1-2h hike", open months 4-10 → "2-3h uphill hike", open 5-9 / marginal 4,10, "roughly Apr/May to Sep/Oct" (FACTS.md Distances, Passes)
- Skardu road: added 2025+2026 monsoon closures and Sep 2026 flood-damaged sections (+1-2h) (FACTS.md Distances)
- Flights: "~40-60% winter cancellation" (both) → "Frequently cancelled, worst in winter" / "Frequently cancelled, all year" (unsourced figure removed); "Daily PIA flights" to Skardu → "PIA, Airblue and AirSial A320s, ~13-21/week"; Gilgit → "PIA only, ATR, ~6/week, often not retried same day"; "Both airports are sight-flying only... military gets priority, seats confirmed 24h out" → "need clear weather (Gilgit is VFR only)"; KKH fallback "~14-16h" → "~12-16h" (FACTS.md Flights)
- dateModified 2026-07-09 → 2026-10-16

`weather/index.html`
- Byline Updated June → October 2026; dateModified → 2026-10-16
- "spans 3 climate zones" vs stat "4 climate zones" → both 4 (internal contradiction)
- Stat "Oct - Mar high passes closed" → "Nov - May" (FACTS.md Passes)
- "Deosai snowbound from October to June" → "snowbound about November to May, opens around mid-June"; June "Deosai accessible from late June" → "from mid-June"; Deosai row "July-September only. Access road muddy before July" → "Roughly mid-June to late Sep/early Oct (best June-August). Snowbound November-May" (FACTS.md Passes)
- April "Flights reliable" (x2) → "more reliable than winter (keep a road backup)" (FACTS.md Flights)
- July/August: added monsoon closure caveat (KKH, Skardu road, Babusar closed for days in 2025 and 2026; buffer days) (FACTS.md Passes - Monsoon)
- November "High routes closed" → "Most high routes closed (Babusar shuts around Nov)"
- Naltar "(Pakistan's only ski resort)" → "(GB's main ski area)" (FACTS.md Places)
- Babusar "June 15-October 15" → "roughly late May/June to October/November, daylight only" (FACTS.md Passes)
- Khunjerab "May-October (open to traffic)" → "May-October is the tourist window (officially open year-round since Dec 2024; border Mon-Fri only)" (FACTS.md Passes)

`planner/index.html` (visible HTML + embedded JS data; all inline scripts pass `node --check`, JSON-LD parses)
- dateModified → 2026-10-16
- Style tiers / `dailyCost`: budget 4,000 → 6,500; adventure 7,000 → 12,000; culture 9,000 → 15,000; photography 11,000 → 18,000; family 12,000 → 20,000; luxury 35,000 → 45,000+ (labels and JS kept in sync). Per-day strings: luxury "Rs 30,000-45,000" → "Rs 45,000+", budget "Rs 3,000-5,000" → "Rs 5,000-8,000"; extra-day costs "2,000-3,500 / 5,000-9,000 / 15,000-25,000" → "5,000-8,000 / 15,000-22,000 / 45,000+" (FACTS.md Prices - daily budget)
- Entry cards: "40-60% cancellation rate" → "Frequently cancelled"; Gilgit flight "45 min" → "about 1h, ATR"; Skardu "PIA from Islamabad or Lahore" → "PIA, Airblue or AirSial jets from Islamabad (PIA also Karachi/Lahore)"; KKH "15-18h" → "12-16h by car" + FCDO Mansehra-Chilas note; Babusar "Summer only · Jun-Oct" → "late May/Jun-Oct/Nov"; "Jeep only above Naran" → "Daylight only, can shut for snow" (FACTS.md Flights, Passes, Advisories; Wikipedia Babusar Pass: pass "easily accessed by cars")
- Flight rows: Gilgit "PIA PK-571, Rs 8,000-15,000" → "PIA ATR (~6/week), ~Rs 19,000-28,000 one way (2026)"; Skardu "Rs 8,000-16,000" → "~Rs 18,000-30,000"; backup "NATCO Rs 1,200, 18-20h" (x4) → "~Rs 3,800-6,000, 14-18h"; Skardu backup "NATCO to Gilgit then jeep 8h, Rs 800-1,200" → "NATCO ISB→Skardu ~Rs 5,500-6,200, 18-24h, or via Gilgit then 4-5h"; car hire "Rs 25,000-40,000" → "agree a written 2026 quote" (FACTS.md Prices, Buses)
- Critical notes: "40-60% cancellation rates" → "Frequently cancelled (Gilgit most of all)"; Khunjerab "Closed Nov-May / Entry fee Rs 500, May-Oct only" → year-round officially, tourist window May-Oct, park fee "confirm", border Mon-Fri; Network "Jazz has best GB coverage" → "SCOM widest; others in towns/KKH; data can be suspended during unrest/floods"; flight-API fallback "40-60% cancellation" → "frequently cancelled" (FACTS.md Flights, Passes, SIM)
- **Eagle's Nest/Serena merge**: "Serena Hunza (Eagle's Nest Hotel) - Rs 24,000-40,000" and the dining line → "Hunza Serena Hotel (Karimabad) or Eagle's Nest Hotel (Duikar) - two separate hotels, both upper tier, roughly $105-195 a night (confirm)" (FACTS.md Places; facts-prices.md)
- **Skardu → Gilgit "Fly 45min or drive 8h" + "Skardu-Gilgit flight is one of the most scenic"** → "Drive to Gilgit, ~200km, 4-5h; there are no Skardu-Gilgit flights; flood repairs add 1-2h"; same fix in "already in GB" next-steps for Gilgit and Skardu (FACTS.md Flights, Distances)
- Babusar day: "Descent to Chilas - 45 min" → "~110km, 3-4h" (timeline re-timed, Gilgit arrival 17:00); Naran→Babusar "2-3h" → "~65km, about 2h" + daylight-only; jeep-only tip → cars cross, Naran jeeps Rs 12,000 return (official, Jul 2026); "Islamabad to Naran 230km 5-6h" / "ISB → Naran 4-5h" / "Islamabad: 5h" → "~270-283km, 6-9h"; Naran next-steps "Babusar → Chilas → Gilgit 6-8h" → "8-10h"; Chilas "Naran via Babusar 3h" → "5-6h" (FACTS.md Distances, Prices)
- Babusar winter warning "(Nov-May)" → "(roughly Nov to late May)"
- Islamabad→Chilas "~500km, 9-11h" → "~450km, 10-13h"; Chilas tip: added FCDO Mansehra-Chilas advice + 2026 Chilas protests (FACTS.md Advisories, Road works)
- Raikot "40km east of Chilas" (x4) → "on the KKH between Chilas and Gilgit (~80km/2h from Gilgit)"; Chilas → Gilgit "1.5-2h" → "~3h"; Raikot→Gilgit "1.5h" → "~2h" (FACTS.md Distances; Chilas-Raikot km unconfirmed, sources say 28-50km)
- Fairy Meadows: jeep "15km, Rs 2,500-3,500 one way" → "~14km (~2h), union-fixed ~Rs 8,000+ per jeep one way (~16,000-22,500 return), no haggling"; hike "4km, 1.5-2h" (and "1.5h") → "~5km, 2-3h", walking jeep road not allowed, register with police at Raikot; BC gain "800m" → "~600m (BC ~3,900m)"; tented camps "Rs 1,500-2,500 with meals" / meals "Rs 500-800" → rooms from ~Rs 3,500, cottages up to ~10,000, meals ~Rs 1,400 (FACTS.md Distances, Prices; facts-prices.md)
- Baltit Fort "Rs 500 foreigners / Rs 200 locals + guide Rs 500" (x3) → "~Rs 2,000 foreigners, guided tour included (2026, confirm)"; Altit "900+ years", "Pakistan's oldest surviving fort", "Rs 300" (x3) → "about 1,000 years (11th century), GB's oldest fort, ~Rs 1,600 non-locals guide incl."; Ganish "900-year-old watchtowers, Free" → "centuries-old watchtowers, ~Rs 500 village tour"; Hussaini Bridge "Free" (x3) → "~Rs 200 toll" (FACTS.md Entry fees, Places)
- Shangrila/Kachura "30km from Skardu", "Entry free" → "~20km (30-40 min)", "~Rs 1,000 entry (confirm)"; Shangrila stay "Rs 18,000-30,000" → "~Rs 20,000-30,000+ in season (verify)" (FACTS.md Distances, Prices, Entry fees)
- Shigar "30km, 45 min" (x5) → "~45km, 1-2h"; "road continues 20km to Askole" / "Askole 2h further" → "Askole 6-8h rough jeep from Skardu"; "Amburiq Mosque (Chaqchan Mosque)" → "Amburiq Mosque" (Chaqchan is in Khaplu) (FACTS.md Distances)
- Deosai: "1.5h to plateau entry at Bara Pani, fee Rs 500" → "~45km, 2-2.5h by 4x4 via Sadpara to Bara Pani, park fee - confirm" (x4 incl. tags); Sheosar "at the centre of the plateau, 4,142m" → "on the far (Astore) side, roughly 4,140-4,250m"; bear "~40 individuals" → "only a few dozen"; camping permit "Rs 500" → "check the fee"; "Deosai (from Shigar road)... alternative route from the Shigar side" → "back through Skardu, up via Sadpara; open mid-Jun to late Sep/early Oct" (FACTS.md Distances, Passes, LOW-CONFIDENCE fees)
- Satpara "2,636m · 12km" vs "15km" elsewhere → "~2,600m · near Skardu" (FACTS.md Elevations; contradiction)
- Karimabad → Passu "30km, 40min" / "30km above Karimabad" → "~45km, 1-1.5h"; Attabad → Passu "30km, 45 min" → "about 20km, 30-45 min"; Hunza next "Passu & Khunjerab: 1.5h" → "Passu 1-1.5h; Khunjerab 3-5h each way"; Passu → Khunjerab "2h" → "2-3h"; Khunjerab "world's highest international border" → "highest paved border crossing", tourist window May-Oct, border Mon-Fri, park fee confirm (FACTS.md Distances, Passes)
- Shimshal "newly paved road" (x2) → "jeep road / rough jeep road" (road completed 2003)
- Rakaposhi BC "Full day, 15km from Karimabad, 3h hike" → "2-3 days from Minapin; a long day gets you partway" (FACTS.md Treks)
- Naran: Saiful Muluk jeep "Rs 2,500-3,000" / "Rs 2,500" → "official 2026 fare Rs 5,500 return"; Lulusar "20km north, jeep Rs 1,500-2,000" → "~48-50km north toward Babusar, agree the fare" (ProPakistani 8 Jul 2026 via facts-prices.md; https://visitsilkroad.org/destination/lulusar-lake/); Ansoo guide "Rs 2,500-4,000/day" → "agree a written rate in advance" (FACTS.md Guides)
- Hotels: Gilgit "Rs 1,500-2,500 / 4,000-6,000 / Serena 18,000-28,000" → "confirm 2026 rate / mid-range ~15,000-20,000 / Gilgit Serena from ~Rs 23,000 ($84+)"; Hunza budget "2,000-3,500" → "~2,000-6,500"; Passu budget "1,500-2,500" → "~2,000-6,500"; Skardu "1,800-3,000 / 5,000-9,000" → "from ~2,800 / ~8,000-18,000"; Chilas hotel prices → "confirm the 2026 rate" (FACTS.md Prices - Hotels)
- Local dish/meal prices below FACTS floor (Rs 150-400 for daal/roti, chapshoro, manti, dhaba meals, halwa puri) → "Rs 400-700" (~12 spots) (FACTS.md Prices - Food)
- Glacier Breeze (Passu) (x3) → "(check it's open)" (FACTS.md Places)
- Eagle's Nest jeep "Rs 800 return" (x2) vs "Rs 1,500-2,500" elsewhere → unified "~Rs 1,500-2,500 return, confirm" / "jeep" (contradiction)
- Naltar jeep "Rs 4,000-6,000" → "rough jeep track (2-3h), agree the fare first" (FACTS.md Distances)
- Departure "15-18h" drive → "12-16h"

`kkh-map/index.html`
- dateModified → 2026-10-16; hero "14-16hrs Islamabad-Gilgit" → "12-16hrs"; "30 mapped stops" → "28" (there are 28 in the data)
- Road-conditions intro: added FCDO Mansehra-Chilas advice + 2025/2026 monsoon closures, buffer days (FACTS.md Advisories, Passes)
- Sost → Khunjerab row and Khunjerab stop: "Open to tourists May-October only" → "Officially open year-round since Dec 2024; practical tourist window May-Oct; border Mon-Fri; winter access can be suspended" (FACTS.md Passes)
- Babusar turn-off "Open June-October only" → "roughly late May/June to Oct/Nov, daylight only"
- "Motorway (M-1) then dual carriageway"; Hasan Abdal "last motorway exit - then GT Road" → M-1 then Hazara Motorway (E-35) to Abbottabad/Mansehra (general knowledge, E-35 open since 2019-20)
- Pattan "2005 Kashmir earthquake epicentre was near here" → "1974 Pattan earthquake devastated this area" (2005 epicentre was near Muzaffarabad)
- Komila/Shatial "Look for the blue UNESCO sign" removed (GB has no inscribed WHS; FACTS.md Places)
- Indus-Gilgit confluence was placed at km 400, before Chilas, with coordinates west of Chilas → moved after Jaglot (km 515, 35.75N 74.60E), note references the Three Ranges junction
- Upper Hunza order: Gulmit (km 680, "Attabad Lake begins shortly after", coords north of Passu) listed before Attabad → Attabad km 655, Gulmit km 668 "just north of Attabad Lake", corrected coords; Passu 710 → 682, Shimshal turn-off 720 → 684, Sost 760 → 718 (Karimabad-Passu ~45-47km, FACTS.md)
- Raikot: "Jeep hire available at the bridge" → register with police; union jeeps fixed ~Rs 8,000+ one way (FACTS.md Prices)
- Jaglot: Skardu road "4-5hrs" + "allow 1-2h extra in late 2026 for flood-damaged sections" (FACTS.md Distances)
- Minapin: Rakaposhi BC "2 days" → "2-3 days" (FACTS.md Treks)
- Ganish "700-year-old watchtowers" → "centuries-old" (unsourced, aligned with planner)
- Shimshal "NOC required" → "treks over the Shimshal passes need a permit and licensed operator" (FACTS.md Permits)
- Sost "withdraw cash" → "carry enough cash (don't rely on ATMs)" + border Mon-Fri; Passu: Hussaini bridge "small toll" (FACTS.md Cash, Passes, Entry fees)

`atm-locator/index.html`
- dateModified → 2026-10-16
- "there are no ATMs past Karimabad in Hunza" (contradicted by the page's own Gulmit NBP pin) → ATMs in Hunza and beyond scarce/unreliable, foreign cards don't always work, none on trek routes; DIB and Faysal Bank best for foreign cards, ~PKR 600-1,200 fees; carry PKR from Islamabad (FACTS.md SIM, cash)
- Gulmit NBP pin coordinates (were north of Passu) → 36.39N 74.86E; Besham petrol pump labelled city "Hunza" → "KKH", area "Besham (KKH, KP)"

`blog/index.html`
- Byline Updated June → October 2026; dateModified → 2026-10-16
- "GB in 10 Days for Under Rs. 45,000" → "GB in 10 Days on a Budget (2026 Prices)" (FACTS.md budget 5,000-8,000/day makes 45k for 10 days impossible)
- "Karimabad on Rs. 3,000 a Day" → "Karimabad on a Backpacker Budget: A Realistic 2026 Breakdown" (same)
- NOC teaser "Which valleys need a NOC, how to get one... what happens if you enter without one" → "Why most of GB no longer needs a NOC (abolished 2019), which treks and border zones still need permits, and why you still register at police checkposts" (FACTS.md Permits)
- Passu "limestone spires rising 6,000m from the KKH" → "spires topping 6,000m above the KKH"

## Checked, no change needed
- destinations/index.html (already corrected; nothing further found)
- food/index.html
- about/index.html
- contact/index.html

## Flag for Faisal
- Planner/ATM named businesses not verifiable online: Park/Madina Hotel, Tourist Cottage, PTDC Motels (Gilgit, Chilas, Naran), Old Hunza Inn, Haider Inn, Hunza Heritage, Rakaposhi View, Passu Inn, Passu Tourist House, K2 Inn, New Al-Faisal, Mashabrum, Concordia Motel, Raikot Sarai, Café de Hunza, Hunza Kitchen, Café Diran, Chilas Inn/Al-Faisal; every ATM/pharmacy/petrol pin on /atm-locator (coordinates look approximate, many sit on town centres).
- Glacier Breeze (Passu): status unconfirmed in 2026; marked "check it's open".
- Gilgit luxury food line names "Shangrila Mountain Resort dining room" in Gilgit, but Shangrila is in Skardu (Kachura). Left as is: please confirm or remove.
- Small local prices left unverified: Kargah taxi Rs 300, Gilgit airport taxi Rs 200-400, Attabad boat Rs 500-800, Satpara entry Rs 200/boats Rs 400-600, Katpana camel rides Rs 300-500, Kunhar trout permit Rs 1,000, dried apricots/honey/toffee prices, Shigar Fort café Rs 1,500-2,500, Shangrila restaurant Rs 3,000-6,000, Hunza mid-range hotels Rs 6,000-10,000, Passu mid Rs 3,000-5,000, Naran stays.
- Softened rather than corrected: hotel tiers in Gilgit/Skardu/Hunza (FACTS ranges applied to named hotels), Chilas hotel prices ("confirm"), car hire ISB→Gilgit, Naltar jeep fare, Eagle's Nest jeep (Rs 1,500-2,500, not sourced), Islamabad→Chilas ~450km/10-13h (derived), Chilas→Gilgit ~3h and Raikot position (Chilas-Raikot km sources disagree, 28-50km), Lulusar ~48-50km (one source), Deosai bear count ("a few dozen"), 1974 Pattan earthquake and Hazara Motorway wording on /kkh-map.
- New planner style tiers (Rs 6,500 / 12,000 / 15,000 / 18,000 / 20,000 / 45,000+ per day) are my interpolation of the FACTS budget/mid/comfort bands. Please sanity-check.
- Homepage/About say "haggled/negotiated a jeep at Raikot Bridge" (personal voice). Fares are now union-fixed with no haggling. Left as is.
- Homepage "169 honest guides" count not verified.
- Status page cards still show local-check dates of 2026-06-27 (override values left as instructed).
- Several KKH-map coordinates beyond the ones fixed look approximate (e.g. Jaglot, Raikot). Worth a pass on a real map.

## Needs source sync
- None (no generated pages in this group).
