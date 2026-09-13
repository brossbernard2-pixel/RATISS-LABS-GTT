"""Bot de prévisions Metaculus — couche Jonathan SEULE.

Phase 5 (source metac-bot-template, COUCHE JONATHAN SEULE — jamais la base
officielle, liste noire §7.5 ; réécriture provenancée, relais Rouge).
HORS-LIGNE et DÉSARMÉ par construction :
- questions depuis fixtures locales (aucun réseau dans le dépôt) ;
- plafond 200 questions/run (règle du labo) ;
- `submit_predictions` = False en dur : toute tentative de soumission
  réelle lève — les vraies soumissions (FutureEval, Metaculus) passent par
  le compte du chef, hors dépôt, avec reçu scellé ensuite (R7).
STDLIB seule + primitives du juge, déterministe.
"""

from __future__ import annotations

import json

from .sealed_predictions import seal_prediction

CAP_QUESTIONS = 200
SUBMIT_AUTORISE = False  # en dur — jamais True dans ce dépôt


def collect_questions(params: dict) -> list:
    """Récupère les questions de prévision (fixtures hors-ligne).

    params : {"source": "fixture", "fixture": [...]} ou {"source": "file",
    "path": "...json"}. Plafond CAP_QUESTIONS appliqué (troncature +
    drapeau) — la déviation doit être journalisée par l'appelant (R5).
    """
    source = params.get("source", "fixture")
    if source == "fixture":
        questions = list(params.get("fixture", []))
    elif source == "file":
        with open(params["path"], encoding="utf-8") as fh:
            questions = json.load(fh)
    else:
        raise NotImplementedError(
            f"source hors-ligne uniquement : {source} (aucun réseau)")
    for q in questions:
        if "id" not in q or "question" not in q:
            raise ValueError("question invalide : id et question requis")
    truncated = len(questions) > CAP_QUESTIONS
    return questions[:CAP_QUESTIONS] if truncated else questions


def submit_forecast(question: object, probability: float, params: dict) -> str:
    """Soumet une prévision après scellement (R5) — EN SEC.

    Aucune soumission réelle n'existe ici (SUBMIT_AUTORISE = False) :
    retourne un reçu sec `dry-<16 du scellé>` déterministe. Le contenu
    scellé = id de question + probabilité + contexte du run ; le scellé se
    publie AVANT l'issue (voir sealed_predictions). params peut contenir
    {"submit_predictions": ...} : toute valeur vraie lève ValueError.
    """
    if params.get("submit_predictions") or not SUBMIT_AUTORISE is False:
        raise ValueError(
            "soumission reelle interdite dans le depot (compte du chef, "
            "hors depot, recu R7 ensuite)")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probabilité hors [0, 1]")
    content = json.dumps({"id": question["id"], "p": probability},
                         sort_keys=True, separators=(",", ":"))
    seal = seal_prediction(content, params)
    return f"dry-{seal[:16]}"


def count_source(params: dict) -> int:
    """Nombre brut de questions dans la source (avant plafond)."""
    if params.get("source", "fixture") == "fixture":
        return len(params.get("fixture", []))
    with open(params["path"], encoding="utf-8") as fh:
        return len(json.load(fh))


def run_offline(params: dict) -> dict:
    """Run complet hors-ligne : collecte → prévisions de base → scellement.

    Prévision de base scellée au MANIFEST : p = 0.5 (aucune information,
    aucun avantage inventé). Retourne {"n_questions", "truncated",
    "receipts", "sealed_before_outcome": True}.
    """
    questions = collect_questions(params)
    truncated = count_source(params) > CAP_QUESTIONS
    receipts = {}
    for q in questions:
        receipts[q["id"]] = submit_forecast(q, 0.5, params)
    return {"n_questions": len(questions), "truncated": truncated,
            "receipts": receipts, "sealed_before_outcome": True}


__all__ = ["CAP_QUESTIONS", "SUBMIT_AUTORISE", "collect_questions",
           "count_source", "submit_forecast", "run_offline"]
