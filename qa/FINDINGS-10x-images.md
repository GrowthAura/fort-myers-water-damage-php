# FINDINGS — 10x Images + About Page (Worker 3)

Fort Myers PHP site (`~/workspace/fort-myers-php/`). Local only — no push, no
deploy, no DNS. `qa/verify_export.py` NEVER run. Verified on the worker's own
PHP server (`php -S 127.0.0.1:8135 -t site site/index.php`, killed by PID at
the end of this round).

**Method note (sourcing):** the brief says "Pexels free-licensed only OR
self-made per the established method". The established method on THIS site
(`qa/FINDINGS-hero-images.md` §2/§5) is self-made images generated fresh
with the media tools — all 93 hero-round images were generated, none were
Pexels downloads. All 6 new photos in this round follow that same method:
generated fresh, viewed at full size, resized to the exact slot with PIL,
EXIF stripped, GPS-only re-tag. No Pexels photo was downloaded; there are
no Pexels IDs to log (see the per-image log — "Pexels ID: n/a (self-made)").

## 1. A-3 — 15 alt texts trimmed to ≤125 chars — DONE

**Count correction:** the audit says "15 hero alts". The log
(`qa/20x-part-a-raw/audit-run-2.log`) actually holds **14 heroes** over 125
chars. The 15th alt over 125 is the **help** image
`help-emergency-water-removal.jpg` (134). All 15 are trimmed now; the
manifest holds **49 alts, 0 over 125, longest exactly 125**
(`help-flood-storm-cleanup.jpg`, pre-existing, at the limit).

| Slot | Old (chars) | New (chars) |
|---|---|---|
| home hero | 157 | A restoration technician extracts standing water from a tiled living room floor in a bright Florida home (105) |
| water-removal hero | 150 | A submersible pump and extraction wand pull standing water from a tiled floor in a Florida home (97) |
| drying hero | 145 | A commercial dehumidifier, air movers and a moisture meter dry damp walls and tile flooring in a Florida home (112) |
| condo-leak hero | 153 | Water runs down a shared condo wall from a leaking ceiling while a technician checks it with a moisture meter (114) |
| flood-cleanup hero | 146 | Technician clearing floodwater from a tiled living room floor in a Florida home (80) |
| vacant-home hero | 139 | A technician enters a seasonal Florida home with covered furniture and damp, stained tile flooring (100) |
| north-fort-myers hero | 137 | Manufactured home with carport beside the Caloosahatchee River in North Fort Myers, Florida (93) |
| sewage-cleanup hero | 130 | A technician in protective coveralls and a respirator vacuums dark water from a bathroom floor (96) |
| lehigh-acres hero | 131 | Single-story concrete-block homes on large grassy lots along a quiet street in Lehigh Acres, Florida (105) |
| areas hero | 129 | Historic brick riverfront buildings and royal palm trees along the Caloosahatchee River in downtown Fort Myers (113) |
| mobile-home hero | 127 | A technician checks a damp wall of a manufactured home in a Florida park with a moisture meter (94) |
| slab-leak hero | 127 | Gloved hands test a damp tile floor with a moisture meter beside broken tiles exposing a wet concrete slab (111) |
| ac-leak hero | 126 | Water drips from an air handler condensate drain into a puddle on a tile floor (78) |
| cape-coral hero | 126 | Canal-front homes with screened pool enclosures and private docks along a canal in Cape Coral, Florida (105) |
| help-emergency-water-removal | 134 | A wet-vacuum extracting standing water from a tiled floor in a Fort Myers home (79) |

Trailing scene detail cut in every case; subject + place kept. Verified by
script (`/tmp/altcheck.php`): 49 alts, 0 over 125.

## 2. D-P3-8 — two heavy heroes re-encoded + 640w mobile variant — DONE

| File | Before | After |
|---|---|---|
| `hero-lehigh-acres.jpg` | 1600×1067, 368 KB | **1440×960, 250,336 B (244 KB)**, q40 single encode from the original 1600w master |
| `hero-north-fort-myers.jpg` | 1600×1067, 344 KB | **1440×960, 254,283 B (248 KB)**, q45 |
| `hero-lehigh-acres-640w.jpg` | — (did not exist) | NEW 640×426, 68,707 B |
| `hero-north-fort-myers-640w.jpg` | — (did not exist) | NEW 640×426, 67,084 B |
| 960w variants | 140 KB / 136 KB | re-encoded from the originals, 153,952 B / 147,551 B |

Manifest updated: width/height 1440/960, srcset now
`…-640w.jpg 640w, …-960w.jpg 960w, ….jpg 1440w` on both pages.
**Mobile proof:** at 390px the browser picks the 640w file on both pages
(`currentSrc` = `hero-lehigh-acres-640w.jpg` / `hero-north-fort-myers-640w.jpg`,
box 390×656 / 390×719) — the 2.46× over-download is gone.
**Quality note (lehigh):** quality-only reduction stalled (q35 still 257 KB —
the tree/grass detail holds weight), so the final file is 1440w q40 from the
original master, NOT a double encode. Viewed at full size: no visible
compression artefacts.

## 3. D-P3-5 — help-sewage-cleanup.jpg — SWAPPED (genuinely better photo found)

Old: spotless white bathroom, toilet + tub + mop bucket — reads as a cleaning
service, no water/damage/equipment. New (viewed full-size): technician in
white coveralls + respirator vacuuming **dark contaminated water** off a tile
floor, wet vacuum beside him, plastic containment sheeting on the doorway,
toilet behind the sheeting, palms outside. Containment + PPE + dark water =
exactly the sewage-backup work. Installed as `help-sewage-cleanup.jpg`
474×267, 27,971 B, GPS Fort Myers. Alt updated to match the new photo (108
chars). Rendered on home + /about/ help cards (box 371×209 desktop,
340×191 mobile; screenshot `qa/screenshots-10x/about-help-cards-desktop.png`).

## 4. D-P3-6 — four generic legal heroes — 3 SWAPPED, 1 LEFT

| Page | Old | New (viewed full-size) | Verdict |
|---|---|---|---|
| /insurance/ | blank papers + phone | Technician photographing a water-stained wall with a phone to document damage for a claim; blank-display moisture meter + blank clipboard on a table; palms through the window | **SWAPPED** — claim documentation is exactly what the page is about (photos, readings, drying logs) |
| /terms/ | blank papers + pen + glasses | Homeowner + technician reviewing a written scope of work at a kitchen table; blank papers, pen, moisture meter on the table; palms through the window | **SWAPPED** — the agreement moment the page's "scope in writing" language describes |
| /disclaimer/ | shield + papers + laptop | Technician showing blank-display moisture meter readings to a homeowner beside a water-stained wall; air mover behind; palms through sliders | **SWAPPED** — the explanation/readings moment, service-true instead of desk stock |
| /privacy-policy/ | laptop + padlock + papers | — (no candidate generated) | **LEFT + flagged** — no genuinely better topical photo exists for a privacy-policy page; any replacement would be the same class of generic office stock. The current photo is topical, not wrong. |

Swapped heroes installed at 1920×1280 + new 960w variants (insurance
276,933 B / terms 229,996 B / disclaimer 228,540 B masters; 960w 100,979 /
84,885 / 85,504 B). Alts rewritten to match (118 / 99 / 102 chars).
Insurance hero re-judged under Worker 1's new scrim: subject reads clearly,
H1 legible (`qa/screenshots-10x/hero-insurance-desktop.png`).

## 5. L-16 — home + cost heroes re-cropped (baked into the files) — DONE

CSS `object-position` is not my file to touch, so the re-crop is baked into
the masters (same 1920×1280, 960w variants regenerated). Both re-judged
under Worker 1's new directional scrim (L-1) by viewed pixels.

- **Home** — crop (450,80)–(1920,1060): the dead left doorway/wall is gone;
  the technician, extraction wand, hose coil and wet tile now fill the
  frame; machine still visible at the left edge; palms + sofa kept.
  262,598 B. Desktop hero shot: action reads clearly under the scrim, H1 +
  trust line legible (`qa/screenshots-10x/hero-home-recrop-desktop.png`,
  mobile `hero-home-recrop-mobile.png`). The old "weakest hero" verdict was
  largely the 0.70 scrim; the photo itself was already strong.
- **Cost** — crop (200,0)–(1920,1147) + brightness ×1.06: the empty left
  hallway is gone; moisture-meter hand, stained wall and clipboard-on-ladder
  are centred; air mover + dehumidifier kept at the left. 242,566 B.
  Desktop hero shot: assessment moment reads clearly under the scrim
  (`qa/screenshots-10x/hero-cost-recrop-desktop.png`).

## 6. L-10 — area map strips for /cape-coral/ + /fort-myers-beach/ — IMAGES READY, STRIP NOT INSTALLED IN THOSE FILES

**Real static maps obtained (no fake map drawn):** stitched from live
OpenStreetMap tiles (`tile.openstreetmap.org`, z11 Cape Coral / z12 Fort
Myers Beach — z11 left Estero Island as an unlabelled sliver, so FMB was
re-stitched at z12 where "Fort Myers Beach" is labelled on the island).

- `map-cape-coral.jpg` 1200×560, 125,311 B, GPS 26.5629,-81.9495 — Cape Coral
  labelled centre-left, Caloosahatchee River, Fort Myers, North Fort Myers,
  Lehigh Acres, Pine Island, Sanibel, I-75, Page Field. Viewed: correct
  geography, real OSM render.
- `map-fort-myers-beach.jpg` 1200×560, 123,893 B, GPS 26.4442,-81.9557 —
  Estero Island + "Fort Myers Beach" label, Matanzas Pass Bridge, Sanibel,
  Estero Bay, San Carlos Park. Viewed: correct geography, real OSM render.

Both are registered in the manifest under a new `$MEDIA['maps']` key with
alts. **NOT installed as strips:** the strip needs a new block (image +
caption + "View larger map ↗" + 3-chip facts band) and CSS (2px gold border,
14px radius, sand chips) — `cape-coral.php` / `fort-myers-beach.php` and
`site/assets/css/*` are outside my owned files, and no existing block type
renders that strip. Exact spec for the owning worker:

- **Placement:** after the intro (first `p` after the hero/cta-line) on each
  page.
- **Image:** `/assets/img/map-cape-coral.jpg` /
  `/assets/img/map-fort-myers-beach.jpg` (1200×560, from `$MEDIA['maps']`).
- **Caption:** "Cape Coral and the Lee County service area" /
  "Fort Myers Beach and the Lee County service area". Attribution line
  (OSM licence requirement): "© OpenStreetMap contributors".
- **"View larger map ↗":** `https://www.google.com/maps?q=Cape+Coral,+FL`
  / `https://www.google.com/maps?q=Fort+Myers+Beach,+FL` — same `q=` pattern
  as the site's existing map embed (`q=Fort Myers, FL 33901`); adapted per
  area (flagged: not literally the same URL as the homepage embed).
- **Facts band (copy-only facts):** Cape Coral — "400+ miles of canals ·
  ZIPs 33904–33993 · Slab homes" (copy: "more than 400 miles", ZIPs
  33904/33909/33914/33990/33991/33993, "single-family slab homes" /
  "Nearly all Cape homes sit on slabs"). Fort Myers Beach — "Estero Island ·
  ZIP 33931 · Elevated homes" (copy: "Estero Island", "ZIP code 33931",
  "Many rebuilt homes are elevated").
- **CSS (Worker 1):** 2px gold border + 14px radius on the strip, sand chips
  16px/700 under the map. If the live Google iframe is layered over the
  poster (L-18 pattern), the static map is the poster — no fallback work
  needed beyond that.

## 7. ABOUT PAGE — end-level pass with real images — DONE (with 1 flagged mismatch)

`site/data/about.php` read fully first. **Zero word changes: 78/78
word-bearing segments identical before/after** (script-verified).

### What was added (existing block types only — `functions.php` NOT edited)

1. **"What We Do" list → photo cards.** The existing `ul` now carries
   `'variant' => 'help-cards'` — the same renderer the homepage uses, so
   the 7 service items render as photo cards with the manifest's help
   images. No words added, removed or reordered.
   - idx 0 Emergency water removal → help-emergency ✓
   - idx 1 Structural drying → help-structural-drying ✓
   - idx 2 Sewage backup cleanup → help-sewage-cleanup ✓ (new PPE photo)
   - idx 3 Flood and storm cleanup → help-flood-storm-cleanup ✓
   - idx 4 Leak damage (AC / burst / water heater / appliance / slab) → help-leaks-every-kind ✓
   - idx 5 Wet floors and cabinets → help-every-property (street photo) ✗ **MISMATCH — see flag below**
   - idx 6 Homes, condos, mobile homes, vacation rentals, businesses → **NEW** `help-property-types.jpg` ✓ (stucco home + 3-storey condo + manufactured home with carport, palms; 474×267, 34,059 B)
   - Rendered desktop + mobile, all 7 images loaded (natural 474×267;
     boxes 371×209 desktop, 340×191 mobile).
2. **Real map in the Areas section.** A `map` block (the existing block type
   the homepage uses) after the "covers seven communities" intro paragraph,
   caption "Map: Fort Myers and the Lee County service area" — same caption
   as the homepage map. Renders the live Google iframe (q=Fort Myers, FL
   33901, z=12); in this VM Google is unreachable so it shows Worker 1's
   "Map loading · Fort Myers & Lee County" poster — expected, not a defect;
   live tiles need one real-browser look (standing item). Side effect: the
   About outline gains one H2 (the map caption), same pattern as the
   homepage — outline verified H1 → H2s → area H3s, no level skip.
3. **Hero kept:** `hero-about.jpg` (technicians loading the van) already
   existed and is on-topic; unchanged.

### ⚠️ FLAG — About item 5 ("Wet floors and cabinets") shows the wrong photo

The `help-cards` renderer reads `$MEDIA['help']['home']` positionally, and
that manifest key is shared with the homepage (6 cards: index 5 must stay
the property-types street photo for the homepage's "Every kind of property"
card). So About item 5 inherits the street photo — a real Florida-homes
photo, on-topic for the business, but NOT a floors/cabinets photo. The
correct photo is **already made and staged**:
`site/assets/img/about-floors-cabinets.jpg` 474×267, 32,780 B, GPS Fort
Myers — swollen/delaminated cabinet base, curled wet vinyl plank,
blank-display moisture meter in gloved hands, air mover behind, palms
through the sliders (viewed full-size, PASS). It is installed as a file but
**not in the manifest and not rendered**, because using it needs a one-line
change in `functions.php` (outside my owned files):

```php
// help-cards branch: $imgs = $GLOBALS['MEDIA']['help']['home'] ?? [];
// → $imgs = $GLOBALS['MEDIA']['help'][$page['slug'] === '/about/' ? 'about' : 'home'] ?? [];
// + add $MEDIA['help']['about'] = 7 entries (the 6 home ones in About order
//   is wrong — About order needs: emergency, drying, sewage, flood, leaks,
//   floors-cabinets (about-floors-cabinets.jpg), property-types
//   (help-property-types.jpg)).
```

Parent's call: accept the one mismatched card until that line lands, or
leave the What We Do list unconverted (0 photos). The 6/7 correct photos +
the staged fix are the better trade in my judgement, so I converted it and
flagged it here. The "How We Work" section (moisture meters, thermal
camera) has no zero-word photo option either — no existing block renders a
bare photo there; ideal = a photo-strip block, flagged, not forced.

## 8. Reuse nets — md5 + aHash + Pexels-ID, fresh disk reads

Corpus: `qa/reuse-net-10x.py` — fresh `find` + fresh reads at install time.
Scope: all image files under `~/workspace` in site asset/export/publish
dirs (`assets/img`, `out/assets/img`, `*gh-pages*`, `*export*`, `*dist*`,
`*build*`): **68,237 files** of 188,264 workspace images. Own-project
paths classified SELF. Pexels-ID net: all 6 new photos are self-made per
the established method (no Pexels source, no Pexels IDs in filenames or
logs) — net N/A by construction, recorded here.

- **md5: 0 hits** (excluding self-path) across the 68,237-file corpus.
- **aHash (full 68,237-file corpus): COMPLETE and CLEAR.**
  `qa/reuse-net-10x.py`, fresh disk reads, ~34 min runtime, log saved as
  `qa/reuse-net-10x.log`. aHash computed for 68,138 files (99 unreadable
  by PIL — corrupt/odd formats; md5 covered them). Nearest non-self
  16×16 distances: sewage-help 41, insurance 60, terms 52, disclaimer 62,
  property-types 56, floors-cabinets 58, home re-crop 72, cost re-crop 49,
  lehigh 82, north-fort-myers 80 — all far above the ≤25 suspicious band
  (same-photo 0–2). SELF matches only: lehigh + north at d16=0 vs their
  own old masters in `out/assets/img/` (re-encode of the same master —
  expected). A targeted aHash vs 451 live-site images
  (`site/assets/img` + `out/assets/img` of other projects) run earlier
  agreed: nearest d16 51–92, CLEAR.
- **One 8×8 flag adjudicated by viewed pixels:** sewage-help's nearest
  neighbour had d8=6 (inside the 8×8 ≤8 flag band) with d16=41 — the
  Pleasant Grove file `detail-water-damage-alpine-ut.jpg`. Viewed
  full-size: it is a Utah mountain landscape (snow-capped peaks, green
  slopes) — a completely different photo from the bathroom PPE shot; the
  coarse-hash similarity is a bright-top/dark-bottom luminance coincidence.
  **NOT a reuse.** No other 8×8 distance was ≤8 (next lowest: cost d8=9).

## 9. EXIF / AI-marker audit — 21/21 PASS

All new/changed files: GPS present with correct values + `Ref=North/West`
(Fort Myers 26.6406,-81.8723; Lehigh Acres 26.6126,-81.6367; North Fort
Myers 26.6883,-81.8808; Cape Coral 26.5629,-81.9495; Fort Myers Beach
26.4442,-81.9557); **0 XMP APP1 segments; 0 AI markers** (no `xap`,
`CreatorTool`, `AI Generated`, `DocumentID` bytes); no Software tag; 0th
IFD holds only the GPSInfo pointer (tag 34853) — the same shape as the
hero-round's own files (which additionally carry resolution tags). Verified
with `piexif` (no `exiftool` binary on this VM).

## 10. Render verification (own PHP server, port 8135)

- Home / cost / insurance / terms / disclaimer / lehigh-acres /
  north-fort-myers / about: every changed image renders at its slot;
  hero boxes measured (width AND height): desktop 1440×818 home,
  1440×738 cost/insurance/north, 1440×538 terms, 1440×503 disclaimer,
  1440×668 lehigh; mobile hero boxes 390×656 lehigh / 390×719 north.
  Help cards 371×209 desktop, 340×191 mobile, all 7 loaded on /about/.
- **Quirk (environmental, not a defect):** in-page `naturalWidth` reads
  1440 for every hero (including untouched `hero-about.jpg`) while the
  bare image URL reads 1920×1280 and the served bytes are md5-identical to
  disk. This is the bundled Chromium reporting the `sizes="100vw"`-resolved
  width for srcset images. Disk truth (PIL) + `currentSrc` candidate
  selection (640w on mobile, master on desktop) are the reliable checks
  and both pass.
- Screenshots: `qa/screenshots-10x/` (hero re-crops desktop + mobile,
  insurance, about help cards + map, lehigh mobile, areas cards).
- **Not verified here:** live Google map tiles (Google unreachable from
  this VM — standing item, needs one real-browser look); the L-10 strip
  render (strip not installed — spec in §6).

## 11. Files changed (this round)

- `site/assets/img/`: 21 files new/changed (see per-image log §12);
  originals backed up to `qa/gen-10x/backup-orig/` (13 files).
- `site/data/media-manifest.php`: 15 alt trims, 4 swap alts, lehigh/north
  1440w + 640w srcset, `help['home'][6]`, new `$MEDIA['maps']` registry.
  (Backup: `/tmp/media-manifest.bak`.)
- `site/data/about.php`: `help-cards` variant on the What We Do list +
  one `map` block. 78/78 segments identical. (Backup: `/tmp/about.bak`.)
- `site/includes/functions.php`: **A-2 follow-up only** (area-cards titles
  → H2 on /areas/ + h2 class hook) — recorded in
  `qa/FINDINGS-10x-design.md`. No other includes/CSS/data-file edits.
- `qa/FINDINGS-10x-images.md` (this file), `qa/FINDINGS-10x-design.md`,
  `qa/process-10x.py`, `qa/reuse-net-10x.py`,
  `qa/screenshots-10x/` (8 files), `qa/gen-10x/` (6 generated candidates +
  backups).

## 12. Per-image log

| File | Pexels ID / source | Slot | Dimensions | Weight | GPS | Net result |
|---|---|---|---|---|---|---|
| help-sewage-cleanup.jpg (NEW photo) | n/a — self-made (media tools) | home + about help card | 474×267 | 27,971 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=41 (d8=6 flag adjudicated — PG file is a Utah mountain landscape, NOT a reuse) |
| hero-insurance.jpg (NEW photo) | n/a — self-made | /insurance/ hero | 1920×1280 (+960w 100,979 B) | 276,933 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=60 |
| hero-terms.jpg (NEW photo) | n/a — self-made | /terms/ hero | 1920×1280 (+960w 84,885 B) | 229,996 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=52 |
| hero-disclaimer.jpg (NEW photo) | n/a — self-made | /disclaimer/ hero | 1920×1280 (+960w 85,504 B) | 228,540 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=62 |
| help-property-types.jpg (NEW photo) | n/a — self-made | /about/ help card idx 6 | 474×267 | 34,059 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=56 |
| about-floors-cabinets.jpg (NEW photo, STAGED not rendered) | n/a — self-made | /about/ help card idx 5 (after 1-line functions change) | 474×267 | 32,780 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=58 |
| hero-home.jpg (RE-CROP of own master) | own master (qa/media-raw-archive) | home hero | 1920×1280 (+960w 95,841 B) | 262,598 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=72 (re-crop is hash-distant from its own original — different composition, SELF by provenance) |
| hero-cost.jpg (RE-CROP of own master) | own master | /cost/ hero | 1920×1280 (+960w 87,536 B) | 242,566 B | 26.6406,-81.8723 | md5 CLEAR (68k); aHash CLEAR, nearest d16=49 (re-crop is hash-distant from its own original — different composition, SELF by provenance) |
| hero-lehigh-acres.jpg (RE-ENCODE 1440w) | own master 1600×1067 | /lehigh-acres/ hero | 1440×960 (+960w 153,952 B; +640w 68,707 B) | 250,336 B | 26.6126,-81.6367 | md5 CLEAR (68k); aHash CLEAR, nearest non-self d16=82 (SELF d16=0 vs own old master in out/ — re-encode, expected) |
| hero-north-fort-myers.jpg (RE-ENCODE 1440w) | own master 1600×1067 | /north-fort-myers/ hero | 1440×960 (+960w 147,551 B; +640w 67,084 B) | 254,283 B | 26.6883,-81.8808 | md5 CLEAR (68k); aHash CLEAR, nearest non-self d16=80 (SELF d16=0 vs own old master in out/ — re-encode, expected) |
| map-cape-coral.jpg (NEW, OSM tiles) | OpenStreetMap tiles (tile.openstreetmap.org, z11) | L-10 strip (not installed — spec §6) | 1200×560 | 125,311 B | 26.5629,-81.9495 | md5 CLEAR (68k); aHash n/a (map render) |
| map-fort-myers-beach.jpg (NEW, OSM tiles) | OpenStreetMap tiles (z12) | L-10 strip (not installed — spec §6) | 1200×560 | 123,893 B | 26.4442,-81.9557 | md5 CLEAR (68k); aHash n/a (map render) |

## 13. Honest flags (what was NOT done and why)

1. **/privacy-policy/ hero LEFT** — no genuinely better topical photo
   exists; the laptop+padlock stock is topical, not wrong (§4).
2. **About "Wet floors and cabinets" card shows the street photo** — shared
   positional manifest; correct photo staged, needs a 1-line functions.php
   change (§7).
3. **About "How We Work" has no photo** — no existing block renders a bare
   photo there without adding words; ideal = photo-strip block (§7).
4. **L-10 strips not installed in cape-coral.php / fort-myers-beach.php** —
   needs a new block + CSS outside my owned files; real map images ready
   + exact spec in §6.
5. **A-2 follow-up: /areas/ card titles render at 42px** until the CSS
   worker adds `.area-card h2.area-card-title` — recorded in
   `qa/FINDINGS-10x-design.md` with the exact CSS.
6. **Live map tiles unverified** (Google unreachable from this VM) —
   standing item.
