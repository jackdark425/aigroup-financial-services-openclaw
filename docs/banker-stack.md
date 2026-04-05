# AIGroup Banker Stack

## What To Install

Install the stack as two OpenClaw suite plugins:

```bash
openclaw plugins install aigroup-lead-discovery-openclaw
openclaw plugins install aigroup-financial-services-openclaw
```

Recommended roles:

- `aigroup-lead-discovery-openclaw`: company intelligence, customer screening, event scanning, pre-meeting briefing
- `aigroup-financial-services-openclaw`: modeling, analysis, datapacks, decks, financial deliverables

## Recommended MCP Layer

Use these AIGroup data services alongside the two suite plugins:

- `aigroup-fmp-mcp`
- `aigroup-market-mcp`
- `aigroup-finnhub-mcp`
- `Tianyancha`
- `PrimeMatrixData`

Practical split:

- lead-discovery plugin: intelligence entry point
- AIGroup MCPs: data retrieval layer
- financial-services plugin: analysis and deliverable layer

## Recommended Trust Pinning

To remove the default `plugins.allow is empty` warning and explicitly trust only the suite plugins, add this to your OpenClaw config:

```json
{
  "plugins": {
    "allow": [
      "aigroup-lead-discovery-openclaw",
      "aigroup-financial-services-openclaw"
    ]
  }
}
```

Then restart the gateway.

## 30-Second Verification

```bash
openclaw plugins inspect aigroup-lead-discovery-openclaw
openclaw plugins inspect aigroup-financial-services-openclaw
openclaw skills list
```

Expected results:

- both plugins show `Status: loaded`
- both plugins show bundle format `claude`
- lead-discovery skills such as `client-initial-screening` appear
- financial skills such as `dcf-model` or `datapack-builder` appear

## First End-to-End Example

Step 1: use the lead-discovery suite to screen a target account.

Example prompt:

```text
Use the client-initial-screening skill for 华为技术有限公司.
Return company summary, reason_to_contact, risk_flags, and next_steps.
```

Step 2: use the financial-services suite to turn the output into a deliverable.

Example prompt:

```text
Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on the screening summary and available public company context.
```

Recommended operator flow:

1. Run lead-discovery first.
2. Confirm target identity and risk context.
3. Pass the screened company into financial-services.
4. Generate the first workbook or deck deliverable.

## Current Best-Practice Usage

For normal users, prefer installing suites rather than individual skills.

That means:

- install `aigroup-lead-discovery-openclaw`
- install `aigroup-financial-services-openclaw`
- do not ask users to manually assemble skill bundles unless they are advanced operators

## Related Docs

- [Quickstart](./quickstart.md)
- [Test Report](./test-report.md)
