#!/usr/bin/env python3
"""
Minimal recalc placeholder for standalone .xlsx smoke tests.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not path or not path.exists():
        print(json.dumps({"status": "error", "message": "file not found"}))
        raise SystemExit(1)
    print(json.dumps({"status": "success", "file": str(path)}))


if __name__ == "__main__":
    main()
