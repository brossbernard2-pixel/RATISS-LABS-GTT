"""Hash rejouable — ancrage vérifiable d'une commande (R7).

Phase 6 (reconstruction receipt, réutilise ratiss.verify du juge).
Squelette jusqu'à la phase 6.
"""


def replayable_command_hash(command: str, params: dict) -> str:
    """Hash SHA-256 canonique d'une commande rejouable."""
    raise NotImplementedError("phase 6")


def verify_command_hash(command: str, seal: str) -> bool:
    """Compare un hash de commande à un scellé (bool)."""
    raise NotImplementedError("phase 6")