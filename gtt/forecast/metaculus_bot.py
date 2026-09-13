"""Bot de prévisions Metaculus — couche Jonathan SEULE.

Phase 4 (source metac-bot-template, COUCHE JONATHAN SEULE — jamais la base
officielle, voir liste noire §7.5). Phase 1 : squelette.
"""


def collect_questions(params: dict) -> list:
    """Récupère les questions de prévision (phase 4)."""
    raise NotImplementedError("phase 4")


def submit_forecast(question: object, probability: float, params: dict) -> str:
    """Soumet une prévision après scellement (R5)."""
    raise NotImplementedError("phase 4")