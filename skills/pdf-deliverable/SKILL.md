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

Prefer the bundled MiniMax-derived PDF skill shipped inside this plugin:

- `minimax-pdf`

If that bundled path is not available for any reason, fall back to the standard `pdf` workflow in the environment.

This plugin now vendors the MiniMax PDF skill as a convenience layer. If the host already has a compatible PDF skill installed, that is still fine, but a separate MiniMax PDF install should no longer be required for PDF output after this plugin is installed.

Do not use `which`, PATH checks, or shell executable discovery as the test for PDF capability. The host may expose PDF handling as a routed skill without a shell binary named `minimax-pdf`.

The core rule is:

- PDF is usually the packaging layer, not the authoring layer
- create the source artifact first when possible
- preserve readable layout after conversion

Preferred routing order:

1. `minimax-pdf` for design-sensitive, print-ready, or form-aware PDF output
2. environment `pdf` fallback when the bundled path is not clearly available

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
- if the source is already polished and needs strong visual packaging, prefer the bundled `minimax-pdf` route
- absence of a shell-level MiniMax executable is not itself a blocker

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
