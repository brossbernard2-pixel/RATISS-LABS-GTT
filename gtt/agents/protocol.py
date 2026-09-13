"""Protocole rouge/bleu — description scellable, sans exécution.

Le protocole de référence vit dans docs/PROTOCOL.md. Ce module ne contient
aucune logique d'exécution : il décrit les étapes pour les manifests.
"""


def protocol_steps(version: str, params: dict) -> list:
    """Liste les étapes du protocole pour un manifeste (version)."""
    raise NotImplementedError("phase 2")