---
name: pdf-deliverable
description: Package financial-services outputs as a PDF deliverable. Use when the user wants a final review copy, printable memo, presentation export, or shareable PDF derived from Word, Excel, PPT, or markdown outputs.
---

# PDF Deliverable

Use this skill when the user wants the final output delivered as PDF.

## Best-fit cases

- export a Word memo to PDF
- export a PPT deck to PDF for review
- package a summary note as PDF for sharing
- convert a finished analysis artifact into a stable, read-only format

## Tooling preference

Prefer the host's exact MiniMax PDF skill when available:

- `minimax-pdf`

If MiniMax PDF tooling is not exposed, fall back to the standard `pdf` workflow in the environment.

This is an optional acceleration path. If the host already has a compatible PDF skill installed, use it directly. Do not make MiniMax PDF a hard requirement.

The core rule is:

- PDF is usually the packaging layer, not the authoring layer
- create the source artifact first when possible
- preserve readable layout after conversion

## Workflow

### Step 1: Identify the source artifact

Prefer exporting from one of these:

- `word-deliverable`
- `excel-deliverable`
- `ppt-deliverable`
- existing plugin outputs that already exist as office files

If the user only provided markdown or notes, decide whether the PDF should come from Word-style packaging first.

### Step 2: Convert with the smallest stable path

Possible source types:

- `.docx` -> PDF
- `.pptx` -> PDF
- `.xlsx` -> PDF
- markdown / HTML -> PDF when no office source exists

### Step 3: Verify readability

Check:

- page breaks are sensible
- tables are not clipped
- slide exports are legible
- fonts and symbols survived conversion

## Output standard

Deliver:

1. a real `.pdf`
2. a short note describing what was packaged
3. the source artifact path or type, when relevant

## Quality checklist

- PDF opens cleanly
- text and tables are readable
- page count is sensible for the use case
- nothing important was lost during export
- the source file remains available if the user needs future edits
