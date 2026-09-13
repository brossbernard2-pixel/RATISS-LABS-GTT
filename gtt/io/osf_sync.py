"""Synchronisation OSF — dry-run seul, token par environnement.

Phase 6 (méthode neuve ; relais Rouge). AUCUN réseau dans le dépôt :
build_request construit la requête canonique, sync rend un reçu dry-run.
Le token (OSF_TOKEN) vient de l'environnement, n'est JAMAIS inclus ni
echo dans une sortie (masqué en "***"). Le mode live appartient aux
campagnes du chef (NotImplementedError). STDLIB seule.
"""

from __future__ import annotations

API = "https://api.osf.io/v2"
TOKEN_ENV = "OSF_TOKEN"


def get_token(env: dict) -> str | None:
    """Token depuis l'environnement uniquement (jamais de fichier)."""
    t = env.get(TOKEN_ENV)
    return t if t else None


def build_request(node_id: str, params: dict) -> dict:
    """Requête canonique OSF v2 (sans token — il s'ajoute à l'exécution).

    params : {"endpoint"} optionnel (défaut "nodes"). Retourne
    {"url", "method", "query"} déterministe.
    """
    endpoint = params.get("endpoint", "nodes")
    query = params.get("query", {})
    qs = "&".join(f"{k}={query[k]}" for k in sorted(query))
    url = f"{API}/{endpoint}/{node_id}/" + (f"?{qs}" if qs else "")
    return {"url": url, "method": "GET", "query": dict(sorted(query.items()))}


def sync(node_id: str, env: dict, params: dict) -> dict:
    """Synchronisation DRY-RUN : reçu de requête, token masqué.

    params : {"live": True} → NotImplementedError (campagnes du chef,
    hors dépôt). Le reçu ne contient JAMAIS la valeur du token.
    """
    if params.get("live"):
        raise NotImplementedError(
            "sync reelle OSF : campagne du chef, hors depot (aucun reseau)")
    token = get_token(env)
    return {
        "mode": "dry-run",
        "request": build_request(node_id, params),
        "token_present": token is not None,
        "token": "***" if token else None,
    }


__all__ = ["get_token", "build_request", "sync", "API", "TOKEN_ENV"]
