"""Algorithme de Lanczos pour spectres de systèmes topologiques.

Phase 3 (source Algorithmes-quantique-Ratiss-labs-, QPU-Ratiss-COSMOS ;
réécriture provenancée, relais Rouge). Lanczos à réorthogonalisation
complète sur matrices réelles symétriques ; spectre diagonalisé via Jacobi
(gtt.quantum._linalg). STDLIB seule, déterministe (seed du MANIFEST).
"""

from __future__ import annotations

import random

from ._linalg import dot, jacobi_eig_sym, matvec, norm


def convergence_criterion(residual: float, tolerance: float) -> bool:
    """Critère de convergence sur le résiduel de Lanczos."""
    return abs(residual) <= tolerance


def lanczos_iteration(matrix: object, k: int, params: dict) -> dict:
    """Itérations de Lanczos (matrice, k, params) -> spectre approché.

    matrix : liste de listes réelle symétrique. k : nombre de valeurs
    extrémales basses demandées. params (scellés au MANIFEST quantum) :
    tolerance, max_iter, seed. Retourne {eigenvalues (k plus basses,
    croissantes), residual, iterations, converged}.
    """
    mat = [list(row) for row in matrix]
    n = len(mat)
    tol = params.get("tolerance", 1e-10)
    maxit = min(params.get("max_iter", n), n)
    seed = params.get("seed", 20260913)
    if k < 1 or k > n:
        raise ValueError("k hors bornes [1, n]")
    rng = random.Random(seed)
    v = [rng.uniform(-1.0, 1.0) for _ in range(n)]
    nv = norm(v)
    v = [x / nv for x in v]
    basis: list[list[float]] = []
    alpha: list[float] = []
    beta: list[float] = []
    vprev: list[float] = [0.0] * n
    bprev = 0.0
    blast = 0.0
    for _ in range(maxit):
        basis.append(v)
        w = matvec(mat, v)
        a = dot(w, v)
        alpha.append(a)
        w = [w[i] - a * v[i] - (bprev * vprev[i] if bprev else 0.0)
             for i in range(n)]
        for u in basis:  # réorthogonalisation complète (stabilité)
            d = dot(w, u)
            if d:
                w = [w[i] - d * u[i] for i in range(n)]
        b = norm(w)
        blast = b
        if b <= tol:
            bprev, vprev = 0.0, [0.0] * n
            break
        beta.append(b)
        vprev, bprev = v, b
        v = [x / b for x in w]
    m = len(alpha)
    tri = [[0.0] * m for _ in range(m)]
    for i in range(m):
        tri[i][i] = alpha[i]
        if i + 1 < m:
            tri[i][i + 1] = tri[i + 1][i] = beta[i]
    vals, vecs = jacobi_eig_sym(tri, tol=1e-14)
    # Résiduel de la valeur extrême basse : b_final * |dernière composante|
    # du vecteur de Ritz (b_final = dernier beta calculé, y compris celui
    # du breakdown qui marque l'épuisement de Krylov).
    resid = abs(blast * vecs[m - 1][0]) if m else 0.0
    return {
        "eigenvalues": vals[:k],
        "residual": resid,
        "iterations": m,
        "converged": convergence_criterion(resid, tol),
    }
