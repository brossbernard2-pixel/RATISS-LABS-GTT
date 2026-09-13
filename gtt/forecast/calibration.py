"""Calibration des probabilités prédites.

Phase 5 (méthode calibration). Squelette jusqu'à la phase 5.
"""


def brier_score(predicted: float, outcome: bool) -> float:
    """Score de Brier d'une prévision binaire. Non implémenté."""
    raise NotImplementedError("phase 5")


def calibration_curve(predictions: list, outcomes: list, bins: int) -> object:
    """Courbe de calibration (prédictions, issues, bins)."""
    raise NotImplementedError("phase 5")