# STATUS — Fort Myers PHP hero-images + design round (coordinator 17ff0e4c)
## Updated: 2026-11-19 ~18:20 PKT

## Already done (parent, local only — in the working tree, DO NOT revert)
- Header brand cut: site/includes/header.php — brand-name "Fort Myers Water Damage",
  tagline "24/7 · FL", aria-labels updated. Parent re-exported + verified.
- Tasks 9 + 10 (coordinator): FEMA sentence + Category 3 sentence removed from
  homepage.php (whole 'p' blocks). Record: qa/FINDINGS-sentence-cuts.md.

## Working tree (git status, ~18:20 PKT)
- M site/includes/header.php, M site/data/homepage.php (Tasks 9+10), M qa/STATUS-20x.md
  (QA bookkeeping from the last round — leave it).
- out/ re-exported by parent after the header cut (before Tasks 9+10).

## Tasks in this round
- T1 Hero images, 34 routes (geotagged, 1001% relevant, self-made, no AI metadata)
- T2 Details card beautify — icons/row, orange removed, H2/H3 colour; EXTENDED to
  EVERY service page's card (all row labels, best stylish H2)
- T3 "What we help with" ul -> 6 cards with small images (homepage only)
- T4 "About us" / "How it works" as buttons (homepage only)
- T5 Kinds-grid background images, 13 cards (homepage only)
- T6 One internal link per target per page in <main> (header/footer exempt);
  remove "See condo water damage for the full walkthrough." + "See commercial
  water damage." sentences. NOTE: runs in PHASE 2.5, AFTER all card wiring is
  merged + re-exported (counts must be measured on final markup).
- T7 Area paragraphs -> image cards (6 areas, homepage/areas section)
- T8 "Call 239-356-3708 with your ZIP code." -> real call button
- T9 FEMA sentence cut — DONE (see FINDINGS-sentence-cuts.md)
- T10 Category 3 sentence cut — DONE (see FINDINGS-sentence-cuts.md)
- T11 Table + button colouring (contrast proven)
- T12 Menu = 7 services; rest in footer (footer carries ALL)
- T13 Related = exactly 3 per service page (first 2 + homepage last) + homepage
  anchor UNIQUE per page (variation map) + "/" audit (exactly 1 in <main>)

## BAR RAISED by the owner ~18:20–18:21 PKT (applies to the whole round)
- Colouring SITEWIDE to best-ever (not just tables/buttons/details) + H2/H3 colour
  good SITEWIDE (extends the details-card heading fix to all H2/H3) — contrast-proven
  everywhere, screenshots to prove it. Text stays 20px — DO NOT change body text size.
- Hero images for all (T1, best ever). One-link rule re-confirmed sitewide (T6).
- Goal: site Google + users love; every technical gate green; design end-level.
  No invented content, no ranking promises — report measured numbers only.
- T14 Favicon: replace with a HEAVIER/BOLDER droplet mark (same identity, SVG,
  reads at 16px tab size). Worker M owns it (edits site/favicon.svg directly).

## Workers (all running in parallel; proposal files + new images only, NO shared-file edits except K)
- A heroes group 1 (home + 11 services) — manifest-hero-A.php + FINDINGS-hero-A.md
- B heroes group 2 (12 pages) — manifest-hero-B.php + FINDINGS-hero-B.md
- C heroes group 3 (7 areas + 3 legal) — manifest-hero-C.php + FINDINGS-hero-C.md
- D details card (T2 + extension) — css-snippet-details.css + patch-details-functions.txt + FINDINGS-details-card.md
- E help cards (T3) + buttons (T4) + call button (T8) — images + manifest-help-E.php + css-snippet-help.css + css-snippet-buttons.css + patch-help-functions.txt + patch-buttons-homepage.txt + patch-call-button-homepage.txt + FINDINGS-help-cards.md + FINDINGS-call-button.md
- F kinds backgrounds (T5) — images + manifest-kinds-F.php + css-snippet-kinds.css + patch-kinds-functions.txt + FINDINGS-kinds-cards.md
- G area cards (T7) — images + manifest-areas-G.php + css-snippet-areas.css + patch-areas-functions.txt + FINDINGS-areas-G.md
- I tables + buttons colour (T11) — css-snippet-tables-buttons.css + FINDINGS-tables-buttons.md
- J menu 7 (T12) — DONE ~18:20 PKT (proposal files only). KEY FINDING verified by
  coordinator: real service inventory is 17, not 12 — $NAV_SERVICES holds 12;
  cast-iron-pipe, vacant-home, appliance-leak, floors, cabinets have NO nav today.
  Chosen 7 = first 7 of today's $NAV_SERVICES (water-removal, drying, sewage,
  flood, ac-leak, ceiling-leak, burst-pipe). Footer becomes 17 (12 + 5 new labels
  proposed from titles/H1s — "Seasonal Home Water Damage" for vacant-home is
  flagged, owner may prefer "Vacant Home Water Damage"). Patch: $NAV_SERVICES
  becomes full 17 (footer iterates it, no footer code change); new
  $NAV_SERVICES_MENU with the 7 for header + mobile loops.
- K related 3 + anchor variations (T13) — EDITS data files directly (only worker allowed to) + FINDINGS-related-3.md
- L sitewide colour + H2/H3 (bar-raised) — css-snippet-colour-sitewide.css + FINDINGS-colour-sitewide.md (owns base headings + sections not owned by D/E/F/G/I; hero audit-only)
- M favicon (T14) — edits site/favicon.svg directly + FINDINGS-favicon.md

## Shared resources
- Reuse corpus: qa/reuse-corpus/md5-list.txt + ahash.json (building in background;
  workers fall back to their own fresh scan if not ready at verification time).
- Measured slots: hero home desktop 1440x683 / inner 1440x571; mobile home 390x1019 /
  inner 390x759. Kind-card 381x432 desktop / 350x466 mobile. Details desktop 1192x585.
- GPS: Fort Myers 26.6406,-81.8723; Cape Coral 26.5629,-81.9495; Lehigh Acres
  26.6126,-81.6367; North Fort Myers 26.6883,-81.8808; Fort Myers Beach 26.4442,-81.9557;
  Estero 26.4327,-81.8068; Bonita Springs 26.3398,-81.7787.

## Phase plan
- PHASE 1 (now): workers A–K produce images + fragments + proposals.
- PHASE 2 (coordinator): merge manifests into site/data/media-manifest.php; apply CSS
  snippets + template patches (details, help cards, kinds, areas, buttons, call button,
  menu, tables/buttons colour); re-export; measure contrast (hero text, kind-card text);
  screenshot desktop + mobile; check word-diff (only authorized changes), H1=1,
  schema 0/0, 0 self-links, 0 dashes, overflow 0 at 320/390/1440, sitemap 31 = llms 31;
  speed lab before/after.
- PHASE 2.5: spawn the link-dedup worker (T6) on the FINAL export: per-page <main>
  link counts, de-link extras (keep words) / remove "See X." sentences, re-export,
  verify every target count = 1.
- PHASE 3: independent verifier (fresh agent) — full 2x verification, own findings file.
- PHASE 4: deploy ONLY when parent steers the GitHub token (not held yet). Commit as
  GrowthAura <noorullahchhachher2@gmail.com>; push main + cloudflare-pages via transient
  askpass (delete immediately); verify live (home 200 byte-identical, inner 200,
  sitemap 200/31, robots/llms 200, bogus 404, hero images loading on sample live pages,
  details card live). Report back with before/after numbers + live link.
- NO domain attach, NO old repo touch, NO invented content/photos/facts, NO AI metadata.

## PHASE 2 — DONE ~20:30 PKT 2026-11-19 (coordinator)
- Merge: manifests, functions.php cases (details/help/p/kinds/area-cards), homepage
  variants, areas grids, menu 17/7, styles.css (9 steps, 2 L-fixes), favicon live in export.
- DEFECTS fixed: (1) details-case truncation (bare `case 'details':` fell through to h2,
  empty <h2></h2>, cards missing — fixed with full 8-line case, re-exported, 26 cards back);
  (2) areas.php boundary bug (fixed via /tmp/fix_areas.py).
- verify_export.py WIPED all data-file edits TWICE (it regenerates 34 files from pastes;
  parsers + verify BASE hardcoded to live paths — a "safe copy" did NOT help until the
  copy's qa/verify_export.py:33 + tools paths were sed-patched). Recovered twice,
  byte-identical to K's original (0 mismatches). RULE: NEVER run qa/verify_export.py on
  the live project after any post-paste data-file edit. Full log: qa/FINDINGS-hero-images.md §4.
- Verification: schema 34pp/92 scripts ERRORS 0 WARNINGS 0 NOTES 6; copy-verify 129
  failures ALL reconciled (28 word-diffs exact, incl. homepage -57 = T9 33 + T10 24;
  101 link-fails all authorized); render counts all exact (details 26/181, heroes 34/34,
  related 27/27=3, anchors 27 distinct); overflow 0 all pages 1440+390; console errors 0;
  screenshots 86 files in qa/screenshots-hero-round/ (all 68 heroes + elements VIEWED).
- Weight: 4 masters downscaled 1600x1067 q55 (lehigh 498->365, NFM 469->340, estero
  343->260, bonita 304->223); rest accepted.
- PHASE 2.5 NEXT: link-dedup worker (Task 6) — audit: 31/34 pages have dup body targets;
  two named "See..." sentences still to remove. Worker brief carries the verify warning.
- PHASE 3: independent verifier after 2.5. PHASE 4: deploy only on token steer.

## GPS HEMISPHERE FIX + SLUG CHECK — 2026-11-19 ~20:40 PKT (coordinator)
- GPS: 4 downscaled masters lacked GPSLatitudeRef/GPSLongitudeRef (values present, hemisphere unencoded). Fixed with exiftool -overwrite_original (North/West), no _original files. Full 93-file re-scan: 0 missing/wrong. EXIF audit: 0 XMP, 0 AI markers. Re-exported; out/ copies verified North/West, md5 match site.
- Slugs: old live sitemap 30 slugs; ours 31 + 3 legal = 34 routes. Old-but-not-ours: NONE. Ours-but-not-old: only /about/ (owner's paste) + 3 legal (noindex, by design both sides). 101% same.
- WCAG: H2 teal, H3 coral-dark, dropdown coral-dark, focus ring, scrim 0.70 — all confirmed PRESENT in the built minified CSS.
- Post-fix counts: details 26/181, heroes 34/34, related 27/27, schema 0/0, sitemap 31, llms 31.
- PHASE 2 HANDOFF READY. Deploy (parent): push main + cloudflare-pages, attach fortmyerswaterdamagerestoration.us via API {"name": ...}. DNS change is the owner's step; old Vercel site stays live until then.

## PHASE 2.5 TASK 6 DEDUP — VERIFIED 2026-11-19 ~21:10 PKT (coordinator, independent re-verification)
- Worker done ~21:00 PKT: 31 files, 137 removals (62 delink + 74 sentence + 1 block), 659 -> 522 links in <main>, 0 dup targets.
- Coordinator re-verified independently: link audit 522/522 unique, related 27/27 x3, anchors 27 distinct, "/" 1/page, H1 1, dashes 0, self-links 0, schema 0/0, overflow 0 at 390+1440, word-diff -377 EXACT, copy-verify 181 failures ALL reconciled (0 unexplained), named sentences gone (homepage "See commercial water damage." survives only as the single kept occurrence on /how-it-works/).
- Two prose slips in the worker's §6 corrected (75 sentence removals, 27 pages with word removals — data exact).
- FLAG for owner: 3 homepage help cards now link-free (kinds won the 9 overlaps); flip is mechanical if he prefers otherwise.
- ROUND COMPLETE: Phase 1 + Phase 2 + Phase 2.5 ALL VERIFIED. Deploy (parent): push main + cloudflare-pages, attach fortmyerswaterdamagerestoration.us via API {"name": ...}. DNS change is the owner's step.
