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

Prefer the embedded markdown-first PPT path when the source material is already in markdown, structured analysis notes, or a model-written banker memo:

- `aigroup-mdtopptx-mcp__markdown_to_pptx`

Then prefer the host's actual PPT stack when available. On `macmini`, that means:

- `pptx-generator` for create/read flows
- `ppt-editing-skill` for editing existing decks safely
- `ppt-orchestra-skill` for multi-slide planning
- `slide-making-skill` for single-slide implementation details

If that PPT stack is not exposed on the host, fall back to the standard `pptx` workflow already available in the environment.

This plugin now ships an embedded `aigroup-mdtopptx-mcp` stdio server for the stable case where the model has already produced markdown and now needs a real, editable `.pptx` with banker-style layout.

This is an optional acceleration path. If the host already has compatible PPT skills installed, use them. Do not require separate MiniMax setup just to produce slides.

Do not treat shell discovery as the source of truth. Avoid `which`, PATH checks, or binary-name probes for PPT routing because these capabilities may exist only as host skills.

The core rule is:

- ship a real `.pptx`
- preserve template structure when one exists
- keep slides concise and presentation-native
- prefer editable text/table/chart objects over flattened screenshots

Preferred routing order:

1. `aigroup-mdtopptx-mcp__markdown_to_pptx` for markdown-first banker deck generation
2. host PPT skills such as `pptx-generator`, `ppt-editing-skill`, `ppt-orchestra-skill`, and `slide-making-skill`
3. environment `pptx` fallback only when neither of the above is clearly available

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

If the source is already markdown or markdown-like analysis output, strongly prefer `aigroup-mdtopptx-mcp`.

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
