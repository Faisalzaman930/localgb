#!/usr/bin/env python3
"""
Safety + "is it open" pages, built with the same shell/schema code as the
honeymoon guides (build_honeymoon_pages.py):

  /travel/is-gilgit-baltistan-safe            (new)
  /updates/is-gilgit-baltistan-open-for-tourists-2026   (rebuilt, same URL)

Facts: FACTS.md "Permits, visas, advisories (Oct 2026)" and "Passes / seasons".
Run:  python3 research/build_safety_pages.py  (then the sitewide generators)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_honeymoon_pages as b  # noqa: E402

WA = b.wa
cta = b.cta

SEASONS = """<div style="overflow-x:auto"><table class="cmp-table"><thead><tr><th>Place</th><th>Open to visitors</th><th>Good to know</th></tr></thead><tbody>
<tr><td><strong>Hunza</strong> (Karimabad, Upper Hunza)</td><td>Year-round</td><td>Best late March-October; some hotels close in winter</td></tr>
<tr><td><strong>Khunjerab Pass</strong></td><td>Practical tourist window May-October</td><td>Officially open all year for trade; Sost border works Monday-Friday</td></tr>
<tr><td><strong>Skardu</strong>, Shigar, Khaplu</td><td>Year-round</td><td>Flights from Islamabad are weather-dependent</td></tr>
<tr><td><strong>Deosai</strong></td><td>About mid-June to late September/early October</td><td>Snowbound November-May</td></tr>
<tr><td><strong>Gilgit</strong></td><td>Year-round</td><td>The region's hub; flights from Islamabad (PIA) often cancelled</td></tr>
<tr><td><strong>Fairy Meadows</strong></td><td>About April/May to September/October</td><td>The jeep track closes with snow</td></tr>
<tr><td><strong>Babusar Pass</strong> (Naran to Chilas)</td><td>About late May/June to October/November</td><td>Daylight only; opened around 25-27 May in 2026</td></tr>
<tr><td><strong>Naran &amp; Kaghan</strong></td><td>Main season May/June-October</td><td>The lower valley (Balakot to Shogran) stays open year-round</td></tr>
</tbody></table></div>"""

PAGES = [
  {
    "path": "travel/is-gilgit-baltistan-safe", "crumbs": [("Travel", "/travel"), ("Is it safe?", None)],
    "title": "Is Gilgit-Baltistan Safe? Hunza, Skardu & Gilgit in 2026",
    "desc": "Is it safe to travel to Hunza, Skardu and Gilgit in 2026? A local's honest answer: travel advisories, the real risks (roads, weather, altitude), and how to stay safe.",
    "eyebrow": "Safety &middot; Gilgit-Baltistan &middot; October 2026",
    "h1": "Is Gilgit-Baltistan Safe to Visit? A Local's Honest Answer for 2026",
    "img": "hunza-photo.webp", "img_alt": "Hunza Valley seen from Eagle's Nest",
    "caption": "Hunza - consistently rated one of the safest places in Pakistan to visit.",
    "body": f"""
<p><strong>Short answer: yes.</strong> Gilgit-Baltistan is consistently rated among the safest parts of Pakistan for travellers, and Hunza in particular is popular with families, women and solo travellers. I'm from here, so I'll be straight with you: the real risks are the roads, the weather and the altitude - and, now and then, local unrest that shuts things down for a few days.</p>
<h2>What the travel advisories say (October 2026)</h2>
<ul>
<li><strong>UK (FCDO):</strong> Gilgit-Baltistan is not under any "advise against" warning. After unrest in early March 2026, the FCDO advised against all but essential travel to GB from 12 March; it lifted that on 15 April 2026.</li>
<li><strong>One road to avoid on UK advice:</strong> the FCDO still advises against all travel on the KKH between Mansehra and Chilas. Following that advice, you'd fly to Gilgit or Skardu, or use the Naran-Babusar road in summer.</li>
<li><strong>US:</strong> Pakistan as a whole is Level 3, "Reconsider Travel"; GB is not one of its Level 4 areas.</li>
</ul>
<p>Travelling against your government's advice can affect your insurance, so check your policy.</p>
<h2>Is it safe to travel to Hunza?</h2>
<p>Yes. Hunza is calm, friendly and used to visitors, and it's where most first-time visitors - including families and solo travellers - feel most at ease. Take the usual care on the Karakoram Highway (landslides in the monsoon) and keep the visit to Khunjerab Pass (4,693m) short.</p>
<h2>Is Skardu safe?</h2>
<p>Yes. Skardu and the Shigar and Khaplu valleys are safe and welcoming. In March 2026 there was unrest with curfews in Skardu and Gilgit and a mobile shutdown; it passed, but it's a reminder to keep an eye on the news before you go. The road from Gilgit (the Jaglot-Skardu S-1) still has flood-damaged sections, so allow extra time.</p>
<h2>Is Gilgit safe for tourists?</h2>
<p>Yes - Gilgit is the region's hub, and most visitors pass through it. It was also the centre of the March 2026 unrest, so if something is happening, it's usually here first; local news and your hotel will tell you quickly.</p>
<h2>The real risks - and how to handle them</h2>
<ul>
<li><strong>Roads:</strong> landslides and rockfall, especially from late July to mid-August, when floods closed major roads for days in both 2025 and 2026. Keep a spare day, and don't drive mountain roads after dark.</li>
<li><strong>Jeep tracks:</strong> the Raikot-Tato track to Fairy Meadows is exposed. Use the local jeeps, don't go in rain, and register with the police at Raikot.</li>
<li><strong>Altitude:</strong> Babusar (4,173m), Deosai (about 4,100m) and Khunjerab (4,693m) are high. Short visits are fine for most people; go slowly if you feel unwell.</li>
<li><strong>Unrest and shutdowns:</strong> mobile and internet can be suspended during unrest, Muharram and floods. Carry offline maps and enough cash.</li>
<li><strong>Checkposts:</strong> foreign visitors must show their passport and register at police checkposts - carry several copies of your passport and visa. Areas within about 10 miles of the Line of Control and the China and Afghan borders are restricted - see <a href="/travel/noc-permits-gb">NOC and permits</a>.</li>
</ul>
<h2>Safety checklist</h2>
<ul>
<li>Check the <a href="/status">road and pass status</a> and the news the week before you travel.</li>
<li>Carry ID (CNIC or passport, plus copies), cash and offline maps.</li>
<li>Keep one or two spare days, especially in summer and if you're flying.</li>
<li>Use local drivers who know the roads - a private car and driver costs about PKR 8,000-15,000 a day in Hunza.</li>
<li>Dress modestly and respect local customs; it's a conservative, very hospitable region.</li>
</ul>
<p>Is it open right now? See <a href="/updates/is-gilgit-baltistan-open-for-tourists-2026">is Gilgit-Baltistan open for tourists in 2026</a>.</p>
{cta("Worried about something specific?", "Ask me - I'll tell you honestly what the situation is on the ground right now. It's free.", "Hi Faisal, I'm planning a trip to Gilgit-Baltistan. Is it safe to travel right now?")}
""",
    "faq": [
      ("Is it safe to travel to Hunza Valley?", "Yes. Hunza is one of the safest and most welcoming places in Pakistan for visitors, including families and solo travellers. The main risks are road conditions in the monsoon and the altitude at Khunjerab Pass."),
      ("Is Skardu safe for tourists?", "Yes. Skardu, Shigar and Khaplu are safe and friendly. Check the news before you go - there was unrest with a curfew in March 2026 - and allow extra time on the flood-damaged Gilgit-Skardu road."),
      ("Is Gilgit-Baltistan safe for foreigners?", "Yes, it's among the safest parts of Pakistan. As of October 2026 the UK FCDO has no warning against travel to GB, but it still advises against all travel on the KKH between Mansehra and Chilas. Foreigners must register at police checkposts, so carry passport and visa copies."),
      ("Do I need a permit or NOC to visit Gilgit-Baltistan?", "No NOC is needed for tourism (it was abolished in 2019). Treks such as K2 Base Camp need a permit and a licensed operator, and areas close to the borders are restricted."),
    ],
  },
  {
    "path": "updates/is-gilgit-baltistan-open-for-tourists-2026", "crumbs": [("Updates", "/updates"), ("Is GB open?", None)],
    "title": "Is Gilgit-Baltistan Open for Tourists in 2026?",
    "desc": "Yes - Gilgit-Baltistan is open to tourists in 2026. When Hunza, Skardu, Deosai, Fairy Meadows, Babusar and Naran are open, plus visas, checkposts and what can close roads.",
    "eyebrow": "Travel advisory &middot; Update &middot; October 2026",
    "h1": "Is Gilgit-Baltistan Open for Tourists in 2026?",
    "img": "karakoram-highway-photo.webp", "img_alt": "The Karakoram Highway below Rakaposhi",
    "caption": "The Karakoram Highway - open, but check conditions before you travel.",
    "body": f"""
<p><strong>Short answer: yes.</strong> As of October 2026 Gilgit-Baltistan is open to tourists, including foreign travellers. After unrest in early March 2026 (curfews in Gilgit and Skardu and a mobile shutdown) the UK FCDO advised against all but essential travel to GB from 12 March; it lifted that on 15 April 2026, and GB is not under any FCDO "advise against" warning now. The FCDO still advises against all travel on the KKH between Mansehra and Chilas. The real limits are seasonal: high passes and plateaus open and close with the snow.</p>
<h2>What's open, and when</h2>
{SEASONS}
<h2>Is Hunza open?</h2>
<p>Yes, all year. Karimabad and the main Hunza valley are reachable year-round. Khunjerab Pass is officially open all year for trade, but the practical window for tourists is May to October, and the Sost border works Monday to Friday. See my <a href="/hunza">Hunza guide</a>.</p>
<h2>Is Skardu open for tourism?</h2>
<p>Yes, all year. Skardu, Shigar and Khaplu are open year-round, with flights from Islamabad when the weather allows. Deosai is only open from about mid-June to late September or early October. See my <a href="/skardu">Skardu guide</a>.</p>
<h2>Is Naran Kaghan open for tourists?</h2>
<p>Naran's main season is roughly May-June to October; from October, guesthouses in Naran start to close, while the lower valley (Balakot, Kiwai and Shogran) stays open year-round. Babusar Pass opens around late May or June and closes in October or November, depending on snow, and is open in daylight only. See my <a href="/naran-kaghan">Naran and Kaghan guide</a>.</p>
<h2>Is Fairy Meadows open?</h2>
<p>Roughly April or May to September or October - snow closes the jeep track outside that. See my <a href="/fairy-meadows">Fairy Meadows guide</a>.</p>
<h2>Visas, permits and checkposts</h2>
<ul>
<li><strong>Visa:</strong> the free "visa prior to arrival" was suspended from 1 January 2026. Apply for a paid e-visa at visa.nadra.gov.pk 4-6 weeks ahead.</li>
<li><strong>No NOC</strong> is needed for tourism (abolished in 2019), but foreign nationals must register at police checkposts - carry several passport and visa copies.</li>
<li><strong>Permits</strong> are needed for some treks (such as K2 Base Camp and Snow Lake) and for border-adjacent zones.</li>
</ul>
<h2>What can close roads</h2>
<ul>
<li><strong>Monsoon:</strong> from late July to mid-August, floods closed the KKH, the Gilgit-Skardu road, Babusar and valley roads for days in both 2025 and 2026.</li>
<li><strong>Snow:</strong> Babusar, Deosai and Fairy Meadows close for winter; early snow can close Babusar without warning.</li>
<li><strong>Unrest:</strong> occasional, and usually short - but mobile data can be cut, so carry offline maps and cash.</li>
</ul>
<p>Check my <a href="/status">road and pass status</a> page before you set off, and read <a href="/travel/is-gilgit-baltistan-safe">is Gilgit-Baltistan safe?</a> for the full safety picture.</p>
{cta("Want to know what's open on your dates?", "Tell me when you're coming and I'll tell you what will be open and what to watch for. Free.", "Hi Faisal, is Gilgit-Baltistan open on my travel dates? I'm planning to visit in ...")}
""",
    "faq": [
      ("Is Gilgit-Baltistan open for tourists in 2026?", "Yes. As of October 2026 GB is open to domestic and foreign tourists, and the UK FCDO has no warning against travel there (a temporary warning after March unrest was lifted on 15 April 2026)."),
      ("Is Skardu open for tourism?", "Yes, all year. Deosai, near Skardu, is only open from about mid-June to late September or early October."),
      ("Is Naran Kaghan open for tourists?", "Naran's main season is roughly May-June to October, and the lower valley (Balakot to Shogran) is open year-round. Babusar Pass is open from about late May or June to October or November, in daylight only."),
      ("When is Babusar Pass open?", "Roughly late May or June to October or November, depending on snow. It opened around 25-27 May in 2026 and is open in daylight hours only."),
    ],
  },
]

if __name__ == "__main__":
    b.PAGES = PAGES
    b.main()
