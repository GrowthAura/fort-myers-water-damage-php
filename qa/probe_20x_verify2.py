#!/usr/bin/env python3
"""20x-verify follow-up probe: open questions from probe 1."""
import json, os
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
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)

import re
def parse_rgb(s):
    m = re.findall(r"[\d.]+", s)
    return tuple(float(x) for x in m[:3])

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])

    # D2 follow-up: main tabindex + Tab after Enter
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="networkidle")
    M["main_tag"] = pg.evaluate("() => { const m = document.querySelector('main'); return {tag: m.tagName, id: m.id, tabindex: m.getAttribute('tabindex')}; }")
    pg.keyboard.press("Tab")
    pg.wait_for_timeout(200)
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(400)
    after_enter = pg.evaluate("() => ({active: document.activeElement.tagName + '#' + (document.activeElement.id||''), scrollY: Math.round(window.scrollY)})")
    pg.keyboard.press("Tab")
    pg.wait_for_timeout(300)
    after_tab = pg.evaluate("""() => { const a = document.activeElement;
      return {tag: a.tagName, id: a.id, cls: (a.className||'').toString().slice(0,30),
        text: (a.textContent||'').trim().slice(0,30), href: a.getAttribute && a.getAttribute('href')}; }""")
    M["skiplink_flow"] = {"afterEnter": after_enter, "afterTab": after_tab}
    pg.close()

    # D3: all aria-current + self-links, desktop + mobile, on /water-removal/
    for w, name in [(1440, "desktop"), (390, "mobile")]:
        pg = b.new_page(viewport={"width": w, "height": 844})
        pg.goto(BASE + "/water-removal/", wait_until="networkidle")
        M[f"aria_all_{name}"] = pg.evaluate("""() => {
          return [...document.querySelectorAll('[aria-current]')].map(el => {
            const cs = getComputedStyle(el);
            const r = el.getBoundingClientRect();
            return {tag: el.tagName, cls: (el.className||'').toString().slice(0,30),
              text: el.textContent.trim().slice(0,30),
              href: el.getAttribute('href'), aria: el.getAttribute('aria-current'),
              visible: r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden',
              bg: cs.backgroundColor, color: cs.color, weight: cs.fontWeight,
              deco: cs.textDecorationLine, borderLeft: cs.borderLeftWidth + ' ' + cs.borderLeftColor,
              inHeader: !!el.closest('header'), inFooter: !!el.closest('footer'), inMain: !!el.closest('main'),
              ancestor: el.parentElement ? el.parentElement.tagName + '.' + (el.parentElement.className||'').toString().slice(0,30) : ''};
          });
        }""")
        M[f"selflinks_{name}"] = pg.evaluate("""() => {
          const out = [];
          [...document.querySelectorAll('header a, footer a, nav a')].forEach(a => {
            const h = a.getAttribute('href');
            if (!h || h.startsWith('#') || h.startsWith('tel:')) return;
            let u; try { u = new URL(h, location.href); } catch(e) { return; }
            if (u.pathname === location.pathname) {
              const r = a.getBoundingClientRect();
              out.push({href: h, text: a.textContent.trim().slice(0,30),
                inHeader: !!a.closest('header'), inFooter: !!a.closest('footer'),
                visible: r.width > 0 && r.height > 0});
            }
          });
          return out;
        }""")
        # top-level Services summary styling on this page
        M[f"topnav_{name}"] = pg.evaluate("""() => {
          const s = [...document.querySelectorAll('header summary')].find(x => /services/i.test(x.textContent));
          if (!s) return null;
          const cs = getComputedStyle(s);
          return {text: s.textContent.trim().slice(0,20), bg: cs.backgroundColor,
            deco: cs.textDecorationLine, decoColor: cs.textDecorationColor,
            color: cs.color, weight: cs.fontWeight, borderBottom: cs.borderBottom};
        }""")
        pg.close()

    # D3 home brand underline
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="networkidle")
    M["brand_home"] = pg.evaluate("""() => {
      const br = document.querySelector('header .brand, header a[href="/"], header a.brand');
      if (!br) return null;
      const cs = getComputedStyle(br);
      return {tag: br.tagName, href: br.getAttribute('href'), deco: cs.textDecorationLine,
        decoColor: cs.textDecorationColor, color: cs.color};
    }""")
    pg.close()

    # Menu Call button vs call bar (proper: panel's own button)
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/water-removal/", wait_until="networkidle")
    pg.click("details.mobile-menu > summary")
    pg.wait_for_timeout(500)
    M["menu_call_button"] = pg.evaluate("""() => {
      const panel = document.querySelector('.mobile-menu-panel');
      const btn = [...panel.querySelectorAll('a')].find(a => /call/i.test(a.textContent));
      const bar = document.querySelector('.call-bar');
      const br = btn ? btn.getBoundingClientRect() : null;
      const barR = bar ? bar.getBoundingClientRect() : null;
      const panelR = panel.getBoundingClientRect();
      return {btn: br ? {text: btn.textContent.trim().slice(0,30), top: Math.round(br.top), bottom: Math.round(br.bottom),
          h: Math.round(br.height), visible: br.height > 0} : null,
        barTop: barR ? Math.round(barR.top) : null,
        panelBottom: Math.round(panelR.bottom),
        gapBtnToBar: (br && barR) ? Math.round(barR.top - br.bottom) : null};
    }""")
    # mobile menu section-label contrast
    M["menu_label_contrast"] = pg.evaluate("""() => {
      const labels = [...document.querySelectorAll('.mobile-menu-panel .menu-label, .mobile-menu-panel [class*=label], .mobile-menu-panel summary')];
      return labels.map(el => {
        const cs = getComputedStyle(el);
        let bg = cs.backgroundColor, node = el;
        while ((bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') && node.parentElement) {
          node = node.parentElement;
          bg = getComputedStyle(node).backgroundColor;
        }
        return {text: el.textContent.trim().slice(0,20), color: cs.color, effBg: bg};
      });
    }""")
    # compute contrasts in python
    for row in M["menu_label_contrast"]:
        try:
            row["ratio"] = contrast(parse_rgb(row["color"]), parse_rgb(row["effBg"]))
        except Exception as e:
            row["ratio"] = f"err {e}"
    pg.screenshot(path=os.path.join(OUT, "13b-menu-open-mobile-scrolled.png"))
    pg.close()

    # M1 map link: rect + style + location (footer vs main)
    for w, name in [(390, "mobile"), (1440, "desktop")]:
        pg = b.new_page(viewport={"width": w, "height": 844})
        pg.goto(BASE + "/", wait_until="networkidle")
        M[f"maplink_{name}"] = pg.evaluate("""() => {
          const a = [...document.querySelectorAll('a')].find(x => x.textContent.trim() === 'View larger map');
          if (!a) return null;
          const cs = getComputedStyle(a);
          const r = a.getBoundingClientRect();
          const ifr = a.closest('footer') ? a.closest('footer').querySelector('iframe') : null;
          return {href: a.getAttribute('href'), target: a.getAttribute('target'),
            w: Math.round(r.width), h: Math.round(r.height),
            inFooter: !!a.closest('footer'), inMain: !!a.closest('main'),
            color: cs.color, deco: cs.textDecorationLine,
            iframeSrc: ifr ? ifr.getAttribute('src') : null};
        }""")
        pg.close()

    # D-V1: table 1 mobile, scrolled into view
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/cost/", wait_until="networkidle")
    pg.evaluate("document.querySelectorAll('.table-wrap.prices')[0].scrollIntoView({block:'center'})")
    pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(OUT, "20b-cost-table1-mobile-scrolled.png"))
    pg.close()

    b.close()

json.dump(M, open(os.path.join(OUT, "measurements2.json"), "w"), indent=2)
print(json.dumps(M, indent=2))
