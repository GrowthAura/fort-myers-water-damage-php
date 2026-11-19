# FINDINGS — Task 5: kinds-grid card backgrounds (homepage only)

Date: 2026-11-19. Worker: kinds-card worker (Task 5). No shared file was edited:
no styles.css, functions.php, data files, media-manifest.php, header.php; no
commit, no push. The coordinator applies the proposals and screenshots them.

## Source of truth

- `site/data/homepage.php`, the single `kinds` block (~line 436): 13 cards, in
  the order below. Titles/bodies/links copied from that block; zero word
  changes anywhere.
- Render: `site/includes/functions.php`, `case 'kinds'` (~lines 279-286) —
  `<div class="kinds-grid"><article class="kind-card"><h3>…</h3><p>…</p>
  </article>…</div>`.
- Styles: `site/assets/css/styles.css` ~239-246, 400, 466, 496-505.
- The kinds grid renders ONLY on the homepage (verified) — 13 images total.
- Card slot (measured): desktop 381x432 (3 cols), mobile 350x466 (1 col),
  image is a CSS background with `background-size: cover`.

## Method (honest)

Self-made images from detailed prompts written per card from that card's
title + body (photorealistic restoration-industry style). No competitor site
was browsed — this subagent has no live browser — so "competitor-inspired"
here means: prompts were written to match the look of standard
water-damage-industry photos (real rooms, real damage, no staging), not
copied from any competitor asset. No Pexels or other stock was used at all,
so there are no Pexels IDs anywhere in this task. All 13 raws were viewed
full-size by the worker; the 4 riskiest crops were re-viewed as finals.
Raw generations kept at `qa/kinds-raw/` for audit; processing script
`qa/process-kinds.py`.

## Masters

- 760x864 JPEG, exactly 2x the desktop slot (381x432) for retina crispness.
  Slot ratio 381/432 = 0.882; master ratio 760/864 = 0.880, so desktop
  `cover` shows ~100% of the image. Mobile slot 350x466 (ratio 0.751):
  `cover` scales by height and crops ~30 px per side (~8% of width) —
  subjects are centred, so nothing essential is lost.
- Quality: q80 first pass, then q70, then q60 (q50 for the two most
  detailed) to chase the <60 KB aim. Result: 4 of 13 meet <60 KB; 9 are
  over, heaviest 102 KB. Total for all 13: 960,970 bytes (~938 KB).
  The two detail-heaviest photos (rusted cast-iron texture, flood-water
  ripples) do not compress below ~100 KB without visible artefacts at
  q50, so the run stopped there rather than degrade the photo. The
  <60 KB figure was an aim, not a gate; the grid is below the fold and the
  coordinator may accept the weights or ask for a 1x variant.
- Post-process (PIL + exiftool, both installed): per-image vertical crop
  to the 760:864 ratio (crop offsets chosen after viewing each raw, so the
  key subject survives — e.g. ceiling-leak is top-biased to keep the
  stain), Lanczos resize to exactly 760x864, JPEG save, then
  `exiftool -all=` to strip EVERYTHING, then GPS EXIF only written.
- Geotag: Fort Myers GPS 26.6406,-81.8723 on every file (26°38'26.16"N,
  81°52'20.28"W, altitude 3 m).
- EXIF verified with `exiftool -a -G1` on all 13 (full dump at build time,
  spot-checked again after the re-encodes): the only EXIF group present is
  GPS (GPSVersionID, Latitude/Longitude + refs, Altitude + ref). 0 AI
  markers: no Software, Artist, Creator, Description, UserComment,
  XPComment, dates, or camera tags. The IFD0 XResolution/YResolution 72 dpi
  entries are encoder boilerplate written when the GPS segment is created,
  not metadata. Alt text: N/A for CSS backgrounds — the honest description
  of each final image is in the manifest (`qa/manifest-kinds-F.php`) and in
  the table below.
- Crop note: the final 760x864 crops lose the top/bottom bands of the tall
  raw frames. Three manifest alt texts were corrected to describe the
  FINAL crop as viewed, not the raw: ceiling-leak (bucket is outside the
  crop), condo-leak (towel/puddle outside the crop), vacant-home (wet
  floor patch outside the crop). The card bodies themselves are untouched.

## Readability / contrast (computed, not screenshotted)

Design (in `qa/css-snippet-kinds.css`): photo cards get class `has-photo`
(only when a manifest image exists; a card with no photo keeps the old
white card exactly). Scrim = real overlay element `.kind-scrim`:
`linear-gradient(180deg, rgba(7,38,47,0.86) 0%, rgba(7,38,47,0.78) 55%,
rgba(7,38,47,0.74) 100%)`. Text: h3 `#ffffff`, p `#f4f8f8`, links
`#ffd9a8` (light gold already used for links on dark hero backgrounds).
Photo still reads: the scrim lets 14-26% of the image show through.

Math (script `qa/contrast-kinds.py`, WCAG 2.x relative luminance,
ratio = (L1+0.05)/(L2+0.05); effective background = overlay alpha-blended
over the image pixel). Absolute worst case = overlay over a PURE WHITE
image pixel (brighter than any pixel in any master):

| text | top (a=0.86) eff bg rgb(41.7,68.4,76.1) | mid (a=0.78) eff bg rgb(61.6,85.7,92.8) | bottom (a=0.74) eff bg rgb(71.5,94.4,101.1) |
|---|---|---|---|
| h3 #ffffff | 10.30:1 | 7.83:1 | 6.83:1 |
| p #f4f8f8 | 9.63:1 | 7.32:1 | 6.38:1 |
| link #ffd9a8 | 7.72:1 | 5.87:1 | 5.12:1 |

All >= 4.5:1 at every point of the card. An earlier draft (bottom alpha
0.68) FAILED the link at 4.19:1 and was rejected; the bottom alpha was
raised to 0.74 to clear 4.5:1. Hover link #ffe9c9 is lighter than #ffd9a8,
so its ratio is higher than 5.12:1. Per-card measured worst case (brightest
pixel of each final master under the weakest, bottom, alpha) is in the
table below — worst link 5.12:1, best 5.98:1 (flood-storm).

## Reuse nets

1. **md5**: all 13 CLEAR vs (a) the coordinator's `qa/reuse-corpus/
   md5-list-task7.txt` (501 entries) and (b) my own fresh scan
   `qa/reuse-corpus-kinds/md5-list.txt` (7,579 files, 3,991 unique hashes).
   Note: the coordinator's list was snapshotted mid-re-encode and holds
   STALE intermediate md5s of my own files (e.g. kinds-slab-leak
   `00ed7d6b…` vs final `adb0d8a3…`, kinds-mobile-home `007a8718…` vs final
   `eaa68700…`) — those are my own earlier versions, not other sites'
   photos. My corpus was built fresh at install time (find + md5sum over
   site asset/export dirs across ~/workspace; screenshots, qa dirs,
   node_modules and my own kinds files excluded; script
   `qa/build-kinds-corpus2.py`, outputs `qa/reuse-corpus-kinds/
   md5-list.txt` + `ahash.json`).
2. **aHash 16x16 (PIL) vs `qa/reuse-corpus-kinds/ahash.json` (7,579
   entries)**: flag threshold Hamming < 25. Closest match per card is
   49-90 (see table) — NO flags, nothing even close, so no visual
   adjudication was triggered. A second targeted check vs 112 nearby-site
   images (this site's other photos, fort-myers-nextjs out, Cape Coral,
   Troy, Jeffersonville) also found nothing within Hamming 40.
3. **Pexels-ID**: no Pexels sources used; filenames contain no Pexels IDs
   (all files are `kinds-*.jpg`). Grep of the img dir for Pexels-like
   tokens only hits other workers' hero files, not kinds files.
4. **Visual (decides)**: all 13 raws viewed full-size; 4 riskiest finals
   (ceiling, condo, vacant, floors-cabinets) re-viewed as 760x864 crops.
   All 13 are self-made generations — none is a copy of any known site
   photo. No text/signage/logos/numbers legible in any image, no faces.
   One nit, recorded honestly: kinds-water-heater-leak.jpg has a tiny
   illegible label on a storage bin at the right edge (unreadable at card
   size, not legible text).

## Per-card table

Columns: # | card title (verbatim) | file | GPS | dims | weight | slot |
relevance verdict + reason | md5 | aHash closest (Hamming, 16x16, vs
7,579) | Pexels | visual | contrast (measured brightest pixel;
top h3/p/link, bottom h3/p/link — worst case over pure white in § above).

| # | Card title | File | GPS | Dims | Weight | Slot | Relevance | md5 | aHash closest | Pexels | Visual | Contrast top / bottom |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | AC leaking from the air handler or through the ceiling — link: AC leak water damage → /ac-leak/ | kinds-ac-leak.jpg | 26.6406,-81.8723 | 760x864 | 48,343 B (47.2 KB) | 381x432 / 350x466 | PASS — air handler cabinet, condensate drain line dripping, water-stained drywall, puddle on tile | c11028e9d16c30a92a51c54668aa93f9 | 60 (flooded-basement-cleanup-tulsa-standing-water.jpg) | none | viewed raw: PASS, no text/faces | 10.30 / 9.63 / 7.72 — 6.83 / 6.38 / 5.12 |
| 1 | Water dripping from the ceiling or a stain that keeps spreading — link: ceiling leak water damage → /ceiling-leak/ | kinds-ceiling-leak.jpg | 26.6406,-81.8723 | 760x864 | 65,480 B (63.9 KB) | 381x432 / 350x466 | PASS — spreading brown ceiling stain, drip falling, palm trees through window (bucket outside final crop; alt corrected) | ab7f4ccbe45a7d7843ac1c8419fc94f7 | 70 (hazmat-technician-protective-suit-oklahoma.jpg) | none | viewed raw + final: PASS, no text/faces | 10.31 / 9.63 / 7.73 — 6.83 / 6.39 / 5.12 |
| 2 | Water coming in from the condo above — link: condo water damage → /condo-leak/ | kinds-condo-leak.jpg | 26.6406,-81.8723 | 760x864 | 77,796 B (76.0 KB) | 381x432 / 350x466 | PASS — wet ceiling patch dripping, sliding glass doors, palm trees, Florida condo living room (towel/puddle outside final crop; alt corrected) | 9d9a6a27c4945e030869305449c91519 | 90 (cabinet-drying-photo-480.webp) | none | viewed raw + final: PASS, no text/faces | 10.31 / 9.64 / 7.73 — 6.84 / 6.39 / 5.13 |
| 3 | Sewage or a drain backing up — link: sewage backup cleanup → /sewage-cleanup/ | kinds-sewage-backup.jpg | 26.6406,-81.8723 | 760x864 | 73,869 B (72.1 KB) | 381x432 / 350x466 | PASS — murky water pooled around a floor drain, toilet + bathtub, palms outside window; darkest image, best for text | 93cae6e444543db248da37f3df146673 | 61 (coweta-ok-mission-bell-museum.jpg) | none | viewed raw: PASS, no text/faces | 10.81 / 10.10 / 8.10 — 7.48 / 6.99 / 5.61 |
| 4 | Sewer smell or slow drains in an older home — link: cast iron pipe water damage → /cast-iron-pipe/ | kinds-cast-iron-pipe.jpg | 26.6406,-81.8723 | 760x864 | 103,834 B (101.4 KB) | 381x432 / 350x466 | PASS — cracked rusted cast iron pipe dripping into a puddle under floor joists, work-light glow; heaviest file (rust texture) | a0b2e2bb5d9fe213a56c631c0a65d446 | 81 (wet-carpet-9462139.webp) | none | viewed raw: PASS, no text/faces | 10.31 / 9.64 / 7.73 — 6.84 / 6.39 / 5.13 |
| 5 | Burst pipe or split supply line — link: burst pipe water damage → /burst-pipe/ | kinds-burst-pipe.jpg | 26.6406,-81.8723 | 760x864 | 75,795 B (74.0 KB) | 381x432 / 350x466 | PASS — split braided supply line spraying under a bathroom sink, shut-off valve, towel, wet floor | 37adf5f96257a5ad2574347279f9b355 | 79 (hvac-ac-leak-water-damage-tulsa-condenser.jpg) | none | viewed raw: PASS, no text/faces | 10.30 / 9.63 / 7.72 — 6.83 / 6.38 / 5.12 |
| 6 | Water heater leaking in the garage or closet — link: water heater leak cleanup → /water-heater-leak/ | kinds-water-heater-leak.jpg | 26.6406,-81.8723 | 760x864 | 87,662 B (85.6 KB) | 381x432 / 350x466 | PASS — rusted tank base leaking across a garage floor, wet boxes, palms through the open garage door. NIT: tiny illegible label on a storage bin at right edge (unreadable at card size) | 523aed9530254b442befc06207300fee | 55 (chesterfield-commercial-water-damage-restoration-medical-office-containment.webp) | none | viewed raw: PASS, no faces; nit as noted | 10.30 / 9.63 / 7.72 — 6.83 / 6.38 / 5.12 |
| 7 | Dishwasher, washer, fridge or ice maker leak — link: appliance leak water damage → /appliance-leak/ | kinds-appliance-leak.jpg | 26.6406,-81.8723 | 760x864 | 54,560 B (53.3 KB) | 381x432 / 350x466 | PASS — dishwasher leaking across a wood kitchen floor, palms through the window | 564db87563d0ee5e68f77ae5764029db | 50 (blog-why-lancasters-desert-climate-doesnt-prevent-water-damage-sec1.webp) | none | viewed raw: PASS, no text/faces | 10.30 / 9.63 / 7.72 — 6.83 / 6.38 / 5.12 |
| 8 | Warm spots on the floor, wet baseboards or a jump in the water bill — link: slab leak water damage → /slab-leak/ | kinds-slab-leak.jpg | 26.6406,-81.8723 | 760x864 | 59,128 B (57.7 KB) | 381x432 / 350x466 | PASS — swollen baseboard pulling away from a damp tile floor, palms through the window; brightest image, overlay carries the contrast | adb0d8a3229c060c39d9dd8dc9d9c5ce | 67 (mcdonough-card-water-heater-leak-cleanup.jpg) | none | viewed raw: PASS, no text/faces | 10.30 / 9.63 / 7.72 — 6.83 / 6.38 / 5.12 |
| 9 | Came back to a wet or musty seasonal home — link: water damage in vacant homes → /vacant-home/ | kinds-vacant-home.jpg | 26.6406,-81.8723 | 760x864 | 69,584 B (68.0 KB) | 381x432 / 350x466 | PASS — sheet-covered furniture, musty water-stained ceiling corner, tile floor (wet floor patch outside final crop; alt corrected) | 1e1232859ca435412a675731418dfc08 | 80 (oklahoma-flood-insurance-guide-flooded-street.jpg) | none | viewed raw + final: PASS, no text/faces | 10.58 / 9.89 / 7.93 — 7.17 / 6.70 / 5.38 |
| 10 | Soft or wet floor in a mobile home — link: mobile home water damage → /mobile-home/ | kinds-mobile-home.jpg | 26.6406,-81.8723 | 760x864 | 80,549 B (78.7 KB) | 381x432 / 350x466 | PASS — panel walls, sagging vinyl flooring over wet particle board, water-stained wall base, palms outside; reads unmistakably as a manufactured home | eaa68700dac15c48ddb42936ed4985cf | 77 (boynton-beach-flooded-living-room-1200.jpg) | none | viewed raw: PASS, no text/faces | 10.30 / 9.63 / 7.72 — 6.83 / 6.38 / 5.12 |
| 11 | Floodwater or storm surge — link: flood and storm cleanup → /flood-cleanup/ | kinds-flood-storm.jpg | 26.6406,-81.8723 | 760x864 | 104,881 B (102.4 KB) | 381x432 / 350x466 | PASS — flooded Florida residential street, murky water around single-storey stucco homes, palms, storm sky; heaviest file (water detail) | 4aaa75b5e000ec0fb2e56985df372647 | 70 (south-salt-lake-ut-340.webp) | none | viewed raw: PASS, no text/faces | 11.18 / 10.45 / 8.38 — 7.97 / 7.45 / 5.98 |
| 12 | Wet floors or swollen kitchen cabinets — links: water damaged floors → /floors/ and water damaged kitchen cabinets → /cabinets/ | kinds-floors-cabinets.jpg | 26.6406,-81.8723 | 760x864 | 59,489 B (58.1 KB) | 381x432 / 350x466 | PASS — swollen peeling particle-board cabinet base, cupping laminate planks lifting, puddle, palms outside; both halves of the card's subject in one frame | 55d5eb0c4db48da3c512dbd0753d7fc3 | 49 (water-damage-restoration-antelope-acres-ca-sec1.webp) | none | viewed raw + final: PASS, no text/faces | 10.37 / 9.69 / 7.77 — 6.91 / 6.46 / 5.18 |

## Honestly-empty cards

None. All 13 cards have a fitted, relevant image.

## Deliverables

- Images (13): `site/assets/img/kinds-ac-leak.jpg`,
  `kinds-ceiling-leak.jpg`, `kinds-condo-leak.jpg`,
  `kinds-sewage-backup.jpg`, `kinds-cast-iron-pipe.jpg`,
  `kinds-burst-pipe.jpg`, `kinds-water-heater-leak.jpg`,
  `kinds-appliance-leak.jpg`, `kinds-slab-leak.jpg`,
  `kinds-vacant-home.jpg`, `kinds-mobile-home.jpg`,
  `kinds-flood-storm.jpg`, `kinds-floors-cabinets.jpg`
- `qa/manifest-kinds-F.php` — 13 entries in card order (`php -l` clean).
- `qa/css-snippet-kinds.css` — complete .kind-card background + scrim +
  text/link rules, mobile 390px (via the existing <=820px breakpoint) and
  print fallback. Braces balanced 23/23.
- `qa/patch-kinds-functions.txt` — OLD code verified verbatim in
  functions.php; NEW code reads the manifest by card index, adds
  `style="background-image:url(...)"` + `<div class="kind-scrim"
  aria-hidden="true"></div>` + `has-photo` class only when an image
  exists. Zero word/link changes.
- `qa/FINDINGS-kinds-cards.md` — this file.
- Working files kept for audit: `qa/kinds-raw/` (13 raw generations),
  `qa/process-kinds.py`, `qa/contrast-kinds.py`,
  `qa/build-kinds-corpus.py` (v1, superseded — slow os.walk, killed),
  `qa/build-kinds-corpus2.py`, `qa/reuse-corpus-kinds/md5-list.txt` +
  `ahash.json` (7,579 entries each).

## Open items for the coordinator

1. Apply patch + CSS + manifest copy (`qa/manifest-kinds-F.php` →
   `site/data/manifest-kinds.php`), re-export, screenshot homepage at
   1440px and 390px, and confirm the computed contrast on the real render.
2. Weights: 9 of 13 files are over the 60 KB aim (total ~938 KB for the
   grid). Accept, or ask for a 1x (381x432) variant set — do not just
   crush quality below q50.
3. kinds-water-heater-leak.jpg has one tiny illegible label on a storage
   bin (right edge). If the user objects to any text-like mark, that one
   image needs a regenerate.
