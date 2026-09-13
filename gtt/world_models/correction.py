"""Correction des incohérences détectées (R6 : séparé du chemin critique).

Phase 4 (méthode des neuf couches).
Squelette jusqu'à la phase 4.
"""


def propose_correction(world: object, issue: dict, params: dict) -> dict:
    """Propose une correction (jamais appliquée seule)."""
    raise NotImplementedError("phase 4")


def apply_after_review(world: object, patch: dict, verdict: str) -> object:
    """Applique un patch si verdict explicite. Pas implémenté."""
    raise NotImplementedError("phase 4")