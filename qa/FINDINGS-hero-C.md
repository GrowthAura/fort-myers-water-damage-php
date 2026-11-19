# Hero images — Group C findings (Fort Myers PHP site)

**Date:** 2026-11-19
**Worker:** image worker C (pages: cape-coral, lehigh-acres, areas, north-fort-myers, fort-myers-beach, estero, bonita-springs, privacy-policy, terms, disclaimer)
**Slot:** hero, desktop inner 1440x571, mobile inner 390x759 (object-fit:cover, subject centred to survive both crops)
**Method:** competitor pages searched for inspiration only (Cape Coral canal/dock scenes, Fort Myers Beach elevated homes + white sand — never downloaded/copied); every image generated fresh with the media tools, then post-processed with PIL + exiftool. Prior rejections in `qa/hero-findings.md` read first — no web stock used at all, so the Sanford/CBP/European-house/banned-ID failures cannot recur.
**Honestly-empty pages:** NONE — all 10 pages filled.

## Results

| page | file | GPS | dimensions | weight KB (master / 960w) | slot | relevance verdict + reason |
|---|---|---|---|---|---|---|
| cape-coral | hero-cape-coral.jpg | 26.5629,-81.9495 | 1920x1280 / 960x640 | 283 / 88 | hero | PASS — residential canal with screened pool enclosures, private docks, small boats, royal palms. Exactly the canal city the page describes (canals, slab homes, canal flooding). |
| lehigh-acres | hero-lehigh-acres.jpg | 26.6126,-81.6367 | 1920x1280 / 960x640 | 498 / 139 | hero | PASS — single-story concrete-block ranch homes on large grassy lots, paved street, drainage swale, palms + moss-draped oaks. Inland Florida residential, matches the page (wells/septic, slab block homes, street flooding). |
| areas | hero-areas.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 213 / 68 | hero | PASS — historic brick riverfront buildings + royal palms along the Caloosahatchee at sunset in downtown Fort Myers. Page is the Lee County service-area hub; Fort Myers riverfront is the right anchor. |
| north-fort-myers | hero-north-fort-myers.jpg | 26.6883,-81.8808 | 1920x1280 / 960x640 | 458 / 133 | hero | PASS — manufactured home with carport on a large lot beside the Caloosahatchee, wooden dock, palms + live oaks. Matches the page exactly (manufactured/55+ communities, riverfront + canal homes, wells/septic). |
| fort-myers-beach | hero-fort-myers-beach.jpg | 26.4442,-81.9557 | 1920x1280 / 960x640 | 256 / 79 | hero | PASS — elevated beach house on tall wooden pilings behind white sand, sea oats and turquoise Gulf water. Matches the page (elevated/rebuilt homes, storm surge, Estero Island flood rules). |
| estero | hero-estero.jpg | 26.4327,-81.8068 | 1920x1280 / 960x640 | 343 / 106 | hero | PASS — Mediterranean stucco condo/coach-home buildings with tile roofs around a landscaped courtyard with fountain, palms. Matches the page (gated neighborhoods, coach homes, villas, condos). |
| bonita-springs | hero-bonita-springs.jpg | 26.3398,-81.7787 | 1920x1280 / 960x640 | 297 / 91 | hero | PASS — riverfront condos/homes with tile roofs beside a mangrove-lined river, small dock. Matches the page (Imperial River neighborhoods, coastal condos near Bonita Beach, gated communities). |
| privacy-policy | hero-privacy-policy.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 142 / 46 | hero | PASS — blank papers, small brass padlock, closed laptop, pen on a bright desk. Document/privacy theme, no readable text, no people. |
| terms | hero-terms.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 144 / 47 | hero | PASS — blank cream papers, fountain pen, reading glasses on a wooden desk by a window. No readable text, no people. |
| disclaimer | hero-disclaimer.jpg | 26.6406,-81.8723 | 1920x1280 / 960x640 | 134 / 41 | hero | PASS — small blank metal shield beside a stack of blank papers and a closed laptop. No readable text, no people. |

All 10 images viewed at full size by the worker: no readable text, no signage, no logos, no watermarks, no close-up faces, no wrong-country/wrong-place content. One nit noted: the terms image has faint illegible markings on a glasses temple (not readable as text at full size) — accepted.

## Weight — AIM MISSED, recorded honestly

Aim was master <150KB, variant <60KB at JPEG q~80. Only the three legal pages meet it (134–144KB masters at q80). The seven outdoor scenes do not: even at q55 the masters are 213–498KB, and tests proved the gap is structural, not a settings miss — q35 still leaves Lehigh Acres at 387KB, and a 0.8px Gaussian blur + q70 still leaves it at 457KB (dense grass/foliage detail). Forcing <150KB would need q~25 or heavy blur, visibly damaging a hero. Kept at q55 (masters) / q55 (variants): the q55 Cape Coral master was viewed at full size after compression and shows no visible blocking in sky or water. Coordinator call: accept the weights, or downscale the master — do not re-compress lower.

## EXIF / AI check

- Every final (20 files) run through `exiftool -all=` (strip everything) then GPS-only rewrite. `exiftool -a -G1` on all 10 masters: IFD0 holds only resolution tags; the only GPS-group tags are GPSVersionID + lat/lon + refs; no XMP, no IPTC, no MakerNotes, no Software/CreatorTool. AI-marker grep (AI|Generat|CreatorTool|Adobe|Prompt) across all 20 finals: 0 hits.
- GPS verified numerically (`exiftool -n`) on all 20 finals after the fix below: cape-coral 26.5629,-81.9495; lehigh-acres 26.6126,-81.6367; areas 26.6406,-81.8723; north-fort-myers 26.6883,-81.8808; fort-myers-beach 26.4442,-81.9557; estero 26.4327,-81.8068; bonita-springs 26.3398,-81.7787; privacy-policy/terms/disclaimer 26.6406,-81.8723. All correct, re-checked after 90s idle with no drift.

### GPS DRIFT INCIDENT — another process rewrote my files (flagged for the coordinator)

My post-process script wrote the correct per-place GPS at ~13:20 and printed the correct values. Subsequent checks found files carrying Fort Myers coords (26.6406,-81.8723) instead: first cape-coral + bonita-springs (both master + variant, mtimes 13:21:17–24), then lehigh-acres, north-fort-myers, fort-myers-beach and estero (mtimes 13:21:39–13:22:20) — a staggered, file-by-file rewrite consistent with a concurrent process tagging hero files with the Fort Myers default. I re-wrote the correct GPS for all six affected slugs (quoted DMS via exiftool, verified numerically) and confirmed all 10 hold after 90s idle (last touches are my own fixes, 13:26:43–50). If the coordinator's later verification finds GPS drift again, the cause is that concurrent writer, not this worker's output — worth identifying before deploy so it does not re-flatten every area page to Fort Myers coords.

## Reuse nets

- (1) md5: PASS (bounded fresh scan) — `qa/reuse-corpus/md5-list.txt` did not exist when verification ran (corpus dir empty), so a fresh scan was run instead: md5 of the 10 finals vs all 458 image files under `~/workspace/fort-myers-php/` (site assets incl. sibling heroes + raw generator outputs, `out/`, `qa/` candidates, screenshots) — **0 collisions**. Whole-workspace md5 was attempted but killed as infeasible: a bare `find` counted **186,425** image files in `~/workspace`, and the hashing walk was still running after ~11 min under heavy concurrent load (sibling workers active). The images were generated fresh and never downloaded, so a byte-identical copy of an existing file is not possible except by coincidence; the site-tree scan is the substantive net and it is clean.
- (2) aHash 16x16 (pure-PIL, fresh disk reads): PASS — my 10 finals vs the same 458-file corpus: the ONLY Hamming-distance <25 flags are each master vs its own 960w variant (distance 0, expected — same image). Zero flags vs any other file (sibling heroes, raw outputs, qa candidates). Pairwise distances among my own 10: 89–149, all far above the <25 flag band — the 10 images are mutually distinct. No side-by-side MAD adjudication was triggered.
- (3) Pexels-ID: PASS — no Pexels ID in any hero-C filename; grep for banned IDs (28447774, 14216445, 14216449, 1386577x, 8292785, 8293664, 11899611, 32497161, 6419128, 8293678, 15206136, 16509869, 32497162) across the 10 filenames: 0 hits. All images were generated fresh, so there is no Pexels source at all.
- (4) Visual: PASS — every finished image viewed at full size by the worker (see table); none is a copy of any known site photo (all generated, no web stock used).

## Deliverables

- Images: `site/assets/img/hero-<slug>.jpg` + `hero-<slug>-960w.jpg` for all 10 slugs (20 files).
- Manifest fragment: `qa/manifest-hero-C.php` — `php -l` clean, 10 entries, alt text per image (honest description of what is shown, no invented facts/addresses/names).
- This findings file: `qa/FINDINGS-hero-C.md`.
- Raw generator outputs (`media-generation-hero-<slug>-*.jpg`) left in `site/assets/img/` — the coordinator may delete them; this worker did not, so as not to touch files another worker might still need. NOTE: sibling workers are generating into the same directory concurrently; only the 10 hero-C slugs above are this worker's.
- No shared file edited (no styles.css, functions.php, data files, media-manifest.php, header.php). No commit, no push, no token. Local only.
