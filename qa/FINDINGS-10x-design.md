# FINDINGS — 10x Design / Includes Work (Worker 3)

Fort Myers PHP site (`~/workspace/fort-myers-php/`). Local only — no push, no deploy.
PHP verified on the worker's own server (`php -S 127.0.0.1:8135`, `qa/verify_export.py` never run).

## A-2 — /areas/ heading outline: H1 → H2s, no level skip — STRUCTURE DONE, CSS PENDING

**Follow-up from Worker 2 (CONTENT):** Worker 2 promoted 5 headings on /areas/
from H3 to H2 (table heading "Lee County Service Areas and ZIP Codes" +
Fort Myers, Sanibel and Captiva, Pine Island and Matlacha, San Carlos
Park/Gateway/Iona). The other 6 area headings (Cape Coral, Lehigh Acres,
North Fort Myers, Fort Myers Beach, Estero, Bonita Springs) are `area-cards`
titles whose `<h3>` was hardcoded in `site/includes/functions.php`.

### What changed (functions.php only — no data file touched)

1. **`area-cards` case — slug-gated H2.** Card titles render as
   `<h2 class="area-card-title">` when `$page['slug'] === '/areas/'`, and
   stay `<h3>` otherwise. `area-cards` blocks exist ONLY in
   `site/data/areas.php` (2 grids), so no other page is affected; the gate
   keeps it that way if a block is ever added elsewhere.
2. **`h2` case — optional class hook.** An h2 block may now carry
   `'class' => '...'`; it is APPENDED to Worker 1's L-6 feature/standard
   class (`h2-feature` / `h2-standard`), never replaces it. No block sets
   one today, so L-6 output is byte-identical.

### Verified outline (/areas/, live render on port 8135)

- H1 count: **1** — "Water Damage Help Across Lee County, FL"
- H2 count: **17**, H3 count in `<main>`: **0**
- Order: table heading first ("Lee County Service Areas and ZIP Codes"),
  then Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers,
  Fort Myers Beach, Sanibel and Captiva, Pine Island and Matlacha, Estero,
  Bonita Springs, San Carlos Park/Gateway/Iona, then the remaining section
  H2s (permits/50% rule, problems, what to do first, what to expect, FAQ,
  closing). No level skip anywhere on the page.
- The 6 card titles are `<h2 class="area-card-title">` (count 6 in HTML).

### The 5 promoted headings — left at full H2 size (decision recorded)

They are top-level section headings, so full H2 size (42px desktop /
31px mobile) is correct for them. The class hook exists if design ever
wants the H3 look: add `'class' => 'h2-as-h3'` to those 5 blocks in
`site/data/areas.php` (Worker 2's file — NOT edited here) plus a CSS rule
for it. No action needed unless design says so.

### ⚠️ OPEN — card titles render at 42px until CSS lands (Worker 1)

A bare H2 inside a card inherits the base `h2 { font-size: 42px }` plus
the `.page-body h2::before` coral bar, and loses the `.area-card h3`
sizing (23px, 20px top margin, 28px side padding — the selector does not
match an h2). Measured on port 8135: card-title computed font-size
**42px**, `::before` bar present, "North Fort Myers" wraps to two lines
and titles run to the card's left edge. Screenshot:
`qa/screenshots-10x/areas-cards-h2-42px-before-css.png`.

**Exact CSS needed (Worker 1 / CSS owner):**

```css
.area-card h2.area-card-title { margin: 20px 0 0; padding: 0 28px; font-size: 23px; }
.page-body h2.area-card-title::before { display: none; }
```

Until that rule lands, the /areas/ cards look broken at desktop and
mobile. The outline fix itself is complete and verified; this is a
styling follow-up, not a structural one.

---

# FINDINGS — 10x DESIGN ROUND (Worker 1, DESIGN)

- **Project:** `~/workspace/fort-myers-php/` — Fort Myers PHP site, 34 pages
- **Date:** 2026-11-19 ~23:04–00:30 PKT · **Mode:** LOCAL ONLY (no push, no deploy, no DNS, no git; `qa/verify_export.py` never run; `out/` never touched)
- **Server:** own PHP 8.3.6 server on `127.0.0.1:8133` (`php -S 127.0.0.1:8133 -t site site/index.php`, killed by PID at end); Playwright bundled Chromium only
- **Audit base:** `qa/FINDINGS-20x-testing.md` (P2 C-01/02/03, B-P3-1, C-04–08, D-P3-3, L-1–L-4, L-6–L-9, L-11–L-15, L-17, L-18). L-5 NOT implemented (owner order: wide lines — see §7).
- **Files owned (only these):** `site/assets/css/styles.css` (1273 → 1609+ lines), `site/includes/functions.php`, `site/includes/header.php`, `site/includes/footer.php`. `site/data/*`, `site/assets/img/*`, `out/` untouched by this worker.
- **Probe:** `qa/probe_10x_design.py` (+ `qa/10x-design-measure.json`, 102 rows = 34 slugs × 1440/390/320, plus an 820px pass `/tmp/probe820.py`). Screenshots: `qa/shots-10x-design/` (59 files).

## VERDICT

**All 25 assigned items done, plus Worker 3's open A-2 CSS item (below).** Overflow **0 at 1440/390/320/820 on all 34 pages** (was 31 pages overflowing at 320 in the first probe run — see §5, fixed same round). Tables **0 overflow at every width** (81 tables measured in-view). Console/page errors **0**. H1: **no hero ends on a 1–2-word line at 1440/390/820** (last-line/first-line ratio ≥0.53 at 1440/390; at 320, /contact/ and /about/ end on "Pros" — 1 word, 88px — see §7). Schema validator on a temp export (`/tmp/10x-export`, NOT `out/`): **ERRORS 0, WARNINGS 0**, Article-image note gone (only 3 publisher-logo notes remain, by design). Word-diff vs the 4 pre-change baselines (home/cost/how-it-works/drying, saved before any edit): **only authorized additions** (§6).

## 0. WORKER 3 OPEN ITEM CLOSED — A-2 /areas/ card-title CSS

Worker 3's section above left one open item for the CSS owner: the 6 `/areas/` card titles are now `<h2 class="area-card-title">` and needed sizing like the old `.area-card h3` with the `::before` bar suppressed. **Done in `styles.css` (appended 10x DESIGN block):**

```css
.page-body .area-card h2.area-card-title {
  margin: 20px 0 0; padding: 0 28px;
  font-size: 24px; line-height: 1.25; letter-spacing: -0.01em;
  color: var(--terra); padding-bottom: 0; border-bottom: 0;
}
.page-body h2.area-card-title::before { display: none; }
```

Deviation from Worker 3's spec (23px): this round's area-card h3 renders **24px terracotta** (L-6), so the card titles match that for consistency across pages. Verified on port 8133 (`/tmp/areas_check.py`): 6 titles, computed **24px**, colour `rgb(147, 56, 14)` (terracotta), `::before` display none, `<main>` H2 **17** / H3 **0** on /areas/, overflow 0 at 1440 and 390. Screenshot: `qa/shots-10x-design/areas-1440-cards.png` ("Fort Myers Beach" title in terracotta, no bar, correct padding). Worker 3's structural change in `functions.php` (slug-gated H2 + h2 `'class'` hook) is intact in the file alongside this round's edits — no conflict.

## 1. HEADLINE — H2 + H3 COLOUR CHANGE (fresh premium palette)

Old: H2 deep `#0A2E38` (14.38:1 white), H3 teal `#0B5563` (8.42:1 white) + 44px gold rule on every H3.
New (coherent with Caloosahatchee: deep river teal + sunset coral + sand + gold):
- **H2 — lagoon `#0B3D4E`** (`styles.css` §1, ~line 1057; `:root` `--lagoon`): 11.72 white / 10.41 sand / 9.53 sand-2.
- **H3 — sunset terracotta `#93380E`** (`--terra`): 7.47 white / 6.63 sand / 6.07 sand-2. H2 (river) vs H3 (sunset) now read as two halves of one theme instead of two teals.
- Gradient bar kept (teal→coral); feature H2 72px bar, standard 48px (L-6).
- Where: `site/assets/css/styles.css` (proposal block §1/§2 edited in place + appended 10x DESIGN block, line 1252+). No other file carries the colours.

## 2. WHAT CHANGED, BY TASK

| # | Task | Change (file:location) | Before → After (measured) |
|---|---|---|---|
| 1 | Headline H2/H3 | `styles.css` :root + §1/§2 + appended block | H2 `#0A2E38`→`#0B3D4E`, H3 `#0B5563`→`#93380E` (§3 contrast table, all ≥4.5:1) |
| 2 | C-01 table floor | `styles.css` `table{font-size:19px}`→20px, `th 18px`→20px, `@620px table 18px`→20px | td/th **20px at 1440/390/320 on all 81 tables** (probe); /cost/ prices fit — stacked layout at ≤620, no overflow |
| 3 | C-02 + C-04 tables | `styles.css` appended block: stacked-card tables ≤620px (thead visually hidden, `td::before` = own header words via `data-label`); `functions.php` table case adds `data-label` per cell | 8 worst tables 45–142px hidden @390 → **0 overflow @390/320, all 81 tables** (in-view measurement after `scrollIntoView`, content-visibility-safe) |
| 4 | C-03 hero/final CTA @320 | `styles.css` ≤380px: `white-space:nowrap` on `.hero-ctas .btn` + `.closing-cta-line .btn` (19px, padding 16/20); ghost 17px (hero) / 16px (closing) | Hero call button **58.8px tall @320 on 34/34** (was 86px, wrapped "Call 239-356- / 3708"); closing button one line. Scope note: nowrap is NOT on middle `.cta-line` buttons — their label is the long "Call 239-356-3708, answered 24/7" and nowrap forced a 400px button (97px overflow, found in probe run 1) — they keep wrapping (66px @820) |
| 5 | L-1 hero scrim | `styles.css` `.hero-scrim` (in place): directional gradient `100deg, 0.92/0.78@38%/0.38@68%/0.22@100%` + bottom-only `0deg 0.55→transparent 32%`; `.hero-img` `saturate(1.12) contrast(1.04)`; `.hero-area` right stop **0.12** (`functions.php` adds `hero-area` class on the 7 location pages) | Cape Coral canal no longer murky grey — photo breathes right side (shot `cape-coral-1440-hero2.png`); white H1 ≥7:1 (worst-case scrim composite over a pure-white photo pixel: eyebrow 8.32:1, trust 6.14:1 at the 0.78 stop) |
| 6 | L-2 eyebrow + trust | `functions.php` `hero_eyebrow()` (~363), `hero_trust_items()` (~390), `hero_trust_html()` (~409); hero cases (~490, ~856) | Eyebrow 13px Inter 800, 0.24em, gold `#E8C87A`, 32px gold rule, margin-bottom 18px; trust row 15px/600 `#CFE0E4`, gold `·` separators. Copy is per-page from its own words only: home "Fort Myers · Lee County, FL"; area pages "<Area> · Lee County, FL"; service/guide "Emergency Service · Answered 24/7"; trust = "Answered 24/7" + ("Moisture readings logged" if the copy says "readings logged", else "Moisture readings taken" / "Photos and moisture logs") + ("Written scope before rebuild" if the copy says "written scope", else the footer place line). No invented text |
| 7 | L-3 H1 balance | `styles.css` `h1{text-wrap:balance}`, `.hero-inner h1{max-width:820px}` (was 960px); mobile H1 40→**38px**, line-height 1.08; `functions.php` `h1_html()` (~441) nowrap-spans the place phrase on /drying/ ("Fort Myers, FL") and /cost/ ("Fort Myers?") | No hero ends on a 1–2-word line at 1440/390/820 (probe: last/first ratio ≥0.53 at 1440/390; worst 1440 = /cost/ 0.53, "Fort Myers?" full line). At 320, /contact/ + /about/ end on "Pros" (1 word, 88px, ratio 0.36–0.43) — flagged §7. The 75px "line" the probe reported for /drying/ @820 is a measurement artefact: the Range rects split at the nowrap-span boundary; the screenshot shows "in Fort Myers, FL" on one line (`drying-820-hero.png`) |
| 8 | L-4 banding | `functions.php` `render_page()` (~899): blocks grouped into H2-led `<section class="body-section">` (words/order/headings unchanged); CSS: alternating `.band-sand` `#F6F1E7`, full-bleed via `margin:0 calc(50% - 50vw)`, padding **88px** desktop / **64px** mobile; ONE `.band-deep` per page = the section holding the final CTA (see L-14). Legal pages (no cta-line) get **no** deep band — flagged §7 | Body is no longer one white river (visible in `how-it-works-1440-full.png`: white/sand alternation, deep closing band) |
| 9 | L-6 kickers + H2/H3 scale | `functions.php` h2 case (~510): `<p class="sec-kicker">` + `h2-feature` (first H2-section) / `h2-standard`; CSS: kicker 13px/700/0.20em uppercase teal `#0B5563`; feature H2 **46px/1.08**, standard **40px/1.12**; bar 72px feature / 48px standard; H3 **24px**, `-0.01em`, gold underline **only on feature H3s** | Kicker text = the page's own group label (Services / Areas / Guide / About / Fort Myers) — already on the page as breadcrumb/nav label, 0 invented words. It repeats per H2 (23× "Services" on home) — a deliberate section-label pattern; flagged as visually repetitive in §7 |
| 10 | L-7 kind/help cards | `styles.css` appended block: padding 28→**32px**, radius 12→**16px**, H3 23px, body **18px/1.55** (per brief — below the 20px floor, flagged §7), hover 0.25s `translateY(-4px)` + shadow + photo `scale(1.04)` in `overflow:hidden`; link styling bold teal, no underline until hover | Hover verified live: `transform: matrix(1,0,0,1,0,-4)` on hover (`home-1440-kinds-hover.png`). Arrow draft removed: a gold "→" via `::after` rendered as "Emergency water removal →:" / "businesses →." (link sits mid-sentence, punctuation outside the anchor) — removed, bold+hover-underline kept |
| 11 | L-8 buttons | `styles.css` `.btn-call` flat `#C2410C`, radius 12px, padding 18/32, shadow `rgba(194,65,12,0.30)`, **inset gold removed**; hover `#9A3412` + `translateY(-2px)`; `.btn-ghost` 1.5px `rgba(255,255,255,0.85)` border, `rgba(10,46,56,0.25)` bg, blur 4px; hover `rgba(255,255,255,0.14)`, no gold fill; `.btn-ghost-dark:hover` gold inset removed | Buttons read flat coral + ghost, no stray-underline edge (visible in every hero shot) |
| 12 | L-9 header | `styles.css`: `.brand-name` 20px nowrap, `aria-current` underline removed (gold inset stays only on `.nav-current-top`); nav **17px/600**, ls 0.01em, padding 12/14; header gradient `180deg #0A2E38→#0C3340` + 3px gold hairline (existing inset shadow); `header.php` line 113: compact **38×38px** phone-icon button (mobile header) | **Fit problem found + fixed (§5):** 17px nowrap brand is ~269px in Archivo Black, so 17px + mark + icon + "Menu" = 423px in a 350px row at 390 — the first screenshot showed the icon overlapping "Damage". Fit that keeps nowrap + icon: brand **15px** ≤620px (14px ≤380px), brand-mark hidden ≤620px, menu icon-only ≤620px (347px @390, 277px @320). The ordered 17px mobile brand does not fit with the ordered icon — flagged §7 |
| 13 | L-11 mobile hero | `styles.css`: hero padding 40→**32px top / 96px bottom** (incl. `.hero-inner-page`); intro capped at 3 lines ≤620px with fade mask + "Read the intro ↓" anchor (`functions.php` hero cases; `:target` unclamps); mobile ghost nowrap | Intro cap verified by click: intro height **90px → 360px** after tapping the anchor (`cost-390-intro-expanded.png`); last intro line clears the call bar (96px bottom padding, visible in `cost-390-hero.png`) |
| 14 | L-12 utility line | `functions.php` cta-line case (~759, role `utility` for the FIRST cta-line on each page): slim line, 18px muted `#46585F`, phone as plain teal link, 16px phone glyph: "Answered 24/7 · Call 239-356-3708", left-aligned | Post-breadcrumb coral button gone on all 31 pages with one (visible in `how-it-works-1440-full.png`); coral buttons remain only in hero + closing band |
| 15 | L-13 steps spine + chips | `styles.css`: 2px vertical connector gold→teal (`left:29px; top:64px; bottom:-4px`, last li none); `.step-duration` chip 13px/700/0.14em uppercase, sand bg, teal text; step H3 26→**28px**; `functions.php` `step_duration()` (~456) + steps-rich case (~743) | Chips on 6 of 9 how-it-works steps, verbatim from the page's own "How Long Each Stage Takes" table: "One short phone call", "Usually at the first visit" ×2, "Usually the first day" ×2, "About 3 to 5 days". "While you wait", "Final readings and paperwork", "Repairs" get **no chip** — no stage-time row exists for them in the copy, and "Final day" does not occur anywhere in the data (grep-verified); inventing one was refused. Spine visible in `hiw-1440-steps.png`. Other pages' `steps` lists have no durations in their copy, so no chips there (spine + 28px H3 apply sitewide) |
| 16 | L-14 closing band | `functions.php`: last cta-line → role `closing` (coral button "Call 239-356-3708" + ghost "Describe your water problem" + trust line "Answered 24/7, including holidays and the days after a storm"); its section gets `.band-deep`: gradient `#0A2E38→#0D3A46→#0B5563`, padding 88px 0, white H2 40px + 72px gold rule, intro 22px `#EEF4F5`, wave SVG top edge `rgba(201,155,63,0.14)` | Visible at the foot of every page with a CTA (`how-it-works-1440-full.png` bottom). The closing button drops ", answered 24/7" from its label — those words move into the trust line directly under it, so no words are lost (word-diff §6) |
| 17 | L-15 cost page | `functions.php` table case (~682–718): "One room" row → `.cost-row-highlight` (bg `#FDF8EC`, 5px coral left border, "Most common" chip in first cell) + range bar after the first cost table (8px track `#EFE7D6`, coral fill $500–$15,000, gold marker at $1,200–$3,500 = 4.8%–20.7% of the track, labelled "Most Fort Myers jobs land here", 16px) | Prices unchanged (verified in word-diff: $1,200/$3,500 untouched). Shots: `cost-1440-rangebar.png`, `cost-390-table.png` (stacked "One room / MOST COMMON" card) |
| 18 | L-17 palette | `styles.css`: sand-2 `#EFE7D6` was already `--sand-2` (bands use it); kickers gold-on-deep `#E8C87A` in `.band-deep`; footer top border 3px→**6px gradient teal→gold→coral** (`border-image`); 1px gold hairline under H2 areas (`border-bottom:1px solid #EFE7D6` on `.page-body h2`) | Gold stays an accent (rules/chips/kickers only) |
| 19 | L-18 map fallback | `functions.php` map case + `footer.php` line 10: `<figure class="map-figure">` with sand/teal gradient + centred caption "Map loading · Fort Myers & Lee County"; iframe `background:transparent`, `z-index:1` over the poster (`z-index:0`) | Proven in the sandbox (Google unreachable here): every footer/section map shows the poster instead of a blank box (`how-it-works-1440-full.png` footer, `home-390-footer2.png`). Limitation: a hard-failed iframe can paint its own error page over the poster in some browsers — the poster covers slow/blocked loads, not a browser error page. No fake map image invented |
| 20 | C-05 chrome/label floor | Raised to 20px: breadcrumb 18→20, `.hero-areas` 18→20, `.map-link` 18→20, footer-col links 18→20, `.footer-zips` 17→20, `.footer-hours` 18→20, footer-base 17→20, back-to-top 17→20, footer-col h3 19→20, `.details-sub` 15→**20px** desktop (18px mobile, ls 0.12em) | Flagged exceptions (below floor, per brief / label nature): nav **17px** (L-9 order wins), brand-tag **18px** (20px would equal the brand-name size and break hierarchy), nav-group labels **18px**, eyebrow/kicker 13px, hero trust 15px, closing trust 16px, utility line 18px, step chips 13px, cost chip 12px, range labels 16px, stacked-table `data-label`s 18px, card body 18px (L-7) |
| 21 | C-06 kind-card H3 rule | `styles.css` appended block: `.kind-card.has-photo h3::after` 44px gold rule | **Decided: rule ADDED.** Under the new H3 system the photo cards get the same 44px gold rule as feature H3s (gold on the dark scrim, decorative). The old exclusion (white H3, no rule) is gone |
| 22 | C-07 + C-08 footer | `styles.css` ≤620px: 2-col link grid (brand spans full width), map height 280→**200px**; `.footer-col a` padding 9→**10px 0** | Footer @390: **1,774px → 1,614px** (non-area pages), **1,472px → 1,344px** (7 area pages, no footer map). Min footer link tap height **49px** (44.09px on the non-link current-page spans, which are not tap targets) |
| 23 | B-P3-1 Article image | `functions.php` `ld_normalize_given($schema, $heroUrl)` (~283) + call site (~822, `$heroUrl` from `page_hero()`); render-time only, data files verbatim | `qa/validate_schema.py /tmp/10x-export` → **ERRORS 0, WARNINGS 0**; the 3 Article-image notes are gone. `image` = `https://fortmyerswaterdamagerestoration.us/assets/img/hero-<slug>.jpg` on /cost/, /insurance/, /how-it-works/ (verified in the exported JSON-LD). Only 3 notes remain: publisher has no logo (by design) |
| 24 | D-P3-3 footer comment | `footer.php` line 34 | Long comment → `<!-- Areas is header-only -->` on all 34 pages (grep-verified in export) |
| 25 | Cache-bust | `header.php` line 48 | `styles.css?v=2` → **`styles.css?v=3`** |

## 3. CONTRAST TABLE (WCAG 2.x, computed from the hex values)

| Element | Foreground on background | Ratio |
|---|---|---|
| H2 `#0B3D4E` | white / sand `#F6F1E7` / sand-2 `#EFE7D6` | 11.72 / 10.41 / 9.53 |
| H3 `#93380E` | white / sand / sand-2 | 7.47 / 6.63 / 6.07 |
| H2 white | deep band `#0A2E38` / mid `#0D3A46` / teal end `#0B5563` | 14.38 / 12.28 / 8.42 |
| Eyebrow `#E8C87A` | deep `#0A2E38` | 8.88 (8.32 worst case: scrim 0.92 over a pure-white photo pixel) |
| Trust `#CFE0E4` / intro `#EEF4F5` | deep | 10.57 / 12.93 (trust 6.14 worst case at the 0.78 scrim stop) |
| Kicker teal `#0B5563` | white / sand | 8.42 / 7.48; gold-light on deep 8.88 |
| Utility muted `#46585F` / teal link | white | 7.44 / 8.42 |
| Step chip teal on sand | `#0B5563` on `#F6F1E7` | 7.48 |
| "Most common" chip white on coral | `#FFFFFF` on `#C2410C` | 5.18 |
| Range labels muted on white | `#46585F` on white | 7.44 |
| Table th white on deep / price gold `#C99B3F` on deep | — | 14.38 / 5.64 |
| Table label teal-dark on white / sand-2 | `#083F4A` | 11.54 / 9.38 |
| Map poster gold-light | teal `#0B5563` / deep | 5.20 / 8.88 |
| Footer link `#D7E4E7` / brand-tag `#B8D2D8` on deep | — | 11.05 / 9.07 |
| Details-sub teal-dark on sand | `#083F4A` on `#F6F1E7` | 10.25 |
| Area-card title terracotta on white | `#93380E` | 7.47 |

All changed text elements ≥4.5:1 in every context they sit in. Old colours for reference: H2 `#0A2E38` 14.38 white, H3 `#0B5563` 8.42 white.

## 4. MEASUREMENTS (probe `qa/10x-design-measure.json`, 102 rows)

- **Overflow:** 0 at 1440 / 390 / 320 / 820 on all 34 pages (final run; first run found 31 pages overflowing at 320 — §5).
- **Tables:** 0 overflow at 1440/390/320, all 81 tables, measured in-view after `scrollIntoView` (content-visibility-safe). td/th font 20px at all widths.
- **Hero call button @320:** 58.8px on 34/34 (one line); home ghost 56px (one line). Mid-page `.cta-line` buttons wrap to 66px at 820 (long label, by design — §5).
- **H1:** no 1–2-word last line at 1440/390/820 (last/first ratio ≥0.53); see §7 for the 320px /contact/ + /about/ exception.
- **Footer @390:** 1,614px (non-area) / 1,344px (area); min link tap 49px; min button height: the probe's `minBtn 0.0` is the hidden mobile-menu call button inside the closed `<details>` panel (display:none), not a visible tap target.
- **Console/page errors:** 0 across all renders.
- **H1 count:** exactly 1 on all 34 exported pages; **dashes:** 0 em/en dashes in visible HTML of all 34 exported pages.
- **Schema:** `qa/validate_schema.py /tmp/10x-export` → 34 pages, 92 scripts/nodes, ERRORS 0, WARNINGS 0, NOTES 3 (publisher logo only).
- **/areas/ outline (A-2):** `<main>` H2 17 / H3 0; card titles 24px terracotta, `::before` none.

## 5. DEFECTS FOUND IN MY OWN FIRST PASS (fixed same round)

1. **320px overflow, 31 pages (25–100px).** Cause: (a) `white-space:nowrap` on ALL `.cta-line .btn` — the middle buttons' long label forced a 400px button; (b) the closing ghost button ("Describe your water problem") was 313px at 19px. Fix: nowrap scoped to `.hero-ctas .btn` + `.closing-cta-line .btn` only; closing ghost 16px/padding 16/14 at ≤380px. Re-measured: scrollWidth 320 on all sampled pages, then 0 overflow in the full re-run.
2. **Mobile header overlap at 390px** (screenshot `cost-390-hero.png` pre-fix): the ordered 17px nowrap brand + phone icon + "Menu" overlapped "Damage". Fix: brand 15px ≤620px (14px ≤380px), brand-mark hidden ≤620px, menu icon-only ≤620px; re-shot clean at 390 and 320 (`cost-390-header.png`, `cost-320-header.png`).
3. **"Learn more →" arrow** rendered as "Emergency water removal →:" — removed (see L-7 row).

## 6. WORD-DIFF (0 unauthorised changes)

- **4-page pre/post baseline** (HTML saved before any edit: `/tmp/base-{home,cost,hiw,drying}.html` vs post-edit): added words are ONLY the authorised categories — kickers (group label), eyebrow, trust items, utility line, closing trust + ghost-button text, "Read the intro ↓", map-poster caption, cost chip + range-bar labels, step chips. Removed words are ONLY "answered" + "239-356-3708," from the closing button label — those exact words reappear in the closing trust line directly under it ("Answered 24/7, including holidays and the days after a storm").
- **34-page diff vs old `out/`** (temp export `/tmp/10x-export`): same authorised additions (kickers dominate: "Services" 284, "Areas" 104, "Guide" 71) plus **concurrent data edits by sibling workers, NOT mine** — visible in the removed list: /areas/ ZIPs `33993`/`33931`/`33956,` (D-P2-1/D-P3-1), the 7-page drying-step sentence word "run" and the sign-off "General pricing information:" (D-P3-7), home "cleanup:" (D-P2-2 help-card links). I touched no data file; those edits were in flight while I exported. The verifier's canonical export will be built from final data.
- **Dashes:** 0 in all 34 exported pages.

## 7. WHAT I COULD NOT DO / FLAGS / OPEN CALLS

1. **L-5 (780px prose cap) — NOT implemented.** Directly contradicts the owner's standing "wide lines" order; needs his explicit call (audit's own ruling).
2. **Mobile brand 17px nowrap + 38px phone icon do not fit at 390px** (measured 423px in a 350px row). Implemented as brand 15px ≤620px / 14px ≤380px, mark hidden, icon-only menu. If he wants the literal 17px, the icon has to go (call bar already serves mobile) or the brand must wrap.
3. **H1 at 320px: /contact/ + /about/ end on "Pros"** (1 word, 88px). At 1440/390/820 they end on full lines. A nowrap span on "Restoration Pros" would fix 320px but I did not add a third hand-tune beyond the two ordered pages; owner's call.
4. **Legal pages have no deep-teal band** (no cta-line to anchor L-14 on; L-4's "one deep band per page" does not apply to them as built).
5. **Kickers repeat the group label before every H2** (23× "Services" on home). Honest (0 invented words) but repetitive by design; a per-section kicker would need new words.
6. **Step chips missing on 3 of 9 how-it-works steps** ("While you wait", "Final readings and paperwork", "Repairs") — no duration exists for them in the copy; "Final day" does not occur in the data. Other pages' step lists have no durations in their copy either.
7. **Below-20px labels kept deliberately** (see C-05 row): nav 17px (L-9 order), brand-tag 18px, nav-group 18px, eyebrow/kicker 13px, trust 15px, closing trust 16px, utility 18px, chips 12–13px, range labels 16px, card body 18px (L-7 order), stacked-table labels 18px. All are labels/chips/navigation, not prose.
8. **Full-page screenshots show empty table/FAQ boxes** on long pages — a `content-visibility:auto` screenshot artefact (blocks never scrolled into view don't render for the capture). Tables/FAQs were verified separately in-view (0 overflow, 20px fonts); not a site defect.
9. **Map poster limitation** (L-18): covers slow/blocked loads; a browser error page for a hard-failed iframe can paint over it. Live map tiles still need one real-browser look (standing item; Google unreachable from this VM).

## 8. SCREENSHOTS (all in `qa/shots-10x-design/`)

Heroes: `home-1440-full.png`, `home-390-full.png`, `cost-{1440,390}-hero.png`, `cost-{390,320}-header.png`, `cost-820-hero.png`, `drying-{1440,820}-hero.png`, `cape-coral-1440-hero2.png` (area scrim 0.12), `how-it-works-1440-hero.png`, `water-removal/ceiling-leak/contact/areas-{1440,390}-hero.png`, `cost-390-intro-expanded.png` (intro :target expansion 90→360px). Components: `cost-1440-rangebar.png`, `cost-390-table.png`, `ceiling-390-table.png`, `hiw-1440-steps.png`, `how-it-works-1440-full.png` (banding + deep band + footer poster), `home-1440-kinds.png`, `home-1440-kinds-hover.png`, `home-390-footer2.png`, `areas-1440-cards.png`, `areas-390-cards.png`, plus per-page hero/footer shots for the 9 sampled slugs at 1440/390. Full-page `cost-1440-full.png` exceeds the image reader's size limit — use the targeted shots above instead.

## 9. FILES CHANGED (only the 4 owned files + this shared findings file)

- `site/assets/css/styles.css` — 1273 → ~1625 lines (in-place: palette vars, H1 balance, flat buttons, header gradient/brand/nav, hero scrim + H1 max-width, table floor 20px, H2/H3 colours, footer 6px gradient border, mobile H1 38px, hero padding 32/96, mobile table 20px; appended 10x DESIGN block line 1252+, incl. the A-2 area-card-title rule).
- `site/includes/functions.php` — helpers (~328–470), hero cases, h2 kicker/feature (+ Worker 3's `'class'` hook, intact), table data-labels + cost highlight/range bar, steps-rich chips, cta-line roles, map poster figure, `ld_normalize_given($schema, $heroUrl)`, inner-hero `hero-area` class, H2-led `.body-section` grouping + deep-band detection. (Worker 3's area-cards H2 gate also lives here, untouched by this worker.)
- `site/includes/header.php` — line 48 `?v=3`; line 113 mobile 38×38 phone-icon button.
- `site/includes/footer.php` — line 10 footer map poster figure; line 34 comment shortened to `<!-- Areas is header-only -->`.
- `qa/probe_10x_design.py`, `qa/10x-design-measure.json`, `qa/shots-10x-design/` (59 shots), this file (appended below Worker 3's A-2 section). Temp export `/tmp/10x-export/` (validation only — `out/` untouched, `qa/verify_export.py` never run).
