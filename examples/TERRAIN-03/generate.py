"""TERRAIN-03 : diffusion de chaleur 1D — masses et stabilité.

Réécriture provenancée de l'idée RATISS-HPC (aucune copie de code ;
URL+sha en PROVENANCE). Schéma volumes finis à bords NEUMANN miroir :
la masse totale Σu est CONSERVÉE exactement (télescopage des fluxes) —
vérité analytique. Deux sondes : r = D·dt/dx² = 0.4 (stable,
l'amplitude décroît) et r = 0.6 (instable, l'amplitude EXPLOSE —
l'audit doit la voir). Déterministe : bosse gaussienne en formule pure.
"""

import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "heat.json"
PARAMS = {"n": 21, "dx": 1.0, "D": 1.0, "dt_stable": 0.4,
          "dt_instable": 0.6, "steps": 25}


def bosse_initiale(p: dict = PARAMS) -> list:
    """Bosse gaussienne déterministe centrée (aucune RNG)."""
    c = (p["n"] - 1) / 2.0
    return [round(math.exp(-((i - c) ** 2) / 8.0), 12) for i in range(p["n"])]


if __name__ == "__main__":
    OUT.write_text(json.dumps({"params": PARAMS, "u0": bosse_initiale()},
                              sort_keys=True, indent=2) + "\n",
                   encoding="utf-8")
    print(f"chaleur écrite : {OUT.name}")
