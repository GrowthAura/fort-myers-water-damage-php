#!/usr/bin/env python3
"""Task 5 kinds cards: crop raw generations to 760x864 masters (q80), then
strip EXIF and write GPS-only via exiftool. Crop offsets chosen per image
after full-size visual review (0.0 = top of frame, 1.0 = bottom)."""
import os, subprocess
from PIL import Image

RAW = "/home/hatch/workspace/fort-myers-php/qa/kinds-raw"
OUT = "/home/hatch/workspace/fort-myers-php/site/assets/img"
os.makedirs(OUT, exist_ok=True)

# (raw stem fragment, final filename, crop_y offset)
JOBS = [
    ("kinds-ac-leak-raw",            "kinds-ac-leak.jpg",            0.45),
    ("kinds-ceiling-leak-raw",       "kinds-ceiling-leak.jpg",       0.05),
    ("kinds-condo-leak-raw",         "kinds-condo-leak.jpg",         0.20),
    ("kinds-sewage-backup-raw",      "kinds-sewage-backup.jpg",      0.45),
    ("kinds-cast-iron-pipe-raw",     "kinds-cast-iron-pipe.jpg",     0.55),
    ("kinds-burst-pipe-raw",         "kinds-burst-pipe.jpg",         0.40),
    ("kinds-water-heater-leak-raw",  "kinds-water-heater-leak.jpg",  0.45),
    ("kinds-appliance-leak-raw",     "kinds-appliance-leak.jpg",     0.45),
    ("kinds-slab-leak-raw",          "kinds-slab-leak.jpg",          0.40),
    ("kinds-vacant-home-raw",        "kinds-vacant-home.jpg",        0.30),
    ("kinds-mobile-home-raw",        "kinds-mobile-home.jpg",        0.50),
    ("kinds-flood-storm-raw",        "kinds-flood-storm.jpg",        0.45),
    ("kinds-floors-cabinets-raw",    "kinds-floors-cabinets.jpg",    0.55),
]

TARGET_W, TARGET_H = 760, 864
RATIO = TARGET_W / TARGET_H  # 0.87963

def find_raw(fragment):
    for f in os.listdir(RAW):
        if fragment in f and f.endswith(".jpg"):
            return os.path.join(RAW, f)
    raise FileNotFoundError(fragment)

for frag, final, off in JOBS:
    src = find_raw(frag)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    crop_h = int(w / RATIO)
    excess = h - crop_h
    top = int(excess * off)
    im2 = im.crop((0, top, w, top + crop_h)).resize((TARGET_W, TARGET_H), Image.LANCZOS)
    dst = os.path.join(OUT, final)
    im2.save(dst, "JPEG", quality=80, optimize=True)
    print(f"{final}: raw {w}x{h} crop y={top}..{top+crop_h} -> {TARGET_W}x{TARGET_H} "
          f"{os.path.getsize(dst)//1024} KB")

# Strip ALL metadata, then write GPS only (Fort Myers 26.6406,-81.8723)
for _, final, _ in JOBS:
    dst = os.path.join(OUT, final)
    subprocess.run(["exiftool", "-all=", "-overwrite_original", dst],
                   check=True, capture_output=True)
    subprocess.run(["exiftool", "-overwrite_original",
                    "-GPSLatitude=26.6406", "-GPSLatitudeRef=North",
                    "-GPSLongitude=-81.8723", "-GPSLongitudeRef=West",
                    "-GPSAltitude=3", "-GPSAltitudeRef=0", dst],
                   check=True, capture_output=True)
    print("geotagged", final)

print("DONE")
