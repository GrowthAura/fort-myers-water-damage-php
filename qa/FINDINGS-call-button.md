# Call button — "with your ZIP code" — findings (Fort Myers PHP, homepage only, Task 8)

**Date:** 2026-11-19 · **Worker:** homepage-cards (Task 8) · **Status:** proposal file only — no shared file was edited, no commit, no push. The coordinator applies the patch and screenshots desktop + mobile.

## Which block it is

- **Location:** `site/data/homepage.php`, the `'p'` block immediately after the ZIP/areas table (the table listing ZIP codes per area), before H2 "Water Damage Help Across Lee County".
- **Original text (single segment, verbatim):** `Not sure your street is covered? Call 239-356-3708 with your ZIP code.`
- **Scope:** this text occurs exactly once on the site (grep "with your ZIP code" hits only this line in `site/data/`). Homepage only.

## What changed

- The phone number becomes a real call button: `<a class="btn btn-call" href="tel:+12393563708">[phone SVG] Call 239-356-3708</a>` — the same `.btn-call` style and the same `phone_svg()` + `Call 239-356-3708` markup as the hero call button (and the `cta-line` button), with the href hardcoded to `tel:+12393563708` exactly as in the hero and cta-line cases.
- The rest stays as surrounding text in the same sentence: `Not sure your street is covered? ` before the button, ` with your ZIP code.` after it.
- **Word accounting (all words survive, each exactly once):** the original sentence is `Not sure your street is covered? Call 239-356-3708 with your ZIP code.` The render branch splits the segment on the phone number; the trailing `Call ` moves into the button label so the word "Call" appears once (in the button), not twice. Rendered line reads: `Not sure your street is covered? [Call 239-356-3708] with your ZIP code.` — every word of the original is present.
- **No other change:** no words added, removed or reworded; no other block touched. The plain `<p>` render path is unchanged for every other paragraph (the branch only fires when the block carries `'variant' => 'call-button'`).
- **Why a branch, not `render_segments`:** the existing `render_segments()` auto-links the phone number as a plain inline `tel:` link. A button needs different markup (class + SVG + "Call " label), so the branch renders the split explicitly instead of calling `render_segments()` for this block. If the number is absent (defensive path), the text renders unchanged as plain text.
- **Patch:** `qa/patch-call-button-homepage.txt` — verbatim OLD (data `p` block + functions.php `p` case) and NEW (one `'variant' => 'call-button'` line in the data + the `call-button` branch in the `p` case). The NEW data block was verified to differ from OLD by exactly that one line; the NEW branch was `php -l` linted and stub-rendered.
- **CSS:** one spacing rule, included in the patch file (`.call-zip-line .btn { margin: 4px 8px; vertical-align: middle; }`). No new button styling — `.btn` / `.btn-call` already exist.

## Tap-target measurement — proves >= 44px

From `site/assets/css/styles.css` (existing rules, no fix needed):

- `.btn { font-size: 20px; line-height: 1.2 (= 24px); padding: 16px 28px; min-height: 56px; }`
- Rendered height = max(56px min-height, 24px text + 32px vertical padding) = **56px**.
- **56px ≥ 44px — PASS.** Same measurement as the hero call button, which uses the identical classes. No height fix was required or included.

## Confirmation all words survived

Stub-render of the NEW branch (with the real segment text) produced:

`<p class="call-zip-line">Not sure your street is covered? <a class="btn btn-call" href="tel:+12393563708">[phone SVG] Call 239-356-3708</a> with your ZIP code.</p>`

Word-by-word against the original `Not sure your street is covered? Call 239-356-3708 with your ZIP code.`:

| Original word | Present in rendered line | Where |
|---|---|---|
| Not | ✓ | lead text |
| sure | ✓ | lead text |
| your | ✓ | lead text |
| street | ✓ | lead text |
| is | ✓ | lead text |
| covered? | ✓ | lead text |
| Call | ✓ | button label |
| 239-356-3708 | ✓ | button label (+ `tel:+12393563708` href) |
| with | ✓ | trailing text |
| your | ✓ | trailing text |
| ZIP | ✓ | trailing text |
| code. | ✓ | trailing text |

**Words added: 0. Words removed: 0. Words reordered: 0.** The button is the phone number itself, not an extra label.

## Deliverables

- `qa/patch-call-button-homepage.txt` (verbatim OLD + NEW)
- This file: `qa/FINDINGS-call-button.md`

**Not done here (coordinator):** applying the patch, real render on the PHP site, desktop + mobile screenshots (button wrapping on a 390px line: the button is inline-flex inside the paragraph, so on narrow screens it wraps below the lead text — verify visually).
