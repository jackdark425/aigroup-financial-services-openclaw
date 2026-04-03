#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


INCLUDE_PATHS = [
    ".claude-plugin",
    ".mcp.json",
    "skills",
    "commands",
    "README.md",
    "LICENSE",
    "NOTICE",
]


def copy_path(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prepare_release_bundle.py <target-dir>")

    repo_root = Path(__file__).resolve().parents[1]
    target_root = Path(sys.argv[1]).resolve()

    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True)

    for relative_path in INCLUDE_PATHS:
        source = repo_root / relative_path
        if not source.exists():
            raise SystemExit(f"missing required release path: {relative_path}")
        copy_path(source, target_root / relative_path)

    subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "validate_bundle.py"),
            str(target_root),
            "--strict-release",
            "--expected-name",
            repo_root.name,
        ],
        check=True,
    )
    print(f"OK: prepared release bundle at {target_root}")


if __name__ == "__main__":
    main()
