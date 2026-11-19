#!/usr/bin/env python3
"""Diagnosis for the five-fix round (2026-11-19 ~21:22+ PKT):
Task 1 kinds-grid render + Task 4 details-card icons + Task 2/3 nav/footer state.
Serves out/ on 127.0.0.1:8322 (already running) and renders with bundled Chromium.
Screenshots + computed-style dumps go to qa/screenshots-five-fixes/.
Usage: python3 qa/diag-five-fixes.py
"""
import json, os
from playwright.sync_api import sync_playwright

BASE = "/home/hatch/workspace/fort-myers-php"
OUT = os.path.join(BASE, "out")
SHOTS = os.path.join(BASE, "qa", "screenshots-five-fixes")
os.makedirs(SHOTS, exist_ok=True)
SERVER = "http://127.0.0.1:8322"

JS_KINDS = """() => {
  const grids = [...document.querySelectorAll('.kinds-grid')];
  const grid = grids.find(g => g.querySelectorAll('.kind-card.has-photo').length > 0);
  if (!grid) return {error: 'no photo kinds grid'};
  const cards = [...grid.querySelectorAll('.kind-card.has-photo')].map((c, i) => {
    const h3 = c.querySelector('h3'), p = c.querySelector('p'), a = c.querySelector('a');
    const scrim = c.querySelector('.kind-scrim');
    const cs = getComputedStyle(c), hs = h3 ? getComputedStyle(h3) : null,
          ps = p ? getComputedStyle(p) : null, as = a ? getComputedStyle(a) : null,
          ss = scrim ? getComputedStyle(scrim) : null;
    const r = c.getBoundingClientRect();
    return {i, h3: h3 ? h3.textContent.slice(0,40) : null,
      cardBox: [r.x, r.y, r.width, r.height].map(Math.round),
      bgImage: cs.backgroundImage.slice(0, 80),
      h3Color: hs && hs.color, pColor: ps && ps.color, aColor: as && as.color,
      scrimDisplay: ss && ss.display, scrimBg: ss && ss.backgroundImage.slice(0, 120),
      scrimBox: scrim ? [scrim.getBoundingClientRect().x, scrim.getBoundingClientRect().y, scrim.getBoundingClientRect().width, scrim.getBoundingClientRect().height].map(v => Math.round(v)) : null,
      h3Box: h3 ? [h3.getBoundingClientRect().x, h3.getBoundingClientRect().y, h3.getBoundingClientRect().width, h3.getBoundingClientRect().height].map(v => Math.round(v)) : null};
  });
  const gr = grid.getBoundingClientRect(); return {cards, gridBox: [gr.x, gr.y, gr.width, gr.height].map(v => Math.round(v))};
}"""

JS_DETAILS = """() => {
  const card = document.querySelector('.details-card');
  if (!card) return {error: 'no details card'};
  const cr = card.getBoundingClientRect();
  const rows = [...card.querySelectorAll('.detail-row')].map((row, i) => {
    const icon = row.querySelector('.detail-icon');
    const dt = row.querySelector('dt'), dd = row.querySelector('dd');
    const label = row.querySelector('.detail-label');
    const box = el => { if (!el) return null; const r = el.getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(v => Math.round(v)); };
    const ics = icon ? getComputedStyle(icon) : null;
    return {i, label: label ? label.textContent.trim().slice(0, 30) : null,
      rowBox: box(row), iconBox: box(icon), dtBox: box(dt), ddBox: box(dd),
      iconSize: ics ? [ics.width, ics.height] : null,
      iconOverflow: icon ? (icon.getBoundingClientRect().left < cr.left + 1 ||
        icon.getBoundingClientRect().right > cr.right - 1) : null};
  });
  return {cardBox: [cr.x, cr.y, cr.width, cr.height].map(v => Math.round(v)), rows};
}"""

JS_NAV = """() => {
  const areas = [...document.querySelectorAll('header details.nav-services')].find(d => {
    const s = d.querySelector('summary'); return s && s.textContent.trim() === 'Areas';
  });
  if (!areas) return {error: 'no Areas dropdown'};
  const items = [...areas.querySelectorAll('.nav-dropdown a, .nav-dropdown span')].map(el =>
    ({tag: el.tagName, text: el.textContent.trim(), href: el.getAttribute('href')}));
  const mob = [...document.querySelectorAll('.mobile-menu-panel .nav-group')].find(g => g.textContent.trim() === 'Areas');
  let mobItems = [];
  if (mob) {
    let el = mob.nextElementSibling;
    while (el && !(el.classList && el.classList.contains('btn-call')) && el.getAttribute('href') !== '/contact/') {
      if (el.tagName === 'A' || (el.classList && el.classList.contains('nav-current'))) mobItems.push({tag: el.tagName, text: el.textContent.trim(), href: el.getAttribute('href')});
      el = el.nextElementSibling;
    }
  }
  const footer = [...document.querySelectorAll('footer .footer-col')].map(col => ({
    label: col.getAttribute('aria-label'),
    items: [...col.querySelectorAll('a, span.nav-current')].map(el => ({text: el.textContent.trim(), href: el.getAttribute('href')}))
  }));
  return {areasItems: items, mobItems, footer};
}"""

def main():
    out = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        # --- desktop 1440: homepage kinds grid ---
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(SERVER + "/", wait_until="networkidle")
        pg.evaluate("document.querySelector('.kinds-grid').scrollIntoView()")
        pg.wait_for_timeout(400)
        kinds = pg.evaluate(JS_KINDS)
        out["kinds_desktop"] = kinds
        grid = pg.query_selector_all(".kinds-grid")[1] if len(pg.query_selector_all(".kinds-grid")) > 1 else pg.query_selector(".kinds-grid")
        grid.screenshot(path=os.path.join(SHOTS, "kinds-desktop-1440.png"))
        pg.screenshot(path=os.path.join(SHOTS, "home-desktop-1440-full.png"), full_page=False)
        # --- mobile 390: homepage kinds grid ---
        pg2 = b.new_page(viewport={"width": 390, "height": 844})
        pg2.goto(SERVER + "/", wait_until="networkidle")
        pg2.evaluate("document.querySelector('.kinds-grid').scrollIntoView()")
        pg2.wait_for_timeout(400)
        out["kinds_mobile"] = pg2.evaluate(JS_KINDS)
        grid2 = pg2.query_selector_all(".kinds-grid")[1] if len(pg2.query_selector_all(".kinds-grid")) > 1 else pg2.query_selector(".kinds-grid")
        grid2.screenshot(path=os.path.join(SHOTS, "kinds-mobile-390.png"))
        # --- details card: water-removal desktop + mobile ---
        for name, page, url in (("desktop", pg, "/water-removal/"), ("mobile", pg2, "/water-removal/")):
            page.goto(SERVER + url, wait_until="networkidle")
            page.evaluate("document.querySelector('.details-card').scrollIntoView({block:'center'})")
            page.wait_for_timeout(300)
            out[f"details_{name}"] = page.evaluate(JS_DETAILS)
            page.query_selector(".details-card").screenshot(path=os.path.join(SHOTS, f"details-water-removal-{name}.png"))
        # --- nav state (desktop home) ---
        pg.goto(SERVER + "/", wait_until="networkidle")
        out["nav"] = pg.evaluate(JS_NAV)
        # open Areas dropdown, screenshot header
        pg.click("header details.nav-services >> nth=1 >> summary")
        pg.wait_for_timeout(300)
        pg.query_selector("header.site-header").screenshot(path=os.path.join(SHOTS, "header-areas-open-desktop.png"))
        # --- mobile menu open (390) ---
        pg2.goto(SERVER + "/", wait_until="networkidle")
        pg2.click(".mobile-menu summary")
        pg2.wait_for_timeout(400)
        pg2.query_selector("header.site-header").screenshot(path=os.path.join(SHOTS, "mobile-menu-open-390.png"))
        pg2.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg2.wait_for_timeout(300)
        pg2.query_selector("footer.site-footer").screenshot(path=os.path.join(SHOTS, "footer-mobile-390.png"))
        # --- footer desktop ---
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(300)
        pg.query_selector("footer.site-footer").screenshot(path=os.path.join(SHOTS, "footer-desktop-1440.png"))
        b.close()
    json.dump(out, open(os.path.join(SHOTS, "diag.json"), "w"), indent=1)
    print("kinds desktop cards:", len(out["kinds_desktop"].get("cards", [])))
    for c in out["kinds_desktop"].get("cards", [])[:3]:
        print(" ", c["i"], c["h3"], "| h3:", c["h3Color"], "| p:", c["pColor"], "| scrim:", c["scrimDisplay"])
    print("kinds mobile cards:", len(out["kinds_mobile"].get("cards", [])))
    print("details desktop rows:", len(out["details_desktop"].get("rows", [])))
    for r in out["details_desktop"].get("rows", []):
        print(" ", r["i"], r["label"], "| icon:", r["iconBox"], "| overflow:", r["iconOverflow"])
    print("details mobile rows:", len(out["details_mobile"].get("rows", [])))
    print("nav areas:", out["nav"].get("areasItems"))
    print("nav mobile areas:", out["nav"].get("mobItems"))
    for col in out["nav"].get("footer", []):
        print("footer", col["label"], "count:", len(col["items"]))
    print("DONE")

if __name__ == "__main__":
    main()
