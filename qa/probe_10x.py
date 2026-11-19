#!/usr/bin/env python3
"""10X fix-round probe: BEFORE/AFTER measurements + screenshots.
Serves out/ on 127.0.0.1:8135 (started separately). Playwright bundled Chromium only.
Usage: python3 qa/probe_10x.py <before|after>
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8135"
STAGE = sys.argv[1] if len(sys.argv) > 1 else "before"
OUT = f"/home/hatch/workspace/fort-myers-php/qa/screenshots/10x-fix/{STAGE}"
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
    return (l1 + 0.05) / (l2 + 0.05)


def parse_rgb(s):
    return tuple(int(x) for x in s.replace("rgba(", "").replace("rgb(", "").rstrip(")").split(",")[:3])


with sync_playwright() as pw:
    b = pw.chromium.launch()
    # ---------- DESKTOP 1440x900 ----------
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="load")
    pg.wait_for_timeout(400)
    m = pg.evaluate(
        """() => {
        const q = s => document.querySelector(s);
        const r = s => { const el = q(s); if (!el) return null; const b = el.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height,top:b.top,bottom:b.bottom}; };
        const summs = [...document.querySelectorAll('.site-nav summary')].map(s => {
          const b = s.getBoundingClientRect();
          return {text: s.textContent.trim(), h: b.height, w: b.width, lines: s.getClientRects().length};
        });
        const hero = q('.hero').getBoundingClientRect();
        const fl = [...document.querySelectorAll('.footer-col a')].slice(0,3).map(a => a.getBoundingClientRect().height);
        const fb = q('.footer-base a').getBoundingClientRect();
        return {
          headerH: q('.site-header').getBoundingClientRect().height,
          navSummaries: summs,
          hero: {x: hero.x, y: hero.y, w: hero.width, h: hero.height},
          footerLinkH: fl,
          footerBaseLinkH: fb.height,
          bodyFont: getComputedStyle(document.body).fontSize,
        };
      }"""
    )
    M["desktop_home"] = m
    pg.screenshot(path=f"{OUT}/01-nav-caret-desktop.png")
    # hero crop: full hero
    pg.locator(".hero").screenshot(path=f"{OUT}/02-home-hero-desktop.png")

    # cost desktop: price table
    pg.goto(BASE + "/cost/", wait_until="load")
    pg.wait_for_timeout(300)
    m = pg.evaluate(
        """() => {
        const wraps = [...document.querySelectorAll('.table-wrap')];
        return wraps.map(w => {
          const tds = [...w.querySelectorAll('tbody tr:first-child td')];
          const last = tds[tds.length-1];
          const lr = last.getBoundingClientRect();
          const rows = [...w.querySelectorAll('tbody tr')].slice(0,3).map(tr => {
            const c = tr.querySelector('td:last-child'); const r = c.getBoundingClientRect();
            return {text: c.textContent.trim().slice(0,40), h: r.height, lines: c.getClientRects().length};
          });
          return {tableW: w.getBoundingClientRect().width, lastColH: lr.height, rows};
        });
      }"""
    )
    M["desktop_cost_tables"] = m
    pg.locator(".table-wrap").first.screenshot(path=f"{OUT}/03-cost-table-desktop.png")
    pg.screenshot(path=f"{OUT}/04-cost-desktop-viewport.png")

    # D-06 stacked CTA check on cape-coral (desktop)
    pg.goto(BASE + "/cape-coral/", wait_until="load")
    pg.wait_for_timeout(300)
    m = pg.evaluate(
        """() => {
        const q = s => document.querySelector(s);
        const r = s => { const el = q(s); if (!el) return null; const b = el.getBoundingClientRect(); return {top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY)}; };
        return { heroCta: r('.hero-ctas .btn-call'), breadcrumb: r('.breadcrumb'), ctaLine: r('.cta-line .btn-call') };
      }"""
    )
    M["d06_cape_coral"] = m
    # footer on location page (desktop): brand col vs services col heights
    m = pg.evaluate(
        """() => {
        const q = s => document.querySelector(s);
        const r = s => { const el = q(s); if (!el) return null; const b = el.getBoundingClientRect(); return {h: Math.round(b.height), top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY)}; };
        return { brand: r('.footer-brand'), services: r('.footer-col'), grid: r('.footer-grid'), mapIframes: document.querySelectorAll('iframe.footer-map').length };
      }"""
    )
    M["desktop_cape_footer"] = m
    pg.locator(".site-footer").screenshot(path=f"{OUT}/05-footer-location-desktop.png")
    # home footer for comparison
    pg.goto(BASE + "/", wait_until="load")
    pg.wait_for_timeout(300)
    m = pg.evaluate(
        """() => {
        const q = s => document.querySelector(s);
        const r = s => { const el = q(s); if (!el) return null; const b = el.getBoundingClientRect(); return {h: Math.round(b.height), top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY)}; };
        return { brand: r('.footer-brand'), services: r('.footer-col'), grid: r('.footer-grid'), mapIframes: document.querySelectorAll('iframe.footer-map').length };
      }"""
    )
    M["desktop_home_footer"] = m
    pg.locator(".site-footer").screenshot(path=f"{OUT}/06-footer-home-desktop.png")
    pg.close()

    # ---------- MOBILE 390x844 ----------
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/", wait_until="load")
    pg.wait_for_timeout(400)
    m = pg.evaluate(
        """() => {
        const q = s => document.querySelector(s);
        const hero = q('.hero').getBoundingClientRect();
        const cta = q('.hero-ctas .btn-call').getBoundingClientRect();
        const wrap = q('.table-wrap');
        return {
          heroH: Math.round(hero.height), heroBottom: Math.round(hero.bottom),
          heroCta: {top: Math.round(cta.top), bottom: Math.round(cta.bottom)},
          viewportH: innerHeight,
          tableScrollW: wrap ? wrap.scrollWidth : null, tableClientW: wrap ? wrap.clientWidth : null,
          bodyFont: getComputedStyle(document.body).fontSize,
          h1: q('h1').getBoundingClientRect().height,
        };
      }"""
    )
    M["mobile_home"] = m
    pg.screenshot(path=f"{OUT}/10-home-hero-mobile-firstviewport.png")
    # table first paint: scroll into view first so content-visibility:auto
    # actually renders it (otherwise scrollWidth reports the placeholder)
    pg.locator(".table-wrap").first.scroll_into_view_if_needed()
    pg.wait_for_timeout(300)
    m = pg.evaluate(
        """() => {
        const wrap = document.querySelector('.table-wrap');
        const table = wrap.querySelector('table');
        return {tableScrollW: wrap.scrollWidth, tableClientW: wrap.clientWidth,
                tableW: Math.round(table.getBoundingClientRect().width),
                scrollLeft: wrap.scrollLeft,
                hasFade: getComputedStyle(wrap).boxShadow.includes('inset')};
      }"""
    )
    M["mobile_home_table"] = m
    pg.locator(".table-wrap").first.screenshot(path=f"{OUT}/11-home-table-mobile.png")
    pg.evaluate("window.scrollTo(0,0)")
    pg.wait_for_timeout(200)
    # menu open
    pg.click(".mobile-menu summary")
    pg.wait_for_timeout(400)
    m = pg.evaluate(
        """() => {
        const q = s => document.querySelector(s);
        const panel = q('.mobile-menu-panel').getBoundingClientRect();
        const bar = q('.call-bar').getBoundingClientRect();
        const btn = q('.mobile-menu-panel .btn').getBoundingClientRect();
        const grp = q('.mobile-menu-panel .nav-group');
        const cs = getComputedStyle(grp);
        const panelBg = getComputedStyle(q('.mobile-menu-panel')).backgroundColor;
        const links = [...document.querySelectorAll('.mobile-menu-panel a')].map(a => {
          const r = a.getBoundingClientRect(); return {t: a.textContent.trim().slice(0,30), top: Math.round(r.top), bottom: Math.round(r.bottom)};
        });
        return {
          panel: {top: Math.round(panel.top), bottom: Math.round(panel.bottom), h: Math.round(panel.height), maxH: getComputedStyle(q('.mobile-menu-panel')).maxHeight},
          callBar: {top: Math.round(bar.top), h: Math.round(bar.height)},
          menuCallBtn: {top: Math.round(btn.top), bottom: Math.round(btn.bottom)},
          navGroupColor: cs.color, panelBg,
          toggleLabel: q('.menu-label').textContent,
          toggleText: q('.mobile-menu summary').textContent.trim(),
          lastLinks: links.slice(-4),
        };
      }"""
    )
    M["mobile_menu_open"] = m
    fg = parse_rgb(m["navGroupColor"])
    bg = parse_rgb(m["panelBg"])
    M["mobile_menu_open"]["navGroupContrast"] = round(contrast(fg, bg), 2)
    # scroll the panel to its bottom: the menu's own Call button must land
    # fully above the fixed call bar when the user scrolls to the end
    M["mobile_menu_scrolled_bottom"] = pg.evaluate(
        """() => {
        const panel = document.querySelector('.mobile-menu-panel');
        panel.scrollTop = panel.scrollHeight;
        const btn = document.querySelector('.mobile-menu-panel .btn').getBoundingClientRect();
        const bar = document.querySelector('.call-bar').getBoundingClientRect();
        return {menuCallBtnBottom: Math.round(btn.bottom), callBarTop: Math.round(bar.top),
                btnVisibleAboveBar: btn.bottom <= bar.top, panelScrollTop: panel.scrollTop,
                panelScrollHeight: panel.scrollHeight};
      }"""
    )
    pg.screenshot(path=f"{OUT}/12-menu-open-mobile.png")
    # menu closed toggle label
    pg.click(".mobile-menu summary")
    pg.wait_for_timeout(300)
    M["mobile_menu_closed_label"] = pg.evaluate(
        "() => document.querySelector('.menu-label').textContent"
    )
    pg.screenshot(path=f"{OUT}/13-menu-closed-mobile.png")

    # cost mobile: prices + tel
    pg.goto(BASE + "/cost/", wait_until="load")
    pg.wait_for_timeout(300)
    m = pg.evaluate(
        """() => {
        const wraps = [...document.querySelectorAll('.table-wrap')];
        const first = wraps[0];
        const rows = [...first.querySelectorAll('tbody tr')].slice(0,3).map(tr => {
          const c = tr.querySelector('td:last-child'); const r = c.getBoundingClientRect();
          return {text: c.textContent.trim().slice(0,45), h: Math.round(r.height)};
        });
        return {rows, tableScrollW: first.scrollWidth, tableClientW: first.clientWidth};
      }"""
    )
    M["mobile_cost"] = m
    pg.locator(".table-wrap").first.scroll_into_view_if_needed()
    pg.wait_for_timeout(200)
    pg.locator(".table-wrap").first.screenshot(path=f"{OUT}/14-cost-table-mobile.png")
    # HIW mobile tel break
    pg.goto(BASE + "/how-it-works/", wait_until="load")
    pg.wait_for_timeout(300)
    m = pg.evaluate(
        """() => {
        const tels = [...document.querySelectorAll('a[href^="tel:"]')].filter(a => a.closest('.steps'));
        if (!tels.length) return {found: 0};
        const a = tels[0]; const r = a.getBoundingClientRect();
        const cs = getComputedStyle(a);
        return {found: tels.length, h: Math.round(r.height), lineHeight: cs.lineHeight, whiteSpace: cs.whiteSpace, text: a.textContent};
      }"""
    )
    M["mobile_hiw_tel"] = m
    pg.locator(".steps").first.scroll_into_view_if_needed()
    pg.wait_for_timeout(200)
    pg.locator(".steps").first.screenshot(path=f"{OUT}/15-hiw-steps-mobile.png")
    # footer links mobile (home)
    pg.goto(BASE + "/", wait_until="load")
    pg.wait_for_timeout(300)
    m = pg.evaluate(
        """() => {
        const fl = [...document.querySelectorAll('.footer-col a')].slice(0,3).map(a => Math.round(a.getBoundingClientRect().height));
        const fb = document.querySelector('.footer-base a').getBoundingClientRect();
        return {footerLinkH: fl, footerBaseLinkH: Math.round(fb.height)};
      }"""
    )
    M["mobile_footer_links"] = m
    pg.locator(".site-footer").screenshot(path=f"{OUT}/16-footer-mobile.png")
    # mobile hero heights on other page classes
    for slug, key in [("/cost/", "cost"), ("/insurance/", "insurance"), ("/cape-coral/", "cape"), ("/contact/", "contact"), ("/water-removal/", "water")]:
        pg.goto(BASE + slug, wait_until="load")
        pg.wait_for_timeout(250)
        m = pg.evaluate(
            """() => {
            const hero = document.querySelector('.hero').getBoundingClientRect();
            const cta = document.querySelector('.hero-ctas .btn-call').getBoundingClientRect();
            return {heroH: Math.round(hero.height), ctaTop: Math.round(cta.top), ctaBottom: Math.round(cta.bottom), viewportH: innerHeight};
          }"""
        )
        M[f"mobile_hero_{key}"] = m
        if key == "cost":
            pg.screenshot(path=f"{OUT}/17-cost-hero-mobile-firstviewport.png")
    pg.close()
    b.close()

with open(os.path.join(OUT, "measurements.json"), "w") as fh:
    json.dump(M, fh, indent=2)
print(json.dumps(M, indent=2))
print("saved to", OUT)
