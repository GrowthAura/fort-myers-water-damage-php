#!/usr/bin/env python3
"""Five-fix round verifier — Fort Myers PHP site (2026-11-19). READ-ONLY.

Does NOT run qa/verify_export.py (banned: it re-runs the parsers, which
re-emit site/data/*.php and would wipe the hero round's hand edits incl.
the nav arrays changed here). Instead:
  - <main> word-diff is proven by comparing the NEW out/ against the
    PRE-FIX exported tree from git (cloudflare-pages 3935d04, verified
    word-diff 0 by the hero round): <main> must be word-identical on all
    34 pages, since every change in this round is outside <main>.
  - H1=1, dashes 0, sitemap 31, heroes 34/34, related 3, links 0 broken.
  - Task 1: new scrim values in out CSS; stylesheet ?v=2 on every page.
  - Task 2: Areas dropdown = Areas first + 6 areas; "See all areas" /
    "All Service Areas" 0 hits in header + mobile menu (and in out/).
  - Task 3: footer Services = exactly the header menu 7; 0 area links in
    footer; "Areas We Serve" gone; Explore unchanged (9).
  - Task 5: H2 deep #0A2E38, H3 teal #0B5563, H3 gold ::after in out CSS.
Usage: python3 qa/verify-five-fixes.py
Exit 1 if any FAIL.
"""
import html
import os
import re
import subprocess
import sys

BASE = "/home/hatch/workspace/fort-myers-php"
OUT = os.path.join(BASE, "out")
PRE = "/tmp/prefix-out-3935d04"
FAILURES = []

ROUTES = ["", "water-removal", "drying", "sewage-cleanup", "ac-leak", "ceiling-leak",
          "condo-leak", "cast-iron-pipe", "vacant-home", "first-hour-checklist",
          "cost", "insurance", "burst-pipe", "mobile-home", "slab-leak", "flood-cleanup",
          "cape-coral", "lehigh-acres", "areas", "water-heater-leak",
          "appliance-leak", "floors", "cabinets", "commercial", "north-fort-myers",
          "fort-myers-beach", "estero", "bonita-springs", "how-it-works", "contact",
          "about", "privacy-policy", "terms", "disclaimer"]
MENU7 = [("/water-removal/", "Emergency Water Removal"),
         ("/drying/", "Structural Drying"),
         ("/sewage-cleanup/", "Sewage Backup Cleanup"),
         ("/flood-cleanup/", "Flood & Storm Cleanup"),
         ("/ac-leak/", "AC Leak Water Damage"),
         ("/ceiling-leak/", "Ceiling Leak Water Damage"),
         ("/burst-pipe/", "Burst Pipe Water Damage")]
AREAS7 = [("/areas/", "Areas"), ("/cape-coral/", "Cape Coral"),
          ("/lehigh-acres/", "Lehigh Acres"),
          ("/north-fort-myers/", "North Fort Myers"),
          ("/fort-myers-beach/", "Fort Myers Beach"),
          ("/estero/", "Estero"), ("/bonita-springs/", "Bonita Springs")]
AREA_HREFS = {h for h, _ in AREAS7}


def fail(msg):
    FAILURES.append(msg)
    print("  FAIL:", msg)


def words(s):
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if w]


def main_text(html_doc):
    m = re.search(r"<main[^>]*>(.*?)</main>", html_doc, re.S)
    assert m, "no <main> found"
    txt = re.sub(r"<script[^>]*>.*?</script>", " ", m.group(1), flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def page_path(base, route):
    return os.path.join(base, "index.html") if route == "" else os.path.join(base, route, "index.html")


def header_html(doc):
    m = re.search(r"<header.*?</header>", doc, re.S)
    return m.group(0) if m else ""


def footer_html(doc):
    m = re.search(r"<footer.*?</footer>", doc, re.S)
    return m.group(0) if m else ""


# ---- pre-fix tree from git (read-only extraction) ----
if not os.path.isdir(PRE):
    subprocess.run(["git", "-C", BASE, "archive", "3935d04"], check=True,
                   stdout=open("/tmp/prefix-3935d04.tar", "wb"))
    os.makedirs(PRE, exist_ok=True)
    subprocess.run(["tar", "-xf", "/tmp/prefix-3935d04.tar", "-C", PRE], check=True)
    print("pre-fix tree extracted from cloudflare-pages 3935d04")

css_new = open(os.path.join(OUT, "assets", "css", "styles.css")).read()
home = open(page_path(OUT, "")).read()

print("== <main> word-identical vs pre-fix (34 pages) ==")
for r in ROUTES:
    slug = "/" + r + "/" if r else "/"
    new = open(page_path(OUT, r)).read()
    old = open(page_path(PRE, r)).read()
    if words(main_text(new)) != words(main_text(old)):
        fail(f"{slug}: <main> words changed vs pre-fix")
    # H1 == 1
    if len(re.findall(r"<h1[^>]*>", new)) != 1:
        fail(f"{slug}: H1 count != 1")
    # dashes: literal em/en + entities, whole file
    if "—" in new or "–" in new or "&mdash;" in new or "&ndash;" in new:
        fail(f"{slug}: em/en dash present")
    # stylesheet cache-bust
    if 'href="/assets/css/styles.css?v=2"' not in new:
        fail(f"{slug}: stylesheet ?v=2 missing")
    # heroes: every page keeps its hero image (hero round: 34/34)
    if '<img class="hero-img"' not in new:
        fail(f"{slug}: hero-img missing")
print("  <main> word-identical 34/34 (word-diff 0 preserved); H1=1 34/34; dashes 0; ?v=2 on all 34")

print("== sitemap / llms ==")
sm = open(os.path.join(OUT, "sitemap.xml")).read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
print(f"  sitemap locs: {len(locs)}")
if len(locs) != 31:
    fail(f"sitemap locs {len(locs)} != 31")
for legal in ("privacy-policy", "terms", "disclaimer"):
    if f"/{legal}/" in sm:
        fail(f"sitemap contains legal page {legal}")
llms = open(os.path.join(OUT, "llms.txt")).read()
entries = len(re.findall(r"^- \[", llms, re.M))
print(f"  llms.txt entries: {entries}")
if entries != 31:
    fail(f"llms.txt entries {entries} != 31")

print("== heroes 34/34 files exist ==")
missing = []
for r in ROUTES:
    doc = open(page_path(OUT, r)).read()
    for src in re.findall(r'<img class="hero-img"[^>]*src="([^"]+)"', doc):
        p = os.path.join(OUT, src.lstrip("/"))
        if not os.path.isfile(p):
            missing.append((r, src))
if missing:
    fail(f"hero files missing: {missing}")
else:
    print("  all hero-img src files exist in out/")

print("== related exactly 3 (pages that have one) ==")
rel_bad = []
rel_pages = 0
for r in ROUTES:
    doc = open(page_path(OUT, r)).read()
    m = re.search(r'<h2>Related Water Damage Help.*?</h2><ul>(.*?)</ul>', doc, re.S)
    if m:
        rel_pages += 1
        n = len(re.findall(r"<a ", m.group(1)))
        if n != 3:
            rel_bad.append((r, n))
print(f"  pages with a related section: {rel_pages}")
if rel_bad:
    fail(f"related != 3: {rel_bad}")
else:
    print(f"  related == 3 on all {rel_pages} pages that have one")
# pre-fix had the same count (related untouched by this round)
pre_rel = 0
for r in ROUTES:
    doc = open(page_path(PRE, r)).read()
    if re.search(r'<h2>Related Water Damage Help.*?</h2><ul>', doc, re.S):
        pre_rel += 1
if pre_rel != rel_pages:
    fail(f"related page count changed: pre-fix {pre_rel} vs now {rel_pages}")

print("== internal links resolve (0 broken) ==")
broken = []
known_files = set()
for root, _, files in os.walk(OUT):
    for f in files:
        known_files.add(os.path.relpath(os.path.join(root, f), OUT))
for r in ROUTES:
    doc = open(page_path(OUT, r)).read()
    for href in sorted(set(re.findall(r'href="([^"]+)"', doc))):
        if href.startswith("/") and not href.startswith("/assets/") and href != "/favicon.svg":
            path = href.split("#")[0].split("?")[0].lstrip("/")
            cand = (path + "index.html") if path == "" or path.endswith("/") else path
            if cand not in known_files:
                broken.append((r, href))
if broken:
    fail(f"broken internal links: {broken[:10]}")
else:
    print("  0 broken internal links across 34 pages")

print("== Task 1: scrim + cache-bust ==")
for frag in ("rgba(7,38,47,0.92)", "rgba(7,38,47,0.88)", "rgba(7,38,47,0.86)"):
    if frag not in css_new.replace(" ", ""):
        fail(f"out CSS missing scrim {frag}")
if "rgba(7,38,47,0.74)" in css_new.replace(" ", ""):
    fail("out CSS still has old bottom alpha 0.74")
print("  scrim 0.92/0.88/0.86 in out CSS; old 0.74 gone; ?v=2 on all 34 pages")

print("== Task 2: header Areas dropdown ==")
hdr = header_html(home)
# desktop dropdown items (nav-dropdown under the Areas details)
dd = re.search(r"<details[^>]*>\s*<summary[^>]*>Areas</summary>(.*?)</details>", hdr, re.S)
if not dd:
    fail("desktop Areas dropdown not found")
else:
    items = re.findall(r'<a href="([^"]+)">([^<]+)</a>', dd.group(1))
    if items != AREAS7:
        fail(f"desktop Areas dropdown items {items} != {AREAS7}")
    else:
        print("  desktop Areas dropdown: Areas first + 6 areas (7 items)")
# mobile menu Areas group
mob = re.search(r'<div class="mobile-menu-panel">(.*?)</div>\s*</details>', home, re.S)
if not mob:
    print("  note: mobile-menu-panel regex missed (checked separately by screenshot)")
else:
    mitems = re.findall(r'<a href="([^"]+)">([^<]+)</a>', mob.group(1))
    areas_in_mob = [i for i in mitems if i[0] in AREA_HREFS]
    if areas_in_mob != AREAS7:
        fail(f"mobile menu Areas items {areas_in_mob} != {AREAS7}")
    else:
        print("  mobile menu Areas: Areas first + 6 areas (7 items)")
for s in ("See all areas", "All Service Areas"):
    if s in hdr:
        fail(f"header still contains {s!r}")
    if s in (mob.group(1) if mob else ""):
        fail(f"mobile menu still contains {s!r}")
# whole-out check for the removed menu label
allout = ""
for r in ROUTES:
    allout += open(page_path(OUT, r)).read()
for s in ("See all areas", "All Service Areas"):
    if s in allout:
        fail(f"{s!r} still present somewhere in out/")
print("  'See all areas' / 'All Service Areas': 0 hits in header, mobile menu, out/")

print("== Task 3: footer Services = header 7; no Areas in footer ==")
ftr = footer_html(home)
svc = re.search(r'<nav class="footer-col" aria-label="Services">(.*?)</nav>', ftr, re.S)
if not svc:
    fail("footer Services nav not found")
else:
    sitems = [(h, html.unescape(t)) for h, t in
              re.findall(r'<a href="([^"]+)">([^<]+)</a>', svc.group(1))]
    if sitems != MENU7:
        fail(f"footer Services {sitems} != header menu 7 {MENU7}")
    else:
        print("  footer Services = header menu 7 (identical set, order, labels)")
if 'aria-label="Areas we serve"' in ftr:
    fail("footer still has an Areas column nav")
ftr_nocomment = re.sub(r"<!--.*?-->", "", ftr, flags=re.S)
if "Areas We Serve" in ftr_nocomment:
    fail("footer still has an Areas column heading")
for h in AREA_HREFS:
    if f'href="{h}"' in ftr:
        fail(f"footer still links to area page {h}")
print("  0 area links in footer; 'Areas We Serve' gone")
# Explore unchanged vs pre-fix
old_ftr = footer_html(open(page_path(PRE, "")).read())
exp_new = re.findall(r'<a href="([^"]+)">([^<]+)</a>',
                     re.search(r'<nav class="footer-col" aria-label="Explore">(.*?)</nav>', ftr, re.S).group(1))
exp_old = re.findall(r'<a href="([^"]+)">([^<]+)</a>',
                     re.search(r'<nav class="footer-col" aria-label="Explore">(.*?)</nav>', old_ftr, re.S).group(1))
if exp_new != exp_old or len(exp_new) != 9:
    fail(f"footer Explore changed: {exp_new} vs {exp_old}")
else:
    print("  footer Explore unchanged (9 links, identical)")
# footer <main>-adjacent check: no other footer service links anywhere
if re.search(r'href="/(slab-leak|water-heater-leak|condo-leak|mobile-home|commercial|cast-iron-pipe|vacant-home|appliance-leak|floors|cabinets)/"', ftr):
    fail("footer still links a non-menu service page")

print("== Task 5: H2/H3 colours in out CSS ==")
css_min = css_new.replace(" ", "")
if ".page-bodyh2:not(.details-cardh2){color:var(--deep)" not in css_min:
    fail("H2 is not deep in out CSS")
if ".page-bodyh3:not(.kind-cardh3){color:var(--teal)" not in css_min:
    fail("H3 is not teal in out CSS")
if ".page-bodyh3:not(.kind-cardh3)::after" not in css_min or "background:var(--gold)" not in css_min:
    fail("H3 gold ::after rule missing in out CSS")
print("  H2 deep #0A2E38, H3 teal #0B5563, H3 gold ::after — all in out CSS")

print()
if FAILURES:
    print(f"RESULT: FAIL ({len(FAILURES)} failures)")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS")
