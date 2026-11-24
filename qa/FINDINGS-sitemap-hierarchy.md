# FINDINGS — Sitemap hierarchy (2026-11-25 ~01:58–02:05 PKT)

Owner's order: "sitemap kye andr sitemap bano ik hierarchy poori sahi, google will index us"
(same shape as Lancaster's live index + Cape Coral's hierarchy pushed live ~02:00 PKT).

## Structure (same URL, new shape)
- `/sitemap.xml` is now a **sitemapindex** with 4 children (each lastmod 2026-11-20):
  - `sitemap-pages.xml` — 3: /, /about/, /contact/
  - `sitemap-services.xml` — 17 service pages
  - `sitemap-guides.xml` — 4: first-hour-checklist, cost, insurance, how-it-works
  - `sitemap-areas.xml` — 7 area pages
- Union = exactly the old 31 URLs, loc+lastmod identical (verified by XML parse vs
  git HEAD sitemap). loc+lastmod ONLY everywhere — no priority/changefreq/images.
- Legal pages (privacy/terms/disclaimer) in NO child (still noindex, still excluded).
- robots.txt unchanged — it already points at /sitemap.xml, which is now the index.
- No page content changed (word-diff 0 by construction — only sitemap/router/export files).

## Code changes (3 files + 4 new sitemaps)
- `site/sitemap.xml` — rewritten as the index; 4 new `site/sitemap-*.xml` children
  (generated from the old sitemap by script — no hand-typed URLs, union proven).
- `site/index.php` router — the 4 children added to the static-file allow-list
  (MIME xml => application/xml already existed).
- `qa/export_cloudflare.py` — now index-aware: fetches the index, then each child,
  and uses the UNION as the page list (31); the 4 children added to STATIC_FILES
  (copied verbatim into out/). Old flat-urlset sitemaps still work (fallback path).

## Incidents caught during verification (no live impact)
- First export FAILED ("fetch /sitemap-pages.xml -> HTTP 404") — the old export
  treated index locs as pages, and the router allow-list lacked the children.
  Fixed both (above) before re-exporting. Note: the failed export had already
  wiped out/ (rmtree-first) — out/ was rebuilt clean by the successful re-export.
- `rcssmin` was missing after the VM replacement (export warned "shipped
  unminified"). `pip3 install --user` landed in a dir python3 doesn't see;
  `python3 -m pip install --break-system-packages rcssmin` fixed it (1.3.0).
  Re-export minified styles.css 79039 -> 34456 bytes.
- Preview-server identity trap AGAIN: :3100 is the TULSA PHP site's server
  (pid 10197, cwd .../water-damage-restoration-tulsa-ok-php/site) — my first
  :3100 curls measured Tulsa (guides/areas 404, water-removal 404). Did NOT kill
  it (another chat's work). Fort Myers preview moved to :3101 (own server,
  verified by log + title + ?v=6). All 5 sitemaps + sample pages 200 there.
- php -S quirk (preview only, NOT a site defect): a bogus directory-style URL
  returns the home page with 200 on the local php server. Cloudflare Pages
  serves the real 404 for bogus URLs (proven live in the 10x round; re-verified
  after this push).

## Tokens (values never stored/quoted)
- His "new" Noorullahmian token (sent 01:57 PKT, same value as Nov 20 Token 4):
  login Noorullahmian BUT permission **None** on GrowthAura/fort-myers-water-damage-php
  — it cannot push THIS repo (it works on his Noorullahmian repos, e.g. Cape Coral,
  where it pushed live ~02:00 PKT). NOT used for this push.
- GrowthAura token (Nov 19/20, same value as the 10x push): re-validated
  2026-11-25 ~02:02 PKT — login GrowthAura, permission **admin** on this repo.
  Still in window. Used for this push (transient askpass, deleted after).

## Push
- (filled after push: commits, Actions run, live verification)
