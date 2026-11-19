#!/usr/bin/env python3
"""20X probe: BEFORE/AFTER measurements + screenshots.
Serves out/ on 127.0.0.1:8135 (started separately). Playwright bundled Chromium only.
Usage: python3 qa/probe_20x.py <before|after>
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8135"
STAGE = sys.argv[1] if len(sys.argv) > 1 else "before"
OUT = f"/home/hatch/workspace/fort-myers-php/qa/screenshots/20x/{STAGE}"
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


JS_COST = """() => {
  const wraps = [...document.querySelectorAll('.table-wrap.prices')];
  return wraps.map(w => {
    const table = w.querySelector('table');
    const lastCells = [...w.querySelectorAll('tbody tr td:last-child')];
    const firstRow = w.querySelector('tbody tr');
    const firstLast = firstRow ? firstRow.querySelector('td:last-child') : null;
    const fr = firstLast ? firstLast.getBoundingClientRect() : null;
    const cs = firstLast ? getComputedStyle(firstLast) : null;
    const rows = [...w.querySelectorAll('tbody tr')].slice(0,3).map(tr => {
      const c = tr.querySelector('td:last-child'); const r = c.getBoundingClientRect();
      return {text: c.textContent.trim().slice(0,50), h: Math.round(r.height), right: Math.round(r.right)};
    });
    return {
      tableW: Math.round(table.getBoundingClientRect().width),
      wrapClientW: w.clientWidth, wrapScrollW: w.scrollWidth,
      lastColW: fr ? Math.round(fr.width) : null,
      lastColRight: fr ? Math.round(fr.right) : null,
      priceVisibleFirstPaint: fr ? (fr.right <= innerWidth && fr.left >= 0) : null,
      whiteSpace: cs ? cs.whiteSpace : null, textAlign: cs ? cs.textAlign : null,
      rows
    };
  });
}"""

JS_TAPS = """() => {
  const out = {};
  const all = [...document.querySelectorAll('a, summary, button, [role=button]')].filter(el => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none';
  });
  out.count = all.length;
  out.sub44 = all.map(el => {
    const r = el.getBoundingClientRect();
    return {tag: el.tagName, cls: (el.className.baseVal !== undefined ? el.className.baseVal : el.className || '').toString().slice(0,40),
            text: (el.textContent || '').trim().slice(0,34), w: Math.round(r.width), h: Math.round(r.height)};
  }).filter(x => x.h < 44 || x.w < 44);
  // inline prose links are exempt in practice (WCAG 2.5.8 inline exception);
  // list them separately so the sub-44 list is not noise.
  out.inlineLinksSub44 = all.filter(el => {
    const r = el.getBoundingClientRect();
    const inBody = !!el.closest('.page-body p, .page-body li, .faq-item p, .hero-intro, .hero-areas, .breadcrumb, .details-card dd, .kind-card p, .steps p');
    return inBody && (r.height < 44 || r.width < 44);
  }).length;
  return out;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    # ---------- DESKTOP 1440x900 ----------
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE + "/", wait_until="load")
    pg.wait_for_timeout(400)
    M["desktop_home_hero"] = pg.evaluate(
        """() => {
        const hero = document.querySelector('.hero').getBoundingClientRect();
        const hm = document.querySelector('.hero-no-media');
        const cs = getComputedStyle(hm);
        return {x: Math.round(hero.x), w: Math.round(hero.width), h: Math.round(hero.height),
                bgImage: cs.backgroundImage.slice(0, 300), bg: cs.background.slice(0, 200)};
      }"""
    )
    pg.locator(".hero").screenshot(path=f"{OUT}/01-hero-desktop-home.png")
    pg.screenshot(path=f"{OUT}/01b-home-desktop-viewport.png")
    # skip link: real Tab press
    pg.keyboard.press("Tab")
    pg.wait_for_timeout(200)
    M["skip_link"] = pg.evaluate(
        """() => {
        const el = document.querySelector('.skip-link');
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        return {text: el.textContent.trim(), href: el.getAttribute('href'),
                focused: document.activeElement === el,
                x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
                color: cs.color, bg: cs.backgroundColor, visible: r.width > 0 && r.x >= 0 && r.x < innerWidth};
      }"""
    )
    pg.locator(".site-header").screenshot(path=f"{OUT}/02-skiplink-focused-desktop.png")
    # active nav (desktop, home + a service page + cost)
    M["active_nav_home"] = pg.evaluate(
        """() => [...document.querySelectorAll('[aria-current="page"]')].map(el => ({
          tag: el.tagName, cls: (el.className || '').toString().slice(0,30), text: el.textContent.trim().slice(0,30),
          bg: getComputedStyle(el).backgroundColor, decoration: getComputedStyle(el).textDecorationLine,
          color: getComputedStyle(el).color, weight: getComputedStyle(el).fontWeight}))"""
    )
    pg.goto(BASE + "/water-removal/", wait_until="load")
    pg.wait_for_timeout(300)
    M["active_nav_water"] = pg.evaluate(
        """() => [...document.querySelectorAll('header [aria-current="page"], footer [aria-current="page"]')].map(el => ({
          where: el.closest('footer') ? 'footer' : (el.closest('.nav-dropdown') ? 'dropdown' : el.closest('.mobile-menu-panel') ? 'mobile-panel' : 'header-nav'),
          tag: el.tagName, text: el.textContent.trim().slice(0,32),
          bg: getComputedStyle(el).backgroundColor, decoration: getComputedStyle(el).textDecorationLine,
          color: getComputedStyle(el).color, weight: getComputedStyle(el).fontWeight}))"""
    )
    # open Services dropdown to screenshot the active item
    pg.click(".nav-services summary")
    pg.wait_for_timeout(300)
    pg.locator(".site-header").screenshot(path=f"{OUT}/03-nav-active-desktop.png")
    # cost desktop tables
    pg.goto(BASE + "/cost/", wait_until="load")
    pg.wait_for_timeout(300)
    M["desktop_cost_tables"] = pg.evaluate(JS_COST)
    pg.locator(".table-wrap").first.screenshot(path=f"{OUT}/04-cost-table-desktop.png")
    # FAQ link affordance (home desktop)
    pg.goto(BASE + "/", wait_until="load")
    pg.wait_for_timeout(300)
    M["faq_links"] = pg.evaluate(
        """() => {
        const a = document.querySelector('.faq-item p a');
        if (!a) return null;
        const cs = getComputedStyle(a);
        const p = a.closest('p');
        const pcs = getComputedStyle(p);
        return {text: a.textContent.trim().slice(0,40), href: a.getAttribute('href'),
                decoration: cs.textDecorationLine, underlineOffset: cs.textUnderlineOffset,
                color: cs.color, bg: pcs.backgroundColor, fontSize: cs.fontSize};
      }"""
    )
    # FAQ open by real click (home desktop)
    pg.click(".faq-item summary")
    pg.wait_for_timeout(300)
    M["faq_open"] = pg.evaluate(
        """() => { const it = document.querySelector('.faq-item'); return {open: it.open, h: Math.round(it.getBoundingClientRect().height)}; }"""
    )
    pg.locator(".faq-list").first.screenshot(path=f"{OUT}/05-faq-open-desktop.png")
    # footer: back-to-top + map link presence (desktop)
    M["footer_home"] = pg.evaluate(
        """() => ({
          backToTop: !!document.querySelector('.back-to-top'),
          backToTopText: (document.querySelector('.back-to-top') || {textContent: ''}).textContent.trim(),
          mapLinks: [...document.querySelectorAll('a.map-link')].map(a => ({text: a.textContent.trim(), href: a.getAttribute('href'), target: a.getAttribute('target')})),
          footerMapIframes: document.querySelectorAll('iframe.footer-map').length,
          sectionMapIframes: document.querySelectorAll('iframe.map-embed').length })"""
    )
    pg.locator(".site-footer").screenshot(path=f"{OUT}/06-footer-desktop.png")
    # tap targets desktop (home)
    M["taps_desktop_home"] = pg.evaluate(JS_TAPS)
    pg.close()

    # ---------- MOBILE 390x844 ----------
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/cost/", wait_until="load")
    pg.wait_for_timeout(400)
    # scroll each prices table into view so content-visibility renders it
    for i in range(3):
        pg.evaluate(f"document.querySelectorAll('.table-wrap.prices')[{i}].scrollIntoView()")
        pg.wait_for_timeout(250)
    pg.evaluate("window.scrollTo(0,0)")
    pg.wait_for_timeout(200)
    M["mobile_cost_tables"] = pg.evaluate(JS_COST)
    pg.evaluate("document.querySelectorAll('.table-wrap.prices')[0].scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.locator(".table-wrap.prices").first.screenshot(path=f"{OUT}/10-cost-table1-mobile.png")
    pg.evaluate("document.querySelectorAll('.table-wrap.prices')[2].scrollIntoView()")
    pg.wait_for_timeout(200)
    pg.locator(".table-wrap.prices").nth(2).screenshot(path=f"{OUT}/11-cost-table3-mobile.png")
    pg.goto(BASE + "/", wait_until="load")
    pg.wait_for_timeout(400)
    pg.locator(".hero").screenshot(path=f"{OUT}/12-hero-mobile-home.png")
    pg.screenshot(path=f"{OUT}/12b-home-mobile-viewport.png")
    # skip link on mobile via Tab
    pg.keyboard.press("Tab")
    pg.wait_for_timeout(200)
    M["skip_link_mobile"] = pg.evaluate(
        """() => { const el = document.querySelector('.skip-link'); const r = el.getBoundingClientRect();
        return {focused: document.activeElement === el, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), visible: r.width > 0 && r.x >= 0}; }"""
    )
    # mobile menu open: active item visible?
    pg.keyboard.press("Escape")
    pg.click(".mobile-menu summary")
    pg.wait_for_timeout(400)
    M["mobile_menu_active"] = pg.evaluate(
        """() => [...document.querySelectorAll('.mobile-menu-panel [aria-current="page"]')].map(el => ({
          tag: el.tagName, text: el.textContent.trim().slice(0,30),
          bg: getComputedStyle(el).backgroundColor, decoration: getComputedStyle(el).textDecorationLine,
          color: getComputedStyle(el).color, weight: getComputedStyle(el).fontWeight}))"""
    )
    pg.screenshot(path=f"{OUT}/13-menu-open-mobile.png")
    M["taps_mobile_menu_open"] = pg.evaluate(JS_TAPS)
    pg.click(".mobile-menu summary")
    pg.wait_for_timeout(300)
    # FAQ open mobile (home)
    pg.click(".faq-item summary")
    pg.wait_for_timeout(300)
    M["faq_open_mobile"] = pg.evaluate(
        """() => { const it = document.querySelector('.faq-item'); return {open: it.open, h: Math.round(it.getBoundingClientRect().height)}; }"""
    )
    pg.locator(".faq-list").first.screenshot(path=f"{OUT}/14-faq-open-mobile.png")
    # footer mobile: back to top + map link tap sizes
    pg.evaluate("document.querySelector('.site-footer').scrollIntoView()")
    pg.wait_for_timeout(300)
    M["footer_mobile"] = pg.evaluate(
        """() => {
        const bt = document.querySelector('.back-to-top');
        const ml = document.querySelector('a.map-link');
        const r = el => el ? {w: Math.round(el.getBoundingClientRect().width), h: Math.round(el.getBoundingClientRect().height)} : null;
        return {backToTop: r(bt), mapLink: r(ml),
                backToTopText: bt ? bt.textContent.trim() : null,
                mapLinkText: ml ? ml.textContent.trim() : null};
      }"""
    )
    pg.locator(".site-footer").screenshot(path=f"{OUT}/15-footer-mobile.png")
    M["taps_mobile_home"] = pg.evaluate(JS_TAPS)
    pg.close()
    b.close()

with open(os.path.join(OUT, "measurements.json"), "w") as fh:
    json.dump(M, fh, indent=2)
print(json.dumps(M, indent=2))
print("saved to", OUT)
