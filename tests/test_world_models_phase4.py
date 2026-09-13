"""Tests world_models — phase 4 (vérités analytiques + doctrine).

Portique : conservation exacte de l'harmonique analytique ; dérive EXACTE
(1 + ω²dt²)^t du surrogate appris (Euler, gain 0) ; correction en aval →
violation nulle à précision machine SANS toucher au modèle ; ablation
avec/sans = delta mesuré ; verdicts chiffrés ; immuabilité des worlds ;
MANIFEST scellé (R6).
"""

import copy
import json
import math
from pathlib import Path

import pytest

from gtt.world_models import ablation, coherence_audit, correction, lewm_bridge

PKG = Path(__file__).resolve().parents[1]
P = {"omega": 1.0, "dt": 0.1, "gain": 0.0}
AUD = {"steps": 10, "tol": 1e-9,
       "x0s": [[1.0, 0.0], [0.5, 0.5], [0.0, 1.0]]}
FACTEUR = (1.0 + P["omega"] ** 2 * P["dt"] ** 2)  # 1.01, exact


def _exact():
    return lewm_bridge.world_state(
        {"model": "exact_harmonic", "x0": [1.0, 0.0]}, P)


def _appris(gain=0.0):
    return lewm_bridge.world_state(
        {"model": "learned_surrogate", "x0": [1.0, 0.0]},
        dict(P, gain=gain))


# ---------- Dynamiques : vérités analytiques ----------

def test_harmonique_conserve_exactement():
    traj = lewm_bridge.rollout(_exact(), 50)
    e0 = lewm_bridge.energy(traj[0])
    assert max(abs(lewm_bridge.energy(s) - e0) for s in traj) < 1e-12


def test_euler_derive_exactement_facteur_analytique():
    """Euler explicite sur l'harmonique : E_t = E_0 (1 + ω²dt²)^t EXACT."""
    traj = lewm_bridge.rollout(_appris(), 10)
    e0 = lewm_bridge.energy(traj[0])
    for t, s in enumerate(traj):
        attendu = e0 * FACTEUR ** t
        assert abs(lewm_bridge.energy(s) - attendu) < 1e-12 * attendu


def test_violation_max_egale_forme_fermee():
    v = coherence_audit.violation_max(_appris(), AUD)
    assert abs(v - (FACTEUR ** 10 - 1.0)) < 1e-12


def test_gain_aggrave_la_derive():
    v0 = coherence_audit.violation_max(_appris(0.0), AUD)
    v1 = coherence_audit.violation_max(_appris(0.05), AUD)
    assert v1 > v0 > 0.0


# ---------- Audit : score et contradictions ----------

def test_coherence_score_exact_vaut_un():
    assert coherence_audit.coherence_score(_exact(), AUD) == 1.0


def test_coherence_score_appris_vaut_zero():
    assert coherence_audit.coherence_score(_appris(), AUD) == 0.0


def test_contradiction_detect():
    stmts = [{"claim": "a", "measured": 1.0, "expected": 1.0},
             {"claim": "b", "measured": 2.0, "expected": 1.0},
             {"claim": "c", "measured": 1.05, "expected": 1.0, "tol": 0.1}]
    assert coherence_audit.contradiction_detect(stmts, {"tol_defaut": 1e-9}) == [1]


# ---------- Correction : aval, jamais seule, modèle intact ----------

def test_propose_correction_ne_touche_pas_le_modele():
    w = _appris()
    avant = copy.deepcopy(w)
    patch = correction.propose_correction(w, {"type": "energy_drift"}, AUD)
    assert w == avant  # immuable
    assert patch["type"] == "energy_rescale"
    assert patch["verdict_required"] == "APPROVED"
    assert abs(patch["measured_violation"] - (FACTEUR ** 10 - 1.0)) < 1e-12


def test_apply_exige_verdict_explicite():
    w = _appris()
    patch = correction.propose_correction(w, {"type": "energy_drift"}, AUD)
    with pytest.raises(ValueError):
        correction.apply_after_review(w, patch, "peut-etre")
    with pytest.raises(ValueError):
        correction.apply_after_review(w, patch, "")


def test_correction_aval_annule_la_violation():
    w = _appris()
    avant = copy.deepcopy(w)
    fixed = correction.apply_after_review(
        w, {"type": "energy_rescale", "verdict_required": "APPROVED"},
        "APPROVED")
    assert w == avant            # le modèle n'est PAS touché
    assert fixed["corrected"] is True
    v = coherence_audit.violation_max(fixed, AUD)
    assert v < 1e-12             # exact à précision machine


# ---------- Ablation : delta mesuré, déterministe ----------

def test_run_ablation_delta_mesure():
    w = _appris()
    r = ablation.run_ablation(w, "correction", AUD)
    assert r["metric"] == "energy_violation_max"
    assert abs(r["without"] - (FACTEUR ** 10 - 1.0)) < 1e-12
    assert r["with"] < 1e-12
    assert abs(r["delta"] - r["without"]) < 1e-12
    r2 = ablation.run_ablation(w, "correction", AUD)
    assert r == r2  # déterministe


def test_ablation_verdict_chiffre():
    ok, msg = ablation.ablation_verdict(0.0, 0.1046221254, "energy_violation_max")
    assert ok is True and "delta=" in msg and "amelioration mesuree" in msg
    ko, msg2 = ablation.ablation_verdict(0.2, 0.1, "energy_violation_max")
    assert ko is False and "pas d amelioration" in msg2
    with pytest.raises(NotImplementedError):
        ablation.ablation_verdict(0.0, 1.0, "metrique_inventee")
    with pytest.raises(NotImplementedError):
        ablation.run_ablation(_appris(), "composant_invente", AUD)


# ---------- Immuabilité du pont ----------

def test_update_world_ne_mute_jamais():
    w = _appris()
    avant = copy.deepcopy(w)
    lewm_bridge.update_world(w, None, {})
    assert w == avant


# ---------- MANIFEST scellé (R6) ----------

def test_manifest_world_models_scelle():
    from ratiss.seal import seal_manifest
    manifest = json.loads(
        (PKG / "gtt/world_models/MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "0.2.0"
    assert manifest["status"] == "implemented-p4"
    p = manifest["params"]
    assert p["dynamics"]["omega"] == P["omega"]
    assert p["dynamics"]["dt"] == P["dt"]
    assert p["audit"]["steps"] == AUD["steps"]
    assert p["audit"]["x0s"] == AUD["x0s"]
    assert p["ablation"]["metric"] == "energy_violation_max"
    assert p["correction"]["verdict_required"] == "APPROVED"
    seals = json.loads((PKG / "gtt/SEALS.json").read_text(encoding="utf-8"))
    expected = next(s["sha256"] for s in seals["seals"]
                    if s["layer"] == "world_models")
    assert seal_manifest(manifest) == expected
