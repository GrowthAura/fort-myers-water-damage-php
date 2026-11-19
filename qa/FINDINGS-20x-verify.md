# FINDINGS — Fort Myers NEW PHP site, 20X round, INDEPENDENT VERIFICATION
## `~/workspace/fort-myers-php/` — 2026-11-19, verifier (fresh eyes; did not build)

**Method:** re-exported first (`python3 qa/export_cloudflare.py out` — reproduced
the builder exactly: CSS 24,335 → 15,596 B minified, llms-full.txt 419,280 B,
Archivo 18,084 B), then measured everything myself with new probes
(`qa/probe_20x_verify.py`, `qa/probe_20x_verify2.py`, `qa/probe_20x_verify3.py`,
`qa/probe_20x_fontpixel.py`, served `out/` on 127.0.0.1:8145, Playwright
bundled Chromium only, no `executable_path`). Every screenshot below was
viewed at full size. No `site/` source file was edited; no push, no deploy,
no MEMORY.md edit. Temp servers stopped by PID; scratch copy
`/tmp/out-fontfull20x-verify` removed.

**Verdict: NOT READY — 2 defects, both P3.** Nothing here is broken for a
visitor: the D-V1 money-page fix is exact, the hero, FAQ, maps, fonts,
robots and llms work all verify, and the full regression suite is clean.
What fails is completeness against the round as specified: D3 was ordered
with "NO self-linking nav item remains anywhere in header/footer" and the
current page unmistakable in the header nav — 51 self-linking nav items
remain sitewide and the closed Services/Areas header shows no current-section
marker on 27 pages (D-V2); and D2 was ordered with "moves focus to main" —
DOM focus never lands on `<main>` (D-V3). Both fixes are small (spans +
a summary marker + `tabindex="-1"`); re-verify just D2/D3 after.

---

## 1. Per-item verdicts (all measurements mine)

| # | Item | Verdict | My measurement |
|---|---|---|---|
| D-V1 | Mobile /cost/ prices visible again | **PASS** | 390px: tables **390/390/390px**, price cols 114/129/200px, prices at first paint on all 3, rows 222/194/166, 83/83/111, 83/83/83 — byte-identical to the pre-round state the 10x ruling required; `documentElement.scrollWidth` 390. Viewed `20b-cost-table1-mobile-scrolled.png` (all 3 columns + wrapped right-aligned prices, e.g. "About $1,200 to $3,500") and `21-cost-table3-mobile-viewport.png` ("From about $500 for a small area to $10,000 or more" wrapping to 3 lines). Desktop: all 3 tables 1190px, `white-space: nowrap`, `text-align: right`, rows 90/90/60, 60/60/60, 60/60/60 — unchanged. CSS confirms the rule now lives only in `@media (min-width:621px)`. |
| D1 | Hero river motif, subtle, geometry unchanged | **PASS** | `.hero-no-media::after`, z-index 1 (below text), radial teal glow top-right (30% opacity) + two wave bands (white 5%, gold 8%). Hero x=0, y=80, w=1440, **h=683** — unchanged; header 80px. Viewed `01-hero-desktop-home.png` + `12-hero-mobile-home.png`: visible but subtle, text contrast untouched, no layout shift (Lighthouse CLS 0 both viewports). |
| D2 | Skip link, real Tab test | **PARTIAL — see D-V3** | Text exactly **"Skip to main content"**, href `#main`; real Tab → focused=true, visible **238×58 at (12,12)**, coral bg, white text, 3px gold outline — desktop AND mobile 390px. Viewed `02-skiplink-focused-desktop.png`. Enter → viewport jumps to main (scrollY 80) and the next Tab lands on the first link *inside* main (hero tel link) — the keyboard flow works. BUT `document.activeElement` after Enter is **BODY, not MAIN** (`<main id="main">` has **no `tabindex`**), so DOM focus does not move to main as ordered. |
| D3 | Active nav, desktop + mobile + footer | **PARTIAL — see D-V2** | Desktop dropdown current item IS a non-link **`<span class="nav-current">`** (sand `#efe7d6`, coral `#c2410c`, 700) — viewed `03-nav-dropdown-active-desktop.png`, unmistakable. Mobile-menu current item distinctly styled (white 14% bg, 700, 4px gold left border — viewed `13-menu-open-mobile.png`). Footer current link distinctly styled (white, 700, gold underline). Brand on home: gold underline on `.brand-name` (4px offset) ✓. Top-level Cost link on /cost/: gold 22% bg + inset 0 −3px gold ✓. BUT: **51 self-linking nav items remain** in header/footer chrome (see §3), and the closed Services/Areas summary has **no** current-section styling on the 27 dropdown pages. |
| D4 | Back to top, real click | **PASS** | Footer-only `<a class="back-to-top" href="#top">`, 92×45px. Real click: scrollY 20,847 → **0** desktop; 35,170 → **0** mobile (~2 s smooth scroll). No functional collision with the sticky mobile call bar: link fully legible and tappable in `15-footer-mobile.png` (phone link + "Back to top" side by side, clear of the orange bar). Trivial observation only: the link's border-box bottom (780) sits 2px inside the call bar's top edge (778) — visually nothing is covered. |
| D5 | FAQ links distinct; open by real click | **PASS** | Answer links: `text-decoration: underline`, `text-underline-offset: 3px`, teal `#0b5563`, 20px. Real click opens the item: desktop open=true, 186px; mobile open=true, 393px. Viewed `05-faq-open-desktop.png` + `05-faq-open-mobile.png` (coral − badge, gold left border, tel link underlined inside the open answer). |
| S1 | Archivo subset: smaller, 0 used chars lost, 0 pixel diffs | **PASS** | **18,084 B** (was 18,604 B, −520 B), cmap **220 glyphs, same codepoint set as the full font** (only 3 glyph-name renames from the subsetter: `uni0000`/`NULL`, `uni000D`/`nonmarkingreturn`, `mu`/`uni00B5`). Distinct visible chars in out/: 84; the only ones missing from the subset (☎, ☰) are equally missing from the FULL font (pre-existing system fallback). My own pixel proof (scratch export with the full font, full-page, 1440px): home **0 differing pixels** (31,315,680), cost **0** (25,598,880), insurance **0** (22,754,880). Inter subset intact: 40,656 B. |
| S2 | fetchpriority="high" on both font preloads, all pages | **PASS** | Exactly **2** occurrences on **all 68 HTML files** (34 routes + twins + 404). |
| E1 | OG/Twitter complete, 0 og:image | **PASS** | All 6 og: + 3 twitter: tags on **34/34** route files; `og:image` on **0**. Note only: `404.html` carries 5/6 og tags (no `og:url`) — it is not one of the 34 routes and is non-indexed. |
| E2 | robots.txt: 20 named AI crawlers, Bytespider out, Sitemap | **PASS** | **22 `User-agent:` lines** = 20 named AI allowed + `*` + Bytespider `Disallow: /` + Sitemap line. The 5 new ones are all present: Perplexity-User, Applebot, Amazonbot, Amzn-SearchBot, Amzn-User. |
| E3 | llms-full.txt: 31 pages, linked from llms.txt | **PASS** | `out/llms-full.txt` **419,280 B, 31 `##` pages, all 31 sitemap locs present (0 missing)**. `site/llms.txt` links it with a plain line; llms.txt still **31 entries**. |
| M1 | Map fallback "View larger map" under footer maps | **PASS** | **54 occurrences = 27 footer-map pages × 2 twins**; the 14 files without it are exactly the 7 location pages × 2. Link 139×51px mobile + desktop, gold-cream `#ffd9a8`, underlined, `target="_blank"`, href = **the same pin URL as the iframe src** (`https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed`). **0 occurrences inside `<main>`** — word-diff 0 holds; home + contact section maps correctly have no added text. |
| A1 | Tap targets: 0 discrete sub-44px remain | **PASS** | Re-measured ALL interactive elements on home, cost, contact, water-removal — desktop + mobile: **0 discrete sub-44px**. Brand fixed: **540×44 desktop, 248×62 mobile**. New controls all ≥44px: skip link 238×58, back-to-top 92×45, map link 139×51. Remaining sub-44 items are all inline prose links (24px, e.g. the table-cell "North Fort Myers" 149×23) — the WCAG 2.5.8 inline exception, same class the 10x round accepted. |

---

## 2. Full regression suite (my own runs, fresh export)

| Check | Result |
|---|---|
| `python3 qa/verify_export.py` | **FAILURES 0 / NOTES 0** (word-diff 0 all 34 pages) |
| `python3 qa/validate_schema.py` | **pages 34 \| scripts 92 \| nodes 92 \| ERRORS 0 \| WARNINGS 0** (+ 6 by-design NOTES, unchanged: 3× Article `image`, 3× publisher `logo`) |
| `python3 qa/render_check.py` | **34/34 overflow 0** at 320/360/390/1440; body font **20px** at 390 + 1440 |
| Dash sweep (literal – — + entities `&ndash;`/`&mdash;`/`&#8211;`/`&#8212;`) | **0 files** (68 HTML files) |
| Sitemap / robots / llms | **31 locs**; robots 22 `User-agent:` lines; llms **31 entries** |
| Footer map | **0 iframes on all 7 location pages**; 2 on home + contact; 1 on the other 25 routes |
| Images | **0 `<img>`** in out/ (68 files); **0 `og:image`** |
| Links (own census, fixed resolver, all 68 files, 7,653 hrefs) | **0 broken local targets**; **0 self-links in `<main>`**; **0 missing fragment targets**; single tel: `tel:+12393563708`; externals only the canonical self-domain URLs + `msc.fema.gov` + the Google Maps pin URL. **51 self-links in header/footer chrome — see D-V2.** (My first census script undercounted these: it resolved `/slug/` to the directory itself instead of the file. The fixed resolver + the browser probe agree on 51.) |
| Header / nav / hero / menu (regression) | Header **80px**; Services/Areas summaries **1 line** (55px); menu Call button **698–754, 24px gap** above the call bar (panel scrolled to bottom, panel bottom 778 = bar top); home hero **x=0, w=1440, h=683**; table fade `rgba(10,46,56,0.28) -24px 0 16px -16px inset` present; mobile CTA top worst case **427px** (insurance) on 11/11 sampled page classes — identical to the 10x verifier's numbers; menu labels `#a9c3c9` on `#0a2e38` = **7.76:1** (my own luminance calc); footer links min **44.1px** desktop + mobile; CSS minified **15,596 B, 0 newlines, 0 comments**, guards present (`calc(100dvh - 80px - 66px)`, `\25BE`, prices nowrap only inside `@media (min-width:621px)`) |

### Speed — Lighthouse (local out/ on :8145, Lighthouse 13.6.0, bundled Chromium)

| Run | Perf | FCP | SI | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| Mobile home m1 | 88 | 1.4 s | 4.1 s | 1.4 s | 390 ms | 0 |
| Mobile home m2 | 70 | 1.4 s | 4.5 s | 1.4 s | 1,680 ms | 0 |
| Mobile home m3 | 76 | 1.5 s | 4.3 s | 1.5 s | 940 ms | 0 |
| **Mobile median-of-3** | **76** | **1.4 s** | **4.3 s** | **1.4 s** | **940 ms** | **0** |
| Desktop home d1 | 100 | 0.4 s | 0.5 s | 0.4 s | 0 ms | 0 |

The mobile median (76) is below the builder's 95 and the 10x verifier's 93 —
**not a regression and not a defect.** FCP/SI/LCP/CLS match the builder's
numbers; the entire Perf gap is TBT, and the TBT is Style & Layout long
tasks under 4× CPU throttle on a loaded VM (m2: Style & Layout 2,802 ms,
"Other" 1,305 ms, Script Evaluation **35 ms**; the 20x JS additions are a
click handler + a toggle handler, scripting 14–32 ms across runs). Desktop
100 holds with TBT 0. Reports:
`qa/screenshots/20x-verify/lighthouse/home-m{1,2,3}.json`, `home-d1.json`.

---

## 3. Defect list

### D-V2 (P3) — D3 incomplete: self-linking nav items remain sitewide + closed header shows no current section
**Scope:** header/footer chrome, all 28 inner pages (51 occurrences in the
flat route files; twins inherit the same markup).

Measured on `/water-removal/` (browser + static census agree):
- Mobile-menu panel: `<a href="/water-removal/" aria-current="page">` —
  white 14% bg, 700, 4px gold left border. Distinctly styled, but still a
  **link to the current page inside the header**.
- Footer Services column: `<a href="/water-removal/" aria-current="page">` —
  white, 700, gold underline, visible. A **link to the current page inside
  the footer**.
- Count by page: service/area pages 2 each (mobile menu + footer);
  `/cost/` and `/contact/` 3 each (mobile menu + footer + the top-level
  direct `<a aria-current>`); guide/legal pages 1 each (footer only).
  Home is the only page with 0 (its brand link `href="/"` was excluded
  from the count by the census's root-link rule; the brand itself is
  `aria-current="page"` on home).

Only the desktop dropdown was converted to a span. The builder's own note
says "header self-links were never counted as defects, only `<main>` ones
are" — but this round's D3 brief explicitly ordered "NO self-linking nav
item remains anywhere in header/footer", so as specified this is
incomplete. (Tension noted for the parent: the project's standing rule
exempts header/footer from the no-self-link rule; the D3 brief and this
verification task demand zero. The items are all `aria-current="page"`,
distinctly styled, and standard accessible practice — no visitor or
crawler harm, hence P3, not P2.)

**Second half of the same defect:** the closed header shows no current
section on the 27 dropdown pages. The builder claimed "top-level nav
current link (gold 22% bg + 3px gold underline)" — that CSS rule
(`.site-nav > a[aria-current="page"]`) only matches direct `<a>` children,
i.e. Cost/Contact (verified working on /cost/: gold 22% bg + inset 0 −3px
gold). On a service/area page the "Services ▾"/"Areas ▾" summary measures
bg transparent, decoration none, weight 600 — nothing marks it. A visitor
on `/water-removal/` sees no indication in the closed header of which
section they are in until they open the dropdown.

**Fix:** convert the remaining current items (mobile-menu panel, footer
columns, Cost/Contact top-level links) to non-link spans on the current
page, same `.nav-current` pattern as the dropdown; and give the
Services/Areas summary a current-section marker (e.g. `aria-current` on
the parent + the gold treatment) when the current page sits in that
dropdown. Re-verify on /water-removal/, /cost/, /cape-coral/ and /about/.

### D-V3 (P3) — D2 incomplete: skip-link activation does not move DOM focus to `<main>`
**Pages:** all 34. **Cause:** `<main id="main">` has no `tabindex`
(verified: `tabindex: None`).

Real Tab → link focused + visible ✓; Enter → viewport jumps to main
(scrollY 80) ✓; the next Tab lands on the first link inside main (hero
tel link) ✓ — so the keyboard flow works in Chrome, which sets the
sequential-focus starting point at the fragment target. But
`document.activeElement` after Enter is **BODY (`#top`)**, not MAIN, so
the task's literal requirement ("moves focus to main") is not met, and
AT/browser combinations that rely on actual DOM focus will not follow.
**Fix:** add `tabindex="-1"` to `<main>`, then re-run the Tab → Enter →
`activeElement === MAIN` check on desktop + mobile.

---

## 4. Observations (not defects)

- **Mobile Lighthouse median 76 vs builder 95** — TBT-driven host-CPU
  noise (see §2); script evaluation ~35 ms, desktop 100, all other
  metrics match. No action.
- **`404.html` lacks `og:url`** (5/6 og tags). It is outside the 34-route
  scope and non-indexed; noted, not counted.
- **Back-to-top 2px box overlap** vs the call bar's top edge (link bottom
  780 vs bar top 778) — visually nothing is covered; the link is fully
  legible and tappable. Not counted.
- **M1 section maps (home + contact) deliberately have no fallback
  link** — the word-diff 0 rule forbids visible text inside `<main>`.
  Both pages carry a footer map with the link. Accepted as designed.
- **E1/D5 were hardenings of already-correct states** (OG complete
  before; FAQ links already underlined by UA default) — verified as
  claimed, no visual change.

## 5. Standing / not re-verified (unchanged)

- Live site is still the OLD pre-10x build
  (`fort-myers-water-damage-php.pages.dev`); nothing here was pushed or
  deployed. Live map tiles still need one real-browser look.
- Live Speed Index still unmeasured from this VM (PageSpeed 429, per the
  speed audit).

## 6. Evidence

- Probes: `qa/probe_20x_verify.py`, `qa/probe_20x_verify2.py`,
  `qa/probe_20x_verify3.py`, `qa/probe_20x_fontpixel.py`
- Measurements: `qa/screenshots/20x-verify/measurements{,2,3}.json`
- Screenshots: `qa/screenshots/20x-verify/` (01 hero desktop, 12 hero
  mobile, 02 skip-link focused desktop+mobile, 03 dropdown active,
  13/13b/13c mobile menu open + scrolled + bottom, 15 footer mobile,
  06 footer desktop, 05 FAQ open desktop+mobile, 11 home table mobile,
  20/20b/21 cost tables mobile, 22 cost desktop,
  `fontpixel/` subset-vs-full shots, `lighthouse/` JSON reports)
- This file: `qa/FINDINGS-20x-verify.md`
