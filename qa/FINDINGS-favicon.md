# FINDINGS — Task 14: Favicon (heavier/bolder mark)

Date: 2026-11-19. Owner's order: "favicon koi heavy sa lagao, badal do".
File changed: `site/favicon.svg` ONLY. No commit, no push, nothing else touched.

## Brand identity (source of truth)

Header brand mark in `site/includes/header.php` (line ~72): coral droplet
`#E8590C` + white highlight arc, no background, `viewBox 0 0 34 34`.
`theme-color` is `#0A2E38` (dark teal). The favicon keeps exactly this identity:
same coral droplet, same white highlight, same teal — only heavier.

## Before (old `favicon.svg`, 311 bytes)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0a2e38"/><path d="M32 10C32 10 18 26.5 18 36.5a14 14 0 0 0 28 0C46 26.5 32 10 32 10Z" fill="#e8590c"/><path d="M25 38a7 7 0 0 0 7 7" stroke="#fff" stroke-width="3" stroke-linecap="round" fill="none"/></svg>
```

Weaknesses at tab size: droplet only 28/64 = 44% of the canvas wide, tip at
y=10 leaves a large empty teal margin above it, highlight stroke 3 = 0.75px
at 16px (nearly invisible). At 16px it read as a small orange blob, not a
droplet.

## After (new `favicon.svg`, 305 bytes, valid XML, viewBox 0 0 64 64)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0A2E38"/><path d="M32 6C32 6 11 26 11 37a21 21 0 0 0 42 0C53 26 32 6 32 6Z" fill="#E8590C"/><path d="M21 40a11 11 0 0 0 11 11" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none"/></svg>
```

## Why the new mark is heavier

| Element | Old | New |
|---|---|---|
| Droplet width | 28/64 (44% of canvas) | 42/64 (66% of canvas) |
| Droplet height | y 10 → 50.5 (40.5 units) | y 6 → 58 (52 units) |
| Droplet body radius | r=14 | r=21 (+50%) |
| Highlight arc | r=7, stroke-width 3 (0.75px @16px) | r=11, stroke-width 6 (1.5px @16px) |
| Tile corner radius | rx=12 | rx=14 (slightly softer, heavier tile) |
| Colours | unchanged: teal `#0A2E38`, coral `#E8590C`, white highlight | same |

No text in the mark (unreadable at 16px). No invented brand elements.
No teal disc/background added: the full-bleed teal rounded square already
carries the teal identity and gives the coral droplet a high-contrast field
on light tabs; an extra disc inside would have shrunk the droplet and
cluttered the 16px render. Decision recorded: disc NOT added, on purpose.

## Verification (rendered, viewed at full size)

Method: test page `/tmp/favicon-test/test.html` (NOT in the site) showing old
vs new side by side at 16px / 32px / 48px on light `#fff` and dark `#1e1e1e`
backgrounds, plus a simulated browser tab strip (light `#dee1e6`, dark
`#35363a`, 16px icon + page title). Screenshots with Playwright bundled
Chromium (no `executable_path`), device_scale_factor 3, viewed at full size:
`/tmp/favicon-test/full.png`, with zoomed crops of the 16px rows
(`zoom-light16.png`, `zoom-dark16b.png`).

| Size | Light bg | Dark bg | Verdict |
|---|---|---|---|
| 16px | Droplet clearly readable, white highlight swoosh visible; visibly bigger/bolder than old | Coral droplet + bold white highlight read clearly; teal tile still distinguishable from `#1e1e1e` | **PASS — reads clearly at 16px on both** |
| 32px | Crisp droplet, bold highlight | Same, crisp | PASS |
| 48px | Full droplet shape + highlight, unmistakable | Same | PASS |
| Tab strip (16px) | New mark reads next to the title on light tab bar | New mark reads next to the title on dark tab bar | PASS |

Old vs new at 16px (viewed zoomed): old = small orange droplet, highlight
almost gone; new = droplet fills the tile, highlight is a clear white swoosh.

Honest limitation: a real browser-tab render (actual tab strip via
`<link rel="icon">`) was NOT tested — headless Chromium has no real tab UI.
The 16/32/48px renders on both backgrounds plus the tab-strip simulation are
the acceptance test, and they pass. The coordinator / owner can confirm in a
real browser after deploy.

## Reference / export — unchanged, confirmed

- `site/includes/header.php` line 40 still reads:
  `<link rel="icon" href="/favicon.svg" type="image/svg+xml">` — untouched.
- `qa/export_cloudflare.py` line 33: `STATIC_FILES` includes `"favicon.svg"`
  (comment line 10: "Static files (robots, sitemap, llms, favicon, IndexNow
  key) + assets/") — the export copies the new favicon. Export NOT run
  (coordinator's job).

## Verdict

**DONE — new mark reads clearly at 16px on both light and dark backgrounds.**
305 bytes, valid SVG, same droplet brand identity, measurably heavier
(droplet +50% wider/taller, highlight stroke doubled). Ready for the
coordinator's export/push; no further action needed from this worker.
