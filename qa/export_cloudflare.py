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
- llms-full.txt is GENERATED here from the same fetched HTML (31 sitemap
  pages, full visible text, no invented words) and linked from llms.txt.
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
import html as html_lib
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


def page_text(html_bytes):
    """Visible text of one fetched page, in document order — no words
    invented, none dropped except markup/script/style. Returns
    (title, [lines]). Used ONLY for llms-full.txt."""
    doc = html_bytes.decode("utf-8")
    m = re.search(r"<title>(.*?)</title>", doc, re.S)
    title = html_lib.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
    main = re.search(r"<main[^>]*>(.*?)</main>", doc, re.S).group(1)
    main = re.sub(r"<script[^>]*>.*?</script>", " ", main, flags=re.S)
    main = re.sub(r"</(h1|h2|h3|p|li|tr|div|section|details|summary)>", "\n", main)
    main = re.sub(r"<[^>]+>", " ", main)
    text = html_lib.unescape(main)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.split("\n")]
    return title, [ln for ln in lines if ln]


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
        pages_html = {}
        for loc in locs:
            assert loc.startswith(BASE), f"loc outside base: {loc}"
            path = loc[len(BASE):] or "/"
            routes.append(path)
            html = fetch(path)
            pages_html[path] = html
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

        # 20x E3: llms-full.txt — full text of every sitemap page, generated
        # HERE from the same fetched HTML that became the pages above, so it
        # cannot drift from the export: every export regenerates it from
        # the same bytes. Legal pages are out of the sitemap, so out here too.
        full_lines = [
            "# Fort Myers Water Damage Restoration Pros - llms-full.txt",
            "# Full text of every page listed in llms.txt, in the same order.",
            "# Generated by qa/export_cloudflare.py from the same fetched HTML",
            "# as the export itself (regenerated on every export; never edited",
            "# by hand). No words invented: this is the pages' own visible text.",
            "",
        ]
        for path in routes:
            url = BASE + path
            title, lines = page_text(pages_html[path])
            assert title and lines, f"llms-full: empty page {path}"
            full_lines.append(f"## {title}")
            full_lines.append(url)
            full_lines.append("")
            full_lines.extend(lines)
            full_lines.append("")
            full_lines.append("---")
            full_lines.append("")
        full_path = os.path.join(outdir, "llms-full.txt")
        open(full_path, "w", encoding="utf-8").write("\n".join(full_lines))
        assert len(routes) == 31, f"llms-full: {len(routes)} pages, expected 31"
        print(f"  llms-full.txt written: {len(routes)} pages, "
              f"{os.path.getsize(full_path)} bytes")

        # 10x fix (speed §5 fix 3): minify styles.css IN THE EXPORT ONLY —
        # the source in site/ stays readable. rcssmin preserves the spaces
        # calc() requires and quoted content strings; the asserts below
        # prove both survived. If rcssmin is missing the export still
        # succeeds with unminified CSS and a loud warning.
        css_path = os.path.join(outdir, "assets", "css", "styles.css")
        try:
            import rcssmin
            raw_css = open(css_path, encoding="utf-8").read()
            min_css = rcssmin.cssmin(raw_css)
            assert "calc(100dvh - 80px - 66px)" in min_css, "minifier broke calc() spacing"
            assert "25BE" in min_css, "minifier broke the nav caret content"
            assert "/*" not in min_css, "minifier left comments behind"
            assert len(min_css) < len(raw_css), "minifier did not shrink the CSS"
            open(css_path, "w", encoding="utf-8").write(min_css)
            print(f"  styles.css minified: {len(raw_css)} -> {len(min_css)} bytes")
        except ImportError:
            print("  WARNING: rcssmin not installed, styles.css shipped unminified")

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
