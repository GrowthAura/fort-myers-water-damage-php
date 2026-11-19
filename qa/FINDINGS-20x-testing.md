# 20X TECHNICAL TESTING + BLUNDER HUNT — Fort Myers PHP Site

- **Project:** `~/workspace/fort-myers-php/` — five-fix build, main `8cf8cb7` + cloudflare-pages `19992fd`
- **Live base audited:** https://fort-myers-water-damage-php.pages.dev (parent-verified byte-identical to local `out/`)
- **Date:** 2026-11-19 ~22:21–23:00 PKT · **Mode:** audit-only, READ-ONLY (no file edited, nothing pushed/deployed, `qa/verify_export.py` never run)
- **Ordered by:** owner ~22:20 PKT ("20 min tak live hojaye ga, tab tak 20x best ever testing, technical testing, blunder, each and everything, end level") + bar raised ~22:27 PKT (luxury / top-class lens)
- **Scope:** all 34 pages (31 sitemap + 3 legal), A-to-Z, no page skipped
- **Method:** 5 parallel workers — A live/links/SEO, B content+schema, C rendering, D technical/blunder-hunt, E luxury. Live tested with curl; rendering done locally against `out/` served on 127.0.0.1 (VM Chromium cannot reach pages.dev directly — `ERR_TUNNEL_CONNECTION_FAILED` — so no live visual check is claimed; served bytes are byte-identical to live). Playwright bundled Chromium only. Homepage is ~22,251px desktop / ~34,892px mobile (taller than the 17,876px quoted in the brief — five-fix build), shot as labelled slices, never called full-page.

## VERDICT

**P1 1 · P2 6 · P3 16 · + 18 ranked luxury upgrades.** The pages.dev build itself is in strong shape: word-diff 0 unauthorized, schema 0/0, console 0, overflow 0, contrast ≥4.5:1, all images relevant. The single P1 is not a code defect — it is the apex canonical host still serving the stale old Next.js site (domain attach + DNS pending at audit time). The 6 P2s are all real, fixable, and visible. The luxury list is where "end level" still has headroom: the site is correct and legible but reads as a competent template, not a premium brand.

| Severity | Count | IDs |
|---|---|---|
| P1 (breaks page / ranking / trust) | 1 | A-1 |
| P2 (visible defect) | 6 | A-2, C-01, C-02, C-03, D-P2-1, D-P2-2 |
| P3 (polish) | 16 | A-3, B-P3-1, C-04, C-05, C-06, C-07, C-08, D-P3-1…D-P3-9 |
| Luxury upgrades (ranked) | 18 | L-1…L-18 |

---

## P1 — 1 finding

### A-1 — Apex canonical host still serves the STALE old (Next.js) site
- **Pages/URLs:** https://fortmyerswaterdamagerestoration.us/about/ (in sitemap), all 34 `og:image`/`twitter:image` URLs, https://fortmyerswaterdamagerestoration.us/assets/css/styles.css?v=2, https://www.fortmyerswaterdamagerestoration.us/
- **Evidence (curl, 2026-11-19):** apex `/about/` → **404** (pages.dev 200, md5-identical to local `out/about/index.html`); apex sitemap has **30 locs** (missing exactly `/about/`); all 34 og/twitter image URLs **404 on apex** (200 on pages.dev); `styles.css?v=2` **404 on apex** (200 on pages.dev); apex home is 125,635 bytes with `/_next/static/` links (Next.js) vs 65,396-byte Pages home (md5 `36ff3857…`); www → curl **000**.
- **Why P1:** canonicals, the sitemap, and every og:image point at the apex host. Google following the sitemap hits a 404 on `/about/`; every social share gets no image; anyone landing on apex gets the old site.
- **Status note:** the owner confirmed the domain attach (apex only, dashboard) at ~22:27 PKT, during this audit — Worker A's curls predate/overlap the attach, and DNS propagation takes time. **Re-verify apex after DNS propagates** (`/about/` → 200, apex sitemap → 31 locs, apex hero image → 200, www stays unattached per his apex-only order). **No code change in this repo.**

---

## P2 — 6 findings

### A-2 — /areas/ skips heading levels: H1 followed directly by H3s
- **Page:** https://fort-myers-water-damage-php.pages.dev/areas/
- **Evidence:** outline is H1 "Water Damage Help Across Lee County, FL" → H3 "Lee County Service Areas and ZIP Codes" → 10 more H3s (Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, Fort Myers Beach, Sanibel and Captiva, Pine Island and Matlacha, Estero, Bonita Springs, San Carlos Park/Gateway/Iona) → first H2 only after that. All other 33 pages: heading order clean.
- **Fix:** promote the table heading + the 10 area headings on /areas/ from H3 to H2 (keep the visual size via class if the H3 look is wanted). One-page change, then re-export + re-gate headings on all 34 pages.

### C-01 — Table cells below the 20px floor on 30/34 pages
- **Pages:** every page with a table (30 pages; only /about/, /privacy-policy/, /terms/, /disclaimer/ are clean at 20px). Worst: /cost/ (`td` "Small spill caught early", `td` "From about $500").
- **Evidence:** prose-only min font 18px @390 / 19px @1440 on 30 pages (`qa/20x-c-data2.json`); CSS `table{font-size:19px}`, `@media(max-width:620px){table{font-size:18px}}`, `th{font-size:18px}`. Paragraphs/li are 20px everywhere — only tables are short. The five-fix "body 20px" check measured computed `body` font only, so this slipped through.
- **Fix:** `table{font-size:20px}` at both breakpoints (and `th` 20px). Re-check /cost/ prices still fit at 390 after the bump — the prices table was narrowed to fit at 19px, so it may overflow again at 20px (see C-02).

### C-02 — 8 tables overflow at 390 with a whole column hidden at first view
- **Pages / hidden width @390 (in-view measurement):** home table2 **142px** (4th column "What usually happens" entirely off-screen) · /water-removal/ table2 **138px** ("Read more" hidden) · /ceiling-leak/ table0 **127px** ("Who fixes the source" hidden) · /mobile-home/ table2 **104px** ("Can it be dried?" hidden) · /burst-pipe/ table0 **93px** ("What to watch for" hidden) · /cast-iron-pipe/ table2 **88px** ("Good to know" hidden) · /slab-leak/ table1 **74px** ("When it usually fits" hidden) · /cost/ table3 **45px** ("Effect on the price" partly hidden).
- **Evidence:** `qa/20x-c-tables.json` (all 81 tables, in-view widths); screenshots `qa/screenshots-20x-testing/c/table-ceiling-leak-390-0.png` (3rd-column text sliced mid-word), `table-burst-pipe-390-0.png` (4th column entirely off-screen). Tables scroll (`overflow-x:auto` + inset shadow), so content is reachable by swiping — but at first view the table looks cut. Same class as D-V1 in the 20x round (/cost/ prices hidden at 390 → P2, fixed); these 8 did not get the same treatment.
- **Fix:** same treatment D-V1 got — narrow the 4-column tables at ≤620px (shorter headers, tighter cell padding) or convert the widest to stacked rows; re-measure **in view** (off-screen `scrollWidth` lies under `content-visibility:auto` — see Method note in part C).

### C-03 — Hero call button wraps the phone number across two lines at 320px (all 34 pages)
- **Pages:** all 34 (same hero CTA markup). Also the final CTA "Call 239-356-3708, answered 24/7" on 31 pages.
- **Evidence:** screenshots `qa/screenshots-20x-testing/c/firstvp-home-320.png`, `firstvp-burst-pipe-320.png`, `firstvp-cost-320.png` — button reads "Call 239-356- / 3708"; measured heights: hero button **86px @320 vs 61px @390** on 34/34 pages; final CTA **115px @320 vs 89px @390** on 31/31 pages. At 390 the hero button is one line. The fixed bottom call bar still shows the number on one line at 320, so a clean call affordance exists — the hero button itself is what looks broken.
- **Fix:** `white-space:nowrap` on `.hero-ctas .btn` and `.cta-line .btn` at ≤380px, or shrink the hero CTA to 19px / drop the "Call " prefix at ≤380px so `239-356-3708` fits one line.

### D-P2-1 — /areas/ ZIP table assigns 33993 to "Pine Island and Matlacha" — 33993 is Cape Coral
- **Page:** /areas/ — "Lee County Service Areas and ZIP Codes" table.
- **Evidence:** row `Pine Island and Matlacha | 33922, 33956, 33993 | Storm surge, mobile homes, seasonal homes`. 33993 is a Cape Coral ZIP and is already listed in the same table under `Cape Coral | 33904, 33909, 33914, 33990, 33991, 33993`. Pine Island / Matlacha ZIPs are 33922 (Bokeelia), 33945 (Pineland), 33956 (St. James City / Matlacha) — 33993 belongs to none of them.
- **Fix:** remove `33993` from the Pine Island and Matlacha row (optionally add `33945` for Pineland if the row is meant to cover all of Pine Island).

### D-P2-2 — Two homepage help cards name existing service pages but are not clickable, while their 4 sibling cards are
- **Page:** homepage `/` — "What we help with" help grid (`article.kind-card.help-card`).
- **Evidence:** 6 help cards; 3 link (Emergency water removal → /water-removal/, Structural drying → /drying/, Every kind of property → /commercial/), 3 have no link at all (Sewage backup cleanup, Flood and storm cleanup, Leaks of every kind). The first two name exact existing pages — /sewage-cleanup/ and /flood-cleanup/ — so a user tapping the card expecting the service gets nothing, unlike the linked siblings. (0 `href` inside those two card blocks.)
- **Fix:** link "Sewage backup cleanup" → /sewage-cleanup/ and "Flood and storm cleanup" → /flood-cleanup/ in the same pattern as the sibling cards. "Leaks of every kind" has no single target — leave unlinked (see D-P3-4) or link it to /water-removal/.

---

## P3 — 16 findings

### A-3 — 15 alt texts exceed the ~125-character screen-reader guidance (longest 157)
- **Pages:** home hero + 14 inner heroes (full list in `qa/20x-part-a-raw/audit-run-2.log`).
- **Evidence:** longest: home hero 157 chars ("A restoration technician extracts standing water from a tiled living room floor in a bright Florida home, with palm trees visible through sliding glass doors"); also >125: water-removal 150, drying 145, condo-leak 153, flood-cleanup 146, vacant-home 139, north-fort-myers 137, sewage-cleanup 130, lehigh-acres 131, areas 129, mobile-home 127, slab-leak 127, ac-leak 126, cape-coral 126. 30 of 46 alts are >100 chars. Counter-evidence: 0 missing, 0 empty, 0 filename-stuffed alts.
- **Fix:** trim the 15 hero alts to ≤125 characters (cut trailing scene detail, keep subject + place).

### B-P3-1 — Article schema has no `image` on 3 pages, and the validator's "by design" reason is stale
- **Pages:** /cost/, /insurance/, /how-it-works/.
- **Evidence:** `validate_schema.py` emits "Article: no 'image' (by design — heroes honestly empty; no photo passes licence+place+subject)" per page. That reason is no longer true: the hero round filled every hero — `out/assets/img/hero-cost.jpg` (149,702 B), `hero-insurance.jpg` (130,600 B), `hero-how-it-works.jpg` (181,108 B) — and each renders in the page hero. Google lists `image` as required for the Article rich result, so these 3 pages cannot earn it as written. (The companion note, "publisher has no logo", still holds — only the SVG favicon mark exists.)
- **Fix (owner call):** add `"image"` (absolute URL of the page's hero image) to the 3 Article schemas. This deviates from the paste schema, so it needs the owner's word; do not add silently. Alternatively leave as-is and accept no Article rich result on these 3 pages.

### C-04 — 10 more tables overflow 2–28px at 390; 41 tables overflow at 320
- **Evidence:** @390: /north-fort-myers/ table0 28px · /ceiling-leak/ table1 25px · /how-it-works/ table1 19px · /floors/ table0 16px · /bonita-springs/ table0 14px · /cast-iron-pipe/ table0 9px · /insurance/ table0 5px · home table0, /condo-leak/ table2, /vacant-home/ table1 2px each. @320: 41 tables overflow (worst home table2 212px). (`qa/20x-c-tables.json`.)
- **Fix:** fold into the C-02 pass; the 2–9px cases are a sliver of the last cell's padding and visually negligible — the ≥14px ones are worth the same narrowing. At 320, swipe-inside-table is the accepted fallback pattern, so this stays P3.

### C-05 — Chrome/label text below 20px (deliberate styles — owner's call whether the floor is literal)
- **Inventory @390 (all pages unless noted):** `.details-sub` eyebrow **14px** mobile / 15px desktop on 26 pages (includes full-sentence labels, e.g. /insurance/ "Usually covered by homeowners insurance?"); footer column links **18px**; footer-base + back-to-top **17px**; breadcrumb **18px**; nav links **17–18px**; brand tagline **14px** (desktop); nav-group labels **14px**; `.hero-areas` **18px**; `.map-link` **18px**.
- **Fix (only if the 20px floor is meant literally for every rendered glyph):** raise these to 20px / 18px-minimum. If the floor covers prose only, no action — this is a scope question, not a rendering break.

### C-06 — 13 kinds photo-card H3s have no 44px gold rule (white, by CSS design)
- **Page:** / (home) — the 13 `.kind-card.has-photo` H3s. Measured: color `rgb(255,255,255)`, `::after` width `auto`, background `none` — while the other 211 main H3s are teal + 44px gold rule. CSS `.page-body h3:not(.kind-card h3)::after` explicitly excludes them; they read fine as-is.
- **Fix (only if "every H3" was literal):** add the 44px gold `::after` to `.kind-card.has-photo h3` too. If the exclusion is intended, no action — owner's call.

### C-07 — Footer is very tall on mobile (1,774px @390)
- **Pages:** all except the 7 area pages (1,472px @390 — area pages have no footer map iframe; that 302px gap is the map + margins, not a defect).
- **Evidence:** stacking is clean (brand → map → Services 7 → Explore 9 → base), no clipping or ragged edges (`qa/screenshots-20x-testing/c/footer-full-home-390.png`).
- **Fix (optional, design call):** slim the mobile footer (e.g. 2-column link grid, smaller map height). Nothing is broken.

### C-08 — Footer column links sit exactly at the 44px tap-target floor
- **Pages:** all 34. Measured minimum non-inline tap target is **44px** on every page at 390 and 1440 — the footer links (18px × 1.45 lh + 18px padding = 44.1px). Passes, with zero margin.
- **Fix (optional):** raise `.footer-col a` padding to `10px 0` (≈46px) so a future font/padding trim cannot push it under 44px.

### D-P3-1 — /areas/ ZIP table omits two real ZIPs
- **Evidence:** Bonita Springs row lists `34134, 34135` but omits `33923` (also Bonita Springs). Fort Myers Beach row lists `33931` only but omits `33932` — and the Fort Myers Beach page itself mentions 33932.
- **Fix:** add `33923` to the Bonita Springs row and `33932` to the Fort Myers Beach row.

### D-P3-2 — "Seasonal Home" vs "Vacant Home" label mismatch on the vacant-home page (his call, carried from the hero round)
- **Evidence:** `<title>` is "Seasonal Home Water Damage Fort Myers | Came Back to a Leak?" and og/twitter titles match, while the slug is /vacant-home/, the H1 is "Water Damage Found After Returning to Your Fort Myers Home", all 20 in-site anchors say "water damage in vacant homes", and the kinds card says "Came back to a wet or musty seasonal home". The footer no longer links the page at all (five-fix round), so the mismatch is now title-only — but the title is the ranking label.
- **Fix:** his call — either retitle to "Vacant Home Water Damage Fort Myers …" to match slug/H1/anchors, or keep "Seasonal Home" deliberately and align the H1/anchors to it. Do not change silently; it is a naming decision.

### D-P3-3 — Footer still carries an HTML comment naming the removed "Areas We Serve" column (all 34 pages)
- **Evidence:** every page's footer contains `<!-- No Areas column: Areas is header-only (fix round 2026-11-19, owner order). The old "Areas We Serve" column (6 area links + the hub link + the footer-zips line) was removed here. -->`. Invisible to users and Google, but the five-fix claim "'Areas We Serve' gone" only holds for visible text.
- **Fix:** delete the comment (or shorten it to `<!-- Areas is header-only -->`) on the next export.

### D-P3-4 — Estero and Bonita Springs share one homepage paragraph; "Leaks of every kind" help card is link-free by design
- **Evidence:** one paragraph covers both areas — "Estero and Bonita Springs: condo leaks from the unit above and seasonal homes found wet after time away. See Estero and Bonita Springs." (the two links exist, the prose is shared). Help card "Leaks of every kind: AC leaks, burst pipes, water heaters, appliances and slab leaks." has no link and no single target page exists for it.
- **Fix:** his decision (already flagged in the hero round) — split the Estero/Bonita paragraph into two area-specific lines if he wants it; leave the leaks card unlinked or point it at /water-removal/.

### D-P3-5 — `help-sewage-cleanup.jpg` shows a spotless bathroom — no water, damage, or equipment visible
- **Page:** homepage `/` help card "Sewage backup cleanup".
- **Evidence:** viewed pixels (`qa/screenshots-20x-testing/d/sheet-areas-help.jpg`): clean white bathroom, toilet + tub, mop bucket — reads as a cleaning-service photo, not sewage cleanup. Every other help image shows the actual problem or the equipment. (Contrast with `kinds-sewage-backup.jpg`, which correctly shows a flooded bathroom.)
- **Fix:** swap for a photo showing a sewage backup / contaminated water or cleanup crew in PPE; if nothing passes the relevance bar, leave the slot honestly empty rather than a clean-bathroom shot.

### D-P3-6 — Four non-service heroes are generic desk/paper stock (topical, not wrong)
- **Pages:** /disclaimer/ (shield + papers), /insurance/ (stack of papers + phone), /privacy-policy/ (laptop + padlock), /terms/ (notepad + pen + glasses).
- **Evidence:** viewed pixels (`qa/screenshots-20x-testing/d/sheet-heroes-2.jpg`, `sheet-heroes-3.jpg`). None is wrong-country or wrong-service — generic legal/office stock, unlike the 30 service/area heroes which are all specific and on-topic.
- **Fix:** optional polish only — replace with Florida-specific or service-adjacent photos if good ones exist; otherwise keep (no trust harm as-is).

### D-P3-7 — Repeated boilerplate blocks across pages (template text, not a ranking risk at this scale)
- **Evidence (visible `<main>` text, >80-char paragraphs):** "Dehumidifiers and air movers run with readings logged daily. See structural drying." — identical step-5 sentence on 7 pages (bonita-springs, cape-coral, fort-myers-beach, lehigh-acres, mobile-home, vacant-home, water-heater-leak). "Read how insurance handles water damage in Florida. General pricing information: water damage pricing guide." — identical sign-off paragraph on 6 pages (bonita-springs, commercial, estero, floors, fort-myers-beach, north-fort-myers). Well-pump FAQ answer "Turn off the well pump at its breaker and close the main valve near the pressure tank. That stops the pump from pushing more water into a broken line." — identical on /cape-coral/ and /lehigh-acres/ (questions differ slightly).
- **Fix:** optional — localise the drying step sentence per page (e.g. name the room/material) and vary the sign-off wording on 2–3 of the 6 pages. The well-pump answer is the same correct advice in both places; leave or vary one word.

### D-P3-8 — Two heroes over 300 KB; mobile serves the 960w hero at 390px (2.46×)
- **Evidence:** `hero-lehigh-acres.jpg` 364 KB (1600×1067) and `hero-north-fort-myers.jpg` 340 KB (1600×1067) are the only files over 300 KB; all other heroes are 127–283 KB. Desktop ratios are fine (1.11×–1.33×). On mobile the `srcset` has no variant smaller than 960w, so a 390px viewport downloads the 960w file (2.46×).
- **Fix:** re-encode the two heaviest heroes at slightly lower quality / resize to 1440w (target ≤250 KB); optionally add a ~640w hero variant for mobile. Page weights are otherwise fine (max 465 KB on /areas/).

### D-P3-9 — "Every kind of property" help card links only to /commercial/ though it lists five property types
- **Page:** homepage `/` help grid.
- **Evidence:** card text "Every kind of property: single-family homes, condos, mobile homes, vacation rentals and businesses." — the single link goes to /commercial/, so four of the five named property types lead to a page that is not about them.
- **Fix:** either link the card to /areas/ (all properties, all areas) or make only the word "businesses" the link and leave the rest plain.

---

## LUXURY UPGRADES — ranked by impact (Worker E, viewed pixels, 9 sampled pages @1440 + 390)

Verdict in one paragraph: the site is correct, legible and well-built — but it reads as a **competent template**, not a premium brand. One display weight (Archivo Black 400) does every heading on every page; one 0.93→0.70 dark scrim buries every hero photo under the same grey-teal wash; the 12,000–22,000px body is a single white column with no banding, no kickers and no visual crescendo; gold + sand — the two colours that could make this palette feel Floridian-luxury — appear almost only as 3px rules. The single biggest lever is letting the photography breathe.

| Rank | Upgrade | Pages | Concrete change |
|---|---|---|---|
| **L-1** | Hero scrim buries every photo under the same dark wash | All 9 sampled | Directional scrim `linear-gradient(100deg, rgba(6,32,40,0.92) 0%, 0.78 @38%, 0.38 @68%, 0.22 @100%)` + bottom-only gradient `linear-gradient(0deg, rgba(6,32,40,0.55) 0%, transparent 32%)`; area pages drop the right stop to 0.12; `filter: saturate(1.12) contrast(1.04)` on `.hero-img`; keep left 40% dark so white H1 stays ≥7:1. Worst cases: Cape Coral canal renders as murky black water, FMB stilt house as grey, cost worker as near-black silhouette. |
| **L-2** | No eyebrow/kicker and no trust strip in any hero | All 9 sampled | Eyebrow above every H1: 13px Inter 800, `letter-spacing:0.24em`, uppercase, gold `#E8C87A`, preceded by a 32px × 3px gold rule, margin-bottom 18px. Copy from existing words only (e.g. home "Fort Myers · Lee County, FL", services "Emergency Service — Answered 24/7"). Trust row under CTAs: 15px/600 `#CFE0E4`, gold `·` separators: "Answered 24/7 · Moisture readings logged · Written scope before rebuild". |
| **L-3** | H1 orphan wraps on 4 of 9 heroes | drying, cost, water-removal, home mobile | `h1 { text-wrap: balance; max-width: 820px; }` sitewide; hand-tune the two worst with a non-breaking span on the place phrase (`Fort&nbsp;Myers,&nbsp;FL`); mobile H1 40px → 38px, `line-height:1.08`, `text-wrap:balance`. Verify each hero at 1440 + 390 + 820; no hero may end on a 1–2-word line. |
| **L-4** | Body is one 12,000–22,000px white river: no section banding | All pages | Alternate section backgrounds: even sections `background:#F6F1E7` full-bleed, `padding:88px 0`; ONE deep-teal band per page (`.band-deep { background:linear-gradient(115deg,#0A2E38,#0D3A46 60%,#0B5563); color:#fff; padding:96px 0 }`) around the most persuasive section, white H2 + gold rule. Section padding 56px → 88px desktop, 64px mobile. |
| **L-5** | Body measure 1097px ≈ 110 chars/line | All pages | Cap prose measure at `780px` (~68ch at 20px) for `.page-body>p/ul/ol`; keep tables, cards, grids, details card at full 1100–1192px. Compensate with `line-height:1.75` and `p { margin-bottom:1.4em }`. **⚠️ CONFLICT: the owner ordered wide lines (his standing order) — this directly contradicts it. Needs his explicit call; do NOT implement silently.** |
| **L-6** | Every H2 is identical: 42px Archivo Black + the same gradient bar | All pages | H2 eyebrow pattern: preceding 13px/700/0.20em uppercase teal `#0B5563` kicker as a `<p class="sec-kicker">` in markup; scale feature H2s 46px/1.08, standard 40px/1.12; vary the gradient bar (72px feature, 48px standard). H3: 26px → 24px, `letter-spacing:-0.01em`, gold underline only on feature H3s. |
| **L-7** | Kind/help cards have no titles and zero hover life | Homepage; pattern sitewide | Restructure each card: H3 title 23px + 2-line body 18px/1.55 + link styled `Learn more →` (gold `#C99B3F` on dark, teal on light, no underline until hover). Hover (0.25s ease): `transform:translateY(-4px); box-shadow:0 16px 40px rgba(10,46,56,0.18);` + photo `scale(1.04)` inside `overflow:hidden`. Card padding 28px → 32px, radius 12px → 16px. **Note:** CSS has zero `:hover` rules on any card today. |
| **L-8** | Buttons: the gold inset edge reads as a stray underline; gradient is heavy | All pages | Flat coral: `.btn-call { background:#C2410C; border-radius:12px; padding:18px 32px; box-shadow:0 8px 24px rgba(194,65,12,0.30); }`, **remove `inset 0 -3px 0 gold`**; hover `background:#9A3412; transform:translateY(-2px)`. Ghost: `border:1.5px solid rgba(255,255,255,0.85); background:rgba(10,46,56,0.25); backdrop-filter:blur(4px)`; hover `background:rgba(255,255,255,0.14)` (no gold fill). |
| **L-9** | Header: brand wraps and underlines like a link; nav is flat | All pages | `.brand-name { white-space:nowrap; font-size:20px; }` + remove the `aria-current` underline on the brand (keep gold `inset 0 -3px 0` on `.nav-current-top` only). Nav links 17px/600, `letter-spacing:0.01em`, padding 12px 14px. Header background `linear-gradient(180deg,#0A2E38,#0C3340)` + keep 3px gold hairline. Mobile: brand-name 17px nowrap, tagline hidden, add a compact 38×38px phone-icon button in the mobile header. |
| **L-10** | Area pages have no map and no local visual anchor | cape-coral, fort-myers-beach | Compact area map strip after the intro: static map image (1200×560) with 2px gold border + 14px radius, caption "Cape Coral and the Lee County service area", "View larger map ↗" link; layer the live Google iframe over the poster so a blocked/slow embed degrades to the poster (see L-18). Add a 3-chip facts band under the map using facts already in the copy (e.g. "400+ miles of canals · ZIPs 33904–33993 · Slab homes"), sand chips, 16px/700. |
| **L-11** | Mobile hero is 1,019px tall and the intro is cut by the fixed call bar | home, cost; all inner pages | Mobile hero padding 40px → 32px top / **96px bottom** (last intro line clears the ~66px call bar + safe area); cap the mobile hero intro visually at 3 lines with a soft fade (`mask-image:linear-gradient(180deg,#000 78%,transparent)`) and a "Read the intro ↓" anchor — or move the phone number to the CTA only (words unchanged, presentation only). Mobile H1 40px → 38px/1.08. Mobile ghost button `white-space:nowrap`. |
| **L-12** | Post-hero CTA triplication on every inner page | 8 inner pages sampled | Replace the post-breadcrumb button with a slim utility line: 18px, muted `#46585F`, phone as a plain teal link — "Answered 24/7 · Call 239-356-3708" with a 16px phone glyph, left-aligned, `margin:4px 0 8px`. Keep coral buttons for the hero and the closing CTA band only. |
| **L-13** | Steps have no spine, no time labels | how-it-works | 2px vertical connector `.steps>li::before { left:29px; top:64px; bottom:-4px; width:2px; background:linear-gradient(180deg,#C99B3F,#0B5563); }` (last li: none). Duration chip per step (13px/700/0.14em uppercase, sand bg `#F6F1E7`, teal text, 6px radius, padding 6px 10px) using durations already in the copy ("Minutes", "Day 1", "3–5 days", "Final day", …). Step H3 26px → 28px. |
| **L-14** | No closing conversion band; the page just ends into the footer | All pages | Wrap the final CTA in a full-bleed deep band: `background:linear-gradient(115deg,#0A2E38 0%,#0D3A46 55%,#0B5563 100%)`, padding 88px 0, H2 white 40px Archivo Black with gold 72px rule, intro 22px `#EEF4F5`, coral button (flat, per L-8) + ghost "Describe your water problem", 16px trust line "Answered 24/7, including holidays and the days after a storm". Subtle wave/roofline SVG at the band's top edge in `rgba(201,155,63,0.14)`. |
| **L-15** | Cost page: the price table is the best element — but the "typical" job is invisible | cost | Highlight the "One room — About $1,200 to $3,500" row: `background:#FDF8EC`, left border 5px coral, "Most common" chip (12px/800/0.12em uppercase, coral bg, white text, 4px radius) in the first cell. Range bar under the table: 8px rounded track (`#EFE7D6`) with coral fill $500–$15,000 and a gold marker at $1,200–$3,500 labelled "Most Fort Myers jobs land here", 16px. Prices unchanged. |
| **L-16** | Home + cost hero photos are the weakest images on the site | home, cost | Re-crop the home hero to the extraction action (machine + hose + wet tile, `object-position:62% 50%`; if the source allows, swap in the brighter extraction shot already used in the kinds grid); re-crop the cost hero to the assessment moment (moisture meter / clipboard / readings, brighter exposure, `object-position:30% 40%`). After the scrim fix (L-1) re-shoot both heroes and judge again. |
| **L-17** | Gold + sand are under-used: the palette reads as two colours, not four | All pages | (1) deepen sand for bands to `#EFE7D6` (`--sand-2`); (2) gold as a real accent: section kickers in gold-on-deep (`#E8C87A`), footer top border 3px → 6px `linear-gradient(90deg,#0B5563,#C99B3F 50%,#C2410C)`; (3) 1px gold hairline under each H2 area (`.page-body h2 { padding-bottom:20px; border-bottom:1px solid #EFE7D6 }`); (4) price-table "Most common" chip + step connector in gold (L-13/L-15). Gold stays an accent (≤8% of any viewport). |
| **L-18** | Map embeds have no fallback: a blocked Google load leaves a blank box | home | Static map image (1200×560 homepage, 560×280 footer) as the iframe's background/poster (`background-image` on the wrapping figure, iframe `background:transparent`), plus a centred caption inside the frame area ("Map loading — Fort Myers & Lee County") that the iframe covers once loaded. Verify in a real browser with network throttling (Slow 3G) and with maps blocked. **Caveat:** the blank boxes were a sandbox network artefact (Google unreachable from this VM) — robustness work, NOT a confirmed live defect. |

**Already luxurious — do not touch:** details card (sand fill, gold "DETAILS" eyebrow, icon chips — the most premium component on the site); price-table base design; FAQ accordions; H2 gradient bar device (problem is monotony, L-6, not the bar); kind/help card photography (bright, Floridian, action-true — cards need titles/hover, L-7, not new photos); sticky header + bottom call-bar architecture; legibility under the scrim (L-1 must preserve left-side darkness); footer link skeleton (Services 7 + Explore 9 + brand + hours + map + copyright).

---

## WHAT PASSED CLEAN (consolidated — verified, not claimed)

- **Live (pages.dev):** 34/34 routes 200; 33/33 no-slash → 308; bogus → custom 404; sitemap 31 locs, robots, llms.txt (31) + llms-full.txt (31) all 200; `?v=2` on 34/34, zero bare references; 46/46 `<img>` srcs + 68/68 srcset URLs 200; 34 unique internal paths, 0 broken; 0 self-links and 0 duplicate prose targets; related exactly 3 on all 27 pages that have one (3rd link always `/` with a varied anchor); canonicals correct 34/34; titles 51–60 chars; meta 137–155 chars; H1 exactly 1 on 34/34.
- **Content:** word-diff 0 unauthorized on all 34 pages (818 words removed, all authorized: 75 sentences + 98 Related items + 27 anchor variations, 0 inserted words); dashes 0; phone only 239-356-3708 / +1-239-356-3708 / tel:+12393563708 (the one other number, 1-877-693-5236 on /insurance/, is the FL DFS helpline, paste-verbatim); brand matches paste everywhere; FAQ 308 visible = 308 schema across 31 pages; typos 0 in ~72,000 words; "Caloosahatchee" correct in all 14 mentions.
- **Schema:** `validate_schema.py` → 34 pages, 92 scripts/nodes, ERRORS 0, WARNINGS 0, NOTES 6 (3× publisher logo + 3× Article image — see B-P3-1 for the stale half); BreadcrumbList on 30 pages, every ListItem carries `item` (0 missing); legal pages carry 0 JSON-LD.
- **Legal:** privacy/terms/disclaimer `noindex, follow`, excluded from sitemap + llms.txt, "Last updated: November 19, 2026" on privacy + terms only, none on disclaimer.
- **Rendering:** overflow 0 at 320/390/1440 on all 34 pages; contrast ≥4.5:1 on every solid-background text element (sitewide worst: breadcrumb separator 4.90); tap targets ≥44px for every non-inline link/button/summary; all 34 heroes + all 13 kinds cards readable desktop + mobile (viewed); all 26 details cards aligned (icon exactly 40×40, 0 rows off-center >3px); five-fix regression HOLDS on all five items; footer clean at all widths; mobile call affordance + functional skip link on 34/34; zero clipped/overlapping text.
- **Technical:** console errors 0, pageerrors 0 (41 renders), unclosed/mismatched tags 0, duplicate ids 0, mixed content 0, broken `#` anchors 0, empty `href="#"` 0; favicon present + legible at 16px; alt present on 46/46; srcset/width-height attrs correct; page weight max 465 KB (/areas/), no page over 500 KB; sitemap/link graph 0 orphans in either direction.
- **Images (viewed pixels):** all 34 heroes + 13 kinds + 6 area images PASS relevance (no wrong-country / wrong-city / wrong-service); help images 5/6 pass (1 weak — D-P3-5); 4 legal heroes generic-but-topical (D-P3-6).
- **Facts spot-checked clean:** ZIPs (except D-P2-1/D-P3-1), county/geography, NFIP 30-day wait, proof of loss 60 days, ICC $30,000, Citizens 2027 requirement, FEMA 50% rule, Categories 1/2/3, FL Statute 718.111(11), AOB reform 2023, mold 24–48h, drying 3–5 days.

## COORDINATOR RULINGS (for the parent)

1. **Task 13 (Related trim + anchor variations) is AUTHORIZED.** Worker B's brief omitted it, but the owner's hero-round order explicitly included "Related = just 3 per service page + homepage-link anchors VARIED per page, never the same homepage entity twice", recorded in MEMORY.md and `qa/FINDINGS-related-3.md`. B's treatment stands; the 98 removed Related items + 27 anchor variations are NOT findings.
2. **L-5 (780px prose cap) CONFLICTS with the owner's standing "wide lines" order.** It needs his explicit call; do not implement silently. (E's own note agrees the wide feel should survive in full-width components.)
3. **A-1 is a deployment/DNS matter, not a code defect.** Re-verify apex after DNS propagates (owner confirmed attach ~22:27 PKT, apex-only per his 22:15 order — do NOT attach www).
4. **Live map tiles + live Speed Index still need one real-browser look** (Google unreachable from this VM; maps render as blank boxes locally — environmental, not a site defect). Same standing item as the 20x round.

## EVIDENCE INDEX

- This file: `qa/FINDINGS-20x-testing.md`
- Part A (live/links/SEO): `qa/20x-part-a.md` + raw `qa/20x-part-a-raw/`
- Part B (content/schema): `qa/20x-part-b.md` + raw `qa/20x-part-b-raw/`
- Part C (rendering): `qa/20x-part-c.md` + data `qa/20x-c-data*.json`, `qa/20x-c-tables.json` + screenshots `qa/screenshots-20x-testing/c/` (263 files)
- Part D (technical/blunder): `qa/20x-part-d.md` + screenshots `qa/screenshots-20x-testing/d/`
- Part E (luxury): `qa/20x-part-e.md` + screenshots `qa/screenshots-20x-testing/e/` (75 files) + `measurements.json`
