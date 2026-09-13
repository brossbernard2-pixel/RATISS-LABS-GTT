"""Wrapper rouge — applique les primitives du juge, sans approuver.

C3 : ce module n'a AUCUNE identité d'approbation. Il exécute la CLI couche 1
(ratiss) et renvoie les verdicts bruts ; le sens est interprété par le
protocole (docs/PROTOCOL.md), jamais par ce code.
"""


def run_check(module: str, args: list, params: dict) -> dict:
    """Exécute une primitive du juge et renvoie {verdict, exit, output}."""
    raise NotImplementedError("phase 2")


def audit_against(manifest: dict, seal: str) -> tuple[bool, str]:
    """Re-scelle un manifeste et compare au scellé (ratiss.seal)."""
    raise NotImplementedError("phase 2")