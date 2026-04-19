# aigroup-financial-services-openclaw

Financial modeling, analysis, and deliverables suite for OpenClaw. **Stable track (0.2.0+).**

## Quick Install (macmini)

**Just want it running?** See [QUICKSTART.md](QUICKSTART.md) — 3 steps, preflight script, pitfall workarounds. The rest of this README is reference material.

```bash
openclaw plugins install clawhub:aigroup-financial-services-openclaw
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
bash ~/.openclaw/extensions/aigroup-financial-services-openclaw/scripts/preflight.sh
```


AIGroup 自研 + 其他大厂开源能力整合版，用于把企业客户调查、金融分析、建模和交付物生成整合成一套可发布、可运行的 OpenClaw banker workflow。

## Stable vs Lab（0.2.0 开始分两条轨）

从 0.2.0 起，这个包是 **稳定版 (stable track)**，只包含经充分验证的 skills / commands / office 交付层，**不再内置任何实验性 MCP server**。

| 能力 | 稳定版 (本仓库) | 探索版 (`aigroup-financial-services-openclaw-lab`，私仓) |
|------|----------------|------------------------------------------------------|
| Skills（customer-analysis-pack / datapack-builder / dcf-model / pitch-deck / etc.） | ✅ | ✅ |
| Office 交付层（word/excel/pdf via bundled MiniMax skills + `aigroup-mdtoword-mcp` companion） | ✅ | ✅ |
| PPT 路由（unified `ppt-deliverable` → host MiniMax PPT skills） | ✅ | ✅ |
| `aigroup-econ-mcp`（66 个计量经济学工具，PyPI 2.0.10） | ❌ **未启用** | ✅ opt-in |
| `aigroup-mdtopptx-mcp`（嵌入式 pptxgenjs banker 模板） | ❌ **未启用** | ✅ opt-in |
| `.mcp.json` 注册的 MCP server 数 | 0（纯 skills 包） | 2 |

**选择建议**：只要 host 上装了 MiniMax 家 office skills 和标准 MCP（FMP / Finnhub / Market / Tushare），稳定版就能端到端跑完 banker workflow。**需要 econ-mcp 计量工具或 pptxgenjs 嵌入式 PPT 模板的场景才去装探索版**。

## 0.2.0 变更要点

- `.mcp.json`: `mcpServers` 清空 — 本包不再注册任何 MCP server
- `scripts/mdtopptx/`: 目录整体移除（搬到探索版私仓）
- `package.json`: 删除 `@modelcontextprotocol/sdk` / `pptxgenjs` / `marked` / `zod` 依赖（稳定版不再需要 Node 运行时 MCP server）
- `skills/dcf-model/SKILL.md` 和 `skills/datapack-builder/SKILL.md`: econ-mcp 相关段落前加 "stable plugin note"，明确声明需要 lab 包


This repository is a community-built derivative of `anthropics/financial-services-plugins`, distributed under Apache 2.0 with retained attribution, NOTICE preservation, and prominent modification notices in adapted source files. It is not an official Anthropic plugin or Anthropic release.

Install this as the financial workflow suite after `aigroup-lead-discovery-openclaw`. It is designed to be the second half of the AIGroup banker stack: lead-discovery gathers company intelligence, and this plugin turns that context into models, analysis, and deliverables.

This plugin now ships skills and commands only by default, and expects data collection to come from AIGroup lead-intelligence plugins and MCP services.

It now exposes four explicit office-deliverable entrypoints inside the plugin itself:

- `word-deliverable`
- `excel-deliverable`
- `ppt-deliverable`
- `pdf-deliverable`

This plugin now also vendors three MiniMax-origin office skills directly under `skills/`:

- `minimax-docx` (MIT, included in this plugin)
- `minimax-xlsx` (MIT, included in this plugin)
- `minimax-pdf` (MIT, included in this plugin)

These bundled skills are adapted from verified MiniMaxAI host installs, with
thanks to MiniMaxAI for the original Word, Excel, and PDF skill foundations.

These wrapper skills route banker workflows into the plugin's bundled office capabilities first. On `macmini`, the verified mapping is:

- Word -> `minimax-docx` -> `aigroup-mdtoword-mcp__markdown_to_docx` -> standard `docx`
- Excel -> `minimax-xlsx`
- PDF -> `minimax-pdf` -> standard `pdf`
- PPT -> unified `ppt-deliverable` entry -> host PPT skills (`pptx-generator`, `slide-making-skill`, `ppt-orchestra-skill`, `ppt-editing-skill`) -> standard `pptx` fallback

For Word, Excel, and PDF, the bundled MiniMax-derived skills are now part of the install surface of this plugin. Word also treats `aigroup-mdtoword-mcp` as an explicit companion route for banker memo generation and markdown-to-Word packaging. PPT routing is handled through the unified `ppt-deliverable` front door, which delegates to host MiniMax PPT skills (`pptx-generator`, `slide-making-skill`, `ppt-orchestra-skill`, `ppt-editing-skill`) for the actual deck generation. Starting with 0.1.17, this plugin no longer ships its own `aigroup-mdtopptx-mcp` server — earlier versions experimented with an embedded pptxgenjs route but the host MiniMax PPT skill suite produces significantly better banker decks, so the plugin now defers to it.

Important routing note: these wrappers should not use shell-level `which` checks, PATH probing, or same-name executable discovery as the test for host office capability. On some hosts, those capabilities exist as routed skills without matching shell binaries.

Important: the MiniMax / office layer is now split:

- Word, Excel, and PDF MiniMax-derived skills are included in this plugin
- Word output explicitly supports `aigroup-mdtoword-mcp` as a companion path, so environments without MiniMax-style host wiring still have a stable `.docx` route
- PPT delegates entirely to host MiniMax PPT skills via the unified `ppt-deliverable` front door (0.1.17 removed the embedded `aigroup-mdtopptx-mcp` pptxgenjs route)

If a user already has compatible host skills installed, that is still fine. The plugin should simply prefer its bundled Word/Excel/PDF path and use `ppt-deliverable` as the single PPT front door, delegating to compatible host capabilities where available.

This repository is a compatibility layer, not a claim of official Anthropic or OpenClaw endorsement.

## Licensing And Attribution

- Upstream financial plugin source comes from `anthropics/financial-services-plugins` under Apache License 2.0.
- This repository retains Apache 2.0 licensing materials and NOTICE attribution for upstream-derived content.
- Modified upstream-derived skill and command files in this repository carry prominent notices that they were adapted by AIGroup for OpenClaw compatibility and banker workflow packaging.
- Anthropic and MiniMax names, marks, and branding are used only to describe origin and compatibility, not to imply endorsement.
- Bundled MiniMax office components remain separately attributed under their stated MIT terms.
- Each vendored MiniMax skill directory also carries its own `ATTRIBUTION.md` for source and packaging context.

See:

- [LICENSE](LICENSE)
- [NOTICE](NOTICE)
- [docs/apache-2.0-compliance.md](docs/apache-2.0-compliance.md)
- [docs/vendored-minimax-components.md](docs/vendored-minimax-components.md)

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
- `.mcp.json` -> local stdio MCP wiring (only `aigroup-econ-mcp` since 0.1.17; earlier 0.1.13–0.1.16 also registered `aigroup-mdtopptx-mcp`)
- `.mcp.optional-upstream.json` -> preserved reference template for the original 11 upstream HTTP connectors
- `.claude-plugin/plugin.json` -> source metadata only

For external installation and Hub publishing, the root repository now functions as a single bundle plugin that combines the financial-analysis and investment-banking tracks.

## Recommended Pairing

For real-world use, treat installation as a two-suite flow and install this plugin together with `aigroup-lead-discovery-openclaw`.

Recommended stack:

- `aigroup-lead-discovery-openclaw` for company intelligence, customer investigation, and external lead signals
- `aigroup-fmp-mcp`, `aigroup-market-mcp`, and `aigroup-finnhub-mcp` as AIGroup data services
- `aigroup-financial-services-openclaw` for customer analysis, financial modeling, and deliverable generation

## Office Surface Inside The Plugin

The plugin now includes explicit office-oriented commands and skills so the second half of the banker stack can move from analysis to deliverable packaging without leaving the plugin surface:

- `word` -> `word-deliverable`
- `excel` -> `excel-deliverable`
- `ppt` / `ppts` -> `ppt-deliverable`
- `pdf` -> `pdf-deliverable`

Recommended chaining:

1. research or analyze with finance skills such as `customer-analysis-pack`, `datapack-builder`, `comps-analysis`, `dcf-model`, or `lbo-model`
2. package the output through `word-deliverable`, `excel-deliverable`, `ppt-deliverable`, or `pdf-deliverable`
3. use PDF last when the goal is a stable distribution artifact

This office surface is intentionally packaged as a banker-facing front door, with bundled Word/Excel/PDF support and a unified PPT front door that reuses host enhancement when available.

- It is meant to make banker workflows easier to use.
- It is not meant to force every user to preinstall MiniMax office skills just to get Word, Excel, or PDF output.
- It also works cleanly with `aigroup-mdtoword-mcp` when the Word job starts from markdown, notes, or a banker memo draft.
- PPT jobs that start from markdown, structured analysis, or a banker memo go through the unified `ppt-deliverable` front door and land on host MiniMax PPT skills, which produce editable banker-quality decks.
- Users who already have equivalent host skills can still use those alongside the bundled paths.

See:

- [docs/minimax-office-optional.md](docs/minimax-office-optional.md)

## Root Bundle

The repository root now provides a standalone bundle with:

- merged `skills/`
- merged `commands/`
- `.mcp.json` wiring `aigroup-econ-mcp` as the embedded local stdio MCP
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
- [docs/minimax-office-optional.md](docs/minimax-office-optional.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)
- [docs/which-suite-to-use.md](docs/which-suite-to-use.md)

## Default Customer Workflow

The default banker path is now:

1. `aigroup-lead-discovery-openclaw/customer-investigation`
2. `aigroup-financial-services-openclaw/customer-analysis-pack`
3. `datapack-builder`, `dcf-model`, or other downstream modeling skills only when needed

This keeps the first pass focused on banker-usable customer investigation and customer analysis before moving into heavier finance deliverables.

Published package:

- `aigroup-financial-services-openclaw@0.1.16`

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
