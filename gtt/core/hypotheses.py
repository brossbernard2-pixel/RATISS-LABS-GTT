"""Hypothèses scellées du labo — statut HYPOTHESIS, jamais axiome.

Les hypothèses scientifiques (LCT, P_sig) sont déclarées ici comme des
objets testables et scellés. Elles ne fondent aucune construction :
elles se testent. Une hypothèse n'est pas une fondation.

Source des hypothèses (phase 3) : RATISS-ODV-AEON.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Hypothesis:
    """Hypothèse scellée testable (jamais un axiome)."""

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


LCT_HYPOTHESIS = Hypothesis(
    name="LCT",
    params={"cycle": "local", "topology": "constrained"},
    reference="osf.io/wf7qm (contexte, jamais évidence)",
)

P_SIG_HYPOTHESIS = Hypothesis(
    name="P_sig",
    params={"probability": "signature", "threshold": "tbd"},
    reference="osf.io/6jzmb (contexte, jamais évidence)",
)

__all__ = ["Hypothesis", "LCT_HYPOTHESIS", "P_SIG_HYPOTHESIS"]