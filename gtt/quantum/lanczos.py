"""Algorithme de Lanczos pour spectres de systèmes topologiques.

Phase 5 (source Algorithmes-quantique-Ratiss-labs-, QPU-Ratiss-COSMOS).
Phase 1 : squelette.
"""


def lanczos_iteration(matrix: object, k: int, params: dict) -> dict:
    """Itérations de Lanczos (matrice, k, params) -> spectre approché.

    Aucun calcul en phase 1 ; signatures verrouillées (R5).
    """
    raise NotImplementedError("phase 5")


def convergence_criterion(residual: float, tolerance: float) -> bool:
    """Critère de convergence sur le résiduel de Lanczos."""
    raise NotImplementedError("phase 5")