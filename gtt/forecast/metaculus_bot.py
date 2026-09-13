"""Bot de prévisions Metaculus — couche Jonathan SEULE.

Phase 5 (source metac-bot-template, COUCHE JONATHAN SEULE — jamais la base
officielle, voir liste noire §7.5). Squelette jusqu'à la phase 5.
"""


def collect_questions(params: dict) -> list:
    """Récupère les questions de prévision (phase 5)."""
    raise NotImplementedError("phase 5")


def submit_forecast(question: object, probability: float, params: dict) -> str:
    """Soumet une prévision après scellement (R5)."""
    raise NotImplementedError("phase 5")