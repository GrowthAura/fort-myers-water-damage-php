#!/usr/bin/env python3
"""S1 pixel proof: full-page screenshots, subset font (port 8145) vs full font (port 8146)."""
import os
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "qa", "screenshots", "20x-verify")
os.makedirs(os.path.join(OUT, "fontpixel"), exist_ok=True)

pages = ["/", "/cost/", "/insurance/"]
results = {}
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for slug in pages:
        name = slug.strip("/") or "home"
        shots = {}
        for label, port in [("subset", 8145), ("full", 8146)]:
            pg = b.new_page(viewport={"width": 1440, "height": 900})
            pg.goto(f"http://127.0.0.1:{port}{slug}", wait_until="networkidle")
            pg.wait_for_timeout(500)
            path = os.path.join(OUT, "fontpixel", f"{name}-{label}.png")
            pg.screenshot(path=path, full_page=True)
            shots[label] = path
            pg.close()
        a = Image.open(shots["subset"]).convert("RGB")
        c = Image.open(shots["full"]).convert("RGB")
        assert a.size == c.size, (a.size, c.size)
        diff = ImageChops.difference(a, c)
        bbox = diff.getbbox()
        n = sum(1 for px in diff.getdata() if px != (0, 0, 0))
        results[slug] = {"size": a.size, "total_pixels": a.size[0] * a.size[1],
                         "differing_pixels": n, "bbox": bbox}
        print(slug, a.size, "differing:", n, "bbox:", bbox)
    b.close()
print(results)
