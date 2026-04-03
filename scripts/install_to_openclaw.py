#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"


def install_plugin(workspace: Path, plugin_name: str, prefix: bool) -> list[str]:
    pack_skills = PACKS / plugin_name / "skills"
    if not pack_skills.exists():
        raise FileNotFoundError(f"Pack not found or has no skills: {plugin_name}")

    workspace_skills = workspace / "skills"
    workspace_skills.mkdir(parents=True, exist_ok=True)

    installed = []
    for skill_dir in sorted(p for p in pack_skills.iterdir() if p.is_dir()):
        target_name = f"{plugin_name}--{skill_dir.name}" if prefix else skill_dir.name
        target_dir = workspace_skills / target_name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(skill_dir, target_dir)
        installed.append(target_name)
    return installed


def main() -> None:
    parser = argparse.ArgumentParser(description="Install generated financial service skill packs into an OpenClaw workspace.")
    parser.add_argument("--workspace", required=True, help="Path to ~/.openclaw/workspace")
    parser.add_argument("--plugin", action="append", required=True, help="Plugin pack to install, e.g. financial-analysis")
    parser.add_argument("--no-prefix", action="store_true", help="Install skill names without plugin-name prefixes")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    all_installed = {}
    for plugin_name in args.plugin:
        installed = install_plugin(workspace, plugin_name, prefix=not args.no_prefix)
        all_installed[plugin_name] = installed

    for plugin_name, installed in all_installed.items():
        print(f"[{plugin_name}] installed {len(installed)} skill(s)")
        for name in installed:
            print(f"  - {name}")


if __name__ == "__main__":
    main()

