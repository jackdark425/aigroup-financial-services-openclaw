# Plugin Roadmap

This repository has two first-class OpenClaw compatibility targets and both should evolve in parallel.

## 1. aigroup-financial-analysis-openclaw

Primary scope:

- DCF
- comps
- LBO
- 3-statement models
- competitive analysis
- deck QC

Product role:

- analyst toolkit
- valuation toolkit
- financial modeling toolkit

## 2. aigroup-investment-banking-openclaw

Primary scope:

- pitch decks
- data packs
- strip profiles
- teasers
- buyer lists
- process letters
- CIM workflows
- deal tracking

Product role:

- investment banking execution toolkit
- deal materials toolkit
- client delivery toolkit

## Shared engineering goals

- preserve upstream Anthropic plugin structure for traceability
- package reusable content as OpenClaw-compatible Claude bundles
- keep skills installable into OpenClaw workspaces
- preserve `.mcp.json` as connector templates and future runtime targets
- maintain Apache 2.0 attribution and modification notices

## Near-term milestones

1. Keep both bundles building from upstream with the same generator pipeline.
2. Verify both bundles load on macOS and Ubuntu OpenClaw hosts.
3. Smoke test representative skills from both bundles through OpenClaw.
4. Improve MCP compatibility for upstream remote connector definitions.
5. Decide whether to introduce native OpenClaw extension wrappers for selected capabilities.
