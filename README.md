# aigroup-financial-services-openclaw

Financial modeling, analysis, and deliverables suite for OpenClaw.

Install this as the financial workflow suite after `aigroup-lead-discovery-openclaw`. It is designed to be the second half of the AIGroup banker stack: lead-discovery gathers company intelligence, and this plugin turns that context into models, analysis, and deliverables.

This plugin now ships skills and commands only by default, and expects data collection to come from AIGroup lead-intelligence plugins and MCP services.

This repository is a compatibility layer, not a claim of official Anthropic or OpenClaw endorsement.

It now also exposes a standalone root-level Claude bundle so the repository itself can be installed and published as a single OpenClaw plugin:

```bash
openclaw plugins install jackdark425/aigroup-financial-services-openclaw
```

It is also published on OpenClaw Hub:

```bash
openclaw plugins install aigroup-financial-services-openclaw
```

## What This Repo Does

- tracks the latest upstream `anthropics/financial-services-plugins`
- preserves the original Claude plugin structure under `upstream/`
- exposes a standalone root bundle under the repository root
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

OpenClaw does not consume that structure directly as a plugin. However, the `skills/` directories are often directly reusable as OpenClaw workspace skills, and the connector definitions can be repurposed as optional MCP configuration templates.

For distribution, this repository now does two things:

- the repository root acts as a single installable bundle plugin: `aigroup-financial-services-openclaw`
- `bundles/` keeps the narrower sub-bundles for targeted installs and validation

## Repository Layout

```text
aigroup-financial-services-openclaw/
├── .claude-plugin/plugin.json         # root standalone bundle manifest
├── .mcp.json                          # root connector template
├── skills/                            # merged root skill set
├── commands/                          # merged root command set
├── upstream/
│   └── financial-services-plugins/   # latest upstream clone
├── packs/
│   └── <plugin-name>/
│       ├── skills/                   # generated OpenClaw-ready skill copies
│       ├── commands/                 # copied Claude command docs
│       ├── connectors/               # copied MCP templates
│       └── metadata.json
├── bundles/
│   └── aigroup-<plugin-name>-openclaw/
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
- [docs/test-report.md](docs/test-report.md)
- [docs/quickstart.md](docs/quickstart.md)
- [docs/mac-mini-host-runbook.md](docs/mac-mini-host-runbook.md)

## Current Strategy

This repository currently treats Anthropic financial plugins as:

- `skills/` -> OpenClaw workspace skills
- `commands/` -> operator playbooks / future command adapters
- `.mcp.json` -> empty by default, so the published plugin installs cleanly without unsupported remote MCP transports
- `.mcp.optional-upstream.json` -> preserved reference template for the original 11 upstream HTTP connectors
- `.claude-plugin/plugin.json` -> source metadata only

For external installation and Hub publishing, the root repository now functions as a single bundle plugin that combines the financial-analysis and investment-banking tracks.

## Recommended Pairing

For real-world use, treat installation as a two-suite flow and install this plugin together with `aigroup-lead-discovery-openclaw`.

Recommended stack:

- `aigroup-lead-discovery-openclaw` for company intelligence, customer investigation, and external lead signals
- `aigroup-fmp-mcp`, `aigroup-market-mcp`, and `aigroup-finnhub-mcp` as AIGroup data services
- `aigroup-financial-services-openclaw` for customer analysis, financial modeling, and deliverable generation

## Root Bundle

The repository root now provides a standalone bundle with:

- merged `skills/`
- merged `commands/`
- empty `.mcp.json` so installs stay clean by default
- optional `.mcp.optional-upstream.json` for operators who explicitly want the original upstream connector references
- `.claude-plugin/plugin.json` manifest

Use the root bundle when you want one install that covers the full financial-services workflow surface.

## Install From OpenClaw Hub

```bash
openclaw plugins install aigroup-lead-discovery-openclaw
openclaw plugins install aigroup-financial-services-openclaw
openclaw plugins inspect aigroup-lead-discovery-openclaw
openclaw plugins inspect aigroup-financial-services-openclaw
```

## Recommended Trust Pinning

If you want to remove the default `plugins.allow is empty` warning and make trust explicit, pin the suite ids in your OpenClaw config:

```json
{
  "plugins": {
    "allow": [
      "aigroup-lead-discovery-openclaw",
      "aigroup-financial-services-openclaw"
    ]
  }
}
```

Then restart the gateway before testing.

Quick install guide:

- [docs/start-here.md](docs/start-here.md)
- [docs/quickstart.md](docs/quickstart.md)
- [docs/banker-stack.md](docs/banker-stack.md)
- [docs/example-prompts.md](docs/example-prompts.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/which-suite-to-use.md](docs/which-suite-to-use.md)

## Default Customer Workflow

The default banker path is now:

1. `aigroup-lead-discovery-openclaw/customer-investigation`
2. `aigroup-financial-services-openclaw/customer-analysis-pack`
3. `datapack-builder`, `dcf-model`, or other downstream modeling skills only when needed

This keeps the first pass focused on banker-usable customer investigation and customer analysis before moving into heavier finance deliverables.

Published package:

- `aigroup-financial-services-openclaw@0.1.3`

Recommended companion package:

- `aigroup-lead-discovery-openclaw`

## Release Prep

To prepare the minimal publishable artifact used for ClawHub releases:

```bash
python3 scripts/prepare_release_bundle.py /tmp/aigroup-financial-services-openclaw-release
```

To validate the repository bundle shape directly:

```bash
python3 scripts/validate_bundle.py .
```

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

- `bundles/aigroup-financial-analysis-openclaw`
- `bundles/aigroup-investment-banking-openclaw`

Root standalone bundle:

- `aigroup-financial-services-openclaw` (repository root)

These are the two primary plugin tracks for this repository and should be developed in parallel:

- `aigroup-financial-analysis-openclaw`: valuation, modeling, and analytical workflows
- `aigroup-investment-banking-openclaw`: deal materials, pitch workflows, and transaction execution workflows

## Data Inputs

By default, this plugin no longer enables the 11 upstream external financial HTTP MCP connectors during installation.

That choice is intentional:

- it keeps Hub installation simple
- it avoids unsupported transport warnings for most users
- it makes `aigroup-lead-discovery-openclaw` the default AIGroup data-entry layer

If an operator explicitly wants the original upstream connector references, copy or adapt:

```bash
.mcp.optional-upstream.json
```

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

- `aigroup-financial-services-openclaw`
- `aigroup-financial-analysis-openclaw`
- `aigroup-investment-banking-openclaw`

## License

This repository is distributed under Apache 2.0, consistent with the upstream source. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
