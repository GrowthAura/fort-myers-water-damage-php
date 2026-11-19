# FINDINGS — Fort Myers NEW PHP site, full 34-page round
## `~/workspace/fort-myers-php/` — Caloosahatchee theme — 2026-11-19

## 1. Scope
- **34 pages total**: homepage + 32 inner + 3 legal (privacy-policy, terms, disclaimer).
- **Sitemap: 31 locs** (30 content routes + `/about/`). The 3 legal pages are noindex and
  stay OUT of sitemap.xml and llms.txt. `/about/` is a content page, not legal — INCLUDED
  (31 vs the old site's 30; the old site had no `/about/` route).
- URL structure = the old published site's 33 routes exactly, plus `/about/` (the one new
  route he ordered). Verified against old `fort-myers-nextjs/app/` dirs (minus `components`,
  a shared folder, not a route) — exact match, trailing slash included.
- Local build + 2x deepest testing complete. **Deployed 2026-11-19** (see §7).

## 2. Verification table — pages 21–34 (rounds 2–3)

| # | Route | Visible words | FAQ | Schema | Notes |
|---|-------|--------------|-----|--------|-------|
| 21 | /appliance-leak/ | 2,158 | 11 | Service, no description | |
| 22 | /floors/ | 2,070 | 9 | Service, no description | |
| 23 | /cabinets/ | 1,877 | 10 | Service, no description | |
| 24 | /commercial/ | 1,953 | 10 | Service + `audience` BusinessAudience (new field, rendered exactly) | |
| 25 | /north-fort-myers/ | 1,938 | 7 | Service, areaServed Place object, postalCode [33903, 33917] | Location page — footer map absent |
| 26 | /privacy-policy/ | 878 | — | NONE (noindex) | 14 H2s (13 sections + trailing "Contact us"); "Last updated: November 19, 2026" at top (his call) |
| 27 | /terms/ | 675 | — | NONE (noindex) | 13 H2s (12 + trailing "Contact us"); "Last updated: November 19, 2026" at top (his call) |
| 28 | /disclaimer/ | 513 | — | NONE (noindex) | 10 H2s (9 + trailing "Questions"); NO date line (copy never references one) |
| 29 | /fort-myers-beach/ | 2,104 | 9 | Service, areaServed Place, postalCode [33931, 33932] | Location page |
| 30 | /estero/ | 1,971 | 7 | Service, areaServed Place, postalCode [33928] | Location page |
| 31 | /bonita-springs/ | 1,923 | 8 | Service, areaServed Place, postalCode [34134, 34135] | Location page |
| 32 | /how-it-works/ | 2,059 | 8 | ARTICLE (not Service), 9 numbered steps, 3 tables | New `steps-rich` parser block type |
| 33 | /contact/ | 995 | 5 | ContactPage, phone-only (NO form invented) | "Map: Fort Myers, Lee County, Florida" → service-area map embed |
| 34 | /about/ | 1,288 | 4 | AboutPage, areaServed 7 + knowsAbout 7 | "Questions About..." parsed as FAQ (visible == schema) |

All 34 pages: word-diff 0 vs paste, H1 exactly 1, title/meta/canonical byte-match,
FAQ visible == schema, breadcrumb visible == schema, 0 self-links in `<main>`,
overflow 0 at 320/360/390/1440, body text 20px measured (desktop + mobile).
FAQ total across site: **308** (220 round 1 + 47 round 2 + 41 round 3).
JSON-LD: 92 scripts in out/, all parse, 0 errors. BreadcrumbList scripts 30.
Legal pages: zero JSON-LD, robots `noindex, follow`, visible breadcrumb Home » H1.

## 3. Pass 1 (own verification) — final build
- `python3 qa/verify_export.py`: **FAILURES: 0, NOTES: 0** (all 34 pages).
- `python3 qa/render_check.py`: overflow 0 + 20px on all 34 routes.
- Screenshots viewed: homepage (desktop full + mobile) + all 6 newest pages
  (desktop + mobile, full-page for the 7 FULLPAGE routes).
- URL audit vs old site: exact match + /about/ only.
- Agentic SEO 3/3 GREEN (measured — see §5).
- Hero/brand viewed: Caloosahatchee teal/coral/sand/gold consistent across
  header, hero, cards, tables, footer; sticky call button + mobile bottom call bar.

## 4. Pass 2 (independent re-verification) — three runs
- **Run 1 (0aeb13cd): 1 DEFECT.** `(/)` homepage-link annotations leaked as raw
  visible text — 38 annotations on 30 inner pages, 0 `<a href="/">`; 3 FAQPage
  schema answers also contained raw `(/)`. Root cause: link regex `\((/[a-z0-9\-/]+)\)`
  required ≥1 char after `/`, so bare `(/)` never matched; word-diff passed vacuously
  (words() drops `(/)` as punctuation). **Fix:** regex `+` → `*` in all 6 sites
  (parse_page.py:152/:450, parse_homepage.py:41/:496, parse_legal.py:42/:229);
  dashes removed from comments in robots.txt/styles.css/main.js (6 total).
  Re-parsed all 34 (word-diff 0); measured 38 `<a href="/">` in `<main>` on 30 pages,
  0 visible `(/)` literals, FAQ texts clean.
- **Run 2 (426dccc8): 2 FINDINGS.**
  - DEFECT 1 (content-visibility): full-page screenshots showed ~600px blank holes
    where FAQ/steps/tables/kind-grids belong (home 10, estero 4, bonita 5, FMB 4,
    contact 3, about 1, HIW 3). Real scrolling visitors DO see the content
    (scrolled probes proved it); the review pack could not prove it.
    **Fix (KEEP path, not removal):** print override in CSS (`@media print` →
    `content-visibility: visible`); render_check.py injects
    `content-visibility: visible!important` before full-page shots only.
    Two scroll-based attempts FAILED first (sync scrollTo coalesced; async
    60ms steps discarded by Chrome once scrolled away). Final method WORKS —
    viewed: home kinds-grid all 13 cards, Estero FAQ all 7 accordions.
    Speed optimisation stays live for real users.
  - DEFECT 2 (breadcrumb self-link): every page except home had one
    `<a href="https://fortmyerswaterdamagerestoration.us/<slug>/">` in `<main>` —
    the breadcrumb's current-page crumb (absolute URL). Builder's verifier only
    checked `href == slug`. **Fix:** final crumb now renders as
    `<li aria-current="page"><span>` (middle crumbs plain `<span>`);
    BreadcrumbList schema keeps the URL. Measured: 0 self-links in `<main>`
    (both relative and absolute forms).
- **Run 3 (dc2abaa5): ZERO DEFECTS FOUND.** Both fixes re-measured (Defect 1: fresh
  full-page shots, all 13 kinds cards + 14 home FAQs + HIW steps 4–9 + tables visible,
  no blanks; independent scrolled probe, no style override: FAQ list 1195px/14 items,
  kinds-grid 1931px/13 cards, content-visibility still `auto`. Defect 2: 0 self-links
  all 34 pages; About breadcrumb `Home » About …` with span crumb, schema keeps URL.
  (/) fix exact: 38 links, 0 literals. Fonts PASS (0 Google Fonts refs, 2 real woff2,
  `font-display: swap`, 34/34 preload both). Dashes 0 in ALL out/ files. Full suite
  PASS (verify 0/0 twice, render 0/20px, sitemap/redirects/llms, Agentic SEO 3/3,
  URL audit, spot checks). **2x deepest testing CLOSED — zero blunders.**

## 5. Speed Index (Lighthouse 13.6.0, local lab, simulated slow 4G + 4x CPU)
- Home mobile: **SI 2.2s, LCP 2.1s, FCP 2.1s, TBT 360ms, CLS 0, Perf 89**
- Home desktop: **SI 1.0s, LCP 0.7s, FCP 0.7s, TBT 20ms, CLS 0, Perf 99**
- How-it-works mobile: **SI 2.6s, LCP 1.8s, FCP 1.8s, TBT 860ms, CLS 0, Perf 78**
- Every Speed Index in the good band (< 3.4s). No Lighthouse opportunities with savings.
- Fixes that got here: fonts self-hosted (Archivo Black + Inter variable woff2, 67KB,
  `@font-face` swap, Google Fonts links removed); `content-visibility: auto` +
  `contain-intrinsic-size: auto 600px` on `.faq-list, ol.steps, .table-wrap, .kinds-grid`
  (SI 3.8s → 2.1s mobile).
- **LIVE Speed Index NOT measured from this VM** (honest): VM Chromium gets
  `net::ERR_TUNNEL_CONNECTION_FAILED` on pages.dev (proxy tunnel), so local Lighthouse
  cannot load the live URL; PageSpeed Insights API returned 429 (anonymous daily quota
  exhausted). Live HTML is byte-identical to local out/ (md5-verified, §7) and Cloudflare
  serves it with Brotli + edge caching, so live is expected equal or better — but that
  is an expectation, not a measurement. Re-measure on PageSpeed Insights from a real
  browser when convenient.

## 6. Agentic SEO 3/3 GREEN (measured)
1. **llms.txt**: H1 + summary + 31 entries; URLs == sitemap locs in identical order;
   all resolve to files.
2. **robots.txt**: global Allow + 15 named AI crawlers explicitly allowed
   (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-Web, anthropic-ai,
   PerplexityBot, Google-Extended, CCBot, cohere-ai, Meta-ExternalAgent,
   Meta-ExternalFetcher, Applebot-Extended, DuckAssistBot, YouBot); Bytespider
   explicitly Disallowed (training scraper, not a citing search engine — deliberate);
   Sitemap line to the canonical domain.
3. **Structured data**: 92 JSON-LD scripts, all parse, 0 failures; FAQPage 308 answers
   (31 scripts); BreadcrumbList 30; legal 3 zero JSON-LD + noindex.

## 7. Deploy — 2026-11-19 (his order 13:20 PKT)
- **GitHub repo (NEW):** https://github.com/GrowthAura/fort-myers-water-damage-php
  (public, id 1463922039, owner GrowthAura — token owner verified via GET /user).
  - `main` ddcbf2f6 — PHP source, 94 files, author GrowthAura
    <noorullahchhachher2@gmail.com>. (2 `__pycache__` .pyc files caught in staging,
    removed + `__pycache__/` added to .gitignore before commit.)
  - `cloudflare-pages` 72f3ba81 — static export (79 files) + `.github/workflows/
    deploy-cloudflare.yml`. Push via transient askpass (deleted after use);
    remote clean https URL, no credential.helper, config token-free.
- **Secrets:** CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID set via gh CLI and
  verified in the secret list before the branch push.
- **Cloudflare Pages project:** fort-myers-water-damage-php (production branch main).
  Wrangler 4.165.0 note: `pages deploy` does NOT create the project — created first
  with `wrangler pages project create` (production-branch main), then deployed.
  - Direct upload d017417c (09:23:33Z, production, 77 files + _headers/_redirects).
  - Actions run 44496276802 (push to cloudflare-pages) **completed success in 20s**;
    deployment 60eed8d0 (09:25:46Z, production, branch main). Auto-deploy PROVEN.
- **Live verification — https://fort-myers-water-damage-php.pages.dev:**
  home 200 (title + canonical + H1 correct), /how-it-works/ 200, /sitemap.xml 200
  (31 locs), /robots.txt 200, /llms.txt 200 (31 entries), bogus path 404,
  no-slash → slash 308. Live homepage HTML **byte-identical** to local out/index.html
  (md5 fd185c6c5aa5f911b8dfc76be47fd5a4 both).

## 8. Known limitations / still his call
- **Map tiles need one real-browser look.** Google Maps embeds are present and
  correctly sized (contact map 1192×450 in VM capture) but tiles render blank in
  VM Chromium (zero requests to Google from Chromium; curl reaches google.com fine).
  Markup is correct; needs his phone/Chrome look.
- **Residual content-visibility disclosure:** exotic non-scrolling renderers (not
  Googlebot, which scrolls; not print, which is overridden) may see ~600px
  placeholders for FAQ/steps/tables/kind-cards. Review pack + scrolling visitors +
  print all proven fine.
- **NOT done (his later calls):** old domain fortmyerswaterdamagerestoration.us NOT
  attached to this project. OLD repo Noorullahmian/fort-myers-water-damage-restoration
  and the LIVE Next.js site untouched. He reviews pages.dev A to Z himself first.
- Heroes honestly empty (gradient placeholders) — no free-stock photo passes
  licence+place+subject for Fort Myers; never force a wrong photo.
- Live Speed Index unmeasured from this VM (§5) — re-measure on PageSpeed Insights.
- Old-site open items unchanged: Batch-3 push (Next.js, READY at dbdbd98) still
  blocked on his word + token; Seabees photo still live on the old site (his call).
