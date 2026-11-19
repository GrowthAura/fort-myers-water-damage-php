# FINDINGS — Task 12: Menu = 7 services only (Fort Myers NEW PHP site)

Owner order: "menu ma just 7 services add kro, jo bach jaye wo footer ma add kro"
Proposal files only — no shared file was edited, no commit, no push.
Patch: `qa/patch-menu-7.txt` (exact old/new code for `pages.php` + `header.php`;
`footer.php` needs no code change — its loop already iterates the full list).

## 1. What was read

- `site/data/pages.php` — `$NAV_SERVICES` (12), `$NAV_AREAS` (7), `$FOOTER_EXPLORE` (9), `$FOOTER_AREAS` (7)
- `site/includes/header.php` — desktop Services `<details>` dropdown loop (line 75),
  mobile-menu Services loop (line 117), `$inServices` marker loop (line 8)
- `site/includes/footer.php` — footer Services loop (line 16); no "More services" list exists today
- Grep of the whole `site/` tree for `$NAV_SERVICES`: only `pages.php` (definition),
  `header.php` (lines 2, 8, 75, 117) and `footer.php` (lines 1, 16). Nothing else uses it.

## 2. Full service inventory — 17 pages, not 12

Every page below carries `@type: Service` schema in its data file. The 12 in
`$NAV_SERVICES` today are #1–12. **#13–17 are live service pages with NO header or
footer navigation at all today** — reachable only via in-content links / sitemap.
That is the finding the footer count must be judged against: footer = 17, not 12.

| # | Service page | href | Nav label today |
|---|---|---|---|
| 1 | Emergency Water Removal | `/water-removal/` | Emergency Water Removal |
| 2 | Structural Drying | `/drying/` | Structural Drying |
| 3 | Sewage Backup Cleanup | `/sewage-cleanup/` | Sewage Backup Cleanup |
| 4 | Flood & Storm Cleanup | `/flood-cleanup/` | Flood & Storm Cleanup |
| 5 | AC Leak Water Damage | `/ac-leak/` | AC Leak Water Damage |
| 6 | Ceiling Leak Water Damage | `/ceiling-leak/` | Ceiling Leak Water Damage |
| 7 | Burst Pipe Water Damage | `/burst-pipe/` | Burst Pipe Water Damage |
| 8 | Slab Leak Water Damage | `/slab-leak/` | Slab Leak Water Damage |
| 9 | Water Heater Leak Cleanup | `/water-heater-leak/` | Water Heater Leak Cleanup |
| 10 | Condo Water Damage | `/condo-leak/` | Condo Water Damage |
| 11 | Mobile Home Water Damage | `/mobile-home/` | Mobile Home Water Damage |
| 12 | Commercial Water Damage | `/commercial/` | Commercial Water Damage |
| 13 | Cast Iron Pipe Water Damage | `/cast-iron-pipe/` | — NONE (proposed, §4) |
| 14 | Seasonal Home Water Damage | `/vacant-home/` | — NONE (proposed, §4) |
| 15 | Appliance Leak Water Damage | `/appliance-leak/` | — NONE (proposed, §4) |
| 16 | Water Damaged Floors | `/floors/` | — NONE (proposed, §4) |
| 17 | Water Damaged Kitchen Cabinets | `/cabinets/` | — NONE (proposed, §4) |

Not services (correctly excluded from both lists): guides — `/cost/`, `/insurance/`,
`/first-hour-checklist/`, `/how-it-works/` (header top-level / footer Explore);
areas — 6 area pages + `/areas/` (Areas dropdown / footer Areas); home, contact,
about, legal pages. `/about/` is still pending content — unaffected.

## 3. Chosen 7 for the header menu (+ reasoning)

Chosen 7 — header Services dropdown (desktop) AND mobile-menu Services list:

1. **Emergency Water Removal** (`/water-removal/`) — the core emergency service;
   highest-intent "need help now" search, the first thing a flooded home needs.
2. **Structural Drying** (`/drying/`) — follows every water job; core revenue service,
   "drying" is the highest-volume follow-on term after removal.
3. **Sewage Backup Cleanup** (`/sewage-cleanup/`) — emergency + high revenue per job,
   distinct hazard category users search by name; must be one tap away.
4. **Flood & Storm Cleanup** (`/flood-cleanup/`) — Fort Myers / hurricane + storm-surge
   market: the highest local traffic driver of all services in this area.
5. **AC Leak Water Damage** (`/ac-leak/`) — the #1 Fort Myers cause (AC drain line,
   year-round cooling season); very high local search volume, strongly local.
6. **Ceiling Leak Water Damage** (`/ceiling-leak/`) — high-volume symptom search
   ("water leaking through ceiling"); how most homeowners first describe the problem.
7. **Burst Pipe Water Damage** (`/burst-pipe/`) — classic emergency, high-volume
   search, immediate-dispatch intent.

Scoring used: traffic value (local search volume for the problem as users word it)
+ emergency value (needs a call now vs. can wait) + revenue value (job size).
This is also the owner's own suggested set (water removal, drying, sewage, flood,
burst pipe, AC leak, ceiling leak) — it survives the scoring, so it is adopted
unchanged. Note: the 7 are exactly the FIRST 7 entries of today's `$NAV_SERVICES`,
in the same order — the patch keeps that order, so the menu reads as today minus 5.

Why the other 7 existing nav services go to the footer (not dropped):
- **Slab Leak** — high revenue per job, but lower search volume than the 7 and a
  slower, diagnostic sale; footer keeps it one click away.
- **Water Heater Leak** — common emergency, but users usually search "water heater
  leak" and land via content/SEO; the menu's 7 already cover the emergency intent.
- **Condo Water Damage** — important Fort Myers segment (high-rise / HOA jobs) but
  narrower audience than the 7 symptom-based entries.
- **Mobile Home Water Damage** — real local segment, smaller audience than the 7.
- **Commercial Water Damage** — highest ticket size, lowest search volume; businesses
  find it via footer / contact, not the consumer menu.
- The 5 newly listed services (§4) were never in the menu, so they go footer-only
  by definition — they gain navigation instead of losing it.

Owner may swap any pick: e.g. Slab Leak in for Ceiling Leak if revenue-per-job
outweighs symptom volume, or Commercial in for Burst Pipe if B2B is the priority.
Any swap is a one-line change in `$NAV_SERVICES_MENU` only; the footer stays 17.

## 4. Footer list — ALL 17 services (including the 7)

Footer Services column after the patch (order = `$NAV_SERVICES` order, existing
12 first in today's order, then the 5 newly added in sitemap order):

1. Emergency Water Removal — `/water-removal/`
2. Structural Drying — `/drying/`
3. Sewage Backup Cleanup — `/sewage-cleanup/`
4. Flood & Storm Cleanup — `/flood-cleanup/`
5. AC Leak Water Damage — `/ac-leak/`
6. Ceiling Leak Water Damage — `/ceiling-leak/`
7. Burst Pipe Water Damage — `/burst-pipe/`
8. Slab Leak Water Damage — `/slab-leak/`
9. Water Heater Leak Cleanup — `/water-heater-leak/`
10. Condo Water Damage — `/condo-leak/`
11. Mobile Home Water Damage — `/mobile-home/`
12. Commercial Water Damage — `/commercial/`
13. Cast Iron Pipe Water Damage — `/cast-iron-pipe/` *(new label, proposed)*
14. Seasonal Home Water Damage — `/vacant-home/` *(new label, proposed)*
15. Appliance Leak Water Damage — `/appliance-leak/` *(new label, proposed)*
16. Water Damaged Floors — `/floors/` *(new label, proposed)*
17. Water Damaged Kitchen Cabinets — `/cabinets/` *(new label, proposed)*

**New labels (#13–17) — flag for the owner:** no nav label existed for these pages,
so these are proposed, not preserved. Each is taken from the page's own title/H1
minus geography, following the existing label pattern (short service name, no city):
- #13 from H1 "Cast Iron Pipe Water Damage in Fort Myers and Cape Coral".
- #14 from title "Seasonal Home Water Damage Fort Myers | Came Back to a Leak?"
  (alternative the owner may prefer: "Vacant Home Water Damage", from the slug).
- #15 from H1 "Appliance Leak Water Damage in Fort Myers".
- #16 from H1 "Water Damaged Floors in Fort Myers Homes".
- #17 from H1 "Water Damaged Kitchen Cabinets in Fort Myers".
No existing label or href is changed anywhere in this patch.

## 5. Current state today (before the patch)

- Header desktop Services dropdown: **12** (all of today's `$NAV_SERVICES`)
- Mobile menu Services list: **12**
- Footer Services column: **12** — and the 5 unlisted services (#13–17) appear nowhere
- Header Areas dropdown: 7; mobile Areas list: 7; footer Explore: 9; footer Areas: 7
- No "More services" list exists anywhere.

## 6. Verification plan (for the coordinator, after applying the patch)

Render with the PHP server and count rendered items (a link OR a `nav-current`
span on its own page both count as one item — the current page renders as a span,
not a link, so count elements, not just `<a>` tags):

| Check | Where | Expected |
|---|---|---|
| Desktop Services dropdown | `details.nav-services .nav-dropdown` (home + one service page) | **7** |
| Mobile menu Services list | `.mobile-menu-panel` under the "Services" group | **7** |
| Footer Services column | `nav[aria-label="Services"]` | **17** |
| Header Areas dropdown | `details` Areas `.nav-dropdown` | 7 (unchanged) |
| Mobile Areas list | `.mobile-menu-panel` under "Areas" | 7 (unchanged) |
| Footer Explore / Areas | footer columns | 9 / 7 (unchanged) |
| Union | header 7 ∪ footer 17 | **17 = every @type Service page** |
| Reachability | every service href appears in header or footer | **17/17** |
| No self-link break | current page renders as `nav-current` span in each list it belongs to | spot-check on `/slab-leak/` (footer-only: footer span, header menu must NOT contain it, but the Services dropdown must still carry the `nav-section-current` marker) and on `/water-removal/` (in all three lists) |
| Labels/hrefs | diff rendered labels + hrefs against §2 table | identical; only the 5 new labels in §4 are new |

Also verify: no PHP error (both new arrays defined before `header.php`/`footer.php`
run — they live in `pages.php`, already loaded first); `styles.css`/`main.js` untouched
(no new classes or markup); Areas dropdown byte-identical behaviour.

## 7. Deliverables

- `qa/patch-menu-7.txt` — exact old/new code (pages.php data, header.php globals +
  desktop loop + mobile loop; footer.php needs no code edit).
- `qa/FINDINGS-menu-7.md` — this file.
