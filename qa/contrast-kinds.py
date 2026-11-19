#!/usr/bin/env python3
"""Contrast math for kinds cards.
Overlay (proposed): linear-gradient(180deg,
  rgba(7,38,47,0.86) 0%, rgba(7,38,47,0.78) 55%, rgba(7,38,47,0.74) 100%)
Text: h3 #ffffff, p #f4f8f8, link #ffd9a8.
Method: WCAG 2.x relative luminance + ratio (L1+0.05)/(L2+0.05).
Per card: brightest pixel of the final 760x864 master (measured) blended
under the overlay at the weakest alpha (0.74, bottom of card) = worst case
for body text/links; and under 0.86 (top, h3 zone). Also the absolute
worst case: overlay over a pure-white (255,255,255) image pixel.
"""
import glob, os
from PIL import Image

OVERLAY = (7, 38, 47)
A_TOP, A_MID, A_BOT = 0.86, 0.78, 0.74
TEXTS = {"h3 #ffffff": (255, 255, 255),
         "p #f4f8f8": (244, 248, 248),
         "link #ffd9a8": (255, 217, 168)}

def lum(rgb):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(fg, bg):
    l1, l2 = lum(fg), lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)

def blend(over, alpha, under):
    return tuple(round(over[i] * alpha + under[i] * (1 - alpha), 1) for i in range(3))

print("== ABSOLUTE WORST CASE: overlay over pure-white image pixel ==")
for name, fg in TEXTS.items():
    for aname, a in (("top a=0.86", A_TOP), ("mid a=0.78", A_MID), ("bot a=0.74", A_BOT)):
        bg = blend(OVERLAY, a, (255, 255, 255))
        print(f"  {name:16s} {aname}: eff bg rgb{bg} ratio {ratio(fg, bg):.2f}:1")

print()
print("== PER-CARD MEASURED: brightest pixel of final master ==")
for f in sorted(glob.glob("/home/hatch/workspace/fort-myers-php/site/assets/img/kinds-*.jpg")):
    im = Image.open(f).convert("RGB")
    small = im.resize((76, 86))
    px = list(small.getdata())
    brightest = max(px, key=lambda p: lum(p))
    out = [os.path.basename(f)]
    for aname, a in (("top", A_TOP), ("bot", A_BOT)):
        bg = blend(OVERLAY, a, brightest)
        rs = {n: ratio(fg, bg) for n, fg in TEXTS.items()}
        out.append(f"{aname} bg{bg} h3 {rs['h3 #ffffff']:.2f} p {rs['p #f4f8f8']:.2f} link {rs['link #ffd9a8']:.2f}")
    print(f"  brightest pixel {brightest} | " + " | ".join(out))
print("DONE")
