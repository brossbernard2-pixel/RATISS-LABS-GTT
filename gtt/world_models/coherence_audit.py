"""Audit de cohérence d'un modèle du monde (méthode, R6).

Phase 4 (source ratiss-lewm-integration pour la méthode).
Squelette jusqu'à la phase 4.
"""


def coherence_score(world: object, params: dict) -> float:
    """Score de cohérence interne d'un monde (0..1). Non calculé."""
    raise NotImplementedError("phase 4")


def contradiction_detect(statements: list, params: dict) -> list:
    """Détecte des contradictions entre déclarations d'un monde."""
    raise NotImplementedError("phase 4")