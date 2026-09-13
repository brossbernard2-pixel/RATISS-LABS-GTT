"""Correction des incohérences détectées (R6 : séparé du chemin critique).

Phase 3 (méthode des neuf couches). Phase 1 : squelette.
"""


def propose_correction(world: object, issue: dict, params: dict) -> dict:
    """Propose une correction (jamais appliquée seule)."""
    raise NotImplementedError("phase 3")


def apply_after_review(world: object, patch: dict, verdict: str) -> object:
    """Applique un patch si verdict explicite. Pas implémenté."""
    raise NotImplementedError("phase 3")