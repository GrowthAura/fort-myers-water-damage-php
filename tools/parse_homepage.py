#!/usr/bin/env python3
"""Parse the user's pasted homepage into site/data/homepage.php.

The paste is the ceiling: this script converts it into structured blocks
(segments with link offsets) WITHOUT changing any word. It asserts:
  - every expected H2/H3 heading found, in order
  - table dimensions match the paste exactly
  - every (/slug/) token parsed into an anchor (logged for review)
  - word-diff 0 between the emitted blocks and the paste copy
Usage: python3 tools/parse_homepage.py
Writes: site/data/homepage.php
"""
import json
import re
import sys

PASTE = "/home/hatch/workspace/fort-myers-php/homepage-paste-2026-11-19.md"
OUT = "/home/hatch/workspace/fort-myers-php/site/data/homepage.php"

PHONE = "239-356-3708"

# Boundaries an anchor can start after (last occurrence wins, same line).
BOUNDARIES = ["• ", ": ", "See ", "see ", "· ", ", ", "Use the ", " and ",
              "More about who we are: ", ". ", "? ", "! ",
              "Learn ", "Read ", "before ", "also "]


def words(s):
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if w]


def parse_segments(text, where):
    """Split text on (/slug/) tokens into segments.

    Returns list of {'t': str} or {'t': str, 'href': str}.
    Anchor = text after the last boundary marker before the token.
    """
    segs = []
    pos = 0
    for m in re.finditer(r"\((/[a-z0-9\-/]*)\)", text):
        href = m.group(1)
        before = text[pos:m.start()]
        # anchor starts after the last boundary in `before`
        cut = 0
        for b in BOUNDARIES:
            i = before.rfind(b)
            if i >= 0:
                cut = max(cut, i + len(b))
        anchor = before[cut:].rstrip()
        pre = before[:cut]
        if pre:
            segs.append({"t": pre})
        if not anchor or len(words(anchor)) > 12:
            raise SystemExit(f"BAD ANCHOR {where}: {anchor!r} before {href}")
        segs.append({"t": anchor, "href": href})
        print(f"  link {where}: {anchor!r} -> {href}")
        pos = m.end()
    if text[pos:]:
        segs.append({"t": text[pos:]})
    return segs


def seg_text(segs):
    return "".join(s["t"] for s in segs)


def php_str(s):
    # PHP single-quoted string: only \\ and \' are escapes; UTF-8 passes through.
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def php_val(v, ind=0):
    pad = "    " * ind
    pad2 = "    " * (ind + 1)
    if isinstance(v, dict):
        if not v:
            return "[]"
        items = []
        for k, val in v.items():
            items.append(f"{pad2}{php_str(str(k))} => {php_val(val, ind + 1)}")
        return "[\n" + ",\n".join(items) + f"\n{pad}]"
    if isinstance(v, list):
        if not v:
            return "[]"
        items = [f"{pad2}{php_val(x, ind + 1)}" for x in v]
        return "[\n" + ",\n".join(items) + f"\n{pad}]"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    return php_str(str(v))


def main():
    raw = open(PASTE).read()
    assert raw.count("—") + raw.count("–") == 0, "dashes present in paste"
    seo_part, copy = raw.split("FINAL: Homepage page copy", 1)
    copy = copy.strip()
    lines = copy.split("\n")
    # drop empty lines
    lines = [l for l in lines if l.strip() != ""]
    n = len(lines)
    print(f"copy lines: {n}, copy words: {len(words(copy))}")

    # ---- SEO fields -------------------------------------------------------
    def field(name):
        m = re.search(re.escape(name) + r"\n([^\n]+)", seo_part)
        assert m, f"SEO field missing: {name}"
        return m.group(1).strip()

    title = field("Meta title (60 chars)")
    meta = field("Meta description (150 chars)")
    h1 = field("H1")
    m = re.search(r"Schema \(JSON-LD\)\n(\{.*?\n\})", seo_part, re.S)
    assert m, "schema JSON missing"
    schema = json.loads(m.group(1))
    assert schema["@type"] == "HomeAndConstructionBusiness"
    assert schema["name"] == "Fort Myers Water Damage Restoration Pros"
    print(f"title ({len(title)}ch): {title}")
    print(f"meta ({len(meta)}ch): {meta}")
    print(f"H1: {h1}")

    blocks = []
    i = 0  # line cursor

    def expect(idx, text):
        assert lines[idx] == text, f"line {idx}: expected {text!r}, got {lines[idx]!r}"

    def take_para(idx):
        return parse_segments(lines[idx], f"para L{idx}"), idx + 1

    def take_bullets(idx, count, where):
        out = []
        for _ in range(count):
            assert lines[idx].startswith("• "), f"line {idx} not a bullet: {lines[idx][:60]!r}"
            out.append(parse_segments(lines[idx][2:], f"{where} L{idx}"))
            idx += 1
        return out, idx

    def take_steps_numbered(idx, count, where):
        # "1.  Stop the source. Knock ..." — number + full text on one line
        out = []
        for k in range(count):
            m = re.match(rf"{k + 1}\.\s+(.*)", lines[idx])
            assert m, f"line {idx} not step {k + 1}: {lines[idx][:60]!r}"
            out.append(parse_segments(m.group(1), f"{where} L{idx}"))
            idx += 1
        return out, idx

    def take_table(idx, cols, rows, where):
        head = []
        for _ in range(cols):
            head.append(parse_segments(lines[idx], f"{where} head L{idx}"))
            idx += 1
        body = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(parse_segments(lines[idx], f"{where} cell L{idx}"))
                idx += 1
            body.append(row)
        return {"type": "table", "head": head, "rows": body}, idx

    # ---- Hero -------------------------------------------------------------
    expect(0, h1)
    i = 1
    intro, i = take_para(i)
    assert lines[i] == f"Call {PHONE} · Describe your water problem", f"CTA line: {lines[i]!r}"
    i += 1
    areas_line, i = take_para(i)
    blocks.append({"type": "hero", "h1": h1, "intro": intro, "areas": areas_line})

    # ---- Details ----------------------------------------------------------
    expect(i, "Fort Myers water damage help")
    i += 1
    expect(i, "Details")
    i += 1
    detail_rows = []
    for _ in range(6):
        label = lines[i]
        i += 1
        value, i = take_para(i)
        detail_rows.append({"label": label, "value": value})
    blocks.append({"type": "details", "heading": "Fort Myers water damage help",
                   "sub": "Details", "rows": detail_rows})

    # ---- H2 sections in order --------------------------------------------
    def h2(idx, text):
        expect(idx, text)
        return idx + 1

    # 24/7 Water Damage Help
    i = h2(i, "24/7 Water Damage Help for Fort Myers Homes and Businesses")
    p, i = take_para(i)
    blocks.append({"type": "h2", "text": "24/7 Water Damage Help for Fort Myers Homes and Businesses"})
    blocks.append({"type": "p", "segs": p})

    # What we help with
    expect(i, "What we help with")
    i += 1
    bullets, i = take_bullets(i, 6, "help-with")
    blocks.append({"type": "h3", "text": "What we help with"})
    blocks.append({"type": "ul", "items": bullets})

    # How we work with you
    expect(i, "How we work with you")
    i += 1
    bullets, i = take_bullets(i, 3, "how-we-work")
    blocks.append({"type": "h3", "text": "How we work with you"})
    blocks.append({"type": "ul", "items": bullets})

    # What Happens When You Call
    i = h2(i, "What Happens When You Call 239-356-3708 in Fort Myers")
    blocks.append({"type": "h2", "text": "What Happens When You Call 239-356-3708 in Fort Myers"})
    for _ in range(2):
        p, i = take_para(i)
        blocks.append({"type": "p", "segs": p})
    p, i = take_para(i)  # More about who we are line
    blocks.append({"type": "p", "segs": p})

    # Water in Your Home Right Now? Do This First
    i = h2(i, "Water in Your Fort Myers Home Right Now? Do This First")
    blocks.append({"type": "h2", "text": "Water in Your Fort Myers Home Right Now? Do This First"})
    bullets, i = take_bullets(i, 6, "do-first")
    blocks.append({"type": "ul", "items": bullets})
    expect(i, "What not to do")
    i += 1
    bullets, i = take_bullets(i, 5, "not-to-do")
    blocks.append({"type": "h3", "text": "What not to do"})
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)  # Need every step? ... checklist
    blocks.append({"type": "p", "segs": p})

    # What Kind of Water Damage
    i = h2(i, "What Kind of Water Damage Is in Your Fort Myers Home?")
    blocks.append({"type": "h2", "text": "What Kind of Water Damage Is in Your Fort Myers Home?"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    kinds = []
    for _ in range(13):
        ktitle = lines[i]
        i += 1
        # body is ONE paragraph whose last sentence is "See X (/slug/)."
        body, i = take_para(i)
        kinds.append({"title": ktitle, "body": body})
    blocks.append({"type": "kinds", "items": kinds})

    # Signs of Hidden Water Damage
    i = h2(i, "Signs of Hidden Water Damage in Fort Myers Slab Homes")
    blocks.append({"type": "h2", "text": "Signs of Hidden Water Damage in Fort Myers Slab Homes"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 8, "hidden-signs")
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # How Fort Myers Homes Are Built
    i = h2(i, "How Fort Myers Homes Are Built, and Why It Changes the Drying")
    blocks.append({"type": "h2", "text": "How Fort Myers Homes Are Built, and Why It Changes the Drying"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    tbl, i = take_table(i, 3, 5, "built-table")
    blocks.append(tbl)
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # How Water Damage Restoration Works, Step by Step
    i = h2(i, "How Water Damage Restoration Works in Fort Myers, Step by Step")
    blocks.append({"type": "h2", "text": "How Water Damage Restoration Works in Fort Myers, Step by Step"})
    steps = []
    for k in range(5):
        m = re.match(rf"{k + 1}\.\s+(.*)", lines[i])
        assert m, f"line {i} not step {k + 1}: {lines[i][:60]!r}"
        stitle = m.group(1)
        i += 1
        body, i = take_para(i)
        steps.append({"title": stitle, "body": body})
    blocks.append({"type": "steps", "items": steps})
    p, i = take_para(i)  # Most clean-water jobs...
    blocks.append({"type": "p", "segs": p})
    assert lines[i] == f"Call {PHONE}", f"CTA line: {lines[i]!r}"
    blocks.append({"type": "cta-line", "text": f"Call {PHONE}"})
    i += 1

    # What Fort Myers Homes Can Dry in Place
    i = h2(i, "What Fort Myers Homes Can Dry in Place and What Has to Go")
    blocks.append({"type": "h2", "text": "What Fort Myers Homes Can Dry in Place and What Has to Go"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    tbl, i = take_table(i, 3, 9, "dry-table")
    blocks.append(tbl)
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # Clean Water, Gray Water or Sewage
    i = h2(i, "Clean Water, Gray Water or Sewage in Your Fort Myers Home?")
    blocks.append({"type": "h2", "text": "Clean Water, Gray Water or Sewage in Your Fort Myers Home?"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    tbl, i = take_table(i, 4, 3, "category-table")
    blocks.append(tbl)
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # Sewer Backup
    i = h2(i, "Sewer Backup in Fort Myers: Your Line or the Utility's?")
    blocks.append({"type": "h2", "text": "Sewer Backup in Fort Myers: Your Line or the Utility's?"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 5, "sewer-backup")
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # Why Water Damage Spreads Faster
    i = h2(i, "Why Water Damage Spreads Faster in Fort Myers and Lee County")
    blocks.append({"type": "h2", "text": "Why Water Damage Spreads Faster in Fort Myers and Lee County"})
    bullets, i = take_bullets(i, 4, "spreads-faster")
    blocks.append({"type": "ul", "items": bullets})

    # Water Damage Through the Year
    i = h2(i, "Water Damage Through the Year in Fort Myers")
    blocks.append({"type": "h2", "text": "Water Damage Through the Year in Fort Myers"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    tbl, i = take_table(i, 3, 3, "year-table")
    blocks.append(tbl)

    # 50% Rule
    i = h2(i, "Rebuilding in a Fort Myers Flood Zone: The 50% Rule")
    blocks.append({"type": "h2", "text": "Rebuilding in a Fort Myers Flood Zone: The 50% Rule"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 6, "fifty-percent")
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    p, i = take_para(i)  # FEMA Flood Map Service Center (msc.fema.gov)
    blocks.append({"type": "p", "segs": p})

    # Do You Need a Restoration Company
    i = h2(i, "Do You Need a Restoration Company in Fort Myers, or Can You Handle It Yourself?")
    blocks.append({"type": "h2", "text": "Do You Need a Restoration Company in Fort Myers, or Can You Handle It Yourself?"})
    p, i = take_para(i)  # intro para — ends with "You can usually handle it yourself if:" (same line)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 3, "diy-ok")
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)  # It is time to call for help if:
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 6, "call-for-help")
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # Condo Water Damage
    i = h2(i, "Condo Water Damage in Fort Myers: Who Handles What")
    blocks.append({"type": "h2", "text": "Condo Water Damage in Fort Myers: Who Handles What"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    steps, i = take_steps_numbered(i, 5, "condo-steps")
    blocks.append({"type": "steps-numbered", "items": steps})
    p, i = take_para(i)  # See condo water damage ... full walkthrough.
    blocks.append({"type": "p", "segs": p})

    # Businesses and Vacation Rentals
    i = h2(i, "Water Damage in Fort Myers Businesses and Vacation Rentals")
    blocks.append({"type": "h2", "text": "Water Damage in Fort Myers Businesses and Vacation Rentals"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 3, "business")
    blocks.append({"type": "ul", "items": bullets})

    # Insurance
    i = h2(i, "Water Damage and Insurance in Fort Myers: What Florida Homeowners Should Know")
    blocks.append({"type": "h2", "text": "Water Damage and Insurance in Fort Myers: What Florida Homeowners Should Know"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 8, "insurance")
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)  # More detail: how insurance handles...
    blocks.append({"type": "p", "segs": p})

    # Questions to Ask
    i = h2(i, "Questions to Ask a Fort Myers Water Damage Company Before Work Starts")
    blocks.append({"type": "h2", "text": "Questions to Ask a Fort Myers Water Damage Company Before Work Starts"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 6, "questions-to-ask")
    blocks.append({"type": "ul", "items": bullets})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # How to Prevent the Next Leak
    i = h2(i, "How to Prevent the Next Leak in Your Fort Myers Home")
    blocks.append({"type": "h2", "text": "How to Prevent the Next Leak in Your Fort Myers Home"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    bullets, i = take_bullets(i, 6, "prevent")
    blocks.append({"type": "ul", "items": bullets})

    # ZIP Codes
    i = h2(i, "Which Fort Myers ZIP Codes Do You Cover?")
    blocks.append({"type": "h2", "text": "Which Fort Myers ZIP Codes Do You Cover?"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    tbl, i = take_table(i, 2, 11, "zip-table")
    blocks.append(tbl)
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})

    # Water Damage Help Across Lee County
    i = h2(i, "Water Damage Help Across Lee County")
    blocks.append({"type": "h2", "text": "Water Damage Help Across Lee County"})
    for _ in range(6):
        p, i = take_para(i)
        blocks.append({"type": "p", "segs": p})
    p, i = take_para(i)  # See every city and ZIP code... (/areas/)
    blocks.append({"type": "p", "segs": p})
    assert lines[i] == "Map: Fort Myers and the Lee County service area", f"map line: {lines[i]!r}"
    blocks.append({"type": "map", "caption": lines[i]})
    i += 1

    # FAQ — dynamic count: questions run until the final-CTA H2.
    i = h2(i, "Questions Fort Myers Homeowners Ask")
    blocks.append({"type": "h2", "text": "Questions Fort Myers Homeowners Ask"})
    faqs = []
    while lines[i] != "Water Damage in Your Fort Myers Home Right Now?":
        q = lines[i]
        i += 1
        a, i = take_para(i)
        faqs.append({"q": q, "a": a})
    print(f"FAQ pairs: {len(faqs)}")
    blocks.append({"type": "faq", "items": faqs})

    # Final CTA
    i = h2(i, "Water Damage in Your Fort Myers Home Right Now?")
    blocks.append({"type": "h2", "text": "Water Damage in Your Fort Myers Home Right Now?"})
    p, i = take_para(i)
    blocks.append({"type": "p", "segs": p})
    assert lines[i] == f"Call {PHONE}, answered 24/7", f"final CTA: {lines[i]!r}"
    blocks.append({"type": "cta-line", "text": f"Call {PHONE}, answered 24/7"})
    i += 1

    assert i == n, f"consumed {i} of {n} lines; next: {lines[i] if i < n else 'EOF'!r}"

    # ---- word-diff --------------------------------------------------------
    def block_words(b):
        out = []
        if b["type"] == "hero":
            out += words(b["h1"]) + words(seg_text(b["intro"])) + words(f"Call {PHONE} · Describe your water problem") + words(seg_text(b["areas"]))
        elif b["type"] == "details":
            out += words(b["heading"]) + words(b["sub"])
            for r in b["rows"]:
                out += words(r["label"]) + words(seg_text(r["value"]))
        elif b["type"] in ("h2", "h3"):
            out += words(b["text"])
        elif b["type"] == "p":
            out += words(seg_text(b["segs"]))
        elif b["type"] == "ul":
            for it in b["items"]:
                out += words(seg_text(it))
        elif b["type"] == "kinds":
            for k in b["items"]:
                out += words(k["title"]) + words(seg_text(k["body"]))
        elif b["type"] == "table":
            for c in b["head"]:
                out += words(seg_text(c))
            for row in b["rows"]:
                for c in row:
                    out += words(seg_text(c))
        elif b["type"] == "steps":
            for k, s in enumerate(b["items"]):
                # the step number digit is part of the copy text ("1. You call...")
                out += [str(k + 1)] + words(s["title"]) + words(seg_text(s["body"]))
        elif b["type"] == "steps-numbered":
            for k, s in enumerate(b["items"]):
                out += [str(k + 1)] + words(seg_text(s))
        elif b["type"] == "cta-line":
            out += words(b["text"])
        elif b["type"] == "map":
            out += words(b["caption"])
        elif b["type"] == "faq":
            for f in b["items"]:
                out += words(f["q"]) + words(seg_text(f["a"]))
        else:
            raise SystemExit(f"unknown block type {b['type']}")
        return out

    got = []
    for b in blocks:
        got += block_words(b)
    # The (/slug/) tokens are link annotations, not visible copy: strip them
    # from the copy before comparing (their words live in hrefs, not text).
    visible_copy = re.sub(r"\((/[a-z0-9\-/]*)\)", "", copy)
    want = words(visible_copy)
    print(f"copy words (visible, tokens stripped): {len(want)}")
    print(f"blocks words: {len(got)}")
    if got != want:
        for k, (a, b) in enumerate(zip(got, want)):
            if a != b:
                print(f"FIRST DIFF at word {k}: got {a!r} want {b!r}")
                print("got context:", got[max(0, k - 8):k + 8])
                print("want context:", want[max(0, k - 8):k + 8])
                break
        print(f"lengths got={len(got)} want={len(want)}")
        raise SystemExit("WORD-DIFF FAILED")
    print("WORD-DIFF 0 ✓")

    # ---- emit PHP ---------------------------------------------------------
    data = {
        "seo": {"title": title, "meta": meta, "h1": h1, "schema": schema},
        "blocks": blocks,
    }
    import os
    os.makedirs("/home/hatch/workspace/fort-myers-php/site/data", exist_ok=True)
    php = "<?php\n// Homepage content — parsed verbatim from homepage-paste-2026-11-19.md\n"
    php += "// by tools/parse_homepage.py. Do NOT hand-edit: re-run the parser.\n"
    php += "// Segments: ['t' => text] or ['t' => anchor text, 'href' => '/slug/'].\n"
    php += "return " + php_val(data) + ";\n"
    open(OUT, "w").write(php)
    print(f"wrote {OUT} ({len(php)} bytes)")


if __name__ == "__main__":
    main()
