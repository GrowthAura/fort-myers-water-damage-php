# SPEED AUDIT — Fort Myers NEW PHP site, 10X round
## `~/workspace/fort-myers-php/` — 2026-11-19 ~11:00–12:00 PKT — READ-ONLY audit (no site file edited)

## 0. Verdict up front

**The mobile Performance variance (78–98 across all rounds) is host CPU noise amplified by the 4× CPU throttle — not a page defect.** The page itself is light (147 KB total, 6 requests, 661 B of deferred JS, zero images) and there is no render-blocking, font, JS, or iframe culprit to find. Two things are true at once:

1. **Observed (real) behaviour is stable and good:** in all 14 lab runs the page paints exactly once, complete — observed Speed Index == observed First Contentful Paint in 14/14 runs. There is no real late visual event.
2. **The simulated numbers swing because the VM's CPU speed swings.** Byte-identical pages show parseHTML 22→419 ms (19×), style/layout 767→2,327 ms (3×), "other" 209→838 ms (4×), and observed FCP 0.94→2.35 s (2.5×) while the load event stays stable at 0.15–0.35 s. Deterministic work on identical input cannot vary 19× unless the CPU underneath varies. The 4× throttle then multiplies that host noise into simulated FCP 1.2–2.6 s, TBT 0–464 ms, and Perf 86–98.

Desktop is Perf 100 on every run (no throttling). CLS is 0 on every run. Live Speed Index is **still unmeasured** — PageSpeed Insights still returns 429 (see §6).

## 1. Method

- **Tool:** Lighthouse 13.6.0 (`npx --no-install lighthouse`, already in the npx cache — nothing installed).
- **Browser:** Playwright's bundled Chromium 153.0.8010.12 (`~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`), via `CHROME_PATH` env var. Two launch quirks, both fixed without touching the site: Lighthouse 13 ignores `--chrome-path` (needs the env var), and Chrome must be launched with `--no-sandbox --disable-dev-shm-usage --disable-gpu --headless=new` in this VM (without `--no-sandbox` it dies as root with a zygote error; `--headless=new` is what makes the DevTools port appear).
- **Preset:** mobile = Lighthouse default (simulated slow 4G: 1.6 Mbps / 150 ms RTT + 4× CPU throttling); desktop = `--preset=desktop` (no throttling).
- **Server:** local static export `~/workspace/fort-myers-php/out/`, served with `python3 -m http.server`. **Incident:** the run started against port 8123 (a server another agent had left running). It served run 1, then **died mid-batch** (curl 000, PID gone) — every later run in that batch failed with Chrome's "interstitial" error. The remaining 11 runs were done against my own server on port **8124** (PID 18772, ThreadingHTTPServer, stopped by PID after the audit). No file was re-exported (PHP is not installed on this VM, per the task).
- **Runs:** homepage + `/how-it-works/` + `/cost/`, mobile ×3 each + desktop ×1 each, plus 2 probe runs (test1/test2) = 14 successful runs. Performance category only.
- **Lab-vs-live caveat:** `python3 -m http.server` serves uncompressed HTTP/1.1 with no caching. Live Cloudflare Pages serves Brotli + HTTP/2 + edge cache (see §4 for the gzip math) — lab transfer sizes are a pessimistic ceiling. The CPU side of the lab numbers is the real story, not the bytes.

## 2. Results

### 2.1 Mobile (simulated slow 4G + 4× CPU)

Perf = Performance score (0–100). FCP / SI / LCP in seconds, TBT in ms. INP is `None` in every lab run (Lighthouse does not interact with the page — INP is not measurable in the lab; see §5.7).

| Page | Run | Perf | FCP | SI | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|
| / | probe 1 (8123) | 86 | 1.89 | 2.38 | 1.89 | 464 | 0 |
| / | probe 2 (8123) | 97 | 1.58 | 3.98 | 1.58 | 12 | 0 |
| / | m1 (8123) | 93 | 2.59 | 2.59 | 2.59 | 106 | 0 |
| / | m2 (8124) | 97 | 1.45 | 3.90 | 1.45 | 130 | 0 |
| / | m3 (8124) | 96 | 1.53 | 3.89 | 1.53 | 156 | 0 |
| /how-it-works/ | m1 | 96 | 1.22 | 3.84 | 1.22 | 172 | 0 |
| /how-it-works/ | m2 | 95 | 1.23 | 3.77 | 1.23 | 204 | 0 |
| /how-it-works/ | m3 | 97 | 1.22 | 3.81 | 1.22 | 160 | 0 |
| /cost/ | m1 | 98 | 1.32 | 3.81 | 1.32 | 8 | 0 |
| /cost/ | m2 | 98 | 1.48 | 3.89 | 1.48 | 4 | 0 |
| /cost/ | m3 | 96 | 1.38 | 3.89 | 1.38 | 166 | 0 |
| **Mobile range** | | **86–98** | **1.22–2.59** | **2.38–3.98** | **1.22–2.59** | **0–464** | **0** |

Prior round (FINDINGS-fixround-php.md §7, same tool): home mobile Perf 78–90, SI 2.1–2.6 s; HIW mobile Perf 81, SI 2.4 s. Combined with this round, home mobile Perf has now spanned **78–98** with no site change between rounds — the variance is in the measurement environment, not the site.

### 2.2 Desktop (no throttling)

| Page | Perf | FCP | SI | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| / | 100 | 0.46 | 0.53 | 0.46 | 0 | 0 |
| /how-it-works/ | 100 | 0.29 | 0.40 | 0.29 | 0 | 0 |
| /cost/ | 100 | 0.38 | 0.40 | 0.38 | 0 | 0 |

Desktop is rock-stable at Perf 100 / SI ≤ 0.53 s — the same pages, the same bytes, unthrottled. The mobile variance appears only when the 4× CPU throttle is applied.

### 2.3 Observed vs simulated (the `metrics` audit — the key table)

Lighthouse mobile runs use **simulated** throttling: the page actually loads fast on localhost, then Lantern simulates slow 4G + 4× CPU. Both sets of numbers are in every report:

| Run | Observed FCP | Observed SI | Observed load | Simulated FCP | Simulated SI | Simulated TBT |
|---|---|---|---|---|---|---|
| home probe 1 | 0.99 | 1.01 | 0.35 | 1.89 | 2.38 | 464 |
| home probe 2 | 2.35 | 2.35 | 0.21 | 1.58 | 3.98 | 12 |
| home m1 | 0.94 | 0.95 | 0.23 | 2.59 | 2.59 | 106 |
| home m2 | 2.32 | 2.32 | 0.15 | 1.45 | 3.90 | 130 |
| home m3 | 2.29 | 2.29 | 0.22 | 1.53 | 3.89 | 156 |
| hiw m1–m3 | 2.26–2.33 | 2.26–2.34 | 0.17–0.20 | 1.22–1.23 | 3.77–3.84 | 160–204 |
| cost m1–m3 | 2.31–2.34 | 2.31–2.34 | 0.16–0.19 | 1.32–1.48 | 3.81–3.89 | 4–166 |
| desktop ×3 | 0.35–0.52 | 0.35–0.52 | 0.11–0.18 | 0.29–0.46 | 0.40–0.53 | 0 |

Read it as: **observed SI == observed FCP in 14/14 runs** (within 20 ms). The real browser paints once, complete, and nothing else ever changes the viewport. The `load` event fires at 0.15–0.35 s in every run — the network is done almost immediately; everything after that is main-thread CPU work before first paint.

## 3. Variance analysis — what moves, and why

### 3.1 Which metric moves the Perf score

Perf weights: LCP 25%, **TBT 30%**, CLS 25%, SI 10%, FCP 10%. The score variance is driven by:

- **TBT (0–464 ms) — the main score driver.** One long task (usually the initial parse + style + layout chunk) lands either side of the 50 ms long-task threshold depending on host CPU speed at that moment. TBT 464 ms cost probe 1 eleven points (86 vs 97); TBT ≤ 12 ms cost nothing. Cost m1 vs m3 is the cleanest pair: same page, TBT 8 ms → Perf 98, TBT 166 ms → Perf 96.
- **FCP/LCP (1.22–2.59 s).** FCP == LCP in every mobile run — the LCP element is the hero H1 text, painted at first paint. When the host is slow, first paint itself is late.
- **SI (2.38–3.98 s) barely moves the score** (10% weight) but is the most confusing number, so it gets its own section (§3.3).
- **CLS is 0 in all 14 runs.** It never moves. Nothing to fix there.

### 3.2 The cause: host CPU noise × 4× throttle (evidence)

The main-thread breakdown (simulated ms) for identical bytes:

| Run | style/layout | parseHTML | "other" | scriptEval | total task time (observed) |
|---|---|---|---|---|---|
| home probe 1 | 1,643 | 325 | 838 | 106 | 749 |
| home probe 2 | 1,109 | 53 | 371 | 51 | 411 |
| home m1 | 2,327 | 150 | 831 | 47 | 849 |
| home m2 | 1,164 | 67 | 279 | 41 | 397 |
| home m3 | 785 | 419 | 271 | 33 | 385 |
| hiw m1–m3 | 830–1,052 | 22–58 | 209–446 | 30–34 | 340–345 |
| cost m1–m3 | 767–1,000 | 27–41 | 215–427 | 26–35 | 279–340 |
| desktop ×3 | 134–215 | 11–60 | 67–113 | 7–13 | 271–328 |

- **parseHTML 22→419 ms (19×) for byte-identical HTML.** Parsing is deterministic work; a 19× spread can only be the CPU underneath. Same for style/layout 767→2,327 ms (3×) on a 698-element DOM with a 17.6 KB stylesheet.
- **Observed FCP 0.94→2.35 s (2.5×) while the load event is stable at 0.15–0.35 s.** The network finishes in ~0.2 s in every run; the 0.6 s (fast runs) to 2.1 s (slow runs) gap between `load` and first paint is pure main-thread starvation on this shared 1.5-vCPU VM, where other agents' work lands unpredictably. The two fast observed runs (probe 1, home m1: FCP ≈ 0.95 s) and the twelve slow ones (FCP ≈ 2.3 s) cluster into two regimes — the host was quieter for the first two, busier after ~11:11 PKT.
- **The 4× throttle is the amplifier.** Desktop (no throttle) is Perf 100 with total task time 271–328 ms — the same ~300 ms of real work. Under 4× throttle that same work becomes ~1.2 s of simulated pre-paint time, and any host slowdown is multiplied by four as well. That is why mobile Perf spans 12–20 points while desktop never moves.
- **No page-side suspect survives the evidence.** DOM is small (home ~698 elements, HIW ~430, cost ~603); CSS is 17.6 KB / 197 rules with no pathological selectors (one `:nth-child(even)` for table striping, a few box-shadows, two linear gradients — nothing that explains seconds of layout); JS is 661 B, deferred, scriptEval 26–106 ms; fonts are preloaded + `font-display: swap`; there are no images at all; the map iframes never even load in the lab (see §3.4).

Conclusion: **the variance is a property of the lab (shared, contended VM + simulated throttling), not of the site.** On a real mid-range phone the absolute numbers will differ, but the mechanism — first paint gated on ~300 ms (unthrottled) of parse + style + layout — is the same, and there is no heavy asset to remove.

### 3.3 The Speed Index two-regime puzzle — resolved

SI shows two clusters that look contradictory:

- **Regime A (probe 1, home m1): SI == FCP == LCP (2.38 / 2.59 s).** Everything paints at once, late.
- **Regime B (the other 9 mobile runs): FCP/LCP 1.22–1.58 s, but SI stuck at 3.77–3.98 s** — tight cluster, nearly identical across three different pages.

What it is: **the simulated SI tail is the webfont swap, as modelled by Lantern — not a real user-visible delay.** Evidence:

1. Observed SI == observed FCP in 14/14 runs. In the real load there is no late paint at all: the fonts (localhost, preloaded) are already there by first paint, so the page paints once, in its final fonts.
2. Under simulated slow 4G, Lantern models the two font files (67 KB at 1.6 Mbps + RTT) as arriving late. The final visual-progress step — the hero H1 in Archivo Black / body in Inter — is therefore timestamped at font-arrival time, ~3.8–3.9 s, in every Regime B run. The tight clustering (3.77–3.98 across different pages) is the signature of a fixed network-modelled event, not of page work.
3. In Regime A the host was slow, so Lantern modelled first paint itself late (2.4–2.6 s, after the fonts), and SI collapsed onto FCP. Same tail, different labelling: when FCP is modelled late, SI == FCP; when FCP is modelled early (fallback font), the font swap shows up as the SI tail.

So SI 3.8 s does **not** mean users stare at an incomplete page for 3.8 s. It means the simulated model paints the fallback font early and the webfont at ~3.8 s. A real user on slow 4G would see fallback text quickly, then the font swap — which is exactly what `font-display: swap` is designed to do, and CLS stays 0 because the swap is size-matched closely enough to not shift layout.

### 3.4 What is NOT the cause (checked, with numbers)

- **Render-blocking CSS:** one stylesheet, 17.6 KB, in `<head>` (correct — it must block to avoid FOUC). Lighthouse's only CSS opportunity is `unminified-css`, est. 5 KiB saving. Download is not the bottleneck; style recalculation is, and it is small in absolute terms.
- **JS:** `main.js` is 661 B, loaded with `defer`, scriptEval 26–106 ms, scriptParseCompile 3–10 ms. Zero impact.
- **Fonts:** 2 files, 67 KB total, both `<link rel="preload" as="font" crossorigin>` + `font-display: swap`. Correct setup. They are the SI-tail event in the simulation only (see §3.3).
- **Map iframes:** `loading="lazy"`, below the fold on every page (home has 2, HIW/cost/contact 1 each, 7 location pages 0). **Cost in the lab is exactly zero:** the network log in every run shows 6 requests total (HTML + CSS + 2 fonts + JS + favicon) — the Google Maps URLs are never even requested, because lazy below-fold iframes never load during a Lighthouse run. They cannot affect FCP, LCP, SI, TBT, or CLS. (Real scrolled users will load them; that is out of lab scope and the iframes are already lazy.)
- **Images:** zero `<img>` in `out/`. Nothing to optimise.
- **Server response:** simulated root-document time 0–10 ms. Not a factor.
- **Third parties:** none (no analytics, no ads, no external CSS/JS). `third-party-summary` is empty.

## 4. Asset inventory (home page; HIW/cost differ only in HTML size)

| Asset | Raw | gzip -9 (≈ Brotli live) | Role / notes |
|---|---|---|---|
| `index.html` | 60,425 B | 16,899 B (−72%) | 698 elements; 10.3 KB of it is JSON-LD (2 scripts) |
| `assets/css/styles.css` | 17,628 B | 4,890 B (−72%) | 408 lines, 197 rules, 1 render-blocking stylesheet |
| `assets/fonts/inter-var.woff2` | 48,256 B | 48,249 B (already compressed) | Variable font, preloaded, `swap` |
| `assets/fonts/archivoblack-400.woff2` | 18,604 B | 18,632 B (already compressed) | Display font (H1), preloaded, `swap` |
| `assets/js/main.js` | 661 B | 360 B (−46%) | `defer`; closes nav `<details>` on click/Escape only |
| `favicon.svg` | 311 B | 224 B (−28%) | |
| **Home total** | **147,020 B** | **~89 KB wire (≈ −40%)** | 6 requests |
| HIW total | 118,729 B | ~73 KB wire | HTML 32,134 B; 6 requests |
| Cost total | 133,686 B | ~82 KB wire | HTML 47,091 B; 6 requests |

Live (Cloudflare Brotli) will transfer roughly 40% less than the lab for HTML/CSS/JS; the fonts are already compressed and do not shrink. The lab's uncompressed transfer is a pessimistic ceiling — and even so, transfer is not the bottleneck (load event at 0.15–0.35 s).

**Critical path:** HTML (60 KB) → render-blocking CSS (17.6 KB) + 2 font preloads → parse + style + layout of the full DOM (~300 ms unthrottled main-thread work on this VM) → first paint (== LCP, hero H1). JS is deferred and off the path. Iframes are lazy and off the path. Nothing else is on the path.

## 5. Ranked fix list (expected impact per fix)

| # | Fix | Expected impact | Notes |
|---|---|---|---|
| 1 | **Measurement hygiene: report the median of 5 mobile runs, on a quiet machine, and stop chasing single-run Perf.** | Kills the phantom variance. Perf 78–98 becomes ~95–97 median. Zero user impact, but it is the only fix that addresses the actual variance. | The variance is host noise (§3.2). No code change can remove it. Also collect **field data (CrUX)** once the site has real traffic — that is the number that matters, and it is immune to lab host noise. |
| 2 | **Subset the Inter variable font to latin (+ latin-ext if needed).** | Simulated SI tail 3.8 s → ~2.5–3.0 s; real slow-4G font arrival ~0.35 s → ~0.15 s. Perf +0–2 points. Small real-user gain. | Inter variable is 48 KB for the full charset; the site is English-only. Keep Archivo Black as-is (18.6 KB, already small). Keep preload + `swap`. This is the only code change that touches the SI tail, because the tail *is* the font swap in the simulation. |
| 3 | **Minify `styles.css` (and HTML).** | CSS 17.6 → ~12.6 KB (Lighthouse: 5 KiB saving). Perf +0–1. Negligible real gain, but free and removes Lighthouse's only opportunity. | Do it in the export step, not by hand-editing the source CSS. |
| 4 | **Nothing else on the critical path.** | — | Do NOT inline critical CSS (17.6 KB is small; inlining would bloat every HTML file and lose the 1-year immutable cache on `/assets/*`); do NOT remove `content-visibility` (it is already helping — it is why below-fold blocks cost nothing at load); do NOT add preconnects for Google Maps (iframes are lazy/below-fold; a preconnect would spend DNS+TLS on every load for something most visitors never scroll to). |
| 5 | **INP: no action in the lab; watch field data.** | — | Lab INP is unmeasurable (no interaction). With 661 B deferred JS and no post-load long tasks, real INP risk is minimal. If CrUX later shows INP > 200 ms, revisit — the likely culprit would be the map iframe on scroll, and the fix then would be a click-to-load facade. |
| 6 | **(Not a fix) Do not "fix" CLS, TBT, or the iframes.** | — | CLS is 0 in 14/14 runs; TBT variance is host noise; iframes cost zero in the lab. Any change here would be churn, not improvement. |

Net: the site is already at the practical ceiling for this stack. The honest remaining work is (a) the font subset + CSS minify (small, real), and (b) measuring properly (median-of-5 + CrUX) instead of single-run Perf.

## 6. PageSpeed Insights — live check (retried, still blocked)

- **Tried once, 2026-11-19 ~11:17 PKT:** `GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://fort-myers-water-damage-php.pages.dev/&strategy=mobile&category=performance` (no API key, anonymous).
- **Result: HTTP 429, unchanged from this morning.** Body: `Quota exceeded for quota metric 'Queries' and limit 'Queries per day' of service 'pagespeedonline.googleapis.com' for consumer 'project_number:583797351490'` — `rateLimitExceeded` / `RESOURCE_EXHAUSTED`. The anonymous quota is a **shared pool** (project 583797351490 is Google's anonymous consumer, not ours), so it does not reset on our schedule and cannot be fixed from this VM.
- **Live Speed Index therefore remains unmeasured from this VM.** This is a measurement block, not a site problem: live HTML is byte-identical to local `out/` (verified in the fix round, md5 `8c2dce9d`), and live transfer is *better* than the lab (Brotli + HTTP/2 + edge cache, §4), so live is expected equal or better — but that is an expectation, not a measurement, and no number is faked here.
- **Ways to get a real live number:** (1) open PageSpeed Insights in a real browser and paste the pages.dev URL (uses the browser session's quota, not this VM's); (2) run Lighthouse in Chrome DevTools on a real machine against the live URL; (3) wait for CrUX field data once the site has traffic.

## 7. Reproducibility

- Reports: `/tmp/lh-fm/{test1,test2,home-m1,home-m2,home-m3,hiw-m1,hiw-m2,hiw-m3,cost-m1,cost-m2,cost-m3,home-d1,hiw-d1,cost-d1}.json` (ephemeral; `/tmp` may be wiped on VM replacement — the tables in §2 are the durable record).
- Runner scripts: `/tmp/lh-fm/run_lh.sh`, `/tmp/lh-fm/run_lh2.sh` (the second is the corrected one; the first had a broken line-continuation that silently dropped `--chrome-flags`, which is why its first batch failed with the root/`--no-sandbox` error — a lab-harness bug, not a site issue).
- Server: my own `python3 -m http.server 8124` (PID 18772) was stopped by PID after the audit; the pre-existing 8123 server had already died on its own mid-audit and was not touched.
- Prior numbers for comparison: `qa/FINDINGS-fixround-php.md` §7 and `qa/FINDINGS-34-pages-php.md` §5.
