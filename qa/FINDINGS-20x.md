# FINDINGS — Fort Myers NEW PHP site, 20X round, BUILDER
## `~/workspace/fort-myers-php/` — 2026-11-19

**Task:** Part 1 — fix verifier defect D-V1 (NOT READY, P2) exactly as ruled;
Part 2 — take every 10x improvement one step further (D1–D5, S1–S2, E1–E3,
M1, A1); skip anything that cannot be done safely and say why. No push, no
deploy, no MEMORY.md edit.
**Environment:** PHP 8.3.6 already installed (`php -v` verified; mbstring
present — no reinstall needed). Export is Python
(`python3 qa/export_cloudflare.py out`), never run with php. Playwright
bundled Chromium only, no `executable_path`. Temp servers stopped by PID
(8135: 40457, 8136: 44049); scratch copies under `/tmp` removed.
**Baseline:** continued from the uncommitted 10x working tree (no commit);
baseline re-export reproduced the 10x state exactly (CSS 20,235 → 13,523 B
minified, Inter 40,656 B) and the before-probe re-measured D-V1 exactly as
the verifier reported (table 1: 550px, table 3: 616px).

**Files changed (git status, this round on top of the 10x tree):**
`site/assets/css/styles.css`, `site/includes/header.php`,
`site/includes/footer.php`, `site/assets/js/main.js`,
`site/assets/fonts/archivoblack-400.woff2` (subset — see S1),
`site/robots.txt`, `site/llms.txt`, `qa/export_cloudflare.py`
(llms-full.txt generation). New QA tools: `qa/probe_20x.py`
(before/after measurements + screenshots),
`qa/screenshots/20x/{before,after}/` (+ `lighthouse/` JSON reports).
`qa/fonts-orig/archivoblack-400-full.woff2` added (full-font backup,
md5 `4b6914a69e6a586fbe253f73d19d90b0`).
**No visible word changed** — verify_export word-diff 0 on all 34 pages.
No photos added, no address/fact invented, no domain attach, no old repo /
live Next.js touch, no deploy.

---

## PART 1 — D-V1 FIXED (verifier defect, P2): mobile /cost/ prices visible again

**Change:** exactly the verifier's ruling — `white-space: nowrap` on
`.table-wrap.prices td:last-child` moved into a `@media (min-width: 621px)`
block (the site's breakpoint is 620px); the base rule keeps only
`text-align: right`. One CSS rule, no markup change, no word change.

**Re-verified at 390px (own probe, all three prices tables):**

| Table | Width before → after | Price col before → after | Prices at first paint | First-3-row heights before → after |
|---|---|---|---|---|
| 1 — "Size of the job" | 550px → **390px** | 324px → **114px** | hidden → **visible** | 362 / 306 / 278 → **222 / 194 / 166** |
| 2 — "What is being priced" | 390px → **390px** | 181px → 129px | visible → visible | 83 / 83 / 111 → 83 / 83 / 111 |
| 3 — "Repair after water damage" | 616px → **390px** | 480px → **200px** | hidden → **visible** | 111 / 111 / 111 → 83 / 83 / 83 |

Row heights are back to the pre-10x-round state the verifier expected
(~222px first row). Viewed at full size: `10b-cost-table1-mobile-viewport.png`
(all 3 columns + prices visible, right-aligned, wrapped) and
`11b-cost-table3-mobile-viewport.png` (incl. the 51-char "From about $500
for a small area to $10,000 or more" now wrapping to 3 lines, and the prose
value "Priced per linear foot and per room" wrapping too).

**Desktop untouched (measured, same probe):** all 3 tables 1190px,
`white-space: nowrap`, `text-align: right`, row heights 90/90/60,
60/60/60, 60/60/60 — byte-identical to the 10x after-state. **D-V1: FIXED.**

---

## PART 2 — 20X items (before → after, all measured, all screenshotted)

Screenshots: `qa/screenshots/20x/before/` (baseline) and
`qa/screenshots/20x/after/` (final export). Every screenshot below was
viewed at full size. Probe: `qa/probe_20x.py` (measurements.json in each dir).

| # | Item | Before | After |
|---|---|---|---|
| D1 | Hero depth (design): subtle CSS-only river motif, no photo | Hero was a flat linear gradient (`01-hero-desktop-home.png` before: barren right ~40%) | `.hero-no-media::after`: soft teal radial glow top-right + two low-opacity wave bands along the bottom (white 5% + gold 8%, brand palette), above the scrim, below the text (z-index 1 vs hero-inner 2). Viewed desktop (`01-hero-desktop-home.png`) + mobile (`12-hero-mobile-home.png`): visible but subtle, text contrast untouched (hero 683px, x=0/w=1440 unchanged; H1/intro/CTAs pixel-identical positions). No new words, no photo. |
| D2 | Skip link (a11y): "Skip to main content", hidden until focused | Link already existed but read "Skip to content" (plain focus style) | Label is now exactly **"Skip to main content"** (`header.php`), focus style hardened (bold, underline, 3px gold outline). Real Tab press: focused=true, visible 238×58 at (12,12), coral bg, desktop AND mobile 390px. Viewed `02-skiplink-focused-desktop.png`. (Chrome label only; `<main id="main">` already existed.) |
| D3 | Active nav state (design/a11y): current page unmistakable, desktop + mobile | `aria-current="page"` was emitted everywhere but had **zero** distinct styling (bg transparent, decoration none, weight 400/500) | Distinct styling on every nav surface: desktop dropdown current item is now a **non-link `<span class="nav-current">`** (sand `#efe7d6` bg, coral `#c2410c`, 700 — viewed `03b-nav-dropdown-active-desktop.png`: unmistakable); mobile-menu current item (white bg 14% + 4px gold left border + 700 — viewed `13-menu-open-mobile.png`, "Home" highlighted); footer current link (white + 700 + gold underline); top-level nav current link (gold 22% bg + 3px gold underline); brand on home (gold underline). Measured on `/water-removal/`: dropdown SPAN sand/coral/700, mobile-panel A bg .14/700, footer A underline/white/700. Correction to the brief: the dropdown current item was **not** a span before — it was an `<a href=self>`; I converted it to the span the task describes (no self-link in the dropdown now; header self-links were never counted as defects, only `<main>` ones are). |
| D4 | Back to top (UX): footer placement only | No such control | `<a class="back-to-top" href="#top">Back to top</a>` in the footer base (`<body id="top">` added), underlined, 92×45px on mobile (≥44px), 92×45px desktop. Real click from scrollY 20,847 → **0 in ~2 s** (smooth scroll via minimal JS; href still works without JS). Footer-only, so it cannot collide with the sticky mobile call bar. Viewed in `15-footer-mobile.png` (next to the footer phone link) + `06-footer-desktop.png`. |
| D5 | FAQ link affordance (design) | Links were already underlined — but only by the UA default (no CSS rule; `text-decoration: underline`, offset auto, teal `#0b5563` on white = 8.42:1) | Made explicit, not UA-dependent: `.faq-item p a { text-decoration: underline; text-underline-offset: 3px; }`. Measured: underline, 3px offset, teal, 20px. Open state by real click still proven: desktop open=true (186px), mobile open=true (393px). Viewed `05-faq-open-desktop.png` + `14-faq-open-mobile.png` (tel link underlined inside the open answer). No visual change — this was a hardening, not a fix. |
| S1 | Archivo Black subset (speed): latin, same method as Inter | `archivoblack-400.woff2` 18,604 B, cmap 220 glyphs | **18,084 B (−520 B, −2.8%)**, cmap 220 glyphs, **0 glyphs lost**, same tables — via `python3 -m fontTools.subset` with the same latin unicode ranges as the Inter subset. Why so small: the full file was *already* latin-only (no combining diacritics to drop, unlike Inter's 5). Full font backed up at `qa/fonts-orig/archivoblack-400-full.woff2`. Pixel proof (own scratch export with the full font, full-page): home **0 differing pixels** (31,315,680), cost **0** (25,598,880), insurance **0** (22,754,880). Used-char check: all 72 distinct Archivo-context chars (headings/brand/step numbers) are in the subset; the only non-ASCII char anywhere in the export (`·` U+00B7) is in the latin range. |
| S2 | Font preload fetchpriority (speed) | Both font preloads had **no** `fetchpriority` | Added `fetchpriority="high"` to both preloads (Archivo Black + Inter) in `header.php`. Verified: exactly 2 occurrences in every exported page (34/34). Correct: both fonts are render-critical (H1 + body). |
| E1 | OG/Twitter completeness (SEO) | **Already complete — nothing to add.** Audit of all 34 pages: `og:title`, `og:description`, `og:type`, `og:url`, `og:site_name`, `og:locale` present on 34/34; `twitter:card` (summary), `twitter:title`, `twitter:description` present on 34/34; `og:image`/`twitter:image` on **0** pages (no photo exists — correctly absent, never invented). All values factual (paste titles/descs + canonicals). | No change made. |
| E2 | robots.txt crawlers (SEO/AEO) | 15 named AI crawlers allowed + `*` + Bytespider disallowed (17 `User-agent:` lines) | **+5 real, documented, missing crawlers → 20 named AI allowed (22 `User-agent:` lines):** `Perplexity-User` (Perplexity's second documented agent — fetches on a user question), `Applebot` (Apple's actual search crawler for Spotlight/Siri/Safari — only the training-only token `Applebot-Extended` was listed; Apple Support "About Applebot"), `Amazonbot` + `Amzn-SearchBot` + `Amzn-User` (Amazon's three documented agents; Amzn-SearchBot is the Alexa-search one). Each addition cites its operator's docs in a robots.txt comment. **Bytespider still `Disallow: /`.** Deliberately NOT added: Mistral (no documented crawler UA found), DuckDuckBot/Bravebot (search crawlers, not AI answer engines), Grok/xAI (no documented UA verified) — listed here so the next round doesn't re-add them on a guess. |
| E3 | llms-full.txt (AEO/GEO) | No full-content file existed | **Generated + linked.** `qa/export_cloudflare.py` now builds `out/llms-full.txt` from the **same fetched HTML** that becomes the pages (regenerated on every export, so it cannot drift — in sync by construction; never edited by hand). 31 pages, **419,280 bytes**, all 31 sitemap locs present (verified: 0 missing), each page as `## <title>` + canonical URL + full visible text in document order, no invented words. `site/llms.txt` links it with a plain line ("Full text of every page above: …/llms-full.txt") — deliberately NOT a `- [` entry, so the verify_export `llms.txt entries == 31` check still holds. |
| M1 | Map fallback link (robustness) | No fallback link under any map iframe | **"View larger map" under every FOOTER map** — 27 pages × 2 file twins = 54 occurrences in out/, href = the **same pin URL** as the iframes (`https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed`, `target="_blank" rel="noopener"`), gold-cream `#ffd9a8` underlined on the dark footer, 139×51px on mobile. Viewed `15-footer-mobile.png` (link visible under the blank-in-VM iframe — exactly the failure it covers) + `06-footer-desktop.png`. **Section maps (home + contact) deliberately NOT given the link** — see "Skipped / partial" below. Footer map still 0 iframes on the 7 location pages (unchanged); home + contact still 2 iframes each. |
| A1 | Tap targets (a11y): re-measure ALL interactive elements after the changes | One discrete sub-44px target found in the baseline: the brand link, 540×**40px** desktop (mobile brand was already ≥44). Everything else discrete was already ≥44 (nav 53–85px, menu items 61px, toggle 86×55, call bar 390×66, FAQ summaries 64–92px, footer links 44.1px, footer phone 44.9px). The remaining sub-44 items were inline prose links (24px, WCAG 2.5.8 inline exception). | **Brand fixed: `.brand { min-height: 44px; }` → 540×44 desktop, 248×62 mobile.** Re-measured ALL interactive elements on home, desktop + mobile (+ menu open): **0 discrete sub-44px targets remain.** The single remaining sub-44 item in the census is one "North Fort Myers" link *inside a table cell* (149×23) — inline prose inside running text, same exempt class as the other 47/48 (desktop) and 39/40 (mobile) inline links. New controls: skip link 238×58 (focused), back-to-top 92×45, map link 139×51 — all ≥44px. |

### Skipped / partial (with reasons — nothing forced)

- **M1, section maps (home + contact): PARTIAL, by design.** The two
  map-section iframes sit inside `<main>`, where verify_export enforces a
  byte-exact word-diff 0 against the pastes — any visible "View larger map"
  text there would FAIL the word-diff on both pages. Adding the link was
  therefore done only under the footer maps. No page loses the fallback:
  home and contact both carry a footer map with the link on the same page.
  (An icon-only/aria-only link was rejected as worse UX than an honest
  partial.)
- **E1: nothing to add** (already complete — see table).
- **D5: no visual change** (already underlined; rule made explicit only).
- **Everything in the DO-NOT-DO list was not done:** no 780px line cap
  (wide 1240px lines stay), no breadcrumb move, no stacked-CTA removal, no
  photos in heroes, no publisher logo / Article images, no critical-CSS
  inlining, no `content-visibility` removal, no Maps preconnects, no word
  changes, no new links except the M1 map links + D2/D4 chrome controls
  (which link only to `#main` / `#top`), no invented address/fact, no
  domain attach, no old repo / live Next.js touch, no deploy.
- **D3 note:** the dropdown current item was an `<a>` before, not the span
  the brief assumed — converted to the span (see D3 row). The breadcrumb
  current crumb was already a non-link `<span>` and is untouched.

---

## VERIFICATION (final export, after all changes)

| Check | Result |
|---|---|
| `python3 qa/verify_export.py` | **FAILURES 0 / NOTES 0** (word-diff 0 all 34 pages; H1/title/meta/canonical/schema OK) |
| `python3 qa/validate_schema.py` | **pages 34 \| scripts 92 \| nodes 92 \| ERRORS 0 \| WARNINGS 0** (+ 6 by-design NOTES, unchanged: 3× Article `image`, 3× publisher `logo`) |
| `python3 qa/render_check.py` | **34/34 overflow 0** at 320/360/390/1440; body font **20px** at 390 + 1440 on all routes |
| Dash sweep (literal – — + entities `&ndash;`/`&mdash;`/`&#8211;`/`&#8212;`) | **0 files** (68 HTML files) |
| Sitemap / robots / llms | **31 locs**; robots **22 `User-agent:` lines** (20 AI allowed + `*` + Bytespider disallow + Sitemap line); llms **31 entries** (= sitemap locs); **llms-full.txt 31 pages, 419,280 B, 0 sitemap locs missing** |
| Footer map | **0 iframes on all 7 location pages** (areas, cape-coral, fort-myers-beach, estero, bonita-springs, lehigh-acres, north-fort-myers); 2 iframes home + contact; 1 on the other 25 routes |
| Images | **0 `<img>`** in out/ (68 files); **0 `og:image`** |
| Links (own census, 35 flat route files, 4,011 hrefs) | **0 broken local targets**; **0 self-links in `<main>`**; **0 missing fragment targets**; single tel: `tel:+12393563708`; externals only the canonical self-domain URLs + `msc.fema.gov` + the Google Maps pin URL (M1 link / iframe src) |
| OG/Twitter census (34 route files) | All 6 og: tags + 3 twitter: tags on 34/34; 0 og:image |
| FAQ open state (real click, home) | **open: true**, desktop 186px, mobile 393px — viewed `05-` + `14-faq-open-*.png` |
| /cost/ mobile re-check (Part 1) | Tables 390/390/390px, prices visible at first paint, rows 222/194/166 (see §Part 1); desktop nowrap/right/rows unchanged |
| Back to top (real click) | scrollY 20,847 → **0** (~2 s smooth scroll) |
| Skip link (real Tab) | focused + visible 238×58, desktop + mobile |
| Minified CSS guards | `calc(100dvh - 80px - 66px)` + `\25BE` present in out/ CSS; minified **24,335 → 15,596 B** (was 13,523 B — the +2,073 B is the new D1/D3/D5/M1/D4 rules + the wave SVG data URI) |
| Font subset pixel proof | Full-page home/cost/insurance, subset vs full font: **0 differing pixels** (31,315,680 / 25,598,880 / 22,754,880) |
| Header height (regression) | Still **80px** desktop (brand min-height 44px did not grow it); nav summaries single-line |

### Speed — Lighthouse (local out/ on :8135, Lighthouse 13.6.0, bundled Chromium)

| Run | Perf | FCP | SI | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| Mobile home m1 | 97 | 2.0 s | 2.0 s | 2.0 s | 20 ms | 0 |
| Mobile home m2 | 90 | 1.3 s | 4.0 s | 1.3 s | 340 ms | 0 |
| Mobile home m3 | 95 | 1.4 s | 3.9 s | 1.4 s | 190 ms | 0 |
| **Mobile median-of-3** | **95** | **1.4 s** | **3.9 s** | **1.4 s** | **190 ms** | **0** |
| Desktop home d1 | 100 | 0.4 s | 0.6 s | 0.4 s | 10 ms | 0 |

vs 10x: mobile median 93 (verifier) / 96 (builder), desktop 100. **No
material movement** — consistent with the speed audit's verdict that the
mobile variance is host-CPU noise under 4× throttle (m1's SI 2.0 s vs m2/m3's
~3.9 s is the same font-swap SI tail regime split; TBT 20–340 ms drives the
score spread). Real savings this round: Archivo −520 B, CSS +2.1 KB (new
rules), llms-full.txt +419 KB (a crawler file, never loaded by browsers).

### Before/after measurement summary (probe)

| Metric | Before | After |
|---|---|---|
| /cost/ table 1 / table 3 width (390px) | 550px / 616px, prices hidden | **390px / 390px, prices visible** |
| /cost/ table 1 first-row height (mobile) | 362px | **222px** (pre-round state) |
| /cost/ desktop prices | nowrap, right, rows 90/90/60 | **unchanged** |
| Hero (desktop home) | flat gradient, empty right ~40% | **subtle glow + wave bands**, same geometry (683px, x=0/w=1440) |
| Skip link | "Skip to content", plain focus | **"Skip to main content"**, gold focus ring, 238×58 visible on Tab |
| Nav current item (dropdown) | link, no distinct style | **non-link span, sand bg + coral bold** |
| Nav current item (mobile menu) | link, no distinct style | **highlighted bg + gold left border + bold** |
| Footer current link | no distinct style | **white + bold + gold underline** |
| Back to top | absent | **present, footer only, click → scrollY 0** |
| FAQ answer links | underline (UA default only) | **underline, 3px offset, explicit CSS** |
| Archivo Black | 18,604 B, 220 glyphs | **18,084 B (−2.8%), 220 glyphs, 0 lost, 0 differing pixels** |
| Font preloads | no fetchpriority | **fetchpriority="high" ×2** |
| robots.txt named AI crawlers | 15 allowed | **20 allowed** (Perplexity-User, Applebot, Amazonbot, Amzn-SearchBot, Amzn-User added; Bytespider still disallowed) |
| llms-full.txt | absent | **31 pages, 419,280 B, generated from export HTML** |
| Map fallback links | 0 | **27 footer maps** (54 occurrences incl. twins); section maps skipped (word-diff — see above) |
| Brand tap target (desktop) | 540×40px | **540×44px**; 0 discrete sub-44px targets remain |
| styles.css (exported, minified) | 13,523 B | **15,596 B** (new rules + wave SVG) |

## Open / standing (unchanged, not mine to close)

- No push / deploy done — verification + deploy happen after this, by others.
- Live site is still the pre-10x build
  (`fort-myers-water-damage-php.pages.dev`); nothing here was pushed.
- Live map tiles still need one real-browser look (VM Chromium cannot reach
  google.com/maps); markup + pin URL verified, and the new "View larger map"
  link is the fallback for exactly that failure.
- Live Speed Index still unmeasured from this VM (PageSpeed 429, per the
  speed audit); lab numbers above are the measured evidence.
- Scratch copies under `/tmp` (`out-fontfull20x`, font-pixel PNGs) removed;
  both temp servers (8135/8136) stopped by PID.
