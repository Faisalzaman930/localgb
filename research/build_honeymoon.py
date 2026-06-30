#!/usr/bin/env python3
"""Build /tours/<city>/honeymoon pages targeting '<city> honeymoon packages'.
Clones chrome from the city's tour page; body = honeymoon packages + romantic
stays (from research/hotels) + how-to-plan + FAQ. Run then seo_inject.py."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def esc(s): return re.sub(r'&(?!amp;|lt;|gt;|#\d+;|quot;)','&amp;',str(s or ''))

CITY = {
 'skardu': dict(
   disp='Skardu', tour='/tours/skardu', guide='/skardu', hotels='/skardu/hotels',
   title='Skardu Honeymoon Packages 2026: Reviewed + Best Romantic Stays',
   desc="Honest 2026 Skardu honeymoon guide: the published honeymoon package reviewed, the most romantic places to stay (Shigar Fort, Shangrila), the best months, and how to plan a private Skardu honeymoon.",
   h1="Planning a Skardu Honeymoon? The Packages and Stays I'd Pick for 2026",
   blossom='late March to April (apricot &amp; cherry blossom)', autumn='October',
   packages=[dict(name='8 Days Luxury Honeymoon Tour to Skardu, Shangrila, Khaplu & Shigar Valley',
                  op='Pakistan Travel Places', home='https://pakistantravelplaces.com',
                  url='https://pakistantravelplaces.com/tour/8-days-super-deluxe-honeymoon-tour-to-skardu-shangrila-khaplu-shiger-valley/',
                  days='8 days', price='Rs 190,000',
                  good=['Stays at genuinely romantic, named properties - Shangrila Resort and Khaplu Serena Palace','All three meals a day and a private car with driver included','Covers Shangrila/Kachura, Shigar, Khaplu and Deosai in one loop'],
                  bad=['Two of the eight days are long Karakoram Highway transit','"Royal treatment" is undefined - confirm the room category before paying'],
                  verdict='The one published Skardu honeymoon package, and a strong one: five-star-grade named hotels and full board. Best if you want it all arranged and do not mind the long drive in.')],
   stays=['Serena Shigar Fort','Shangrila Resort Skardu','Arish Luxury Suites'],
   plan=["<strong>Best months:</strong> late March to April for apricot blossom, or September to October for crisp, clear, romantic light. Avoid deep winter unless you want snow and quiet.",
         "<strong>Fly if you can:</strong> the Islamabad-Skardu flight saves two long road days - worth it on a short honeymoon (it is weather-dependent, so keep a buffer).",
         "<strong>For privacy:</strong> base at Shigar Fort or a Kachura-lake resort rather than the busy town, and ask for a private jeep for Deosai and Shigar rather than a group.",
         "<strong>Build your own:</strong> most GB honeymoons are custom - tell me your dates and budget and I will plan a private route and book the romantic rooms before they go."],
   faqs=[("How much does a Skardu honeymoon package cost?","The published luxury honeymoon package runs about Rs 190,000 for 8 days with named five-star-grade hotels and full board. Custom private trips vary with hotels, vehicle and length - get an itemised quote."),
         ("What is the best month for a Skardu honeymoon?","Late March-April for apricot and cherry blossom, or September-October for clear skies and golden light. Both are mild and beautiful; summer is busy and winter is cold and quiet."),
         ("Where should we stay in Skardu for a honeymoon?","Serena Shigar Fort (a restored 17th-century fort with gardens) and the Shangrila lakeside resort are the most romantic; Arish Luxury Suites is the best modern option in town."),
         ("Should we fly or drive to Skardu?","Fly if your schedule is tight - it saves two long road days. Keep a buffer day either side because the Skardu flight is weather-dependent.")]),
 'hunza': dict(
   disp='Hunza', tour='/tours/hunza', guide='/hunza', hotels='/hunza/hotels',
   title='Hunza Honeymoon Packages 2026: Reviewed + Best Romantic Stays',
   desc="Honest 2026 Hunza honeymoon guide: the published honeymoon packages reviewed, the most romantic places to stay (Serena Altit, Eagle's Nest), the best months, and how to plan a private Hunza honeymoon.",
   h1="Planning a Hunza Honeymoon? The Packages and Stays I'd Pick for 2026",
   blossom='late March to mid-April (cherry blossom)', autumn='mid-October to early November',
   packages=[dict(name='5 Days Luxury Honeymoon Tour to Hunza Valley',
                  op='Pakistan Travel Places', home='https://pakistantravelplaces.com',
                  url='https://pakistantravelplaces.com/tour/5-days-super-deluxe-honeymoon-tour-to-hunza-valley/',
                  days='5 days', price='Rs 160,000',
                  good=['Private Prado with a dedicated driver from Islamabad - a self-contained car for two','All three daily meals included, plus fort entry tickets','Covers Attabad Lake, Passu, Khunjerab and the Karimabad forts'],
                  bad=['Hotel is not named ("good family hotel" vs "5-star" on the page) - confirm it','Long onward drive days top and tail the trip'],
                  verdict='The fuller Hunza honeymoon option: private car, all meals and forts handled. Pin down the exact hotel before you pay.'),
             dict(name='5 Days Standard Honeymoon Tour to Hunza Valley',
                  op='Pakistan Travel Places', home='https://pakistantravelplaces.com',
                  url='https://pakistantravelplaces.com/tour/5-days-deluxe-honeymoon-tour-to-hunza-valley/',
                  days='5 days', price='Rs 135,000',
                  good=['Same private-car Hunza honeymoon at a lower price','Both fort entry tickets and tolls bundled in'],
                  bad=['Breakfast and dinner only - lunch is on you','Unnamed 3-star hotel; no published cancellation terms'],
                  verdict='The budget-friendlier private Hunza honeymoon. Good value if you accept a 3-star unnamed hotel and pay your own lunches.')],
   stays=['Serena Altit Fort Residence','Eagle\'s Nest Hotel','Luxus Hunza Attabad Lake Resort'],
   plan=["<strong>Best months:</strong> late March-mid April for the famous cherry blossom, or mid-October-early November for golden foliage. Both are the most romantic windows; book early as they are popular.",
         "<strong>Pay for the view:</strong> a Rakaposhi or valley-facing room is the whole point in Hunza - it is worth the upgrade on a honeymoon.",
         "<strong>Stay in Karimabad:</strong> walkable to the forts, cafes and viewpoints, so you are not driving every evening; Duikar (Eagle's Nest) for sunrise.",
         "<strong>Build your own:</strong> most Hunza honeymoons are custom - send me your dates and budget and I will plan a private route and lock in the best rooms."],
   faqs=[("How much does a Hunza honeymoon package cost?","The published private honeymoon packages run about Rs 135,000 (standard) to Rs 160,000 (luxury) for 5 days. Custom trips vary with the hotel and vehicle - get an itemised quote."),
         ("What is the best month for a Hunza honeymoon?","Late March to mid-April for cherry blossom, or mid-October to early November for autumn foliage. Both are mild, photogenic and the most romantic times to go."),
         ("Where should we stay in Hunza for a honeymoon?","Serena Altit Fort Residence (heritage and quiet) and Eagle's Nest at Duikar (the legendary Rakaposhi sunrise view) are the most romantic; Luxus is the luxury lake resort at Attabad."),
         ("How many days do we need?","Five days covers the Hunza honeymoon highlights comfortably; add two or three if you want Khunjerab Pass and upper Hunza at a relaxed pace.")]),
}

def load_hotels(city):
    try: return {h['name']: h for h in json.load(open(os.path.join(ROOT,'research','hotels',city+'.json')))}
    except: return {}

def stay_card(h):
    meta=''
    if h.get('area'): meta+=f'<span>📍 <strong>{esc(h["area"])}</strong></span>'
    if h.get('type'): meta+=f'<span>🏨 <strong>{esc(h["type"])}</strong></span>'
    if h.get('rating'):
        src=h.get('rating_src') or 'Google'
        ten = src.lower() in ('booking.com','booking','expedia')
        val = f'<strong>{float(h["rating"]):.1f}</strong>/10' if ten else f'&#9733; <strong>{float(h["rating"]):.1f}</strong>'
        rv=f' ({h["reviews"]})' if h.get('reviews') else ''
        meta+=f'<span>{val} {esc(src)}{rv}</span>'
    return ('<div class="rev"><div class="rev-head"><div><div class="rev-badge">Romantic stay</div>'
            f'<h3>{esc(h["name"])}</h3><div class="rev-op">{esc(h.get("type",""))}{(" · "+esc(h.get("area",""))) if h.get("area") else ""}</div></div></div>'
            f'<div class="rev-meta">{meta}</div>'
            + (f'<p style="font-size:.9rem;line-height:1.62;color:#2E2A22;margin:.4rem 0 .2rem"><strong>Why for a honeymoon:</strong> {esc(h.get("highlight",""))}</p>' if h.get('highlight') else '')
            + (f'<div class="rev-verdict"><strong>My take:</strong> {esc(h["take"])}</div>' if h.get('take') else '')
            + '</div>')

def build_body(key):
    c=CITY[key]; disp=c['disp']; hotels=load_hotels(key)
    # packages table + cards
    rows=''.join(f'<tr><td><strong>{esc(p["name"])}</strong></td><td>{esc(p["days"])}</td><td>{esc(p["price"])}</td>'
                 f'<td><a href="{p["url"]}" target="_blank" rel="nofollow noopener">link</a></td></tr>' for p in c['packages'])
    table=('<h2>Honeymoon tour packages compared</h2>\n<table class="cmp-table"><thead><tr><th>Package</th><th>Length</th><th>From</th><th>Book</th></tr></thead><tbody>'+rows+'</tbody></table>')
    pcards=[]
    for p in c['packages']:
        op=f'<a href="{p["home"]}" target="_blank" rel="nofollow noopener">{esc(p["op"])}</a>'
        pl=''.join(f'<li>{esc(x)}</li>' for x in p['good']); cl=''.join(f'<li>{esc(x)}</li>' for x in p['bad'])
        pcards.append('<div class="rev">'
          f'<div class="rev-head"><div><div class="rev-badge">Honeymoon</div><h3>{esc(p["name"])}</h3>'
          f'<div class="rev-op">by {op} · {esc(p["days"])} · from {esc(p["price"])}</div></div></div>'
          f'<div class="rev-meta"><span>🗓 <strong>{esc(p["days"])}</strong></span><span>💷 <strong>{esc(p["price"])}</strong></span></div>'
          f'<div class="rev-pc"><div><h4 class="pros">What\'s good</h4><ul>{pl}</ul></div><div><h4 class="cons">Could be better</h4><ul>{cl}</ul></div></div>'
          f'<div class="rev-verdict"><strong>Verdict:</strong> {esc(p["verdict"])}</div>'
          f'<div class="rev-links">🔗 <a href="{p["url"]}" target="_blank" rel="nofollow noopener">View this package</a> · {op}</div></div>')
    stays=''.join(stay_card(hotels[n]) for n in c['stays'] if n in hotels)
    plan='<h2>How to plan a '+disp+' honeymoon</h2>\n<ul>'+''.join(f'<li>{x}</li>' for x in c['plan'])+'</ul>'
    faq='<h2>FAQ</h2>\n<div class="faq">'+''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in c['faqs'])+'</div>'
    intro=(f'<p>A {disp} honeymoon is one of the most beautiful (and underrated) you can have in Asia: '
           f'{c["blossom"].split("(")[0].strip()} blossom or {c["autumn"]} foliage, snow peaks over your room, and very few crowds. '
           f"I'm from Gilgit-Baltistan, so here's the honest version - the one published package worth a look, the genuinely romantic places to stay, and how I'd plan it.</p>"
           f'<p>There are very few <em>published</em> {disp} honeymoon packages (most are built custom), so I review what exists, then give you the romantic stays and a plan to build your own.</p>')
    cta=('<div class="article-cta"><h3>Want it planned around just the two of you?</h3>'
         '<p>Tell me your dates and budget and I\'ll plan a private route and lock in the romantic rooms before they go - free, with my '
         '<a href="/planner">trip planner</a> or a quick <a href="/contact">message</a>.</p>'
         '<a href="/planner?entry=honeymoon" class="btn-primary">Plan our honeymoon &rarr;</a></div>')
    return '\n'.join([intro, table, '\n'.join(pcards),
                      f'<h2>The most romantic places to stay in {disp}</h2>', stays,
                      cta, plan, faq])

def schema(key):
    c=CITY[key]
    items=[{"@type":"ListItem","position":i+1,"item":{"@type":"TouristTrip","name":p["name"],"url":p["url"],
            "provider":{"@type":"Organization","name":p["op"]}}} for i,p in enumerate(c['packages'])]
    il={"@context":"https://schema.org","@type":"ItemList","name":c['title'],"itemListElement":items}
    fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faqs']]}
    return '<script type="application/ld+json">'+json.dumps(il)+'</script>\n<script type="application/ld+json">'+json.dumps(fq)+'</script>'

def build(key):
    c=CITY[key]
    tmpl=os.path.join(ROOT, c['tour'].strip('/'), 'index.html')
    s=open(tmpl).read()
    head=s[:s.index('</head>')+len('</head>')]
    head=re.sub(r'<title>.*?</title>', f'<title>{esc(c["title"])}</title>', head, count=1, flags=re.S)
    head=re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m:m.group(1)+esc(c['desc'])+m.group(2), head, count=1)
    nav=re.search(r'<body>(.*?)(?=<main|<section)', s, re.S).group(1).strip()
    foot=s[s.index('<footer>'):]
    disp=c['disp']
    crumb=(f'<div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em">'
           f'<a href="/" style="color:inherit">Home</a> / <a href="/tours" style="color:inherit">Tours</a> / '
           f'<a href="{c["tour"]}" style="color:inherit">{disp}</a> / <span style="color:var(--cream)">Honeymoon</span></div>')
    main=(f'<main class="article">\n<div class="article-head">{crumb}\n'
          f'<div class="article-eyebrow">Honeymoon &middot; {disp} &middot; 2026</div>\n'
          f'<h1 class="article-title">{esc(c["h1"])}</h1>\n'
          f'<div class="article-meta"><span>By <a href="/about"><strong>Faisal Zaman</strong></a></span>'
          f'<span class="sep">&middot;</span><span>Local, Gilgit-Baltistan</span><span class="sep">&middot;</span><span>Updated June 2026</span></div></div>\n'
          f'<div class="article-body">\n{build_body(key)}\n</div></main>')
    out=head+'\n<body>\n'+nav+'\n'+main+'\n'+schema(key)+'\n\n'+foot
    d=os.path.join(ROOT, c['tour'].strip('/'), 'honeymoon'); os.makedirs(d, exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(out)
    return c['tour']+'/honeymoon'

if __name__=='__main__':
    for k in CITY: print('  built', build(k))
    print('done')
