"""Décohérence et temps de cohérence ambient.

Phase 5 (sources RATISS-QPU-AMBIENT, ratiss-topological-decoherence-engine).
Phase 1 : squelette.
"""


def coherence_time(qubit: object, ambient: dict, params: dict) -> float:
    """Temps de cohérence d'un qubit dans un environnement donné."""
    raise NotImplementedError("phase 5")


def decoherence_rate(circuit: object, params: dict) -> float:
    """Taux de décohérence d'un circuit topologique."""
    raise NotImplementedError("phase 5")


def ambient_coupling_map(qubits: list, params: dict) -> dict:
    """Carte de couplage ambiant (qubits, params) -> mapping."""
    raise NotImplementedError("phase 5")