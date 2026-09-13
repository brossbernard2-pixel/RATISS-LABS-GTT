"""Hypothèses scellées du labo — statut HYPOTHESIS uniquement.

Phase 2. Les hypothèses (LCT, P_sig) sont des objets testables aux paramètres
figés AVANT tout run (R6). Leur protocole renvoie des MESURES — jamais des
verdicts. Une hypothèse n'est pas une fondation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Hypothesis:
    """Hypothèse scellée testable (statut HYPOTHESIS)."""

    name: str
    status: str = "HYPOTHESIS"
    params: dict[str, Any] = field(default_factory=dict)
    reference: str = ""

    def as_dict(self) -> dict[str, Any]:
        """Représentation scellable (R5)."""
        return {
            "name": self.name,
            "status": self.status,
            "params": self.params,
            "reference": self.reference,
        }

    def protocole(self) -> dict[str, Any]:
        """Protocole : prédiction testable, métrique, seuil de réfutation.

        Renvoie des MESURES (paramètres de mesure) ; aucune affirmation.
        """
        return {
            "hypothesis": self.name,
            "prediction": f"mesure de {self.name} dans le domaine scellé",
            "metric": self.params.get("refutation_metric"),
            "seuil_refutation": self.params.get("refutation_threshold"),
            "mesurabilité": True,
        }


LCT_HYPOTHESIS = Hypothesis(
    name="LCT",
    status="HYPOTHESIS",
    params={
        "cycle": "local",
        "topology": "constrained",
        "takens_dim": 2,
        "window": 240,
        "refutation_metric": "psig_mean_abs",
        "refutation_threshold": 0.01,
    },
    reference="osf.io/wf7qm (contexte, jamais évidence)",
)

P_SIG_HYPOTHESIS = Hypothesis(
    name="P_sig",
    status="HYPOTHESIS",
    params={
        "probability": "signature",
        "threshold": "tbd",
        "area_norm": "trapezoid",
        "refutation_metric": "psig_cv",
        "refutation_threshold": 0.5,
    },
    reference="osf.io/6jzmb (contexte, jamais évidence)",
)

__all__ = ["Hypothesis", "LCT_HYPOTHESIS", "P_SIG_HYPOTHESIS"]