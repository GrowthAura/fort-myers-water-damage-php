# FINDINGS — 10x ROUND VERIFICATION (Independent Verifier)

- **Project:** `~/workspace/fort-myers-php/` — Fort Myers PHP site, 34 pages
- **Date:** 2026-11-19 ~23:50 – 2026-11-20 ~00:40 PKT
- **Mode:** LOCAL ONLY. No push, no deploy, no DNS, no git commit (nothing committed;
  working tree left exactly as the workers left it). `qa/verify_export.py` NEVER run.
- **Audited:** `qa/FINDINGS-20x-testing.md` (the audit this round fixes) +
  `qa/FINDINGS-10x-design.md` (Worker 1) + `qa/FINDINGS-10x-content.md` (Worker 2) +
  `qa/FINDINGS-10x-images.md` (Worker 3) + `qa/FINDINGS-10x-closer.md` (closer).
- **Method:** own canonical export (`python3 qa/export_cloudflare.py out`, exit 0),
  own word-diff script (rendered `<main>` vs paste copy, SequenceMatcher regions,
  adjudicated against the dedup / Related-trim / Worker-2 inventories),
  own static link/SEO gates, own Playwright probe (bundled Chromium only,
  `out/` served on 127.0.0.1:8139), gradient-aware contrast re-measurement,
  scrim composite computed independently, EXIF re-checked with piexif,
  reuse-net log + script inspected (net NOT re-run — nothing smelled).
  Nothing taken on any worker's word; every number below was re-measured.

## VERDICT — READY

**P1 0 · P2 0 · P3 0 — FINAL (re-verified 2026-11-20 ~02:30 PKT).** First verdict
was P1 0 · P2 4 · P3 5, NOT READY; all 9 were fixed by the P2-fix and P3-fix
workers and this final independent re-verification re-gated everything from a
fresh canonical export and found 0 remaining defects. The first-verdict text
below is preserved for the record; the "FINAL RE-VERIFICATION" section at the
end of this file is authoritative.
and the build is in strong shape (word-diff 0 unauthorized, schema 0/0,
overflow 0, FAQ 308 = 308, ?v=3 on 34/34, both map strips rendering, About
photo fixed). It is NOT READY because of 4 P2s: one unverified fact live on
/areas/ (ZIP 33923), one dangling homepage sentence (D-P3-9 tradeoff), and
two mobile tap targets below the 44px floor that this round itself introduced.
(All 4 fixed and re-verified — see FINAL RE-VERIFICATION at the end.)

| Severity | Count | IDs |
|---|---|---|
| P2 (visible defect / unverified fact) | 4 | V-P2-1 (33923), V-P2-2 (dangling "See…" sentence), V-P2-3 (mobile menu 36px), V-P2-4 ("Read the intro ↓" 31px) |
| P3 (polish) | 5 | V-P3-1 (phone icon 38px), V-P3-2 (H1 orphan @320), V-P3-3 (card body 18px), V-P3-4 (trust-row place-line fallback), V-P3-5 (/contact/ ghost self-link, pre-existing) |

---

## P2 DEFECTS

### V-P2-1 — ZIP 33923 in the Bonita Springs row is NOT confirmed as a current Bonita Springs ZIP — remove it
- **Page:** /areas/ — ZIP table row `Bonita Springs | 33923, 34134, 34135`.
- **Task rule applied:** Worker 2 admitted 33923 appears in NO paste (auditor-sourced
  only) and the brief ordered independent confirmation before shipping.
- **What I found (web search, 2026-11-20):** current Bonita Springs ZIP lists agree
  on **34133, 34134, 34135, 34136 only** — zip-codes.com Lee County table
  (34134 + 34135 standard, 34133 + 34136 PO Box), zipcodestogo.com ("4 unique ZIP
  codes in Bonita Springs"), roadsidethoughts.com (33931, 34133–34136).
  **zip-codes.com returns 404 for a 33923 page** (no such ZIP in its database).
  33923 appears only as a **historical** Bonita Springs ZIP: countryaah lists
  "Bonita Springs | 33923 | Lee", and 1990s Bonita Springs street addresses carry
  33923 where the same addresses today carry 34135 (e.g. 10215 Kentucky St,
  33923 in 1984–1993 → 34135-4869 now; 11430 Pendleton St, 33923 in 1993–1995 →
  34135-5992 now). One source (bestplaces.net) even titles 33923 as Boca Grande.
  I could NOT confirm 33923 as a current Bonita Springs ZIP from any authoritative
  source (USPS lookup not reachable for a direct check from here).
- **Fix:** remove `33923` from the Bonita Springs row → `34134, 34135`
  (the paste-verbatim values). One-token data change; re-export + re-gate /areas/.

### V-P2-2 — D-P3-9 tradeoff: the homepage "See every city and ZIP code…" sentence dangles with no link and nothing to see
- **Page:** homepage `/`, last paragraph of the areas section.
- **Rendered (verified in out/index.html):** `See every city and ZIP code we cover
  in our Lee County service areas.` — plain text, 0 links. The `/areas/` link
  that used to sit on "ZIP code we cover in our Lee County service areas" was
  delinked so the help card "businesses" could point at /areas/ instead
  (`/areas/` is 1x in `<main>`, on "businesses"; `/commercial/` is 0x in `<main>`).
- **Why it reads broken:** the sentence is an imperative — "See every city and ZIP
  code" — but there is nothing to see from it: no link, and no city/ZIP list
  follows it (the next block is the map section, which shows no ZIP codes).
  The preceding paragraphs link individual areas, but none of them is "every
  city and ZIP code". This is exactly the flagged case in the brief.
- **Fix (the revert specified in FINDINGS-10x-content.md §6):** card "businesses"
  back to `'href' => '/commercial/'`, and restore the line-2004 `/areas/` link
  on "ZIP code we cover in our Lee County service areas". D-P3-9 then stands
  unfixed as a known item (card lists five property types, links only to
  /commercial/), not silently duplicated.

### V-P2-3 — Mobile menu button is 36px wide at 390/320 — below the 44px floor, on all 34 pages
- **Measured (Playwright, all 34 pages):** `.mobile-menu summary` = **36 × 54.6px**,
  visible text just "☰" (the "Menu" word is hidden at ≤620px). Height passes;
  width fails the site's ≥44px tap-target gate.
- **Regression introduced by this round:** in the five-fix build the summary read
  "☰ Menu" (~90px wide, both dimensions ≥44px). Worker 1's header-overlap fix
  made the menu icon-only at ≤620px (FINDINGS-10x-design.md §5.2) and shrank
  the target's width below the floor. The 20x audit measured min tap target
  44px at 390; this round regressed it.
- **Fix:** widen the summary to ≥44px (e.g. restore the "Menu" label, or add
  horizontal padding to the icon-only button). Re-measure at 390/320 on all pages.

### V-P2-4 — "Read the intro ↓" link is 142 × 31px at 390/320 — below the 44px floor, on all 34 pages
- **Measured:** `.hero-intro-more` = **142 × 30.6px**, `display: block`, 18px text,
  0 padding. It is the only way to read a capped mobile hero intro (intro cap
  itself works — home 90→450px, cost 90→360px on click, verified).
- **New element in this round** (L-11); the 44px gate applies to it as a
  non-inline link. It is 142px wide, so mis-taps are unlikely, but its height
  is 13px under the floor on every page at mobile widths.
- **Fix:** give it min-height 44px (padding) so the tap area meets the floor
  without changing its words or position. Re-measure at 390/320.

---

## P3 DEFECTS

### V-P3-1 — Mobile header phone-icon button is 38 × 38px at 390
- Measured `.header-call-icon` = 38 × 38px at 390 (hidden at 320 — 0 × 0, the
  bottom call bar serves 320). The L-9 brief explicitly ordered a 38 × 38px
  button, so this is a brief-vs-gate conflict, not a worker slip — and the
  full-width bottom call bar is a compliant alternative affordance on every
  page. Owner call: keep 38px (accept the brief's size) or bump to 44px.

### V-P3-2 — H1 ends on a 1-word line at 320px on /contact/ + /about/ ("Pros")
- Measured last-line word counts at 1440/390/320 on all 34 pages: every page
  ends on a ≥2-word line at all widths **except** /contact/ and /about/ at
  320 ("Pros", ratio 0.38 / 0.45). Confirms Worker 1's own flag
  (FINDINGS-10x-design.md §7.3). Cosmetic, 320px only. Fix would be a nowrap
  span on "Restoration Pros" (Worker 1 declined a third hand-tune; owner call).

### V-P3-3 — Kind/help card body text is 18px (L-7 brief-ordered), below the 20px floor
- Measured `.kind-card p` / `.help-card p` = **18px** on home + about (all widths).
  The L-7 brief ordered "2-line body 18px/1.55" and Worker 1 implemented it as
  ordered + flagged it. Prose `p`/`li` elsewhere is ≥20px (min-prose scan found
  only the 13px eyebrow label below 20px). Owner call if the 20px floor is
  literal for card bodies.

### V-P3-4 — Trust-row third item falls back to the place line on pages without "written scope" in copy
- Worker 1's rule: trust = "Answered 24/7" + readings item + "Written scope
  before rebuild" if the copy says "written scope", else the footer place line.
  On pages without it (e.g. /cost/, /burst-pipe/, /contact/) the row reads
  "Answered 24/7 · Moisture readings taken · Fort Myers · Lee County, FL" —
  coherent, all the page's own words, but the third item is location info, not
  a trust signal. Polish only; the brief's copy-only rule leaves no better
  third item without new words.

### V-P3-5 — /contact/ hero ghost button links to /contact/ itself (self-link in chrome) — PRE-EXISTING, not this round
- The hero ghost "Describe your water problem" → /contact/ renders on
  /contact/ itself (1 occurrence in `<main>`). Verified pre-existing:
  `git show HEAD:site/includes/functions.php:346` already rendered it in the
  five-fix build. The 20x audit's "0 self-links" scoped to prose copy; this
  is CTA chrome. Not a round defect; listed so it is not mistaken for one.
  (Same pattern explains the home/about `/contact/` ×2 counts: hero ghost +
  closing ghost are CTA chrome, not prose — prose duplicates are 0 everywhere.)

---

## GATES — ALL RE-MEASURED (export: `python3 qa/export_cloudflare.py out`, exit 0)

| Gate | Result |
|---|---|
| Routes 200 | **34/34** (local server + export log); 33/33 no-slash → **308** in `_redirects` (33 lines); bogus → custom 404 (export-verified 404.html); sitemap **31 locs**, all lastmod 2026-11-19, 0 legal; robots + llms.txt + llms-full.txt 200 (llms-full 424,863 B, 31 pages) |
| Word-diff vs pastes | **0 UNAUTHORIZED on 34/34.** 103 UNMATCHED regions adjudicated (89 by script + 14 manual — all authorized: dedup/Related-trim fragments, W2 replacement fragments, the how-it-works dedup+chip interleave); 585 insertion regions inventoried — every one is a Worker-1/closer addition (kickers, eyebrow, trust, utility line, closing trust, "Read the intro ↓", map-poster caption, cost chip + range-bar labels, step chips, area-map strips) or chrome (breadcrumb, hero/ghost buttons, "Last updated"); Related p_ok + b_ok **True on 27/27** |
| H1 | Exactly **1 on 34/34** at 1440/390/320 |
| /areas/ outline | H1 → H2s, **H2 17 / H3 0 in `<main>`**; card titles 23px terracotta, `::before` none, "North Fort Myers" one line at 1440 |
| Schema | `qa/validate_schema.py out` → **ERRORS 0, WARNINGS 0**, NOTES 3 (publisher logo only — Article-image notes gone). Article `image` present on /cost/, /insurance/, /how-it-works/. BreadcrumbList every ListItem has `item` (validator). FAQPage inside `@graph` — visible = schema |
| Overflow | **0 at 320/390/1440 on 34/34**, measured in-view after stepwise scroll (content-visibility-safe). (Off-screen TH rects in the raw scan are a content-visibility artefact — tables verified separately in-view.) |
| Tables | **81 tables, 0 overflow at 1440/390/320**, stacked-card layout ≤620px. C-02 worst 8 (home t2, water-removal t2, ceiling-leak t0, mobile-home t2, burst-pipe t0, cast-iron t2, slab-leak t1, cost t3) + C-04 spot 10 (north t0, ceiling-leak t1, how-it-works t1, floors t0, bonita t0, cast-iron t0, insurance t0, condo-leak t2, vacant-home t1) — all 0 at 390 and 320. td/th **20px at all widths**; /cost/ prices fit at 390 (stacked cards, "About $1,200 to $3,500" + MOST COMMON chip visible) |
| 20px floor | td/th 20px everywhere; prose p/li ≥20px except the deliberate 13px eyebrow label and the 18px card bodies (V-P3-3) |
| Contrast ≥4.5:1 | **0 rows below 4.5:1** across 7 sampled pages (gradient-aware re-measurement). Worst changed elements: sec-kicker gold-on-deep **5.20**, map-poster **5.20**, closing-trust **6.19** (worst-case on teal end #0B5563), H2 lagoon #0B3D4E **10.41–11.72**, H3 terracotta #93380E **7.47**, area-card titles **7.47**, area-map chips **9.38**, caption **15.64**, utility line **7.44**. Hero scrim composite computed independently from the CSS gradient (0.92/0.78/0.38/0.22 over pure-white photo pixel): at the 0.78 stop where the text sits — eyebrow **5.16**, trust **6.14**, H1 **8.36**; at 0.92 — 8.32 / 9.90 / 13.47 |
| Tap targets | **3 sub-44 at mobile** (V-P2-3, V-P2-4, V-P3-1); **0 at 1440** (min 44px, brand link). Full-page tap audit (no in-view filter, 6 sampled pages × 390/1440) confirms exactly these 3 |
| Links | **0 broken** internal hrefs, **0 duplicate prose targets**, **0 prose self-links**; related exactly **3 on 27/27** pages that have one; FAQ **308 visible = 308 schema**; phone only 239-356-3708 (+1-239-356-3708, tel:+12393563708) except the paste-verbatim FL DFS helpline 1-877-693-5236 on /insurance/ |
| ?v=3 | **34/34** pages (68 files incl. flat .html duplicates); no other CSS version |
| Dashes | **0** em/en dashes in rendered HTML on 34/34 (incl. the "ZIPs 33904-33993" hyphen) |
| Hero call button @320 | **58.8px tall, one line, on 34/34** (was 86px wrapped). Mobile hero intro 3-line cap + "Read the intro ↓" **works** (home 90→450px, cost 90→360px on click, verified) |
| L-10 strips | Both render: real OSM map **1200×560**, 2px gold border, 14px radius, captions verbatim ("Cape Coral and the Lee County service area" / "Fort Myers Beach and the Lee County service area"), OSM attribution present, "View larger map ↗" **1 each** (google.com/maps?q=Cape+Coral,+FL / ?q=Fort+Myers+Beach,+FL), **3 chips each** (Cape Coral: "400+ miles of canals · ZIPs 33904-33993 · Slab homes"; FMB: "Estero Island · ZIP 33931 · Elevated homes") |
| About | **7 help cards in correct order** (emergency → drying → sewage → flood → leaks → **floors/cabinets** → property-types); idx 5 = `about-floors-cabinets.jpg` (curled vinyl plank + moisture meter, viewed); homepage **unchanged** (idx 5 still the street photo `help-every-property.jpg`; `about-floors-cabinets` 0× on home). About **0 word changes** to copy (diff regions on /about/ are Worker-1 additions only) |
| Images | Slot sizes measured (width AND height): lehigh hero box 1440×668 desktop / 390×656 mobile, north 1440×738 / 390×719, home 390×896, cost 390×719. Weights (exact bytes): lehigh **250,336 B (244.5 KiB)**, north **254,283 B (248.3 KiB)** — see note below; 640w variants 68,707 / 67,084 B. **640w currentSrc picked at 390px on lehigh + north** (2.46× over-download gone). EXIF GPS present on **12/12** new/changed files with correct values + 0 AI markers + no Software tag (piexif). Reuse net: log `qa/reuse-net-10x.log` exists, script does fresh `find` + fresh reads, **68,237-file corpus, md5 0 hits excl. self, aHash nearest non-self d16 41–82**, the one d8=6 flag adjudicated (Pleasant Grove Utah mountain landscape — not a reuse). Net NOT re-run (nothing smelled) |
| Console/page errors | **0** across all renders (102 page loads) |
| Screenshots | **117 files in `qa/screenshots-10x-round/`** (42 full-page: 14 changed pages × 1440/390/320; 60 first-viewport: 20 remaining pages × 1440/390/320; 2 mobile-header; 13 element shots). Viewed: mobile heroes (home/cost/burst-pipe/contact @390), map strips (both, 1440 + 390), About + home help grids, areas grid, cost prices @390, how-it-works steps, full pages home/cost/areas/how-it-works @1440 (downscaled), first viewports (burst-pipe/contact @390, privacy @1440). Empty table/FAQ boxes in full-page captures are the documented content-visibility screenshot artefact (Worker 1 §7.8) — tables/FAQs verified separately in-view |

### Weight note (north hero, 254,283 B)
The brief says "≤250KB". 254,283 B = **248.3 KiB** (÷1024) but 254.3 KB (÷1000).
The site's own established convention is ÷1024: the 20x audit calls the
373,306-byte lehigh original "364 KB" and the 348,389-byte north original
"340 KB" — both ÷1024. Under that convention 248.3 KiB **passes**. Recorded
here with exact bytes so the judgement is transparent; not raised as a defect.

### 20x findings — closure status
- **Fixed + verified:** A-2 (areas outline), C-01 (table 20px floor), C-02 + C-04
  (tables 0 overflow), C-03 (hero button one line @320), D-P2-1 (33993 removed
  from Pine Island — verified: 33993 now 1×, in the Cape Coral row only),
  D-P2-2 (sewage + flood help cards linked, dedup delinks verified: each 1×
  in `<main>`), B-P3-1 (Article image on cost/insurance/how-it-works),
  D-P3-3 (footer comment shortened), D-P3-5 (sewage help photo swapped —
  PPE + dark water, viewed), D-P3-6 (3/4 legal heroes swapped — insurance /
  terms / disclaimer; privacy left, see open decisions), D-P3-7 (drying
  sentences localised on 7/7 pages + sign-offs reworded on 3/6, verbatim
  old→new pairs verified), D-P3-8 (lehigh/north ≤250 KiB + 640w variants),
  A-3 (15 alts trimmed, 0 over 125 — longest exactly 125), L-1 (directional
  scrim, photos breathe), L-2 (eyebrow + trust), L-3 (H1 balance — except
  V-P3-2), L-4 (banding), L-6 (kickers + H2/H3 scale + new palette), L-7
  (cards, except V-P3-3), L-8 (flat buttons), L-9 (header — except V-P2-3 /
  V-P3-1), L-10 (map strips), L-11 (mobile hero — except V-P2-4), L-12
  (utility line), L-13 (steps spine + chips on 6/9 steps), L-14 (closing
  band), L-15 (cost highlight + range bar), L-16 (home/cost re-crops),
  L-17 (palette), L-18 (map poster fallback).
- **NOT fixed in this round (carried, pre-existing):** A-1 (apex canonical host
  still serves the stale old site — deployment/DNS matter, no code change;
  re-verify apex after DNS propagates; NOT re-checked here — local-only
  verification cannot reach the apex host).

---

## WHAT CHANGED vs THE FIVE-FIX BUILD (files + counts)

- **38 site files:** 32 modified + 6 new.
  - Modified: `site/assets/css/styles.css`; 15 images (hero-home/cost/
    insurance/terms/disclaimer + their 960w variants, hero-lehigh-acres/
    north-fort-myers + 960w, help-sewage-cleanup); `site/includes/functions.php`,
    `header.php`, `footer.php`; 13 data files (`about.php`, `areas.php`,
    `bonita-springs.php`, `cape-coral.php`, `estero.php`, `fort-myers-beach.php`,
    `homepage.php`, `lehigh-acres.php`, `media-manifest.php`,
    `mobile-home.php`, `north-fort-myers.php`, `vacant-home.php`,
    `water-heater-leak.php`).
  - New: `hero-lehigh-acres-640w.jpg`, `hero-north-fort-myers-640w.jpg`,
    `help-property-types.jpg`, `about-floors-cabinets.jpg`,
    `map-cape-coral.jpg`, `map-fort-myers-beach.jpg`.
- **Word-diff whitelist (exact):**
  - Worker 2 (content): 7 drying-sentence replacements (old "…run with readings
    logged daily…" → per-page localised sentences, `run` removed); 3 sign-off
    rewordings (bonita-springs / estero / north-fort-myers); ZIP tokens:
    −33993 (Pine Island), +33923 (Bonita Springs — **V-P2-1**), +33932
    (Fort Myers Beach, paste-sourced); 0 word changes for the homepage link
    moves (href-only + one segment merge).
  - Worker 1 (design, added words only): per-H2 kickers (group label —
    Services/Areas/Guide/About/Fort Myers, repeats per H2); hero eyebrow
    ("Fort Myers · Lee County, FL" / "<Area> · Lee County, FL" /
    "Emergency Service · Answered 24/7"); hero trust items ("Answered 24/7"
    + readings item + "Written scope before rebuild" / "Photos and moisture
    logs" / place-line fallback); utility line ("Answered 24/7 · Call
    239-356-3708"); closing trust ("Answered 24/7, including holidays and the
    days after a storm" — brief-given verbatim); ghost-button text
    "Describe your water problem" (pre-existing chrome, now also in the
    closing band); "Read the intro ↓"; map-poster caption ("Map loading ·
    Fort Myers & Lee County"); cost "Most common" chip + range-bar labels
    ("Most Fort Myers jobs land here", $500–$15,000 from the table); step
    chips on how-it-works (6: "One short phone call", "Usually at the first
    visit" ×2, "Usually the first day" ×2, "About 3 to 5 days" — verbatim
    from the page's own stage-times table).
  - Closer: area-map strip text on cape-coral + fort-myers-beach (captions,
    "View larger map ↗", "© OpenStreetMap contributors", 6 chip texts —
    facts from each page's copy; "ZIPs 33904-33993" uses a hyphen per the
    0-dash rule); About `about-floors-cabinets` alt (109 chars).
  - Chrome (pre-existing, not new words): breadcrumb ("Home" + group + H1),
    hero "Call 239-356-3708", "Last updated: November 19, 2026" (legal).
  - Every added string's words come from words already on that page, except
    the brief-given items named above (L-14 trust line, "Read the intro ↓",
    "Map loading" caption, "Most common" / "Most Fort Myers jobs land here"
    labels) and the W2 sign-off words ("For the claim", "If a claim is
    involved", "For typical/ballpark costs", "Questions about a claim?",
    "Wondering what it costs?").

## CONTRAST TABLE (re-measured, worst case per element)

| Element | Foreground on background | Ratio |
|---|---|---|
| H2 lagoon #0B3D4E | white / sand #F6F1E7 | 11.72 / 10.41 |
| H3 terracotta #93380E | white / sand | 7.47 / 6.63 |
| H2 white (deep band) | teal end #0B5563 (worst stop) | 8.42 |
| Eyebrow gold #E8C87A | deep #0A2E38 | 8.88 (5.16 worst-case composite at the 0.78 scrim stop over white) |
| Trust #CFE0E4 | deep | 10.57 (6.14 worst-case composite at 0.78) |
| Kicker teal #0B5563 | white / sand | 8.42 / 7.48; gold-on-deep 5.20 |
| Utility muted #46585F / teal link | white | 7.44 / 8.42 |
| Step chip teal on sand | #0B5563 on #F6F1E7 | 7.48 |
| "Most common" chip white on coral | #FFFFFF on #C2410C | 5.18 (Worker 1) |
| Area-map caption ink on white | #12262E | 15.64 |
| Area-map link teal / attr muted / chips teal-dark on sand-2 | — | 8.42 / 7.44 / 9.38 |
| Map poster gold-light on teal gradient | #E8C87A on #0B5563 | 5.20 |
| Closing trust #CFE0E4 on deep band | teal end #0B5563 (worst) | 6.19 |
| Closing intro #EEF4F5 on deep band | teal end (worst) | 7.58 (Worker 1) |
| Details-sub teal-dark on sand | #083F4A on #F6F1E7 | 10.25 |
| Cost highlight TD teal-dark on #FDF8EC / price gold on deep | — | 14.76 / 5.64 (Worker 1) |
| Area-card title terracotta on white | #93380E | 7.47 |

## SCREENSHOT INDEX (`qa/screenshots-10x-round/`, 117 files)

- Full-page (42): 14 changed pages × 1440/390/320 — home, areas, cost, about,
  cape-coral, fort-myers-beach, insurance, terms, disclaimer, lehigh-acres,
  north-fort-myers, how-it-works, drying, water-removal.
- First-viewport (60): the other 20 pages × 1440/390/320.
- Mobile header (2): home-390-header, cost-390-header.
- Element (13): el-cape-map-1440/390, el-fmb-map-1440, el-about-help-1440,
  el-home-help-1440, el-areas-grid-1440, el-cost-prices-390,
  el-cost-hero-390, el-home-hero-390, el-lehigh-hero-390, el-north-hero-390,
  el-hiw-steps-1440, el-cost-highlight-1440.
- Full-page files exceed the image reader's pixel limit at native size;
  downscaled review copies were made in /tmp (rev-*.png) for viewing — the
  originals in qa/ are the record.

## OPEN OWNER DECISIONS (carried forward — unchanged from the round)

- D-P3-2 Seasonal vs Vacant naming (title "Seasonal Home…" vs slug/H1/anchors
  "vacant") — still his call, nothing renamed.
- D-P3-4 Estero/Bonita shared homepage paragraph + "Leaks of every kind" card
  unlinked — still his call.
- 33945 option for the Pine Island row (auditor's word only, not in any paste)
  — still his call. (Now joined by V-P2-1: remove the unconfirmed 33923.)
- Privacy-policy hero left (laptop + padlock) — no genuinely better topical
  photo exists.
- About "How We Work" photo strip not built — no spec, no zero-word block.
- Live map tiles + live Speed Index still need one real-browser look
  (Google unreachable from this VM; map iframes show the poster locally).
- L-5 (780px prose cap) NOT implemented — contradicts his standing wide-lines
  order; needs his explicit call.
- Mobile brand 17px nowrap + 38px phone icon do not fit at 390px (Worker 1
  shipped 15px/14px brand, mark hidden, icon-only menu — which caused V-P2-3).
- Legal pages have no deep-teal band (no cta-line to anchor L-14 on).
- Step chips on 3/9 how-it-works steps missing — no duration in the copy.
- A-1 apex stale site — re-verify apex after DNS propagates (not re-checked
  in this local-only round).
- NEW from this verification: V-P2-1 (remove 33923), V-P2-2 (D-P3-9 revert),
  V-P2-3/V-P2-4/V-P3-1 (tap-target sizes), V-P3-2 (H1 orphan @320),
  V-P3-3 (card body 18px), V-P3-4 (trust-row fallback).

## EVIDENCE INDEX

- This file: `qa/FINDINGS-10x-round.md`
- Canonical export: `out/` (built by `python3 qa/export_cloudflare.py out`)
- Word-diff: `qa/verify_10x_round.py` + `qa/10x-round-worddiff.json` +
  `qa/adjudicate_10x_round.py` (+ `/tmp/worddiff.log`)
- Static gates: `qa/static_gates_10x_round.py` + `qa/10x-round-gates-static.json`
- Render probe: `qa/probe_10x_round.py` + `qa/10x-round-measure.json`;
  follow-up (tap sizes, gradient-aware contrast): `qa/probe_10x_round2.py` +
  `qa/10x-round-followup.json`; H1-orphan probe `/tmp/orphan.py`
- Schema: `qa/validate_schema.py out` → 34 pages, 92 scripts/nodes, 0/0/3
- Screenshots: `qa/screenshots-10x-round/` (117 files)
- Reuse net (Worker 3, inspected not re-run): `qa/reuse-net-10x.py` +
  `qa/reuse-net-10x.log`

---

# FINAL RE-VERIFICATION (Independent Final Verifier)

- **Date:** 2026-11-20 ~02:00–02:35 PKT
- **Mode:** LOCAL ONLY. No push, no deploy, no DNS/domain changes, no git
  commit. `qa/verify_export.py` NEVER run. The final verifier did not build
  or fix anything — every number below was re-measured independently from a
  fresh canonical export.
- **Method:** own canonical export (`python3 qa/export_cloudflare.py out`,
  exit 0; PHP 8.3.6 + mbstring confirmed present before exporting, no
  reinstall needed); re-ran the first verifier's gate scripts
  (`qa/verify_10x_round.py`, `qa/static_gates_10x_round.py`,
  `qa/adjudicate_10x_round.py`, `qa/validate_schema.py`) + own static
  link/trust/related audit + own Playwright probes (`qa/probe_10x_final.py`,
  `qa/probe_10x_final2.py`, bundled Chromium only, `out/` served on
  127.0.0.1:8142) + pixel-level contrast sampling of the restyled elements.
  Nothing taken on either fix worker's word.

## FINAL VERDICT — READY

**P1 0 · P2 0 · P3 0.** All 9 defects from the first verdict are fixed and
verified fixed; the full re-gate passes with 0 remaining defects of any
severity. The site is READY to push on the owner's word (push itself was not
done and is not part of this verdict).

| Severity | Count | IDs |
|---|---|---|
| P1 (blocking) | 0 | — |
| P2 (visible defect / unverified fact) | 0 | V-P2-1, V-P2-2, V-P2-3, V-P2-4 all PASS |
| P3 (polish) | 0 | V-P3-1, V-P3-2, V-P3-3, V-P3-4, V-P3-5 all PASS |

## PER-FIX VERDICTS

### V-P2-1 (ZIP 33923) — PASS
- `33923` occurs **0×** in `out/` and 0× in `site/data/areas.php`.
  Bonita Springs row renders `<td data-label="ZIP codes">34134, 34135</td>`
  (paste-verbatim). Word-diff confirms the `33923` insertion region is gone
  (/areas/ regions 19 → 18, the only region lost in the whole re-run).

### V-P2-2 (D-P3-9 revert, homepage links) — PASS
- Homepage `<main>`: `/areas/` **1×** (on "ZIP code we cover in our Lee
  County service areas"), `/commercial/` **1×** (help-card "businesses"),
  every other internal target 1×, `href="/"` **0×**, `/contact/` 2× (both
  `.btn-ghost` CTA chrome, pre-existing pattern). 0 duplicate prose targets,
  0 self-links in `<main>` on all 34 pages (own static audit + static gates).

### V-P2-3 (mobile menu button 36px) — PASS
- `.mobile-menu summary` = **44 × 54.6px** at 390 AND 320 on 34/34 pages
  (min across the sweep). Click opens the menu: `open` true, 17 visible
  links on home/cost/contact, 18 on /about/, at both widths (viewed
  `home-390-menu-open.png`: clean list, close × button). Header row fits,
  no overlap, no brand clipping at 390/320.

### V-P2-4 ("Read the intro ↓" 31px) — PASS
- `.hero-intro-more` = **174 × 54.6px** at 390 AND 320 on 34/34 pages.
  Click expands the intro: home 90→450px (390) / 90→570px (320), cost
  90→360 / 90→480, contact 90→240 / 90→300, about 90→300 / 90→360.

### V-P3-1 (phone icon 38px) — PASS
- `.header-call-icon` = **44 × 44px** at 390 AND 320 on 34/34 pages,
  visible at 320 (the old ≤380px `display: none` is gone). Header row fits
  exactly at both widths (390: brand 230 + icon 44 + menu 44 + gaps = 350
  of 350px; 320: 176 + 44 + 44 + gaps = 280 of 280px), brand scrollWidth ==
  clientWidth (no clipping), no overlap. Contrast white on #C2410C =
  **5.18:1**. Desktop keeps the full call button (icon `display: none` at
  1440, as designed).

### V-P3-2 (H1 orphan "Pros" @320) — PASS
- Last-line word counts measured from rendered Range rects (not
  scrollWidth) at 320/340/360/381: /contact/ and /about/ end on
  **"Restoration Pros" (2 words)** at every width; last-word right edge
  287.2px vs viewport 320px, H1 rect right 300px, overflow 0. Home control
  ends "Fort Myers, FL" (3 words). H1 textContent normalises to the exact
  original strings (`Restoration&nbsp;Pros` treated as a space).
  Viewed: `contact-320-vp.png` — no clipping, no 1-word final line.

### V-P3-3 (card body 18px) — PASS
- `.kind-card p` / `.help-card p` compute **20px / 32px line-height** on
  34/34 pages at 1440/390/320; 0 clipped paragraphs. In-view re-check
  (scroll each card into view, defeating the content-visibility artefact
  that made 19 home cards report clipped in the raw sweep): **0 clipped
  card boxes** on home (19 cards) + about (7) at all three widths.

### V-P3-4 (trust-row place-line fallback) — PASS
- Trust rows rendered on 34/34 heroes: **9 pages 3 items, 20 pages 2 items,
  5 pages 1 item** — exactly the fix worker's list; **0 place-line items**
  anywhere. The 5 one-item pages (`/ceiling-leak/`, `/privacy-policy/`,
  `/terms/`, `/disclaimer/`, `/about/`) read "Answered 24/7" alone and read
  cleanly in the viewed screenshots — no second item was invented, per the
  no-invention rule (owner call if a second item is wanted).

### V-P3-5 (/contact/ ghost self-link) — PASS
- /contact/ closing ghost is now `<span class="btn btn-ghost"
  aria-disabled="true">Describe your water problem</span>`; `href="/contact/"`
  **0×** in `<main>` on /contact/ (0× on the whole rendered page).
  Pixel-identical styling vs the link version on /cost/ and home at 1440:
  box **370 × 60.4**, font 22px, bg `rgba(10, 46, 56, 0.25)`, white,
  border `1px solid rgba(255, 255, 255, 0.85)`, padding `16px 28px` — all
  identical; only `cursor` differs (`default` vs `pointer`).

## GATES — ALL RE-MEASURED (fresh canonical export)

| Gate | Result |
|---|---|
| Routes 200 | **34/34** (HTTP check); 33/33 no-slash → **308** in `_redirects` (33 lines; live-server check 301 is the python http.server's own redirect, the export's `_redirects` carries 308); bogus → **404** custom 404.html; sitemap **31 locs**; robots + llms.txt + llms-full.txt (424,185 B) 200 |
| Word-diff vs pastes | **0 UNAUTHORIZED on 34/34.** 103 UNMATCHED regions — the same 14 the first verifier manually adjudicated as authorized (7 drying-sentence replacements, 3 sign-off rewordings, how-it-works dedup+chip interleave ×2, north/estero/bonita sign-offs); 584 INSERTION-REVIEW regions. Region-by-region diff vs the first run is EXACTLY the authorized fix changes: /areas/ `33923` region gone; 20 pages' trust insertion regions shortened by "Fort Myers Lee County FL" (place-line removal). Whitelist = first verifier's + fix workers' changes (ZIP 33923 removal; D-P3-9 revert; `&nbsp;` in /contact/ + /about/ H1s as a space; P3 trust-row item removals — words removed, none added) |
| H1 | Exactly **1 on 34/34** at 1440/390/320 |
| Schema | `qa/validate_schema.py out` → **ERRORS 0, WARNINGS 0**, NOTES 3 (publisher logo only, same as before). FAQ **308 visible = 308 schema** |
| ?v=5 | **68/68** HTML files (34 routes × slash + flat). The static-gates script still hardcodes `?v=3`, so its 68 "fails" are all the stale version check — verified separately that every one is `?v=5` and no other CSS version exists |
| Dashes | **0** em/en dashes in rendered HTML on 34/34 |
| Overflow | **0 at 320/390/1440 on 34/34** (102 page loads, stepwise scroll); **0 console errors** across all loads |
| Tables | **81 tables, 0 overflow** at 1440/390/320; td/th **20px**; /cost/ prices fit at 390 (0 clipped cells, overflow 0) |
| Links | **0 broken** internal hrefs, **0 duplicate prose targets**, **0 self-links** in `<main>` on 34/34; related exactly **3 on 27/27** pages that have one; phone only 239-356-3708 except paste-verbatim FL DFS helpline 1-877-693-5236 on /insurance/ |
| Tap targets | Menu 44×54.6, intro link 174×54.6, phone icon 44×44 at 390/320 on 34/34; hero call button **58.8px, one line** at 320 on 34/34 (scrollH == clientH); hero ghost 56px at 320 |
| Contrast ≥4.5:1 (restyled elements) | Menu button white on header gradient #0a2e38→#0c3340 = **14.38 / 13.43**; phone icon white on #C2410C = **5.18**; card body #12262E on white = **15.64**; intro link gold #ffd9a8 vs local scrim background, pixel-sampled: home median **8.44** (p99 4.75), cost median **12.87** (p99 9.15), contact median **8.48** (p99 5.45); H1 white vs local background, pixel-sampled: medians **8.96–16.65**. No fix changed any colour — the first round's gradient-aware pass (0 rows below 4.5:1) stands. NOTE: two early probe runs gave nonsense ratios (1.0–1.7) for the header/hero elements because the walk-up found the body-white background behind the header gradient / hero scrim overlay; the pixel-sampled values above are the record. H1 ring-sample p90 tails at 390 (3.79–4.45) are glyph anti-aliasing fringe pixels, not background — medians 9–10 and the viewed renders are clearly readable |
| Hero images | **640w currentSrc picked at 390** on lehigh-acres + north-fort-myers (files verified on disk 640×426, 68,707 / 67,084 B; full files 1440×960). NOTE: headless-shell reports `naturalWidth` 390 for these files — a shell quirk, not a file problem (PIL confirms 640×426); the material gate (640w variant served at 390) passes |
| L-10 strips | Both render: map images 1200×560 shown on /cape-coral/ + /fort-myers-beach/ |
| About | **7 help cards in correct order** (emergency → drying → sewage → flood → leaks → floors/cabinets → property-types); idx 5 = `about-floors-cabinets.jpg`; homepage unchanged (idx 5 still `help-every-property.jpg`) |
| Screenshots | **104 files in `qa/screenshots-10x-final/`** (42 full-page: 7 fixed pages × 1440/390/320; 54 first-viewport: 27 remaining pages × 1440/390; 8 menu-open). Viewed: home 390/320/1440, contact 390/320, about 390, areas 390/1440, cost 390, cape-coral 390, fort-myers-beach 390, ceiling-leak 390, home-390-menu-open. All clean — no clipping, no overlap, no overflow, H1s readable, trust rows clean |

## NOTES / NON-DEFECTS FOUND WHILE VERIFYING

- The static-gates script (`qa/static_gates_10x_round.py:35-36`) hardcodes
  `?v=3`; it was not updated for the `?v=5` bump. Its 68 fails are the
  stale check only — all other gates in that script pass (H1, dashes, links,
  self-links, duplicates, related, FAQ, Article image, alt lengths, map
  strips, /areas/ outline). Left as-is (the script is the first verifier's
  record); the `?v=5` count was verified independently (68/68).
- The first verifier's "card boxes clipped" raw-sweep reading (19 on home)
  is a content-visibility artefact: cards off-screen report their 80px
  placeholder height. In-view measurement is the record (0 clipped).
- The P3-fix worker's note stands: /about/ help cards are title-only by the
  page's own data (each `<p>` is just the link text); nothing is missing.
- The export log warns `rcssmin not installed, styles.css shipped
  unminified` — pre-existing, same as the first round; not a defect.

## OPEN OWNER DECISIONS (carried forward — unchanged)

- D-P3-2 Seasonal vs Vacant naming — still his call, nothing renamed.
- D-P3-4 Estero/Bonita shared homepage paragraph + "Leaks of every kind"
  card unlinked — still his call.
- 33945 option for the Pine Island row — still his call.
- Privacy-policy hero left (laptop + padlock) — no genuinely better topical
  photo exists.
- About "How We Work" photo strip not built — no spec, no zero-word block.
- 5 one-item trust pages ("Answered 24/7" alone) — owner call if a second
  item is wanted; nothing was invented.
- Live map tiles + live Speed Index still need one real-browser look.
- L-5 wide-lines cap not implemented — contradicts his standing wide-lines
  order; needs his explicit call.
- A-1 apex canonical host still serves the stale old site (deployment/DNS
  matter, not re-checked — local-only verification cannot reach the apex host).

## EVIDENCE INDEX (final verification)

- This file: `qa/FINDINGS-10x-round.md` (final section)
- Canonical export: `out/` (built by `python3 qa/export_cloudflare.py out`,
  exit 0; local test server on :8142 killed after the probe, confirmed down)
- Word-diff: `qa/verify_10x_round.py` → `qa/10x-final-worddiff.json`;
  adjudication: `qa/adjudicate_10x_round.py` (103 UNMATCHED, same 14
  authorized); first verifier's originals preserved as `qa/10x-round-*.json`
- Static gates: `qa/static_gates_10x_round.py` →
  `qa/10x-final-gates-static.json` (68 fails = stale `?v=3` check only)
- Render probes: `qa/probe_10x_final.py` → `qa/10x-final-measure.json`
  (127 keys); `qa/probe_10x_final2.py` → `qa/10x-final-followup.json`
  (85 keys); pixel-contrast scripts in `/tmp` (`pixel_contrast.py`,
  `word_rects.py`, `clean_intro.py`, `ghost_check.py`)
- Schema: `qa/validate_schema.py out` → 34 pages, 92 scripts/nodes, 0/0/3
- Screenshots: `qa/screenshots-10x-final/` (104 files)
