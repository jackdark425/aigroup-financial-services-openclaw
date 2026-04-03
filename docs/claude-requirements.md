# Claude Source Requirements

This repository is based on Anthropic's `financial-services-plugins` source model.

## Source Plugin Model

Upstream describes each plugin as:

```text
plugin-name/
├── .claude-plugin/plugin.json
├── .mcp.json
├── commands/
└── skills/
```

Key source assumptions from upstream:

- plugins are file-based
- skills are markdown-driven
- commands are markdown-driven
- connectors are expressed through `.mcp.json`
- no build system is required for the core plugin content

## What Must Be Preserved

When adapting upstream content into OpenClaw form:

- keep the upstream Apache 2.0 license and attribution
- keep prominent notices for modified files
- preserve source plugin names and metadata for traceability
- keep `commands/` and `.mcp.json` content available even if OpenClaw cannot consume them directly yet
- do not imply Anthropic endorsement

## What Is Not Directly Compatible

These Claude-specific pieces are not native OpenClaw plugins:

- `.claude-plugin/plugin.json`
- Claude slash command semantics in `commands/`
- Cowork / Claude Code plugin installation flow

These require adaptation, not direct installation.

## What Maps Well To OpenClaw

These pieces are usually reusable:

- `skills/<name>/SKILL.md`
- references, scripts, templates, and assets under each skill
- `.mcp.json` connector definitions as migration templates

## Commercialization Guardrails

Apache 2.0 generally permits commercial modification and redistribution, but:

- trademark rights are not granted
- external MCP providers still have their own service terms
- commercial offers should be positioned as an OpenClaw compatibility layer or derivative integration, not as an official Anthropic plugin

