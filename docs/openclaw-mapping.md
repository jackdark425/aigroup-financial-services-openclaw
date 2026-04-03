# OpenClaw Mapping

## Goal

Turn Anthropic financial services plugins into assets OpenClaw can actually use.

## Mapping Table

| Claude Source | OpenClaw Target | Notes |
|---------------|-----------------|-------|
| `skills/` | `~/.openclaw/workspace/skills/` | Primary compatibility path |
| `commands/*.md` | operator docs / future wrappers | Not directly executable in OpenClaw today |
| `.mcp.json` | MCP config templates | Requires manual or scripted merge into OpenClaw config |
| `.claude-plugin/plugin.json` | metadata only | Useful for source grouping, not OpenClaw runtime |

## Installation Strategy

This repository does not try to pretend Claude plugins are native OpenClaw plugins.

Instead, it:

1. groups upstream content by plugin name
2. copies reusable skills into generated packs
3. preserves command docs and connector templates
4. installs only the parts OpenClaw can consume safely

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

