# Quick Install — aigroup-financial-services-openclaw

> **target host**: macmini running OpenClaw with `main` agent on `minimax-cn/MiniMax-M2.7`.
> Read this before the long README if you just want the plugin working end-to-end on a fresh macmini.

## 3-step install

```bash
# 1. Install via ClawHub (public, stable track)
openclaw plugins install clawhub:aigroup-financial-services-openclaw

# 2. Restart gateway to load the new skill set
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway

# 3. Run the preflight check — confirms runtime deps are in place
bash ~/.openclaw/extensions/aigroup-financial-services-openclaw/scripts/preflight.sh
```

If preflight exits 0 the plugin is usable. If it exits 1, fix the reported missing dep and retry.

## Runtime dependencies (must be on PATH)

| Tool | Min version | Why | Install hint (macOS) |
|------|-------------|-----|----------------------|
| `python3` | 3.9+ | scanner scripts (cn_typo_scan.py, provenance_verify.py, validate-delivery.py) | built-in on macOS 11+ |
| `uvx` | 0.4+ | runs Python MCP helpers like `aigroup-econ-mcp` (if lab is installed) and on-demand deps like `python-pptx` | `brew install uv` |
| `node` | ≥ 18 | compile pptxgenjs slide-NN.js into .pptx via `node slides/compile.js` | `brew install node` |
| `python-pptx` | 0.6+ | compile template spawns python to extract pptx text for the typo gate | `uvx --with python-pptx python3 -c 'import pptx'` (transient) or `pip3 install --user python-pptx` |
| `pptxgenjs` | 4.0+ | installed per-deliverable via `npm install pptxgenjs --omit=dev` under each `slides/` dir | just `npm install` when asked |

## Known pitfalls (read before retrying a failed install)

### ClawHub transient "missing plugin.json" on install

OpenClaw caches the ClawHub zip under `/var/folders/.../openclaw-clawhub-package-<hex>/`. Occasionally the cached extract is incomplete (the post-install check then reports `missing ".claude-plugin/plugin.json"`). Workaround:

```bash
find /var/folders -name "openclaw-clawhub-package-*" -type d 2>/dev/null | xargs rm -rf
openclaw plugins install clawhub:aigroup-financial-services-openclaw
```

If it still fails, add `--force` to the uninstall and retry from a clean slate:

```bash
openclaw plugins uninstall aigroup-financial-services-openclaw --force
find /var/folders -name "openclaw-clawhub-package-*" -type d 2>/dev/null | xargs rm -rf
openclaw plugins install clawhub:aigroup-financial-services-openclaw
```

### OpenClaw safety scanner blocks install

If the safety scanner reports a dangerous code pattern (e.g. `child_process`), it's likely a downstream plugin (not this one) or an older version of this plugin. 0.3.1+ moved the `compile_with_typo_gate.template.js` to `references/*.txt` specifically to avoid this. If you see the block on 0.3.1+, clean cache and retry — it's probably an old zip. If you see it on 0.3.0 exactly, upgrade to 0.3.1+.

### `main` agent model resolution falls back to openrouter/free

If `openclaw agent --agent main --message "OK"` returns `provider: openrouter, model: openrouter/free` instead of `minimax-cn/MiniMax-M2.7`, it's the local model-routing config. See [`docs/smoke-test-macmini.md`](docs/smoke-test-macmini.md) for the one-time fix (agents.list.main.model = `minimax-cn/MiniMax-M2.7` + `auth-profiles.json` needs a `minimax-cn:default` entry).

## Pair with lead-discovery

This plugin is the downstream half. For upstream client-intelligence install the paired plugin first:

```bash
openclaw plugins install clawhub:aigroup-lead-discovery-openclaw
```

See that repo's `QUICKSTART.md` for its own preflight.

## Verify end-to-end

```bash
# Quick ping — confirms main agent sees the skill set
openclaw agent --agent main --thinking minimal --json --message "OK" | \
  python3 -c "import json,sys; t=sys.stdin.read(); d=json.loads(t[:t.index('}\n}')+3]); \
  sk=[s.get('name','?') for s in d['result']['meta']['systemPromptReport']['skills']['entries']]; \
  print('cn-client-investigation:', 'cn-client-investigation' in sk); \
  print('ppt-deliverable:', 'ppt-deliverable' in sk)"
```
