# Hero images — worker B findings (Fort Myers PHP site)

**Date:** 2026-11-19
**Pages:** 12 (flood-cleanup, water-heater-leak, appliance-leak, floors, cabinets, commercial, first-hour-checklist, cost, insurance, how-it-works, contact, about)
**Verdict: 12/12 FILLED. 0 honestly empty.**
**Method:** competitor pages searched for inspiration only (DryOut Inc, SERVPRO Central Ft. Myers, CAT 3 Recovery, Redline — flood/muck-out/extraction/drying themes; NO competitor images downloaded or copied). Every image self-generated with the media pipeline, then post-processed with PIL (resize, JPEG re-encode) + exiftool (`-all=` strip, then GPS only). Each finished image viewed at full size by this worker.

## Slot
Hero slot measured: desktop 1440 wide (inner hero 1440×571), mobile 390 wide (inner 759 tall), `object-fit: cover`. All images 1920×1280 (3:2) masters + 960×640 variants, subject centred so both crops survive. Hero text sits on a scrim over the image.

## Results table

| page | file | GPS | dimensions | weight KB | slot | relevance verdict + reason |
|---|---|---|---|---|---|---|
| flood-cleanup | hero-flood-cleanup.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 179 / 57 | hero | PASS — flooded tile floor, technician from behind with squeegee, extractor + air movers, flood-cut baseboard, palms through sliders. Matches H1/intro (floodwater, muck-out, drying). |
| water-heater-leak | hero-water-heater-leak.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 204 / 74 | hero | PASS — white tank centred in garage, puddle spreading at base, gloved hand + vacuum hose, palms outside door. Matches intro (pooling water, garage tank). Nit: tiny illegible labels on shelf spray bottles (unreadable at hero size). |
| appliance-leak | hero-appliance-leak.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 165 / 58 | hero | PASS — front-load washer, water pooling on tile, gloved hands laying towels, palms at window. Matches intro (washer overflow, hidden water). Nit: washer panel markings illegible. |
| floors | hero-floors.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 138 / 55 | hero | PASS — vinyl planks lifting/curling at seams, moisture meter in gloved hand, air mover, palms. Matches intro (lifting LVP, trapped slab water). Meter screen digits illegible. |
| cabinets | hero-cabinets.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 145 / 56 | hero | PASS — open white cabinets, swollen water-stained base, moisture meter in gloved hand, air mover under toe kick. Matches intro (swollen cabinet bottoms, trapped water). |
| commercial | hero-commercial.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 256 / 82 | hero | PASS — flooded open-plan office, technician from behind with extractor, air movers, desks, palms through full-height windows. Matches intro (office floor, business hours). |
| first-hour-checklist | hero-first-hour-checklist.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 145 / 58 | hero | PASS — hands photographing a wet ceiling stain with a phone (screen blank), shut-off valve, flashlight + towel, puddle below. Matches HowTo steps (photograph, stop the water). Phone camera UI glyphs illegible. |
| cost | hero-cost.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 146 / 57 | hero | PASS — technician from behind measuring a damp, stained wall, BLANK clipboard + pen on ladder, air mover + dehumidifier. Assessment theme, no readable numbers. Matches intro (written number comes after moisture is measured). |
| insurance | hero-insurance.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 127 / 55 | hero | PASS — blank papers, blank folder, pen, phone with blank dark screen on a table, palms out of focus. Claim/documents theme, no readable text. Matches intro (policy, claim). |
| how-it-works | hero-how-it-works.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 176 / 62 | hero | PASS — technician from behind setting up air movers + dehumidifier along a damp wall, extraction wand + hoses, palms. Process theme, matches intro (first call to final dry reading). |
| contact | hero-contact.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 166 / 57 | hero | PASS — front desk with desk phone (blank display), potted palm, plain white van (no lettering) through glass door. Phone/office theme, no readable text. |
| about | hero-about.jpg / -960w.jpg | 26.6406,-81.8723 | 1920×1280 / 960×640 | 230 / 81 | hero | PASS — three technicians seen from behind loading air movers + dehumidifier into a plain white van, Florida stucco house + tile roof + palms. Team/office theme, no faces, no fake portraits. |

**Honestly-empty pages: NONE.**

## Weight — aim missed on 7 masters / 4 variants (recorded honestly)
- Aim: master <150 KB, variant <60 KB, JPEG q~80. Achieved: 5/12 masters, 8/12 variants.
- Over: masters flood-cleanup 179, water-heater-leak 204, appliance-leak 165, commercial 256, how-it-works 176, contact 166, about 230; variants water-heater-leak 74, commercial 82, how-it-works 62, about 81.
- Why: these detailed photographic frames have a flat quality/size curve — commercial at q40 is still 230 KB (vs 256 KB at q55) and about at q40 is 207 KB; lowering quality further would visibly degrade the image without meeting the aim. Mild Gaussian blur was tested and rejected (worse size/quality trade). Quality floor held at q55; the worst case (commercial q55) was viewed at full size after encoding and shows no visible compression artefacts; heroes sit under a dark scrim with H1 on top. If the coordinator wants the aim met strictly, the only honest lever is a smaller master (e.g. 1600w) — not done here, as the task specified 1920×1280.

## EXIF / AI check — PASS (24/24)
- `exiftool -all=` strip, then GPS only: `-GPSLatitude=26.6406 -GPSLongitude=-81.8723` (26°38'26.16"N, 81°52'20.28"W).
- `exiftool -a -G1` on hero-flood-cleanup.jpg: only GPS tags in EXIF (GPS Version ID, Latitude/Longitude + Refs) plus standard IFD0 resolution tags (X/Y Resolution 72, Resolution Unit, YCbCr Positioning). PIL `getexif()` on all 24: tag set exactly [282, 283, 296, 531, 34853] on every file — no Software, no Artist, no Copyright, no UserComment, no XMP.
- Raw-byte scan for `XMP / AI-Generated / CreatorTool / Adobe / c2pa / Content Credentials / openai / dalle`: 1 flag — lowercase `xmp` byte sequence inside hero-cabinets.jpg. JPEG marker parse proves it a false positive: the file has exactly ONE APP1 segment (Exif, 212 bytes); no XMP APP1 segment exists. The match is a random byte sequence inside entropy-coded image data.
- 0 AI markers on 24/24. Final re-verification after all concurrent work: all 24 files still 26.6406,-81.8723 with md5s unchanged.

## Reuse nets — PASS
1. **md5 (fresh disk reads):** my 24 md5s vs the coordinator's fresh workspace-wide corpus `/tmp/fm_corpus_md5.txt` — 79,289 image files hashed 2026-11-19 13:27–13:33 (parallel xargs, incl. export/out/public/gh-pages dirs), DONE marker present: **0 non-self hits**. My own parallel scan (single-threaded, stopped at 16,122 files after the corpus completed): also 0 non-self hits in the portion covered. Note: `qa/reuse-corpus/md5-list-task7.txt` (501 lines) covers only the fort-myers-php project itself, so it was NOT used as the workspace net — my files appear in it only as self-hits.
2. **aHash 16×16 (pure-PIL implementation):** pairwise among my 12 masters, closest pair d=64 (flood-cleanup vs commercial); vs the 3 sister/banned Fort Myers images (`fort-myers-florida-storm-flooding-hero.jpg` = banned European house, `fort-myers-lee-county-storm-coast.jpg`, `fort-myers-florida-gulf-coast-storm.jpg`) min distance d=68 — **no flag <25 anywhere**, so no side-by-side MAD adjudication triggered. Sanity: each master vs its own 960w variant d=0–1, so the implementation is sound.
3. **Pexels-ID check:** my filenames contain no numeric IDs (grep `[0-9]{7,}` over all 24 names: none); all 12 images self-generated, no Pexels source used; banned IDs (28447774, 14216445, 14216449, 13865770–79, 8292785, 8293664, 11899611, 32497161, 6419128) — zero hits under `site/assets/img/`.
4. **Visual:** every finished image viewed at full size by this worker (raw + final q55 commercial re-check). None is a copy of any known site photo; each matches its page's H1 + intro (see table). No wrong-country / wrong-place / wrong-service frame.

## Alt text
Honest, page-specific descriptions of what is shown; no invented facts, addresses or names. Full strings in `qa/manifest-hero-B.php`.

## ⚠️ INCIDENT — cross-worker EXIF contamination (must be verified by the coordinator before deploy)
- My EXIF pass used a `hero-*.jpg` glob in the shared `site/assets/img/` dir. At that moment (2026-11-19 ~13:21 UTC) sibling image worker(s) were writing their own heroes into the same dir concurrently, and my loop stripped + re-geotagged **all 67 files then present** with Fort Myers 26.6406,-81.8723 — including ~43 files that are NOT mine (areas, disclaimer, estero, drying, fort-myers-beach, home, ac-leak, ceiling-leak, lehigh-acres, condo-leak, north-fort-myers, privacy-policy, cast-iron-pipe, sewage-cleanup, terms, vacant-home, burst-pipe, water-removal, mobile-home, slab-leak, cape-coral, bonita-springs).
- Evidence the siblings use per-area GPS: bonita-springs now carries 26.3398,-81.7787 and cape-coral 26.5629,-81.9495 (re-written by the sibling after my pass). Area pages (estero, lehigh-acres, north-fort-myers, fort-myers-beach) now showing 26.6406 were very likely re-stamped by me and need their own area GPS re-applied.
- Damage is metadata-only (pixels untouched; `-all=` + GPS write touches EXIF only). But any md5s the siblings computed before ~13:21 UTC are stale, and their GPS values must be re-verified/re-applied on ALL their files before deploy.
- MY 24 files are verified intact after the fact (dimensions + GPS + md5 re-checked at the end of this task, all OK). I did not touch any other file after discovering this, and used exact filenames (never globs) for all later steps.

## Files delivered
- Images: `site/assets/img/hero-<slug>.jpg` + `hero-<slug>-960w.jpg` for the 12 slugs above (24 files).
- Manifest fragment: `qa/manifest-hero-B.php` (php -l clean; 12 entries; every src + variant verified to exist on disk).
- This note: `qa/FINDINGS-hero-B.md`.
- Raw generations kept at `qa/gen-raw/media-generation-hero-<slug>-raw-*.jpg` (12 files + JSON sidecars) for audit; NOT referenced by the manifest.
- No shared file edited (no styles.css, functions.php, data files, media-manifest.php, header.php). No commit, no push, local only.
