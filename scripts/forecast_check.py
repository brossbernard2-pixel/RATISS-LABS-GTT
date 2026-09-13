#!/usr/bin/env python3
"""Vérifications déterministes forecast phase 5 (sortie stable, R7)."""
import sys, tempfile, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gtt.forecast import calibration, journal, metaculus_bot, sealed_predictions

def r(x): return round(x, 12)

def main():
    ok = True
    b = calibration.brier_score(0.75, True)
    ok &= b == 0.0625
    print(f"Brier 0.75/vrai : {r(b)} (attendu 0.0625)")
    curve = calibration.calibration_curve([0.9, 0.9], [True, False], bins=1)
    ece = calibration.expected_calibration_error(curve)
    ok &= abs(ece - 0.4) < 1e-12
    print(f"ECE jeu connu : {r(ece)} (attendu 0.4)")
    fixture = [{"id": f"q{i}", "question": f"Q{i}?"} for i in range(250)]
    out = metaculus_bot.run_offline({"fixture": fixture})
    ok &= out["n_questions"] == 200 and out["truncated"] and len(out["receipts"]) == 200
    print(f"Run hors-ligne 250 questions : n={out['n_questions']} truncated={out['truncated']} recus={len(out['receipts'])} (plafond 200)")
    p = {"context": {"run_id": "chk"}}
    s1 = sealed_predictions.seal_prediction("p=0.62", p)
    s2 = sealed_predictions.seal_prediction("p=0.62", p)
    ok &= s1 == s2 and sealed_predictions.verify_prediction("p=0.62", s1, p) and not sealed_predictions.verify_prediction("p=0.63", s1, p)
    print(f"Scelle R5 stable : {s1[:16]}… alteration_detectee={not sealed_predictions.verify_prediction('p=0.63', s1, p)}")
    fd, jp = tempfile.mkstemp(suffix=".jsonl"); os.close(fd)
    try:
        journal.append_deviation(jp, "déviation de contrôle", {})
        v1 = journal.verify_journal(jp)
        # altération ASCII sûre (le JSON stocke les accents échappés) :
        lignes = open(jp, encoding="utf-8").read().replace("gtt-forecast", "TRICHEUR")
        open(jp, "w", encoding="utf-8").write(lignes)
        v2 = journal.verify_journal(jp)
        ok &= v1 and not v2
        print(f"Journal chaîne R5 : integre={v1} altere_casse={not v2}")
    finally:
        os.unlink(jp)
    print("RESULTAT:", "CONFORME" if ok else "DIVERGENCE")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
