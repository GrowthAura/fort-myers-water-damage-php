# AUDIT — Fort Myers NEW PHP site, 10X round: SEO / SCHEMA / LINKS / IMAGES / MAP / ACCESSIBILITY
## `~/workspace/fort-myers-php/` — 2026-11-19 (read-only audit; NO site/, out/ or source file edited)

**Scope:** local `out/` (34 routes; 68 HTML files = 34 flat + 34 dir copies) + live
`https://fort-myers-water-damage-php.pages.dev`. Live homepage HTML is byte-identical to
local `out/index.html` (md5 `8c2dce9d3f62d4e1983269f08eb6d53f` both), so local measurements
apply to live. PHP is NOT installed on this VM (wiped by VM replacement) — no re-export
was attempted; `qa/verify_export.py` could not run (see §5 note). Playwright bundled
Chromium only (no `executable_path`).

**Verdict: PASS with 1 P3 finding.** Schema 0/0 holds, links/sitemap/robots/llms all clean,
images 0, map correct, overflow 0, 20px everywhere, FAQ open state proven by pixels for
the first time. The single finding: footer links measure 40px tall (29px for the footer
phone text link) against the strict 44px tap-target bar — they pass WCAG 2.2 AA (24px
minimum) by a wide margin, so this is polish, not a defect. The 6 by-design schema notes
stand — the favicon brand mark is NOT usable as a publisher logo as-is (reasoning in §2).

## 1. SCHEMA — ERRORS 0 / WARNINGS 0 (holds)

| Check | Result |
|---|---|
| `python3 qa/validate_schema.py` | **pages 34 \| JSON-LD scripts 92 \| nodes 92 \| ERRORS 0 \| WARNINGS 0 \| NOTES 6 (by design)** |
| Live BreadcrumbList spot-check, `/water-removal/` | 2 ListItems, positions 1–2, **both have `item`** (Home → `https://fortmyerswaterdamagerestoration.us/`, page → its own URL). No item-less crumb. |
| Live BreadcrumbList spot-check, `/cape-coral/` | 2 ListItems, positions 1–2, **both have `item`**. |
| Old-site GSC defect class ("Missing field 'item' (in 'itemListElement')") | Absent on live. The fix-round repair (item-less middle crumb dropped from JSON-LD only, positions renumbered) holds. |
| Article `datePublished` | Present on all 3 Articles (`2026-11-19` = `dateModified`). |
| Homepage `HomeAndConstructionBusiness` address | Present (Fort Myers, FL 33901, US — the About page's PostalAddress from his paste). |

The 6 NOTES are exactly the by-design ones from the fix round: 3× Article `image` missing
(`/cost/`, `/how-it-works/`, `/insurance/`) + 3× publisher `logo` missing (same 3 pages).
Verdicts per note in §2.

## 2. THE 6 BY-DESIGN NOTES — favicon-as-logo investigation + verdicts

### 2a. What the favicon actually is (viewed, not assumed)
`site/favicon.svg` (311 bytes, identical in `out/`) renders as a **real brand mark**: an
orange water droplet (`#E8590C`) with a white highlight swoosh, on a dark-teal
(`#0a2e38`) rounded square, 64×64 viewBox. Screenshot at 200px:
`qa/screenshots/10x-a11y/favicon-200px.png` — viewed clean, no distortion, no text.
It is the same mark used in the header: `site/includes/header.php:48` inlines the
identical droplet SVG at 34×34 next to the text brand name ("Fort Myers Water Damage
Restoration Pros"). Colours match the site palette exactly. It is a genuine droplet
brand mark, not a placeholder or generic icon.

### 2b. Publisher `logo` — VERDICT: NOT usable as-is; notes stand
Reasoning (no data invented, nothing added):
1. **No wordmark / no business name.** The mark is a bare droplet. As a publisher logo
   in search results / knowledge panels it would identify the publisher as an anonymous
   orange droplet, not "Fort Myers Water Damage Restoration Pros". A logo that does not
   name the business is not a usable publisher identity.
2. **Below Google's size floor.** The SVG is a 64×64 viewBox; Google's Organization
   logo guidance asks for at least 112×112 px. It scales as vector, but the declared
   asset is 64px.
3. **Format risk.** Google's Article/publisher-logo guidance (and the AMP-era rules it
   inherits) expects a raster image (PNG/JPG) for the publisher logo; several
   Google-facing guides state raster-only (PNG/JPG, not SVG) for this field. Referencing
   the SVG favicon as `logo` risks a validator warning instead of a pass — the opposite
   of the zero-error goal.
4. **Deriving a raster logo would invent a brand asset.** Converting the droplet to a
   PNG, or composing a droplet+wordmark lockup, creates a logo the user never supplied
   or approved. That is new brand data, not a fix.
5. **Not required.** Google's current Article docs list no required properties; `logo`
   is recommended. Omitting it costs no error (validator confirms: 0 errors, 0 warnings).
**Standing position:** the 3 publisher-`logo` notes remain by design. The honest fix path
— if he ever wants it — is his call: supply/approve a proper raster logo lockup
(droplet + business name, ≥112×112 PNG, hosted on the domain). Do not improvise one.

### 2c. Article `image` (3 notes) — VERDICT: confirmed unfixable without inventing; notes stand
- `<img>` count in `out/` is **0** (§3); heroes are honestly empty gradient placeholders;
  no photo file exists anywhere in the export.
- No photo can be added without sourcing one, and no free-stock photo passed
  licence + place + subject for Fort Myers in the prior rounds. Adding a wrong-place /
  wrong-subject photo would violate his standing image rule (101% relevant, no wrong
  country/place) and would be worse than an empty hero.
- A logo-as-`image` would also be wrong: Google wants an image that represents the
  article itself, not a site-wide mark reused on every page.
- Article `image` is recommended, not required — validator: 0 errors, 0 warnings.
**Standing position:** the 3 Article-`image` notes remain by design.

## 3. IMAGES — 0 `<img>`, no wrong photo anywhere

| Check | Result |
|---|---|
| `<img>` tags in `out/` (68 HTML files) | **0** |
| `og:image` values anywhere in `out/` | **NONE** (0 hits in `index.html` and `cost/index.html`; `twitter:card` is `summary`, consistent — no large-image card claimed without an image) |
| `twitter:image` | None |
| Every image-file reference in `out/` (src/href/content matching `.svg/.png/.jpg/.jpeg/.webp/.gif/.ico/.avif`, plus a grep over all out/ files incl. CSS/JS) | **Exactly one: `/favicon.svg`** — referenced on all 68 HTML files (`<link rel="icon" href="/favicon.svg" type="image/svg+xml">`). Resolves: local `out/favicon.svg` 311 B (byte-identical to `site/favicon.svg`); live `https://fort-myers-water-damage-php.pages.dev/favicon.svg` **200, 311 B**. Appropriate: the site's own droplet brand mark (§2a). |
| `out/assets/img/` | Empty directory — no image files shipped at all |
| CSS `background-image` / image URLs | None found |
| Wrong / off-topic / wrong-place photo | **None exists to be wrong.** No photo anywhere in the export. |

## 4. MAP — pin URL sole maps URL; footer map absent on exactly the 7 location pages

| Check | Result |
|---|---|
| Distinct maps URLs in `out/` | **1 only:** `https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed` (city-level pin: Fort Myers + ZIP 33901, zoom 12). It appears once per iframe — 57 occurrences across 57 of the 68 HTML files (home/contact files contain it twice, once per iframe). |
| Iframes per page (route terms, 34 routes) | **0 iframes: exactly the 7 location pages** — `/areas/`, `/cape-coral/`, `/fort-myers-beach/`, `/estero/`, `/bonita-springs/`, `/lehigh-acres/`, `/north-fort-myers/`. **2 iframes: home + `/contact/`** (map section + footer map). **1 iframe: the other 25 routes** (footer map only). Total 57 iframes across 68 files (51×1 + 3×2 in file terms, incl. 404.html which has 1). |
| Map-section iframe (home + contact) | `<iframe class="map-embed" title="Map: Fort Myers and the Lee County service area" src="…pin URL…" width="1240" height="560" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen>` — no inline `style="border:0"` (the fix-round defect is gone). Rendered 1192×560 on desktop (container width). |
| Footer-map iframe (27 routes) | `<iframe class="footer-map" title="Map: Fort Myers and the Lee County service area" src="…pin URL…" width="560" height="280" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen>` — rendered 350×240 at 390px viewport (responsive). |
| Iframe a11y | Both iframe classes carry a descriptive `title`; both `loading="lazy"`. |
| No street address | No numbered-street address anywhere in the pin URL or embeds (city + ZIP only), per the service-area-business rule. |

**Live tiles — honest report:** rendered one map page (contact, desktop) and the home
footer map (mobile) in VM Chromium. Both iframes **requested the correct URL**
(performance resource entry confirmed:
`https://www.google.com/maps?q=Fort%20Myers%2C%20FL%2033901&z=12&output=embed`) and
both show their borders (gold 2px on the map-section embed — visible in
`qa/screenshots/10x-a11y/map-contact-desktop.png`; light border on the footer map —
`qa/screenshots/10x-a11y/map-footer-mobile-home.png`), but **no map tiles render** in
VM Chromium: the section embed is blank white, the footer embed is a flat dark-teal
fill. This is the known VM limitation (VM Chromium cannot reach google.com/maps), not a
markup defect — markup, pin URL, sizes and borders are all verified. Live tiles still
need one real-browser look (standing open item, unchanged).

## 5. LINKS / SITEMAP / ROBOTS / LLMS — all clean

| Check | Result |
|---|---|
| Total hrefs (34 flat route files + 404.html = 35 files) | **3,728** |
| Broken local targets | **0** (every internal href resolves to a real route; relative non-root hrefs: none) |
| Self-links inside `<main>` | **0** (relative and absolute forms checked; breadcrumb current crumb is a `<span>`, schema keeps the URL) |
| Fragment hrefs (`#…`) | 35, **0 missing targets** (all resolve to an `id` on the same page) |
| `tel:` values | Exactly one: `tel:+12393563708` sitewide |
| External links (distinct) | **2 only:** `https://fortmyerswaterdamagerestoration.us/` (canonical self-domain) and `https://msc.fema.gov` (FEMA Flood Map Service Center citation, `target="_blank" rel="noopener"`, in body copy — legitimate) |
| sitemap.xml | **31 `<loc>`**, all `<lastmod>2026-11-19</lastmod>`; live count also 31 |
| robots.txt | Global `Allow: /`; **15 named AI crawlers explicitly allowed** (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-Web, anthropic-ai, PerplexityBot, Google-Extended, CCBot, cohere-ai, Meta-ExternalAgent, Meta-ExternalFetcher, Applebot-Extended, DuckAssistBot, YouBot); **Bytespider `Disallow: /`**; `Sitemap: https://fortmyerswaterdamagerestoration.us/sitemap.xml`. Live: 17 `User-agent:` lines (15 AI + `*` + Bytespider), Bytespider block + Sitemap line confirmed live. |
| llms.txt | **31 entries**, URLs == sitemap locs in **identical order** (set equality also true); live count also 31 |

**Note — `qa/verify_export.py` could not run:** it shells out to `php` (line 307) and PHP
is not installed on this VM (`FileNotFoundError: [Errno 2] No such file or directory:
'php'`). It printed only `homepage: title 60ch, meta 150ch, copy words 5402` before
crashing. This is an environment gap, not a site finding — every check verify_export
performs was re-covered independently here (word/H1/title/meta checks were already
proven word-diff 0 in the prior rounds; links, sitemap, robots, llms, dashes and images
are all re-measured in this audit). Do NOT re-export; install PHP only if a re-export
is ever ordered.

## 6. ACCESSIBILITY + MOBILE — tap targets measured, overflow 0, FAQ open proven by pixels

### 6a. Overflow + body text
- `qa/render_check.py` re-run: **completed, exit 0, "render check done"** — overflow 0 at
  320/360/390/1440 and body font 20px on all routes. (First run crashed mid-way with a
  Chromium `TargetClosedError: Page crashed` after ~11 routes; the rerun completed clean
  — transient, not a site defect.)
- Independent probe (own Playwright script, all 34 routes × 4 widths): **overflow 0 on
  all 136 route/width combinations; body font 20px on all 34 routes at both 390px and
  1440px.** The two methods agree.

### 6b. Tap targets — real rendered sizes (Playwright `getBoundingClientRect`)

| Target group | Desktop 1440px | Mobile 390px | vs 44px bar |
|---|---|---|---|
| Header nav links + Services/Areas summaries | 53–85px tall (dropdown items 300×53; summaries 105×85 / 79×85) | nav hidden by design; see menu row | PASS |
| Header call button (`.btn-call`) | 255×52 | hidden ≤620px by design; sticky call bar serves instead | PASS |
| Mobile menu toggle (`☰Menu`) | n/a (desktop) | 86×55 | PASS |
| Mobile menu items (menu opened by real click) | n/a | 342×61 (first 6 sampled, all 61px) | PASS |
| Mobile sticky call bar (`.call-bar`) | n/a | 390×66 | PASS |
| FAQ summaries (`.faq-item summary`) | 73px tall, ~1190px wide | 64–92px tall, 348px wide | PASS |
| FAQ `+`/`−` badge (`summary::after`) | 38×38px circle (CSS) | 34×34px circle (CSS) | n/a — the badge is not the target; the whole 73/92px summary row is the tap target |
| Footer call button (first footer link) | 60px tall (inline-flex, padding 16×28) | same | PASS |
| **Footer column links** | **238×40** | **350×40** | **4px short — see finding F-1** |
| **Footer phone text link** (`239-356-3708`) | **123×29** | **123×29** | **short — see finding F-1** |
| Inline body-text links (prose) | ~24px tall (one line of 20px text), 62–278px wide | same | Exempt in practice — inline links are not discrete targets (WCAG 2.5.8 inline exception; 24px meets the 24×24 minimum) |

**F-1 (P3, the only finding): footer links are 40px tall, not 44px.**
`.footer-col a` is 18px font, `line-height: 1.45` (26px) + 7px vertical padding = 40px
tall on desktop and mobile; the footer phone text link has no padding and measures
29px tall. Against the strict 44×44 bar set for this audit they fall short (by 4px and
15px). Context: they **pass WCAG 2.2 AA target-size minimum (24×24)** by a wide margin,
are 238–350px wide (easy to hit horizontally), and are stacked with no competing
targets adjacent — this is a polish item, not an accessibility failure. Fix (not done
here — read-only audit): raise footer link vertical padding to 9px+ (40→44px) and give
the footer phone link the same treatment.

### 6c. FAQ OPEN state — proven by pixels this round (was CSS-only last round)
Method: real `.click()` on a `.faq-item summary` (home, desktop) and on contact
(mobile 390px) — NOT the `open` attribute alone, and NOT the header Services/Areas
`<details>` (a first-round probe clicked the wrong `<details>` — index 0 is the header
Services dropdown, 105×85 — and measured that instead; corrected here to
`.faq-item` selectors only).
- Desktop home, FAQ #2 ("What does water damage restoration include?"):
  `open: true`, item height 254px, **border-left 5px solid gold `rgb(201,155,63)`**,
  1px teal border, shadow `rgba(10,46,56,0.14) 0 10px 30px`, summary 73px.
  Screenshot `qa/screenshots/10x-a11y/faq-open-desktop.png` — **viewed**: teal question,
  coral `−` badge, gold left accent, answer divider line, answer text + underlined
  links all visible, no overlap.
- Mobile contact, FAQ #1 ("Can I get a price over the phone?"): `open: true`, item
  height 365px, same 5px gold left border, summary 92px. Screenshot
  `qa/screenshots/10x-a11y/faq-open-mobile-contact.png` — **viewed**: clean, badge
  aligned, answer fully visible.
- The open-state CSS matches the pixels: `.faq-item[open] { border-color: teal;
  border-left: 5px solid gold; box-shadow }`, `summary::after` switches `+` → `−` on
  coral. The CSS-only caveat from the fix round is now **closed**.

### 6d. Screenshots saved (this audit)
`qa/screenshots/10x-a11y/` — `faq-open-desktop.png`, `faq-open-mobile-contact.png`,
`map-contact-desktop.png`, `map-footer-mobile-home.png`, `favicon-200px.png`.
(A mobile-menu screenshot taken during probing captured only the toggle element and was
deleted as misleading; the menu-item sizes above are the measured evidence.)

## 7. FINDINGS SUMMARY

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F-1 | P3 | Footer column links 40px tall (footer phone text link 29px) vs the 44px tap-target bar | §6b — measured on home, water-removal, contact, desktop + mobile; CSS `.footer-col a` 18px/1.45 + 7px padding |
| — | — | 6 by-design schema notes stand (3× Article `image`, 3× publisher `logo`) | §2 — favicon is a real brand mark but has no wordmark, is 64×64 (< 112px floor), and rasterising it would invent a brand asset; no photo exists for Article `image` |
| — | — | Live map tiles still need one real-browser look | §4 — VM Chromium shows blank tiles despite the correct URL being requested; borders + markup verified |

**Not findings:** schema 0/0; BreadcrumbList `item` on every live ListItem; 0 broken links;
0 self-links in `<main>`; sitemap 31 = llms 31 (identical order); robots 15 AI allowed +
Bytespider disallowed + Sitemap line; 0 `<img>` / 0 `og:image` / only image ref is the
own favicon; map pin URL sole maps URL; footer map absent on exactly the 7 location
pages; overflow 0 everywhere; 20px body text everywhere; FAQ open state pixel-proven.

## 8. METHOD NOTE
- `python3 qa/validate_schema.py` — ran clean (0/0, 6 notes).
- `python3 qa/verify_export.py` — blocked by missing PHP (environment, §5).
- `python3 qa/render_check.py` — rerun completed clean (first run transient Chromium crash).
- Own static census (Python, over `out/`): hrefs, fragments, iframes, maps URLs, image refs.
- Own Playwright probes (bundled Chromium, local `python3 -m http.server` on 127.0.0.1:8123,
  stopped by PID after use): overflow/font × 34 routes × 4 widths, tap-target
  measurements, real-click FAQ-open screenshots, map render, favicon render.
- Live curl: BreadcrumbList on 2 inner pages, sitemap/robots/llms counts, favicon 200,
  home md5 == local out/index.html.
