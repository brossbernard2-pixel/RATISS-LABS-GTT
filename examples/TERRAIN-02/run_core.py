"""TERRAIN-02 : core de phase 2 sur SIR — conservation + perturbation + Betti.

Mesures : (1) conservation exacte du total S+I+R (violation ~0) ;
(2) perturbation epsilon connue → violation ≈ epsilon (l'audit VOIT les
fuites) ; (3) Betti du réseau de contacts cycle4 = (1, 1) ; (4) score de
cohérence. Sortie déterministe dans expected.json (arrondis 12 décimales).
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from gtt.core import coherence as core_coherence
from gtt.core import invariants
from gtt.core.topology import betti_numbers
from gtt.forecast import calibration  # noqa: F401 — cohérence d'imports


def reseau_cycle4():
    """Cycle de 4 nœuds (sommet+arêtes) : Betti analytique (1, 1)."""
    return [(0,), (1,), (2,), (3,), (0, 1), (1, 2), (2, 3), (0, 3)]


def run(sir_path: Path) -> dict:
    data = json.loads(sir_path.read_text(encoding="utf-8"))
    s, i, r = data["series"]["S"], data["series"]["I"], data["series"]["R"]
    totaux = [a + b + c for a, b, c in zip(s, i, r)]
    cons = invariants.check_conservation(list(range(len(totaux))), totaux,
                                         tol=1e-9)
    # perturbation connue : +1e-6 sur I au pas 10 -> violation ≈ 1e-6
    perturbes = list(totaux)
    perturbes[10] += 1e-6
    pert = invariants.check_conservation(list(range(len(perturbes))),
                                         perturbes, tol=1e-12)
    betti = betti_numbers(reseau_cycle4())
    score = core_coherence.coherence_score({
        "conservation_totale": cons["ok"],
        "perturbation_detectee": not pert["ok"],
    })
    return {
        "terrain": "TERRAIN-02",
        "modele": "SIR discret (beta=0.3, gamma=0.1, N=1000, 30 pas)",
        "conservation_violation": round(cons["violation_max"], 12),
        "conservation_ok": cons["ok"],
        "perturbation_violation": round(pert["violation_max"], 12),
        "perturbation_detectee": not pert["ok"],
        "betti_reseau": list(betti),
        "coherence_score": round(score["score"], 12),
    }


if __name__ == "__main__":
    out = run(HERE / "sir.json")
    (HERE / "expected.json").write_text(
        json.dumps(out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(f"sorties écrites : expected.json")
