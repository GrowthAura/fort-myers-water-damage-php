# FINDINGS — Fort Myers NEW PHP site, 20X round, FIX WORKER
## `~/workspace/fort-myers-php/` — 2026-11-19, fix worker

**Task:** fix the independent verifier's 2 P3 defects (D-V2, D-V3 in
`qa/FINDINGS-20x-verify.md`) + the verifier's small 404 completeness note +
the parent's added hero-underline order (~17:39 PKT), then self-verify.
No push, no deploy, no MEMORY.md edit, no commit (the 20x changes were
uncommitted in the working tree; this round continues from there).

**Environment:** PHP was MISSING in this VM at start (`php: command not
found`) — a fresh cell; another apt process held the dpkg lock, so I waited
for it and re-checked: PHP **8.3.6 + mbstring present** after ~100 s, no
install of my own needed. Export is Python
(`python3 qa/export_cloudflare.py out`), never run with php. Playwright
bundled Chromium only, no `executable_path`. Temp servers stopped by PID
(PHP 8149 killed by PID 18217 after the 404 re-shoot; http.server probes
terminated by their Popen handles). One export caveat: `rcssmin` is not
installed in this VM, so this run ships `styles.css` **unminified**
(export warning only — no functional difference; the 20x verifier's
export had it minified at 15,596 B).

**Files changed (this round only):** `site/includes/header.php`,
`site/includes/footer.php`, `site/includes/functions.php`,
`site/index.php`, `site/assets/css/styles.css`. New QA tools:
`qa/probe_20x_fixes.py` (self-link census, tabindex, og:404, skip-link
keyboard test, cost tables, screenshots), `qa/probe_hero_underline.py`
(hero-link computed decoration + before/after shots).
Screenshots: `qa/screenshots/20x-fixes/` (all viewed at full size).
**No visible word changed** — verify_export word-diff 0 on all 34 pages.

---

## FIX 1 — D-V2 (P3): 0 self-linking nav items anywhere + closed-header section marker

**Before (own baseline census, fixed resolver, all 34 flat route files):**
**53 self-linking nav items** in header/footer chrome — the verifier's 51
plus 2 the verifier's census excluded by its root-link rule (brand `href="/"`
and mobile-menu "Home" on the homepage). By page: 19 dropdown pages × 2
(mobile menu + footer), `/cost/` + `/contact/` × 3 (mobile + footer +
top-level direct link), 7 guide/legal/about pages × 1 (footer only),
home × 2 (brand + mobile Home). Only the desktop dropdown was a span
(19 `span.nav-current`).

**Change (templates + CSS, no words changed):** every current-page nav
item is now a non-link span on the current page, same pattern as the
20x dropdown span:
- Desktop top-level Cost/Contact → `<span class="nav-current-top"
  aria-current="page">` (gold 22% bg + inset 0 −3px gold, as the old
  `a[aria-current]` rule).
- Mobile-menu panel (Home, all Services/Areas items, Cost, Contact) →
  `<span class="nav-current" aria-current="page">` (white 14% bg, 700,
  4px gold left border — the same highlight the old link had).
- Footer columns (Services / Explore / Areas) → `<span
  class="nav-current" aria-current="page">` (white, 700, gold underline).
- Brand on home → `<span class="brand" aria-current="page">` (keeps the
  gold brand-name underline; inner markup byte-identical).
- The old `a[aria-current="page"]` CSS rules are replaced by the span
  rules (the dropdown `a[aria-current]` rule was already dead since 20x
  and is removed). `main.js` needs no change: its click handler only
  matches `.mobile-menu-panel a, .nav-dropdown a`, and a span is not
  clickable — nothing to close.
- Closed-section marker: `header.php` now computes `$inServices` /
  `$inAreas` from the dropdown arrays; the matching `<details>` gets
  `nav-section-current` + `aria-current="true"` on its `<summary>`, styled
  with the same gold treatment as a top-level current link
  (rgba(201,155,63,0.22) bg + inset 0 −3px gold).

**After (same census, final export):**

| Metric | Before | After |
|---|---|---|
| Self-links in nav chrome (all 34 pages) | **53** | **0** |
| Self-links in `<main>` | 0 | **0** |
| `span.nav-current` / `nav-current-top` in chrome | 19 | **71** (19 dropdown + 22 mobile + 28 footer + 2 top-level) |
| Brand self-link on home | 1 | **0** |
| Mobile-menu "Home" self-link on home | 1 | **0** |

Section-marker computed style (desktop, final export):
- `/water-removal/`: Services summary bg `rgba(201,155,63,0.22)`,
  box-shadow gold inset 0 −3px, `aria-current="true"`; Areas plain.
- `/cape-coral/`: Areas marked the same way; Services plain.
- `/cost/`: Cost is `span.nav-current-top` (gold), no section marker.
- `/about/`: no marker anywhere (correct — About sits in no dropdown).
Viewed `09-header-closed-desktop-water-removal.png`: "Services ▾" shows
the gold bg + gold underline in the closed header. Viewed
`01-mobile-menu-water-removal.png`: "Emergency Water Removal" highlighted
in the open mobile panel. Viewed `04-footer-desktop-water-removal.png` +
`03-footer-mobile-water-removal.png`: footer current item white + bold +
gold underline; breadcrumb and all other nav text unchanged.

## FIX 2 — D-V3 (P3): skip link moves DOM focus to `<main>`

**Before:** `<main id="main">` on all 34 pages + 404 had **no
`tabindex`**; real Tab → Enter left `document.activeElement` = `BODY`
(both viewports; reproduced exactly as the verifier reported).

**Change:** `tabindex="-1"` added to `<main>` in the shared render path
(`site/includes/functions.php`, all 34 routes) and in the 404 template
(`site/index.php`). One attribute; no visual change (no focus style on
`main` itself, so no new outline appears).

**After — real keyboard test (Tab → Enter → Tab), Playwright bundled
Chromium:**

| Check | Before | After |
|---|---|---|
| `tabindex="-1"` on `<main>` | 0/34 routes, 404: no | **34/34 routes + 404** |
| Tab focuses skip link ("Skip to main content") | yes, 238×58 | yes, desktop + mobile |
| `activeElement` after Enter | `BODY#top` | **`MAIN#main`** (desktop + mobile) |
| `scrollY` after Enter | 80 | **80** |
| Next Tab lands on | first link inside main (hero tel) | **first link inside main (hero tel)** |

Viewed `06-skiplink-focused-desktop.png` (retaken clean on a fresh page
after the first shot caught the open dropdown instead): "Skip to main
content" coral bg, white text, 3px gold outline, top-left.

## FIX 3 — 404 og:url (verifier completeness note)

**Before:** `404.html` carried 5/6 og tags — no `og:url` (the header only
emitted it inside the `canonical` block, and the 404 sets `canonical`
to null by design).

**Change:** `site/index.php` 404 branch now passes `'og_url' =>
$SITE['url'] . $path` (the requested URL); `header.php` emits `og:url`
from `canonical` if present, else from `og_url` — still **no**
`<link rel="canonical">` on the 404 (it must not claim a real page).
The 34 routes are untouched by this change (their `og:url` still comes
from their canonical).

**After:** 404 output carries **6/6 og tags + 3/3 twitter tags**
(`og:url` =
`https://fortmyerswaterdamagerestoration.us/this-page-does-not-exist-404/`).
Verified against the live PHP router (not the static file): bogus path
answers **HTTP 404**, `og:url` = the requested URL, `main tabindex="-1"`.
Viewed `07-404-desktop.png` + `07b-404-mobile.png` (re-shot from the PHP
server — the first shot caught `python -m http.server`'s own plain 404
page, which does not serve `out/404.html`; the file itself was always
correct): "Page Not Found" template renders with header/footer; the
inline tel link in the 404 body keeps its underline (body links
untouched — see Fix 4).

## FIX 4 — Hero underline (parent order ~17:39 PKT): the "dash" under the hero number

**Cause (confirmed, not guessed):** 0 literal em/en dashes in out/
(dash sweep 0 files). The "dash" was the browser-default underline on
the inline phone link in the hero intro — e.g. homepage
`<a href="tel:+12393563708">239-356-3708</a>`; base `a` sets color
only, `.hero-intro a` set only color `#ffd9a8`. Measured before:
`text-decoration: underline` on that link, desktop + mobile; the hero
CTA buttons were already `none`.

**Scope check first:** census of every `<a>` inside any
`<section class="hero">` across out/ — the only non-button hero links
are the inline `239-356-3708` tel links in the hero intro on **13
pages** (home + about, ac-leak, cast-iron-pipe, ceiling-leak,
condo-leak, contact, drying, first-hour-checklist, privacy-policy,
sewage-cleanup, vacant-home, water-removal). The home hero-areas line
carries no links (plain text), and both hero CTA buttons are already
clean — but the fix covers them anyway.

**Change (CSS only, one rule, scoped to the hero):**
`.hero a { text-decoration: none; }` next to `.hero-intro a`. Color
untouched. Body links keep their underlines everywhere else.

**After (computed style, desktop + mobile, home + /water-removal/):**

| Hero link | Before | After |
|---|---|---|
| Intro number `239-356-3708` (13 pages) | `underline` | **`none`** |
| CTA buttons (all pages) | `none` | `none` (unchanged) |
| Number color | `rgb(255,217,168)` = #ffd9a8 | **`rgb(255,217,168)` (unchanged)** |
| #ffd9a8 contrast | — | **10.78:1 vs #0a2e38, 12.64:1 vs #062028** (AA/AAA, no color change needed) |

Viewed before/after at full size: `hero-before-home-desktop.png`
(underline clearly under the gold number) vs
`hero-after-home-desktop.png` (number clean, same gold, reads clearly);
`hero-after-home-mobile.png` (same, 390px); `hero-after-water-removal-*`
(inner-page hero, same result). Body-link control: the 404 body tel link
and the footer "Back to top" / body links in the footer screenshot still
show underlines — the removal is hero-only.

---

## VERIFICATION (final export, after all four fixes)

| Check | Result |
|---|---|
| `python3 qa/verify_export.py` | **FAILURES 0 / NOTES 0** (word-diff 0 all 34 pages) |
| `python3 qa/validate_schema.py` | **pages 34 \| scripts 92 \| nodes 92 \| ERRORS 0 \| WARNINGS 0** (+ 6 by-design NOTES, unchanged: 3× Article `image`, 3× publisher `logo`) |
| `python3 qa/render_check.py` | **34/34 overflow 0** at 320/360/390/1440; body font **20px** at 390 + 1440 |
| Dash sweep (literal – — + entities `&ndash;`/`&mdash;`/`&#8211;`/`&#8212;`) | **0 files** (68 HTML files) |
| Sitemap / robots / llms | **31 locs**; robots **22 `User-agent:` lines**; llms **31 entries**; llms-full.txt 31 pages, 419,280 B |
| Footer map | **0 iframes on all 7 location pages** |
| Images | **0 `<img>`** in out/ (68 files); **0 `og:image`** |
| Links census (own, fixed resolver, all 68 files) | **0 broken local targets**; **0 self-links in `<main>`**; **0 self-links in nav chrome** |
| Skip-link focus test (real keyboard) | **activeElement MAIN** desktop + mobile; next Tab inside main |
| /cost/ mobile re-check (D-V1 must stay fixed) | Tables **390/390/390px**, price cols **114/129/200px**, prices visible at first paint, `scrollWidth` 390. Viewed `08b-cost-table1-mobile.png`: all 3 columns + wrapped right-aligned prices ("From about $500", "About $1,200 to $3,500") |
| 404 | HTTP 404 from PHP router, 6/6 og + 3/3 twitter, `main tabindex="-1"` |

### Before/after summary

| Metric | Before | After |
|---|---|---|
| Self-linking nav items (chrome, 34 pages) | 53 | **0** |
| Nav current items as non-link spans | 19 | **71** |
| Closed Services/Areas summary shows current section | none (on the 19 dropdown pages) | **gold marker on the 19 dropdown pages** |
| `<main tabindex="-1">` | 0/34 + 404 | **34/34 + 404** |
| `activeElement` after skip-link Enter | BODY | **MAIN** (desktop + mobile) |
| 404 og tags | 5/6 (no og:url) | **6/6 + 3/3 twitter** |
| Hero intro number underline | underline (13 pages) | **none**; color #ffd9a8, contrast 10.78:1+ |
| Word-diff / schema / overflow / dashes / sitemap / maps / images | clean | **clean (unchanged)** |

## Open / standing (unchanged, not mine to close)

- No push / deploy done — verification + deploy happen after this, by others.
- Live site is still the pre-10x build
  (`fort-myers-water-damage-php.pages.dev`); nothing here was pushed.
- Live map tiles still need one real-browser look (VM Chromium cannot
  reach google.com/maps).
- `rcssmin` is not installed in this VM, so this export ships CSS
  unminified (warning only); the next export on a VM with rcssmin will
  minify again. No functional impact measured (render_check 34/34,
  20px, overflow 0 all widths).
- All temp servers stopped (PHP 8149 by PID; http.server probes by
  handle); no stray `php -S` / `http.server` processes remain.
