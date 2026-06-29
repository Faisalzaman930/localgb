#!/usr/bin/env python3
"""Inject a contextual "Related guides" block into every inner page (idempotent),
linking hub->children, child->hub+siblings, and curated cross-cluster pairs.
This distributes link equity and removes orphans. Anchor text = each target's
real <title> (descriptive, good for SEO)."""
import re, os, glob
from collections import defaultdict

START, END = "<!-- RELATED:START -->", "<!-- RELATED:END -->"

# Curated cross-cluster links (page -> extra targets) for high-value semantic
# relationships and to rescue standalone pages with no hub-parent.
CROSS = {
    "mountains/k2": ["trekking/k2-base-camp"],
    "mountains/rakaposhi": ["trekking/rakaposhi-base-camp"],
    "mountains/nanga-parbat": ["trekking/nanga-parbat-base-camp", "fairy-meadows"],
    "mountains/spantik": ["trekking/spantik-base-camp"],
    "mountains/masherbrum": ["trekking/masherbrum-base-camp", "trekking/hushe-valley"],
    "mountains/laila-peak": ["trekking/laila-peak-base-camp", "trekking/hushe-valley"],
    "mountains/broad-peak": ["trekking/concordia", "trekking/k2-base-camp"],
    "mountains/gasherbrum": ["trekking/concordia"],
    "mountains/haramosh-peak": ["trekking/haramosh-kutwal-lake", "gilgit/haramosh-valley"],
    "mountains/trango-towers": ["things-to-do/rock-climbing-trango"],
    "trekking/k2-base-camp": ["mountains/k2", "tours/k2-base-camp" if os.path.isdir("tours/k2-base-camp") else "tours"],
    "trekking/rakaposhi-base-camp": ["mountains/rakaposhi", "hunza"],
    "trekking/nanga-parbat-base-camp": ["mountains/nanga-parbat", "fairy-meadows"],
    "trekking/spantik-base-camp": ["mountains/spantik"],
    "trekking/masherbrum-base-camp": ["mountains/masherbrum", "trekking/hushe-valley"],
    "trekking/laila-peak-base-camp": ["mountains/laila-peak", "trekking/hushe-valley"],
    "trekking/concordia": ["mountains/k2", "mountains/broad-peak", "trekking/gondogoro-la"],
    "trekking/haramosh-kutwal-lake": ["mountains/haramosh-peak", "gilgit/haramosh-valley"],
    "trekking/rush-lake": ["mountains/rakaposhi", "hunza/shimshal-valley"],
    "trekking/naltar-lakes": ["naltar", "things-to-do/skiing-naltar"],
    # destinations <-> tours
    "hunza": ["tours/hunza", "trekking/rakaposhi-base-camp"],
    "skardu": ["tours/skardu", "deosai", "trekking/k2-base-camp"],
    "fairy-meadows": ["tours/fairy-meadows", "trekking/nanga-parbat-base-camp", "mountains/nanga-parbat"],
    "naran-kaghan": ["tours/naran-kaghan", "travel/karakoram-highway", "fairy-meadows"],
    "deosai": ["skardu", "skardu/sheosar-lake", "things-to-do/stargazing-gb"],
    "naltar": ["things-to-do/skiing-naltar", "trekking/naltar-lakes", "gilgit"],
    "gilgit": ["naltar", "trekking/haramosh-kutwal-lake"],
    "tours/hunza": ["hunza","hunza/places-to-visit","hunza/things-to-do","hunza/attabad-lake","hunza/baltit-fort","hunza/khunjerab-pass","hunza/karimabad","hunza/best-time-to-visit"],
    "tours/skardu": ["skardu","skardu/tourist-places","skardu/things-to-do","skardu/shangrila-resort","skardu/shigar-valley","skardu/khaplu","skardu/satpara-lake","deosai"],
    "tours/k2-base-camp": ["trekking/k2-base-camp", "mountains/k2"],
    "tours/fairy-meadows": ["fairy-meadows","fairy-meadows/camping","fairy-meadows/how-to-reach","mountains/nanga-parbat","trekking/nanga-parbat-base-camp"],
    "tours/naran-kaghan": ["naran-kaghan","fairy-meadows","travel/karakoram-highway","mountains/nanga-parbat","things-to-do/river-rafting"],
    "tours/gilgit": ["gilgit","gilgit/places-to-visit","gilgit/things-to-do","gilgit/bagrot-valley","gilgit/kargah-buddha","naltar","trekking/naltar-lakes"],
    "tours/gilgit-baltistan": ["hunza","skardu","gilgit","deosai","fairy-meadows","naran-kaghan"],
    "tours/chitral": ["things-to-do/shandur-polo-festival","tours/gilgit-baltistan","gilgit"],
    "tours/from-islamabad": ["tours/hunza","tours/skardu","tours/naran-kaghan","tours/gilgit-baltistan","hunza","skardu"],
    "tours/from-lahore": ["tours/naran-kaghan","tours/hunza","tours/skardu","tours/gilgit-baltistan","naran-kaghan","hunza"],
    "tours/from-karachi": ["tours/hunza","tours/skardu","tours/gilgit-baltistan","tours/naran-kaghan","hunza","skardu"],
    # standalone-page rescue
    "kkh-map": ["karakoram-highway", "travel/karakoram-highway", "status"],
    "karakoram-highway": ["travel/karakoram-highway", "kkh-map", "hunza/khunjerab-pass"],
    "travel/karakoram-highway": ["karakoram-highway", "kkh-map", "status"],
    "atm-locator": ["status", "travel/what-to-pack", "travel/budget-gb-itinerary"],
    "status": ["atm-locator", "weather", "travel/karakoram-highway"],
    "weather": ["travel/best-time-to-visit-gb", "status"],
}

def clean_title(h):
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    if not m: return None
    t = re.sub(r"\s*[—|]\s*GB Guide.*$", "", m.group(1)).strip()
    t = re.sub(r"\s*—\s*$", "", t)
    return t or None

def main():
    pages = sorted(os.path.dirname(f) or "" for f in glob.glob("**/index.html", recursive=True))
    pages = [p for p in pages if p]  # exclude home
    titles = {}
    for p in pages:
        titles[p] = clean_title(open(p + "/index.html", encoding="utf-8").read()) or p.split("/")[-1].replace("-", " ").title()
    children = defaultdict(list)   # hub -> [child pages]
    by_hub = defaultdict(list)     # top segment -> pages
    for p in pages:
        seg = p.split("/")
        by_hub[seg[0]].append(p)
        if len(seg) >= 2:
            children["/".join(seg[:-1])].append(p)

    def related_for(p):
        seg = p.split("/")
        is_hub = p in children
        out = []
        if seg[0]=="tours" and not is_hub:                # tour pages: link destination guides first
            out = [c for c in CROSS.get(p,[]) if c in titles]
            if "tours" in titles or "tours" in by_hub: out.append("tours")
            out += [s for s in children.get("tours",[]) if s!=p][:2]
            seen=set(); final=[]
            for t in out:
                if t and t!=p and t in titles and t not in seen: seen.add(t); final.append(t)
            return final[:8]
        if is_hub:                                # hub/parent: link ALL children (uncapped)
            out += children[p]
        if len(seg) >= 2:                         # this page is a child
            parent = "/".join(seg[:-1])
            if parent in titles or parent in by_hub: out.append(parent)
            sibs = [s for s in children.get(parent, []) if s != p]
            out += sibs[:6]
        out += [c for c in CROSS.get(p, []) if c in titles]
        # dedup, drop self & missing
        seen = set(); final = []
        for t in out:
            if t and t != p and t in titles and t not in seen:
                seen.add(t); final.append(t)
        # hubs list every child; child/standalone pages capped for tidiness
        return final if is_hub else final[:8]

    EYEBROW = {  # short tag per top section for the anchor sub-label
        "hunza":"Hunza","skardu":"Skardu","gilgit":"Gilgit","fairy-meadows":"Fairy Meadows",
        "trekking":"Trek","mountains":"Peak","things-to-do":"Things to Do","tours":"Tour",
        "travel":"Travel","agencies":"Operators","ghizer":"Ghizer","naltar":"Naltar",
        "yasin":"Yasin","ishkoman":"Ishkoman","astore":"Astore","deosai":"Deosai","gojal":"Gojal",
    }
    n = 0
    for p in pages:
        rel = related_for(p)
        if len(rel) < 2:   # skip pages with too little to relate
            continue
        cards = ""
        for t in rel:
            sub = EYEBROW.get(t.split("/")[0], "Guide")
            cards += f'<a href="/{t}">{titles[t]}<span>{sub}</span></a>'
        block = (f"{START}\n<section class=\"related-links\"><div class=\"related-inner\">"
                 f"<h2 class=\"related-title\">Related guides &amp; nearby</h2>"
                 f"<div class=\"related-grid\">{cards}</div></div></section>\n{END}")
        f = p + "/index.html"; h = open(f, encoding="utf-8").read()
        if START in h:
            h = re.sub(re.escape(START) + r".*?" + re.escape(END), block, h, flags=re.S)
        elif "<footer>" in h:
            h = h.replace("<footer>", block + "\n<footer>", 1)
        else:
            continue
        open(f, "w", encoding="utf-8").write(h); n += 1
    print(f"injected related-links block on {n} pages")

if __name__ == "__main__":
    main()
