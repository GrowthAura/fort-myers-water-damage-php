# FINDINGS — Fort Myers NEW PHP site, 10X round, BUILDER
## `~/workspace/fort-myers-php/` — 2026-11-19

**Task:** apply the adjudicated fix list only (design P1/P2/P3 + speed §5 fixes
2–3), re-export, self-verify. No push, no deploy, no MEMORY.md edit.
**Environment:** PHP was NOT installed (VM replacement wiped it). Installed
`php-cli php8.3-mbstring` — `apt-get update` took ~15 min (slow mirror, not
stuck; verified healthy 1.1 MB/s to azure.archive.ubuntu.com while it ran).
PHP 8.3.6, `mbstring` present. Export is Python
(`python3 qa/export_cloudflare.py out`), never run with php. Playwright
bundled Chromium only, no `executable_path`. All temp servers stopped by PID
at the end (8135/8136/8137); scratch copies under `/tmp` removed from use.

**Files changed (git status):** `site/assets/css/styles.css`,
`site/assets/js/main.js`, `site/includes/functions.php`,
`site/assets/fonts/inter-var.woff2` (subset — see §3), `qa/export_cloudflare.py`
(minify step). New QA tools: `qa/probe_10x.py` (before/after measurements +
screenshots), `qa/lh-10x-run.sh` (Lighthouse runner), `qa/fonts-orig/` (full
Inter backup, md5 `260c81a4759baf163c025001c4f27872`).
**No visible word changed** — verify_export word-diff 0 on all 34 pages.
No links added, no address/fact invented, no photos added, no domain attach.

---

## 1. Applied fixes — before / after (all measured, all screenshotted)

Screenshots: `qa/screenshots/10x-fix/before/` (baseline) and
`qa/screenshots/10x-fix/after/` (final export). Every screenshot below was
viewed at full size. Probe: `qa/probe_10x.py` (measurements.json in each dir).

| # | Fix | Before | After |
|---|---|---|---|
| 1 | Nav carets wrap (D-02): `white-space: nowrap; flex: none` on `.site-nav > a, .site-nav summary` | Header **101.2px**; "Services ▾" / "Areas ▾" wrapped, caret alone on line 2 (`01-nav-caret-desktop.png`) | Header **80px**; summaries 54.6px tall, single line, caret inline (`01-nav-caret-desktop.png` after). Header stays 80px. |
| 2 | Call bar covers open mobile menu (D-03): at ≤620px `.mobile-menu-panel { max-height: calc(100dvh - 80px - 66px); }` | Panel bottom **844** = viewport bottom; call bar (top 778) covered bottom 66px; menu Call button at y1539–1595 unreachable | Panel bottom **778** = call-bar top; max-height 698px. Scrolled to bottom, menu Call button bottom = **754 ≤ 778** — fully visible + tappable above the bar. |
| 3 | Homepage hero inset (D-04): hero block rendered as direct child of `<main>` in `render_page()` (template move, same markup) | Hero x=124, w=1192 — white gutters all round | Hero **x=0, w=1440, y=80** — full-bleed like the other 33 pages (`02-home-hero-desktop.png` after). No word changes. |
| 4 | Mobile tables hide a column, no cue (D-07): inset right-edge fade on `.table-wrap` | Home table first paint: 4th column invisible, right edge flush, no cue | Fade present on the right edge (`11-home-table-mobile.png` after; `box-shadow: inset -24px 0 16px -16px rgba(10,46,56,.28)`, `hasFade: true` measured). Home table is 529px wide vs 390px wrap (audit figure; own probe's scrollWidth read 390 pre-scroll because `content-visibility:auto` defers it — re-measured after scrollIntoView, see §5 note). |
| 5 | Mobile hero taller than viewport (D-08): ≤620px padding 56→40px (inner 44→32px), intro line-height 1.5, **CTA-first flex order** (H1 → CTAs → intro → areas). Padding alone could not do it (home hero 1195px); the audit's stronger CTA-first option was used. Desktop hero untouched. | Hero Call button top: home **965**, cost 778, insurance 887, cape 656, contact 650, water-removal 701 (viewport 844 — all below the fold) | Hero Call button top: home **304**, cost 382, insurance 427, cape 292, contact 382, water-removal 337 — **visible in the first viewport on all page classes** (`10-` + `17-` after). Hero itself still tall (home 1019px) — the button, not the hero, is what moved into view. |
| 6 | Menu group labels ~1.9:1 (D-09): `.mobile-menu-panel .nav-group { color: #a9c3c9; }` | `#46585f` on `#0a2e38` = **1.93:1**, "SERVICES" barely legible | **7.76:1** — passes WCAG AA (≥4.5:1). Viewed legible (`12-menu-open-mobile.png` after). |
| 7 | Footer links 40px (F-1): `.footer-col a` padding 7→9px; `.footer-base a` inline-block + 8px padding | Column links **40.1px**, footer phone text link **28.9px** | Column links **44.1px**, phone link **44.9px** desktop / **44 / 45px** mobile — meets the 44px bar. Footer grows slightly taller; fine. |
| 8a | Cost price column wraps (D-12): `prices` class on tables whose last header is "Rough area range" (render-time detection in `render_block()`), CSS `.table-wrap.prices td:last-child { text-align: right; white-space: nowrap; }` | Prices wrapped ("About $7,000 to $20,000 or more" over 2 lines); left-aligned | **Exactly the 3 price tables** got the class (of 7 on /cost/); the 4 prose-last-column tables ("Effect on the price", "Fort Myers example", "What to check", "What usually happens") are untouched. Desktop: prices single-line, right-aligned, scan as a column; last-col cell heights unchanged (89.9/89.9/60.4px). Mobile trade-off — see flag in §4. |
| 8b | Phone numbers break (D-13): `a[href^="tel:"]:not(.btn) { white-space: nowrap; }` | HIW step-1 "239-356-3708" split "239-356-" / "3708" (58px tall, 2 lines) | **24px, single line, nowrap** (`15-hiw-steps-mobile.png` after). The `:not(.btn)` scope is load-bearing — see §2 incident. |
| 9 | Menu toggle no Close state (D-14): `toggle` listener in `main.js` swaps label + icon + aria-label | Toggle read "☰Menu" while open | Open: **"×Close"**; closed: "☰Menu" (`12-` / `13-` after). Link-click and Escape close paths re-fire `toggle`, so the label resets correctly. |
| 10 | Footer brand void on 7 map-less location pages (D-11): `.footer-brand { align-self: center; }` (CSS only, no new links/content) | Brand content pooled at the top of its column, ~300px void below (audit figure); brand block top == Services top | Brand block centred in its track: grid 10248–10963, brand 10436–10783 — top gap 188px, bottom gap 180px. On the 27 map pages the brand column is tallest, so the rule is a no-op there. Viewed (`05-footer-location-desktop.png` after). |
| 11 | Speed — subset Inter variable font to latin (§5 fix 2) | `inter-var.woff2` 48,256 B, cmap 230 glyphs, fvar wght 100–900 | **40,656 B (−7,600 B, −15.7%)**, cmap 225, fvar + gvar retained, wght 100–900. Coverage PROVEN: all 102 distinct rendered chars collected from every out/ HTML file + CSS + JS; **0 used chars lost** (every char the full font covered is still covered). 3 glyphs (▾ U+25BE, ☎ U+260E, ☰ U+2630) were already absent from full Inter (system fallback before and after — unchanged behaviour). Pixel proof: full-page screenshots home + cost + insurance, identical HTML/CSS, only the font file swapped — **0 differing pixels** (31.3M / 25.5M / 22.7M pixels). Archivo Black kept as-is (18.6 KB). Original backed up at `qa/fonts-orig/inter-var-full.woff2`. |
| 12 | Speed — minify CSS in the export step (§5 fix 3) | `styles.css` 19,984 B source (17,628 B at audit time + this round's additions) | Minified **in the export only** (`qa/export_cloudflare.py`, rcssmin): **19,984 → 13,523 B (−32%)** in the first export, 20,235 → 13,523 B after the §2 fix. Source stays readable. Guards in the script assert `calc(100dvh - 80px - 66px)` spacing and the `\25BE` caret content survive; if rcssmin is missing the export still succeeds with a loud warning. verify_export + render_check pass clean on the minified output (below). HTML minification skipped — see §3. |

### D-06 stacked Call CTAs — INSPECTED, left as-is (per the adjudication)
Cape Coral desktop, measured: hero CTA bottom 585 → breadcrumb 673–725 →
top-of-body `.cta-line` CTA top 773. The two CTAs are **separated by the
breadcrumb (88px gap + breadcrumb content)** — not visually adjacent with
zero content between them. Call affordance is his explicit preference, so
both stay. No change made.

---

## 2. Incident during verification — tel: nowrap caused mobile overflow (caught, fixed, re-verified)

First re-export + `render_check.py` showed **new horizontal overflow at
320/360/390 on pages with a `.cta-line` button** (e.g. cape-coral: overflow
97px at 390, worst element `A.btn right=487 w=467`). Cause: my
`a[href^="tel:"] { white-space: nowrap; }` also matched the `.cta-line`
Call button, which is itself a tel: link — its label ("Call 239-356-3708,
answered 24/7", 467px) could no longer wrap, so the button forced the page
wider. The audits had measured overflow 0, so this was my regression, not
pre-existing.
Fix: scoped the rule to `a[href^="tel:"]:not(.btn)` — body-text phone
numbers stay unwrapped (HIW step 1 still 24px / single line), buttons keep
wrapping their labels. Re-exported, re-ran render_check: **0 pages with
overflow** (34/34, all widths). The minified CSS was regenerated with the
fix (20,235 → 13,523 B).

---

## 3. Skipped / not done

- **HTML minification (speed §5 fix 3, optional part): SKIPPED.** Only CSS
  was minified. Reason: the CSS minify already removes Lighthouse's only
  `unminified-css` opportunity; HTML is served Brotli-compressed live
  (~72% smaller on the wire per the speed audit), so the extra saving is
  negligible; and minifying HTML risks the byte-exact word-diff and
  JSON-LD verification this site depends on. No HTML minifier was run.
- **Everything in the DO-NOT-DO list was not done:** no 780px line cap
  (wide 1240px lines stay), no breadcrumb move, no stacked-CTA removal
  (§1 D-06), no photos, no publisher logo / Article images, no critical-CSS
  inlining, no `content-visibility` removal, no Maps preconnects, no word
  changes, no new links, no invented address/fact, no domain attach, no old
  repo / live Next.js touch, no deploy.

---

## 4. Flag for the parent — cost price nowrap: mobile row-height trade-off

The ordered nowrap works exactly as specified on desktop (prices scan as a
column, zero height change). On **mobile** it has a real side effect, measured:
the price column sizes to its longest value ("About $7,000 to $20,000 or
more" → column **324px** wide), so the table grows to **550px** inside the
390px wrap (scrolls; the D-07 fade cue signals it) and the two prose columns
squeeze to 110/116px, so their text wraps into more lines — first three rows'
last-cell heights **222 → 362, 194 → 306, 166 → 278px**. Prices themselves
are single-line + right-aligned and readable once scrolled (`14-` after).
Kept as ordered (the adjudication says nowrap on price cells); if he wants
the mobile rows back down, the natural refinement is desktop-only nowrap —
that is a parent call, not applied here.

---

## 5. Verification (final export, after the §2 fix)

| Check | Result |
|---|---|
| `python3 qa/verify_export.py` | **FAILURES 0 / NOTES 0** (word-diff 0 all 34 pages; H1/title/meta/schema OK) |
| `python3 qa/validate_schema.py` | **pages 34 \| scripts 92 \| nodes 92 \| ERRORS 0 \| WARNINGS 0** (+ 6 by-design NOTES, unchanged: 3× Article `image`, 3× publisher `logo`) |
| `python3 qa/render_check.py` | **34/34 overflow 0** at 320/360/390/1440; body font **20px** at 390 + 1440 on all routes |
| Dash sweep (literal + entities `&ndash;`/`&mdash;`/`&#8211;`/`&#8212;`) | **0 files** |
| Sitemap | **31 locs**; `_redirects` 33 lines |
| Footer map | **0 iframes on all 7 location pages** (areas, cape-coral, fort-myers-beach, estero, bonita-springs, lehigh-acres, north-fort-myers); 1 on home |
| Images | **0 `<img>`** in out/ (heroes honestly empty, unchanged) |
| Home hero full-bleed | `<section class="hero">` is a direct child of `<main>`, before the `.page-body` container; measured x=0 w=1440 |
| `prices` class scope | 3 price tables on /cost/ only; 4 prose tables untouched |
| Menu scrolled to bottom | Call button bottom 754 ≤ call-bar top 778 — reachable |
| Minified CSS guards | `calc(100dvh - 80px - 66px)` + `\25BE` present in out/ CSS; 150 CSS rules parse clean (print + content-visibility blocks intact) |

### Speed — Lighthouse (local out/ on :8135, Lighthouse 13.6.0, bundled Chromium)

| Run | Perf | FCP | SI | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| Mobile home m1 | 96 | 1.4 s | 4.0 s | 1.4 s | 170 ms | 0 |
| Mobile home m2 | 96 | 1.4 s | 3.8 s | 1.4 s | 160 ms | 0 |
| Mobile home m3 | 99 | 1.5 s | 2.5 s | 1.5 s | 10 ms | 0 |
| **Mobile median-of-3** | **96** | **1.4 s** | **3.8 s** | **1.4 s** | **160 ms** | **0** |
| Desktop home d1 | 100 | 0.4 s | 0.4 s | 0.4 s | 0 ms | 0 |

vs audit baseline: mobile home 86–98 (median ~96–97), desktop 100. **No
material score movement** — consistent with the audit's verdict that the
variance is host-CPU noise under 4× throttle and the font subset + CSS
minify are worth +0–2 points at most. The SI tail (2.5–4.0 s) is the same
simulated font-swap tail the audit identified; observed first paint is a
single complete paint (CLS 0 in every run). Real savings: font −7.6 KB,
CSS −6.5 KB raw (Brotli makes the CSS wire saving smaller).

### Before/after measurement summary (probe)

| Metric | Before | After |
|---|---|---|
| Header height (desktop) | 101.2px | **80px** |
| Nav summary height | 85.2px (wrapped) | 54.6px (single line) |
| Home hero (desktop) | x=124, w=1192 (inset) | x=0, w=1440 (full-bleed) |
| Mobile hero CTA top (home / cost / insurance / cape / contact / water) | 965 / 778 / 887 / 656 / 650 / 701 | **304 / 382 / 427 / 292 / 382 / 337** (viewport 844) |
| Mobile menu panel bottom | 844 (under call bar) | 778 (= call-bar top) |
| Menu group-label contrast | 1.93:1 | **7.76:1** |
| Footer column links / phone link | 40.1px / 28.9px | **44.1px / 44.9px** |
| HIW tel link height | 58px (2 lines) | **24px (1 line)** |
| Menu toggle | "☰Menu" always | "×Close" open / "☰Menu" closed |
| Footer brand column (cape-coral) | top-aligned, void below | centred (top gap 188px, bottom 180px) |
| Cost price column (desktop) | wrapped, left-aligned | single-line, right-aligned |
| Inter variable font | 48,256 B | **40,656 B** (0 glyphs lost, 0 differing pixels) |
| styles.css (exported) | 17,628 B unminified | **13,523 B minified** |

## 6. Open / standing (unchanged, not mine to close)

- No push / deploy done — verification + deploy happen after this, by others.
- Live map tiles still need one real-browser look (VM Chromium cannot reach
  google.com/maps); markup + pin URL verified, unchanged.
- Live Speed Index still unmeasured from this VM (PageSpeed 429, per the
  speed audit); lab numbers above are the measured evidence.
- Scratch copies under `/tmp` (`out-scratch`, `out-fontfull`) and their
  servers (8136/8137) were stopped/removed; the 8135 server (final out/)
  was also stopped by PID at the end of verification.
