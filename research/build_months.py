#!/usr/bin/env python3
"""Generate /<city>/in-<month> pages (Hunza + Skardu x 12) targeting
'<city> in <month>'. Weather + access data are verified (climate-data.org /
weather2travel); seasonal narrative is authored. Run then seo_inject.py."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def esc(s): return re.sub(r'&(?!amp;|lt;|gt;|#\d+;|quot;)','&amp;',str(s or ''))

MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
MNUM = {m:i+1 for i,m in enumerate(MONTHS)}

CLIMATE = {
 'hunza':[{'high':0,'low':-9,'cond':'cold, clear, snow on peaks'},{'high':1,'low':-8,'cond':'cold, occasional valley snow'},
   {'high':7,'low':-2,'cond':'cool, blossom begins late month'},{'high':14,'low':3,'cond':'mild, cherry & apricot blossom'},
   {'high':18,'low':6,'cond':'pleasant, green, clear skies'},{'high':23,'low':10,'cond':'warm, sunny, peak access'},
   {'high':26,'low':13,'cond':'hot, dry, glacial-melt rivers high'},{'high':25,'low':12,'cond':'warm, mostly clear, busy'},
   {'high':22,'low':8,'cond':'warm days, cool nights'},{'high':16,'low':2,'cond':'crisp, golden autumn foliage'},
   {'high':9,'low':-3,'cond':'cold, late foliage, first snow'},{'high':2,'low':-7,'cond':'cold, clear, snow on peaks'}],
 'skardu':[{'high':-3,'low':-12,'cond':'very cold, frozen, snow'},{'high':-1,'low':-11,'cond':'freezing, snowy, cloudy'},
   {'high':5,'low':-5,'cond':'cold, thaw, blossom starts'},{'high':12,'low':0,'cond':'mild, apricot blossom'},
   {'high':15,'low':3,'cond':'pleasant, green, clear'},{'high':20,'low':7,'cond':'warm, sunny, dry'},
   {'high':23,'low':10,'cond':'warm, peak season'},{'high':22,'low':10,'cond':'warm, clear, lush'},
   {'high':20,'low':5,'cond':'mild, crisp, clear'},{'high':14,'low':-1,'cond':'cool, autumn colours'},
   {'high':7,'low':-6,'cond':'cold, dry, clearing'},{'high':0,'low':-10,'cond':'very cold, snow begins'}],
}
WX_SRC = {'hunza':'Gilgit station averages (weather2travel.com); Karimabad/valley villages run a few degrees cooler',
          'skardu':'Skardu station averages (climate-data.org)'}

CITY = {
 'hunza': dict(disp='Hunza', hero='/images/hunza-hero.webp', guide='/hunza', tours='/tours/hunza',
   hotels='/hunza/hotels', eat='/hunza/food', do='/hunza/things-to-do', best='/hunza/best-time-to-visit',
   weather='/hunza/weather'),
 'skardu': dict(disp='Skardu', hero='/images/skardu-hero.webp', guide='/skardu', tours='/tours/skardu',
   hotels='/skardu/hotels', eat='/skardu/restaurants', do='/skardu/things-to-do', best=None,
   weather='/skardu/weather', tourist='/skardu/tourist-places'),
}

# season tag + crowd + one-line character, keyed by month number
SEASON = {
 1:('Deep winter','Very quiet','snow, short cold days and almost no other tourists'),
 2:('Deep winter','Very quiet','still cold and snowy, but the light starts to lengthen'),
 3:('Early spring','Quiet','the thaw, with blossom starting in the lower valleys late in the month'),
 4:('Spring (blossom)','Building','blossom season - one of the most beautiful and popular times to come'),
 5:('Late spring','Building','green, mild and clear, with the high passes reopening'),
 6:('Early summer','Busy','warm, dry and the start of full high-mountain access'),
 7:('Peak summer','Peak','the warmest, busiest month, with everything open'),
 8:('Peak summer','Peak','warm and lush but the most crowded - independence-day holidays add to it'),
 9:('Early autumn','Easing','arguably the sweet spot: warm days, cool nights and thinning crowds'),
 10:('Autumn (foliage)','Building','crisp, clear and golden - the famous autumn-colour window'),
 11:('Late autumn','Quiet','cold and quiet as the foliage finishes and the first snow arrives'),
 12:('Winter','Very quiet','cold, clear and atmospheric, with snow on the peaks and few visitors'),
}

def access_bullets(city, m):
    b=[]
    if city=='hunza':
        b.append(('open' if 5<=m<=11 else 'closed',
                  'Khunjerab Pass (Pak-China border, 4,693m) is normally open' if 5<=m<=11
                  else 'Khunjerab Pass is snow-closed for the season'))
        if 7<=m<=9: b.append(('open','Babusar Pass is open - the scenic shortcut via Naran'))
        elif m in (6,10): b.append(('check','Babusar Pass is opening/closing this month - check before relying on it'))
        else: b.append(('closed','Babusar Pass is closed; use the main Karakoram Highway via Chilas'))
        b.append(('open','Attabad Lake, Karimabad and the Baltit & Altit forts are open year-round'))
        if m in (12,1,2): b.append(('snow','Upper Hunza (Passu, Gulmit, Gojal) gets heavy snow and roads can be disrupted'))
    else:  # skardu
        if 7<=m<=8: b.append(('open','Deosai National Park (Sheosar Lake) is open'))
        elif m==9: b.append(('check','Deosai is open early in the month then starts to close with the first snow'))
        elif m==6: b.append(('check','Deosai usually opens late this month once the snow clears'))
        else: b.append(('closed','Deosai National Park is snow-bound and closed'))
        b.append(('open','Shangrila/Lower Kachura, Upper Kachura, Shigar Fort and Khaplu are open year-round'))
        if m in (12,1,2): b.append(('snow','Skardu flights and the road are most weather-affected now - keep buffer days'))
        if m in (4,5,9,10): b.append(('open','The Sarfaranga cold desert is at its best (good light, jeep rallies in spring)'))
    # blossom / foliage shared
    if m==3: b.append(('bloom','Apricot and cherry blossom begins in the lower valleys late in the month'))
    if m==4: b.append(('bloom','Blossom is in full bloom (peaks early-mid April) - the signature spring sight'))
    if city=='hunza' and m==10: b.append(('foliage','Autumn foliage peaks mid-to-late October - the best photography window'))
    if city=='hunza' and m==11: b.append(('foliage','Late foliage lingers early in the month before the first valley snow'))
    if city=='skardu' and m==10: b.append(('foliage','Autumn colours along the Indus and in Shigar/Khaplu'))
    return b

def do_items(city, m):
    if city=='hunza':
        base=['Walk up to the Baltit and Altit forts above Karimabad','Coffee and walnut cake at the Karimabad view cafes','Photograph the Passu Cones and Hussaini bridge']
        if m in (3,4): return ['See the cherry & apricot blossom across the terraces (the spring highlight)','Walk the Karimabad orchards and forts in mild weather']+base[:1]
        if 5<=m<=9: return ['Day trip to Khunjerab Pass on the Pakistan-China border','Boat on the turquoise Attabad Lake','Explore upper Hunza - Passu, Gulmit and the Hopper glacier viewpoints']+base[:1]
        if m==10 or (m==11): return ['Shoot the golden autumn foliage around Karimabad and Duikar','Sunrise at Eagle\'s Nest (Duikar) over Rakaposhi']+base[:2]
        return ['Snow-quiet forts and bazaar with almost no crowds','Warm up with chapshuro, harissa and tumuro tea','Clear-sky peak views of Rakaposhi from Eagle\'s Nest']
    else:
        base=['Boat on the heart-shaped Lower Kachura (Shangrila) lake','Visit the 17th-century Shigar Fort and Khaplu Palace','Hike up to Kharpocho Fort over the Indus']
        if m in (3,4): return ['See the apricot blossom in Shigar and the side valleys','Sarfaranga cold desert in soft spring light']+base[:1]
        if 7<=m<=9: return ['Jeep across Deosai National Park to Sheosar Lake','Use Skardu as the gateway to K2 and the Baltoro treks','Camp or picnic by Sadpara and the Kachura lakes']+base[:1]
        if m in (10,11): return ['Autumn colours along the Indus and Sarfaranga desert','Quiet fort and lake photography in crisp, clear air']+base[:2]
        return ['Snowbound Katpana/Sarfaranga desert and frozen lakes','Fresh trout and Balti karahi in a near-empty town','Shigar and Khaplu forts without a single other tourist']

def pack(city, m):
    hi=CLIMATE[city][m-1]['high']; lo=CLIMATE[city][m-1]['low']
    if lo<=-5: return 'A proper down jacket, thermals, gloves, hat and waterproof boots - nights are well below freezing.'
    if lo<3: return 'Warm layers and a windproof jacket for cold mornings and nights, lighter clothing for midday sun.'
    if hi>=22: return 'Light, breathable clothing for warm days, plus a fleece for cool evenings and strong sun protection.'
    return 'Layers: comfortable daytime clothing plus a warm jacket for the evenings, and sun protection.'

def verdict(city, m, disp):
    tag, crowd, char = SEASON[m]
    good = {4:'one of the very best times', 5:'an excellent time', 9:'arguably the best time', 10:'a beautiful time',
            6:'a great time', 7:'a good (if busy) time', 8:'a good (if busy) time'}.get(m, None)
    if good: return f'{MONTHS[m-1]} is {good} to visit {disp} - {char}.'
    if m in (1,2,12): return f'{MONTHS[m-1]} is for travellers who want snow, solitude and the lowest prices - not for high-mountain access.'
    if m==3: return f'March is a quiet shoulder month in {disp} - cold early on, but rewarding if you catch the first blossom.'
    return f'{MONTHS[m-1]} is a transitional month in {disp} - {char}.'

def cluster(city, m):
    c=CITY[city]; disp=c['disp']
    nxt=MONTHS[m % 12]; prv=MONTHS[(m-2) % 12]
    cells=[('Plan',c['best'] or f"{c['guide']}", f'Best time to visit {disp}'),
           ('Weather',c['weather'], f'{disp} weather by month'),
           ('Do',c['do'], f'Things to do in {disp}'),
           ('Tours',c['tours'], f'{disp} tour packages'),
           ('Stay',c['hotels'], f'Best hotels in {disp}'),
           ('Month',f'{c["guide"]}/in-{prv.lower()}', f'{disp} in {prv}'),
           ('Month',f'{c["guide"]}/in-{nxt.lower()}', f'{disp} in {nxt}')]
    cells=[(cat,u,l) for cat,u,l in cells if u and os.path.exists(os.path.join(ROOT,u.strip('/'),'index.html')) or cat=='Month']
    inner=''.join(f'<a href="{u}"><span>{cat}</span>{esc(l)}</a>' for cat,u,l in cells)
    return f'<div class="cluster-links"><h2>Plan your {disp} trip</h2><div class="cluster-grid">{inner}</div></div>'

ICON={'open':'✅','closed':'⛔','check':'⚠️','snow':'❄️','bloom':'🌸','foliage':'🍂'}

def build_body(city, m):
    c=CITY[city]; disp=c['disp']; mn=MONTHS[m-1]; cl=CLIMATE[city][m-1]; tag,crowd,char=SEASON[m]
    intro=(f"<p>Thinking about {disp} in {mn}? Here's the honest, on-the-ground picture for 2026 - the weather, what's actually open, "
           f"how busy it is, and whether it's worth timing your trip for. In short, {mn} is {tag.lower()}: {char}.</p>")
    wx=(f'<h2>Weather in {disp} in {mn}</h2>\n'
        f'<ul class="trek-facts"><li>Avg high ~{cl["high"]}&deg;C</li><li>Avg low ~{cl["low"]}&deg;C</li><li>{esc(cl["cond"])}</li><li>{tag}</li></ul>\n'
        f'<p>Expect daytime highs around {cl["high"]}&deg;C and nights near {cl["low"]}&deg;C ({esc(cl["cond"])}). '
        f'<span style="font-size:.85em;color:var(--cream-2)">(Figures are {WX_SRC[city]}; mountains and high villages are colder.)</span></p>')
    ab=access_bullets(city,m)
    access=('<h2>What\'s open &amp; getting around</h2>\n<ul>'
            +''.join(f'<li>{ICON.get(s,"")} {esc(t)}</li>' for s,t in ab)+'</ul>')
    crowds=(f'<h2>Crowds &amp; prices</h2>\n<p>{mn} is <strong>{crowd.lower()}</strong> in {disp}. '
            + ('Expect peak-season rates and book hotels and jeeps well ahead.' if crowd=='Peak'
               else 'Prices are at their lowest and you\'ll often have sights to yourself.' if 'quiet' in crowd.lower()
               else 'Rates and availability are reasonable, but the best rooms still go early in this window.')+'</p>')
    do=(f'<h2>Best things to do in {disp} in {mn}</h2>\n<ul>'+''.join(f'<li>{esc(x)}</li>' for x in do_items(city,m))+'</ul>')
    pk=f'<h2>What to pack</h2>\n<p>{esc(pack(city,m))}</p>'
    vd=f'<h2>Is {mn} a good time to visit {disp}?</h2>\n<p>{esc(verdict(city,m,disp))} '+(f'If your dates are flexible, compare it with the <a href="{c["best"]}">best time to visit {disp}</a>.' if c.get('best') else f'See the full <a href="{c["weather"]}">{disp} weather guide</a> to compare months.')+'</p>'
    faqs=[(f'What is the weather like in {disp} in {mn}?', f'Average highs are around {cl["high"]}&deg;C and lows near {cl["low"]}&deg;C - {cl["cond"]}. High villages and passes are colder.'),
          (f'Is {mn} a good time to visit {disp}?', esc(verdict(city,m,disp))),
          (f'What should I pack for {disp} in {mn}?', esc(pack(city,m)))]
    faq='<h2>FAQ</h2>\n<div class="faq">'+''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q,a in faqs)+'</div>'
    cta=('<div class="article-cta"><h3>Want a trip planned around the right month?</h3>'
         f'<p>Tell me your dates and I\'ll plan a {disp} route that fits the season - free, with my '
         '<a href="/planner">trip planner</a> or a quick <a href="/contact">message</a>.</p>'
         '<a href="/planner" class="btn-primary">Plan my trip &rarr;</a></div>')
    return '\n'.join([intro, wx, access, crowds, do, pk, vd, cta, cluster(city,m), faq])

def schema(city,m):
    c=CITY[city]; disp=c['disp']; mn=MONTHS[m-1]; cl=CLIMATE[city][m-1]
    faqs=[(f'What is the weather like in {disp} in {mn}?', f'Average highs are around {cl["high"]}C and lows near {cl["low"]}C - {cl["cond"]}.'),
          (f'Is {mn} a good time to visit {disp}?', verdict(city,m,disp).replace('&','and')),
          (f'What should I pack for {disp} in {mn}?', pack(city,m))]
    fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    return '<script type="application/ld+json">'+json.dumps(fq)+'</script>'

def build(city, m):
    c=CITY[city]; disp=c['disp']; mn=MONTHS[m-1]
    tmpl=os.path.join(ROOT, c['guide'].strip('/'), 'index.html')
    s=open(tmpl).read()
    head=s[:s.index('</head>')+len('</head>')]
    title=f'{disp} in {mn} 2026: Weather, What\'s Open &amp; Tips'
    desc=f"Visiting {disp} in {mn}? Honest 2026 guide to the weather (avg {CLIMATE[city][m-1]['high']}/{CLIMATE[city][m-1]['low']}C), what's open, crowds, the best things to do and what to pack."
    head=re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1, flags=re.S)
    if '<meta name="description"' in head:
        head=re.sub(r'(<meta name="description" content=")[^"]*(")', lambda mm:mm.group(1)+esc(desc)+mm.group(2), head, count=1)
    nav=re.search(r'<body>(.*?)(?=<main|<section)', s, re.S).group(1).strip()
    foot=s[s.index('<footer>'):]
    crumb=(f'<div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em">'
           f'<a href="/" style="color:inherit">Home</a> / <a href="{c["guide"]}" style="color:inherit">{disp}</a> / '
           f'<span style="color:var(--cream)">in {mn}</span></div>')
    main=(f'<main class="article">\n<div class="article-head">{crumb}\n'
          f'<div class="article-eyebrow">When to Go &middot; {disp} &middot; {mn} 2026</div>\n'
          f'<h1 class="article-title">Thinking of {disp} in {mn}? Here\'s the Honest Picture</h1>\n'
          f'<div class="article-meta"><span>By <a href="/about"><strong>Faisal Zaman</strong></a></span>'
          f'<span class="sep">&middot;</span><span>Local, Gilgit-Baltistan</span><span class="sep">&middot;</span><span>Updated June 2026</span></div></div>\n'
          f'<figure class="article-figure"><div class="img" style="background-image:url(\'{c["hero"]}\')" role="img" aria-label="{disp} in {mn}"></div>'
          f'<figcaption>{disp} in {mn}, Gilgit-Baltistan.</figcaption></figure>\n'
          f'<div class="article-body">\n{build_body(city,m)}\n</div></main>')
    out=head+'\n<body>\n'+nav+'\n'+main+'\n'+schema(city,m)+'\n\n'+foot
    d=os.path.join(ROOT, c['guide'].strip('/'), f'in-{mn.lower()}'); os.makedirs(d, exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(out)
    return f'{c["guide"]}/in-{mn.lower()}'

if __name__=='__main__':
    n=0
    for city in CITY:
        for m in range(1,13):
            build(city,m); n+=1
    print(f'built {n} month pages')
