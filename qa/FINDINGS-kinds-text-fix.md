# FINDINGS — Five-Fix Round (kinds text, menu Areas, footer 7-only, details icons, H2/H3) — 2026-11-19

Owner orders 2026-11-19 ~21:22–21:29 PKT, bar raised to END LEVEL at ~21:29
("end level krdo, footer 1001 percent, jo jo kam kaha A to Z end krdo").
One re-export, one handoff. NO push — parent pushes after this handoff.

## 0. ROOT CAUSE — read this first (it changes what the fix is)

The owner's two screenshots (kinds cards dark text on photos; details icons
clipped with text colliding) are NOT what a fresh browser renders. The fresh
build was already correct: white kinds text on a dark scrim, clean details
icons. The cause is a **stale cached stylesheet in the owner's browser**:

- `out/_headers` serves `/assets/*` as `Cache-Control: public,
  max-age=31536000, immutable` (CSS cached 1 year).
- The stylesheet filename never changed between the 20X deploy and the
  ~21:16 hero-images deploy, so after the deploy his browser refreshed the
  HTML (`/*.html` is `no-cache`) but kept the 20X CSS.
- The 20X CSS has ZERO kinds rules (no `kind-scrim`, no `has-photo`, no
  white text) and ZERO `detail-icon` rules (verified: `git show
  bad30b5:assets/css/styles.css | grep -c` = 0 for all three). New HTML +
  old CSS = exactly his screenshots.

**PROOF — old-CSS simulation reproduces both screenshots pixel-for-pixel:**
current HTML + 20X CSS, served locally (`/tmp/oldcss-site`, since removed):
- `qa/screenshots-five-fixes/SIM-OLD-CSS-kinds-desktop.png` — dark teal
  headings + dark body text directly on the photos ("Sewer smell" and
  "Floodwater" text unreadable), identical to his kinds screenshot.
- `qa/screenshots-five-fixes/SIM-OLD-CSS-details-mobile.png` — bare 22px
  inline SVG icons with NO disc and NO gap, text touching the icon
  ("Phone", "What it covers", "Extraction time"), identical to his
  details screenshot.

**Consequence: a CSS-only change CANNOT fix his view.** His browser will
keep serving the cached 20X CSS until it expires or he hard-refreshes.
The fix therefore has two parts, both shipped in this round:
(a) the CSS changes themselves (stronger scrim, hardened icons, new H2/H3,
nav/footer data), and
(b) **the stylesheet URL is cache-busted** — `site/includes/header.php`
now links `/assets/css/styles.css?v=2` (was `/assets/css/styles.css`).
A new URL is a cache miss in every browser and in Cloudflare, so the
pushed build fetches the new CSS on first load. **Bump the `?v=` on EVERY
future CSS change** (comment added in header.php + styles.css). The
1-year immutable cache stays (good for ranking); versioned URLs are the
mechanism that lets it update. This is the one change that goes slightly
beyond the "CSS only" scope of Task 1 — without it, the push would not
fix what the owner sees.

## 1. TASK 1 — Kinds-grid card text (his: "text visible kr yaar")

Files: `site/assets/css/styles.css` (scrim + comments), `site/includes/header.php` (?v=2).

- Scrim strengthened: `linear-gradient(180deg, rgba(7,38,47,0.92) 0%,
  rgba(7,38,47,0.88) 55%, rgba(7,38,47,0.86) 100%)` (was 0.86/0.78/0.74).
  Text unchanged: h3 #ffffff, p #f4f8f8, links #ffd9a8. Orange top border
  kept. 0 word changes, 0 link changes. Kinds grid is homepage-only
  (`out/index.html` is the only file with `kinds-grid`); the "What we help
  with" grid is a different component (top `<img>`, not photo backgrounds).
- Trade-off, stated plainly: the photos are now quite muted behind the
  stronger scrim (they read as dark teal panels with faint photo texture).
  Readability is now beyond doubt; the photo presence is reduced. If the
  owner wants the photos more visible, the scrim can come back down — the
  old 0.86/0.78/0.74 already measured 5.12:1 worst-case.

### Contrast — measured, two independent ways (both worst case)

(a) THEORETICAL (scrim alpha blended over each master's brightest pixel,
WCAG 2.x formula; absolute worst = pure-white pixel at weakest alpha 0.86):
h3 10.30:1, p 9.63:1, link 7.72:1. Per-card (brightest pixel, bottom 0.86):
link 7.72:1 (7 cards) to 8.38:1 (flood-storm); h3 10.30:1 to 11.18:1;
p 9.63:1 to 10.45:1. Full table method in `qa/contrast-kinds.py`.

(b) RENDERED (from the real desktop + mobile screenshots, bottom padding
strip of each card = weakest alpha 0.86, clear of text, AA fringes, the
sticky header and the fixed call bar — see method note below):
- Desktop worst: h3 **10.22:1**, p **9.56:1**, link **7.66:1**
  (AC + ceiling-leak cards; bg (42,69,76)).
- Mobile worst: same 10.22 / 9.56 / 7.66 (identical, all 13 cards).
- Per-card rendered range: h3 10.22–12.21:1, p 9.56–11.41:1,
  link 7.66–9.15:1. Rendered matches theoretical (7.66 vs 7.72) — the
  model is confirmed by viewed pixels. ALL >= 4.5:1 by a wide margin.

Method note (three failed attempts, for the record): measuring "brightest
pixel in the text block" from a screenshot does NOT work — it picks up
subpixel-AA fringe pixels (1.01:1), then the luminance cap (3.00:1), then
the rounded-corner white + orange border (1.00:1). The correct sample is
the card's bottom padding strip: genuine scrimmed photo, weakest alpha,
no text, no chrome. The two artifact values in the intermediate runs were
the fixed call bar (mobile ceiling-leak, coral #C2410C) and the sticky
header (desktop first row) painting over element screenshots — both are
capture artifacts, not card backgrounds. The screenshots themselves were
viewed and are clean.

### Screenshots viewed (kinds)
- `qa/screenshots-five-fixes/verify/kinds-desktop-1440.png` — all 13 cards,
  white headings + white body + gold links, every card readable.
- `qa/screenshots-five-fixes/verify/kinds-mobile-390.png` — all 13 cards,
  same, mobile. (First-row headings are partly behind the sticky header in
  the element capture — screenshot artifact, not a page defect.)

## 2. TASK 2 — Menu Areas link (his: "areas ko link kr menu se, aur menu se see all areas hata de")

Files: `site/data/pages.php` (`$NAV_AREAS`), nothing else (header + mobile
menu both iterate the one array).

- `$NAV_AREAS` is now: **Areas → /areas/ FIRST**, then Cape Coral, Lehigh
  Acres, North Fort Myers, Fort Myers Beach, Estero, Bonita Springs (7).
- The old trailing item was labelled **"All Service Areas"** (the text
  "See all areas" does not exist anywhere in site/ or out/ — that was the
  owner's paraphrase; the menu item was "All Service Areas"). It is GONE.
- "See all areas" / "All Service Areas": **0 hits** in rendered header,
  mobile menu, and all of out/ (verified by `qa/verify-five-fixes.py`).
  Note: "See all service areas." still appears inside FAQ JSON-LD answer
  text on a few pages — that is body copy, not menu, and was NOT touched
  (0 word changes).
- The `/areas/` hub already marked the Areas section current (`$inAreas`
  uses the same array), so the hub page now shows "Areas" as the current
  item. Footer untouched by this task.

### Screenshots viewed (nav)
- `verify/nav-areas-open-desktop.png` — dropdown open: Areas first + 6 areas.
- `verify/nav-mobile-menu-open-390.png` — mobile menu: AREAS group, "Areas"
  first (rest below the fold of the viewport shot; menu is scrollable).

## 3. TASK 3 — Footer Services = header's 7 ONLY (his: "footer set kr — footer ma areas na add kr, footer ma pehle 7 services na add kr jo header ma kr rhrye hain")

Files: `site/includes/footer.php`, `site/data/pages.php`, `site/assets/css/styles.css` (grid).

- Footer Services now iterates `$NAV_SERVICES_MENU` — EXACTLY the header's
  7 (Emergency Water Removal, Structural Drying, Sewage Backup Cleanup,
  Flood & Storm Cleanup, AC Leak Water Damage, Ceiling Leak Water Damage,
  Burst Pipe Water Damage), same labels, same order, same pages.
  Verified set-identical to the header menu 7.
- The **"Areas We Serve" footer column is REMOVED entirely** (6 area links
  + "All Service Areas" + the footer-zips line "Fort Myers ZIPs 33901 to
  33967 · North Fort Myers 33903, 33917"). The `$FOOTER_AREAS` array is
  deleted from `pages.php` (its only user was footer.php). The footer grid
  is now 3 columns (`1.4fr 1fr 1fr`, was `1.4fr 1fr 1fr 1fr`).
- **FLAG for the parent/owner:** this removal is bigger than the literal
  order ("footer ma areas na add kr" = don't ADD areas; the column already
  existed). The verify demanded "0 Areas links anywhere in the footer", so
  the column had to go. If he meant to KEEP the column, it is a one-line
  revert (restore the nav block + `$FOOTER_AREAS` array). The ZIPs line
  went with the column; it is not a link and could be restored on its own
  if wanted. `.footer-zips` CSS rule left in place (harmless, for a
  restore).
- Footer Explore column (9 links) UNCHANGED — verified identical to
  pre-fix. Footer brand line UNCHANGED (name, address, hours, Call button,
  map, "View larger map").
- The other 10 service pages lose ONLY the footer nav link. They remain
  reachable via in-content links (kinds grid, help cards, related) +
  sitemap (31 locs, unchanged).
- Footer end-level (bar raised): 3-column grid is balanced; brand + Call
  button + map + Services + Explore all tidy; spacing/padding even;
  no clipping, no overflow, no ragged edges at desktop + 390 + 320.

### Screenshots viewed (footer)
- `verify/footer-desktop.png` — 3 columns, clean, balanced.
- `verify/footer-mobile.png` — single-column stack, clean.
- `verify/footer-mobile320.png` — 320px, brand name wraps to 2 lines,
  no clipping, no overflow.

## 4. TASK 4 — Details-card icons (his: "har service page par ye icon conflict rakh rahe hain, inki proper set kr, padding kr inki")

Files: `site/assets/css/styles.css` only. Root cause is the same stale CSS
as Task 1 (see §0 — the old-CSS simulation reproduces his screenshot);
the layout itself was already correct in a fresh render, so this task
hardens it AND delivers it via the ?v=2 cache-bust.

Settled layout (recorded):
- Icon box: **fixed 40px column** (`flex: 0 0 40px`, width/height 40px),
  pale-teal disc #E0EBED, teal glyph, svg 22×22 with `max-width/max-height:
  22px` + `flex: none` guards.
- Gap: **14px** between icon and label (`dt` gap), label `padding-top:
  5px` kept.
- Alignment: `dt` is now `align-items: center` (was `flex-start`) — the
  icon is vertically centred on its row label, including 2-line labels.
  First-line alignment with the value column is preserved (label and `dd`
  both sit at +5px).
- Mobile: single column; value indented **54px** (40px disc + 14px gap),
  aligned under the label text, not under the icon.
- 0 word changes, 0 link changes.

### Verification (all 26 details pages)
- Geometry, measured on every row of every card at desktop 1440 + mobile
  390 + mobile 320 (`verify/details-geometry.json`): **0 issues** — every
  icon exactly 40×40, inside the card padding, label ≥10px from the icon.
- Screenshots: all 26 desktop cards viewed
  (`verify/montage-details-desktop-1/2/3.png` — 9+9+8); mobile viewed
  (water-removal, commercial, cape-coral @320); home card viewed at all 3
  widths. Every icon fully visible, aligned in a clean column, clear
  padding around it. (Sticky header + fixed call bar paint over element
  screenshots in places — capture artifact, not a defect; geometry proves
  the layout underneath.)
- 26 pages = 25 service/area/guide pages + homepage (the homepage has a
  details card too; the first pass missed it because the glob skipped
  `out/index.html` — caught and shot separately, OK at all 3 widths).

## 5. TASK 5 — H2/H3 colour + style, sitewide (his: "H2 H3 ka colour badlo, piyara kro, aur thora sa stylish krdo")

Files: `site/assets/css/styles.css` only. 0 word changes, 0 link changes.

- **H2: teal #0B5563 → deep #0A2E38** (the darkest ink in the theme).
  The `::before` gradient bar (teal → coral, 72px × 6px) is UNCHANGED —
  the bar is the accent, the text is the ink.
- **H3: coral-dark #9A3412 → teal #0B5563**, PLUS a stylish accent: a
  44px × 4px **gold rule under every H3** (`::after`, `var(--gold)`),
  echoing the details-card eyebrow bar. Decorative only.
- Hierarchy is now deep > teal, with gold as the accent (was teal >
  coral-dark). Excluded by the same scopes as before: kind-card h3 (white
  on photo), footer h3 (own #fff rule), details-card h2 (own deep rule).
  The gold rule was checked in all three h3 contexts: plain content h3,
  `.steps` h3 (burst-pipe), `.area-card` h3 (/areas/) — clean in all three.

### Contrast — measured (WCAG 2.x)
- H2 #0A2E38: **14.38:1** on white, **12.77:1** on sand, **11.69:1** on sand-2.
- H3 #0B5563: **8.42:1** on white, **7.48:1** on sand, **6.85:1** on sand-2.
- All >= 4.5:1 on every background an H2/H3 can sit on.

### Screenshots viewed (headings)
- H2: `verify/h2-water-removal-desktop.png`, `verify/h2-cape-coral-mobile.png`,
  `verify/h2-cost-desktop.png`, `verify/h2-home-desktop.png`,
  `verify/h3-steps-burst-pipe-desktop.png` (H2 above the steps) — deep H2 +
  gradient bar, clean desktop + mobile.
- H3: `verify/h3-home-desktop.png` ("What we help with" — teal + gold rule),
  `verify/h3-steps-burst-pipe-desktop.png` (step titles),
  `verify/h3-areacard-areas-desktop.png` (Cape Coral / Lehigh Acres /
  North Fort Myers cards) — teal H3 + gold rule, clean in all contexts.

## 6. GATES — all re-run after the fixes (independent re-scan)

- `qa/verify-five-fixes.py` (read-only; written for this round — see note):
  **ALL CHECKS PASS.** `<main>` word-identical vs pre-fix on 34/34 pages
  (word-diff 0 preserved); H1=1 on 34/34; dashes 0 (all 34 files);
  stylesheet `?v=2` on all 34 pages; sitemap 31 locs; llms.txt 31 entries;
  heroes 34/34 files exist in out/; related == 3 on all 24 pages that have
  one (same count as pre-fix); 0 broken internal links across 34 pages;
  scrim 0.92/0.88/0.86 in out CSS, old 0.74 gone; Areas dropdown (desktop
  + mobile) = Areas first + 6; "See all areas"/"All Service Areas" 0 hits;
  footer Services = header menu 7; 0 area links in footer; Explore
  unchanged (9); H2 deep + H3 teal + H3 gold ::after in out CSS.
- `qa/validate_schema.py out`: **ERRORS 0, WARNINGS 0** (34 pages, 92
  scripts). The 6 NOTES are the standing by-design ones (Article `image`
  + publisher `logo` — fixing would require inventing data).
- `qa/probe-five-fixes-render.py` (viewport-only; `qa/render_check.py`
  crashes on the homepage full-page capture — Chromium single-capture
  height limit, homepage ~17,876px, plus /tmp 81% full; the probe uses
  TMPDIR=qa/tmp-chrome and no full-page shots):
  **overflow 0 at 320/360/390/1440 on all 34 pages; body 20px at 1440 +
  390 on all 34 pages.**
- `qa/verify_export.py` was NOT run (banned: it re-runs the parsers, which
  re-emit `site/data/*.php` and would wipe the hero round's hand edits
  incl. the nav arrays changed here). Word-diff is proven instead by the
  `<main>` word-identical comparison against the pre-fix exported tree
  (`cloudflare-pages 3935d04`, verified word-diff 0 by the hero round).

## 7. What changed, file by file (for the push)

Source (git status — only these 4 files modified):
- `site/assets/css/styles.css` — kinds scrim 0.92/0.88/0.86; details icon
  column fixed 40px + centred + svg guards; H2 deep; H3 teal + gold
  ::after; footer grid 3 columns; comments updated with the new numbers
  and the cache-bust rule.
- `site/includes/header.php` — stylesheet `?v=2` + comment (bump on every
  CSS change).
- `site/includes/footer.php` — Services iterates `$NAV_SERVICES_MENU`;
  "Areas We Serve" column removed; globals updated.
- `site/data/pages.php` — `$NAV_AREAS` = Areas first, "All Service Areas"
  gone; `$FOOTER_AREAS` deleted; comments updated (the `$NAV_SERVICES`
  array itself is kept — header's `$inServices` check still uses it).

Export: `python3 qa/export_cloudflare.py out` (re-run after the last
source edit). `out/` is the fixed build: styles.css minified 59,539 →
22,751 B; llms-full.txt 414,031 B (was 419,280 — the removed footer links).
**out/ is the fixed build. No push, no deploy, no domain touch — parent
pushes.**

New QA tooling (untracked, in qa/): `verify-five-fixes.py` (the gate),
`probe-five-fixes-render.py` (overflow + 20px), `shots-five-fixes-verify.py`
(screenshots + details geometry), `diag-five-fixes.py` (diagnosis).
Screenshots: `qa/screenshots-five-fixes/verify/` (99 files incl. the 26
details cards × 3 widths, kinds desktop+mobile, nav, footer, headings)
plus `SIM-OLD-CSS-*.png` (the stale-cache proof).

## 8. OPEN / for the parent + owner (not blockers)

1. **The push only fixes his view because of `?v=2`.** If he still sees
   dark kinds text after the push, it is his browser cache again — a hard
   refresh (Ctrl+Shift+R) fixes it, and the new URL should make that
   unnecessary. Worth telling him plainly.
2. **Footer Areas column removal** (§3 flag) — revertible in one edit if
   he meant to keep it. The ZIPs line went with it.
3. **Kinds photos are muted** under the stronger scrim (§1 trade-off).
4. **Still open from the hero round** (not this round's scope): 3 homepage
   help cards link-free ("Sewage backup cleanup", "Flood and storm
   cleanup", "Leaks of every kind"); Estero/Bonita shared-paragraph split;
   `kinds-water-heater-leak.jpg` tiny illegible label nit; "Seasonal Home
   Water Damage" vs "Vacant Home Water Damage" footer label.
5. **Still needs a real-browser look** (VM Chromium cannot): live map
   tiles (blank in VM, markup correct) and live Speed Index.
6. Element screenshots in this round show the sticky header / fixed call
   bar painting over card tops in places — capture artifact, not a defect
   (geometry + viewed pixels confirm the layout underneath).
