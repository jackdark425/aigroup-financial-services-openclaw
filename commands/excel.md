---
description: Create or refresh an Excel workbook from financial-services outputs
argument-hint: "[company, model type, or workbook task]"
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Modified by AIGroup for OpenClaw compatibility and banker workflow packaging. Not an official Anthropic release. -->


# Excel Deliverable Command

Create a real `.xlsx` output from this plugin's analysis and modeling skills.

## Workflow

### Step 1: Identify workbook type

Decide whether the user wants:

- model workbook
- datapack workbook
- comps workbook
- tracker workbook

### Step 2: Load the skill

Use `skill: "excel-deliverable"`.

### Step 3: Build or refresh

Prefer outputs from:

- `3-statement-model`
- `comps-analysis`
- `datapack-builder`
- `dcf-model`
- `lbo-model`
- `merger-model`
- `deal-tracker`

Prefer the bundled `minimax-xlsx` skill included in this plugin, but do not use `which`, PATH checks, or executable-name probing to decide that. If the bundled skill is not clearly exposed, continue with the standard `xlsx` path.

### Step 4: Deliver

Provide:

1. the `.xlsx`
2. a short note on workbook structure
3. any assumptions or manual inputs still pending
