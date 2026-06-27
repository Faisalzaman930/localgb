#!/usr/bin/env python3
"""Regenerate the global nav, mobile drawer, and mega-footer on every inner page
with depth-correct relative paths, so all section hubs + key pages are linked
sitewide (kills orphans). Homepage is handled separately (different chrome)."""
import re, os, glob

NAV = [("Destinations","destinations/"),("Mountains","mountains/"),("Treks","trekking/"),
       ("Things to Do","things-to-do/"),("Tours","tours/"),("Travel Tips","travel/"),
       ("Road Status","status/"),("Agencies","agencies/")]

REGIONS = [("Hunza Valley","hunza/"),("Skardu","skardu/"),("Gilgit","gilgit/"),
           ("Fairy Meadows","fairy-meadows/"),("Naltar","naltar/"),("Deosai","deosai/"),
           ("Ghizer","ghizer/"),("Astore","astore/"),("Gojal","gojal/"),
           ("Yasin","yasin/"),("Ishkoman","ishkoman/"),("Naran-Kaghan","naran-kaghan/")]
TREKS = [("All Treks","trekking/"),("K2 Base Camp","trekking/k2-base-camp/"),
         ("Concordia","trekking/concordia/"),("Rakaposhi BC","trekking/rakaposhi-base-camp/"),
         ("Rush Lake","trekking/rush-lake/"),("Mountains","mountains/"),
         ("K2","mountains/k2/"),("Nanga Parbat","mountains/nanga-parbat/"),("Rakaposhi","mountains/rakaposhi/")]
PLAN = [("Trip Planner","explore/"),("Best Time to Visit","travel/best-time-to-visit-gb/"),
        ("How to Reach","travel/islamabad-to-hunza/"),("What to Pack","travel/what-to-pack/"),
        ("NOC & Permits","travel/noc-permits-gb/"),("Budget Guide","travel/budget-gb-itinerary/"),
        ("Road & Pass Status","status/"),("Weather","weather/"),("Tours","tours/"),
        ("Choosing an Operator","agencies/"),("About GB Guide","about/"),("Blog","blog/")]

def li(items, p): return "".join(f'<li><a href="/{u.rstrip("/")}">{t}</a></li>' for t,u in items)
def nav_li(p): return "".join(f'<li><a href="/{u.rstrip("/")}">{t}</a></li>' for t,u in NAV)

def build_nav(p):
    return (f'<nav id="navbar" class="solid">\n'
        f'  <a href="/" class="nav-logo"><span class="l1">GB</span><span class="l2">Guide</span></a>\n'
        f'  <ul class="nav-links">{nav_li(p)}</ul>\n'
        f'  <a href="/explore" class="nav-cta" style="text-decoration:none">Plan Your Trip</a>\n'
        f'  <button class="nav-hamburger" id="navHamburger" aria-label="Menu"><span></span><span></span><span></span></button>\n'
        f'</nav>')

def build_drawer(p):
    return (f'<div class="nav-drawer" id="navDrawer">\n'
        f'  <ul>{nav_li(p)}</ul>\n'
        f'  <a href="/explore" class="nav-cta" style="text-decoration:none">Plan Your Trip</a>\n'
        f'</div>')

def build_footer(p):
    return (f'<footer>\n  <div class="footer-inner">\n    <div class="footer-top">\n'
        f'      <div><a href="/" class="footer-logo"><span class="l1">GB</span><span class="l2">Guide</span></a>'
        f'<p class="footer-tagline">"Gilgit-Baltistan, as only a local can tell it."</p>'
        f'<div class="footer-socials"><div class="social-btn">Y</div><div class="social-btn">I</div><div class="social-btn">T</div><div class="social-btn">F</div></div></div>\n'
        f'      <div><div class="footer-col-title">Regions</div><ul class="footer-links">{li(REGIONS,p)}</ul></div>\n'
        f'      <div><div class="footer-col-title">Treks &amp; Peaks</div><ul class="footer-links">{li(TREKS,p)}</ul></div>\n'
        f'      <div><div class="footer-col-title">Plan Your Trip</div><ul class="footer-links">{li(PLAN,p)}</ul></div>\n'
        f'    </div>\n'
        f'    <div class="footer-bottom"><span class="footer-copy">&copy; 2026 GB Guide · Last updated June 2026</span>'
        f'<span class="footer-made">Made with honesty, <span>from Gilgit-Baltistan.</span></span></div>\n'
        f'  </div>\n</footer>')

def main():
    changed=0; skipped=[]
    for f in glob.glob('**/index.html', recursive=True):
        if f=='index.html': continue  # homepage handled separately
        d=os.path.dirname(f)
        p='../'*(d.count('/')+1)
        h=open(f,encoding='utf-8').read(); orig=h
        h2=re.sub(r'<nav id="navbar".*?</nav>', lambda m: build_nav(p), h, count=1, flags=re.S)
        h2=re.sub(r'<div class="nav-drawer".*?</button>\s*</div>', lambda m: build_drawer(p), h2, count=1, flags=re.S)
        h2=re.sub(r'<footer>.*?</footer>', lambda m: build_footer(p), h2, count=1, flags=re.S)
        if ('<nav id="navbar"' not in h) or ('nav-drawer' not in h) or ('<footer>' not in h):
            skipped.append(f); continue
        if h2!=orig:
            open(f,'w',encoding='utf-8').write(h2); changed+=1
    print(f"updated nav+drawer+footer on {changed} inner pages")
    if skipped: print("SKIPPED (missing chrome):", skipped)

if __name__=='__main__': main()
