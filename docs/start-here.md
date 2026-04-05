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
- customer investigation
- outreach triggers
- first-meeting briefing

Use `aigroup-financial-services-openclaw` first when you need:

- customer analysis packs
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
Use the customer-investigation skill for 华为技术有限公司.
Generate a Chinese internal customer investigation report covering company identity, business overview, risk review, banking entry points, and next steps.
```

Financial-services first run:

```text
Use the customer-analysis-pack skill for 华为技术有限公司.
Turn the investigation memo into a Chinese internal customer analysis pack with financial snapshot, banking product fit, risks, and next actions.
```

## 6. First End-to-End Flow

Step 1:

```text
Use the customer-investigation skill for 华为技术有限公司.
Generate a Chinese internal customer investigation report covering company identity, business overview, risk review, banking entry points, and next steps.
```

Step 2:

```text
Use the customer-analysis-pack skill for 华为技术有限公司.
Turn the investigation memo into a Chinese internal customer analysis pack, then produce a workbook-backed deliverable if the facts are sufficient.
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
