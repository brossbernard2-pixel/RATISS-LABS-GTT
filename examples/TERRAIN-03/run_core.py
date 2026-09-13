"""TERRAIN-03 : core sur la chaleur 1D — conservation, stabilité, cohérence.

Mesures : (1) masse totale conservée exactement dans les DEUX sondes
(invariant analytique, indépendant de la stabilité) ; (2) amplitude
décroissante en stable (r=0.4) et CROISSANTE en instable (r=0.6) —
l'audit doit signaler la configuration instable ; (3) score de cohérence
= fraction d'invariants respectés (3/3 quand la physique est reproduite).

Graine de von Neumann : les deux sondes reçoivent la MÊME perturbation
alternée ε·(−1)^i (ε = 1e-3, documentée, déterministe) — tout schéma
numérique réel contient l'équivalent en arrondi. Sans elle, une bosse
pure met des dizaines de pas avant d'exciter le mode de Nyquist ; avec
elle, le critère de stabilité r ≤ 0.5 se voit immédiatement : le mode
instable croît en |1−4r| = 1.4 par pas. Amplitude = max |u|.
Sortie déterministe (arrondis 12 décimales) dans expected.json.
"""

GRAINE_VON_NEUMANN = 1e-3

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from gtt.core import coherence as core_coherence
from gtt.core import invariants


def diffuser(u0: list, r: float, steps: int) -> list:
    """Schéma volumes finis, bords de Neumann miroir (forme fluxique).

    u'_i = u_i + r·(g_{i+1/2} − g_{i−1/2}), g_{i+1/2} = u_{i+1} − u_i,
    ghosts miroirs aux bords → la somme télescope : masse conservée.
    """
    u = list(u0)
    n = len(u)
    for _ in range(steps):
        v = list(u)
        for i in range(n):
            gauche = u[i - 1] if i > 0 else u[0]        # miroir
            droite = u[i + 1] if i < n - 1 else u[n - 1]  # miroir
            v[i] = u[i] + r * ((droite - u[i]) - (u[i] - gauche))
        u = v
    return u


def run(heat_path: Path) -> dict:
    data = json.loads(heat_path.read_text(encoding="utf-8"))
    p, u0 = data["params"], data["u0"]
    n, dx, D = p["n"], p["dx"], p["D"]
    sorties = {}
    u_graine = [u + GRAINE_VON_NEUMANN * (-1) ** i for i, u in enumerate(u0)]
    for nom, dt in (("stable", p["dt_stable"]), ("instable", p["dt_instable"])):
        r = D * dt / (dx * dx)
        uf = diffuser(u_graine, r, p["steps"])
        masses = [sum(u_graine)]
        u = list(u_graine)
        for _ in range(p["steps"]):
            u = diffuser(u, r, 1)
            masses.append(sum(u))
        cons = invariants.check_conservation(list(range(len(masses))), masses,
                                             tol=1e-9)
        amp0 = max(abs(x) for x in u_graine)
        ampf = max(abs(x) for x in uf)
        sorties[nom] = {
            "r": round(r, 12),
            "graine_von_neumann": GRAINE_VON_NEUMANN,
            "violation_masse": round(cons["violation_max"], 12),
            "masse_conservée": cons["ok"],
            "amplitude_initiale": round(amp0, 12),
            "amplitude_finale": round(ampf, 12),
            "amplitude_decroissante": ampf < amp0,
        }
    # L'invariant « stabilité conforme » n'est respecté que si la sonde
    # stable décroît ET la sonde instable explose — c'est la physique,
    # pas un bug : un schéma stable amortit, un schéma instable explose.
    score = core_coherence.coherence_score({
        "masse_stable": sorties["stable"]["masse_conservée"],
        "masse_instable": sorties["instable"]["masse_conservée"],
        "stabilite_conforme": sorties["stable"]["amplitude_decroissante"]
        and (not sorties["instable"]["amplitude_decroissante"]),
    })
    return {"terrain": "TERRAIN-03", "modele": "chaleur 1D Neumann miroir",
            "stable": sorties["stable"], "instable": sorties["instable"],
            "coherence_score": round(score["score"], 12)}


if __name__ == "__main__":
    out = run(HERE / "heat.json")
    (HERE / "expected.json").write_text(
        json.dumps(out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("sorties écrites : expected.json")
