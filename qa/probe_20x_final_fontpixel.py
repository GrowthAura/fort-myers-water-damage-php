#!/usr/bin/env python3
"""Font subset pixel spot-check: home full page, subset fonts (out/, :8153)
vs full fonts (/tmp/out-fullfont-final, :8154). Playwright bundled Chromium."""
import os, subprocess, sys, time, urllib.request
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = os.path.join(ROOT, "qa", "screenshots", "20x-final-verify", "fontpixel")
os.makedirs(SHOT, exist_ok=True)


def wait(port):
    for _ in range(40):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2)
            return
        except Exception:
            time.sleep(0.25)


def main():
    s1 = subprocess.Popen([sys.executable, "-m", "http.server", "8153", "-d",
                           os.path.join(ROOT, "out")],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    s2 = subprocess.Popen([sys.executable, "-m", "http.server", "8154", "-d",
                           "/tmp/out-fullfont-final"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait(8153); wait(8154)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(args=["--no-sandbox",
                                        "--disable-dev-shm-usage"])
            shots = {}
            for label, port in (("subset", 8153), ("full", 8154)):
                pg = b.new_page(viewport={"width": 1440, "height": 900})
                pg.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle")
                pg.wait_for_timeout(600)
                p = os.path.join(SHOT, f"home-{label}.png")
                pg.screenshot(path=p, full_page=True)
                shots[label] = p
                pg.close()
            b.close()
        a = Image.open(shots["subset"]).convert("RGB")
        c = Image.open(shots["full"]).convert("RGB")
        print("sizes:", a.size, c.size)
        assert a.size == c.size
        diff = ImageChops.difference(a, c)
        n = sum(1 for px in diff.getdata() if px != (0, 0, 0))
        print("home total pixels:", a.size[0] * a.size[1],
              "differing:", n, "bbox:", diff.getbbox())
    finally:
        for s in (s1, s2):
            s.terminate()
        print("servers stopped by Popen handles")


if __name__ == "__main__":
    main()
