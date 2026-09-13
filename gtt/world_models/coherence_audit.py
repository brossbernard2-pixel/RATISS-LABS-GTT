"""Audit de cohérence d'un modèle du monde (méthode, R6).

Phase 4 (source ratiss-lewm-integration pour la méthode ; réécriture
provenancée, relais Rouge). L'audit MESURE la violation des invariants
physiques d'un modèle déroulé — il ne décrète rien, ne touche jamais au
modèle (mesure externe scellée, doctrine du labo). Utilise les outils de
core (invariants, coherence) : une seule boîte à outils, pas deux lois.
STDLIB seule, déterministe.
"""

from __future__ import annotations

from gtt.core import coherence as core_coherence
from gtt.core import invariants as core_invariants

from . import lewm_bridge


def violation_max(world: object, params: dict) -> float:
    """Violation d'énergie pire cas sur réplicats scellés.

    params : {"steps", "x0s"} (figés au MANIFEST world_models AVANT tout
    run — R6). Pour chaque x0 : déroulé déterministe, energies E_t,
    violation = max_t |E_t − E_0| / E_0. Retourne le max sur réplicats.
    """
    steps = int(params["steps"])
    worst = 0.0
    for x0 in params["x0s"]:
        w = dict(world)
        w["state"] = [float(x0[0]), float(x0[1])]
        traj = lewm_bridge.rollout(w, steps)
        energies = [lewm_bridge.energy(s) for s in traj]
        r = core_invariants.check_conservation(
            list(range(len(energies))), energies, tol=0.0)
        e0 = energies[0]
        worst = max(worst, r["violation_max"] / abs(e0) if e0 else 0.0)
    return worst


def coherence_score(world: object, params: dict) -> float:
    """Score de cohérence interne d'un monde (0..1).

    Un réplicat « respecte » l'invariant si sa violation ≤ params["tol"]
    (scellé). Score = fraction pondérée des réplicats respectueux, via
    core.coherence (outil de mesure, aucun verdict de loi).
    """
    steps = int(params["steps"])
    tol = float(params["tol"])
    results: dict[str, bool] = {}
    for i, x0 in enumerate(params["x0s"]):
        w = dict(world)
        w["state"] = [float(x0[0]), float(x0[1])]
        traj = lewm_bridge.rollout(w, steps)
        energies = [lewm_bridge.energy(s) for s in traj]
        e0 = energies[0]
        viol = max(abs(e - e0) for e in energies) / abs(e0) if e0 else 0.0
        results[f"rep{i}_energy"] = viol <= tol
    return core_coherence.coherence_score(results)["score"]


def contradiction_detect(statements: list, params: dict) -> list:
    """Détecte des contradictions entre déclarations d'un monde.

    statements : [{"claim", "measured", "expected"}] — une déclaration est
    en contradiction si |measured − expected| > tol (params["tol_defaut"]
    ou statement["tol"]). Retourne les INDICES contradictoires (mesure,
    pas interprétation).
    """
    tol_defaut = float(params.get("tol_defaut", 1e-9))
    out: list[int] = []
    for i, st in enumerate(statements):
        tol = float(st.get("tol", tol_defaut))
        if abs(float(st["measured"]) - float(st["expected"])) > tol:
            out.append(i)
    return out


__all__ = ["violation_max", "coherence_score", "contradiction_detect"]
