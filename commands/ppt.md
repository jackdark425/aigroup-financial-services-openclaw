---
description: Create or refresh a PowerPoint deliverable from financial-services outputs
argument-hint: "[company, slide ask, or deck task]"
---

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

Use the host's PPT stack when available:

- `pptx-generator`
- `ppt-editing-skill`
- `ppt-orchestra-skill`
- `slide-making-skill`

### Step 4: Deliver

Provide:

1. the `.pptx`
2. a short summary of slide coverage
3. any flagged numbers or placeholders that still need user review
