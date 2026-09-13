"""Vérificateurs d'invariants numériques (déterministes, phase 2).

Conservation, symplecticité et réversibilité sont testées sur des données
exactes (violation 0) et des perturbations connues (violation ~ eps).
STDLIB seule.
"""

from __future__ import annotations

import math


def check_conservation(trajectory: list[float], quantity: list[float],
                       tol: float = 1e-9) -> dict:
    """Vérifie qu'une quantité est conservée le long d'une trajectoire.

    Retourne {ok, violation_max, position}. Données exactes -> violation 0 ;
    perturbation eps connue -> violation ~ eps à la tolérance près.
    """
    if len(trajectory) != len(quantity) or not quantity:
        raise ValueError("trajectoire et quantité de longueurs égales non nulles")
    base = quantity[0]
    viol, pos = 0.0, 0
    for i, q in enumerate(quantity):
        v = abs(q - base)
        if v > viol:
            viol, pos = v, i
    return {"ok": viol <= tol, "violation_max": viol, "position": pos}


def check_symplecticite(map_coeffs: tuple[float, float, float, float],
                        points: list[tuple[float, float]],
                        tol: float = 1e-9) -> dict:
    """Vérifie la symplecticité d'une application linéaire 2D (a,b,c,d).

    Une carte (x',y')=(a x + b y, c x + d y) est symplectique sur R2 si
    le déterminant vaut 1 (Préservation de l'aire). Retourne
    {ok, det, ecart}.
    """
    a, b, c, d = map_coeffs
    det = a * d - b * c
    deviation = abs(det - 1.0)
    return {"ok": deviation <= tol, "det": det, "ecart": deviation}


def check_reversibilite(f: callable, x0: list[float], inv_f: callable,
                        steps: int = 5, tol: float = 1e-9) -> dict:
    """Vérifie que f puis inv_f (aller-retour déterministe) ramène à x0.

    Retourne {ok, erreur_max}. Données exactes -> erreur 0 ; un epsilon de
    perturbation dans f -> erreur ~ eps.
    """
    x = list(x0)
    for _ in range(steps):
        x = list(f(x))
    for _ in range(steps):
        x = list(inv_f(x))
    erreur = max(abs(a - b) for a, b in zip(x, x0))
    return {"ok": erreur <= tol, "erreur_max": erreur}