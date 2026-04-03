#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
BUNDLES = ROOT / "bundles"
SUPPORTED_BUNDLES = ("financial-analysis", "investment-banking")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_optional_dir(src: Path, dest: Path) -> bool:
    if not src.exists():
        return False
    shutil.copytree(src, dest)
    return True


def copy_optional_file(src: Path, dest: Path) -> bool:
    if not src.exists():
        return False
    shutil.copy2(src, dest)
    return True


def render_manifest(pack_name: str, metadata: dict, has_commands: bool, has_mcp: bool) -> dict:
    manifest: dict[str, object] = {
        "name": f"{pack_name}-openclaw",
        "description": metadata.get("description") or f"{pack_name} OpenClaw bundle",
        "version": metadata.get("version") or "0.1.0",
        "skills": "skills",
    }
    if has_commands:
        manifest["commands"] = "commands"
    if has_mcp:
        manifest["mcpServers"] = ".mcp.json"
    return manifest


def render_readme(bundle_name: str, metadata: dict, has_commands: bool, has_mcp: bool) -> str:
    lines = [
        f"# {bundle_name}",
        "",
        metadata.get("description") or f"OpenClaw bundle for {bundle_name}.",
        "",
        "This bundle is derived from Anthropic's `financial-services-plugins` and adapted for OpenClaw bundle loading.",
        "",
        "## Included",
        "",
        "- `skills/`: OpenClaw-loadable skills",
    ]
    if has_commands:
        lines.append("- `commands/`: Claude command markdown exposed as additional skill-like bundle content")
    if has_mcp:
        lines.append("- `.mcp.json`: MCP connector template for OpenClaw bundle import")
    lines.extend(
        [
            "",
            "## Install",
            "",
            "Point OpenClaw at this bundle directory as a local plugin source, or copy the `skills/` directory into `~/.openclaw/workspace/skills/`.",
            "",
            "## Attribution",
            "",
            "See `LICENSE`, `NOTICE`, and `UPSTREAM.md` for licensing, provenance, and modification notes.",
            "",
        ]
    )
    return "\n".join(lines)


def render_upstream_note(pack_name: str, metadata: dict) -> str:
    source_dir = metadata.get("source_plugin_dir", pack_name)
    return "\n".join(
        [
            f"Source plugin: anthropics/financial-services-plugins/{source_dir}",
            f"Adapted bundle: {pack_name}-openclaw",
            "License: Apache-2.0",
            "",
            "This bundle is a derivative packaging for OpenClaw compatibility.",
            "It preserves original attribution and should not be presented as an official Anthropic plugin.",
            "",
        ]
    )


def build_bundle(pack_name: str) -> Path:
    pack_dir = PACKS / pack_name
    metadata = load_json(pack_dir / "metadata.json")
    bundle_dir = BUNDLES / f"{pack_name}-openclaw"

    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_dir.mkdir(parents=True)
    (bundle_dir / ".claude-plugin").mkdir()

    has_commands = copy_optional_dir(pack_dir / "commands", bundle_dir / "commands")
    copy_optional_dir(pack_dir / "skills", bundle_dir / "skills")

    mcp_file = pack_dir / "connectors" / ".mcp.json"
    mcp_payload = load_json(mcp_file) if mcp_file.exists() else {"mcpServers": {}}
    has_mcp = bool(mcp_payload.get("mcpServers"))
    if has_mcp:
        (bundle_dir / ".mcp.json").write_text(
            json.dumps(mcp_payload, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )

    manifest = render_manifest(pack_name, metadata, has_commands=has_commands, has_mcp=has_mcp)
    (bundle_dir / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (bundle_dir / "README.md").write_text(
        render_readme(f"{pack_name}-openclaw", metadata, has_commands=has_commands, has_mcp=has_mcp)
        + "\n",
        encoding="utf-8",
    )
    (bundle_dir / "UPSTREAM.md").write_text(
        render_upstream_note(pack_name, metadata),
        encoding="utf-8",
    )
    copy_optional_file(ROOT / "LICENSE", bundle_dir / "LICENSE")
    copy_optional_file(ROOT / "NOTICE", bundle_dir / "NOTICE")
    return bundle_dir


def main() -> None:
    BUNDLES.mkdir(parents=True, exist_ok=True)
    built: list[Path] = []
    for pack_name in SUPPORTED_BUNDLES:
        built.append(build_bundle(pack_name))
    for bundle_dir in built:
        print(bundle_dir)


if __name__ == "__main__":
    main()
