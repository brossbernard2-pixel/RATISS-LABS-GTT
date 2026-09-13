"""Calibration des probabilités prédites.

Phase 4 (méthode calibration). Phase 1 : squelette.
"""


def brier_score(predicted: float, outcome: bool) -> float:
    """Score de Brier d'une prévision binaire. Non implémenté."""
    raise NotImplementedError("phase 4")


def calibration_curve(predictions: list, outcomes: list, bins: int) -> object:
    """Courbe de calibration (prédictions, issues, bins)."""
    raise NotImplementedError("phase 4")