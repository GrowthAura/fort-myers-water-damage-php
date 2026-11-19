#!/usr/bin/env python3
"""Export the Fort Myers PHP site to a static tree for Cloudflare Pages.

- Serves site/ with the PHP built-in server (index.php router) and fetches
  every sitemap loc; writes <path>/index.html + flat <path>.html
  (homepage -> index.html only). Canonicals carry trailing slashes.
- _redirects: no-slash -> slash 308 for every exported route.
- _headers: HTML fresh, /assets/* immutable 1y.
- 404.html from the PHP 404 template (bogus path must answer 404).
- Static files (robots, sitemap, llms, favicon, IndexNow key) + assets/
  are copied verbatim from site/.
Usage: python3 qa/export_cloudflare.py <export-dir>
NEVER run as `php qa/export_cloudflare.py` — that dumps this source and
exports nothing.
"""
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BUILD, "site")
BASE = "https://fortmyerswaterdamagerestoration.us"
PORT = 8132

STATIC_FILES = ["robots.txt", "llms.txt", "sitemap.xml", "favicon.svg",
                "5aacacd72541e41a25cbc83799292d44.txt"]  # last: IndexNow key file

# Legal pages are noindex + OUT of the sitemap, but they are real routes:
# their no-slash forms still 308 to the slash form, like every other route.
LEGAL_ROUTES = ["/privacy-policy/", "/terms/", "/disclaimer/"]


def fetch(path, expect=200):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=30) as r:
            if r.status != expect:
                raise SystemExit(f"fetch {path} -> HTTP {r.status}, expected {expect}")
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == expect:
            return e.read()
        raise SystemExit(f"fetch {path} -> HTTP {e.code}, expected {expect}")


def main():
    outdir = sys.argv[1]
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)

    server = subprocess.Popen(
        ["/usr/bin/php", "-S", f"127.0.0.1:{PORT}", "-t", SITE, os.path.join(SITE, "index.php")],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(30):
            try:
                fetch("/robots.txt")
                break
            except Exception:
                time.sleep(0.5)
        else:
            raise SystemExit("PHP server did not come up")

        sitemap = fetch("/sitemap.xml").decode("utf-8")
        locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
        assert locs, "sitemap has no locs"
        print(f"sitemap locs: {len(locs)}")

        routes = []
        for loc in locs:
            assert loc.startswith(BASE), f"loc outside base: {loc}"
            path = loc[len(BASE):] or "/"
            routes.append(path)
            html = fetch(path)
            if path == "/":
                open(os.path.join(outdir, "index.html"), "wb").write(html)
            else:
                d = os.path.join(outdir, path.strip("/"))
                os.makedirs(d, exist_ok=True)
                open(os.path.join(d, "index.html"), "wb").write(html)
                # flat <path>.html twin (same content, canonical points to slash form)
                open(os.path.join(outdir, path.strip("/") + ".html"), "wb").write(html)
            print(f"  200 {path}")

        # Legal pages: real routes, but noindex + out of the sitemap —
        # still exported as static files (and redirected, see below).
        for path in LEGAL_ROUTES:
            html = fetch(path)
            d = os.path.join(outdir, path.strip("/"))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "wb").write(html)
            open(os.path.join(outdir, path.strip("/") + ".html"), "wb").write(html)
            print(f"  200 {path} (legal, noindex)")

        # 404.html from the PHP 404 template
        html404 = fetch("/this-page-does-not-exist-404/", expect=404)
        assert b"Page Not Found" in html404, "404 body missing H1"
        open(os.path.join(outdir, "404.html"), "wb").write(html404)
        print("  404 /this-page-does-not-exist-404/ -> 404.html")

        # Static files + assets, verbatim
        for f in STATIC_FILES:
            shutil.copy(os.path.join(SITE, f), os.path.join(outdir, f))
        shutil.copytree(os.path.join(SITE, "assets"), os.path.join(outdir, "assets"))
        print("  static + assets copied")

        # _redirects: no-slash -> slash 308 for every exported route,
        # plus the legal routes (in the router, out of the sitemap).
        with open(os.path.join(outdir, "_redirects"), "w") as fh:
            for path in routes:
                if path != "/":
                    fh.write(f"{path.rstrip('/')} {path} 308\n")
            for path in LEGAL_ROUTES:
                fh.write(f"{path.rstrip('/')} {path} 308\n")
        # _headers: HTML fresh, assets immutable
        with open(os.path.join(outdir, "_headers"), "w") as fh:
            fh.write("/*.html\n  Cache-Control: no-cache\n")
            fh.write("/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n")
        print("  _redirects + _headers written")
    finally:
        server.terminate()
        server.wait(timeout=10)
    print(f"export done: {outdir}")


if __name__ == "__main__":
    main()
