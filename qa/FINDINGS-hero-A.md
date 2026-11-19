# Hero images — Findings (Group A, 12 pages) — Fort Myers PHP site

**Date:** 2026-11-19
**Worker:** image worker A (pages: home, water-removal, drying, sewage-cleanup, ac-leak, ceiling-leak, condo-leak, cast-iron-pipe, vacant-home, burst-pipe, mobile-home, slab-leak)
**Method:** competitor pages checked for inspiration only via web search (DryOut Inc, SERVPRO of Central Ft. Myers, iMold, DryZone, Pure Team — extraction rigs, air movers, dehumidifiers, moisture meters, tile/slab Florida homes). NO competitor image downloaded or copied. Every image generated fresh with the media tools, then viewed at full size, resized to exact slot dimensions with PIL, stripped with `exiftool -all=`, and re-tagged with Fort Myers GPS only.
**Slot:** desktop 1440 wide (home hero 1440x683, inner 1440x571), mobile 390 wide (home 1019 tall, inner 759 tall); `object-fit: cover`. All images are 3:2 (1920x1280 master / 960x640 variant) with the subject centered, so both the wide desktop crop and the tall mobile crop keep the subject.
**GPS (all 24 files):** 26.6406, -81.8723 (Fort Myers) — verified with `exiftool -a -G1`: ONLY GPS tags present (plus standard IFD0 resolution fields written by exiftool), 0 AI markers (no AI/Generated/CreatorTool-AI/XMP/Software/Comment).

## Results

| Page | File | GPS | Dimensions | Weight KB (master / 960w) | Slot | Relevance verdict + reason |
|---|---|---|---|---|---|---|
| / (home) | hero-home.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 144.3 / 59.1 | home hero | PASS — technician extracting standing water from a tiled living-room floor, palms through sliding doors; matches H1 "Water Damage Restoration in Fort Myers, FL" and the intro (slab homes, water under baseboards/vinyl/cabinets). |
| /water-removal/ | hero-water-removal.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 142.0 / 56.8 | inner hero | PASS — submersible pump + extraction wand pulling standing water off tile, hose to doorway, palms outside; exactly the page's standing-water extraction + moisture-mapping work. |
| /drying/ | hero-drying.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 136.5 / 56.6 | inner hero | PASS — commercial dehumidifier + two air movers + moisture meter on a damp baseboard, palms in window; exactly the page's structural-drying equipment and daily readings. |
| /sewage-cleanup/ | hero-sewage-cleanup.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 146.7 / 58.1 | inner hero | PASS — technician in full PPE + respirator vacuuming dark water at a toilet base behind plastic containment sheeting; exactly the page's Category 3 containment/extraction/disinfection work. No face visible. |
| /ac-leak/ | hero-ac-leak.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 127.8 / 53.2 | inner hero | PASS — air handler with condensate drain dripping into a puddle on tile, bucket + towels + vacuum hose, palms in window; exactly the page's AC condensate-overflow cause. |
| /ceiling-leak/ | hero-ceiling-leak.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 148.0 / 58.7 | inner hero | PASS — sagging, brown-stained ceiling dripping into a bucket, gloved hand with a blank-display moisture meter, palms in window; exactly the page's dripping/sagging ceiling. V1 REJECTED (meter display showed a number, "22.4%") and regenerated as V2 with a blank display; V1 file deleted. |
| /condo-leak/ | hero-condo-leak.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 144.2 / 58.5 | inner hero | PASS — water running down a shared condo wall from the ceiling, technician checking the wall with a meter, balcony + palms behind; exactly the page's leak-from-the-unit-above. Technician seen from behind; no face features visible. |
| /cast-iron-pipe/ | hero-cast-iron-pipe.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 165.2 / 57.4 | inner hero | PASS — rusted cast iron drain pipe exposed in an opened wall, pipe wrench, wet vacuum, damp towels; exactly the page's older-home cast iron drain leaks. Master 165 KB is over the 150 KB aim (see weight note). |
| /vacant-home/ | hero-vacant-home.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 144.2 / 57.2 | inner hero | PASS — technician entering a seasonal home with covered furniture and damp, stained tile, palms outside; exactly the page's "back for the season to a wet floor / musty smell". |
| /burst-pipe/ | hero-burst-pipe.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 144.8 / 56.8 | inner hero | PASS — split supply pipe under a kitchen sink spraying water, gloved hand reaching for the shut-off valve, towels on wet tile; exactly the page's burst supply line + shut-off-first steps. |
| /mobile-home/ | hero-mobile-home.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 213.9 / 71.5 | inner hero | PASS — manufactured home in a palm-filled Florida park, technician kneeling with a moisture meter at a damp wall section; exactly the page's soft-floor / belly / water-heater-closet subject. Master 214 KB and variant 71 KB are over the weight aim (see weight note). Final compressed file re-viewed at full size: no visible compression artefacts. |
| /slab-leak/ | hero-slab-leak.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 141.6 / 56.5 | inner hero | PASS — gloved hands testing a damp tile floor with a listening device and moisture meter beside broken tiles exposing wet concrete slab, thermal camera nearby; exactly the page's warm-spot / slab-leak signs. |

**Honestly-empty pages: NONE.** All 12 pages filled.

## Weight note

Aim was master <150 KB, variant <60 KB. 10 of 12 masters and 11 of 12 variants meet it. Two do not, even at JPEG quality 40 (floor — going lower would visibly degrade) plus a 0.5px blur pass: cast-iron-pipe master 165.2 KB (variant 57.4 KB OK) and mobile-home master 213.9 KB / variant 71.5 KB. Both are detail-dense frames (rust/texture, palm foliage). No mozjpeg/ImageMagick on this VM to squeeze further with PIL alone. Accepted as best-effort; the files are still light for a 1920px hero and the mobile-home final was re-viewed at full size after compression.

## Reuse nets (fresh disk reads, 2026-11-19)

- **md5:** the coordinator's `qa/reuse-corpus/md5-list.txt` was NOT ready (empty dir), so I ran my own fresh scan as instructed: full workspace file list (186,408 images) built with `find`, restricted to the live-served corpus — paths under `public/images`, `out/`, `assets/img`, `gh-pages`, `export`, `dist`, `build` (79,289 files, QA/screenshot dirs excluded). My 12 md5s (see below) were compared against that corpus (parallel md5sum, 79,289/79,289 hashed, DONE). RESULT: **ZERO matches to any other file** — the only hits are the 12 files themselves (self-matches inside the corpus).
- **aHash 16x16 (pure PIL):** my 12 masters vs every image under `fort-myers*` dirs (3,278 files, fresh disk read). Flag threshold Hamming <25. RESULT: **23 flags, ALL self-matches only** — each master vs its own 960w variant (distance 0–1) and vs its own media-generation source file (distance 0). **Zero flags against any other file** — the closest non-self distance is ≥25 for every slug, so no side-by-side MAD adjudication was triggered. (A first attempt vs 53,080 topically-named served images was stopped as infeasible on this VM's disk/CPU — ~1 hr projected; the Fort Myers corpus is the highest-risk set since it holds every Fort Myers photo on disk, including the banned old hero, the Sanford candidates, the CBP aerial and the sister-site images, and the md5 net above already covers the full 79,289-file served corpus.) One bookkeeping note: `hero-vacant-home-960w.jpg` does not appear in the aHash target list because the workspace file list was built while that variant was missing (see note below); the regenerated variant is a direct resize of the verified master.
- **Pexels-ID check:** my filenames contain no Pexels IDs (all generated). Filename grep for the banned IDs (28447774, 14216445, 14216449, 13865770–13865779, 8292785, 8293664, 11899611, 32497161, 6419128, 8293678, 15206136, 16509869, 32497162) across the whole workspace: hits exist ONLY in other sites' QA/scout pools (Lancaster `work/img-scout/pool`, Stockbridge raw dirs) — none in `fort-myers-php/`, none among my files.
- **Visual:** every finished image was viewed at full size by me (13 generations viewed: 12 finals + the rejected ceiling V1). None is a copy of any known site photo (banned European house 28447774, Sanford series, CBP aerial, beached-yacht wreckage, Seabees photo, sister-site Fort Myers images) — all are newly generated scenes with distinct compositions. No text, signage, logos, watermarks or legible numbers in any final image (one tiny illegible label on the drying dehumidifier display and one on the burst-pipe cleaning bottle; neither is readable text).

## My md5s (masters, post-EXIF)

- home d80585215e78e0f114cc14f213962ac6
- water-removal 7cabb2a04fbb66f91d3160a9561f41e6
- drying d0e8c405261ef04cfa293db427224446
- sewage-cleanup a77bc20a76c553d5704c257fa83d3265
- ac-leak c4771fc137fb9a902ae7b6121fb58726
- ceiling-leak 9bdea49cd800d9ed3a8b6d76ccfc9bf2
- condo-leak 7a654112fd5ed1a641fea9894c1da62d
- cast-iron-pipe addc88666db94434eb71978c3da5d49b
- vacant-home 0056d753fd5dbf4560b3b273ff58044b
- burst-pipe 7da733f2287221708063110f081f2a6c
- mobile-home 84e38287c6b6fb12523e781bf9a731f2
- slab-leak 9e4ebe92bf83f85777f77ba2ab5d025d

## Files delivered

- Images: `site/assets/img/hero-<slug>.jpg` + `hero-<slug>-960w.jpg` for all 12 slugs (24 files).
- Manifest fragment: `qa/manifest-hero-A.php` (12 entries; verified with `php -r`, parses, 12/12).
- This findings file: `qa/FINDINGS-hero-A.md`.
- No shared file edited (no styles.css, functions.php, data files, media-manifest.php, header.php). No commit, no push, local only.
- NOTE: `hero-vacant-home-960w.jpg` went missing between my compression pass and the EXIF pass (shared img dir; other image workers active in parallel). Regenerated from the retained source generation, re-tagged with GPS, re-verified (960x640, 57 KB, GPS present). Recommend the coordinator re-check all 24 files exist at deploy time.
- NOTE: other workers are writing to the same `site/assets/img/` dir in parallel (hero-about, hero-areas, hero-bonita-springs, help-* etc. were present). I touched only my own 12 slugs' files plus the rejected ceiling V1 (deleted).
