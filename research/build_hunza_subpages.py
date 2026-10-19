#!/usr/bin/env python3
"""
Hunza tour sub-pages: /tours/hunza/5-days, /tours/hunza/family, /tours/hunza/budget.

Clones the site shell (head, nav, footer, scripts) from tours/hunza/honeymoon and
writes each page's article from the PAGES data below. Visible FAQ and FAQPage
JSON-LD come from the same list, so they always match. Facts follow FACTS.md
(Oct 2026). Re-run after editing, then run the sitewide generators:

  python3 research/build_hunza_subpages.py
  python3 related_links.py && python3 whatsapp_help.py && python3 photo_credits.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = "https://www.gilgitbaltistanguide.com"
TEMPLATE = ROOT / "tours/hunza/honeymoon/index.html"
TODAY = "2026-10-20"
e = html.escape

PAGES = [
  {
    "slug": "5-days", "crumb": "5 Days",
    "title": "5 Days Hunza Tour 2026: Itinerary, Cost & Packages",
    "desc": "Planning a 5-day Hunza tour? A local's day-by-day itinerary, fly vs road, what it costs in 2026, and the 5-day packages worth booking.",
    "eyebrow": "Hunza &middot; 5-day trip &middot; 2026",
    "h1": "A 5-Day Hunza Tour: The Itinerary I'd Actually Do",
    "img": "attabad-photo.webp", "img_alt": "Attabad Lake, Upper Hunza",
    "caption": "Attabad Lake - an easy half-day from Karimabad, and on every good 5-day plan.",
    "body": """
<p>Five days is the most common trip length people ask me about - and it can work, but only if you're honest about the journey. Islamabad to Hunza is 14-20 hours by road, so how you get there decides whether you get two days in Hunza or four.</p>
<h2>Can you do Hunza in 5 days?</h2>
<p>Yes, with one of two choices:</p>
<ul>
<li><strong>Fly one way (or both).</strong> Islamabad to Gilgit is about an hour on PIA's small ATR planes, around 6 flights a week, and they're often cancelled for cloud. Fly up, drive back, and you get roughly three full days in Hunza.</li>
<li><strong>Drive, and accept two travel days.</strong> By road, a 5-day trip gives you about two full days in Hunza. That's what the budget 5-day packages do. In summer the Naran-Babusar road (open roughly late May to October) is the more scenic way up.</li>
</ul>
<div class="callout"><h3>Fly vs drive for 5 days</h3>
<table class="cmp-table"><thead><tr><th></th><th>Fly up, drive back</th><th>Drive both ways</th></tr></thead><tbody>
<tr><td>Full days in Hunza</td><td>About 3</td><td>About 2</td></tr>
<tr><td>Getting there</td><td>About 1 h flight, then 2-3.5 h drive to Karimabad</td><td>14-20 h, usually with a night in Chilas or Besham</td></tr>
<tr><td>Typical one-way cost</td><td>PKR 19,000-28,000 flight (more in peak season)</td><td>PKR 4,850-6,100 by coach from Rawalpindi</td></tr>
<tr><td>Main risk</td><td>Flight cancelled - have a road plan B</td><td>Landslides, especially late July to mid-August</td></tr>
</tbody></table></div>
<h2>My 5-day Hunza itinerary (fly in, drive out)</h2>
<table class="rev-itin"><tbody>
<tr><td>Day 1</td><td>Fly Islamabad to Gilgit and drive up to Karimabad (2-3.5 h). If you're in time, sunset at Eagle's Nest above Duikar - a short jeep ride up.</td></tr>
<tr><td>Day 2</td><td>Karimabad: Baltit Fort, then walk down through the old village to Altit Fort. Both have guided tours (around PKR 2,000 and 1,600 for non-locals in 2026 - confirm at the gate). Evening in the bazaar.</td></tr>
<tr><td>Day 3</td><td>Upper Hunza: Attabad Lake (30-60 minutes away), the Hussaini suspension bridge (small toll), Passu Cones and Borith Lake. Sleep in Gulmit or Passu.</td></tr>
<tr><td>Day 4</td><td>Khunjerab Pass (4,693m) on the China border - a few hours each way from Passu, so start early, and don't stay long at that height. Back down towards Karimabad or Gilgit.</td></tr>
<tr><td>Day 5</td><td>The long drive south to Islamabad (12-16 h from Gilgit), or fly if you've booked both ways.</td></tr>
</tbody></table>
<p>Driving both ways? Swap Day 1 for Islamabad to Chilas (via Babusar in summer), reach Karimabad on Day 2, and drop either Khunjerab or Upper Hunza - you can't fit both in comfortably.</p>
<h2>5-day Hunza packages</h2>
<p>Two published 5-day packages are in my <a href="/tours/hunza">Hunza tour packages comparison</a>, both by road from Lahore:</p>
<ul>
<li><a href="/tours/hunza#ptp-5">5-Day Hunza &amp; Khunjerab Pass Trip</a> - from Rs 17,500, breakfast and dinner, via Babusar.</li>
<li><a href="/tours/hunza#ptp-autumn">Autumn Tour to Hunza</a> - from Rs 22,000, all meals.</li>
</ul>
<p>For a private 5-day trip with your own car and driver, expect roughly Rs 49,500 per person in 2026, depending on the car, hotels and group size - get an itemised quote.</p>
<h2>Tips for a 5-day trip</h2>
<ul>
<li>Keep the last day flexible. If a flight is cancelled or the road closes, it's the day you'll need.</li>
<li>Best months: late March to mid-April for blossom, May-June and September-October for steady roads and clear views. Late July to mid-August brings monsoon road closures.</li>
<li>Khunjerab is the highest point of the trip - short visits only, and skip it if anyone in your group struggles with altitude.</li>
</ul>
""",
    "faq": [
      ("Is 5 days enough for Hunza?", "Yes, if you fly at least one way - that leaves about three full days for Karimabad, Upper Hunza and Khunjerab. By road both ways you'll have about two full days in Hunza, so choose between Khunjerab and Upper Hunza."),
      ("How much does a 5-day Hunza tour cost?", "Published budget packages by road start at about Rs 17,500-22,000 per person. A private 5-day trip with your own car runs roughly Rs 49,500 per person in 2026. Flights add about PKR 19,000-28,000 each way."),
      ("Should I fly or drive for a 5-day Hunza trip?", "Fly up and drive back if you can. The Gilgit flight is about an hour but often cancelled, so keep a road plan B; driving takes 14-20 hours each way."),
      ("Can I visit Khunjerab Pass on a 5-day trip?", "Yes - give it a full day from Passu or Karimabad, start early, and keep the stop at 4,693m short."),
    ],
  },
  {
    "slug": "family", "crumb": "Family",
    "title": "Hunza Family Tour 2026: Planning a Trip with Kids or Parents",
    "desc": "Taking kids or parents to Hunza? A local's guide to family pacing, the long road, altitude, family-friendly sights and stays, and a 7-day family itinerary.",
    "eyebrow": "Hunza &middot; Family trip &middot; 2026",
    "h1": "Taking the Family to Hunza: What I'd Plan for Kids and Parents",
    "img": "blossom-photo.webp", "img_alt": "Cherry blossom in Hunza",
    "caption": "Blossom season in Hunza - one of the best times for a family trip.",
    "body": """
<p>Hunza is a lovely family trip once you're there: short drives between sights, safe villages, apricots and cherries in season, and people who are kind to children. The hard part is the journey - so a family trip is mostly about pacing.</p>
<h2>Getting there with kids or older parents</h2>
<ul>
<li><strong>By road it's 14-20 hours from Islamabad.</strong> Split it: stop overnight in Besham or Chilas rather than doing it in one push. The KKH is winding, so pack motion-sickness tablets and plenty of water and snacks.</li>
<li><strong>Flying saves two days.</strong> Islamabad to Gilgit is about an hour, but flights are often cancelled for weather - book a flexible day either side.</li>
<li><strong>Summer route over Babusar:</strong> the top is 4,173m. A short photo stop is fine for most families; don't linger if anyone feels unwell.</li>
</ul>
<h2>Altitude, gently</h2>
<p>Karimabad sits at about 2,500m, which most families barely notice. The one place to be careful is <strong>Khunjerab Pass at 4,693m</strong>: keep the visit short, keep children warm, and if a parent has a heart or lung condition, check with their doctor first or skip it.</p>
<h2>Family-friendly things to do in Hunza</h2>
<ul>
<li>A boat ride on <a href="/hunza/attabad-lake">Attabad Lake</a> - the favourite with kids.</li>
<li><a href="/hunza/baltit-fort">Baltit</a> and <a href="/hunza/altit-fort">Altit</a> forts - guided, with lots of stairs; manageable for most ages at a slow pace.</li>
<li>Walking the lanes and orchards of old Altit and Karimabad, and the bazaar.</li>
<li>Sunset at Eagle's Nest (a short jeep ride up).</li>
<li>Borith Lake and the views of Passu Cones from the road.</li>
<li>Skip with small children: the <strong>Hussaini suspension bridge</strong> - it sways, has big gaps between planks, and is for confident adults only.</li>
</ul>
<h2>A 7-day family itinerary</h2>
<table class="rev-itin"><tbody>
<tr><td>Day 1</td><td>Islamabad to Besham or Chilas - break the long road in two.</td></tr>
<tr><td>Day 2</td><td>On to Karimabad, with a stop at the Rakaposhi viewpoint. Early night.</td></tr>
<tr><td>Day 3</td><td>Baltit Fort in the morning, rest after lunch, Eagle's Nest for sunset.</td></tr>
<tr><td>Day 4</td><td>Attabad Lake boat ride, then a slow drive to Gulmit or Passu.</td></tr>
<tr><td>Day 5</td><td>Borith Lake and the Passu villages; a short Khunjerab visit if everyone's up for it.</td></tr>
<tr><td>Day 6</td><td>Back down to Gilgit or Chilas.</td></tr>
<tr><td>Day 7</td><td>Home to Islamabad. If you fly, you can cut the trip to 5 days or add two easy days in Hunza.</td></tr>
</tbody></table>
<h2>Where to stay and how to get around</h2>
<p>Family guesthouses in Karimabad cost roughly PKR 2,000-6,500 a room per night in 2026, and many have family rooms - see my <a href="/hunza/hotels">Hunza hotels guide</a>. A private car and driver (about PKR 8,000-15,000 a day) is far easier with kids than shared vans, because you stop when they need to.</p>
<h2>Which packages suit families?</h2>
<p>From my <a href="/tours/hunza">Hunza tour packages comparison</a>, the slower trips suit families best - ones with a private vehicle, at least two nights in each place, and no overnight bus. Avoid packages that start with a midnight departure if you have young children. Or tell me your family's ages and dates on WhatsApp and I'll point you to a locally owned operator that runs private family trips.</p>
<h2>Family checklist</h2>
<ul>
<li>Warm layers for everyone, even in summer - evenings and Khunjerab get cold.</li>
<li>Cash: ATMs are limited outside Gilgit and Karimabad.</li>
<li>A basic first-aid kit, motion-sickness tablets, and any regular medicines.</li>
<li>One spare day, especially from late July to mid-August when monsoon landslides can close roads.</li>
</ul>
""",
    "faq": [
      ("Is Hunza good for a family trip?", "Yes - once you're there, sights are close together and the villages are safe and welcoming. Plan around the long journey: split the road over two days or fly to Gilgit."),
      ("How many days does a family need for Hunza?", "About 7 days by road, so nobody spends more than one long day in the car. Flying one way can bring it down to 5."),
      ("Is the altitude a problem for kids or elderly parents?", "Karimabad is about 2,500m and fine for most people. Khunjerab Pass at 4,693m is the exception - keep it short, and check with a doctor first if anyone has a heart or lung condition."),
      ("What is the best month for a family trip to Hunza?", "May-June and September-October have the most reliable roads. Late March to mid-April is blossom season. Avoid late July to mid-August, when monsoon landslides can close the road."),
    ],
  },
  {
    "slug": "budget", "crumb": "Budget",
    "title": "Cheap Hunza Tour 2026: Budget Packages vs Doing It Yourself",
    "desc": "The cheapest Hunza tour packages for 2026, what a budget trip really costs if you do it yourself, and when each is the better deal - from a local.",
    "eyebrow": "Hunza &middot; Budget trip &middot; 2026",
    "h1": "Hunza on a Budget: Cheap Packages vs Doing It Yourself",
    "img": "karakoram-highway-photo.webp", "img_alt": "The Karakoram Highway below Rakaposhi",
    "caption": "The Karakoram Highway - the cheapest way to Hunza is by road.",
    "body": """
<p>Hunza doesn't have to be expensive. The two real choices are a budget group package or doing it yourself by coach - and which is cheaper depends mostly on whether you're travelling alone or with friends.</p>
<h2>The cheapest Hunza packages in 2026</h2>
<p>These are the lowest published prices in my <a href="/tours/hunza">Hunza tour packages comparison</a>:</p>
<ul>
<li><a href="/tours/hunza#ptp-5">5-Day Hunza &amp; Khunjerab Pass Trip</a> - from Rs 17,500 per person (breakfast and dinner).</li>
<li><a href="/tours/hunza#ptp-naltar">6-Day Hunza &amp; Naltar Valley Trip</a> - from Rs 19,500 (breakfast only).</li>
<li><a href="/tours/hunza#ptp-autumn">Autumn Tour to Hunza</a> - from Rs 22,000 (all meals).</li>
</ul>
<p>Before you pay, ask: how many people share the vehicle, which hotels (by name), which meals, and whether the price is a deposit or the full amount.</p>
<h2>What it costs to do it yourself</h2>
<table class="cmp-table"><thead><tr><th>Item</th><th>2026 cost (confirm locally)</th></tr></thead><tbody>
<tr><td>Coach Rawalpindi to Hunza</td><td>PKR 4,850-6,100 each way (14-18 h)</td></tr>
<tr><td>Coach from Lahore</td><td>PKR 6,900-8,400 each way</td></tr>
<tr><td>Guesthouse in Karimabad</td><td>PKR 2,000-6,500 per room per night</td></tr>
<tr><td>Local food</td><td>PKR 400-700 a dish; about PKR 1,500-2,000 a day</td></tr>
<tr><td>Private car with driver</td><td>About PKR 8,000-15,000 a day (split it between 3-4 people)</td></tr>
<tr><td>Baltit / Altit forts</td><td>Around PKR 2,000 / 1,600 for non-locals (locals pay much less)</td></tr>
</tbody></table>
<p>On the ground, a budget traveller spends roughly PKR 5,000-8,000 a day. So a 6-day trip from Rawalpindi - two days on the coach and four in Hunza - comes to roughly <strong>PKR 30,000-45,000 per person</strong> for one person travelling alone.</p>
<h2>So which is cheaper?</h2>
<ul>
<li><strong>Travelling alone:</strong> a budget group package is usually cheaper, because you're sharing the vehicle with the group.</li>
<li><strong>Three or four friends:</strong> doing it yourself often wins - you split one car and share rooms, and you choose your own pace and stops.</li>
</ul>
<h2>How to save money in Hunza</h2>
<ul>
<li>Avoid the peak weeks (blossom season and public holidays) if you can - rooms fill up and often cost more.</li>
<li>Stay in family-run guesthouses and eat local dishes - they're cheaper and the money stays in the valley.</li>
<li>Share a car for Khunjerab and Upper Hunza; split between four, a day's hire is very reasonable.</li>
<li>Carry enough cash - ATMs are limited outside Gilgit and Karimabad.</li>
</ul>
<p>Planning more of Gilgit-Baltistan on a budget? See my <a href="/travel/budget-gb-itinerary">GB budget itinerary</a> for a full route with costs.</p>
""",
    "faq": [
      ("What is the cheapest Hunza tour package in 2026?", "The lowest published price I found is a 5-day trip by road from about Rs 17,500 per person, with a 6-day Hunza and Naltar trip from Rs 19,500. Confirm what's included before paying."),
      ("How much does a budget trip to Hunza cost if I do it myself?", "Roughly PKR 30,000-45,000 per person for 6 days from Rawalpindi when travelling alone: about PKR 4,850-6,100 each way by coach, plus PKR 5,000-8,000 a day on the ground. Groups sharing a car and rooms pay less."),
      ("What is the cheapest way to get to Hunza?", "The coach from Rawalpindi, about PKR 4,850-6,100 one way, taking 14-18 hours."),
      ("Is a cheap Hunza package worth it?", "Often, if you're travelling alone - you share transport costs. Ask how many people share the vehicle, which hotels you'll stay in, which meals are included, and whether the price is a deposit or the full amount."),
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
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": D},
            {"@type": "ListItem", "position": 2, "name": "Tours", "item": f"{D}/tours"},
            {"@type": "ListItem", "position": 3, "name": "Hunza", "item": f"{D}/tours/hunza"},
            {"@type": "ListItem", "position": 4, "name": p["crumb"], "item": url}]},
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
    # drop page-specific JSON-LD and generator blocks from the tail; generators re-add theirs
    tail = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", tail, flags=re.S)
    tail = re.sub(r"<!-- (WA-FLOAT|WA-HELP|RELATED|PHOTO-CREDITS|REC-OPS|TOUR-LINKS):START -->.*?<!-- \1:END -->\n?", "", tail, flags=re.S)
    for p in PAGES:
        url = f"{D}/tours/hunza/{p['slug']}"
        img_url = f"{D}/images/{p['img']}"
        head = head_pre
        head = re.sub(r"<title>.*?</title>", f"<title>{e(p['title'])}</title>", head, count=1, flags=re.S)
        head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(p["desc"]), head, count=1)
        faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
        main = f'''<main class="article">
<div class="article-head"><div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em"><a href="/" style="color:inherit">Home</a> / <a href="/tours" style="color:inherit">Tours</a> / <a href="/tours/hunza" style="color:inherit">Hunza</a> / <span style="color:var(--cream)">{e(p["crumb"])}</span></div>
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
        page = head + seo_block(tpl_seo, p, url, img_url) + "\n" + nav + main + tail
        out = ROOT / "tours" / "hunza" / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
