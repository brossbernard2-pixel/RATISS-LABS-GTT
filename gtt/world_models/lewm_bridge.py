"""Pont LEWM (modèle du monde) — intégration de modèles.

Phase 4 (source ratiss-lewm-integration). Phase 1 : squelette.
"""


def world_state(lewm_input: object, params: dict) -> object:
    """État du monde à partir d'une entrée LEWM."""
    raise NotImplementedError("phase 4")


def update_world(world: object, observation: object, params: dict) -> object:
    """Met à jour un modèle du monde avec une observation."""
    raise NotImplementedError("phase 4")