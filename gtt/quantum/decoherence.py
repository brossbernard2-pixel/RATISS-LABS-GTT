"""Décohérence et temps de cohérence ambient.

Phase 3 (sources RATISS-QPU-AMBIENT, ratiss-topological-decoherence-engine).
Aucun calcul avant la phase 3 ; signatures verrouillées (R5).
"""


def coherence_time(qubit: object, ambient: dict, params: dict) -> float:
    """Temps de cohérence d'un qubit dans un environnement donné."""
    raise NotImplementedError("phase 3")


def decoherence_rate(circuit: object, params: dict) -> float:
    """Taux de décohérence d'un circuit topologique."""
    raise NotImplementedError("phase 3")


def ambient_coupling_map(qubits: list, params: dict) -> dict:
    """Carte de couplage ambiant (qubits, params) -> mapping."""
    raise NotImplementedError("phase 3")