---
description: Create or refresh a PowerPoint deliverable from financial-services outputs
argument-hint: "[company, slide ask, or deck task]"
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Modified by AIGroup for OpenClaw compatibility and banker workflow packaging. Not an official Anthropic release. -->


# PPT Deliverable Command

Create a `.pptx` slide or deck from this plugin's analysis outputs.

## Workflow

### Step 1: Identify the ask

Decide whether the user wants:

- a new slide
- a new deck
- a template-filled deck
- a refresh to an existing presentation

### Step 2: Load the skill

Use `skill: "ppt-deliverable"`.

### Step 3: Build from existing financial-services work

Prefer:

- `strip-profile`
- `teaser`
- `pitch-deck`
- `deck-refresh`
- `process-letter`
- `customer-analysis-pack`

If the source is already markdown or a markdown-like analysis draft, route through:

- `aigroup-mdtopptx-mcp__markdown_to_pptx`

Use the host's PPT stack when available:

- `pptx-generator`
- `ppt-editing-skill`
- `ppt-orchestra-skill`
- `slide-making-skill`

Do not try to prove PPT availability with `which`, PATH checks, or binary-name probing. Treat `aigroup-mdtopptx-mcp` and host PPT skills as routed capabilities first, then fall back to the standard `pptx` workflow if they are not exposed.

### Step 4: Deliver

Provide:

1. the `.pptx`
2. a short summary of slide coverage
3. any flagged numbers or placeholders that still need user review
