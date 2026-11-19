# AUDIT — Fort Myers NEW PHP site, 10X DESIGN/UX round (read-only)
## `~/workspace/fort-myers-php/` — 2026-11-19

**Scope:** visual audit only. No file in `site/`, `out/`, or any source was edited.
Local static export served with `python3 -m http.server` on port 8123
(PHP is not installed on this VM; no re-export). Playwright **bundled**
Chromium only (`pw.chromium.launch()`, no `executable_path`).
Live site also reachable by curl; screenshots are of the local export, which
is byte-identical to live (per FINDINGS-fixround-php.md).

**Pages viewed (9):** `/`, `/water-removal/`, `/cape-coral/`, `/cost/`,
`/insurance/`, `/how-it-works/`, `/contact/`, `/about/`,
`/privacy-policy/` — each at **1440 desktop** and **390 mobile**,
first-viewport **and** full-page, plus: FAQ open state (home + insurance,
desktop and mobile), mobile menu open, sticky header mid-page (insurance),
desktop Services/Areas dropdowns open, sticky bottom call bar at page bottom
(contact, mobile), element crops (details card, kinds grid, FAQ list,
footer, map sections, cost/HIW tables, steps), and a 320px overflow probe
(home, cost, how-it-works).

**Screens viewed: 63** (18 viewport + 18 full-page + 3 FAQ-open + 1 mobile
menu + 1 sticky header + 2 dropdowns + 16 element crops + 2 table
first-paint probes + 1 mobile footer viewport + 1 contact call-bar bottom).
All PNGs under
`qa/screenshots/10x-design/`; measurements in
`qa/screenshots/10x-design/measurements.json`.

**Counts: P1 = 3, P2 = 6, P3 = 5. Total 14 findings.**
**Zero page overflow** at 1440 / 390 / 320 on all 9 pages.
All contrast pairs pass WCAG AA (measured, §7).

**How to read severity:** judged against a best-ever bar, not pass/fail.
P1 = visibly below best-ever on a first look, or functionally obscures
content. P2 = a real weakness a careful visitor notices. P3 = polish.

---

## 1. Findings table

| # | Sev | Page(s) / viewport | What looks less than best-ever | Evidence | Concrete proposed fix (CSS-only where possible; no visible words change) |
|---|---|---|---|---|---|
| D-01 | P1 | All 9 pages / desktop 1440 | **Body line length 109–114 chars.** `.page-body > p` is capped at 1100px, so every desktop paragraph runs ~1.5× past the 50–75ch readability band. Worst rendered lines measured with the Range API (real lines, 20px body): home 113, water-removal 114, cape-coral 114, cost 114, insurance 114, HIW 110, contact 111, about 112, privacy 109. Long, tiring lines on the longest articles (insurance, cost). Mobile is fine (35–36ch). | `home-desktop-viewport.png`, `contact-desktop-viewport.png`, `cost-desktop-viewport.png` (see any body paragraph) | `.page-body > p, .page-body > ul, .page-body > ol { max-width: 780px; }` (≈75ch at 20px). Optionally apply the same cap to `.faq-item p` and `.steps p`, whose answers also run ~113ch. Compromise if the wide look must stay: 900px (≈88ch) — better, still long. Note: this site's brief says "wide lines", but 114ch is past readable even for a wide design. |
| D-02 | P1 | All pages / desktop 1440 | **Nav dropdown carets wrap onto their own line.** "Services ▾" and "Areas ▾" render as the label on one line with the small gold ▾ alone underneath (see every desktop viewport shot). The flexed nav summaries shrink below content width and wrap at the space before the `::after` caret. It also inflates the sticky header to 101px tall. | `home-desktop-viewport.png`, `cost-desktop-viewport.png`, `insurance-desktop-viewport.png`, `home-desktop-nav-services-open.png` | `.site-nav > a, .site-nav summary { white-space: nowrap; flex: none; }` Header drops back toward its 80px min-height. |
| D-03 | P1 | All pages / mobile 390 | **Sticky bottom call bar covers the bottom of the open mobile menu.** The menu panel (`z-index 120`) lives inside the header stacking context (`z-index 100`), so the fixed call bar (`z-index 110`) paints OVER the panel's bottom 66px. "Condo Water Damage" is half-hidden behind the bar, and the menu's own Call button (last item, panel bottom = viewport bottom) can never be seen or tapped while the menu is open. Panel is scrollable (23 links, last-link bottom 1595px), so the user can scroll — but the final items always land under the bar. | `home-mobile-menu-open.png` (call bar over "Condo Water Damage") | At ≤620px: `.mobile-menu-panel { max-height: calc(100dvh - 80px - 66px); }` (66px = call-bar height) so the panel ends above the bar. |
| D-04 | P2 | Homepage / desktop 1440 + mobile 390 | **Homepage hero is the only inset hero on the site.** On `/`, the hero sits inside `<div class="container page-body">`, so the teal panel floats with white gutters on all four sides plus a white band between the sticky header and the hero. The other 33 pages render the hero as a direct child of `<main>` — full-bleed, edge to edge. The most important page has the weakest hero presentation; at first paint it reads as a card, not a hero. | `home-desktop-viewport.png` vs `cost-desktop-viewport.png` / `insurance-desktop-viewport.png` (full-bleed) | Move the home hero out of `.container.page-body` (template change, same markup otherwise), or CSS-only full-bleed on the home hero: `.page-body > .hero { width: 100vw; margin-left: calc(50% - 50vw); }` plus pull up the 8px `.page-body` top padding for the hero. No words change. |
| D-05 | P2 | All 30 inner pages / desktop + mobile | **Breadcrumb sits BELOW the hero**, orphaned between the hero and the first content block ("Home » H1" on white, then the CTA, then body text). Convention — and the hierarchy the eye expects — is breadcrumb above the H1. Here the H1 is inside the hero, so the trail reads as disconnected from both. | `cost-desktop-viewport.png`, `cape-coral-desktop-viewport.png`, `how-it-works-desktop-viewport.png` (breadcrumb at y≈795, under the hero) | Move `<nav class="breadcrumb">` above `<section class="hero">` in the inner-page template (order change only, no words change). |
| D-06 | P2 | All inner pages / desktop + mobile | **Two near-identical coral Call buttons stacked ~90px apart.** Hero CTA ("Call 239-356-3708") then breadcrumb, then the top-of-body `.cta-line` CTA ("Call 239-356-3708, answered 24/7"). Reads as repetition and pushes real content down a viewport notch. Seen clearest on contact + cape-coral. | `contact-desktop-viewport.png`, `cape-coral-desktop-viewport.png` | Demote the top-of-body one without removing any words: give it `.btn-ghost-dark` (teal outline) instead of `.btn-call` — one class swap in the template, or a page-scoped CSS rule. Dropping it entirely is his call (it would remove visible words). |
| D-07 | P2 | Home, water-removal, cost / mobile 390 | **Mobile tables hide a whole column with zero cue.** `.table-wrap` scrolls horizontally, but there is no fade, shadow, or hint: home table is 529px wide — its 4th column "What usually happens" (136px) is entirely invisible at first paint; water-removal table 523px — 4th column "Read more" entirely hidden; cost 4-col table 432px — last column header clipped mid-word ("Effect on the pric…"). A visitor has no reason to swipe. (Other mobile tables fit at 390px.) | `home-mobile-table-firstpaint.png` (clean first-paint shot: 3 columns, 4th absent, right edge flush, no cue), `crop-cost-mobile-table-scrolled.png`, `crop-home-mobile-table.png`, `measurements.json` (`tableW` 529/523/432 vs wrap 390) | Add a scroll cue on `.table-wrap`: `box-shadow: inset -24px 0 16px -16px rgba(10,46,56,.28);` (right-edge fade that reads as "more to the right"). Optionally also tighten mobile cell padding (13px→11px) — not enough alone for 4-col tables. |
| D-08 | P2 | All 9 pages / mobile 390 | **Mobile hero is taller than the viewport, so the first viewport is H1 + intro only.** Measured hero heights: home 1195px (1.4 viewports), insurance 936, cost 827, about 763, water-removal 750, HIW 731, cape-coral 706, contact 699, privacy 584. The hero's own Call button sits at or behind the fixed call-bar line — the page itself offers no CTA and no content preview in the first viewport, just a wall of teal. | `home-mobile-viewport.png`, `cost-mobile-viewport.png` (intro runs past the fold, no button visible) | Tighten mobile hero: `.hero-inner { padding-top: 40px; padding-bottom: 40px; }` (from 56px) + `.hero-intro { line-height: 1.5; }` (from 1.6). Stronger option, CSS-only: CTA-first on mobile via flex order — `.hero-inner { display: flex; flex-direction: column; } .hero-ctas { order: -1; }` under 620px puts the buttons directly under the H1, intro below. No words change either way. |
| D-09 | P2 | All pages / mobile 390 (menu open) | **Mobile menu group labels are ~1.9:1 contrast.** "SERVICES" / "AREAS" use `.nav-group { color: var(--muted) #46585f }` on the dark teal panel — the same class that is 7.44:1 on white in the desktop dropdowns. On `#0a2e38` it is faint grey-on-dark, far below 4.5:1 for 14px text. | `home-mobile-menu-open.png` ("SERVICES" barely legible) | `.mobile-menu-panel .nav-group { color: #a9c3c9; }` (same value as `.footer-zips`, measured 7.76:1 on deep teal). |
| D-10 | P3 | All pages / desktop 1440 | **Desktop hero's right ~40% is empty flat gradient**, plus a ~90–110px empty band below the CTA on inner pages (hero 506–671px tall vs content ending ~110px earlier). Honest gradient (no photo exists) — judged on its own terms, the expanse is barren rather than designed. | `cost-desktop-viewport.png`, `insurance-desktop-viewport.png`, `privacy-policy-desktop-viewport.png` | CSS-only enrichment, no photo invented: add a soft radial glow top-right inside `.hero-no-media` (e.g. `background: radial-gradient(60% 90% at 85% 20%, rgba(14,124,140,.55), transparent 60%), linear-gradient(115deg, var(--deep), var(--teal-dark) 55%, var(--teal));`) and tighten inner hero padding 64px→52px. |
| D-11 | P3 | 7 location pages / desktop 1440 | **Footer brand column has a ~300px empty void on location pages.** The footer map is absent by design on the 7 location pages, so column 1 ends after the Call button while Services runs ~300px taller. On the other 27 pages the map fills the column and the footer is balanced. | `crop-cape-coral-footer-full.png` (brand column ends ~y545, Services runs to ~790) vs `crop-home-footer.png` (balanced) | `.footer-brand { align-self: center; }` — centres the brand block in its column so the void splits top/bottom instead of pooling at the bottom. |
| D-12 | P3 | /cost/ / desktop 1440 | **Price column left-aligned and wrapping.** In the cost tables the "Rough area range" values wrap ("About $7,000 to $20,000 or more" over two lines), so prices don't scan as a column. | `crop-cost-table-1.png` | Add a `prices` class to the cost tables in the template and: `.table-wrap.prices td:last-child { text-align: right; white-space: nowrap; }` Scoped so prose last-columns elsewhere are untouched. |
| D-13 | P3 | /how-it-works/ (and anywhere a tel link lands at a line edge) / mobile 390 | **Phone number breaks across lines.** In HIW step 1 the "239-356-3708" link splits as "239-356-" / "3708". | `crop-hiw-mobile-steps.png` (step 1) | `a[href^="tel:"] { white-space: nowrap; }` — sitewide, CSS-only. |
| D-14 | P3 | All pages / mobile 390 (menu open) | **Menu toggle still reads "Menu" when the menu is open** — no Close state, so the only affordance is tapping the same button again. (Minor; Esc / link tap also closes it.) | `home-mobile-menu-open.png` (button still says "☰Menu") | One line in `assets/js/main.js`: toggle `.menu-label` text between "Menu" / "Close" on `details` toggle; or CSS-only swap with `.mobile-menu[open] .menu-label`. |

---

## 2. Ranked fix list (do in this order)

1. **D-01 — cap desktop reading measure at 780px** (P1, one CSS rule, sitewide readability win).
2. **D-02 — `white-space: nowrap` on desktop nav items** (P1, one CSS rule, fixes the wrapped carets + header height).
3. **D-03 — shorten the mobile menu panel above the call bar** (P1, one CSS rule, unblocks the menu's bottom links + Call button).
4. **D-04 — full-bleed the homepage hero** (P2, template move or full-bleed CSS trick).
5. **D-07 — scroll cue on mobile tables** (P2, one CSS rule, unhides the 4th column's existence).
6. **D-08 — tighten mobile hero / CTA-first on mobile** (P2, CSS-only, first viewport gains a CTA).
7. **D-05 — breadcrumb above the hero** (P2, template order change).
8. **D-06 — demote the duplicated top-of-body CTA to ghost-dark** (P2, one class swap).
9. **D-09 — mobile menu group-label colour `#a9c3c9`** (P2, one CSS rule, contrast 1.9:1 → 7.76:1).
10. **D-10 — radial glow + tighter inner hero padding** (P3, CSS-only).
11. **D-11 — centre the footer brand column** (P3, one CSS rule).
12. **D-12 — right-align + nowrap the cost price column** (P3, template class + CSS).
13. **D-13 — `white-space: nowrap` on tel links** (P3, one CSS rule).
14. **D-14 — "Menu" → "Close" when open** (P3, one JS line or CSS swap).

All fixes are CSS/template-order/class changes. **No visible words change** in
any of them except D-06's alternative (dropping the duplicate CTA), which is
flagged as his call. No content, photos, or links are invented anywhere.

---

## 3. Already best-ever — do not touch

- **Contrast everywhere it was measured:** white on coral 5.18:1, coral on
  white 5.18:1, gold on deep 5.64:1, teal on white 8.42:1, hero intro
  `#eef4f5` on deep 12.93:1, footer links 11.05:1, footer ZIPs 7.76:1,
  muted on white 7.44:1. (The ghost button's computed 1.0 was a measurement
  artifact — its `rgba(255,255,255,.08)` background blends over deep teal to
  ≈11:1 in reality.)
- **Type scale + rhythm:** body 20px/34px on both viewports, H1 58px desktop /
  40px mobile, H2 42/31, H3 26/23, Archivo Black display + Inter body,
  H2 coral tick, consistent gold/teal/coral usage across homepage, service,
  location, article, steps, contact, about and legal page classes.
- **Mobile line length 35–36ch** on all 9 pages — ideal.
- **FAQ closed AND open, desktop + mobile:** circular coral +/− badge,
  sand hover, teal question + gold left accent + shadow when open, divider
  line, badge vertically centred on 2–3-line questions. Open-state geometry
  verified: summary 73px, answer 111px, no overlap.
  (`home-desktop-faq-open.png`, `home-mobile-faq-open.png`,
  `insurance-desktop-faq-open.png`.)
- **Steps (HIW 9 + cost inline 6):** coral numbered circles, clear
  hierarchy, clean on mobile (52px circles, no collisions).
- **Details cards, kinds grid (13 cards, 3-col), desktop tables:** teal
  headers, sand zebra rows, generous padding — all clean.
- **Sticky header:** stays put mid-page, shadow intact, dropdowns open clean
  with no clipping (Services dropdown right edge 1012/1440).
- **Sticky bottom call bar ≤620px:** 66px, always visible; at page bottom it
  covers only empty footer padding — measured 2px overlap of the footer-base
  div, **0 text covered** (`contact-mobile-bottom-callbar.png`).
- **Footer (27 pages with map):** balanced 4-column grid, map 333×280
  desktop / 350×240 mobile, single-line footer base.
- **Zero overflow** at 1440 / 390 / 320 on all 9 pages; 320px tables scroll
  inside their wraps (no page overflow).
- **Hero typography:** H1 + intro + CTAs + areas line are well set; the
  gradient + scrim are honest (no photo exists) and the intro contrast is
  excellent. The findings above are about layout/measure, not the gradient
  itself.
- **Maps:** main map 1192×560 desktop / 350×420 mobile with gold 2px border;
  footer map present on 27 pages, absent by design on the 7 location pages.
  Tiles are blank in VM Chromium only (VM cannot reach google.com/maps) —
  standing open item, needs one real-browser look.

---

## 4. Method notes (what was checked, what was disproved)

- **Two apparent defects were disproved by re-probe and are NOT findings:**
  1. An early "144 chars" worst-line figure came from a 16px label
     (`.details-sub`, 7 visible chars in an 1105px box). Re-measured with
     the Range API on real 20px body lines only: worst is **109–114 chars**
     (D-01) — still P1, but the honest number.
  2. An element screenshot seemed to show the mobile table's first column
     header cut ("ategory"). A clean window-scroll re-probe proved
     `th[0].left == 0` and "Category" renders fully at `scrollLeft == 0` —
     the cut was a `scrollIntoView` artifact. The real mobile-table finding
     is D-07 (hidden 4th column), evidenced by the clean first-paint shot.
- **Not defects:** the `.btn` entries measuring 0×0 are the mobile-menu
  panel button (`display: none` on desktop); the header-call button's
  doubled `textContent` is the full + short phone spans, only one of which
  is ever visible.
- **Known limits of this audit:** map tiles blank in VM Chromium (standing
  item); no live Speed Index measured from this VM (standing item); the
  audit covers the 9 listed pages in depth — the other 25 pages share the
  same header/hero/footer/table/FAQ components, so D-01/D-02/D-03/D-05/D-06
  apply to them by construction, but their individual bodies were not
  screenshotted here.
