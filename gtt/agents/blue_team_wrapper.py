"""Wrapper bleu — défense constructive face au rapport juge.

Le bleu ne « prouve » rien : il répond par des reproductions rejouables.
Voir docs/PROTOCOL.md pour le rôle complet.
"""


def respond_to_findings(findings: dict, evidence: list, params: dict) -> dict:
    """Assemble une réponse d'équipe bleue à partir de rejouages exploitables."""
    raise NotImplementedError("phase 6")


def reproduce(claim: dict, params: dict) -> tuple[bool, str]:
    """Rejoue une affirmation et rend un verdict calculé (R7)."""
    raise NotImplementedError("phase 6")