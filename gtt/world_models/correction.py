"""Correction des incohérences détectées (R6 : séparé du chemin critique).

Phase 4 (méthode des neuf couches ; relais Rouge). Principe directeur :
on ne réentraîne JAMAIS le modèle audité — la correction est EN AVAL
(post-traitement déterministe de ses sorties), proposée puis appliquée
seulement après verdict explicite « APPROVED ». Aucune correction ne
s'applique seule. STDLIB seule, déterministe.
"""

from __future__ import annotations

from . import coherence_audit, lewm_bridge


def propose_correction(world: object, issue: dict, params: dict) -> dict:
    """Propose une correction (jamais appliquée seule).

    issue : {"type": "energy_drift"}. params : ceux de l'audit scellés
    (steps, x0s). Mesure d'abord la violation réelle, puis propose le
    patch adapté. Le world d'entrée n'est PAS modifié.
    """
    if issue.get("type") != "energy_drift":
        raise NotImplementedError(
            f"issue non prise en charge phase 4 : {issue.get('type')}")
    viol = coherence_audit.violation_max(world, params)
    return {
        "type": "energy_rescale",
        "verdict_required": "APPROVED",
        "measured_violation": viol,
        "predicted_effect": "violation -> 0 a precision machine "
                            "(remise a l'echelle par pas, en aval)",
        "model_touche": "jamais",
    }


def apply_after_review(world: object, patch: dict, verdict: str) -> object:
    """Applique un patch si verdict explicite. Pas d'application seule.

    verdict doit valoir exactement patch["verdict_required"] (« APPROVED »).
    Renvoie une COPIE corrigée (world["corrected"] = True) : update_world
    remet alors l'énergie à l'échelle après chaque pas brut — le modèle
    sous-jacent reste intact (jamais réentraîné, jamais modifié).
    """
    required = patch.get("verdict_required", "APPROVED")
    if verdict != required:
        raise ValueError(
            f"verdict explicite requis : {required!r} (recu : {verdict!r})")
    if patch.get("type") != "energy_rescale":
        raise NotImplementedError(
            f"patch non pris en charge phase 4 : {patch.get('type')}")
    out = dict(world)
    out["state"] = list(world["state"])
    out["corrected"] = True
    return out


def corrected_violation(world: object, params: dict) -> float:
    """Violation APRÈS correction aval (mesure, pas promesse)."""
    patch = propose_correction(world, {"type": "energy_drift"}, params)
    fixed = apply_after_review(world, patch, patch["verdict_required"])
    return coherence_audit.violation_max(fixed, params)


__all__ = ["propose_correction", "apply_after_review", "corrected_violation"]
