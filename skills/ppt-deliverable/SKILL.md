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

Prefer the host's actual PPT stack when available. On `macmini`, that means:

- `pptx-generator` for create/read flows
- `ppt-editing-skill` for editing existing decks safely
- `ppt-orchestra-skill` for multi-slide planning
- `slide-making-skill` for single-slide implementation details

If that PPT stack is not exposed on the host, fall back to the standard `pptx` workflow already available in the environment.

This is an optional acceleration path. If the host already has compatible PPT skills installed, use them. Do not require separate MiniMax setup just to produce slides.

Do not treat shell discovery as the source of truth. Avoid `which`, PATH checks, or binary-name probes for PPT routing because these capabilities may exist only as host skills.

The core rule is:

- ship a real `.pptx`
- preserve template structure when one exists
- keep slides concise and presentation-native

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

### Step 3: Build the deck

Requirements:

- use real slide structure, not giant paragraph dumps
- keep numbers synced with underlying models
- match the provided template or established banker style
- use tables/charts where they communicate better than prose
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
- slides are presentation-ready, not document pages pasted into PowerPoint
- formatting is consistent with the source template or banker style
- charts/tables reflect current numbers
- no placeholder or draft scaffolding remains
