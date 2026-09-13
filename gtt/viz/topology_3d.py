"""Topologie 3D — visualisation de diagrammes de persistance.

Phase 6 (source ratiss-decoherence-atlas pour la méthode visuelle ;
réécriture provenancée, relais Rouge). SVG texte en stdlib seule,
déterministe : projection isométrique d'un diagramme (naissance, mort),
points triés, coordonnées arrondies à ARRONDI décimales (scellé MANIFEST
viz). Classes essentielles (mort = inf) dessinées en bleu avec flèche
vers le haut et plafond affiché. Aucun asset externe.
"""

from __future__ import annotations

import math

ARRONDI = 3  # décimales (scellé MANIFEST viz)
_C, _S = math.cos(math.pi / 6), math.sin(math.pi / 6)


def _proj(x: float, y: float) -> tuple[float, float]:
    """Projection isométrique au sol d'un point (x = naissance, y = 0)."""
    return (x - y) * _C, (x + y) * _S


def diagram_to_svg(points: list, params: dict) -> str:
    """SVG d'un diagramme de persistance en projection isométrique.

    points : [(naissance, mort)] ; mort peut être float('inf') (classe
    essentielle). params : {"size"} optionnel. Déterministe : mêmes
    points (même ordre ou non, tri appliqué) → exactement même chaîne.
    """
    if not points:
        raise ValueError("diagramme vide")
    size = float(params.get("size", 400))
    finis = sorted((b, d) for b, d in points if math.isfinite(d))
    essentiels = sorted((b, d) for b, d in points if not math.isfinite(d))
    bornes = [b for b, _ in points] + [d for _, d in finis]
    plafond = max(bornes) * 1.1 if max(bornes) > 0 else 1.0
    echelle = (size * 0.6) / plafond
    cx, cy = size / 2, size * 0.62

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size:g}" '
        f'height="{size:g}" viewBox="0 0 {size:g} {size:g}">',
        f'<rect width="{size:g}" height="{size:g}" fill="#ffffff"/>',
        f'<text x="8" y="16" font-size="12" fill="#333">diagramme de '
        f'persistance — plafond {round(plafond, ARRONDI)}</text>',
        f'<line x1="{round(cx - size * 0.4, ARRONDI)}" y1="{round(cy, ARRONDI)}"'
        f' x2="{round(cx + size * 0.4, ARRONDI)}" y2="{round(cy, ARRONDI)}" '
        'stroke="#888888" stroke-width="1"/>',
    ]
    for b, d in finis:
        px, py = _proj(b * echelle, 0.0)
        sx = round(cx + px, ARRONDI)
        sy = round(cy + py - d * echelle, ARRONDI)
        parts.append(f'<circle cx="{sx}" cy="{sy}" r="3" fill="#c0392b"/>')
    for b, _ in essentiels:
        px, py = _proj(b * echelle, 0.0)
        sx = round(cx + px, ARRONDI)
        sy = round(cy + py - size * 0.42, ARRONDI)
        parts.append(f'<circle cx="{sx}" cy="{sy}" r="3" fill="#2980b9"/>')
        parts.append(
            f'<line x1="{sx}" y1="{sy}" x2="{sx}" '
            f'y2="{round(sy - 12, ARRONDI)}" stroke="#2980b9" '
            'stroke-width="1"/>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


__all__ = ["diagram_to_svg", "ARRONDI"]
