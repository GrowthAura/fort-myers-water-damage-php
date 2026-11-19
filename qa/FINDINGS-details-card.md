# FINDINGS — Details card beautification (Task 2, Fort Myers PHP site)

Date: 2026-11-19. Designer proposal only — **no shared file was edited**
(no `styles.css`, `functions.php`, data file, header, commit or push).
The coordinator applies the two proposal files and screenshots the result.

Deliverables (all under `~/workspace/fort-myers-php/qa/`):
- `css-snippet-details.css` — complete replacement CSS for the section.
- `patch-details-functions.txt` — exact old code + exact new code for `functions.php`.
- `FINDINGS-details-card.md` — this file.

## 1. What the card actually is (measured, not assumed)

- **26 pages** carry a `'details'` block — exactly one block per file
  (verified by grepping every `site/data/*.php`; `grep -rln "'type' => 'details'"`
  returns 26 files). The brief's "26 pages" is correct.
- **181 rows total, 100 distinct labels.** The homepage's 6 rows
  (Phone / Service area / Services / Properties / Typical drying time /
  What you keep) are only the homepage — every service page has different
  rows (e.g. water-removal: Phone / What it covers / Extraction time /
  Drying after extraction / Service area; cost: 9 rows, the longest card).
- Trap avoided: a naive `grep "'label'"` over all data files also matches
  nav labels in `site/data/pages.php` ("AC Leak Water Damage", "About Us",
  …). Those are **not** details rows. The inventory below was extracted
  from `'type' => 'details'` blocks only, and the expected-icon map was
  cross-checked against that inventory (100/100, zero missing, zero extra).
- Sub labels vary too: "Details" on 10 pages, "What to know" on 15,
  "Rough area idea" on /cost/, and a full question on /insurance/
  ("Usually covered by homeowners insurance?"). The eyebrow treatment
  below works for all of them — it styles the text, never replaces it.
- The section contains **no H3 anywhere** (renderer emits only `h2` +
  `p.details-sub` + `dl` on all 26 pages). The brief's "fix the H2/H3
  colour in this section" is therefore satisfied by the H2 treatment
  in §3; there is no H3 to fix here.

### Per-file inventory (rows + card heading, verbatim from data files)

| File | Rows | Card heading |
|---|---|---|
| homepage.php | 6 | Fort Myers water damage help |
| ac-leak.php | 6 | Fort Myers AC leak damage |
| appliance-leak.php | 8 | Appliance leak in a Fort Myers home |
| bonita-springs.php | 7 | Water damage in Bonita Springs |
| burst-pipe.php | 8 | Burst pipe in a Fort Myers home |
| cabinets.php | 8 | Water damaged cabinets in a Fort Myers home |
| cape-coral.php | 7 | Cape Coral water damage |
| cast-iron-pipe.php | 6 | Cast iron leaks in Lee County |
| ceiling-leak.php | 6 | Fort Myers ceiling leaks |
| commercial.php | 8 | Commercial water damage in Fort Myers |
| condo-leak.php | 6 | Fort Myers condo leaks |
| cost.php | 9 | Water damage pricing in Fort Myers |
| drying.php | 6 | Fort Myers structural drying |
| estero.php | 7 | Water damage in Estero |
| flood-cleanup.php | 7 | Flood cleanup in a Fort Myers home |
| floors.php | 8 | Water damaged floor in a Fort Myers home |
| fort-myers-beach.php | 7 | Water damage on Fort Myers Beach |
| insurance.php | 7 | Fort Myers water damage |
| lehigh-acres.php | 7 | Lehigh Acres water damage |
| mobile-home.php | 7 | Mobile home water damage in Fort Myers |
| north-fort-myers.php | 7 | Water damage in North Fort Myers |
| sewage-cleanup.php | 6 | Fort Myers sewage cleanup |
| slab-leak.php | 8 | Slab leak in a Fort Myers home |
| vacant-home.php | 6 | Seasonal homes in Lee County |
| water-heater-leak.php | 8 | Water heater leak in a Fort Myers home |
| water-removal.php | 5 | Fort Myers water removal |

## 2. Current state (what is being replaced)

- `site/assets/css/styles.css` ~226–240: sand background, 1px `var(--line)`
  border, **6px coral left border**, 14px radius, 36/40px padding.
  `.details-grid` is `240px 1fr` with `.detail-row { display: contents; }`
  (so rows cannot have hover states); `dt` is bold `var(--teal-dark)`;
  `.details-sub` is 16px muted small-caps **below** the H2.
- `site/includes/functions.php` `case 'details':` (lines 258–265) renders
  plain `<dt>label</dt><dd>value</dd>` rows — no icons, no spans.
- Base `.page-body h2::before` paints a **coral 72×6px bar** above every
  H2; the card currently kills it with `.details-card h2::before
  { display: none; }` — that kill is kept (see §3).
- Base `a:hover` is coral sitewide, and Phone-row values render as
  `tel:` links — so without a scoped override the phone link would
  still flash orange on hover inside this "orange-free" section.
  The snippet overrides it (teal-dark + underline).

## 3. Design rationale + H2 treatment (design freedom used)

The Caloosahatchee theme's river-teal family carries the card; gold is
used once, decoratively; the sunset accent is removed entirely.

- **Card frame:** sand background kept (it is the theme's paper, and the
  screenshot's sand is what the owner recognised). The 6px coral left
  bar becomes a **6px deep-teal (`var(--deep)`) left bar** — the same
  deep teal as the header, so the card reads as part of the site chrome
  rather than a warning strip. 1px `var(--line)` border, 16px radius,
  soft `0 10px 30px rgba(10,46,56,.10)` shadow.
- **H2 — best stylish:** deep river teal `#0A2E38` in the inherited
  Archivo Black (size unchanged: 42px desktop / 31px mobile, so no
  other heading scale is disturbed). The "DETAILS" sub is lifted
  **above** the H2 visually as the eyebrow — teal-dark, 15px, 700,
  0.18em letter-spacing, uppercase — with a short **44×4px gold bar**
  before it. This is the classic eyebrow + display-heading pairing:
  the small gold rule gives the "stylish" cue, the deep-teal H2 gives
  the authority, and no colour in the header drops below 10:1.
  The eyebrow move is CSS-only (`order: -1` on a flex column): DOM
  order stays h2-then-sub, so screen readers and crawlers still meet
  the heading first, and **zero words move**.
- **Rows:** hairline-separated list (hairline above the list, one under
  each row). Each row is now a real grid row (250px label / 1fr value)
  instead of `display: contents`, so hover works: the row washes white
  and its icon disc fills deep teal with a white glyph. `dt` stays
  teal-dark bold; `dd` stays ink. Label text sits on a 5px top pad so
  it optically centres on the 40px disc.
- **Icons:** 22px stroke glyphs (Feather / Lucide style, MIT/ISC) in a
  40px pale-teal disc (`#E0EBED`, scoped as `--details-tint` on
  `.details-card` itself so `:root` needs no edit). Stroke is
  `currentColor`, so the icon inherits the disc's teal and turns white
  on hover with it. Icons are decorative (`aria-hidden="true"` on the
  SVG); the label text always carries the meaning, so a failed or
  unloaded icon loses nothing. The phone icon is a stroke handset,
  **not** the filled `phone_svg()` used in CTAs — deliberately, so all
  36 card icons share one stroke weight and look like a set.
- **Scope discipline:** every selector is `.details-card …` /
  `.detail-row …` / `.detail-icon …`. No sitewide heading, link or
  list rule is touched. The only cross-cutting change is inside the
  card: link hover/focus colours (teal-dark / teal outline) overriding
  the coral base `a:hover` *within this section only*.

## 4. Colours + measured WCAG contrast ratios

Computed from relative luminance (WCAG 2.x formula), script-run, not
estimated. Text needs ≥ 4.5:1; non-text (icons, focus ring) needs ≥ 3:1.

| Element | Foreground | Background | Ratio | Pass |
|---|---|---|---|---|
| H2 | deep `#0A2E38` | sand `#F6F1E7` | **12.77:1** | ✓ AAA |
| dt label | teal-dark `#083F4A` | sand | **10.25:1** | ✓ AAA |
| dd value | ink `#12262E` | sand | **13.90:1** | ✓ AAA |
| Eyebrow (.details-sub) | teal-dark `#083F4A` | sand | **10.25:1** | ✓ AAA |
| Link in dd (tel:) | teal `#0B5563` | sand | **7.48:1** | ✓ AAA |
| Link hover | teal-dark `#083F4A` | sand | **10.25:1** | ✓ AAA |
| Icon stroke | teal `#0B5563` | disc tint `#E0EBED` | **6.93:1** | ✓ (needs 3:1) |
| Icon stroke (hover disc) | white `#FFFFFF` | deep `#0A2E38` | **14.38:1** | ✓ |
| Focus outline | teal `#0B5563` | sand | **7.48:1** | ✓ (needs 3:1) |
| H2 / dt / dd on hover-row white | as above | white `#FFFFFF` | 14.38 / 11.54 / 15.64 :1 | ✓ AAA |
| Gold `#C99B3F` on sand | — | sand | **2.26:1** | ✗ for text — **decorative only** |

**Gold caveat (deliberate):** gold on sand is 2.26:1, so gold is used
only for the 44×4px eyebrow bar — a decorative shape, never text.
No text in the section uses gold. (Gold on deep teal is 5.64:1, but
that combination is not used either; it is recorded here only so a
future tweak does not have to re-measure it.)

## 5. Icon map — every label (100 distinct, 181 rows)

One keyword matcher, `details_icon($label)`, covers all 100 labels
with 36 glyphs; unknown future labels fall back to the `info` glyph
(the fallback is never hit by any current label — verified 100/100,
§7). Order matters: specific phrases are checked before the generic
words inside them (e.g. "drying time" → clock before "drying" → wind;
"flood insurance" → shield before "flood cut" → ruler;
"Who issues permits" → file-text before "Who…" → users).

- **phone** (3) — Phone; Most common calls; Your real number
- **map-pin** (7) — Service area; ZIP code; ZIP codes; Location;
  Land-lease communities; Where heaters sit here; Where it's common
- **droplet** (7) — Services; Water category; Water and sewer;
  What's usually wet; Irrigation; Small leak caught fast;
  Burst supply line, failed water heater, AC overflow
- **home** (4) — Properties; Homes; Common homes; Elevated homes
- **clock** (7) — Typical drying time; Drying time; Typical time;
  Extraction time; Typical tank life; Slow leak that ran for weeks
  or months; What changes after weeks of water
- **camera** (1) — What you keep (value is photos + moisture logs,
  so the camera beats the shield-check alternative in the brief)
- **shield-check** (3) — Insurance; Insurance in short; Flood insurance
- **check-circle** (5) — What it covers; What the work covers;
  What usually stays; What can often be saved; When it's done
- **alert-triangle** (7) — Biggest danger; Biggest risks;
  Homes most at risk; Mold from a covered leak;
  Sewage backup (Category 3); Sewage or drain backup; What usually fails
- **wind** (4) — Drying after extraction; Drying method;
  What drying involves; What gets dried
- **file-text** (4) — Who issues permits; Permits and the 50% rule;
  Records; What helps your claim
- **users** (8) — Who fixes what; Who fixes the source;
  Who finds and fixes the leak; Who does what; Who clears the pipe;
  Who is usually involved; Who to notify; What each owner gets
- **search** (5) — How it's confirmed; Quickest check;
  Where the water goes; Where the water hides; Where water hides
- **tool** (4) — Equipment; Repair options; Before tear-out;
  The broken pipe, AC unit or water heater itself
- **target** (3) — Most common cause; Most common causes here;
  Most common sources
- **tag** (1) — Most jobs, from water removal to dry
- **square** (1) — One room
- **layers** (2) — Before new flooring; Two or three rooms
- **building** (2) — Condos; Condo or high-rise unit
- **eye** (1) — Telltale sign
- **arrow-right** (2) — First move; First moves
- **arrow-up** (1) — What usually comes up
- **move** (1) — How far it spreads
- **trash-2** (1) — What comes out
- **refresh-cw** (1) — What usually gets replaced
- **cloud-rain** (2) — Roof leak after wind damage; Storm flooding
- **waves** (4) — River water; Saltwater surge; Drainage;
  Rising water, storm surge, canal overflow
- **ruler** (1) — Flood cut height
- **scale** (1) — Florida law
- **percent** (1) — 50% rule
- **calendar** (1) — Empty season
- **coffee** (1) — Restaurants (commercial food-service row)
- **briefcase** (1) — Staying open (business continuity)
- **log-in** (1) — Before going in
- **help-circle** (1) — Can the floor be dried?
- **life-buoy** (1) — Help
- **info** (fallback, 0 current labels) — any future label

Judgement calls worth knowing: "Staying open" gets a briefcase, not a
clock, because the row is about the business staying trading, not a
duration; "Homes most at risk" gets the warning triangle, not the
house, because the risk is the point of the row; "Most common calls"
gets the phone (it is a calls row), while "Most common cause/sources"
get the target (finding the cause); "What you keep" gets the camera
because its value is literally photos + moisture logs.

## 6. Mobile behaviour (390px, inside existing `@media (max-width: 620px)`)

- Card padding 28px 22px (unchanged from the old mobile rule), left
  bar 5px, radius 14px.
- Rows collapse to one column: icon + label on top, value below.
  The icon disc stays 40px (aligned left, never shrunk or hidden);
  the value is indented 54px (40px disc + 14px gap) so value text
  aligns with label text, never under the icon.
- Eyebrow 14px / 0.16em, gold bar 36px. H2 size is inherited from the
  base mobile rule (31px) — not restated here.
- Tap targets: the only tappable things in the card are the `tel:`
  links in Phone rows; they keep the site's 20px text and gain the
  teal focus outline. Icon discs are decorative, not buttons.
- `prefers-reduced-motion: reduce` disables the row/disc transitions.
- No horizontal overflow is introduced: the widest fixed pieces are
  the 40px disc and the 250px desktop label column (mobile is 1fr).

## 7. No-orange proof + verification performed

- Grep over both proposal files (all text, rules and comments):
  `grep -rniE "coral|orange|#c2410c|#e8590c|#9a3412"
  qa/css-snippet-details.css qa/patch-details-functions.txt`
  → **0 hits**. The words do not appear even in comments (the comments
  say "sunset accent" / "old accent" instead), so a naive grep by the
  coordinator also returns zero. The old coral is referenced only in
  this findings file and in the live `styles.css` the snippet replaces.
- **Icon test — 100/100, 0 failures.** The helper in the patch file
  is byte-identical to the copy tested by `php
  /tmp/details-icon-helper.php` against all 100 real labels with an
  expected-icon map (`/tmp/details-labels-expected.json`, cross-checked
  against the data files: 100 distinct, zero missing, zero extra).
  It also asserts every emitted SVG carries `aria-hidden="true"`,
  `stroke="currentColor"` and exactly one `<svg>` tag. First run caught
  13 harness-fingerprint mismatches (not helper bugs); after fixing
  the harness fingerprints the run is clean, exit 0. (The unused `zap`
  glyph was removed from the helper during this test.)
- **Patch integrity.** The OLD code block in the patch file is
  byte-identical to live `functions.php` lines 258–265 (verified by
  script), and the helper in the patch is byte-identical to the tested
  helper. The patch was applied to a `/tmp` copy of `functions.php`:
  `php -l` passes (no syntax errors), and a live render of a
  water-removal details block through the patched copy outputs the
  expected markup — phone → phone SVG, What it covers → check-circle,
  Extraction time → clock, Drying after extraction → wind,
  Service area → map-pin — with labels, values and the auto `tel:`
  link byte-identical to the old renderer's output.
- **Zero word changes.** Labels, values, headings and subs still pass
  through `esc()` / `render_segments()` untouched. The only new
  markup is `<span class="detail-icon">` + SVG and
  `<span class="detail-label">` around the already-escaped label.

## 8. Coordinator apply steps + checks

1. `functions.php`: insert `details_icon()` after `phone_svg()`
   (line 44) and replace the `case 'details':` block (lines 258–265)
   exactly as `patch-details-functions.txt` PART A / PART B say.
   Run `php -l site/includes/functions.php`, then re-run the icon
   test (`php /tmp/details-icon-helper.php` — needs
   `/tmp/details-labels-expected.json`; both are in /tmp, ask the
   designer if the VM was replaced).
2. `styles.css`: delete the old details base block (~226–240) and the
   old mobile details rules inside `@media (max-width: 620px)`
   (~463–464), paste `css-snippet-details.css` in their place
   (base block after the `.page-body h2` rules, mobile block inside
   the existing 620px query — cascade position matters, see the
   header comment in the snippet; AGENTS.md lesson: responsive
   overrides must come after their base rules).
3. Re-export and screenshot: homepage + one 5-row card
   (/water-removal/) + the 9-row card (/cost/) + one "What to know"
   card (e.g. /cape-coral/), desktop + 390px mobile. Confirm:
   word-diff 0, H2 deep teal with gold eyebrow bar, no sunset
   accent anywhere in the section (including link hover), icons
   present on every row, 0 overflow at 390px, tel: link still works.
4. Do **not** re-run the old `display: contents` assumption anywhere
   — rows are real grid rows now; any QA probe that counted on
   `dt`/`dd` being direct grid children of `.details-grid` must be
   updated to the new structure.

## 9. Open items / not done by this task

- No screenshot was taken by the designer (this subagent has no live
  browser); visual sign-off is the coordinator's step 3 above.
- The live site is untouched — proposal files only, as briefed.
- If a future data file adds a new details label, it will render with
  the `info` fallback icon until a keyword rule is added to
  `details_icon()` — by design, never a broken row.
