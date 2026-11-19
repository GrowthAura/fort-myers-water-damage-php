#!/usr/bin/env python3
"""Independent 20x verifier probe — fresh measurements, no builder numbers trusted.
Serves out/ on 127.0.0.1:8145, Playwright bundled Chromium only.
Writes qa/screenshots/20x-verify/ + measurements.json there."""
import json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8145"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "qa", "screenshots", "20x-verify")
os.makedirs(OUT, exist_ok=True)
M = {}

def shot(page, name):
    page.screenshot(path=os.path.join(OUT, name))

def lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(c1, c2):
    l1, l2 = lum(c1), lum(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def parse_rgb(s):
    m = re.findall(r"[\d.]+", s)
    return tuple(float(x) for x in m[:3])

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    # ---------- D-V1 + desktop cost ----------
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/cost/", wait_until="networkidle")
    cost_m = pg.evaluate("""() => {
      const out = [];
      document.querySelectorAll('.table-wrap.prices').forEach((w, i) => {
        const t = w.querySelector('table');
        const rows = [...t.querySelectorAll('tbody tr')].slice(0,3).map(r => Math.round(r.getBoundingClientRect().height));
        const lastCells = [...t.querySelectorAll('tbody tr td:last-child')];
        const first = lastCells[0];
        const cs = getComputedStyle(first);
        const r = first.getBoundingClientRect();
        const wr = w.getBoundingClientRect();
        const vis = r.left < 390 && r.right > 0 && r.width > 0;
        // is any price text visible inside viewport at first paint?
        const txt = lastCells.map(c => c.textContent.trim().slice(0,30));
        out.push({i, tableW: Math.round(t.getBoundingClientRect().width), wrapW: Math.round(wr.width),
          priceColW: Math.round(r.width), priceLeft: Math.round(r.left), priceRight: Math.round(r.right),
          whiteSpace: cs.whiteSpace, textAlign: cs.textAlign, rows, firstPaintVisible: vis, sample: txt[0]});
      });
      return {tables: out, scrollW: document.documentElement.scrollWidth};
    }""")
    M["cost_mobile_390"] = cost_m
    pg.screenshot(path=os.path.join(OUT, "20-cost-table1-mobile-viewport.png"))
    # scroll to table 3 and shoot
    pg.evaluate("document.querySelectorAll('.table-wrap.prices')[2].scrollIntoView()")
    pg.wait_for_timeout(400)
    shot(pg, "21-cost-table3-mobile-viewport.png")
    pg.close()

    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/cost/", wait_until="networkidle")
    M["cost_desktop"] = pg.evaluate("""() => {
      const out = [];
      document.querySelectorAll('.table-wrap.prices').forEach((w, i) => {
        const t = w.querySelector('table');
        const c = t.querySelector('tbody tr td:last-child');
        const cs = getComputedStyle(c);
        out.push({i, tableW: Math.round(t.getBoundingClientRect().width), whiteSpace: cs.whiteSpace,
          textAlign: cs.textAlign, rows: [...t.querySelectorAll('tbody tr')].slice(0,3).map(r => Math.round(r.getBoundingClientRect().height))});
      });
      return out;
    }""")
    shot(pg, "22-cost-desktop.png")
    pg.close()

    # ---------- D1 hero motif + regression header/hero ----------
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="networkidle")
    M["hero_desktop"] = pg.evaluate("""() => {
      const h = document.querySelector('.hero, .hero-no-media, header + main > section:first-child, main > *:first-child');
      const hero = document.querySelector('.hero-no-media') || document.querySelector('[class*=hero]');
      const r = hero.getBoundingClientRect();
      const cs = getComputedStyle(hero, '::after');
      const inner = hero.querySelector('.hero-inner, .wrap, div');
      const ir = inner ? inner.getBoundingClientRect() : null;
      return {tag: hero.tagName, cls: hero.className, x: r.x, y: r.y, w: Math.round(r.width), h: Math.round(r.height),
        afterBg: cs.backgroundImage.slice(0,120), afterZ: cs.zIndex,
        innerRect: ir ? {x: Math.round(ir.x), y: Math.round(ir.y)} : null,
        headerH: Math.round(document.querySelector('header').getBoundingClientRect().height)};
    }""")
    shot(pg, "01-hero-desktop-home.png")
    pg.close()

    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/", wait_until="networkidle")
    M["hero_mobile"] = pg.evaluate("""() => {
      const hero = document.querySelector('.hero-no-media') || document.querySelector('[class*=hero]');
      const r = hero.getBoundingClientRect();
      return {x: r.x, w: Math.round(r.width), h: Math.round(r.height)};
    }""")
    shot(pg, "12-hero-mobile-home.png")
    # mobile CTA top across page classes
    cta = {}
    for slug in ["/", "/cost/", "/insurance/", "/cape-coral/", "/contact/", "/water-removal/", "/how-it-works/", "/about/", "/areas/", "/privacy-policy/", "/estero/"]:
        pg.goto(BASE + slug, wait_until="domcontentloaded")
        pg.wait_for_timeout(300)
        cta[slug] = pg.evaluate("""() => {
          const btns = [...document.querySelectorAll('main a.btn, main a[href^="tel:"]')];
          const b = btns.find(x => /call/i.test(x.textContent));
          if (!b) return null;
          const r = b.getBoundingClientRect();
          return {top: Math.round(r.top + window.scrollY), label: b.textContent.trim().slice(0,40)};
        }""")
    M["mobile_cta_top"] = cta
    pg.close()

    # ---------- D2 skip link (real Tab) ----------
    for w, name in [(1440, "desktop"), (390, "mobile")]:
        pg = b.new_page(viewport={"width": w, "height": 844})
        pg.goto(BASE + "/", wait_until="networkidle")
        pg.keyboard.press("Tab")
        pg.wait_for_timeout(300)
        r = pg.evaluate("""() => {
          const a = document.querySelector('a.skip-link, .skip-link, a[href="#main"]');
          if (!a) return {exists: false};
          const cs = getComputedStyle(a);
          const rect = a.getBoundingClientRect();
          return {exists: true, text: a.textContent.trim(), href: a.getAttribute('href'),
            focused: document.activeElement === a,
            visible: rect.width > 0 && rect.height > 0 && cs.opacity !== '0',
            w: Math.round(rect.width), h: Math.round(rect.height), x: Math.round(rect.x), y: Math.round(rect.y),
            bg: cs.backgroundColor, color: cs.color, outline: cs.outline};
        }""")
        M[f"skiplink_{name}"] = r
        shot(pg, f"02-skiplink-focused-{name}.png")
        # press Enter -> focus should move to main
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(400)
        M[f"skiplink_enter_{name}"] = pg.evaluate("""() => {
          const ae = document.activeElement;
          return {tag: ae.tagName, id: ae.id, isMain: ae.id === 'main' || ae.tagName === 'MAIN',
            scrollY: Math.round(window.scrollY)};
        }""")
        pg.close()

    # ---------- D3 active nav ----------
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/water-removal/", wait_until="networkidle")
    M["nav_water_removal_desktop"] = pg.evaluate("""() => {
      const out = {};
      const dd = [...document.querySelectorAll('header .dropdown a, header nav a, header a')];
      // dropdown current item
      const cur = document.querySelector('header .nav-current');
      out.dropdownCurrent = cur ? {tag: cur.tagName, cls: cur.className, text: cur.textContent.trim(),
        bg: getComputedStyle(cur).backgroundColor, color: getComputedStyle(cur).color,
        weight: getComputedStyle(cur).fontWeight} : null;
      // top-level current link
      const top = document.querySelector('header a[aria-current="page"], header [aria-current="page"]');
      out.ariaCurrent = top ? {tag: top.tagName, text: top.textContent.trim().slice(0,30),
        bg: getComputedStyle(top).backgroundColor, deco: getComputedStyle(top).textDecorationLine} : null;
      // footer current
      const f = document.querySelector('footer [aria-current="page"], footer a[aria-current]');
      out.footerCurrent = f ? {tag: f.tagName, text: f.textContent.trim().slice(0,30),
        color: getComputedStyle(f).color, weight: getComputedStyle(f).fontWeight,
        deco: getComputedStyle(f).textDecorationLine} : null;
      // any <a> in header/footer whose href resolves to this page?
      const selfLinks = [...document.querySelectorAll('header a, footer a')].filter(a => {
        const u = new URL(a.getAttribute('href'), location.href);
        return u.pathname === location.pathname && !a.getAttribute('href').startsWith('#');
      }).map(a => a.getAttribute('href') + ' :: ' + a.textContent.trim().slice(0,25));
      out.selfLinksHeaderFooter = selfLinks;
      return out;
    }""")
    # open services dropdown for screenshot
    pg.evaluate("document.querySelector('header details')?.setAttribute('open','')")
    pg.wait_for_timeout(300)
    shot(pg, "03-nav-dropdown-active-desktop.png")
    pg.close()

    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/water-removal/", wait_until="networkidle")
    # open mobile menu
    pg.click("details.mobile-menu > summary")
    pg.wait_for_timeout(500)
    M["nav_water_removal_mobile"] = pg.evaluate("""() => {
      const cur = document.querySelector('.mobile-menu [aria-current="page"], .mobile-nav [aria-current="page"], header [aria-current="page"]');
      const panel = document.querySelector('.mobile-menu, .mobile-nav, [class*=mobile-menu]');
      return {current: cur ? {tag: cur.tagName, text: cur.textContent.trim().slice(0,30),
        bg: getComputedStyle(cur).backgroundColor, weight: getComputedStyle(cur).fontWeight,
        borderLeft: getComputedStyle(cur).borderLeftWidth + ' ' + getComputedStyle(cur).borderLeftColor} : null,
        panelVisible: panel ? panel.getBoundingClientRect().height > 0 : null};
    }""")
    shot(pg, "13-menu-open-mobile.png")
    # menu call button vs call bar
    M["menu_callbar"] = pg.evaluate("""() => {
      const bar = document.querySelector('.call-bar, [class*=call-bar], .sticky-call');
      const btns = [...document.querySelectorAll('a')].filter(a => /call/i.test(a.textContent) && a.getBoundingClientRect().top > 400);
      const b = btns[btns.length-1];
      if (!b) return null;
      const r = b.getBoundingClientRect();
      const barR = bar ? bar.getBoundingClientRect() : null;
      return {btnTop: Math.round(r.top), btnBottom: Math.round(r.bottom),
        barTop: barR ? Math.round(barR.top) : null, gap: barR ? Math.round(barR.top - r.bottom) : null};
    }""")
    pg.close()

    # ---------- D4 back to top (real click) + call-bar collision ----------
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(600)
    before = pg.evaluate("Math.round(window.scrollY)")
    info = pg.evaluate("""() => {
      const a = document.querySelector('a.back-to-top, .back-to-top');
      if (!a) return {exists: false};
      const r = a.getBoundingClientRect();
      const bar = document.querySelector('.call-bar, [class*=call-bar]');
      const barR = bar ? bar.getBoundingClientRect() : null;
      return {exists: true, text: a.textContent.trim(), href: a.getAttribute('href'),
        w: Math.round(r.width), h: Math.round(r.height),
        bottom: Math.round(r.bottom), viewportH: innerHeight,
        barTop: barR ? Math.round(barR.top) : null, barBottom: barR ? Math.round(barR.bottom) : null,
        overlapBar: barR ? !(r.bottom <= barR.top || r.top >= barR.bottom) : false};
    }""")
    M["backtotop_mobile"] = {"scrollY_before": before, **info}
    shot(pg, "15-footer-mobile.png")
    if info.get("exists"):
        pg.click("a.back-to-top")
        pg.wait_for_timeout(2500)
        M["backtotop_mobile"]["scrollY_after_click"] = pg.evaluate("Math.round(window.scrollY)")
    pg.close()

    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(500)
    b4 = pg.evaluate("Math.round(window.scrollY)")
    pg.click("a.back-to-top")
    pg.wait_for_timeout(2500)
    M["backtotop_desktop"] = {"scrollY_before": b4, "scrollY_after_click": pg.evaluate("Math.round(window.scrollY)")}
    shot(pg, "06-footer-desktop.png")
    pg.close()

    # ---------- D5 FAQ links + open state ----------
    for w, name in [(1440, "desktop"), (390, "mobile")]:
        pg = b.new_page(viewport={"width": w, "height": 844})
        pg.goto(BASE + "/", wait_until="networkidle")
        M[f"faq_{name}"] = pg.evaluate("""() => {
          const d = document.querySelector('details.faq-item');
          if (!d) return {exists: false};
          const link = d.querySelector('a');
          const cs = link ? getComputedStyle(link) : null;
          return {exists: true, openBefore: d.open,
            linkText: link ? link.textContent.trim().slice(0,40) : null,
            linkDeco: cs ? cs.textDecorationLine : null,
            linkOffset: cs ? cs.textUnderlineOffset : null,
            linkColor: cs ? cs.color : null};
        }""")
        # real click on first summary
        pg.click("details.faq-item summary")
        pg.wait_for_timeout(400)
        M[f"faq_{name}"]["openAfterClick"] = pg.evaluate("document.querySelector('details.faq-item').open")
        M[f"faq_{name}"]["openHeight"] = pg.evaluate("Math.round(document.querySelector('details.faq-item').getBoundingClientRect().height)")
        shot(pg, f"05-faq-open-{name}.png")
        pg.close()

    # ---------- A1 tap targets (all pages sampled: home + cost + contact, desktop+mobile) ----------
    for w, name in [(1440, "desktop"), (390, "mobile")]:
        pg = b.new_page(viewport={"width": w, "height": 844})
        sub44 = []
        for slug in ["/", "/cost/", "/contact/", "/water-removal/"]:
            pg.goto(BASE + slug, wait_until="domcontentloaded")
            pg.wait_for_timeout(300)
            res = pg.evaluate("""() => {
              const els = [...document.querySelectorAll('a, button, summary, input, select, [role=button]')];
              const bad = [];
              els.forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width === 0 || r.height === 0) return;
                const cs = getComputedStyle(el);
                if (cs.display === 'none' || cs.visibility === 'hidden') return;
                // inline prose link? check if it's inside a paragraph/list/table cell and display inline
                const inline = cs.display === 'inline';
                const h = Math.round(r.height * 10) / 10, wd = Math.round(r.width * 10) / 10;
                if (h < 44 || wd < 44) {
                  bad.push({tag: el.tagName, text: (el.textContent||'').trim().slice(0,35),
                    href: el.getAttribute('href') || '', w: wd, h, display: cs.display,
                    parent: el.parentElement ? el.parentElement.tagName + '.' + (el.parentElement.className||'').toString().slice(0,25) : ''});
                }
              });
              return bad;
            }""")
            for r in res:
                r["page"] = slug
                sub44.append(r)
        M[f"tap_targets_{name}"] = sub44
        # discrete = not inline
        M[f"tap_targets_{name}_discrete_sub44"] = [r for r in sub44 if r["display"] != "inline"]
        pg.close()

    # ---------- Regression: header, carets, fade, contrast, footer links ----------
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="networkidle")
    M["regression_desktop"] = pg.evaluate("""() => {
      const header = document.querySelector('header');
      const sums = [...document.querySelectorAll('header summary, header .nav-item summary, header details summary')];
      return {
        headerH: Math.round(header.getBoundingClientRect().height),
        carets: sums.map(s => ({text: s.textContent.trim().slice(0,20), lines: s.getClientRects().length, h: Math.round(s.getBoundingClientRect().height)})),
        brandSize: (() => { const b = document.querySelector('.brand, header a.brand, header .site-brand'); if (!b) return null; const r=b.getBoundingClientRect(); return {w: Math.round(r.width), h: Math.round(r.height)}; })(),
        footerLinks: [...document.querySelectorAll('footer a')].slice(0,40).map(a => Math.round(a.getBoundingClientRect().height * 10) / 10),
        menuLabels: (() => {
          const els = [...document.querySelectorAll('header summary, header .nav-label')];
          return els.map(e => { const cs = getComputedStyle(e); return {text: e.textContent.trim().slice(0,12), color: cs.color, bg: cs.backgroundColor}; });
        })(),
      };
    }""")
    pg.close()

    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/", wait_until="networkidle")
    M["regression_mobile"] = pg.evaluate("""() => {
      const w = document.querySelector('.table-wrap');
      let fade = null;
      if (w) { const cs = getComputedStyle(w); fade = cs.boxShadow; }
      const brand = document.querySelector('.brand, header a.brand');
      const br = brand ? brand.getBoundingClientRect() : null;
      return {tableFade: fade,
        brandMobile: br ? {w: Math.round(br.width), h: Math.round(br.height)} : null,
        footerLinksMin: Math.min(...[...document.querySelectorAll('footer a')].map(a => a.getBoundingClientRect().height))};
    }""")
    shot(pg, "11-home-table-mobile.png")
    pg.close()

    b.close()

json.dump(M, open(os.path.join(OUT, "measurements.json"), "w"), indent=2)
print(json.dumps(M, indent=2)[:12000])
