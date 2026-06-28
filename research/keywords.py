#!/usr/bin/env python3
"""Free keyword harvester via Google Autocomplete (no API key, no Semrush).
Expands each seed with modifiers + a–z, dedupes, scores by how often Google
surfaces a phrase (a rough demand proxy). Output: keywords.csv
Usage: python3 keywords.py
"""
import urllib.parse, urllib.request, json, time, csv, string
from collections import Counter

DESTS = ["skardu","hunza","gilgit","naran kaghan","fairy meadows","deosai",
         "gilgit baltistan","northern areas"]
BASES = ["{d} tour packages","{d} tour","{d} trip","{d} travel package",
         "{d} tour package from","{d} tour package price"]
SUFFIXES = ["", " from", " by", " price", " cost", " best", " cheap", " 2026",
            " for", " for couple", " for family", " 3 day", " 5 day", " 7 day"] + \
           [" "+c for c in string.ascii_lowercase]
UA = "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/126 Safari/537.36"

def ac(q):
    u = "https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=pk&q=" + urllib.parse.quote(q)
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        return json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8","ignore"))[1]
    except Exception:
        return []

counts, seen_for = Counter(), {}
seeds = [b.format(d=d) for d in DESTS for b in BASES]
print(f"{len(seeds)} seeds × {len(SUFFIXES)} suffixes...")
for i, s in enumerate(seeds):
    for suf in SUFFIXES:
        for kw in ac(s + suf):
            kw = kw.lower().strip()
            if any(d.split()[0] in kw for d in DESTS) and ("tour" in kw or "trip" in kw or "package" in kw or "travel" in kw):
                counts[kw] += 1
        time.sleep(0.15)
    print(f"  {i+1}/{len(seeds)}  {s[:40]}  (uniq so far: {len(counts)})")

rows = counts.most_common()
with open("keywords.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["keyword","score"])
    for kw,c in rows: w.writerow([kw,c])
print(f"\n✅ {len(rows)} unique keywords → keywords.csv")
# quick buckets
def has(*t): return [k for k,_ in rows if all(x in k for x in t)]
print("from-city variants:", len([k for k,_ in rows if " from " in k]))
print("by air/road:", len([k for k,_ in rows if "by air" in k or "by road" in k]))
print("price/cost:", len([k for k,_ in rows if "price" in k or "cost" in k]))
