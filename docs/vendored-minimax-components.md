# Vendored MiniMax Components

This plugin vendors two MiniMax-origin office skills directly into the public repository:

- `skills/minimax-docx`
- `skills/minimax-xlsx`

## Why they are included

The goal is to make Word and Excel output work immediately after installing
`aigroup-financial-services-openclaw`, instead of forcing every host to
preinstall a separate office plugin stack.

## Source and attribution

These components were copied from a verified MiniMaxAI skill installation on
`macmini` and preserved with attribution:

- `minimax-docx` includes a standalone MIT `LICENSE` file
- `minimax-xlsx` declares `license: MIT` in its `SKILL.md` frontmatter

This repository keeps the original skill names so operators can see what was
vendored and where it came from.

## What is not vendored

This repository does not currently vendor the MiniMax / PPT stack or MiniMax PDF
skill into the public package. Those remain host-dependent because their
redistribution posture is less clear or requires separate review.

## Operator guidance

- Install this plugin alone if you need Word and Excel support immediately.
- If your host already has equivalent office skills, that is fine; the plugin
  can still use compatible host capabilities.
- For richer PPT or PDF workflows, add compatible host skills separately.
