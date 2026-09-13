#!/usr/bin/env bash
# Audit indépendant GTT — tout rejouer en une commande (kit : docs/AUDIT-INDEPENDANT-KIT.md).
# Clone frais, installation, 108 tests, juge, 5 checks, rejeux ×2, hygiène,
# puis formulaire de verdict. Le run externe LeWM (dépendances lourdes) est
# proposé mais jamais imposé. Aucune confiance : tout est rejoué.
set -u
BASE="${1:-/tmp/gtt-audit-independant}"
rm -rf "$BASE"
echo "== clone frais =="
git clone -q https://github.com/brossbernard2-pixel/RATISS-LABS-GTT.git "$BASE" || { echo "ÉCHEC clone"; exit 1; }
cd "$BASE" || exit 1
SHA=$(git rev-parse HEAD); echo "commit rejoué : $SHA"
echo "== installation =="
pip install -q "ratiss-framework @ git+https://github.com/brossbernard2-pixel/RATISS-Framework.git" >/dev/null 2>&1
pip install -q -e . >/dev/null 2>&1 || { echo "ÉCHEC install"; exit 1; }
FAIL=0
echo "== tests =="
python -m pytest -q -p no:cacheprovider 2>&1 | tail -1 | grep -q "108 passed" && echo "pytest : 108 passed ✔" || { echo "pytest : ÉCHEC ✗"; FAIL=1; }
echo "== juge =="
python -m gtt.judge --ci >/dev/null 2>&1 && echo "judge : exit 0 ✔" || { echo "judge : ÉCHEC ✗"; FAIL=1; }
echo "== 5 checks déterministes =="
for c in wm quantum forecast agents examples; do
  R=$(python "scripts/${c}_check.py" 2>/dev/null | tail -1)
  echo "  ${c}_check : $R"
  [ "$R" = "RESULTAT: CONFORME" ] || FAIL=1
done
echo "== rejeux R7 ×2 (phases 4-7) =="
for p in 4 5 6 7; do
  bash "scripts/replay_phase$p.sh" >/dev/null 2>&1; e1=$?
  bash "scripts/replay_phase$p.sh" >/dev/null 2>&1; e2=$?
  A=$(ls -t proofs/PHASE$p-REPLAY-*.md | head -2 | sort | head -1)
  B=$(ls -t proofs/PHASE$p-REPLAY-*.md | head -2 | sort | tail -1)
  if [ $e1 -eq 0 ] && [ $e2 -eq 0 ] && diff -q <(sed "s/$(basename "$A" .md)/RUN/" "$A") <(sed "s/$(basename "$B" .md)/RUN/" "$B") >/dev/null; then
    echo "  phase $p : exits 0/0, reçus identiques ✔"
  else
    echo "  phase $p : ÉCHEC ✗"; FAIL=1
  fi
done
echo "== hygiène =="
S=$(git log -p | grep -cE '^\+.*(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-)')
echo "  secrets dans l'historique : $S (attendu 0)"
[ "$S" = "0" ] || FAIL=1
echo "== run externe LeWM (optionnel) =="
if python -c "import torch, transformers, stable_worldmodel, einops" >/dev/null 2>&1; then
  python scripts/wm_externe_lewm.py | tail -6
else
  echo "  NON EXÉCUTÉ — dépendances absentes (pip install torch 'transformers<5' stable-worldmodel einops)"
fi
echo
echo "===================== FORMULAIRE DE VERDICT ====================="
echo "AUDIT INDÉPENDANT GTT"
echo "Auditeur (identité) : ______________________"
echo "Commit rejoué (SHA) : $SHA"
echo "Date (UTC)          : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ $FAIL -eq 0 ]; then echo "Rejeu automatique   : TOUT VERT"; else echo "Rejeu automatique   : ÉCHEC(S) — voir ci-dessus"; fi
echo "run externe LeWM    : APPROVED / DIVERGENCE / NON EXÉCUTÉ (ci-dessus)"
echo "VERDICT FINAL       : CONFORME / DIVERGENCE (à trancher par l'auditeur)"
echo "Réserves            : ______________________"
echo "Signature           : ______________________"
echo "FORMULAIRE PRÊT — à signer par l'auditeur"
exit $FAIL
