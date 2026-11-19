#!/usr/bin/env python3
"""20x-verify probe 3: brand underline, nav-group contrast, menu call button scrolled."""
import json, os, re
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8145"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "qa", "screenshots", "20x-verify")
M = {}

def lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(c1, c2):
    l1, l2 = lum(c1), lum(c2)
    return round((max(l1, l2) + 0.05) / (min(l1, l2) + 0.05), 2)

def prgb(s):
    m = re.findall(r"[\d.]+", s)
    return tuple(float(x) for x in m[:3])

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="networkidle")
    M["brand_home_inner"] = pg.evaluate("""() => {
      const br = document.querySelector('header a.brand');
      const name = br.querySelector('.brand-name');
      const cs = getComputedStyle(name);
      return {brandAria: br.getAttribute('aria-current'), deco: cs.textDecorationLine,
        decoColor: cs.textDecorationColor, offset: cs.textUnderlineOffset, color: cs.color};
    }""")
    # cost page top-level current link (direct <a> child)
    pg.goto(BASE + "/cost/", wait_until="networkidle")
    M["topnav_cost"] = pg.evaluate("""() => {
      const a = document.querySelector('.site-nav > a[aria-current="page"]');
      if (!a) return null;
      const cs = getComputedStyle(a);
      return {text: a.textContent.trim(), bg: cs.backgroundColor, shadow: cs.boxShadow, color: cs.color};
    }""")
    pg.close()

    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/water-removal/", wait_until="networkidle")
    pg.click("details.mobile-menu > summary")
    pg.wait_for_timeout(500)
    M["nav_group_contrast"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('.mobile-menu-panel .nav-group')].map(el => {
        const cs = getComputedStyle(el);
        let bg = cs.backgroundColor, node = el;
        while ((bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') && node.parentElement) {
          node = node.parentElement; bg = getComputedStyle(node).backgroundColor;
        }
        return {text: el.textContent.trim(), color: cs.color, effBg: bg};
      });
    }""")
    for row in M["nav_group_contrast"]:
        row["ratio"] = contrast(prgb(row["color"]), prgb(row["effBg"]))
    # scroll panel to bottom, measure call button
    M["menu_call_scrolled"] = pg.evaluate("""() => {
      const panel = document.querySelector('.mobile-menu-panel');
      panel.scrollTop = panel.scrollHeight;
      const btn = [...panel.querySelectorAll('a.btn-call')][0];
      const bar = document.querySelector('.call-bar');
      const br = btn.getBoundingClientRect();
      const barR = bar.getBoundingClientRect();
      return new Promise(res => setTimeout(() => {
        const r2 = btn.getBoundingClientRect();
        res({btnTop: Math.round(r2.top), btnBottom: Math.round(r2.bottom), h: Math.round(r2.height),
          barTop: Math.round(barR.top), gap: Math.round(barR.top - r2.bottom),
          panelBottom: Math.round(panel.getBoundingClientRect().bottom)});
      }, 300));
    }""")
    pg.wait_for_timeout(600)
    pg.screenshot(path=os.path.join(OUT, "13c-menu-open-mobile-bottom.png"))
    pg.close()
    b.close()

json.dump(M, open(os.path.join(OUT, "measurements3.json"), "w"), indent=2)
print(json.dumps(M, indent=2))
