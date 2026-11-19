# FINDINGS — Fort Myers NEW PHP site, FIX ROUND
## `~/workspace/fort-myers-php/` — 2026-11-19 (orders 14:30–14:31 PKT)

## 1. Orders (his words)
- Schema: ZERO errors, 4000000% — the old site's GSC error "Missing field
  'item' (in 'itemListElement')" must never appear; no room for blunder/defect.
- Google Map: heavy + pin, further 10x better.
- Q section: look at it. Header/footer: only important items.
- 10x testing of images, schema, everything A to Z. Then end it.

## 2. Schema audit — BEFORE (what was wrong)
Google's BreadcrumbList rule (Search Central, verified 2026-11-19): every
ListItem needs `position`, `name` and `item`; `item` may be omitted ONLY on
the last item. The old site's GSC error was exactly this.
- **BEFORE, live on the new site:** `/water-removal/` BreadcrumbList item 2
  was `{"@type":"ListItem","position":2,"name":"Services"}` with NO `item`
  (items 1 and 3 had it) — the same defect on all 30 inner pages.
- **BEFORE, homepage:** `HomeAndConstructionBusiness` had NO `address`.
  Google requires `name` + `address` for LocalBusiness — a second
  "Missing field" error of the same class.
- **BEFORE, Articles (cost, insurance, how-it-works):** NO `datePublished`
  (only `dateModified`) — Google requires it for Article.

## 3. Schema fixes — AFTER (all render-time; paste data files untouched)
| # | Fix | Where | Source of the value |
|---|---|---|---|
| 1 | BreadcrumbList drops the item-less middle crumb ("Services"/"Areas") from the JSON-LD only; positions renumbered 1..n | `site/includes/functions.php` `ld_breadcrumb_node()` | No URL invented — no /services/ or /areas-group/ route exists. Visible breadcrumb keeps the full trail (Home » Services » H1). |
| 2 | `HomeAndConstructionBusiness` gains `address` | `ld_normalize_given()` | Exactly the About page's PostalAddress from HIS paste: Fort Myers, FL 33901, US. No street address exists; none invented. |
| 3 | Article gains `datePublished` = `dateModified` | `ld_normalize_given()` | The paste's own dateModified (2026-11-19, first publication of this content on this site). |

Validation method: `qa/validate_schema.py` (new, committed) — parses all 92
JSON-LD scripts on all 34 pages and checks per-type Google requirements
(BreadcrumbList ≥2 items, sequential positions, every item has a real-route
`item`; LocalBusiness name+address; FAQPage Q/A + visible count; Service
name+provider; Article headline/author/datePublished/dateModified; HowTo
steps; ContactPage/AboutPage mainEntity; WebSite; legal pages 0 scripts).
Result: **ERRORS 0, WARNINGS 0** (34 pages, 92 scripts/nodes).
By-design NOTES (6, not fixable without inventing data): the 3 Articles have
no `image` (heroes honestly empty) and no publisher `logo` (only the SVG
favicon brand mark exists; no raster logo file).

## 4. Google Map — heavy + pin
- Embed URL (the ONLY maps URL in out/): 
  `https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed`
  — city-level pin on Fort Myers (city + ZIP only). NO street address
  anywhere (numbered-street regex 0 hits; only city+ZIP forms).
- Map-section iframe (home + contact only): 1240×560, gold 2px border,
  shadow. Footer map: 100% × 280, light border. Both previously had an
  inline `style="border:0"` that killed the CSS border — removed from both.
- Footer map ABSENT on all 7 location pages (0 iframes each), present on
  the other 27 pages.
- Map tiles are blank in VM Chromium screenshots (VM cannot reach
  google.com/maps) — markup, borders and pin URL verified; live tiles still
  need one real-browser look (standing open item).

## 5. Q section — 10x restyle (CSS only, no visible words changed)
FAQ accordions: circular coral `+`/`−` badge, sand hover, 3px gold
focus-visible ring, open state = teal border + 5px gold left accent +
shadow, answer divider line, `scroll-margin-top` for #faq. Viewed in
screenshots (home + contact full-page): clean, badge aligned, no overlap.
Caveat: `<details>` ship closed, so the OPEN state was verified in CSS
only, not in a screenshot. FAQ visible==schema on all 31 FAQ pages
(308 total); legal 3 have 0/0.

## 6. Header / footer — only important
REMOVED (3 redundant home-links, each duplicated the brand link):
- "Fort Myers" → `/` from the header Areas dropdown (8 → 7)
- "Fort Myers" → `/` from the footer Areas column (8 → 7)
- "Home" → `/` from footer Explore (10 → 9)
KEPT: header Services 12, Cost, Areas 7, Contact + call button (desktop +
mobile nav); footer Services 12, Explore 9 (How It Works, About Us, Cost,
Insurance Claims, First-Hour Checklist, Contact, Privacy, Terms,
Disclaimer), Areas 7 + ZIPs line, brand + call + map. A "Home" → `/` link
still exists in the mobile-menu panel only (correct nav behaviour).

## 7. 10x testing — two passes
**Pass 1 (own):** verify_export FAILURES 0 / NOTES 0; validate_schema
ERRORS 0 / WARNINGS 0; render_check 34/34 overflow 0 at 320/360/390/1440,
20px measured; links 0 broken, 0 self-links in `<main>` (Pass 2 count:
3,817 hrefs); images 0 `<img>` in out/ (heroes honestly empty);
sitemap 31 locs, robots 15 AI crawlers + Bytespider disallowed, llms 31
entries; speed lab (Lighthouse 13.6.0): desktop home Perf 100 / SI 0.9s /
LCP 0.6s / CLS 0; mobile home Perf 78–90 across two runs (SI 2.1–2.6s,
CLS 0); HIW mobile Perf 81 / SI 2.4s. Map footer-box proven in layout
(333×280, border 2px) via Playwright probe after catching the inline
`border:0` defect by viewed pixels.
**Pass 2 run 1 (independent): NOT READY — 1 defect (D-1, P3).** En dash
rendered in the footer on all 34 pages: `33901&ndash;33967` hardcoded in
`footer.php:30`; the old dash check only looked for literal characters.
Fix: `33901 to 33967` (footer chrome only) + hardened the verify script's
dash check to also flag `&ndash;`/`&mdash;`/`&#8212;`/`&#8211;`.
**Pass 1 re-verify after fix:** verify_export 0/0, validate_schema 0/0,
dash sweep (literal + entities) 0 files, render_check rerun 34/34 clean.
**Pass 2 run 2 (independent re-check): READY — ZERO DEFECTS.** Fix
verified in source, in all 68 rendered files, and visually in the footer
screenshot; hardened regex tested live (catches all 4 old entities);
regression sweep clean (images 0, sitemap 31, footer map 0 on 7 location
pages, pin URL the only maps URL, header/footer trim intact).

## 8. Deploy — LIVE 2026-11-19
- Repo `GrowthAura/fort-myers-water-damage-php` (public). `main` = PHP
  source; `cloudflare-pages` b5547b9 = static export + workflow.
- Push via transient askpass (token never stored/quoted; askpass deleted
  after use; remote clean https; no credential.helper). Commit author
  GrowthAura <noorullahchhachher2@gmail.com>.
- GitHub Actions run 44500552402 (cloudflare-pages) completed success —
  auto-deploy proven again.
- LIVE https://fort-myers-water-damage-php.pages.dev — parent-coordinator
  verified by curl: home 200 (title exact, footer "33901 to 33967",
  pin URL), live home HTML byte-identical to local out/index.html (md5
  8c2dce9d); /water-removal/ + /cape-coral/ BreadcrumbList live: 2 items,
  BOTH with `item`; sitemap 200 (31 locs), robots 200, llms 200,
  /how-it-works/ 200, bogus 404; home LocalBusiness address live.
- NO domain attach. Old repo + live Next.js site untouched (his call later).

## 9. Still his call / open
- Old domain connect + old repo delete: later, on his word.
- Live map tiles: one real-browser look.
- Live Speed Index: not measurable from this VM (Chromium tunnel fail +
  PageSpeed 429 earlier); lab numbers above are the measured evidence.
- Old-site open items unchanged: Batch-3 push (Next.js, READY at dbdbd98)
  still blocked on his word + token; Seabees photo still live there.
