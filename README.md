# Fort Myers Water Damage Restoration Pros — PHP site

New PHP rebuild of the Fort Myers water damage restoration site
(Caloosahatchee theme), built to be hosted as static files on
Cloudflare Pages. URL structure matches the published site exactly,
plus one new route: `/about/`.

- `site/` — PHP templates, data, assets, sitemap, robots, llms.txt
- `tools/` — content parsers (paste in, PHP data out)
- `pages/` — verbatim source pastes, one file per page
- `qa/` — export script, verifiers, render checks, findings logs
- `out/` — exported static tree (build artifact; lives on the
  `cloudflare-pages` branch, not on main)

Build: `python3 qa/export_cloudflare.py out`
Verify: `python3 qa/verify_export.py` then `python3 qa/render_check.py`

34 pages (31 in sitemap + 3 noindex legal pages). Phone 239-356-3708.
No street address: service-area business, Fort Myers + Lee County, FL.
