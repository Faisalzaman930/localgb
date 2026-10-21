#!/usr/bin/env python3
"""
Multi-operator tour comparison for /tours/* pages.

Reads research/tours/<slug>-compare.json (hand-written: own-words itineraries,
prices/dates re-checked on the operators' live sites) and writes the comparison
between <!-- TOUR-COMPARE:START --> / END markers in the page, plus the page's
ItemList JSON-LD. Re-run after editing the JSON:

    python3 research/build_tour_compare.py hunza
"""
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- TOUR-COMPARE:START -->", "<!-- TOUR-COMPARE:END -->"
DOMAIN = "https://www.gilgitbaltistanguide.com"
WA = "923111915550"
e = html.escape


def ext(url, text):
    return f'<a href="{e(url)}" target="_blank" rel="nofollow noopener">{e(text)}</a>'


def wa_match(place):
    msg = (f"Hi Faisal, I'm looking at {place} tour packages. My dates: ... Group size: ... "
           "Budget: ... Could you recommend a locally owned operator?")
    return f"https://wa.me/{WA}?text={urllib.parse.quote(msg)}"


def render(d):
    ops, pk = d["operators"], d["packages"]
    n_ops = len({p["op"] for p in pk})
    rows = "".join(
        f'<tr><td><a href="#{p["id"]}"><strong>{e(p["name"])}</strong></a></td>'
        f'<td>{e(ops[p["op"]]["name"])}</td><td>{p["days"]}</td>'
        f'<td>From {e(p["start"])}<br><span style="font-size:.76rem;color:var(--cream-2)">{e(p["travel"])}</span></td>'
        f'<td>{e(p["price"])}</td></tr>' for p in pk)
    best = "".join(f'<li><strong>{e(p["best"])}</strong> - <a href="#{p["id"]}">{e(p["name"])}</a> '
                   f'({e(ops[p["op"]]["name"])}, {e(p["price"])})</li>' for p in pk)
    place = d["place"]
    groups = [(g["label"], g["min"], g["max"], g["why"]) for g in d["day_groups"]]
    days_html = "".join(
        f'<li><strong>{label}:</strong> {why} ' + ", ".join(f'<a href="#{p["id"]}">{e(p["name"])}</a>' for p in pk if lo <= p["days"] <= hi) + '.</li>'
        for label, lo, hi, why in groups if any(lo <= p["days"] <= hi for p in pk))
    notes = "".join(f"<p>{e(n)}</p>" for n in d.get("notes", []))
    cards = []
    for i, p in enumerate(pk, 1):
        op = ops[p["op"]]
        itin = "".join(f"<tr><td>Day {j}</td><td>{e(t)}</td></tr>" for j, t in enumerate(p["itinerary"], 1))
        good = "".join(f"<li>{e(x)}</li>" for x in p["good"])
        watch = "".join(f"<li>{e(x)}</li>" for x in p["watch"])
        cards.append(f'''<div class="rev" id="{p["id"]}">
<div class="rev-head"><div><div class="rev-badge">#{i} &middot; Best for: {e(p["best"])}</div><h3>{e(p["name"])}</h3><div class="rev-op">by {ext(op["url"], op["name"])} &middot; {e(op["based"])}</div></div></div>
<div class="rev-meta"><span>🗓 <strong>{p["days"]} days</strong></span><span>📍 <strong>Starts {e(p["start"])}</strong></span><span>🚐 <strong>{e(p["travel"])}</strong></span><span>💷 <strong>{e(p["price"])}</strong></span><span>🍽 <strong>{e(p["meals"])}</strong></span></div>
<h4>Day by day</h4><table class="rev-itin"><tbody>{itin}</tbody></table>
<div class="rev-pc"><div><h4 class="pros">What's good</h4><ul>{good}</ul></div><div><h4 class="cons">Check before you book</h4><ul>{watch}</ul></div></div>
<div class="rev-links">Full details and booking: {ext(p["url"], op["name"] + " - " + p["name"])}</div>
</div>''')
    return f'''{START}
<p>I'm from Gilgit-Baltistan, so here's the honest comparison: <strong>{len(pk)} {place} tour packages from {n_ops} different operators</strong> - {d["mix"]}. I read every itinerary day by day and rewrote it below in plain words, so you can see exactly where each trip spends its time.</p>
<div class="callout"><h3>How I compared them</h3><p>Packages, prices and dates were re-checked on each operator's own website on {e(d["checked"])}. Many operators don't publish prices ("on request") - that's normal in Pakistan, and I say so rather than guess. Where an operator says where it's based, I show it.</p>{notes}</div>
{d.get("top_html", "")}<h2>At a glance - {len(pk)} {place} packages compared</h2>
<div style="overflow-x:auto"><table class="cmp-table"><thead><tr><th>Package</th><th>Operator</th><th>Days</th><th>Route</th><th>Price</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Which one is best for you?</h2><ul>{best}</ul>
<h2>How many days do you need for a {place} tour?</h2><ul>{days_html}</ul><p>{d["days_tip"]}</p>
<div class="article-cta"><h3>Not sure which to book? Ask me.</h3><p>Send me your dates, group size and budget on WhatsApp. I'll tell you which of these fits, or match you with a locally owned operator I trust. It's free.</p><a href="{e(wa_match(place))}" class="btn-primary" target="_blank" rel="noopener">Get matched on WhatsApp &rarr;</a></div>
<h2>The {len(pk)} packages, day by day</h2>
{chr(10).join(cards)}
{d.get("footer_html", "")}
{END}'''


def itemlist(d, page):
    return {"@context": "https://schema.org", "@type": "ItemList",
            "name": f"{d['place']} tour packages compared ({len(d['packages'])})",
            "url": f"{DOMAIN}/{page}",
            "itemListElement": [{"@type": "ListItem", "position": i, "name": p["name"], "url": p["url"]}
                                for i, p in enumerate(d["packages"], 1)]}


def main(slug):
    d = json.loads((ROOT / "research" / "tours" / f"{slug}-compare.json").read_text(encoding="utf-8"))
    path = ROOT / d["page"] / "index.html"
    s = path.read_text(encoding="utf-8")
    block = render(d)
    if START in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, s, flags=re.S)
    else:  # first run: replace the old single-operator review section
        a = s.index(d.get("replace_from", "<p>I only include packages"))
        b = s.index("<h2>What&#x27;s usually included") if "<h2>What&#x27;s usually included" in s else s.index("<h2>What's usually included")
        s = s[:a] + block + "\n" + s[b:]
    # ItemList JSON-LD
    def swap(m):
        try:
            data = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        if isinstance(data, dict) and data.get("@type") == "ItemList":
            return m.group(1) + json.dumps(itemlist(d, d["page"]), ensure_ascii=False) + m.group(3)
        return m.group(0)
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', swap, s, flags=re.S)
    path.write_text(s, encoding="utf-8")
    print(f"{d['page']}: {len(d['packages'])} packages from {len({p['op'] for p in d['packages']})} operators")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "hunza")
