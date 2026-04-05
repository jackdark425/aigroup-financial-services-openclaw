# Which Suite To Use

Use this page when you are not sure whether to start with the lead-discovery suite or the financial-services suite.

## Quick Rule

Start with `aigroup-lead-discovery-openclaw` if you are still identifying the target, scanning external signals, or deciding whether a banker should engage.

Start with `aigroup-financial-services-openclaw` if you already know the target company and need a model, workbook, datapack, or presentation-ready output.

## Decision Table

| If you need to... | Start here |
| --- | --- |
| confirm company identity | `aigroup-lead-discovery-openclaw` |
| scan public events and outreach triggers | `aigroup-lead-discovery-openclaw` |
| prepare a first meeting briefing | `aigroup-lead-discovery-openclaw` |
| rank a weekly watchlist | `aigroup-lead-discovery-openclaw` |
| build a datapack | `aigroup-financial-services-openclaw` |
| build a DCF or LBO model | `aigroup-financial-services-openclaw` |
| create a deck or financial deliverable | `aigroup-financial-services-openclaw` |
| turn screened lead context into analysis output | `aigroup-financial-services-openclaw` after lead-discovery |

## Recommended Workflow

For most banker workflows, the best order is:

1. `aigroup-lead-discovery-openclaw`
2. `aigroup-financial-services-openclaw`

That means:

1. screen the target
2. confirm why the account matters
3. identify the main risks and next steps
4. move into datapacks, models, or deliverables

## Best First Prompt For Each Suite

Lead-discovery:

```text
Use the client-initial-screening skill for 华为技术有限公司.
Return company summary, reason_to_contact, risk_flags, and next_steps.
```

Financial-services:

```text
Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on available public company context.
Include key business description, headline financial context, major assumptions, and a concise deliverable summary.
```

## Related Docs

- [Quickstart](./quickstart.md)
- [Example Prompts](./example-prompts.md)
- [Troubleshooting](./troubleshooting.md)
