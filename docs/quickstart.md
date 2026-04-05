# Quickstart

## Recommended Installation Order

Install the AIGroup intelligence layer first:

```bash
openclaw plugins install aigroup-lead-discovery-openclaw
```

Then install the financial workflow layer:

```bash
openclaw plugins install aigroup-financial-services-openclaw
```

If OpenClaw asks you to restart the gateway after installation, do that before testing.

## 30-Second Self-Check

```bash
openclaw plugins inspect aigroup-financial-services-openclaw
openclaw skills list
```

Expected results:

- the plugin shows `Status: loaded`
- the bundle format shows `claude`
- financial skills such as `dcf-model`, `lbo-model`, `datapack-builder`, or `pitch-deck` appear in `openclaw skills list`

## Recommended Trust Pinning

To remove the `plugins.allow is empty` warning, pin the two suite plugins explicitly:

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

After updating config, restart the gateway and re-run:

```bash
openclaw plugins inspect aigroup-financial-services-openclaw
```

## What This Plugin Does

Use this plugin for:

- financial modeling
- valuation workflows
- investment-banking deliverables
- workbook and presentation generation

Do not expect this plugin to be your default data-source layer. By design, the published package keeps upstream HTTP MCP connectors disabled by default.

## Recommended Pairing

Use it together with:

- `aigroup-lead-discovery-openclaw`
- `aigroup-fmp-mcp`
- `aigroup-market-mcp`
- `aigroup-finnhub-mcp`

That gives you a cleaner split:

- lead discovery plugin = intelligence and research inputs
- financial services plugin = analysis and deliverables
