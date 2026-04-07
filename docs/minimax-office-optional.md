# MiniMax Office Optional Companion

This plugin can work on its own, but it works better when the host already exposes compatible office/document skills.

These MiniMax-aligned office skills are treated as an **optional companion layer**, not a hard dependency.

If the user already has equivalent skills installed on their machine, they can skip this entirely.

## Why optional

The goal is convenience, not lock-in.

This repository focuses on banker workflows:

- analysis
- modeling
- packaging

The actual office execution surface may already exist on the host. If so, duplicating those skills adds maintenance overhead without much value.

## Recommended optional skills

Verified on `macmini`:

- Word: `minimax-docx`
- Excel: `minimax-xlsx`
- PDF: `minimax-pdf`
- PPT stack:
  - `pptx-generator`
  - `ppt-editing-skill`
  - `ppt-orchestra-skill`
  - `slide-making-skill`

## Default behavior

The plugin's office wrapper skills are:

- `word-deliverable`
- `excel-deliverable`
- `ppt-deliverable`
- `pdf-deliverable`

They should prefer the host-provided MiniMax / PPT office skills when available.

If those skills are not present, they should fall back to the standard environment workflows (`docx`, `xlsx`, `pptx`, `pdf`) instead of failing hard.

## Public-repo policy

For the public GitHub repository, the stable policy is:

- keep the banker workflow wrappers in this plugin
- document the compatible MiniMax skills clearly
- do not assume every user wants or needs the full MiniMax office stack
- do not make optional office skills a required install step

This keeps the public plugin lean, easier to publish, and safer from license / provenance confusion.

## User guidance

If a user already has the relevant office skills installed:

- they do **not** need to install anything extra
- they can use this plugin directly

If a user does **not** have those office skills installed and wants the best office output quality:

- they can install a compatible office skill set separately
- then use this plugin's office wrappers as the banker-oriented front door

## Suggested wording for users

You can treat MiniMax office skills as optional accelerators.

- Already installed on your host? Great, just use this plugin.
- Not installed? The plugin still works; you just lose the richer office-specific execution paths.
