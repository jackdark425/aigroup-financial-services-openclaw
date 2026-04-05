# Example Prompts

These are copy-paste examples for the AIGroup banker stack.

Install the suite first:

```bash
openclaw plugins install aigroup-lead-discovery-openclaw
openclaw plugins install aigroup-financial-services-openclaw
```

## Financial Services First Run

Use this when you want a fast deliverable from the financial-services suite:

```text
Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on available public company context.
Include key business description, headline financial context, major assumptions, and a concise deliverable summary.
```

## DCF Example

Use this when you want a first-pass valuation workflow:

```text
Use dcf-model for 华为技术有限公司 or its closest public comparable context.
Build a first-pass DCF-style output with clearly stated assumptions, valuation drivers, and a concise executive summary.
If exact public-company data is incomplete, say so and use reasonable placeholder assumptions explicitly.
```

## Datapack From Screened Lead

If you already screened the target with the lead-discovery suite, use this pattern:

```text
Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on this screening context:

- Company summary: [paste lead-discovery summary]
- Reason to contact: [paste lead-discovery reason]
- Risk flags: [paste lead-discovery risks]
- Next steps: [paste lead-discovery next steps]

Return a workbook-ready deliverable summary and list the main assumptions used.
```

## End-to-End Stack Example

Step 1 prompt for the lead-discovery suite:

```text
Use the client-initial-screening skill for 华为技术有限公司.
Return company summary, reason_to_contact, risk_flags, and next_steps.
```

Step 2 prompt for the financial-services suite:

```text
Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on the screening summary and available public company context.
Include a short assumptions section and produce a workbook-ready deliverable summary.
```

## CLI Example

```bash
openclaw agent --agent main --session-id banker-demo-002 -m "Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on available public company context. Include key business description, headline financial context, major assumptions, and a concise deliverable summary."
```

If your environment uses a non-default agent, replace `main` with your preferred agent id.
