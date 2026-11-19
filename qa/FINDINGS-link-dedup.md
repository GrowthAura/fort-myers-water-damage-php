# FINDINGS — Phase 2.5 Task 6: One Internal Link Per Target Per Page

Fort Myers NEW PHP site (`~/workspace/fort-myers-php/`). Coordinator: subagent 17ff0e4c.
Date: 2026-11-19 ~20:30–21:10 PKT. Worker: link-dedup worker (Task 6).
Local only — no commit, no push, no deploy (no token held).

## 0. Rule — one link per target per page in `<main>`

Every internal link target (`href="/slug/"`) appears at most once inside `<main>` on every page.
Header, footer, nav, mobile menu and breadcrumb are chrome and exempt (the breadcrumb Home link is
an absolute site URL, not a relative `/` link, and was never counted — same convention as the
coordinator's audit and the Task 13 `/` audit). The hero `/contact/` CTA button on the homepage is
hardcoded in `site/includes/functions.php`, not in page data; it is the homepage's only `/contact/` link
in `<main>` and was untouched.

## 1. Card-vs-body decision (recorded for the owner to correct if he disagrees)

**Decision: card links win over body-copy links.** Where a target appears in both a card and body
copy, the card keeps the link and every body occurrence is de-linked (words stay as plain text) or,
for a whole pointer sentence, removed. Where a target appears only in body copy, the first body
occurrence in document order keeps the link and the rest are de-linked/removed. Related lists
(Task 13: exactly 3 items, unique homepage anchor per page) were NOT touched — no Related item was
removed, reordered or re-anchored; every Related link that was kept is the kept occurrence for its
target on its page.

Card = Related list (`h2` "Related…" + `ul`), `kinds` cards, `help-cards` (`ul` variant), `area-cards`.
Everything else (`p`, plain `ul`, `table`, `steps`, `steps-numbered`, `steps-rich` parts, `faq`,
`details` rows, `hero-intro`) is body copy.

**Within cards, kinds beat help-cards.** The homepage carries two card systems with 9 overlapping
targets (AC, appliance, burst pipe, slab, water heater, flood, sewage, condo, mobile home). A kinds
card exists for exactly one target and its "See X." sentence IS the card's only link — de-linking it
would leave a photo card with a dangling "See X." pointer to nowhere. A help-card link is one inline
word inside a multi-link list sentence ("Leaks of every kind: AC leaks, burst pipes, …") — de-linking
it leaves a readable plain list. So the 9 help-card occurrences were de-linked and the 9 kinds-card
"See X." links kept. Consequence to be aware of: help cards "Sewage backup cleanup", "Flood and storm
cleanup" and "Leaks of every kind" now carry no link at all; "Every kind of property" keeps one
(businesses → /commercial/). If the owner prefers the help cards linked instead, the flip is mechanical:
re-link those 9 help-card words and de-link the 9 kinds "See X." sentences (the kinds cards would then
read "See X." as plain text).

**Pointer sentences.** A duplicate occurrence that IS a whole standalone pointer sentence ("See X.",
"See X for …", "The full list: X.", "Read …", "Use the …", "Learn how …", "For more on …, see X.")
was removed whole (words + link) — leaving it as plain text would leave a dead pointer ("See X." with
nowhere to go). A duplicate that is inline mid-sentence was de-linked only (words stay plain text).
Bright line used: the sentence must START with the pointer verb/phrase. A sentence with an informative
clause before the pointer ("If your AC is in the attic and the stain is near it, read AC leak water
damage.", "For dishwasher, fridge and washer leaks, see appliance leak water damage.") was de-linked,
words kept — the clause carries real meaning.

**Two exceptions, both deliberate:**

- Commercial + Lehigh Acres `steps` items "Water extraction" / "Extract standing water" consist of
  ONLY the sentence "See emergency water removal." — removing it would empty a titled, numbered step.
  De-linked only; the step still reads "See emergency water removal." as plain text (the Related list
  keeps the live /water-removal/ link).
- The homepage FAQ answer "See AC leak water damage, ceiling leaks and cast iron pipe damage." holds
  THREE duplicate links in one pointer sentence. Removed whole (all three links were duplicates; the
  answer is complete without it).

**Corrections to the brief (from my own re-audit — trust this over the brief where they differ):**

- `/contact/` has NO "area-keyword H3 cards". Its duplicates were the areas TABLE ("Local page" column,
  one link per area — kept) + the FAQ answer listing the same area names inline (de-linked, words kept).
  The table is the navigation here; the FAQ list is body copy.
- `/terms/` + `/disclaimer/` + `/privacy-policy/`: only `/terms/` had duplicates, in its inline "Related
  pages:" paragraph — the second occurrences of /disclaimer/ and /privacy-policy/ were de-linked there.
  /disclaimer/ and /privacy-policy/ themselves were already clean and untouched.
- The coordinator's audit table is reproduced EXACTLY by my independent re-audit (same 31 pages, same
  targets, same counts — see §2). No count shifted with the card wiring.

## 2. Per-page before / after (`<main>` internal links only)

Before = export before this task (`/tmp/dedup-pre-out`, snapshot kept); After = re-export after the
edits. "Links" = relative internal links in `<main>`; "Dup targets" = targets with count > 1.
After: every target on every page is exactly 1 (total == unique on all 34 pages).

| Page | Links before | Dup targets before (target: count) | Links after |
|---|---|---|---|
| `/` | 54 | /ac-leak/: 3, /appliance-leak/: 2, /burst-pipe/: 2, /cast-iron-pipe/: 2, /ceiling-leak/: 2, /commercial/: 3, /condo-leak/: 4, /drying/: 3, /flood-cleanup/: 2, /how-it-works/: 2, /mobile-home/: 3, /north-fort-myers/: 2, /sewage-cleanup/: 2, /slab-leak/: 2, /vacant-home/: 3, /water-heater-leak/: 2, /water-removal/: 3 | 29 |
| `/about/` | 25 | — | 25 |
| `/ac-leak/` | 17 | /ceiling-leak/: 2, /condo-leak/: 2, /drying/: 2 | 14 |
| `/appliance-leak/` | 21 | /cabinets/: 2, /condo-leak/: 2, /floors/: 2 | 18 |
| `/areas/` | 19 | /how-it-works/: 2 | 18 |
| `/bonita-springs/` | 20 | /condo-leak/: 3, /flood-cleanup/: 3, /vacant-home/: 2 | 15 |
| `/burst-pipe/` | 23 | /ceiling-leak/: 2, /slab-leak/: 2, /vacant-home/: 2, /water-removal/: 2 | 19 |
| `/cabinets/` | 17 | /appliance-leak/: 2, /floors/: 2 | 15 |
| `/cape-coral/` | 23 | /cast-iron-pipe/: 3, /flood-cleanup/: 2, /slab-leak/: 3 | 18 |
| `/cast-iron-pipe/` | 14 | /insurance/: 2, /sewage-cleanup/: 2 | 12 |
| `/ceiling-leak/` | 19 | /ac-leak/: 3, /condo-leak/: 3 | 15 |
| `/commercial/` | 21 | /drying/: 2, /sewage-cleanup/: 2, /water-removal/: 2 | 18 |
| `/condo-leak/` | 18 | /ac-leak/: 2, /ceiling-leak/: 2 | 16 |
| `/contact/` | 20 | /bonita-springs/: 2, /cape-coral/: 2, /estero/: 2, /fort-myers-beach/: 2, /how-it-works/: 2, /lehigh-acres/: 2, /north-fort-myers/: 2 | 13 |
| `/cost/` | 20 | /cast-iron-pipe/: 2, /condo-leak/: 2, /first-hour-checklist/: 2, /insurance/: 2, /vacant-home/: 2 | 15 |
| `/disclaimer/` | 5 | — | 5 |
| `/drying/` | 23 | /ac-leak/: 2, /ceiling-leak/: 2, /condo-leak/: 2, /vacant-home/: 2, /water-removal/: 3 | 17 |
| `/estero/` | 20 | /ac-leak/: 3, /condo-leak/: 3, /flood-cleanup/: 2, /vacant-home/: 2 | 14 |
| `/first-hour-checklist/` | 26 | /condo-leak/: 2, /drying/: 2, /water-removal/: 2 | 23 |
| `/flood-cleanup/` | 19 | /drying/: 2, /sewage-cleanup/: 3 | 16 |
| `/floors/` | 15 | /slab-leak/: 2 | 14 |
| `/fort-myers-beach/` | 21 | /condo-leak/: 4, /flood-cleanup/: 3, /sewage-cleanup/: 2 | 15 |
| `/how-it-works/` | 11 | /first-hour-checklist/: 2, /water-removal/: 2 | 9 |
| `/insurance/` | 18 | /ac-leak/: 2, /burst-pipe/: 2, /cast-iron-pipe/: 2, /first-hour-checklist/: 2, /slab-leak/: 2 | 13 |
| `/lehigh-acres/` | 23 | /ac-leak/: 3, /burst-pipe/: 2, /flood-cleanup/: 2, /sewage-cleanup/: 2, /water-removal/: 2 | 17 |
| `/mobile-home/` | 19 | /burst-pipe/: 2, /flood-cleanup/: 2, /north-fort-myers/: 2 | 16 |
| `/north-fort-myers/` | 22 | /areas/: 2, /mobile-home/: 4, /water-heater-leak/: 2 | 17 |
| `/privacy-policy/` | 3 | — | 3 |
| `/sewage-cleanup/` | 18 | /cast-iron-pipe/: 2, /condo-leak/: 2, /lehigh-acres/: 2, /north-fort-myers/: 2 | 14 |
| `/slab-leak/` | 17 | /burst-pipe/: 2, /cape-coral/: 2, /floors/: 2, /lehigh-acres/: 2 | 13 |
| `/terms/` | 6 | /disclaimer/: 2, /privacy-policy/: 2 | 4 |
| `/vacant-home/` | 18 | /ac-leak/: 2, /condo-leak/: 2 | 16 |
| `/water-heater-leak/` | 16 | /water-removal/: 2 | 15 |
| `/water-removal/` | 28 | /condo-leak/: 2, /drying/: 4, /flood-cleanup/: 3, /sewage-cleanup/: 2 | 21 |

**Totals: 659 → 522 links in `<main>` (137 removed/de-linked). Clean before this task (no dups, untouched): /about/, /disclaimer/, /privacy-policy/.**

## 3. Every removal, listed exactly (137)

Actions: DELINK = `<a>` removed, words kept as plain text. REMOVE-SENTENCE = the whole pointer sentence
(words + link) removed. REMOVE-BLOCK = the whole paragraph block removed (it was only that sentence).
KEEP is not listed per occurrence (the kept occurrence is stated in §4 for the card-wins cases; otherwise
it is the first body occurrence in document order, or the Related/kinds/area-cards link).

### `/`

- DELINK `/ac-leak/` — anchor "AC leaks" — blk5 ul items[4] — in: "Leaks of every kind: AC leaks, burst pipes, water heaters, appliances and slab leaks."
- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage, ceiling leaks and cast iron pipe damage." — blk90 faq items[6].a — from: "Clogged AC condensate lines are one of the most common causes, followed by split supply lines under sinks and toilets, failing water heaters, roof and window leaks in summer storms, appliance leaks and, in older homes, cracked cast iron drains under the slab. See AC leak water damage, ceiling leaks and cast iron pipe damage."
- DELINK `/appliance-leak/` — anchor "appliances" — blk5 ul items[4] — in: "Leaks of every kind: AC leaks, burst pipes, water heaters, appliances and slab leaks."
- DELINK `/burst-pipe/` — anchor "burst pipes" — blk5 ul items[4] — in: "Leaks of every kind: AC leaks, burst pipes, water heaters, appliances and slab leaks."
- REMOVE-SENTENCE `/cast-iron-pipe/` — "See AC leak water damage, ceiling leaks and cast iron pipe damage." — blk90 faq items[6].a — from: "Clogged AC condensate lines are one of the most common causes, followed by split supply lines under sinks and toilets, failing water heaters, roof and window leaks in summer storms, appliance leaks and, in older homes, cracked cast iron drains under the slab. See AC leak water damage, ceiling leaks and cast iron pipe damage."
- REMOVE-SENTENCE `/ceiling-leak/` — "See AC leak water damage, ceiling leaks and cast iron pipe damage." — blk90 faq items[6].a — from: "Clogged AC condensate lines are one of the most common causes, followed by split supply lines under sinks and toilets, failing water heaters, roof and window leaks in summer storms, appliance leaks and, in older homes, cracked cast iron drains under the slab. See AC leak water damage, ceiling leaks and cast iron pipe damage."
- REMOVE-SENTENCE `/commercial/` — "See commercial water damage." — blk64 ul items[0] — from: "Businesses. Restaurants, medical and dental offices, retail stores and warehouses get drying plans built around opening hours, with equipment placed so parts of the space can stay open where it is safe. See commercial water damage."
- DELINK `/commercial/` — anchor "businesses" — blk90 faq items[11].a — in: "Yes. Condos and townhomes, manufactured homes, vacation rentals, seasonal homes and businesses each hide water in different places, so each one gets a drying plan built around how it is put together."
- DELINK `/condo-leak/` — anchor "condos" — blk5 ul items[5] — in: "Every kind of property: single-family homes, condos, mobile homes, vacation rentals and businesses."
- REMOVE-BLOCK `/condo-leak/` — whole paragraph "See condo water damage for the full walkthrough." — blk61 p segs
- DELINK `/condo-leak/` — anchor "townhomes" — blk90 faq items[11].a — in: "Yes. Condos and townhomes, manufactured homes, vacation rentals, seasonal homes and businesses each hide water in different places, so each one gets a drying plan built around how it is put together."
- REMOVE-SENTENCE `/drying/` — "See how structural drying works." — blk29 steps items[3].body — from: "Dehumidifiers and air movers run around the clock. Moisture readings are taken and logged as the job goes on, and equipment is adjusted until materials reach normal dry readings, not just until surfaces feel dry. See how structural drying works."
- DELINK `/drying/` — anchor "structural drying" — blk90 faq items[1].a — in: "Everything from the first call to a dry, clean structure: emergency water removal, moisture mapping with meters and a thermal camera, structural drying with daily readings, cleaning and antimicrobial treatment where needed, and photos and moisture logs for your records and your insurer. The rebuild of drywall, flooring and cabinets comes after, and who does it is your choice."
- DELINK `/flood-cleanup/` — anchor "storm cleanup" — blk5 ul items[3] — in: "Flood and storm cleanup: rising water, storm surge and wind-driven rain."
- REMOVE-SENTENCE `/how-it-works/` — "See what happens after you call." — blk30 p segs — from: "Most clean-water jobs take about 3 to 5 days to dry. Concrete slabs, hardwood, tile on slab and sewage jobs usually take longer. See what happens after you call."
- DELINK `/mobile-home/` — anchor "mobile homes" — blk5 ul items[5] — in: "Every kind of property: single-family homes, condos, mobile homes, vacation rentals and businesses."
- DELINK `/mobile-home/` — anchor "manufactured homes" — blk90 faq items[11].a — in: "Yes. Condos and townhomes, manufactured homes, vacation rentals, seasonal homes and businesses each hide water in different places, so each one gets a drying plan built around how it is put together."
- REMOVE-SENTENCE `/north-fort-myers/` — "See North Fort Myers." — blk84 p segs — from: "North Fort Myers: manufactured-home communities and riverfront homes. See North Fort Myers."
- DELINK `/sewage-cleanup/` — anchor "Sewage backup cleanup" — blk5 ul items[2] — in: "Sewage backup cleanup: toilet, tub, floor-drain and cast iron drain backups handled as contaminated water."
- DELINK `/slab-leak/` — anchor "slab leaks" — blk5 ul items[4] — in: "Leaks of every kind: AC leaks, burst pipes, water heaters, appliances and slab leaks."
- DELINK `/vacant-home/` — anchor "seasonal homes" — blk90 faq items[11].a — in: "Yes. Condos and townhomes, manufactured homes, vacation rentals, seasonal homes and businesses each hide water in different places, so each one gets a drying plan built around how it is put together."
- REMOVE-SENTENCE `/vacant-home/` — "See the full checklist for seasonal homes." — blk90 faq items[12].a — from: "Shut off the main water valve and the water heater, leave the AC running to control humidity, and have someone walk the house regularly while you're away. A leak in an empty home can run for weeks before anyone sees it. See the full checklist for seasonal homes."
- DELINK `/water-heater-leak/` — anchor "water heaters" — blk5 ul items[4] — in: "Leaks of every kind: AC leaks, burst pipes, water heaters, appliances and slab leaks."
- REMOVE-SENTENCE `/water-removal/` — "See emergency water removal." — blk29 steps items[2].body — from: "Standing water is extracted, and soaked carpet pad and anything that cannot be saved are removed. With contaminated water, affected materials come out under containment. See emergency water removal."
- DELINK `/water-removal/` — anchor "emergency water removal" — blk90 faq items[1].a — in: "Everything from the first call to a dry, clean structure: emergency water removal, moisture mapping with meters and a thermal camera, structural drying with daily readings, cleaning and antimicrobial treatment where needed, and photos and moisture logs for your records and your insurer. The rebuild of drywall, flooring and cabinets comes after, and who does it is your choice."

### `/ac-leak/`

- REMOVE-SENTENCE `/ceiling-leak/` — "See what to do about a leaking ceiling." — blk7 ul items[3] — from: "Check the ceiling. If it sags or bulges, keep everyone out from underneath it. See what to do about a leaking ceiling."
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk40 p segs — from: "See condo water damage."
- REMOVE-SENTENCE `/drying/` — "See how structural drying works." — blk30 ul items[2] — from: "Drying with dehumidifiers and air movers, with readings logged daily. See how structural drying works."

### `/appliance-leak/`

- REMOVE-SENTENCE `/cabinets/` — "See water damaged kitchen cabinets." — blk14 ul items[2] — from: "Particle board swells. Most cabinet bases are particle board, and once it swells it doesn't go back. See water damaged kitchen cabinets."
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk23 p segs — from: "Under Florida Statute 718.111(11), the association's policy generally leaves appliances, water heaters, water filters, built-in cabinets, countertops and floor, wall and ceiling coverings inside a unit to the owner's HO-6 policy. If a washer hose or ice maker line in one unit damages another, who pays often depends on the cause and whether the appliance was kept up, and your declaration can change parts of the default. Report it to building management and your insurer the same day. See condo water damage."
- REMOVE-SENTENCE `/floors/` — "See water damaged floors." — blk21 p segs — from: "Tile that's still bonded can usually stay while the slab and grout dry. Vinyl plank and laminate often have to be lifted, because they hold water against the concrete. See water damaged floors."

### `/areas/`

- DELINK `/how-it-works/` — anchor "How it works" — blk29 p segs — in: "Who we are and how a job runs: About us · How it works · Commercial properties"

### `/bonita-springs/`

- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk10 ul items[2] — from: "Coastal condos. Condos near Bonita Beach mean leaks between units. See condo water damage."
- DELINK `/condo-leak/` — anchor "Condo water damage" — blk12 table rows[1][2] — in: "Condo water damage"
- REMOVE-SENTENCE `/flood-cleanup/` — "See flood and storm cleanup." — blk10 ul items[0] — from: "The Imperial River. It runs through the middle of Bonita Springs, fed by creeks and canals such as Leitner Creek and the Kehl Canal, and can rise into nearby yards, garages and homes. River water is floodwater, Category 3. See flood and storm cleanup."
- DELINK `/flood-cleanup/` — anchor "storm cleanup" — blk12 table rows[0][2] — in: "Flood and storm cleanup"
- DELINK `/vacant-home/` — anchor "Water damage in vacant homes" — blk12 table rows[2][2] — in: "Water damage in vacant homes"

### `/burst-pipe/`

- REMOVE-SENTENCE `/ceiling-leak/` — "See ceiling leak water damage." — blk38 faq items[7].a — from: "Yes. A split attic line soaks insulation and ceiling drywall, which can sag or fall. Turn off power to that room and stay out from under a bulging ceiling. See ceiling leak water damage."
- REMOVE-SENTENCE `/slab-leak/` — "See slab leak water damage." — blk10 ul items[8] — from: "Lines under the slab. A break below the floor is a slab leak. See slab leak water damage."
- REMOVE-SENTENCE `/vacant-home/` — "See water damage in vacant homes." — blk36 ul items[5] — from: "Turn off the main water when you leave for more than a few days. See water damage in vacant homes."
- REMOVE-SENTENCE `/water-removal/` — "See emergency water removal." — blk27 steps items[1].body — from: "Standing water and water held in carpet are removed. See emergency water removal."

### `/cabinets/`

- DELINK `/appliance-leak/` — anchor "appliance leak water damage" — blk11 p segs — in: "For dishwasher, fridge and washer leaks, see appliance leak water damage."
- REMOVE-SENTENCE `/floors/` — "See water damaged floors." — blk21 p segs — from: "How the flooring meets the cabinets changes the size of the repair. Tile laid before the cabinets went in usually runs under them, so it can stay while the cabinets are dried, but replacing that tile can mean pulling cabinets. Vinyl plank is normally installed up to the cabinets, not under them, so it can usually be lifted without touching the cabinets, though water can still be trapped under the cabinet bases. See water damaged floors."

### `/cape-coral/`

- DELINK `/cast-iron-pipe/` — anchor "Cast iron pipe water damage" — blk15 table rows[1][2] — in: "Cast iron pipe water damage"
- REMOVE-SENTENCE `/cast-iron-pipe/` — "See cast iron pipe water damage." — blk24 ul items[0] — from: "Cast iron drains that corrode and crack under the slab, leaking wastewater under floors. Signs include slow drains, sewer smells and damp, cracked tile. See cast iron pipe water damage."
- REMOVE-SENTENCE `/flood-cleanup/` — "See flood and storm cleanup." — blk29 p segs — from: "See flood and storm cleanup."
- DELINK `/slab-leak/` — anchor "Slab leak water damage" — blk15 table rows[0][2] — in: "Slab leak water damage"
- REMOVE-SENTENCE `/slab-leak/` — "See slab leak water damage." — blk24 ul items[1] — from: "Older copper supply lines that develop pinholes, causing slab leaks and wet walls. See slab leak water damage."

### `/cast-iron-pipe/`

- REMOVE-SENTENCE `/insurance/` — "See what a limited water damage endorsement does." — blk41 p segs — from: "Older homes are the ones most likely to carry a limited water damage endorsement, and cast iron claims are where it matters most, because reaching the pipe often means opening tile and slab. Some endorsements cap water damage and tear-out together at a fixed amount; others cap the water damage but say nothing about tear-out. Before demolition starts, ask your agent or adjuster which wording your policy has, and keep a copy of the endorsement in your claim file. See what a limited water damage endorsement does."
- REMOVE-SENTENCE `/sewage-cleanup/` — "For more on wastewater cleanup, see sewage backup cleanup." — blk33 p segs — from: "For more on wastewater cleanup, see sewage backup cleanup."

### `/ceiling-leak/`

- DELINK `/ac-leak/` — anchor "read AC leak water damage" — blk17 p segs — in: "If your AC is in the attic and the stain is near it, read AC leak water damage. In a condo, see condo water damage."
- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage." — blk48 ul items[0] — from: "Have the AC condensate line cleared at every service and the float switch tested. See AC leak water damage."
- REMOVE-SENTENCE `/condo-leak/` — "In a condo, see condo water damage." — blk17 p segs — from: "If your AC is in the attic and the stain is near it, read AC leak water damage. In a condo, see condo water damage."
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk42 p segs — from: "See condo water damage."

### `/commercial/`

- REMOVE-SENTENCE `/drying/` — "See structural drying." — blk12 steps items[4].body — from: "Commercial dehumidifiers and air movers run with readings logged daily. See structural drying."
- REMOVE-SENTENCE `/sewage-cleanup/` — "See sewage backup cleanup." — blk18 p segs — from: "See sewage backup cleanup."
- DELINK `/water-removal/` — anchor "emergency water removal" — blk12 steps items[1].body — in: "See emergency water removal."

### `/condo-leak/`

- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage." — blk17 ul items[0] — from: "AC condensate overflows from a clogged drain line or failed condensate pump in an interior closet. See AC leak water damage."
- REMOVE-SENTENCE `/ceiling-leak/` — "See ceiling leak water damage." — blk37 steps items[2].body — from: "Sagging ceiling drywall, soaked insulation and swollen cabinet bases are removed and photographed. See ceiling leak water damage."

### `/contact/`

- DELINK `/bonita-springs/` — anchor "Bonita Springs" — blk20 faq items[1].a — in: "Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs are covered. If you're nearby and not sure, call and ask."
- DELINK `/cape-coral/` — anchor "Cape Coral" — blk20 faq items[1].a — in: "Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs are covered. If you're nearby and not sure, call and ask."
- DELINK `/estero/` — anchor "Estero" — blk20 faq items[1].a — in: "Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs are covered. If you're nearby and not sure, call and ask."
- DELINK `/fort-myers-beach/` — anchor "Fort Myers Beach" — blk20 faq items[1].a — in: "Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs are covered. If you're nearby and not sure, call and ask."
- DELINK `/how-it-works/` — anchor "How it works" — blk21 p segs — in: "Who we are: about Fort Myers Water Damage Restoration Pros · How it works"
- DELINK `/lehigh-acres/` — anchor "Lehigh Acres" — blk20 faq items[1].a — in: "Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs are covered. If you're nearby and not sure, call and ask."
- DELINK `/north-fort-myers/` — anchor "North Fort Myers" — blk20 faq items[1].a — in: "Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs are covered. If you're nearby and not sure, call and ask."

### `/cost/`

- REMOVE-SENTENCE `/cast-iron-pipe/` — "See cast iron pipe water damage." — blk27 steps-numbered items[3] — from: "Cast iron drain failure under a 1970s slab home. Sewage cleanup in the bathroom and hallway often lands around $7,000 to $20,000 or more, before the plumbing repair, the trench through the slab and new flooring. See cast iron pipe water damage."
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk60 faq items[3].a — from: "Often, yes. South Florida cost guides put condo and high-rise losses about 20% to 40% higher than a house with the same damage, because water reaches more than one unit and building access, elevators and work hours add time. See condo water damage."
- REMOVE-SENTENCE `/first-hour-checklist/` — "Use the first-hour checklist." — blk43 p segs — from: "In Fort Myers heat and humidity, each step can come sooner. Use the first-hour checklist."
- REMOVE-SENTENCE `/insurance/` — "Read how insurance handles water damage in Florida." — blk49 p segs — from: "Read how insurance handles water damage in Florida."
- REMOVE-SENTENCE `/vacant-home/` — "See water damage in vacant homes." — blk27 steps-numbered items[4] — from: "Supply line that ran for three weeks in an empty seasonal home. Several rooms, wet walls and often mold, which frequently puts drying in the $8,000 to $15,000 range, with mold removal and rebuilding on top. See water damage in vacant homes."

### `/drying/`

- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage." — blk55 ul items[0] — from: "AC condensate overflows that soak ceilings, insulation and closet walls. See AC leak water damage."
- REMOVE-SENTENCE `/ceiling-leak/` — "See ceiling leak water damage." — blk55 ul items[1] — from: "Ceiling leaks where wet insulation keeps the drywall wet from above. See ceiling leak water damage."
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk55 ul items[2] — from: "Condo leaks that cross into the unit below and need drying in two homes at once. See condo water damage."
- REMOVE-SENTENCE `/vacant-home/` — "See water damage in vacant homes." — blk55 ul items[4] — from: "Homes left empty for the season. See water damage in vacant homes."
- DELINK `/water-removal/` — anchor "Drying starts after emergency water removal" — blk5 ul items[3] — in: "Drying starts after emergency water removal and ends before repairs begin."
- DELINK `/water-removal/` — anchor "Standing water is extracted first through emergency water removal" — blk11 steps items[1].body — in: "Wet carpet pad, soaked insulation, swollen particle board and anything touched by sewage come out. Standing water is extracted first through emergency water removal."

### `/estero/`

- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage." — blk10 ul items[2] — from: "AC closets. Air handlers in interior closets are common. See AC leak water damage."
- DELINK `/ac-leak/` — anchor "AC leak water damage" — blk12 table rows[1][2] — in: "AC leak water damage"
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk10 ul items[0] — from: "Condos and attached homes. A failed water heater, AC drain or washer in one unit can reach the unit below or next door. See condo water damage."
- DELINK `/condo-leak/` — anchor "Condo water damage" — blk12 table rows[0][2] — in: "Condo water damage"
- DELINK `/flood-cleanup/` — anchor "storm cleanup" — blk12 table rows[5][2] — in: "Flood and storm cleanup"
- DELINK `/vacant-home/` — anchor "Water damage in vacant homes" — blk12 table rows[2][2] — in: "Water damage in vacant homes"

### `/first-hour-checklist/`

- DELINK `/condo-leak/` — anchor "Condo water damage" — blk15 table rows[5][2] — in: "Condo water damage"
- DELINK `/drying/` — anchor "structural drying" — blk23 p segs — in: "Fort Myers homes are mostly built on concrete slabs, and the air stays humid most of the year. Water spreads sideways under flooring and stays trapped, which is why fast extraction and structural drying matter more here than in drier climates."
- REMOVE-SENTENCE `/water-removal/` — "See emergency water removal." — blk13 ul items[0] — from: "Call for water removal and drying. Standing water and hidden moisture in walls, under tile and in the slab need commercial equipment and moisture readings. See emergency water removal."

### `/flood-cleanup/`

- REMOVE-SENTENCE `/drying/` — "See structural drying." — blk17 steps items[5].body — from: "Dehumidifiers and air movers run until framing and slab read dry. See structural drying."
- DELINK `/sewage-cleanup/` — anchor "sewage backup cleanup" — blk12 p segs — in: "If the water came up through your drains rather than in from outside, see sewage backup cleanup."
- REMOVE-SENTENCE `/sewage-cleanup/` — "See sewage backup cleanup." — blk29 ul items[2] — from: "Drains backing up. If toilets and tubs gurgle or back up after the water goes down, the septic system or sewer line may be overloaded. See sewage backup cleanup."

### `/floors/`

- REMOVE-SENTENCE `/slab-leak/` — "See slab leak water damage." — blk12 p segs — from: "Concrete is porous. When water gets under flooring, the slab soaks it up and releases it slowly. Vinyl plank, laminate and many underlayments act like a lid, so the slab can't breathe and stays wet for weeks. That's why lifting the flooring is often the fastest way to dry the house, even when the planks look fine. Under-slab leaks are a different problem, because the water comes from below. See slab leak water damage."

### `/fort-myers-beach/`

- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk10 ul items[3] — from: "Condos. Mid-rise and high-rise buildings mean a leak can travel to several units below. See condo water damage."
- DELINK `/condo-leak/` — anchor "Condo water damage" — blk12 table rows[3][2] — in: "Condo water damage"
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk24 p segs — from: "In island condos, a leak in one unit can reach several floors below. Florida Statute 718.111(11) generally puts the building and common elements on the association's policy and the finishes inside each unit on the owner's HO-6. Ask the association how the building's flood policy treats ground-level areas, and report every leak to management right away. See condo water damage."
- REMOVE-SENTENCE `/flood-cleanup/` — "See flood and storm cleanup." — blk10 ul items[0] — from: "Storm surge. Estero Island sits low between the Gulf and Estero Bay, so water can come from the beach side and the back bay. Porous materials surge touches usually have to go. See flood and storm cleanup."
- DELINK `/flood-cleanup/` — anchor "storm cleanup" — blk12 table rows[0][2] — in: "Flood and storm cleanup"
- REMOVE-SENTENCE `/sewage-cleanup/` — "See sewage backup cleanup." — blk39 faq items[4].a — from: "Lee County runs the public sewer, so a backup in the main line goes to Lee County Utilities. Drain lines inside your home are yours. Either way, sewage inside is Category 3 and needs cleanup. See sewage backup cleanup."

### `/how-it-works/`

- REMOVE-SENTENCE `/first-hour-checklist/` — "The full list: first-hour water damage checklist." — blk5 p items[1].parts[1] — from: "The full list: first-hour water damage checklist."
- REMOVE-SENTENCE `/water-removal/` — "See emergency water removal." — blk5 p items[4].parts[0] — from: "Standing water is pulled out with truck-mounted or portable extractors. Extraction removes far more water than drying ever could, which shortens drying and limits damage. See emergency water removal."

### `/insurance/`

- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage." — blk58 faq items[1].a — from: "Often for sudden overflows that damage ceilings, walls and floors. The AC repair itself usually isn't covered, and leaks that ran for weeks may be excluded. See AC leak water damage."
- REMOVE-SENTENCE `/burst-pipe/` — "See burst pipe water damage." — blk58 faq items[0].a — from: "Usually yes for the water damage the burst causes, such as wet drywall, flooring and cabinets. Repairing the pipe itself may not be covered. See burst pipe water damage."
- DELINK `/cast-iron-pipe/` — anchor "cast iron pipe water damage" — blk54 p segs — in: "Many Florida insurers ask for a four-point inspection on older homes, covering the roof, electrical, plumbing and HVAC. Older plumbing, like polybutylene supply lines or cast iron drains, can make coverage harder to get or lead to exclusions. Replacing it can help with insurability and lowers the risk of the next leak. See cast iron pipe water damage and slab leak water damage."
- REMOVE-SENTENCE `/first-hour-checklist/` — "Use the first-hour water damage checklist." — blk48 ul items[0] — from: "Stop the water and make it safe. Use the first-hour water damage checklist."
- REMOVE-SENTENCE `/slab-leak/` — "See slab leak water damage." — blk58 faq items[2].a — from: "The resulting damage to floors, walls and cabinets often is, when the leak was sudden. The pipe repair may not be, though some policies pay to break out the slab to reach it. See slab leak water damage."

### `/lehigh-acres/`

- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage." — blk10 ul items[5] — from: "AC that rarely rests. Inland Lehigh Acres runs hot, and clogged condensate lines are a top cause of indoor water damage. See AC leak water damage."
- DELINK `/ac-leak/` — anchor "AC leak water damage" — blk16 table rows[0][2] — in: "AC leak water damage"
- DELINK `/burst-pipe/` — anchor "Burst pipe water damage" — blk16 table rows[1][2] — in: "Burst pipe water damage"
- REMOVE-SENTENCE `/flood-cleanup/` — "See flood and storm cleanup." — blk22 p segs — from: "See flood and storm cleanup."
- REMOVE-SENTENCE `/sewage-cleanup/` — "See sewage backup cleanup." — blk35 faq items[3].a — from: "Stop using water, keep people and pets away from the overflow and photograph it. Don't have the tank pumped while the ground is still flooded. Call a septic company, and treat anything the backup touched as sewage. See sewage backup cleanup."
- DELINK `/water-removal/` — anchor "emergency water removal" — blk26 steps items[1].body — in: "See emergency water removal."

### `/mobile-home/`

- REMOVE-SENTENCE `/burst-pipe/` — "See burst pipe water damage." — blk30 ul items[0] — from: "Sudden leaks, such as a burst supply line or a failed water heater, are often covered for the resulting damage. See burst pipe water damage."
- REMOVE-SENTENCE `/flood-cleanup/` — "See flood and storm cleanup." — blk27 p segs — from: "See flood and storm cleanup."
- DELINK `/north-fort-myers/` — anchor "mobile homes in North Fort Myers" — blk39 faq items[9].a — in: "Yes. Call 239-356-3708, answered 24/7, for manufactured and mobile homes in North Fort Myers, Fort Myers, Pine Island, Lehigh Acres, Cape Coral, Estero and Bonita Springs."

### `/north-fort-myers/`

- DELINK `/areas/` — anchor "all service areas" — blk39 faq items[6].a — in: "Yes. See water damage restoration in Cape Coral, Fort Myers and all service areas."
- REMOVE-SENTENCE `/mobile-home/` — "See mobile home water damage." — blk10 ul items[0] — from: "Manufactured homes. Particle board or OSB decking, insulation in the floor system and a belly wrap underneath. Water soaks into the floor and gets trapped in the belly. See mobile home water damage."
- DELINK `/mobile-home/` — anchor "Mobile home water damage" — blk12 table rows[0][2] — in: "Mobile home water damage"
- REMOVE-SENTENCE `/mobile-home/` — "See mobile home water damage." — blk23 p segs — from: "Drying usually means opening the belly, removing wet insulation and replacing damaged decking, not just running fans inside. See mobile home water damage."
- DELINK `/water-heater-leak/` — anchor "Water heater leak cleanup" — blk12 table rows[1][2] — in: "Water heater leak cleanup"

### `/sewage-cleanup/`

- REMOVE-SENTENCE `/cast-iron-pipe/` — "See cast iron pipe water damage." — blk15 ul items[1] — from: "Cast iron drains. Many homes built before about 1975 have cast iron drain lines that corrode, scale and crack under the slab. See cast iron pipe water damage."
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk34 p segs — from: "In condo buildings, a blockage in a shared drain stack can push sewage into lower units, often the ground floor. Report it to building management immediately so everyone stops using water. Who pays depends on where the blockage was and your condo documents: a shared line is often the association's responsibility, while a line serving only your unit is often yours. See condo water damage."
- DELINK `/lehigh-acres/` — anchor "Lehigh Acres" — blk46 faq items[12].a — in: "Call 239-356-3708. The line is answered 24/7 for sewage backups in Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs."
- DELINK `/north-fort-myers/` — anchor "North Fort Myers" — blk46 faq items[12].a — in: "Call 239-356-3708. The line is answered 24/7 for sewage backups in Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero and Bonita Springs."

### `/slab-leak/`

- DELINK `/burst-pipe/` — anchor "burst pipe water damage" — blk14 p segs — in: "Not every leak under the slab is a supply line. A cracked drain line carries wastewater instead; see cast iron pipe water damage. A leak you can see above the floor is a different job; see burst pipe water damage."
- DELINK `/cape-coral/` — anchor "Cape Coral" — blk39 faq items[9].a — in: "After the plumber repairs the line, call 239-356-3708, answered 24/7, to dry the slab, walls and flooring in Fort Myers, Cape Coral, Lehigh Acres, Estero and Bonita Springs."
- DELINK `/floors/` — anchor "water damaged floors" — blk23 p segs — in: "More detail: water damaged floors and water damaged kitchen cabinets."
- DELINK `/lehigh-acres/` — anchor "Lehigh Acres" — blk39 faq items[9].a — in: "After the plumber repairs the line, call 239-356-3708, answered 24/7, to dry the slab, walls and flooring in Fort Myers, Cape Coral, Lehigh Acres, Estero and Bonita Springs."

### `/terms/`

- DELINK `/disclaimer/` — anchor "Disclaimer" — blk31 p segs — in: "Related pages: Privacy Policy · Disclaimer · Contact"
- DELINK `/privacy-policy/` — anchor "Privacy Policy" — blk31 p segs — in: "Related pages: Privacy Policy · Disclaimer · Contact"

### `/vacant-home/`

- REMOVE-SENTENCE `/ac-leak/` — "See AC leak water damage." — blk11 ul items[1] — from: "AC condensate overflow. The AC keeps running but the drain line clogs, and water spills into the closet, ceiling or floor for weeks. See AC leak water damage."
- REMOVE-SENTENCE `/condo-leak/` — "See condo water damage." — blk11 ul items[6] — from: "Leaks from the unit above in condos, where your neighbor may also be away. See condo water damage."

### `/water-heater-leak/`

- REMOVE-SENTENCE `/water-removal/` — "See emergency water removal." — blk21 steps items[1].body — from: "Standing water is extracted from the slab, carpet and closet floor. See emergency water removal."

### `/water-removal/`

- REMOVE-SENTENCE `/condo-leak/` — "Read more about condo water damage." — blk49 p segs — from: "Upper-floor units usually need portable equipment, and the water may already be in the unit below. Tell building management right away so a shared riser or the unit above can be shut off, and photograph both units. Read more about condo water damage."
- DELINK `/drying/` — anchor "Structural drying" — blk5 ul items[0] — in: "Extraction removes the liquid water. Structural drying removes the water that has already soaked into drywall, slab, baseboards and cabinets."
- DELINK `/drying/` — anchor "From here the job becomes structural drying" — blk16 steps items[4].body — in: "Dehumidifiers and air movers are placed and the first moisture readings are logged. From here the job becomes structural drying, which runs until the materials reach normal dry readings."
- REMOVE-SENTENCE `/drying/` — "Learn how water mitigation and structural drying work." — blk67 faq items[2].a — from: "Water removal is the first part of mitigation. Mitigation is the whole job of stopping further damage: extracting water, removing what can't be saved and drying the structure. Learn how water mitigation and structural drying work."
- DELINK `/flood-cleanup/` — anchor "storm cleanup" — blk42 table rows[7][3] — in: "Flood and storm cleanup"
- REMOVE-SENTENCE `/flood-cleanup/` — "See flood and storm cleanup." — blk59 p segs — from: "See flood and storm cleanup."
- DELINK `/sewage-cleanup/` — anchor "Sewage backup cleanup" — blk42 table rows[5][3] — in: "Sewage backup cleanup"

## 4. Kept occurrences where the card wins over an earlier body occurrence

These are the cases where the kept link is NOT the first occurrence in document order (card priority, §1).
All other kept occurrences are the first occurrence in document order (body-only targets) or the sole
card occurrence.

- `/` `/ac-leak/` — kept #15 [CARD] kinds items[0].body; first was #4 [CARD] ul items[4] (de-linked/removed).
- `/` `/appliance-leak/` — kept #22 [CARD] kinds items[7].body; first was #7 [CARD] ul items[4] (de-linked/removed).
- `/` `/burst-pipe/` — kept #20 [CARD] kinds items[5].body; first was #5 [CARD] ul items[4] (de-linked/removed).
- `/` `/condo-leak/` — kept #17 [CARD] kinds items[2].body; first was #9 [CARD] ul items[5] (de-linked/removed).
- `/` `/flood-cleanup/` — kept #26 [CARD] kinds items[11].body; first was #3 [CARD] ul items[3] (de-linked/removed).
- `/` `/mobile-home/` — kept #25 [CARD] kinds items[10].body; first was #10 [CARD] ul items[5] (de-linked/removed).
- `/` `/sewage-cleanup/` — kept #18 [CARD] kinds items[3].body; first was #2 [CARD] ul items[2] (de-linked/removed).
- `/` `/slab-leak/` — kept #23 [CARD] kinds items[8].body; first was #8 [CARD] ul items[4] (de-linked/removed).
- `/` `/water-heater-leak/` — kept #21 [CARD] kinds items[6].body; first was #6 [CARD] ul items[4] (de-linked/removed).
- `/ac-leak/` `/ceiling-leak/` — kept #14 [CARD] ul items[0]; first was #0 [BODY] ul items[3] (de-linked/removed).
- `/ac-leak/` `/drying/` — kept #15 [CARD] ul items[1]; first was #3 [BODY] ul items[2] (de-linked/removed).
- `/appliance-leak/` `/cabinets/` — kept #18 [CARD] ul items[0]; first was #5 [BODY] ul items[2] (de-linked/removed).
- `/appliance-leak/` `/floors/` — kept #19 [CARD] ul items[1]; first was #8 [BODY] p segs (de-linked/removed).
- `/bonita-springs/` `/condo-leak/` — kept #18 [CARD] ul items[1]; first was #2 [BODY] ul items[2] (de-linked/removed).
- `/bonita-springs/` `/flood-cleanup/` — kept #17 [CARD] ul items[0]; first was #1 [BODY] ul items[0] (de-linked/removed).
- `/burst-pipe/` `/slab-leak/` — kept #21 [CARD] ul items[1]; first was #4 [BODY] ul items[8] (de-linked/removed).
- `/burst-pipe/` `/water-removal/` — kept #20 [CARD] ul items[0]; first was #8 [BODY] steps items[1].body (de-linked/removed).
- `/cabinets/` `/appliance-leak/` — kept #14 [CARD] ul items[0]; first was #1 [BODY] p segs (de-linked/removed).
- `/cabinets/` `/floors/` — kept #15 [CARD] ul items[1]; first was #3 [BODY] p segs (de-linked/removed).
- `/cape-coral/` `/cast-iron-pipe/` — kept #21 [CARD] ul items[1]; first was #2 [BODY] table rows[1][2] (de-linked/removed).
- `/cape-coral/` `/slab-leak/` — kept #20 [CARD] ul items[0]; first was #1 [BODY] table rows[0][2] (de-linked/removed).
- `/cast-iron-pipe/` `/sewage-cleanup/` — kept #11 [CARD] ul items[0]; first was #2 [BODY] p segs (de-linked/removed).
- `/ceiling-leak/` `/ac-leak/` — kept #16 [CARD] ul items[0]; first was #1 [BODY] p segs (de-linked/removed).
- `/ceiling-leak/` `/condo-leak/` — kept #17 [CARD] ul items[1]; first was #2 [BODY] p segs (de-linked/removed).
- `/commercial/` `/drying/` — kept #19 [CARD] ul items[1]; first was #3 [BODY] steps items[4].body (de-linked/removed).
- `/commercial/` `/water-removal/` — kept #18 [CARD] ul items[0]; first was #1 [BODY] steps items[1].body (de-linked/removed).
- `/condo-leak/` `/ac-leak/` — kept #16 [CARD] ul items[1]; first was #1 [BODY] ul items[0] (de-linked/removed).
- `/condo-leak/` `/ceiling-leak/` — kept #15 [CARD] ul items[0]; first was #6 [BODY] steps items[2].body (de-linked/removed).
- `/cost/` `/first-hour-checklist/` — kept #18 [CARD] ul items[1]; first was #10 [BODY] p segs (de-linked/removed).
- `/cost/` `/insurance/` — kept #17 [CARD] ul items[0]; first was #11 [BODY] p segs (de-linked/removed).
- `/drying/` `/ac-leak/` — kept #21 [CARD] ul items[1]; first was #9 [BODY] ul items[0] (de-linked/removed).
- `/drying/` `/water-removal/` — kept #20 [CARD] ul items[0]; first was #0 [BODY] ul items[3] (de-linked/removed).
- `/estero/` `/ac-leak/` — kept #18 [CARD] ul items[1]; first was #3 [BODY] ul items[2] (de-linked/removed).
- `/estero/` `/condo-leak/` — kept #17 [CARD] ul items[0]; first was #1 [BODY] ul items[0] (de-linked/removed).
- `/first-hour-checklist/` `/drying/` — kept #24 [CARD] ul items[1]; first was #13 [BODY] p segs (de-linked/removed).
- `/first-hour-checklist/` `/water-removal/` — kept #23 [CARD] ul items[0]; first was #0 [BODY] ul items[0] (de-linked/removed).
- `/flood-cleanup/` `/drying/` — kept #17 [CARD] ul items[1]; first was #3 [BODY] steps items[5].body (de-linked/removed).
- `/flood-cleanup/` `/sewage-cleanup/` — kept #16 [CARD] ul items[0]; first was #1 [BODY] p segs (de-linked/removed).
- `/floors/` `/slab-leak/` — kept #13 [CARD] ul items[1]; first was #1 [BODY] p segs (de-linked/removed).
- `/fort-myers-beach/` `/condo-leak/` — kept #19 [CARD] ul items[1]; first was #2 [BODY] ul items[3] (de-linked/removed).
- `/fort-myers-beach/` `/flood-cleanup/` — kept #18 [CARD] ul items[0]; first was #1 [BODY] ul items[0] (de-linked/removed).
- `/how-it-works/` `/first-hour-checklist/` — kept #8 [CARD] ul items[0]; first was #0 [BODY] p items[1].parts[1] (de-linked/removed).
- `/how-it-works/` `/water-removal/` — kept #9 [CARD] ul items[1]; first was #2 [BODY] p items[4].parts[0] (de-linked/removed).
- `/insurance/` `/first-hour-checklist/` — kept #16 [CARD] ul items[1]; first was #6 [BODY] ul items[0] (de-linked/removed).
- `/lehigh-acres/` `/ac-leak/` — kept #20 [CARD] ul items[0]; first was #1 [BODY] ul items[5] (de-linked/removed).
- `/lehigh-acres/` `/burst-pipe/` — kept #21 [CARD] ul items[1]; first was #3 [BODY] table rows[1][2] (de-linked/removed).
- `/mobile-home/` `/burst-pipe/` — kept #17 [CARD] ul items[1]; first was #7 [BODY] ul items[0] (de-linked/removed).
- `/north-fort-myers/` `/mobile-home/` — kept #19 [CARD] ul items[0]; first was #1 [BODY] ul items[0] (de-linked/removed).
- `/north-fort-myers/` `/water-heater-leak/` — kept #20 [CARD] ul items[1]; first was #5 [BODY] table rows[1][2] (de-linked/removed).
- `/sewage-cleanup/` `/cast-iron-pipe/` — kept #15 [CARD] ul items[0]; first was #1 [BODY] ul items[1] (de-linked/removed).
- `/sewage-cleanup/` `/condo-leak/` — kept #16 [CARD] ul items[1]; first was #6 [BODY] p segs (de-linked/removed).
- `/slab-leak/` `/burst-pipe/` — kept #15 [CARD] ul items[1]; first was #2 [BODY] p segs (de-linked/removed).
- `/slab-leak/` `/floors/` — kept #14 [CARD] ul items[0]; first was #3 [BODY] p segs (de-linked/removed).
- `/vacant-home/` `/ac-leak/` — kept #15 [CARD] ul items[0]; first was #1 [BODY] ul items[1] (de-linked/removed).
- `/vacant-home/` `/condo-leak/` — kept #16 [CARD] ul items[1]; first was #5 [BODY] ul items[6] (de-linked/removed).
- `/water-heater-leak/` `/water-removal/` — kept #13 [CARD] ul items[0]; first was #4 [BODY] steps items[1].body (de-linked/removed).
- `/water-removal/` `/drying/` — kept #25 [CARD] ul items[0]; first was #0 [BODY] ul items[0] (de-linked/removed).
- `/water-removal/` `/sewage-cleanup/` — kept #26 [CARD] ul items[1]; first was #10 [BODY] table rows[5][3] (de-linked/removed).

## 5. Owner-named sentences (his explicit order)

- (a) Homepage paragraph "See condo water damage for the full walkthrough." — whole block removed
  (`site/data/homepage.php`, block 61). The /condo-leak/ link survives in the kinds card ("See condo
  water damage.") and nowhere else on the homepage.
- (b) Homepage "Businesses. … See commercial water damage." bullet (Vacation Rentals section, block 64,
  item 0) — the "See commercial water damage." sentence removed; the bullet now ends "…parts of the space
  can stay open where it is safe." The /commercial/ link survives in the help card ("businesses") and
  nowhere else on the homepage.

## 6. Verification (on the re-exported `out/`)

- Link audit re-run on the new export: **all 34 pages, every target exactly 1** (total == unique per page;
  522 links in `<main>` vs 659 before). Zero duplicate targets remain.
- Related: **27/27 lists exactly 3 items**; homepage anchors **27 distinct**; exactly one `/` link in
  `<main>` on all 27 Related pages.
- H1 = 1 on all 34 pages. 0 em/en dashes (literal + entities) in served text. 0 self-links in `<main>`.
- No empty `<p>` / `<li>` / `<td>` left in `<main>` by the removals.
- Word-diff vs the pre-dedup export (punctuation-normalised, so de-linking scores 0): **377 words removed
  on 29 pages, reconciled exactly** — 73 removed sentence occurrences (72 REMOVE-SENTENCE + 1 REMOVE-BLOCK);
  every other page 0. No other word changed anywhere. (Naive word-splitting overcounts by ~100 because a
  de-linked anchor's trailing "." / "," was its own segment and re-joins the preceding word — the words
  are all still there; the normalised diff is the true one.)
- Overflow: **0 on all 34 routes at 390px and 1440px** (Playwright bundled Chromium probe on the static export).
- `php -l` clean on all 31 edited files (and all data files).
- Spot checks on the render: commercial + Lehigh Acres "Water extraction" steps still read "See emergency
  water removal." as plain text with the live link only in Related; contact table keeps all 6 area links
  with FAQ area names plain; terms "Related pages: Privacy Policy · Disclaimer · Contact" (Contact still
  linked); ceiling-leak paragraph now ends "…read AC leak water damage." as plain text with the condo
  pointer sentence gone; homepage kinds "See X." links all present (12 checked targets exactly 1 link each).

## 7. Method + safety notes

- Read-only inventory first: PHP walker (`/tmp/dedup_walk.php`) listed every internal href in render order
  with block context; its counts reproduced the coordinator's audit table EXACTLY on all 34 pages (homepage
  53 in data + 1 hardcoded hero `/contact/` CTA = 54). Decisions were computed from that inventory
  (`/tmp/dedup_decide.py` → `/tmp/dedup_decisions.json`), then applied by a source-surgery script
  (`/tmp/dedup_edit.py`, 263 line operations) — first on a copy of `site/data/` (`/tmp/dedup-data-test`,
  full diff reviewed, `php -l` clean), then on the live files; live files verified byte-identical to the
  reviewed test copy. Backup of pre-dedup data at `/tmp/dedup-data-backup`; pre-dedup export snapshot at
  `/tmp/dedup-pre-out`.
- `qa/verify_export.py` was NEVER run (it regenerates all data files from the pastes and would wipe this
  work — see FINDINGS-hero-images.md §4c). Verification used read-only checks only: re-export, link audit,
  word-diff, `php -l`, Playwright overflow probe.
- Files edited (31): `site/data/homepage.php`, `ac-leak`, `appliance-leak`, `areas`, `bonita-springs`,
  `burst-pipe`, `cabinets`, `cape-coral`, `cast-iron-pipe`, `ceiling-leak`, `commercial`, `condo-leak`,
  `contact`, `cost`, `drying`, `estero`, `first-hour-checklist`, `flood-cleanup`, `floors`,
  `fort-myers-beach`, `how-it-works`, `insurance`, `lehigh-acres`, `mobile-home`, `north-fort-myers`,
  `sewage-cleanup`, `slab-leak`, `terms`, `vacant-home`, `water-heater-leak`, `water-removal`.
  Untouched: `about`, `disclaimer`, `privacy-policy` (already clean), `pages.php`, `functions.php`,
  `header.php`, `styles.css`, all images/manifests. No commit, no push, no deploy.
