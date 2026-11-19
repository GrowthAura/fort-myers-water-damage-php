# FINDINGS — Fort Myers NEW PHP site, 20X round, FINAL INDEPENDENT VERIFICATION
## `~/workspace/fort-myers-php/` — 2026-11-19, final verifier (fresh eyes; did not build or fix)

**Method:** re-exported first (`python3 qa/export_cloudflare.py out` — after
installing `rcssmin` 1.3.0 with `pip install --break-system-packages rcssmin`;
plain `pip install` is blocked by PEP 668 in this VM), then measured
everything myself with new probes (`qa/probe_20x_final_verify.py`,
`qa/probe_20x_final_followup.py`, `qa/probe_20x_final_fontpixel.py`; served
`out/` on 127.0.0.1:8150/8152/8153 and `site/` via the PHP router on
127.0.0.1:8151, Playwright bundled Chromium only, no `executable_path`).
Every screenshot below was viewed at full size. No `site/` source file was
edited; no push, no deploy, no MEMORY.md edit. All temp servers stopped by
PID/Popen handle; scratch copy `/tmp/out-fullfont-final` removed.

**Verdict: READY — 0 defects.** D-V2, D-V3, the 404 og:url note and the hero
underline order are all fixed exactly as specified, D-V1 stays fixed, and
the full regression suite is clean. The two prior P3s are closed.

---

## 1. Per-item verdicts (all measurements mine)

| # | Item | Verdict | My measurement |
|---|---|---|---|
| D-V2 | 0 self-linking nav items anywhere | **PASS** | Static census, own resolver, all 34 flat route files (+ twins spot-checked via the same chrome split): **self-links in nav chrome 0, in `<main>` 0** — the fix worker's 53 → 0 reproduces exactly (their count included brand + mobile Home on home, which the previous verifier's census had excluded). Non-link spans total **71** across the 34 routes (19 dropdown + 22 mobile + 28 footer + 2 top-level), per-route: home 1, 19 dropdown pages 3 each, `/cost/` + `/contact/` 3, guide/legal/about pages 1, `/cast-iron-pipe/` + `/appliance-leak/` + `/floors/` + `/cabinets/` 0 — those four sit in no dropdown and carry no footer current item either; verified by hand that their footer columns list no self-target. Brand self-link on home: 0. Mobile-menu "Home" self-link on home: 0. |
| D-V2b | Closed Services/Areas section marker | **PASS** | Computed style, desktop: `/water-removal/` → Services `nav-section-current`, `aria-current="true"`, bg `rgba(201,155,63,0.22)`, box-shadow gold inset 0 −3px; Areas plain. `/cape-coral/` → Areas marked identically; Services plain. `/about/` → no marker anywhere. `/cost/` → Cost is `span.nav-current-top` ("Cost"), no section marker. Viewed `marker-water-removal.png`: "Services ▾" shows the gold bg + gold underline in the closed header. |
| D-V3 | Skip link moves DOM focus to `<main>` | **PASS** | Real keyboard test, desktop AND mobile 390px: Tab → skip link focused ("Skip to main content", 238×58 at (12,12)); Enter → **`document.activeElement` = `MAIN#main`**, scrollY 80; next Tab → first link inside main (hero tel `239-356-3708`). `<main tabindex="-1">` on **34/34 routes + 404**. |
| 404 | og:url = requested URL, HTTP 404, no canonical | **PASS** | Live PHP router (not the static file), two bogus paths: both **HTTP 404**, `og:url` = the requested URL exactly (`…/this-page-does-not-exist-404/` and `…/definitely-not-a-page-xyz/`), **6/6 og tags + 3/3 twitter tags**, **0 canonical links**, `main tabindex="-1"`, title "Page Not Found \| Fort Myers Water Damage Restoration Pros". Static `out/404.html` agrees (6/6 + 3/3, canonical 0). |
| HERO | No underline under hero number, 13 pages | **PASS** | Own intro-only census (`.hero-intro a[href^="tel:"]`, CTA buttons excluded): exactly **13 pages** — home, water-removal, drying, sewage-cleanup, ac-leak, ceiling-leak, condo-leak, cast-iron-pipe, vacant-home, first-hour-checklist, contact, privacy-policy, about — matching the builder's list. Computed style on all 13, desktop + mobile: `text-decoration: none`, color `rgb(255,217,168)` = **#ffd9a8**, 22px desktop / 20px mobile. Contrast #ffd9a8: **10.78:1 vs #0a2e38, 12.64:1 vs #062028** (own luminance calc, matches the fix worker). Viewed all 13 desktop + 13 mobile shots; home desktop + mobile + water-removal viewed at full size: number clean, same gold, reads clearly. |
| HERO-ctrl | Body links elsewhere keep underlines | **PASS** | Plain prose tel links in `<main>` are `underline` on home, water-removal, cost, about (incl. FAQ answers); footer "Back to top" `underline`. The only non-underlined tel links outside the hero are `.btn.btn-call` CTAs — buttons, which never had underlines (pre-existing, not part of this fix). |
| D-V1 | /cost/ mobile prices still visible | **PASS** | 390px: tables **390/390/390px**, price cols **114/129/200px**, `white-space: normal` on mobile, `documentElement.scrollWidth` 390. tbody row heights byte-identical to the pre-round state: **222/194/166, 83/83/111, 83/83/83**. Viewed `cost-table1-mobile-scrolled.png`: all 3 columns + wrapped right-aligned prices ("From about $500", "About $1,200 to $3,500", "About $3,500 to $8,000"). Desktop unchanged: tables 1190px, `nowrap`, rows 60/90/90, 60/60/60, 60/60/60 (first value is the thead row). |
| R1 | Header 80px; nav carets single-line | **PASS** | Header **80px** desktop; Services/Areas summaries **55px, 1 line** each. |
| R2 | Menu Call button clears call bar | **PASS** | Mobile menu open (details open, panel [0,80,390×698], bottom **778** = call-bar top). Panel scrolled to bottom: Call button **[24,698,342×56, bottom 754]**, **24px gap** above the call bar (778) — byte-identical to the 20x verifier's numbers. Viewed `menu-open-mobile-bottom.png`: button fully visible, clear of the orange bar. (My first probe read [0,0,0] — it had matched the hidden desktop `.header-call`, `display:none`; the follow-up probe isolates the panel button.) |
| R3 | Home hero full-bleed | **PASS** | Hero x=0, w=1440, **h=683** — unchanged. |
| R4 | Table fade | **PASS** | `.table-wrap` box-shadow `rgba(10,46,56,0.28) -24px 0 16px -16px inset` present (same mechanism the 20x verifier measured; mask none). |
| R5 | Mobile CTA ≤ ~430px | **PASS** | Worst case **427px** (insurance) across home / cost / insurance / water-removal / contact; home 304, cost 382, water-removal 337, contact 382. |
| R6 | Menu labels ≥ 4.5:1 | **PASS** | Panel links white `rgb(255,255,255)` on `#0a2e38` = **14.38:1** (own luminance calc); summary "Menu"/"×Close" same pair. |
| R7 | Footer links ≥ 44px | **PASS** | Min footer-link height **44.09px** desktop (32 links) and mobile (31 links). |
| R8 | Skip link present; back-to-top works; FAQ opens by real click | **PASS** | Skip link present, text exactly "Skip to main content", href `#main`. Back-to-top real click: scrollY 20,847 → **0**. FAQ real click: closed → **open=true, 186px** desktop. |
| R9 | Inter + Archivo subsets intact, 0 px diff | **PASS** | Archivo **18,084 B** (full 18,604 B, md5 `4b6914a6…` matches the 20x record), Inter **40,656 B** (full 48,256 B). Own pixel proof, home full page 1440px, subset vs full fonts (scratch export, both fonts swapped): **0 differing pixels** (31,315,680 total). |
| R10 | CSS minified | **PASS** | Export minified **25,102 → 15,868 B** (`rcssmin` installed this run; the fix worker's unminified export is superseded). File has 1 newline; `calc(100dvh - 80px - 66px)` and `\25BE` guards present. The +272 B vs the 20x verifier's 15,596 B is the fix-round rules (span/section-marker/hero rules) — expected. |
| R11 | fetchpriority ×2; robots 20 crawlers; llms-full 31 pages; 54 "View larger map" | **PASS** | `fetchpriority="high"` exactly **2** on all **68** HTML files. robots.txt **22 `User-agent:` lines** (20 named AI allowed + `*` + Bytespider `Disallow: /` + Sitemap). `llms-full.txt` **419,280 B, 31 `##` pages**. "View larger map" **54 occurrences** (27 footer-map pages × 2 twins). |

---

## 2. Full regression suite (my own runs, fresh export)

| Check | Result |
|---|---|
| `python3 qa/verify_export.py` | **FAILURES 0 / NOTES 0** (word-diff 0 all 34 pages) |
| `python3 qa/validate_schema.py` | **pages 34 \| scripts 92 \| nodes 92 \| ERRORS 0 \| WARNINGS 0** (+ 6 by-design NOTES, unchanged: 3× Article `image`, 3× publisher `logo`) |
| `python3 qa/render_check.py` | **34/34 overflow 0** at 320/360/390/1440; body font **20px** at 390 + 1440 on all routes (full log: `qa/screenshots/20x-final-verify/render_check.log`) |
| Dash sweep (literal – — + entities `&ndash;`/`&mdash;`/`&#8211;`/`&#8212;`) | **0 files** (68 HTML files) |
| Sitemap / robots / llms | **31 locs**; robots 22 `User-agent:` lines; llms **31 entries**; llms-full.txt 31 pages, 419,280 B |
| Footer map | **0 iframes on all 7 location pages** (areas, cape-coral, fort-myers-beach, estero, bonita-springs, lehigh-acres, north-fort-myers); 2 on home + contact; 1 on the other 25 routes |
| Images | **0 `<img>`** in out/ (68 files); **0 `og:image`** |
| Links census (own, fixed resolver, all 34 routes) | **0 broken local targets**; **0 self-links in `<main>`**; **0 self-links in nav chrome**; **0 missing fragment targets**; single tel: `tel:+12393563708`; externals only `msc.fema.gov` + `www.google.com` (maps pin) besides the self-domain canonicals |
| OG/Twitter census (34 routes + 404) | All 6 og: + 3 twitter: tags on **34/34** routes and on the 404; `og:image` on **0** |

### Speed — Lighthouse (local out/ on :8155, Lighthouse 13.6.0, Playwright bundled Chromium 153 via `--port=9222`)

Note: `npx lighthouse` on its own cannot find Chrome in this VM
(`CHROME_PATH` unset, and chrome-launcher's own launch hangs at "Waiting
for browser"); the working path is launching the bundled Chromium with
`--remote-debugging-port=9222` and passing `--port=9222` to Lighthouse.

| Run | Perf | FCP | SI | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| Mobile home m1 | 88 | 1.1 s | 1.4 s | 1.1 s | 480 ms | 0 |
| Mobile home m2 | 88 | 1.1 s | 1.3 s | 1.1 s | 470 ms | 0 |
| Mobile home m3 | 92 | 1.1 s | 1.2 s | 1.1 s | 340 ms | 0 |
| **Mobile median-of-3** | **88** | **1.1 s** | **1.3 s** | **1.1 s** | **470 ms** | **0** |
| Desktop home d1 | 100 | 0.3 s | 0.4 s | 0.3 s | 0 ms | 0 |

The mobile median (88) sits between the builder's 95 and the 20x verifier's
76 — **not a regression and not a defect.** FCP/SI/LCP are the best of the
three rounds (SI 1.2–1.4 s vs 3.9–4.5 s before); the entire Perf gap is TBT
under 4× CPU throttle on a loaded VM, and TBT varies run to run (340–480 ms
here). Desktop 100 holds with TBT 0. Reports:
`qa/screenshots/20x-final-verify/lighthouse/home-m{1,2,3}.json`, `home-d1.json`.

---

## 3. Defect list

**None.** D-V2, D-V3, the 404 og:url note and the hero underline order are
all fixed as specified; D-V1 stays fixed; every 20x regression item
re-measures clean. No new defect was found in any check.

## 4. Observations (not defects)

- **Four pages carry 0 `nav-current` spans** (`/cast-iron-pipe/`,
  `/appliance-leak/`, `/floors/`, `/cabinets/`): they sit in no dropdown and
  their footer columns list no self-target, so there is nothing to mark.
  Correct as built, not a gap.
- **`/cost/` mobile price cells sit below the fold** (first price cell top
  4,553px at load): "prices visible at first paint" in the D-V1 sense means
  visible without horizontal scrolling once scrolled to the table — verified
  by the scrolled screenshot, not by the load viewport.
- **Lighthouse needs the `--port=9222` workaround in this VM** (see §2) —
  worth keeping in the QA notes for the next round.

## 5. Standing / not re-verified (unchanged)

- No push / deploy done — verification only, by others after this.
- Live site is still the OLD pre-10x build
  (`fort-myers-water-damage-php.pages.dev`); nothing here was pushed.
- Live map tiles still need one real-browser look (VM Chromium cannot
  reach google.com/maps).
- `rcssmin` 1.3.0 was installed in this VM with `--break-system-packages`
  (plain `pip install` is PEP 668-blocked here); a fresh VM will need the
  same install before the next export ships minified CSS.

## 6. Evidence

- Probes: `qa/probe_20x_final_verify.py`, `qa/probe_20x_final_followup.py`,
  `qa/probe_20x_final_fontpixel.py`
- Measurements: `qa/screenshots/20x-final-verify/static.json`,
  `measurements-final.json`, `measurements-followup.json`,
  `render_check.log`
- Screenshots: `qa/screenshots/20x-final-verify/` — hero desktop + mobile
  for all 13 intro pages (26 shots), `marker-{water-removal,cape-coral,
  about,cost}.png`, `skiplink-{desktop,mobile}.png`,
  `menu-open-mobile.png`, `menu-open-mobile-bottom.png`,
  `cost-table{1,3}-mobile-scrolled.png`, `cost-mobile.png`,
  `faq-open-desktop.png`, `fontpixel/home-{subset,full}.png`,
  `lighthouse/home-m{1,2,3}.json` + `home-d1.json`
- This file: `qa/FINDINGS-20x-final-verify.md`
