"""Shared helpers for cn-client-investigation scanners.

Keep this module small and import-light. Scripts in this folder (e.g.
provenance_verify.py, style_scan.py) import from here to avoid
duplicating commonly-used scanning primitives.
"""
from __future__ import annotations

import collections
import re


_METRIC_CONTEXT_CHARS = 8


def _metric_key(line: str, start: int) -> str:
    """Extract a short CJK-only pre-context window used to disambiguate
    values with the same rounded int + unit but belonging to different
    metrics (e.g. ``毛利率 19.4%`` vs ``净利润同比 -18.97%``).

    Keep only Chinese chars from the preceding ``_METRIC_CONTEXT_CHARS``
    characters; whitespace / punctuation / non-CJK chars usually carry no
    metric-identifier signal and would make the key over-strict.
    """
    window = line[max(0, start - _METRIC_CONTEXT_CHARS):start]
    return "".join(ch for ch in window if "\u4e00" <= ch <= "\u9fff")


def find_precision_drift(
    text: str, hard_number_re: re.Pattern[str]
) -> list[str]:
    """Detect same-metric multi-precision writes across the doc.

    Group hard numbers by ``(pre-context CJK key, round(value), unit)``
    and emit a warning for each group with ≥ 2 distinct textual forms
    (e.g. ``1.34 元/股`` / ``1.340 元/股`` / ``1.3 元/股`` under pre-context
    ``EPS``).

    The CJK pre-context key disambiguates metrics that coincidentally
    share a rounded integer + unit, e.g. ``毛利率 19.4%`` and
    ``净利润同比 -18.97%`` both round to ``(19, %)`` but have distinct
    pre-context (``毛利率`` vs ``净利润同比``), so they no longer collide.
    Fallback: when the pre-context window is empty (number at
    line-start), key falls back to ``""`` — all such numbers still
    collide, which is the behavior we had before the fix.

    ``hard_number_re`` is injected rather than imported so each scanner
    can keep its own unit vocabulary.
    """
    groups: dict[tuple[str, int, str], set[str]] = collections.defaultdict(set)
    for line in text.splitlines():
        for m in hard_number_re.finditer(line):
            num_str, unit = m.group(1), m.group(2)
            try:
                n = float(num_str.replace(",", ""))
            except ValueError:
                continue
            key = (_metric_key(line, m.start()), int(round(n)), unit)
            groups[key].add(f"{num_str}{unit}")
    warnings: list[str] = []
    for (metric, int_part, unit), values in groups.items():
        if len(values) < 2:
            continue
        label = f"{metric} {int_part}{unit}" if metric else f"{int_part}{unit}"
        warnings.append(
            f"precision drift near {label}: {', '.join(sorted(values))}"
        )
    return warnings
