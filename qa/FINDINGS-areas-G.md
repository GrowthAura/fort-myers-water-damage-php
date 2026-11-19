# FINDINGS — Task 7: Area Paragraphs Get Images (areas-G)

Date: 2026-11-19. Worker: area-section worker (Task 7). Status: COMPLETE — 6/6 areas filled, 0 omitted, 0 word changes.

## 1. Which page / section

**Target: `/areas/` — `site/data/areas.php`, the section under the H3
"Lee County Service Areas and ZIP Codes".**

- The "ZIP-code line" is the table directly above the six paragraphs
  (`Area | ZIP codes | Most common water damage`, 9 rows). It is NOT touched.
- The six image cards cover, in order: Cape Coral, Lehigh Acres,
  North Fort Myers, Fort Myers Beach, Estero, Bonita Springs. Each is an
  H3 + paragraph pair in the data file today, each with its own guide link.
- NOT in this task and NOT touched: Fort Myers, Sanibel and Captiva,
  Pine Island and Matlacha, San Carlos Park / Gateway / Iona (H3 + paragraph
  pairs with no image in this task). They stay as prose around the grids.

**Why `/areas/` and not the homepage section:** the homepage H2 "Water
Damage Help Across Lee County" has the same six areas, but Estero and
Bonita Springs SHARE one paragraph ("Estero and Bonita Springs: condo
leaks … See Estero and Bonita Springs."), so a 6-card split there would
require word changes or duplicated text. `/areas/` is the only place with
six distinct area paragraphs (1:1 with the six image slugs), each with its
own guide link. The same six manifest entries + CSS can dress the homepage
section later once the owner decides how to split that shared paragraph —
see the note at the end of `qa/patch-areas-functions.txt`.

## 2. Card layout + slot sizes

Mirrors the "What we help with" treatment exactly: `.kinds-grid` /
`.kind-card` (white card, 1px `--line` border, 5px coral top border,
12px radius, `0 4px 16px rgba(10,46,56,.06)` shadow, 28px padding,
23px H3). New classes `.area-grid` / `.area-card` / `.area-card-img`
(see `qa/css-snippet-areas.css`): the photo is a full-bleed header at the
top of the card (under the coral strip), H3 + paragraph below it.
Grid: 3 columns desktop, 2 columns ≤1020px, **1 column ≤620px (390px
holds)** — same breakpoints as `.kinds-grid`. `aspect-ratio: 3/2` +
`object-fit: cover` on the image, so the box is exact at every width
(no layout shift).

Slot math (container max 1240px, padding 24px → content 1192px; gap 24px):

| Viewport | Columns | Image slot (3:2) |
|---|---|---|
| Desktop ≥1021px | 3 | 381 × 254 |
| ≤1020px (2-col) | 2 | **474 × 316 — largest slot, file size** |
| 390px mobile | 1 | 350 × 233 |

**Files are served at exactly the largest slot: 474 × 316.** The browser
downscales at desktop/mobile. All six are JPEG q78, 28–40 KB (< 50 KB).

## 3. Image table

Raws (1920×1280 webp, media-generation sidecars) live in
`qa/gen-raw-areas/`. Finals are center-crops to 3:2 + Lanczos resize to
474×316. GPS: city-centre coordinates from the task brief; Cape Coral
(26.56285, −81.94953) and Bonita Springs (26.33981, −81.77870) confirmed
against a web search (GeoNames); the other four are the standard
city-centre values and were not disputed by any source checked.

| Area | File | GPS (EXIF) | Dims | Weight | Relevance verdict |
|---|---|---|---|---|---|
| Cape Coral | `site/assets/img/area-cape-coral.jpg` | 26.5629, −81.9495 | 474×316 | 28.4 KB | PASS — canal-front slab homes with screened lanais, docks, small boat, palms; exactly the canal-front flooding paragraph. No legible text/signage/faces (one boat-hull marking is illegible even at full size, invisible at card size). |
| Lehigh Acres | `site/assets/img/area-lehigh-acres.jpg` | 26.6126, −81.6367 | 474×316 | 35.4 KB | PASS — concrete-block homes on flat grassy lots along a wide quiet street, palms + live oaks with Spanish moss, big sky; inland Florida residential, matches the flat-lot / well-and-septic paragraph. No text/signage/faces. |
| North Fort Myers | `site/assets/img/area-north-fort-myers.jpg` | 26.6883, −81.8808 | 474×316 | 28.3 KB | PASS — riverfront manufactured homes and houses on a wide river (Caloosahatchee), palms, green bank; matches "manufactured-home communities and riverfront homes". No text/signage/faces. |
| Fort Myers Beach | `site/assets/img/area-fort-myers-beach.jpg` | 26.4442, −81.9557 | 474×316 | 34.9 KB | PASS — white-sand Gulf beach, sea-oats dunes, turquoise water, elevated beach houses + low-rise condos; matches the storm-surge / beach paragraph. No text/signage/faces. |
| Estero | `site/assets/img/area-estero.jpg` | 26.4327, −81.8068 | 474×316 | 39.6 KB | PASS — gated condo / coach-home community with tile roofs around a lake, walkway, manicured landscaping, palms; matches "gated communities, condos, coach homes". No text/signage/faces. |
| Bonita Springs | `site/assets/img/area-bonita-springs.jpg` | 26.3398, −81.7787 | 474×316 | 29.7 KB | PASS — condos + homes along a calm river waterway (Imperial River) with docks, palms, mangroves; matches the river / condo paragraph. No text/signage/faces. |

No area was omitted: all six could be filled honestly.

## 4. EXIF / metadata verification

Process per file: PIL resize → `exiftool -all=` (strip EVERYTHING) →
write GPS EXIF only. Verified with `exiftool -a -G1` on all six finals:

- ONLY GPS tags present in EXIF: `GPSVersionID`, `GPSLatitudeRef`,
  `GPSLatitude`, `GPSLongitudeRef`, `GPSLongitude` — values match the
  table above (e.g. Cape Coral 26°33'46.44" N, 81°56'58.20" W).
- **0 AI markers**: no XMP, no IPTC, no `Software`, no `Creator`,
  no `Description`, no `Make`/`Model`/`DateTime` — explicit
  `exiftool -XMP:All / -IPTC:All / -Software` reads return empty.
- The remaining `[IFD0]` lines (`XResolution/YResolution 72`,
  `ResolutionUnit`, `YCbCrPositioning`) and `[File]`/`[System]` lines are
  baseline JPEG structural fields written by the encoder, not metadata
  content.

## 5. Reuse nets (hashes support only — visual comparison decides)

Coordinator's `qa/reuse-corpus/md5-list.txt` was not ready, so a fresh
scan was run over the whole project tree instead (script `/tmp/reuse_areas.py`;
outputs `qa/reuse-corpus/md5-list-task7.txt` — 501 files — and
`qa/reuse-corpus/ahash-task7.json`). Corpus: every image under
`site/assets/img/`, `qa/gen-raw/`, `qa/kinds-raw/`,
`qa/gen-raw-areas/`, `qa/screenshots/`.

| Area | md5 (final) | md5 dupes | Closest aHash 16×16 Hamming (excl. own raw) | vs own hero Hamming |
|---|---|---|---|---|
| cape-coral | `94cad0f587b892076f8e3e574b70ce43` | none | 43 (screenshot `05-footer-location-desktop.png`) | 101 |
| lehigh-acres | `de426770e00c04adc9aa874820a4db74` | none | 42 (`kinds-flood-storm` raw) | 114 |
| north-fort-myers | `6e617b7cb5bb1ec9a29e8e371d2d4d6c` | none | 49 (`hero-areas-960w.jpg`) | 106 |
| fort-myers-beach | `722333de8c3f58e466882669feb78292` | none | 42 (screenshot `disclaimer-desktop.png`) | 130 |
| estero | `e03677eb470dca8cc4ad7fc57ac114f6` | none | 61 (screenshot `05-footer-location-desktop.png`) | 102 |
| bonita-springs | `863064561fbca2b315455e68f7568801` | none | 38 (screenshot `05-footer-location-desktop.png`) | 102 |

- **md5: 0 duplicates** for all six.
- **aHash: 0 flags.** Flag threshold is Hamming < 25; the closest
  non-self match anywhere in the 501-file corpus is 38. (Hamming 0 is each
  file's own raw webp source — same pixels, expected.)
- **Pexels-ID: none.** No Pexels ID in any final filename; `grep -ri
  pexels` over the six generation sidecar JSONs in `qa/gen-raw-areas/`
  returns 0 hits (images are generated, not stock).
- **Visual (decides):** all six raws AND all six finals viewed full-size
  by this worker. Each is a different photo from its area-page hero:
  hero-vs-card compositions differ in every case (e.g. Cape Coral hero
  is a canal shot from a bridge; the card is a wide canal-front row;
  Estero hero is a condo courtyard with fountain; the card is a lake +
  coach homes). aHash vs own hero is 101–130/256 — essentially unrelated.
  No card image copies any known site photo.

## 6. Before / after link inventory (0 word changes)

The six paragraphs contain 7 links; the patch moves their segments
verbatim into the new `area-cards` blocks (segments emitted from the
parsed data file, not retyped — the builder asserted all 20 text segments
and all 7 hrefs byte-identical between old and new code).

| # | Anchor (verbatim) | href | Card |
|---|---|---|---|
| 1 | water damage restoration in Cape Coral | `/cape-coral/` | Cape Coral |
| 2 | water damage help in Lehigh Acres | `/lehigh-acres/` | Lehigh Acres |
| 3 | water damage restoration in North Fort Myers | `/north-fort-myers/` | North Fort Myers |
| 4 | mobile home water damage | `/mobile-home/` | North Fort Myers |
| 5 | water damage help on Fort Myers Beach | `/fort-myers-beach/` | Fort Myers Beach |
| 6 | water damage restoration in Estero | `/estero/` | Estero |
| 7 | water damage restoration in Bonita Springs | `/bonita-springs/` | Bonita Springs |

All 7 survive exactly (same anchor, same href, same card, same paragraph
words). The ZIP table above the cards (incl. each area's ZIP-code line)
and the surrounding Fort Myers / Sanibel / Pine Island / San Carlos
sections are untouched. Heading level is preserved (H3 inside each card).

## 7. Deliverables

- Images (6): `site/assets/img/area-cape-coral.jpg`,
  `area-lehigh-acres.jpg`, `area-north-fort-myers.jpg`,
  `area-fort-myers-beach.jpg`, `area-estero.jpg`, `area-bonita-springs.jpg`
- `qa/manifest-areas-G.php` — 6 entries, exact requested shape
  (`['areas' => [slug => [src, alt, width, height]]]`); `php -l` clean.
- `qa/css-snippet-areas.css` — `.area-grid` / `.area-card` /
  `.area-card-img` + responsive rules (after base rules, kinds-grid
  breakpoints).
- `qa/patch-areas-functions.txt` — verbatim old data blocks
  (areas.php lines 323–404 and 443–482) + verbatim `kinds` anchor +
  paste-ready new `area-cards` blocks (grid 1 = 4 cards, grid 2 = 2 cards)
  and the new `render_block` case. New blocks + render case pass
  `php -l`; parsed check: grid 1 = 4 items, grid 2 = 2 items, slugs in
  order.
- `qa/reuse-corpus/md5-list-task7.txt` + `qa/reuse-corpus/ahash-task7.json`
  — fresh 501-file corpus (coordinator's `md5-list.txt` was not ready).
- Raws + sidecars: `qa/gen-raw-areas/` (6 webp + 6 json).

## 8. Files NOT touched (per task)

No edits to `styles.css`, `functions.php`, any data file,
`media-manifest.php`, `header.php`. No commit, no push.

## 9. For the coordinator (apply + verify)

1. Merge `qa/manifest-areas-G.php` into `$MEDIA['areas']` in
   `site/data/media-manifest.php`.
2. Apply `qa/patch-areas-functions.txt` (data grids + render case),
   append `qa/css-snippet-areas.css` to `styles.css` (responsive rules
   after base rules; optionally merge the `.area-grid`
   content-visibility selector into the existing rule).
3. `php -l` both edited files; render `/areas/` and check: 6 cards with
   the 6 images, all 7 links from §6 present with identical anchor/href,
   0 word changes (diff the six paragraphs' plain text before/after),
   overflow 0 at 390 / 768 / 1240px, screenshots desktop + mobile.
4. Open: homepage section left as-is (see §1) — needs an owner decision
   on splitting the shared Estero/Bonita paragraph before the same
   treatment can apply there.
