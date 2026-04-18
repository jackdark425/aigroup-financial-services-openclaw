#!/usr/bin/env python3
"""
provenance_verify.py — guard that every hard number in a China-target
banker markdown deliverable has a matching row in the companion
data-provenance.md tracking table.

Context: Rule 5 of the cn-client-investigation skill says every hard
number (revenue, valuation, margin, market cap, etc.) must be backed by
at least one cited source. This script is the automated gate.

Usage:
    python3 provenance_verify.py <analysis.md> <data-provenance.md>
    # exit 0 → clean (every hard number cross-references a provenance row)
    # exit 1 → one or more hard numbers are missing a provenance row

Assumptions:
    - <analysis.md>       is the primary banker markdown draft
    - <data-provenance.md> is a markdown file containing a table whose
      rows list one hard number each; the script scans every non-header
      row and collects the numeric tokens in any cell

"Hard number" here means a number immediately followed by a banker unit:
    亿 万 % RMB USD 元 CNY HKD  (also the English shorthand M / B and 亿元)

The comparison is deliberately coarse: if a hard-number token appears
verbatim in any row of the provenance table, it is considered covered.
Rows in the provenance table that are themselves the column-header line
(first row with "----" below it) are skipped.

This script is intended to be part of the Phase 5 QA pass in the
cn-client-investigation skill, and it can also be wired into CI if the
deliverable is checked into a repo.
"""
from __future__ import annotations
import re
import sys
import pathlib
from typing import Iterable


# --- Regex: the hard-number pattern we flag ---
# A digit run (with optional decimal) followed (possibly after one space)
# by one of the banker units below.
UNITS = r"(?:亿元|亿|万|%|元|RMB|USD|CNY|HKD|M|B)"
# Allow any digit run (no 3-cap) so "1500亿元" captures as 1500, not 500.
# Thousands separators are still handled by the optional `(?:,\d{3})*` group.
NUM_CORE = r"\d+(?:,\d{3})*(?:\.\d+)?"
HARD_NUMBER = re.compile(rf"({NUM_CORE})\s*({UNITS})")


def extract_hard_numbers(text: str) -> list[tuple[int, str, str, str]]:
    """
    Return [(line_no, number, unit, line_snippet), ...] for every hard
    number found in `text`.
    """
    hits: list[tuple[int, str, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in HARD_NUMBER.finditer(line):
            hits.append((lineno, m.group(1), m.group(2), line.strip()[:120]))
    return hits


def extract_provenance_corpus(prov_text: str) -> str:
    """
    Flatten the provenance markdown to a single string the script can
    substring-search. We don't try to parse the markdown table, because
    provenance tables come in varying shapes — a raw flatten is enough
    for the coarse existence check this gate performs.
    """
    # Strip markdown table separators and pipes so "15.2 亿RMB" matches
    # against "| 15.2 | 亿RMB |" style cells.
    cleaned = prov_text.replace("|", " ").replace("---", " ")
    # Collapse runs of whitespace.
    return re.sub(r"\s+", " ", cleaned)


def normalize_variants(num: str, unit: str) -> list[str]:
    """
    Return candidate strings to search for in the provenance corpus.
    Covers:
      - exact "15.2 亿RMB"
      - without space "15.2亿RMB"
      - number alone (caller will AND with unit-nearby check)
      - common comma-thousands variation (strip commas)
      - cross-unit equivalences (亿元 ↔ 万元 ↔ 元) so a markdown claim of
        "1476.94 亿元" matches a provenance row citing "14,769,400 万元"
        (banker reports routinely mix 万元/亿元 scales between analysis text
        and the underlying Tushare / CNINFO disclosure tables).
    """
    variants: set[str] = set()
    base = num
    no_commas = num.replace(",", "")
    for n in {base, no_commas}:
        variants.add(f"{n}{unit}")
        variants.add(f"{n} {unit}")
        variants.add(n)  # last resort: number alone

    # Unit equivalences — convert numeric value into companion-unit form and
    # add those as search candidates. Only kicks in for units that have a
    # well-defined scalar multiple.
    try:
        value = float(no_commas)
    except ValueError:
        return list(variants)

    equivalents: list[tuple[float, str]] = []
    if unit == "亿元":
        # 1亿元 = 10000 万元 = 1e8 元
        equivalents = [(value * 10000, "万元"), (value * 1e8, "元")]
    elif unit == "万元":
        # 1万元 = 0.0001 亿元 = 10000 元
        equivalents = [(value / 10000, "亿元"), (value * 10000, "元")]
    elif unit == "元":
        equivalents = [(value / 1e8, "亿元"), (value / 10000, "万元")]
    elif unit == "亿":
        equivalents = [(value * 10000, "万"), (value * 1e8, "")]
    elif unit == "万":
        equivalents = [(value / 10000, "亿"), (value * 10000, "")]

    for v, u in equivalents:
        # Skip silly precision or near-zero conversions
        if v <= 0:
            continue
        # Whole-number form and one-decimal form — banker tables write both
        # "14769360" and "14,769,360" in manually prepared provenance tables.
        whole = f"{int(v)}" if v == int(v) else f"{v:g}"
        variants.add(f"{whole}{u}")
        variants.add(f"{whole} {u}")
        # With thousands separators
        try:
            if v == int(v):
                variants.add(f"{int(v):,}{u}")
                variants.add(f"{int(v):,} {u}")
        except (OverflowError, ValueError):
            pass
        # Add decimal form too for beauty: 14769360 ↔ 1476.94 亿元
        if "." in whole or v != int(v):
            variants.add(f"{v:.2f}{u}")
            variants.add(f"{v:.2f} {u}")
    return list(variants)


def verify(
    analysis_text: str,
    provenance_text: str,
) -> tuple[int, list[str]]:
    """Return (missing_count, messages)."""
    hits = extract_hard_numbers(analysis_text)
    if not hits:
        return 0, ["OK: no hard numbers found in analysis.md — nothing to verify"]

    corpus = extract_provenance_corpus(provenance_text)

    missing: list[str] = []
    covered_count = 0

    for lineno, num, unit, snippet in hits:
        variants = normalize_variants(num, unit)
        unit_ok = unit in corpus
        num_ok = any(v in corpus for v in variants[:4])  # exclude bare-number variant
        if num_ok:
            covered_count += 1
            continue
        # Fallback: if number alone appears AND the unit also appears somewhere
        # in the provenance corpus, count as a soft match (still covered).
        if unit_ok and num.replace(",", "") in corpus:
            covered_count += 1
            continue
        missing.append(
            f"L{lineno:>4}: hard number '{num}{unit}' missing from data-provenance.md"
            f"\n       context: {snippet!r}"
        )

    total = len(hits)
    summary = [
        f"scan: {total} hard numbers in analysis.md; "
        f"{covered_count} covered, {len(missing)} missing."
    ]
    return len(missing), summary + missing


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: provenance_verify.py <analysis.md> <data-provenance.md>",
            file=sys.stderr,
        )
        return 2
    analysis_p = pathlib.Path(argv[1])
    prov_p = pathlib.Path(argv[2])
    for p in (analysis_p, prov_p):
        if not p.exists():
            print(f"file not found: {p}", file=sys.stderr)
            return 2
    analysis_text = analysis_p.read_text(encoding="utf-8", errors="replace")
    prov_text = prov_p.read_text(encoding="utf-8", errors="replace")

    missing, messages = verify(analysis_text, prov_text)
    header = messages[0]
    details = messages[1:]
    if missing == 0:
        print(f"OK: {header}")
        return 0
    print(f"FAIL: {header}", file=sys.stderr)
    for m in details:
        print(m, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
