# FINDINGS — 10X FIX ROUND, P3s (Fix Worker)

- **Project:** `~/workspace/fort-myers-php/` — Fort Myers PHP site, 34 pages
- **Date:** 2026-11-20 ~01:20–02:05 PKT
- **Scope:** fix the remaining 4 P3s from the independent verification
  (`qa/FINDINGS-10x-round.md`, verdict NOT READY, P1 0 · P2 4 · P3 5).
  The 4 P2s + V-P3-2 (H1 orphan) were already fixed by the previous fix
  worker (`qa/FINDINGS-10x-fix.md`); nothing else touched.
- **Mode:** LOCAL ONLY. No push, no deploy, no DNS/domain changes, no git
  commit. `qa/verify_export.py` NEVER run. No export to `out/` (the final
  verifier owns the canonical export). Verification on my own PHP server
  on port 8141 (`php -S 127.0.0.1:8141 -t site site/index.php`, killed by
  PID when done) + Playwright bundled Chromium.
- **Result: all 4 P3 fixes verified.** Phone icon 44×44 at 390 AND 320,
  card body 20px/1.6 everywhere, trust-row place-line fallback gone on
  34/34 heroes, /contact/ ghost delinked with pixel-identical styling.
  102 page loads (34 pages × 1440/390/320): 200 on 34/34, H1 = 1 on
  34/34, overflow 0, 0 console errors, `styles.css?v=5` on 34/34.

## Environment note (PHP was NOT installed on this VM)

The task brief said "PHP 8.3.6 + mbstring installed". It was not: this VM
has no `php` binary anywhere (`which php`, `/usr/bin/php*`,
`/usr/local/bin/php*` all empty — a VM replacement wiped it, the same
failure AGENTS.md records for 2026-11-19). Reinstalled per the AGENTS.md
lesson: `sudo apt-get update && sudo apt-get install -y php-cli
php8.3-mbstring` — the update alone took ~12.5 min (71.3 MB at ~95 kB/s
off a slow mirror); final state verified `PHP 8.3.6` + `mbstring` in
`php -m`. No code was changed to work around the missing PHP; all
verification ran on the real PHP server as ordered.

## Files changed (3)

| File | Change |
|---|---|
| `site/assets/css/styles.css:1386, 1573, 1589, 133` | Card body 20px; phone icon 44px; ≤380px header fit; delinked-ghost cursor |
| `site/includes/functions.php:392, 789` | Trust-row fallback removed; /contact/ ghost delinked |
| `site/includes/header.php:48` | Stylesheet cache-bust `?v=4` → `?v=5` |

## FIX V-P3-1 — header phone icon 38×38 → 44×44 (at 390 AND 320)

- **File:lines:** `site/assets/css/styles.css:1573` (the ≤620px
  `.header-call-icon` rule) + `styles.css:1589` (the ≤380px block) +
  the L-9 comment at `styles.css:1558-1565` (rewritten with the measured
  fit; it still said "38x38" and "icon hidden" below 380px).
- **Before:** `width/height/min-width/min-height: 38px` at ≤620px;
  `display: none` at ≤380px, so the icon measured 38×38 at 390 and
  0×0 at 320 (bottom call bar was the only affordance at 320).
- **After:** 44px on all four properties at ≤620px; the ≤380px
  `display: none` is REMOVED, so the icon stays visible at 320 too.
  The 320px row fits by shrinking the brand + header gap only:
  `.header-inner { gap: 8px; }` and `.brand-name { font-size: 12px; }`
  at ≤380px (was 14px). No other change: menu button untouched (44px
  from the P2 fix), bottom call bar untouched.
- **Measured (Playwright, home page, live boxes):**
  - **390px:** icon **44×44** at x=266; brand 230 (x=20→250); menu
    44×54.6 at x=326→370. Row: brand 230 + icon 44 + menu 44 + 2×16px
    gaps = **350 of 350px** — exactly fits, no overlap, no overflow
    (`documentElement.scrollWidth` 390). Brand-name scrollWidth ==
    clientWidth (214) — no clipping.
  - **320px:** icon **44×44** at x=204; brand 176 (x=20→196); menu
    44×54.6 at x=256→300. Row: brand 176 + icon 44 + menu 44 + 2×8px
    gaps = **280 of 280px** — exactly fits, no overlap, no overflow
    (scrollWidth 320). Brand-name scrollWidth == clientWidth (168) —
    the 12px brand is legible and unclipped (viewed).
- **Screenshots:** `qa/screenshots-10x-fix-p3/header-390.png`,
  `header-320.png` (viewed: brand + orange icon + hamburger, clean at
  both widths).
- **No regressions:** menu button still 44×54.6 at 390/320; hero call
  button 65.2px tall at 390/1440, 58.8px at 320 (min across all pages);
  hero ghost 56–84.4px tall at mobile — all ≥44px.

## FIX V-P3-3 — kind/help card body 18px → 20px

- **File:line:** `site/assets/css/styles.css:1386` (the L-7 rule).
- **Before:** `.kind-card p { font-size: 18px; line-height: 1.55; }`
  (measured 18px on home + about, all widths).
- **After:** `.kind-card p { font-size: 20px; line-height: 1.6; }`
  (one rule covers both `.kind-card` and `.help-card`, which share the
  class; `.area-card p` has no font-size rule of its own and already
  inherited the 20px body size — verifier did not flag it, untouched).
  No colours changed, so contrast is untouched.
- **Measured (Playwright, all card grids, 1440/390/320):** every
  `.kind-card p` / `.help-card p` computes to **20px / 32px line-height**;
  0 clipped paragraphs (`scrollHeight == clientHeight`) and 0 clipped
  card boxes after a stepwise scroll-through on all 34 pages. In-view
  re-check on the home drying card: 445px tall at 390 (350 wide),
  431px at 1440 (381 wide), paragraph + card both unclipped.
- **Screenshots:** `cards-home-1440/390/320.png`,
  `cards-about-1440/390/320.png` (grids viewed),
  `help-card-drying-inview-390/1440.png` (full card text visible:
  "…moisture readings taken and logged until materials are back to
  normal."), `help-cards-about-inview-1440.png`.
- **Note (pre-existing, NOT a defect):** the /about/ help cards are
  title-only by the page's own data (each `<p>` is just the link text,
  e.g. "Emergency water removal" — verified in the DOM, pH 32/64/96 =
  1/2/3 lines). The home cards carry link + body sentence. Nothing is
  missing or clipped on /about/; the 20px bump applies to the titles
  there too. Also noted while verifying: element screenshots of tall
  grids show the sticky header/call bar painted across the stitch and
  off-screen cards at their `content-visibility` placeholder height
  (80px) — screenshot artefacts only; in-view DOM measurements are the
  record (see the drying-card in-view shots).

## FIX V-P3-4 — trust-row third item no longer falls back to the place line

- **File:lines:** `site/includes/functions.php` — `hero_trust_items()`,
  comment + fallback branch (~line 392). The `else` branch that appended
  `'Fort Myers · Lee County, FL'` is deleted; the function now returns
  only sourced items (1–3). `hero_trust_html()` is unchanged (it joins
  whatever items exist with ` · ` separators, so 1- and 2-item rows
  render cleanly).
- **Before (verifier's examples):** `/cost/`, `/burst-pipe/`,
  `/contact/` read "Answered 24/7 · Moisture readings taken · Fort Myers
  · Lee County, FL" — the third item was location info, not a trust
  signal.
- **After:** no page's trust row contains the place line. Authoritative
  list (from the renderer's own `hero_trust_items()`, re-run per page,
  then confirmed in rendered HTML on 34/34 pages at 1440/390/320):
  - **3 items, unchanged (9 pages):** `/`, `/water-removal/`,
    `/drying/`, `/ac-leak/`, `/first-hour-checklist/`, `/insurance/`,
    `/areas/`, `/commercial/`, `/how-it-works/`
    (e.g. home: "Answered 24/7 · Moisture readings taken · Written
    scope before rebuild").
  - **2 items, place line removed (20 pages):** `/sewage-cleanup/`,
    `/condo-leak/`, `/cast-iron-pipe/`, `/vacant-home/`, `/cost/`,
    `/burst-pipe/`, `/mobile-home/`, `/slab-leak/`, `/flood-cleanup/`,
    `/cape-coral/`, `/lehigh-acres/`, `/water-heater-leak/`,
    `/appliance-leak/`, `/floors/`, `/cabinets/`, `/north-fort-myers/`,
    `/fort-myers-beach/`, `/estero/`, `/bonita-springs/`, `/contact/`
    (e.g. /cost/: "Answered 24/7 · Moisture readings taken";
    /contact/: "Answered 24/7 · Written scope before rebuild").
  - **1 item (5 pages):** `/ceiling-leak/`, `/privacy-policy/`,
    `/terms/`, `/disclaimer/`, `/about/` — "Answered 24/7" alone.
    These pages have no "readings" wording AND no "written scope" /
    "moisture log" wording, so no sourced second item exists. See
    "Flagged" below; nothing was invented to fill them.
- **No sourced third item was substituted anywhere:** no page's copy
  offered a different trust-signal phrase that the existing builder
  variants (`written scope`, `moisture log`) did not already cover, so
  the drop-to-fewer-items fix is the complete fix. 0 words added.
- **Screenshots:** `hero-cost-390.png` (2-item row viewed),
  `hero-ceiling-leak-390.png` (1-item row viewed — reads clean),
  `hero-burst-pipe-*/hero-contact-*/hero-about-*/hero-home-*` at
  1440/390/320 (18 files).
- **FLAGGED (consequence, not a failure — owner call if wanted):** the
  5 one-item pages show a lone "Answered 24/7" line in the hero. It is
  honest (every word is on the page) and it reads cleanly in the
  screenshot, but it is thinner than the 2–3 item rows. The only way to
  give those 5 pages a second item without inventing words would be to
  reuse a phrase already on the page (e.g. a readings phrase they do
  not contain — they do not) — so this stands as the correct outcome
  under the no-invention rule unless the owner orders otherwise.

## FIX V-P3-5 — /contact/ hero ghost button self-link (pre-existing)

- **File:lines:** `site/includes/functions.php:789` (the `cta-line`
  `closing` role in `render_block()`) + `site/assets/css/styles.css:133`
  (one-line cursor rule).
- **Before:** the closing ghost rendered
  `<a class="btn btn-ghost" href="/contact/">Describe your water
  problem</a>` on every page — including /contact/ itself (1 self-link
  in `<main>`, pre-existing since the five-fix build).
- **After:** on `/contact/` ONLY, it renders
  `<span class="btn btn-ghost" aria-disabled="true">Describe your water
  problem</span>` — same classes, same text, no href. Every other page
  keeps the link. Clean conditional in the renderer (no hack): the
  `$page['slug']` is already in scope in `render_block()`. The
  homepage hero ghost (functions.php ~line 504) is untouched — home is
  not /contact/, and its ghost correctly links to /contact/.
- **Measured:**
  - `/contact/`: ghost tag **SPAN**, href **null**; `a[href="/contact/"]`
    in `<main>` = **0** at 1440/390/320; whole rendered page contains
    **0** `href="/contact/"` (header/footer render the current page as
    a span too). H1 = 1, trust 2 items, ?v=5.
  - **Pixel-identical styling:** closing ghost on /contact/ (SPAN) vs
    /cost/ and / (A) at 1440 — box **370×60.4**, font 22px, background
    `rgba(10, 46, 56, 0.25)`, colour white, border
    `1px solid rgba(255, 255, 255, 0.85)`, padding `16px 28px` — all
    identical. Only `cursor` differs (`default` on the span via the new
    `.btn-ghost[aria-disabled="true"] { cursor: default; }` rule, vs
    `pointer` on the links), which is the honest affordance for a
    non-link. At 390 the span measures 338×86.8 (wraps to two lines,
    same as the link version would).
  - Home untouched: hero ghost still `<a href="/contact/">`, and home
    `<main>` still has exactly 2 `/contact/` links (hero + closing
    ghosts, both legitimate from home).
- **Screenshots:** `contact-closing-cta-1440/390/320.png` (viewed at
  390: ghost visually identical to the link version),
  `closing-cta-contact-1440.png` vs `closing-cta-cost-1440.png`.

## CACHE-BUST

- **File:line:** `site/includes/header.php:48` — `styles.css?v=4` →
  `styles.css?v=5` (CSS changed again; the header comment requires a
  bump on EVERY CSS change).
- **Verified:** rendered stylesheet href is `styles.css?v=5` on 34/34
  pages at all three widths (102/102 loads).

## GATES — ALL RE-MEASURED (own server :8141, Playwright bundled Chromium)

| Gate | Result |
|---|---|
| Routes 200 | **34/34** at 1440/390/320 (102 loads) |
| H1 | Exactly **1 on 34/34** at all widths |
| Overflow | **0 at 320/390/1440 on 34/34** (`scrollWidth == clientWidth` after stepwise scroll) |
| Console/page errors | **0** across all 102 loads |
| Card body | **20px / 32px** on every `.kind-card p` / `.help-card p`; 0 clipped |
| Trust rows | **0** place-line items on 34/34; 9×3-item, 20×2-item, 5×1-item (see §V-P3-4) |
| Phone icon | **44×44 at 390 and 320**; header row fits exactly at both widths, brand unclipped |
| Hero buttons | Call 65.2px (390/1440) / 58.8px (320) min; ghost 56–84.4px mobile — all ≥44px |
| /contact/ self-link | **0** `href="/contact/"` in `<main>` (was 1); ghost is a SPAN |
| ?v=5 | **34/34** pages (102/102 loads) |
| Dashes | **0** em/en dashes in rendered HTML on home, /cost/, /contact/, /burst-pipe/, /about/ (sampled; no rendered words were added or changed anywhere — trust rows only remove an item) |
| Word changes | **0** added; the only word removal is the place-line trust item on 25 pages (authorised by the fix) |

## SCREENSHOT INDEX (`qa/screenshots-10x-fix-p3/`, 32 files)

- Headers: `header-390.png`, `header-320.png` (viewed).
- Heroes (trust rows): `hero-{home,cost,burst-pipe,contact,ceiling-leak,about}-{1440,390,320}.png` (cost + ceiling-leak viewed at 390).
- Card grids: `cards-{home,about}-{1440,390,320}.png` + `help-card-drying-390.png` (artefact shot, see note) + `help-card-drying-inview-390/1440.png` (viewed) + `help-cards-about-inview-1440.png` (viewed).
- Contact closing CTA: `contact-closing-cta-{1440,390,320}.png` (390 viewed) + `closing-cta-contact-1440.png` + `closing-cta-cost-1440.png` (comparison).

## PROBE SCRIPTS (mine, in /tmp — not committed)

- `/tmp/trust_audit.php` — calls the real `hero_trust_items()` per page.
- `/tmp/probe_p3.py` — 102-load probe; raw results `/tmp/probe_p3.json`.
- `/tmp/routes.json` — the 34 routes from `site/data/pages.php`.
