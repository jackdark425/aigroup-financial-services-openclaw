---
description: Create a banker-ready Word deliverable from financial-services outputs
argument-hint: "[memo topic, company, or source material]"
---

# Word Deliverable Command

Create a `.docx` deliverable from this plugin's financial-services work.

## Workflow

### Step 1: Identify the source

Use the provided company, memo topic, or existing material.

If no source is given, ask what should be turned into Word:

- customer analysis
- datapack summary
- comps / valuation memo
- diligence note

### Step 2: Load the skill

Use `skill: "word-deliverable"`.

### Step 3: Build the deliverable

Prefer prior outputs from:

- `customer-analysis-pack`
- `datapack-builder`
- `comps-analysis`
- `dcf-model`
- `lbo-model`

Use `minimax-docx` when the host exposes it.

### Step 4: Deliver

Provide:

1. the `.docx`
2. a short summary of contents
3. any open assumptions still needing confirmation
