"""Tenseurs MPS et DMRG pour états produits matriciels.

Phase 3 (source Algorithmes-quantique-Ratiss-labs-, Travaux).
Phase 1 : squelette.
"""


def mps_from_statevector(state: object, max_bond: int, params: dict) -> object:
    """Décompose un vecteur d'état en MPS (liens bornés). Squelette."""
    raise NotImplementedError("phase 3")


def dmrg_sweep(mps: object, hamiltonian: object, params: dict) -> object:
    """Un balayage DMRG : optimise un MPS pour un hamiltonien local."""
    raise NotImplementedError("phase 3")


def truncate_bond_dimension(mps: object, max_bond: int) -> object:
    """Tronque les liens MPS à max_bond. Pas de calcul en phase 1."""
    raise NotImplementedError("phase 3")