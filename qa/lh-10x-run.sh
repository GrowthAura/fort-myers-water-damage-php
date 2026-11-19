#!/bin/bash
# Fort Myers 10X fix round — Lighthouse runs against local out/ on :8135.
# Method per qa/AUDIT-10x-speed.md: Playwright bundled Chromium via
# CHROME_PATH, --no-sandbox --disable-dev-shm-usage --disable-gpu
# --headless=new (Lighthouse 13 ignores --chrome-path; needs the env var).
# Usage: qa/lh-10x-run.sh <name> <url-path> [mobile|desktop]
set -e
NAME="$1"; PATH_="$2"; MODE="${3:-mobile}"
CHROME="$HOME/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"
OUTDIR="/home/hatch/workspace/fort-myers-php/qa/screenshots/10x-fix/lighthouse"
mkdir -p "$OUTDIR"
export CHROME_PATH="$CHROME"
FLAGS="--no-sandbox --disable-dev-shm-usage --disable-gpu --headless=new"
if [ "$MODE" = "desktop" ]; then
  npx --no-install lighthouse "http://127.0.0.1:8135${PATH_}" \
    --preset=desktop --chrome-flags="$FLAGS" \
    --only-categories=performance --output=json --quiet \
    --output-path="$OUTDIR/${NAME}.json"
else
  npx --no-install lighthouse "http://127.0.0.1:8135${PATH_}" \
    --chrome-flags="$FLAGS" \
    --only-categories=performance --output=json --quiet \
    --output-path="$OUTDIR/${NAME}.json"
fi
python3 -c "
import json
r = json.load(open('$OUTDIR/${NAME}.json'))
a = r['audits']
print('$NAME', 'Perf', round(r['categories']['performance']['score']*100),
      'FCP', a['first-contentful-paint']['displayValue'],
      'SI', a['speed-index']['displayValue'],
      'LCP', a['largest-contentful-paint']['displayValue'],
      'TBT', a['total-blocking-time']['displayValue'],
      'CLS', a['cumulative-layout-shift']['displayValue'])
"
