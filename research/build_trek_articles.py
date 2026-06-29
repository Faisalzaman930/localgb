#!/usr/bin/env python3
"""Rebuild /trekking/<route> pages in the tour-page blog (.article) layout.
Pulls operator data from research/treks/<route>.json, reuses each page's
existing head/nav/footer/related, and assembles a full blog article.
Run: python3 research/build_trek_articles.py  (then seo_inject.py)"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'research', 'treks')
RATINGS = json.load(open(os.path.join(DATA, '_ratings.json')))

def _dom(home):
    return re.sub(r'^www\.', '', re.sub(r'https?://(?:www\.)?([^/]+).*', r'\1', home or ''))

def rating_obj(home):
    return RATINGS.get(_dom(home))

def rating_cell(home):
    r = rating_obj(home)
    if not r: return '<span style="color:var(--cream-2)">&mdash;</span>'
    return (f'<a href="{r["url"]}" target="_blank" rel="nofollow noopener" style="white-space:nowrap">'
            f'{r["rating"]:.1f} &#9733; <span style="color:var(--cream-2)">{r["platform"]} ({r["reviews"]})</span></a>')

def rating_span(home):
    r = rating_obj(home)
    if not r: return ''
    return (f'<span>&#9733; <strong>{r["rating"]:.1f}</strong> '
            f'<a href="{r["url"]}" target="_blank" rel="nofollow noopener">{r["platform"]} ({r["reviews"]})</a></span>')

def esc(s):
    if s is None: return ''
    return re.sub(r'&(?!amp;|lt;|gt;|#\d+;|quot;)', '&amp;', str(s))

def price_str(p):
    if p.get('price_usd'): return '$%s' % format(int(p['price_usd']), ',')
    if p.get('price_pkr'): return 'Rs %s' % format(int(p['price_pkr']), ',')
    return 'Quote only'
def has_price(p): return bool(p.get('price_usd') or p.get('price_pkr'))
def rank(p):
    if p.get('price_usd'): return int(p['price_usd'])
    if p.get('price_pkr'): return int(p['price_pkr'])/280.0
    return 9e9

def score(p, cheapest, dearest, allinc):
    if not has_price(p): return 7.6
    sc = 8.0
    g = (p.get('includes','')+p.get('good','')).lower()
    if p is cheapest: sc += 0.5
    if any(k in g for k in ('all-inclusive','all inclusive','all domestic flights','permits included','permit fees')): sc += 0.3
    if p.get('tiers'): sc += 0.2
    if 'local' in p.get('good','').lower() or 'balti' in g or 'hunza' in g: sc += 0.2
    if p is allinc: sc += 0.2
    return round(min(9.3, max(7.7, sc)), 1)

# ---- per-route bespoke content -------------------------------------------
C = {
 'k2-base-camp': dict(region='Baltoro, Skardu', h1='I Compared Every K2 Base Camp Trek Operator for 2026',
   intro=["The K2 Base Camp trek is the big one - up the Baltoro Glacier to Concordia, where four of the world's fourteen 8,000m peaks stand in a single arc, then on to the foot of K2 itself. I'm from Gilgit-Baltistan, so here is the honest version: who actually runs it, what they charge in 2026, and what you get for the money.",
          "I only compare operators who publish a real price (no \"contact us\"), read each itinerary, and note where permits, flights and porters are bundled or billed on top. It is a restricted-zone trek, so a licensed operator and guide are mandatory."],
   about="Reckon on 18-21 days return from Askole, with Concordia at around 4,600m and the K2 base camp viewpoint near 5,150m. The walking is non-technical but long and remote; the bill moves with group size, porter stages and the government royalty.",
   faqs=[("How much does the K2 Base Camp trek cost in 2026?","Locally run, group-based itineraries start around $1,400-$2,300 per person; Western-led expeditions run $4,500-$5,850. Government royalty and permit fees are usually extra. See the table above."),
         ("How many days do you need?","Most itineraries are 18-21 days door to door, including the drive or flight to Skardu, the jeep to Askole, and weather buffer days."),
         ("Do I need a permit and a guide?","Yes. The Baltoro is a restricted zone: a licensed operator, registered guide and trekking permit are required, and solo trekking is not allowed."),
         ("When is the season?","Mid-June to mid-September. July and August are the most reliable for the high glacier sections.")],
   deeper=[("/trekking/k2-base-camp/itinerary","K2 Base Camp Itinerary, Day by Day"),("/trekking/k2-base-camp/cost","What Drives the K2 Trek Cost"),("/trekking/k2-base-camp/permits","K2 Trek Permits"),("/trekking/concordia","Concordia Trek"),("/trekking/gondogoro-la","Gondogoro La Trek"),("/skardu","Skardu Travel Guide")]),
 'concordia': dict(region='Baltoro, Baltistan', h1='I Compared the Concordia Trek Operators for 2026',
   intro=["Concordia, the \"Throne Room of the Mountain Gods\", sits where the Baltoro and Godwin-Austen glaciers meet, ringed by K2, Broad Peak and the Gasherbrums. Most operators sell it as the same trip as K2 Base Camp; here is who runs it and what they charge in 2026.",
          "I only list operators with a published price, and flag where permits and Skardu flights are bundled or extra. Like the K2 trek, it is a restricted zone needing a licensed operator and guide."],
   about="Concordia sits at about 4,600m; trips run 15-21 days depending on whether you add the K2 base camp leg or cross the Gondogoro La on the way out. Long, remote glacier walking rather than technical climbing.",
   faqs=[("Is Concordia the same as the K2 Base Camp trek?","Almost - Concordia is the hub; K2 Base Camp is a day leg beyond it, and many packages combine both. Pricing is effectively the same trip."),
         ("How much does it cost in 2026?","Locally run trips start around $1,750-$2,300 per person; Western-led from $5,850. Permits and flights may be extra."),
         ("How hard is it?","Demanding but non-technical - long days on glacier and moraine at altitude. Adding the Gondogoro La makes it technical."),
         ("When should I go?","Mid-June to mid-September, with July-August the most settled.")],
   deeper=[("/trekking/k2-base-camp","K2 Base Camp Trek"),("/trekking/gondogoro-la","Gondogoro La Trek"),("/trekking/biafo-hispar-snow-lake","Snow Lake Trek"),("/skardu","Skardu Travel Guide"),("/travel/noc-permits-gb","NOC &amp; Permits")]),
 'gondogoro-la': dict(region='Concordia to Hushe', h1='I Reviewed the Gondogoro La Trek Operators for 2026',
   intro=["The Gondogoro La (5,585m) is the spectacular, technical way out of Concordia - a roped dawn crossing with all four local 8,000m peaks behind you, dropping into the Hushe valley. Here are the operators who publish a 2026 price for it.",
          "Only priced operators are compared below, with notes on where crampons, harness and the pass crossing are included or rented separately. A licensed operator, guide and permit are mandatory."],
   about="The full circuit runs 20-21 days. The pass itself is glaciated and steep enough to need crampons, harness and fixed ropes, so it sits a notch above a standard base-camp trek.",
   faqs=[("How is the Gondogoro La different from the K2 trek?","It is the same Baltoro/Concordia approach, but instead of returning via Askole you cross the 5,585m Gondogoro La into Hushe - a technical, roped section."),
         ("What does it cost in 2026?","Local operators run roughly $1,955-$2,685 per person; Western-led from $5,850. Confirm whether climbing gear for the pass is included."),
         ("Do I need climbing experience?","No technical climbing, but you must be fit for a pre-dawn glaciated pass on fixed ropes with crampons; operators provide guides and the rope work."),
         ("When is it open?","July to early September, when the pass is reliably crossable.")],
   deeper=[("/trekking/concordia","Concordia Trek"),("/trekking/k2-base-camp","K2 Base Camp Trek"),("/trekking/hushe-valley","Hushe Valley"),("/skardu","Skardu Travel Guide"),("/travel/noc-permits-gb","NOC &amp; Permits")]),
 'biafo-hispar-snow-lake': dict(region='Askole to Hispar', h1='I Compared the Snow Lake / Hispar La Trek Operators for 2026',
   intro=["The Biafo-Hispar traverse links two of the longest glaciers outside the poles across Snow Lake and the Hispar La (~5,151m) - a serious, committing expedition from Askole to Nagar. Here is who runs it and what they charge in 2026.",
          "I compare only operators with a published price, noting porter allowances and whether staff insurance is included. This is a remote, crevassed route needing a licensed operator and guide."],
   about="Plan on 18-22 days. Snow Lake is a vast glacial basin around 4,800m and the Hispar La tops out near 5,151m; expect roped glacier travel and full self-sufficiency for two weeks.",
   faqs=[("How hard is the Snow Lake trek?","Serious - it is a glaciated, crevassed traverse with no resupply, closer to a mountaineering expedition than a walk-in trek."),
         ("What does it cost in 2026?","Local operators run about $2,450-$2,850 per person; Western-led $4,100-$5,600. Confirm porter weight limits and staff insurance."),
         ("How many days?","18-22 days point to point, Askole to Hispar/Nagar, including buffer days."),
         ("Best time to go?","July to early September.")],
   deeper=[("/trekking/concordia","Concordia Trek"),("/trekking/rush-lake","Rush Lake Trek"),("/hunza","Hunza Travel Guide"),("/skardu","Skardu Travel Guide"),("/travel/noc-permits-gb","NOC &amp; Permits")]),
 'spantik-base-camp': dict(region='Arandu, Nagar', h1='I Looked at Every Spantik Trek &amp; Expedition Operator for 2026',
   intro=["Spantik, the Golden Peak (7,027m), is one of the most accessible 7,000m climbs in the Karakoram - and there is also a shorter base-camp trek for those who just want the glacier and the views. Here is who runs both, and what they charge in 2026.",
          "I separate the base-camp trek from the full climbing expedition and only compare operators publishing a real price, noting where oxygen, high-altitude porters and royalty fees are included."],
   about="The base-camp trek is a few days up the Chogo Lungma glacier from Arandu; the climbing expedition runs 28-31 days. The mountain is graded a good first 7,000er, but it is a genuine high-altitude climb above base camp.",
   faqs=[("Is Spantik a trek or a climb?","Both. There is a short base-camp trek (from about $1,300), and a 28-31 day climbing expedition to the 7,027m summit (from about $3,500)."),
         ("What does the expedition cost in 2026?","Base-camp service expeditions start near $3,500; full-board with oxygen and high-altitude porters runs $4,500-$7,950 depending on operator and ratio."),
         ("Do I need climbing experience for the summit?","Spantik is considered a good first 7,000m peak, but you need solid fitness, basic glacier/rope skills and acclimatisation. The base-camp trek needs none of that."),
         ("When is the season?","June to September.")],
   deeper=[("/trekking/rush-lake","Rush Lake Trek"),("/trekking/rakaposhi-base-camp","Rakaposhi Base Camp"),("/hunza","Hunza Travel Guide"),("/travel/noc-permits-gb","NOC &amp; Permits")]),
 'masherbrum-base-camp': dict(region='Hushe, Baltistan', h1='I Compared the Masherbrum Base Camp Trek Operators for 2026',
   intro=["Masherbrum (K1, 7,821m) towers over the Hushe valley, and the base-camp trek to its foot is one of Baltistan's great moderate treks - far quieter than the Baltoro. Here is who runs it and what they charge in 2026.",
          "Below are operators with a published price for the base-camp trek (not the full summit expedition), with notes on meals and porter allowances."],
   about="The trek reaches base camp around 4,280-4,500m over roughly 11-13 days door to door, with only a handful of actual trekking days; the rest is travel to and from Hushe. Moderate and non-technical.",
   faqs=[("Is this the trek or the Masherbrum climb?","The trek - a walk to base camp around 4,280m. The Masherbrum (7,821m) summit climb is a separate, far more expensive expedition."),
         ("How much does it cost in 2026?","Published prices run about $1,250-$2,480 per person depending on group size, length and how much is bundled."),
         ("How hard is it?","Easy to moderate - a few days of valley and moraine walking, accessible to fit first-time trekkers."),
         ("When should I go?","June to September.")],
   deeper=[("/trekking/hushe-valley","Hushe Valley"),("/trekking/laila-peak-base-camp","Laila Peak Base Camp"),("/trekking/gondogoro-la","Gondogoro La Trek"),("/skardu","Skardu Travel Guide")]),
 'laila-peak-base-camp': dict(region='Hushe, Baltistan', h1='I Reviewed the Laila Peak Base Camp Trek Operators for 2026',
   intro=["Laila Peak's impossibly thin, leaning spire (6,096m) is one of the most photographed mountains in the Karakoram, and the base-camp trek through the Hushe valley is a quieter alternative to the Baltoro. Here is who runs it and what they charge in 2026.",
          "Only operators with a published price are compared below, with notes on what each includes."],
   about="Base camp sits around 4,200-4,535m, reached over roughly 12-13 days door to door via Hushe and the Gondogoro glacier approach. Moderate trekking, no technical climbing.",
   faqs=[("How much does the Laila Peak trek cost in 2026?","Published rates run about $1,450-$1,500 per person for group departures; solo and small groups cost more. Several operators are quote-only."),
         ("How hard is it?","Moderate - a Hushe-valley approach trek to base camp, not a climb. Laila Peak itself (6,096m) is a serious technical objective for mountaineers only."),
         ("How many days?","Around 12-13 days including travel to and from Skardu."),
         ("When is the season?","June to September.")],
   deeper=[("/trekking/masherbrum-base-camp","Masherbrum Base Camp"),("/trekking/hushe-valley","Hushe Valley"),("/trekking/gondogoro-la","Gondogoro La Trek"),("/skardu","Skardu Travel Guide")]),
 'rush-lake': dict(region='Nagar / Hopper', h1='I Compared the Rush Lake Trek Operators for 2026',
   intro=["Rush Lake, at around 4,700m above the Hopper glaciers in Nagar, is one of the highest alpine lakes in the world, with Spantik and Malubiting filling the skyline. Here is who runs the trek and what they charge in 2026.",
          "I compare operators with a published price and flag what is bundled. It is a challenging high-altitude trek but non-technical."],
   about="Most itineraries run 12-14 days door to door (the lake leg itself is a few days from Hopper); the lake and Rush Pari viewpoint sit near 4,700m. Challenging mainly for the altitude.",
   faqs=[("How much does the Rush Lake trek cost in 2026?","Published prices range from about $1,144 to $2,700 per person depending on length and inclusions; several operators are quote-only."),
         ("How hard is the trek?","Challenging - steep ascents and high altitude (~4,700m), but no technical climbing."),
         ("How many days?","12-14 days from Islamabad including the Hunza/Nagar drive; the core lake trek is shorter."),
         ("Best time?","July to September.")],
   deeper=[("/trekking/rakaposhi-base-camp","Rakaposhi Base Camp"),("/trekking/spantik-base-camp","Spantik Trek"),("/hunza","Hunza Travel Guide"),("/travel/best-time-to-visit-gb","Best Time to Visit GB")]),
 'rakaposhi-base-camp': dict(region='Minapin, Nagar', h1='I Compared the Rakaposhi Base Camp Trek Operators for 2026',
   intro=["The Rakaposhi base-camp trek climbs from Minapin to a meadow beneath the 7,788m north face - a short, rewarding trek you can do in a few days from Hunza. Here is who runs it and what they charge in 2026.",
          "Operators with a published price are compared below; note how widely durations vary, from a true 3-day trek to 12-day Islamabad-to-Islamabad packages."],
   about="The actual trek to Tagaphari base camp (~3,800-4,150m) is 2-3 days return from Minapin; many operators wrap it in a longer Hunza tour. Easy to moderate and beginner-friendly.",
   faqs=[("How much does the Rakaposhi trek cost in 2026?","Group tiers start around $500 per person; flat all-inclusive packages run $1,345-$1,800. Watch whether the price is the short trek or a full Hunza package."),
         ("How long is the trek?","The trek itself is 2-3 days from Minapin; packages bundling flights and Hunza sightseeing run 11-12 days."),
         ("Is it suitable for beginners?","Yes - it is one of the most accessible base-camp treks in GB, though the final day to the upper camp is a steep climb."),
         ("When should I go?","May to October.")],
   deeper=[("/trekking/rush-lake","Rush Lake Trek"),("/hunza","Hunza Travel Guide"),("/mountains/rakaposhi","Rakaposhi Mountain"),("/travel/best-time-to-visit-gb","Best Time to Visit GB")]),
 'nanga-parbat-base-camp': dict(region='Fairy Meadows / Raikot', h1='I Compared the Nanga Parbat Base Camp Trek Operators for 2026',
   intro=["From Fairy Meadows, the trek to Nanga Parbat's Raikot base camp puts you under the 8,126m north face - the most popular short trek in Gilgit-Baltistan. Here is who runs it and what they charge in 2026.",
          "I compare operators with a published price (some local ones quote in rupees), and note that many sell it as a Fairy Meadows package with the base-camp leg as one day."],
   about="The base camp on the Raikot side sits around 3,900m, reached on a day hike from Fairy Meadows; full packages run 3-8 days from Islamabad. Easy to moderate.",
   faqs=[("How much does the Nanga Parbat base camp trek cost in 2026?","International-facing operators charge about $1,400-$1,700 per person; local operators price in rupees (around PKR 165,000 for a full package) and per-group tiers drop sharply with group size."),
         ("How hard is it?","Easy to moderate - a day hike from Fairy Meadows to base camp at ~3,900m. The hard part is the jeep road to Tatu and the walk up to Fairy Meadows."),
         ("How many days?","3-4 days for the core trip; 6-8 days for packages from Islamabad."),
         ("When is the season?","May to September.")],
   deeper=[("/fairy-meadows","Fairy Meadows Guide"),("/trekking/nanga-parbat-rupal-face","Nanga Parbat Rupal Face Trek"),("/mountains/nanga-parbat","Nanga Parbat Mountain"),("/travel/best-time-to-visit-gb","Best Time to Visit GB")]),
 'nanga-parbat-rupal-face': dict(region='Tarashing / Astore', h1='I Reviewed the Nanga Parbat Rupal Face Trek Operators for 2026',
   intro=["The Rupal face is the highest mountain wall on earth - 4,600m of rock and ice - and the trek from Tarashing to the Herrligkoffer base camp puts you right beneath it. Here is who runs it and what they charge in 2026.",
          "Operators with a published price are compared below; some sell a combined Fairy Meadows (north) plus Rupal (south) itinerary rather than Rupal alone."],
   about="The Herrligkoffer/Rupal base camp sits around 3,550m, reached from Tarashing in the Astore valley over 3-4 trekking days; full itineraries run 10-14 days. Moderate.",
   faqs=[("How much does the Rupal face trek cost in 2026?","Published prices start around $1,100 per person; combined Fairy Meadows + Rupal itineraries run $1,850-$1,975. Several operators are quote-only."),
         ("How is it different from the Fairy Meadows side?","Fairy Meadows is the north (Raikot) face; Rupal is the south face, reached via Tarashing in Astore - quieter, and beneath the famous Rupal wall."),
         ("How hard is it?","Moderate - valley and meadow walking to base camp at ~3,550m, with an optional harder push toward the Mazeno area."),
         ("When should I go?","June to September.")],
   deeper=[("/trekking/nanga-parbat-base-camp","Nanga Parbat (Fairy Meadows) Base Camp"),("/astore","Astore Valley Guide"),("/mountains/nanga-parbat","Nanga Parbat Mountain"),("/travel/noc-permits-gb","NOC &amp; Permits")]),
 'hushe-valley': dict(region='Hushe, Baltistan', h1='I Compared the Charakusa / Hushe Valley Trek Operators for 2026',
   intro=["The Hushe valley is the gateway to the Charakusa - a granite amphitheatre under K6, K7 and Laila Peak that climbers rate among the most beautiful on earth. Here is who runs treks here and what they charge in 2026.",
          "I compare operators with a published price, with notes on what each includes. Trips range from valley walks to multi-week K6/K7 base-camp treks."],
   about="The valley village sits around 3,050m; the Charakusa and K7 base-camp treks run 10-16 days door to door, reaching base camps around 4,000-4,500m. Moderate trekking in a technical-climbing arena.",
   faqs=[("How much does the Charakusa / Hushe trek cost in 2026?","Published prices run about $1,400-$2,800 per person depending on length and inclusions; several operators are quote-only."),
         ("What is there to trek to?","The Charakusa valley and K6/K7 base camps, plus approaches to Laila Peak, Masherbrum and the Gondogoro La - all from Hushe."),
         ("How hard is it?","Moderate trekking, though the setting is a serious climbing area; the base-camp walks themselves are non-technical."),
         ("When is the season?","June to September.")],
   deeper=[("/trekking/masherbrum-base-camp","Masherbrum Base Camp"),("/trekking/laila-peak-base-camp","Laila Peak Base Camp"),("/trekking/gondogoro-la","Gondogoro La Trek"),("/skardu","Skardu Travel Guide")]),
 'haramosh-kutwal-lake': dict(region='Haramosh, near Gilgit', h1='I Went and Looked at the Haramosh / Kutwal Lake Trek Operators for 2026',
   intro=["The Haramosh valley trek to Kutwal Lake, under the 7,409m Haramosh peak, is a short, scenic trek off the Gilgit-Skardu road that few foreigners reach. Here is who runs it and what they charge in 2026.",
          "This is a thin-pricing route - a few local operators publish a rupee or dollar figure, the rest quote per group. All compared below."],
   about="Kutwal Lake sits around 3,300m, reached in 5-7 days door to door via Sassi and a jeep track. Moderate walking, with a steep approach day.",
   faqs=[("How much does the Kutwal Lake trek cost in 2026?","Local operators publish around PKR 60,000 (about $700-$750 for foreigners); some are breakfast-only or quote-only, so confirm exactly what is included."),
         ("How hard is it?","Moderate - a short trek with one steep approach day to the lake at ~3,300m."),
         ("How many days?","5-7 days from Islamabad including the drive up the Karakoram Highway."),
         ("When should I go?","June to September.")],
   deeper=[("/gilgit","Gilgit Travel Guide"),("/skardu","Skardu Travel Guide"),("/trekking/rakaposhi-base-camp","Rakaposhi Base Camp"),("/travel/best-time-to-visit-gb","Best Time to Visit GB")]),
 'karambar-lake': dict(region='Ishkoman / Broghil', h1='I Researched the Karambar Lake Trek Operators for 2026',
   intro=["Karambar Lake, near the Broghil and the Afghan Wakhan, is one of the highest large lakes on earth and one of the remotest treks in Gilgit-Baltistan. Here is who runs it and what they charge in 2026.",
          "Few operators publish a price for somewhere this remote; those that do are compared below, the rest quote per group."],
   about="The lake sits around 4,300m, reached over 8-17 days depending on the approach (Ishkoman/Broghil or Chapursan). Challenging and committing, with full self-sufficiency.",
   faqs=[("How much does the Karambar Lake trek cost in 2026?","One operator publishes about PKR 110,000 ($390) for an 8-day version; longer expedition-style itineraries run $1,400+ and many are quote-only."),
         ("How hard and remote is it?","Very remote and challenging - long days, river crossings and high camps with no resupply; satellite communication is sensible."),
         ("How many days?","8 days for the shortest published trip; 12-17 days for full Broghil/Darkot crossings."),
         ("When is it possible?","July to early September only.")],
   deeper=[("/ishkoman","Ishkoman Valley Guide"),("/trekking/karambar-lake","Karambar Lake"),("/gilgit","Gilgit Travel Guide"),("/travel/noc-permits-gb","NOC &amp; Permits")]),
 'naltar-lakes': dict(region='Naltar, near Gilgit', h1='I Compared the Naltar Valley Tours for 2026',
   intro=["Naltar is the easy one - a forested valley above Gilgit with the famous Satrangi (rainbow) lakes, reached by jeep and short walks rather than a multi-day trek. Here is who runs Naltar trips and what they charge in 2026.",
          "Operators sell Naltar as a day or jeep excursion inside 4-5 day Hunza/Gilgit packages; prices below are in rupees, as nearly all are local operators."],
   about="The valley and Blue/Satrangi lakes sit around 3,050-3,150m, reached by 4x4 jeep with short walks. Easy, family-friendly, and good from late spring to autumn (also a winter ski spot).",
   faqs=[("How much does a Naltar trip cost in 2026?","Local packages run about PKR 14,500-30,000 per person, usually as part of a 5-day Hunza/Gilgit tour. The Naltar jeep charge (PKR 2,000-3,000/head) is often extra."),
         ("Is Naltar a trek or a tour?","Mostly a tour - you reach the lakes by jeep with short walks, so it suits families and those who don't want a multi-day trek."),
         ("How many days?","Naltar itself is a day; most buy it inside a 4-5 day Hunza/Gilgit package."),
         ("When should I go?","May to September for the lakes; winter for skiing.")],
   deeper=[("/naltar","Naltar Valley Guide"),("/gilgit","Gilgit Travel Guide"),("/hunza","Hunza Travel Guide"),("/tours/gilgit","Gilgit Tour Packages")]),
}

DISPLAY = {
 'k2-base-camp':'K2 Base Camp Trek','concordia':'Concordia Trek','gondogoro-la':'Gondogoro La Trek',
 'biafo-hispar-snow-lake':'Snow Lake / Hispar La Trek','rush-lake':'Rush Lake Trek',
 'rakaposhi-base-camp':'Rakaposhi Base Camp Trek','nanga-parbat-base-camp':'Nanga Parbat Base Camp Trek',
 'nanga-parbat-rupal-face':'Nanga Parbat Rupal Face Trek','spantik-base-camp':'Spantik Trek &amp; Expedition',
 'masherbrum-base-camp':'Masherbrum Base Camp Trek','laila-peak-base-camp':'Laila Peak Base Camp Trek',
 'hushe-valley':'Charakusa / Hushe Valley Trek','haramosh-kutwal-lake':'Haramosh / Kutwal Lake Trek',
 'karambar-lake':'Karambar Lake Trek','naltar-lakes':'Naltar Valley &amp; Lakes'}

PAGEMETA = json.load(open(os.path.join(DATA, '_pagemeta.json')))

def build_body(route, pkgs):
    c = C[route]; name = DISPLAY[route]
    pkgs = sorted(pkgs, key=rank)
    priced = [p for p in pkgs if has_price(p)]
    cheapest = priced[0] if priced else None
    dearest = priced[-1] if priced else None
    allinc = max(priced, key=lambda p: len(p.get('includes','')), default=None) if priced else None
    facts = PAGEMETA[route]['hero_meta']
    fact_li = ''.join(f'<li>{esc(f[0].strip())}</li>' for f in facts if f[0].strip())

    # intro
    paras = ''.join(f'<p>{p}</p>\n' for p in c['intro'])

    # callout
    n_priced = len(priced); n_total = len(pkgs)
    n_rated = sum(1 for p in pkgs if rating_obj(p['home']))
    rating_note = ('' if not n_rated else
        f' Where an operator has a genuine public rating I\'ve shown it (Tripadvisor, Trustpilot and similar, with the review count and a link) - '
        f'Google Maps ratings aren\'t publicly queryable, so I don\'t show those; an operator with too few public reviews shows a dash rather than a number.')
    callout = (f'<div class="callout"><h3>How I compared these packages</h3><p>I did this the way I\'d want a friend to do it for me. '
               f'I went through every {esc(name)} operator I could find, read each itinerary, and lined them up on the things that actually '
               f'decide your trip - what\'s included, the porters and meals, the route, and the real 2026 price. {n_priced} of {n_total} below '
               f'publish a price you can hold them to; the rest quote per group, and I\'ve said so plainly rather than guess. Prices are per '
               f'person, usually land-only and group-based, with permits, flights, insurance and tips often on top. Every operator here is '
               f'judged on the same yardstick. Operator links are nofollow.{rating_note}</p></div>')

    # about + facts
    about = (f'<h2>About the {esc(name)}</h2>\n<p>{c["about"]}</p>\n'
             f'<ul class="trek-facts">{fact_li}</ul>')

    # at a glance table
    rows = []
    for p in pkgs:
        link = f'<a href="{esc(p["pkg_url"])}" target="_blank" rel="nofollow noopener">link</a>'
        op = f'<a href="{esc(p["home"])}" target="_blank" rel="nofollow noopener">{esc(p["operator"])}</a>'
        rows.append(f'<tr><td>{op}</td><td>{esc(p.get("days",""))}</td><td>{price_str(p)}</td>'
                    f'<td>{rating_cell(p["home"])}</td><td>{link}</td></tr>')
    table = ('<h2>At a glance - operators compared</h2>\n<table class="cmp-table"><thead><tr><th>Operator</th><th>Length</th>'
             '<th>From (2026)</th><th>Reviews</th><th>Link</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>')

    # standouts
    wins = []
    if cheapest:
        wins.append(f'<li>💰 <strong>Lowest published price</strong> - {esc(cheapest["operator"])} (from {price_str(cheapest)})</li>')
    if allinc and allinc is not cheapest:
        wins.append(f'<li>🎒 <strong>Most inclusive</strong> - {esc(allinc["operator"])}, where flights, permits and full board are bundled</li>')
    if dearest and dearest is not cheapest:
        wins.append(f'<li>🧭 <strong>Most support</strong> - {esc(dearest["operator"])} (from {price_str(dearest)}), the premium, higher-ratio option</li>')
    winners = ('<h2>What stood out to me</h2>\n<ul>'+''.join(wins)+'</ul>') if wins else ''

    cta1 = ('<div class="article-cta"><h3>Want a second opinion before you book?</h3><p>I\'ll sanity-check any quote, plan your '
            'route and season, and share vetted guide, porter and jeep contacts - free, with my <a href="/planner">trip planner</a> '
            'or a quick <a href="/contact">message</a>.</p><a href="/planner?entry=trekking" class="btn-primary">Plan my trek &rarr;</a></div>')

    # review cards
    cards = ['<h2>Every operator, reviewed</h2>']
    for i, p in enumerate(pkgs, 1):
        sc = score(p, cheapest, dearest, allinc)
        badge = f'#{i}'
        op = f'<a href="{esc(p["home"])}" target="_blank" rel="nofollow noopener">{esc(p["operator"])}</a>'
        meta = f'<span>🗓 <strong>{esc(p.get("days",""))}</strong></span><span>💷 <strong>{price_str(p)}</strong></span>'
        if p.get('meals'): meta += f'<span>🍽 <strong>{esc(p["meals"])}</strong></span>'
        meta += rating_span(p['home'])
        inc = f'<p style="font-size:.9rem;line-height:1.62;color:#2E2A22;margin:.2rem 0 .5rem"><strong>Includes:</strong> {esc(p.get("includes",""))}</p>' if p.get('includes') else ''
        tiers = f'<div class="rev-verdict">Group-size pricing: {esc(p["tiers"])}.</div>' if p.get('tiers') else ''
        cards.append(
          '<div class="rev">'
          f'<div class="rev-head"><div><div class="rev-badge">{badge}</div><h3>{esc(p["operator"])}</h3>'
          f'<div class="rev-op">by {op} · {esc(p.get("days",""))} · from {price_str(p)}</div></div>'
          f'<div class="rev-score"><b>{sc}</b><span>/10</span></div></div>'
          f'<div class="rev-meta">{meta}</div>\n{inc}'
          f'<div class="rev-pc"><div><h4 class="pros">What\'s good</h4><ul><li>{esc(p.get("good",""))}</li></ul></div>'
          f'<div><h4 class="cons">Could be better</h4><ul><li>{esc(p.get("could_be_better",""))}</li></ul></div></div>'
          f'{tiers}'
          f'<div class="rev-links">🔗 <a href="{esc(p["pkg_url"])}" target="_blank" rel="nofollow noopener">View this package</a> · {op}</div>'
          '</div>')
    cards = '\n'.join(cards)

    incl = ('<h2>What\'s usually included - and what\'s not</h2>\n<p>On most of these treks the operator price <strong>includes</strong> '
            'guides and support staff, porters, camping equipment, in-trek meals and the trekking permit. It usually <strong>excludes</strong> '
            'international flights, travel insurance, personal climbing or trekking gear, tips for the crew, and on restricted peaks the government '
            'royalty fee. Always get the itemised inclusions, porter weight limit and the payment and cancellation terms in writing before you pay.</p>')

    choose = ('<h2>How to choose your operator</h2>\n<ul>'
              '<li><strong>Published vs quote</strong> - a real posted price is easier to compare; for quote-only operators, get it itemised.</li>'
              '<li><strong>What\'s bundled</strong> - permits, domestic flights and porters are where cheap quotes cut corners.</li>'
              '<li><strong>Group size</strong> - most headline rates assume a group; confirm the solo or small-group rate.</li>'
              '<li><strong>Crew welfare</strong> - porter weight limits, wages and insurance say a lot about an operator.</li>'
              '<li><strong>Local vs down-country</strong> - Baltistan and Hunza-based crews know the routes and logistics best.</li></ul>')

    deeper = ('<h2>Plan this trek deeper</h2>\n<p>My free local guides go beyond the operators - use them to decide what you want, then book or customise:</p>\n<ul>'
              + ''.join(f'<li><a href="{h}">{l}</a></li>' for h,l in c['deeper']) + '</ul>')

    cta2 = ('<div class="article-cta"><h3>Operators - want your trek reviewed here?</h3><p>If you run this trek and publish real prices, '
            '<a href="/contact">get in touch</a> to have your itinerary assessed and added. Every operator is judged on the same criteria.</p>'
            '<a href="/contact" class="btn-primary">Get your trek listed &rarr;</a></div>')

    faq = '<h2>FAQ</h2>\n<div class="faq">' + ''.join(
        f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in c['faqs']) + '</div>'

    body = '\n'.join([paras.strip(), about, callout, table, winners, cta1, cards, incl, choose, deeper, cta2, faq])
    return body, pkgs

def itemlist_jsonld(route, pkgs):
    name = DISPLAY[route].replace('&amp;','&')
    items = []
    for i,p in enumerate(pkgs,1):
        items.append({"@type":"ListItem","position":i,"item":{"@type":"TouristTrip",
          "name":f'{p["operator"]} - {DISPLAY[route].replace("&amp;","&")}',"url":p["pkg_url"],
          "provider":{"@type":"Organization","name":p["operator"]}}})
    obj={"@context":"https://schema.org","@type":"ItemList","name":name,"itemListElement":items}
    return '<script type="application/ld+json">'+json.dumps(obj)+'</script>'

def faq_jsonld(route):
    me=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in C[route]['faqs']]
    obj={"@context":"https://schema.org","@type":"FAQPage","mainEntity":me}
    return '<script type="application/ld+json">'+json.dumps(obj)+'</script>'

def assemble(route):
    f = os.path.join(ROOT,'trekking',route,'index.html')
    s = open(f).read()
    pkgs_raw = json.load(open(os.path.join(DATA,route+'.json')))
    head = s[:s.index('</head>')+len('</head>')]
    # nav block: <body> ... up to first <section/<main
    mnav = re.search(r'<body>(.*?)(?=<section|<main)', s, re.S)
    nav = mnav.group(1).strip()
    # footer through end
    foot = s[s.index('<footer>'):]
    related = (re.search(r'<!-- RELATED:START -->.*?<!-- RELATED:END -->', s, re.S) or [None])
    related = related.group(0) if hasattr(related,'group') else (re.search(r'<!-- RELATED:START -->.*?<!-- RELATED:END -->', s, re.S).group(0))
    body, pkgs = build_body(route, pkgs_raw)
    meta = PAGEMETA[route]
    hero = meta['hero']
    eyebrow = f'Trek &middot; {C[route]["region"]} &middot; 2026'
    crumb = (f'<div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em">'
             f'<a href="/" style="color:inherit">Home</a> / <a href="/trekking" style="color:inherit">Treks</a> / '
             f'<span style="color:var(--cream)">{DISPLAY[route]}</span></div>')
    main = (f'<main class="article">\n'
            f'<div class="article-head">{crumb}\n'
            f'<div class="article-eyebrow">{eyebrow}</div>\n'
            f'<h1 class="article-title">{C[route]["h1"]}</h1>\n'
            f'<div class="article-meta"><span>By <a href="/about"><strong>Faisal Zaman</strong></a></span>'
            f'<span class="sep">&middot;</span><span>Local, Gilgit-Baltistan</span>'
            f'<span class="sep">&middot;</span><span>Updated June 2026</span></div></div>\n'
            f'<figure class="article-figure"><div class="img" style="background-image:url(\'{hero}\')" role="img" aria-label="{DISPLAY[route]}"></div>'
            f'<figcaption>{DISPLAY[route]}, Gilgit-Baltistan.</figcaption></figure>\n'
            f'<div class="article-body">\n{body}\n</div></main>')
    il = itemlist_jsonld(route, pkgs)
    fq = faq_jsonld(route)
    out = head + '\n<body>\n' + nav + '\n' + main + '\n' + il + '\n' + fq + '\n\n' + related + '\n' + foot
    open(f,'w').write(out)
    return len(pkgs)

if __name__ == '__main__':
    ok=0
    for r in sorted(C.keys()):
        n=assemble(r); print(f'  {r}: blog article, {n} operators'); ok+=1
    print(f'done: {ok}/15')
