"""Prévisions scellées (R5) : hash publié avant, contenu après.

Phase 5 (méthode des prévisions scellées ; relais Rouge). Le scellement
réutilise la primitive canonique du JUGE (ratiss.seal) : une seule loi.
Le scellé se publie AVANT l'issue ; le contenu se révèle APRÈS ; toute
altération se détecte.
"""

from __future__ import annotations

from ratiss.seal import canonical_json
from ratiss.verify import sha256_hex


def seal_prediction(content: str, params: dict) -> str:
    """Scelle une prévision (SHA-256 canonique via le juge).

    Le contexte scellé = {"content", "context"} où context vient de
    params["context"] (horodatage, run_id… fournis par l'appelant).
    Même contenu + même contexte → exactement le même scellé.
    """
    if not isinstance(content, str) or not content:
        raise ValueError("contenu non vide requis")
    payload = {"content": content, "context": params.get("context", {})}
    return sha256_hex(canonical_json(payload))


def verify_prediction(content: str, seal: str, params: dict) -> bool:
    """Vérifie qu'un contenu révélé correspond au scellé publié (R5)."""
    return seal_prediction(content, params) == seal


def sealed_envelope(content: str, params: dict) -> dict:
    """Enveloppe à deux temps : {"seal"} à publier maintenant,
    {"reveal"} à publier après l'issue. Le seal ne dépend que du contenu
    et du contexte — jamais de l'issue."""
    return {
        "seal": seal_prediction(content, params),
        "reveal": {"content": content, "context": params.get("context", {})},
        "rule": "publier seal AVANT l'issue ; reveal APRÈS ; toute "
                "divergence = déviation journalisée (R5)",
    }


__all__ = ["seal_prediction", "verify_prediction", "sealed_envelope"]
