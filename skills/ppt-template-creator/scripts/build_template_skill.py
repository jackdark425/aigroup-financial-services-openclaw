#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: Reusable PowerPoint template skill generated from {source_name}.
---

# {skill_name}

Template: `assets/template.pptx`

## Usage

- Use this skill when generating presentations that should match the supplied template.
- Copy the template and fill placeholders instead of building slides from scratch.
- Safe smoke-test path: confirm `assets/template.pptx` exists and generate a sample presentation before production use.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--summary-out", required=True)
    args = parser.parse_args()

    template = Path(args.template)
    output_dir = Path(args.output_dir)
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template, assets_dir / "template.pptx")

    skill_md = output_dir / "SKILL.md"
    skill_md.write_text(
        SKILL_TEMPLATE.format(skill_name=args.skill_name, source_name=template.name),
        encoding="utf-8",
    )

    summary_out = Path(args.summary_out)
    summary_out.parent.mkdir(parents=True, exist_ok=True)
    summary_out.write_text(
        "\n".join(
            [
                f"# {args.skill_name}",
                "",
                f"- Template source: {template}",
                f"- Generated skill dir: {output_dir}",
                "- Includes `SKILL.md` and `assets/template.pptx`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
