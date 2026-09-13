#!/usr/bin/env bash
# Rejoue les tests core, le terrain TERRAIN-01 et le juge (phase 2).
# Écrit proofs/PHASE2-REPLAY-<date>.md avec commande, exit code, SHA-256.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF="$ROOT/proofs/PHASE2-REPLAY-$(date +%Y%m%d-%H%M%S).md"
: > "$PROOF"
fail=0

step() {
  echo "## $1" >> "$PROOF"
}

run_step() {
  local name="$1"; shift
  local out
  out="$("$@" 2>&1)"
  local code=$?
  # Reçu machine-indépendant (correction Rouge 2026-09-13) : les chemins
  # absolus du poste sont normalisés avant scellement.
  out="$(printf '%s' "$out" | sed "s|$ROOT|<ROOT>|g")"
  local sha
  sha="$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)"
  {
    echo "### $name"
    echo "commande : \`$(printf '%s' "$*" | sed "s|$ROOT|<ROOT>|g")\`"
    echo "exit : $code"
    echo "sha256 : $sha"
  } >> "$PROOF"
  [ $code -ne 0 ] && fail=1
}

step "Rejeu phase 2 (tests + terrain + juge)"
run_step "tests core (pytest)" bash -c "cd '$ROOT' && python3 -m pytest -q -p no:cacheprovider 2>&1 | sed -E 's/ in [0-9]+\\.[0-9]+s//'"
run_step "terrain generate" bash -c "cd '$ROOT/examples/TERRAIN-01' && python3 generate.py"
run_step "terrain run_core" bash -c "cd '$ROOT/examples/TERRAIN-01' && python3 run_core.py"
run_step "expected.json sha" bash -c "cd '$ROOT/examples/TERRAIN-01' && sha256sum expected.json"
run_step "juge (gtt.judge --ci)" bash -c "cd '$ROOT' && python3 -m gtt.judge --ci"

if [ "$fail" -eq 0 ]; then
  echo "REPLAY OK — reçu : $PROOF"
  echo "" >> "$PROOF"
  echo "**Résultat : rejoué sans erreur.**" >> "$PROOF"
else
  echo "REPLAY KO — voir $PROOF" >&2
  exit 1
fi