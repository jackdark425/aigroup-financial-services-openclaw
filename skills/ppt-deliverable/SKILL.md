---
name: ppt-deliverable
description: Turn financial-services outputs into slides or a PowerPoint deck. Use when the user wants a strip, teaser, pitch material, refreshed deck, or a banker-ready .pptx generated from this plugin.
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Modified by AIGroup for OpenClaw compatibility and banker workflow packaging. Not an official Anthropic release. -->


# PPT Deliverable

Use this skill when the final output should be a PowerPoint artifact.

## Best-fit cases

- single-slide strip profile
- teaser or process letter deck
- refreshed deck after number changes
- customer or deal summary slides
- packaging analysis into presentation-ready pages

## Tooling preference

Route PPT generation through the host's MiniMax PPT stack. On `macmini`, that means:

- `pptx-generator` for create/read flows
- `slide-making-skill` for single-slide implementation details
- `ppt-orchestra-skill` for multi-slide planning
- `ppt-editing-skill` for editing existing decks safely

If that PPT stack is not exposed on the host, fall back to the standard `pptx` workflow already available in the environment.

> **Note on removed path (0.1.17)** — versions 0.1.13 through 0.1.16 shipped an embedded `aigroup-mdtopptx-mcp` stdio server that converted markdown to `.pptx` via `pptxgenjs` with a banker template derived from the NVIDIA sample. In practice the MiniMax host PPT skill suite produces noticeably better banker decks, so 0.1.17 removed the embedded server to let routing converge on a single good path. Archive of the `scripts/mdtopptx/` directory is retained in the repository for reference but is no longer registered in `.mcp.json`.

Do not treat shell discovery as the source of truth. Avoid `which`, PATH checks, or binary-name probes for PPT routing because these capabilities may exist only as host skills.

The core rule is:

- ship a real `.pptx`
- preserve template structure when one exists
- keep slides concise and presentation-native
- prefer editable text/table/chart objects over flattened screenshots

Preferred routing order:

1. host MiniMax PPT skills — `pptx-generator`, `slide-making-skill`, `ppt-orchestra-skill`, `ppt-editing-skill`
2. environment `pptx` fallback when the MiniMax stack is not exposed

## Workflow

### Step 1: Decide whether this is create vs refresh

Use the smallest path that matches the job:

- new deck / new slide
- refresh an existing deck
- fill a template

### Step 2: Start from existing plugin skills

Prefer these building blocks:

- `strip-profile`
- `teaser`
- `pitch-deck`
- `deck-refresh`
- `process-letter`
- `competitive-analysis`
- `customer-analysis-pack`

If the user already has source tables in Excel or text in Word/markdown, consume those as inputs rather than recreating the analysis.

If the source is already markdown or markdown-like analysis output, feed it to the host's MiniMax PPT skills (`pptx-generator` / `slide-making-skill`) rather than trying to script the conversion manually — MiniMax preserves banker-style layout far better than a hand-rolled pptxgenjs pipeline.

### Step 3: Build the deck

Requirements:

- use real slide structure, not giant paragraph dumps
- keep numbers synced with underlying models
- match the provided template or established banker style
- use tables/charts where they communicate better than prose
- keep the output editable in PowerPoint / Keynote
- do not stop just because no same-named PPT executable exists in the shell

### Step 4: Review before delivery

Check:

- no text overflow
- slide titles are meaningful
- numbers and dates are internally consistent
- all placeholders are removed

If the user also needs a PDF review copy, generate the PPT first, then hand off to `pdf-deliverable`.

## Output standard

Deliver:

1. a `.pptx`
2. a quick description of slide coverage
3. any data points that still need verification before external use

## Quality checklist

- final artifact is a real `.pptx`
- the final artifact remains editable rather than being flattened into image-only slides
- slides are presentation-ready, not document pages pasted into PowerPoint
- formatting is consistent with the source template or banker style
- charts/tables reflect current numbers
- no placeholder or draft scaffolding remains
