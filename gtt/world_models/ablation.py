"""Ablation : verdict par suppression, jamais par intuition (R6).

Phase 4 (méthode). Squelette jusqu'à la phase 4.
"""


def run_ablation(world: object, component: str, params: dict) -> dict:
    """Exécute avec/sans composant et compare (verdict par ablation)."""
    raise NotImplementedError("phase 4")


def ablation_verdict(with_: object, without: object, metric: str) -> tuple[bool, str]:
    """Compare deux mesures et rend un verdict (différence mesurée)."""
    raise NotImplementedError("phase 4")