# Start Here

This is the fastest path to get the AIGroup banker stack working in OpenClaw.

## 1. Install The Two Suite Plugins

```bash
openclaw plugins install aigroup-lead-discovery-openclaw
openclaw plugins install aigroup-financial-services-openclaw
```

## 2. Pin Trust Once

Add this to your OpenClaw config if you want to remove the default plugin trust warning:

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

## 3. Verify Install

```bash
openclaw plugins inspect aigroup-lead-discovery-openclaw
openclaw plugins inspect aigroup-financial-services-openclaw
openclaw skills list
```

Healthy results:

- both plugins show `loaded`
- lead-discovery skills such as `client-initial-screening` appear as `ready`
- financial-services skills such as `datapack-builder` or `dcf-model` appear as `ready`

## 4. Know Which Suite To Start With

Use `aigroup-lead-discovery-openclaw` first when you need:

- company identity confirmation
- public-event scanning
- outreach triggers
- first-meeting briefing

Use `aigroup-financial-services-openclaw` first when you need:

- datapacks
- DCF or LBO models
- decks
- financial deliverables

For most workflows, the best order is:

1. lead-discovery
2. financial-services

## 5. Copy-Paste First Prompt

Lead-discovery first run:

```text
Use the client-initial-screening skill for 华为技术有限公司.
Return company summary, reason_to_contact, risk_flags, and next_steps.
```

Financial-services first run:

```text
Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on available public company context.
Include key business description, headline financial context, major assumptions, and a concise deliverable summary.
```

## 6. First End-to-End Flow

Step 1:

```text
Use the client-initial-screening skill for 华为技术有限公司.
Return company summary, reason_to_contact, risk_flags, and next_steps.
```

Step 2:

```text
Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on the screening summary and available public company context.
Include a short assumptions section and produce a workbook-ready deliverable summary.
```

## 7. If Something Looks Wrong

Check these first:

- plugin status is `loaded`
- required skills show as `ready`
- your OpenClaw config contains the needed credentials for external data services
- you are starting from the example prompts before trying custom prompts

## 8. Next Docs

- [Quickstart](./quickstart.md)
- [Banker Stack](./banker-stack.md)
- [Example Prompts](./example-prompts.md)
- [Troubleshooting](./troubleshooting.md)
- [Which Suite To Use](./which-suite-to-use.md)
