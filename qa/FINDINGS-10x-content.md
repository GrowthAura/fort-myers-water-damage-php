# 10X CONTENT — Fort Myers PHP Site (Worker 2: CONTENT)

- **Project:** `~/workspace/fort-myers-php/` — 10X improvement round, LOCAL ONLY
- **Date:** 2026-11-19 ~23:05–23:20 PKT
- **Scope:** `site/data/*.php` EXCEPT `site/data/about.php` (Worker 3) and EXCEPT `site/data/media-manifest.php` (Worker 3). No `site/includes/*`, no `site/assets/*`, no `out/`, no git, no push/deploy/DNS. `qa/verify_export.py` NEVER run.
- **Baseline:** 20X audit (`qa/FINDINGS-20x-testing.md`, 2026-11-19 ~22:21–23:00 PKT) — word-diff 0 unauthorized on all 34 pages. This round's changes are the ONLY deltas from that baseline: 27 asserted replacements (each old string occurred exactly once in its file before replacement), applied by `/tmp/apply_10x_content.py`, verified by `/tmp/verify_10x_content.py` against my own PHP server on port 8134 (`php -S 127.0.0.1:8134 -t site site/index.php`, killed by PID when done).
- **Verification result: 0 FAILURES** (full run: 11/11 pages 200, heading outline, ZIP rows, homepage link audit, per-page duplicate/self-link audit, old-absent/new-present on every changed sentence, dashes 0). `php -l` clean on all 11 changed files.

## Files changed (11)

`site/data/areas.php`, `site/data/homepage.php`, `site/data/bonita-springs.php`, `site/data/cape-coral.php`, `site/data/fort-myers-beach.php`, `site/data/lehigh-acres.php`, `site/data/mobile-home.php`, `site/data/vacant-home.php`, `site/data/water-heater-leak.php`, `site/data/estero.php`, `site/data/north-fort-myers.php`.

## 1. A-2 — /areas/ heading skip (FIXED at outline level, with one structural caveat)

### Changed — 5 `h3` blocks promoted to `h2` in `site/data/areas.php`

| Heading | Old | New |
|---|---|---|
| Table heading | `'type' => 'h3', 'text' => 'Lee County Service Areas and ZIP Codes'` | `'type' => 'h2', 'text' => 'Lee County Service Areas and ZIP Codes'` |
| Area heading | `'type' => 'h3', 'text' => 'Fort Myers'` | `'type' => 'h2', 'text' => 'Fort Myers'` |
| Area heading | `'type' => 'h3', 'text' => 'Sanibel and Captiva'` | `'type' => 'h2', 'text' => 'Sanibel and Captiva'` |
| Area heading | `'type' => 'h3', 'text' => 'Pine Island and Matlacha'` | `'type' => 'h2', 'text' => 'Pine Island and Matlacha'` |
| Area heading | `'type' => 'h3', 'text' => 'San Carlos Park, Gateway and Iona in Lee County'` | `'type' => 'h2', 'text' => 'San Carlos Park, Gateway and Iona in Lee County'` |

No words changed — heading level only.

### Caveat — the other 6 of the 10 area headings stay H3 (NOT a silent skip)

The 10 area headings are split across two block types in `areas.php`. The 5 above are standalone `h3` blocks. The other 6 — Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero, Bonita Springs — are `area-cards` item titles, and `render_block()` in `site/includes/functions.php` (read-only for this worker, NOT edited) hardcodes them as `<h3>` (`'<h3>' . esc($a['title']) . '</h3>'`). There is no data-level way to promote them: the `h2`/`h3` block types take only `text` (no class or level key is read), and restructuring the cards into `h2`+`p` blocks would drop the card grid and its images. Promoting those 6 needs a Worker 1 change in `functions.php` (e.g. render area-card titles as `h2`), or acceptance of the current outline.

The current outline is nevertheless VALID — no level is skipped anywhere, which is what the audit defect was (H1 followed directly by H3s). Rendered outline on `/areas/` (verified live on port 8134):

```
H1 Water Damage Help Across Lee County, FL
H2 Lee County Service Areas and ZIP Codes
H2 Fort Myers
H3 Cape Coral / H3 Lehigh Acres / H3 North Fort Myers / H3 Fort Myers Beach
H2 Sanibel and Captiva
H2 Pine Island and Matlacha
H3 Estero / H3 Bonita Springs
H2 San Carlos Park, Gateway and Iona in Lee County
H2 Who Handles Permits and the 50% Rule in Each Part of Lee County
H2 Water Damage Problems Across Lee County
H2 What to Do First Anywhere in Lee County
H2 What You Can Expect Anywhere in Lee County
H2 Questions About Water Damage Help Across Lee County
H2 Water Damage Anywhere in Lee County?
```

### Visual-size note

The task suggested keeping the H3 look via class if wanted. `render_block()` supports no class on `h2`/`h3` blocks — it renders bare `<h2>text</h2>`. So the 5 promoted headings now render at the H2 size. If the owner wants the H3 look back on them, that is a Worker 1 CSS/includes change, not a data change.

## 2. D-P2-1 — /areas/ ZIP table: 33993 removed from Pine Island (FIXED)

`site/data/areas.php`, Pine Island and Matlacha row:

- Old: `'t' => '33922, 33956, 33993'`
- New: `'t' => '33922, 33956'`

33993 remains exactly once on the page, in its correct row: Cape Coral `'33904, 33909, 33914, 33990, 33991, 33993'` (verified rendered).

**33945 NOT added** (per order — that would be a new fact). Flag for the owner: the audit states Pine Island / Matlacha ZIPs are 33922 (Bokeelia), 33945 (Pineland), 33956 (St. James City / Matlacha). `33945` appears NOWHERE in any paste or data file in this repo (grep 2026-11-19), so adding it would rest entirely on the auditor's word, not on the owner's paste. Owner call: add `33945` to the Pine Island row, or leave the row as `33922, 33956`.

## 3. D-P2-2 — homepage help cards linked (FIXED, with dedup delinks)

`site/data/homepage.php`, "What we help with" help grid:

- Old: `'t' => 'Sewage backup cleanup',` (no href) → New: `'t' => 'Sewage backup cleanup', 'href' => '/sewage-cleanup/'`
- Old: `'t' => 'Flood and '` + `'t' => 'storm cleanup',` (no href) → New: `'t' => 'Flood and storm cleanup', 'href' => '/flood-cleanup/'` (two segments merged into one so the full phrase is the anchor; rendered words identical)
- "Leaks of every kind" UNTOUCHED — still unlinked (no single target; see D-P3-4).

**Dedup (one link per target per page in body copy):** both targets were already linked in the homepage's kinds cards, so the OTHER occurrences were delinked, words unchanged:

- Kinds card "Sewage or a drain backing up": old `'t' => 'sewage backup cleanup', 'href' => '/sewage-cleanup/'` → new `'t' => 'sewage backup cleanup',` (plain text; the card still reads "See sewage backup cleanup.")
- Kinds card "Floodwater or storm surge": old `'t' => 'storm cleanup', 'href' => '/flood-cleanup/'` → new `'t' => 'storm cleanup',` (plain text; the card still reads "See flood and storm cleanup.")

Rendered anchors verified: `Sewage backup cleanup → /sewage-cleanup/`, `Flood and storm cleanup → /flood-cleanup/`, each exactly 1x in `<main>`.

## 4. D-P3-1 — /areas/ ZIP omissions (FIXED)

`site/data/areas.php`:

- Bonita Springs row — Old: `'t' => '34134, 34135'` → New: `'t' => '33923, 34134, 34135'` (ascending order, matching the table's convention)
- Fort Myers Beach row — Old: `'t' => '33931'` → New: `'t' => '33931, 33932'`

Evidence, cited as ordered:

- **33932:** the Fort Myers Beach page's own paste (`pages/fort-myers-beach-paste-2026-11-19.md`): line 53 "33931, with 33932 for post office boxes"; line 109 "Fort Myers Beach is ZIP code 33931, covering Estero Island from the north end near the Matanzas Pass Bridge to the south end near Big Carlos Pass; 33932 is used for post office boxes." Its schema also lists `"postalCode": ["33931", "33932"]` (line 36). Paste-sourced, not invented.
- **33923:** HONEST CAVEAT — `33923` appears NOWHERE in any paste or data file in this repo (grep 2026-11-19; the Bonita Springs paste details card says only "34134 and 34135"). It was added solely on the 20X auditor's verification ("33923 is also Bonita Springs"). The verifier should independently confirm 33923 is a Bonita Springs ZIP before this ships; if it is not, revert that one token to `34134, 34135`.

Full rendered ZIP table verified: Fort Myers `33901, 33905, 33907, 33908, 33912, 33913, 33916, 33919, 33966, 33967`; Cape Coral `33904, 33909, 33914, 33990, 33991, 33993`; Lehigh Acres `33936, 33971, 33972, 33973, 33974, 33976`; North Fort Myers `33903, 33917`; Fort Myers Beach `33931, 33932`; Sanibel and Captiva `33957, 33924`; Pine Island and Matlacha `33922, 33956`; Estero `33928`; Bonita Springs `33923, 34134, 34135`.

## 5. D-P3-7 — repeated boilerplate (AUTHORIZED wording changes)

Every changed sentence is recorded verbatim old → new below, with the word multiset delta (parser-style `words()` — case-sensitive — computed from the replacement pairs). The `See structural drying.` link (`/drying/`) is kept intact in all 7 drying sentences; both sign-off links (`/insurance/` anchor "how insurance handles water damage in Florida", `/cost/` anchor "water damage pricing guide") are kept verbatim in all 3 reworded sign-offs. All localising nouns were verified to occur in that page's OWN paste before use.

### (a) Drying step-5 sentence — localised on all 7 pages

Old (identical on all 7): `Dehumidifiers and air movers run with readings logged daily. See structural drying.`

| Page | New sentence | Word delta (removed → added) |
|---|---|---|
| bonita-springs | `Dehumidifiers and air movers dry the wet condo drywall and carpet, with readings logged daily. See structural drying.` | removed `[run]`; added `[and, dry, the, wet, condo, drywall, carpet]` ("condo", "drywall", "carpet" in its paste) |
| cape-coral | `Dehumidifiers and air movers dry the slab home, with readings logged daily. See structural drying.` | removed `[run]`; added `[dry, the, slab, home]` ("slab homes" in its paste) |
| fort-myers-beach | `Dehumidifiers and air movers dry the wet drywall and flooring in the elevated home, with readings logged daily. See structural drying.` | removed `[run]`; added `[and, dry, the, the, wet, drywall, flooring, in, elevated, home]` ("elevated homes", "drywall", "flooring" in its paste) |
| lehigh-acres | `Dehumidifiers and air movers dry the wet drywall and carpet in the concrete block home, with readings logged daily. See structural drying.` | removed `[run]`; added `[and, dry, the, the, wet, drywall, carpet, in, concrete, block, home]` ("concrete block", "drywall", "carpet" in its paste) |
| mobile-home | `Dehumidifiers and air movers dry the subfloor and belly wrap from above and below, with readings logged daily. See structural drying.` | removed `[run]`; added `[and, and, dry, the, subfloor, belly, wrap, from, above, below]` ("subfloor", "belly wrap" in its paste; "from above and below" is the step's own title, "Dry the floor system from above and below") |
| vacant-home | `Dehumidifiers and air movers dry the wet drywall and flooring in the seasonal home, with readings logged daily. See structural drying.` | removed `[run]`; added `[and, dry, the, the, wet, drywall, flooring, in, seasonal, home]` ("seasonal home", "drywall", "flooring" in its paste) |
| water-heater-leak | `Dehumidifiers and air movers dry the garage and the wet lower drywall, with readings logged daily. See structural drying.` | removed `[run]`; added `[and, dry, the, the, garage, wet, lower, drywall]` ("garage", "drywall" in its paste; "wet lower drywall" is the page's own preceding step text) |

Note: the similar sentences on `/appliance-leak/` ("…run with readings logged daily, then repairs follow. See…") and `/cabinets/` ("…run with readings logged daily, then damaged panels, toe kicks and drywall are replaced. See…") were already varied in the paste and were NOT touched.

### (b) Sign-off paragraph — reworded on 3 of its 6 pages

Old (identical on all 6): `Read how insurance handles water damage in Florida. General pricing information: water damage pricing guide.`

| Page | New paragraph | Word delta |
|---|---|---|
| bonita-springs | `For the claim, read how insurance handles water damage in Florida. For typical costs, see the water damage pricing guide.` | removed `[Read, General, pricing, information]`; added `[For, For, the, the, claim, read, typical, costs, see]` |
| estero | `If a claim is involved, read how insurance handles water damage in Florida. For ballpark costs, see the water damage pricing guide.` | removed `[Read, General, pricing, information]`; added `[If, a, claim, is, involved, read, For, ballpark, costs, see, the]` |
| north-fort-myers | `Questions about a claim? Read how insurance handles water damage in Florida. Wondering what it costs? See the water damage pricing guide.` | removed `[General, pricing, information]`; added `[Questions, about, a, claim, Wondering, what, it, costs, See, the]` |

UNCHANGED (identical original kept): commercial, floors, fort-myers-beach — verified rendered verbatim.

### (c) Well-pump FAQ answer — LEFT AS-IS (per order)

Identical answer on `/cape-coral/` and `/lehigh-acres/` — `Turn off the well pump at its breaker and close the main valve near the pressure tank. That stops the pump from pushing more water into a broken line.` — verified still present verbatim on both pages. Same correct advice in both places; no change.

## 6. D-P3-9 — "Every kind of property" card link (CHANGED, with a dedup tradeoff — see below)

`site/data/homepage.php`, help card "Every kind of property: single-family homes, condos, mobile homes, vacation rentals and businesses."

- Old: `'t' => 'businesses', 'href' => '/commercial/'`
- New: `'t' => 'businesses', 'href' => '/areas/'`
- Card words unchanged. Reason (as ordered): the card lists five property types but its single link went to `/commercial/`, so four of the five named types led to a page that is not about them; `/areas/` covers all properties in all areas.

**Dedup tradeoff (flagged for the verifier/owner):** `/areas/` was ALREADY linked once in the homepage body copy — the paragraph "See every city and ZIP code we cover in our Lee County service areas." (line ~2004). Keeping both would create a duplicate body target (the 20X audit's "0 duplicate prose targets" would regress), so that occurrence was delinked to keep exactly one `/areas/` link on the page:

- Old: `'t' => 'ZIP code we cover in our Lee County service areas', 'href' => '/areas/'` → New: `'t' => 'ZIP code we cover in our Lee County service areas',` (words unchanged, plain text now).

Consequence to weigh: the delinked sentence still says "See every city and ZIP code we cover…" but no longer links anywhere, while the word "businesses" now points at the areas hub. If the owner prefers the line-2004 link to stay (it is the natural, specific anchor for `/areas/`), the correct revert is: card back to `'href' => '/commercial/'` on "businesses" (the audit's alternative fix — which was already the pre-round state) and restore the line-2004 `/areas/` link. D-P3-9 would then stand unfixed as a known item, not silently duplicated.

## 7. D-P3-2 — "Seasonal Home" vs "Vacant Home" naming (NO CHANGE — owner decision needed)

NOTHING RENAMED, per order. Facts as found (unchanged from the 20X audit): the page slug is `/vacant-home/`, the H1 is "Water Damage Found After Returning to Your Fort Myers Home", all 20 in-site anchors say "water damage in vacant homes", the kinds card says "Came back to a wet or musty seasonal home" — but the `<title>` is "Seasonal Home Water Damage Fort Myers | Came Back to a Leak?" and og/twitter titles match it. The footer no longer links the page at all, so the mismatch is title-only — but the title is the ranking label.

**Owner decision needed:** (a) retitle to "Vacant Home Water Damage Fort Myers …" to match slug / H1 / anchors, OR (b) keep "Seasonal Home" deliberately and align the H1/anchors to it. Do not change silently — it is a naming decision. (Note: the title lives in `site/data/vacant-home.php` seo, which is inside my file ownership, but the order was explicitly DO NOT rename — so no edit was made.)

## 8. D-P3-4 — Estero/Bonita shared homepage paragraph (NO CHANGE — owner decision needed)

NOTHING SPLIT, per order. Facts as found: one homepage paragraph covers both areas — "Estero and Bonita Springs: condo leaks from the unit above and seasonal homes found wet after time away. See Estero and Bonita Springs." (both links exist, prose shared). The "Leaks of every kind" help card is link-free by design (no single target page exists for it) and was left unlinked (see §3).

**Owner decision needed:** split the Estero/Bonita paragraph into two area-specific lines if he wants it, or keep the shared paragraph; and for the leaks card, leave unlinked or point it at `/water-removal/`. No edit made either way.

## Word-diff vs pastes (summary for the verifier)

The pre-round build was word-diff 0 unauthorized (20X audit). The ONLY deltas introduced by this round are the authorized changes in §§1–6 above. Full accounting (parser-style words, case-sensitive):

- **Headings (§1):** 0 word changes (level only).
- **ZIPs (§2, §4):** removed `[33993]` (Pine Island row); added `[33923]` (Bonita Springs row), `[33932]` (Fort Myers Beach row). Note the 33923 caveat in §4 — not paste-sourced.
- **Homepage links (§3, §6):** 0 word changes — href-only changes plus one segment merge ("Flood and " + "storm cleanup" → "Flood and storm cleanup", rendered words identical).
- **Drying sentences (§5a):** 7 pages × removed `[run]` + the per-page additions listed in the table.
- **Sign-offs (§5b):** 3 pages × removed `[General, pricing, information]` (plus `Read`→`read` case change on bonita-springs and estero) + the per-page additions listed in the table.
- **Everything else:** verbatim. No other word was added, removed, or reordered in any file I touched. Dashes 0 on all 11 rendered pages (visible `<main>` text). No invented facts, certifications, reviews, rates, or addresses; no invented links (every href used already existed as a route and, except the delinks, as a paste annotation).

## Link-audit results (rendered, port 8134)

- Homepage `<main>`: 29 distinct internal targets, each exactly **1x** — 0 duplicate body targets, 0 self-links (no `href="/"`). `/sewage-cleanup/` 1x, `/flood-cleanup/` 1x, `/areas/` 1x, `/commercial/` 0x in body (the card was its only body link; it remains in header/footer chrome).
- All 11 changed pages: 0 duplicate body targets and 0 self-links each (checked per page in `<main>`).
- No page links to itself from its body on any changed page.
- Old sentences absent + new sentences present, verified in rendered text on all 10 affected inner pages (7 drying + 3 sign-off, with fort-myers-beach sign-off verified unchanged and well-pump FAQ verified unchanged on both pages).

## Not done / open items

1. **A-2 remainder:** 6 area-card headings (Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Estero, Bonita Springs) remain H3 — needs a `functions.php` change by whoever owns includes (see §1 caveat). Outline is valid without it.
2. **H2 visual size:** the 5 promoted headings now render at H2 size (no class hook exists in `render_block()`); restore-H3-look is a CSS/includes call.
3. **Owner decisions:** D-P3-2 (Seasonal vs Vacant title), D-P3-4 (split Estero/Bonita paragraph? link leaks card to `/water-removal/`?), D-P2-1 option (add 33945 to Pine Island?), D-P3-9 tradeoff (keep card→`/areas/` + delinked line-2004, or revert to card→`/commercial/` + line-2004 link).
4. **33923 verification:** confirm 33923 is a Bonita Springs ZIP (not in any paste — auditor-sourced only).
5. **Not verified here:** full-site re-gate (other workers' files), export/`out/` (verifier owns the canonical export), live deploy (local only by order).
