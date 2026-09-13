"""Thermodynamique de l'information : Shannon, KL, Helmholtz, fluctuation.

Phase 2 (réécriture provenancée depuis RATISS-ODV-AEON). STDLIB seule.
L'entropie et l'énergie libre mesurent des distributions finies ; elles ne
décrètent rien (outil de mesure).
"""

from __future__ import annotations

import math
import random


def shannon_entropy(p: list[float], bits: bool = True) -> float:
    """Entropie de Shannon d'une distribution finie p (somme(p)=1).

    Garde documentée : p_i == 0 ne contribue pas (limite x*log(x) -> 0).
    """
    if bits:
        return -sum(x * math.log2(x) for x in p if x > 0)
    return -sum(x * math.log(x) for x in p if x > 0)


def kl_divergence(p: list[float], q: list[float]) -> float:
    """Divergence de Kullback-Leibler D(p||q), nats.

    Garde division par zéro documentée : si q_i == 0 et p_i > 0, KL est
    infinie (événement prédit impossible). Si p_i == 0, contribution nulle.
    """
    if len(p) != len(q):
        raise ValueError("longueurs de p et q différentes")
    total = 0.0
    for pi, qi in zip(p, q):
        if pi == 0:
            continue
        if qi == 0:
            return float("inf")
        total += pi * math.log(pi / qi)
    return total


def helmholtz_free_energy(u: float, temperature: float,
                          entropy: float) -> float:
    """Énergie libre de Helmholtz F = U - T*S sur une distribution finie."""
    return u - temperature * entropy


def fluctuation_ratio_forward_backward(forward: list[float],
                                       backward: list[float]) -> float:
    """Rapport des probabilités avant/arrière le long d'une trajectoire.

    Retourne ln(P_av/P_ar) cumulé (signe : travail dissipé). Utilisée sur
    trajectoires synthétiques déterministes (seed fixée) en phase 2.
    """
    if len(forward) != len(backward):
        raise ValueError("trajectoires de longueurs différentes")
    return sum(math.log(f / b) if b > 0 else float("inf")
               for f, b in zip(forward, backward) if f > 0 and b > 0)


def synthetic_trajectories(seed: int = 20260913, steps: int = 40,
                           drift: float = 0.02) -> tuple[list[float], list[float]]:
    """Trajectoires synthétiques déterministes avant/arrière (seed fixée)."""
    rng = random.Random(seed)
    forward, backward = [], []
    p = 0.5
    for _ in range(steps):
        p = min(0.99, p + drift + rng.uniform(-0.01, 0.01))
        forward.append(p)
        p2 = min(0.99, p - drift + rng.uniform(-0.01, 0.01))
        backward.append(p2)
    return forward, backward