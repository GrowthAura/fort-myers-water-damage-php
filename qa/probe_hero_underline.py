#!/usr/bin/env python3
"""Hero-underline probe: measure computed text-decoration on every link
inside any hero, and screenshot home + one inner-page hero (desktop +
mobile). Usage: probe_hero_underline.py <tag> — screenshots go to
qa/screenshots/20x-fixes/hero-<tag>-*.png. Serves out/ on 127.0.0.1:8147,
Playwright bundled Chromium only."""
import json
import os
import subprocess
import sys
import time

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BUILD, "out")
SHOT = os.path.join(BUILD, "qa", "screenshots", "20x-fixes")
PORT = 8147


def lum(hexcol):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return round((l1 + 0.05) / (l2 + 0.05), 2)


def main(tag):
    from playwright.sync_api import sync_playwright
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT),
                            "--bind", "127.0.0.1"],
                           cwd=OUT, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    res = {"tag": tag, "hero_links": {}, "contrast_ffd9a8": {
        "vs_#0a2e38": contrast("#ffd9a8", "#0a2e38"),
        "vs_#062028": contrast("#ffd9a8", "#062028")}}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            for slug, name in (("/", "home"), ("/water-removal/", "water-removal")):
                for vw, vname in (((1440, 900), "desktop"), ((390, 844), "mobile")):
                    pg = b.new_page(viewport={"width": vw[0], "height": vw[1]})
                    pg.goto(f"http://127.0.0.1:{PORT}{slug}")
                    time.sleep(0.4)
                    links = pg.evaluate(
                        """() => [...document.querySelectorAll('.hero a')].map(a => {
                            const cs = getComputedStyle(a);
                            return {text: a.textContent.trim().slice(0, 30),
                                    href: a.getAttribute('href'),
                                    decoration: cs.textDecorationLine,
                                    color: cs.color};
                        })""")
                    res["hero_links"][f"{name}_{vname}"] = links
                    pg.screenshot(path=os.path.join(
                        SHOT, f"hero-{tag}-{name}-{vname}.png"))
                    pg.close()
            b.close()
    finally:
        srv.terminate()
    print(json.dumps(res, indent=2))
    with open(os.path.join(SHOT, f"hero-measurements-{tag}.json"), "w") as f:
        json.dump(res, f, indent=2)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "after")
