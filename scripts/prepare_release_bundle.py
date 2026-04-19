#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import json
from pathlib import Path


INCLUDE_PATHS = [
    ".claude-plugin",
    ".mcp.json",
    "skills",
    "commands",
    "scripts",
    "docs",            # smoke-test-macmini.md + related user-facing docs
    "QUICKSTART.md",   # 3-step macmini install guide (referenced from README)
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


def load_plugin_name(repo_root: Path) -> str:
    manifest_path = repo_root / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text())
    plugin_name = manifest.get("name")
    if not plugin_name:
        raise SystemExit("missing plugin name in .claude-plugin/plugin.json")
    return plugin_name


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prepare_release_bundle.py <target-dir>")

    repo_root = Path(__file__).resolve().parents[1]
    target_root = Path(sys.argv[1]).resolve()
    expected_name = load_plugin_name(repo_root)

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
            expected_name,
        ],
        check=True,
    )
    print(f"OK: prepared release bundle at {target_root}")


if __name__ == "__main__":
    main()
