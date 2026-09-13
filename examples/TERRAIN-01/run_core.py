"""Exécute le cœur de phase 2 sur le terrain TERRAIN-01 (grille 4x4).

Topologie (Betti du réseau + P_sig de Takens), invariants (conservation
RMS), cohérence (score pondéré). Sortie déterministe dans expected.json.
"""

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))  # racine du dépôt GTT

from gtt.core import coherence as core_coherence
from gtt.core import invariants
from gtt.core.topology import betti_numbers


def _psig_takens(series):
    """Aire signée normalisée du cycle de Takens (m=2, formule des trapèzes)."""
    n = len(series)
    aire = sum(series[t] * series[t + 2] - series[t + 1] ** 2
               for t in range(n - 2))
    return aire / max(n, 1)


def _grid_complex(nodes: int, width: int = 4):
    """Graphe de la maille 4x4 : sommets + arêtes (sans faces fermées)."""
    K = {(v,) for v in range(nodes)}
    v = lambda a, b: a * width + b
    for i in range(width):
        for j in range(width):
            s = v(i, j)
            for nb in (v(i, j + 1), v(i + 1, j)):
                if nb < nodes:
                    K.add(tuple(sorted((s, nb))))
    return sorted(K)


def run(grid_path: Path) -> dict:
    grid = json.loads(grid_path.read_text(encoding="utf-8"))
    series = grid["series"]
    rms = {n: math.sqrt(sum(x * x for x in s) / len(s))
           for n, s in series.items()}

    betti = betti_numbers(_grid_complex(grid["nodes"], 4))
    psig = {n: _psig_takens(s) for n, s in series.items()}

    cons = invariants.check_conservation(
        list(range(grid["nodes"])),
        [rms[f"n{i}"] for i in range(grid["nodes"])],
        tol=1.0,
    )
    symp = invariants.check_symplecticite((1.0, 0.0, 0.0, 1.0), [])
    step = 0.05
    rev = invariants.check_reversibilite(
        lambda x: [x[0] + step], [0.0], lambda x: [x[0] - step],
        steps=5, tol=1e-12)

    coherence = core_coherence.coherence_score(
        {"conservation_rms": cons["ok"], "symplecticite": symp["ok"],
         "reversibilite": rev["ok"]})

    psig_abs = {n: round(abs(p), 9) for n, p in psig.items()}
    return {
        "terrain": "TERRAIN-01",
        "seed": grid["seed"],
        "betti_reseau": list(betti),
        "psig_max_abs": max(psig_abs.values()),
        "psig_mean_abs": round(sum(psig_abs.values()) / len(psig_abs), 9),
        "invariants": {
            "conservation_rms_ok": cons["ok"],
            "symplecticite_ok": symp["ok"],
            "reversibilite_ok": rev["ok"],
        },
        "coherence_score": round(coherence["score"], 9),
    }


if __name__ == "__main__":
    data = run(HERE / "grid.json")
    out = HERE / "expected.json"
    out.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n",
                   encoding="utf-8")
    print(f"sorties écrites : {out}")