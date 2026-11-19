# FINDINGS — Hero Images + Design Round (Tasks 1–14) — CONSOLIDATED

Fort Myers NEW PHP site (`~/workspace/fort-myers-php/`). Coordinator: subagent 17ff0e4c.
Phase 1 workers A–M delivered ~18:52 PKT 2026-11-19. Phase 2 merge + verification
completed by coordinator ~20:30 PKT 2026-11-19. Local only — NOT deployed (no token held).

## 1. What shipped in this round (all 14 tasks)

| Task | Change | Verified |
|---|---|---|
| T1 heroes | Real image in every hero, 34/34 routes (68 files: 34 masters + 34 960w variants) | hero-img on 34/34 pages; all loaded (naturalWidth > 0) |
| T2 details card | Icons per row, orange removed, H2 teal + eyebrow, on all 26 pages with a card | details-card 26 pages; detail-icon 181/181 rows |
| T3 help cards | "What we help with" = 6 cards, small image each | 6 articles + 6 imgs on home |
| T4 about buttons | "About us" / "How it works" = ghost buttons | rendered, 56px tap target |
| T5 kinds backgrounds | 13 cards, photo + scrim behind each | 13 has-photo + 13 scrims |
| T6 one-link rule | PHASE 2.5 (separate worker) — audit done: 31/34 pages have dup body targets (see §7) | audit only in this round |
| T7 area cards | /areas/ = 6 cards with place photos (2 grids) | 6 articles + 6 imgs |
| T8 call button | "Call 239-356-3708 with your ZIP code." = real tel button | rendered desktop + mobile |
| T9 FEMA sentence | Removed (homepage) | 0 hits in out/ |
| T10 Category 3 sentence | Removed (homepage) | 0 hits in out/ |
| T11 tables + buttons | Table header/zebra/price colour; button gradient + gold | screenshots desktop + mobile |
| T12 menu 7 | Header dropdown + mobile menu = 7; footer = 17 | click-tested; footer list 17/17 |
| T13 related 3 | Related = 3 on 27 pages; 27 unique homepage anchors | 27/27 = 3; 27 distinct anchors |
| T14 favicon | Heavier droplet mark (305 B) | renders 16/32/48/64px |
| Bar-raised | Sitewide colour + H2/H3 sitewide; text stays 20px | H2 #0B5563, H3 #9A3412; 0 font-size changes |

Header brand cut (parent, before this round) kept: "Fort Myers Water Damage" / "24/7 · FL".

## 2. Image inventory (93 finals in site/assets/img/, 9.8 MB)

GPS re-verified personally by the coordinator (script /tmp/gps_check.py): 93/93 correct,
0 wrong, 0 missing. EXIF audit (/tmp/exif_audit.py): only GPS + IFD0 resolution tags;
0 XMP APP1 segments; 0 AI markers. Reuse nets (/tmp/reuse_final.py, fresh disk reads,
186,627 files md5 / 88,972 aHash): MD5 0 non-self hits; aHash <25 only self-matches
(master vs own 960w variant). Verdict: reuse CLEAR. Every image viewed at full size
by its worker; honestly-empty pages: NONE.

GPS: Fort Myers 26.6406,-81.8723; Cape Coral 26.5629,-81.9495; Lehigh Acres
26.6126,-81.6367; North Fort Myers 26.6883,-81.8808; Fort Myers Beach 26.4442,-81.9557;
Estero 26.4327,-81.8068; Bonita Springs 26.3398,-81.7787.

### Heroes (34 masters; 960w variants alongside — master weights below)
home 144 KB · water-removal 142 · drying 136 · sewage-cleanup 147 · ac-leak 128 ·
ceiling-leak 148 · condo-leak 144 · cast-iron-pipe 165 · vacant-home 144 · burst-pipe 145 ·
mobile-home 214 · slab-leak 142 · flood-cleanup 180 · water-heater-leak 204 ·
appliance-leak 166 · floors 139 · cabinets 146 · commercial 257 · first-hour-checklist 145 ·
cost 146 · insurance 128 · how-it-works 177 · contact 167 · about 230 · cape-coral 283 ·
lehigh-acres 365* · areas 214 · north-fort-myers 340* · fort-myers-beach 256 · estero 260* ·
bonita-springs 223* · privacy-policy 143 · terms 144 · disclaimer 135. (* = downscaled
master 1600x1067 @ q55; all others 1920x1280.) Variants 960x640, worst 139 KB.
Weight call: 4 masters >300 KB downscaled 24–27% (lehigh 498→365, north-fort-myers
469→340, estero 343→260, bonita 304→223); re-compression alone was near-useless
(q40 barely smaller). All other weights accepted: mobile loads only the 960w variant.

### Help (6, 474x267): emergency-water-removal 28 KB · structural-drying 23 ·
sewage-cleanup 17 · flood-storm-cleanup 36 · leaks-every-kind 17 · every-property 36.
### Areas (6, 474x316): cape-coral 28 · lehigh-acres 35 · north-fort-myers 28 ·
fort-myers-beach 35 · estero 40 · bonita-springs 30.
### Kinds (13, 760x864): ac-leak 47 KB · appliance-leak 53 · burst-pipe 74 ·
cast-iron-pipe 101 · ceiling-leak 64 · condo-leak 76 · flood-storm 102 ·
floors-cabinets 58 · mobile-home 79 · sewage-backup 72 · slab-leak 58 ·
vacant-home 68 · water-heater-leak 86. (938 KB total; below the fold; accepted.)

Slots measured: hero home desktop 1440x683 / inner 1440x571; home mobile 390x1019 /
inner 390x759. Kind-card 381x432 desktop / 350x466 mobile. Help img slot ≤474x267.
Area img slot ≤474x316.

## 3. Merge log (Phase 2 — what the coordinator changed and why)

- Manifests: site/data/media-manifest.php = hero 34 + help 6 + areas 6 (merged from
  manifest-hero-A/B/C.php); site/data/manifest-kinds.php = F's file verbatim.
- functions.php: details_icon() + 'details' case (D); 'ul' help-cards branch (E);
  'p' about-buttons + call-button branches (E); 'kinds' case (F); 'area-cards' case (G).
- homepage.php: 3 variant lines (help-cards / about-buttons / call-button).
- areas.php: 2 area-cards grids (G) — see §4 for the boundary bug + fix.
- pages.php + header.php: $NAV_SERVICES 12→17, new $NAV_SERVICES_MENU (7);
  header + mobile loops use MENU; footer iterates $NAV_SERVICES (= 17, no change needed).
- styles.css (57,883 chars, 302 braces): hero scrim 0.38→0.70; D details block;
  F kinds block; E help/buttons/call CSS; G areas rules; I tables + buttons (base rules
  KEPT — deleting them would lose properties I's rules don't restate); D mobile details;
  .area-grid into visibility/print/media lists; L colour-sitewide LAST with 2 fixes:
  (a) `:not(.kind-card.has-photo a)` on the 3 body-link selectors — without it L's teal
  would override F's gold #ffd9a8 on photo scrims (~1.5:1 fail); (b) :focus-visible =
  gold outline + dark-gold outer ring (4.90:1 on white; gold-only was 2.55:1, fails 2.4.11).
- WCAG fails fixed: header coral <4.5:1; dropdown .nav-current coral-on-sand 4.21:1 →
  coral-dark #9A3412 (5.94:1); dropdown hover 4.60→6.49:1.
- Known minor: E's help-img uses -28px margins for 28px card padding, but F's ≤820px rule
  sets .kind-card padding 24/22px — image clips 4–6px/side at ≤820px, invisible (photo).
  Verify visually at 390px (done — help-grid-mobile renders clean).

## 4. Defects found + fixed during the merge (own errors, owned plainly)

### (a) Details-case truncation — the blocking defect
`/tmp/apply_patches.py` extracted the NEW details case with end-marker `'\n'`, which
matched the first newline — so `newB` was just ` case 'details':` (1 line). The script
replaced the full 7-line OLD case with it (assertions passed, printed "OK"). Result:
`case 'details':` fell through to `case 'h2':`, rendering `<h2></h2>` (empty — details
blocks have no 'text' key) and dropping heading/sub/rows on all 26 pages. Caught by
the verify word-diffs (homepage −166, water-removal −111 vs authorized) + grep
(details-card 0). FIX: replaced the bare stub with the full 8-line NEW case from
qa/patch-details-functions.txt; php -l clean; re-exported; details-card now 26 pages,
detail-icon 181/181, empty h2 0. LESSON: never use a bare '\n' as an extraction end
marker; assert the extracted block's line count + a content marker (e.g. 'details-card').

### (b) areas.php boundary bug (same script family)
The first apply script's `section()` searched start markers from position 0, so the
grid-2 extraction grabbed grid 1's marker and patch text landed inside areas.php +
Pine Island's `],` + San Carlos's `[` were eaten (parse error line 438). FIX: restored
from /tmp/areas.php.bak and redid with /tmp/fix_areas.py (correct offsets + boundary
handling). Verified: grid 1 at line 324, Sanibel + Pine Island untouched, grid 2 at 438.
LESSON: never reuse /tmp/apply_patches.py as-is — its section() has the position-0 bug.

### (c) verify_export.py WIPED all data-file edits — TWICE (the big one)
`qa/verify_export.py` REGENERATES all 34 page data files from the pastes on EVERY run:
it runs `tools/parse_homepage.py` as a subprocess + `pp.Parser(spec).run()` for every
inner page + `pl.LegalParser(...).run()` for legal pages. The parsers write to
HARDCODED absolute paths (`tools/parse_page.py:21 BASE = "/home/hatch/workspace/fort-myers-php"`;
`tools/parse_homepage.py:17-18` PASTE/OUT; `qa/verify_export.py:33` BASE). Consequences:
- Run 1 (~14:39 UTC): wiped K's related-3 edits (27 files) + T9/T10 cuts + homepage
  variants + areas grids. All 34 data files regenerated (mtime 14:39:34-35).
- My "safe copy" fix FAILED: running the copy's verify still wiped the LIVE project,
  because verify_export.py:33 BASE is hardcoded to live — the copy was never used.
  Run 2 (~15:00 UTC) wiped the recovery again.
- RECOVERY (twice, deterministic, byte-identical to K's original — 0 mismatches on
  re-compare vs /tmp/rel_trim_results.json): homepage restored from /tmp/homepage.php.bak
  (has T9/T10) + 3 variants re-applied; /tmp/rel_trim.py --apply (27 files, 98 removed);
  re-indent of the 3 item brackets per file (K's postscript); /tmp/rel_delink.py (8 links);
  /tmp/fix_areas.py (2 grids). php -l clean on all 29 files.
- SAFE VERIFY METHOD (proven): copy project to /tmp/verify-copy, `sed` the hardcoded
  live path → copy path in tools/parse_page.py, tools/parse_homepage.py AND
  qa/verify_export.py:33, copy pages/ + root pastes, run the copy's verify against the
  REAL out/ path. Live files untouched (mtimes verified identical before/after).
- RULE FOR EVERYONE: NEVER run qa/verify_export.py on the live project after ANY
  post-paste data-file edit. Earlier rounds were safe only because no post-paste edits
  existed yet. This must be added to the project notes / AGENTS.md.

## 5. Verification (post-recovery export) — all numbers

- Export: all routes 200, 404 handled, styles.css minified 57883→22564 B.
- Schema validator: 34 pages, 92 scripts, ERRORS 0, WARNINGS 0, NOTES 6 (by design:
  no publisher logo; no Article 'image' — note text is stale, heroes now exist, but the
  facts are unchanged by design; do not change the paste's schema).
- Copy-verify (patched copy, /tmp/verify3.txt): FAILURES 129 — ALL RECONCILED, 0 problems:
  28 word-diffs (homepage −57 = T9 33 + T10 24 per the verify's words() — CORRECTION:
  FINDINGS-sentence-cuts.md says 30/22 by hand-count; words() counts 33/24, sum 57,
  exactly the observed delta; the sentences are unchanged, only the count was off) +
  27 pages (removed related items + anchor word deltas, exact to the word) + 101 link
  failures (all in the authorized sets: removed related links + old homepage anchor +
  8 de-links; the 32 not-reported ones are explained by the verify's own rule — the
  link renders elsewhere in the doc, or href+text present separately).
- H1 = 1 per page; 0 self-links (except paste-annotated, kept verbatim — none found
  beyond those); 0 dashes (literal + entities) in served text; sitemap 31 = llms 31;
  robots/llms 200.
- Render counts: details-card 26, detail-icon 181, help 6+6, kinds 13+13, areas 6+6,
  about-buttons 1, call-zip-line 1, hero-img 34/34, empty h2 0, FEMA/Cat3 sentences 0.
- Related: 27/27 = 3 items; body "/" links 27/27 exactly 1; homepage anchors 27 distinct;
  old anchor 0 hits anywhere.
- Menu: dropdown click-opens with exactly 7 (Emergency Water Removal, Structural Drying,
  Sewage Backup Cleanup, Flood & Storm Cleanup, AC Leak, Ceiling Leak, Burst Pipe);
  mobile menu 7; footer services 17/17 (incl. the 5 previously unlisted:
  cast-iron-pipe, vacant-home, appliance-leak, floors, cabinets).
- Screenshots (qa/screenshots-hero-round/, 86 files + probe.json): hero viewport shots
  desktop + mobile for all 34 routes (VIEWED — contact sheets + full-size spot checks);
  details cards home/water-removal/cost; help/kinds/areas grids; about/call buttons;
  cost table desktop + mobile; menu dropdown (click) + mobile menu; footer; favicon
  16/32/48/64px. Overflow 0 on all 34 pages at 1440 + 390 (probe.json). Console errors 0.
- Visual verdicts: heroes all readable (scrim 0.70 works — white H1 + gold links over
  every photo); kinds text readable over scrims (gold #ffd9a8 links); details cards
  clean, icons match rows, zero orange; help cards beautiful + relevant; area cards
  place-correct; tables beautiful (desktop) + horizontally scrollable in .table-wrap
  (mobile, page overflow 0); favicon bold + readable at 16px. Screenshot capture notes:
  element shots of the cost details card / areas grid / call button showed the sticky
  header overlapping the capture — a capture artifact (full-page crop / scroll-offset
  re-shots confirmed the cards render clean); the mobile cost table is cut in the
  element shot because it scrolls inside .table-wrap (by design); the first kinds-grid
  shot captured the help grid (same class, first in DOM) — re-shot with .nth(1).
- NOT measured: live Speed Index (needs real-browser PageSpeed; PSI API 429 on anonymous
  quota); map tiles need one real-browser look (blank in VM Chromium, markup correct).

## 6. Open items (his call / later)

- "Seasonal Home Water Damage" (vacant-home footer label, from page title) vs "Vacant Home
  Water Damage" (from slug) — flag for his call.
- Kinds-water-heater-leak.jpg: tiny illegible label on a storage bin (right edge) — flag if
  he objects.
- Homepage area section (H2 "Water Damage Help Across Lee County") NOT card-treated —
  Estero/Bonita share one paragraph; needs his decision on splitting.
- Map tiles: one real-browser look needed. Live Speed Index: unmeasured.
- Old domain / old repo: NOT touched (later, after his pages.dev review, on his word).
- Seabees photo on the Next.js site: his call, "Seabees baad me". Batch-3 Next.js push
  still waits on his word + token (source dbdbd98, local only).

## 7. Phase 2.5 — Task 6 audit (done in this round; the DEDUP is a separate worker)

Per-page <main> internal-link audit on the FINAL export: 31/34 pages have a target linked
more than once in <main> (header/footer exempt). Homepage worst: /condo-leak/ x4.
Full per-page table is in the coordinator's report (parent). The two named sentences are
NOT yet removed: homepage "See condo water damage for the full walkthrough." and
"See commercial water damage." (Vacation Rentals bullet). The dedup worker must decide
the card-vs-body tension and record it: Related/kinds/help/area CARD links are navigation
(card purpose) vs BODY COPY links (prose) — coordinator's recommendation: keep card links,
de-link body-copy duplicates (words kept plain); first occurrence keeps the link otherwise.
Worker brief carries the CRITICAL verify_export.py warning (§4c).

## 8. Files changed in this round (git status at Phase 2 close)

Modified: site/includes/functions.php, site/includes/header.php, site/data/pages.php,
site/data/media-manifest.php, site/data/homepage.php, site/data/areas.php + 27 related-3
data files, site/assets/css/styles.css, site/favicon.svg, qa/STATUS-20x.md.
Untracked: site/data/manifest-kinds.php, site/assets/img/ (93 files), qa/FINDINGS-*.md,
qa/manifest-*.php, qa/css-snippet-*.css, qa/patch-*.txt, qa/screenshots-hero-round/,
qa/rel_trim_results-K-original.json, qa/recover-related-3.py (n/a — recovery used
/tmp/rel_trim.py + /tmp/rel_delink.py + /tmp/fix_areas.py, all in /tmp).
NOT committed, NOT pushed — deploy waits on the parent steering the GitHub token.
Commit author when pushing: GrowthAura <noorullahchhachher2@gmail.com>.

## §8. GPS HEMISPHERE FIX — 4 masters (2026-11-19 ~20:40 PKT, coordinator)
- DEFECT: the 4 downscaled masters (lehigh-acres, north-fort-myers, estero, bonita-springs — 1600x1067, downscaled by coordinator at Phase 1 close) carried GPSLatitude/GPSLongitude VALUES but NO GPSLatitudeRef/GPSLongitudeRef tags. Without the Ref tags the hemisphere is undefined per EXIF spec (most readers guess North/East, but it is not encoded). All other 89 files had Ref=North/West.
- CAUSE: the downscale + re-tag step wrote the coordinate magnitudes but dropped the Ref tags.
- FIX: `exiftool -overwrite_original -GPSLatitudeRef=North -GPSLongitudeRef=West` on the 4 exact files (no _original files created; verified none left).
- VALUES (unchanged, verified correct): lehigh 26deg36'45.36"N 81deg38'12.12"W (26.6126,-81.6367); north-fort-myers 26deg41'17.88"N 81deg52'50.88"W (26.6883,-81.8808); estero 26deg25'57.72"N 81deg48'24.48"W (26.4327,-81.8068); bonita-springs 26deg20'23.28"N 81deg46'43.32"W (26.3398,-81.7787).
- RE-VERIFY: full 93-file Ref scan = 0 missing/wrong. GPS check script: OK 93, WRONG 0, MISSING 0. EXIF audit: 0 real XMP APP1, 0 AI markers (re-tag added nothing).
- NEW MD5s (re-tag changes file bytes; reuse corpus md5s for these 4 are now stale — noted, not re-run: values are identical, only 2 Ref tags added): lehigh 69553b4310e1bf74f70f6657e33f57ad; north-fort-myers c349d3d78f52e270241c8207c6c6669d; estero bba8c9fb3d4e1b8802d653be151e56bb; bonita 417df5025ba0da25cc6dc7e9705fd4e9.
- RE-EXPORT: `python3 qa/export_cloudflare.py out` re-run; out/ copies of the 4 carry North/West refs; site-vs-out md5 MATCH on all 4.
- POST-FIX RENDER COUNTS (same export): details-card 26/26, detail-icon 181/181, hero-img 34/34, related-3 27/27. Schema 0 errors / 0 warnings (34 pages, 92 scripts). Sitemap 31, llms 31.

## §9. SLUG CHECK vs OLD LIVE SITE — 101% same (2026-11-19 ~20:40 PKT, coordinator)
- Old live sitemap fetched (https://fortmyerswaterdamagerestoration.us/sitemap.xml, crawled 2026-11-19 15:31 UTC): 30 slugs.
- Our sitemap: 31 locs. Our total routes (sitemap + 3 legal): 34.
- "In old but NOT ours": NONE. Every old route exists in ours, identical slug.
- "In ours but NOT old sitemap": /about/ + /privacy-policy/ + /terms/ + /disclaimer/. The 3 legal pages are noindex + excluded from sitemap BY DESIGN on both sites (the old site has them too, just not in its sitemap). /about/ is the one genuinely new route — the owner's own about paste, built in this PHP round (not invented). So: 33 old routes + /about/ = 34, exactly as ordered.
- Domain attach changes NOTHING about URLs: same slugs, same trailing-slash form, same host path structure.

## §10. WCAG / COLOUR FIXES — re-verified in the BUILT (minified) CSS (2026-11-19 ~20:40 PKT, coordinator)
- H2 sitewide: `.page-body h2:not(.details-card h2){color:var(--teal)}` — river teal #0B5563, 8.42:1 on white. PRESENT in out/assets/css/styles.css.
- H3 sitewide: `.page-body h3:not(.kind-card h3){color:var(--coral-dark)}` — coral-dark #9A3412, 7.31:1 on white. PRESENT.
- Dropdown current-page: `.nav-dropdown span.nav-current{color:var(--coral-dark)}` — 6.49:1 (was 4.21:1 fail). PRESENT; the old `color:var(--coral)` base rule is overridden by this later rule.
- Focus ring: `:focus-visible{outline:3px solid var(--gold);outline-offset:2px;box-shadow:0 0 0 6px #8a6d1f}` — dark-gold outer ring 4.90:1 on white. PRESENT.
- Hero scrim right stop 0.70: PRESENT in built CSS (`rgba(6,32,40,0.70`).
- --coral-dark defined as #9a3412 in built :root. Text size: 20px unchanged (0 font-size declarations in L's block, verified at Phase 2).

## §11. PHASE 2.5 TASK 6 LINK DEDUP — INDEPENDENT VERIFICATION (2026-11-19 ~21:10 PKT, coordinator)
- Worker (8460e7c0) delivered ~21:00 PKT. Findings: qa/FINDINGS-link-dedup.md. 31 data files edited, re-exported, local only.
- INDEPENDENT AUDIT (coordinator, on my own fresh re-export of out/): 34 pages, **522 total links in <main>, 522 unique — 0 duplicate targets** (was 659). Related 27/27 = 3 items; homepage anchors 27 distinct of 27; exactly one "/" per Related page. H1=1 all pages; 0 dashes; 0 self-links in <main>; no empty p/li/td; details 26/26; heroes 34/34. Schema 0/0 (34 pages, 92 scripts). Overflow: **0 on all 34 routes at 390 + 1440** (my own Playwright probe, static export).
- WORD-DIFF vs pre-dedup export (/tmp/dedup-pre-out): **-377 words total — EXACT match** to the worker's claim. Per-page deltas match the worker's table exactly; 27 pages carry word removals (4 pages de-link-only: areas, contact, slab-leak, terms).
- COPY-VERIFY (patched /tmp/verify-copy, /tmp/verify4.txt): FAILURES 181 = 28 word-diffs + 143 link failures + 10 FAQ mismatches. ALL RECONCILED, 0 unexplained: word-diffs = Phase 2 -438 (already reconciled) + dedup -377 + 3 naive-splitter +/-1 artifacts (cost, how-it-works, insurance); link failures = 48 dedup + 68 K-related + 27 anchor-variation artifacts (the old "Water damage restoration in Fort Myers" anchor, now replaced by K's 27 unique anchors — target still links once); FAQ mismatches = 10, each a dedup pointer-sentence removal from a FAQ answer.
- NAMED SENTENCES: "See condo water damage for the full walkthrough." = 0 hits anywhere (site/data, out/, llms-full.txt). "See commercial water damage." = exactly 1 hit in llms-full.txt, on /how-it-works/ — the legitimate single kept occurrence on that page; the homepage copy is gone.
- CORRECTIONS to the worker's §6 prose (data itself is exact): §6 says "73 removed sentence occurrences (72 REMOVE-SENTENCE + 1 REMOVE-BLOCK)" and "29 pages" — the §3 list actually holds **74 REMOVE-SENTENCE + 1 REMOVE-BLOCK = 75 sentence removals**, and **27 pages** carry word removals (4 more pages de-link-only). Total 137 removals (62 DELINK + 74 REMOVE-SENTENCE + 1 REMOVE-BLOCK) is correct and matches the §3 line count.
- FLAG FOR THE OWNER (worker's own, confirmed): 3 homepage help cards now carry NO link ("Sewage backup cleanup", "Flood and storm cleanup", "Leaks of every kind") because kinds cards won those 9 overlaps. The flip is mechanical if he prefers help cards linked instead (re-link the 9 help-card words, de-link the 9 kinds "See X." sentences).
- GPS refs still North/West in out/ after my re-export (post-dedup). md5s of the 4 fixed masters unchanged since the fix.
