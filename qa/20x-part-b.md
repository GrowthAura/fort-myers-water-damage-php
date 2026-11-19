# 20X AUDIT — WORKER B: Content Fidelity + Schema

**Project:** `~/workspace/fort-myers-php/` — live base `https://fort-myers-water-damage-php.pages.dev` (five-fix build)
**Date:** 2026-11-19 ~22:30 PKT · **Scope:** all 34 pages · **Mode:** audit-only, READ-ONLY
**Source of truth:** pastes in `pages/<slug>-paste-2026-11-19.md` (33 files) + `homepage-paste-2026-11-19.md`

## Method (read-only)

`qa/verify_export.py` was **not** run (banned — it re-emits data files). No parser `run()`/`emit()` was executed and no file was edited. Instead, two independent stages, both read-only:

- **Stage 1 — render fidelity:** visible `<main>` words from `out/` vs words rebuilt from the already-parsed `site/data/*.php` blocks (dumped via `php` `json_encode` to `/tmp`, never written back), plus the known chrome insertions (Call button + breadcrumb + "Last updated" line). Result: **34/34 pages, 0 differing ops** — the render is exactly faithful to the data.
- **Stage 2 — data vs paste:** block words vs paste copy words (link `(/slug/)` annotations stripped). Every differing region was adjudicated against the authorized-change inventory, re-parsed from the findings records:
  - dedup: `qa/FINDINGS-link-dedup.md` §3 — 74 REMOVE-SENTENCE + 1 REMOVE-BLOCK (73 distinct sentences after dedupe) + 62 DELINK (words kept, no word impact);
  - sentence cuts: `qa/FINDINGS-sentence-cuts.md` — FEMA flood-zone sentence (33 words) + Category 3 sewage sentence (24 words), homepage only;
  - Task 13 Related trim: `qa/FINDINGS-related-3.md` §§1–2 — 27 pages trimmed to exactly 3 Related items (98 items removed) + 27 distinct homepage-anchor variations. Related lists were verified **item-by-item** (paste items vs block items vs the doc's kept/removed lists), not just by flat word-diff.
- **Schema:** `python3 qa/validate_schema.py` run as-is (read-only) + an independent JSON-LD census.
- **Facts/legal:** phone/ZIP/brand/keyword census of rendered `<main>` vs paste; legal-page robots/sitemap/llms/date checks.

> **Scope note for the parent (please confirm):** the task brief's authorized list did not mention Task 13 (Related trim + anchor variations), but it is plainly owner-ordered work — the owner's hero-round order recorded in memory ("Related = just 3 per service page + homepage-link anchors VARIED per page, never the same homepage entity twice") plus the worker record `qa/FINDINGS-related-3.md`. This audit treats Task 13 as authorized on that basis. If the parent rules otherwise, the 98 removed Related items + 27 anchor variations on 27 pages become findings instead of authorized diffs. Nothing else in this report depends on that call.

## (a) Per-page word-diff table (34 rows)

"Rendered" = visible `<main>` words in `out/`. "Paste" = visible paste-copy words (annotations stripped). "Diff" = the `verify_export` word-diff (rendered vs paste + chrome insertions: Call button + breadcrumb + "Last updated" line). Negative = words absent from the render; every negative is fully explained by the authorized composition shown. "Clean" pages have diff 0 (rendered exceeds paste only by the chrome words).

| Page | URL | Rendered | Paste | Diff | Authorized composition | Verdict |
|---|---|---|---|---|---|---|
| `/` | https://fort-myers-water-damage-php.pages.dev | 5295 | 5402 | −107 | 10 dedup/cut sentence(s) | −107 — authorized only |
| `/water-removal/` | https://fort-myers-water-damage-php.pages.dev/water-removal/ | 3389 | 3418 | −42 | 3 dedup/cut sentence(s) + 5 Related item(s) removed + homepage anchor varied | −42 — authorized only |
| `/drying/` | https://fort-myers-water-damage-php.pages.dev/drying/ | 2717 | 2744 | −42 | 4 dedup/cut sentence(s) + 5 Related item(s) removed + homepage anchor varied | −42 — authorized only |
| `/sewage-cleanup/` | https://fort-myers-water-damage-php.pages.dev/sewage-cleanup/ | 2553 | 2563 | −23 | 2 dedup/cut sentence(s) + 4 Related item(s) removed + homepage anchor varied | −23 — authorized only |
| `/ac-leak/` | https://fort-myers-water-damage-php.pages.dev/ac-leak/ | 2835 | 2855 | −34 | 3 dedup/cut sentence(s) + 4 Related item(s) removed + homepage anchor varied | −34 — authorized only |
| `/ceiling-leak/` | https://fort-myers-water-damage-php.pages.dev/ceiling-leak/ | 2583 | 2598 | −30 | 3 dedup/cut sentence(s) + 4 Related item(s) removed + homepage anchor varied | −30 — authorized only |
| `/condo-leak/` | https://fort-myers-water-damage-php.pages.dev/condo-leak/ | 2353 | 2367 | −31 | 2 dedup/cut sentence(s) + 5 Related item(s) removed + homepage anchor varied | −31 — authorized only |
| `/cast-iron-pipe/` | https://fort-myers-water-damage-php.pages.dev/cast-iron-pipe/ | 2466 | 2478 | −29 | 2 dedup/cut sentence(s) + 4 Related item(s) removed + homepage anchor varied | −29 — authorized only |
| `/vacant-home/` | https://fort-myers-water-damage-php.pages.dev/vacant-home/ | 2342 | 2349 | −23 | 2 dedup/cut sentence(s) + 4 Related item(s) removed + homepage anchor varied | −23 — authorized only |
| `/first-hour-checklist/` | https://fort-myers-water-damage-php.pages.dev/first-hour-checklist/ | 2371 | 2377 | −24 | 1 dedup/cut sentence(s) + 5 Related item(s) removed + homepage anchor varied | −24 — authorized only |
| `/cost/` | https://fort-myers-water-damage-php.pages.dev/cost/ | 3719 | 3751 | −47 | 5 dedup/cut sentence(s) + 5 Related item(s) removed + homepage anchor varied | −47 — authorized only |
| `/insurance/` | https://fort-myers-water-damage-php.pages.dev/insurance/ | 3318 | 3342 | −38 | 4 dedup/cut sentence(s) + 4 Related item(s) removed + homepage anchor varied | −38 — authorized only |
| `/burst-pipe/` | https://fort-myers-water-damage-php.pages.dev/burst-pipe/ | 2300 | 2321 | −35 | 4 dedup/cut sentence(s) + 4 Related item(s) removed + homepage anchor varied | −35 — authorized only |
| `/mobile-home/` | https://fort-myers-water-damage-php.pages.dev/mobile-home/ | 2085 | 2093 | −22 | 2 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −22 — authorized only |
| `/slab-leak/` | https://fort-myers-water-damage-php.pages.dev/slab-leak/ | 2121 | 2117 | −12 | 3 Related item(s) removed + homepage anchor varied | −12 — authorized only |
| `/flood-cleanup/` | https://fort-myers-water-damage-php.pages.dev/flood-cleanup/ | 2404 | 2409 | −20 | 2 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −20 — authorized only |
| `/cape-coral/` | https://fort-myers-water-damage-php.pages.dev/cape-coral/ | 2005 | 2022 | −30 | 3 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −30 — authorized only |
| `/lehigh-acres/` | https://fort-myers-water-damage-php.pages.dev/lehigh-acres/ | 1811 | 1823 | −25 | 3 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −25 — authorized only |
| `/areas/` | https://fort-myers-water-damage-php.pages.dev/areas/ | 1628 | 1615 | 0 | — | 0 — clean |
| `/water-heater-leak/` | https://fort-myers-water-damage-php.pages.dev/water-heater-leak/ | 2026 | 2026 | −14 | 1 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −14 — authorized only |
| `/appliance-leak/` | https://fort-myers-water-damage-php.pages.dev/appliance-leak/ | 2149 | 2158 | −22 | 3 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −22 — authorized only |
| `/floors/` | https://fort-myers-water-damage-php.pages.dev/floors/ | 2068 | 2070 | −15 | 1 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −15 — authorized only |
| `/cabinets/` | https://fort-myers-water-damage-php.pages.dev/cabinets/ | 1878 | 1877 | −12 | 1 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −12 — authorized only |
| `/commercial/` | https://fort-myers-water-damage-php.pages.dev/commercial/ | 1950 | 1953 | −16 | 2 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −16 — authorized only |
| `/north-fort-myers/` | https://fort-myers-water-damage-php.pages.dev/north-fort-myers/ | 1930 | 1938 | −22 | 1 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −22 — authorized only |
| `/fort-myers-beach/` | https://fort-myers-water-damage-php.pages.dev/fort-myers-beach/ | 1925 | 1941 | −30 | 3 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −30 — authorized only |
| `/estero/` | https://fort-myers-water-damage-php.pages.dev/estero/ | 1809 | 1824 | −27 | 2 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −27 — authorized only |
| `/bonita-springs/` | https://fort-myers-water-damage-php.pages.dev/bonita-springs/ | 1746 | 1758 | −25 | 2 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −25 — authorized only |
| `/how-it-works/` | https://fort-myers-water-damage-php.pages.dev/how-it-works/ | 1862 | 1870 | −21 | 2 dedup/cut sentence(s) + 3 Related item(s) removed + homepage anchor varied | −21 — authorized only |
| `/contact/` | https://fort-myers-water-damage-php.pages.dev/contact/ | 807 | 795 | 0 | — | 0 — clean |
| `/about/` | https://fort-myers-water-damage-php.pages.dev/about/ | 1105 | 1093 | 0 | — | 0 — clean |
| `/privacy-policy/` | https://fort-myers-water-damage-php.pages.dev/privacy-policy/ | 892 | 880 | 0 | — | 0 — clean |
| `/terms/` | https://fort-myers-water-damage-php.pages.dev/terms/ | 691 | 678 | 0 | — | 0 — clean |
| `/disclaimer/` | https://fort-myers-water-damage-php.pages.dev/disclaimer/ | 520 | 514 | 0 | — | 0 — clean |

**Totals:** 818 words removed vs paste+chrome across the site, all authorized: 75 removed sentences (73 dedup + 2 cuts, every one matched to its record — inventory usage 75/75) + 98 Related items removed + 27 homepage anchors varied (27/27 distinct, verified item-by-item on all 27 Related pages; every page's Related list is exactly 3 items, homepage link last). Zero unmatched regions on any page; zero inserted words anywhere (no added copy). The five-fix round's CSS/menu changes contribute 0 words, as claimed — Stage 1 proves the render matches the data word-for-word on all 34 pages.

Spot-check of the homepage −107: FEMA sentence 33 words + Category 3 sentence 24 words (= 57, exactly the figure in `FINDINGS-sentence-cuts.md`) + 8 dedup sentences (50 words: "See emergency water removal" 4, "See how structural drying works" 5, "See what happens after you call" 6, "See AC leak water damage, ceiling leaks and cast iron pipe damage" 11, "See commercial water damage" 4, "See condo water damage for the full walkthrough" 8, "See North Fort Myers" 4, "See the full checklist for seasonal homes" 8) = 107. The two "See condo/commercial" sentences the brief names are inside that 50.

## Dashes

**0 em/en dashes (— –), literal or entity (`&ndash;`/`&mdash;`/`&#8211;`/`&#8212;`), in the whole rendered HTML of all 34 pages** (and 0 in visible `<main>` text). The pastes are also dash-free, so this is paste-faithful, not a render fix.

## Facts

- **Phone:** only `239-356-3708` (display), `+1-239-356-3708` (schema), `tel:+12393563708` appear sitewide — on all 34 pages (`tel:` on 34/34). One other number exists: `1-877-693-5236` on `/insurance/` only, twice, verbatim from the owner's paste — it is the Florida Department of Financial Services Insurance Consumer Helpline ("Questions can go to the Florida Department of Financial Services Insurance Consumer Helpline at 1-877-693-5236", paste lines 189/245). Not a business number, not invented.
- **Brand:** "Fort Myers Water Damage Restoration Pros" matches the paste exactly on every page. The only apparent +1s are breadcrumb chrome: `/about/` (rendered 5 vs paste 4) and `/contact/` (7 vs 6) — the breadcrumb repeats the H1, which contains the brand ("Home » About Fort Myers Water Damage Restoration Pros", "Home » Contact Fort Myers Water Damage Restoration Pros"). No brand wording added or changed anywhere.
- **ZIPs / geography:** every ZIP in rendered `<main>` also appears in that page's paste (0 render-only ZIPs, 0 paste-only ZIPs). Lee County ZIPs 33901–33967, 34134/34135 (Bonita Springs) all correct in context. Two apparent anomalies are false positives from the 5-digit scan: "70131"/"70132" are Florida Statute numbers `627.70131` / `627.70132` on `/insurance/` and `/about/` (paste-verbatim), not ZIPs. No invented addresses: no street address appears anywhere (service-area business, as ordered).
- **Certifications / reviews / rates:** no invented claims. "IICRC" occurs only where the paste has it, same counts (homepage 1, `/cost/` 2, `/drying/` 2, `/how-it-works/` 1) — all references to the IICRC S500 standard or "ask whether the technicians are IICRC-trained" (owner's words). No "certified", "licensed", "BBB", star-rating or review language invented; no dollar amount appears in the render that is not in the paste.

## FAQ

- **308 visible FAQs = 308 FAQPage schema questions across 31 pages; 0 mismatches.** Per-page visible == schema on all 31 FAQ pages (homepage 14, water-removal 14, drying 13, sewage-cleanup 13, ac-leak 11, ceiling-leak 11, condo-leak 10, cast-iron-pipe 11, vacant-home 9, first-hour-checklist 10, cost 12, insurance 12, burst-pipe 10, mobile-home 10, slab-leak 10, flood-cleanup 11, cape-coral 10, lehigh-acres 10, areas 9, water-heater-leak 10, appliance-leak 11, floors 9, cabinets 10, commercial 10, north-fort-myers 7, fort-myers-beach 9, estero 7, bonita-springs 8, how-it-works 8, contact 5, about 4). Each also equals its parser spec count. The 3 legal pages have 0 FAQs and no FAQPage schema (correct).

## (b) Schema validation

`python3 qa/validate_schema.py` (read-only), full output saved at `qa/20x-part-b-raw/schema-validation.txt`:

- **pages checked: 34 | JSON-LD scripts: 92 | nodes: 92**
- **ERRORS: 0 · WARNINGS: 0 · NOTES (by design): 6**
- All 92 JSON-LD scripts parse; every script's `@context` is `https://schema.org`; no duplicate `@id` per page.
- Type census: HomeAndConstructionBusiness 1 (homepage), Service 24, Article 3 (`/cost/`, `/insurance/`, `/how-it-works/`), HowTo 1 (`/first-hour-checklist/`), ContactPage 1, AboutPage 1, FAQPage 31, BreadcrumbList 30.
- **BreadcrumbList: 30 pages** (every inner page except homepage and the 3 legal pages). Independently re-asserted here: **every ListItem on all 30 pages carries an `item` field — 0 missing** (the old site's GSC error is gone). Positions are sequential from 1; every `item` URL is a real route.
- **Legal pages carry 0 JSON-LD scripts** (privacy-policy, terms, disclaimer — verified).
- The 6 NOTES are 3× "Article: publisher has no logo" + 3× "Article: no 'image'", one pair per Article page. See finding P3-1 below: the "no image" half of the note is stale.

## Legal pages

| Page | robots | JSON-LD | "Last updated: November 19, 2026" | In sitemap.xml | In llms.txt |
|---|---|---|---|---|---|
| `/privacy-policy/` | `noindex, follow` | 0 | present (1×) | no | no |
| `/terms/` | `noindex, follow` | 0 | present (1×) | no | no |
| `/disclaimer/` | `noindex, follow` | 0 | absent (0×) | no | no |

Supporting: sitemap.xml has 31 locs, all `<lastmod>2026-11-19</lastmod>`, no image/changefreq/priority entries; llms.txt has 31 entries. All as specified.

## (c) Findings

### P3-1 — Article schema has no `image` on 3 pages, and the validator's "by design" reason is stale

- **Pages:** `/cost/` — https://fort-myers-water-damage-php.pages.dev/cost/ · `/insurance/` — https://fort-myers-water-damage-php.pages.dev/insurance/ · `/how-it-works/` — https://fort-myers-water-damage-php.pages.dev/how-it-works/
- **Severity:** P3 (polish / rich-result eligibility, not a break — pages validate with 0 errors).
- **Evidence:** `qa/validate_schema.py` emits, for each of the 3 pages: `NOTE: /cost/: Article: no 'image' (by design — heroes honestly empty; no photo passes licence+place+subject)`. That reason is no longer true: the hero round filled every hero, and the three hero files exist in the export — `out/assets/img/hero-cost.jpg` (149,702 B), `out/assets/img/hero-insurance.jpg` (130,600 B), `out/assets/img/hero-how-it-works.jpg` (181,108 B) — and each renders in the page hero (e.g. `/insurance/` hero `<img src="/assets/img/hero-insurance.jpg" ...>`). Google lists `image` as required for the Article rich result, so these 3 pages cannot earn it as written. (The companion note, "publisher has no logo", still holds — only the SVG favicon mark exists, no raster logo — so that half is not a finding.)
- **Proposed fix (owner call):** add `"image"` (absolute URL of the page's hero image, e.g. `https://fortmyerswaterdamagerestoration.us/assets/img/hero-cost.jpg`) to the 3 Article schemas in the pastes and re-parse/re-export. Note this deviates from the paste schema, so it needs the owner's word; do not add it silently. Alternatively, leave as-is and accept no Article rich result on these 3 pages.

### Checked and clear (not findings — recorded so they are not re-raised)

- `1-877-693-5236` on `/insurance/`: owner's paste, FL DFS helpline (see Facts).
- "70131"/"70132": Florida Statute numbers `627.70131`/`627.70132`, paste-verbatim (see Facts).
- IICRC mentions: paste-verbatim S500 references, no invented certification (see Facts).
- Brand +1 on `/about/` and `/contact/`: breadcrumb repeats the H1 (see Facts).
- Task 13 Related trim + anchor variations: treated as authorized per the scope note above; item-by-item verified against `FINDINGS-related-3.md` (98 removed, 27 distinct new anchors, all 27 lists exactly 3 items with the homepage link last).

## Summary

**P1 0 · P2 0 · P3 1 — word-diff 0 unauthorized on all 34 pages (818 words removed, all authorized), dashes 0, FAQ 308 = 308, schema 0 errors / 0 warnings, legal pages fully compliant; the only finding is P3-1 (Article `image` missing on `/cost/`, `/insurance/`, `/how-it-works/`, with a stale "heroes honestly empty" justification).**

## Raw evidence

- `qa/20x-part-b-raw/audit_b.py` + `worddiff.json` + `worddiff-log.txt` — first-pass word-diff + FAQ/dash census
- `qa/20x-part-b-raw/audit_b2.py` + `worddiff2.json` + `worddiff2-log.txt` — two-stage word-diff (render-vs-blocks, blocks-vs-paste) with per-region adjudication + Related item-list verification
- `qa/20x-part-b-raw/audit_b3.py` + `facts.json` + `facts-log.txt` — phone/ZIP/brand/keyword census + legal/sitemap/llms checks
- `qa/20x-part-b-raw/schema-validation.txt` — full `validate_schema.py` output
- Live parity (out/ byte-identical to live) was taken as given per the task brief and was **not** independently re-verified here (no live-browser access in this subagent); all checks above are against local `out/`.
