#!/usr/bin/env python3
"""Build per-trek operator comparison sections into existing /trekking/* pages
from research/treks/<route>.json, and rebuild the /trekking hub cross-table.
Idempotent: replaces content between <!-- TREKCMP:START/END --> markers."""
import json, re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'research', 'treks')

DISPLAY = {
 'k2-base-camp':'K2 Base Camp Trek',
 'concordia':'Concordia / Baltoro Trek',
 'gondogoro-la':'Gondogoro La Trek',
 'biafo-hispar-snow-lake':'Snow Lake / Hispar La Trek',
 'rush-lake':'Rush Lake Trek',
 'rakaposhi-base-camp':'Rakaposhi Base Camp Trek',
 'nanga-parbat-base-camp':'Nanga Parbat Base Camp Trek',
 'nanga-parbat-rupal-face':'Nanga Parbat Rupal Face Trek',
 'spantik-base-camp':'Spantik (Golden Peak) Trek & Expedition',
 'masherbrum-base-camp':'Masherbrum Base Camp Trek',
 'laila-peak-base-camp':'Laila Peak Base Camp Trek',
 'hushe-valley':'Charakusa / Hushe Valley Trek',
 'haramosh-kutwal-lake':'Haramosh / Kutwal Lake Trek',
 'karambar-lake':'Karambar Lake Trek',
 'naltar-lakes':'Naltar Valley & Lakes',
}

def esc(s):
    if s is None: return ''
    s = str(s)
    # encode bare & only (leave existing entities)
    s = re.sub(r'&(?!amp;|lt;|gt;|#\d+;|quot;)', '&amp;', s)
    return s

def price_str(p):
    if p.get('price_usd'): return '$%s' % format(int(p['price_usd']), ',')
    if p.get('price_pkr'): return 'Rs %s' % format(int(p['price_pkr']), ',')
    return 'Quote only'

def price_rank(p):
    if p.get('price_usd'): return int(p['price_usd'])
    if p.get('price_pkr'): return int(p['price_pkr'])/280.0
    return 9_999_999  # quote-only sorts last

def has_price(p):
    return bool(p.get('price_usd') or p.get('price_pkr'))

CTA = '''
  <div style="background:var(--gold-glow);border:1px solid var(--gold-border);border-radius:14px;padding:1.6rem 1.7rem;margin:1.8rem 0;">
    <h3 style="font-family:var(--fd);font-size:1.3rem;margin:0 0 .5rem;color:var(--cream)">Want a second opinion before you book?</h3>
    <p style="font-size:.92rem;color:var(--cream-2);line-height:1.6;margin:0 0 1rem">I'm Faisal, from Hunza. I'll sanity-check any quote, plan your route and season, and share vetted contacts for guides, porters, jeeps and hotels across Gilgit-Baltistan. No fee.</p>
    <div style="display:flex;gap:.7rem;flex-wrap:wrap">
      <a href="/planner?entry=trekking" style="display:inline-block;background:var(--gold);color:var(--ink);font-family:var(--fu);font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:.85rem 1.8rem;text-decoration:none;border-radius:6px;">Build my trek plan &rarr;</a>
      <a href="/contact" style="display:inline-block;border:1px solid var(--gold-border);color:var(--cream);font-family:var(--fu);font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:.85rem 1.8rem;text-decoration:none;border-radius:6px;">Ask for guide / porter contacts</a>
    </div>
    <p style="font-size:.78rem;color:var(--cream-2);margin:1rem 0 0;padding-top:.9rem;border-top:1px solid var(--gold-border)"><strong>Run this trek?</strong> Publish real prices and look after your crew, and I'll review and list you here. <a href="/contact">Get listed &rarr;</a></p>
  </div>'''

def badge_for(p, cheapest_op):
    if not has_price(p): return 'Quote only'
    if p['operator'] == cheapest_op: return 'Lowest verified price'
    return ''

def build_section(route, pkgs):
    name = DISPLAY[route]
    pkgs = sorted(pkgs, key=price_rank)
    priced = [p for p in pkgs if has_price(p)]
    quote = [p for p in pkgs if not has_price(p)]
    cheapest_op = priced[0]['operator'] if priced else None

    n_priced, n_quote = len(priced), len(quote)
    if n_priced >= 2:
        lo, hi = price_str(priced[0]), price_str(priced[-1])
        intro = (f"I tracked down every {esc(name)} operator I could find that puts a real 2026 price on the page, "
                 f"opened each package, and compared what you actually get for the money. "
                 f"{n_priced} publish a price (from {lo} to {hi})"
                 + (f" and {n_quote} quote per group" if n_quote else "")
                 + f"; here is how they stack up. Operator links open the booking page and are nofollow.")
    elif n_priced == 1:
        intro = (f"Few {esc(name)} operators post a fixed price; most quote per group once permits and porters are counted. "
                 f"Below is the one I found publishing a real 2026 figure ({price_str(priced[0])}), plus the operators that run it on a custom quote.")
    else:
        intro = (f"No operator I found publishes a fixed web price for the {esc(name)}; it is quoted per group once permits, "
                 f"porters and transport are counted. Below are the operators that actually run this route, with what each one includes, so you can compare quotes on a like-for-like basis.")

    # comparison table
    rows = []
    for p in pkgs:
        notable = esc(p.get('good','')).split(';')[0]
        if len(notable) > 70: notable = notable[:68].rstrip()+'…'
        book = f'<a href="{esc(p["pkg_url"])}" target="_blank" rel="nofollow noopener">{esc(p["operator"])}</a>'
        rows.append(f'<tr><td><strong>{esc(p["operator"])}</strong></td><td>{esc(p.get("days",""))}</td>'
                    f'<td>{price_str(p)}</td><td>{notable}</td><td>{book}</td></tr>')
    table = ('<table class="cmp-table"><thead><tr><th>Operator</th><th>Length</th><th>From (2026)</th>'
             '<th>Notable</th><th>Book</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>')

    # review cards
    cards = []
    for p in pkgs:
        badge = badge_for(p, cheapest_op)
        badge_html = f'<div class="rev-badge">{badge}</div>' if badge else ''
        pr = price_str(p)
        op_link = f'<a href="{esc(p["home"])}" target="_blank" rel="nofollow noopener">{esc(p["operator"])}</a>'
        meta = f'<span>🗓 <strong>{esc(p.get("days",""))}</strong></span><span>💷 <strong>{pr}</strong></span>'
        if p.get('meals'): meta += f'<span>🍽 <strong>{esc(p["meals"])}</strong></span>'
        tiers = f'<div class="rev-verdict">Group-size pricing: {esc(p["tiers"])}.</div>' if p.get('tiers') else ''
        cards.append(
          '<div class="rev">'
          f'<div class="rev-head"><div>{badge_html}<h3>{esc(p["operator"])}</h3>'
          f'<div class="rev-op">by {op_link} · {esc(p.get("days",""))} · from {pr}</div></div></div>'
          f'<div class="rev-meta">{meta}</div>'
          f'<div class="rev-pc"><div><h4 class="pros">What\'s good</h4><ul><li>{esc(p.get("good",""))}</li></ul></div>'
          f'<div><h4 class="cons">Could be better</h4><ul><li>{esc(p.get("could_be_better",""))}</li></ul></div></div>'
          f'{tiers}'
          f'<div class="rev-links">🔗 <a href="{esc(p["pkg_url"])}" target="_blank" rel="nofollow noopener">View this package</a> · '
          f'<a href="{esc(p["home"])}" target="_blank" rel="nofollow noopener">{esc(p["operator"])}</a></div>'
          '</div>')

    note = ('<div class="update-note"><strong>How these prices work.</strong> Most are per-person "from" rates, land-only, '
            'and often assume a group; solo and small-group rates run higher. Government royalty/permit fees, international '
            'flights, insurance and tips are usually extra. Always confirm group size, exact dates and what is included in '
            'writing before you pay a deposit.</div>')

    body = (f'<section class="section">\n<div style="max-width:860px;margin:0 auto;padding:0 1.5rem">\n'
            f'<span class="label">2026 Operator Prices</span>\n'
            f'<h2 class="section-title">{esc(name)}: Operators Compared</h2>\n'
            f'<p style="font-size:.96rem;color:var(--cream-2);line-height:1.7;margin:.6rem 0 1.2rem">{intro}</p>\n'
            f'{table}\n' + '\n'.join(cards) + f'\n{note}\n{CTA}\n</div>\n</section>')
    return '<!-- TREKCMP:START -->\n' + body + '\n<!-- TREKCMP:END -->'

def splice(route):
    f = os.path.join(ROOT, 'trekking', route, 'index.html')
    if not os.path.exists(f):
        print('  MISSING', route); return False
    data = json.load(open(os.path.join(DATA, route+'.json')))
    s = open(f).read()
    # 1. remove existing TREKCMP block
    s = re.sub(r'<!-- TREKCMP:START -->.*?<!-- TREKCMP:END -->\s*', '', s, flags=re.S)
    # 2. remove any leftover first-pass CTA section (contains entry=trekking)
    s = re.sub(r'<section class="section">(?:(?!</section>).)*?entry=trekking(?:(?!</section>).)*?</section>\s*', '', s, flags=re.S)
    block = build_section(route, data)
    anchor = '<!-- RELATED:START -->'
    if anchor not in s:
        print('  NO ANCHOR', route); return False
    s = s.replace(anchor, block + '\n\n' + anchor, 1)
    open(f, 'w').write(s)
    return True

if __name__ == '__main__':
    routes = sorted(DISPLAY.keys())
    ok = 0
    for r in routes:
        if os.path.exists(os.path.join(DATA, r+'.json')) and splice(r):
            n = len(json.load(open(os.path.join(DATA, r+'.json'))))
            print(f'  built {r} ({n} operators)'); ok += 1
    print(f'done: {ok}/{len(routes)} route pages')
