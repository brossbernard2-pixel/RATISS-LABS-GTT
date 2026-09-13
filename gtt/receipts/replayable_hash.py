"""Hash rejouable — ancrage vérifiable d'une commande (R7).

Phase 6 (reconstruction receipts ; réécriture provenancée, relais Rouge).
Réutilise la canonisation du JUGE (ratiss.seal) : une seule loi. Le scellé
d'une commande ne dépend que de la commande et des paramètres de hash —
rejouer la commande et re-vérifier le scellé est à la portée de tous.
"""

from __future__ import annotations

from ratiss.seal import canonical_json
from ratiss.verify import sha256_hex


def replayable_command_hash(command: str, params: dict) -> str:
    """Hash SHA-256 canonique d'une commande rejouable.

    params : {"hash_params": {...}} optionnel — contexte ajouté au scellé
    (version d'outil, seed…). Même commande + même contexte → même scellé.
    """
    if not command or not command.strip():
        raise ValueError("commande non vide requise")
    payload = {"command": command, "hash_params": params.get("hash_params", {})}
    return sha256_hex(canonical_json(payload))


def verify_command_hash(command: str, seal: str) -> bool:
    """Compare un hash de commande à un scellé (bool)."""
    return replayable_command_hash(command, {}) == seal


__all__ = ["replayable_command_hash", "verify_command_hash"]
