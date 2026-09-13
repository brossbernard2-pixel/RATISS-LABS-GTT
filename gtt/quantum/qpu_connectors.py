"""Connecteurs QPU — IBM Open Plan uniquement.

Phase 3 (source QPU-Ratiss-COSMOS, IBM Open Plan seul).
Squelette. Aucun token ; les tokens viendront de variables
d'environnement, jamais d'un fichier committé (C5).
"""


def connect(plan: str, env: dict) -> object:
    """Connecte un plan QPU (Open Plan). env['IBM_TOKEN'] si fourni."""
    raise NotImplementedError("phase 3")


def submit(circuit: object, backend: object, params: dict) -> str:
    """Soumet un circuit sur un backend. Token via variable env uniquement."""
    raise NotImplementedError("phase 3")