#!/usr/bin/env python3
"""Vérifications déterministes world_models phase 4 (sortie stable, R7).

Mêmes entrées -> exactement la même sortie sur toute machine.
Valeurs arrondies à 12 décimales ; RESULTAT final : CONFORME/DIVERGENCE.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gtt.world_models import ablation, coherence_audit, correction, lewm_bridge

P = {"omega": 1.0, "dt": 0.1, "gain": 0.0}
AUD = {"steps": 10, "tol": 1e-9,
       "x0s": [[1.0, 0.0], [0.5, 0.5], [0.0, 1.0]]}
FACTEUR = 1.0 + P["omega"] ** 2 * P["dt"] ** 2


def r(x: float) -> float:
    return round(x, 12)


def main() -> int:
    ok = True
    exact = lewm_bridge.world_state(
        {"model": "exact_harmonic", "x0": [1.0, 0.0]}, P)
    appris = lewm_bridge.world_state(
        {"model": "learned_surrogate", "x0": [1.0, 0.0]}, P)

    v_exact = coherence_audit.violation_max(exact, AUD)
    ok &= v_exact < 1e-12
    print(f"harmonique exact : violation={r(v_exact)} (attendu ~0)")

    v_appris = coherence_audit.violation_max(appris, AUD)
    ff = FACTEUR ** 10 - 1.0
    d = abs(v_appris - ff)
    ok &= d < 1e-12
    print(f"surrogate appris : violation={r(v_appris)} forme_fermee={r(ff)} delta={r(d)}")

    v_corr = correction.corrected_violation(appris, AUD)
    ok &= v_corr < 1e-12
    print(f"correction aval : violation_apres={r(v_corr)} (modele intact)")

    ab = ablation.run_ablation(appris, "correction", AUD)
    verdict, msg = ablation.ablation_verdict(ab["with"], ab["without"], ab["metric"])
    ok &= verdict and ab["delta"] > 0
    print(f"ablation : sans={r(ab['without'])} avec={r(ab['with'])} delta={r(ab['delta'])}")
    print(f"verdict chiffre : {msg}")

    s_exact = coherence_audit.coherence_score(exact, AUD)
    s_appris = coherence_audit.coherence_score(appris, AUD)
    ok &= s_exact == 1.0 and s_appris == 0.0
    print(f"scores coherence : exact={r(s_exact)} appris={r(s_appris)}")

    print("RESULTAT:", "CONFORME" if ok else "DIVERGENCE")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
