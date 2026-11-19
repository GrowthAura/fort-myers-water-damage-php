#!/usr/bin/env python3
"""Schema validator — Fort Myers NEW PHP site (fix round, 2026-11-19).

Validates EVERY JSON-LD script in out/ against Google's rich-results
requirements (grounded 2026-11-19 from Google Search Central docs via
third-party summaries of those docs):

- BreadcrumbList: itemListElement >= 2 ListItems; positions sequential ints
  from 1; EVERY ListItem needs `name` + `item` (URL string). `item` may be
  omitted ONLY on the last item — a MIDDLE item without `item` is the GSC
  error "Missing field 'item' (in 'itemListElement')" (old site's error).
  Our build drops item-less middle crumbs from the schema, so every item
  must carry `item`. Each `item` URL must be a real route on this site.
- LocalBusiness (incl. HomeAndConstructionBusiness): Google requires
  `name` + `address` (PostalAddress). Recommended: telephone, url, hours.
- FAQPage: mainEntity non-empty; each Question needs `name` +
  acceptedAnswer.text; count must equal the visible <details> count.
- Service: `name` required; provider.name required.
- Article: headline, author.name, datePublished, dateModified required.
  `image` is required for the Article rich result but is a BY-DESIGN NOTE
  here (heroes are honestly empty — no photo passes licence+place+subject).
  publisher.logo is a NOTE for the same reason (only the SVG favicon mark
  exists; no raster brand logo).
- HowTo: name, totalTime, step[] each with name or text.
- ContactPage / AboutPage: name, url, mainEntity.name (+ address,
  contactPoint on ContactPage).
- WebSite: name, url.
- Global: every script parses as JSON; @context is schema.org; no
  duplicate @id per page; legal pages carry ZERO JSON-LD.

Levels: ERROR (Google-required, must be 0), WARNING (fixable gap),
NOTE (by design — fixing it would require inventing data, which is
forbidden; each note carries its reason).
Usage: python3 qa/validate_schema.py [outdir]
Exit 1 if ERRORS > 0 or WARNINGS > 0.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BUILD, "out")
SITE_URL = "https://fortmyerswaterdamagerestoration.us"
LEGAL = {"/privacy-policy/", "/terms/", "/disclaimer/"}

errors, warnings, notes = [], [], []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


def note(page, msg):
    notes.append(f"{page}: {msg}")


def is_url(v):
    return isinstance(v, str) and v.startswith(SITE_URL + "/") or v == SITE_URL + "/"


# --- routes: sitemap locs + legal pages ------------------------------------
sitemap = os.path.join(OUT, "sitemap.xml")
tree = ET.parse(sitemap)
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
routes = set()
for loc in tree.getroot().findall("s:url/s:loc", ns):
    routes.add(loc.text.replace(SITE_URL, ""))
routes |= LEGAL
routes.add("/")


class DetailsCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.faq = 0

    def handle_starttag(self, tag, attrs):
        if tag == "details":
            d = dict(attrs)
            if "faq-item" in d.get("class", ""):
                self.faq += 1


def postal_ok(addr):
    if not isinstance(addr, dict) or addr.get("@type") != "PostalAddress":
        return False
    return all(addr.get(k) for k in
                ("addressLocality", "addressRegion", "postalCode", "addressCountry"))


def check_breadcrumb(page, node):
    items = node.get("itemListElement")
    if not isinstance(items, list) or len(items) < 2:
        err(page, "BreadcrumbList: itemListElement must have >= 2 ListItems")
        return
    for i, it in enumerate(items):
        if not isinstance(it, dict) or it.get("@type") != "ListItem":
            err(page, f"BreadcrumbList item {i}: not a ListItem")
            continue
        if it.get("position") != i + 1:
            err(page, f"BreadcrumbList item {i}: position {it.get('position')} != {i + 1}")
        if not it.get("name"):
            err(page, f"BreadcrumbList item {i}: missing 'name'")
        # THE GSC RULE: every ListItem needs `item` except (optionally) the
        # last. Our build carries `item` on ALL items, so any miss is an error.
        item = it.get("item")
        if not item:
            err(page, f"BreadcrumbList item {i} ({it.get('name')!r}): missing 'item' "
                      f"— GSC 'Missing field item (in itemListElement)'")
        elif isinstance(item, str):
            if not item.startswith(SITE_URL):
                err(page, f"BreadcrumbList item {i}: 'item' URL not on this site: {item}")
            else:
                path = item.replace(SITE_URL, "") or "/"
                if path not in routes:
                    err(page, f"BreadcrumbList item {i}: 'item' URL is not a real route: {item}")
        elif isinstance(item, dict):
            if not item.get("@id"):
                err(page, f"BreadcrumbList item {i}: 'item' object has no @id")


def check_faq(page, node, visible_count):
    ents = node.get("mainEntity")
    if not isinstance(ents, list) or not ents:
        err(page, "FAQPage: mainEntity empty")
        return
    if len(ents) != visible_count:
        err(page, f"FAQPage: schema has {len(ents)} questions but page shows "
                  f"{visible_count} visible FAQs")
    for j, q in enumerate(ents):
        if not isinstance(q, dict) or q.get("@type") != "Question":
            err(page, f"FAQPage Q{j}: not a Question")
            continue
        if not q.get("name"):
            err(page, f"FAQPage Q{j}: missing 'name'")
        ans = q.get("acceptedAnswer")
        if not isinstance(ans, dict) or not ans.get("text"):
            err(page, f"FAQPage Q{j} ({str(q.get('name'))[:40]!r}): missing acceptedAnswer.text")


def check_localbiz(page, node):
    if not node.get("name"):
        err(page, f"{node.get('@type')}: missing 'name'")
    if not node.get("url"):
        err(page, f"{node.get('@type')}: missing 'url'")
    if not node.get("telephone"):
        warn(page, f"{node.get('@type')}: missing 'telephone' (recommended)")
    if not postal_ok(node.get("address")):
        err(page, f"{node.get('@type')}: missing/incomplete 'address' "
                  f"(Google requires name + address for LocalBusiness)")


def check_article(page, node):
    for f in ("headline", "datePublished", "dateModified"):
        if not node.get(f):
            err(page, f"Article: missing '{f}' (Google-required)")
    auth = node.get("author")
    if not isinstance(auth, dict) or not auth.get("name"):
        err(page, "Article: missing author.name")
    pub = node.get("publisher")
    if not isinstance(pub, dict) or not pub.get("name"):
        err(page, "Article: missing publisher.name")
    elif not pub.get("logo"):
        note(page, "Article: publisher has no logo (by design — only the SVG "
                   "favicon brand mark exists; no raster logo file)")
    if not node.get("image"):
        note(page, "Article: no 'image' (by design — heroes honestly empty; "
                   "no photo passes licence+place+subject)")


def check_node(page, node, visible_faq):
    t = node.get("@type")
    if t == "BreadcrumbList":
        check_breadcrumb(page, node)
    elif t == "FAQPage":
        check_faq(page, node, visible_faq)
    elif t in ("HomeAndConstructionBusiness", "LocalBusiness"):
        check_localbiz(page, node)
    elif t == "Service":
        if not node.get("name"):
            err(page, "Service: missing 'name'")
        prov = node.get("provider")
        if not isinstance(prov, dict) or not prov.get("name"):
            err(page, "Service: missing provider.name")
    elif t == "Article":
        check_article(page, node)
    elif t == "HowTo":
        if not node.get("name"):
            err(page, "HowTo: missing 'name'")
        if not node.get("totalTime"):
            err(page, "HowTo: missing 'totalTime'")
        steps = node.get("step")
        if not isinstance(steps, list) or not steps:
            err(page, "HowTo: empty 'step'")
        else:
            for j, st in enumerate(steps):
                if not isinstance(st, dict) or not (st.get("name") or st.get("text")):
                    err(page, f"HowTo step {j}: missing name and text")
    elif t in ("ContactPage", "AboutPage"):
        if not node.get("name"):
            err(page, f"{t}: missing 'name'")
        if not node.get("url"):
            err(page, f"{t}: missing 'url'")
        me = node.get("mainEntity")
        if not isinstance(me, dict) or not me.get("name"):
            err(page, f"{t}: missing mainEntity.name")
        elif not postal_ok(me.get("address")):
            err(page, f"{t}: mainEntity missing/incomplete 'address'")
        if t == "ContactPage" and not me.get("contactPoint"):
            err(page, "ContactPage: mainEntity missing 'contactPoint'")
    elif t == "WebSite":
        if not node.get("name"):
            err(page, "WebSite: missing 'name'")
        if not node.get("url"):
            err(page, "WebSite: missing 'url'")


def page_file(route):
    if route == "/":
        return os.path.join(OUT, "index.html")
    return os.path.join(OUT, route.strip("/"), "index.html")


def main():
    pages = sorted(routes)
    total_scripts = 0
    total_nodes = 0
    for route in pages:
        f = page_file(route)
        if not os.path.exists(f):
            err(route, f"export file missing: {f}")
            continue
        html = open(f, encoding="utf-8").read()
        scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                             html, re.S)
        counter = DetailsCounter()
        counter.feed(html)
        if route in LEGAL and scripts:
            err(route, f"legal page carries {len(scripts)} JSON-LD script(s), must be 0")
        if route not in LEGAL and not scripts:
            err(route, "no JSON-LD scripts at all")
        seen_ids = set()
        for s in scripts:
            total_scripts += 1
            try:
                d = json.loads(s)
            except Exception as e:
                err(route, f"JSON-LD parse failure: {e}")
                continue
            if d.get("@context") != "https://schema.org":
                err(route, "JSON-LD @context is not https://schema.org")
            nodes = d.get("@graph", [d])
            for n in nodes:
                total_nodes += 1
                if not isinstance(n, dict) or "@type" not in n:
                    err(route, "JSON-LD node without @type")
                    continue
                if n.get("@id"):
                    if n["@id"] in seen_ids:
                        err(route, f"duplicate @id on page: {n['@id']}")
                    seen_ids.add(n["@id"])
                check_node(route, n, counter.faq)
    print(f"pages checked: {len(pages)} | JSON-LD scripts: {total_scripts} | "
          f"nodes: {total_nodes}")
    print(f"ERRORS: {len(errors)}")
    for e in errors:
        print("  ERROR:", e)
    print(f"WARNINGS: {len(warnings)}")
    for w in warnings:
        print("  WARN:", w)
    print(f"NOTES (by design): {len(notes)}")
    for n in notes:
        print("  NOTE:", n)
    return 1 if (errors or warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
