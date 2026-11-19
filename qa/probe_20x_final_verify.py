#!/usr/bin/env python3
"""FINAL independent verifier probe for Fort Myers PHP 20x round.
Fresh eyes: own resolver, own measurements. Serves out/ on 127.0.0.1:8150
(http.server) and site/ via PHP router on 127.0.0.1:8151 for the 404 test.
Playwright bundled Chromium only (no executable_path).
Writes qa/screenshots/20x-final-verify/ + measurements-final.json.
"""
import json, os, re, subprocess, sys, time, urllib.parse, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
SITE = os.path.join(ROOT, "site")
SHOT = os.path.join(ROOT, "qa", "screenshots", "20x-final-verify")
os.makedirs(SHOT, exist_ok=True)
PORT_STATIC = 8150
PORT_PHP = 8151

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
LOC_PAGES = ["areas", "cape-coral", "fort-myers-beach", "estero",
             "bonita-springs", "lehigh-acres", "north-fort-myers"]
SELF_DOMAIN = ("fortmyerswaterdamagerestoration.us",
               "www.fortmyerswaterdamagerestoration.us")


def route_file(route):
    return os.path.join(OUT, "index.html") if route == "/" else \
        os.path.join(OUT, route.strip("/") + ".html")


def resolve(href, page_url):
    if not href or href.startswith(("#", "tel:", "mailto:", "javascript:")):
        return None
    if href.startswith("http"):
        u = urllib.parse.urlparse(href)
        if u.netloc not in SELF_DOMAIN:
            return None
        return u.path or "/"
    p = urllib.parse.urljoin(page_url, href).split("#")[0].split("?")[0]
    return p or "/"


def split_main(html):
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
    if not m:
        return "", html, None
    return m.group(1), html[:m.start()] + html[m.end():], m.group(0)[:200]


def static_census():
    res = {"self_chrome": {}, "self_main": {}, "spans_per_route": {},
           "tabindex_main": 0, "broken": [], "missing_frag": [],
           "hero_tel_pages": [], "external_hosts": set(), "tel_values": set()}
    # all local route targets that exist as files
    existing = set()
    for f in os.listdir(OUT):
        if f.endswith(".html"):
            existing.add("/" + f[:-5] + "/" if f != "index.html" else "/")
    for d in os.listdir(OUT):
        if os.path.isdir(os.path.join(OUT, d)) and os.path.exists(
                os.path.join(OUT, d, "index.html")):
            existing.add("/" + d + "/")
    res["existing_targets"] = sorted(existing)
    for route in ROUTES:
        html = open(route_file(route), encoding="utf-8").read()
        main_html, chrome, _ = split_main(html)
        mt = re.search(r"<main[^>]*>", html)
        if mt and 'tabindex="-1"' in mt.group(0):
            res["tabindex_main"] += 1
        for region, key in ((chrome, "self_chrome"), (main_html, "self_main")):
            n = sum(1 for h in re.findall(r'<a[^>]+href="([^"]+)"', region)
                    if resolve(h, route) == route)
            if n:
                res[key][route] = n
        res["spans_per_route"][route] = len(re.findall(
            r'<span class="nav-current[^"]*"', chrome))
        # hero INTRO tel links only: <p class="hero-intro"> containing a tel: link
        # (hero CTA buttons are also tel: links on all 34 pages — excluded here)
        for m in re.finditer(r'<p class="hero-intro">(.*?)</p>', html, re.S):
            tels = re.findall(r'<a[^>]+href="(tel:[^"]+)"', m.group(1))
            if tels:
                res["hero_tel_pages"].append(route)
                res["tel_values"].update(tels)
        # broken + fragments
        for h in re.findall(r'<a[^>]+href="([^"]+)"', html):
            if h.startswith("http"):
                u = urllib.parse.urlparse(h)
                if u.netloc not in SELF_DOMAIN:
                    res["external_hosts"].add(u.netloc)
                continue
            if h.startswith(("tel:", "mailto:", "javascript:")):
                continue
            if h.startswith("#"):
                frag = h[1:]
                if frag and not re.search(
                        r'id="%s"' % re.escape(frag), html):
                    res["missing_frag"].append((route, h))
                continue
            p = resolve(h, route)
            if p is not None and p not in existing:
                res["broken"].append((route, h, p))
    # 404 file
    h404 = open(os.path.join(OUT, "404.html"), encoding="utf-8").read()
    res["og_404"] = sorted(set(re.findall(r'property="(og:[a-z_]+)"', h404)))
    res["tw_404"] = sorted(set(re.findall(r'name="(twitter:[a-z_]+)"', h404)))
    res["canonical_404"] = h404.count('rel="canonical"')
    m = re.search(r'property="og:url" content="([^"]+)"', h404)
    res["og_url_404_file"] = m.group(1) if m else None
    res["tabindex_404"] = ('tabindex="-1"' in
                           (re.search(r"<main[^>]*>", h404).group(0)
                            if re.search(r"<main[^>]*>", h404) else ""))
    res["external_hosts"] = sorted(res["external_hosts"])
    res["tel_values"] = sorted(res["tel_values"])
    return res


def start_servers():
    s1 = subprocess.Popen([sys.executable, "-m", "http.server",
                           str(PORT_STATIC), "-d", OUT],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    s2 = subprocess.Popen(["/usr/bin/php", "-S", f"127.0.0.1:{PORT_PHP}",
                           "-t", SITE, os.path.join(SITE, "index.php")],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT_STATIC}/", timeout=2)
            break
        except Exception:
            time.sleep(0.25)
    return s1, s2


def php_404_check():
    out = {}
    for path in ("/this-page-does-not-exist-404/",
                 "/definitely-not-a-page-xyz/"):
        try:
            with urllib.request.urlopen(
                    f"http://127.0.0.1:{PORT_PHP}{path}", timeout=10) as r:
                code, body = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            code, body = e.code, e.read().decode("utf-8", "replace")
        m = re.search(r'property="og:url" content="([^"]+)"', body)
        out[path] = {"http": code,
                     "og_url": m.group(1) if m else None,
                     "og_tags": sorted(set(re.findall(r'property="(og:[a-z_]+)"', body))),
                     "tw_tags": sorted(set(re.findall(r'name="(twitter:[a-z_]+)"', body))),
                     "canonical": body.count('rel="canonical"'),
                     "tabindex_main": ('tabindex="-1"' in
                                       (re.search(r"<main[^>]*>", body).group(0)
                                        if re.search(r"<main[^>]*>", body) else "")),
                     "title": (re.search(r"<title>(.*?)</title>", body).group(1)
                               if re.search(r"<title>(.*?)</title>", body) else None)}
    return out


def browser_checks():
    from playwright.sync_api import sync_playwright
    res = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        # --- section markers (desktop) ---
        markers = {}
        for route, want in (("/water-removal/", "Services"),
                            ("/cape-coral/", "Areas"),
                            ("/about/", None), ("/cost/", "Cost-span")):
            pg = b.new_page(viewport={"width": 1440, "height": 900})
            pg.goto(f"http://127.0.0.1:{PORT_STATIC}{route}",
                    wait_until="networkidle")
            info = pg.evaluate("""() => {
              const out = {};
              document.querySelectorAll('.site-nav details').forEach(d => {
                const s = d.querySelector('summary');
                const cs = getComputedStyle(s);
                out[s.textContent.trim()] = {cls: d.className,
                  aria: s.getAttribute('aria-current'),
                  bg: cs.backgroundColor, shadow: cs.boxShadow,
                  weight: cs.fontWeight};
              });
              const top = document.querySelector('.site-nav > span.nav-current-top');
              out['top_cost_span'] = top ? top.textContent.trim() : null;
              return out;
            }""")
            markers[route] = info
            pg.screenshot(path=os.path.join(
                SHOT, f"marker-{route.strip('/').replace('/', '-') or 'home'}.png"))
            pg.close()
        res["section_markers"] = markers
        json.dump(res, open(os.path.join(SHOT, "measurements-final.json"), "w"), indent=1)
        # --- skip link keyboard test, desktop + mobile ---
        skip = {}
        for label, vp in (("desktop", {"width": 1440, "height": 900}),
                          ("mobile", {"width": 390, "height": 844})):
            pg = b.new_page(viewport=vp)
            pg.goto(f"http://127.0.0.1:{PORT_STATIC}/",
                    wait_until="networkidle")
            pg.keyboard.press("Tab")
            focused = pg.evaluate(
                "() => { const a = document.activeElement; return "
                "{tag: a.tagName, id: a.id, cls: a.className, "
                "text: a.textContent.trim(), "
                "box: JSON.stringify(a.getBoundingClientRect())}; }")
            pg.keyboard.press("Enter")
            pg.wait_for_timeout(300)
            after = pg.evaluate(
                "() => { const a = document.activeElement; return "
                "{tag: a.tagName, id: a.id, scrollY: window.scrollY}; }")
            pg.keyboard.press("Tab")
            pg.wait_for_timeout(200)
            nxt = pg.evaluate(
                "() => { const a = document.activeElement; const m = "
                "a.closest('main'); return {tag: a.tagName, "
                "href: a.getAttribute('href'), inMain: !!m, "
                "text: (a.textContent||'').trim().slice(0,40)}; }")
            skip[label] = {"focused": focused, "after_enter": after,
                           "next_tab": nxt}
            pg.screenshot(path=os.path.join(SHOT, f"skiplink-{label}.png"))
            pg.close()
        res["skip_link"] = skip
        # --- hero underline: every hero-tel page, desktop + mobile ---
        hero_pages = json.loads(open(os.path.join(SHOT, "static.json")).read())["hero_tel_pages"] \
            if os.path.exists(os.path.join(SHOT, "static.json")) else None
        res["hero"] = browser_hero(b, hero_pages)
        json.dump(res, open(os.path.join(SHOT, "measurements-final.json"), "w"), indent=1)
        # --- cost tables ---
        res["cost"] = browser_cost(b)
        json.dump(res, open(os.path.join(SHOT, "measurements-final.json"), "w"), indent=1)
        # --- regression spot checks ---
        res["regression"] = browser_regression(b)
        b.close()
    return res


def browser_hero(b, hero_pages):
    # hero_pages passed in via static result stored by caller; recompute here
    # from out/ directly to stay self-contained
    import glob
    pages = []
    for route in ROUTES:
        html = open(route_file(route), encoding="utf-8").read()
        for m in re.finditer(r'<p class="hero-intro">(.*?)</p>', html, re.S):
            if re.search(r'<a[^>]+href="tel:', m.group(1)):
                pages.append(route)
                break
    out = {"pages": pages, "per_page": {}}
    for route in pages:
        slug = route.strip("/") or "home"
        per = {}
        for label, vp in (("desktop", {"width": 1440, "height": 900}),
                          ("mobile", {"width": 390, "height": 844})):
            pg = b.new_page(viewport=vp)
            pg.goto(f"http://127.0.0.1:{PORT_STATIC}{route}",
                    wait_until="networkidle")
            info = pg.evaluate("""() => {
              const a = document.querySelector('.hero-intro a[href^="tel:"]');
              if (!a) return null;
              const cs = getComputedStyle(a);
              const r = a.getBoundingClientRect();
              return {decoration: cs.textDecorationLine, color: cs.color,
                fontSize: cs.fontSize, text: a.textContent.trim(),
                rect: [Math.round(r.x), Math.round(r.y),
                       Math.round(r.width), Math.round(r.height)]};
            }""")
            per[label] = info
            pg.screenshot(path=os.path.join(
                SHOT, f"hero-{slug}-{label}.png"))
            pg.close()
        out["per_page"][route] = per
    # control: body tel link + footer links must KEEP underlines (home page)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(f"http://127.0.0.1:{PORT_STATIC}/", wait_until="networkidle")
    ctrl = pg.evaluate("""() => {
      const out = {};
      const bodyTel = document.querySelector('main a[href^="tel:"]:not(.hero-intro a)');
      // first tel link inside main but outside the hero
      let bt = null;
      document.querySelectorAll('main a[href^="tel:"]').forEach(a => {
        if (!a.closest('section.hero') && !bt) bt = a;
      });
      if (bt) { const cs = getComputedStyle(bt);
        out.body_tel = {decoration: cs.textDecorationLine,
          text: bt.textContent.trim().slice(0,30)}; }
      const fl = document.querySelector('footer a');
      if (fl) { const cs = getComputedStyle(fl);
        out.footer_link = {decoration: cs.textDecorationLine,
          text: fl.textContent.trim().slice(0,30)}; }
      const btt = document.querySelector('footer a.back-to-top');
      if (btt) { const cs = getComputedStyle(btt);
        out.back_to_top = {decoration: cs.textDecorationLine}; }
      return out;
    }""")
    out["control_home"] = ctrl
    # control 2: a body tel link on /water-removal/ (FAQ/body) if any
    pg.goto(f"http://127.0.0.1:{PORT_STATIC}/water-removal/",
            wait_until="networkidle")
    ctrl2 = pg.evaluate("""() => {
      let bt = null;
      document.querySelectorAll('main a[href^="tel:"]').forEach(a => {
        if (!a.closest('section.hero') && !bt) bt = a;
      });
      if (!bt) return null;
      const cs = getComputedStyle(bt);
      return {decoration: cs.textDecorationLine,
              text: bt.textContent.trim().slice(0,40)};
    }""")
    out["control_water_removal_body_tel"] = ctrl2
    pg.close()
    return out


def browser_cost(b):
    out = {}
    for label, vp in (("mobile", {"width": 390, "height": 844}),
                      ("desktop", {"width": 1440, "height": 900})):
        pg = b.new_page(viewport=vp)
        pg.goto(f"http://127.0.0.1:{PORT_STATIC}/cost/",
                wait_until="networkidle")
        info = pg.evaluate("""() => {
          const tabs = [];
          document.querySelectorAll('.table-wrap.prices table').forEach(t => {
            const r = t.getBoundingClientRect();
            const last = t.querySelector('td:last-child');
            const cs = last ? getComputedStyle(last) : null;
            const rows = [...t.querySelectorAll('tr')].slice(0,3)
              .map(tr => Math.round(tr.getBoundingClientRect().height));
            tabs.push({w: Math.round(r.width),
              priceCol: last ? Math.round(last.getBoundingClientRect().width) : null,
              nowrap: cs ? cs.whiteSpace : null, rows});
          });
          return {tables: tabs, scrollW: document.documentElement.scrollWidth};
        }""")
        out[label] = info
        if label == "mobile":
            pg.screenshot(path=os.path.join(SHOT, "cost-mobile.png"))
            # first-paint visibility: price cell text in viewport?
            vis = pg.evaluate("""() => {
              const t = document.querySelector('.table-wrap.prices table');
              const td = t.querySelector('td:last-child');
              const r = td.getBoundingClientRect();
              return {top: Math.round(r.top), inViewport: r.top < 844};
            }""")
            out["mobile"]["first_price_cell"] = vis
        pg.close()
    return out


def browser_regression(b):
    out = {}
    # header height, hero full-bleed, nav carets single line (home desktop)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(f"http://127.0.0.1:{PORT_STATIC}/", wait_until="networkidle")
    out["home_desktop"] = pg.evaluate("""() => {
      const h = document.querySelector('header');
      const hero = document.querySelector('section.hero');
      const hr = hero.getBoundingClientRect();
      const sums = [...document.querySelectorAll('.site-nav details summary')]
        .map(s => ({t: s.textContent.trim(),
                    h: Math.round(s.getBoundingClientRect().height),
                    lines: Math.round(s.getBoundingClientRect().height) <= 60 ? 1 : 2}));
      const fade = getComputedStyle(document.querySelector('.table-wrap') || document.body);
      return {headerH: Math.round(h.getBoundingClientRect().height),
              hero: {x: Math.round(hr.x), w: Math.round(hr.width),
                     h: Math.round(hr.height)},
              navSummaries: sums,
              skipLink: !!document.querySelector('a.skip-link, a[href="#main"]'),
              skipText: (document.querySelector('a[href="#main"]')||{textContent:''}).textContent.trim(),
              backToTop: !!document.querySelector('a.back-to-top'),
              fetchpriority: document.querySelectorAll('[fetchpriority="high"]').length};
    }""")
    # back to top real click
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(400)
    y0 = pg.evaluate("window.scrollY")
    pg.click("a.back-to-top")
    pg.wait_for_timeout(2500)
    out["back_to_top"] = {"from": y0, "to": pg.evaluate("window.scrollY")}
    # FAQ real click
    pg.goto(f"http://127.0.0.1:{PORT_STATIC}/", wait_until="networkidle")
    faq = pg.evaluate("""() => {
      const d = document.querySelector('.faq-item details, details.faq-item');
      if (!d) return null;
      return {wasOpen: d.open};
    }""")
    try:
        pg.click(".faq-item summary")
        pg.wait_for_timeout(300)
        faq_after = pg.evaluate("""() => {
          const d = document.querySelector('.faq-item details, details.faq-item');
          return d ? {open: d.open, h: Math.round(d.getBoundingClientRect().height)} : null;
        }""")
    except Exception as e:
        faq_after = {"error": str(e)}
    out["faq"] = {"before": faq, "after_click": faq_after}
    pg.screenshot(path=os.path.join(SHOT, "faq-open-desktop.png"))
    # footer links min height (desktop)
    out["footer_links_desktop"] = pg.evaluate("""() => {
      const ls = [...document.querySelectorAll('footer a')];
      return {n: ls.length,
              minH: Math.min(...ls.map(a => a.getBoundingClientRect().height))};
    }""")
    pg.close()
    # mobile: menu Call button vs call bar, CTA top, menu labels contrast
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(f"http://127.0.0.1:{PORT_STATIC}/", wait_until="networkidle")
    pg.click(".mobile-menu summary")
    pg.wait_for_timeout(500)
    out["mobile_menu"] = pg.evaluate("""() => {
      const panel = document.querySelector('.mobile-menu-panel, .mobile-menu');
      const callBtn = [...document.querySelectorAll('a')].find(a =>
        /call/i.test(a.textContent) && a.closest('.mobile-menu-panel, .mobile-menu, header'));
      const bar = document.querySelector('.call-bar, .sticky-call, [class*="call-bar"]');
      const r = callBtn ? callBtn.getBoundingClientRect() : null;
      const br = bar ? bar.getBoundingClientRect() : null;
      const labels = [...document.querySelectorAll('.mobile-menu-panel a, .mobile-menu a')]
        .slice(0, 8).map(a => { const cs = getComputedStyle(a);
          return {t: a.textContent.trim().slice(0,20), color: cs.color}; });
      return {callBtn: r ? [Math.round(r.x), Math.round(r.y),
                             Math.round(r.bottom)] : null,
              callBarTop: br ? Math.round(br.top) : null,
              panelBottom: panel ? Math.round(panel.getBoundingClientRect().bottom) : null,
              labels};
    }""")
    pg.screenshot(path=os.path.join(SHOT, "menu-open-mobile.png"))
    # mobile CTA top worst case: sample pages
    cta = {}
    for route in ["/", "/cost/", "/insurance/", "/water-removal/", "/contact/"]:
        pg.goto(f"http://127.0.0.1:{PORT_STATIC}{route}",
                wait_until="networkidle")
        cta[route] = pg.evaluate("""() => {
          const els = [...document.querySelectorAll('section.hero a, section.hero .cta, .hero a.btn, .hero a[class*="btn"]')];
          if (!els.length) return null;
          return Math.round(Math.min(...els.map(e => e.getBoundingClientRect().top)));
        }""")
    out["mobile_cta_top"] = cta
    # table fade (home has a table? use cost mobile) + footer links mobile
    pg.goto(f"http://127.0.0.1:{PORT_STATIC}/cost/", wait_until="networkidle")
    out["table_fade"] = pg.evaluate("""() => {
      const w = document.querySelector('.table-wrap');
      if (!w) return null;
      const cs = getComputedStyle(w);
      return {mask: cs.maskImage || cs.webkitMaskImage || '',
              boxShadow: cs.boxShadow};
    }""")
    out["footer_links_mobile"] = pg.evaluate("""() => {
      const ls = [...document.querySelectorAll('footer a')];
      return {n: ls.length,
              minH: Math.min(...ls.map(a => a.getBoundingClientRect().height))};
    }""")
    pg.close()
    return out


def main():
    static = static_census()
    json.dump(static, open(os.path.join(SHOT, "static.json"), "w"), indent=1)
    print("STATIC self_chrome:", static["self_chrome"])
    print("STATIC self_main:", static["self_main"])
    print("STATIC spans total (34 routes):",
          sum(static["spans_per_route"].values()))
    print("STATIC spans per route:", static["spans_per_route"])
    print("STATIC tabindex_main:", static["tabindex_main"], "/34; 404:",
          static["tabindex_404"])
    print("STATIC hero_tel_pages (%d):" % len(static["hero_tel_pages"]),
          static["hero_tel_pages"])
    print("STATIC broken:", static["broken"], "missing_frag:",
          static["missing_frag"])
    print("STATIC 404 og:", static["og_404"], "tw:", static["tw_404"],
          "canonical:", static["canonical_404"], "og_url:", static["og_url_404_file"])
    print("STATIC tel:", static["tel_values"], "ext hosts:", static["external_hosts"])
    s1, s2 = start_servers()
    pid1, pid2 = s1.pid, s2.pid
    try:
        php404 = php_404_check()
        print("PHP404:", json.dumps(php404, indent=1))
        try:
            brow = browser_checks()
        except Exception as e:
            print("BROWSER CHECKS PARTIAL-FAIL:", repr(e))
            brow = {"_error": repr(e)}
            partial = os.path.join(SHOT, "measurements-final.json")
            if os.path.exists(partial):
                brow = json.load(open(partial))
        json.dump({"php404": php404, "browser": brow},
                  open(os.path.join(SHOT, "measurements-final.json"), "w"), indent=1)
        print("MARKERS:", json.dumps(brow["section_markers"], indent=1))
        print("SKIP:", json.dumps(brow["skip_link"], indent=1))
        print("HERO pages:", brow["hero"]["pages"])
        for r, v in brow["hero"]["per_page"].items():
            print("HERO", r, v)
        print("HERO control:", brow["hero"]["control_home"],
              brow["hero"]["control_water_removal_body_tel"])
        print("COST:", json.dumps(brow["cost"], indent=1))
        print("REGRESSION:", json.dumps(brow["regression"], indent=1))
    finally:
        for p in (s1, s2):
            try:
                p.terminate()
            except Exception:
                pass
        print("servers stopped by Popen handles (pids %d, %d)" % (pid1, pid2))


if __name__ == "__main__":
    main()
