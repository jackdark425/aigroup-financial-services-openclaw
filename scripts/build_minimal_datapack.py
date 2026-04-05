#!/usr/bin/env python3
"""Stable entrypoint for datapack-builder smoke tests.

This thin wrapper keeps the published repository root consistent with the
datapack-builder skill instructions. It forwards to the actual skill-local
implementation so OpenClaw can call `python scripts/build_minimal_datapack.py`
without needing a `cd && python ...` shell pattern.
"""

from pathlib import Path
import runpy
import sys


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "skills" / "datapack-builder" / "scripts" / "build_minimal_datapack.py"
    if not target.exists():
        raise SystemExit(f"Missing datapack builder script: {target}")

    sys.argv[0] = str(target)
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
