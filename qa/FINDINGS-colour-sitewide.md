# FINDINGS — Sitewide colour audit (base headings + unowned sections)
## Fort Myers NEW PHP site — `~/workspace/fort-myers-php/` — 2026-11-19

**Task:** sitewide colour auditor for the raised bar (~18:20 PKT): colouring to
BEST-EVER (not just tables/buttons/details), H2/H3 colour good sitewide, text
stays 20px (no size change), goal = a site Google and users love, every
technical gate green. Proposal files ONLY — no shared file edited, no commit,
no push.

**Method:** served the current export (`python3 -m http.server 8137` from
`out/`, PID in `/tmp/http8137.pid` — stopped after probing) and measured
computed colours with Playwright (bundled Chromium, no `executable_path`) on
`/`, `/water-removal/`, `/cost/`, `/contact/`, `/areas/`, `/404.html` at
desktop 1440 + mobile 390. Every ratio below was COMPUTED (WCAG relative
luminance), not eyeballed. Raw measurements:
`/tmp/colour-sitewide/measured.json` (12 page×viewport runs); screenshots
`/tmp/colour-sitewide/shot-{home,water-removal}-{desktop,mobile}-{full,viewport}.png`
(viewed: home desktop viewport, water-removal mobile viewport — hero reads
clean, skip-link focus state visible, gold-cream intro phone link legible).

**20x decisions respected (from `qa/FINDINGS-20x.md`, not undone):**
D1 river motif (`hero-no-media::after`) untouched; D3 current-page nav states
kept (only the one failing colour inside them fixed, §5b); D5 FAQ links stay
teal + underlined (8.42:1); mobile nav-group labels stay #A9C3C9 (7.76:1);
skip-link focus (coral bg, gold outline) kept; back-to-top stays footer-only;
map fallback link stays gold-cream #FFD9A8 (10.78:1).

---

## 1. THE H2/H3 DECISION (the owner's headline order)

**Current (measured, all 34 pages — 524 plain `<h2>`, 2 `.map-caption` h2s,
24 h3s on home alone): H2 and H3 are the SAME colour, deep #0A2E38, 14.38:1
on white.** The contrast is excellent but there is zero heading hierarchy —
a page reads as one flat ink colour from H2 to H3. That is the defect this
round exists to fix.

**Decision — one theme accent per level (river + sunset):**
- **H2 → river teal #0B5563.** 8.42:1 on white, 7.48:1 on sand, 6.85:1 on
  sand-2. Still far above 4.5:1 (normal text) and 3:1 (large text) on every
  background an H2 can sit on.
- **H3 → sunset coral-dark #9A3412.** 7.31:1 on white, 6.49:1 on sand,
  5.94:1 on sand-2. Coral-dark was chosen over plain coral #C2410C (5.18:1
  white / 4.60:1 sand — a pass, but the thinnest margin on the site) so H3s
  keep a comfortable margin on sand-tinted sections too.
- **The H2 coral bar: KEPT, and upgraded to a gradient.** Same 72px × 6px,
  same position — now `linear-gradient(90deg, teal → coral)`, the river
  flowing into the sunset. It ties the new teal H2 to the coral brand
  accent instead of floating as an unrelated red dash.
- **Mobile:** no separate rules. The same base rules cascade: H2 31px teal,
  H3 23px coral-dark, same bar, same ratios. Measured mobile values are
  identical to desktop (only sizes differ, and sizes are untouched).
- **Map-caption H2** (home + contact, 30px) is an H2 and gets the same
  treatment — it is a section heading, consistency wins.
- **Excluded by design:** `.details-card h2` (worker D) and `.kind-card h3`
  (worker F) — the snippet uses `:not()` so those rules never match them,
  in either application order. `.footer-col h3` is outside `.page-body`
  and stays white (see §6).

---

## 2. PER-SECTION: CURRENT → PROPOSED (all ratios computed)

### 2.1 Base H2/H3 — CHANGED (§1 above)
| Element | Before | After |
|---|---|---|
| H2 text | #0A2E38 on white, **14.38:1** | #0B5563 on white, **8.42:1** (sand 7.48:1, sand-2 6.85:1) |
| H2 bar | solid coral #C2410C | gradient teal → coral, same 72×6px |
| H3 text | #0A2E38 on white, **14.38:1** | #9A3412 on white, **7.31:1** (sand 6.49:1, sand-2 5.94:1) |

### 2.2 Body text + links — LINKS CHANGED, text unchanged
- Body text ink #12262E on white **15.64:1** — already best. Unchanged.
- Body links: teal #0B5563 **8.42:1**, hover coral #C2410C **5.18:1** —
  both pass, but links were **colour-only**: teal vs surrounding ink
  measures only **1.86:1**, so a reader who cannot distinguish teal from
  ink has no cue (WCAG 1.4.1 wants 3:1 or a non-colour cue).
  **Proposed:** same teal, now **always underlined** (3px offset, matching
  the 20x D5 FAQ rule); hover deepens to coral-dark #9A3412 (**7.31:1**)
  with the underline kept. **NEW visited treatment:** no `:visited` rule
  existed, so visited links looked exactly like unvisited ones. Visited
  → #0C6B7A (**6.18:1** white / **5.49:1** sand — chosen over teal-bright
  #0E7C8C, which is 4.91:1 white but **4.36:1 on sand: a fail**).
  Buttons (worker I), table links (worker I) and details links (worker D)
  are excluded from this rule by `:not()`.
- List markers stay coral (decorative). Unchanged.

### 2.3 Breadcrumb — SEPARATOR CHANGED
- Links teal **8.42:1**, current crumb ink **15.64:1** — unchanged, both best.
- Separator "»": gold #C99B3F on white **2.55:1** — nearly invisible.
  **Proposed:** dark gold #8A6D1F, **4.90:1** — still gold, now visible.
  (Teal-dark #083F4A at 11.54:1 was the alternative; gold kept for brand.)

### 2.4 Header / nav — TWO REAL FIXES + two accents
- **REAL DEFECT (the only measured WCAG failure in the header):**
  `.nav-dropdown span.nav-current` — coral #C2410C on sand-2 #EFE7D6,
  **4.21:1**. 18px bold is normal text under WCAG (large starts at 18.66px
  bold), so it needs 4.5:1 and **fails**. **Proposed:** coral-dark #9A3412
  on sand-2, **5.94:1**. Background, weight, padding untouched.
- Dropdown link hover: coral on sand **4.60:1** (pass, thinnest on site)
  → coral-dark on sand **6.49:1**.
- **NEW:** header gold baseline — `inset 0 -3px 0 gold` added to the existing
  shadow. Zero layout change (inset shadow, no border). Frames the page
  with the footer rule in §2.5.
- **NEW:** mobile menu toggle hover — same 12% white wash as desktop nav
  (no hover state existed).
- **Measured-pass, UNCHANGED:** brand white **14.38:1**, brand-tag #B8D2D8
  **9.07:1**, nav links white **14.38:1**, current-page gold wash (white
  **10.08:1** on the true composite #34463A — the raw 2.55:1 in the probe
  was an uncomposited-alpha artefact, verified by compositing
  rgba(201,155,63,0.22) over #0A2E38), gold underline 3.96:1 (non-text),
  mobile group labels #A9C3C9 **7.76:1**, mobile links white **14.38:1**,
  mobile current white **9.37:1** on its composite #2C4B54.
  (Desktop-probe "failures" for `.nav-group` / mobile-menu links at 1440px
  are artefacts: those elements are `display:none` at desktop and the base
  rule colours never render. Mobile measurement is the true value: 7.76:1.)

### 2.5 Footer — GOLD FRAME ADDED, everything else measured-pass
- **NEW:** gold rule above the footer — `inset 0 3px 0 gold`. Zero layout
  change. Mirrors the header baseline; the page is now framed in gold.
- **Measured-pass, UNCHANGED:** column headings white **14.38:1** (gold was
  considered and rejected — three gold column headings would shout; gold
  already speaks in the brand-name span and the current-page underline),
  column links #D7E4E7 **11.05:1** (hover white + underline), current item
  white **14.38:1** + gold underline, ZIPs #A9C3C9 **7.76:1**, base text
  #D7E4E7 **11.05:1**, base phone white **14.38:1**, brand-name white +
  gold span (gold on deep **5.64:1**, large display text), footer map link
  gold-cream #FFD9A8 **10.78:1**, back-to-top white **14.38:1** with gold
  hover **5.64:1**.

### 2.6 FAQ — HOVER FIX + OPEN-STATE WASH
- Closed summary teal **8.42:1** — unchanged (already best).
- Closed-summary hover: coral on sand **4.60:1** → coral-dark on sand
  **6.49:1**, scoped to closed items only so an open summary keeps its
  teal identity (20x open state preserved).
- **NEW:** open summary gains a sand background wash (teal on sand
  **7.48:1**) so an open answer is unmistakable without reading the glyph.
  Gold left border + teal border (20x) unchanged.
- +/- glyph: white on coral **5.18:1** (open), coral glyph on white
  **5.18:1** (closed) — unchanged, passes with margin.
- Answer links: teal underlined **8.42:1** (20x D5) — unchanged; the §2.2
  rule agrees with it and adds the visited treatment.

### 2.7 Steps — BADGE GRADIENT
- Number badge: white on flat coral **5.18:1** (28px/24px display numerals,
  large text) — passes, but flat. **Proposed:** the same sunset gradient
  worker I uses on `.btn-call` (coral → coral-dark), so badges and buttons
  read as one CTA system. White on lightest point **5.18:1**, darkest
  **7.31:1**. Step titles are covered by the base H3 rule (coral-dark), so
  badge + title are now one family. Hairline between steps unchanged.

### 2.8 Map section + caption — COVERED BY §1, no extra rule
- Caption H2 → teal + gradient bar (§1). Iframe 2px gold border unchanged.
  Footer "View larger map" link unchanged (10.78:1).

### 2.9 CTA lines + last-updated — MEASURED, no rule needed
- `.cta-line` holds only worker I's buttons. `.last-updated` muted #46585F
  on white **7.44:1** — passes with margin. No change.

### 2.10 404 page — H1 CHANGED
- The 404 H1 is the ONLY deep-colour H1 on the site (every other H1 sits
  white on the hero). Deep #0A2E38 **14.38:1** → river teal #0B5563
  **8.42:1**, so the error page reads as part of the H2 system instead of
  an unstyled default. Paragraph links covered by §2.2; buttons are
  worker I's.

### 2.11 Selection + focus — NEW
- No `::selection` rule existed. **Proposed:** gold background + deep text
  (**5.64:1**), readable selected text in the brand palette.
- **NEW global `:focus-visible`:** 3px gold outline, 2px offset — a safety
  net for plain links, whose only focus cue today is the browser default.
  Stronger rings already win on specificity and are untouched:
  `.btn:focus-visible` (worker I — white ring + coral outer ring),
  `.skip-link:focus` (coral bg + gold outline), FAQ `summary:focus-visible`
  (gold outline). Honest caveat: gold vs white is 2.55:1 as a colour, and
  WCAG 2.4.11 wants 3:1 for the focus indicator against adjacent colours —
  if the coordinator wants the strict reading, swap gold for #8A6D1F
  (4.90:1 on white) in that one rule; the trade-off is a less golden ring.

### 2.12 Hero — AUDIT ONLY (Task 1 owns the implementation)
- **Hero text colours: NO CHANGE.** Where the text actually sits (left
  ~46%, scrim 0.93–0.80 over the deep gradient): H1 white **16.87:1**,
  intro #EEF4F5 **15.18:1**, intro link gold-cream #FFD9A8 **12.64:1**,
  areas line #CFE0E4 **12.40:1** (composites computed against scrim-left
  #062028; the probe's raw 1.00:1 figures were the transparent-background
  artefact — the hero has a gradient, not a flat background).
- **The risk is the right edge once a photo lands:** current scrim ends at
  0.38 alpha; over a pure-white photo the composite is #A0AAAD and white
  text would fall to **2.37:1**. No text sits there today, but any bright
  photo + text drift would fail.
- **Proposed scrim (colour numbers only, for Task 1):** right stop 0.38 →
  **0.70**, left/mid stops unchanged
  (`100deg, rgba(6,32,40,0.93) 0%, rgba(6,32,40,0.80) 46%,
  rgba(6,32,40,0.70) 100%`). Worst case over a pure-white photo the
  composite is #516369: white text **6.29:1**, gold-cream intro link
  **4.72:1**, areas line **4.62:1** — every hero text colour passes 4.5:1
  even in the worst case, while 30% of the photo still shows. 0.60 was
  measured too (white 4.52:1) but leaves the gold-cream link at 3.39:1,
  so 0.70 is the value that covers ALL hero text. The left 46% where the
  text sits is pixel-identical to today.
- The commented-out rule is at the end of the snippet file, marked
  DO NOT APPLY — hand it to Task 1.
- Note: `.hero-areas` has NO links on any page (plain text + "·"
  separators, verified across `out/*.html`) — the `.hero-areas a` rule in
  styles.css is dead code. Left alone; not deleted in a colour round.

---

## 3. CONTRAST TABLE — HIGHLIGHTS (before → after)

| Pair | Before | After | Bar |
|---|---|---|---|
| H2 teal #0B5563 / white | 14.38:1 (deep) | **8.42:1** | 4.5:1 ✓ |
| H2 teal / sand | — | **7.48:1** | 4.5:1 ✓ |
| H3 coral-dark #9A3412 / white | 14.38:1 (deep) | **7.31:1** | 4.5:1 ✓ |
| H3 coral-dark / sand-2 | — | **5.94:1** | 4.5:1 ✓ |
| Body link teal / white | 8.42:1 | 8.42:1 + underline | 4.5:1 ✓ |
| Body link vs surrounding ink | 1.86:1 (colour-only) | underline cue added | 3:1 cue ✓ |
| Visited #0C6B7A / white | (no rule — same as link) | **6.18:1** | 4.5:1 ✓ |
| Visited #0C6B7A / sand | — | **5.49:1** | 4.5:1 ✓ |
| Breadcrumb sep #8A6D1F / white | 2.55:1 (gold) | **4.90:1** | 4.5:1 ✓ |
| Dropdown current coral-dark / sand-2 | **4.21:1 FAIL** (coral) | **5.94:1** | 4.5:1 ✓ |
| Dropdown hover coral-dark / sand | 4.60:1 (coral) | **6.49:1** | 4.5:1 ✓ |
| FAQ hover coral-dark / sand | 4.60:1 (coral) | **6.49:1** | 4.5:1 ✓ |
| FAQ open summary teal / sand wash | (white bg) | **7.48:1** | 4.5:1 ✓ |
| Step badge white / gradient | 5.18:1 (flat coral) | **5.18–7.31:1** | 3:1 large ✓ |
| Nav current white / composite #34463A | 10.08:1 | unchanged | 4.5:1 ✓ |
| 404 H1 teal / white | 14.38:1 (deep) | **8.42:1** | 3:1 large ✓ |
| Selection deep / gold | (browser default) | **5.64:1** | 4.5:1 ✓ |
| Hero H1 white / scrim-left | 16.87:1 | unchanged | 3:1 large ✓ |
| Hero worst-case white / scrim-right (white photo) | 2.37:1 (0.38 stop) | **6.29:1** (0.70 stop, proposal) | 4.5:1 ✓ |

Full per-element measured table (all 12 runs): `/tmp/colour-sitewide/measured.json`.

---

## 4. RECONCILIATION TABLE (section → owner → my action)

| Section | Owner | My action |
|---|---|---|
| Base H2/H3 (all pages, incl. H2 bar) | **Me** | **Changed** — H2 teal, H3 coral-dark, gradient bar |
| Details card (incl. its H2, sub, dt) | Worker D | **Left to owner** — excluded via `:not()`; measured only (H2 deep 12.77:1 on sand, sub muted 6.61:1, dt teal-dark 10.25:1 — all pass) |
| Tables + buttons (+ call bar) | Worker I | **Left to owner** — excluded via `:not(.btn)` / `:not(.table-wrap a)`; no table/button rule in my snippet. (Worker I's snippet already proposes coral-dark hover text and a coral→coral-dark button gradient; my step-badge gradient and FAQ/dropdown coral-dark hovers harmonise with it.) |
| Kind cards incl. text over images | Worker F | **Left to owner** — kind H3 excluded via `:not()`; measured only (deep 14.38:1) |
| Help cards | Worker E | **Left to owner** — no `.help-card` selector exists in the current build (verified); nothing to exclude, nothing changed. If E introduces the class, add it to my `:not()` lists (see snippet note S3). |
| Area cards | Worker G | **Left to owner** — no `.area-card` selector exists in the current build (verified); same note as help cards. (The Areas page itself has no card grid yet — its H2/H3 fall under my base rules.) |
| Hero images / scrim | Task 1 + coordinator | **Audit-only** — text colours pass, scrim right-stop 0.38 → 0.70 proposed with numbers; commented-out rule in the snippet, DO NOT APPLY here |
| Header / nav colours | **Me** | **Changed** — dropdown current fix (4.21→5.94:1), dropdown hover, header gold baseline, mobile toggle hover; rest measured-pass, unchanged |
| Footer colours | **Me** | **Changed** — gold top rule only; all text/links measured-pass, unchanged |
| Breadcrumb | **Me** | **Changed** — separator gold → dark gold (2.55→4.90:1) |
| FAQ | **Me** | **Changed** — closed-hover colour, open sand wash; summary/answer/glyph colours unchanged (already best) |
| Map section + caption | **Me** | **Changed** — caption via base H2; iframe border + footer map link unchanged |
| Steps | **Me** | **Changed** — badge gradient; titles via base H3 |
| CTA lines / last-updated | **Me** | **Measured, no change** — last-updated 7.44:1; buttons are worker I's |
| Body links (default/hover/visited) | **Me** | **Changed** — underline added, hover deepened, visited #0C6B7A added |
| Back-to-top | **Me** | **Measured, no change** — white 14.38:1, gold hover 5.64:1 |
| 404 page | **Me** | **Changed** — H1 deep → teal (8.42:1) |
| Selection / focus | **Me** | **Changed** — new gold selection (5.64:1) + global gold focus ring (caveat in §2.11) |
| Skip link | 20x D2 (kept) | **Measured, no change** — white on coral 5.18:1, gold outline; focus visible 238×58 in probe |

---

## 5. TEXT SIZE — CONFIRMATION

**Body text stays 20px. No text-size rule in the snippet: `grep -c "font-size"
qa/css-snippet-colour-sitewide.css` returns 0.** The snippet changes colours
(and two inset box-shadows + one gradient background, all zero-layout) and
nothing else. H1/H2/H3 sizes are untouched (58/42/26px desktop, 40/31/23px
mobile — measured, unchanged). No padding/margin/width changes anywhere in
the snippet; the only non-colour declarations are the two inset gold rules
(header baseline, footer top rule — box-shadow, zero layout change) and the
step-badge gradient (background only). No word changes, no layout changes, no
invented content.

## 6. DELIVERABLES

- `qa/css-snippet-colour-sitewide.css` — complete CSS for my sections
  (18 rules, braces balanced 18/18, 0 text-size declarations). Apply AFTER
  the other workers' snippets; specificity notes S1–S5 in the file header.
- `qa/FINDINGS-colour-sitewide.md` — this file.

## 7. OPEN / FOR THE COORDINATOR

- Apply + re-screenshot: the H2 teal / H3 coral-dark pairing needs one real
  visual look at a full page (my probe screenshots show the BEFORE state
  only — this is a proposal, never applied). If the coral-dark H3 reads too
  loud at 26px Archivo Black across a whole page, the fallback is H3 in
  teal-dark #083F4A (11.54:1 white) with H2 staying teal — hierarchy is
  then carried by size + the gradient bar alone.
- The global gold `:focus-visible` ring carries the 2.4.11 caveat in §2.11
  (gold/white 2.55:1); swap to #8A6D1F if the strict reading is wanted.
- The hero scrim proposal (0.70 right stop) belongs to Task 1 — do not apply
  it from this file.
- Temp server on :8137 stopped after probing; probe artefacts remain in
  `/tmp/colour-sitewide/` (measurements + 8 screenshots).
