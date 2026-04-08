# Apache 2.0 Compliance Notes

This repository adapts material from `anthropics/financial-services-plugins`.

## What we preserve

- The upstream Apache License 2.0 text is retained in the repository root.
- NOTICE-style attribution is preserved in the repository root [NOTICE](/Users/jackdark/kimi/ai/aigroup-financial-services-openclaw/NOTICE).
- Upstream origin is identified in README and other operator-facing docs.

## How modified files are marked

Upstream-derived `skills/*/SKILL.md` and `commands/*.md` files that were adapted
for OpenClaw distribution carry a prominent notice stating that they:

- are derived from `anthropics/financial-services-plugins`
- are distributed under Apache 2.0
- were modified by AIGroup for OpenClaw compatibility and banker workflow packaging
- are not official Anthropic releases

## Trademark posture

- Anthropic names, marks, and branding are referenced only to identify origin.
- This plugin must not be presented as an official Anthropic plugin.
- MiniMax names, marks, and branding are referenced only for attribution and compatibility.

## Bundled third-party components

This repository also bundles MiniMax-derived office skills under their stated MIT terms:

- `skills/minimax-docx`
- `skills/minimax-xlsx`
- `skills/minimax-pdf`

Their attribution remains in [NOTICE](/Users/jackdark/kimi/ai/aigroup-financial-services-openclaw/NOTICE).
Each vendored skill directory also includes an `ATTRIBUTION.md` file with source and packaging notes.

## Practical release checklist

- Keep `LICENSE` in the repository root.
- Keep `NOTICE` in the repository root.
- Preserve attribution when copying or adapting upstream-derived files.
- Keep modification notices in adapted source files.
- Avoid language or branding that implies Anthropic endorsement or official status.
