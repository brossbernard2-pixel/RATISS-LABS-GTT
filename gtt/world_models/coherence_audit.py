"""Audit de cohérence d'un modèle du monde (méthode, R6).

Phase 3 (source ratiss-lewm-integration pour la méthode). Phase 1 :
squelette.
"""


def coherence_score(world: object, params: dict) -> float:
    """Score de cohérence interne d'un monde (0..1). °(non calculé)."""
    raise NotImplementedError("phase 3")


def contradiction_detect(statements: list, params: dict) -> list:
    """Détecte des contradictions entre déclarations d'un monde."""
    raise NotImplementedError("phase 3")