#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / "upstream" / "financial-services-plugins"
PACKS = ROOT / "packs"


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> None:
    if not UPSTREAM.exists():
        raise SystemExit(f"Missing upstream repo: {UPSTREAM}")

    plugin_dirs = [
        p
        for p in UPSTREAM.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / ".claude-plugin" / "plugin.json").exists()
    ]

    for plugin_dir in sorted(plugin_dirs):
        plugin_name = plugin_dir.name
        pack_dir = PACKS / plugin_name
        skills_src = plugin_dir / "skills"
        commands_src = plugin_dir / "commands"
        mcp_src = plugin_dir / ".mcp.json"
        meta_src = plugin_dir / ".claude-plugin" / "plugin.json"

        pack_dir.mkdir(parents=True, exist_ok=True)

        if skills_src.exists():
            copy_tree(skills_src, pack_dir / "skills")
        if commands_src.exists():
            copy_tree(commands_src, pack_dir / "commands")

        connectors_dir = pack_dir / "connectors"
        connectors_dir.mkdir(parents=True, exist_ok=True)
        if mcp_src.exists():
            shutil.copy2(mcp_src, connectors_dir / ".mcp.json")

        metadata = {}
        if meta_src.exists():
            metadata = json.loads(meta_src.read_text())
        metadata["source_plugin_dir"] = str(plugin_dir.relative_to(UPSTREAM))
        metadata["generated_by"] = "scripts/sync_upstream.py"
        (pack_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    print(f"Generated packs for {len(plugin_dirs)} plugin(s) into {PACKS}")


if __name__ == "__main__":
    main()

