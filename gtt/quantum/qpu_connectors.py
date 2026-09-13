"""Connecteurs QPU — IBM Open Plan uniquement.

Phase 5 (source QPU-Ratiss-COSMOS, IBM Open Plan seul).
Phase 1 : squelette. Aucun token en phase 1 ; tokens en variables
d'environnement comme prévu à la phase 6.
"""


def connect(plan: str, env: dict) -> object:
    """Connecte un plan QPU (Open Plan). env['IBM_TOKEN'] à la phase 6."""
    raise NotImplementedError("phase 5")


def submit(circuit: object, backend: object, params: dict) -> str:
    """Soumet un circuit sur un backend. Idem, token en variable env."""
    raise NotImplementedError("phase 5")