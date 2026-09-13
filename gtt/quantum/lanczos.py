"""Algorithme de Lanczos pour spectres de systèmes topologiques.

Phase 3 (source Algorithmes-quantique-Ratiss-labs-, QPU-Ratiss-COSMOS).
Aucun calcul avant la phase 3 ; signatures verrouillées (R5).
"""


def lanczos_iteration(matrix: object, k: int, params: dict) -> dict:
    """Itérations de Lanczos (matrice, k, params) -> spectre approché."""
    raise NotImplementedError("phase 3")


def convergence_criterion(residual: float, tolerance: float) -> bool:
    """Critère de convergence sur le résiduel de Lanczos."""
    raise NotImplementedError("phase 3")