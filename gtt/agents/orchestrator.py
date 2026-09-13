"""Orchestrateur d'exécution — phase 5.

Sources ratiss-cypher-odv-scientist-v3, ratiss-scientist-agent.
Squelette uniquement : aucune identité d'approbation.
"""


def orchestrate(steps: list, context: dict, params: dict) -> dict:
    """Enchaîne des étapes du protocole (voir docs/PROTOCOL.md)."""
    raise NotImplementedError("phase 5")


def handoff(step: str, input_ctx: dict, params: dict) -> object:
    """Transfère une étape au composant suivant. Skeleton."""
    raise NotImplementedError("phase 5")