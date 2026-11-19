#!/usr/bin/env python3
"""Parse the 3 legal pastes into site/data/<slug>.php.

Legal pastes differ from content pastes: the header is 'URL: / Meta Title: /
Meta Description: / H1: ' lines (no char counts, no schema, no CTA, no
details card, no FAQ). The body is the intro para + 'H2: ' sections +
bullets + a trailing 'Related pages: ...' link line. Content is verbatim;
word-diff 0 is asserted.

'last_updated' (spec) is chrome, NOT paste content: it renders a
"Last updated: <date>" line at the top of the page body and is excluded
from the word-diff. It is only set when the user supplies the date
(privacy-policy + terms: November 19, 2026, his call 2026-11-19).
Disclaimer carries none — its copy never references one.
Usage: python3 tools/parse_legal.py [slug ...]
Writes: site/data/<slug>.php
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parse_page as pp

BASE = pp.BASE
PAGES_DIR = pp.PAGES_DIR
OUT_DIR = pp.OUT_DIR


def words(s):
    return pp.words(s)


def seg_text(segs):
    return pp.seg_text(segs)


def parse_segments(text, where, links):
    """Same anchor rule as parse_page.Parser.parse_segments."""
    segs = []
    pos = 0
    for m in re.finditer(r"\((/[a-z0-9\-/]*)\)", text):
        href = m.group(1)
        before = text[pos:m.start()]
        cut = 0
        for b in pp.BOUNDARIES:
            j = before.rfind(b)
            if j >= 0:
                cut = max(cut, j + len(b))
        anchor = before[cut:].rstrip()
        pre = before[:cut]
        if pre:
            segs.append({"t": pre})
        if not anchor or len(words(anchor)) > 12:
            raise SystemExit(f"BAD ANCHOR {where}: {anchor!r} before {href}")
        if href not in pp.PLANNED:
            raise SystemExit(f"HREF NOT A PLANNED ROUTE {where}: {href}")
        segs.append({"t": anchor, "href": href})
        links.append((anchor, href))
        pos = m.end()
    if text[pos:]:
        segs.append({"t": text[pos:]})
    return segs


def block_words(b):
    out = []
    t = b["type"]
    if t == "hero-intro":
        out += words(seg_text(b["segs"]))
    elif t == "h2":
        out += words(b["text"])
    elif t == "p":
        out += words(seg_text(b["segs"]))
    elif t == "ul":
        for it in b["items"]:
            out += words(seg_text(it))
    else:
        raise SystemExit(f"unknown block type {t}")
    return out


SPECS = [
    {
        "slug": "privacy-policy",
        "paste": "privacy-policy-paste-2026-11-19.md",
        "expect": {
            "url": "https://fortmyerswaterdamagerestoration.us/privacy-policy/",
            "title": "Privacy Policy | Fort Myers Water Damage Restoration Pros",
            "meta": "How Fort Myers Water Damage Restoration Pros collects, uses and protects the information you share when you call 239-356-3708 or use this website.",
            "h1": "Privacy Policy",
        },
        "last_updated": "November 19, 2026",
        "h2s": [
            "Information you give us",
            "Information collected automatically",
            "Cookies and similar technologies",
            "Phone calls",
            "How we use your information",
            "When we share information",
            "Text messages",
            "How long we keep information",
            "How we protect information",
            "Your choices",
            "Children's privacy",
            "Links to other websites",
            "Changes to this policy",
            "Contact us",
        ],
    },
    {
        "slug": "terms",
        "paste": "terms-paste-2026-11-19.md",
        "expect": {
            "url": "https://fortmyerswaterdamagerestoration.us/terms/",
            "title": "Terms of Use | Fort Myers Water Damage Restoration Pros",
            "meta": "The terms that apply when you use this website or contact Fort Myers Water Damage Restoration Pros about water damage help in Lee County.",
            "h1": "Terms of Use",
        },
        "last_updated": "November 19, 2026",
        "h2s": [
            "What the Site is for",
            "Services are agreed separately",
            "Information on the Site",
            "Acceptable use",
            "Phone calls and messages",
            "Intellectual property",
            "Links to other websites",
            "No warranties",
            "Limitation of liability",
            "Indemnity",
            "Governing law",
            "Changes to these Terms",
            "Contact us",
        ],
    },
    {
        "slug": "disclaimer",
        "paste": "disclaimer-paste-2026-11-19.md",
        "expect": {
            "url": "https://fortmyerswaterdamagerestoration.us/disclaimer/",
            "title": "Disclaimer | Fort Myers Water Damage Restoration Pros",
            "meta": "The limits of the general water damage, cost and insurance information on fortmyerswaterdamagerestoration.us. Read before relying on any page.",
            "h1": "Disclaimer",
        },
        "last_updated": None,
        "h2s": [
            "General information, not professional advice",
            "Not legal or insurance advice",
            "Cost information is not an estimate or quote",
            "Health and safety",
            "Mold",
            "Accuracy and changes",
            "No promise of results",
            "Outside links",
            "Images",
            "Questions",
        ],
    },
]


class LegalParser:
    def __init__(self, spec):
        self.spec = spec
        self.slug = spec["slug"]
        raw = open(os.path.join(PAGES_DIR, spec["paste"])).read()
        assert raw.count("—") + raw.count("–") == 0, "dashes present in paste"
        assert "Schema" not in raw, "legal paste must not carry a schema"
        m = re.search(r"URL: (\S+)\nMeta Title: ([^\n]+)\nMeta Description: ([^\n]+)\n\nH1: ([^\n]+)\n", raw)
        assert m, "legal header (URL/Meta Title/Meta Description/H1) not found"
        self.url, self.title, self.meta, self.h1 = (m.group(1), m.group(2).strip(),
                                                     m.group(3).strip(), m.group(4).strip())
        ex = spec["expect"]
        assert self.url == ex["url"], f"url mismatch: {self.url!r}"
        assert self.title == ex["title"], f"title mismatch: {self.title!r}"
        assert self.meta == ex["meta"], f"meta mismatch: {self.meta!r}"
        assert self.h1 == ex["h1"], f"H1 mismatch: {self.h1!r}"
        self.copy = raw[m.end():].strip()
        self.lines = [ln for ln in self.copy.split("\n") if ln.strip() != ""]
        self.blocks = []
        self.links = []
        print(f"[{self.slug}] title ({len(self.title)}ch): {self.title}")
        print(f"[{self.slug}] meta ({len(self.meta)}ch)")
        print(f"[{self.slug}] H1: {self.h1}")
        print(f"[{self.slug}] schema: none (legal page, no JSON-LD)")
        if spec.get("last_updated"):
            print(f"[{self.slug}] last updated: {spec['last_updated']} (chrome, not paste content)")

    def run(self):
        spec = self.spec
        lines, n = self.lines, len(self.lines)
        i = 0
        # First line is the intro para -> hero-intro.
        intro = parse_segments(lines[0], "intro", self.links)
        self.blocks.append({"type": "hero-intro", "segs": intro})
        i = 1
        h2_idx = 0
        h2s = spec["h2s"]
        while i < n:
            line = lines[i]
            if line.startswith("H2: "):
                h = line[4:]
                assert h2_idx < len(h2s), f"[{self.slug}] extra H2: {h!r}"
                assert h == h2s[h2_idx], \
                    f"[{self.slug}] H2 {h2_idx}: expected {h2s[h2_idx]!r}, got {h!r}"
                h2_idx += 1
                self.blocks.append({"type": "h2", "text": h})
                i += 1
                continue
            if line.startswith("• "):
                items = []
                while i < n and lines[i].startswith("• "):
                    items.append(parse_segments(lines[i][2:], f"bullet L{i}", self.links))
                    i += 1
                self.blocks.append({"type": "ul", "items": items})
                continue
            self.blocks.append({"type": "p", "segs": parse_segments(line, f"para L{i}", self.links)})
            i += 1
        assert h2_idx == len(h2s), \
            f"[{self.slug}] consumed {h2_idx} of {len(h2s)} H2s"
        print(f"[{self.slug}] H2s: {h2_idx}")
        # word-diff: H1 words + block words vs H1 + copy words
        # (copy with 'H2: ' markers and (/slug/) tokens stripped).
        got = words(self.h1)
        for b in self.blocks:
            got += block_words(b)
        visible = re.sub(r"^H2: ", "", self.copy, flags=re.M)
        visible = re.sub(r"\((/[a-z0-9\-/]*)\)", "", visible)
        want = words(self.h1) + words(visible)
        print(f"[{self.slug}] copy words (visible): {len(want) - len(words(self.h1))}; blocks words: {len(got) - len(words(self.h1))}")
        assert got == want, f"[{self.slug}] WORD-DIFF FAILED (got {len(got)} want {len(want)})"
        print(f"[{self.slug}] WORD-DIFF 0 ✓")
        self.emit()

    def emit(self):
        data = {"seo": {"title": self.title, "meta": self.meta, "h1": self.h1,
                        "schema": None},
                "blocks": self.blocks}
        if self.spec.get("last_updated"):
            data = {"seo": data["seo"], "last_updated": self.spec["last_updated"],
                    "blocks": self.blocks}
        out = os.path.join(OUT_DIR, self.slug + ".php")
        php = "<?php\n"
        php += f"// {self.slug} content — parsed verbatim from {self.spec['paste']}\n"
        php += "// by tools/parse_legal.py. Do NOT hand-edit: re-run the parser.\n"
        php += "// Legal page: noindex, out of sitemap/llms, NO JSON-LD schema.\n"
        php += "return " + pp.php_val(data) + ";\n"
        open(out, "w").write(php)
        print(f"[{self.slug}] wrote {out} ({len(php)} bytes)")
        distinct = sorted(set(h for _, h in self.links))
        pending = [h for h in distinct if h not in pp.BUILT]
        print(f"[{self.slug}] links: {len(self.links)} total, {len(distinct)} distinct; "
              f"pending pages linked: {pending}")


def main():
    want = sys.argv[1:]
    for spec in SPECS:
        if want and spec["slug"] not in want:
            continue
        print(f"=== {spec['slug']} ===")
        LegalParser(spec).run()
        print()


if __name__ == "__main__":
    main()
