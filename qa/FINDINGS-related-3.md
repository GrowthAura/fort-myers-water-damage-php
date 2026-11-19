# FINDINGS — Task 13: Related = 3 + Homepage Anchor Variations

Fort Myers NEW PHP site (`~/workspace/fort-myers-php/`). Local only — no commit, no push.
Date: 2026-11-19 ~18:20–18:40 PKT. Worker: related-links worker (Task 13).

## Structure (verified)

The Related section is NOT a `related` block type. It is an `h2` ("Related Water Damage Help in Fort Myers",
or the guide/area variant heading) followed by a plain `ul` block of link items. Every page's homepage
link (`href="/"`) was already the LAST item in its list before this task — no reordering was needed.
The old homepage anchor on ALL 27 pages was identical: "Water damage restoration in Fort Myers".

## Summary

- Pages with a Related section: **27** (18 service + 4 guide + 6 area — see classification below).
- Every Related list trimmed to **exactly 3 items**: first 2 service links in original order + homepage link last.
- Total items removed: **98** (words + links, deleted entirely).
- Homepage anchor variations: **27 distinct new anchors** (uniqueness proof below).
- "/" audit: all 27 Related pages now have **exactly 1** `href="/"` link inside `<main>` (the varied homepage link).
- Extra body "/" links de-linked (words kept as plain text): **8 links on 7 pages** (see §4).
- `php -l` clean on all 27 edited files. All changes re-verified by re-rendering every route on the local PHP server.

## 1. Per-page trim (old count -> 3)

### ac-leak.php — service — "Related Water Damage Help in Fort Myers" — 7 -> 3
Kept:
  1. "Ceiling leak water damage" -> /ceiling-leak/
  2. "Structural drying" -> /drying/
  3. "Fort Myers water damage experts" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Condo water damage" -> /condo-leak/
  - "Water damage in vacant homes" -> /vacant-home/
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Emergency water removal" -> /water-removal/

### appliance-leak.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Water damaged kitchen cabinets" -> /cabinets/
  2. "Water damaged floors" -> /floors/
  3. "water damage restoration experts in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Condo water damage" -> /condo-leak/
  - "Burst pipe water damage" -> /burst-pipe/
  - "Emergency water removal" -> /water-removal/

### bonita-springs.php — area — "Related Water Damage Help in Bonita Springs" — 6 -> 3
Kept:
  1. "Flood and storm cleanup" -> /flood-cleanup/
  2. "Condo water damage" -> /condo-leak/
  3. "Fort Myers water damage restoration pros" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Water damage in vacant homes" -> /vacant-home/
  - "Commercial and vacation rental water damage" -> /commercial/
  - "Water damage restoration in Estero" -> /estero/

### burst-pipe.php — service — "Related Water Damage Help in Fort Myers" — 7 -> 3
Kept:
  1. "Emergency water removal" -> /water-removal/
  2. "Slab leak water damage" -> /slab-leak/
  3. "Fort Myers water damage cleanup" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Ceiling leak water damage" -> /ceiling-leak/
  - "Structural drying" -> /drying/
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Water damaged floors" -> /floors/

### cabinets.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Appliance leak water damage" -> /appliance-leak/
  2. "Water damaged floors" -> /floors/
  3. "water damage cleanup in Fort Myers, FL" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Condo water damage" -> /condo-leak/
  - "Burst pipe water damage" -> /burst-pipe/
  - "Structural drying" -> /drying/

### cape-coral.php — area — "Related Water Damage Help in Cape Coral and Lee County" — 6 -> 3
Kept:
  1. "Slab leak water damage" -> /slab-leak/
  2. "Cast iron pipe water damage" -> /cast-iron-pipe/
  3. "water damage restoration in Fort Myers, Florida" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Flood and storm cleanup" -> /flood-cleanup/
  - "Water damage in vacant homes" -> /vacant-home/
  - "Commercial and vacation rental water damage" -> /commercial/

### cast-iron-pipe.php — service — "Related Water Damage Help in Fort Myers" — 7 -> 3
Kept:
  1. "Sewage backup cleanup" -> /sewage-cleanup/
  2. "Emergency water removal" -> /water-removal/
  3. "24/7 water damage help in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Slab leak water damage" -> /slab-leak/
  - "Water damaged floors" -> /floors/
  - "Structural drying" -> /drying/

### ceiling-leak.php — service — "Related Water Damage Help in Fort Myers" — 7 -> 3
Kept:
  1. "AC leak water damage" -> /ac-leak/
  2. "Condo water damage" -> /condo-leak/
  3. "water damage repair in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Emergency water removal" -> /water-removal/
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Structural drying" -> /drying/
  - "Flood and storm cleanup" -> /flood-cleanup/

### commercial.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Emergency water removal" -> /water-removal/
  2. "Structural drying" -> /drying/
  3. "commercial water damage restoration in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Ceiling leak water damage" -> /ceiling-leak/
  - "Condo water damage" -> /condo-leak/

### condo-leak.php — service — "Related Water Damage Help in Fort Myers" — 8 -> 3
Kept:
  1. "Ceiling leak water damage" -> /ceiling-leak/
  2. "AC leak water damage" -> /ac-leak/
  3. "Fort Myers water damage restoration services" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Water damage in vacant homes" -> /vacant-home/
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Insurance and water damage in Florida" -> /insurance/
  - "Structural drying" -> /drying/

### cost.php — guide — "Related Water Damage Guides for Fort Myers Homeowners" — 8 -> 3
Kept:
  1. "How insurance handles water damage in Florida" -> /insurance/
  2. "First-hour water damage checklist" -> /first-hour-checklist/
  3. "Fort Myers water damage restoration team" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Emergency water removal" -> /water-removal/
  - "Structural drying" -> /drying/
  - "Burst pipe water damage" -> /burst-pipe/
  - "Slab leak water damage" -> /slab-leak/
  - "What happens after you call" -> /how-it-works/

### drying.php — service — "Related Water Damage Help in Fort Myers" — 8 -> 3
Kept:
  1. "Emergency water removal" -> /water-removal/
  2. "AC leak water damage" -> /ac-leak/
  3. "Fort Myers water damage restoration company" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Ceiling leak water damage" -> /ceiling-leak/
  - "Water damage in vacant homes" -> /vacant-home/
  - "What happens after you call" -> /how-it-works/
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Commercial water damage" -> /commercial/

### estero.php — area — "Related Water Damage Help in Estero" — 6 -> 3
Kept:
  1. "Condo water damage" -> /condo-leak/
  2. "AC leak water damage" -> /ac-leak/
  3. "Fort Myers water damage specialists" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Water damage in vacant homes" -> /vacant-home/
  - "Commercial and vacation rental water damage" -> /commercial/
  - "Water damage restoration in Bonita Springs" -> /bonita-springs/

### first-hour-checklist.php — guide — "Related Water Damage Help in Fort Myers" — 8 -> 3
Kept:
  1. "Emergency water removal" -> /water-removal/
  2. "Structural drying" -> /drying/
  3. "Fort Myers water damage help" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Water damage in vacant homes" -> /vacant-home/
  - "AC leak water damage" -> /ac-leak/
  - "Ceiling leak water damage" -> /ceiling-leak/
  - "Condo water damage" -> /condo-leak/

### flood-cleanup.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Sewage backup cleanup" -> /sewage-cleanup/
  2. "Structural drying" -> /drying/
  3. "flood damage restoration in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Mobile home water damage" -> /mobile-home/
  - "Insurance and water damage in Florida" -> /insurance/
  - "Commercial water damage" -> /commercial/

### floors.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Water damaged kitchen cabinets" -> /cabinets/
  2. "Slab leak water damage" -> /slab-leak/
  3. "Fort Myers water damage restoration" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Appliance leak water damage" -> /appliance-leak/
  - "Emergency water removal" -> /water-removal/
  - "Structural drying" -> /drying/

### fort-myers-beach.php — area — "Related Water Damage Help on Fort Myers Beach" — 6 -> 3
Kept:
  1. "Flood and storm cleanup" -> /flood-cleanup/
  2. "Condo water damage" -> /condo-leak/
  3. "emergency water damage restoration in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Water damage in vacant homes" -> /vacant-home/
  - "Commercial and vacation rental water damage" -> /commercial/

### how-it-works.php — guide — "Related Water Damage Guides for Fort Myers" — 6 -> 3
Kept:
  1. "First-hour water damage checklist" -> /first-hour-checklist/
  2. "Emergency water removal" -> /water-removal/
  3. "water damage help in Fort Myers, FL" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Structural drying" -> /drying/
  - "How insurance handles water damage in Florida" -> /insurance/
  - "Contact" -> /contact/

### insurance.php — guide — "Related Water Damage Guides for Fort Myers Homeowners" — 7 -> 3
Kept:
  1. "Water damage pricing guide" -> /cost/
  2. "First-hour water damage checklist" -> /first-hour-checklist/
  3. "Fort Myers water damage restoration professionals" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Condo water damage" -> /condo-leak/
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Water damage in vacant homes" -> /vacant-home/
  - "What happens after you call" -> /how-it-works/

### lehigh-acres.php — area — "Related Water Damage Help in Lehigh Acres and Lee County" — 6 -> 3
Kept:
  1. "AC leak water damage" -> /ac-leak/
  2. "Burst pipe water damage" -> /burst-pipe/
  3. "Fort Myers water damage restoration service" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Water heater leak cleanup" -> /water-heater-leak/
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Flood and storm cleanup" -> /flood-cleanup/

### mobile-home.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Water heater leak cleanup" -> /water-heater-leak/
  2. "Burst pipe water damage" -> /burst-pipe/
  3. "water damage restoration company in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Flood and storm cleanup" -> /flood-cleanup/
  - "Water damage in vacant homes" -> /vacant-home/
  - "Lee County service areas" -> /areas/

### north-fort-myers.php — area — "Related Water Damage Help in North Fort Myers" — 6 -> 3
Kept:
  1. "Mobile home water damage" -> /mobile-home/
  2. "Water heater leak cleanup" -> /water-heater-leak/
  3. "water damage experts in Fort Myers, FL" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Flood and storm cleanup" -> /flood-cleanup/
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Water damage restoration in Cape Coral" -> /cape-coral/

### sewage-cleanup.php — service — "Related Water Damage Help in Fort Myers" — 7 -> 3
Kept:
  1. "Cast iron pipe water damage" -> /cast-iron-pipe/
  2. "Condo water damage" -> /condo-leak/
  3. "emergency water damage cleanup in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Emergency water removal" -> /water-removal/
  - "Structural drying" -> /drying/
  - "Flood and storm cleanup" -> /flood-cleanup/

### slab-leak.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Water damaged floors" -> /floors/
  2. "Burst pipe water damage" -> /burst-pipe/
  3. "Fort Myers water damage repair experts" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Cast iron pipe water damage" -> /cast-iron-pipe/
  - "Structural drying" -> /drying/
  - "First-hour water damage checklist" -> /first-hour-checklist/

### vacant-home.php — service — "Related Water Damage Help in Fort Myers" — 7 -> 3
Kept:
  1. "AC leak water damage" -> /ac-leak/
  2. "Condo water damage" -> /condo-leak/
  3. "emergency water removal in Fort Myers" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Ceiling leak water damage" -> /ceiling-leak/
  - "Sewage backup cleanup" -> /sewage-cleanup/
  - "Structural drying" -> /drying/
  - "First-hour water damage checklist" -> /first-hour-checklist/

### water-heater-leak.php — service — "Related Water Damage Help in Fort Myers" — 6 -> 3
Kept:
  1. "Emergency water removal" -> /water-removal/
  2. "Burst pipe water damage" -> /burst-pipe/
  3. "Fort Myers emergency water damage restoration" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "Condo water damage" -> /condo-leak/
  - "Mobile home water damage" -> /mobile-home/
  - "Water damaged floors" -> /floors/

### water-removal.php — service — "Related Water Damage Help in Fort Myers" — 8 -> 3
Kept:
  1. "Water mitigation and structural drying" -> /drying/
  2. "Sewage backup cleanup" -> /sewage-cleanup/
  3. "water damage restoration in Fort Myers, FL" -> /  (homepage, anchor varied — was "Water damage restoration in Fort Myers")
Removed:
  - "First-hour water damage checklist" -> /first-hour-checklist/
  - "Ceiling leak water damage" -> /ceiling-leak/
  - "Water damage in vacant homes" -> /vacant-home/
  - "What happens after you call" -> /how-it-works/
  - "All Lee County service areas" -> /areas/

## 2. Homepage anchor variation map (page -> old anchor -> new anchor)

Old anchor on every page: "Water damage restoration in Fort Myers". `href` stays `/` on all 27.

- ac-leak.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage experts"
- appliance-leak.php: "Water damage restoration in Fort Myers" -> "water damage restoration experts in Fort Myers"
- bonita-springs.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage restoration pros"
- burst-pipe.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage cleanup"
- cabinets.php: "Water damage restoration in Fort Myers" -> "water damage cleanup in Fort Myers, FL"
- cape-coral.php: "Water damage restoration in Fort Myers" -> "water damage restoration in Fort Myers, Florida"
- cast-iron-pipe.php: "Water damage restoration in Fort Myers" -> "24/7 water damage help in Fort Myers"
- ceiling-leak.php: "Water damage restoration in Fort Myers" -> "water damage repair in Fort Myers"
- commercial.php: "Water damage restoration in Fort Myers" -> "commercial water damage restoration in Fort Myers"
- condo-leak.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage restoration services"
- cost.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage restoration team"
- drying.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage restoration company"
- estero.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage specialists"
- first-hour-checklist.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage help"
- flood-cleanup.php: "Water damage restoration in Fort Myers" -> "flood damage restoration in Fort Myers"
- floors.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage restoration"
- fort-myers-beach.php: "Water damage restoration in Fort Myers" -> "emergency water damage restoration in Fort Myers"
- how-it-works.php: "Water damage restoration in Fort Myers" -> "water damage help in Fort Myers, FL"
- insurance.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage restoration professionals"
- lehigh-acres.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage restoration service"
- mobile-home.php: "Water damage restoration in Fort Myers" -> "water damage restoration company in Fort Myers"
- north-fort-myers.php: "Water damage restoration in Fort Myers" -> "water damage experts in Fort Myers, FL"
- sewage-cleanup.php: "Water damage restoration in Fort Myers" -> "emergency water damage cleanup in Fort Myers"
- slab-leak.php: "Water damage restoration in Fort Myers" -> "Fort Myers water damage repair experts"
- vacant-home.php: "Water damage restoration in Fort Myers" -> "emergency water removal in Fort Myers"
- water-heater-leak.php: "Water damage restoration in Fort Myers" -> "Fort Myers emergency water damage restoration"
- water-removal.php: "Water damage restoration in Fort Myers" -> "water damage restoration in Fort Myers, FL"

**Uniqueness proof:** 27 pages, 27 distinct new anchors — count of distinct new anchors == count of pages. No anchor is used twice.
Each new anchor is an honest Fort Myers water-damage keyword phrase; no facts, places, or links were invented.

## 3. Non-service Related sections (task §d)

Guides and area pages carry the SAME component (identical `h2` + plain `ul` of link items), so the same
3-item rule was applied to them — no guessing was needed:
- Guides (4): cost.php, insurance.php, how-it-works.php ("Related Water Damage Guides for Fort Myers
  Homeowners" / "...for Fort Myers"), first-hour-checklist.php (service-style heading). All trimmed 8/7/6/8 -> 3.
- Area pages (6): cape-coral.php, lehigh-acres.php, north-fort-myers.php, fort-myers-beach.php, estero.php,
  bonita-springs.php (area-specific headings, e.g. "Related Water Damage Help in Estero"). All trimmed 6 -> 3.
  Note: on area pages the first 2 kept items are service links and the 3rd is the homepage link; the
  area-to-area link that sat in position 5 on bonita-springs / estero / north-fort-myers (e.g. Estero ->
  Bonita Springs) was removed as part of the trim — it was not among the first 2 items.

### Left UNCHANGED (different construct — flagged for the coordinator)

- privacy-policy.php, terms.php, disclaimer.php: NO `h2` + `ul` Related section. They only contain an inline
  paragraph lead-in "Related pages: " with links inside body copy. NOT the Related component — left
  completely unchanged.
- homepage.php, areas.php, about.php, contact.php: NO Related section at all. Left unchanged.

## 4. "/" audit — body links to "/" inside <main> (rendered pages, local PHP server)

Header/footer/breadcrumb/nav/mobile-menu "Home" links are chrome and EXEMPT (not counted, not touched).
Rule: exactly ONE "/" link per page inside <main> (the Related homepage link, where a Related section exists).
"Before" = rendered before the de-links in this section (Related trim already applied; the trim did not change
"/" counts — each Related list kept its single homepage link). "After" = re-rendered after the de-links.

| Page | "/" in <main> before | "/" in <main> after | Extra link(s) de-linked (words kept as plain text) |
|---|---|---|---|
| ac-leak | 1 | 1 | — (none; Related homepage link was already the only one) |
| appliance-leak | 1 | 1 | — (none; Related homepage link was already the only one) |
| bonita-springs | 2 | 1 | "Fort Myers" (area intro paragraph) |
| burst-pipe | 1 | 1 | — (none; Related homepage link was already the only one) |
| cabinets | 1 | 1 | — (none; Related homepage link was already the only one) |
| cape-coral | 1 | 1 | — (none; Related homepage link was already the only one) |
| cast-iron-pipe | 1 | 1 | — (none; Related homepage link was already the only one) |
| ceiling-leak | 1 | 1 | — (none; Related homepage link was already the only one) |
| commercial | 1 | 1 | — (none; Related homepage link was already the only one) |
| condo-leak | 1 | 1 | — (none; Related homepage link was already the only one) |
| cost | 2 | 1 | "water damage restoration in Fort Myers" ("More on the 50% rule: ..." paragraph) |
| drying | 3 | 1 | "black water explained on the homepage" (water-class paragraph); "planning the rebuild" (50% rule checklist item) |
| estero | 2 | 1 | "Fort Myers" (area intro paragraph) |
| first-hour-checklist | 1 | 1 | — (none; Related homepage link was already the only one) |
| flood-cleanup | 2 | 1 | "water damage restoration in Fort Myers" ("More on the 50% rule: ..." paragraph) |
| floors | 1 | 1 | — (none; Related homepage link was already the only one) |
| fort-myers-beach | 2 | 1 | "Fort Myers" (area intro paragraph) |
| how-it-works | 1 | 1 | — (none; Related homepage link was already the only one) |
| insurance | 1 | 1 | — (none; Related homepage link was already the only one) |
| lehigh-acres | 1 | 1 | — (none; Related homepage link was already the only one) |
| mobile-home | 1 | 1 | — (none; Related homepage link was already the only one) |
| north-fort-myers | 2 | 1 | "Fort Myers" (area intro paragraph) |
| sewage-cleanup | 1 | 1 | — (none; Related homepage link was already the only one) |
| slab-leak | 1 | 1 | — (none; Related homepage link was already the only one) |
| vacant-home | 1 | 1 | — (none; Related homepage link was already the only one) |
| water-heater-leak | 1 | 1 | — (none; Related homepage link was already the only one) |
| water-removal | 1 | 1 | — (none; Related homepage link was already the only one) |
| areas | 1 | 1 | — (no Related section; single body "/" link, untouched) |
| about | 1 | 1 | — (no Related section; single body "/" link, untouched) |
| contact | 1 | 1 | — (no Related section; single body "/" link, untouched) |
| homepage (/) | 0 | 0 | — (no Related section; no "/" link in <main>, no self-link) |
| privacy-policy | 0 | 0 | — (no Related section) |
| terms | 0 | 0 | — (no Related section) |
| disclaimer | 0 | 0 | — (no Related section) |

De-link method (Task 6 rule): the `'href' => '/'` line was removed from the segment; the `'t'` text was
kept verbatim as plain text. Verified in the render: e.g. drying still shows "black water explained on the
homepage" as plain text; cost still shows "More on the 50% rule: water damage restoration in Fort Myers"
as plain text. No other words changed anywhere.

## 5. Verification performed

- Inventory: parsed all 35 data files; 27 carry the Related `h2` + `ul`; homepage link present on all 27, last on all 27.
- Trim script asserted per file: exactly 1 homepage link, homepage last, old anchor exactly
  "Water damage restoration in Fort Myers"; rebuilt the `ul` from the kept items' original source text.
- `php -l` on all 27 edited files: no syntax errors (plus the 7 de-linked files re-linted after de-linking).
- Render check 1 (after trim, before de-links): all 27 Related lists render exactly 3 `<li>` items; every new
  homepage anchor present in its page's `<main>`.
- Render check 2 (after de-links, all 34 routes): every page has 0 or 1 "/" link in `<main>` as tabulated above;
  all 27 Related pages exactly 1.
- Postscript: after the first render check the kept items' opening brackets were found at column 0 (the
  trim script had dropped their 16-space indent). All 3 brackets in each of the 27 files were re-indented
  to the file's original 16-space style (content unchanged); `php -l` re-run clean on all files and the
  full render audit (§4) was re-run after the fix — all 27 Related pages still exactly 3 items and exactly
  1 "/" link in `<main>`. Final `git diff` on e.g. water-removal.php shows only the removed items + the
  anchor change.
- No other files touched: header.php / footer.php / functions.php / styles.css untouched. No hrefs changed.
  No commit, no push. (Note: `git status` also shows pre-existing modifications by other workers —
  e.g. homepage.php, header.php, qa/STATUS-20x.md — none of those are mine.)

## 6. Files edited (27)

site/data/ac-leak.php, site/data/appliance-leak.php, site/data/bonita-springs.php,
site/data/burst-pipe.php, site/data/cabinets.php, site/data/cape-coral.php, site/data/cast-iron-pipe.php,
site/data/ceiling-leak.php, site/data/commercial.php, site/data/condo-leak.php, site/data/cost.php,
site/data/drying.php, site/data/estero.php, site/data/first-hour-checklist.php, site/data/flood-cleanup.php,
site/data/floors.php, site/data/fort-myers-beach.php, site/data/how-it-works.php, site/data/insurance.php,
site/data/lehigh-acres.php, site/data/mobile-home.php, site/data/north-fort-myers.php,
site/data/sewage-cleanup.php, site/data/slab-leak.php, site/data/vacant-home.php,
site/data/water-heater-leak.php, site/data/water-removal.php

