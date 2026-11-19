#!/usr/bin/env python3
"""Own fresh reuse corpus for kinds cards (coordinator's qa/reuse-corpus/
was still empty at build time). Scope: images actually shipped on sites
(site asset dirs + export/out/gh-pages image dirs). Excludes screenshots,
qa working dirs, node_modules, and this task's own raw/final kinds images.
Writes md5-list.txt + ahash.json (16x16 aHash) to qa/reuse-corpus-kinds/."""
import hashlib, json, os, subprocess
from PIL import Image

ROOT = "/home/hatch/workspace"
OUTDIR = "/home/hatch/workspace/fort-myers-php/qa/reuse-corpus-kinds"
os.makedirs(OUTDIR, exist_ok=True)

EXCLUDE_SUBSTR = ["screenshots", "/qa/", "node_modules", "kinds-raw",
                  "fort-myers-php/site/assets/img/kinds-",
                  "fort-myers-php/out", "goals/", "onboarding_tour"]
INCLUDE_SUBSTR = ["/site/assets/img/", "/out/assets/img/", "/out/images/",
                  "/images/", "gh-pages", "/export", "/dist/", "/build/"]
EXTS = (".jpg", ".jpeg", ".png", ".webp")

def ahash16(path):
    try:
        im = Image.open(path).convert("L").resize((16, 16), Image.LANCZOS)
        px = list(im.getdata())
        avg = sum(px) / len(px)
        bits = 0
        for i, p in enumerate(px):
            if p > avg:
                bits |= 1 << (255 - i)
        return format(bits, "064x")
    except Exception:
        return None

def hamming(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")

cands = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    if any(e in dirpath for e in EXCLUDE_SUBSTR):
        dirnames[:] = []
        continue
    # prune heavy non-image trees fast
    dirnames[:] = [d for d in dirnames if d not in
                   ("node_modules", ".git", "screenshots", "qa")]
    if not any(s in dirpath for s in INCLUDE_SUBSTR):
        continue
    for fn in filenames:
        if fn.lower().endswith(EXTS):
            cands.append(os.path.join(dirpath, fn))

print("candidates:", len(cands))
md5_lines, ahashes = [], {}
for p in cands:
    try:
        h = hashlib.md5()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        md5_lines.append(f"{h.hexdigest()}  {p}")
        a = ahash16(p)
        if a:
            ahashes[p] = a
    except Exception as e:
        print("skip", p, e)

with open(os.path.join(OUTDIR, "md5-list.txt"), "w") as f:
    f.write("\n".join(sorted(md5_lines)) + "\n")
with open(os.path.join(OUTDIR, "ahash.json"), "w") as f:
    json.dump(ahashes, f, indent=1)
print("md5 entries:", len(md5_lines), "| ahash entries:", len(ahashes))
print("DONE")
