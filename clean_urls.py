#!/usr/bin/env python3
"""Convert internal links/assets to clean, root-relative URLs:
  ../../hunza/baltit-fort/index.html  -> /hunza/baltit-fort
  ../index.html                       -> /
  ../../css/main.css?v=1              -> /css/main.css?v=1
  images/foo.webp                     -> /images/foo.webp
Root-relative removes /index.html and the fragile ../ depth math, and matches
the canonical URLs. Skips external/mailto/tel/#/JS-template (${) values.
Usage: python3 clean_urls.py [--dry FILE]
"""
import re, os, glob, sys

def to_clean(d, val):
    # split query/fragment
    m = re.match(r'^([^?#]*)([?#].*)?$', val)
    base, tail = m.group(1), (m.group(2) or '')
    if (not base) or base.startswith(('http://','https://','mailto:','tel:','//','#','data:')) or '${' in base:
        return None
    # resolve to absolute site path
    b = base
    if b.startswith('/'):
        abss = b.lstrip('/')
    else:
        abss = os.path.normpath(os.path.join(d, b))
        if abss == '.': abss = ''
    abss = abss.strip('/')
    # map to clean URL
    if abss == 'index.html' or abss == '':
        clean = '/'
    elif abss.endswith('/index.html'):
        clean = '/' + abss[:-len('/index.html')]
    elif abss.endswith('.html'):
        clean = '/' + abss[:-len('.html')]
    else:
        clean = '/' + abss   # asset (css/js/images/...)
    return clean + tail

def convert(html, d):
    def attr(m):
        a, q, val = m.group(1), m.group(2), m.group(3)
        nv = to_clean(d, val)
        return f'{a}={q}{nv}{q}' if nv is not None else m.group(0)
    html = re.sub(r'\b(href|src)=(["\'])([^"\']+)\2', attr, html)
    def urlf(m):
        q, val = m.group(1), m.group(2)
        nv = to_clean(d, val)
        return f'url({q}{nv}{q})' if nv is not None else m.group(0)
    html = re.sub(r'url\((["\']?)([^)\'"]+)\1\)', urlf, html)
    return html

def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--dry':
        f = sys.argv[2]; d = os.path.dirname(f)
        out = convert(open(f,encoding='utf-8').read(), d)
        import difflib
        old = open(f,encoding='utf-8').read().splitlines()
        for line in difflib.unified_diff(old, out.splitlines(), lineterm='', n=0):
            if line.startswith(('+','-')) and not line.startswith(('+++','---')):
                print(line[:160])
        return
    n = 0
    for f in glob.glob('**/index.html', recursive=True):
        d = os.path.dirname(f)
        h = open(f, encoding='utf-8').read()
        h2 = convert(h, d)
        if h2 != h:
            open(f,'w',encoding='utf-8').write(h2); n += 1
    print(f"cleaned URLs on {n} pages")

if __name__ == '__main__':
    main()
