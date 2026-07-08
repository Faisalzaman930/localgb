#!/usr/bin/env python3
"""Rebuild town hotel pages (skardu/hotels, hunza/hotels, gilgit/hotels) as
'N Best Hotels in <Town> 2026' blog articles from research/hotels/<town>.json.
Reuses each page's head/nav/footer/related. Run then seo_inject.py."""
import json, re, os, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'research', 'hotels')
def esc(s):
    if s is None: return ''
    return re.sub(r'&(?!amp;|lt;|gt;|#\d+;|quot;)', '&amp;', str(s))
def gmaps(name, town, coords=None):
    if coords: return "https://www.google.com/maps/search/?api=1&query="+urllib.parse.quote(str(coords))
    return "https://www.google.com/maps/search/?api=1&query="+urllib.parse.quote(f"{name} {town}")
def applemaps(name, town, coords=None):
    if coords: return f"https://maps.apple.com/?ll={urllib.parse.quote(str(coords))}&q="+urllib.parse.quote(name)
    return "https://maps.apple.com/?q="+urllib.parse.quote(f"{name} {town}")
def map_links(h, town):
    co=h.get('coords'); approx='' if co else ' <span style="color:var(--cream-2);font-size:.9em">(approx.)</span>'
    return (f'<div class="rev-links">📍 <a href="{gmaps(h["name"],town,co)}" target="_blank" rel="nofollow noopener">Google Maps</a> · '
            f'<a href="{applemaps(h["name"],town,co)}" target="_blank" rel="nofollow noopener">Apple Maps</a>{approx}</div>')

TOWNS = {
 'skardu': dict(path='skardu/hotels', town='Skardu', hero='/images/skardu-hero.webp',
   h1="I Checked Out Where to Stay in Skardu - the Best Hotels for 2026",
   crumb_parent=('/skardu','Skardu'),
   intro=["Where you stay in Skardu shapes the trip: a lakeside resort, a town hotel near the bazaar, or a budget guesthouse close to the jeep stands for Deosai and K2. I'm from Gilgit-Baltistan, so here's the honest ranked list for 2026 across every budget.",
          "I've ranked real, open places on location, comfort, value and view, and shown each one's real public rating where it has one."],
   ctx_h="How to choose where to stay in Skardu",
   ctx=["<strong>Town vs lake</strong> - stay in Skardu town for food and transport, or out at Kachura/Shangrila for the view (but you'll drive in).",
        "<strong>Book ahead in season</strong> - July-September and the K2/Deosai window fill fast; rates jump.",
        "<strong>Heating &amp; power</strong> - confirm room heating and backup power for shoulder-season and remote stays.",
        "<strong>Location for jeeps</strong> - if you're doing Deosai, Khaplu or K2, a town base near the jeep stands saves time."],
   faqs=[("Where should I stay in Skardu?","Skardu town if you want food, bazaar and transport on the doorstep; the Kachura/Shangrila lakeside if you want the view and don't mind driving in. See the ranked list above."),
         ("How much is a hotel in Skardu?","Budget guesthouses are cheap; mid-range town hotels are moderate; the lakeside resorts and top hotels are the priciest. Each place is marked $ to $$$."),
         ("Do Skardu hotels have heating and wifi?","The better hotels do, but in shoulder season and at remote/lake properties confirm heating, hot water and backup power before booking."),
         ("When should I book?","For July-September and the Deosai/K2 season, book weeks ahead - the best rooms and rates go early.")],
   deeper=[("/skardu","Skardu Travel Guide"),("/skardu/restaurants","Best Restaurants in Skardu"),("/skardu/tourist-places","Places to Visit in Skardu"),("/tours/skardu","Skardu Tour Packages")]),
 'hunza': dict(path='hunza/hotels', town='Hunza', hero='/images/hunza-hero.webp',
   h1="I Checked Out Where to Stay in Hunza - the Best Hotels for 2026",
   crumb_parent=('/hunza','Hunza'),
   intro=["Hunza has some of the most spectacular places to stay in Pakistan: heritage hotels by Altit and Baltit forts, view hotels terraced above Karimabad facing Rakaposhi, and friendly guesthouses for a fraction of the price. I'm from Hunza, so here's the honest ranked list for 2026.",
          "I've ranked real, open places on view, location, comfort and value, with each one's real public rating where it has one."],
   ctx_h="How to choose where to stay in Hunza",
   ctx=["<strong>Karimabad vs Aliabad</strong> - Karimabad for views, forts and cafes on foot; Aliabad is the busier service town on the highway.",
        "<strong>The view is the point</strong> - pay for a Rakaposhi/valley-facing room; it's why you came.",
        "<strong>Upper Hunza (Gulmit/Passu)</strong> - quieter, dramatic, but fewer services; good for a night near the Cones.",
        "<strong>Book the heritage/view rooms early</strong> - the best Karimabad rooms sell out in spring blossom and autumn."],
   faqs=[("Where should I stay in Hunza?","Karimabad for the views, forts and walkable cafes; Aliabad for highway convenience; Gulmit/Passu for a quiet upper-Hunza night. The ranked list above covers each."),
         ("Which Hunza hotels have the best Rakaposhi views?","The terraced hotels above Karimabad and the heritage properties near the forts have the best valley and Rakaposhi views - noted per hotel above."),
         ("How much is a hotel in Hunza?","Guesthouses are inexpensive; mid-range view hotels are moderate; heritage and luxury properties are the priciest. Marked $ to $$$ in the table."),
         ("When should I book Hunza hotels?","For cherry-blossom (late March-April) and autumn (October), book weeks ahead - those are the busiest, most beautiful windows.")],
   deeper=[("/hunza","Hunza Travel Guide"),("/hunza/karimabad","Karimabad Guide"),("/hunza/food","Best Restaurants in Hunza"),("/tours/hunza","Hunza Tour Packages")]),
 'gilgit': dict(path='gilgit/hotels', town='Gilgit', hero='/images/gilgit-hero.webp',
   h1="I Checked Out Where to Stay in Gilgit - the Best Hotels for 2026",
   crumb_parent=('/gilgit','Gilgit'),
   intro=["Most GB trips pass through Gilgit, and it has the region's widest range of places to stay: a polished luxury hotel, reliable mid-range business hotels near the airport, and cheap, central guesthouses. Here's the honest ranked list for 2026.",
          "I've ranked real, open places on location, comfort, value and quiet, with each one's real public rating where it has one."],
   ctx_h="How to choose where to stay in Gilgit",
   ctx=["<strong>Near the airport</strong> - handy if you're flying in/out on a weather-dependent PIA flight that can shift.",
        "<strong>Jutial &amp; Chinar Bagh</strong> - quieter, greener parts of town for a calmer night.",
        "<strong>It's usually a transit night</strong> - most travellers stay one night either side of Hunza/Skardu, so prioritise location and a good bed over resort features.",
        "<strong>Confirm power &amp; hot water</strong> - load-shedding happens; the better hotels have backup."],
   faqs=[("Where should I stay in Gilgit?","Near the airport if you're flying and want flexibility; Jutial or Chinar Bagh for a quieter, greener stay; the bazaar area for budget and convenience. See the list above."),
         ("Is Gilgit just a transit stop?","For most travellers, yes - a night either side of Hunza or Skardu. So pick for location and a comfortable bed rather than resort extras."),
         ("How much is a hotel in Gilgit?","Budget guesthouses are cheap; mid-range hotels are moderate; the top hotel (Serena) is the priciest. Marked $ to $$$ in the table."),
         ("Do Gilgit hotels have backup power?","The better ones do - useful given occasional load-shedding. Confirm backup power and hot water when you book.")],
   deeper=[("/gilgit","Gilgit Travel Guide"),("/gilgit/restaurants","Best Restaurants in Gilgit"),("/gilgit/places-to-visit","Places to Visit in Gilgit"),("/tours/gilgit","Gilgit Tour Packages")]),
}
def rrank(r): return (r.get('rating') or 0, r.get('reviews') or 0)
def rating_cell(r, town):
    if not r.get('rating'): return '<span style="color:var(--cream-2)">&mdash;</span>'
    src=r.get('rating_src') or 'Google'; rv=f' ({r["reviews"]})' if r.get('reviews') else ''
    ten = src.lower() in ('booking.com','booking','expedia','hotels.com','agoda')
    val = f'{float(r["rating"]):.1f}/10' if ten else f'{float(r["rating"]):.1f} &#9733;'
    return (f'<a href="{gmaps(r["name"],town)}" target="_blank" rel="nofollow noopener" style="white-space:nowrap">'
            f'{val} <span style="color:var(--cream-2)">{esc(src)}{rv}</span></a>')
def rating_chip(r, town):
    if not r.get('rating'): return ''
    src=r.get('rating_src') or 'Google'; rv=f' ({r["reviews"]})' if r.get('reviews') else ''
    ten = src.lower() in ('booking.com','booking','expedia','hotels.com','agoda')
    val = f'<strong>{float(r["rating"]):.1f}</strong>/10' if ten else f'&#9733; <strong>{float(r["rating"]):.1f}</strong>'
    return (f'<span>{val} <a href="{gmaps(r["name"],town)}" target="_blank" rel="nofollow noopener">{esc(src)}{rv}</a></span>')
def build_body(key, hs):
    c=TOWNS[key]; town=c['town']; hs=sorted(hs,key=rrank,reverse=True); n=len(hs)
    paras=''.join(f'<p>{p}</p>\n' for p in c['intro'])
    nr=sum(1 for h in hs if h.get('rating'))
    callout=(f'<div class="callout"><h3>How I picked these {town} hotels</h3><p>I went through the places actually worth booking in '
             f'{town} across luxury, mid-range and budget, judging each on location, comfort, value and the view. {nr} of {n} have a real '
             f'public rating, shown with the review count and a maps link; the rest I rate from local knowledge and mark with a dash rather '
             f'than invent a score.</p></div>')
    rows=''
    for h in hs:
        rows+=(f'<tr><td><strong>{esc(h["name"])}</strong></td><td>{esc(h.get("area",""))}</td>'
               f'<td>{esc(h.get("type",""))}</td><td>{esc(h.get("price",""))}</td><td>{rating_cell(h,town)}</td></tr>')
    table=('<h2>At a glance - the best places to stay</h2>\n<table class="cmp-table"><thead><tr><th>Hotel</th><th>Area</th>'
           '<th>Type</th><th>Price</th><th>Rating</th></tr></thead><tbody>'+rows+'</tbody></table>')
    wins=[]; rated=[h for h in hs if h.get('rating')]
    if rated: wins.append(f'<li>🏆 <strong>Highest rated</strong> - {esc(rated[0]["name"])} ({float(rated[0]["rating"]):.1f}★)</li>')
    lux=next((h for h in hs if 'lux' in (h.get('type','')).lower()),None)
    if lux: wins.append(f'<li>✨ <strong>Best splurge</strong> - {esc(lux["name"])} ({esc(lux.get("highlight",""))})</li>')
    bud=next((h for h in hs if h.get('price','').strip()=='$' or 'budget' in (h.get('type','')).lower() or 'guest' in (h.get('type','')).lower()),None)
    if bud: wins.append(f'<li>💰 <strong>Best value</strong> - {esc(bud["name"])} ({esc(bud.get("highlight",""))})</li>')
    winners=('<h2>The standouts</h2>\n<ul>'+''.join(wins)+'</ul>') if wins else ''
    cta1=('<div class="article-cta"><h3>Planning your trip?</h3><p>I can build your whole route with my free '
          f'<a href="/planner">trip planner</a> and point you to the right base in {town} for what you want to do - '
          'just <a href="/contact">message me</a>.</p><a href="/planner" class="btn-primary">Plan my trip &rarr;</a></div>')
    cards=[f'<h2>The {n} best, reviewed</h2>']
    for i,h in enumerate(hs,1):
        meta=''
        if h.get('area'): meta+=f'<span>📍 <strong>{esc(h["area"])}</strong></span>'
        if h.get('type'): meta+=f'<span>🏨 <strong>{esc(h["type"])}</strong></span>'
        pr=esc(h.get('price','')) + (f' &middot; {esc(h["price_pkr"])}' if h.get('price_pkr') else '')
        if pr.strip(): meta+=f'<span>💷 <strong>{pr}</strong></span>'
        if h.get('best_for'): meta+=f'<span>👍 <strong>{esc(h["best_for"])}</strong></span>'
        if h.get('season') and 'year' not in str(h.get('season','')).lower(): meta+=f'<span>🗓 <strong>{esc(h["season"])}</strong></span>'
        meta+=rating_chip(h,town)
        hl=f'<p style="font-size:.9rem;line-height:1.62;color:#2E2A22;margin:.4rem 0 .3rem"><strong>Why stay:</strong> {esc(h["highlight"])}</p>' if h.get('highlight') else ''
        pl=''.join(f'<li>{esc(x)}</li>' for x in (h.get('pros') or []))
        cl=''.join(f'<li>{esc(x)}</li>' for x in (h.get('cons') or []))
        pc=(f'<div class="rev-pc"><div><h4 class="pros">What\'s good</h4><ul>{pl}</ul></div>'
            f'<div><h4 class="cons">Could be better</h4><ul>{cl}</ul></div></div>') if (pl or cl) else ''
        take=f'<div class="rev-verdict"><strong>My take:</strong> {esc(h["take"])}</div>' if h.get('take') else ''
        cards.append('<div class="rev">'
          f'<div class="rev-head"><div><div class="rev-badge">#{i}</div><h3>{esc(h["name"])}</h3>'
          f'<div class="rev-op">{esc(h.get("type",""))}{(" · "+esc(h.get("area",""))) if h.get("area") else ""}</div></div></div>'
          f'<div class="rev-meta">{meta}</div>\n{hl}{pc}{take}{map_links(h,town)}</div>')
    cards='\n'.join(cards)
    ver=next((h.get('verified') for h in hs if h.get('verified')),None)
    verline=f'<p style="font-size:.78rem;color:var(--cream-2);margin-top:1.2rem">Ratings and details cross-checked against recent Booking.com/Google/Tripadvisor reviews and local sources{(", last verified "+esc(ver)) if ver else ""}. Confirm current rates, room condition and winter opening directly before booking.</p>'
    ctx=(f'<h2>{c["ctx_h"]}</h2>\n<ul>'+''.join(f'<li>{x}</li>' for x in c['ctx'])+'</ul>')
    deeper=('<h2>Plan your trip deeper</h2>\n<ul>'+''.join(f'<li><a href="{h}">{l}</a></li>' for h,l in c['deeper'])+'</ul>')
    faq='<h2>FAQ</h2>\n<div class="faq">'+''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in c['faqs'])+'</div>'
    return '\n'.join([paras.strip(),callout,table,winners,cta1,cards,ctx,deeper,faq,verline])
def schema(key,hs):
    c=TOWNS[key]; town=c['town']; items=[]
    for i,h in enumerate(hs,1):
        items.append({"@type":"ListItem","position":i,"item":{"@type":"Hotel","name":h["name"],
          "address":{"@type":"PostalAddress","addressLocality":town,"addressRegion":"Gilgit-Baltistan","addressCountry":"PK"}}})
    il={"@context":"https://schema.org","@type":"ItemList","name":f"Best Hotels in {town} 2026","itemListElement":items}
    fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faqs']]}
    return ('<script type="application/ld+json">'+json.dumps(il)+'</script>\n<script type="application/ld+json">'+json.dumps(fq)+'</script>')
def assemble(key,title):
    c=TOWNS[key]; f=os.path.join(ROOT,c['path'],'index.html'); s=open(f).read()
    hs=json.load(open(os.path.join(DATA,key+'.json')))
    head=s[:s.index('</head>')+len('</head>')]
    head=re.sub(r'<title>.*?</title>',f'<title>{esc(title)}</title>',head,count=1,flags=re.S)
    nav=re.search(r'<body>(.*?)(?=<section|<main)',s,re.S).group(1).strip()
    foot=s[s.index('<footer>'):]
    rel=re.search(r'<!-- RELATED:START -->.*?<!-- RELATED:END -->',s,re.S); related=rel.group(0) if rel else ''
    parent=c['crumb_parent']
    crumb=(f'<div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em">'
           f'<a href="/" style="color:inherit">Home</a> / <a href="{parent[0]}" style="color:inherit">{parent[1]}</a> / '
           f'<span style="color:var(--cream)">Hotels</span></div>')
    main=(f'<main class="article">\n<div class="article-head">{crumb}\n'
          f'<div class="article-eyebrow">Where to Stay &middot; {c["town"]} &middot; 2026</div>\n'
          f'<h1 class="article-title">{esc(c["h1"])}</h1>\n'
          f'<div class="article-meta"><span>By <a href="/about"><strong>Faisal Zaman</strong></a></span>'
          f'<span class="sep">&middot;</span><span>Local, Gilgit-Baltistan</span>'
          f'<span class="sep">&middot;</span><span>Updated June 2026</span></div></div>\n'
          f'<figure class="article-figure"><div class="img" style="background-image:url(\'{c["hero"]}\')" role="img" aria-label="{esc(c["town"])} hotels"></div>'
          f'<figcaption>Where to stay in {esc(c["town"])}, Gilgit-Baltistan.</figcaption></figure>\n'
          f'<div class="article-body">\n{build_body(key,hs)}\n</div></main>')
    open(f,'w').write(head+'\n<body>\n'+nav+'\n'+main+'\n'+schema(key,hs)+'\n\n'+related+'\n'+foot)
    return len(hs)
if __name__=='__main__':
    for key in TOWNS:
        p=os.path.join(DATA,key+'.json')
        if not os.path.exists(p): print('  skip (no data):',key); continue
        n=len(json.load(open(p))); title=f"{n} Best Hotels in {TOWNS[key]['town']} 2026 - Reviewed"
        assemble(key,title); print(f'  {key}: {n} hotels -> {title}')
    print('done')
