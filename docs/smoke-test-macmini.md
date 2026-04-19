# macmini Smoke Test — fresh install → agent turn → three-gate pass

End-to-end recipe to take a clean `macmini` to a working banker-analysis stack with both public plugins installed, the `main` agent on `minimax-cn/MiniMax-M2.7`, and a real audit-ready deliverable generated. Each block is copy-paste-safe from a laptop that can `ssh jackmac-mini`.

## 1. Fresh install both public plugins

```bash
ssh jackmac-mini '
export PATH=/opt/homebrew/bin:/Users/jackdong/.npm-global/bin:$PATH

# Clean slate
openclaw plugins uninstall aigroup-financial-services-openclaw --force 2>/dev/null
openclaw plugins uninstall aigroup-lead-discovery-openclaw --force 2>/dev/null
find /var/folders -name "openclaw-clawhub-package-*" -type d 2>/dev/null | xargs rm -rf

# Install upstream (lead-discovery) first, then downstream (financial-services)
openclaw plugins install clawhub:aigroup-lead-discovery-openclaw
openclaw plugins install clawhub:aigroup-financial-services-openclaw

# Verify versions
for p in aigroup-lead-discovery-openclaw aigroup-financial-services-openclaw; do
  echo "  $p: $(grep version ~/.openclaw/extensions/$p/.claude-plugin/plugin.json)"
done
'
```

## 2. Preflight both plugins

```bash
ssh jackmac-mini '
bash ~/.openclaw/extensions/aigroup-lead-discovery-openclaw/scripts/preflight.sh
bash ~/.openclaw/extensions/aigroup-financial-services-openclaw/scripts/preflight.sh
'
```

Both must exit 0. If `uvx` or `node` missing on macmini, `brew install uv node`.

## 3. Verify main agent config

The `main` agent must use `minimax-cn/MiniMax-M2.7` and its workspace must be `~/.openclaw/workspace` (so host MiniMax PPT skills are visible). One-time fix if not already in place:

```bash
ssh jackmac-mini '
python3 -c "
import json
p = \"/Users/jackdong/.openclaw/openclaw.json\"
d = json.load(open(p))
for a in d[\"agents\"][\"list\"]:
    if a.get(\"id\") == \"main\":
        a[\"workspace\"] = \"/Users/jackdong/.openclaw/workspace\"
        a[\"model\"] = \"minimax-cn/MiniMax-M2.7\"
# Make sure main agent has an auth-profile for provider minimax-cn
with open(p, \"w\") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print(\"main agent config: workspace + model pinned\")
"

# Confirm minimax-cn:default profile exists in main agent auth-profiles
python3 -c "
import json, pathlib
p = pathlib.Path.home() / \".openclaw/agents/main/agent/auth-profiles.json\"
d = json.load(open(p))
if \"minimax-cn:default\" not in d.get(\"profiles\", {}):
    print(\"WARN: minimax-cn:default missing; copy minimax:cn profile and rename provider.\")
else:
    print(\"ok: minimax-cn:default profile present\")
"
'
```

## 4. Restart gateway

```bash
ssh jackmac-mini 'launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway'
sleep 5
```

## 5. Ping — verify skill visibility

```bash
ssh jackmac-mini '
export PATH=/opt/homebrew/bin:/Users/jackdong/.npm-global/bin:$PATH
rm -f /tmp/ping.json
openclaw agent --agent main --thinking minimal --json --message "OK" > /tmp/ping.json 2>/dev/null
python3 -c "
import json
txt = open(\"/tmp/ping.json\").read()
depth, end = 0, None
for i,c in enumerate(txt):
    if c==\"{\": depth+=1
    elif c==\"}\":
        depth-=1
        if depth==0: end=i+1; break
d = json.loads(txt[:end])
sp = d[\"result\"][\"meta\"][\"systemPromptReport\"]
print(\"provider:\", sp.get(\"provider\"), \"model:\", sp.get(\"model\"))
sk = [s.get(\"name\") or \"?\" for s in sp.get(\"skills\", {}).get(\"entries\", [])]
for want in [\"cn-client-investigation\", \"cn-lead-safety\", \"data-quality-audit\", \"ppt-deliverable\", \"customer-investigation\"]:
    print(f\"  {want}:\", want in sk)
"
'
```

All 5 skill names should print `True`. Provider must be `minimax-cn`, model `MiniMax-M2.7`.

## 6. End-to-end real analysis (smoke case: 五粮液 000858.SZ)

Full banker workflow with `main` agent using both plugins. See `companies/五粮液-stable/` under the research lab for the verified reference deliverable.

```bash
ssh jackmac-mini '
cat > /tmp/smoke_wuliangye.txt << "EOF"
给「五粮液 000858.SZ」做一份投行客户调研。先用 aigroup-lead-discovery-openclaw 产 intelligence MD，再用 aigroup-financial-services-openclaw 走 banker workflow + 20 页 PPTX。路径 ~/deliverables/wuliangye-smoke/。交付前用 validate-delivery.py 做 3-gate QA；跑完再用 data-quality-audit 做一次独立审计产 audit-report.md。
EOF

nohup python3 -c "
import subprocess, os
os.environ[\"PATH\"] = \"/opt/homebrew/bin:/Users/jackdong/.npm-global/bin:\" + os.environ.get(\"PATH\",\"\")
msg = open(\"/tmp/smoke_wuliangye.txt\").read()
with open(\"/tmp/smoke_wuliangye.json\",\"w\") as o, open(\"/tmp/smoke_wuliangye.err\",\"w\") as e:
    rc = subprocess.call([
        \"openclaw\",\"agent\",\"--agent\",\"main\",
        \"--message\",msg,\"--thinking\",\"high\",
        \"--timeout\",\"3600\",\"--json\",
    ], stdout=o, stderr=e)
    e.write(f\"\\nDONE_EXIT={rc}\\n\")
" > /tmp/smoke_wuliangye.log 2>&1 &
disown
echo "smoke kicked off; wait ~20 min"
'
```

Monitor until `intelligence.md` + `analysis.md` + `data-provenance.md` + `*.pptx` + `audit-report.md` all appear under `~/deliverables/wuliangye-smoke/`.

## 7. Independent 3-gate validation on the deliverable

```bash
ssh jackmac-mini '
python3 ~/.openclaw/extensions/aigroup-financial-services-openclaw/skills/cn-client-investigation/scripts/validate-delivery.py \
    ~/deliverables/wuliangye-smoke
'
```

Expected: `OVERALL: PASS — all applicable gates clean. Shippable.`

## 8. Trigger independent audit

```bash
ssh jackmac-mini '
export PATH=/opt/homebrew/bin:/Users/jackdong/.npm-global/bin:$PATH
openclaw agent --agent main --thinking high --timeout 1800 --json --message \
  "对 ~/deliverables/wuliangye-smoke 跑 data-quality-audit，按 skill 里的 5 步工作流做交叉验证 + 常识 check，把 audit-report.md 写进同一目录" \
  > /tmp/audit_run.json 2>/dev/null
'
```

Read `~/deliverables/wuliangye-smoke/audit-report.md` to see the PASS/FLAG/FAIL breakdown. If OVERALL verdict is PASS the deliverable is client-ship ready.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|------|
| Ping shows provider `openrouter` / model `openrouter/free` | `minimax-cn` profile or provider misconfig | see Step 3 + `~/.openclaw/agents/main/agent/auth-profiles.json` needs `minimax-cn:default` with `provider: minimax-cn` + real key |
| `missing ".claude-plugin/plugin.json"` on install | ClawHub cache transient | `rm -rf /var/folders/.../openclaw-clawhub-package-*` + retry |
| Safety scanner blocks install on `child_process` | Old cached version; fixed in 0.3.1+ | upgrade to latest |
| Compile aborts on "createSlide declares 1 param(s)" | slide-NN.js wrote `createSlide(theme)` single param | signature must be `(pres, theme)` and mutate the passed-in `pres` |
| `validate-delivery.py` SKIPs gate 1 | lead-discovery plugin not installed | install `aigroup-lead-discovery-openclaw` first (order matters) |
| audit FLAG `second-source-unavailable` rate too high | MCP data sources blocked | add Tushare / FMP / Finnhub credentials to the host config and retry |
