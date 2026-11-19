# 20X Audit — Worker C: RENDERING (desktop 1440 + mobile 390 + 320)

**Project:** `~/workspace/fort-myers-php/` — five-fix build (22:05 push, main `8cf8cb7`)
**Live base:** https://fort-myers-water-damage-php.pages.dev (byte-identical to local `out/`)
**Audit date:** 2026-11-19 ~23:00 PKT · **Scope:** all 34 pages, widths 320 / 390 / 1440
**Method:** read-only. Local serve of `out/` on `http://127.0.0.1:8931` (Chromium on this VM cannot
reach pages.dev — `ERR_TUNNEL_CONNECTION_FAILED` — so no live visual check is claimed; the served
bytes are the same as live). Playwright bundled Chromium (no `executable_path`), `TMPDIR` pointed
at `qa/tmp-chrome/` (`/tmp` was 68% full at start; a VM replacement mid-audit wiped `/tmp` to 0%
and killed the server — server restarted on 8931, all data survived). Homepage is ~22,251px tall
at 1440 / ~34,892px at 390, so it was captured in viewport slices, never as one full-page shot.

**Evidence files:** `qa/20x-c-data.json` (overflow/fonts/contrast/taps/hero/kinds/details/five-fix/footer/
call-bar/skip/clipped), `qa/20x-c-data2.json` (alpha-composited contrast, prose-only fonts, skip-link
functional test, footer Services incl. spans), `qa/20x-c-data3.json` (hero/final CTA button heights,
first-table widths), `qa/20x-c-tables.json` (all 81 tables, in-view measurement).
Probes: `qa/20x-c-measure.py`, `qa/20x-c-measure2.py`, `qa/20x-c-shots.py` (all read-only).
Screenshots: `qa/screenshots-20x-testing/c/` (263 files — hero per page @1440+390, montages,
kinds grids, details cards, footers, mobile menu, tables, full-page @390, home slices).

**Measurement notes**
- Contrast is WCAG ratio computed from rendered styles with **alpha compositing** (a first pass
  returned false 1.0/2.55 readings on translucent `.btn-ghost-dark` / `.btn-ghost` backgrounds —
  those were artefacts, corrected; the corrected pass finds **zero** solid-bg elements below 4.5:1).
  Text over photos (all heroes, 13 kinds photo-cards) is excluded from the numeric pass and judged
  by viewed pixels instead.
- "Min font" in the table is **prose-only**: `.page-body p/li`, `td`, `dd` (eyebrow `.details-sub`
  and breadcrumb `»` glyph excluded — they are listed separately under C-05).
- `content-visibility:auto` on `.table-wrap` makes `scrollWidth` report the viewport width while
  the table is off-screen; table widths below were therefore measured **after scrollIntoView**.
  Any off-screen table measurement reporting "fits" is a false negative.
- Tap targets: inline links inside paragraphs are excluded (WCAG 2.5.8 inline exception); every
  other link/button/summary was measured.

## (a) Per-page render table

Overflow is `documentElement.scrollWidth − innerWidth` (0 = none). Min font = smallest prose
font-size. Worst contrast = worst solid-background WCAG ratio @390. Min tap = smallest
non-inline interactive target (w×h, smaller side).

| Page | Overflow 320 / 390 / 1440 | Min prose font 390 / 1440 | Worst contrast @390 | Min tap target 390 / 1440 |
|---|---|---|---|---|
| / (home) | 0 / 0 / 0 | 18px / 19px (td) | 5.18 (skip-link, white on coral) | 44px / 44px (footer link) |
| /water-removal/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 (breadcrumb `»`) | 44px / 44px |
| /drying/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /sewage-cleanup/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /ac-leak/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /ceiling-leak/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /condo-leak/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /cast-iron-pipe/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /vacant-home/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /first-hour-checklist/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /cost/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /insurance/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /burst-pipe/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /mobile-home/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /slab-leak/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /flood-cleanup/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /cape-coral/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /lehigh-acres/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /areas/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /water-heater-leak/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /appliance-leak/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /floors/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /cabinets/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /commercial/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /north-fort-myers/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /fort-myers-beach/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /estero/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /bonita-springs/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /how-it-works/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /contact/ | 0 / 0 / 0 | 18px / 19px (td) | 4.90 | 44px / 44px |
| /about/ | 0 / 0 / 0 | **20px / 20px** | 4.90 | 44px / 44px |
| /privacy-policy/ | 0 / 0 / 0 | **20px / 20px** | 4.90 | 44px / 44px |
| /terms/ | 0 / 0 / 0 | **20px / 20px** | 4.90 | 44px / 44px |
| /disclaimer/ | 0 / 0 / 0 | **20px / 20px** | 4.90 | 44px / 44px |

Worst-contrast detail (all ≥ 4.5:1, @390 and @1440 identical): H2 deep `#0A2E38` on sand
**12.77** · H3 teal `#0B5563` on white **8.42** · body `p` muted `#46585f` on white **7.44** ·
body links teal **8.42** · skip-link white on coral **5.18** · footer gold `#C99B3F` on deep **5.64** ·
breadcrumb separator `#8A6D1F` on white **4.90** (sitewide worst). H1 is white on the hero
photo/scrim on all 34 pages — judged visually (see below), not numerically.

## Five-fix regression — VERIFIED HOLDS (22:05 push)

| Fix | Result |
|---|---|
| Kinds scrim strong + white text | PASS — scrim `linear-gradient(rgba(7,38,47,0.92), 0.88, 0.86)` on all 13 photo cards; H3 `#fff` 23px/22px, body `#F4F8F8` 20px; all 13 viewed readable @1440 + @390 (`kindsgrid1-home-1440-*.png`, `kindsgrid1-home-390-*.png`) |
| Header Areas dropdown: "Areas" FIRST then 6 areas, no "See all areas" / "All Service Areas" | PASS — 34/34 pages: `[Areas, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero, Bonita Springs]`; 0 hits for either removed string sitewide. Mobile menu likewise flat list with group label AREAS → Areas first (`mobile-menu-home-390.png`) |
| Footer Services = EXACTLY the header's 7 services | PASS — 34/34 pages show all 7; on the 7 service pages the current service is a non-link `span.nav-current` (no-self-link rule), the other 6 are links. Not a defect. |
| NO Areas column in footer | PASS — footer navs are only `Services` + `Explore` on 34/34 pages; 0 area links in footer |
| H2 deep `#0A2E38`, H3 teal `#0B5563` + 44px gold rule under every H3 | PASS with one scoped exception (see C-06): 211/224 main H3s are teal with computed `::after` 44px gold; all main H2s are `rgb(10,46,56)`. Visually confirmed: `h3-rule-burst-pipe-1440.png` (teal H3 + gold rule), `kindsgrid1-home-1440-2.png` (deep H2 + gradient rule) |

## (b) Findings

### P2 — C-01: Table cells below the 20px floor on 30/34 pages
- **Pages:** every page with a table (30 pages; only /about/, /privacy-policy/, /terms/, /disclaimer/ are clean at 20px). Worst: /cost/ (`td "Small spill caught early"`, `td "From about $500"`).
- **Widths:** 390 (18px) and 1440 (19px). Paragraphs/li are 20px everywhere — only tables are short.
- **Evidence:** prose-only min font 18px @390 / 19px @1440 on 30 pages (`qa/20x-c-data2.json`, `minProse`); CSS `table{font-size:19px}` and `@media(max-width:620px){table{font-size:18px}}`, `th{font-size:18px}`. Screenshot `qa/screenshots-20x-testing/c/table-ceiling-leak-390-0.png` shows 18px cells.
- **Why P2:** the owner's order is "text stays 20px" (his confirmation). The five-fix round's "body 20px" check measured computed `body` font-size only, so this slipped through. Table cells are body content (prices, diagnostics), not chrome.
- **Fix:** `table{font-size:20px}` at both breakpoints (and `th` 20px). Re-check /cost/ prices still fit at 390 after the bump — the prices table was narrowed to fit at 19px, so it may overflow again at 20px (see C-02).

### P2 — C-02: 8 tables overflow at 390 with a whole column hidden at first view
- **Pages / tables (hidden width @390, in-view measurement):**
  - / (home) table2 — **142px** hidden; 4th column "What usually happens" entirely off-screen
  - /water-removal/ table2 — **138px**; "Read more" column hidden
  - /ceiling-leak/ table0 — **127px**; "Who fixes the source" column hidden
  - /mobile-home/ table2 — **104px**; "Can it be dried?" column hidden
  - /burst-pipe/ table0 — **93px**; "What to watch for" column hidden
  - /cast-iron-pipe/ table2 — **88px**; "Good to know" column hidden
  - /slab-leak/ table1 — **74px**; "When it usually fits" column hidden
  - /cost/ table3 — **45px**; "Effect on the price" column partly hidden
- **Evidence:** `qa/20x-c-tables.json` (all 81 tables, in-view widths); screenshots
  `qa/screenshots-20x-testing/c/table-ceiling-leak-390-0.png` (3rd-column text sliced mid-word,
  4th-column header cut to "IS"), `table-burst-pipe-390-0.png` (4th column entirely off-screen),
  `full-home-390-slice30.png` (home table2, 4th column cut). The wrap scrolls (`overflow-x:auto`
  + inset shadow), so content is reachable by swiping — but at first view the table looks cut.
- **Why P2:** same class as D-V1 in the 20x round (/cost/ prices hidden at 390 → P2, fixed).
  The /cost/ prices table itself now fits at 390 — but these 8 did not get the same treatment.
- **Fix:** same treatment D-V1 got — narrow the 4-column tables at ≤620px (shorter headers,
  tighter cell padding, `th`/`td` 18px→ keep) or convert the widest to stacked rows; re-measure
  **in view** (off-screen `scrollWidth` lies — see Method note).

### P2 — C-03: Hero call button wraps the phone number across two lines at 320px (all 34 pages)
- **Pages:** all 34 (same hero CTA markup). Also the final CTA "Call 239-356-3708, answered 24/7"
  on 31 pages.
- **Width:** 320 only. At 390 the hero button is one line (61px tall).
- **Evidence:** screenshots `qa/screenshots-20x-testing/c/firstvp-home-320.png`,
  `firstvp-burst-pipe-320.png`, `firstvp-cost-320.png` — button reads "Call 239-356- / 3708";
  measured heights `qa/20x-c-data3.json`: hero button **86px @320 vs 61px @390** on 34/34 pages;
  final CTA **115px @320 vs 89px @390** on 31/31 pages (home's shorter CTA: 89px @320 vs 62px @390).
  The fixed bottom call bar still shows the number on one line at 320, so a clean call affordance
  exists — the hero button itself is what looks broken.
- **Fix:** `white-space:nowrap` on `.hero-ctas .btn` and `.cta-line .btn` at ≤380px, or shrink the
  hero CTA to 19px / drop the "Call " prefix at ≤380px so `239-356-3708` fits one line.

### P3 — C-04: 10 more tables overflow 2–28px at 390; 41 tables overflow at 320
- **Pages @390 (marginal):** /north-fort-myers/ table0 28px · /ceiling-leak/ table1 25px ·
  /how-it-works/ table1 19px · /floors/ table0 16px · /bonita-springs/ table0 14px ·
  /cast-iron-pipe/ table0 9px · /insurance/ table0 5px · / (home) table0, /condo-leak/ table2,
  /vacant-home/ table1 2px each. **@320:** 41 tables overflow (worst home table2 212px,
  water-removal table2 208px, ceiling-leak table0 197px).
- **Evidence:** `qa/20x-c-tables.json`.
- **Fix:** fold into the C-02 pass; the 2–9px cases are a sliver of the last cell's padding and
  are visually negligible — the ≥14px ones are worth the same narrowing. At 320, swipe-inside-table
  is the accepted fallback pattern, so this stays P3.

### P3 — C-05: Chrome/label text below 20px (deliberate styles — owner's call whether the floor is literal)
- **Inventory @390 (all pages unless noted):** `.details-sub` eyebrow **14px** mobile / 15px desktop
  on 26 pages (includes full-sentence labels, e.g. /insurance/ "Usually covered by homeowners
  insurance?"); footer column links **18px**; footer-base + back-to-top **17px**; breadcrumb **18px**
  (incl. `»` separator); nav links **17–18px**; brand tagline **14px** (desktop); nav-group labels
  **14px**; `.hero-areas` **18px**; `.map-link` **18px**.
- **Evidence:** `qa/20x-c-data.json` `sub20` inventory (per-page top-25 lists) + CSS.
- **Fix (only if the 20px floor is meant literally for every rendered glyph):** raise these to
  20px / 18px-minimum. If the floor covers prose only, no action — this is a scope question, not
  a rendering break. The `.details-sub` eyebrow is a standard uppercase-kicker treatment and reads
  fine at 14px bold + letter-spacing.

### P3 — C-06: 13 kinds photo-card H3s have no 44px gold rule (white, by CSS design)
- **Page:** / (home) — the 13 `.kind-card.has-photo` H3s (e.g. "AC leaking from the air handler…",
  "Water dripping from the ceiling…"). Measured: color `rgb(255,255,255)`, `::after` width `auto`,
  background `none` — while the other 211 main H3s are teal + 44px gold rule.
- **Evidence:** `qa/20x-c-data.json` `fivefix.h3s` (13× white/auto/none, all home kinds);
  CSS `.page-body h3:not(.kind-card h3)::after`; screenshots `kindsgrid1-home-1440-0.png`,
  `kindsgrid1-home-1440-1.png` (white H3s, no rule — and readable as-is).
- **Fix (only if "every H3" was literal):** add the 44px gold `::after` to `.kind-card.has-photo h3`
  too. If the exclusion is intended (teal text would fail on the photo; the rule is a page-body
  device), no action — owner's call.

### P3 — C-07: Footer is very tall on mobile (1,774px @390)
- **Pages:** all except the 7 area pages (1,472px @390 — area pages have **no footer map iframe**,
  verified: `footer-map` count 0 on /cape-coral/, /areas/ etc. vs 1 elsewhere; that 302px gap is
  the map + margins, not a defect).
- **Evidence:** footer height measurement (`qa/20x-c-data.json`); screenshots
  `qa/screenshots-20x-testing/c/footer-full-home-390.png`, `footer-full-home-320.png` — stacking
  is clean (brand → map → Services 7 → Explore 9 → base), no clipping or ragged edges.
- **Fix (optional, design call):** slim the mobile footer (e.g. 2-column link grid, smaller map
  height) — the "footer 1001%" bar from the five-fix order leaves room, but nothing is broken.

### P3 — C-08: Footer column links sit exactly at the 44px tap-target floor
- **Pages:** all 34. Measured minimum non-inline tap target is **44px** on every page at 390 and
  1440 — the footer links (`18px × 1.45 lh + 18px padding = 44.1px`). Passes, with zero margin.
- **Evidence:** `qa/20x-c-data.json` `taps` (min per zone; `*_below44` empty everywhere).
- **Fix (optional):** raise `.footer-col a` padding to `10px 0` (≈46px) so a future font/padding
  trim cannot push it under 44px.

## What passed clean (verified, not just claimed)

- **Overflow 0** at 320 / 390 / 1440 on all 34 pages (102 measurements, worst-offender scan clean).
- **Contrast ≥ 4.5:1** on every solid-background text element at 390 and 1440 — zero below-threshold
  elements in the corrected pass.
- **Tap targets ≥ 44px** for every non-inline link/button/summary on all pages/widths
  (header CTA, nav, mobile menu, cards, footer, call bar). Inline body links are < 44px tall
  (6–31/page) — WCAG 2.5.8 inline exception, not a finding.
- **Hero text readable on its image on all 34 pages, desktop + mobile** — viewed every hero
  (`montage-hero-1440-0..5.png`, `montage-hero-390b-0..8.png`): white H1 + `#EEF4F5` intro on the
  0.93→0.70 scrim, CTAs visible, no clipping/overlap. All 34 hero images loaded
  (`imgLoaded: true`). Note: cabinets / how-it-works / terms / disclaimer heroes look near-black
  under the scrim, but the source files are bright (mean luminance 135–169) — the scrim is doing
  its job; not a defect.
- **Kinds-grid card text readable on all 13 photo cards, desktop + mobile** — white H3 + `#F4F8F8`
  body + gold links on the strong scrim; the 6 help cards (photo on top, 20px ink text below) are
  also clean. Help-card titles are lead-in text inside the paragraph (no H3) — structure note only.
- **Details-card icons aligned on all 26 cards** — icon exactly 40×40, 0 rows off-center > 3px
  (icon center = label center), desktop grid `250px 1fr`, mobile single column with `dd` text
  aligned under the label (both at x=101px @390). Viewed: `details-burst-pipe-1440/390.png`,
  `details-cost-390.png`, `details-drying-1440.png` (+ water-removal, sewage-cleanup, flood-cleanup
  captured). The sticky-header / call-bar bands visible mid-image in the 390 element screenshots
  are capture artefacts of fixed elements, not page defects.
- **Footer clean at all widths** — 3-column @1440, single-column @390/@320, alignment/spacing
  correct, no clipping/overflow/ragged edges (`footer-full-home-1440/390/320.png`,
  `footer-full-burst-pipe-390.png`, `footer-full-cape-coral-390.png`, `footer-full-cost-1440.png`).
- **Mobile first viewport has a call affordance** — fixed call bar "☎ Call 239-356-3708" visible
  without scrolling at 390 and 320 on all 34 pages (66px tall, in-viewport at load); header call
  button present @1440.
- **Skip link present + functional on 34/34** — "Skip to main content", `href="#main"`; focus test:
  link becomes visible at left:12px/top:12px, Enter moves focus to `MAIN#main` (scrollY 80).
- **No clipped or overlapping text anywhere** — `clippedCount: 0` on all pages/widths, confirmed by
  viewing hero montages, kinds/details/footer shots and home slices (the fixed call bar covering
  content mid-scroll is normal fixed-bar behaviour; page-body/footer bottom padding clears it at
  page end).

## Limitations (not findings)

- **Footer map tiles not verifiable locally:** the Google Maps iframe renders as an empty bordered
  box in this VM (google.com unreachable — same tunnel block as pages.dev). Live tiles need a
  real-browser look (standing open item from the 20x round).
- **Live render not checked:** all visual checks are of local `out/` served on 127.0.0.1:8931;
  the parent verified local `out/` byte-identical to live, so this stands in for live.
- Local server left running on port 8931 for follow-up workers (kill with `kill $(pgrep -f "http.server 8931")`).

## Summary

**P1 0 · P2 3 · P3 5 — what passed clean: overflow 0 on 34/34 pages at all widths; contrast ≥4.5:1 everywhere solid; tap targets ≥44px everywhere; all 34 heroes + all 13 kinds cards readable desktop and mobile; all 26 details cards aligned; five-fix regression holds on all five items; footer clean at all widths; mobile call affordance + functional skip link on 34/34; zero clipped/overlapping text.**
