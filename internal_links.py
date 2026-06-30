#!/usr/bin/env python3
"""Inject a 'Plan your <Town> trip' cluster block that cross-links each town's
Guide / Tours / Hotels / Restaurants / Things-to-do + the treks reachable from
it. Closes the tours<->stay<->eat gap and feeds inbound links to the weak
restaurant + long-tail trek pages. Idempotent via CLUSTER:START/END markers."""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
def exists(url):  # url like '/hunza/hotels'
    return os.path.exists(os.path.join(ROOT, url.strip('/'), 'index.html'))

TREK_LABEL = {
 'k2-base-camp':'K2 Base Camp Trek','concordia':'Concordia Trek','gondogoro-la':'Gondogoro La Trek',
 'biafo-hispar-snow-lake':'Snow Lake Trek','rush-lake':'Rush Lake Trek','rakaposhi-base-camp':'Rakaposhi Base Camp',
 'masherbrum-base-camp':'Masherbrum Base Camp','laila-peak-base-camp':'Laila Peak Trek','spantik-base-camp':'Spantik Trek',
 'hushe-valley':'Charakusa / Hushe Trek','nanga-parbat-base-camp':'Nanga Parbat Base Camp',
 'nanga-parbat-rupal-face':'Nanga Parbat Rupal Trek','naltar-lakes':'Naltar Lakes','haramosh-kutwal-lake':'Kutwal Lake Trek',
 'karambar-lake':'Karambar Lake Trek'}

# town -> (Display, eat_url, [relevant trek slugs])
TOWNS = {
 'hunza':  ('Hunza',  '/hunza/food',         ['rush-lake','rakaposhi-base-camp','naltar-lakes']),
 'skardu': ('Skardu', '/skardu/restaurants', ['k2-base-camp','concordia','masherbrum-base-camp','laila-peak-base-camp','spantik-base-camp','hushe-valley']),
 'gilgit': ('Gilgit', '/gilgit/restaurants', ['naltar-lakes','haramosh-kutwal-lake','rakaposhi-base-camp']),
 'naran-kaghan': ('Naran-Kaghan', None, []),
 'fairy-meadows':('Fairy Meadows', None, ['nanga-parbat-base-camp','nanga-parbat-rupal-face']),
 'chitral': ('Chitral', None, []),
}

def cluster_block(town, current_url):
    disp, eat, treks = TOWNS[town]
    items = []  # (category, url, label)
    def add(cat, url, label):
        if url and url != current_url and exists(url):
            items.append((cat, url, label))
    add('Guide',  f'/{town}',               f'{disp} Travel Guide')
    add('Tours',  f'/tours/{town}',         f'{disp} Tour Packages')
    add('Stay',   f'/{town}/hotels',        f'Best Hotels in {disp}')
    if eat: add('Eat', eat,                 f'Best Restaurants in {disp}')
    add('Do',     f'/{town}/things-to-do',  f'Things to Do in {disp}')
    add('See',    f'/{town}/places-to-visit',f'Places to Visit in {disp}')
    for slug in treks:
        add('Trek', f'/trekking/{slug}', TREK_LABEL.get(slug, slug))
    if len(items) < 2:
        return None
    cells = ''.join(f'<a href="{u}"><span>{cat}</span>{lbl}</a>' for cat,u,lbl in items)
    return ('<!-- CLUSTER:START -->\n'
            f'<div class="cluster-links"><h2>Plan your {disp} trip</h2>'
            f'<div class="cluster-grid">{cells}</div></div>\n'
            '<!-- CLUSTER:END -->')

def inject(path, town):
    url = '/' + os.path.dirname(path)
    if not os.path.exists(path): return False
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<!-- CLUSTER:START -->.*?<!-- CLUSTER:END -->\s*', '', s, flags=re.S)
    block = cluster_block(town, url)
    if not block: return False
    if '<!-- RELATED:START -->' in s:
        s = s.replace('<!-- RELATED:START -->', block + '\n\n<!-- RELATED:START -->', 1)
    elif '<footer>' in s:
        s = s.replace('<footer>', block + '\n\n<footer>', 1)
    else:
        return False
    open(path, 'w', encoding='utf-8').write(s)
    return True

if __name__ == '__main__':
    n = 0
    for town, (disp, eat, treks) in TOWNS.items():
        targets = [f'{town}/index.html', f'tours/{town}/index.html',
                   f'{town}/hotels/index.html', f'{town}/things-to-do/index.html']
        if eat: targets.append(eat.strip('/') + '/index.html')
        for t in targets:
            if inject(t, town):
                print('  + cluster block ->', '/'+os.path.dirname(t)); n += 1
    print(f'done: injected/updated {n} pages')
