# OpenClaw Mapping

## Goal

Turn Anthropic financial services plugins into assets OpenClaw can actually use.

## Mapping Table

| Claude Source | OpenClaw Target | Notes |
|---------------|-----------------|-------|
| `skills/` | `~/.openclaw/workspace/skills/` | Primary compatibility path |
| `commands/*.md` | bundle capability plus operator docs | OpenClaw can inspect Claude bundle command roots, but command semantics still need adaptation |
| `.mcp.json` | bundle MCP capability or config template | Can ship inside a Claude-style bundle or be copied into config templates |
| `.claude-plugin/plugin.json` | bundle manifest | Not a native OpenClaw extension manifest, but usable through OpenClaw bundle compatibility |

## Installation Strategy

This repository does not try to pretend Claude plugins are native TypeScript OpenClaw extensions.

Instead, it:

1. groups upstream content by plugin name
2. copies reusable skills into generated packs
3. builds Claude-style bundles that OpenClaw can inspect and load
4. preserves command docs and connector templates
5. installs only the parts OpenClaw can consume safely

## Collision Strategy

Some upstream skill names are generic, for example:

- `competitive-analysis`
- `skill-creator`
- `pitch-deck`

To reduce collisions during installation, this repository prefixes installed skills by default:

```text
financial-analysis--dcf-model
investment-banking--pitch-deck
equity-research--earnings-analysis
```

## MCP Strategy

The `financial-analysis` upstream plugin contains the core connector set. In OpenClaw terms, those should eventually become:

- reusable MCP config snippets
- optional install profiles
- or fully developed OpenClaw extension wrappers

This repository currently preserves them as templates first.
