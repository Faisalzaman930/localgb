#!/usr/bin/env python3
"""Rebuild the town restaurant pages (skardu/restaurants, hunza/food,
gilgit/restaurants) as 'N Best Restaurants in <Town> 2026' blog articles from
research/restaurants/<town>.json. Reuses each page's head/nav/footer/related.
Run: python3 research/build_restaurants.py  (then seo_inject.py)"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'research', 'restaurants')

def esc(s):
    if s is None: return ''
    return re.sub(r'&(?!amp;|lt;|gt;|#\d+;|quot;)', '&amp;', str(s))

import urllib.parse
def gmaps(name, town): return "https://www.google.com/maps/search/?api=1&query="+urllib.parse.quote(f"{name} {town}")

TOWNS = {
 'skardu': dict(
   path='skardu/restaurants', town='Skardu', hero='/images/skardu-hero.webp',
   h1="I Ate Around Skardu to Find Its Best Restaurants for 2026",
   crumb_parent=('/skardu','Skardu'),
   intro=["Skardu's food is its own quiet pleasure: fresh trout from the rivers, slow-cooked Balti karahi, apricot-sweet desserts, and a handful of cafes with a Shangri-La view. I'm from Gilgit-Baltistan, so here is the honest list of where to actually eat in 2026, not a copy-paste of the same three names.",
          "I've ranked real, currently-open places on the food, the setting, value and consistency, and shown each one's real rating where it has a public one."],
   food_h="What to eat in Skardu",
   food=["<strong>Trout</strong> - river or farmed, usually grilled or fried; the regional signature.",
         "<strong>Balti karahi</strong> and <strong>mamtu</strong> (steamed dumplings), <strong>prapu</strong> and <strong>balay</strong> (buckwheat noodles).",
         "<strong>Apricot</strong> everything - oil, jam, dried fruit and the famous apricot-kernel desserts.",
         "<strong>Organic, slow food</strong> - Skardu cooks for taste, not speed; order ahead for trout or karahi."],
   faqs=[("What food is Skardu famous for?","Fresh trout, Balti karahi, steamed mamtu dumplings, buckwheat prapu/balay, and apricot-based sweets. Most of it is organic and cooked slowly, so order ahead."),
         ("Where do tourists eat in Skardu?","Around the main bazaar and the Satpara/Kachura road, plus the view cafes and hotel restaurants. See the ranked list above."),
         ("Is Skardu good for vegetarians?","Yes - daal, seasonal vegetables, naan and rice are everywhere, though trout and karahi are the highlights. Tell the cook in advance for the best vegetarian spread."),
         ("How much does a meal cost in Skardu?","A simple local meal runs a few hundred rupees; trout and full karahi at a mid-range place cost more. Prices are marked $ (budget) to $$$ (upscale) in the table.")],
   deeper=[("/skardu","Skardu Travel Guide"),("/skardu/hotels","Where to Stay in Skardu"),("/skardu/tourist-places","Places to Visit in Skardu"),("/tours/skardu","Skardu Tour Packages")]),
 'hunza': dict(
   path='hunza/food', town='Hunza', hero='/images/hunza-hero.webp',
   h1="I Ate My Way Around Hunza - the Best Restaurants for 2026",
   crumb_parent=('/hunza','Hunza'),
   intro=["Hunza is one of the most rewarding places to eat in Pakistan: organic Hunzai dishes you won't find elsewhere, apricot and walnut everything, and cafes terraced above Karimabad with Rakaposhi filling the window. I'm from Hunza, so this is the real ranked list for 2026.",
          "I judged each place on the food, the view and setting, value and consistency, and listed its real public rating where it has one."],
   food_h="What to eat in Hunza",
   food=["<strong>Chapshuro</strong> - the Hunza meat-filled pastry, the one dish to not miss.",
         "<strong>Harissa</strong>, <strong>diram fitti</strong> (sweet sprouted-wheat bread) and <strong>hoi garma</strong> - traditional Hunzai comfort food.",
         "<strong>Apricot &amp; walnut</strong> - apricot soup, oil, cakes, and walnut cake at the view cafes.",
         "<strong>Tumuro (mountain thyme) chai</strong> and Hunza water - the local drinks to try."],
   faqs=[("What food is Hunza famous for?","Chapshuro (meat pastry), harissa, diram fitti, apricot soup and cakes, walnut cake, and tumuro herbal tea. The food is largely organic and local."),
         ("Where are the best cafes in Karimabad?","The terraced view cafes above Karimabad bazaar - several look straight at Rakaposhi. The ranked list above covers the best for food and for view."),
         ("Can you get traditional Hunzai food in restaurants?","Yes - several places do a Hunzai set or platter (chapshuro, harissa, local breads). A few need a little notice for the full traditional spread."),
         ("How much does eating in Hunza cost?","Chapshuro and cafe plates are inexpensive; a full sit-down meal with a view costs more. The table marks each place $ to $$$.")],
   deeper=[("/hunza","Hunza Travel Guide"),("/hunza/karimabad","Karimabad Guide"),("/hunza/hotels","Where to Stay in Hunza"),("/tours/hunza","Hunza Tour Packages")]),
 'gilgit': dict(
   path='gilgit/restaurants', town='Gilgit', hero='/images/gilgit-hero.webp',
   h1="I Tried Gilgit's Restaurants - Here Are the Best for 2026",
   crumb_parent=('/gilgit','Gilgit'),
   intro=["Gilgit is where most GB trips begin or end, and it has the region's broadest spread of food: river trout, hearty Pakistani karahi and BBQ, Hunzai and Shina local dishes, and the chai dhabbas locals actually use. Here is the honest ranked list for 2026.",
          "I ranked real, open places on food, value, setting and consistency, and shown each one's real public rating where it has one."],
   food_h="What to eat in Gilgit",
   food=["<strong>Trout</strong> - Gilgit and its rivers are trout country; grilled is best.",
         "<strong>Karahi &amp; BBQ</strong> - the city does a strong chicken/mutton karahi and tikka.",
         "<strong>Shina &amp; Hunzai local food</strong> - daal, local breads, chapshuro and seasonal vegetables.",
         "<strong>Chai dhabbas</strong> - roadside tea stops for doodh-patti and parathas, a Gilgit ritual."],
   faqs=[("What food is Gilgit famous for?","River trout, chicken and mutton karahi, BBQ/tikka, Shina and Hunzai local dishes, and strong roadside chai. It is the most varied food scene in Gilgit-Baltistan."),
         ("Where do tourists eat in Gilgit?","Along Airport Road, Jutial and the main bazaar, plus hotel restaurants and the trout spots. See the ranked list above."),
         ("Is Gilgit good for a quick or budget meal?","Very - karahi houses, BBQ stalls and chai dhabbas are cheap and quick. Budget places are marked $ in the table."),
         ("How much does a meal cost in Gilgit?","Street and dhabba food is very cheap; a trout or full karahi dinner at a mid-range restaurant costs more. The table marks each place $ to $$$.")],
   deeper=[("/gilgit","Gilgit Travel Guide"),("/gilgit/hotels","Where to Stay in Gilgit"),("/gilgit/places-to-visit","Places to Visit in Gilgit"),("/tours/gilgit","Gilgit Tour Packages")]),
}

def rrank(r):
    return (r.get('rating') or 0, r.get('reviews') or 0)

def rating_cell(r, town):
    if not r.get('rating'):
        return '<span style="color:var(--cream-2)">&mdash;</span>'
    src = r.get('rating_src') or 'Google'
    rv = f' ({r["reviews"]})' if r.get('reviews') else ''
    return (f'<a href="{gmaps(r["name"], town)}" target="_blank" rel="nofollow noopener" style="white-space:nowrap">'
            f'{float(r["rating"]):.1f} &#9733; <span style="color:var(--cream-2)">{esc(src)}{rv}</span></a>')

def rating_chip(r, town):
    if not r.get('rating'): return ''
    src = r.get('rating_src') or 'Google'
    rv = f' ({r["reviews"]})' if r.get('reviews') else ''
    return (f'<span>&#9733; <strong>{float(r["rating"]):.1f}</strong> '
            f'<a href="{gmaps(r["name"], town)}" target="_blank" rel="nofollow noopener">{esc(src)}{rv}</a></span>')

def build_body(key, rests):
    c = TOWNS[key]; town = c['town']
    rests = sorted(rests, key=rrank, reverse=True)
    n = len(rests)
    paras = ''.join(f'<p>{p}</p>\n' for p in c['intro'])
    n_rated = sum(1 for r in rests if r.get('rating'))
    callout = (f'<div class="callout"><h3>How I picked these {town} restaurants</h3><p>I went through the places that are '
               f'actually open and worth your time in {town}, judging each on the food, the setting, value and consistency rather '
               f'than hype. {n_rated} of {n} have a real public rating, which I show with the review count and a maps link; the rest '
               f'are local spots I rate from experience, shown with a dash rather than an invented score.</p></div>')
    # table
    rows = ''
    for r in rests:
        rows += (f'<tr><td><strong>{esc(r["name"])}</strong></td><td>{esc(r.get("area",""))}</td>'
                 f'<td>{esc(r.get("cuisine",""))}</td><td>{esc(r.get("price",""))}</td>'
                 f'<td>{rating_cell(r, town)}</td></tr>')
    table = ('<h2>At a glance - the best places to eat</h2>\n<table class="cmp-table"><thead><tr><th>Restaurant</th>'
             '<th>Area</th><th>Cuisine</th><th>Price</th><th>Rating</th></tr></thead><tbody>'+rows+'</tbody></table>')
    # standouts
    wins = []
    rated = [r for r in rests if r.get('rating')]
    if rated:
        wins.append(f'<li>🏆 <strong>Highest rated</strong> - {esc(rated[0]["name"])} ({float(rated[0]["rating"]):.1f}★)</li>')
    budget = next((r for r in rests if str(r.get('price','')).strip()=='$'), None)
    if budget: wins.append(f'<li>💰 <strong>Best cheap eat</strong> - {esc(budget["name"])} ({esc(budget.get("must_try",""))})</li>')
    local = next((r for r in rests if re.search(r'hunzai|balti|shina|local|traditional', (r.get("cuisine","")+r.get("must_try","")+ " ".join(r.get("pros",[]))), re.I)), None)
    if local: wins.append(f'<li>🍲 <strong>Best for local food</strong> - {esc(local["name"])} ({esc(local.get("must_try",""))})</li>')
    winners = ('<h2>The standouts</h2>\n<ul>'+''.join(wins)+'</ul>') if wins else ''
    cta1 = ('<div class="article-cta"><h3>Planning your trip?</h3><p>I can build your whole route with my free '
            f'<a href="/planner">trip planner</a>, and point you to the best places to eat, stay and visit around {town} - '
            'just <a href="/contact">message me</a>.</p><a href="/planner" class="btn-primary">Plan my trip &rarr;</a></div>')
    # cards
    cards = [f'<h2>The {n} best, reviewed</h2>']
    for i, r in enumerate(rests, 1):
        meta = ''
        if r.get('area'): meta += f'<span>📍 <strong>{esc(r["area"])}</strong></span>'
        if r.get('cuisine'): meta += f'<span>🍴 <strong>{esc(r["cuisine"])}</strong></span>'
        if r.get('price'): meta += f'<span>💷 <strong>{esc(r["price"])}</strong></span>'
        meta += rating_chip(r, town)
        must = f'<p style="font-size:.9rem;line-height:1.62;color:#2E2A22;margin:.4rem 0 .3rem"><strong>Must try:</strong> {esc(r["must_try"])}</p>' if r.get('must_try') else ''
        pros = r.get('pros') or []
        cons = r.get('cons') or []
        pl = ''.join(f'<li>{esc(x)}</li>' for x in pros)
        cl = ''.join(f'<li>{esc(x)}</li>' for x in cons)
        pc = (f'<div class="rev-pc"><div><h4 class="pros">What\'s good</h4><ul>{pl}</ul></div>'
              f'<div><h4 class="cons">Could be better</h4><ul>{cl}</ul></div></div>') if (pl or cl) else ''
        take = f'<div class="rev-verdict"><strong>My take:</strong> {esc(r["take"])}</div>' if r.get('take') else ''
        cards.append(
          '<div class="rev">'
          f'<div class="rev-head"><div><div class="rev-badge">#{i}</div><h3>{esc(r["name"])}</h3>'
          f'<div class="rev-op">{esc(r.get("cuisine",""))}{(" · "+esc(r.get("area",""))) if r.get("area") else ""}</div></div></div>'
          f'<div class="rev-meta">{meta}</div>\n{must}{pc}{take}'
          '</div>')
    cards = '\n'.join(cards)
    food = (f'<h2>{c["food_h"]}</h2>\n<ul>'+''.join(f'<li>{x}</li>' for x in c['food'])+'</ul>')
    deeper = ('<h2>Plan your trip deeper</h2>\n<ul>'+''.join(f'<li><a href="{h}">{l}</a></li>' for h,l in c['deeper'])+'</ul>')
    faq = '<h2>FAQ</h2>\n<div class="faq">'+''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in c['faqs'])+'</div>'
    return '\n'.join([paras.strip(), callout, table, winners, cta1, cards, food, deeper, faq])

def schema(key, rests):
    c = TOWNS[key]; town = c['town']
    items = []
    for i, r in enumerate(rests, 1):
        # NOTE: no aggregateRating - the visible ratings are third-party (Google/
        # Tripadvisor), which Google's guidelines say must not be marked up as our own.
        it = {"@type":"Restaurant","name":r["name"],"servesCuisine":r.get("cuisine",""),
              "address":{"@type":"PostalAddress","addressLocality":town,"addressRegion":"Gilgit-Baltistan","addressCountry":"PK"}}
        items.append({"@type":"ListItem","position":i,"item":it})
    il = {"@context":"https://schema.org","@type":"ItemList","name":f"Best Restaurants in {town} 2026","itemListElement":items}
    fq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faqs']]}
    return ('<script type="application/ld+json">'+json.dumps(il)+'</script>\n'
            '<script type="application/ld+json">'+json.dumps(fq)+'</script>')

def assemble(key, title):
    c = TOWNS[key]
    f = os.path.join(ROOT, c['path'], 'index.html')
    s = open(f).read()
    rests = json.load(open(os.path.join(DATA, key+'.json')))
    head = s[:s.index('</head>')+len('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', head, count=1, flags=re.S)
    mnav = re.search(r'<body>(.*?)(?=<section|<main)', s, re.S)
    nav = mnav.group(1).strip()
    foot = s[s.index('<footer>'):]
    rel = re.search(r'<!-- RELATED:START -->.*?<!-- RELATED:END -->', s, re.S)
    related = rel.group(0) if rel else ''
    n = len(rests)
    parent = c['crumb_parent']
    crumb = (f'<div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em">'
             f'<a href="/" style="color:inherit">Home</a> / <a href="{parent[0]}" style="color:inherit">{parent[1]}</a> / '
             f'<span style="color:var(--cream)">Restaurants</span></div>')
    main = (f'<main class="article">\n<div class="article-head">{crumb}\n'
            f'<div class="article-eyebrow">Food &amp; Restaurants &middot; {c["town"]} &middot; 2026</div>\n'
            f'<h1 class="article-title">{esc(c["h1"])}</h1>\n'
            f'<div class="article-meta"><span>By <a href="/about"><strong>Faisal Zaman</strong></a></span>'
            f'<span class="sep">&middot;</span><span>Local, Gilgit-Baltistan</span>'
            f'<span class="sep">&middot;</span><span>Updated June 2026</span></div></div>\n'
            f'<figure class="article-figure"><div class="img" style="background-image:url(\'{c["hero"]}\')" role="img" aria-label="{esc(c["town"])} restaurants"></div>'
            f'<figcaption>Where to eat in {esc(c["town"])}, Gilgit-Baltistan.</figcaption></figure>\n'
            f'<div class="article-body">\n{build_body(key, rests)}\n</div></main>')
    out = head + '\n<body>\n' + nav + '\n' + main + '\n' + schema(key, rests) + '\n\n' + related + '\n' + foot
    open(f, 'w').write(out)
    return n

if __name__ == '__main__':
    import json as _j
    for key in TOWNS:
        p = os.path.join(DATA, key+'.json')
        if not os.path.exists(p): print('  skip (no data):', key); continue
        n = len(_j.load(open(p)))
        title = f"{n} Best Restaurants in {TOWNS[key]['town']} 2026 - Reviewed"
        assemble(key, title)
        print(f'  {key}: {n} restaurants -> {title}')
    print('done')
