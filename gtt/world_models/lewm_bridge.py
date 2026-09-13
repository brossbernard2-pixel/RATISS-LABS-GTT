"""Pont LEWM (modèle du monde) — intégration de modèles.

Phase 4 (source ratiss-lewm-integration pour la méthode ; réécriture
provenancée, relais Rouge). Deux dynamiques scellées au MANIFEST :
- `exact_harmonic` : oscillateur harmonique en pas analytique (l'énergie
  E = (v² + ω²x²)/2 est CONSERVÉE exactement — vérité analytique) ;
- `learned_surrogate` : surrogate « appris » synthétique — Euler explicite
  avec gain (l'énergie dérive ; pour gain=0 la dérive est EXACTEMENT
  (1 + ω²dt²)^t, vérité analytique testée).

Le vrai pont LeWM/JEPA est une campagne ultérieure : inférence seule,
JAMAIS de réentraînement du modèle audité (doctrine du labo). Les worlds
sont des dicts immuables à l'appel : update_world renvoie une copie.
STDLIB seule, déterministe.
"""

from __future__ import annotations

import math

MODELS = ("exact_harmonic", "learned_surrogate")


def energy(world: dict) -> float:
    """Énergie de l'oscillateur : E = (v² + ω² x²) / 2."""
    x, v = world["state"]
    w = world["omega"]
    return 0.5 * (v * v + w * w * x * x)


def world_state(lewm_input: object, params: dict) -> object:
    """État du monde à partir d'une entrée LEWM.

    lewm_input : {"model": MODELS, "x0": [x, v]}. params : {"omega", "dt",
    "gain"} (scellés au MANIFEST world_models). Retourne un world dict.
    """
    model = lewm_input["model"]
    if model not in MODELS:
        raise ValueError(f"modele inconnu : {model} (scelles : {MODELS})")
    x0, v0 = lewm_input["x0"]
    return {
        "model": model,
        "state": [float(x0), float(v0)],
        "t": 0,
        "omega": float(params.get("omega", 1.0)),
        "dt": float(params.get("dt", 0.1)),
        "gain": float(params.get("gain", 0.0)),
        "corrected": False,
    }


def _step_exact(w: dict) -> list[float]:
    """Pas analytique de l'oscillateur (rotation exacte du plan (x, v/ω))."""
    x, v = w["state"]
    om, dt = w["omega"], w["dt"]
    c, s = math.cos(om * dt), math.sin(om * dt)
    return [x * c + (v / om) * s, -om * x * s + v * c]


def _step_learned(w: dict) -> list[float]:
    """Pas du surrogate appris : Euler explicite + gain (dérive l'énergie)."""
    x, v = w["state"]
    om, dt, g = w["omega"], w["dt"], w["gain"]
    xn = x + dt * v
    vn = (v - dt * om * om * x) * (1.0 + g)
    return [xn, vn]


def update_world(world: object, observation: object, params: dict) -> object:
    """Met à jour un modèle du monde avec une observation.

    observation : accepté pour l'interface (dict ou None) ; les dynamiques
    scellées de phase 4 sont autonomes (aucun forçage). params :
    {"correct": bool} ignoré — la correction passe par correction.py,
    jamais par ici. Renvoie une COPIE (jamais de mutation de l'entrée).
    Si world["corrected"] : le pas brut est suivi d'une remise à l'échelle
    (x, v) * sqrt(E_avant / E_apres) — correction EN AVAL, modèle intact.
    """
    w = dict(world)
    w["state"] = list(world["state"])
    e_before = energy(w)
    if w["model"] == "exact_harmonic":
        w["state"] = _step_exact(w)
    elif w["model"] == "learned_surrogate":
        w["state"] = _step_learned(w)
    else:
        raise ValueError(f"modele inconnu : {w['model']}")
    if w.get("corrected"):
        e_after = energy(w)
        if e_after > 0.0:
            s = math.sqrt(e_before / e_after)
            w["state"] = [c * s for c in w["state"]]
    w["t"] = world["t"] + 1
    return w


def rollout(world: object, steps: int) -> list[dict]:
    """Trajectoire déterministe : [world_0, world_1, ..., world_steps]."""
    out = [dict(world, state=list(world["state"]))]
    for _ in range(steps):
        out.append(update_world(out[-1], None, {}))
    return out


__all__ = ["MODELS", "energy", "world_state", "update_world", "rollout"]
