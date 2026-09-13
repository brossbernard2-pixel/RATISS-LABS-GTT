"""Vérification de reçus — couche juge (R7).

Phase 6 (reconstruction receipts ; relais Rouge). Vérifie la COHÉRENCE
INTERNE d'un reçu structuré : champs présents (scellés au MANIFEST
receipts), scellé de commande recalculé identique, format SHA-256 valide.
Ne juge jamais la véracité du contenu externe — pour ça il faut rejouer
la commande (blue_team_wrapper.reproduce) ou attendre les vrais reçus
Lean (EN ATTENTE, C5).
"""

from __future__ import annotations

import re

from .replayable_hash import replayable_command_hash

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CHAMPS_REQUIS = ("command", "command_sha256", "artifact_sha256", "source")


def verify_receipt(receipt: dict, params: dict) -> tuple[bool, str]:
    """Vérifie un reçu structuré et rend (ok, raison).

    receipt : {"command", "command_sha256", "artifact_sha256", "source",
    "hash_params"?}. Raison = message brut, sans interprétation au-delà
    de la conformité interne.
    """
    manquants = [c for c in CHAMPS_REQUIS if c not in receipt]
    if manquants:
        return False, f"champs manquants : {manquants}"
    if not _SHA256_RE.match(str(receipt["artifact_sha256"])):
        return False, "artifact_sha256 : format SHA-256 invalide"
    calcule = replayable_command_hash(
        receipt["command"], {"hash_params": receipt.get("hash_params", {})})
    if calcule != receipt["command_sha256"]:
        return False, (f"command_sha256 divergent : reçu "
                       f"{receipt['command_sha256'][:16]}… calculé "
                       f"{calcule[:16]}…")
    return True, "reçu cohérent (commande scellée, format valide)"


__all__ = ["verify_receipt", "CHAMPS_REQUIS"]
