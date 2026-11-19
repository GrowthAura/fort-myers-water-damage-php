# Homepage hero — findings (Fort Myers PHP site)

**Date:** 2026-11-19
**Slot:** homepage hero, full-width, desktop ~1600×900 (16:9), mobile ~800px wide, dark scrim + H1/intro/call buttons on top
**Verdict: HONESTLY EMPTY — nothing installed.** No free-stock photo passes all three gates (licence + place + subject). The `site/assets/img/` directory is intentionally left empty. Do NOT force any photo below into the slot.

## What was searched

- **Wikimedia Commons** — full 372-file category "Effects of Hurricane Ian in Florida" (imageinfo pulled for all 372; keyword-filtered + viewed 17 shortlisted thumbs at full size), "Effects of Hurricane Milton in Florida" (38 files), File-namespace searches ("Fort Myers flood", "Fort Myers Beach flooding", "Hurricane Milton Fort Myers", "Fort Myers storm surge").
- **Pexels** — search pages "florida flood", "fort myers", "hurricane ian florida", "fort myers beach" (photo pages opened for 13865771 and 14216445 to confirm photographer, date, dimensions, location).
- **Openverse API** (Flickr CC + Commons, licences by/by-sa/cc0) — "Fort Myers Hurricane Ian flood", "Fort Myers Beach Hurricane Ian", "Cape Coral Hurricane Ian flooding", "Sanibel Hurricane Ian flood", "Fort Myers flood", "Lee County Florida flood", "Caloosahatchee flood", "Fort Myers Beach flood water street".
- **image-search CLI** — "Fort Myers Florida flooded street palm trees hurricane" (returned news-agency photos — AP etc. — not free licence; unusable).

## Near-misses (each viewed at full size; why each fails)

### 1. Wikimedia — CBP aerial `220929-H-DO456-0204.jpg` (closest, still fails)
- **What it is:** U.S. Customs and Border Protection Air and Marine Operations UH-60 aerial, 29 Sep 2022 14:03, 5000×3333, public domain (PD US DHS). Top-down aerial of canal-front homes with damaged roofs, debris fields, dark canal water, palms. Bright daylight; would read under a scrim. No people, no helicopter-frame intrusion (tiny dark corner bottom-left only). File page: https://commons.wikimedia.org/wiki/File:220929-H-DO456-0204.jpg
- **Why it fails — place UNVERIFIED:** description says only "flew along the Florida coast". No GPS, no location category. The dense canal-grid of homes is characteristic of **Cape Coral** (Lee County), not Fort Myers proper — Fort Myers Beach is a barrier island with no such grid. I cannot verify the city is Fort Myers, and the task + standing rule require 101% place relevance. Installing it as a "Fort Myers" hero would assert a place I cannot prove.
- **Why it fails — subject:** it is a top-down aerial of wind-damage rubble; the "water" is dark canal water, not floodwater on a street or in a home. As a water-damage hero it reads as "disaster rubble", not "flood/water damage".
- **Reuse check:** appears NOWHERE in ~/workspace (filename + content grep, zero hits). Proven a different photo from the banned old hero and from the beached-yacht wreckage photo (see nets below). Not installed anyway, for the reasons above.

### 2. Pexels 13865770 / 13865771 / 13865772 / 13865773 / 13865776 / 13865778 (+ portrait 13865768/75/77/79) — Connor Scott McManus series
- **What they are:** Hurricane Ian flooding, 2 Oct 2022, 6240×4160, Pexels free licence. Bright, genuinely Floridian (palms, flooded streets, marina, road-closed signs, lakefront). 13865772 (flooded street, barriers reflecting in water) is the best-composed frame of the lot.
- **Why they fail — WRONG PLACE:** the photographer's Pexels pages title them "in Sanford" — **Sanford, FL, Lake Monroe / St. Johns River, inland central Florida, ~200 miles NE of Fort Myers**. Not Fort Myers, not the Gulf coast, not the Caloosahatchee. A lakeside/marina flood in Sanford is a wrong-place photo by the same standard that banned the European house. (13865768/75/77/79 are also portrait orientation — unusable for a 16:9 hero without a destructive crop.)
- **Reuse check:** no live-served copies found anywhere in ~/workspace (only QA candidate dirs on Lancaster, San Bruno, Acworth, Elyria, Rocky Mount — evaluated, never installed). Not installed anyway, for place.

### 3. Pexels 14216445 / 14216447 — same photographer, same Sanford shoot
- **What they are:** Connor Scott McManus, 29 Oct 2022, 6240×4160, Pexels free licence. Flooded urban street, palms, overcast. Dark/moody — would go muddy under a dark scrim.
- **Why they fail:** same Sanford place failure as #2, plus dark. **14216445 is additionally a PROVEN REUSE — live right now on Plano 3** (`plano3-water-damage/public/images/flooded-floor-14216445.webp`, plus `out/` and `plano3-publish/` copies). 14216447 has zero hits anywhere but is the same shoot/place. 14216449 (sibling frame) is already on the banned list (Owasso/Lancaster).

### 4. Wikimedia — "Wreckage in Fort Myers in April 2023" (CC0, Mx. Granger)
- **What it is:** ground-level Fort Myers wreckage, 4000×2168 — beached yacht + crane + palms + rubble, blue sky. Genuinely Fort Myers.
- **Why it fails:** matches the banned old-hero description (beached yacht + palms + crane) and shows **no water at all** — it is a dry wreckage lot seven months after Ian. Wrong subject for a water-damage hero. Not installed.

### 5. Wikimedia — Florida National Guard Fort Myers Beach set (CC BY 2.0, SrA Jesse Hanson)
- Files 52396323142 / 52396833336 / 52397331803 (RED HORSE clearing roads, 30 Sep 2022), 52402266144 (tattered US flag over a destroyed foundation, 2 Oct 2022, 8058×5372), 52402481088 (soldiers evacuating citizens + dog).
- **Why they fail:** every frame is military/rescue-personnel dominant (soldiers, skid-steer, military truck) — not a homeowner water-damage scene. The flag photo has no people but also **no water** (dry foundation rubble). Not installed.

### 6. Wikimedia — "Flooded highway due to Ian.jpg" (public domain, CBP, 5000×3333)
- Aerial oblique of a flooded highway (US 17 at Charlie Creek) with cars, green flat Florida landscape, blue floodwater. Bright, dramatic, genuinely Florida floodwater.
- **Why it fails:** US 17 at Charlie Creek is **Hardee County, inland central Florida** — not Fort Myers, not the Gulf coast. Wrong place. Not installed.

### 7. Wikimedia — Hurricane Milton set (38 files)
- "Intersection flooded by Milton" is **Volusia County** (east coast) and only 1171×879 — too small and wrong place. "Flooded field…" has no homes/street and unverified location. Keys photos are the Florida Keys. The North Fort Myers file is EF2 tornado damage to a mobile home — no water. All rejected.

### 8. Banned / already-live (confirmed by viewing + nets, do not install)
- Old homepage hero `fort-myers-florida-storm-flooding-hero.jpg` — **viewed: it IS the European house (Pexels 28447774)**: white house, tiled roof, red fence, muddy water. Banned.
- Pexels 28447774 (European house), 8292785 / 8293664 (inspectors), 11899611 (Lancaster washing machine), 14216449 (Owasso/Lancaster), 32497161, 6419128, 8293678, 15206136, 16509869, 32497162 — none used.
- Any U.S. Navy Seabees photo (Breezy Point NY 2012) — none used. (Note: the Seabees photo is still live on the separate Next.js Fort Myers site by the user's own call; that is out of scope here and untouched.)
- Sister-site Fort Myers images `fort-myers-lee-county-storm-coast.jpg` and `fort-myers-florida-gulf-coast-storm.jpg` — live on the old sites; reuse, not used.

## Reuse + fit verification (fresh disk reads, 2026-11-19)

- **md5 + aHash (8×8 and 16×16, pure-PIL implementation):** computed fresh from the files on disk (1200px thumbs for the web candidates, original local files for the banned/sister images). Self-comparisons return 0/0, so the implementation is sound. **No aHash ≤8 flag anywhere** — all pairwise distances are large (8×8: 28–44; 16×16: 112–156). In particular:
  - CBP 0204 vs banned old hero: md5 differ, aHash8 34, aHash16 131 — **proven a different photo, not a crop**.
  - CBP 0204 vs beached-yacht wreckage photo: aHash8 39, aHash16 139 — different photo.
  - CBP 0204 vs sister lee-county / gulf-coast images: aHash8 36 / 44 — different photos.
  - Sanford Pexels frames vs banned hero: aHash8 28–44 — different photos (their failure is place, not reuse).
- **Pexels-ID filename/log grep across ALL of ~/workspace** (fresh `find`, incl. export dirs `*/out*/images`, `*/public/images`, `*/assets*`, `*gh-pages*`, `*export*`, `*dist*`):
  - `14216445` → **LIVE on Plano 3** (`public/images/flooded-floor-14216445.webp` + `out/` + `plano3-publish/` copies). Also in Lancaster img-scout pool and Apopka QA candidates.
  - `14216449` → Lancaster pool + Apopka candidates (banned already).
  - `14216447` → zero hits anywhere.
  - `13865770–13865779` → QA candidate dirs only (Lancaster, San Bruno, Acworth, Elyria, Rocky Mount); **no live-served copies** in any public/out/assets/export dir.
  - `DO456-0204` → zero hits anywhere in ~/workspace (never used before).
  - Banned IDs (28447774, 8292785, 8293664, 11899611, 32497161, 6419128, 8293678, 15206136, 16509869, 32497162) → none installed here.
- **Corpus note:** the filename/ID grep covered the whole workspace (two `find` passes, ~60s and ~107s); the hash net compared the six shortlisted candidates against the three Fort Myers sister-site images on disk. No stale manifest was used. No aHash ≤8 flag arose, so no side-by-side MAD adjudication was triggered.
- **Viewed-pixel verdicts:** every shortlisted photo above was viewed at full size (contact sheets + full-size reads of the CBP aerial and the banned hero). Judgements above are from the pixels, not from titles or hashes.

## EXIF / AI check
- No file was installed, so there is nothing to strip or check. For the record: all shortlisted web candidates are real photographs (US federal / National Guard / Pexels photographer Connor Scott McManus, Oct 2022); none is AI-generated and none carries AI metadata. The Canva "AIGC bundle" images that Pexels search interleaves were ignored, not downloaded.

## Files delivered
- **None.** `~/workspace/fort-myers-php/site/assets/img/` is empty by design; no `fort-myers-php-homepage-hero-1600.jpg` / `-800.jpg` was created.
- This note: `~/workspace/fort-myers-php/qa/hero-findings.md` (this file).

## Recommendation for the coordinator
Leave the hero slot empty (or a plain branded/scrim treatment) until one of these happens — do not ship the Sanford series or the CBP aerial as "Fort Myers":
1. A real job photo from the user's own Fort Myers work (best option; the Next.js site's own history shows free stock cannot supply a verified Fort Myers flood photo), or
2. Licensed stock with a verifiable Fort Myers caption, or
3. The user's explicit call to accept the closest honest frame (CBP 0204 aerial, labelled as Southwest Florida coast — NOT as Fort Myers proper — with its place caveat stated on the record).
