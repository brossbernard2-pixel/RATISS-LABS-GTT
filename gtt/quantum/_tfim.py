"""TFIM ouvert + environnements MPS — interne (aucune API publique).

H = -J sum_{i<N-1} X_i X_{i+1} - h sum_i Z_i (chaîne ouverte, réel).
Dense 2^N x 2^N pour N <= 8 (garde explicite). Environnements gauche/
droite contractés depuis les tenseurs MPS, état dense depuis MPS.
Phase 3 (relais Rouge). STDLIB seule, déterministe.
"""

from __future__ import annotations

from ._linalg import jacobi_svd, keep_singular_values

I2 = [[1.0, 0.0], [0.0, 1.0]]
X = [[0.0, 1.0], [1.0, 0.0]]
Z = [[1.0, 0.0], [0.0, -1.0]]


def kron(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Produit de Kronecker dense."""
    return [[a[i][j] * b[k][l] for j in range(len(a[0]))
             for l in range(len(b[0]))] for i in range(len(a))
            for k in range(len(b))]


def tfim_open_dense(n: int, j: float, h: float) -> list[list[float]]:
    """Hamiltonien TFIM ouvert dense (2^n x 2^n). N <= 8."""
    if n > 8:
        raise NotImplementedError("phase suivante : dense limite a N <= 8")
    dim = 1 << n
    mat = [[0.0] * dim for _ in range(dim)]

    def op_at(ops: dict[int, list[list[float]]]) -> list[list[float]]:
        out = [[1.0]]
        for site in range(n):
            out = kron(out, ops.get(site, I2))
        return out

    for i in range(n - 1):
        m = op_at({i: X, i + 1: X})
        for r in range(dim):
            for c in range(dim):
                mat[r][c] -= j * m[r][c]
    for i in range(n):
        m = op_at({i: Z})
        for r in range(dim):
            for c in range(dim):
                mat[r][c] -= h * m[r][c]
    return mat


def energy_dense(mat: list[list[float]], state: list[float]) -> float:
    """<psi|H|psi> / <psi|psi> sur vecteur réel."""
    nrm = sum(x * x for x in state)
    if nrm <= 0.0:
        raise ValueError("vecteur nul")
    hs = [sum(mij * vj for mij, vj in zip(row, state)) for row in mat]
    return sum(a * b for a, b in zip(state, hs)) / nrm


def env_left(tensors: list, upto: int) -> list[list[float]]:
    """Environnement gauche L[a, cl] pour les sites 0..upto-1.

    L[r, (cl << 1) | s] = somme_a L[a, cl] * T[a][s][r].
    """
    env = [[1.0]]
    for t in tensors[:upto]:
        chi_l, _, chi_r = len(t), 2, len(t[0][0])
        ncl = len(env[0])
        new = [[0.0] * (ncl * 2) for _ in range(chi_r)]
        for a in range(chi_l):
            for cl in range(ncl):
                lav = env[a][cl]
                if lav == 0.0:
                    continue
                for s in (0, 1):
                    for r in range(chi_r):
                        new[r][(cl << 1) | s] += lav * t[a][s][r]
        env = new
    return env


def env_right(tensors: list, frm: int) -> list[list[float]]:
    """Environnement droit R[l, cr] pour les sites frm..N-1.

    R_new[l, (s << len_cr) | cr] = somme_r T[l][s][r] * R[r, cr].
    """
    env = [[1.0]]
    for t in reversed(tensors[frm:]):
        chi_l, _, chi_r = len(t), 2, len(t[0][0])
        ncr = len(env[0])
        new = [[0.0] * (2 * ncr) for _ in range(chi_l)]
        for l in range(chi_l):
            for s in (0, 1):
                for r in range(chi_r):
                    tval = t[l][s][r]
                    if tval == 0.0:
                        continue
                    for cr in range(ncr):
                        new[l][s * ncr + cr] += tval * env[r][cr]
        env = new
    return env


def state_from_mps(tensors: list) -> list[float]:
    """Vecteur d'état dense (2^N) contracté depuis un MPS."""
    env = env_left(tensors, len(tensors))
    return env[0][:]


def split_config(row: int, n: int, i: int
                 ) -> tuple[int, int, int, int]:
    """Découpe (cl, sigma, tau, cr) d'une config pour le lien (i, i+1).

    Convention de bits : le site j pèse 2^(N-1-j) ; cl = i bits de tête,
    sigma = site i, tau = site i+1, cr = N-i-2 bits de queue.
    """
    ncr = n - i - 2
    cr = row & ((1 << ncr) - 1)
    tau = (row >> ncr) & 1
    sigma = (row >> (ncr + 1)) & 1
    cl = row >> (ncr + 2)
    return cl, sigma, tau, cr


def _absorb_left(carry: list[list[float]], t: list) -> list:
    """Contracte une matrice de poids à gauche d'un tenseur."""
    chi_c = len(carry)
    chi_t = len(t)
    chi_r = len(t[0][0])
    return [[[sum(carry[a2][a] * t[a][s_][r] for a in range(chi_t))
              for r in range(chi_r)] for s_ in (0, 1)]
            for a2 in range(chi_c)]


def _absorb_right(t: list, carry: list[list[float]]) -> list:
    """Contracte une matrice de poids à droite d'un tenseur."""
    chi_l = len(t)
    chi_c = len(carry[0])
    return [[[sum(t[a][s_][r] * carry[r][b] for r in range(len(carry)))
              for b in range(chi_c)] for s_ in (0, 1)] for a in range(chi_l)]


def left_canonicalize(tensors: list, upto: int, max_bond: int) -> list:
    """Jauge gauche : sites 0..upto-1 left-orthonormaux, poids poussés
    dans le site `upto`. Assure L^T L = I pour l'environnement gauche."""
    out = [t for t in tensors]
    carry = None
    for i in range(upto):
        t = _absorb_left(carry, out[i]) if carry is not None else out[i]
        chi_l, chi_r = len(t), len(t[0][0])
        mat = [[t[a][s_][r] for r in range(chi_r)]
               for a in range(chi_l) for s_ in (0, 1)]
        u, sv, vt = jacobi_svd(mat)
        chi = keep_singular_values(sv, max_bond)
        out[i] = [[[u[a * 2 + s_][k] for k in range(chi)] for s_ in (0, 1)]
                  for a in range(chi_l)]
        carry = [[sv[k] * vt[c][k] for c in range(chi_r)] for k in range(chi)]
    if carry is not None:
        out[upto] = _absorb_left(carry, out[upto])
    return out


def right_canonicalize(tensors: list, frm: int, max_bond: int) -> list:
    """Jauge droite : sites frm+1..N-1 right-orthonormaux, poids poussés
    dans le site `frm`. Assure R R^T = I pour l'environnement droit.

    T[l][s][r] vu comme matrice lignes l, colonnes (s,r) : SVD = U S V^T ;
    le tenseur right-orthonormal est V (colonnes orthonormées sur (s,r)),
    le poids U S est poussé vers le site frm.
    """
    out = [t for t in tensors]
    carry = None
    for i in range(len(tensors) - 1, frm, -1):
        t = _absorb_right(out[i], carry) if carry is not None else out[i]
        chi_l, chi_r = len(t), len(t[0][0])
        mat = [[t[a][s_][r] for s_ in (0, 1) for r in range(chi_r)]
               for a in range(chi_l)]
        u, sv, vt = jacobi_svd(mat)
        chi = keep_singular_values(sv, max_bond)
        out[i] = [[[vt[s_ * chi_r + r][k] for r in range(chi_r)]
                   for s_ in (0, 1)] for k in range(chi)]
        carry = [[u[c][k] * sv[k] for k in range(chi)] for c in range(chi_l)]
    if carry is not None:
        out[frm] = _absorb_right(out[frm], carry)
    return out
