# FINDINGS — Authorized sentence removals (Tasks 9 + 10)
## Fort Myers NEW PHP site — ordered by the owner ~18:17 PKT, removed by the coordinator

Both sentences are on the HOMEPAGE (site/data/homepage.php). Each was a whole
standalone 'p' block; the whole block was removed (words + links). No other
word on any page was touched by these two edits.

## Task 9 — FEMA flood-zone sentence — REMOVED
- Page: / (homepage), site/data/homepage.php, was a 'p' block just before the
  h2 "Do You Need a Restoration Company in Fort Myers, or Can You Handle It Yourself?"
- Exact sentence removed (verbatim):
  "Not sure which flood zone you are in? Look up your address on FEMA's Flood Map Service Center (msc.fema.gov) or ask your building department for the elevation certificate on file."
- Link removed with it: msc.fema.gov (auto-linked by render_segments).

## Task 10 — Category 3 sewage sentence — REMOVED
- Page: / (homepage), site/data/homepage.php, was a 'p' block just before the
  h2 "Why Water Damage Spreads Faster in Fort Myers and Lee County"
- Exact sentence removed (verbatim, segments joined):
  "Once the line is open, everything the sewage touched is treated as Category 3. See sewage backup cleanup and cast iron pipe water damage."
- Links removed with it: "sewage backup cleanup" -> /sewage-cleanup/ and
  "cast iron pipe water damage" -> /cast-iron-pipe/.

## Word-diff impact
- The homepage word count drops by exactly these two sentences (FEMA: 30 words;
  Category 3: 22 words). All other pages: word-diff 0 from these edits.
- The independent verifier must check: word-diff across all 34 pages equals
  ONLY (a) these two sentences, (b) the Task 6 "See ..." sentence removals,
  (c) the Task 13 removed related items, and (d) the Task 13 homepage anchor
  text variations — nothing else.

## CORRECTION — word counts (coordinator, 2026-11-19 ~20:30 PKT)
The counts above (FEMA 30, Category 3 22) were hand-counts. The verifier's words()
splits on every non-word character (hyphens split, "FEMA's" -> 2, "(msc.fema.gov)" -> 3),
giving FEMA = 33 words and Category 3 = 24 words, sum 57 — exactly the observed
homepage word-diff (-57: 5345 vs 5402). The sentences removed are unchanged; only the
counts were off. Reconciled in the copy-verify (129/129 authorized, 0 problems).
