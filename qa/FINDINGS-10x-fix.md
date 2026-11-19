# FINDINGS — 10X FIX ROUND (Fix Worker)

- **Project:** `~/workspace/fort-myers-php/` — Fort Myers PHP site, 34 pages
- **Date:** 2026-11-20 ~00:35–01:10 PKT
- **Scope:** fix the 4 P2s + 1 P3 from the independent verification
  (`qa/FINDINGS-10x-round.md`, verdict NOT READY, P1 0 · P2 4 · P3 5).
  Nothing else touched.
- **Mode:** LOCAL ONLY. No push, no deploy, no DNS/domain changes, no git
  commit. `qa/verify_export.py` NEVER run. No export to `out/` (the
  re-verifier owns the canonical export). Verification on my own PHP
  server on port 8140 (`php -S 127.0.0.1:8140 -t site site/index.php`,
  killed by PID when done) + Playwright bundled Chromium.
- **Result: all 5 fixes verified.** Menu 44×54.6, intro link 174×54.6,
  ZIP 33923 gone, homepage links reverted (1× each), H1 last line ≥2 words
  on /contact/ + /about/ at 1440/820/390/381/360/340/320 with no clipping.
  Overflow 0 at 1440/390/320 on the 5 probed pages; dashes 0 on all 5;
  H1 textContent normalises to the exact original strings.

## Files changed (5)

| File | Change |
|---|---|
| `site/data/areas.php:272` | Bonita Springs ZIP `33923, 34134, 34135` → `34134, 34135` |
| `site/data/homepage.php:255, 2001` | D-P3-9 revert (see Fix 2) |
| `site/assets/css/styles.css:875-884, 1404-1429, 1274-1285` | Menu button ≥44px; intro link ≥44px tall; H1 small-width shrink |
| `site/includes/functions.php:448-457` | `h1_html()` nowrap span on "Restoration Pros" for /contact/ + /about/ |
| `site/includes/header.php:48` | Stylesheet cache-bust `?v=3` → `?v=4` (CSS changed; the header comment requires a bump on every CSS change, or the fix never reaches a browser that cached the file) |

## FIX 1 (V-P2-1) — ZIP 33923 removed from the Bonita Springs row

- **File:line:** `site/data/areas.php:272`.
- **Before:** `'t' => '33923, 34134, 34135'` (rendered row:
  `Bonita Springs | 33923, 34134, 34135`).
- **After:** `'t' => '34134, 34135'` — back to the paste-verbatim values.
- **Verified (rendered HTML, port 8140):** ZIP table cell reads
  `<td data-label="ZIP codes">34134, 34135</td>`; the string `33923`
  occurs **0×** anywhere on the rendered /areas/ page.
  Screenshot: `qa/screenshots-10x-fix/el-areas-ziptable-1440.png`
  (Bonita Springs row visibly `34134, 34135`; all other rows unchanged).
- **Record:** 33923 was auditor-sourced only (never in any paste); the
  verifier could not confirm it as a current Bonita Springs ZIP (current
  lists: 34133–34136 only; 33923 is a historical ZIP renumbered to
  34135). Removed, not replaced — no new ZIP invented.

## FIX 2 (V-P2-2) — D-P3-9 tradeoff reverted per FINDINGS-10x-content.md §6

- **File:lines:** `site/data/homepage.php:255` and `:2001`. Words unchanged
  (href-only changes).
- **Before:** help card "businesses" → `/areas/`; the sentence
  "See every city and ZIP code we cover in our Lee County service areas."
  was plain unlinked text (`/areas/` 1× in `<main>`, on "businesses";
  `/commercial/` 0×).
- **After:** help card "businesses" → `/commercial/` (line 255, back to the
  pre-round state); the `/areas/` link restored on
  "ZIP code we cover in our Lee County service areas" (line 2001).
  The sentence now links somewhere again; D-P3-9 stands unfixed as a
  known item (the card lists five property types and links only to
  /commercial/), not silently duplicated.
- **Verified (rendered homepage `<main>`, port 8140):** `/areas/` **1×**,
  `/commercial/` **1×**, every other internal target **1×**. Full count:
  /water-removal/ 1, /drying/ 1, /sewage-cleanup/ 1, /flood-cleanup/ 1,
  /areas/ 1, /commercial/ 1, /about/ 1, /how-it-works/ 1,
  /first-hour-checklist/ 1, /ac-leak/ 1, /ceiling-leak/ 1, /condo-leak/ 1,
  /cast-iron-pipe/ 1, /burst-pipe/ 1, /water-heater-leak/ 1,
  /appliance-leak/ 1, /slab-leak/ 1, /vacant-home/ 1, /mobile-home/ 1,
  /floors/ 1, /cabinets/ 1, /insurance/ 1, /north-fort-myers/ 1,
  /cape-coral/ 1, /lehigh-acres/ 1, /fort-myers-beach/ 1, /estero/ 1,
  /bonita-springs/ 1 — **0 duplicate prose targets, 0 self-links**
  (no `href="/"` in `<main>`).
- **Note on the one ×2 count:** `/contact/` is 2× in `<main>`, exactly as
  before this fix. Both are the `.btn.btn-ghost` "Describe your water
  problem" buttons (hero CTA + closing CTA chrome), not prose — the
  pre-existing pattern the verifier already documented under V-P3-5.
  Not a prose duplicate; untouched.

## FIX 3 (V-P2-3) — mobile menu button ≥44px wide

- **File:lines:** `site/assets/css/styles.css:875-884` (the ≤820px
  `.mobile-menu summary` rule). CSS only; no HTML, no brand size, no
  phone-icon change.
- **Before:** `padding: 12px 10px`, icon-only at ≤620px → measured
  **36 × 54.6px** at 390/320 (reproduced on the untouched build before
  editing).
- **After:** `padding: 12px 14px; display: inline-flex; align-items:
  center; justify-content: center; gap: 8px; min-width: 44px;
  min-height: 44px; box-sizing: border-box;` — the `min-width` + 
...[truncated 5832 chars]