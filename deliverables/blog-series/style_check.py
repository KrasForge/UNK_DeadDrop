#!/usr/bin/env python3
"""Fact-preservation check for a restyle pass: every number, code span, defanged indicator,
link target and figure in the old post must still be in the new one (repeats in takeaways are fine).
Usage: style_check.py <old.md> <new.md>   exit 1 if anything was lost or a banned pattern appears."""
import re, sys
from collections import Counter
P = {
    "numbers": r"(?<![\w.])\d[\d,.]*\d|(?<![\w.])\d(?![\w])",
    "code": r"`[^`]+`",
    "defanged": r"\b[\w.-]+\[\.\][\w.\[\]-]+",
    "links": r"\]\(([^)]+)\)",
}
def body(t):
    m = re.match(r"---\n.*?\n---\n", t, re.S)
    return t[m.end():] if m else t
a, b = (open(f).read() for f in sys.argv[1:3])
bad = 0
if re.match(r"---\n.*?\n---\n", a, re.S).group(0) != re.match(r"---\n.*?\n---\n", b, re.S).group(0):
    print("  frontmatter changed"); bad = 1
FENCE = r"```.*?```"
fa, fb = (Counter(re.findall(FENCE, body(x), re.S)) for x in (a, b))
if fa - fb: print(f"  lost fenced code blocks: {len(list((fa - fb).elements()))}"); bad = 1
strip = lambda x: re.sub(FENCE, "", body(x), flags=re.S)
for k, p in P.items():
    lost = Counter(re.findall(p, strip(a))) - Counter(re.findall(p, strip(b)))
    if lost: print(f"  lost {k}: {dict(lost)}"[:900]); bad = 1
for pat in ["—", r"\bwe\b", r"\bWe\b", r"\bour\b"]:
    if re.search(pat, re.sub(r"`[^`]+`|\]\([^)]+\)|\"[^\"]*\"", "", body(b))): print(f"  banned: {pat}"); bad = 1
print(f"{sys.argv[2]}: {'OK' if not bad else 'CHECK'}")
sys.exit(bad)
