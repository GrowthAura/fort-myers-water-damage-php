# FINDINGS — Fort Myers NEW PHP site, 10X round, INDEPENDENT VERIFICATION
## `~/workspace/fort-myers-php/` — 2026-11-19, verifier (fresh eyes; did not build)

**Method:** re-exported first (`python3 qa/export_cloudflare.py out` — reproduced
builder exactly: CSS 20,235 chars → 13,523 B minified, font 40,656 B), then measured
everything myself with a new probe (`qa/probe_10x_verify.py`, served `out/` on
127.0.0.1:8140, Playwright bundled Chromium only, no `executable_path`). Every
screenshot below was viewed at full size. No `site/` source file was edited;
no push, no deploy, no MEMORY.md edit. Temp servers stopped by PID; scratch
copy `/tmp/out-fontfull` removed.

**Verdict: NOT READY — 1 defect (P2).** 11 of 12 claims verify exactly as
stated, most to the pixel. The single defect is the cost-price nowrap on
mobile: on the money page, two of the three price tables now hide their
entire price column off-screen at first paint on a 390px phone. Ruling in §4:
**DESKTOP-ONLY nowrap** — the coordinator should apply it, re-export, and
re-verify just the cost page on mobile; everything else is ready to ship.

---

## 1. Per-claim verdicts (all measurements mine)

| # | Claim | Verdict | My measurement |
|---|---|---|---|
| 1 | Nav carets: header exactly 80px desktop, "Services ▾"/"Areas ▾" single-line on all pages | **PASS** | Header **80.0px** on home + 6 spot-checked pages (cost, insurance, cape-coral, HIW, contact, about). Summaries 54.6px tall, **1 line each** everywhere (`getClientRects().length == 1`). Screenshot `01-nav-desktop.png` viewed: carets inline, header slim. |
| 2 | Mobile menu vs call bar: menu Call button fully visible/tappable above the fixed call bar | **PASS** | Panel bottom **778** = call-bar top (max-height 698px). Scrolled to bottom, menu Call button 698–**754**, i.e. **24px gap** above the bar — fully visible + tappable. Viewed `12b-menu-open-scrolled-bottom.png`: button clear of the bar. |
| 3 | Homepage hero full-bleed: x=0, w=1440 desktop; word-diff 0 | **PASS** | Hero **x=0, y=80, w=1440, h=683**, parent is `<main>` (direct child). Viewed `02-home-hero-desktop.png`: full-bleed, same words as builder's before shot. Word-diff 0 on all 34 pages (verify_export, §2). |
| 4 | Table scroll cue: visible right-edge fade on `.table-wrap` at mobile | **PASS** | Computed `box-shadow: rgba(10,46,56,0.28) -24px 0 16px -16px inset`, `hasFade: true`. Viewed `11-home-table-mobile.png`: fade clearly visible on the right edge; 4th column hidden but cued. |
| 5 | Mobile hero CTA-first: Call button top ≤ ~430px first viewport, all page classes at 390px; desktop hero unchanged | **PASS** | Call-button top (viewport 844): home **304**, cost 382, insurance **427**, cape 292, contact 382, water 337, HIW 382, about 382, areas 292, privacy 203, estero 292 — worst case 427 ≤ ~430 on 11/11 sampled classes. Viewed `1home-`/`1cost-hero-mobile-firstviewport.png`: Call button in view, intro below it. Desktop hero untouched: inner padding still **64px**, heroes x=0/w=1440 (536–671px tall, matching pre-round geometry). |
| 6 | Menu labels contrast ≥ 4.5:1 | **PASS** | Measured from computed styles: `#a9c3c9` on `#0a2e38` = **7.76:1** (my own luminance calc, not the builder's number). Viewed: "SERVICES"/"AREAS" legible in `12-menu-open-mobile.png`. |
| 7 | Footer links ≥ 44px tall | **PASS** | Column links **44.1px**, phone text link **44.9px**, footer-base link **44.9px** — desktop AND mobile (390px), identical. Footer Call button 60px. |
| 8 | Cost prices single-line + right-aligned desktop; tel: nowrap; HIW phone 1 line | **PASS (desktop) / FAIL (mobile) — see §4** | Desktop: exactly **3/7** tables carry `prices` (the other 4 prose-last-column tables untouched, `white-space: normal`); price cells **1 line, `text-align: right`, `white-space: nowrap`**, row heights unchanged (89.9/89.9/60.4px). HIW step-1 phone: **24px, 1 line, nowrap** at 390px. Mobile cost tables are the defect (§4). |
| 9 | Menu toggle Close state live | **PASS** | Real clicks: closed **"☰Menu"** → open **"×Close"** (icon `×`, aria-label "Close menu") → toggle-click re-close **"☰Menu"** → open + Escape **"☰Menu"**, menu closed. All paths reset the label. |
| 10 | Location-page footer void rebalanced, CSS only, no new footer links | **PASS** | Cape Coral: grid 10248–10963, brand 10436–10783 — top gap **188px**, bottom gap **180px** (balanced, matches builder). Viewed `05-footer-cape-desktop.png`: brand centred in its column. No new hrefs: `site/includes/footer.php` is **unchanged vs the fix-round commit** (`git diff` empty) and the `functions.php` diff adds no hrefs; footer href list identical (30 hrefs) on home and cape-coral. |
| 11 | Font subset safe: Inter 40,656 B; no used char lost; no pixel differences vs full font | **PASS** | Subset **40,656 B** (was 48,256 B, −15.7%), cmap 225 vs full 230 glyphs. The 5 lost glyphs are combining diacritics (U+0300, U+0301, U+0303, U+0309, U+0323) — **0 used chars lost** (all 95 distinct chars in out/ HTML+CSS+JS checked against both cmaps; only `\n` is in neither font, i.e. pre-existing system fallback for ▾/☎/☰ as the builder stated). fvar wght 100–900 + gvar retained. Pixel proof (my own scratch export with the full font): full-page home/cost/insurance — **0 differing pixels** (31,224,960 / 25,508,160 / 22,664,160). |
| 12 | CSS minify: minified in out/, calc() + caret intact, no visual regression | **PASS** | Minified **13,523 B, 0 newlines, 0 comments**, 204 rule blocks. Guards present: `calc(100dvh - 80px - 66px)`, `\25BE` caret, `.table-wrap.prices td:last-child{text-align:right;white-space:nowrap}`, `a[href^="tel:"]:not(.btn){white-space:nowrap}`, inset fade, `.footer-brand{align-self:center}`. Pixel comparison of my screenshots vs the builder's after-shots: **0 differing pixels** on nav, home hero, cost viewport, mobile footer (the menu-open pair differs only because the builder's file is the scrolled-to-bottom state — it is byte-identical to my scrolled shot, same sha256). |

---

## 2. Full regression suite (my own runs, fresh export)

| Check | Result |
|---|---|
| `python3 qa/verify_export.py` | **FAILURES 0 / NOTES 0** (word-diff 0 all 34 pages; H1/title/meta/canonical/schema OK) |
| `python3 qa/validate_schema.py` | **pages 34 \| scripts 92 \| nodes 92 \| ERRORS 0 \| WARNINGS 0** (+ 6 by-design NOTES, unchanged: 3× Article `image`, 3× publisher `logo`) |
| `python3 qa/render_check.py` | **34/34 overflow 0** at 320/360/390/1440; body font **20px** at 390 + 1440 |
| Own overflow sweep (all 34 routes × 320/360/390/1440, own probe) | **0 bad** at every width; body font 20px everywhere |
| Dash sweep (literal – — + entities `&ndash;`/`&mdash;`/`&#8211;`/`&#8212;`) | **0 files** (68 HTML files) |
| Sitemap / robots / llms | **31 locs**; robots 17 `User-agent:` lines (15 AI allowed + `*` + Bytespider disallow + Sitemap line); llms **31 URL entries** (= sitemap locs) |
| Footer map | **0 iframes on all 7 location pages** (areas, cape-coral, fort-myers-beach, estero, bonita-springs, lehigh-acres, north-fort-myers); 2 on home |
| Images | **0 `<img>`** in out/ (68 files) |
| Links (own census, 34 flat route files, 3,817 hrefs) | **0 broken local targets** (asset refs included — favicon, fonts, CSS all resolve); **0 self-links in `<main>`**; **0 missing fragment targets**; single tel: `tel:+12393563708`; externals only the canonical self-domain + `msc.fema.gov` |
| FAQ open state (real click, mobile home) | **open: true**, item 393px, 5px gold left border, shadow — viewed `18-faq-open-mobile.png`: clean, coral − badge, answer fully visible |

### Speed — Lighthouse (local out/ on :8140, Lighthouse 13.6.0, bundled Chromium)

| Run | Perf | FCP | SI | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| Mobile home m1 | 97 | 1.8 s | 3.9 s | 1.8 s | 0 ms | 0 |
| Mobile home m2 | 93 | 1.4 s | 3.9 s | 1.4 s | 270 ms | 0 |
| Mobile home m3 | 91 | 1.4 s | 4.0 s | 1.4 s | 320 ms | 0 |
| **Mobile median-of-3** | **93** | **1.4 s** | **3.9 s** | **1.4 s** | **270 ms** | **0** |
| Desktop home d1 | 100 | 0.4 s | 0.6 s | 0.4 s | 0 ms | 0 |

Builder reported mobile median 96 (96/96/99). Mine is 93 — **not a regression
and not a defect**: FCP/SI/LCP/CLS match the builder's numbers exactly; the
gap is TBT (0/270/320 ms vs builder's 170/160/10 ms), which the speed audit
proved is host-CPU noise under 4× throttle (mobile Perf spans 78–98 on
byte-identical pages). Desktop 100 holds. Reports:
`qa/screenshots/10x-verify/lighthouse/home-m{1,2,3}.json`, `home-d1.json`.

---

## 3. Defect list

### D-V1 (P2) — Mobile cost tables: price column pushed entirely off-screen
**Pages:** `/cost/` (mobile ≤ 620px). **Cause:** the ordered `white-space:
nowrap` on `.table-wrap.prices td:last-child`, applied at all widths.

Measured (my probe, 390px viewport, all three prices tables):

| Table | Table width in 390px wrap | Price col width | First-paint state |
|---|---|---|---|
| 1 — "Size of the job" / "Rough area range" | **550px** | 324px | Prices invisible; prose cols squeezed to ~110px; rows 222→**362** / 194→306 / 166→278px (builder's figure confirmed) |
| 2 — "What is being priced" / "Rough area range per sq ft" | 390px (fits) | 181px | OK — fits, rows 83–111px |
| 3 — "Repair after water damage" / "Rough area range" | **616px — worse than the 550px the builder flagged** | **480px** | Prices **entirely invisible**; only a sliver of "A…" shows at the right edge |

The 616px table is driven by one long value forced onto a single line:
"From about $500 for a small area to $10,000 or more" → **480px** wide
(plus "Priced per linear foot and per room", a prose value in the price
column, also forced nowrap). Viewed `14-cost-table-mobile.png` (table 1) and
`14b-cost-table3-mobile.png` (table 3): at first paint the visitor sees a
list of repair names with **no prices at all** — the whole point of the page
— until a horizontal swipe. The fade cue (claim 4) is present and visible,
but a cue to swipe for the page's core content is not the same as showing it.

**Before/after (builder's own shots, viewed):** before, all three columns
were visible at first paint with prices wrapped but readable ("From about
$500", "About $1,200 to $3,500"), rows ~222px. After, the prices are gone
from first paint and rows nearly double. Desktop is perfect and must not
change. This is a regression against the pre-round state on the money page,
on mobile — the viewport that matters most for this audience.

---

## 4. RULING — cost-price nowrap: DESKTOP-ONLY nowrap

**Firm ruling: apply the nowrap (and the right-alignment, which is harmless
either way) only above 620px; below 620px let prices wrap as before.**

Reasoning:
1. **The mobile cost is not a cosmetic trade-off, it is the content
   disappearing.** Two of three price tables show zero prices at first paint
   on a phone. The /cost/ page exists to answer "how much?" — a visitor who
   has to discover a horizontal swipe to see any number is a visitor who may
   bounce to a competitor whose prices are on screen. The fade cue does not
   fix this: it signals "more table", not "the prices are over there".
2. **The desktop gain is fully preserved.** Desktop is where the scan-as-a-
   column benefit actually exists (1192px tables, prices aligned right in one
   clean column, zero height change). Nothing about desktop needs the mobile
   behaviour.
3. **The mobile "loss" from wrapping is the pre-round state, which was
   already good.** Before, prices wrapped to two lines and were readable at
   first paint with rows ~222px. That was not a defect anyone flagged — the
   audit's D-12 was a desktop-only complaint ("price column left-aligned and
   wrapping" on a 1440px screenshot). The nowrap was specified for the
   desktop problem; extending it to mobile created a new mobile problem.
4. **The 616px table proves the rule is not safely scoped.** The class is
   applied by last-header text, but table 3's last column is not purely
   prices (one prose value, one 51-character range). A blanket nowrap at all
   widths lets the longest string dictate the table width (480px column).
   Scoping nowrap to desktop bounds that failure mode to a viewport where
   the table has room.
5. **Cost of the fix is one CSS rule + re-export + a mobile-only re-check.**
   No words change, no markup change, no desktop re-verification needed
   beyond confirming the desktop numbers are untouched.

**Exact change for the coordinator:** move `white-space: nowrap` for
`.table-wrap.prices td:last-child` inside the existing desktop media query
(above 620px; the site's breakpoint is 620px per the menu/call-bar rules).
Keep `text-align: right` everywhere or scope it with the nowrap — either is
fine on mobile, since right-aligned wrapped prices still read. Re-export,
re-run render_check + verify_export, and re-measure /cost/ at 390px: table
widths must be ≤ 390px and first-paint must show prices again (expect the
pre-round ~222px first rows). Then this round is READY.

---

## 5. Standing / not re-verified (unchanged)

- Live site is still the OLD pre-fix build (`fort-myers-water-damage-php.pages.dev`);
  nothing here was pushed or deployed. Live map tiles still need one real-browser look.
- Live Speed Index still unmeasured from this VM (PageSpeed 429, per the speed audit).
- D-01 (780px line cap), D-05 (breadcrumb above hero), D-06 (stacked CTAs), D-10
  (hero glow) were not in this round's adjudicated list and were correctly not done;
  D-06 re-confirmed as inspected and left as-is by the builder.

## 6. Evidence

- Probe + measurements: `qa/probe_10x_verify.py`,
  `qa/screenshots/10x-verify/measurements.json`
- Screenshots: `qa/screenshots/10x-verify/` (01 nav, 02 home hero, 03/04 cost
  desktop, 05 cape footer, 11 home table mobile, 12/12b menu open + scrolled,
  14/14b cost tables mobile, 15 HIW steps, 16 footer mobile, 18 FAQ open mobile,
  1home/1cost hero mobile first viewport, `lighthouse/` JSON reports)
- This file: `qa/FINDINGS-10x-verify.md`
