#!/usr/bin/env python3
"""
"Locally owned operators I recommend" - Faisal's own shortlist.

Reads recommended_operators.json. ONLY entries with "approved": true are
published - nothing appears on the site until Faisal has personally vetted an
operator. Each approved operator is shown on the tour/agency pages for the
regions it serves (plus /agencies and /tours). Idempotent; with no approved
entries it removes the section everywhere.

Entry fields:
  name, based_in, regions (e.g. ["hunza", "skardu"]), what (one line),
  why (Faisal's own words), whatsapp (digits, intl format), website, approved

Run after editing the JSON:  python3 recommended_operators.py
"""
import html
import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START, END = "<!-- REC-OPS:START -->", "<!-- REC-OPS:END -->"
e = html.escape

# page -> regions it shows ("*" = every approved operator)
PAGES = {
    "tours": "*", "agencies": "*",
    "tours/hunza": ["hunza"], "tours/hunza/honeymoon": ["hunza"], "agencies/hunza": ["hunza"],
    "tours/skardu": ["skardu"], "tours/skardu/honeymoon": ["skardu"], "agencies/skardu": ["skardu"],
    "agencies/k2-trekking": ["skardu", "k2"], "tours/fairy-meadows": ["fairy-meadows"],
    "tours/gilgit": ["gilgit"], "tours/chitral": ["chitral"], "tours/naran-kaghan": ["naran-kaghan"],
    "tours/from-islamabad": "*", "tours/from-lahore": "*", "tours/from-karachi": "*",
}


def wa(num, name):
    msg = f"Hi, Faisal from GB Guide recommended {name}. I'd like to ask about a trip."
    return f"https://wa.me/{num}?text={urllib.parse.quote(msg)}"


def card(o):
    links = []
    if o.get("whatsapp"):
        links.append(f'<a href="{e(wa(o["whatsapp"], o["name"]))}" target="_blank" rel="noopener">WhatsApp</a>')
    if o.get("website"):
        links.append(f'<a href="{e(o["website"])}" target="_blank" rel="noopener">Website</a>')
    return (f'<div class="rev"><div class="rev-head"><div><div class="rev-badge">Recommended by Faisal</div>'
            f'<h3>{e(o["name"])}</h3><div class="rev-op">Locally owned &middot; based in {e(o["based_in"])}</div></div></div>'
            f'<p style="margin:.3rem 0 .5rem">{e(o["what"])}</p>'
            f'<div class="rev-verdict"><strong>Why I recommend them:</strong> {e(o["why"])}</div>'
            f'<div class="rev-links">{" &middot; ".join(links)}</div></div>')


def section(ops):
    cards = "\n".join(card(o) for o in ops)
    return (f'{START}\n<section style="max-width:820px;margin:2.5rem auto;padding:0 1.5rem">'
            f'<h2 style="font-family:var(--fd);font-weight:500">Locally owned operators I recommend</h2>'
            f"<p>These are operators from Gilgit-Baltistan that I've checked out personally. "
            f'Mention GB Guide when you message them.</p>\n{cards}\n</section>\n{END}\n')


def main():
    data = json.loads((ROOT / "recommended_operators.json").read_text(encoding="utf-8"))
    approved = [o for o in data.get("operators", []) if o.get("approved") is True]
    shown = 0
    for rel, regions in PAGES.items():
        path = ROOT / rel / "index.html"
        if not path.exists():
            continue
        s = path.read_text(encoding="utf-8")
        new = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
        ops = approved if regions == "*" else [o for o in approved if set(o.get("regions", [])) & set(regions)]
        if ops:
            anchor = next((a for a in ("<!-- WA-HELP:START -->", "<!-- RELATED:START -->", "<!-- PHOTO-CREDITS:START -->", "<footer>") if a in new), None)
            new = new.replace(anchor, section(ops) + anchor, 1)
            shown += 1
        if new != s:
            path.write_text(new, encoding="utf-8")
    print(f"{len(approved)} approved operators; section shown on {shown} pages")


if __name__ == "__main__":
    main()
