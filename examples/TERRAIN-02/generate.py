"""TERRAIN-02 : épidémie SIR discrète — invariant analytique exact.

Réécriture provenancée de l'idée RATISS-BIOLAB (aucune copie de code ;
URL+sha en PROVENANCE). Le total S+I+R est CONSERVÉ exactement à chaque
pas (les transferts sont symétriques) — vérité analytique, pas une
approximation. Déterministe : aucune RNG, mêmes paramètres → mêmes
données sur toute machine.
"""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "sir.json"
PARAMS = {"N": 1000.0, "S0": 999.0, "I0": 1.0, "R0": 0.0,
          "beta": 0.3, "gamma": 0.1, "steps": 30,
          "reseau_contacts": "cycle4"}


def build_sir(p: dict = PARAMS) -> dict:
    """Séries SIR déterministes (pas de RNG — formule pure)."""
    s, i, r = p["S0"], p["I0"], p["R0"]
    n = p["N"]
    serie = {"S": [s], "I": [i], "R": [r]}
    for _ in range(p["steps"]):
        infection = p["beta"] * s * i / n
        guerison = p["gamma"] * i
        s = s - infection
        i = i + infection - guerison
        r = r + guerison
        serie["S"].append(s)
        serie["I"].append(i)
        serie["R"].append(r)
    return {"params": p, "series": serie}


if __name__ == "__main__":
    OUT.write_text(json.dumps(build_sir(), sort_keys=True, indent=2) + "\n",
                   encoding="utf-8")
    print(f"SIR écrit : {OUT.name}")
