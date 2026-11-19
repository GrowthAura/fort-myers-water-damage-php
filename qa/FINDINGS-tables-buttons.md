# TASK 11 — Table + Button Colouring: findings

Owner's words: "tables ke andar ki colouring piyari kro, eye attractive kro;
buttons ki colouring piyari kro". Proposal files only — **no shared file was
edited** (no `styles.css`, `functions.php`, data file or header change; no
commit, no push). The coordinator applies
`qa/css-snippet-tables-buttons.css`, re-runs overflow + `/cost/` table checks,
and screenshots it.

## Sources read before designing

- `site/assets/css/styles.css` — theme variables (`:root`), button rules
  (lines 84–96), table rules (lines 249–272), the 20x D-V1 responsive block
  (lines 393–397), `.call-bar` (lines ~381–388).
- `qa/FINDINGS-20x.md` D-V1 section — the cost-table constraint (below).
- Live export `out/cost/index.html` — 6 tables: 3× `.table-wrap.prices`
  ("Size of the job", "What is being priced", "Repair after water damage")
  + 3× plain `.table-wrap` (water category, damage class, estimate line
  items, waiting). Price tables are 2–3 columns; prose tables up to 4.
- Button usage: `.btn-call` everywhere (header, hero, `.cta-line`, footer);
  `.btn-ghost` on home hero ("Describe your water problem") + 404 page;
  `.btn-ghost-dark` defined in CSS (used on 404); `.call-bar` sticky mobile
  call bar (≤620px).

## Design idea (Caloosahatchee theme, colour only)

- **Tables:** the header becomes the deep river (`#0A2E38`) with a gold
  baseline, the zebra deepens from sand to sand-2 so the stripe is actually
  visible, the first column becomes bold deep-teal labels, and the price
  column gets its own pale-gold tint + bold deep-teal figures with a gold
  header — so prices scan as a column instead of hiding in the prose.
- **Buttons:** the call button becomes a sunset gradient (coral → coral-dark)
  with a 3px gold baseline; the ghost button on dark backgrounds gets a gold
  border + gold wash and flips to solid gold on hover; the light ghost gets a
  faint teal wash and a teal-gradient hover with the same gold baseline; the
  sticky mobile call bar gets the same sunset gradient as `.btn-call`.
- **New:** a `:focus-visible` ring for `.btn` / `.call-bar` — none existed
  before (only the skip link and FAQ summaries had one).

## Before / after colour table

### Tables

| Element | Before | After | Why |
|---|---|---|---|
| `th` background | teal `#0B5563` | deep `#0A2E38` | river-deep header, matches header/footer |
| `th` text | white `#FFFFFF` | white `#FFFFFF` (unchanged) | — |
| `th` bottom accent | none | 3px gold `#C99B3F` (inset box-shadow, zero height change) | sunset line under the header |
| `th + th`, `td + td` | no vertical separator | 1px `#E7DFCF` left border (F1, flagged) | column scanning |
| Even-row zebra | sand `#F6F1E7` | sand-2 `#EFE7D6` | stripe actually visible |
| Odd rows | white (unchanged) | white (unchanged) | — |
| `td:first-child` (label col) | ink `#12262E`, weight 400 | teal-dark `#083F4A`, weight 700 (F2, flagged) | label → detail reading |
| Row hover | none | `#EDE5D3` wash | row lifts under pointer |
| `.prices td:last-child` (odd) | ink, weight 400, no tint | teal-dark `#083F4A`, weight 700, `#FDF8EC` pale-gold tint | money column stands out |
| `.prices td:last-child` (even) | ink, sand zebra | teal-dark, weight 700, `#F4EAD2` deeper gold tint | tint survives the zebra |
| `.prices td:last-child` (hover) | — | `#EFE0B9` richest gold tint | hover follows the price column |
| `.prices th:last-child` | white | gold `#C99B3F` | money column signalled in the header |
| `td` top border | `#DCD5C6` (unchanged) | `#DCD5C6` (unchanged) | — |

### Buttons

| Element | Before | After | Why |
|---|---|---|---|
| `.btn-call` background | flat coral `#C2410C` | gradient `#C2410C → #A83A10 → #9A3412` | sunset depth, still ≥4.5:1 everywhere |
| `.btn-call` shadow / base | `0 6px 18px rgba(194,65,12,.35)` | same glow (`.38`) + inset 3px gold baseline | gold sunset edge |
| `.btn-call:hover` | flat coral-dark `#9A3412` | gradient `#9A3412 → #7C2D12`, stronger glow, gold baseline kept | hover deepens instead of just darkening |
| `.btn-ghost` background | `rgba(255,255,255,0.08)` | `rgba(201,155,63,0.16)` gold wash | reads as the sunset secondary action |
| `.btn-ghost` border | white `#FFFFFF` | gold `#C99B3F` | gold frame on dark hero |
| `.btn-ghost:hover` | `rgba(255,255,255,0.2)`, white text | solid gold `#C99B3F`, deep `#0A2E38` text | button "lights up" |
| `.btn-ghost-dark` background | transparent | `rgba(11,85,99,0.06)` teal wash | faint teal tint on light bg |
| `.btn-ghost-dark:hover` | flat teal `#0B5563`, white text | gradient teal → teal-dark + inset 3px gold baseline | matches `.btn-call` treatment |
| `.call-bar` background | flat coral `#C2410C` | gradient `#C2410C → #9A3412` | one CTA system with `.btn-call` |
| `.call-bar:hover` | (no hover rule) | gradient `#9A3412 → #7C2D12` | — |
| `.btn` / `.call-bar` focus | **no focus style existed** | white 3px outline + 5px coral ring | visible on light AND dark backgrounds |

## WCAG contrast ratios — all computed (relative-luminance formula, Python)

Every text/background pair below is **≥ 4.5:1 (WCAG AA, normal text)**.
The worst case of each gradient is its lightest point; that is the number
reported.

### Tables

| Text | On background | Ratio | Pass |
|---|---|---|---|
| white `#FFFFFF` (header text) | deep `#0A2E38` (new header) | **14.38:1** | ✓ (was 8.42:1 on old teal header) |
| gold `#C99B3F` (price header) | deep `#0A2E38` | **5.64:1** | ✓ |
| ink `#12262E` (body text) | white (odd rows) | **15.64:1** | ✓ |
| ink `#12262E` | sand-2 `#EFE7D6` (new zebra) | **12.72:1** | ✓ (was 13.90:1 on old sand — slightly lower, still 2.8× the bar) |
| ink `#12262E` | hover wash `#EDE5D3` | **12.48:1** | ✓ |
| teal-dark `#083F4A` (label col / price) | white | **11.54:1** | ✓ |
| teal-dark `#083F4A` | sand-2 `#EFE7D6` (zebra) | **9.38:1** | ✓ |
| teal-dark `#083F4A` | price odd `#FDF8EC` | **10.89:1** | ✓ |
| teal-dark `#083F4A` | price even `#F4EAD2` | **9.64:1** | ✓ |
| teal-dark `#083F4A` | price hover `#EFE0B9` | **8.81:1** | ✓ |
| ink `#12262E` | price odd `#FDF8EC` | **14.76:1** | ✓ |
| ink `#12262E` | price even `#F4EAD2` | **13.07:1** | ✓ |
| teal `#0B5563` (in-cell links, unchanged) | sand-2 `#EFE7D6` | **6.85:1** | ✓ |
| teal `#0B5563` (in-cell links) | price even `#F4EAD2` | **7.04:1** | ✓ |

Deliberately NOT used for text: white on gold `#C99B3F` = **2.55:1** — gold
is used only for borders, baselines and backgrounds behind deep text
(deep on gold = 5.64:1), never behind white text.

### Buttons

| Text | On background | Ratio | Pass |
|---|---|---|---|
| white (`.btn-call` label) | coral `#C2410C` (gradient top — lightest point) | **5.18:1** | ✓ |
| white | coral-dark `#9A3412` (gradient base) | **7.31:1** | ✓ |
| white (`.btn-call:hover`) | coral-dark `#9A3412` (hover top) | **7.31:1** | ✓ |
| white (`.btn-call:hover`) | `#7C2D12` (hover base — darkest) | **9.37:1** | ✓ |
| white (`.btn-ghost`) | gold-wash composite `#293F39` over deep hero | **11.26:1** | ✓ |
| deep `#0A2E38` (`.btn-ghost:hover`) | gold `#C99B3F` | **5.64:1** | ✓ |
| teal `#0B5563` (`.btn-ghost-dark`) | white | **8.42:1** | ✓ (unchanged) |
| teal `#0B5563` (`.btn-ghost-dark`) | teal-wash composite `#F0F5F6` | **7.66:1** | ✓ |
| white (`.btn-ghost-dark:hover`) | teal `#0B5563` (gradient top) | **8.42:1** | ✓ |
| white (`.btn-ghost-dark:hover`) | teal-dark `#083F4A` (gradient base) | **11.54:1** | ✓ |
| white (`.call-bar`) | coral `#C2410C` (gradient top) | **5.18:1** | ✓ |
| white (`.call-bar:hover`) | `#7C2D12` (darkest) | **9.37:1** | ✓ |

### Focus indicator (non-text, 3:1 bar)

| Ring | Against | Ratio | Pass |
|---|---|---|---|
| coral `#C2410C` ring | white page background | **5.18:1** | ✓ |
| white `#FFFFFF` ring | deep `#0A2E38` hero/header | **14.38:1** | ✓ |
| (gold was rejected as the focus colour: gold on white = 2.55:1) | | | |

Note on the coral gradient: a brighter coral top (e.g. `#D14D0F`) was
considered and **rejected** — white on it measures 4.40:1, below AA. The
gradient therefore tops out at the existing `#C2410C` (5.18:1); the
"richer" feel comes from the depth of the gradient + gold baseline, not
from a brighter coral.

## Cost-table mobile rules — UNTOUCHED (explicit confirmation)

The 20x D-V1 constraint, from `qa/FINDINGS-20x.md` Part 1: on mobile the
`white-space: nowrap` on `.table-wrap.prices td:last-child` forced table 1
to 550px and table 3 to 616px inside a 390px wrap and hid the entire price
column at first paint. The fix moved nowrap into
`@media (min-width: 621px)`; the base rule keeps only `text-align: right`,
so prices wrap on mobile (table 1: 390px, prices visible; table 3: 390px).

This proposal touches **none** of that:

- No `white-space` property appears anywhere in the snippet.
- No `padding`, `margin`, `width`, `font-size` or `line-height` change
  anywhere in the snippet.
- `.table-wrap.prices td:last-child { text-align: right }` is not
  re-declared and not overridden — right-alignment survives as-is.
- The `@media (min-width: 621px)` nowrap block is not re-declared and not
  overridden — desktop nowrap + mobile wrapping both survive as-is.
- `.table-wrap { overflow-x: auto }`, its border, radius and right-edge
  fade are not re-declared.
- The only two non-pure-colour adjustments are flagged in the snippet
  (F1: 1px column separators; F2: bold first column). Neither can create
  overflow: the table is `width: 100%` with `border-collapse: collapse`
  (borders compress content, they do not widen the table), cells wrap,
  and `.table-wrap` already scrolls horizontally as a safety net.
- The price-column tint is a `background` on `td` only — it cannot change
  any cell's size.

Coordinator re-checks after applying: `/cost/` tables at 390px (all 3
price tables 390px wide, prices visible at first paint, wrapping) and
desktop (1190px, nowrap, right-aligned), plus overflow 0 sitewide.

## What the coordinator must verify (screenshot)

1. `/cost/` desktop + 390px: header deep teal + gold baseline, zebra
   visible, price column gold-tinted with bold deep-teal figures, gold
   price header, prices wrapping on mobile, no overflow.
2. Home hero desktop + 390px: `.btn-call` sunset gradient + gold baseline,
   `.btn-ghost` gold-bordered ("Describe your water problem"), sticky call
   bar gradient on mobile.
3. Tab-focus a `.btn-call` on a light page and on the dark hero: white +
   coral double ring visible in both cases.
4. Overflow 0 at 320 / 390 / 768 / 1440 (the snippet changes no geometry,
   but the F1/F2 flags deserve the re-measurement).

## Deliverables

- `qa/css-snippet-tables-buttons.css` — complete drop-in snippet with
  apply instructions and the F1/F2 flags inline.
- `qa/FINDINGS-tables-buttons.md` — this file.
