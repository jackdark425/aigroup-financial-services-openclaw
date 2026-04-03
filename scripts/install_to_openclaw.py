#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
BUNDLES = ROOT / "bundles"


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


def install_bundle_mcp(workspace: Path, bundle_name: str) -> list[str]:
    bundle_mcp = BUNDLES / bundle_name / ".mcp.json"
    if not bundle_mcp.exists():
        return []

    payload = json.loads(bundle_mcp.read_text(encoding="utf-8"))
    mcp_servers = payload.get("mcpServers")
    if not isinstance(mcp_servers, dict) or not mcp_servers:
        return []

    target_dir = workspace / "plugin-connectors"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"{bundle_name}.mcp.json"
    target_file.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return list(mcp_servers.keys())


def main() -> None:
    parser = argparse.ArgumentParser(description="Install generated financial service skill packs into an OpenClaw workspace.")
    parser.add_argument("--workspace", required=True, help="Path to ~/.openclaw/workspace")
    parser.add_argument("--plugin", action="append", required=True, help="Plugin pack to install, e.g. financial-analysis")
    parser.add_argument("--no-prefix", action="store_true", help="Install skill names without plugin-name prefixes")
    parser.add_argument(
        "--with-bundle-connectors",
        action="store_true",
        help="Also copy bundle MCP templates into workspace/plugin-connectors",
    )
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    all_installed = {}
    for plugin_name in args.plugin:
        installed = install_plugin(workspace, plugin_name, prefix=not args.no_prefix)
        all_installed[plugin_name] = installed
        if args.with_bundle_connectors:
            connector_ids = install_bundle_mcp(workspace, f"{plugin_name}-openclaw")
            if connector_ids:
                print(f"[{plugin_name}] copied MCP template with {len(connector_ids)} server(s)")
                for connector_id in connector_ids:
                    print(f"  * {connector_id}")

    for plugin_name, installed in all_installed.items():
        print(f"[{plugin_name}] installed {len(installed)} skill(s)")
        for name in installed:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
