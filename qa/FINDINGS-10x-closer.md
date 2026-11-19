# FINDINGS — 10x CLOSER (3 open items)

Fort Myers PHP site (`~/workspace/fort-myers-php/`). LOCAL ONLY — no push, no
deploy, no DNS, no git commit (no commit made in this round; the author
preference Noorullahmian <noorullahchhachher3@gmail.com> stands but was
not needed — nothing was committed). `qa/verify_export.py` NEVER run.
`out/` never touched. Verified on my own PHP 8.3.6 server
(`php -S 127.0.0.1:8136 -t site site/index.php`, killed by PID at end)
with Playwright bundled Chromium only.

## Verdict — all 3 items DONE and verified

| Item | Result |
|---|---|
| 1. L-10 map strips, /cape-coral/ + /fort-myers-beach/ | Installed, renders at 1440/390/320 |
| 2. About "Wet floors and cabinets" wrong photo | Fixed — idx 5 now the floors/cabinets photo; homepage unchanged |
| 3. /areas/ card titles 42px | Now 23px, side padding, no bar; promoted H2s untouched |

Global gates (5 pages × 1440/390/320, `qa/10x-closer-measure.json`):
**H1 = 1 on all 5 pages at all 3 widths; overflow 0 at 320/390/1440 on all
5; console/page errors 0; 0 em/en dashes in the rendered HTML of all 5.**

## 1. ITEM 1 — L-10 area map strips

### Decision: new block type `area-map` (did NOT reuse `map`)

The existing `map` block hardcodes the Fort Myers iframe
(`q=Fort%20Myers%2C%20FL%2033901`, z=12), renders the caption as an H2
(would add a heading to the outline), and has no caption-link / facts-band
slots. Adapting it would have meant parameterising its URL + caption level
+ adding chips — a bigger, riskier change than a small dedicated case. The
new `area-map` case renders a static image from `$MEDIA['maps']` only, adds
no heading, and takes caption/facts/link from the data block.

### What changed

- `site/includes/functions.php:791` — new `case 'area-map'` in
  `render_block()`. Renders
  `<figure class="area-map-strip">` with the manifest map image
  (1200×560, `loading="lazy"`), `<figcaption>` = caption + `View larger
  map ↗` link (`target="_blank" rel="noopener"`), `<p
  class="area-map-attr">© OpenStreetMap contributors</p>`, and
  `<ul class="area-map-facts">` with one `<li>` per fact. Missing manifest
  slot renders nothing (honestly empty).
- `site/data/cape-coral.php:75` — `area-map` block inserted immediately
  after the intro `p` ("For water damage in a Cape Coral home, shut off
  the water…", the first `p` after the hero/cta-line). `map =>
  'cape-coral'`, caption `Cape Coral and the Lee County service area`,
  facts `['400+ miles of canals', 'ZIPs 33904-33993', 'Slab homes']`,
  `map_url => 'https://www.google.com/maps?q=Cape+Coral,+FL'`.
- `site/data/fort-myers-beach.php:71` — same placement after the intro `p`
  ("For water damage on Fort Myers Beach, follow official re-entry
  rules…"). Caption `Fort Myers Beach and the Lee County service area`,
  facts `['Estero Island', 'ZIP 33931', 'Elevated homes']`,
  `map_url => 'https://www.google.com/maps?q=Fort+Myers+Beach,+FL'`.
  (DOM-verified: the figure's previous element sibling is the intro `<p>`
  on both pages.)
- `site/assets/css/styles.css:1635-1643` — appended 10x CLOSER block:
  `.area-map-strip { margin: 40px 0; }` (32px ≤620px);
  `.area-map-img` 2px gold border (`var(--gold)`), 14px radius,
  `width:100%; height:auto`; caption 20px ink; attribution 16px muted;
  facts chips sand (`var(--sand-2)`) bg, teal-dark text, 16px/700,
  pill radius, wrap with 10px gap.

### Deliberate deviation — en dash → hyphen in one chip (0-dash rule)

The spec writes the Cape Coral chip as `ZIPs 33904–33993` with an **en
dash**. The round's hard rule is 0 dashes in visible HTML. I rendered it
as `ZIPs 33904-33993` (hyphen-minus, same as the site's own copy style) —
meaning identical, dash count stays 0. All other caption/fact text is
verbatim from the spec.

### Measured (Playwright, port 8136)

| Check | Cape Coral | Fort Myers Beach |
|---|---|---|
| Image | `/assets/img/map-cape-coral.jpg`, natural 1200×560, box 1192×558 @1440, 350×165 @390, 280×133 @320 | `/assets/img/map-fort-myers-beach.jpg`, natural 1200×560, same boxes |
| Border / radius | 2px solid `rgb(201,155,63)` (gold) / 14px | same |
| Caption | `Cape Coral and the Lee County service area` (+ link), 20px, ink `rgb(18,38,46)` | `Fort Myers Beach and the Lee County service area` (+ link), 20px, ink |
| Link | `https://www.google.com/maps?q=Cape+Coral,+FL` (1 occurrence; same `q=` pattern as the existing embed) | `https://www.google.com/maps?q=Fort+Myers+Beach,+FL` (1 occurrence) |
| Attribution | `© OpenStreetMap contributors`, 16px, 1 occurrence | same, 1 occurrence |
| Chips | `400+ miles of canals` / `ZIPs 33904-33993` / `Slab homes` — 16px/700, bg `rgb(239,231,214)`, text `rgb(8,63,74)` | `Estero Island` / `ZIP 33931` / `Elevated homes` — same styling |
| Placement | figure directly after the intro `<p>` | figure directly after the intro `<p>` |

Contrast (computed from the hex values): caption ink on white **15.64:1**;
attribution muted on white **7.44:1**; chips teal-dark on sand-2
**9.38:1**; map link teal on white **8.42:1**. Gold border is decorative
only (2.55:1 — not a text contrast). All text ≥4.5:1.

Screenshots (viewed): `qa/screenshots-10x-closer/cape-coral-1440-mapstrip.png`
(real OSM render, Cape Coral labelled, gold border, caption + link +
attribution + 3 chips), `fort-myers-beach-1440-mapstrip.png` (Estero
Island + "Fort Myers Beach" label, Sanibel, Estero Bay), and the 390px
versions of both (chips wrap, no overflow).

## 2. ITEM 2 — About help card idx 5, wrong photo

### What changed

- `site/includes/functions.php:583` — help-cards branch, exact line from
  FINDINGS-10x-images.md §7 verified in the file before editing:
  - Before: `$imgs = $GLOBALS['MEDIA']['help']['home'] ?? [];`
  - After: `$imgs = $GLOBALS['MEDIA']['help'][$page['slug'] === '/about/' ? 'about' : 'home'] ?? [];`
  - Comment updated: the branch now serves homepage + /about/ (was
    labelled "homepage only"). No other logic touched.
- `site/data/media-manifest.php:347` — new `$MEDIA['help']['about']`, 7
  entries in About order (header comment updated, line 13):
  0 emergency (`help-emergency-water-removal.jpg`), 1 drying
  (`help-structural-drying.jpg`), 2 sewage (`help-sewage-cleanup.jpg`,
  the new PPE photo), 3 flood (`help-flood-storm-cleanup.jpg`), 4 leaks
  (`help-leaks-every-kind.jpg`), 5 floors/cabinets
  (`about-floors-cabinets.jpg`, NEW alt 109 chars — "A swollen cabinet
  base and curled wet vinyl plank flooring checked with a moisture meter
  in a Fort Myers home", ≤125), 6 property-types
  (`help-property-types.jpg`). The 6 reused entries copy the home entries
  verbatim (src/alt/width/height); only idx 5 is new. `home` key
  untouched (still 7 entries; homepage uses idx 0–5).

### Measured

- /about/: 7 help cards at 1440/390/320, all images natural 474×267,
  boxes 381×327/355 desktop. Order verified:
  emergency → drying → sewage → flood → leaks →
  **`about-floors-cabinets.jpg` (idx 5)** → property-types.
  `about-floors-cabinets` occurs 1× in /about/ HTML, 0× on the homepage.
- Homepage: 6 help cards UNCHANGED at all widths — same 6 home images in
  home order, idx 5 still `help-every-property.jpg` (the street photo,
  correct for the homepage's "Every kind of property" card).
- Screenshots (viewed): `qa/screenshots-10x-closer/about-1440-helpcards.png`
  — idx 5 "Wet floors and cabinets" now shows the curled vinyl plank +
  moisture meter in gloved hands + air mover (the correct photo, not the
  street photo); idx 6 shows the street/property-types photo.
  `home-1440-helpcards.png` — all 6 homepage cards correct, idx 5 the
  street photo as before.

### Note — lazy-load timing, not a defect

At measure time (before any scroll) the homepage's 6 help images read
`naturalWidth 0` — they are `loading="lazy"` and sit below the fold, so
they had not loaded yet; /about/'s 7 (near the top) read 474×267
immediately. After `scrollIntoView` the homepage images all load (visible
in `home-1440-helpcards.png`). Same behaviour as Worker 3 recorded for
heroes.

### Note — screenshot artefact, not a defect

In the element screenshots the sticky header overlaps the top row of
cards. That is the capture scrolling the element under the fixed header;
on the live page the header sits above the content normally.

## 3. ITEM 3 — /areas/ card titles at 42px

### What changed

- `site/assets/css/styles.css:1628-1629` — appended the EXACT A-2 rules
  from `qa/FINDINGS-10x-design.md`:
  `.area-card h2.area-card-title { margin: 20px 0 0; padding: 0 28px; font-size: 23px; }`
  `.page-body h2.area-card-title::before { display: none; }`
- `site/assets/css/styles.css:1566-1571` — the Worker-1 rule
  `.page-body .area-card h2.area-card-title` corrected **24px → 23px**
  (comment updated). This was REQUIRED, not optional: that rule's
  specificity (3 classes) beats the exact A-2 rule (2 classes), so adding
  the A-2 rule alone would have left the titles at 24px. Worker 1's 24px
  deviation rested on "area-card h3 renders 24px" — that came from the
  generic `.page-body .body-section h3 { font-size: 24px; }` rule, while
  the base `.area-card h3` rule (line 652) and the L-7 rule (line 1373)
  are both 23px. The closer brief's explicit 23px spec + the A-2 spec
  agree, so 23px is now the single value everywhere. All other properties
  of the Worker-1 rule (line-height, letter-spacing, terracotta colour,
  padding-bottom/border-bottom 0) are unchanged.

### Measured

- 6 card titles, all widths: **23px**, padding-left/right **28px**,
  margin-top **20px**, colour terracotta `rgb(147,56,14)` (7.47:1 on
  white), `::before` display **none**. "North Fort Myers" now fits on one
  line at 1440. Outline unchanged: `<main>` H2 **17** (6 card titles +
  11 section H2s), H3 **0**.
- The 5 promoted H2 headings stay at FULL H2 size — measured **46px**
  (feature: "Lee County Service Areas and ZIP Codes") and **40px**
  (standard: Fort Myers, Sanibel and Captiva, Pine Island and Matlacha,
  San Carlos Park/Gateway/Iona) at 1440; 34px / 31px at 390/320 (the
  ≤620px L-6 scale). The brief's parenthetical "(42px)" predates L-6's
  feature/standard scale (base `h2` is 42px, but L-6 classes override it
  to 46/40) — the promoted headings were NOT resized to 42px, because
  that would fight L-6 and is outside this item. They are at their full
  designed H2 size, as decided.
- Screenshots (viewed): `qa/screenshots-10x-closer/areas-1440-cards.png`
  (23px terracotta titles, no bar, side padding, one-line "North Fort
  Myers"), `areas-390-cards.png`.

## Word / link audit (all 5 pages)

- 0 word changes outside the authorised additions. The only new visible
  strings are the two strips' spec text (caption, `View larger map ↗`,
  `© OpenStreetMap contributors`, 6 chip texts) — occurrence counts
  verified in rendered HTML: strip 1×, `area-map-link` 1×, OSM
  attribution 1× per map page; 0× on home/about/areas. (Apparent extra
  hits are pre-existing copy: "Slab homes" ×2 on /cape-coral/ = chip +
  the list item "Slab homes, everywhere."; "Estero Island" ×7 on
  /fort-myers-beach/ = chip + 6 pre-existing mentions; "Elevated homes"
  ×2 = chip + the details-row label.)
- No invented links: the only new external URLs are the two Google Maps
  `q=` links above (1 occurrence each), same pattern as the site's
  existing map embed. Footer `View larger map` links are pre-existing and
  untouched (home 1, about 1, areas 0, map pages 0 — footer maps exist
  only on home/about, so the map pages' single "View larger map" is the
  new strip link).
- 0 em/en dashes in rendered HTML of all 5 pages (the en dash in the
  spec's `33904–33993` is the one deliberate hyphen substitution above).
- No other files touched. About "How We Work" photo strip NOT added
  (flagged, no spec — left for the owner, per brief).

## Files changed (this round only)

- `site/includes/functions.php` — help-cards slug gate (:583) + new
  `area-map` case (:791–813).
- `site/data/media-manifest.php` — `$MEDIA['help']['about']` 7 entries
  (:347–396) + header comment (:13–15).
- `site/data/cape-coral.php` — `area-map` block (:75–81).
- `site/data/fort-myers-beach.php` — `area-map` block (:71–77).
- `site/assets/css/styles.css` — Worker-1 rule 24px → 23px (:1566) +
  appended closer block (:1624–1643: exact A-2 rules + L-10 strip CSS).
- `qa/probe_10x_closer.py`, `qa/10x-closer-measure.json`,
  `qa/screenshots-10x-closer/` (10 PNGs), this file.

## Open notes for the owner / deploy

1. `styles.css?v=3` in `header.php` was NOT bumped (out of the three
   items' scope; the file was not listed). Consider `?v=4` at deploy time
   so cached CSS refreshes — the verifier/deploy owner to decide.
2. Live Google map tiles still need one real-browser look (standing item;
   Google unreachable from this VM — the strips use static OSM images, so
   they render fully here, but the `map` iframes elsewhere do not).
3. One read-only `git status` was run during this round to list changed
   files (no commit, no staging, no history change); the working tree
   also holds sibling workers' in-flight changes — not mine, not touched.
