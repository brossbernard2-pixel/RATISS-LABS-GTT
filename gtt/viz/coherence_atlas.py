"""Atlas de cohérence — heatmap SVG de scores [0, 1].

Phase 6 (sources ratiss-decoherence-atlas, quantum-circuit-studio pour la
méthode visuelle ; réécriture provenancée, relais Rouge). SVG texte stdlib,
déterministe : une case par score, gris #000 (0) → #fff (1), arrondi des
coordonnées scellé au MANIFEST viz. Aucun asset externe.
"""

from __future__ import annotations

ARRONDI = 3


def _gris(v: float) -> str:
    """Niveau de gris hex déterministe d'un score [0, 1]."""
    if not 0.0 <= v <= 1.0:
        raise ValueError(f"score hors [0, 1] : {v}")
    g = round(v * 255)
    return f"#{g:02x}{g:02x}{g:02x}"


def atlas_svg(matrice: list, params: dict) -> str:
    """Heatmap SVG d'une matrice de scores de cohérence.

    matrice : listes de listes de floats dans [0, 1]. params : {"cell",
    "labels"} optionnels (cell = taille de case en px ; labels = lignes
    affichées). Déterministe : mêmes entrées → même chaîne au bit près.
    """
    if not matrice or not all(len(l) == len(matrice[0]) for l in matrice):
        raise ValueError("matrice vide ou rectangulaire requise")
    cell = float(params.get("cell", 18))
    labels = params.get("labels", False)
    marge = 24.0 if labels else 4.0
    lignes, cols = len(matrice), len(matrice[0])
    w = round(marge * 2 + cols * cell, ARRONDI)
    h = round(marge * 2 + lignes * cell, ARRONDI)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">',
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
    ]
    if labels:
        parts.append(f'<text x="4" y="14" font-size="11" fill="#333">'
                     f'atlas de coherence ({lignes}x{cols})</text>')
    for i, ligne in enumerate(matrice):
        for j, v in enumerate(ligne):
            x = round(marge + j * cell, ARRONDI)
            y = round(marge + i * cell, ARRONDI)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell:g}" height="{cell:g}" '
                f'fill="{_gris(v)}" stroke="#dddddd" stroke-width="0.5"/>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


__all__ = ["atlas_svg", "ARRONDI"]
