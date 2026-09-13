"""Score de cohérence physique — OUTIL de mesure, sans verdict.

Phase 2. Le score agrège les résultats de vérificateurs d'invariants en une
fraction pondérée dans [0, 1] avec détail par invariant. Il mesure, il ne
décrète aucun statut.
"""

from __future__ import annotations


def coherence_score(invariant_results: dict[str, bool],
                    weights: dict[str, float] | None = None) -> dict:
    """Score de cohérence pondéré ∈ [0,1] à partir de résultats d'invariants.

    - invariant_results : {nom_invariant: bool_respecte}
    - weights : {nom: poids>=0} ; par défaut poids égal.
    Retourne {score, detail: {nom: (respecte, poids)}}.
    """
    if not invariant_results:
        raise ValueError("au moins un invariant requis")
    weights = weights or {k: 1.0 for k in invariant_results}
    total = sum(w for k, w in weights.items() if k in invariant_results)
    if total <= 0:
        raise ValueError("poids totaux nuls")
    detail = {}
    num = 0.0
    for name, ok in invariant_results.items():
        w = weights.get(name, 1.0)
        detail[name] = (bool(ok), w)
        if ok:
            num += w
    return {"score": num / total, "detail": detail}