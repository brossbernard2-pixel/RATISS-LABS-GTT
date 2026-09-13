#!/usr/bin/env bash
# Rejoue les tests quantum, les vérifications déterministes et le juge
# (phase 6). Écrit proofs/PHASE6-REPLAY-<date>.md avec commande, exit,
# SHA-256 — reçu machine-indépendant (normalisation <ROOT>, règle R7).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROOF="$ROOT/proofs/PHASE6-REPLAY-$(date +%Y%m%d-%H%M%S).md"
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
  # Reçu machine-indépendant : chemins absolus normalisés avant scellement.
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

step "Rejeu phase 6 (tests + vérifications agents+receipts+viz+io + juge)"
run_step "tests (pytest)" bash -c "cd '$ROOT' && python3 -m pytest -q -p no:cacheprovider 2>&1 | sed -E 's/ in [0-9]+\.[0-9]+s//'"
run_step "verifications agents+receipts+viz+io" bash -c "cd '$ROOT' && python3 scripts/agents_check.py"
run_step "juge (gtt.judge --ci)" bash -c "cd '$ROOT' && python3 -m gtt.judge --ci"

if [ "$fail" -eq 0 ]; then
  echo "REPLAY OK — reçu : $PROOF"
  echo "" >> "$PROOF"
  echo "**Résultat : rejoué sans erreur.**" >> "$PROOF"
else
  echo "REPLAY KO — voir $PROOF" >&2
  exit 1
fi
