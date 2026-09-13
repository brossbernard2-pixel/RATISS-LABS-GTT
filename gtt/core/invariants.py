"""Invariants topologiques et de complexité.

Phase 4 : audit physique de complexité (sources RATISS-V10 et
Algorithmes-quantique-Ratiss-labs-). Phase 1 : squelette.
"""


def physical_complexity(circuit: object, params: dict) -> float:
    """Complexité physique d'un circuit/objet (phase 4).

    Calcul scellé avec paramètres et hash (R4). Non implémenté.
    """
    raise NotImplementedError("phase 4")


def invariant_v10(sequence: object, params: dict) -> dict:
    """Invariant V10 de complexité physique.

    Version squelette : aucun chiffre publié avant calcul (R4).
    """
    raise NotImplementedError("phase 4")


def check_reference_change(baseline: str, measured: str) -> tuple[bool, str]:
    """Compare deux références (baseline, measured) -> (ok, raison)."""
    raise NotImplementedError("phase 4")