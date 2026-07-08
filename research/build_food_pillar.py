#!/usr/bin/env python3
"""Build /food - 'What to Eat in Gilgit-Baltistan' pillar page linking the 3
city restaurant roundups + a signature-dish guide (where to try each). Clones
chrome from hunza/index.html. Run then seo_inject.py."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def esc(s): return re.sub(r'&(?!amp;|lt;|gt;|#\d+;|quot;)','&amp;',str(s or ''))

CITY_PAGES=[('/hunza/food','Best Restaurants in Hunza'),('/skardu/restaurants','Best Restaurants in Skardu'),('/gilgit/restaurants','Best Restaurants in Gilgit')]

# signature GB dishes: (dish, one-line, where-to-try link, where label)
DISHES=[
 ('Chapshuro','The Hunza meat-filled pastry - the one dish nobody should miss.','/hunza/food','Hunza'),
 ('Mamtu','Balti steamed meat dumplings with a signature sauce, Skardu\'s street-food star.','/skardu/restaurants','Skardu'),
 ('Yak (burger, pizza, karahi)','Highland yak meat done local-meets-modern - a yak burger in Skardu, yak pizza in Hunza, yak karahi in Gilgit.','/skardu/restaurants','Skardu &amp; Hunza'),
 ('Apricot cake','Warm, syrupy cake from Hunza\'s apricots - legendary at the Passu view cafes.','/hunza/food','Hunza / Passu'),
 ('Walnut cake','Honey-caramel walnut cake, the Karimabad cafe classic.','/hunza/food','Hunza'),
 ('Dowdo &amp; harissa','Hunzai comfort food - hand-cut noodle soup (dowdo) and slow-cooked harissa.','/hunza/food','Hunza'),
 ('Diram fitti &amp; burus','Sweet sprouted-wheat bread and apricot-kernel breads - rare traditional Hunza plates.','/hunza/food','Hunza'),
 ('Balay &amp; prapu','Balti buckwheat noodles and wheat-noodle soup, the Skardu home-kitchen staples.','/skardu/restaurants','Skardu'),
 ('Gral &amp; molida (Wakhi)','Upper-Hunza Wakhi specialties you won\'t find down-country, best in Gulmit.','/hunza/food','Gulmit, Hunza'),
 ('River trout','Fresh Karakoram trout, grilled - a Gilgit and Skardu signature.','/gilgit/restaurants','Gilgit &amp; Skardu'),
 ('Chapli kebab &amp; mantu','Gilgiti/Central-Asian plates - flat spiced kebab and dumplings by the river.','/gilgit/restaurants','Gilgit'),
 ('Tumuro (mountain thyme) tea','The wild-herb tea poured across the valleys - order it with anything.','/hunza/food','All GB'),
]

def build_body():
    intro=("<p>Gilgit-Baltistan quietly has one of the most distinctive food cultures in Pakistan - organic, mountain, and unlike anything "
           "down-country. Alongside the familiar karahi and BBQ you'll find things that are genuinely local: yak, apricot and walnut everything, "
           "Balti dumplings, Hunzai sprouted-wheat breads, and Wakhi dishes from the far north. I'm from here, so this is what to actually eat, and "
           "where to find the best of it.</p>")
    # dish list
    dl=''.join(f'<li><strong>{d}</strong> - {desc} <a href="{u}" style="color:var(--gold)">Try it in {w} &rarr;</a></li>' for d,desc,u,w in DISHES)
    dishes=f'<h2>The dishes to try (and where)</h2>\n<ul>{dl}</ul>'
    # local vs classic note
    mix=("<div class=\"callout\"><h3>Local specialties vs the usual menu</h3><p>Every good GB meal is a mix: order at least one thing that only "
         "exists here (chapshuro, mamtu, yak, apricot cake, dowdo, gral) alongside the reliable Pakistani classics (karahi, BBQ, trout). The city "
         "guides below tag each restaurant's <strong>GB local specialty</strong> so you can build that mix.</p></div>")
    # town cards
    cards=''.join(f'<a href="{u}"><span>City food guide</span>{esc(l)}</a>' for u,l in CITY_PAGES)
    towns=f'<h2>Best restaurants by town</h2>\n<div class="cluster-links"><div class="cluster-grid">{cards}</div></div>'
    faqs=[('What food is Gilgit-Baltistan famous for?','Chapshuro (Hunza meat pastry), Balti mamtu dumplings, apricot and walnut cakes, dowdo and harissa, river trout, yak dishes, and wild tumuro (mountain-thyme) tea - much of it organic and local to the region.'),
          ('What is chapshuro?','A Hunza specialty: a flatbread pastry stuffed with spiced minced meat and onion, baked or griddled. It is the single most iconic GB dish - best in Karimabad.'),
          ('Where can I try yak in Gilgit-Baltistan?','Yak turns up as a yak burger in Skardu, yak pizza in Hunza (Karimabad), and yak karahi in Gilgit. See the city guides for the exact spots.'),
          ('Is there vegetarian food in Gilgit-Baltistan?','Yes - daal, seasonal vegetables, local breads, apricot dishes and rice are widely available, though the signature plates are meat-based.')]
    faq='<h2>FAQ</h2>\n<div class="faq">'+''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q,a in faqs)+'</div>'
    cta=('<div class="article-cta"><h3>Planning a GB food trip?</h3><p>Tell me what you like and I\'ll route you through the best local kitchens - '
         'free, with my <a href="/planner">trip planner</a> or a quick <a href="/contact">message</a>.</p><a href="/planner" class="btn-primary">Plan my trip &rarr;</a></div>')
    return '\n'.join([intro, mix, dishes, towns, cta, faq])

def schema():
    faqs=[('What food is Gilgit-Baltistan famous for?','Chapshuro, Balti mamtu, apricot and walnut cakes, dowdo, harissa, river trout, yak dishes and tumuro tea.'),
          ('What is chapshuro?','A Hunza flatbread stuffed with spiced minced meat, baked or griddled - the most iconic GB dish.'),
          ('Where can I try yak in Gilgit-Baltistan?','As a yak burger in Skardu, yak pizza in Hunza, and yak karahi in Gilgit.'),
          ('Is there vegetarian food in Gilgit-Baltistan?','Yes - daal, vegetables, local breads and rice are widely available.')]
    fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    return '<script type="application/ld+json">'+json.dumps(fq)+'</script>'

def build():
    tmpl=os.path.join(ROOT,'hunza','index.html'); s=open(tmpl).read()
    head=s[:s.index('</head>')+len('</head>')]
    title='What to Eat in Gilgit-Baltistan 2026: Food Guide &amp; Best Dishes'
    desc="A local's guide to Gilgit-Baltistan food: chapshuro, mamtu, yak, apricot & walnut cake, dowdo, trout and where to eat in Hunza, Skardu and Gilgit."
    head=re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1, flags=re.S)
    if '<meta name="description"' in head:
        head=re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m:m.group(1)+esc(desc)+m.group(2), head, count=1)
    nav=re.search(r'<body>(.*?)(?=<main|<section)', s, re.S).group(1).strip()
    foot=s[s.index('<footer>'):]
    crumb=('<div class="art-crumb" style="font-size:.7rem;color:var(--cream-2);margin-bottom:1.4rem;letter-spacing:.04em">'
           '<a href="/" style="color:inherit">Home</a> / <span style="color:var(--cream)">Food</span></div>')
    main=(f'<main class="article">\n<div class="article-head">{crumb}\n'
          f'<div class="article-eyebrow">Food Guide &middot; Gilgit-Baltistan &middot; 2026</div>\n'
          f'<h1 class="article-title">What to Eat in Gilgit-Baltistan: A Local\'s Food Guide</h1>\n'
          f'<div class="article-meta"><span>By <a href="/about"><strong>Faisal Zaman</strong></a></span>'
          f'<span class="sep">&middot;</span><span>Local, Gilgit-Baltistan</span><span class="sep">&middot;</span><span>Updated June 2026</span></div></div>\n'
          f'<figure class="article-figure"><div class="img" style="background-image:url(\'/images/hunza-hero.webp\')" role="img" aria-label="Gilgit-Baltistan food"></div>'
          f'<figcaption>The food of Gilgit-Baltistan - local, organic and unlike anywhere else in Pakistan.</figcaption></figure>\n'
          f'<div class="article-body">\n{build_body()}\n</div></main>')
    out=head+'\n<body>\n'+nav+'\n'+main+'\n'+schema()+'\n\n'+foot
    d=os.path.join(ROOT,'food'); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(out)
    return '/food'

if __name__=='__main__':
    print('built', build())
