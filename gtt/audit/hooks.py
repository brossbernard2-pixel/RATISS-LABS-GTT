"""Hooks vers la CLI du juge (couche 1 du RATISS-Framework).

C4 : ce module ne redéfinit aucun principe. Il appelle la commande
`python -m ratiss` (verdicts calculés) et remonte les résultats bruts.
"""


def call_judge(args: list, params: dict) -> dict:
    """Appelle `python -m ratiss <args>` et rend {exit, output, verdict}."""
    raise NotImplementedError("phase 2")


def report_to_judge(report: dict, params: dict) -> None:
    """Soumet un rapport d'audit au juge (R7). Squelette."""
    raise NotImplementedError("phase 2")