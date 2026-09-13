"""Complexes simpliciaux finis sur Z2 : Betti, persistance, bottleneck.

Phase 2 (réécriture provenancée depuis ratiss-topological-decoherence-engine).
STDLIB seule, aucune dépendance autre que pytest et le juge.
"""

from __future__ import annotations

from ._z2 import bottleneck_distance as _bd, reduce_boundary, z2_rank


def faces(simplex: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Facettes (dim n-1) d'un simplexe."""
    return [tuple(simplex[:i] + simplex[i + 1:]) for i in range(len(simplex))]


def _by_dim(K, d):
    return sorted(set(s for s in K if len(s) - 1 == d))


def boundary_rank(K: list[tuple[int, ...]], d: int) -> int:
    """Rang de la matrice de bord d -> (d-1) sur Z2."""
    hi, lo = _by_dim(K, d), _by_dim(K, d - 1)
    if d <= 0 or not hi or not lo:
        return 0
    lo_idx = {s: i for i, s in enumerate(lo)}
    mat = [[0] * len(hi) for _ in lo]
    for col, s in enumerate(hi):
        for f in faces(s):
            if f in lo_idx:
                mat[lo_idx[f]][col] ^= 1
    return z2_rank(mat)


def betti_numbers(K: list[tuple[int, ...]], reduced: bool = False) -> tuple[int, ...]:
    """Nombres de Betti (b0..bd) d'un complexe simplicial sur Z2."""
    maxd = max((len(s) - 1 for s in K), default=0)
    cnt = {d: 0 for s in K for d in (len(s) - 1,)}
    for s in K:
        cnt[len(s) - 1] += 1
    out, prev = [], 0
    for d in range(maxd + 1):
        nxt = boundary_rank(K, d + 1)
        out.append(cnt.get(d, 0) - prev - nxt)
        prev = nxt
    if reduced and out:
        out[0] -= 1
    return tuple(out)


def persistent_pairs(K: list[tuple[int, ...]], values: list[float]
                     ) -> dict[int, list[tuple[float, float]]]:
    """Paires naissance/mort par dimension (mort=inf pour les essentielles).

    Filtration par seuil croissant (à égalité : tri lexicographique) puis
    réduction de la matrice de bord sur Z2. Une colonne réduite à zéro dont
    le simplex n'est pas un low est une classe essentielle.
    """
    order = sorted(range(len(K)), key=lambda i: (values[i], K[i]))
    tup2idx = {K[orig]: j for j, orig in enumerate(order)}
    dims = [len(K[o]) - 1 for o in order]
    cols = [set() for _ in order]
    for j, orig in enumerate(order):
        for f in faces(K[orig]):
            if f in tup2idx:
                cols[j].add(tup2idx[f])
    init_empty = {j for j, c in enumerate(cols) if not c}
    red, pairs = reduce_boundary(cols)
    paired_low = set(pairs)
    dgm = {d: [] for d in set(dims)}
    for i, j in pairs.items():
        dgm[dims[i]].append((values[order[i]], values[order[j]]))
    for i in range(len(order)):
        if i in init_empty and i not in paired_low:
            dgm[dims[i]].append((values[order[i]], float("inf")))
    return dgm


def bottleneck_distance(dgm1: list[tuple[float, float]],
                        dgm2: list[tuple[float, float]]) -> float:
    """Distance bottleneck exacte (L_inf) entre deux diagrammes.

    Version exacte pour diagrammes <= 50 points ; au-delà,
    NotImplementedError("phase 7: approximation").
    """
    if len(dgm1) > 50 or len(dgm2) > 50:
        raise NotImplementedError("phase 7: approximation")
    return _bd(dgm1, dgm2)