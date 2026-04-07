---
name: word-deliverable
description: Turn financial-services outputs into a polished Word deliverable. Use when the user wants an IC memo, customer memo, internal note, diligence summary, or banker-ready .docx built from this plugin's analysis.
---

# Word Deliverable

Use this skill when the user wants a Word document as the final output surface for work produced by this plugin.

## Best-fit cases

- Customer memo after `customer-analysis-pack`
- Investment committee memo after `datapack-builder`
- Diligence note after `comps-analysis`, `dcf-model`, or `lbo-model`
- Internal banking brief assembled from multiple plugin outputs

## Tooling preference

Prefer the host's exact MiniMax Word skill when it is available:

- `minimax-docx`

If the host does not expose that MiniMax path, fall back to the standard `docx` workflow already available in the environment.

This is an optional acceleration path. If the host already has a compatible Word / DOCX skill installed, use it directly. Do not require a fresh MiniMax install just to proceed.

The core rule is:

- author the document as a real `.docx`
- keep tables and headings structured
- do not stop at markdown if the user explicitly asked for Word

## Workflow

### Step 1: Gather source material

Use existing outputs from this plugin first:

- `customer-analysis-pack`
- `datapack-builder`
- `comps-analysis`
- `competitive-analysis`
- `dcf-model`
- `lbo-model`
- `process-letter`

If the user already has markdown, Excel, PPT, or notes, treat them as input material rather than rewriting from scratch.

### Step 2: Choose document type

Pick the smallest document that matches the ask:

- memo
- briefing note
- IC summary
- diligence note
- board-ready written appendix

Clarify audience and tone only if needed for structure.

### Step 3: Build the `.docx`

Default structure:

```markdown
# Title
## Executive Summary
## Company Overview / Situation
## Analysis
## Risks
## Recommendation / Next Steps
## Appendix
```

Requirements:

- real section headings
- clean tables instead of pasted ASCII blocks
- explicit source notes where numbers matter
- banker-readable prose, not placeholder text

### Step 4: Keep the file lineage clean

If data came from an Excel model or analysis pack, say so in the document or delivery note.

If the user also wants a PDF, finish the Word file first, then hand off to `pdf-deliverable`.

## Output standard

Deliver:

1. a `.docx`
2. a short summary of what the document contains
3. any open assumptions or numbers still requiring verification

## Quality checklist

- the final artifact is a real `.docx`, not markdown renamed by hand
- headings and tables are readable in Word
- numbers match the underlying plugin output
- the narrative is concise and banker-usable
- no fake citations or placeholder sections remain
