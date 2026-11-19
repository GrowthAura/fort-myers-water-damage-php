# FINDINGS — Footer Areas column + desktop H1 wide (2026-11-20 ~03:34–03:45 PKT)

Owner's orders (live review, "baqki all good" otherwise):
1. "area ko bhi menu se link do" — link Areas from the menu too.
2. "desktop pr sair h1 wide krdo" — make all H1 wide on desktop.

## What was true before the fix
- Header menu ALREADY had all 7 area links (desktop dropdown + mobile menu, $NAV_AREAS) — verified live.
- Footer had NO area links: the five-fix round (2026-11-19) removed the "Areas We Serve"
  column. The removal was flagged then as possibly bigger than his literal words; this
  order confirms he wants the column back.

## Changes (3 source files)
- `site/includes/footer.php` — "Areas We Serve" column restored, iterating the header's
  own `$NAV_AREAS` (Areas + 6 area pages, identical set/order/labels as the header),
  current-page renders as nav-current span (no self-link), plus the original zips line
  verbatim ("Fort Myers ZIPs 33901 to 33967 · North Fort Myers 33903, 33917").
  The `<!-- Areas is header-only -->` comment is gone (also closes 20x audit D-P3-3).
- `site/assets/css/styles.css` — footer grid back to 4 columns
  (`1.4fr 1fr 1fr 1fr`); `.hero-inner h1` max-width 820px → **1180px** (base/desktop
  rule; mobile unaffected — viewport is narrower than the cap).
- `site/includes/header.php` — stylesheet `?v=5` → `?v=6` (cache-bust rule: bump on every
  CSS change).

## Verification (local export, fresh)
- Gates 34/34: H1=1, `?v=6` only (0 × `?v=5`), footer areas 7/7, header areas 7/7,
  zips line present, old comment gone. Area pages: 6 links + current-page span = 7/7
  in both header and footer.
- Playwright (bundled Chromium, :3100): desktop H1 box **1180px × 2 lines**, 58px,
  computed max-width 1180px; footer **4 columns**, 987px tall; overflow 0 at 1440 and 390;
  mobile H1 350px at 390px, overflow 0.
- Screenshots viewed (qa/shots-fix2/): home hero 1440 — H1 wide, 2 lines, white text
  readable across the full width; home footer 1440 — 4 columns, all 7 area links + zips
  line visible. (Map shows the by-design "Map loading" poster; tiles need a real browser.)

## Incident caught during verification (no live impact)
- First screenshot run measured the WRONG site: port :3000 is held by a stale Next.js
  dev server (pid 2842, the old Fort Myers Next.js site) — it answered 200 for `/`
  and 404 for the CSS, so the first measurements (H1 1304px / 62.4px, footer 3 cols)
  were the old site's, not this build's. Lesson: **always prove the preview server's
  identity (CSS 200 + ?v= match) before trusting any measurement.** Fix: PHP preview
  moved to :3100 (pid in /tmp/fm-php-3100.pid); :3000 left alone — the stale server
  belongs to other chats' work, do not kill it.
- Also caught mid-round: an early `pkill -f "php -S 127.0.0.1:3000"` matched the
  exec's own shell and SIGTERM'd it (same trap as the ps/grep lesson in AGENTS.md).
  Never pattern-match your own command line.

## Push
- Token re-validated before push: login GrowthAura, repo permission admin (the 401
  reported ~03:39 in the Cape Coral chat was a different token, not this one).
- Commits carry author Noorullahmian <noorullahchhachher3@gmail.com>.
