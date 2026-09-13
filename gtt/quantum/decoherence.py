"""Décohérence et temps de cohérence ambient.

Phase 3 (sources RATISS-QPU-AMBIENT, ratiss-topological-decoherence-engine ;
réécriture provenancée, relais Rouge). Canaux exacts sur qubit unique
(déphasage T2, relaxation T1), pureté, entropie de von Neumann en bits.
Unités : temps en µs, taux en 1/µs. STDLIB seule, déterministe.
"""

from __future__ import annotations

import math


def apply_dephasing(rho: list[list[complex]], t: float, t2: float
                    ) -> list[list[complex]]:
    """Canal de déphasage pur : hors-diagonale * exp(-t/T2).

    Loi exacte (testée analytiquement) ; les populations sont invariantes.
    """
    if t2 <= 0:
        raise ValueError("T2 doit etre > 0")
    f = math.exp(-t / t2)
    out = [[rho[0][0], rho[0][1] * f], [rho[1][0] * f, rho[1][1]]]
    return out


def apply_amplitude_damping(rho: list[list[complex]], t: float, t1: float
                            ) -> list[list[complex]]:
    """Canal de relaxation T1 exact : rho11 * exp(-t/T1), rho01 * exp(-t/2T1).

    Convention : |1> = état excité (population rho[1][1]) qui relaxe vers
    |0>. Loi exacte testée analytiquement.
    """
    if t1 <= 0:
        raise ValueError("T1 doit etre > 0")
    e = math.exp(-t / t1)
    f = math.exp(-t / (2.0 * t1))
    p1 = rho[1][1] * e
    p0 = rho[0][0] + (rho[1][1] - p1)
    return [[p0, rho[0][1] * f], [rho[1][0] * f, p1]]


def purity(rho: list[list[complex]]) -> float:
    """Pureté Tr(rho^2) d'une matrice 2x2 hermitienne (réelle)."""
    a, b, c, d = rho[0][0], rho[0][1], rho[1][0], rho[1][1]
    return float((a * a + b * c + c * b + d * d).real)


def von_neumann_entropy_bits(rho: list[list[complex]]) -> float:
    """Entropie de von Neumann en bits (valeurs propres 2x2 analytiques)."""
    tr = float((rho[0][0] + rho[1][1]).real)
    det = float((rho[0][0] * rho[1][1] - rho[0][1] * rho[1][0]).real)
    disc = max(tr * tr / 4.0 - det, 0.0)
    root = math.sqrt(disc)
    out = 0.0
    for lam in (tr / 2.0 + root, tr / 2.0 - root):
        lam = min(max(lam, 0.0), 1.0)
        if lam > 0.0:
            out -= lam * math.log2(lam)
    return out


def coherence_time(qubit: object, ambient: dict, params: dict) -> float:
    """Temps de cohérence effectif T2* (µs) d'un qubit dans son environnement.

    qubit : {"T1", "T2"} (µs). ambient : {"extra_dephasing_rate"} (1/µs,
    bruit ambiant ajouté). params : {"model": "t2_star"} (scellé MANIFEST).
    Modèle scellé : 1/T2* = 1/T2 + extra (combinaison harmonique exacte).
    """
    if params.get("model", "t2_star") != "t2_star":
        raise NotImplementedError("modele inconnu (MANIFEST : t2_star)")
    t2 = qubit["T2"]
    extra = ambient.get("extra_dephasing_rate", 0.0)
    return 1.0 / (1.0 / t2 + extra)


def decoherence_rate(circuit: object, params: dict) -> float:
    """Probabilité de perte de cohérence d'un circuit (modèle exponentiel).

    circuit : {"duration_us", "qubits": [{"T2"}, ...]}. params :
    {"model": "exp_t2_harmonic"} (scellé MANIFEST). T2 effectif = moyenne
    harmonique des T2 des qubits ; rate = 1 - exp(-duration / T2_eff).
    """
    if params.get("model", "exp_t2_harmonic") != "exp_t2_harmonic":
        raise NotImplementedError("modele inconnu (MANIFEST)")
    t2s = [q["T2"] for q in circuit["qubits"]]
    if not t2s:
        raise ValueError("aucun qubit")
    t2_eff = len(t2s) / sum(1.0 / t for t in t2s)
    return 1.0 - math.exp(-circuit["duration_us"] / t2_eff)


def ambient_coupling_map(qubits: list, params: dict) -> dict:
    """Carte de couplage ambiant : id -> {taux de déphasage, classe}.

    qubits : [{"id", "T1", "T2"}]. params : {"good_rate_max", "mid_rate_max"}
    (1/µs, seuils scellés au MANIFEST). Classe : good/mid/bad. Aucun verdict
    physique — classification outillée des taux, point.
    """
    good = params["good_rate_max"]
    mid = params["mid_rate_max"]
    out: dict = {}
    for q in qubits:
        rate = 1.0 / q["T2"]
        cls = "good" if rate <= good else ("mid" if rate <= mid else "bad")
        out[q["id"]] = {"dephasing_rate_per_us": rate,
                        "relaxation_rate_per_us": 1.0 / q["T1"],
                        "class": cls}
    return out


__all__ = ["apply_dephasing", "apply_amplitude_damping", "purity",
           "von_neumann_entropy_bits", "coherence_time", "decoherence_rate",
           "ambient_coupling_map"]
