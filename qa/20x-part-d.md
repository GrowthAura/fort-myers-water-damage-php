# 20X AUDIT — WORKER D: TECHNICAL + BLUNDER HUNT

**Project:** `~/workspace/fort-myers-php/` — **Live base:** https://fort-myers-water-damage-php.pages.dev (five-fix build)
**Date:** 2026-11-19 ~22:40 PKT. **Scope:** all 34 pages + 404. **Mode:** audit-only, READ-ONLY (no file edited, no push/deploy, `qa/verify_export.py` never run).
**Method:** static parse of `out/` (HTMLParser stack check), live curl checks, local render of `out/` via `python3 -m http.server` + Playwright **bundled** Chromium (no `executable_path`), desktop 1440×900 all 34 pages + 7 mobile 390px samples + 404, contact-sheet viewed-pixel review of all 34 heroes + 13 kinds + 6 area + 6 help images.

**Live vs local:** live home byte-identical to local `out/index.html` (md5 `36ff385725999c7b73979023e3491965` both). Live `/water-removal/` 200, `/cost/` 200, `/favicon.svg` 200 (`image/svg+xml`), bogus URL 404.

---

## (a) TECHNICAL CHECKLIST — results with counts

| # | Check | Result |
|---|---|---|
| T1 | Console errors, local render, desktop 34/34 pages | **0** |
| T2 | Console errors, mobile 390px sample (home, cost, water-removal, areas, contact, vacant-home, about) | **0** |
| T3 | `pageerror` (uncaught JS exceptions), all 41 renders | **0** |
| T4 | Unclosed / mismatched tags (parser stack check, 34 pages + 404) | **0** |
| T5 | Duplicate `id` attributes per page (34 + 404) | **0** |
| T6 | Mixed content — `http://` resources | **0** (all local assets + `https://` embeds only) |
| T7 | Dead `#` anchors — every `href="#…"` target exists | **0 broken**; also **0** empty `href="#"` |
| T8 | Favicon present + renders | **35/35 files** link `/favicon.svg`; rendered at 16/32/48px — bold orange drop on dark teal, legible at 16px (shot `favicon-16-32-48.png`) |
| T9 | Missing/empty `alt` on `<img>` | **0** — every image has a non-empty alt |
| T10 | Horizontal overflow | **0** on 34 desktop + 7 mobile + 404 |
| T11 | H1 count | **1 on every page** (34/34 + 404) |
| T12 | `srcset` width descriptors vs real file widths (all heroes) | **0 mismatches** |
| T13 | `width`/`height` attributes vs real file dims (all heroes) | **0 mismatches** |
| T14 | Phone consistency | **239-356-3708** everywhere; all `tel:` hrefs exactly `+12393563708` (578 displayed mentions). The only other number, 877-693-5236 on `/insurance/`, is the Florida Dept. of Financial Services helpline (1-877-MY-FL-CFO) in FAQ text + JSON-LD — correct, not a business number |
| T15 | Sitemap vs link graph | Sitemap **31** locs; all 31 linked from site; the 3 non-sitemap routes (`/privacy-policy/`, `/terms/`, `/disclaimer/`) are linked from the footer (legal pages, intentionally not in sitemap). **0 orphans** in either direction |
| T16 | Five-fix cross-check: footer Services = exactly header menu 7 | **HOLDS** — footer lists exactly Emergency Water Removal, Structural Drying, Sewage Backup Cleanup, Flood & Storm Cleanup, AC Leak, Ceiling Leak, Burst Pipe |
| T17 | Five-fix cross-check: no Areas column / no area links in footer | **HOLDS** (visible) — 0 area hrefs in footer on all pages; visible "Areas We Serve" heading gone. Caveat: the text survives in an HTML comment — see D-P3-3 |
| T18 | Five-fix cross-check: stylesheet `?v=2` | **HOLDS** — `styles.css?v=2` on all 35 files incl. 404 |
| T19 | Page weight (HTML+CSS 22 KB+JS 2 KB+images) | Max **465 KB** (`/areas/`, 7 images), then Lehigh Acres 423 KB, home 389 KB; lightest 173 KB (disclaimer). **No page over 500 KB** — reasonable |
| T20 | Image file weights (93 files, 9.6 MB total) | 10 heaviest below; only 2 files over 300 KB (see D-P3-8). No image served at >2× its desktop display size: heroes 1920/1600w files in a 1440px slot (1.33×/1.11×); kinds backgrounds 760×864 in a 381×432 card (2.0×, retina-correct); help/area `<img>` 474w in 379px slots (1.25×) |

### 10 heaviest images (slot size vs file size)

| File | Bytes | File dims | Display slot (desktop) | Ratio | Verdict |
|---|---|---|---|---|---|
| hero-lehigh-acres.jpg | 364 KB | 1600×1067 | 1440×536 hero | 1.11× | Over 300 KB — see D-P3-8 |
| hero-north-fort-myers.jpg | 340 KB | 1600×1067 | 1440×607 hero | 1.11× | Over 300 KB — see D-P3-8 |
| hero-cape-coral.jpg | 283 KB | 1920×1280 | 1440×571 hero | 1.33× | OK |
| hero-estero.jpg | 259 KB | 1600×1067 | 1440×607 hero | 1.11× | OK |
| hero-commercial.jpg | 256 KB | 1920×1280 | 1440×571 hero | 1.33× | OK |
| hero-fort-myers-beach.jpg | 256 KB | 1920×1280 | 1440×571 hero | 1.33× | OK |
| hero-about.jpg | 230 KB | 1920×1280 | 1440×536 hero | 1.33× | OK |
| hero-bonita-springs.jpg | 222 KB | 1600×1067 | 1440×571 hero | 1.11× | OK |
| hero-mobile-home.jpg | 214 KB | 1920×1280 | 1440×571 hero | 1.33× | OK |
| hero-areas.jpg | 213 KB | 1920×1280 | 1440×536 hero | 1.33× | OK |

### Not defects (checked, clean — do not re-file)

- **Google Maps iframe "failed" in VM Chromium** (`ERR_TUNNEL_CONNECTION_FAILED` on `/contact/`, `/terms/`, `/disclaimer/`, mobile contact): the VM proxy blocks `google.com/maps` in Chromium. Not a site defect. Live map tiles still need one real-browser look (standing item).
- **404 console line** `Failed to load resource: 404` is the browser reporting the 404 page's own status, not a JS error. 404 renders clean (overflow 0, H1 1, no pageerror; shot `404-desktop.png`).
- **`/areas/` last two area images** (`area-estero.jpg`, `area-bonita-springs.jpg`) read as `currentSrc="" / naturalWidth 0` on first paint: they are `loading="lazy"` below the fold. After stepwise scrolling all 6 load (`naturalWidth 474`, `complete true`). Not broken.
- **Hero `naturalWidth` reads 1440** in-DOM while the file is 1920×1280: a fresh `Image()` load of the same URL reports 1920×1280 — Chromium decodes the in-DOM hero at display size. File is correct; not a site issue.
- **"See commercial water damage." on `/how-it-works/`** is the page's only `/commercial/` link in `<main>` (count 1) — a legitimate single body link. The homepage version the hero round flagged is gone (0 hits on home, incl. tag-tolerant search). No action.

---

## (b) IMAGE-RELEVANCE VERDICTS (viewed pixels)

Contact sheets in `qa/screenshots-20x-testing/d/`: `sheet-heroes-1.jpg`, `sheet-heroes-2.jpg`, `sheet-heroes-3.jpg`, `sheet-kinds.jpg`, `sheet-areas-help.jpg`. Every image below was looked at, not hash-checked.

### Heroes — 34/34 PASS (no wrong-country / wrong-city / wrong-service)

| File | What the photo actually shows | Verdict |
|---|---|---|
| hero-home.jpg | Technician extracting water from a tiled FL living room, palms through sliders | PASS |
| hero-about.jpg | Crew unloading drying gear from a van, palms + tile-roof FL house | PASS |
| hero-ac-leak.jpg | Leaking AC closet, drip + bucket, palms outside window | PASS |
| hero-appliance-leak.jpg | Front-load washer leaking onto laundry-room tile | PASS |
| hero-areas.jpg | Downtown Fort Myers riverfront, brick buildings + royal palms at sunset | PASS |
| hero-bonita-springs.jpg | Waterfront homes on a lake/river, FL vegetation | PASS |
| hero-burst-pipe.jpg | Burst pipe spraying under a sink, gloved hand on valve | PASS |
| hero-cabinets.jpg | Water-damaged cabinet base, moisture meter, air mover | PASS |
| hero-cape-coral.jpg | Canal with boats, screened lanais, palms — classic Cape Coral | PASS |
| hero-cast-iron-pipe.jpg | Opened wall, rusted cast-iron stack, mould, work light | PASS |
| hero-ceiling-leak.jpg | Bulging stained ceiling dripping into a bucket, moisture meter | PASS |
| hero-commercial.jpg | Flooded open-plan office, drying fans, worker | PASS |
| hero-condo-leak.jpg | Wet condo living room, sliders, palms, technician at wall | PASS |
| hero-contact.jpg | Bright office reception, palms outside | PASS (generic, on-topic) |
| hero-cost.jpg | Technician probing a damp stained wall, air mover behind | PASS |
| hero-disclaimer.jpg | Shield + papers + laptop on a desk | PASS (generic legal stock — see D-P3-6) |
| hero-drying.jpg | Dehumidifier + air movers drying a wet room | PASS |
| hero-estero.jpg | Mediterranean condo/coach-home courtyard, fountain, tile roofs | PASS |
| hero-first-hour-checklist.jpg | Person photographing a flooded hallway with a phone | PASS |
| hero-flood-cleanup.jpg | Flooded living room, worker + extraction/fans | PASS |
| hero-floors.jpg | Buckled wood flooring + moisture meter | PASS |
| hero-fort-myers-beach.jpg | Elevated stilt house on white-sand beach, Gulf, palms | PASS |
| hero-how-it-works.jpg | Technician with drying equipment on wet tile | PASS |
| hero-insurance.jpg | Stack of papers + phone on a desk | PASS (generic — see D-P3-6) |
| hero-lehigh-acres.jpg | Flat lots, concrete-block homes, oaks with Spanish moss | PASS |
| hero-mobile-home.jpg | Technician at a mobile home exterior | PASS |
| hero-north-fort-myers.jpg | Manufactured homes by the river, oaks/moss | PASS |
| hero-privacy-policy.jpg | Laptop + padlock + papers | PASS (generic legal stock — see D-P3-6) |
| hero-sewage-cleanup.jpg | Worker in hazmat suit cleaning sewage by a toilet | PASS |
| hero-slab-leak.jpg | Gloved hands, moisture meter on wet cracked tile | PASS |
| hero-terms.jpg | Notepad + pen + glasses on a desk | PASS (generic legal stock — see D-P3-6) |
| hero-vacant-home.jpg | Technician entering a home, sheet-covered furniture, wet floor | PASS |
| hero-water-heater-leak.jpg | Water heater leaking in a garage, puddle, extraction hose | PASS |
| hero-water-removal.jpg | Extraction wand on wet tile, pump | PASS |

### Kinds cards (background images) — 13/13 PASS

| File | What it shows | Verdict |
|---|---|---|
| kinds-ac-leak.jpg | Leaking AC closet | PASS |
| kinds-appliance-leak.jpg | Dishwasher leaking onto kitchen floor | PASS |
| kinds-burst-pipe.jpg | Burst supply line spraying | PASS |
| kinds-cast-iron-pipe.jpg | Rusted cracked cast-iron pipe in a crawlspace | PASS |
| kinds-ceiling-leak.jpg | Stained sagging ceiling | PASS |
| kinds-condo-leak.jpg | Condo living room, sliders, palms | PASS |
| kinds-flood-storm.jpg | Flooded FL street, palms, storm sky | PASS |
| kinds-floors-cabinets.jpg | Swollen cabinet base + buckled flooring | PASS |
| kinds-mobile-home.jpg | Water-damaged mobile-home interior, warped vinyl floor | PASS |
| kinds-sewage-backup.jpg | Flooded bathroom, toilet + tub | PASS |
| kinds-slab-leak.jpg | Swollen baseboard / damp tile floor | PASS |
| kinds-vacant-home.jpg | Sheet-covered furniture, mouldy ceiling corner | PASS |
| kinds-water-heater-leak.jpg | Rusted water heater leaking in a garage | PASS |

### Area images — 6/6 PASS

| File | What it shows | Verdict |
|---|---|---|
| area-bonita-springs.jpg | River waterway, condos + docks | PASS |
| area-cape-coral.jpg | Canal-front homes, lanais, docks | PASS |
| area-estero.jpg | Gated condo community around a lake | PASS |
| area-fort-myers-beach.jpg | White-sand beach + beachfront condos | PASS |
| area-lehigh-acres.jpg | Flat street, block homes, oaks | PASS |
| area-north-fort-myers.jpg | Riverfront manufactured homes | PASS |

### Help images (homepage) — 5/6 PASS, 1 weak

| File | What it shows | Verdict |
|---|---|---|
| help-emergency-water-removal.jpg | Extraction machine on wet tile | PASS |
| help-every-property.jpg | FL house + condo block + mobile home in one frame | PASS (fits "every property") |
| help-flood-storm-cleanup.jpg | Flooded street, sandbagged homes | PASS |
| help-leaks-every-kind.jpg | AC closet + water heater in a garage | PASS |
| help-sewage-cleanup.jpg | A spotless clean bathroom — no water, no damage, no equipment | WEAK — see D-P3-5 |
| help-structural-drying.jpg | Drying equipment + opened wall base | PASS |

---

## (c) FINDINGS

### P1 — 0

None. No page is broken, no ranking/trust break found.

### P2

**D-P2-1 — Areas ZIP table assigns 33993 to "Pine Island and Matlacha" — 33993 is Cape Coral**
- Page/URL: `/areas/` — "Lee County Service Areas and ZIP Codes" table (`out/areas/index.html`).
- Evidence: table row `Pine Island and Matlacha | 33922, 33956, 33993 | Storm surge, mobile homes, seasonal homes`. 33993 is a Cape Coral ZIP and is already listed in the same table under `Cape Coral | 33904, 33909, 33914, 33990, 33991, 33993`. Pine Island / Matlacha ZIPs are 33922 (Bokeelia), 33945 (Pineland), 33956 (St. James City / Matlacha) — 33993 belongs to none of them.
- Fix: remove `33993` from the Pine Island and Matlacha row (optionally add `33945` for Pineland if the row is meant to cover all of Pine Island).

**D-P2-2 — Two homepage help cards name existing service pages but are not clickable, while their 4 sibling cards are**
- Page/URL: homepage `/` — "What we help with" help grid (`out/index.html`, `article.kind-card.help-card`).
- Evidence: 6 help cards; 3 link (`Emergency water removal` → `/water-removal/`, `Structural drying` → `/drying/`, `Every kind of property` → `/commercial/`), 3 have no link at all (`Sewage backup cleanup`, `Flood and storm cleanup`, `Leaks of every kind`). The first two name exact existing pages — `/sewage-cleanup/` and `/flood-cleanup/` — so a user tapping the card expecting the service gets nothing, unlike the linked siblings. (Confirmed: 0 `href` inside those two card blocks.)
- Fix: link `Sewage backup cleanup` → `/sewage-cleanup/` and `Flood and storm cleanup` → `/flood-cleanup/` in the same pattern as the sibling cards. `Leaks of every kind` has no single target — leave unlinked (see D-P3-4 note) or link it to `/water-removal/`.

### P3

**D-P3-1 — Areas ZIP table omits two real ZIPs**
- Page/URL: `/areas/` ZIP table.
- Evidence: Bonita Springs row lists `34134, 34135` but omits `33923` (also Bonita Springs). Fort Myers Beach row lists `33931` only but omits `33932` — and the Fort Myers Beach page itself mentions 33932. (34134/34135 for Bonita Springs are correct — Bonita uses the Naples-series ZIPs.)
- Fix: add `33923` to the Bonita Springs row and `33932` to the Fort Myers Beach row.

**D-P3-2 — "Seasonal Home" vs "Vacant Home" label mismatch on the vacant-home page (his call, carried from the hero round)**
- Page/URL: `/vacant-home/`.
- Evidence: `<title>` is `Seasonal Home Water Damage Fort Myers | Came Back to a Leak?` and og/twitter titles match, while the slug is `/vacant-home/`, the H1 is `Water Damage Found After Returning to Your Fort Myers Home`, all 20 in-site anchors say `water damage in vacant homes`, and the kinds card says `Came back to a wet or musty seasonal home`. The footer no longer links the page at all (five-fix round), so the mismatch is now title-only — but the title is the ranking label.
- Fix: his call — either retitle to `Vacant Home Water Damage Fort Myers …` to match slug/H1/anchors, or keep `Seasonal Home` deliberately and align the H1/anchors to it. Do not change silently; it is a naming decision.

**D-P3-3 — Footer still carries an HTML comment naming the removed "Areas We Serve" column (all 34 pages)**
- Page/URL: every page, footer.
- Evidence: `out/index.html` (and all 34 pages) footer contains `<!-- No Areas column: Areas is header-only (fix round 2026-11-19, owner order). The old "Areas We Serve" column (6 area links + the hub link + the footer-zips line) was removed here. -->`. Invisible to users and Google, but the five-fix claim "'Areas We Serve' gone" only holds for visible text.
- Fix: delete the comment (or shorten it to `<!-- Areas is header-only -->`) on the next export.

**D-P3-4 — Estero and Bonita Springs share one homepage paragraph; "Leaks of every kind" help card is link-free by design**
- Page/URL: homepage `/` — areas section ("Water Damage Help Across Lee County") + help grid.
- Evidence: one paragraph covers both areas — `Estero and Bonita Springs: condo leaks from the unit above and seasonal homes found wet after time away. See Estero and Bonita Springs.` (the two links exist, the prose is shared). Help card `Leaks of every kind: AC leaks, burst pipes, water heaters, appliances and slab leaks.` has no link and no single target page exists for it.
- Fix: his decision (already flagged in the hero round) — split the Estero/Bonita paragraph into two area-specific lines if he wants it; leave the leaks card unlinked or point it at `/water-removal/`.

**D-P3-5 — `help-sewage-cleanup.jpg` shows a spotless bathroom — no water, damage, or equipment visible**
- Page/URL: homepage `/` help card "Sewage backup cleanup".
- Evidence: viewed pixels (`sheet-areas-help.jpg`): clean white bathroom, toilet + tub, mop bucket — reads as a cleaning-service photo, not sewage cleanup. Every other help image shows the actual problem or the equipment. (Contrast with `kinds-sewage-backup.jpg`, which correctly shows a flooded bathroom.)
- Fix: swap for a photo showing a sewage backup / contaminated water or cleanup crew in PPE; if nothing passes the relevance bar, leave the slot honestly empty rather than a clean-bathroom shot.

**D-P3-6 — Four non-service heroes are generic desk/paper stock (topical, not wrong)**
- Pages: `/disclaimer/` (shield + papers), `/insurance/` (stack of papers + phone), `/privacy-policy/` (laptop + padlock), `/terms/` (notepad + pen + glasses).
- Evidence: viewed pixels (`sheet-heroes-2.jpg` / `sheet-heroes-3.jpg`). None is wrong-country or wrong-service — they are generic legal/office stock, unlike the 30 service/area heroes which are all specific and on-topic.
- Fix: optional polish only — replace with Florida-specific or service-adjacent photos if good ones exist; otherwise keep (no trust harm as-is).

**D-P3-7 — Repeated boilerplate blocks across pages (template text, not a ranking risk at this scale)**
- Evidence (visible `<main>` text, `>80`-char paragraphs):
  - `Dehumidifiers and air movers run with readings logged daily. See structural drying.` — identical step-5 sentence on 7 pages (bonita-springs, cape-coral, fort-myers-beach, lehigh-acres, mobile-home, vacant-home, water-heater-leak). The surrounding 5-step lists are localised per page; only this one step sentence is shared verbatim.
  - `Read how insurance handles water damage in Florida. General pricing information: water damage pricing guide.` — identical sign-off paragraph on 6 pages (bonita-springs, commercial, estero, floors, fort-myers-beach, north-fort-myers).
  - Well-pump FAQ answer `Turn off the well pump at its breaker and close the main valve near the pressure tank. That stops the pump from pushing more water into a broken line.` — identical on `/cape-coral/` and `/lehigh-acres/` (questions differ slightly).
- Fix: optional — localise the drying step sentence per page (e.g. name the room/material) and vary the sign-off wording on 2–3 of the 6 pages. The well-pump answer is the same correct advice in both places; leave or vary one word.

**D-P3-8 — Two heroes over 300 KB; mobile serves the 960w hero at 390px (2.46×)**
- Evidence: `hero-lehigh-acres.jpg` 364 KB (1600×1067) and `hero-north-fort-myers.jpg` 340 KB (1600×1067) are the only files over 300 KB; all other heroes are 127–283 KB. Desktop ratios are fine (1.11×–1.33×). On mobile the `srcset` has no variant smaller than 960w, so a 390px viewport downloads the 960w file (2.46×).
- Fix: re-encode the two heaviest heroes at slightly lower quality / resize to 1440w (target ≤250 KB); optionally add a ~640w hero variant for mobile. Page weights are otherwise fine (max 465 KB on `/areas/`).

**D-P3-9 — "Every kind of property" help card links only to `/commercial/` though it lists five property types**
- Page/URL: homepage `/` help grid.
- Evidence: card text `Every kind of property: single-family homes, condos, mobile homes, vacation rentals and businesses.` — the single link goes to `/commercial/`, so four of the five named property types lead to a page that is not about them.
- Fix: either link the card to `/areas/` (all properties, all areas) or make only the word "businesses" the link and leave the rest plain.

---

## Facts spot-checked (clean — no finding)

- Phone 239-356-3708 consistent on all 35 files; `tel:+12393563708` everywhere.
- ZIPs in the areas table otherwise correct: Fort Myers 33901/33905/33907/33908/33912/33913/33916/33919/33966/33967; Cape Coral 33904/33909/33914/33990/33991/33993; Lehigh Acres 33936/33971–33976; North Fort Myers 33903/33917; Fort Myers Beach 33931; Sanibel 33957 / Captiva 33924; Estero 33928; Bonita Springs 34134/34135.
- County/geography: Bonita Springs "in southern Lee County, just north of the Collier County line" — correct; Estero in Lee County — correct; "North of the Caloosahatchee" for North Fort Myers — correct.
- Regulatory/fact claims read in body text, all plausible and standard: NFIP 30-day waiting period; proof of loss within 60 days; ICC coverage up to $30,000; Citizens flood-policy requirement reaching all wind policies January 1, 2027; FEMA 50% rule in A/V zones; water Categories 1/2/3; Florida Statute 718.111(11) (condo insurance split); post-loss assignment-of-benefits reform for policies issued on/after January 1, 2023; mold in 24–48 hours; drying "about 3 to 5 days" for clean water.
- Typos: pattern scan over all 34 pages' visible `<main>` text (~72,000 words) — **0 hits** for teh/recieve/seperate/occured/adress/Fort Meyers/Ft. Myers/Lee Country/Fllorida/damge/plumming/structual/insurence/cliam/deductable/floood/sewrage/humidty/dehumidifer/mould; "Caloosahatchee" spelled correctly in all 14 mentions; 0 double spaces; "mold" 116 / "mould" 0.
- Legal pages: `Last updated: November 19, 2026` on privacy + terms (current); disclaimer has no date line.
- Mobile home top viewport renders clean (shot `mobile-top-home.png`): brand, Menu, H1, call CTA, "Describe your water problem" button, hero intro with phone link, sticky call bar — no overflow, no clipping.

## Screenshots (defects / evidence)

`qa/screenshots-20x-testing/d/`: `favicon-16-32-48.png`, `mobile-top-{home,cost,water-removal,areas,contact,vacant-home,about}.png`, `areas-grid-bottom-desktop.png`, `404-desktop.png`, `sheet-heroes-{1,2,3}.jpg`, `sheet-kinds.jpg`, `sheet-areas-help.jpg`. No defect screenshot was needed for P2s (both are visible in the HTML / contact sheets, cited above by file + line content).

---

## SUMMARY

**P1 0 · P2 2 · P3 9 — what passed clean:** console errors 0, pageerrors 0, unclosed/mismatched tags 0, duplicate ids 0, mixed content 0, broken # anchors 0, overflow 0, H1 1/page, favicon present + legible at 16px, alt text 100%, srcset/width-height attrs all correct, phone + ZIPs + county + regulatory facts spot-checked clean, typos 0 in ~72k words, sitemap/link graph 0 orphans, live home byte-identical to local, all five-fix claims in scope hold (footer 7 services, no Areas column, `?v=2`), and all 34 heroes + 13 kinds + 6 area images pass viewed-pixel relevance (only 1 weak help image + 4 generic legal heroes noted as P3).
