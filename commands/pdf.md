---
description: Package a financial-services output as a PDF
argument-hint: "[source artifact or desired PDF output]"
---

# PDF Deliverable Command

Create a `.pdf` distribution copy from this plugin's outputs.

## Workflow

### Step 1: Identify source artifact

Prefer a finished source file:

- `.docx`
- `.pptx`
- `.xlsx`

If no source exists yet, decide whether the artifact should be produced first via Word, Excel, or PPT.

### Step 2: Load the skill

Use `skill: "pdf-deliverable"`.

### Step 3: Convert and verify

Prefer a host-routed `minimax-pdf` skill when available, but do not use `which`, PATH checks, or executable-name probing to decide that. If the host skill is not clearly exposed, continue with the standard `pdf` path.

Check readability after conversion:

- page breaks
- clipped tables
- legibility

### Step 4: Deliver

Provide:

1. the `.pdf`
2. a short note describing what was packaged
3. the source artifact used for conversion
