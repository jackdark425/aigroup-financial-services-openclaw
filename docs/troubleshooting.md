# Troubleshooting

Use this page if the suite installs but your first model or deliverable run does not behave as expected.

## Healthy Install Checklist

Run:

```bash
openclaw plugins inspect aigroup-financial-services-openclaw
openclaw skills list
```

Healthy results usually look like this:

- plugin status shows `loaded`
- plugin id shows `aigroup-financial-services-openclaw`
- skills such as `dcf-model`, `lbo-model`, or `datapack-builder` appear as `ready`

## Healthy First Result

A successful first run normally includes:

- a clear task-specific summary
- an assumptions section if source data is incomplete
- a model, workbook, or deliverable-oriented output path

If you use `datapack-builder`, expect an answer shaped roughly like:

```text
Deliverable summary
- [what was created]

Business context
- [company summary and why it matters]

Assumptions
- [explicit placeholders or estimated inputs]

Next steps
- [what to refine next]
```

## If The Plugin Installed But Skills Do Not Appear

Check:

- the plugin was installed under the correct id
- OpenClaw gateway was restarted after install
- your OpenClaw config does not block the plugin via `plugins.allow`

Recommended trust pinning:

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

## If Financial Data Connectors Are Missing

That can be normal.

This suite is now optimized to install cleanly without the original 11 upstream financial HTTP connectors enabled by default. The intended stack is:

- `aigroup-lead-discovery-openclaw` for intelligence and lead context
- AIGroup data services such as `aigroup-fmp-mcp`, `aigroup-market-mcp`, and `aigroup-finnhub-mcp`
- `aigroup-financial-services-openclaw` for models and deliverables

## If A Model Uses Placeholder Assumptions

That usually means exact public-company inputs were incomplete.

The correct operator flow is:

1. gather lead or company context first
2. confirm the target entity
3. pass the screened context into `datapack-builder`, `dcf-model`, or another downstream skill
4. refine assumptions after the first pass

## If Terminal Invocation Fails

Start with a simple call:

```bash
openclaw agent --agent main --session-id banker-demo-102 -m "Use datapack-builder to create a first-pass datapack for 华为技术有限公司 based on available public company context. Include key business description, headline financial context, major assumptions, and a concise deliverable summary."
```

If your environment uses a different default agent, replace `main` with your agent id.

## Recommended Escalation Order

1. Confirm plugin install and `loaded` status.
2. Confirm skills show as `ready`.
3. Retry with the copy-paste example prompt from [Example Prompts](./example-prompts.md).
4. Add lead-discovery context and rerun.
5. If needed, reinstall the plugin from Hub and retry.
