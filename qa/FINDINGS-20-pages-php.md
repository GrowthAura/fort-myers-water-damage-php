# Findings — Fort Myers NEW PHP site, 20 pages (2026-11-19)

Build: `~/workspace/fort-myers-php/`, LOCAL ONLY. Live Next.js site untouched.
Export: `out/` (49 files: 20 × `index.html` + 19 flat `<path>.html` + `404.html`
+ sitemap/robots/llms/favicon/IndexNow key + `_redirects` + `_headers` + assets).
Verified with `qa/verify_export.py` (content) + `qa/render_check.py` (render).

## Theme
"Caloosahatchee" (coordinator's choice): deep river teal #0A2E38, sunset coral CTA
#C2410C, sand #F6F1E7, gold #C99B3F. Display "Archivo Black" + body "Inter"
(Google Fonts, display=swap, system fallbacks). Body 20px/1.7, container 1240px
(wide lines), H1 58px desktop / 40px mobile, H2 42/31, H3 26/23. Sticky dark
header, hero with dark teal gradient scrim (no photo — honestly empty, see
Images), details card (sand, coral left border), kind cards (3-col, coral top
border), styled tables (teal header row, zebra), numbered steps (coral circles),
FAQ as native `<details>` accordions, Google Maps service-area embed
(q=Fort Myers, FL&z=11&output=embed, no key, no fake address/pin), footer with
map (ABSENT on the 7 location pages per standing rule), mobile call bar ≤620px
only, tap targets ≥44px mobile. Responsive overrides AFTER base rules.

## Pages built — 20/33 routes (+ /about/ pending)
| Page | Copy words | FAQ | Links | Schema |
|---|---|---|---|---|
| / (homepage, FINAL paste) | 5,402 | 14 | 56 | HomeAndConstructionBusiness |
| /water-removal/ | 3,418 | 14 | 32 | Service |
| /drying/ | 2,744 | 13 | 27 | Service |
| /sewage-cleanup/ | 2,563 | 13 | 21 | Service |
| /ac-leak/ | 2,855 | 11 | 20 | Service |
| /ceiling-leak/ | 2,598 | 11 | 22 | Service |
| /condo-leak/ | 2,367 | 10 | 22 | Service |
| /cast-iron-pipe/ | 2,478 | 11 | 17 | Service |
| /vacant-home/ | 2,349 | 9 | 21 | Service |
| /first-hour-checklist/ | 2,377 | 10 | 30 | HowTo (PT1H, 5 steps) |
| /cost/ | 3,751 | 12 | 24 | Article (2026-11-19) |
| /insurance/ | 3,342 | 12 | 21 | Article (2026-11-19) |
| /burst-pipe/ | 2,321 | 10 | 26 | Service, NO description field |
| /mobile-home/ | 2,093 | 10 | 21 | Service, NO description field |
| /slab-leak/ | 2,117 | 10 | 19 | Service, NO description field |
| /flood-cleanup/ | 2,409 | 11 | 21 | Service, NO description field |
| /cape-coral/ | 2,022 | 10 | 25 | Service, NO description field; areaServed = City OBJECT + 6 ZIPs |
| /lehigh-acres/ | 1,823 | 10 | 25 | Service, NO description field; areaServed = Place OBJECT + 6 ZIPs |
| /areas/ | 1,615 | 9 | 18 | Service, NO description field; areaServed = ARRAY of 11 objects |
| /water-heater-leak/ | 2,026 | 10 | 18 | Service, NO description field |
| **Total** | **52,271** | **220** | **486** | |

All schemas emitted exactly as pasted (burst-pipe / mobile-home / slab-leak /
flood-cleanup / cape-coral / lehigh-acres / areas / water-heater-leak have NO
`description` field — none added). Cape Coral areaServed is a single City
object, Lehigh Acres a single Place object, Areas an array of 11 objects —
all preserved verbatim. FAQPage script is built from the visible FAQs (the
pastes give no FAQPage node); BreadcrumbList on inner pages
(service → Home » Services » H1; area → Home » Areas » H1; guide → Home » H1;
middle items name-only, no URL invented).

## Verification — all green (final run, after the 3 fixes below)
- Export: 20/20 sitemap locs 200, 404 → 404.html, statics + assets copied.
- `verify_export.py`: **FAILURES 0, NOTES 0**. Per page: H1 count = 1 and
  byte-match; title/meta byte-match; given schema JSON parses and equals the
  paste schema exactly (dict equality, incl. areaServed shapes); FAQPage
  mainEntity count == visible FAQ count with Q/A byte-match; BreadcrumbList
  names == visible breadcrumb; `<main>` ordered word-diff 0 vs paste copy
  (plus known chrome: hero CTA button + breadcrumb); every (/slug/) link
  renders as `<a href>` with the same anchor text; all internal hrefs are
  planned routes (33 + /about/) or static assets; 0 em/en dashes in any
  rendered HTML; no self-links in any `<main>` (homepage paste has zero `(/)`
  annotations); sitemap 20 locs, all lastmod 2026-11-19, no image/changefreq/
  priority entries; `_redirects` 19 no-slash→slash 308 lines; llms.txt 20
  entries; 404.html has no canonical and no og:url.
- PHP server smoke test: 20/20 routes 200; no-slash → 308; `//` → 308;
  unknown + pending routes → branded 404.
- `render_check.py`: **overflow 0 at 320 / 360 / 390 / 1440 on all 20 pages**;
  body font-size **20px measured at 390 and 1440 on all 20 pages**.
  Screenshots: 58 in `qa/screenshots/` — desktop 1440×900 + mobile 390×844
  viewport shots for every page, full-page desktop + mobile for home,
  mobile-home, slab-leak, flood-cleanup, cape-coral, lehigh-acres, areas,
  water-heater-leak, plus menu-open shots at 320/390. Viewed: 4 new pages
  desktop + mobile, home mobile, menu-open 390 — all clean.
- `php -l`: all PHP files pass.

## Defects found by verification this round — all fixed + re-verified
1. **Breadcrumb H1 empty (P1, all inner pages).** `page_crumbs()` read
   `$page['h1']`, but the H1 lives at `$page['seo']['h1']` — the visible
   breadcrumb and the BreadcrumbList schema both rendered the last crumb as
   empty, and `<main>` word-diff was short by exactly the H1 word count on
   every inner page. Fixed in `site/includes/functions.php:182`. The homepage
   has no breadcrumb, which is why the earlier homepage-only rounds never saw
   it. Re-verified: breadcrumb visible == schema on all 19 inner pages.
2. **404 page carried an empty canonical (P2).** `header.php` rendered
   `<link rel="canonical">` + `og:url` unconditionally; the 404 sets canonical
   null, so 404.html had `href=""`. Both tags are now conditional on a
   non-empty canonical. Re-verified: 404.html has no canonical/og:url.
3. **Mobile horizontal overflow (P1, all pages, 320/360/390).**
   Measured 331/291/316px identical on every page. Two causes, both in shared
   chrome: (a) the closed mobile menu's panel rendered off-viewport — the
   author's `.mobile-menu-panel { display: flex }` beats the UA's
   closed-`<details>` hiding, so the closed panel (positioned at the header's
   right edge) extended the scroll width; (b) the brand forced a ~360px
   single-line name, pushing the call button + menu button off-viewport.
   Fixed in `site/assets/css/styles.css` (820px block):
   `.mobile-menu:not([open]) .mobile-menu-panel { display: none; }`,
   `.brand { flex: 1 1 auto; min-width: 0; }` (brand wraps to 2–3 lines);
   (620px block) `.header-call { display: none; }` — the sticky bottom call
   bar already serves ≤620px. Re-verified: overflow 0 at all 4 widths on all
   20 pages, closed and open. Open menu probe: panel spans the full viewport
   (left 0, right = viewport width), overflow 0 while open and after closing,
   at 320 and 390.

## Parser notes (for the next pages)
- `tools/parse_page.py` (generic walker + per-page SPECS) + `tools/parse_homepage.py`.
  All 19 inner pages WORD-DIFF 0; homepage WORD-DIFF 0.
- New this round: `intro_tables` spec (areas: ZIP-codes table before the first
  H2); `related: None` (areas has NO Related section); count-driven FAQ loop
  (handles a link-line para between FAQ and the next heading — areas "Who we
  are and how a job runs: ..."); anchor boundary "also " added (areas "See
  also mobile home water damage" → anchor "mobile home water damage", was
  "also mobile home water damage"). Homepage re-parse after the boundary
  change is byte-identical (md5 225b63366fb254ba8e27339fc21cfeb5).
- Verifier `qa/verify_export.py` re-parses every paste and re-checks the
  export end to end; `qa/render_check.py` measures overflow + font + shots.

## Images — none installed (honest empty)
- Every hero slot renders the `hero-no-media` gradient (no `<img>` anywhere).
  Image worker findings: `qa/hero-findings.md` — no free-stock photo passes
  licence + place + subject for the homepage hero (Wikimedia CBP aerial is
  place-unverifiable; Pexels Ian series is Sanford, FL; Pexels 14216445 is
  LIVE on Plano 3; the genuine Fort Myers wreckage photo matches the banned
  hero description and shows no water). Recommendation stands: leave slots
  empty until a real Fort Myers job photo, licensed stock with a verifiable
  Fort Myers caption, or the user's explicit call. `site/assets/img/` is
  empty by design. `site/data/media-manifest.php` is empty.
- Known carry-overs (chrome, not content, flagged for the record):
  "Describe your water problem" → /contact/ (inference from the published
  site; the paste gives no target); msc.fema.gov rendered as a link to
  https://msc.fema.gov (URL written in the paste); phone numbers auto-linked
  tel: (chrome). Homepage FAQ "Do you handle condos..." anchor 'townhomes'
  → /condo-leak/ (last-boundary rule) — as parsed, kept.

## Pending pages — 13 routes + /about/
Not yet sent: appliance-leak, floors, cabinets, commercial, north-fort-myers,
fort-myers-beach, estero, bonita-springs, how-it-works, contact,
privacy-policy, terms, disclaimer. /about/ linked from the homepage and from
the areas FAQ tail line ("About us (/about/)") — page NOT sent, link kept,
content NOT invented. Pending routes linked from built copy (10):
appliance-leak, bonita-springs, cabinets, commercial, estero, floors,
fort-myers-beach, how-it-works, north-fort-myers, /about/. Footer/header also
link contact + legal pages (chrome). All pending routes 404 with the branded
template until their pages arrive.

## Open flags (need the user / a real browser)
- Live map tiles need one real-browser look (VM Chromium can't reach
  google.com/maps; the service-area embed is present, no fake address/pin).
- Deploy target (same domain vs new domain) is HIS call later. Local only:
  no push/deploy/domain/DNS, no git remote.
- Hero slots honestly empty on all 20 pages (see Images).
- The old site's Seabees photo does not exist in this build (no images at all).
