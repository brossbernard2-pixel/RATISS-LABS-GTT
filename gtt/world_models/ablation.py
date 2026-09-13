"""Ablation : verdict par suppression, jamais par intuition (R6).

Phase 4 (méthode ; relais Rouge). Le verdict d'ablation est la DIFFÉRENCE
MESURÉE entre « avec composant » et « sans composant » sur les mêmes
réplicats scellés — rien d'autre. Le delta est publié quel qu'il soit
(y compris s'il est nul ou défavorable : doctrine du labo). STDLIB seule,
déterministe.
"""

from __future__ import annotations

from . import coherence_audit, correction

METRIQUES_PLUS_BAS_MEILLEUR = ("energy_violation_max",)


def run_ablation(world: object, component: str, params: dict) -> dict:
    """Exécute avec/sans composant et compare (verdict par ablation).

    component : "correction" (seul composant de la phase 4). params :
    {"steps", "x0s"} scellés au MANIFEST (R6). Sans = world brut ;
    avec = world + correction aval approuvée. Retourne les DEUX mesures,
    le delta et la métrique — jamais une interprétation.
    """
    if component != "correction":
        raise NotImplementedError(
            f"composant hors phase 4 : {component} (scelle : correction)")
    sans = coherence_audit.violation_max(world, params)
    patch = correction.propose_correction(
        world, {"type": "energy_drift"}, params)
    avec_world = correction.apply_after_review(
        world, patch, patch["verdict_required"])
    avec = coherence_audit.violation_max(avec_world, params)
    return {
        "component": component,
        "metric": "energy_violation_max",
        "without": sans,
        "with": avec,
        "delta": sans - avec,
        "reps": len(params["x0s"]),
    }


def ablation_verdict(with_: object, without: object, metric: str
                     ) -> tuple[bool, str]:
    """Compare deux mesures et rend un verdict (différence mesurée).

    metric dans METRIQUES_PLUS_BAS_MEILLEUR : amélioration ssi
    with_ < without. Retourne (ameliore, message chiffre). Le message
    contient les nombres — un verdict sans nombres n'existe pas ici.
    """
    if metric not in METRIQUES_PLUS_BAS_MEILLEUR:
        raise NotImplementedError(f"metrique hors phase 4 : {metric}")
    w, wo = float(with_), float(without)
    ameliore = w < wo
    etat = "amelioration mesuree" if ameliore else "pas d amelioration"
    return ameliore, (f"{metric}: sans={wo:.12g} avec={w:.12g} "
                      f"delta={wo - w:.12g} ({etat})")


__all__ = ["run_ablation", "ablation_verdict",
           "METRIQUES_PLUS_BAS_MEILLEUR"]
