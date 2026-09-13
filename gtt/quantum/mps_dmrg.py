"""Tenseurs MPS et DMRG pour états produits matriciels.

Phase 3 (sources Algorithmes-quantique-Ratiss-labs-, Travaux ; réécriture
provenancée, relais Rouge). MPS = liste de tenseurs T[a][s][b] (a=lien
gauche, s=physique 2, b=lien droit). DMRG 2 sites : hamiltonien effectif
EXACT contracté depuis les environnements gauche/droit, diagonalisé par
Jacobi, re-splitté par SVD Jacobi avec troncature. STDLIB seule.
Limite documentée : dense N <= 8 en phase 3 (MPO généraux ensuite).
"""

from __future__ import annotations

from ._linalg import jacobi_eig_sym, jacobi_svd, keep_singular_values
from ._tfim import (energy_dense, env_left, env_right, left_canonicalize,
                    right_canonicalize, split_config, state_from_mps,
                    tfim_open_dense)


def _keep(sv: list[float], max_bond: int) -> int:
    """Nombre de valeurs singulières à garder (délégue à _linalg)."""
    return keep_singular_values(sv, max_bond)


def mps_from_statevector(state: object, max_bond: int, params: dict) -> object:
    """Décompose un vecteur d'état réel normalisé en MPS (liens bornés).

    Retourne {tensors, N, error (norme tronquée relative), max_bond}.
    SVD successifs gauche -> droite ; params : {"svd_floor": optionnel}.
    """
    vec = [float(x) for x in state]
    dim = len(vec)
    n = dim.bit_length() - 1
    if (1 << n) != dim or n < 1:
        raise ValueError("longueur non puissance de 2")
    nrm = sum(x * x for x in vec) ** 0.5
    cur = [[x / nrm for x in vec]]   # 1 x 2^n
    tensors: list = []
    discarded = 0.0
    for site in range(n):
        rows, cols = len(cur), len(cur[0])
        half = cols // 2
        mat = [[0.0] * half for _ in range(rows * 2)]
        for a in range(rows):
            for s in (0, 1):
                src = cur[a][s * half:(s + 1) * half]
                mat[a * 2 + s] = src
        u, sv, vt = jacobi_svd(mat)
        chi = _keep(sv, max_bond)
        discarded += sum(s * s for s in sv[chi:])
        tensors.append([[[u[a * 2 + s][k] for k in range(chi)]
                         for s in (0, 1)] for a in range(rows)])
        cur = [[sv[k] * vt[c][k] for c in range(half)] for k in range(chi)]
    return {"tensors": tensors, "N": n, "error": discarded ** 0.5,
            "max_bond": max_bond}


def truncate_bond_dimension(mps: object, max_bond: int) -> object:
    """Tronque les liens MPS à max_bond (SVD par paire de sites).

    Retourne {tensors, trunc_error, max_bond}.
    """
    tensors = [t for t in mps["tensors"]]
    trunc = 0.0
    for i in range(len(tensors) - 1):
        ti, tj = tensors[i], tensors[i + 1]
        chi_l, chi_mid, chi_r = len(ti), len(ti[0][0]), len(tj[0][0])
        if chi_mid <= max_bond:
            continue
        mat = [[0.0] * (2 * chi_r) for _ in range(chi_l * 2)]
        for a in range(chi_l):
            for s1 in (0, 1):
                for k in range(chi_mid):
                    v1 = ti[a][s1][k]
                    if v1 == 0.0:
                        continue
                    for s2 in (0, 1):
                        for b in range(chi_r):
                            mat[a * 2 + s1][s2 * chi_r + b] += v1 * tj[k][s2][b]
        u, sv, vt = jacobi_svd(mat)
        chi = _keep(sv, max_bond)
        trunc += sum(s * s for s in sv[chi:])
        tensors[i] = [[[u[a * 2 + s][k] for k in range(chi)]
                       for s in (0, 1)] for a in range(chi_l)]
        tensors[i + 1] = [[[sv[k] * vt[s2 * chi_r + b][k] for b in range(chi_r)]
                           for s2 in (0, 1)] for k in range(chi)]
    return {"tensors": tensors, "trunc_error": trunc ** 0.5,
            "max_bond": max_bond}


def _two_site_update(tensors: list, ham: list[list[float]], n: int,
                     i: int, max_bond: int) -> list:
    """Update DMRG 2 sites sur le lien (i, i+1) : H_eff exact + Jacobi.

    Jauge canonique d'abord (left_canonicalize jusqu'à i, right_canonicalize
    depuis i+1) : les environnements sont alors orthonormés (L^T L = I,
    R R^T = I) et le problème aux valeurs propres STANDARD sur H_eff est
    équivalent au problème généralisé — sans jauge, λmin(H_eff) n'est pas
    le minimum variationnel (bug capturé à l'audit : E/2 au lieu de E).
    """
    tensors = left_canonicalize(tensors, i, max_bond)
    tensors = right_canonicalize(tensors, i + 1, max_bond)
    left = env_left(tensors, i)
    right = env_right(tensors, i + 2)
    chi_l, ncl = len(left), len(left[0])
    chi_r, ncr = len(right), len(right[0])
    dim = chi_l * 4 * chi_r

    def idx(a: int, s: int, t: int, b: int) -> int:
        return ((a * 2 + s) * 2 + t) * chi_r + b

    heff = [[0.0] * dim for _ in range(dim)]
    for cl in range(ncl):
        for cl2 in range(ncl):
            ll = [left[a][cl] * left[a2][cl2]
                  for a in range(chi_l) for a2 in range(chi_l)]
            if not any(ll):
                continue
            for cr in range(ncr):
                for cr2 in range(ncr):
                    rr = [right[b][cr] * right[b2][cr2]
                          for b in range(chi_r) for b2 in range(chi_r)]
                    if not any(rr):
                        continue
                    for s1 in (0, 1):
                        for t1 in (0, 1):
                            row = ((cl << 2 | s1 << 1 | t1)
                                   << (n - i - 2)) | cr
                            hv_row = ham[row]
                            for s2 in (0, 1):
                                for t2 in (0, 1):
                                    col = ((cl2 << 2 | s2 << 1 | t2)
                                           << (n - i - 2)) | cr2
                                    hv = hv_row[col]
                                    if hv == 0.0:
                                        continue
                                    for a in range(chi_l):
                                        for a2 in range(chi_l):
                                            c = ll[a * chi_l + a2] * hv
                                            if c == 0.0:
                                                continue
                                            r1 = idx(a, s1, t1, 0)
                                            c1 = idx(a2, s2, t2, 0)
                                            for b in range(chi_r):
                                                for b2 in range(chi_r):
                                                    heff[r1 + b][c1 + b2] += (
                                                        c * rr[b * chi_r + b2])
    vals, vecs = jacobi_eig_sym(heff)
    del vals
    ground = [vecs[r][0] for r in range(dim)]
    mat = [[0.0] * (2 * chi_r) for _ in range(chi_l * 2)]
    for a in range(chi_l):
        for s in (0, 1):
            for t in (0, 1):
                for b in range(chi_r):
                    mat[a * 2 + s][t * chi_r + b] = ground[idx(a, s, t, b)]
    u, sv, vt = jacobi_svd(mat)
    chi = _keep(sv, max_bond)
    ti = [[[u[a * 2 + s][k] for k in range(chi)] for s in (0, 1)]
          for a in range(chi_l)]
    tj = [[[sv[k] * vt[t * chi_r + b][k] for b in range(chi_r)]
           for t in (0, 1)] for k in range(chi)]
    out = list(tensors)  # tensors déjà canonicalisés : gauge cohérente
    out[i], out[i + 1] = ti, tj
    return out


def dmrg_sweep(mps: object, hamiltonian: object, params: dict) -> object:
    """Balayages DMRG 2 sites (gauche->droite puis droite->gauche).

    hamiltonian : {"N", "J", "h"} (modèle TFIM ouvert scellé au MANIFEST).
    params : {"sweeps", "max_bond"}. Retourne {tensors, energy, history}.
    """
    n = hamiltonian["N"]
    j = hamiltonian.get("J", 1.0)
    h = hamiltonian.get("h", 0.7)
    sweeps = params.get("sweeps", 2)
    max_bond = params.get("max_bond", 4)
    ham = tfim_open_dense(n, j, h)
    tensors = [[[[c for c in b] for b in a] for a in t]
               for t in mps["tensors"]]
    history: list[float] = []
    for _ in range(sweeps):
        for i in range(n - 1):
            tensors = _two_site_update(tensors, ham, n, i, max_bond)
        for i in reversed(range(n - 1)):
            tensors = _two_site_update(tensors, ham, n, i, max_bond)
        history.append(energy_dense(ham, state_from_mps(tensors)))
    return {"tensors": tensors, "energy": history[-1], "history": history,
            "N": n, "J": j, "h": h}


__all__ = ["mps_from_statevector", "dmrg_sweep", "truncate_bond_dimension",
           "split_config"]
