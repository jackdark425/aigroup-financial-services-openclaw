# Vendored MiniMax Components

This plugin vendors three MiniMax-origin office skills directly into the public repository:

- `skills/minimax-docx`
- `skills/minimax-xlsx`
- `skills/minimax-pdf`

## Why they are included

The goal is to make Word and Excel output work immediately after installing
`aigroup-financial-services-openclaw`, instead of forcing every host to
preinstall a separate office plugin stack.

## Source and attribution

These components were copied from a verified MiniMaxAI skill installation on
`macmini` and preserved with attribution:

- `minimax-docx` includes a standalone MIT `LICENSE` file
- `minimax-xlsx` declares `license: MIT` in its `SKILL.md` frontmatter
- `minimax-pdf` declares `license: MIT` in its `SKILL.md` frontmatter

This repository keeps the original skill names so operators can see what was
vendored and where it came from.

We are grateful to MiniMaxAI for publishing the original office-skill building
blocks that this plugin adapts for OpenClaw banker workflows.

## What is not vendored

This repository does not currently vendor the MiniMax / PPT stack into the
public package. Those remain host-dependent because their redistribution
posture is less clear or requires separate review.

## Operator guidance

- Install this plugin alone if you need Word, Excel, and PDF support immediately.
- If your host already has equivalent office skills, that is fine; the plugin
  can still use compatible host capabilities.
- For richer PPT workflows, add compatible host skills separately.
