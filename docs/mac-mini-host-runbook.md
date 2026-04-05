# Mac Mini Host Runbook

## Purpose

This runbook captures the host-level cleanup that stabilized OpenClaw on the macOS validation machine after the plugin layer had already been confirmed healthy.

Use it when the bundles themselves load correctly, but the host keeps producing background noise such as:

- `session file locked`
- `remote bin probe timed out`
- `pricing bootstrap failed: TypeError: fetch failed`
- repeated gateway or node-host warnings that are not tied to actual plugin failures

This is a host-operations note, not a plugin feature change.

## Symptoms

Typical signals that the problem is in the host runtime rather than the bundle:

- `openclaw plugins inspect` shows the plugin as `loaded`
- `openclaw skills list` still shows the financial skills as `ready`
- real workflows intermittently work, but `gateway.err.log` keeps collecting unrelated warnings
- a legacy default agent or session file keeps getting reused

## Root Causes Seen On Host A

During validation, the macOS host had four overlapping causes of noise:

1. Legacy `main` session history

An oversized historical session file kept polluting the default agent path and made background behavior harder to reason about.

2. Remote gateway probe state

The host config still contained a `gateway.remote` block, which caused `skills-remote` to keep probing a remote node path that was not needed for local bundle validation.

3. LaunchAgent environment mismatch

The gateway LaunchAgent environment was missing locale variables, and it also carried a problematic `NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem` value. In practice, that combination was enough to make Node's startup-time `fetch()` to the OpenRouter pricing catalog fail in the service context even though the same fetch worked from an interactive shell.

4. Low-value warning paths in OpenClaw runtime

Two warnings were noisy but not operationally meaningful for local plugin use on this host:

- `pricing bootstrap failed`
- `remote bin probe timed out`

Those warnings came from OpenClaw runtime files, not from the AIGroup plugins.

## Files Touched

Host-side config and state files:

- `~/.openclaw/openclaw.json`
- `~/.openclaw/agents/main/sessions/sessions.json`
- `~/.openclaw/agents/main/sessions/*.jsonl`
- `~/Library/LaunchAgents/ai.openclaw.gateway.plist`
- `~/.openclaw/logs/gateway.err.log`
- `~/.openclaw/logs/node.err.log`

Runtime files patched on the host:

- `~/.npm-global/lib/node_modules/openclaw/dist/usage-format-DD-9lWqe.js`
- `~/.npm-global/lib/node_modules/openclaw/dist/skills-remote-fYLkhhDd.js`

## Recovery Procedure

### 1. Confirm the bundles are healthy first

Do not treat host noise as a plugin bug until these pass:

```bash
openclaw plugins inspect aigroup-financial-services-openclaw
openclaw plugins inspect aigroup-lead-discovery-openclaw
openclaw skills list
```

If the plugins are loaded and the core skills are `ready`, move on to host cleanup.

### 2. Remove stale local session baggage

Back up and disable the oversized historical `main` session files instead of deleting them outright.

Recommended pattern:

```bash
cp ~/.openclaw/agents/main/sessions/<session>.jsonl \
  ~/.openclaw/agents/main/sessions/<session>.jsonl.bak-<timestamp>

mv ~/.openclaw/agents/main/sessions/<session>.jsonl \
  ~/.openclaw/agents/main/sessions/<session>.jsonl.disabled-<timestamp>
```

If needed, also inspect:

```bash
~/.openclaw/agents/main/sessions/sessions.json
```

### 3. Remove unneeded remote gateway probing

Unset `gateway.remote` if the host is meant to validate local bundles only:

```bash
openclaw config unset gateway.remote
```

Then restart the gateway.

This was enough to stop the recurring `skills-remote` warning caused by remote-node probing in the original validation setup.

### 4. Fix the LaunchAgent environment

Inspect the LaunchAgent:

```bash
plutil -p ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

Ensure the environment contains:

```text
LANG=C.UTF-8
LC_ALL=C.UTF-8
LC_CTYPE=C.UTF-8
```

Remove this if present:

```text
NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem
```

That certificate override caused Node service-context `fetch()` calls to fail on this host, even though interactive fetches worked.

### 5. Fully restart the gateway service

After editing the LaunchAgent, reload it instead of relying on a soft restart alone:

```bash
openclaw gateway restart
```

If the service still appears to carry the old environment, unload and start it again:

```bash
openclaw gateway start
```

Then inspect:

```bash
openclaw gateway status
launchctl print gui/$(id -u)/ai.openclaw.gateway
```

### 6. Clear logs and retest

```bash
: > ~/.openclaw/logs/gateway.err.log
: > ~/.openclaw/logs/node.err.log
```

Then rerun:

```bash
openclaw plugins inspect aigroup-financial-services-openclaw
openclaw plugins inspect aigroup-lead-discovery-openclaw
openclaw skills list
```

If the logs stay clean after those checks, the host is stable enough for normal bundle use.

## Runtime Noise Suppression

If the host is still clean functionally but OpenClaw runtime keeps logging warnings that do not affect plugin execution, a temporary host-local patch may be appropriate.

This was used during validation for:

- `usage-format-DD-9lWqe.js`
- `skills-remote-fYLkhhDd.js`

The goal was narrow:

- keep startup-time pricing fetch failures from polluting `gateway.err.log`
- keep disconnected remote-bin probes from polluting `gateway.err.log`

Important:

- this is a host-local operational patch
- it is not a substitute for upstream fixes
- it may be overwritten by a future OpenClaw upgrade

Always keep a backup before patching:

```bash
cp <runtime-file> <runtime-file>.bak-<reason>
```

## After OpenClaw Upgrade

If OpenClaw is upgraded on the host, assume the local runtime patches may have been overwritten.

Use this post-upgrade sequence:

1. Confirm the upgrade actually completed:

```bash
openclaw --version
```

2. Restart the gateway once:

```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

3. Clear the host logs:

```bash
python3 -c 'from pathlib import Path; home = Path.home(); [(home / ".openclaw/logs/gateway.err.log").write_text(""), (home / ".openclaw/logs/node.err.log").write_text("")]'
```

4. Re-run the banker smoke path:

```bash
openclaw plugins inspect aigroup-lead-discovery-openclaw
openclaw plugins inspect aigroup-financial-services-openclaw
openclaw skills list
```

5. If these warnings come back:

- `pricing bootstrap failed: TypeError: fetch failed`
- `remote bin probe timed out`

re-apply the host-local runtime patch to these files:

- `~/.npm-global/lib/node_modules/openclaw/dist/usage-format-DD-9lWqe.js`
- `~/.npm-global/lib/node_modules/openclaw/dist/skills-remote-fYLkhhDd.js`

Recommended minimal patch:

- change the pricing bootstrap line from `log.warn(...)` to `log.info(...)`
- change the remote bin probe timeout line from `log.warn(...)` to `log.info(...)`

This keeps the warnings from polluting `gateway.err.log` while preserving runtime behavior.

6. Restart the gateway again after patching:

```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

7. Clear logs one more time and rerun a real plugin call:

```bash
openclaw agent --agent aigroup-clean --session-id post-update-check -m "Use the client-initial-screening skill for 华为技术有限公司. Return company summary, reason_to_contact, risk_flags, and next_steps."
```

If the call succeeds and the logs remain quiet, the host is back in the expected steady state.

## Validation Standard

After cleanup, all of the following should be true:

- `gateway.err.log` is empty or quiet after a fresh restart
- `node.err.log` is empty or quiet after a fresh restart
- `aigroup-financial-services-openclaw` is still `loaded`
- `aigroup-lead-discovery-openclaw` is still `loaded`
- core skills such as `dcf-model`, `datapack-builder`, `client-initial-screening`, and `weekly-lead-watchlist` remain `ready`

## Known Tradeoff

This runbook prioritizes operational stability for a real host over strict purity of runtime state. If you patch OpenClaw runtime files locally to suppress non-functional warnings, record those edits and expect to re-apply or discard them after future OpenClaw upgrades.
