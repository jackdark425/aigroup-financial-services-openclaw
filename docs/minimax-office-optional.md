# MiniMax Office Optional Companion

This plugin now bundles MiniMax-derived Word and Excel skills, and can also work with compatible host office/document skills.

The office surface is now split between bundled and optional components.

If the user already has equivalent skills installed on their machine, they can continue using them; they do not need to remove them.

## What is bundled vs optional

Bundled in this plugin:

- `minimax-docx`
- `minimax-xlsx`

Still optional / host-provided:

- `minimax-pdf`
- `pptx-generator`
- `ppt-editing-skill`
- `ppt-orchestra-skill`
- `slide-making-skill`

## Why split it this way

The goal is convenience, not lock-in.

This repository focuses on banker workflows:

- analysis
- modeling
- packaging

The actual office execution surface may already exist on the host. If so, duplicating those skills adds maintenance overhead without much value.

## Verified host skills

Verified on `macmini`:

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

For Word and Excel, the plugin should prefer its bundled MiniMax-derived skills.

For PPT and PDF, the plugin should prefer compatible host-provided skills when available.

If those skills are not present, they should fall back to the standard environment workflows (`docx`, `xlsx`, `pptx`, `pdf`) instead of failing hard.

They should not rely on shell-level `which` checks, PATH probing, or same-name executable discovery to decide whether a host office skill exists. Skill routing and host exposure are the source of truth.

## Public-repo policy

For the public GitHub repository, the stable policy is:

- keep the banker workflow wrappers in this plugin
- vendor only the components whose redistribution posture is clear enough for a public repo
- document the compatible MiniMax skills clearly
- do not make PPT/PDF companion skills a required install step

This keeps the public plugin lean, easier to publish, and safer from license / provenance confusion.

## User guidance

If a user already has the relevant office skills installed:

- they do **not** need to install anything extra
- they can use this plugin directly

If a user does **not** have those office skills installed:

- Word and Excel are already covered by this plugin install
- PPT and PDF can still be added later via a compatible host office stack

## Suggested wording for users

You can treat the remaining host office skills as optional accelerators.

- Already installed on your host? Great, just use this plugin.
- Not installed? Word and Excel still work through bundled MiniMax-derived skills; PPT and PDF may use standard fallback paths until a richer host stack is added.
