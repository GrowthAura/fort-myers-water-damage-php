# 20X Audit — Worker A: LIVE + LINKS + SEO

- **Project:** `~/workspace/fort-myers-php/` (five-fix build, main `8cf8cb7` + cloudflare-pages `19992fd`)
- **Live base audited:** https://fort-myers-water-damage-php.pages.dev
- **Date:** 2026-11-19 (PKT, evening)
- **Method:** READ-ONLY. Live status via curl; markup parsed from local `out/` (byte-identical to live — md5-verified on home, water-removal, about, areas; see §1). No live visual check: Chromium on this VM cannot reach pages.dev (`ERR_TUNNEL_CONNECTION_FAILED`), per task note. No files edited, nothing pushed/deployed, `qa/verify_export.py` not run.
- **Raw evidence:** `qa/20x-part-a-raw/` (`live-status.txt`, `sitemap-check.txt`, `image-status.txt`, `srcset-status.txt`, `internal-link-status.txt`, `internal-links.txt`, `og-image-status.txt`, `per-page-seo.json`, `related.txt`, `css-refs.txt`, `images.txt`, `apex-sitemap.txt`, `local-sitemap.txt`, `audit-run-2.log`, `NOTES.txt`).

## PASS/FAIL table

| # | Check | Result | Counts |
|---|-------|--------|--------|
| 1 | Live: every route 200 (slash form) | **PASS** | 34/34 |
| 2 | Live: no-slash form 308 | **PASS** | 33/33 inner routes 308 → slash form; home `/` 200 |
| 3 | Live: bogus path 404 | **PASS** | `/bogus-xyz/` → 404, custom 404 page (`<title>Page Not Found …`) |
| 4 | Live: sitemap.xml 200 + exactly 31 locs | **PASS** on pages.dev | 31 locs; pages.dev 31/31 200 — **but see Finding A-1: apex host serves a stale sitemap (30 locs) and /about/ 404s there** |
| 5 | Live: robots.txt 200 | **PASS** | 200; `Allow: /`, named AI crawlers allowed, Bytespider disallowed, sitemap line present |
| 6 | Live: llms.txt + llms-full.txt 200 + 31 entries each | **PASS** | llms.txt 31 `- [` entries (+ 1 full-text link line); llms-full.txt 31 page URLs across 4,508 lines; both 200 |
| 7 | Stylesheet `?v=2` on all 34 pages | **PASS** | 34/34 reference exactly `/assets/css/styles.css?v=2`; 0 bare `styles.css` references in any HTML (`grep` 0 lines) |
| 8 | Every `<img>` src returns 200 live | **PASS** on pages.dev | 46 `<img>` tags / 46 unique srcs, 0 non-200; 68 srcset URLs, 0 non-200 — **but see Finding A-1: the same files 404 on the apex host** |
| 9 | Alt text present and sane | **PASS with 1 P3** | 46/46 have alt; 0 missing, 0 empty, 0 filename-stuffed — see Finding A-3 (15 alts >125 chars) |
| 10 | Internal links: 0 broken | **PASS** | 34 unique internal paths, all 200 live, all resolve to a local file in `out/` |
| 11 | Self-links in `<main>` body copy | **PASS** | 0 (prose-only check, breadcrumb + related excluded as template chrome) |
| 12 | Related section exactly 3 links per page that has one | **PASS** | 27 pages with a related list, all exactly 3 links; 3rd link is always `/` with a per-page varied anchor |
| 13 | One link per target in body copy (prose only) | **PASS** | 0 duplicate targets in prose on any page |
| 14 | SEO: canonical present, self-referential, correct | **PASS** | 34/34 canonical = `https://fortmyerswaterdamagerestoration.us/<slug>/` |
| 15 | SEO: `<title>` present + sane length | **PASS** | 34/34; lengths 51–60 chars, none >60 |
| 16 | SEO: meta description present | **PASS** | 34/34; lengths 137–155 chars |
| 17 | SEO: H1 exactly 1 per page | **PASS** | 34/34 exactly 1 |
| 18 | SEO: heading order clean | **FAIL — 1 page** | /areas/ skips H1→H3 — see Finding A-2 |
| 19 | Sitemap vs live: every loc 200; every live route in sitemap except 3 legal | **PASS** on pages.dev; **FAIL** on apex | pages.dev 31/31; apex 30/31 (`/about/` 404); legal pages (privacy-policy, terms, disclaimer) correctly absent from sitemap and correctly `noindex, follow` — see Finding A-1 |

## Findings

### A-1 — P1 — Apex canonical host still serves the STALE old (Next.js) site: sitemap URL 404s, all og:image + CSS 404 there, www unreachable

**Pages/URLs:** https://fortmyerswaterdamagerestoration.us/about/ (in sitemap), all 34 `og:image`/`twitter:image` URLs, https://fortmyerswaterdamagerestoration.us/assets/css/styles.css?v=2, https://www.fortmyerswaterdamagerestoration.us/

**Evidence (curl, 2026-11-19):**
- `https://fortmyerswaterdamagerestoration.us/about/` → **404** (pages.dev `/about/` → 200, md5-identical to local `out/about/index.html`).
- Apex sitemap has **30 locs**; diff vs local sitemap (`qa/20x-part-a-raw/apex-sitemap.txt` vs `local-sitemap.txt`): the only missing loc is `https://fortmyerswaterdamagerestoration.us/about/`.
- All 34 og/twitter image URLs 404 on apex, e.g. `https://fortmyerswaterdamagerestoration.us/assets/img/hero-home.jpg` → **404**, `…/hero-about.jpg` → **404** (full list in `qa/20x-part-a-raw/og-image-status.txt` — 34/34 404). The same paths return **200 on pages.dev** (e.g. `https://fort-myers-water-damage-php.pages.dev/assets/img/hero-about.jpg` → 200; all 46 `<img>` srcs 200).
- `https://fortmyerswaterdamagerestoration.us/assets/css/styles.css?v=2` → **404** on apex (200 on pages.dev).
- Apex home is a different build: 125,635 bytes, md5 `e04093b355f73063c199b219332ae74e`, containing `/_next/static/css/…` links (Next.js); pages.dev home is 65,396 bytes, md5 `36ff385725999c7b73979023e3491965`, byte-identical to local `out/index.html`. Apex 404 bodies are the same 27,129-byte Next.js 404 HTML for both `/about/` and `/assets/img/hero-home.jpg`.
- `https://www.fortmyerswaterdamagerestoration.us/` and `/about/` → **000** (connection/DNS failure, curl).
- This is **not a defect in this build**: every canonical, sitemap loc, and og:image URL in `out/` is correct and the files exist in the deployed Pages build. The apex host simply has not been cut over to it yet.

**Why P1:** canonicals, the sitemap, and every og:image point at the apex host. Google following the sitemap hits a 404 on `/about/`; every social share of any page gets no image; anyone landing on apex gets the old site with broken CSS/images on some paths. Ranking/trust impact on the canonical domain.

**Proposed fix:** Attach `fortmyerswaterdamagerestoration.us` (+ `www`) to the Cloudflare Pages project (API with `{"name": …}` per the Troy method, or Pages → Custom domains in the dashboard) with a valid Cloudflare token, then the user's DNS step; re-verify apex `/about/` → 200, apex `/assets/img/hero-home.jpg` → 200, apex sitemap → 31 locs, www → 200. No code change in this repo. (Outside this audit's read-only scope; do not rebuild/redeploy to fix it.)

### A-2 — P2 — /areas/ skips heading levels: H1 followed directly by H3s

**Page/URL:** https://fort-myers-water-damage-php.pages.dev/areas/ (`out/areas/index.html`)

**Evidence — full heading outline (`qa/20x-part-a-raw/audit-run-2.log`):**
- `h1 'Water Damage Help Across Lee County, FL'`
- `h3 'Lee County Service Areas and ZIP Codes'` ← directly after H1, no H2
- `h3 'Fort Myers'`, `h3 'Cape Coral'`, `h3 'Lehigh Acres'`, `h3 'North Fort Myers'`, `h3 'Fort Myers Beach'`, `h3 'Sanibel and Captiva'`, `h3 'Pine Island and Matlacha'`, `h3 'Estero'`, `h3 'Bonita Springs'`, `h3 'San Carlos Park, Gateway and Iona in Lee County'` (11 H3s)
- then `h2 'Who Handles Permits and the 50% Rule in Each Part of Lee County'`, `h2 'Water Damage Problems Across Lee County'`, `h2 'What to Do First Anywhere in Lee County'`, `h2 'What You Can Expect Anywhere in Lee County'`, `h2 'Questions About Water Damage Help Across Lee County'`, `h2 'Water Damage Anywhere in Lee County?'`, then footer `h3 'Services'`, `h3 'Explore'`.
- All other 33 pages: heading order clean (no skips, no empty headings).

**Proposed fix:** Promote the table heading + the 10 area headings on /areas/ from H3 to H2 (keep the visual size via class if the H3 look is wanted), so the outline is H1 → H2 (table) → H2 (areas) → H2 (sections). One-page template/content change, then re-export + re-gate headings on all 34 pages.

### A-3 — P3 — 15 alt texts exceed the ~125-character screen-reader guidance (longest 157)

**Pages/URLs:** home hero + 14 inner heroes (full list in `qa/20x-part-a-raw/audit-run-2.log`, "ALT lengths >100").

**Evidence (alt lengths, from `out/`):**
- Longest: home `/assets/img/hero-home.jpg` — **157 chars**: "A restoration technician extracts standing water from a tiled living room floor in a bright Florida home, with palm trees visible through sliding glass doors"
- Also >125: water-removal 150, drying 145, condo-leak 153, flood-cleanup 146, vacant-home 139, north-fort-myers 137, sewage-cleanup 130, lehigh-acres 131, areas 129, mobile-home 127, slab-leak 127, ac-leak 126, cape-coral 126.
- 30 of 46 alts are >100 chars; 15 are >125. Counter-evidence: **0 missing, 0 empty, 0 filename-stuffed** alts — every alt is descriptive and place/service-relevant.

**Proposed fix:** Trim the 15 hero alts to ≤125 characters (cut trailing scene detail, keep subject + place), e.g. home hero → "A restoration technician extracts standing water from a tiled living room floor in a Florida home". No image or layout change; re-export + re-check alt lengths.

## What passed clean (no finding)

- **Live:** 34/34 routes 200; 33/33 no-slash → 308 to the slash form; bogus → custom 404; sitemap/robots/llms/llms-full all 200 on pages.dev; live HTML md5-identical to local `out/` on the 4 sampled pages (home, water-removal, about, areas).
- **CSS:** `styles.css?v=2` on 34/34 pages, zero bare references.
- **Images:** 46/46 `<img>` srcs + 68/68 srcset URLs return 200 on pages.dev.
- **Links:** 34 unique internal paths, 0 broken; 0 self-links and 0 duplicate prose targets on any page (breadcrumb + related treated as template chrome — the earlier naive count flagged only breadcrumb-"Home" + related-"/" pairs, which are not prose duplicates); related = exactly 3 on all 27 pages that have one (home, areas, contact, about + 3 legal have none, per the service-pages-only order); related 3rd link is always `/` with a varied anchor per page.
- **SEO:** canonical correct on 34/34; titles 51–60 chars; meta descriptions 137–155 chars; H1 exactly 1 on 34/34; heading order clean on 33/34; sitemap = exactly the 31 non-legal routes (privacy-policy, terms, disclaimer correctly excluded and `noindex, follow`); llms.txt 31 entries, llms-full.txt 31 page URLs.

## Summary

**P1 1 · P2 1 · P3 1 — the pages.dev build itself is clean on every live/link/SEO check; the single P1 is the apex canonical host still serving the stale pre-PHP site (/about/ 404, all og:image + CSS 404 there, www unreachable), which needs the pending domain attach, not a code fix; the P2 is the /areas/ H1→H3 heading skip; the P3 is 15 over-long alt texts.**

Report file: `~/workspace/fort-myers-php/qa/20x-part-a.md` — raw evidence in `~/workspace/fort-myers-php/qa/20x-part-a-raw/`.
