"""Hash rejouable — ancrage vérifiable d'une commande (R7).

Phase 2 (reconstruction receipt, réutilise ratiss.verify du juge).
Phase 1 : squelette.
"""


def replayable_command_hash(command: str, params: dict) -> str:
    """Hash SHA-256 canonique d'une commande rejouable."""
    raise NotImplementedError("phase 2")


def verify_command_hash(command: str, seal: str) -> bool:
    """Compare un hash de commande à un scellé (bool)."""
    raise NotImplementedError("phase 2")