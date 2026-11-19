#!/usr/bin/env python3
"""Render checks for the exported static tree: overflow + 20px text + screenshots.

Serves out/ on 127.0.0.1:8133 and, for each of the 28 routes, measures at
320 / 360 / 390 / 1440 px widths:
  - horizontal overflow: documentElement.scrollWidth - innerWidth (must be 0)
  - body computed font-size at 1440 and 390 (must be 20px)
  - worst offending element when overflow > 0
Screenshots: viewport shots desktop 1440x900 + mobile 390x844 for every page;
full-page shots for homepage + the 8 newest pages.
Usage: python3 qa/render_check.py [outdir]
"""
import json
import os
import subprocess
import sys
import time

BASE = "/home/hatch/workspace/fort-myers-php"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "out")
SHOTS = os.path.join(BASE, "qa", "screenshots")
os.makedirs(SHOTS, exist_ok=True)

ROUTES = ["", "water-removal", "drying", "sewage-cleanup", "ac-leak", "ceiling-leak",
          "condo-leak", "cast-iron-pipe", "vacant-home", "first-hour-checklist",
          "cost", "insurance", "burst-pipe", "mobile-home", "slab-leak", "flood-cleanup",
          "cape-coral", "lehigh-acres", "areas", "water-heater-leak",
          "appliance-leak", "floors", "cabinets", "commercial", "north-fort-myers",
          "fort-myers-beach", "estero", "bonita-springs", "how-it-works", "contact",
          "about", "privacy-policy", "terms", "disclaimer"]
FULLPAGE = {"", "fort-myers-beach", "estero", "bonita-springs", "how-it-works",
            "contact", "about"}
PORT = 8133

JS_MEASURE = """() => {
  const de = document.documentElement;
  const over = de.scrollWidth - window.innerWidth;
  let worst = null, worstW = 0;
  if (over > 0) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.right > window.innerWidth + 0.5 && r.width > worstW) {
        worstW = r.width;
        worst = el.tagName + '.' + String(el.className).split(' ')[0]
          + ' right=' + Math.round(r.right) + ' w=' + Math.round(r.width);
      }
    }
  }
  return { over, worst, fs: getComputedStyle(document.body).fontSize };
}"""

server = subprocess.Popen(
    ["python3", "-m", "http.server", str(PORT), "-d", OUT],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=BASE)
time.sleep(1.5)

from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug in ROUTES:
            url = f"http://127.0.0.1:{PORT}/{'/' + slug + '/' if slug else ''}"
            name = slug or "home"
            row = {"slug": name, "overflow": {}, "font": {}, "worst": {}}
            for w in [320, 360, 390, 1440]:
                ctx = browser.new_context(viewport={"width": w, "height": 844 if w < 500 else 900})
                page = ctx.new_page()
                page.goto(url, wait_until="load", timeout=30000)
                page.wait_for_timeout(400)
                m = page.evaluate(JS_MEASURE)
                row["overflow"][str(w)] = m["over"]
                row["worst"][str(w)] = m["worst"]
                if w in (1440, 390):
                    row["font"][str(w)] = m["fs"]
                if w in (1440, 390) and slug in FULLPAGE:
                    # content-visibility: auto defers below-fold blocks until
                    # they intersect the viewport, and Chrome discards their
                    # rendering again once they leave it — so neither a plain
                    # full_page capture nor a scroll-through (tried both)
                    # shows them. For the full-page proof shot only, force
                    # them visible: this is exactly what a scrolling visitor
                    # sees at each section, and it changes no content.
                    page.add_style_tag(content=".faq-list, ol.steps, .table-wrap, .kinds-grid { content-visibility: visible !important; }")
                    page.wait_for_timeout(400)
                if w == 1440:
                    page.screenshot(path=f"{SHOTS}/{name}-desktop.png")
                    if slug in FULLPAGE:
                        page.screenshot(path=f"{SHOTS}/{name}-desktop-full.png", full_page=True)
                if w == 390:
                    page.screenshot(path=f"{SHOTS}/{name}-mobile.png")
                    if slug in FULLPAGE:
                        page.screenshot(path=f"{SHOTS}/{name}-mobile-full.png", full_page=True)
                ctx.close()
            print(json.dumps(row), flush=True)
        browser.close()
finally:
    server.terminate()
print("render check done")
