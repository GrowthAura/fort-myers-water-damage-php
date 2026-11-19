#!/usr/bin/env python3
"""Parse the 10 inner-page pastes into site/data/<slug>.php.

Generic walker + per-page SPEC (H2 list, tables, details, FAQ/Related).
The paste is the ceiling: converts to structured blocks WITHOUT changing
any word. Asserts:
  - SEO fields byte-match the spec (title, meta, H1, schema @type + url)
  - every expected H2 found, in order
  - table dimensions match the paste exactly
  - every (/slug/) token parsed into an anchor (logged); href must be one
    of the planned 33 routes + /about/
  - word-diff 0 between the emitted blocks and the paste copy
Usage: python3 tools/parse_page.py [slug ...]   (default: all 10)
Writes: site/data/<slug>.php
"""
import json
import os
import re
import sys

BASE = "/home/hatch/workspace/fort-myers-php"
PAGES_DIR = os.path.join(BASE, "pages")
OUT_DIR = os.path.join(BASE, "site", "data")
PHONE = "239-356-3708"
CTA = f"Call {PHONE}, answered 24/7"

BOUNDARIES = ["• ", ": ", "See ", "see ", "· ", ", ", "Use the ", " and ",
              "More about who we are: ", ". ", "? ", "! ",
              "Learn ", "Read ", "before ", "also "]

PLANNED = ["/", "/water-removal/", "/drying/", "/sewage-cleanup/", "/ac-leak/",
           "/ceiling-leak/", "/condo-leak/", "/cast-iron-pipe/", "/vacant-home/",
           "/first-hour-checklist/", "/cost/", "/insurance/", "/burst-pipe/",
           "/mobile-home/", "/slab-leak/", "/flood-cleanup/", "/cape-coral/",
           "/lehigh-acres/", "/areas/", "/water-heater-leak/", "/appliance-leak/",
           "/floors/", "/cabinets/", "/commercial/", "/north-fort-myers/",
           "/fort-myers-beach/", "/estero/", "/bonita-springs/", "/how-it-works/",
           "/contact/", "/privacy-policy/", "/terms/", "/disclaimer/", "/about/"]

BUILT = ["/", "/water-removal/", "/drying/", "/sewage-cleanup/", "/ac-leak/",
         "/ceiling-leak/", "/condo-leak/", "/cast-iron-pipe/", "/vacant-home/",
         "/first-hour-checklist/", "/cost/", "/insurance/", "/burst-pipe/",
         "/mobile-home/", "/slab-leak/", "/flood-cleanup/", "/cape-coral/",
         "/lehigh-acres/", "/areas/", "/water-heater-leak/", "/appliance-leak/",
         "/floors/", "/cabinets/", "/commercial/", "/north-fort-myers/",
         "/fort-myers-beach/", "/estero/", "/bonita-springs/", "/how-it-works/",
         "/contact/", "/privacy-policy/", "/terms/", "/disclaimer/", "/about/"]


def words(s):
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if w]


def seg_text(segs):
    return "".join(s["t"] for s in segs)


def php_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def php_val(v, ind=0):
    pad = "    " * ind
    pad2 = "    " * (ind + 1)
    if v is None:
        return "null"
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


class Parser:
    def __init__(self, spec):
        self.spec = spec
        self.slug = spec["slug"]
        raw = open(os.path.join(PAGES_DIR, spec["paste"])).read()
        assert raw.count("—") + raw.count("–") == 0, "dashes present in paste"
        parts = re.split(r"FINAL: [^\n]* page copy\n", raw, maxsplit=1)
        assert len(parts) == 2, "copy marker not found"
        self.seo_part, self.copy = parts[0], parts[1].strip()
        # Keep blank lines: a blank line can be an empty table header cell
        # (sewage "Sewer or Septic?" table). The walker skips blanks between
        # blocks; the table consumer reads raw lines including blanks.
        self.lines = self.copy.split("\n")
        self.n = len(self.lines)
        self.i = 0
        self.blocks = []
        self.links = []  # (anchor, href)
        self.h2_idx = 0
        self.section = None
        self.p_count = 0
        self.table_idx = 0
        self.parse_seo()

    # ---- SEO -------------------------------------------------------------
    def parse_seo(self):
        def field(pat):
            m = re.search(pat, self.seo_part)
            assert m, f"SEO field missing: {pat}"
            return m.group(1).strip(), (int(m.group(2)) if m.lastindex and m.lastindex >= 2 and m.group(2) else None)

        m = re.search(r"Meta title \((\d+) chars\)\n([^\n]+)", self.seo_part)
        assert m, "meta title missing"
        self.title = m.group(2).strip()
        assert len(self.title) == int(m.group(1)), f"title len {len(self.title)} != {m.group(1)}"
        m = re.search(r"Meta description \((\d+) chars\)\n([^\n]+)", self.seo_part)
        assert m, "meta description missing"
        self.meta = m.group(2).strip()
        assert len(self.meta) == int(m.group(1)), f"meta len {len(self.meta)} != {m.group(1)}"
        m = re.search(r"\nH1\n([^\n]+)", self.seo_part)
        assert m, "H1 missing"
        self.h1 = m.group(1).strip()
        m = re.search(r"Schema \(JSON-LD\)\n(\{.*?\n\})", self.seo_part, re.S)
        assert m, "schema JSON missing"
        self.schema = json.loads(m.group(1))
        ex = self.spec["expect"]
        assert self.title == ex["title"], f"title mismatch: {self.title!r}"
        assert self.meta == ex["meta"], f"meta mismatch: {self.meta!r}"
        assert self.h1 == ex["h1"], f"H1 mismatch: {self.h1!r}"
        assert self.schema["@type"] == ex["schema_type"], f"schema type {self.schema['@type']}"
        assert self.schema.get("url") == ex["url"], f"schema url {self.schema.get('url')}"
        if ex["schema_type"] == "HowTo":
            assert self.schema.get("totalTime") == "PT1H"
            assert len(self.schema.get("step", [])) == 5
        if ex["schema_type"] == "Article":
            assert self.schema.get("dateModified") == "2026-11-19"
            assert self.schema.get("inLanguage") == "en-US"
        print(f"[{self.slug}] title ({len(self.title)}ch): {self.title}")
        print(f"[{self.slug}] meta ({len(self.meta)}ch)")
        print(f"[{self.slug}] H1: {self.h1}")
        print(f"[{self.slug}] schema: {self.schema['@type']} name={self.schema.get('name') or self.schema.get('headline')}")

    # ---- segment / line helpers ------------------------------------------
    def parse_segments(self, text, where):
        segs = []
        pos = 0
        for m in re.finditer(r"\((/[a-z0-9\-/]*)\)", text):
            href = m.group(1)
            before = text[pos:m.start()]
            cut = 0
            for b in BOUNDARIES:
                j = before.rfind(b)
                if j >= 0:
                    cut = max(cut, j + len(b))
            anchor = before[cut:].rstrip()
            pre = before[:cut]
            if pre:
                segs.append({"t": pre})
            if not anchor or len(words(anchor)) > 12:
                raise SystemExit(f"[{self.slug}] BAD ANCHOR {where}: {anchor!r} before {href}")
            if href not in PLANNED:
                raise SystemExit(f"[{self.slug}] HREF NOT A PLANNED ROUTE {where}: {href}")
            segs.append({"t": anchor, "href": href})
            self.links.append((anchor, href))
            pos = m.end()
        if text[pos:]:
            segs.append({"t": text[pos:]})
        return segs

    def expect(self, text):
        assert self.lines[self.i] == text, \
            f"[{self.slug}] line {self.i}: expected {text!r}, got {self.lines[self.i]!r}"
        self.i += 1

    def take_para(self):
        assert self.lines[self.i].strip() != "", f"[{self.slug}] blank para at {self.i}"
        segs = self.parse_segments(self.lines[self.i], f"para L{self.i}")
        self.i += 1
        return segs

    def take_bullets(self):
        out = []
        start = self.i
        while self.i < self.n and self.lines[self.i].startswith("• "):
            out.append(self.parse_segments(self.lines[self.i][2:], f"bullet L{self.i}"))
            self.i += 1
        assert out, f"[{self.slug}] expected bullets at {start}"
        return out

    def take_steps(self):
        # "1. Title" + body para, OR "1.  Full sentence." inline items.
        m0 = re.match(r"(\d+)\.\s+(.*)", self.lines[self.i])
        assert m0, f"[{self.slug}] not a step at {self.i}: {self.lines[self.i][:60]!r}"
        inline = m0.group(2).rstrip().endswith((".", "?", "!"))
        out = []
        k = 0
        while self.i < self.n:
            m = re.match(rf"{k + 1}\.\s+(.*)", self.lines[self.i])
            if not m:
                break
            if inline:
                out.append(self.parse_segments(m.group(1), f"step-inline L{self.i}"))
                self.i += 1
            else:
                title = m.group(1)
                self.i += 1
                body = self.take_para()
                out.append({"title": title, "body": body})
            k += 1
        assert out, f"[{self.slug}] no steps at {self.i}"
        return {"type": "steps-numbered" if inline else "steps", "items": out}

    def take_steps_rich(self):
        # How-it-works steps: "N. Title" followed by ANY mix of paras and
        # bullet lists (each step runs until the next step number or the
        # next H2). Parts keep their own block shape for the renderer.
        out = []
        k = 0
        h2s = self.spec["h2s"]
        while self.i < self.n:
            m = re.match(rf"{k + 1}\.\s+(.*)", self.lines[self.i])
            if not m:
                break
            title = m.group(1)
            self.i += 1
            parts = []
            while self.i < self.n:
                line = self.lines[self.i]
                if re.match(rf"{k + 2}\.\s+", line):
                    break
                if self.h2_idx < len(h2s) and line == h2s[self.h2_idx]:
                    break
                if line.startswith("• "):
                    parts.append({"type": "ul", "items": self.take_bullets()})
                    continue
                if line.strip() == "":
                    self.i += 1
                    continue
                parts.append({"type": "p", "segs": self.take_para()})
            out.append({"title": title, "parts": parts})
            k += 1
        assert out, f"[{self.slug}] no rich steps at {self.i}"
        return {"type": "steps-rich", "items": out}

    def take_table(self, cols, rows):
        head = []
        for _ in range(cols):
            head.append(self.parse_segments(self.lines[self.i], f"table head L{self.i}"))
            self.i += 1
        body = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(self.parse_segments(self.lines[self.i], f"table cell L{self.i}"))
                self.i += 1
            body.append(row)
        return {"type": "table", "head": head, "rows": body}

    def pending_table(self):
        if self.section is None:
            return None
        tabs = self.spec.get("tables", {}).get(self.section, [])
        if self.table_idx < len(tabs) and tabs[self.table_idx]["after"] == self.p_count:
            return tabs[self.table_idx]
        return None

    # ---- main walk -------------------------------------------------------
    def run(self):
        spec = self.spec
        # Hero: H1 line, intro para, CTA line.
        self.expect(self.h1)
        intro = self.take_para()
        self.blocks.append({"type": "hero-intro", "segs": intro})
        self.expect(CTA)
        self.blocks.append({"type": "cta-line", "text": CTA})
        # Optional pre-details paras, then the details card.
        det = spec.get("details")
        if det:
            for _ in range(det[3]):
                self.blocks.append({"type": "p", "segs": self.take_para()})
            self.expect(det[0])
            self.expect(det[1])
            rows = []
            for _ in range(det[2]):
                label = self.lines[self.i]
                self.i += 1
                value = self.take_para()
                rows.append({"label": label, "value": value})
            self.blocks.append({"type": "details", "heading": det[0], "sub": det[1], "rows": rows})
        # Tables that come before the first H2 (intro section): paras, an
        # optional h3, then the table. (Areas page: ZIP-codes table.)
        for it in spec.get("intro_tables", []):
            for _ in range(it.get("pre", 0)):
                self.blocks.append({"type": "p", "segs": self.take_para()})
            if it.get("h3"):
                self.expect(it["h3"])
                self.blocks.append({"type": "h3", "text": it["h3"]})
            self.blocks.append(self.take_table(it["cols"], it["rows"]))
        h2s = spec["h2s"]
        faq_h, faq_n = spec["faq"]
        rel = spec.get("related")
        rel_h, rel_n = rel if rel else (None, 0)
        final_h = spec["final"]
        if rel_h is None:
            assert h2s[-2] == faq_h and h2s[-1] == final_h, \
                f"[{self.slug}] h2s tail != faq/final"
        else:
            assert h2s[-3] == faq_h and h2s[-2] == rel_h and h2s[-1] == final_h, \
                f"[{self.slug}] h2s tail != faq/related/final"
        while True:
            # Table due? Check BEFORE skipping blanks: a blank line may be an
            # empty header cell (sewage "Sewer or Septic?" table).
            tbl = self.pending_table()
            if tbl is not None:
                self.blocks.append(self.take_table(tbl["cols"], tbl["rows"]))
                self.table_idx += 1
                continue
            while self.i < self.n and self.lines[self.i].strip() == "":
                self.i += 1
            if self.i >= self.n:
                break
            line = self.lines[self.i]
            if self.h2_idx < len(h2s) and line == h2s[self.h2_idx]:
                h = line
                self.i += 1
                self.h2_idx += 1
                self.blocks.append({"type": "h2", "text": h})
                if h == faq_h:
                    faqs = []
                    # FAQ runs until the Related heading, or the final H2 when
                    # the page has no Related section (areas page). The count
                    # is the authority; link-line paras between FAQ and the
                    # next heading (areas: "Who we are and how a job runs:")
                    # are plain paragraphs.
                    stop = rel_h if rel_h is not None else final_h
                    while len(faqs) < faq_n and self.lines[self.i] != stop:
                        q = self.lines[self.i]
                        self.i += 1
                        a = self.take_para()
                        faqs.append({"q": q, "a": a})
                    assert len(faqs) == faq_n, \
                        f"[{self.slug}] FAQ count {len(faqs)} != {faq_n}"
                    print(f"[{self.slug}] FAQ pairs: {len(faqs)}")
                    self.blocks.append({"type": "faq", "items": faqs})
                    while self.i < self.n and self.lines[self.i] != stop:
                        self.blocks.append({"type": "p", "segs": self.take_para()})
                    continue
                if h == rel_h:
                    items = self.take_bullets()
                    assert len(items) == rel_n, \
                        f"[{self.slug}] Related count {len(items)} != {rel_n}"
                    self.blocks.append({"type": "ul", "items": items})
                    continue
                if h == final_h:
                    self.blocks.append({"type": "p", "segs": self.take_para()})
                    self.expect(CTA)
                    self.blocks.append({"type": "cta-line", "text": CTA})
                    assert self.i == self.n, \
                        f"[{self.slug}] lines left after final CTA: {self.lines[self.i]!r}"
                    break
                self.section = h
                self.p_count = 0
                self.table_idx = 0
                continue
            if line.startswith("• "):
                self.blocks.append({"type": "ul", "items": self.take_bullets()})
                continue
            if re.match(r"^\d+\.\s", line):
                if self.spec.get("rich_steps"):
                    self.blocks.append(self.take_steps_rich())
                else:
                    self.blocks.append(self.take_steps())
                continue
            if line.startswith("Map: "):
                # Service-area map embed (contact page). Same 'map' block
                # shape as the homepage parser emits.
                self.blocks.append({"type": "map", "caption": line})
                self.i += 1
                continue
            if line == CTA or line == f"Call {PHONE}":
                self.blocks.append({"type": "cta-line", "text": line})
                self.i += 1
                continue
            if len(line) < 60 and not line.endswith((".", ":")):
                self.blocks.append({"type": "h3", "text": line})
                self.i += 1
                continue
            self.blocks.append({"type": "p", "segs": self.take_para()})
            self.p_count += 1
        assert self.h2_idx == len(h2s), \
            f"[{self.slug}] consumed {self.h2_idx} of {len(h2s)} H2s; next: {h2s[self.h2_idx]!r}"
        assert self.i == self.n, f"[{self.slug}] consumed {self.i} of {self.n} lines"
        self.word_diff()
        self.emit()

    # ---- word-diff -------------------------------------------------------
    def block_words(self, b):
        out = []
        t = b["type"]
        if t == "hero-intro":
            out += words(seg_text(b["segs"]))
        elif t == "details":
            out += words(b["heading"]) + words(b["sub"])
            for r in b["rows"]:
                out += words(r["label"]) + words(seg_text(r["value"]))
        elif t in ("h2", "h3"):
            out += words(b["text"])
        elif t == "p":
            out += words(seg_text(b["segs"]))
        elif t == "ul":
            for it in b["items"]:
                out += words(seg_text(it))
        elif t == "table":
            for c in b["head"]:
                out += words(seg_text(c))
            for row in b["rows"]:
                for c in row:
                    out += words(seg_text(c))
        elif t == "steps":
            for k, s in enumerate(b["items"]):
                out += [str(k + 1)] + words(s["title"]) + words(seg_text(s["body"]))
        elif t == "steps-rich":
            for k, s in enumerate(b["items"]):
                out += [str(k + 1)] + words(s["title"])
                for part in s["parts"]:
                    out += self.block_words(part)
        elif t == "map":
            out += words(b["caption"])
        elif t == "steps-numbered":
            for k, s in enumerate(b["items"]):
                out += [str(k + 1)] + words(seg_text(s))
        elif t == "cta-line":
            out += words(b["text"])
        elif t == "faq":
            for f in b["items"]:
                out += words(f["q"]) + words(seg_text(f["a"]))
        else:
            raise SystemExit(f"[{self.slug}] unknown block type {t}")
        return out

    def word_diff(self):
        got = words(self.h1)
        for b in self.blocks:
            got += self.block_words(b)
        visible_copy = re.sub(r"\((/[a-z0-9\-/]*)\)", "", self.copy)
        want = words(visible_copy)
        print(f"[{self.slug}] copy words (visible): {len(want)}; blocks words: {len(got)}")
        if got != want:
            for k, (a, b) in enumerate(zip(got, want)):
                if a != b:
                    print(f"[{self.slug}] FIRST DIFF at word {k}: got {a!r} want {b!r}")
                    print("  got context:", got[max(0, k - 8):k + 8])
                    print("  want context:", want[max(0, k - 8):k + 8])
                    break
            print(f"[{self.slug}] lengths got={len(got)} want={len(want)}")
            raise SystemExit(f"[{self.slug}] WORD-DIFF FAILED")
        print(f"[{self.slug}] WORD-DIFF 0 ✓")

    def emit(self):
        data = {"seo": {"title": self.title, "meta": self.meta, "h1": self.h1,
                        "schema": self.schema},
                "blocks": self.blocks}
        out = os.path.join(OUT_DIR, self.slug + ".php")
        php = "<?php\n"
        php += f"// {self.slug} content — parsed verbatim from {self.spec['paste']}\n"
        php += "// by tools/parse_page.py. Do NOT hand-edit: re-run the parser.\n"
        php += "return " + php_val(data) + ";\n"
        open(out, "w").write(php)
        print(f"[{self.slug}] wrote {out} ({len(php)} bytes)")
        distinct = sorted(set(h for _, h in self.links))
        pending = [h for h in distinct if h not in BUILT]
        print(f"[{self.slug}] links: {len(self.links)} total, {len(distinct)} distinct; "
              f"pending pages linked: {pending}")


SPECS = []

SPECS = [
{
    "slug": "water-removal",
    "paste": "water-removal-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/water-removal/",
        "title": "Emergency Water Removal Fort Myers, FL | 24/7 Extraction",
        "meta": "Standing water in your Fort Myers home? Call 239-356-3708, answered 24/7, for water extraction, moisture mapping and drying setup across Lee County.",
        "h1": "Emergency Water Removal in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Fort Myers water removal", "Details", 5, 1),
    "h2s": [
        "Water Spreading in Your Fort Myers Home Right Now? Do This First",
        "What to Have Ready When You Call for Water Removal in Fort Myers",
        "What Happens During Emergency Water Removal in Fort Myers?",
        "How Fast Does Water Need to Come Out of a Fort Myers Home?",
        "What Equipment Is Used for Water Extraction in Fort Myers Homes?",
        "What You Get After Water Removal in Fort Myers",
        "Can You Remove the Water Yourself With a Shop Vac in Fort Myers?",
        "What Can Be Saved After Water Removal in Fort Myers?",
        "What Happens to Furniture and Belongings During Water Removal in Fort Myers?",
        "Water Removal by Source in Fort Myers Homes",
        "Water Removal in Fort Myers Block Homes, Condos, Garages and Lanais",
        "Water Removal After a Storm or Flood in Lee County",
        "Saltwater Storm Surge: Why Water Removal Is Different Near the Gulf",
        "Will Insurance Pay for Water Removal in Fort Myers?",
        "Questions About Emergency Water Removal in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Water on Your Fort Myers Floor Right Now?",
    ],
    "tables": {
        "How Fast Does Water Need to Come Out of a Fort Myers Home?": [
            {"cols": 2, "rows": 4, "after": 1}],
        "What Can Be Saved After Water Removal in Fort Myers?": [
            {"cols": 3, "rows": 7, "after": 1}],
        "Water Removal by Source in Fort Myers Homes": [
            {"cols": 4, "rows": 8, "after": 1}],
    },
    "faq": ("Questions About Emergency Water Removal in Fort Myers", 14),
    "related": ("Related Water Damage Help in Fort Myers", 8),
    "final": "Water on Your Fort Myers Floor Right Now?",
},
{
    "slug": "drying",
    "paste": "drying-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/drying/",
        "title": "Water Mitigation & Structural Drying Fort Myers, FL | 24/7",
        "meta": "Walls or slab still wet after a leak? Structural drying in Fort Myers with daily moisture readings until it's truly dry. Call 239-356-3708, 24/7.",
        "h1": "Water Mitigation and Structural Drying in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Fort Myers structural drying", "Details", 6, 1),
    "h2s": [
        "Water Mitigation vs. Restoration in Fort Myers: What's the Difference?",
        "How Structural Drying Works in Fort Myers Homes",
        "Why Drying Takes Longer in Fort Myers Homes",
        "Drying Fort Myers Block Homes, Ceilings, Condos and Mobile Homes",
        "Why Box Fans and a Home Dehumidifier Aren't Enough in Fort Myers Humidity",
        "How Long Structural Drying Takes in Fort Myers",
        "Drying Classes 1 to 4: How Equipment Is Sized in Fort Myers Homes",
        'What "Dry" Means: How Fort Myers Drying Jobs Are Measured',
        "Does Wet Drywall Have to Be Cut Out in Fort Myers Homes?",
        "How Slabs, Floors and Cabinets Are Dried in Fort Myers",
        "Living With Drying Equipment in Your Fort Myers Home",
        "Before Repairs Start: Your Fort Myers Drying Checklist",
        "Why Moisture Logs Matter for Your Florida Insurance Claim",
        "Leaks That Need Careful Drying in Fort Myers",
        "Questions About Water Mitigation and Drying in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Wet Walls or Floors in Your Fort Myers Home That Won't Dry?",
    ],
    "tables": {
        "Water Mitigation vs. Restoration in Fort Myers: What's the Difference?": [
            {"cols": 3, "rows": 3, "after": 1}],
        "How Long Structural Drying Takes in Fort Myers": [
            {"cols": 2, "rows": 5, "after": 1}],
        "Drying Classes 1 to 4: How Equipment Is Sized in Fort Myers Homes": [
            {"cols": 2, "rows": 4, "after": 1}],
        'What "Dry" Means: How Fort Myers Drying Jobs Are Measured': [
            {"cols": 3, "rows": 6, "after": 1}],
    },
    "faq": ("Questions About Water Mitigation and Drying in Fort Myers", 13),
    "related": ("Related Water Damage Help in Fort Myers", 8),
    "final": "Wet Walls or Floors in Your Fort Myers Home That Won't Dry?",
},
{
    "slug": "sewage-cleanup",
    "paste": "sewage-cleanup-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/sewage-cleanup/",
        "title": "Sewage Backup Cleanup Fort Myers, FL | Answered 24/7",
        "meta": "Toilet or drain backing up in Fort Myers? Call 239-356-3708, answered 24/7, for safe sewage cleanup, disinfection and drying across Lee County.",
        "h1": "Sewage Backup Cleanup in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Fort Myers sewage cleanup", "Details", 6, 1),
    "h2s": [
        "Sewage Backing Up in Your Fort Myers Home Right Now? Do This First",
        "Is Sewage Water Dangerous? Staying Safe in a Fort Myers Backup",
        "Why Sewage Backs Up in Fort Myers Homes",
        "Signs Your Fort Myers Main Sewer Line Is Backing Up",
        "Sewer or Septic? What Lee County Homeowners Should Check",
        "Who Is Responsible for the Sewer Line in Fort Myers?",
        "How Sewage Cleanup Works in Fort Myers Homes",
        "What Can Be Saved After a Sewage Backup in Fort Myers?",
        "After Cleanup: How to Know Your Fort Myers Home Is Safe Again",
        "Sewage Backups in Fort Myers Condos and Multi-Unit Buildings",
        "Sewage After Storms and Flooding in Lee County",
        "Does Insurance Cover Sewage Backup in Florida?",
        "How to Prevent Another Sewage Backup in Your Fort Myers Home",
        "Questions About Sewage Backup Cleanup in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Sewage in Your Fort Myers Home Right Now?",
    ],
    "tables": {
        "Sewer or Septic? What Lee County Homeowners Should Check": [
            {"cols": 3, "rows": 5, "after": 1}],
        "What Can Be Saved After a Sewage Backup in Fort Myers?": [
            {"cols": 2, "rows": 10, "after": 0}],
    },
    "faq": ("Questions About Sewage Backup Cleanup in Fort Myers", 13),
    "related": ("Related Water Damage Help in Fort Myers", 7),
    "final": "Sewage in Your Fort Myers Home Right Now?",
},
{
    "slug": "ac-leak",
    "paste": "ac-leak-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/ac-leak/",
        "title": "AC Leak Water Damage Fort Myers | Air Handler & Drain Line",
        "meta": "AC leaking through the ceiling or out of the air handler closet in Fort Myers? Call 239-356-3708, answered 24/7, to dry the ceiling, walls and floor.",
        "h1": "AC Leak Water Damage in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Fort Myers AC leak damage", "Details", 6, 1),
    "h2s": [
        "AC Leaking in Your Fort Myers Home Right Now? Do This First",
        "What You See vs. What's Wrong: Reading an AC Leak in Fort Myers",
        "Why Is My AC Leaking Water Inside My Fort Myers Home?",
        "The Backup Drain and Float Switch in Fort Myers AC Systems",
        "Signs of AC Water Damage in Fort Myers Homes",
        "Where AC Leak Water Goes in Fort Myers Homes and Condos",
        "AC Repair vs. Water Damage Restoration in Fort Myers: Who Fixes What?",
        "How AC Leak Damage Is Dried and Repaired in Fort Myers",
        "Is AC Condensate Water Clean in a Fort Myers Home?",
        "Condo AC Leaks in Fort Myers: When Your Unit Floods the One Below",
        "Does Insurance Cover AC Leak Water Damage in Florida?",
        "How to Stop AC Leaks in Your Fort Myers Home",
        "Questions About AC Leak Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "AC Leaking in Your Fort Myers Home Right Now?",
    ],
    "tables": {
        "What You See vs. What's Wrong: Reading an AC Leak in Fort Myers": [
            {"cols": 3, "rows": 7, "after": 1}],
        "Where AC Leak Water Goes in Fort Myers Homes and Condos": [
            {"cols": 3, "rows": 4, "after": 1}],
    },
    "faq": ("Questions About AC Leak Water Damage in Fort Myers", 11),
    "related": ("Related Water Damage Help in Fort Myers", 7),
    "final": "AC Leaking in Your Fort Myers Home Right Now?",
},
{
    "slug": "ceiling-leak",
    "paste": "ceiling-leak-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/ceiling-leak/",
        "title": "Water Leaking Through Ceiling in Fort Myers? 24/7 Help",
        "meta": "Ceiling dripping or sagging in Fort Myers? Call 239-356-3708, answered 24/7. Find the source (AC, roof, bathroom above) and get the ceiling dried.",
        "h1": "Water Leaking Through the Ceiling in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Fort Myers ceiling leaks", "Details", 6, 1),
    "h2s": [
        "Water Coming Through Your Fort Myers Ceiling? Do This Right Now",
        "Is a Sagging Ceiling in Your Fort Myers Home About to Fall?",
        "Where Is the Water in Your Fort Myers Ceiling Coming From?",
        "Why Is My Fort Myers Ceiling Leaking When It Isn't Raining?",
        "Roof Leaks in Fort Myers: Tile, Shingle and Flat Roofs",
        "Why Ceiling Leaks Are So Common in Fort Myers Homes",
        "Why a Ceiling Stain in a Fort Myers Home Is More Than a Paint Problem",
        "Should You Go Into the Attic in a Fort Myers Home?",
        "How a Wet Ceiling Is Dried or Replaced in Fort Myers",
        "Popcorn Ceilings in Older Fort Myers Homes",
        "Condo Ceiling Leaks in Fort Myers: Water From the Unit Above",
        "Does Insurance Cover a Leaking Ceiling in Florida?",
        "How to Prevent Ceiling Leaks in Your Fort Myers Home",
        "Questions About Ceiling Leaks in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Ceiling Leaking in Your Fort Myers Home Right Now?",
    ],
    "tables": {
        "Where Is the Water in Your Fort Myers Ceiling Coming From?": [
            {"cols": 4, "rows": 7, "after": 1}],
        "Roof Leaks in Fort Myers: Tile, Shingle and Flat Roofs": [
            {"cols": 3, "rows": 4, "after": 1}],
        "Why a Ceiling Stain in a Fort Myers Home Is More Than a Paint Problem": [
            {"cols": 3, "rows": 3, "after": 2}],
    },
    "faq": ("Questions About Ceiling Leaks in Fort Myers", 11),
    "related": ("Related Water Damage Help in Fort Myers", 7),
    "final": "Ceiling Leaking in Your Fort Myers Home Right Now?",
},
{
    "slug": "condo-leak",
    "paste": "condo-leak-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/condo-leak/",
        "title": "Condo Water Damage Fort Myers | Leak From the Unit Above",
        "meta": "Water coming from the condo above in Fort Myers? Call 239-356-3708, answered 24/7. First steps, who usually handles what under Florida law, and drying.",
        "h1": "Condo Water Damage in Fort Myers: Leaks From the Unit Above",
        "schema_type": "Service",
    },
    "details": ("Fort Myers condo leaks", "Details", 6, 1),
    "h2s": [
        "Water Leaking From the Condo Above in Fort Myers? First-Hour Steps",
        "Why Condo Leaks in Fort Myers Are Different From House Leaks",
        "How Water Travels in Fort Myers Condo Buildings",
        "What Causes Most Condo Leaks in Southwest Florida",
        "Who Pays for a Condo Leak in Fort Myers? What Florida Law Says",
        "Who Should Start the Cleanup in a Fort Myers Condo?",
        "Can the Association Get Into a Fort Myers Condo to Stop a Leak?",
        "Your Fort Myers Condo Leak Paper Trail",
        "How Condo Water Damage Is Dried in Fort Myers",
        "What an HO-6 Policy Usually Covers for Fort Myers Condo Owners",
        "Condo Leaks in Seasonal Fort Myers Buildings",
        "Questions About Condo Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Water Coming From the Condo Above Right Now?",
    ],
    "tables": {
        "How Water Travels in Fort Myers Condo Buildings": [
            {"cols": 3, "rows": 3, "after": 1}],
        "Who Pays for a Condo Leak in Fort Myers? What Florida Law Says": [
            {"cols": 2, "rows": 5, "after": 4}],
        "Your Fort Myers Condo Leak Paper Trail": [
            {"cols": 3, "rows": 7, "after": 1}],
    },
    "faq": ("Questions About Condo Water Damage in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 8),
    "final": "Water Coming From the Condo Above Right Now?",
},
{
    "slug": "cast-iron-pipe",
    "paste": "cast-iron-pipe-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/cast-iron-pipe/",
        "title": "Cast Iron Pipe Water Damage Fort Myers & Cape Coral",
        "meta": "Sewer smell, slow drains or damp tile in an older Fort Myers or Cape Coral home? Call 239-356-3708, answered 24/7, for Category 3 cleanup and drying.",
        "h1": "Cast Iron Pipe Water Damage in Fort Myers and Cape Coral",
        "schema_type": "Service",
    },
    "details": ("Cast iron leaks in Lee County", "Details", 6, 1),
    "h2s": [
        "Sewer Smell, Backups or Damp Tile in Your Fort Myers Home? Do This First",
        "Why Cast Iron Pipes Fail in Fort Myers and Cape Coral",
        "Signs of Cast Iron Pipe Failure in Fort Myers Homes",
        "How to Tell If Your Fort Myers or Cape Coral Home Has Cast Iron Pipes",
        "What the Camera Shows: Stages of Cast Iron Failure in Fort Myers Homes",
        "What a Leaking Cast Iron Drain Does to a Fort Myers Home",
        "How Cast Iron Pipe Is Fixed in Fort Myers Homes: Lining, Spot Repair or Replacement",
        "Questions to Ask Your Plumber After the Camera Inspection",
        "How a Cast Iron Job Runs in a Fort Myers Home, Start to Finish",
        "Living Through Cast Iron Repairs in Your Fort Myers Home",
        "Does Insurance Cover Cast Iron Pipe Damage in Florida?",
        "Check for a water damage limit before the floor is opened",
        "Cast Iron in Fort Myers Condo Buildings",
        "Questions About Cast Iron Pipe Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Sewer Smell, Backups or Damp Tile in an Older Fort Myers Home?",
    ],
    "tables": {
        "What the Camera Shows: Stages of Cast Iron Failure in Fort Myers Homes": [
            {"cols": 3, "rows": 5, "after": 1}],
        "What a Leaking Cast Iron Drain Does to a Fort Myers Home": [
            {"cols": 2, "rows": 6, "after": 1}],
        "How Cast Iron Pipe Is Fixed in Fort Myers Homes: Lining, Spot Repair or Replacement": [
            {"cols": 4, "rows": 4, "after": 1}],
    },
    "faq": ("Questions About Cast Iron Pipe Water Damage in Fort Myers", 11),
    "related": ("Related Water Damage Help in Fort Myers", 7),
    "final": "Sewer Smell, Backups or Damp Tile in an Older Fort Myers Home?",
},
{
    "slug": "vacant-home",
    "paste": "vacant-home-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/vacant-home/",
        "title": "Seasonal Home Water Damage Fort Myers | Came Back to a Leak?",
        "meta": "Back in your Fort Myers home to a wet floor, ceiling stain or musty smell? Call 239-356-3708, answered 24/7. What failed, what to do first and drying.",
        "h1": "Water Damage Found After Returning to Your Fort Myers Home",
        "schema_type": "Service",
    },
    "details": ("Seasonal homes in Lee County", "Details", 6, 1),
    "h2s": [
        "Found Water Damage After Time Away From Fort Myers? Do This First",
        "What Usually Fails While a Fort Myers Home Sits Empty",
        "Room-by-Room Return Check for Your Fort Myers Home",
        "Is That Musty Smell in Your Fort Myers Home Humidity or Water Damage?",
        "How Long-Running Leaks Change the Cleanup in a Fort Myers Home",
        "How Water Damage in a Vacant Fort Myers Home Is Dried",
        "Insurance When Nobody Was Home: What Fort Myers Owners Should Know",
        "What a Good Home Watch Visit Covers in Lee County",
        "Smart Devices That Protect an Empty Fort Myers Home",
        "How to Protect Your Fort Myers Home Next Time You Leave",
        "If a Storm Hits Lee County While You're Away",
        "Questions About Water Damage in Vacant Fort Myers Homes",
        "Related Water Damage Help in Fort Myers",
        "Came Back to Water Damage in Your Fort Myers Home?",
    ],
    "tables": {
        "Room-by-Room Return Check for Your Fort Myers Home": [
            {"cols": 2, "rows": 9, "after": 1}],
        "Smart Devices That Protect an Empty Fort Myers Home": [
            {"cols": 3, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Damage in Vacant Fort Myers Homes", 9),
    "related": ("Related Water Damage Help in Fort Myers", 7),
    "final": "Came Back to Water Damage in Your Fort Myers Home?",
},
{
    "slug": "first-hour-checklist",
    "paste": "first-hour-checklist-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/first-hour-checklist/",
        "title": "What to Do After Water Damage in Fort Myers: Checklist",
        "meta": "What to do in the first hour after a leak or flood in a Fort Myers home: safety, shut-off, photos, drying and insurance steps. Printable checklist.",
        "h1": "What to Do in the First Hour After Water Damage in Fort Myers",
        "schema_type": "HowTo",
    },
    "details": None,
    "h2s": [
        "The First-Hour Checklist for Fort Myers Homes, Minute by Minute",
        "What to Do First in a Fort Myers Home, by Type of Water Damage",
        "Extra First-Hour Steps After a Storm or Flood in Lee County",
        "What Not to Do After Water Damage in a Fort Myers Home",
        "Why the First 48 Hours Matter So Much in Fort Myers",
        "Before It Happens: Set Up Your Fort Myers Home in 15 Minutes",
        "What to Have Ready When You Call for Help in Fort Myers",
        "What Happens in the Next 1 to 5 Days in a Fort Myers Home",
        "Insurance Steps in the First Hour for Florida Homeowners",
        "Printable First-Hour Checklist for Fort Myers Homes",
        "Questions About the First Hour After Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Water Damage Happening Now in Your Fort Myers Home?",
    ],
    "tables": {
        "What to Do First in a Fort Myers Home, by Type of Water Damage": [
            {"cols": 3, "rows": 11, "after": 0}],
        "Why the First 48 Hours Matter So Much in Fort Myers": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About the First Hour After Water Damage in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 8),
    "final": "Water Damage Happening Now in Your Fort Myers Home?",
},
{
    "slug": "cost",
    "paste": "cost-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/cost/",
        "title": "Water Damage Restoration Cost Fort Myers, FL | Price Guide",
        "meta": "What water damage restoration costs in Fort Myers: rough local ranges by job size, square foot and repair, and what moves the price in Lee County.",
        "h1": "How Much Does Water Damage Restoration Cost in Fort Myers?",
        "schema_type": "Article",
    },
    "details": ("Water damage pricing in Fort Myers", "Rough area idea", 9, 2),
    "h2s": [
        "Water Damage Restoration Cost in Fort Myers by Size of the Job",
        "Water Damage Cost per Square Foot in Fort Myers",
        "Damage Class: Why Two Fort Myers Leaks of the Same Size Are Priced Differently",
        "What Goes on a Fort Myers Water Damage Estimate, Line by Line",
        "Why Water Damage Can Run Higher in a Fort Myers Home",
        "Typical Fort Myers Jobs and Where They Usually Land",
        "How Fort Myers Water Damage Estimates Are Priced",
        "What a Fair Fort Myers Water Damage Estimate Should Include",
        "Repair Prices After Drying in Fort Myers Homes",
        "What Waiting Does to the Price in a Fort Myers Home",
        "Costs Fort Myers Homeowners Often Forget",
        "How Insurance Changes What You Pay in Fort Myers",
        "Lee County's 50% Rule and Your Repair Total",
        "How to Keep the Water Damage Bill Down in Fort Myers",
        "Is It Cheaper to Dry It Yourself in Fort Myers?",
        "Questions About Water Damage Restoration Cost in Fort Myers",
        "Related Water Damage Guides for Fort Myers Homeowners",
        "Want a Real Number for Your Fort Myers Home?",
    ],
    "tables": {
        "Water Damage Restoration Cost in Fort Myers by Size of the Job": [
            {"cols": 3, "rows": 6, "after": 1}],
        "Water Damage Cost per Square Foot in Fort Myers": [
            {"cols": 2, "rows": 4, "after": 0},
            {"cols": 3, "rows": 3, "after": 1}],
        "Damage Class: Why Two Fort Myers Leaks of the Same Size Are Priced Differently": [
            {"cols": 4, "rows": 4, "after": 1}],
        "What Goes on a Fort Myers Water Damage Estimate, Line by Line": [
            {"cols": 3, "rows": 8, "after": 1}],
        "Repair Prices After Drying in Fort Myers Homes": [
            {"cols": 2, "rows": 8, "after": 1}],
        "What Waiting Does to the Price in a Fort Myers Home": [
            {"cols": 2, "rows": 3, "after": 0}],
    },
    "faq": ("Questions About Water Damage Restoration Cost in Fort Myers", 12),
    "related": ("Related Water Damage Guides for Fort Myers Homeowners", 8),
    "final": "Want a Real Number for Your Fort Myers Home?",
},
{
    "slug": "insurance",
    "paste": "insurance-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/insurance/",
        "title": "Does Insurance Cover Water Damage in Fort Myers, Florida?",
        "meta": "Sudden vs gradual leaks, flood vs water damage, Citizens limits, the $10,000 cap and claim deadlines for Fort Myers and Lee County homeowners.",
        "h1": "Does Homeowners Insurance Cover Water Damage in Fort Myers?",
        "schema_type": "Article",
    },
    "details": ("Fort Myers water damage", "Usually covered by homeowners insurance?", 7, 2),
    "h2s": [
        "What Florida Homeowners Insurance Usually Covers for Fort Myers Water Damage",
        "Sudden vs Gradual: The Rule Behind Most Fort Myers Water Claims",
        "Flood vs Water Damage for Lee County Homes",
        "Citizens Policies in Lee County: Water Limits and the Flood Requirement",
        "Sewer and Drain Backup Coverage for Fort Myers Homes",
        "Condo Water Damage Insurance in Fort Myers: Association vs HO-6",
        "Water Damage Limits and Endorsements on Fort Myers Policies",
        "Deductibles and Policy Terms Fort Myers Homeowners Should Know",
        "Florida Deadlines for a Fort Myers Water Damage Claim",
        "What Your Insurer Must Do for a Fort Myers Claim Under Florida Law",
        "Assignment of Benefits Is Gone: Who Pays Whom in Fort Myers Now",
        "How to Protect Your Fort Myers Water Damage Claim",
        "Will Insurance Pay for a Hotel While Your Fort Myers Home Dries?",
        "Seasonal and Vacant Homes in Lee County",
        "Older Fort Myers Homes: Plumbing and Insurability",
        "If Your Fort Myers Water Damage Claim Is Denied or Underpaid",
        "Questions About Water Damage Insurance in Fort Myers",
        "Related Water Damage Guides for Fort Myers Homeowners",
        "Water Damage and a Claim to File in Your Fort Myers Home?",
    ],
    "tables": {
        "What Florida Homeowners Insurance Usually Covers for Fort Myers Water Damage": [
            {"cols": 3, "rows": 10, "after": 0}],
        "Florida Deadlines for a Fort Myers Water Damage Claim": [
            {"cols": 2, "rows": 3, "after": 0}],
        "What Your Insurer Must Do for a Fort Myers Claim Under Florida Law": [
            {"cols": 2, "rows": 5, "after": 1}],
    },
    "faq": ("Questions About Water Damage Insurance in Fort Myers", 12),
    "related": ("Related Water Damage Guides for Fort Myers Homeowners", 7),
    "final": "Water Damage and a Claim to File in Your Fort Myers Home?",
},
{
    "slug": "burst-pipe",
    "paste": "burst-pipe-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/burst-pipe/",
        "title": "Burst Pipe Water Damage Fort Myers, FL | 24/7 Cleanup",
        "meta": "Pipe or supply line burst in your Fort Myers home? Shut-off steps, why Florida pipes fail without freezing and same-day drying. Call 239-356-3708.",
        "h1": "Burst Pipe Water Damage in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Burst pipe in a Fort Myers home", "What to know", 8, 1),
    "h2s": [
        "Pipe Burst in Your Fort Myers Home? Do This Now",
        "Why Pipes Burst in Fort Myers Homes Without Freezing",
        "What Kind of Pipe Is in Your Fort Myers Home?",
        "Signs of a Hidden Burst Pipe in a Fort Myers Home",
        "How Far Burst Pipe Water Spreads in a Fort Myers Slab Home",
        "Supply Line vs Drain Line Leaks in Fort Myers Homes",
        "Who Does What After a Burst Pipe in Fort Myers",
        "How Burst Pipe Damage Is Cleaned Up and Dried in Fort Myers",
        "Is Water From a Burst Pipe in Your Fort Myers Home Clean?",
        "Does Insurance Cover a Burst Pipe in Fort Myers?",
        "How to Prevent the Next Burst Pipe in Your Fort Myers Home",
        "Questions About Burst Pipe Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Pipe Burst Right Now in Your Fort Myers Home?",
    ],
    "tables": {
        "What Kind of Pipe Is in Your Fort Myers Home?": [
            {"cols": 4, "rows": 6, "after": 1}],
        "Supply Line vs Drain Line Leaks in Fort Myers Homes": [
            {"cols": 3, "rows": 4, "after": 0}],
        "Who Does What After a Burst Pipe in Fort Myers": [
            {"cols": 2, "rows": 5, "after": 0}],
    },
    "faq": ("Questions About Burst Pipe Water Damage in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 7),
    "final": "Pipe Burst Right Now in Your Fort Myers Home?",
},
{
    "slug": "mobile-home",
    "paste": "mobile-home-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/mobile-home/",
        "title": "Mobile Home Water Damage Fort Myers | Soft Floors & Belly",
        "meta": "Soft floors or water under your mobile home in Fort Myers? How decking, insulation and belly wrap get dried or replaced. Call 239-356-3708, 24/7.",
        "h1": "Mobile Home Water Damage in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Mobile home water damage in Fort Myers", "What to know", 7, 1),
    "h2s": [
        "Water Leaking in Your Fort Myers Mobile Home? Do This First",
        "Why Water Damage Is Different in a Fort Myers Manufactured Home",
        "What Causes Water Damage in Lee County Mobile Homes",
        "Signs of Hidden Water Damage in a Fort Myers Mobile Home",
        "Particle Board, OSB or Plywood Under Your Fort Myers Mobile Home Floor?",
        "How Mobile Home Water Damage Is Dried and Repaired in Fort Myers",
        "Can a Soft Mobile Home Floor in Fort Myers Be Dried Instead of Replaced?",
        "After a Flood: Piers, Tie-Downs and Ducts in Lee County Manufactured Homes",
        "Insurance for Manufactured Homes in Fort Myers",
        "Manufactured-Home Communities in Lee County",
        "How to Protect a Fort Myers Manufactured Home From Water Damage",
        "Questions About Mobile Home Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Water Under or Inside Your Fort Myers Mobile Home Right Now?",
    ],
    "tables": {
        "Why Water Damage Is Different in a Fort Myers Manufactured Home": [
            {"cols": 2, "rows": 6, "after": 1}],
        "What Causes Water Damage in Lee County Mobile Homes": [
            {"cols": 2, "rows": 10, "after": 0}],
        "Particle Board, OSB or Plywood Under Your Fort Myers Mobile Home Floor?": [
            {"cols": 4, "rows": 3, "after": 0}],
    },
    "faq": ("Questions About Mobile Home Water Damage in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Water Under or Inside Your Fort Myers Mobile Home Right Now?",
},
{
    "slug": "slab-leak",
    "paste": "slab-leak-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/slab-leak/",
        "title": "Slab Leak Water Damage Fort Myers & Cape Coral | 24/7",
        "meta": "Warm floor, high water bill or wet baseboards in Fort Myers? How slab leaks spread and how slabs, floors and walls get dried. Call 239-356-3708.",
        "h1": "Slab Leak Water Damage in Fort Myers and Cape Coral",
        "schema_type": "Service",
    },
    "details": ("Slab leak in a Fort Myers home", "What to know", 8, 1),
    "h2s": [
        "Think You Have a Slab Leak in Your Fort Myers Home? Do This First",
        "Signs of a Slab Leak in a Fort Myers Home",
        "Why Slab Leaks Happen in Fort Myers and Lee County Homes",
        "How Fort Myers Plumbers Find a Slab Leak",
        "Spot Repair, Reroute or Repipe: Slab Leak Repair Options in Fort Myers",
        "What a Slab Leak Does to a Fort Myers Home",
        "How Slab Leak Water Damage Is Dried in Fort Myers",
        "When Can New Flooring Go Down on a Fort Myers Slab?",
        "Is Slab Leak Water in a Fort Myers Home Clean?",
        "Does Insurance Cover a Slab Leak for Fort Myers Homeowners?",
        "Slab Leaks in Cape Coral, Fort Myers and Lehigh Acres",
        "How to Lower the Risk of Another Slab Leak in Your Fort Myers Home",
        "Questions About Slab Leak Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Warm Floor, Wet Baseboards or a Spinning Meter in Your Fort Myers Home?",
    ],
    "tables": {
        "How Fort Myers Plumbers Find a Slab Leak": [
            {"cols": 2, "rows": 4, "after": 0}],
        "Spot Repair, Reroute or Repipe: Slab Leak Repair Options in Fort Myers": [
            {"cols": 4, "rows": 3, "after": 0}],
        "What a Slab Leak Does to a Fort Myers Home": [
            {"cols": 2, "rows": 7, "after": 0}],
    },
    "faq": ("Questions About Slab Leak Water Damage in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Warm Floor, Wet Baseboards or a Spinning Meter in Your Fort Myers Home?",
},
{
    "slug": "flood-cleanup",
    "paste": "flood-cleanup-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/flood-cleanup/",
        "title": "Flood & Storm Surge Cleanup Fort Myers, FL | 24/7 Help",
        "meta": "Floodwater in your Fort Myers home? Safety first, muck-out, flood cuts, drying and flood insurance basics for Lee County. Call 239-356-3708, 24/7.",
        "h1": "Flood and Storm Surge Cleanup in Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Flood cleanup in a Fort Myers home", "What to know", 7, 1),
    "h2s": [
        "Before You Go Back Into a Flooded Fort Myers Home",
        "Why Floodwater Cleanup in Fort Myers Is Different From a Leak",
        "Saltwater Storm Surge in Fort Myers Homes",
        "How Flood Cleanup Works in a Fort Myers Home, Step by Step",
        "2-Foot vs 4-Foot Flood Cuts in Fort Myers Homes",
        "What to Keep and What to Throw Out After a Lee County Flood",
        "Where Flooding Hits Hardest in Lee County",
        "Septic Systems and Wells After a Lee County Flood",
        "Storm Water That Came In From Above in Fort Myers Homes",
        "Flood Insurance Basics for Fort Myers Homeowners",
        "Rebuilding After a Fort Myers Flood: Permits and the 50% Rule",
        "Renting Out or Selling a Fort Myers Home That Has Flooded",
        "Getting a Fort Myers Home Ready Before the Next Storm",
        "Questions About Flood Cleanup in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Floodwater in Your Fort Myers Home?",
    ],
    "tables": {
        "2-Foot vs 4-Foot Flood Cuts in Fort Myers Homes": [
            {"cols": 2, "rows": 3, "after": 0}],
        "What to Keep and What to Throw Out After a Lee County Flood": [
            {"cols": 2, "rows": 8, "after": 0}],
    },
    "faq": ("Questions About Flood Cleanup in Fort Myers", 11),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Floodwater in Your Fort Myers Home?",
},
{
    "slug": "cape-coral",
    "paste": "cape-coral-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/cape-coral/",
        "title": "Water Damage Restoration Cape Coral, FL 33904 | 24/7 Help",
        "meta": "Water damage in your Cape Coral home? Slab leaks, cast iron drains, AC leaks and canal flooding in 33904 to 33993. Call 239-356-3708, answered 24/7.",
        "h1": "Water Damage Restoration in Cape Coral, FL",
        "schema_type": "Service",
    },
    "details": ("Cape Coral water damage", "What to know", 7, 1),
    "h2s": [
        "Water Damage in Your Cape Coral Home Right Now? Do This First",
        "What Makes Water Damage Different in Cape Coral Homes",
        "Cape Coral's Water System and What It Means for Leaks",
        "Most Common Water Damage Problems in Cape Coral",
        "Cape Coral Neighborhoods and ZIP Codes",
        "How Water Damage Restoration Works in a Cape Coral Home",
        "Older Cape Coral Homes: Cast Iron and Copper",
        "Canal-Front Cape Coral Homes and Flooding",
        "Cape Coral Water Damage Through the Year",
        "Insurance for Cape Coral Water Damage",
        "What to Have Ready When You Call About Cape Coral Water Damage",
        "Questions About Water Damage in Cape Coral",
        "Related Water Damage Help in Cape Coral and Lee County",
        "Water Damage in Your Cape Coral Home?",
    ],
    "tables": {
        "Most Common Water Damage Problems in Cape Coral": [
            {"cols": 3, "rows": 7, "after": 0}],
        "Cape Coral Water Damage Through the Year": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Damage in Cape Coral", 10),
    "related": ("Related Water Damage Help in Cape Coral and Lee County", 6),
    "final": "Water Damage in Your Cape Coral Home?",
},
{
    "slug": "lehigh-acres",
    "paste": "lehigh-acres-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/lehigh-acres/",
        "title": "Water Damage Restoration Lehigh Acres, FL 33971 | 24/7",
        "meta": "Water in your Lehigh Acres home? AC leaks, well and pressure tank leaks, burst lines and street flooding in 33936 to 33976. Call 239-356-3708, 24/7.",
        "h1": "Water Damage Restoration in Lehigh Acres, FL",
        "schema_type": "Service",
    },
    "details": ("Lehigh Acres water damage", "What to know", 7, 1),
    "h2s": [
        "Water Damage in Your Lehigh Acres Home Right Now? Do This First",
        "What Makes Water Damage Different in Lehigh Acres Homes",
        "Wells, Septic and City Utilities in Lehigh Acres",
        "Most Common Water Damage Problems in Lehigh Acres",
        "Lehigh Acres ZIP Codes",
        "Storm and Street Flooding in Lehigh Acres",
        "Lehigh Acres Rental Homes: Landlords and Tenants",
        "How Water Damage Restoration Works in a Lehigh Acres Home",
        "Lehigh Acres Water Damage Through the Year",
        "Insurance for Lehigh Acres Water Damage",
        "Questions About Water Damage in Lehigh Acres",
        "Related Water Damage Help in Lehigh Acres and Lee County",
        "Water Damage in Your Lehigh Acres Home?",
    ],
    "tables": {
        "Wells, Septic and City Utilities in Lehigh Acres": [
            {"cols": 3, "rows": 5, "after": 1}],
        "Most Common Water Damage Problems in Lehigh Acres": [
            {"cols": 3, "rows": 7, "after": 0}],
        "Lehigh Acres Water Damage Through the Year": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Damage in Lehigh Acres", 10),
    "related": ("Related Water Damage Help in Lehigh Acres and Lee County", 6),
    "final": "Water Damage in Your Lehigh Acres Home?",
},
{
    "slug": "areas",
    "paste": "areas-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/areas/",
        "title": "Water Damage Service Areas in Lee County, FL | 24/7",
        "meta": "24/7 water damage help across Lee County: Fort Myers, Cape Coral, Lehigh Acres, North Fort Myers, the islands, Estero and Bonita Springs. 239-356-3708.",
        "h1": "Water Damage Help Across Lee County, FL",
        "schema_type": "Service",
    },
    "details": None,
    "intro_tables": [
        {"pre": 1, "h3": "Lee County Service Areas and ZIP Codes", "cols": 3, "rows": 9},
    ],
    "h2s": [
        "Who Handles Permits and the 50% Rule in Each Part of Lee County",
        "Water Damage Problems Across Lee County",
        "What to Do First Anywhere in Lee County",
        "What You Can Expect Anywhere in Lee County",
        "Questions About Water Damage Help Across Lee County",
        "Water Damage Anywhere in Lee County?",
    ],
    "tables": {
        "Who Handles Permits and the 50% Rule in Each Part of Lee County": [
            {"cols": 2, "rows": 7, "after": 1}],
        "Water Damage Problems Across Lee County": [
            {"cols": 2, "rows": 8, "after": 0}],
    },
    "faq": ("Questions About Water Damage Help Across Lee County", 9),
    "related": None,
    "final": "Water Damage Anywhere in Lee County?",
},
{
    "slug": "water-heater-leak",
    "paste": "water-heater-leak-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/water-heater-leak/",
        "title": "Water Heater Leak Cleanup Fort Myers | 24/7 Emergency",
        "meta": "Water heater leaking in your Fort Myers garage, closet or attic? Shut-off steps, why tanks fail and how floors and walls get dried. Call 239-356-3708.",
        "h1": "Emergency Water Heater Leak Cleanup in Fort Myers",
        "schema_type": "Service",
    },
    "details": ("Water heater leak in a Fort Myers home", "What to know", 8, 1),
    "h2s": [
        "Water Heater Leaking in Your Fort Myers Home? Do This First",
        "Where Is Your Fort Myers Water Heater Leaking From?",
        "Tank, Tankless or Heat Pump: How Each Fort Myers Water Heater Leaks",
        "Where Water Heaters Sit in Lee County Homes, and Where the Water Goes",
        "What Florida's Plumbing Code Expects Around a Fort Myers Water Heater",
        "How Water Heater Leak Cleanup Works in a Fort Myers Home",
        "Is Water Heater Water in a Fort Myers Home Clean?",
        "Slow Leak or Sudden Burst in a Fort Myers Water Heater",
        "Warning Signs Before a Fort Myers Water Heater Fails",
        "How to Lower the Risk of a Water Heater Flood in Your Fort Myers Home",
        "Does Insurance Cover Water Heater Leak Damage in Fort Myers?",
        "Questions About Water Heater Leaks in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Water Heater Leaking in Your Fort Myers Home Right Now?",
    ],
    "tables": {
        "Where Is Your Fort Myers Water Heater Leaking From?": [
            {"cols": 2, "rows": 6, "after": 0}],
        "Tank, Tankless or Heat Pump: How Each Fort Myers Water Heater Leaks": [
            {"cols": 3, "rows": 3, "after": 0}],
        "Slow Leak or Sudden Burst in a Fort Myers Water Heater": [
            {"cols": 3, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Heater Leaks in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Water Heater Leaking in Your Fort Myers Home Right Now?",
},
{
    "slug": "appliance-leak",
    "paste": "appliance-leak-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/appliance-leak/",
        "title": "Appliance Leak Water Damage Fort Myers | Washer & Fridge",
        "meta": "Washer overflow, dishwasher leak or ice maker line in Fort Myers? First steps and how hidden water under cabinets and floors is dried. 239-356-3708.",
        "h1": "Appliance Leak Water Damage in Fort Myers",
        "schema_type": "Service",
    },
    "details": ("Appliance leak in a Fort Myers home", "What to know", 8, 1),
    "h2s": [
        "Appliance Leaking in Your Fort Myers Home? Do This First",
        "Which Appliances Leak Most in Fort Myers Homes?",
        "Where Laundry Rooms Sit in Lee County Homes, and Where the Water Goes",
        "Why Appliance Leaks Do More Damage Than They Look in Fort Myers",
        "Is Appliance Water in a Fort Myers Home Clean?",
        "How Appliance Leak Cleanup Works in a Fort Myers Home",
        "Floors After an Appliance Leak in Fort Myers",
        "Appliance Leaks in Fort Myers Condos",
        "How to Prevent the Next Appliance Leak in Your Fort Myers Home",
        "Does Insurance Cover Appliance Leak Damage in Fort Myers?",
        "Questions About Appliance Leaks in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Appliance Leaking in Your Fort Myers Home Right Now?",
    ],
    "tables": {
        "Which Appliances Leak Most in Fort Myers Homes?": [
            {"cols": 3, "rows": 7, "after": 0}],
        "Is Appliance Water in a Fort Myers Home Clean?": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Appliance Leaks in Fort Myers", 11),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Appliance Leaking in Your Fort Myers Home Right Now?",
},
{
    "slug": "floors",
    "paste": "floors-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/floors/",
        "title": "Water Damaged Floors Fort Myers | Tile, LVP, Wood & Carpet",
        "meta": "Vinyl plank lifting, hollow tile or cupped wood after a leak? What can be dried, what comes up and how slab floors dry in Fort Myers. 239-356-3708.",
        "h1": "Water Damaged Floors in Fort Myers Homes",
        "schema_type": "Service",
    },
    "details": ("Water damaged floor in a Fort Myers home", "What to know", 8, 1),
    "h2s": [
        "Water on Your Fort Myers Floor Right Now? Do This First",
        "Can My Floor Be Saved After a Fort Myers Leak?",
        "Why Fort Myers Slab Floors Trap Water",
        "Signs of Water Under Your Floor in a Fort Myers Home",
        "How Water-Damaged Floors Are Dried in Fort Myers Homes",
        "Tile and Terrazzo Floors After a Fort Myers Leak",
        "Is It Water or Heat? Tile Tenting in Fort Myers Homes",
        "Vinyl Plank and Laminate After a Fort Myers Leak",
        "Wood Floors After a Fort Myers Leak",
        "Carpet After a Fort Myers Leak",
        "Floors in Fort Myers and Lee County Condos",
        "Older Floors and Asbestos in Lee County Homes",
        "Insurance and Continuous Flooring in Fort Myers",
        "LVP vs Tile vs Wood in Fort Myers Slab Homes",
        "Questions About Water-Damaged Floors in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Wet Floors in Your Fort Myers Home?",
    ],
    "tables": {
        "Can My Floor Be Saved After a Fort Myers Leak?": [
            {"cols": 3, "rows": 8, "after": 0}],
    },
    "faq": ("Questions About Water-Damaged Floors in Fort Myers", 9),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Wet Floors in Your Fort Myers Home?",
},
{
    "slug": "cabinets",
    "paste": "cabinets-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/cabinets/",
        "title": "Water Damaged Kitchen Cabinets Fort Myers | Dry or Replace",
        "meta": "Swollen cabinet bottoms or a musty sink base in Fort Myers? How cabinets dry in place, when particle board is replaced and countertops saved. 239-356-3708.",
        "h1": "Water Damaged Kitchen Cabinets in Fort Myers",
        "schema_type": "Service",
    },
    "details": ("Water damaged cabinets in a Fort Myers home", "What to know", 8, 1),
    "h2s": [
        "Water Under Your Fort Myers Cabinets Right Now? Do This First",
        "Where Cabinet Leaks Come From in Fort Myers Homes",
        "Can My Fort Myers Cabinets Be Saved?",
        "Why Water Hides Under Fort Myers Cabinets",
        "How Water-Damaged Cabinets Are Dried in Fort Myers Homes",
        "Does the Floor Run Under Your Fort Myers Cabinets?",
        "When Do Countertops Have to Come Off in Fort Myers Kitchens?",
        "Signs of Hidden Water Damage in Fort Myers Cabinets",
        "Bathroom Vanities After a Fort Myers Leak",
        "Cabinets in Fort Myers and Lee County Condos",
        "How to Prevent Cabinet Water Damage in Your Fort Myers Home",
        "Does Insurance Cover Water-Damaged Cabinets in Fort Myers?",
        "Questions About Water-Damaged Cabinets in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Water Under Your Fort Myers Cabinets?",
    ],
    "tables": {
        "Where Cabinet Leaks Come From in Fort Myers Homes": [
            {"cols": 2, "rows": 8, "after": 0}],
        "Can My Fort Myers Cabinets Be Saved?": [
            {"cols": 2, "rows": 6, "after": 0}],
    },
    "faq": ("Questions About Water-Damaged Cabinets in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Water Under Your Fort Myers Cabinets?",
},
{
    "slug": "commercial",
    "paste": "commercial-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/commercial/",
        "title": "Commercial Water Damage Restoration Fort Myers | 24/7",
        "meta": "Water damage at a Fort Myers office, restaurant, store or rental? Drying planned around your hours, records for owners and insurers. 239-356-3708.",
        "h1": "Commercial Water Damage Restoration in Fort Myers",
        "schema_type": "Service",
    },
    "details": ("Commercial water damage in Fort Myers", "What to know", 8, 1),
    "h2s": [
        "Water Damage at Your Fort Myers Business Right Now? Do This First",
        "Which Lee County Businesses and Properties Get Water Damage?",
        "How Commercial Water Damage Restoration Works in Fort Myers",
        "Keeping Your Fort Myers Business Open During Drying",
        "Restaurants and Food Service in Lee County",
        "Asbestos Rules Before Tear-Out in Fort Myers Commercial Buildings",
        "Ceiling Tiles and Drop Ceilings in Fort Myers Offices and Stores",
        "Fire Sprinkler Water Damage in Lee County Buildings",
        "Storm and Flood Damage to Fort Myers Commercial Property",
        "Landlords, Tenants and Property Managers in Lee County",
        "Condo and HOA Buildings in Lee County",
        "Vacation Rentals and Short-Term Rentals in Fort Myers",
        "How to Document a Commercial Water Loss in Fort Myers",
        "What Causes Commercial Water Damage in Lee County?",
        "Insurance for Commercial Water Damage in Fort Myers",
        "Questions About Commercial Water Damage in Fort Myers",
        "Related Water Damage Help in Fort Myers",
        "Water Damage at Your Fort Myers Business?",
    ],
    "tables": {
        "Which Lee County Businesses and Properties Get Water Damage?": [
            {"cols": 2, "rows": 7, "after": 0}],
    },
    "faq": ("Questions About Commercial Water Damage in Fort Myers", 10),
    "related": ("Related Water Damage Help in Fort Myers", 6),
    "final": "Water Damage at Your Fort Myers Business?",
},
{
    "slug": "north-fort-myers",
    "paste": "north-fort-myers-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/north-fort-myers/",
        "title": "Water Damage Restoration North Fort Myers, FL 33903 | 24/7",
        "meta": "24/7 water damage help in North Fort Myers 33903 and 33917: manufactured homes, wells and septic, water heater leaks and river flooding. 239-356-3708.",
        "h1": "Water Damage Restoration in North Fort Myers, FL",
        "schema_type": "Service",
    },
    "details": ("Water damage in North Fort Myers", "What to know", 7, 1),
    "h2s": [
        "Water Damage in North Fort Myers Right Now? Do This First",
        "What Makes Water Damage Different in North Fort Myers?",
        "Common Water Damage Problems in North Fort Myers",
        "North Fort Myers ZIP Codes and Neighborhoods",
        "Who Supplies Your Water in North Fort Myers?",
        "Manufactured-Home Communities in North Fort Myers: Who Fixes What?",
        "Manufactured Homes in North Fort Myers: Where Does the Water Go?",
        "Flooding Along the Caloosahatchee in North Fort Myers",
        "Seasonal and 55+ Communities in North Fort Myers",
        "How Water Damage Restoration Works in North Fort Myers Homes",
        "North Fort Myers Water Damage Through the Year",
        "Permits and the 50% Rule in North Fort Myers",
        "Insurance for North Fort Myers Water Damage",
        "Questions About Water Damage in North Fort Myers",
        "Related Water Damage Help in North Fort Myers",
        "Water Damage in Your North Fort Myers Home?",
    ],
    "tables": {
        "Common Water Damage Problems in North Fort Myers": [
            {"cols": 3, "rows": 7, "after": 0}],
        "North Fort Myers Water Damage Through the Year": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Damage in North Fort Myers", 7),
    "related": ("Related Water Damage Help in North Fort Myers", 6),
    "final": "Water Damage in Your North Fort Myers Home?",
},
{
    "slug": "fort-myers-beach",
    "paste": "fort-myers-beach-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/fort-myers-beach/",
        "title": "Water Damage Restoration Fort Myers Beach, FL 33931 | 24/7",
        "meta": "24/7 water damage help on Fort Myers Beach 33931: storm surge, enclosures under elevated homes, condo and vacation rental leaks. 239-356-3708.",
        "h1": "Water Damage Restoration on Fort Myers Beach, FL",
        "schema_type": "Service",
    },
    "details": ("Water damage on Fort Myers Beach", "What to know", 7, 1),
    "h2s": [
        "Water Damage on Fort Myers Beach Right Now? Do This First",
        "What Makes Water Damage Different on Fort Myers Beach?",
        "Common Water Damage Problems on Fort Myers Beach",
        "Fort Myers Beach ZIP Code and Where the Town Ends",
        "Who Supplies Water and Sewer on Fort Myers Beach?",
        "The 50% Rule on Fort Myers Beach",
        "Ground-Level Enclosures Under Elevated Fort Myers Beach Homes",
        "Condos on Fort Myers Beach",
        "Vacation Rental Water Damage on Fort Myers Beach",
        "After a Storm: Getting Back to Fort Myers Beach",
        "How Water Damage Restoration Works on Fort Myers Beach",
        "Fort Myers Beach Water Damage Through the Year",
        "Insurance for Fort Myers Beach Water Damage",
        "Questions About Water Damage on Fort Myers Beach",
        "Related Water Damage Help on Fort Myers Beach",
        "Water Damage on Fort Myers Beach?",
    ],
    "tables": {
        "Common Water Damage Problems on Fort Myers Beach": [
            {"cols": 3, "rows": 6, "after": 0}],
        "Fort Myers Beach Water Damage Through the Year": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Damage on Fort Myers Beach", 9),
    "related": ("Related Water Damage Help on Fort Myers Beach", 6),
    "final": "Water Damage on Fort Myers Beach?",
},
{
    "slug": "estero",
    "paste": "estero-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/estero/",
        "title": "Water Damage Restoration Estero, FL 33928 | 24/7 Condo Help",
        "meta": "24/7 water damage help in Estero 33928: condo and coach home leaks, AC closet overflows, Estero River flooding and seasonal homes. 239-356-3708.",
        "h1": "Water Damage Restoration in Estero, FL",
        "schema_type": "Service",
    },
    "details": ("Water damage in Estero", "What to know", 7, 1),
    "h2s": [
        "Water Damage in Estero Right Now? Do This First",
        "What Makes Water Damage Different in Estero?",
        "Common Water Damage Problems in Estero",
        "Estero ZIP Code and Communities",
        "Who Supplies Water and Sewer in Estero?",
        "Condo or HOA? Why It Matters for Estero Coach Homes and Villas",
        "Condo Leaks in Estero: Who Pays?",
        "Coach Homes, Villas and Shared Walls in Estero",
        "Returning to Estero for the Season",
        "Preventing Summer Damage in Estero Seasonal Homes",
        "Estero River Flooding",
        "Permits and the 50% Rule in Estero",
        "How Water Damage Restoration Works in Estero Homes",
        "Estero Water Damage Through the Year",
        "Insurance for Estero Water Damage",
        "Questions About Water Damage in Estero",
        "Related Water Damage Help in Estero",
        "Water Damage in Your Estero Home?",
    ],
    "tables": {
        "Common Water Damage Problems in Estero": [
            {"cols": 3, "rows": 6, "after": 0}],
        "Estero Water Damage Through the Year": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Damage in Estero", 7),
    "related": ("Related Water Damage Help in Estero", 6),
    "final": "Water Damage in Your Estero Home?",
},
{
    "slug": "bonita-springs",
    "paste": "bonita-springs-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/bonita-springs/",
        "title": "Water Damage Restoration Bonita Springs, FL 34135 | 24/7",
        "meta": "24/7 water damage help in Bonita Springs 34134 and 34135: Imperial River flooding, condo leaks near Bonita Beach and seasonal homes. 239-356-3708.",
        "h1": "Water Damage Restoration in Bonita Springs, FL",
        "schema_type": "Service",
    },
    "details": ("Water damage in Bonita Springs", "What to know", 7, 1),
    "h2s": [
        "Water Damage in Bonita Springs Right Now? Do This First",
        "What Makes Water Damage Different in Bonita Springs?",
        "Common Water Damage Problems in Bonita Springs",
        "Bonita Springs ZIP Codes and Neighborhoods",
        "Who Supplies Water and Sewer in Bonita Springs?",
        "Imperial River Flooding in Bonita Springs: What Should I Know?",
        "What to Keep and Throw Out After Flooding in Bonita Springs",
        "Coastal Condos Near Bonita Beach",
        "Seasonal Homes in Bonita Springs",
        "Permits and the 50% Rule in Bonita Springs",
        "How Water Damage Restoration Works in Bonita Springs Homes",
        "Bonita Springs Water Damage Through the Year",
        "Insurance for Bonita Springs Water Damage",
        "Questions About Water Damage in Bonita Springs",
        "Related Water Damage Help in Bonita Springs",
        "Water Damage in Your Bonita Springs Home?",
    ],
    "tables": {
        "Common Water Damage Problems in Bonita Springs": [
            {"cols": 3, "rows": 6, "after": 0}],
        "What to Keep and Throw Out After Flooding in Bonita Springs": [
            {"cols": 2, "rows": 6, "after": 0}],
        "Bonita Springs Water Damage Through the Year": [
            {"cols": 2, "rows": 4, "after": 0}],
    },
    "faq": ("Questions About Water Damage in Bonita Springs", 8),
    "related": ("Related Water Damage Help in Bonita Springs", 6),
    "final": "Water Damage in Your Bonita Springs Home?",
},
{
    "slug": "how-it-works",
    "paste": "how-it-works-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/how-it-works/",
        "title": "Water Damage Restoration Process Fort Myers | Step by Step",
        "meta": "What happens after you call about water damage in Fort Myers: the questions, inspection, written scope, drying, final readings and your paperwork.",
        "h1": "How Water Damage Restoration Works in Fort Myers",
        "schema_type": "Article",
    },
    "details": None,
    "intro_tables": [
        {"pre": 1, "cols": 2, "rows": 7},
    ],
    "rich_steps": True,
    "h2s": [
        "Water Damage Restoration in Fort Myers, Step by Step",
        "Why Fort Myers Humidity Changes the Drying Plan",
        "What Changes for Fort Myers Condos, Rentals and Businesses",
        "What You Won't Be Asked to Do in Your Fort Myers Home",
        "Mitigation, Restoration, Remediation: Words You'll Hear From Fort Myers Adjusters",
        "What the Water Category Means for Your Fort Myers Job",
        "What the Drying Equipment Does in a Fort Myers Home",
        "How Long Each Stage Takes in Fort Myers",
        "Insurance Paperwork for Fort Myers Water Damage Claims",
        "Mold After Water Damage in Fort Myers Homes",
        "Questions About the Water Damage Restoration Process in Fort Myers",
        "Related Water Damage Guides for Fort Myers",
        "Water Damage in Your Fort Myers Home Right Now?",
    ],
    "tables": {
        "What the Water Category Means for Your Fort Myers Job": [
            {"cols": 3, "rows": 3, "after": 1}],
        "How Long Each Stage Takes in Fort Myers": [
            {"cols": 2, "rows": 5, "after": 0}],
    },
    "faq": ("Questions About the Water Damage Restoration Process in Fort Myers", 8),
    "related": ("Related Water Damage Guides for Fort Myers", 6),
    "final": "Water Damage in Your Fort Myers Home Right Now?",
},
{
    "slug": "contact",
    "paste": "contact-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/contact/",
        "title": "Contact Fort Myers Water Damage Restoration Pros | 24/7",
        "meta": "Call 239-356-3708, answered 24/7, for water damage help in Fort Myers and across Lee County. What to have ready and what happens after you call.",
        "h1": "Contact Fort Myers Water Damage Restoration Pros",
        "schema_type": "ContactPage",
    },
    "details": None,
    "h2s": [
        "Contact Details for Fort Myers Water Damage Restoration Pros",
        "Before You Call: If Water Is Still Coming Into Your Fort Myers Home",
        "What to Have Ready When You Call About Fort Myers Water Damage",
        "Calling About a Lee County Home You're Not At",
        "What Happens After You Call in Fort Myers",
        "Areas Covered Across Lee County",
        "Questions About Contacting Fort Myers Water Damage Restoration Pros",
        "Water Damage in Your Fort Myers Home Right Now?",
    ],
    "tables": {
        "Contact Details for Fort Myers Water Damage Restoration Pros": [
            {"cols": 2, "rows": 5, "after": 0}],
        "Areas Covered Across Lee County": [
            {"cols": 3, "rows": 7, "after": 0}],
    },
    "faq": ("Questions About Contacting Fort Myers Water Damage Restoration Pros", 5),
    "related": None,
    "final": "Water Damage in Your Fort Myers Home Right Now?",
},
{
    "slug": "about",
    "paste": "about-paste-2026-11-19.md",
    "expect": {
        "url": "https://fortmyerswaterdamagerestoration.us/about/",
        "title": "About Fort Myers Water Damage Restoration Pros | Lee County",
        "meta": "Who Fort Myers Water Damage Restoration Pros is, how the work is done across Lee County, and how the water damage guides on this site are written.",
        "h1": "About Fort Myers Water Damage Restoration Pros",
        "schema_type": "AboutPage",
    },
    "details": None,
    "h2s": [
        "What We Do in Fort Myers and Lee County",
        "What We Leave to Other Fort Myers Trades",
        "Areas We Serve: Water Damage Restoration Across Lee County",
        "How We Work in Fort Myers Homes",
        "How the Guides on This Site Are Written for Lee County Homeowners",
        "Questions About Fort Myers Water Damage Restoration Pros",
        "Water Damage in Your Fort Myers Home Right Now?",
    ],
    "faq": ("Questions About Fort Myers Water Damage Restoration Pros", 4),
    "related": None,
    "final": "Water Damage in Your Fort Myers Home Right Now?",
},
]


def main():
    want = sys.argv[1:]
    for spec in SPECS:
        if want and spec["slug"] not in want:
            continue
        print(f"=== {spec['slug']} ===")
        Parser(spec).run()
        print()


if __name__ == "__main__":
    main()
