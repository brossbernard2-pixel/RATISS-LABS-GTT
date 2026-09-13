"""Calibration des probabilités prédites.

Phase 5 (méthode calibration ; réécriture provenancée, relais Rouge).
Brier exact, courbe de calibration par bacs, erreur de calibration (ECE).
Aucune dépendance ; déterministe ; testé sur vérités analytiques.
"""

from __future__ import annotations


def brier_score(predicted: float, outcome: bool) -> float:
    """Score de Brier d'une prévision binaire : (p − o)², o ∈ {0, 1}.

    Vérité analytique : p=0.75, issue vraie → 0.0625.
    """
    if not 0.0 <= predicted <= 1.0:
        raise ValueError("probabilité hors [0, 1]")
    o = 1.0 if outcome else 0.0
    return (predicted - o) ** 2


def calibration_curve(predictions: list, outcomes: list, bins: int
                      ) -> object:
    """Courbe de calibration (prédictions, issues, bins).

    Bacs [i/bins, (i+1)/bins) ; le dernier bac est fermé à droite.
    Retourne [{"bin", "lo", "hi", "n", "mean_pred", "freq_outcome"}] —
    n=0 → mean_pred/freq None (bac vide, jamais inventé).
    """
    if len(predictions) != len(outcomes):
        raise ValueError("longueurs différentes")
    if bins < 1:
        raise ValueError("bins >= 1")
    curve = []
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        idx = [j for j, p in enumerate(predictions)
               if (lo <= p < hi) or (i == bins - 1 and p == 1.0)]
        n = len(idx)
        curve.append({
            "bin": i, "lo": lo, "hi": hi, "n": n,
            "mean_pred": (sum(predictions[j] for j in idx) / n) if n else None,
            "freq_outcome": (sum(1 for j in idx if outcomes[j]) / n) if n else None,
        })
    return curve


def expected_calibration_error(curve: object) -> float:
    """ECE = Σ (n/N)·|mean_pred − freq_outcome| sur bacs non vides."""
    total = sum(b["n"] for b in curve)
    if total == 0:
        raise ValueError("aucune prédiction")
    ece = 0.0
    for b in curve:
        if b["n"]:
            ece += (b["n"] / total) * abs(b["mean_pred"] - b["freq_outcome"])
    return ece


def delta_brier(before: list, after: list, outcomes: list) -> float:
    """ΔBrier = Brier_moyen(before) − Brier_moyen(after) (R6 : ablation).

    Positif = amélioration mesurée. Aucun verdict, que le nombre.
    """
    if not (len(before) == len(after) == len(outcomes)):
        raise ValueError("longueurs différentes")
    if not before:
        raise ValueError("liste vide")
    mb = sum(brier_score(p, o) for p, o in zip(before, outcomes)) / len(before)
    ma = sum(brier_score(p, o) for p, o in zip(after, outcomes)) / len(after)
    return mb - ma


__all__ = ["brier_score", "calibration_curve", "expected_calibration_error",
           "delta_brier"]
