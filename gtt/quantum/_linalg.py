"""Algèbre linéaire minimale — interne (aucune API publique de couche).

Jacobi symétrique (valeurs/vecteurs propres), SVD Jacobi unilatéral,
produits matriciels denses. STDLIB seule, déterministe (pas de RNG).
Phase 3 (relais Rouge). Tailles visées : matrices <= 256x256.
"""

from __future__ import annotations

import math


def matvec(m: list[list[float]], v: list[float]) -> list[float]:
    """Produit matrice-vecteur dense."""
    return [sum(mij * vj for mij, vj in zip(row, v)) for row in m]


def dot(u: list[float], v: list[float]) -> float:
    """Produit scalaire réel."""
    return sum(a * b for a, b in zip(u, v))


def norm(u: list[float]) -> float:
    """Norme L2 réelle."""
    return math.sqrt(dot(u, u))


def transpose(m: list[list[float]]) -> list[list[float]]:
    """Transposée dense."""
    return [list(col) for col in zip(*m)]


def jacobi_eig_sym(a_in: list[list[float]], tol: float = 1e-14,
                   max_sweeps: int = 100
                   ) -> tuple[list[float], list[list[float]]]:
    """Valeurs/vecteurs propres d'une matrice réelle symétrique.

    Jacobi cyclique déterministe. Retourne (valeurs croissantes, vecteurs
    en colonnes, signe fixé : plus grande composante absolue positive).
    """
    n = len(a_in)
    a = [row[:] for row in a_in]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                off = max(off, abs(a[i][j]))
        if off <= tol:
            break
        for p in range(n):
            for q in range(p + 1, n):
                apq = a[p][q]
                if abs(apq) <= tol:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * apq)
                t = math.copysign(
                    1.0 / (abs(theta) + math.sqrt(theta * theta + 1.0)), theta)
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    order = sorted(range(n), key=lambda i: (a[i][i], i))
    vals = [a[i][i] for i in order]
    vecs = [[v[k][i] for i in order] for k in range(n)]
    for j in range(n):
        kmax = max(range(n), key=lambda k: abs(vecs[k][j]))
        if vecs[kmax][j] < 0:
            for k in range(n):
                vecs[k][j] = -vecs[k][j]
    return vals, vecs


def jacobi_svd(m_in: list[list[float]], tol: float = 1e-14,
               max_sweeps: int = 100
               ) -> tuple[list[list[float]], list[float], list[list[float]]]:
    """SVD unilatéral Jacobi : M = U diag(sv) V^T, sv décroissantes.

    Déterministe : signes fixés par la plus grande composante absolue de
    chaque colonne de U. Colonnes quasi-nulles -> U colonne nulle.
    """
    rows = len(m_in)
    cols = len(m_in[0]) if m_in else 0
    a = [row[:] for row in m_in]
    v = [[1.0 if i == j else 0.0 for j in range(cols)] for i in range(cols)]
    for _ in range(max_sweeps):
        done = True
        for p in range(cols):
            for q in range(p + 1, cols):
                alpha = sum(a[i][p] * a[i][p] for i in range(rows))
                beta = sum(a[i][q] * a[i][q] for i in range(rows))
                gamma = sum(a[i][p] * a[i][q] for i in range(rows))
                if abs(gamma) <= tol * max(alpha, beta, 1e-300):
                    continue
                done = False
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(
                    1.0 / (abs(zeta) + math.sqrt(zeta * zeta + 1.0)), zeta)
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = t * c
                for i in range(rows):
                    ap, aq = a[i][p], a[i][q]
                    a[i][p] = c * ap - s * aq
                    a[i][q] = s * ap + c * aq
                for i in range(cols):
                    vp, vq = v[i][p], v[i][q]
                    v[i][p] = c * vp - s * vq
                    v[i][q] = s * vp + c * vq
        if done:
            break
    sv = [math.sqrt(sum(a[i][j] * a[i][j] for i in range(rows)))
          for j in range(cols)]
    u = [[(a[i][j] / sv[j] if sv[j] > tol else 0.0) for j in range(cols)]
         for i in range(rows)]
    for j in range(cols):
        kmax = max(range(rows), key=lambda i: abs(u[i][j]))
        if u[kmax][j] < 0:
            for i in range(rows):
                u[i][j] = -u[i][j]
            for i in range(cols):
                v[i][j] = -v[i][j]
    order = sorted(range(cols), key=lambda j: (-sv[j], j))
    sv = [sv[j] for j in order]
    u = [[row[j] for j in order] for row in u]
    v = [[row[j] for j in order] for row in v]
    return u, sv, v


def keep_singular_values(sv: list[float], max_bond: int,
                         floor: float = 1e-13) -> int:
    """Nombre de valeurs singulières à garder (plancher relatif + borne)."""
    top = sv[0] if sv else 0.0
    kept = sum(1 for s in sv if s > floor * max(top, 1e-300))
    return max(1, min(max_bond, kept))
