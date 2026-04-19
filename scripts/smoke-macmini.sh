#!/usr/bin/env bash
# smoke-macmini.sh — from a laptop with `ssh jackmac-mini` access, run a
# non-interactive smoke that goes: uninstall → install both plugins →
# preflight both → plugins list → ping main agent → report.
#
# Exits 0 only if every phase reports OK. Exit != 0 means the macmini is
# not in a ready state for banker workflow — inspect stderr output for
# which phase failed, then consult docs/smoke-test-macmini.md.
#
# Does NOT run an actual banker analysis turn — that's a separate concern
# (see docs/smoke-test-macmini.md Step 6). This script only verifies the
# install + configuration surface.

set -u
SSH_TARGET="${SSH_TARGET:-jackmac-mini}"
EXIT=0

_ssh() {
  ssh -o BatchMode=yes "$SSH_TARGET" "$@"
}

section() {
  echo
  echo "==== $* ===="
}

section "1/5 · fresh install both plugins"
_ssh '
export PATH=/opt/homebrew/bin:/Users/jackdong/.npm-global/bin:$PATH
openclaw plugins uninstall aigroup-financial-services-openclaw --force 2>/dev/null | tail -1
openclaw plugins uninstall aigroup-lead-discovery-openclaw --force 2>/dev/null | tail -1
find /var/folders -name "openclaw-clawhub-package-*" -type d 2>/dev/null | xargs rm -rf
openclaw plugins install clawhub:aigroup-lead-discovery-openclaw@latest 2>&1 | tail -2
openclaw plugins install clawhub:aigroup-financial-services-openclaw@latest 2>&1 | tail -2
' || EXIT=1

section "2/5 · versions"
_ssh '
for p in aigroup-lead-discovery-openclaw aigroup-financial-services-openclaw; do
  v=$(python3 -c "import json; print(json.load(open(\"/Users/jackdong/.openclaw/extensions/$p/.claude-plugin/plugin.json\"))[\"version\"])" 2>/dev/null || echo "MISSING")
  echo "  $p: $v"
done
' || EXIT=1

section "3/5 · preflight both"
_ssh '
bash ~/.openclaw/extensions/aigroup-lead-discovery-openclaw/scripts/preflight.sh
bash ~/.openclaw/extensions/aigroup-financial-services-openclaw/scripts/preflight.sh
' || { echo "preflight failed" >&2; EXIT=1; }

section "4/5 · restart gateway"
_ssh 'launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway 2>&1 | head -1' || true
sleep 5

section "5/5 · ping main — confirm skill visibility + model"
_ssh '
export PATH=/opt/homebrew/bin:/Users/jackdong/.npm-global/bin:$PATH
rm -f /tmp/smoke-macmini-ping.json
openclaw agent --agent main --thinking minimal --json --message "OK" > /tmp/smoke-macmini-ping.json 2>/dev/null
python3 -c "
import json,sys
txt = open(\"/tmp/smoke-macmini-ping.json\").read()
depth, end = 0, None
for i,c in enumerate(txt):
    if c==\"{\": depth+=1
    elif c==\"}\":
        depth-=1
        if depth==0: end=i+1; break
d = json.loads(txt[:end])
sp = d[\"result\"][\"meta\"][\"systemPromptReport\"]
provider = sp.get(\"provider\")
model = sp.get(\"model\")
print(f\"  provider={provider} model={model}\")
if provider != \"minimax-cn\" or model != \"MiniMax-M2.7\":
    print(\"  WARN: expected minimax-cn/MiniMax-M2.7\", file=sys.stderr)
    sys.exit(2)
sk = [s.get(\"name\",\"?\") for s in sp.get(\"skills\", {}).get(\"entries\", [])]
missing = []
for want in [\"cn-client-investigation\",\"cn-lead-safety\",\"data-quality-audit\",\"ppt-deliverable\",\"customer-investigation\"]:
    present = want in sk
    print(f\"  {want}: {present}\")
    if not present: missing.append(want)
if missing:
    print(f\"  WARN: missing skills: {missing}\", file=sys.stderr)
    sys.exit(3)
"
' || EXIT=1

section "summary"
if [ $EXIT -eq 0 ]; then
  echo "SMOKE PASS — macmini ready for banker workflow."
else
  echo "SMOKE FAIL (exit $EXIT) — see docs/smoke-test-macmini.md for troubleshooting." >&2
fi
exit $EXIT
