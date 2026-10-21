#!/usr/bin/env python3
"""
Honeymoon guides: /travel/honeymoon (hub), /hunza/honeymoon, /skardu/honeymoon,
/naran-kaghan/honeymoon. These replace /tours/hunza/honeymoon and
/tours/skardu/honeymoon (301-redirected in vercel.json) so each destination has
ONE honeymoon page.

Facts: FACTS.md (Oct 2026), research/hotels/*.json (verified Jul 2026), the
Naran-Kaghan guide, and packages re-checked live on 21 Oct 2026. Visible FAQ and
FAQPage JSON-LD come from the same list. Re-run, then the sitewide generators:

  python3 research/build_honeymoon_pages.py
  python3 related_links.py && python3 tour_links.py && python3 whatsapp_help.py && python3 photo_credits.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = "https://www.gilgitbaltistanguide.com"
TEMPLATE = ROOT / "tours/hunza/5-days/index.html"
TODAY = "2026-10-21"
e = html.escape
WA = "https://wa.me/923111915550?text="


def wa(msg):
    import urllib.parse
    return WA + urllib.parse.quote(msg)


def stays_table(rows):
    body = "".join(f"<tr><td><strong>{n}</strong><br><span style=\"font-size:.78rem;color:var(--cream-2)\">{a}</span></td><td>{w}</td><td>{r}</td></tr>" for n, a, w, r in rows)
    return ('<div style="overflow-x:auto"><table class="cmp-table"><thead><tr><th>Stay</th><th>Why couples pick it</th><th>Rating</th></tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def pkg_table(rows):
    body = "".join(f'<tr><td><a href="{u}" target="_blank" rel="nofollow noopener"><strong>{n}</strong></a></td><td>{d}</td><td>{p}</td><td>{note}</td></tr>' for n, u, d, p, note in rows)
    return ('<div style="overflow-x:auto"><table class="cmp-table"><thead><tr><th>Package</th><th>Days</th><th>Listed price</th><th>Good to know</th></tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def cta(heading, text, msg):
    return (f'<div class="article-cta"><h3>{heading}</h3><p>{text}</p>'
            f'<a href="{e(wa(msg))}" class="btn-primary" target="_blank" rel="noopener">Plan our honeymoon on WhatsApp &rarr;</a></div>')


PTP = "https://pakistantravelplaces.com/tour/"
COUPLE_TIPS = """<h2>Tips for couples travelling in Gilgit-Baltistan</h2>
<ul>
<li>Carry your CNICs or passports - hotels ask for ID at check-in, and so do checkposts on the way.</li>
<li>It's a conservative, friendly region: dress modestly and keep public affection low-key. In your hotel and on a private jeep, you'll have all the privacy you want.</li>
<li>Book the view room early for blossom (late March to mid-April) and autumn (late September to October) - the best rooms go first.</li>
<li>Carry enough cash; ATMs are limited outside the main towns.</li>
<li>Keep one spare day for weather, especially if you're flying.</li>
</ul>"""

PAGES = [
  # ------------------------------------------------------------------ HUB
  {
    "path": "travel/honeymoon", "crumbs": [("Travel", "/travel"), ("Honeymoon", None)],
    "title": "Honeymoon in Northern Pakistan 2026: Hunza, Skardu or Naran?",
    "desc": "Where to honeymoon in northern Pakistan: Hunza, Skardu or Naran compared - best months, romantic stays, packages and costs for 2026, from a local.",
    "eyebrow": "Honeymoon &middot; Gilgit-Baltistan &amp; Kaghan &middot; 2026",
    "h1": "Honeymoon in Northern Pakistan: Hunza, Skardu or Naran?",
    "img": "kachura-photo.webp", "img_alt": "Upper Kachura Lake near Skardu",
    "caption": "Upper Kachura Lake, Skardu - northern Pakistan does romantic scenery better than almost anywhere.",
    "body": f"""
<p>I'm from Gilgit-Baltistan, and couples ask me the same question every season: where should we go for our honeymoon? There are three real answers - Hunza, Skardu and Naran - and they suit very different couples. Here's how I'd choose.</p>
<h2>Hunza, Skardu or Naran: at a glance</h2>
<div style="overflow-x:auto"><table class="cmp-table"><thead><tr><th></th><th>Hunza</th><th>Skardu</th><th>Naran &amp; Kaghan</th></tr></thead><tbody>
<tr><td>Best for</td><td>Views, cosy heritage stays, blossom and autumn</td><td>Luxury and heritage hotels, lakes, wide open landscapes</td><td>A short, easy-to-reach mountain break</td></tr>
<tr><td>Best months</td><td>Late March-mid April; late September-October</td><td>April; September-October</td><td>June and September</td></tr>
<tr><td>From Islamabad</td><td>14-20 h by road, or about 1 h flight to Gilgit + 2-3.5 h drive</td><td>About 1 h flight, or 16-18 h by road</td><td>6-9 h by road</td></tr>
<tr><td>Ideal length</td><td>5-7 days</td><td>6-8 days</td><td>3-4 days</td></tr>
<tr><td>Published packages from</td><td>Rs 120,000 (5 days)</td><td>Rs 160,000 (8 days)</td><td>Rs 40,000 (2 days, Shogran)</td></tr>
<tr><td>Full guide</td><td><a href="/hunza/honeymoon">Honeymoon in Hunza</a></td><td><a href="/skardu/honeymoon">Honeymoon in Skardu</a></td><td><a href="/naran-kaghan/honeymoon">Honeymoon in Naran</a></td></tr>
</tbody></table></div>
<h2>Which one should you choose?</h2>
<ul>
<li><strong>Choose Hunza</strong> if you want the classic: a room facing Rakaposhi, old forts, apricot blossom or golden poplars, and cosy cafes in Karimabad. <a href="/hunza/honeymoon">Honeymoon in Hunza &rarr;</a></li>
<li><strong>Choose Skardu</strong> if you want the most special hotels - a restored fort in Shigar, a palace in Khaplu, lakeside resorts - and you can fly. <a href="/skardu/honeymoon">Honeymoon in Skardu &rarr;</a></li>
<li><strong>Choose Naran</strong> if you only have 3-4 days or don't want to fly: Lake Saif-ul-Malook, Shogran's forests and Babusar are a day's drive from Islamabad. <a href="/naran-kaghan/honeymoon">Honeymoon in Naran &rarr;</a></li>
</ul>
<h2>Can we combine two?</h2>
<p>Yes - in summer (roughly late May to October) the Babusar road links Naran to Chilas, so you can do Naran and Hunza in one trip of about 8-9 days without coming back to Islamabad. Skardu and Hunza combine well too (Gilgit to Skardu is about 4-5 hours by road), but you'll want 10 days or more.</p>
<h2>For adventurous couples: Fairy Meadows</h2>
<p>If your idea of romance is a wooden cottage facing Nanga Parbat, <a href="/fairy-meadows">Fairy Meadows</a> is unforgettable - but it's rustic. You'll take a rough jeep track and hike 2-3 hours to reach it, rooms are simple (about Rs 3,500-10,000 a night in 2026) and there's no luxury option. Add it to a Hunza trip rather than making it the whole honeymoon.</p>
<h2>When to go</h2>
<ul>
<li><strong>Spring blossom</strong> (late March to mid-April) - Hunza and Skardu at their most romantic.</li>
<li><strong>Summer</strong> (June to August) - everything is open, including Deosai and Babusar; late July to mid-August brings monsoon landslides, so keep spare days.</li>
<li><strong>Autumn</strong> (late September to October) - golden colours, clear skies, fewer people. My favourite for couples.</li>
<li><strong>Winter</strong> - quiet and snowy; many hotels close, and Naran's high roads shut.</li>
</ul>
<h2>What does a honeymoon in northern Pakistan cost?</h2>
<p>Published honeymoon packages run from about Rs 40,000 for a 2-day Shogran break to Rs 120,000-190,000 for 5-8 days in Hunza or Skardu with a private car. If you plan it yourselves, a private car and driver costs about PKR 8,000-15,000 a day in Hunza, and a mid-range to luxury hotel is the biggest part of the budget - see each destination guide for real hotel options.</p>
{COUPLE_TIPS}
{cta("Tell me about your honeymoon", "Send me your dates, budget and what you love - views, history, quiet, adventure - and I'll suggest where to go and how to plan it. It's free.", "Hi Faisal, we're planning our honeymoon in northern Pakistan. Can you help us choose between Hunza, Skardu and Naran?")}
""",
    "faq": [
      ("Which is better for a honeymoon: Hunza or Skardu?", "Hunza is better for classic mountain views, cosy heritage stays and blossom or autumn colours. Skardu is better for special hotels - a restored fort at Shigar, a palace at Khaplu, lakeside resorts - and wide open landscapes. If you can fly, either works; Hunza is the easier first choice."),
      ("What is the best month for a honeymoon in northern Pakistan?", "Late March to mid-April for blossom, or late September to October for autumn colours and clear skies. June and September are best for Naran."),
      ("How many days do we need for a honeymoon in Hunza or Skardu?", "About 5-7 days for Hunza and 6-8 for Skardu. Naran works in 3-4 days."),
      ("How much does a honeymoon package in northern Pakistan cost?", "Published packages run from about Rs 40,000 for a 2-day Shogran break to Rs 120,000-190,000 for 5-8 days in Hunza or Skardu with a private car. Confirm what's included and the hotel names before paying."),
    ],
  },
  # ------------------------------------------------------------------ HUNZA
  {
    "path": "hunza/honeymoon", "crumbs": [("Hunza", "/hunza"), ("Honeymoon", None)],
    "title": "Honeymoon in Hunza 2026: Best Time, Romantic Hotels & Packages",
    "desc": "Planning a honeymoon in Hunza? A local's guide to the best months, the most romantic hotels, things to do as a couple, a 5-day plan and 2026 honeymoon packages.",
    "eyebrow": "Honeymoon &middot; Hunza &middot; 2026",
    "h1": "Honeymoon in Hunza: A Local's Guide for Couples",
    "img": "hunza-autumn-photo.webp", "img_alt": "Hunza Valley in autumn colours",
    "caption": "Hunza in autumn - golden poplars, snow peaks and very few crowds.",
    "body": f"""
<p>A Hunza honeymoon is one of the most beautiful you can have in Asia: snow peaks outside your window, old forts above apricot orchards, and evenings in quiet cafes. I'm from Gilgit-Baltistan, so here's how I'd plan it - when to go, where to stay, and what's worth doing as a couple.</p>
<h2>Best time for a honeymoon in Hunza</h2>
<ul>
<li><strong>Late March to mid-April:</strong> cherry and apricot blossom across Karimabad and Altit - the most romantic window, and the busiest, so book early.</li>
<li><strong>Late September to October:</strong> golden poplars, clear skies and fewer visitors. My pick for couples.</li>
<li><strong>Summer:</strong> everything is open and green, but late July to mid-August brings monsoon landslides on the road - keep spare days.</li>
<li><strong>Winter:</strong> beautiful and silent, but several hotels close (Luxus at Attabad shuts for winter) and evenings are very cold.</li>
</ul>
<h2>The most romantic hotels in Hunza</h2>
{stays_table([
  ("Serena Altit Fort Residence", "Altit &middot; luxury heritage", "Heritage rooms and luxury tents in the royal garden of Altit Fort - quiet, historic and intimate.", "9.7 Booking.com"),
  ("Hunza Serena Hotel", "Karimabad &middot; luxury", "The safe upscale choice: consistent service and a panorama of Rakaposhi, Ultar and Lady Finger.", "9.1 Trip.com (24 reviews)"),
  ("Luxus Hunza Attabad Lake Resort", "Attabad Lake &middot; luxury", "Rooms right over the turquoise lake, with a spa. Book the newer rooms; closed in winter.", "9.0 Booking.com (361)"),
  ("Eagle's Nest Hotel", "Duikar &middot; upper tier", "The famous clifftop sunrise over 11 peaks. Stay one or two nights for the view, not the service.", "4.0 Tripadvisor (142)"),
  ("Roomy Daastaan Hotel", "Karimabad &middot; mid-range", "Modern rooms and a big panoramic terrace - the best value for couples on a budget.", "8.7 Booking.com"),
  ("Passu Tourist Lodge", "Passu &middot; mid-range", "A small, quiet lodge under the Passu Cones - and open all winter.", "4.5 Tripadvisor (6)"),
])}
<p>Ratings were checked in July 2026; prices change by season, so ask for a valley- or Rakaposhi-facing room - on a honeymoon, the view is the point. More options in my <a href="/hunza/hotels">Hunza hotels guide</a>.</p>
<h2>Romantic things to do in Hunza</h2>
<ul>
<li>Watch sunrise or sunset at <strong>Eagle's Nest</strong> above Duikar - eleven peaks turning pink.</li>
<li>Take the guided tour of <a href="/hunza/altit-fort">Altit Fort</a> and have tea in the royal garden below it.</li>
<li>A boat ride on <a href="/hunza/attabad-lake">Attabad Lake</a>, then lunch in Gulmit.</li>
<li>Walk around <a href="/hunza/borith-lake">Borith Lake</a> and drive past the Passu Cones in the late afternoon light.</li>
<li>Cross the <strong>Hussaini suspension bridge</strong> together - if you're both brave.</li>
<li>Wander Karimabad's lanes and cafes in the evening, below <a href="/hunza/baltit-fort">Baltit Fort</a>.</li>
</ul>
<h2>A 5-day Hunza honeymoon plan</h2>
<table class="rev-itin"><tbody>
<tr><td>Day 1</td><td>Fly Islamabad to Gilgit (about 1 h, weather permitting) and drive to Karimabad (2-3.5 h). Slow evening.</td></tr>
<tr><td>Day 2</td><td>Baltit Fort in the morning, Altit Fort and its garden in the afternoon, sunset at Eagle's Nest.</td></tr>
<tr><td>Day 3</td><td>Attabad Lake by boat, lunch in Gulmit, Borith Lake and the Passu Cones. One night at Attabad or Passu.</td></tr>
<tr><td>Day 4</td><td>A lazy morning, then back to Karimabad for a last evening in the old town.</td></tr>
<tr><td>Day 5</td><td>Drive to Gilgit and fly home - or take two days by road via Chilas.</td></tr>
</tbody></table>
<p>Want more? Add Khunjerab Pass (4,693m - keep it short) or two nights at <a href="/fairy-meadows">Fairy Meadows</a> on the way in.</p>
<h2>Hunza honeymoon packages 2026</h2>
<p>Most Hunza honeymoons are built custom, but these are the published packages, all 5 days by road from Islamabad or Lahore with a private car (prices re-checked 21 October 2026):</p>
{pkg_table([
  ("5-Day Luxury Honeymoon Tour to Hunza", PTP + "5-days-super-deluxe-honeymoon-tour-to-hunza-valley/", "5", "Rs 160,000", "All meals; hotel listed as \"5-star\" but not named - confirm it."),
  ("5-Day Standard Honeymoon Tour to Hunza", PTP + "5-days-deluxe-honeymoon-tour-to-hunza-valley/", "5", "Rs 135,000", "Breakfast and dinner; listed as a 3-star hotel."),
  ("5-Day Honeymoon Tour to Hunza", PTP + "7-days-honeymoon-tour-to-hunza-valley/", "5", "Rs 120,000", "Breakfast and lunch; listed as a 2-star hotel."),
])}
<p>All three are from Pakistan Travel Places and are road trips, so only about one full day is spent in Hunza itself - the rest is mostly driving. If you can, fly instead and plan privately. Ask which hotel you'll be in, by name, before you pay. For group tours and longer trips, see my <a href="/tours/hunza">Hunza tour packages comparison</a>.</p>
{cta("Want it planned around just the two of you?", "Tell me your dates and budget and I'll suggest the route and the romantic rooms, or point you to a locally owned operator for a private trip. Free.", "Hi Faisal, we're planning our honeymoon in Hunza. Can you help us plan it?")}
{COUPLE_TIPS}
""",
    "faq": [
      ("What is the best month for a honeymoon in Hunza?", "Late March to mid-April for cherry and apricot blossom, or late September to October for autumn colours and clear skies. Avoid late July to mid-August, when monsoon landslides can close the road."),
      ("Which is the most romantic hotel in Hunza?", "Serena Altit Fort Residence for heritage and quiet, Luxus at Attabad Lake for a luxury lake view (closed in winter), and Eagle's Nest at Duikar for the famous sunrise. Hunza Serena is the most consistent all-rounder."),
      ("How much does a Hunza honeymoon package cost?", "Published 5-day honeymoon packages by road cost Rs 120,000, Rs 135,000 or Rs 160,000 depending on the hotel level and meals. Ask for the hotel name in writing."),
      ("How many days do we need for a honeymoon in Hunza?", "Five days covers it if you fly to Gilgit; allow seven by road, or if you want Khunjerab Pass and Upper Hunza at a relaxed pace."),
    ],
  },
  # ------------------------------------------------------------------ SKARDU
  {
    "path": "skardu/honeymoon", "crumbs": [("Skardu", "/skardu"), ("Honeymoon", None)],
    "title": "Honeymoon in Skardu 2026: Romantic Hotels, Shigar & Packages",
    "desc": "Honeymoon in Skardu: the most romantic hotels (Shigar Fort, Himmel, Arish), Shangrila and Khaplu, the best months, a 6-day plan and 2026 honeymoon packages.",
    "eyebrow": "Honeymoon &middot; Skardu &middot; 2026",
    "h1": "Honeymoon in Skardu: Forts, Lakes and the Best Romantic Stays",
    "img": "shangrila-photo.webp", "img_alt": "Shangrila Resort on Lower Kachura Lake, Skardu",
    "caption": "Shangrila on Lower Kachura Lake - Skardu's most famous romantic spot.",
    "body": f"""
<p>Skardu has the most special honeymoon hotels in northern Pakistan: a 400-year-old fort in Shigar, a royal palace in Khaplu, and new lodges with glass walls facing the Indus. Add turquoise lakes, cold deserts and - in summer - the Deosai plateau, and it's a honeymoon you'll talk about for years.</p>
<h2>Best time for a honeymoon in Skardu</h2>
<ul>
<li><strong>April:</strong> apricot and cherry blossom in Shigar and Khaplu.</li>
<li><strong>Mid-June to September:</strong> everything open, including Deosai (only open from about mid-June to late September or early October).</li>
<li><strong>September to October:</strong> clear skies, golden light and quieter hotels - lovely for couples.</li>
<li><strong>Winter:</strong> snowy and peaceful, but cold; the main Skardu hotels stay open.</li>
</ul>
<h2>The most romantic hotels in Skardu</h2>
{stays_table([
  ("Serena Shigar Fort", "Shigar, ~1-2 h from Skardu &middot; heritage luxury", "A restored 400-year-old fort-palace with apricot gardens - the region's flagship boutique stay.", "4.7 Tripadvisor (223)"),
  ("Himmel Skardu by Luxus", "Wazir Pur, by the Indus &middot; luxury", "Newer riverside lodge with floor-to-ceiling views of snow peaks. The drive in is bumpy.", "9.4 Booking.com (52)"),
  ("Arish Luxury Suites", "Skardu &middot; luxury", "Spacious, elegant suites - often called the best hotel in Skardu town.", "9.2 Booking.com (45)"),
  ("Byarsa Hotel", "Skardu &middot; boutique", "Design-led rooms and a rooftop terrace facing the mountains.", "4.4 Google (337)"),
  ("Shangrila Resort", "Lower Kachura Lake &middot; resort", "The famous red-roofed cottages around the heart-shaped lake. Come for the setting - rooms are tired; a day visit or one night is enough.", "6.6 HotelsCombined (81)"),
  ("Hotel Himalaya Skardu", "Outside town &middot; mid-range", "Small, quiet and service-first - good value for couples.", "4.3 Google (692)"),
])}
<p>Ratings were checked in July 2026. Split your stay: one or two nights at Shigar Fort, the rest in Skardu or by the river. More in my <a href="/skardu/hotels">Skardu hotels guide</a>.</p>
<h2>Romantic things to do in Skardu</h2>
<ul>
<li>A boat on <a href="/skardu/kachura-lake">Lower Kachura (Shangrila)</a> and a quiet walk at Upper Kachura Lake.</li>
<li>Sunset on the dunes of the <a href="/skardu/katpana-desert">Katpana</a> or <a href="/skardu/sarfaranga-cold-desert">Sarfaranga</a> cold deserts.</li>
<li>Breakfast in the gardens of <a href="/skardu/shigar-fort">Shigar Fort</a>.</li>
<li>A day in <a href="/skardu/khaplu">Khaplu</a>: the palace and the old Chaqchan Mosque.</li>
<li>In summer, a private jeep to <a href="/deosai">Deosai</a> for wildflowers and Sheosar Lake.</li>
</ul>
<h2>A 6-day Skardu honeymoon plan</h2>
<table class="rev-itin"><tbody>
<tr><td>Day 1</td><td>Fly Islamabad to Skardu (about 1 h). Settle in; evening at Upper Kachura Lake.</td></tr>
<tr><td>Day 2</td><td>Shangrila by boat, then Katpana desert at sunset.</td></tr>
<tr><td>Day 3</td><td>To Shigar: Sarfaranga desert on the way, then a night at Shigar Fort.</td></tr>
<tr><td>Day 4</td><td>On to Khaplu for the palace and Chaqchan Mosque (3-4 h from Skardu).</td></tr>
<tr><td>Day 5</td><td>Back to Skardu - or, from mid-June to September, a day trip to Deosai.</td></tr>
<tr><td>Day 6</td><td>Fly home. Keep the next day free in case the flight is cancelled.</td></tr>
</tbody></table>
<h2>Skardu honeymoon packages 2026</h2>
<p>These are the published Skardu honeymoon packages, both 8 days by road from Islamabad with a private car (re-checked 21 October 2026):</p>
{pkg_table([
  ("8-Day Luxury Honeymoon Tour to Skardu, Shangrila, Khaplu & Shigar", PTP + "8-days-super-deluxe-honeymoon-tour-to-skardu-shangrila-khaplu-shiger-valley/", "8", "Rs 190,000", "All meals; nights at Shangrila and the Khaplu palace."),
  ("8-Day Honeymoon Tour to Skardu, Shangrila, Khaplu & Shigar", PTP + "5-days-honeymoon-tour-to-skardu-shangrila-khaplu-shiger-valley/", "8", "Rs 160,000", "Breakfast and dinner; same route."),
])}
<p>Both are from Pakistan Travel Places and spend about four of the eight days driving, so if you can, fly in and build the rest privately. For other Skardu trips, see my <a href="/tours/skardu">Skardu tour packages comparison</a>.</p>
{cta("Want it planned around just the two of you?", "Tell me your dates and budget and I'll suggest the route and the right rooms - Shigar Fort books up early - or point you to a locally owned operator. Free.", "Hi Faisal, we're planning our honeymoon in Skardu. Can you help us plan it?")}
{COUPLE_TIPS}
""",
    "faq": [
      ("What is the best month for a honeymoon in Skardu?", "April for blossom, or September to October for clear skies and golden light. Come between mid-June and September if you want to see Deosai."),
      ("Which is the most romantic hotel in Skardu?", "Serena Shigar Fort, a restored 400-year-old fort-palace, is the most romantic. Himmel Skardu by Luxus and Arish Luxury Suites are the best modern luxury options; Shangrila has the famous lake setting but tired rooms."),
      ("How much does a Skardu honeymoon package cost?", "The published 8-day honeymoon packages by road cost Rs 160,000 (breakfast and dinner) or Rs 190,000 (all meals). Flying in and planning privately can save time."),
      ("Should we fly or drive to Skardu for our honeymoon?", "Fly if you can - it's about an hour instead of 16-18 hours by road. Flights are weather-dependent, so keep a spare day."),
    ],
  },
  # ------------------------------------------------------------------ NARAN
  {
    "path": "naran-kaghan/honeymoon", "crumbs": [("Naran Kaghan", "/naran-kaghan"), ("Honeymoon", None)],
    "title": "Honeymoon in Naran & Kaghan 2026: Stays, Lakes & Packages",
    "desc": "Honeymoon in Naran and Kaghan: Saif-ul-Malook, Shogran and Babusar, romantic stays, the best months to avoid crowds, a 3-day plan and 2026 honeymoon packages.",
    "eyebrow": "Honeymoon &middot; Naran &amp; Kaghan &middot; 2026",
    "h1": "Honeymoon in Naran and Kaghan: The Short Mountain Escape",
    "img": "naran-kaghan-photo.webp", "img_alt": "Lake Saif-ul-Malook in the Kaghan Valley",
    "caption": "Lake Saif-ul-Malook - where, legend says, a prince fell in love with a fairy princess.",
    "body": f"""
<p>Naran is the honeymoon for couples short on time: it's 6-9 hours by road from Islamabad, there's no flight to worry about, and the scenery - glacier lakes, pine forests and the Babusar Pass - is some of the best in Pakistan. The catch is crowds, so timing is everything.</p>
<h2>Best time for a honeymoon in Naran</h2>
<ul>
<li><strong>June:</strong> snow just cleared, cool days and wildflowers everywhere.</li>
<li><strong>September:</strong> clear, quiet and golden. My favourite.</li>
<li><strong>Avoid July-August if you can:</strong> Naran fills up, and a 2-hour valley drive can take 6 in traffic.</li>
<li><strong>Season:</strong> the Babusar road is open roughly late May to October; outside that, stay lower down at Shogran.</li>
</ul>
<h2>Romantic places to stay</h2>
<ul>
<li><strong>PTDC Log Huts, Shogran</strong> - government log cabins in the forest, about PKR 10,000-18,000 a night. Quiet and cosy.</li>
<li><strong>Pine Park Hotel, Shogran</strong> - reliable, with views of Malika Parbat, about PKR 6,000-12,000.</li>
<li><strong>Lalazar Hotel, Naran</strong> - the best-appointed hotel in Naran town, with river views and reliable heating.</li>
<li><strong>PTDC Motel, Naran</strong> - basic but dependable, about PKR 2,000-4,000, if you'd rather spend on experiences.</li>
</ul>
<p>For a quieter honeymoon, stay at Shogran rather than in Naran town - it's lower (2,362m), forested and much calmer. Prices are 2026 guides; they rise sharply in August.</p>
<h2>Romantic things to do</h2>
<ul>
<li><strong>Lake Saif-ul-Malook</strong> early in the morning, before the crowds (jeep about PKR 5,500 return from Naran). It's the lake of the prince-and-fairy legend.</li>
<li><strong>Lulusar Lake</strong> - bigger and quieter, perfect reflections on a calm morning.</li>
<li><strong>Babusar Top at dawn</strong> (4,173m) - stay near Lulusar and drive up before the tour jeeps arrive.</li>
<li><strong>Siri Paye meadows</strong> above Shogran - a 2-hour walk or a horse ride (about PKR 800-1,500 one way).</li>
<li><strong>Lalazar plateau</strong> for wildflowers and birch forest, and a trout lunch by the Kunhar River.</li>
</ul>
<h2>A 3-day Naran honeymoon plan</h2>
<table class="rev-itin"><tbody>
<tr><td>Day 1</td><td>Islamabad to Shogran (via Kiwai). Afternoon walk towards Siri Paye; night in a log hut.</td></tr>
<tr><td>Day 2</td><td>Up the valley to Naran: Lake Saif-ul-Malook in the morning, Lulusar and Babusar Top in the afternoon.</td></tr>
<tr><td>Day 3</td><td>A slow morning by the Kunhar, then home.</td></tr>
</tbody></table>
<p>Got more time? In summer, cross Babusar to Chilas and carry on to Hunza - see <a href="/hunza/honeymoon">honeymoon in Hunza</a>.</p>
<h2>Naran honeymoon packages 2026</h2>
<p>Published couples' packages from Islamabad or Lahore (re-checked 21 October 2026):</p>
{pkg_table([
  ("3-Day Honeymoon Tour to Naran & Kaghan", PTP + "3-days-honeymoon-tour-to-naran-kaghan/", "3", "Rs 60,000", "Breakfast and dinner; Kiwai waterfall, Lulusar, Babusar Top and Saif-ul-Malook."),
  ("2-Day Honeymoon Tour to Shogran", PTP + "3-days-luxury-honeymoon-tour-to-murree-shogran/", "2", "Rs 40,000", "Breakfast and dinner; jeep up to Siri Paye."),
  ("4-Day Couple Tour, Naran & Kaghan", "https://narankaghantours.com/tours/4-days-3-nights-couple-trip-naran-kaghan/", "4", "On request", "All meals listed; Balakot, Shogran, Naran and Babusar. Naran Kaghan Tours asks you to WhatsApp for the current price."),
])}
<p>See also my <a href="/tours/naran-kaghan">Naran Kaghan tour packages</a> and the full <a href="/naran-kaghan">Naran &amp; Kaghan guide</a>.</p>
{cta("Want a quiet Naran honeymoon?", "Tell me your dates and I'll suggest where to stay to avoid the crowds, or point you to a locally run operator. Free.", "Hi Faisal, we're planning our honeymoon in Naran and Kaghan. Can you help us plan it?")}
{COUPLE_TIPS}
""",
    "faq": [
      ("Is Naran good for a honeymoon?", "Yes, especially if you have only 3-4 days: it's 6-9 hours by road from Islamabad with no flights to worry about. Go in June or September to avoid the summer crowds, and stay at Shogran for a quieter base."),
      ("What is the best month for a honeymoon in Naran?", "June or September. July and August are the busiest months, with heavy traffic in the valley."),
      ("How much does a Naran honeymoon package cost?", "Published packages cost about Rs 60,000 for 3 days in Naran and Kaghan, or Rs 40,000 for 2 days in Shogran, with breakfast and dinner."),
      ("Where should we stay in Naran for a honeymoon?", "The PTDC log huts or Pine Park Hotel at Shogran for quiet forest views, or Lalazar Hotel in Naran town for comfort and river views."),
    ],
  },
]


def seo_block(tpl_block, p, url, img_url):
    b = tpl_block
    b = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, b)
    for prop, val in (("og:title", p["title"]), ("og:description", p["desc"]), ("og:url", url), ("og:image", img_url)):
        b = re.sub(rf'(<meta property="{prop}" content=")[^"]*', lambda m, v=val: m.group(1) + e(v), b)
    for name, val in (("twitter:title", p["title"]), ("twitter:description", p["desc"]), ("twitter:image", img_url)):
        b = re.sub(rf'(<meta name="{name}" content=")[^"]*', lambda m, v=val: m.group(1) + e(v), b)
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": D}]
    for i, (name, href) in enumerate(p["crumbs"], 2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": D + href if href else url})
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": items},
        {"@type": "Article", "headline": p["title"], "description": p["desc"], "image": img_url,
         "author": {"@type": "Person", "name": "Faisal Zaman", "@id": f"{D}/#faisal"},
         "publisher": {"@id": f"{D}/#org"}, "dateModified": TODAY, "mainEntityOfPage": url}]}
    return re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda m: '<script type="application/ld+json">\n' + json.dumps(graph, indent=2, ensure_ascii=False) + '\n</script>',
                  b, count=1, flags=re.S)


def main():
    t = TEMPLATE.read_text(encoding="utf-8")
    head_pre = t[:t.index("<!-- SEO:START -->")]
    tpl_seo = t[t.index("<!-- SEO:START -->"):t.index("<!-- SEO:END -->") + len("<!-- SEO:END -->")]
    nav = t[t.index("</head>"):t.index('<main class="article">')]
    tail = t[t.index("<footer>"):]
    tail = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", tail, flags=re.S)
    tail = re.sub(r"<!-- (WA-FLOAT|WA-HELP|RELATED|PHOTO-CREDITS|REC-OPS|TOUR-LINKS):START -->.*?<!-- \1:END -->\n?", "", tail, flags=re.S)
    for p in PAGES:
        url = f"{D}/{p['path']}"
        img_url = f"{D}/images/{p['img']}"
        head = re.sub(r"<title>.*?</title>", f"<title>{e(p['title'])}</title>", head_pre, count=1, flags=re.S)
        head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(p["desc"]), head, count=1)
        crumb_html = '<a href="/" style="color:inherit">Home</a>' + "".join(
            f' / <a href="{h}" style="color:inherit">{e(n)}</a>' if h else f' / <span style="color:var(--cream)">{e(n)}</span>'
            for n, h in p["crumbs"])
        faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
        main_html = f'''<main class="article">
<div class="article-head"><div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em">{crumb_html}</div>
<div class="article-eyebrow">{p["eyebrow"]}</div>
<h1 class="article-title">{e(p["h1"])}</h1>
<div class="article-meta"><span>By <a href="/about"><strong>Faisal Zaman</strong></a></span><span class="sep">&middot;</span><span>Local, Gilgit-Baltistan</span><span class="sep">&middot;</span><span>Updated October 2026</span></div></div>
<figure class="article-figure"><div class="img" style="background-image:url('/images/{p["img"]}')" role="img" aria-label="{e(p["img_alt"])}"></div><figcaption>{e(p["caption"])}</figcaption></figure>
<div class="article-body">
{p["body"].strip()}
<h2>FAQ</h2>
<div class="faq">{faq_html}</div>
</div></main>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
'''
        out = ROOT / p["path"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(head + seo_block(tpl_seo, p, url, img_url) + "\n" + nav + main_html + tail, encoding="utf-8")
        print("wrote", p["path"])


if __name__ == "__main__":
    main()
