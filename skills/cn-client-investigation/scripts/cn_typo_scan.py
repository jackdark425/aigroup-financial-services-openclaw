#!/usr/bin/env python3
"""
cn_typo_scan.py — scan a text-extracted PPTX / MD for the character-level typo
patterns observed in MiniMax-M2.7 `\\uXXXX` escape mis-encoding.

Usage:
    python -m markitdown deck.pptx > /tmp/deck.txt
    python3 cn_typo_scan.py /tmp/deck.txt
    # Exit 0 = clean; exit 1 = hits found (see stderr for details).

Exit code is what CI / compile.js can gate on.
"""
from __future__ import annotations
import sys
import re
import pathlib

# Red-flag dyads and phrases observed in 2026-04-18 runs.
# These are character combinations that should never appear in banker prose and
# strongly suggest a `\\uXXXX` escape went wrong. Extend this list as new typo
# patterns are encountered.
RED_FLAG_DYADS = [
    # Cambricon case (寒武纪 → 宽厭谛79 observed)
    ("宽厭", "likely meant 寒武 (Cambricon)"),
    ("谛79", "likely meant 纪 (third char of 寒武纪)"),
    ("谛\\d", "Chinese char 谛 followed by digit — suspected escape drift"),
    # Finance line-item case (净利 / 财务 / 亏损 → 洁利 / 贜务 / 贜损 observed)
    ("洁利", "likely meant 净利 (net profit)"),
    ("贜务", "likely meant 财务 (financial)"),
    ("贜损", "likely meant 亏损 (loss)"),
    ("贜", "rare character 贜; in banker prose almost always a typo"),
    # Market case (核心 / 加速 → 校虚 observed)
    ("校虚", "likely meant 核心 or 加速 (market adj)"),
    # Catalyst case (催化 → 筹划 observed when the context is catalysts not planning)
    # Note: 筹划 is a real word (to plan) — only flag if context suggests catalyst-list
    ("催化济", "probably intended 催化剂 — last char shifted"),
]

# Generic patterns that signal broken escape sequences
# 1. Chinese ideograph directly followed by a digit is extremely rare in
#    banker prose (numbers are typically surrounded by digits/units), and is
#    the classic symptom of a `\\uXXXX` truncation where the closing digits
#    of the escape got parsed as literal text.
RE_HANZI_THEN_DIGIT = re.compile(r"[\u4e00-\u9fff][0-9]")

# 2. CJK Compatibility / rare CJK-Extension chars that should not appear in
#    banker deliverables. A simple hit on U+3400-U+4DBF (CJK Extension A) or
#    U+20000+ (Extension B/C/D) is almost always a corruption indicator.
RE_RARE_CJK = re.compile(r"[\u3400-\u4dbf]|[\U00020000-\U0002ffff]")


def scan(text: str) -> list[tuple[int, str, str]]:
    """Return list of (line_no, matched_snippet, reason)."""
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for dyad, reason in RED_FLAG_DYADS:
            if re.search(dyad, line):
                hits.append((lineno, line.strip()[:120], f"red-flag dyad '{dyad}': {reason}"))
        for m in RE_HANZI_THEN_DIGIT.finditer(line):
            # allow a few benign patterns: 年份数字, 百分比, unit-attached numbers
            # e.g. "2024年" is hanzi-after-digit, not digit-after-hanzi. the
            # pattern only fires hanzi→digit, which is the suspicious direction.
            ctx = line[max(0, m.start() - 5):m.end() + 5]
            # whitelist: Chinese sequence + number + unit (e.g. 金额 15亿)
            # skip if the hanzi is a measure/count word
            if m.group(0)[0] in "第共计":
                continue
            hits.append((lineno, ctx.strip()[:120], f"hanzi-then-digit '{m.group(0)}' — escape drift suspect"))
        for m in RE_RARE_CJK.finditer(line):
            hits.append((lineno, line.strip()[:120], f"rare CJK char U+{ord(m.group(0)):04X}"))
    return hits


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: cn_typo_scan.py <text-file>", file=sys.stderr)
        return 2
    p = pathlib.Path(argv[1])
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2
    text = p.read_text(encoding="utf-8", errors="replace")
    hits = scan(text)
    if not hits:
        print(f"OK: cn_typo_scan clean on {p} ({len(text):,} chars)")
        return 0
    print(f"FAIL: {len(hits)} typo red-flag hit(s) in {p}", file=sys.stderr)
    for lineno, snippet, reason in hits[:80]:
        print(f"  L{lineno:>4}: {reason}", file=sys.stderr)
        print(f"         {snippet!r}", file=sys.stderr)
    if len(hits) > 80:
        print(f"  ...and {len(hits) - 80} more hits truncated.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
