"""Orchestrateur d'exécution — phase 6.

Sources ratiss-cypher-odv-scientist-v3, ratiss-scientist-agent (réécriture
provenancée, relais Rouge). AUCUNE identité d'approbation (C3) :
l'orchestrateur enchaîne des étapes d'un registre fourni par l'appelant et
rapporte des résultats bruts. Qui approuve ? Le protocole
(docs/PROTOCOL.md) et le chef — jamais ce code. STDLIB seule.
"""

from __future__ import annotations


def orchestrate(steps: list, context: dict, params: dict) -> dict:
    """Enchaîne des étapes du protocole (voir docs/PROTOCOL.md).

    steps : [{"name": str, "fn": callable(ctx, params) -> dict}]. Chaque
    fn reçoit le contexte (copie) et ses résultats fusionnent dans le
    contexte pour l'étape suivante. Retourne {"results", "context",
    "ok"} — ok = toutes les étapes ont rendu {"ok": True} ou n'ont pas
    rendu de drapeau (succès d'exécution, PAS approbation).
    """
    registry = params.get("registry", {})
    ctx = dict(context)
    results = []
    for step in steps:
        name = step["name"]
        fn = step.get("fn") or registry.get(name)
        if fn is None:
            raise ValueError(f"étape sans fonction ni registre : {name}")
        out = fn(dict(ctx), params)
        out = out if isinstance(out, dict) else {"value": out}
        results.append({"name": name, "out": out})
        ctx.update(out)
    ok = all(r["out"].get("ok", True) for r in results)
    return {"results": results, "context": ctx, "ok": ok,
            "authority": "aucune — exécution rapportée, pas approuvée"}


def handoff(step: str, input_ctx: dict, params: dict) -> object:
    """Transfère une étape au composant suivant (enveloppe, sans autorité).

    Retourne l'enveloppe {"step", "payload", "note"} — le payload est une
    COPIE ; rien n'est transformé ni validé ici.
    """
    if not step:
        raise ValueError("étape requise")
    return {"step": step, "payload": dict(input_ctx),
            "note": "enveloppe de transfert — aucune approbation"}


__all__ = ["orchestrate", "handoff"]
