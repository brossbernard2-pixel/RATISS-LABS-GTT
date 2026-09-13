"""Algèbre Z2 minimale pour la topologie — interne (aucune API publique).

Rang de matrices 0/1 sur F2 et réduction de colonnes de bord pour
l'homologie persistante. Docstrings courtes ; ce n'est pas un module couche.
"""


def z2_rank(mat: list[list[int]]) -> int:
    """Rang d'une matrice 0/1 sur F2 (élimination gaussienne booléenne)."""
    mat = [row[:] for row in mat]
    h, w = len(mat), (len(mat[0]) if mat else 0)
    r = 0
    for c in range(w):
        piv = next((i for i in range(r, h) if mat[i][c]), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        for i in range(h):
            if i != r and mat[i][c]:
                mat[i] = [a ^ b for a, b in zip(mat[i], mat[r])]
        r += 1
    return r


def reduce_boundary(cols: list[set[int]]) -> tuple[list[set[int]], dict[int, int]]:
    """Réduit les colonnes de bord ; renvoie (reduit, pairs) avec pairs[low]=j.

    Convention : low(j) est le plus grand indice de ligne à 1 dans la colonne
    réduite R_j. pairs[low]=j pour chaque colonne non vide.
    """
    n = len(cols)
    col_red = [set(c) for c in cols]
    pairs: dict[int, int] = {}
    low: dict[int, int] = {}
    for j in range(n):
        c = set(col_red[j]) - set()  # copie
        while c and max(c) in low:
            c ^= col_red[low[max(c)]]
        col_red[j] = set(c)
        if c:
            i = max(c)
            low[i] = j
            pairs[i] = j
    return col_red, pairs


def _max_matching(adj: list[list[int]], left: list[int]) -> int:
    """Taille d'un couplage maximum (augmenting paths) sur graphe biparti."""
    pair_r: dict[int, int] = {}

    def augment(u, seen):
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in pair_r or augment(pair_r[v], seen):
                pair_r[v] = u
                return True
        return False

    size = 0
    for u in left:
        if augment(u, set()):
            size += 1
    return size


def bottleneck_distance(dgm1: list[tuple[float, float]],
                        dgm2: list[tuple[float, float]]) -> float:
    """Distance bottleneck exacte (L_inf) entre deux diagrammes.

    dgm1/dgm2 : listes de points (naissance, mort) avec naissance <= mort.
    Recherche binaire sur delta + couplage parfait sur les diagrammes
    augmentés de leurs projections diagonales.
    """
    M = lambda p: ((p[0] + p[1]) / 2, (p[0] + p[1]) / 2)
    left = list(dgm1) + [M(p) for p in dgm2]
    right = list(dgm2) + [M(p) for p in dgm1]
    lo, hi = 0.0, max((max(abs(a[0] - b[0]), abs(a[1] - b[1]))
                       for a in left for b in right), default=0.0)
    n = len(left)
    for _ in range(60):
        d = (lo + hi) / 2
        adj = [[v for v in range(n)
                if max(abs(left[u][0] - right[v][0]),
                       abs(left[u][1] - right[v][1])) <= d]
               for u in range(n)]
        if _max_matching(adj, list(range(n))) == n:
            hi = d
        else:
            lo = d
    return hi
