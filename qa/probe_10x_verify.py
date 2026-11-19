#!/usr/bin/env python3
"""INDEPENDENT 10X verifier probe (fresh eyes). Serves out/ on 127.0.0.1:8140.
Usage: python3 qa/probe_10x_verify.py
Writes qa/screenshots/10x-verify/*.png + measurements.json. No site edits."""
import json, os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8140"
OUT = "/home/hatch/workspace/fort-myers-php/qa/screenshots/10x-verify"
os.makedirs(OUT, exist_ok=True)
M = {}

def lum(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(fg, bg):
    l1, l2 = sorted([lum(fg), lum(bg)], reverse=True)
    return round((l1 + 0.05) / (l2 + 0.05), 2)

def parse_rgb(s):
    return tuple(int(float(x)) for x in s.replace("rgba(", "").replace("rgb(", "").rstrip(")").split(",")[:3])

with sync_playwright() as pw:
    b = pw.chromium.launch()
    # ---- 1. DESKTOP 1440: header, nav carets, home hero, footer links ----
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="load"); pg.wait_for_timeout(400)
    M["d1_header_nav"] = pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const r = el => { const b = el.getBoundingClientRect(); return {x: Math.round(b.x*10)/10, y: Math.round(b.y*10)/10, w: Math.round(b.width*10)/10, h: Math.round(b.height*10)/10}; };
      const summs = [...document.querySelectorAll('.site-nav summary')].map(s => ({text: s.textContent.trim(), rect: r(s), lines: s.getClientRects().length}));
      const links = [...document.querySelectorAll('.site-nav > a')].map(a => ({text: a.textContent.trim(), rect: r(a), lines: a.getClientRects().length}));
      const hero = q('.hero').getBoundingClientRect();
      const heroParent = q('.hero').parentElement.tagName + '.' + q('.hero').parentElement.className;
      const fl = [...document.querySelectorAll('.footer-col a')].slice(0, 4).map(a => Math.round(a.getBoundingClientRect().height*10)/10);
      const fphone = [...document.querySelectorAll('.site-footer a[href^="tel:"]')].map(a => ({text: a.textContent.trim().slice(0,30), h: Math.round(a.getBoundingClientRect().height*10)/10, w: Math.round(a.getBoundingClientRect().width*10)/10}));
      const fbase = [...document.querySelectorAll('.footer-base a')].map(a => Math.round(a.getBoundingClientRect().height*10)/10);
      const cs = getComputedStyle(q('.hero-inner'));
      return { headerH: Math.round(q('.site-header').getBoundingClientRect().height*10)/10,
        summaries: summs, navLinks: links,
        hero: {x: Math.round(hero.x), y: Math.round(hero.y), w: Math.round(hero.width), h: Math.round(hero.height), parent: heroParent},
        heroInnerPaddingTop: cs.paddingTop, heroInnerPaddingBottom: cs.paddingBottom,
        footerColLinkH: fl, footerPhoneLinks: fphone, footerBaseLinkH: fbase,
        bodyFont: getComputedStyle(document.body).fontSize };
    }""")
    pg.screenshot(path=f"{OUT}/01-nav-desktop.png")
    pg.locator(".hero").screenshot(path=f"{OUT}/02-home-hero-desktop.png")
    # footer brand void on cape-coral (desktop)
    pg.goto(BASE + "/cape-coral/", wait_until="load"); pg.wait_for_timeout(300)
    M["d10_cape_footer"] = pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const doc = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return {h: Math.round(b.height), top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY)}; };
      const grid = doc(q('.footer-grid'));
      const brand = doc(q('.footer-brand'));
      const cols = [...document.querySelectorAll('.footer-grid > *')].map(el => ({cls: el.className, top: Math.round(el.getBoundingClientRect().top + scrollY), bottom: Math.round(el.getBoundingClientRect().bottom + scrollY)}));
      return { grid, brand, cols, topGap: brand ? brand.top - grid.top : null, bottomGap: brand && grid ? grid.bottom - brand.bottom : null,
        footerHrefs: [...document.querySelectorAll('.site-footer a')].map(a => a.getAttribute('href')) };
    }""")
    pg.locator(".site-footer").screenshot(path=f"{OUT}/05-footer-cape-desktop.png")
    # home footer for comparison + footer hrefs
    pg.goto(BASE + "/", wait_until="load"); pg.wait_for_timeout(300)
    M["d10_home_footer"] = pg.evaluate("""() => {
      const q = s => document.querySelector(s);
      const doc = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return {h: Math.round(b.height), top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY)}; };
      return { grid: doc(q('.footer-grid')), brand: doc(q('.footer-brand')),
        footerHrefs: [...document.querySelectorAll('.site-footer a')].map(a => a.getAttribute('href')) };
    }""")
    # cost desktop: price tables
    pg.goto(BASE + "/cost/", wait_until="load"); pg.wait_for_timeout(300)
    M["d8_cost_desktop"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('.table-wrap')].map(w => {
        const last = w.querySelector('tbody tr:first-child td:last-child');
        const lr = last.getBoundingClientRect();
        const cs = getComputedStyle(last);
        const rows = [...w.querySelectorAll('tbody tr')].slice(0, 3).map(tr => {
          const c = tr.querySelector('td:last-child');
          return {text: c.textContent.trim().slice(0, 45), h: Math.round(c.getBoundingClientRect().height*10)/10, lines: c.getClientRects().length};
        });
        return {pricesClass: w.classList.contains('prices'), tableW: Math.round(w.getBoundingClientRect().width),
          lastCol: {text: last.textContent.trim().slice(0,45), h: Math.round(lr.height*10)/10, lines: last.getClientRects().length,
                    textAlign: cs.textAlign, whiteSpace: cs.whiteSpace}, rows};
      });
    }""")
    pg.locator(".table-wrap.prices").first.screenshot(path=f"{OUT}/03-cost-table-desktop.png")
    pg.screenshot(path=f"{OUT}/04-cost-desktop-viewport.png")
    pg.close()

    # ---- 2. MOBILE 390: menu, hero CTA-first, table fade, footer, HIW ----
    pg = b.new_page(viewport={"width": 390, "height": 844})
    # menu toggle live test (claim 9) + menu bottom (claim 2) + contrast (claim 6)
    pg.goto(BASE + "/", wait_until="load"); pg.wait_for_timeout(400)
    M["d9_toggle_closed"] = pg.evaluate("""() => {
      const s = document.querySelector('.mobile-menu summary');
      return {label: s.querySelector('.menu-label') ? s.querySelector('.menu-label').textContent : s.textContent.trim(), aria: s.getAttribute('aria-label')};
    }""")
    pg.locator(".mobile-menu summary").click(); pg.wait_for_timeout(400)
    M["d9_toggle_open"] = pg.evaluate("""() => {
      const s = document.querySelector('.mobile-menu summary');
      const d = document.querySelector('.mobile-menu');
      return {label: s.querySelector('.menu-label') ? s.querySelector('.menu-label').textContent : s.textContent.trim(),
        icon: s.querySelector('span[aria-hidden]') ? s.querySelector('span[aria-hidden]').textContent : null,
        aria: s.getAttribute('aria-label'), open: d.open};
    }""")
    pg.screenshot(path=f"{OUT}/12-menu-open-mobile.png")
    M["d2_menu_bottom"] = pg.evaluate("""() => {
      const panel = document.querySelector('.mobile-menu-panel');
      const bar = document.querySelector('.call-bar');
      const btn = [...document.querySelectorAll('.mobile-menu-panel a.btn, .mobile-menu-panel .btn')].pop();
      panel.scrollTop = panel.scrollHeight;
      const pr = panel.getBoundingClientRect(), br = bar.getBoundingClientRect();
      const bbr = btn ? btn.getBoundingClientRect() : null;
      return { panelBottom: Math.round(pr.bottom), panelMaxH: getComputedStyle(panel).maxHeight,
        callBarTop: Math.round(br.top), callBarH: Math.round(br.height),
        menuCallBtn: bbr ? {text: btn.textContent.trim().slice(0,40), top: Math.round(bbr.top), bottom: Math.round(bbr.bottom), h: Math.round(bbr.height)} : null,
        gapBtnBottomToBarTop: bbr ? Math.round(br.top - bbr.bottom) : null };
    }""")
    pg.wait_for_timeout(300)
    pg.screenshot(path=f"{OUT}/12b-menu-open-scrolled-bottom.png")
    # contrast claim 6
    M["d6_contrast"] = pg.evaluate("""() => {
      const g = document.querySelector('.mobile-menu-panel .nav-group');
      const panel = document.querySelector('.mobile-menu-panel');
      return { groupColor: getComputedStyle(g).color, panelBg: getComputedStyle(panel).backgroundColor, groupText: g.textContent.trim() };
    }""")
    M["d6_contrast"]["ratio"] = contrast(parse_rgb(M["d6_contrast"]["groupColor"]), parse_rgb(M["d6_contrast"]["panelBg"]))
    # close menu via toggle click again, confirm label resets
    pg.locator(".mobile-menu summary").click(); pg.wait_for_timeout(300)
    M["d9_toggle_reclosed"] = pg.evaluate("""() => {
      const s = document.querySelector('.mobile-menu summary');
      return {label: s.querySelector('.menu-label') ? s.querySelector('.menu-label').textContent : s.textContent.trim(), open: document.querySelector('.mobile-menu').open};
    }""")
    # Escape-close path: open, press Escape, check label
    pg.locator(".mobile-menu summary").click(); pg.wait_for_timeout(300)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    M["d9_escape_close"] = pg.evaluate("""() => {
      const s = document.querySelector('.mobile-menu summary');
      return {label: s.querySelector('.menu-label') ? s.querySelector('.menu-label').textContent : s.textContent.trim(), open: document.querySelector('.mobile-menu').open};
    }""")
    # mobile hero CTA-first across page classes (claim 5)
    cta = {}
    for slug, name in [("/", "home"), ("/cost/", "cost"), ("/insurance/", "insurance"),
                       ("/cape-coral/", "cape"), ("/contact/", "contact"), ("/water-removal/", "water"),
                       ("/how-it-works/", "hiw"), ("/about/", "about"), ("/areas/", "areas"),
                       ("/privacy-policy/", "privacy"), ("/estero/", "estero")]:
        pg.goto(BASE + slug, wait_until="load"); pg.wait_for_timeout(300)
        cta[name] = pg.evaluate("""() => {
          const btn = document.querySelector('.hero-ctas .btn-call');
          const hero = document.querySelector('.hero').getBoundingClientRect();
          const cs = getComputedStyle(document.querySelector('.hero-inner'));
          return btn ? {callTop: Math.round(btn.getBoundingClientRect().top), heroH: Math.round(hero.height),
            heroPadTop: cs.paddingTop, heroPadBottom: cs.paddingBottom, viewport: 844} : null;
        }""")
        if name in ("home", "cost"):
            pg.screenshot(path=f"{OUT}/1{name}-hero-mobile-firstviewport.png")
    M["d5_mobile_hero_cta"] = cta
    # table fade (claim 4) home mobile
    pg.goto(BASE + "/", wait_until="load"); pg.wait_for_timeout(300)
    M["d4_table_fade"] = pg.evaluate("""() => {
      const w = document.querySelector('.table-wrap');
      const t = w.querySelector('table');
      const cs = getComputedStyle(w);
      return { wrapW: Math.round(w.getBoundingClientRect().width), tableScrollW: w.scrollWidth,
        boxShadow: cs.boxShadow, hasFade: cs.boxShadow.includes('inset') };
    }""")
    pg.locator(".table-wrap").first.screenshot(path=f"{OUT}/11-home-table-mobile.png")
    # cost mobile table width + row heights (trade-off measurement)
    pg.goto(BASE + "/cost/", wait_until="load"); pg.wait_for_timeout(300)
    M["cost_mobile"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('.table-wrap.prices')].map(w => {
        const t = w.querySelector('table');
        const rows = [...w.querySelectorAll('tbody tr')].slice(0, 3).map(tr => {
          const c = tr.querySelector('td:last-child');
          return {text: c.textContent.trim().slice(0,40), h: Math.round(c.getBoundingClientRect().height), lines: c.getClientRects().length};
        });
        const lastHead = w.querySelector('thead th:last-child').textContent.trim();
        return {lastHead, wrapW: Math.round(w.getBoundingClientRect().width), tableScrollW: w.scrollWidth,
          lastColW: Math.round(w.querySelector('tbody tr:first-child td:last-child').getBoundingClientRect().width), rows};
      });
    }""")
    pg.locator(".table-wrap.prices").first.screenshot(path=f"{OUT}/14-cost-table-mobile.png")
    # HIW mobile phone nowrap (claim 8b)
    pg.goto(BASE + "/how-it-works/", wait_until="load"); pg.wait_for_timeout(300)
    M["d8b_hiw_mobile"] = pg.evaluate("""() => {
      const links = [...document.querySelectorAll('.steps a[href^="tel:"]')];
      return links.map(a => { const b = a.getBoundingClientRect();
        return {text: a.textContent.trim(), h: Math.round(b.height*10)/10, lines: a.getClientRects().length,
                whiteSpace: getComputedStyle(a).whiteSpace}; });
    }""")
    pg.locator(".steps").first.screenshot(path=f"{OUT}/15-hiw-steps-mobile.png")
    # footer mobile heights
    pg.goto(BASE + "/", wait_until="load"); pg.wait_for_timeout(300)
    M["d7_footer_mobile"] = pg.evaluate("""() => {
      const fl = [...document.querySelectorAll('.footer-col a')].slice(0, 4).map(a => Math.round(a.getBoundingClientRect().height*10)/10);
      const fphone = [...document.querySelectorAll('.site-footer a[href^="tel:"]')].map(a => ({text: a.textContent.trim().slice(0,30), h: Math.round(a.getBoundingClientRect().height*10)/10}));
      const fbase = [...document.querySelectorAll('.footer-base a')].map(a => Math.round(a.getBoundingClientRect().height*10)/10);
      return {footerColLinkH: fl, footerPhoneLinks: fphone, footerBaseLinkH: fbase};
    }""")
    pg.locator(".site-footer").screenshot(path=f"{OUT}/16-footer-mobile.png")
    # FAQ open state, real click (home mobile)
    pg.evaluate("""() => { document.querySelector('.faq-item summary').scrollIntoView({block: 'center'}); }""")
    pg.wait_for_timeout(200)
    pg.locator(".faq-item summary").first.click(); pg.wait_for_timeout(400)
    M["faq_open_mobile"] = pg.evaluate("""() => {
      const item = document.querySelector('.faq-item');
      const cs = getComputedStyle(item);
      return {open: item.open, h: Math.round(item.getBoundingClientRect().height),
        borderLeft: cs.borderLeft, boxShadow: cs.boxShadow.slice(0, 60)};
    }""")
    pg.locator(".faq-item").first.screenshot(path=f"{OUT}/18-faq-open-mobile.png")
    # overflow + font sweep all 34 routes x 4 widths (independent regression)
    import_routes = ["/", "/water-removal/", "/drying/", "/sewage-cleanup/", "/ac-leak/", "/ceiling-leak/",
      "/condo-leak/", "/cast-iron-pipe/", "/vacant-home/", "/first-hour-checklist/", "/cost/", "/insurance/",
      "/burst-pipe/", "/mobile-home/", "/slab-leak/", "/flood-cleanup/", "/cape-coral/", "/lehigh-acres/",
      "/areas/", "/water-heater-leak/", "/appliance-leak/", "/floors/", "/cabinets/", "/commercial/",
      "/north-fort-myers/", "/fort-myers-beach/", "/estero/", "/bonita-springs/", "/how-it-works/",
      "/contact/", "/about/", "/privacy-policy/", "/terms/", "/disclaimer/"]
    ov = {}
    for slug in import_routes:
        pg.goto(BASE + slug, wait_until="load"); pg.wait_for_timeout(120)
        ov[slug] = pg.evaluate("""() => {
          const out = {};
          for (const w of [320, 360, 390, 1440]) { }
          return {scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth,
                  overflow: document.documentElement.scrollWidth - window.innerWidth,
                  bodyFont: getComputedStyle(document.body).fontSize};
        }""")
    # NOTE: widths above are all at 390 viewport; do a proper per-width pass below
    M["overflow_390_only"] = ov
    pg.close()
    # proper per-width overflow pass
    for w in [320, 360, 390, 1440]:
        p2 = b.new_page(viewport={"width": w, "height": 844})
        bad = {}
        for slug in import_routes:
            p2.goto(BASE + slug, wait_until="load"); p2.wait_for_timeout(80)
            r = p2.evaluate("() => ({o: document.documentElement.scrollWidth - window.innerWidth, f: getComputedStyle(document.body).fontSize})")
            if r["o"] != 0 or r["f"] != "20px":
                bad[slug] = r
        M[f"overflow_w{w}"] = {"badCount": len(bad), "bad": bad}
        p2.close()
    b.close()

print(json.dumps(M, indent=1))
with open(f"{OUT}/measurements.json", "w") as fh:
    json.dump(M, fh, indent=1)
