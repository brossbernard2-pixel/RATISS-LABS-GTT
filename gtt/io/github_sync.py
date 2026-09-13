"""Synchronisation GitHub — dry-run seul, token par environnement.

Phase 6 (méthode neuve ; relais Rouge). Même doctrine que osf_sync :
aucun réseau dans le dépôt, token (GITHUB_TOKEN) par environnement
uniquement, jamais echo (masqué "***"), mode live = campagnes du chef.
STDLIB seule, déterministe.
"""

from __future__ import annotations

API = "https://api.github.com"
TOKEN_ENV = "GITHUB_TOKEN"


def get_token(env: dict) -> str | None:
    """Token depuis l'environnement uniquement (jamais de fichier)."""
    t = env.get(TOKEN_ENV)
    return t if t else None


def build_request(repo: str, params: dict) -> dict:
    """Requête canonique GitHub API v3 pour un dépôt (sans token).

    repo : "compte/nom". params : {"endpoint"} optionnel (défaut "").
    Retourne {"url", "method"} déterministe.
    """
    if repo.count("/") != 1 or not all(repo.split("/")):
        raise ValueError("repo attendu : compte/nom")
    endpoint = params.get("endpoint", "")
    suffix = f"/{endpoint.strip('/')}" if endpoint else ""
    return {"url": f"{API}/repos/{repo}{suffix}", "method": "GET"}


def sync(repo: str, env: dict, params: dict) -> dict:
    """Synchronisation DRY-RUN : reçu de requête, token masqué.

    params : {"live": True} → NotImplementedError (hors dépôt).
    """
    if params.get("live"):
        raise NotImplementedError(
            "sync reelle GitHub : campagne du chef, hors depot (aucun reseau)")
    token = get_token(env)
    return {
        "mode": "dry-run",
        "request": build_request(repo, params),
        "token_present": token is not None,
        "token": "***" if token else None,
    }


__all__ = ["get_token", "build_request", "sync", "API", "TOKEN_ENV"]
