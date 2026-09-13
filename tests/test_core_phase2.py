"""Tests core — phase 2 (vérités analytiques + outils).

Portique §6 : triangle, bord tétraèdre, tore 4×4, sphères disjointes ;
persistance ; invariants ; cohérence ; hypothèses HYPOTHESIS + protocole.
"""

import itertools
import json
from pathlib import Path

import pytest

from gtt.core import coherence, hypotheses, invariants, thermodynamics
from gtt.core.topology import (betti_numbers, bottleneck_distance,
                               persistent_pairs)

PKG = Path(__file__).resolve().parents[1]


# ---------- Constructions simpliciales ----------

def _triangle_plein():
    return [(0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]


def _bord_tetraedre():
    K = [(v,) for v in range(4)]
    K += [tuple(sorted(e)) for e in itertools.combinations(range(4), 2)]
    K += list(itertools.combinations(range(4), 3))
    return K


def _tore_4x4():
    K = {(v,) for v in range(16)}
    v = lambda a, b: (a % 4) * 4 + (b % 4)
    edges, tris = set(), set()
    for i in range(4):
        for j in range(4):
            s, a, b, c = v(i, j), v(i + 1, j), v(i, j + 1), v(i + 1, j + 1)
            edges.add(tuple(sorted((s, a))))
            edges.add(tuple(sorted((s, b))))
            edges.add(tuple(sorted((s, c))))
            tris.add(tuple(sorted((s, a, c))))
            tris.add(tuple(sorted((s, c, b))))
    return list(K | edges | tris)


def _deux_spheres():
    K = []
    for base in (0, 4):
        sommets = range(base, base + 4)
        K += [(v,) for v in sommets]
        K += [tuple(sorted(e)) for e in itertools.combinations(sommets, 2)]
        K += list(itertools.combinations(sommets, 3))
    return K


def _cercle():
    return [(0,), (1,), (2,), (3,), (0, 1), (1, 2), (2, 3), (3, 0)]


# ---------- Betti (vérités analytiques) ----------

def test_betti_triangle():
    assert betti_numbers(_triangle_plein()) == (1, 0, 0)


def test_betti_bord_tetraedre():
    # surface S^2 : vérité analytique (1, 0, 1)
    assert betti_numbers(_bord_tetraedre()) == (1, 0, 1)


def test_betti_cycle_1_1_0():
    # un cercle unique : signature (1, 1, 0) sur (b0, b1, b2)
    b = betti_numbers(_cercle())
    assert b + (0,) * (3 - len(b)) == (1, 1, 0)


def test_betti_tore_4x4():
    assert betti_numbers(_tore_4x4()) == (1, 2, 1)


def test_betti_deux_spheres_b0():
    assert betti_numbers(_deux_spheres())[0] == 2


# ---------- Persistance ----------

def test_persistance_triangle():
    tri = _triangle_plein()
    dgm = persistent_pairs(tri, [0, 0, 0, 1, 1, 1, 2])
    h0 = sorted((a, b) for a, b in dgm[0] if b != float("inf"))
    assert h0 == [(0.0, 1.0), (0.0, 1.0)]
    assert sum(1 for _, b in dgm[0] if b == float("inf")) == 1
    assert dgm[1] == [(1.0, 2.0)]


# ---------- Bottleneck ----------

def test_bottleneck_identical():
    d1 = [(0, 1), (0, 2), (2, 3.0)]
    assert bottleneck_distance(d1, list(d1)) < 1e-9


def test_bottleneck_notimplemented_si_plus_de_50():
    big = [(float(i) / 100, float(i) / 100 + 1) for i in range(51)]
    with pytest.raises(NotImplementedError):
        bottleneck_distance(big, [])


# ---------- Invariants ----------

def test_conservation_exacte_et_perturbee():
    r = invariants.check_conservation([1, 2, 3], [5, 5, 5])
    assert r["ok"] and r["violation_max"] == 0.0
    eps = 1e-6
    r2 = invariants.check_conservation([1, 2, 3], [5, 5 + eps, 5], tol=eps / 2)
    assert not r2["ok"]
    assert abs(r2["violation_max"] - eps) < 1e-12


def test_symplecticite_det_egal_un():
    assert invariants.check_symplecticite((1.0, 0.5, 0.0, 1.0), [])["ok"]
    r = invariants.check_symplecticite((2.0, 0.0, 0.0, 1.0), [])
    assert not r["ok"] and abs(r["det"] - 2.0) < 1e-12


def test_reversibilite_exacte_et_perturbee():
    f = lambda x: [x[0] + 0.25]
    g = lambda x: [x[0] - 0.25]
    assert invariants.check_reversibilite(f, [1.0, 2.0], g,
                                         steps=5, tol=1e-12)["ok"]
    f2 = lambda x: [x[0] + 0.25 + 1e-6]
    r = invariants.check_reversibilite(f2, [1.0, 2.0], g, steps=5, tol=1e-4)
    assert r["ok"]
    r3 = invariants.check_reversibilite(f2, [1.0, 2.0], g, steps=5, tol=1e-6)
    assert not r3["ok"] and abs(r3["erreur_max"] - 5e-6) < 1e-9


# ---------- Cohérence ----------

def test_coherence_score_pondere():
    res = {"conservation": True, "symplecticite": False}
    out = coherence.coherence_score(res, {"conservation": 2.0,
                                          "symplecticite": 1.0})
    assert out["score"] == 2.0 / 3.0
    assert out["detail"]["symplecticite"] == (False, 1.0)


def test_coherence_score_exige_invariants():
    with pytest.raises(ValueError):
        coherence.coherence_score({})


# ---------- Hypothèses ----------

def test_hypotheses_statut_et_params_figes():
    for name in ("LCT_HYPOTHESIS", "P_SIG_HYPOTHESIS"):
        hyp = getattr(hypotheses, name)
        assert hyp.status == "HYPOTHESIS"
        assert hyp.params
        assert hyp.as_dict() == hyp.as_dict()


def test_hypotheses_params_scelles_dans_manifest():
    """Les params du code doivent être ceux scellés dans le MANIFEST core."""
    from ratiss.seal import seal_manifest
    manifest = json.loads(
        (PKG / "gtt/core/MANIFEST.json").read_text(encoding="utf-8"))
    m = manifest["params"]["hypotheses"]
    assert m["LCT"]["status"] == hypotheses.LCT_HYPOTHESIS.status
    assert (m["LCT"]["refutation_threshold"]
            == hypotheses.LCT_HYPOTHESIS.params["refutation_threshold"])
    assert (m["P_sig"]["refutation_threshold"]
            == hypotheses.P_SIG_HYPOTHESIS.params["refutation_threshold"])
    seals = json.loads((PKG / "gtt/SEALS.json").read_text(encoding="utf-8"))
    expected = next(s["sha256"] for s in seals["seals"] if s["layer"] == "core")
    assert seal_manifest(manifest) == expected


def test_protocole_renvoie_des_mesures():
    p = hypotheses.LCT_HYPOTHESIS.protocole()
    assert p["mesurabilité"] is True
    assert p["metric"] == "psig_mean_abs"
    assert p["seuil_refutation"] == 0.01


# ---------- Thermodynamique ----------

def test_shannon_et_kl():
    assert thermodynamics.shannon_entropy([0.5, 0.5]) == 1.0
    assert thermodynamics.shannon_entropy([1.0]) == 0.0
    assert thermodynamics.kl_divergence([0.5, 0.5], [0.5, 0.5]) == 0.0
    assert thermodynamics.kl_divergence([1.0, 0.0], [0.0, 1.0]) == float("inf")


def test_helmholtz():
    assert thermodynamics.helmholtz_free_energy(10.0, 2.0, 3.0) == 4.0