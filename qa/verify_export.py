#!/usr/bin/env python3
"""Verify the exported static tree (out/) against the pastes, end to end.

Checks per page (31 content + 3 legal):
  - H1 count == 1, H1/title/meta byte-match the paste
  - given schema JSON-LD parses and equals the paste schema exactly
    (content pages only — legal pages carry NO JSON-LD at all)
  - FAQPage script: mainEntity count == visible FAQ count, Q names match
  - BreadcrumbList script (inner content only): names match the visible breadcrumb
  - legal pages: robots noindex, follow; absent from sitemap + llms;
    visible breadcrumb reads Home » H1; "Last updated" line where ordered
  - <main> ordered word list == paste copy words (+ known chrome insertions)
  - every (/slug/) link from the paste renders as <a href> with the same anchor
  - all internal hrefs resolve to the planned 34 routes or a static asset
  - no self-links inside <main> (reported, not fatal: homepage (/) annotations)
  - 0 em/en dashes anywhere in the rendered HTML
Also: sitemap 31 locs (lastmod 2026-11-19, no image entries, no legal pages),
_redirects 33 lines (30 content + 3 legal), robots.txt + llms.txt (31 entries)
+ IndexNow key present, 404.html has no canonical.
Usage: python3 qa/verify_export.py [outdir]
"""
import html
import json
import os
import re
import sys

BASE = "/home/hatch/workspace/fort-myers-php"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "out")
sys.path.insert(0, os.path.join(BASE, "tools"))
import parse_page as pp

PLANNED = pp.PLANNED
PHONE = "239-356-3708"
LEGAL_SLUGS = {"/privacy-policy/", "/terms/", "/disclaimer/"}
FAILURES = []
NOTES = []


def words(s):
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if w]


def fail(msg):
    FAILURES.append(msg)
    print("  FAIL:", msg)


def note(msg):
    NOTES.append(msg)
    print("  note:", msg)


def main_text(html_doc):
    m = re.search(r"<main[^>]*>(.*?)</main>", html_doc, re.S)
    assert m, "no <main> found"
    txt = re.sub(r"<script[^>]*>.*?</script>", " ", m.group(1), flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def group_for(slug):
    if slug in ("/cost/", "/insurance/", "/first-hour-checklist/", "/how-it-works/", "/contact/"):
        return "guide"
    if slug in ("/cape-coral/", "/lehigh-acres/", "/north-fort-myers/",
                "/fort-myers-beach/", "/estero/", "/bonita-springs/", "/areas/"):
        return "area"
    if slug in LEGAL_SLUGS:
        return "legal"
    if slug == "/about/":
        # About is not a service page: breadcrumb Home » H1, no middle crumb.
        return "about"
    return "service"


def check_page(slug, title, meta, h1, schema, blocks, want_words, faq_n, extra_words=()):
    path = "index.html" if slug == "/" else f"{slug.strip('/')}/index.html"
    doc = open(os.path.join(OUT, path)).read()
    legal = slug in LEGAL_SLUGS
    print(f"== {slug} ==")
    # dashes
    if "—" in doc or "–" in doc:
        fail(f"{slug}: em/en dash present in rendered HTML")
    # H1
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", doc, re.S)
    if len(h1s) != 1:
        fail(f"{slug}: H1 count {len(h1s)}")
    elif html.unescape(re.sub(r"<[^>]+>", "", h1s[0])).strip() != h1:
        fail(f"{slug}: H1 text mismatch: {h1s[0]!r}")
    # title / meta
    m = re.search(r"<title>(.*?)</title>", doc, re.S)
    if not m or html.unescape(m.group(1)) != title:
        fail(f"{slug}: title mismatch: {m.group(1) if m else None!r}")
    m = re.search(r'<meta name="description" content="([^"]*)"', doc)
    if not m or html.unescape(m.group(1)) != meta:
        fail(f"{slug}: meta mismatch")
    # canonical + robots
    m = re.search(r'<link rel="canonical" href="([^"]*)"', doc)
    expect_canon = "https://fortmyerswaterdamagerestoration.us" + slug
    if not m or m.group(1) != expect_canon:
        fail(f"{slug}: canonical {m.group(1) if m else None!r} != {expect_canon}")
    m = re.search(r'<meta name="robots" content="([^"]*)"', doc)
    expect_robots = "noindex, follow" if legal else "index, follow"
    if not m or m.group(1) != expect_robots:
        fail(f"{slug}: robots {m.group(1) if m else None!r} != {expect_robots}")
    # ld+json scripts
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S)
    if legal:
        if scripts:
            fail(f"{slug}: legal page must carry NO JSON-LD, found {len(scripts)} script(s)")
        # visible breadcrumb must still read Home » H1 (no schema to match)
        bm = re.search(r'<nav class="breadcrumb[^>]*>(.*?)</nav>', doc, re.S)
        if not bm:
            fail(f"{slug}: visible breadcrumb missing")
        else:
            bwords = words(html.unescape(re.sub(r"<[^>]+>", " ", bm.group(1))))
            if bwords != ["Home"] + words(h1):
                fail(f"{slug}: visible breadcrumb {bwords} != Home + H1")
    elif not scripts:
        fail(f"{slug}: no ld+json scripts")
    else:
        try:
            given = json.loads(scripts[0])
        except Exception as e:
            fail(f"{slug}: given schema does not parse: {e}")
            given = None
        if given is not None and given != schema:
            fail(f"{slug}: given schema != paste schema")
            for k in set(list(given.keys()) + list(schema.keys())):
                if given.get(k) != schema.get(k):
                    print(f"    schema key {k!r}: rendered {given.get(k)!r} vs paste {schema.get(k)!r}")
        # FAQPage
        faqs = [b for b in blocks if b["type"] == "faq"]
        faq_items = faqs[0]["items"] if faqs else []
        faq_scripts = [json.loads(s) for s in scripts[1:] if '"FAQPage"' in s]
        if faq_items:
            if len(faq_scripts) != 1:
                fail(f"{slug}: FAQPage scripts {len(faq_scripts)}")
            else:
                ent = faq_scripts[0].get("@graph", [faq_scripts[0]])[0].get("mainEntity", [])
                if len(ent) != len(faq_items):
                    fail(f"{slug}: FAQPage entities {len(ent)} != visible {len(faq_items)}")
                for e, f in zip(ent, faq_items):
                    if e.get("name") != f["q"]:
                        fail(f"{slug}: FAQ Q mismatch: {e.get('name')!r} vs {f['q']!r}")
                    if e.get("acceptedAnswer", {}).get("text") != pp.seg_text(f["a"]):
                        fail(f"{slug}: FAQ A mismatch for {f['q']!r}")
        # BreadcrumbList (inner only)
        if slug != "/":
            crumb_scripts = [json.loads(s) for s in scripts[1:] if '"BreadcrumbList"' in s]
            if len(crumb_scripts) != 1:
                fail(f"{slug}: BreadcrumbList scripts {len(crumb_scripts)}")
            else:
                items = crumb_scripts[0].get("@graph", [crumb_scripts[0]])[0].get("itemListElement", [])
                names = [i.get("name") for i in items]
                grp = group_for(slug)
                expect_names = ["Home"] + (["Services"] if grp == "service" else ["Areas"] if grp == "area" else []) + [h1]
                if names != expect_names:
                    fail(f"{slug}: breadcrumb names {names} != {expect_names}")
    # <main> ordered word-diff vs paste (+ chrome insertions)
    actual = words(main_text(doc))
    if slug == "/":
        expected = want_words
    else:
        hero_intro = blocks[0]
        assert hero_intro["type"] == "hero-intro"
        prefix = words(h1) + words(pp.seg_text(hero_intro["segs"]))
        assert want_words[:len(prefix)] == prefix, f"{slug}: prefix mismatch"
        grp = group_for(slug)
        crumbs = ["Home"] + (["Services"] if grp == "service" else ["Areas"] if grp == "area" else []) + words(h1)
        expected = prefix + ["Call", "239", "356", "3708"] + crumbs + list(extra_words) + want_words[len(prefix):]
    if actual != expected:
        fail(f"{slug}: <main> word-diff != 0 (actual {len(actual)} vs expected {len(expected)})")
        for k, (a, b) in enumerate(zip(actual, expected)):
            if a != b:
                print(f"    FIRST DIFF at word {k}: rendered {a!r} expected {b!r}")
                print("    rendered ctx:", actual[max(0, k - 8):k + 8])
                print("    expected ctx:", expected[max(0, k - 8):k + 8])
                break
        if len(actual) != len(expected):
            print(f"    lengths actual={len(actual)} expected={len(expected)}")
    else:
        print(f"  <main> word-diff 0 ({len(actual)} words)")
    # paste links render with the same anchor
    for b in blocks:
        segs_list = []
        t = b["type"]
        if t in ("hero-intro", "p"):
            segs_list = [b["segs"]]
        elif t == "hero":
            segs_list = [b["intro"], b["areas"]]
        elif t == "details":
            segs_list = [r["value"] for r in b["rows"]]
        elif t == "ul":
            segs_list = b["items"]
        elif t == "table":
            segs_list = b["head"] + [c for r in b["rows"] for c in r]
        elif t == "kinds":
            segs_list = [k["body"] for k in b["items"]]
        elif t == "steps":
            segs_list = [s["body"] for s in b["items"]]
        elif t == "steps-rich":
            for s in b["items"]:
                for part in s["parts"]:
                    if part["type"] == "p":
                        segs_list.append(part["segs"])
                    elif part["type"] == "ul":
                        segs_list.extend(part["items"])
        elif t == "steps-numbered":
            segs_list = b["items"]
        elif t == "faq":
            segs_list = [f["a"] for f in b["items"]]
        for segs in segs_list:
            for s in segs:
                if s.get("href"):
                    pat = f'<a href="{re.escape(s["href"])}">{re.escape(html.escape(s["t"]))}</a>'
                    if not re.search(pat, doc):
                        # anchor may contain & escaped differently; try unescaped-doc search
                        if f'href="{s["href"]}"' not in doc or html.unescape(s["t"]) not in html.unescape(doc):
                            fail(f"{slug}: link not rendered: {s['t']!r} -> {s['href']}")
    # all internal hrefs planned; self-links in <main>
    main_html = re.search(r"<main[^>]*>(.*?)</main>", doc, re.S).group(1)
    for href in sorted(set(re.findall(r'href="([^"]+)"', doc))):
        if href.startswith("/") and not href.startswith("/assets/") and href != "/favicon.svg":
            if href not in PLANNED:
                fail(f"{slug}: href outside planned routes: {href}")
    for href in sorted(set(re.findall(r'href="([^"]+)"', main_html))):
        if href == slug:
            note(f"{slug}: self-link in <main>: {href} (paste-annotated, kept verbatim)")
    print(f"  H1/title/meta/canonical/schema OK; FAQ {faq_n}")


def main():
    # ---- homepage (recompute want from the paste, same formula as its parser)
    raw = open(os.path.join(BASE, "homepage-paste-2026-11-19.md")).read()
    seo_part, copy = raw.split("FINAL: Homepage page copy", 1)
    copy = copy.strip()
    m = re.search(r"Meta title \(60 chars\)\n([^\n]+)", seo_part)
    title = m.group(1).strip()
    m = re.search(r"Meta description \(150 chars\)\n([^\n]+)", seo_part)
    meta = m.group(1).strip()
    m = re.search(r"\nH1\n([^\n]+)", seo_part)
    h1 = m.group(1).strip()
    m = re.search(r"Schema \(JSON-LD\)\n(\{.*?\n\})", seo_part, re.S)
    schema = json.loads(m.group(1))
    want = words(re.sub(r"\((/[a-z0-9\-/]+)\)", "", copy))
    print(f"homepage: title {len(title)}ch, meta {len(meta)}ch, copy words {len(want)}")
    # homepage blocks: re-run the parser module logic by importing its data file
    # (blocks live in site/data/homepage.php — parse the PHP return value via
    # the parser's own emission: simplest is to re-run parse_homepage main in
    # a subprocess, then read blocks back through a tiny PHP dump.)
    import subprocess
    r = subprocess.run(["python3", os.path.join(BASE, "tools/parse_homepage.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:])
        print(r.stderr[-2000:])
        raise SystemExit("homepage parser failed")
    m = re.search(r"FAQ pairs: (\d+)", r.stdout)
    faq_n = int(m.group(1)) if m else -1
    # dump homepage.php blocks to JSON via php
    php_dump = ("<?php $d = require 'site/data/homepage.php'; "
                "echo json_encode($d['blocks']);")
    open("/tmp/hp_dump.php", "w").write(php_dump)
    r = subprocess.run(["php", "/tmp/hp_dump.php"], capture_output=True, text=True,
                       cwd=BASE)
    blocks = json.loads(r.stdout)
    # convert segment dicts to the parser's shape (they already are)
    check_page("/", title, meta, h1, schema, blocks, want, faq_n)

    # ---- inner pages (parser re-verifies word-diff 0 + re-emits data files)
    for spec in pp.SPECS:
        p = pp.Parser(spec)
        p.run()
        want = words(re.sub(r"\((/[a-z0-9\-/]+)\)", "", p.copy))
        check_page("/" + spec["slug"] + "/", p.title, p.meta, p.h1, p.schema,
                   p.blocks, want, spec["faq"][1])

    # ---- legal pages (noindex, out of sitemap, NO JSON-LD)
    import parse_legal as pl
    for spec in pl.SPECS:
        p = pl.LegalParser(spec)
        p.run()
        visible = re.sub(r"^H2: ", "", p.copy, flags=re.M)
        visible = re.sub(r"\((/[a-z0-9\-/]+)\)", "", visible)
        want = words(p.h1) + words(visible)
        extra = words("Last updated " + spec["last_updated"]) if spec.get("last_updated") else []
        check_page("/" + spec["slug"] + "/", p.title, p.meta, p.h1, None,
                   p.blocks, want, 0, extra_words=extra)

    # ---- sitemap / redirects / statics
    print("== site files ==")
    sm = open(os.path.join(OUT, "sitemap.xml")).read()
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    print(f"  sitemap locs: {len(locs)}")
    if len(locs) != 31:
        fail(f"sitemap locs {len(locs)} != 31")
    if "image:" in sm or "changefreq" in sm or "priority" in sm:
        fail("sitemap has image/changefreq/priority entries")
    if sm.count("<lastmod>2026-11-19</lastmod>") != 31:
        fail("sitemap lastmod != 31x 2026-11-19")
    for leg in ["/privacy-policy/", "/terms/", "/disclaimer/"]:
        if leg in sm:
            fail(f"legal page in sitemap: {leg}")
    redir = open(os.path.join(OUT, "_redirects")).read().strip().splitlines()
    print(f"  _redirects lines: {len(redir)}")
    if len(redir) != 33:
        fail(f"_redirects lines {len(redir)} != 33 (30 content + 3 legal)")
    for f in ["robots.txt", "llms.txt", "favicon.svg",
              "5aacacd72541e41a25cbc83799292d44.txt"]:
        if not os.path.isfile(os.path.join(OUT, f)):
            fail(f"missing static: {f}")
    doc404 = open(os.path.join(OUT, "404.html")).read()
    if "Page Not Found" not in doc404:
        fail("404.html missing H1")
    if 'rel="canonical"' in doc404:
        fail("404.html has a canonical")
    llms = open(os.path.join(OUT, "llms.txt")).read()
    if llms.count("- [") != 31:
        fail(f"llms.txt entries {llms.count('- [')} != 31")
    for leg in ["/privacy-policy/", "/terms/", "/disclaimer/"]:
        if leg in llms:
            fail(f"legal page in llms.txt: {leg}")

    print()
    print(f"FAILURES: {len(FAILURES)}")
    for f in FAILURES:
        print(" -", f)
    print(f"NOTES: {len(NOTES)}")
    for n in NOTES:
        print(" -", n)
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
