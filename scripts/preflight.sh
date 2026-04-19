#!/usr/bin/env bash
# preflight.sh — verify macmini runtime deps for aigroup-financial-services-openclaw.
# Exit 0 → all required tools / libraries reachable; plugin is usable.
# Exit 1 → at least one dep missing; stderr lists which + install hint.
#
# Safe to run non-interactively (no prompts). Called from QUICKSTART.md and from
# scripts/smoke-macmini.sh.

set -u
FAIL=0
MISSING=()

need_cmd() {
  # need_cmd <bin> <friendly_name> <install_hint>
  local bin="$1" name="$2" hint="$3"
  if ! command -v "$bin" >/dev/null 2>&1; then
    MISSING+=("$name — $hint")
    FAIL=1
  else
    echo "  ok  $name ($(command -v "$bin"))"
  fi
}

need_python_mod() {
  # need_python_mod <module> <install_hint>
  local mod="$1" hint="$2"
  if ! python3 -c "import $mod" >/dev/null 2>&1; then
    MISSING+=("python3 module '$mod' — $hint")
    FAIL=1
  else
    echo "  ok  python3 module '$mod'"
  fi
}

echo "aigroup-financial-services-openclaw preflight on $(uname -s)/$(uname -m)"
echo

echo "[required binaries]"
need_cmd python3 "python3 (>= 3.9)" "built-in on macOS 11+, or 'brew install python@3.11'"
need_cmd node   "node (>= 18)"       "brew install node"
need_cmd uvx    "uvx"                "brew install uv"

echo
echo "[required python modules]"
# python-pptx is the text extractor the compile gate shells out to. Only
# warn (not hard fail) if missing on the system python — uvx --with
# python-pptx gets us there transient-ly, so this is "nice to have".
if python3 -c "import pptx" >/dev/null 2>&1; then
  echo "  ok  python-pptx (system python3)"
else
  echo "  note python-pptx not in system python3 — compile template will fall back to 'uvx --with python-pptx python3' on demand"
fi

echo
if [ "$FAIL" -ne 0 ]; then
  echo "FAIL: $(printf '%d' "${#MISSING[@]}") dependency issue(s):" >&2
  for m in "${MISSING[@]}"; do
    echo "  - $m" >&2
  done
  exit 1
fi

echo "PASS: all required runtime deps reachable."
exit 0
