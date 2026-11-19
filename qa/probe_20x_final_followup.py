#!/usr/bin/env python3
"""Final-verify follow-up: mobile menu Call button vs call bar (scrolled to
bottom), menu label contrast, body-tel underline control on inner pages,
cost tables scrolled into view + tbody row heights, marker + hero visuals.
Serves out/ on 127.0.0.1:8152. Playwright bundled Chromium only."""
import json, os, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
SHOT = os.path.join(ROOT, "qa", "screenshots", "20x-final-verify")
PORT = 8152


def lum(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT),
                            "-d", OUT], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    for _ in range(40):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=2)
            break
        except Exception:
            time.sleep(0.25)
    res = {}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(args=["--no-sandbox",
                                        "--disable-dev-shm-usage"])
            pg = b.new_page(viewport={"width": 390, "height": 844})
            pg.goto(f"http://127.0.0.1:{PORT}/", wait_until="networkidle")
            pg.click(".mobile-menu summary")
            pg.wait_for_timeout(500)
            res["menu_open"] = pg.evaluate("""() => {
              const d = document.querySelector('details.mobile-menu');
              const panel = document.querySelector('.mobile-menu-panel');
              const pr = panel.getBoundingClientRect();
              const dr = d.getBoundingClientRect();
              const calls = [...document.querySelectorAll('a')].filter(a =>
                /call/i.test(a.textContent)).map(a => {
                const r = a.getBoundingClientRect();
                return {cls: a.className, text: a.textContent.trim().slice(0,30),
                  parent: a.parentElement.className,
                  rect: [Math.round(r.x), Math.round(r.y),
                         Math.round(r.width), Math.round(r.height),
                         Math.round(r.bottom)],
                  visible: getComputedStyle(a).display};
              });
              const bar = document.querySelector('.call-bar, [class*="call-bar"]');
              return {detailsOpen: d.open, panelRect: [Math.round(pr.x), Math.round(pr.y),
                      Math.round(pr.width), Math.round(pr.height), Math.round(pr.bottom)],
                      detailsRect: [Math.round(dr.x), Math.round(dr.y),
                      Math.round(dr.width), Math.round(dr.height), Math.round(dr.bottom)],
                      callBarTop: bar ? Math.round(bar.getBoundingClientRect().top) : null,
                      callBarCls: bar ? bar.className : null,
                      calls};
            }""")
            # scroll the panel to its bottom and re-measure
            pg.evaluate("""() => {
              const p = document.querySelector('.mobile-menu-panel');
              p.scrollTop = p.scrollHeight;
            }""")
            pg.wait_for_timeout(400)
            res["menu_scrolled_bottom"] = pg.evaluate("""() => {
              const panel = document.querySelector('.mobile-menu-panel');
              const pr = panel.getBoundingClientRect();
              const calls = [...document.querySelectorAll('.mobile-menu-panel a')]
                .filter(a => /call/i.test(a.textContent)).map(a => {
                const r = a.getBoundingClientRect();
                return {cls: a.className, text: a.textContent.trim().slice(0,30),
                  rect: [Math.round(r.x), Math.round(r.y),
                         Math.round(r.width), Math.round(r.height),
                         Math.round(r.bottom)]};
              });
              const bar = document.querySelector('.call-bar, [class*="call-bar"]');
              return {panelRect: [Math.round(pr.x), Math.round(pr.y),
                      Math.round(pr.width), Math.round(pr.height), Math.round(pr.bottom)],
                      panelScrollTop: panel.scrollTop,
                      panelScrollH: panel.scrollHeight,
                      callBarTop: bar ? Math.round(bar.getBoundingClientRect().top) : null,
                      calls};
            }""")
            pg.screenshot(path=os.path.join(SHOT, "menu-open-mobile-bottom.png"))
            # menu label contrast: summary label + panel link colors vs panel bg
            res["menu_contrast"] = pg.evaluate("""() => {
              const out = {};
              const panel = document.querySelector('.mobile-menu-panel');
              out.panelBg = getComputedStyle(panel).backgroundColor;
              const link = document.querySelector('.mobile-menu-panel a');
              out.linkColor = getComputedStyle(link).color;
              const sum = document.querySelector('.mobile-menu summary');
              out.summaryColor = getComputedStyle(sum).color;
              out.summaryBg = getComputedStyle(sum).backgroundColor;
              const hdr = document.querySelector('header');
              out.headerBg = getComputedStyle(hdr).backgroundColor;
              return out;
            }""")
            pg.close()
            # body tel control: all tel links in <main> on water-removal + home,
            # with class + decoration
            for route in ("/water-removal/", "/cost/", "/about/"):
                pg = b.new_page(viewport={"width": 1440, "height": 900})
                pg.goto(f"http://127.0.0.1:{PORT}{route}",
                        wait_until="networkidle")
                res[f"body_tel_{route.strip('/')}"] = pg.evaluate("""() => {
                  return [...document.querySelectorAll('main a[href^="tel:"]')].map(a => {
                    const cs = getComputedStyle(a);
                    return {cls: a.className,
                      inHero: !!a.closest('section.hero'),
                      inFaq: !!a.closest('.faq-item, details'),
                      decoration: cs.textDecorationLine,
                      text: a.textContent.trim().slice(0,40)};
                  });
                }""")
                pg.close()
            # cost tables scrolled into view (mobile) + tbody rows
            pg = b.new_page(viewport={"width": 390, "height": 844})
            pg.goto(f"http://127.0.0.1:{PORT}/cost/",
                    wait_until="networkidle")
            res["cost_mobile_detail"] = pg.evaluate("""() => {
              const out = [];
              document.querySelectorAll('.table-wrap.prices table').forEach((t, i) => {
                const tb = t.querySelectorAll('tbody tr');
                const th = t.querySelectorAll('thead tr');
                out.push({table: i + 1, w: Math.round(t.getBoundingClientRect().width),
                  theadRows: [...th].map(tr => Math.round(tr.getBoundingClientRect().height)),
                  tbodyRows: [...tb].slice(0, 3).map(tr => Math.round(tr.getBoundingClientRect().height)),
                  priceColW: Math.round(t.querySelector('td:last-child').getBoundingClientRect().width)});
              });
              return out;
            }""")
            pg.evaluate("document.querySelectorAll('.table-wrap.prices')[0].scrollIntoView()")
            pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(SHOT, "cost-table1-mobile-scrolled.png"))
            pg.evaluate("document.querySelectorAll('.table-wrap.prices')[2].scrollIntoView()")
            pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(SHOT, "cost-table3-mobile-scrolled.png"))
            pg.close()
            b.close()
    finally:
        srv.terminate()
        print("server stopped by Popen handle (pid %d)" % srv.pid)
    # contrast math in python
    mc = res.get("menu_contrast", {})
    def parse(rgb):
        m = rgb.replace("rgba(", "").replace("rgb(", "").replace(")", "").split(",")
        return tuple(int(float(x)) for x in m[:3])
    if mc:
        print("menu_contrast raw:", mc)
        print("link vs panel bg: %.2f:1" % contrast(parse(mc["linkColor"]), parse(mc["panelBg"])))
        print("summary vs header bg: %.2f:1" % contrast(parse(mc["summaryColor"]), parse(mc["headerBg"])))
    print(json.dumps(res, indent=1))
    json.dump(res, open(os.path.join(SHOT, "measurements-followup.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
