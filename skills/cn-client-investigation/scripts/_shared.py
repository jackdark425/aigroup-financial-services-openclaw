"""Shared helpers for cn-client-investigation scanners.

Keep this module small and import-light. Scripts in this folder (e.g.
provenance_verify.py, style_scan.py) import from here to avoid
duplicating commonly-used scanning primitives.
"""
from __future__ import annotations

import collections
import re


def find_precision_drift(
    text: str, hard_number_re: re.Pattern[str]
) -> list[str]:
    """Detect same-unit multi-precision writes across the doc.

    Group all hard numbers in ``text`` by ``(round(value), unit)``. When a
    group holds ≥ 2 distinct textual forms (e.g. ``1.34 元/股`` / ``1.340
    元/股`` / ``1.3 元/股``), emit one drift warning per group.

    ``hard_number_re`` is injected rather than imported so each scanner
    can keep its own unit vocabulary (``provenance_verify.HARD_NUMBER``
    and ``style_scan.HARD_NUMBER`` cover different unit sets).

    Period-distinct values (e.g. ``56 亿元`` vs ``83 亿元`` for different
    years) round to different integers and never collide.
    """
    groups: dict[tuple[int, str], set[str]] = collections.defaultdict(set)
    for line in text.splitlines():
        for m in hard_number_re.finditer(line):
            num_str, unit = m.group(1), m.group(2)
            try:
                n = float(num_str.replace(",", ""))
            except ValueError:
                continue
            groups[(int(round(n)), unit)].add(f"{num_str}{unit}")
    warnings: list[str] = []
    for (int_part, unit), values in groups.items():
        if len(values) < 2:
            continue
        warnings.append(
            f"precision drift near {int_part}{unit}: {', '.join(sorted(values))}"
        )
    return warnings
