#!/usr/bin/env python3
"""20x-fixes probe: self-link census (nav chrome vs <main>), tabindex on
<main>, og:url on 404, skip-link keyboard focus, /cost/ mobile tables,
plus screenshots of the changed areas. Static census runs on out/;
browser checks serve out/ on 127.0.0.1:8146 with Playwright bundled
Chromium only (no executable_path)."""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BUILD, "out")
SHOT = os.path.join(BUILD, "qa", "screenshots", "20x-fixes")
PORT = 8146

ROUTES = ["/", "/water-removal/", "/drying/", "/sewage-cleanup/",
          "/ac-leak/", "/ceiling-leak/", "/condo-leak/",
          "/cast-iron-pipe/", "/vacant-home/", "/first-hour-checklist/",
          "/cost/", "/insurance/", "/burst-pipe/", "/mobile-home/",
          "/slab-leak/", "/flood-cleanup/", "/cape-coral/", "/lehigh-acres/",
          "/areas/", "/water-heater-leak/", "/appliance-leak/", "/floors/",
          "/cabinets/", "/commercial/", "/north-fort-myers/",
          "/fort-myers-beach/", "/estero/", "/bonita-springs/",
          "/how-it-works/", "/contact/", "/privacy-policy/", "/terms/",
          "/disclaimer/", "/about/"]


def route_file(route):
    if route == "/":
        return os.path.join(OUT, "index.html")
    return os.path.join(OUT, route.strip("/") + ".html")


def resolve(href, page_url):
    """Resolve href against the page URL; return path or None if not local."""
    if not href or href.startswith(("#", "tel:", "mailto:", "javascript:")):
        return None
    if href.startswith("http"):
        u = urllib.parse.urlparse(href)
        if u.netloc not in ("fortmyerswaterdamagerestoration.us",
                            "www.fortmyerswaterdamagerestoration.us"):
            return None
        return u.path or "/"
    return urllib.parse.urljoin(page_url, href).split("#")[0].split("?")[0] or "/"


def static_census():
    res = {"nav_self": 0, "main_self": 0, "nav_self_by_page": {},
           "main_self_by_page": {}, "nav_current_spans": 0,
           "main_tabindex": 0, "main_total": 0, "og_404": {},
           "brand_self_home": 0, "mobile_home_self": 0}
    for route in ROUTES:
        f = route_file(route)
        html = open(f, encoding="utf-8").read()
        # split chrome vs main: header is before <main, footer after </main>
        m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
        main_html = m.group(1) if m else ""
        main_tag = re.search(r"<main[^>]*>", html)
        res["main_total"] += 1
        if main_tag and 'tabindex="-1"' in main_tag.group(0):
            res["main_tabindex"] += 1
        chrome = html[:m.start()] + html[m.end():] if m else html
        for region, key in ((chrome, "nav_self"), (main_html, "main_self")):
            n = 0
            for href in re.findall(r'<a[^>]+href="([^"]+)"', region):
                if resolve(href, route) == route:
                    n += 1
            res[key] += n
            if n:
                res[key + "_by_page"][route] = n
        res["nav_current_spans"] += len(re.findall(
            r'<span class="nav-current[^"]*"', chrome))
        # brand + mobile Home self-links on home (root-link rule check)
        if route == "/":
            res["brand_self_home"] = len(re.findall(
                r'<a class="brand" href="/"[^>]*aria-current="page"', chrome))
            res["mobile_home_self"] = len(re.findall(
                r'<a href="/"[^>]*aria-current="page">Home</a>', chrome))
    # 404 output
    h404 = open(os.path.join(OUT, "404.html"), encoding="utf-8").read()
    for tag in ("og:title", "og:description", "og:type", "og:url",
                "og:site_name", "og:locale", "twitter:card", "twitter:title",
                "twitter:description"):
        res["og_404"][tag] = 1 if f'property="{tag}"' in h404 or \
            f'name="{tag}"' in h404 else 0
    m404 = re.search(r"<main[^>]*>", h404)
    res["og_404"]["main_tabindex"] = 1 if m404 and \
        'tabindex="-1"' in m404.group(0) else 0
    return res


def browser_checks():
    from playwright.sync_api import sync_playwright
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT),
                            "--bind", "127.0.0.1"],
                           cwd=OUT, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    out = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            # --- skip-link focus, desktop + mobile ---
            for name, vw in (("desktop", (1440, 900)), ("mobile", (390, 844))):
                pg = b.new_page(viewport={"width": vw[0], "height": vw[1]})
                pg.goto(f"http://127.0.0.1:{PORT}/water-removal/")
                pg.keyboard.press("Tab")
                focused = pg.evaluate(
                    "() => { const a = document.activeElement; return a ? "
                    "a.className + '|' + a.textContent.trim() : 'NONE'; }")
                pg.keyboard.press("Enter")
                time.sleep(0.4)
                ae = pg.evaluate(
                    "() => document.activeElement ? "
                    "document.activeElement.tagName + '#' + "
                    "(document.activeElement.id || '') : 'NONE'")
                scroll = pg.evaluate("() => Math.round(window.scrollY)")
                pg.keyboard.press("Tab")
                ae2 = pg.evaluate(
                    "() => document.activeElement ? "
                    "document.activeElement.tagName + '.' + "
                    "(document.activeElement.className.baseVal !== undefined ? '' : document.activeElement.className) + '#' + "
                    "(document.activeElement.id || '') : 'NONE'")
                out[f"skiplink_{name}"] = {"tab_focused": focused,
                                           "after_enter_activeElement": ae,
                                           "scrollY_after_enter": scroll,
                                           "after_next_tab": ae2}
                pg.close()
            # --- screenshots: mobile menu open on service page ---
            pg = b.new_page(viewport={"width": 390, "height": 844})
            pg.goto(f"http://127.0.0.1:{PORT}/water-removal/")
            pg.click(".mobile-menu summary")
            time.sleep(0.4)
            pg.screenshot(path=os.path.join(SHOT, "01-mobile-menu-water-removal.png"))
            # closed header: Services summary current-section marker
            pg.goto(f"http://127.0.0.1:{PORT}/water-removal/")
            time.sleep(0.3)
            pg.screenshot(path=os.path.join(SHOT, "02-header-closed-water-removal.png"))
            # footer on a service page (desktop + mobile)
            pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.5)
            pg.screenshot(path=os.path.join(SHOT, "03-footer-mobile-water-removal.png"))
            pg.close()
            pg = b.new_page(viewport={"width": 1440, "height": 900})
            pg.goto(f"http://127.0.0.1:{PORT}/water-removal/")
            pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.5)
            pg.screenshot(path=os.path.join(SHOT, "04-footer-desktop-water-removal.png"))
            # desktop dropdown open on a service page
            pg.goto(f"http://127.0.0.1:{PORT}/water-removal/")
            pg.click(".site-nav details.nav-services summary")
            time.sleep(0.4)
            pg.screenshot(path=os.path.join(SHOT, "05-dropdown-desktop-water-removal.png"))
            # skip-link focused shot (desktop)
            pg.keyboard.press("Tab")
            time.sleep(0.3)
            pg.screenshot(path=os.path.join(SHOT, "06-skiplink-focused-desktop.png"))
            # 404 page
            pg.goto(f"http://127.0.0.1:{PORT}/this-page-does-not-exist-404/")
            time.sleep(0.3)
            pg.screenshot(path=os.path.join(SHOT, "07-404-desktop.png"))
            # /cost/ mobile tables
            pg2 = b.new_page(viewport={"width": 390, "height": 844})
            pg2.goto(f"http://127.0.0.1:{PORT}/cost/")
            time.sleep(0.5)
            tables = pg2.evaluate(
                """() => [...document.querySelectorAll('.table-wrap.prices table')].map(t => {
                    const r = t.getBoundingClientRect();
                    const last = t.querySelector('td:last-child');
                    const lr = last ? last.getBoundingClientRect() : null;
                    return {w: Math.round(r.width), priceColW: lr ? Math.round(lr.width) : null,
                            priceVisible: lr ? (lr.right <= innerWidth + 1 && lr.left >= -1) : null};
                })""")
            out["cost_mobile_tables"] = tables
            out["cost_mobile_scrollWidth"] = pg2.evaluate(
                "() => document.documentElement.scrollWidth")
            pg2.screenshot(path=os.path.join(SHOT, "08-cost-mobile.png"))
            pg2.close()
            pg.close()
            b.close()
    finally:
        srv.terminate()
    return out


if __name__ == "__main__":
    os.makedirs(SHOT, exist_ok=True)
    res = static_census()
    res["browser"] = browser_checks()
    print(json.dumps(res, indent=2))
    with open(os.path.join(SHOT, "measurements.json"), "w") as f:
        json.dump(res, f, indent=2)
