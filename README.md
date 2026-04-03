# financial-services-openclaw

OpenClaw-compatible adaptation of Anthropic's `financial-services-plugins`.

This repository is a compatibility layer, not a claim of official Anthropic or OpenClaw endorsement.

## What This Repo Does

- tracks the latest upstream `anthropics/financial-services-plugins`
- preserves the original Claude plugin structure under `upstream/`
- generates OpenClaw-oriented packs under `packs/`
- builds OpenClaw-readable Claude bundle plugins under `bundles/`
- provides install scripts for copying financial skills into an OpenClaw workspace
- documents how Claude plugin concepts map into OpenClaw concepts

## Why This Exists

Anthropic's source repository is file-based and easy to customize, but it is structured for Claude Cowork / Claude Code plugins:

- `.claude-plugin/plugin.json`
- `.mcp.json`
- `commands/`
- `skills/`

OpenClaw does not consume that structure directly as a plugin. However, the `skills/` directories are often directly reusable as OpenClaw workspace skills, and the connector definitions can be repurposed as MCP configuration templates.

## Repository Layout

```text
financial-services-openclaw/
├── upstream/
│   └── financial-services-plugins/   # latest upstream clone
├── packs/
│   └── <plugin-name>/
│       ├── skills/                   # generated OpenClaw-ready skill copies
│       ├── commands/                 # copied Claude command docs
│       ├── connectors/               # copied MCP templates
│       └── metadata.json
├── bundles/
│   └── <plugin-name>-openclaw/
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       ├── commands/
│       ├── .mcp.json
│       └── README.md
├── scripts/
│   ├── sync_upstream.py
│   ├── build_openclaw_bundles.py
│   └── install_to_openclaw.py
├── docs/
│   ├── claude-requirements.md
│   └── openclaw-mapping.md
├── NOTICE
└── LICENSE
```

## Claude Source Requirements

The original Anthropic repositories describe plugins as:

- file-based
- markdown and JSON driven
- built around `skills`, `commands`, and `.mcp.json`

Those source assumptions and adaptation notes are documented here:

- [docs/claude-requirements.md](docs/claude-requirements.md)
- [docs/openclaw-mapping.md](docs/openclaw-mapping.md)
- [docs/plugin-roadmap.md](docs/plugin-roadmap.md)

## Current Strategy

This repository currently treats Anthropic financial plugins as:

- `skills/` -> OpenClaw workspace skills
- `commands/` -> operator playbooks / future command adapters
- `.mcp.json` -> MCP connector templates for OpenClaw-side configuration
- `.claude-plugin/plugin.json` -> source metadata only

## Generate Packs

```bash
python3 scripts/sync_upstream.py
```

## Build OpenClaw-Compatible Bundles

These bundles use Claude bundle manifests because OpenClaw can inspect and load Claude-style bundle plugins for `skills`, `commands`, and `.mcp.json`.

```bash
python3 scripts/build_openclaw_bundles.py
```

Current generated bundles:

- `bundles/financial-analysis-openclaw`
- `bundles/investment-banking-openclaw`

These are the two primary plugin tracks for this repository and should be developed in parallel:

- `financial-analysis-openclaw`: valuation, modeling, and analytical workflows
- `investment-banking-openclaw`: deal materials, pitch workflows, and transaction execution workflows

## Install Skills Into OpenClaw

Example local install into a workspace:

```bash
python3 scripts/install_to_openclaw.py \
  --workspace ~/.openclaw/workspace \
  --plugin financial-analysis \
  --plugin investment-banking \
  --with-bundle-connectors
```

By default, installed skills are prefixed to avoid collisions.

## OpenClaw Bundle Strategy

This repository now supports two OpenClaw-compatible delivery modes:

- `packs/`: direct skill copying into an OpenClaw workspace
- `bundles/`: Claude-format bundle plugins that OpenClaw can inspect and load

The current production targets are:

- `financial-analysis-openclaw`
- `investment-banking-openclaw`

## License

This repository is distributed under Apache 2.0, consistent with the upstream source. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
