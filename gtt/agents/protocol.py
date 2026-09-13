"""Protocole rouge/bleu — description scellable, sans exécution.

Le protocole de référence vit dans docs/PROTOCOL.md. Ce module ne contient
aucune logique d'exécution : il décrit les étapes pour les manifests
(version scellée au MANIFEST agents). Phase 6 (relais Rouge).
"""

from __future__ import annotations

VERSIONS = {
    "1.0": [
        "bleu-construit",
        "rouge-audite",
        "chef-arbitre",
        "recu-r7",
        "visa-provenance",
    ],
}


def protocol_steps(version: str, params: dict) -> list:
    """Liste les étapes du protocole pour un manifeste (version).

    Version inconnue → ValueError (on n'invente pas de protocole).
    params réservé (aucun effet en phase 6).
    """
    if version not in VERSIONS:
        raise ValueError(
            f"version de protocole inconnue : {version} (scellées : "
            f"{sorted(VERSIONS)})")
    return list(VERSIONS[version])


__all__ = ["protocol_steps", "VERSIONS"]
