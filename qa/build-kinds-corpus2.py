#!/usr/bin/env python3
"""Fast reuse corpus via find (C-speed walk). Same scope/rules as v1."""
import hashlib, json, os, subprocess
OUTDIR = "/home/hatch/workspace/fort-myers-php/qa/reuse-corpus-kinds"
os.makedirs(OUTDIR, exist_ok=True)
FIND = ["find", "/home/hatch/workspace", "-type", "f", "(",
        "-iname", "*.jpg", "-o", "-iname", "*.jpeg", "-o",
        "-iname", "*.png", "-o", "-iname", "*.webp", ")",
        "(", "-path", "*/site/assets/img/*",
        "-o", "-path", "*/out/assets/img/*",
        "-o", "-path", "*/out/images/*",
        "-o", "-path", "*gh-pages*/images/*",
        "-o", "-path", "*/export*/images/*",
        "-o", "-path", "*/dist*/images/*",
        "-o", "-path", "*/aquarestore/images/*", ")",
        "-not", "-path", "*screenshots*",
        "-not", "-path", "*/qa/*",
        "-not", "-path", "*kinds-raw*",
        "-not", "-path", "*fort-myers-php/site/assets/img/kinds-*",
        "-not", "-path", "*fort-myers-php/out*"]
r = subprocess.run(FIND, capture_output=True, text=True, check=True)
cands = sorted(p for p in r.stdout.splitlines() if p.strip())
print("candidates:", len(cands))
from PIL import Image
def ahash16(path):
    try:
        im = Image.open(path).convert("L").resize((16, 16), Image.LANCZOS)
        px = list(im.getdata()); avg = sum(px)/len(px); bits = 0
        for i, p in enumerate(px):
            if p > avg: bits |= 1 << (255-i)
        return format(bits, "064x")
    except Exception:
        return None
md5_lines, ahashes = [], {}
for p in cands:
    try:
        h = hashlib.md5()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        md5_lines.append(f"{h.hexdigest()}  {p}")
        a = ahash16(p)
        if a: ahashes[p] = a
    except Exception as e:
        print("skip", p, e)
open(os.path.join(OUTDIR, "md5-list.txt"), "w").write("\n".join(sorted(md5_lines)) + "\n")
json.dump(ahashes, open(os.path.join(OUTDIR, "ahash.json"), "w"), indent=1)
print("md5 entries:", len(md5_lines), "| ahash entries:", len(ahashes))
print("DONE")
