# Test Report

## Scope

This report captures end-to-end validation for the two OpenClaw bundles:

- `aigroup-financial-analysis-openclaw`
- `aigroup-investment-banking-openclaw`

Validation was performed across two primary OpenClaw hosts:

- Host A (macOS)
- Host B (Ubuntu)

The goal was not only to confirm that skills show up as `ready`, but that they can emit real artifacts through repeatable smoke paths and, where practical, through real OpenClaw agent execution.

## Host Notes

### Host A (macOS)

- OpenClaw version: `2026.4.2`
- Default financial workflows were validated through a dedicated clean agent.
- Testing used a dedicated financial validation workspace.
- Important operational note:
  - The legacy default agent had recurrent session-lock issues.
  - A clean replacement agent was created and promoted for financial validation.

### Host B (Ubuntu)

- OpenClaw version: `2026.4.2`
- Default agent remained usable for financial validation.
- Testing used a dedicated financial validation workspace.

## Functional Results

## Validation Matrix

Legend:

- `Loaded`: bundle/plugin loads successfully in OpenClaw
- `Ready`: skill appears as `✓ ready`
- `Artifact`: deterministic smoke artifact re-run succeeded in this round
- `Agent`: real OpenClaw agent execution succeeded in this round

### Plugin-Level Matrix

| Host | Plugin | Loaded | Notes |
|---|---|---|---|
| Host A | `aigroup-financial-analysis-openclaw` | Yes | Bundle format `claude`, loaded cleanly |
| Host A | `aigroup-investment-banking-openclaw` | Yes | Bundle format `claude`, loaded cleanly |
| Host B | `aigroup-financial-analysis-openclaw` | Yes | Loaded; upstream HTTP MCP templates still show `unsupported transport` |
| Host B | `aigroup-investment-banking-openclaw` | Yes | Bundle format `claude`, loaded cleanly |

### Skill Matrix

| Skill | Plugin | Host A Ready | Host B Ready | Host A Artifact | Host B Artifact | Host A Agent | Host B Agent | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `dcf-model` | financial-analysis | Yes | Yes | Yes | Yes | Previously verified | Previously verified | Core workbook flow stable |
| `lbo-model` | financial-analysis | Yes | Yes | Yes | Yes | Not re-run this round | Not re-run this round | Minimal builder fixed malformed workbook issue |
| `3-statement-model` | financial-analysis | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Existing smoke outputs still valid |
| `audit-xls` | financial-analysis | Yes | Yes | Previously verified | N/A | Not re-run this round | N/A | Markdown audit output already validated |
| `clean-data-xls` | financial-analysis | Yes | Yes | Previously verified | N/A | Not re-run this round | N/A | Cleaned workbook path previously validated |
| `deck-refresh` | financial-analysis | Yes | Yes | Previously verified | N/A | Not re-run this round | N/A | PPT refresh output previously validated |
| `competitive-analysis` | financial-analysis | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Text/report workflow already validated |
| `comps-analysis` | financial-analysis | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Text/report workflow already validated |
| `ppt-template-creator` | financial-analysis | Yes | Yes | Yes | Yes | Yes | Not re-run this round | Host A agent path corrected wrong initial lookup and completed |
| `buyer-list` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Prior markdown smoke output available |
| `cim-builder` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Prior markdown smoke output available |
| `datapack-builder` | investment-banking | Yes | Yes | Yes | Yes | Yes | Not re-run this round | Deterministic builder added for stability |
| `deal-tracker` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Prior markdown smoke output available |
| `fsi-strip-profile` | investment-banking | Yes | Yes | Yes | Yes | Not re-run this round | Yes | Host B real-agent path verified |
| `ib-check-deck` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Prior markdown smoke output available |
| `merger-model` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Prior markdown smoke output available |
| `pitch-deck` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Previously verified | Spark PPT artifact already validated |
| `process-letter` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Prior markdown smoke output available |
| `teaser` | investment-banking | Yes | Yes | Previously verified | Previously verified | Not re-run this round | Not re-run this round | Prior markdown smoke output available |

### aigroup-financial-analysis-openclaw

Validated skills:

- `dcf-model`
- `lbo-model`
- `3-statement-model`
- `audit-xls`
- `clean-data-xls`
- `deck-refresh`
- `competitive-analysis`
- `comps-analysis`
- `ppt-template-creator`

Representative artifacts:

- DCF workbook and summary
- 3-statement workbook and summary
- Audit markdown report
- Cleaned workbook and summary
- Deck refresh presentation and summary
- Generated template skill package, template asset, and summary

### aigroup-investment-banking-openclaw

Validated skills:

- `buyer-list`
- `cim-builder`
- `datapack-builder`
- `deal-tracker`
- `fsi-strip-profile`
- `ib-check-deck`
- `merger-model`
- `pitch-deck`
- `process-letter`
- `teaser`

Representative artifacts:

- Pitch deck presentation
- Datapack workbook and summary
- Datapack output via real OpenClaw agent on Host A
- Strip profile presentation and summary
- Strip profile output via real OpenClaw agent on Host B
- Markdown/report outputs for buyer list, CIM builder, deal tracker, merger model, process letter, teaser, and deck review

## Fixes Landed During Validation

### 1. Investment-banking skill recognition

Several investment-banking skills were not initially recognized because their `SKILL.md` files lacked valid frontmatter. That issue was fixed so they could load and test as real OpenClaw skills.

### 2. LBO artifact integrity

`lbo-model` initially emitted malformed `.xlsx` files. A deterministic minimal builder and validator were added so the bundle now produces valid workbooks on both hosts.

### 3. Remaining-skill deterministic smoke paths

The following skills originally depended too heavily on open-ended model behavior during smoke tests:

- `datapack-builder`
- `fsi-strip-profile`
- `ppt-template-creator`

Deterministic helper scripts were added for each of them so validation no longer depends on fragile tool routing.

### 4. Host A financial-agent stability

Because Host A's legacy default agent repeatedly hit session-lock issues during financial workflows, a new clean agent was created and promoted for financial validation.

## Current Known Limitations

- Host A legacy default agent still has historical session-lock baggage for long-running local turns.
- Some agent turns may initially look in the wrong bundle path when two bundles expose similarly named finance workflows; in the most important cases tested here, the agent was still able to self-correct or was verified via deterministic smoke path.
- Upstream HTTP MCP connector templates from the original Anthropic plugin structure are not treated as fully validated runtime MCP integrations in this report; the emphasis here is on skill execution and artifact generation.

## Bottom Line

Both OpenClaw bundles are now in a usable state across both validated hosts.

- Bundle loading is working.
- Skill discovery is working.
- Artifact-producing smoke tests are working.
- Key real-agent OpenClaw execution paths are also working after stabilization.

For ongoing use, Host A should prefer the dedicated clean financial agent for long-running financial workflows.
