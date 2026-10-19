#!/usr/bin/env python3
"""
Free WhatsApp trip help, sitewide.

Idempotently adds (between markers, so re-runs replace instead of duplicating):
  - WA-FLOAT: a small floating "Free trip help" WhatsApp button on every page
  - WA-HELP:  a "Not sure? Ask me" section on the pages where people decide
              (homepage, contact, region hubs, hotels, tours, agencies, planner,
              itineraries) - placed above the photo credits / footer

Everything is self-contained inline HTML/CSS (the homepage doesn't load
main.css, and main.css is cached immutably), so no CSS version bump needed.

Run after adding pages:  python3 whatsapp_help.py   (then photo_credits.py)
"""

import html
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NUMBER = "923111915550"            # international format, no "+"
DISPLAY = "+92 311 1915550"

FLOAT_START, FLOAT_END = "<!-- WA-FLOAT:START -->", "<!-- WA-FLOAT:END -->"
HELP_START, HELP_END = "<!-- WA-HELP:START -->", "<!-- WA-HELP:END -->"

# Pages that get the full help section (path prefixes; "" = homepage).
HELP_PAGES = [
    "", "contact", "about", "planner", "destinations", "agencies", "tours", "trekking",
    "travel", "travel/7-day-itinerary", "travel/14-day-itinerary", "travel/budget-gb-itinerary",
    "hunza", "skardu", "gilgit", "fairy-meadows", "gojal", "ghizer", "naltar", "astore",
    "yasin", "deosai", "ishkoman", "naran-kaghan",
]
HELP_PREFIXES = ["agencies/", "tours/"]          # every page under these
HELP_SUFFIXES = ["/hotels"]                      # e.g. hunza/hotels

ICON = ('<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">'
        '<path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2'
        'a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7'
        '-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0'
        '-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 '
        '11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.1.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.2-.5-.3Z"/></svg>')

STYLE = """<style>
.wa-float{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));z-index:40;display:flex;align-items:center;gap:.5rem;padding:.7rem 1.05rem .7rem .85rem;border-radius:999px;background:#1A7F4B;color:#fff!important;font:600 .85rem/1 var(--fu,'Manrope',system-ui,sans-serif);text-decoration:none!important;box-shadow:0 6px 22px rgba(10,40,25,.28);transition:transform .2s,background .2s}
.wa-float:hover,.wa-float:focus-visible{background:#146B3F;transform:translateY(-2px)}
.wa-float:focus-visible{outline:3px solid #DEAD68;outline-offset:3px}
@media (max-width:560px){.wa-float{padding:.8rem}.wa-float span{display:none}body{padding-bottom:76px}}
@media print{.wa-float,.wa-help{display:none!important}}
.wa-help{max-width:1100px;margin:3rem auto 1rem;padding:0 1.5rem}
.wa-help-in{display:grid;grid-template-columns:1fr auto;gap:1.5rem 2.5rem;align-items:center;padding:clamp(1.6rem,4vw,2.6rem);border-radius:14px;background:#F2F7F3;border:1px solid rgba(26,127,75,.22)}
.wa-help-eyebrow{font:700 .66rem/1.2 var(--fu,'Manrope',system-ui,sans-serif);letter-spacing:.16em;text-transform:uppercase;color:#1A7F4B;margin-bottom:.6rem}
.wa-help h2{font-family:var(--fd,'Fraunces',Georgia,serif);font-weight:500;font-size:clamp(1.5rem,3vw,2.1rem);line-height:1.15;color:#1A1712;margin:0 0 .75rem}
.wa-help p{color:#4A453D;line-height:1.7;margin:0 0 .6rem;font-size:.98rem;max-width:62ch}
.wa-help ul{margin:.4rem 0 0;padding:0;list-style:none;color:#4A453D;font-size:.92rem;line-height:1.6}
.wa-help li{padding-left:1.35rem;position:relative;margin:.3rem 0}
.wa-help li::before{content:"";position:absolute;left:0;top:.55em;width:.55rem;height:.55rem;border-radius:50%;background:#1A7F4B}
.wa-help-cta{display:flex;flex-direction:column;align-items:center;gap:.55rem;text-align:center}
.wa-help-btn{display:inline-flex;align-items:center;gap:.55rem;padding:.95rem 1.5rem;border-radius:999px;background:#1A7F4B;color:#fff!important;font:700 .95rem/1 var(--fu,'Manrope',system-ui,sans-serif);text-decoration:none!important;white-space:nowrap;transition:background .2s}
.wa-help-btn:hover,.wa-help-btn:focus-visible{background:#146B3F}
.wa-help-btn:focus-visible{outline:3px solid #DEAD68;outline-offset:3px}
.wa-help-num{font:600 .85rem/1.3 var(--fu,'Manrope',system-ui,sans-serif);color:#4A453D}
.wa-help-free{font-size:.75rem;color:#6B6458}
@media (max-width:760px){.wa-help-in{grid-template-columns:1fr}.wa-help-cta{align-items:flex-start;text-align:left}}
</style>"""


def wa_link(topic: str) -> str:
    if topic:
        msg = f"Hi Faisal, I was reading your page on {topic} and I'm planning a trip to Gilgit-Baltistan."
    else:
        msg = "Hi Faisal, I found GB Guide and I'm planning a trip to Gilgit-Baltistan."
    msg += " Could you help me with a few questions?"
    return f"https://wa.me/{NUMBER}?text={urllib.parse.quote(msg)}"


SECTIONS = {"tours", "agencies", "trekking", "mountains", "things-to-do", "updates", "travel"}
NAMES = {"gb": "GB", "kkh": "KKH", "noc": "NOC", "k2": "K2", "atm": "ATM", "ptdc": "PTDC"}
MONTHS = {"january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december", "winter", "autumn"}
SMALL = {"to", "in", "of", "the", "and", "a", "from", "for", "vs"}


def title(slug: str) -> str:
    """Place-style title: 'fairy-meadows' -> 'Fairy Meadows', 'k2-base-camp' -> 'K2 Base Camp'."""
    ws = slug.split("-")
    return " ".join(NAMES.get(w) or (w if i and w in SMALL else w.capitalize()) for i, w in enumerate(ws))


def sub(slug: str) -> str:
    """Sub-page words in lower case: 'how-to-reach' -> ' - how to reach', 'hotels' -> ' hotels'."""
    ws = [NAMES.get(w) or (w.capitalize() if w in MONTHS else w) for w in slug.split("-")]
    if ws[0] == "in":                       # 'in-january' -> ' in January'
        return " " + " ".join(ws)
    return (" - " if len(ws) > 1 else " ") + " ".join(ws)


def page_topic(rel: str) -> str:
    """Short topic from the URL: 'hunza/hotels' -> 'Hunza hotels', 'tours/skardu' -> 'Skardu tours'."""
    if not rel:
        return ""
    parts = rel.split("/")
    if parts[0] in SECTIONS and len(parts) > 1:
        topic = title(parts[1]) + "".join(sub(x) for x in parts[2:])
        if parts[0] in ("tours", "agencies"):
            topic += " " + parts[0]
    else:
        topic = title(parts[0]) + "".join(sub(x) for x in parts[1:])
    return topic


def float_block(link: str) -> str:
    return (f'{FLOAT_START}\n{STYLE}\n<a class="wa-float" href="{html.escape(link)}" target="_blank" rel="noopener" '
            f'aria-label="Free trip help from Faisal on WhatsApp">{ICON}<span>Free trip help</span></a>\n{FLOAT_END}\n')


def help_block(link: str) -> str:
    return f"""{HELP_START}
<section class="wa-help" aria-labelledby="wa-help-title"><div class="wa-help-in">
  <div>
    <div class="wa-help-eyebrow">Free help &middot; WhatsApp</div>
    <h2 id="wa-help-title">Not sure where to start? Ask me.</h2>
    <p>I'm Faisal, from Gilgit-Baltistan. Message me your dates, budget and what you'd love to see, and I'll help you plan it. It's free - no booking, no catch.</p>
    <ul>
      <li>Honest answers on routes, roads, weather and how many days you really need</li>
      <li>Tour operators I recommend: locally owned, and more about the valleys than the profit</li>
      <li>Hotels and guesthouses that support sustainable eco-tourism and the families who run them</li>
    </ul>
  </div>
  <div class="wa-help-cta">
    <a class="wa-help-btn" href="{html.escape(link)}" target="_blank" rel="noopener">{ICON}Chat on WhatsApp</a>
    <div class="wa-help-num">{DISPLAY}</div>
    <div class="wa-help-free">Free, from a local</div>
  </div>
</div></section>
{HELP_END}
"""


def wants_help(rel: str) -> bool:
    return (rel in HELP_PAGES or any(rel.startswith(p) for p in HELP_PREFIXES)
            or any(rel.endswith(s) for s in HELP_SUFFIXES))


def strip(doc: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n?", "", doc, flags=re.S)


def main():
    n_float = n_help = 0
    for path in sorted(ROOT.rglob("index.html")):
        if any(p in path.parts for p in (".git", "research", "node_modules", "preview")):
            continue
        rel = str(path.parent.relative_to(ROOT)).replace("\\", "/")
        rel = "" if rel == "." else rel
        doc = path.read_text(encoding="utf-8")
        new = strip(strip(doc, FLOAT_START, FLOAT_END), HELP_START, HELP_END)
        link = wa_link(page_topic(rel))

        if "</body>" in new:
            new = new.replace("</body>", float_block(link) + "</body>", 1)
            n_float += 1
        if wants_help(rel):
            anchor = next((a for a in ("<!-- EMAIL -->", "<!-- PHOTO-CREDITS:START -->", "<footer>") if a in new), None)
            if anchor:
                new = new.replace(anchor, help_block(link) + anchor, 1)
                n_help += 1
        if new != doc:
            path.write_text(new, encoding="utf-8")
    print(f"WhatsApp button on {n_float} pages; help section on {n_help} pages")


if __name__ == "__main__":
    main()
