"""Tests examples — phase 7 (terrains déterministes + vérité analytique).

TERRAIN-02 (SIR) : conservation EXACTE, perturbation ε vue, Betti cycle4.
TERRAIN-03 (chaleur) : masse conservée dans les deux sondes, stabilité de
von Neumann reproduite (r=0.4 décroît, r=0.6 explose), cohérence 3/3.
Les expected.json committés doivent être reproduits au bit près.
"""

import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
import importlib.util


def _charger(terrain: str, module: str):
    """Charge generate/run_core d'un terrain sans collision de noms."""
    chemin = PKG / "examples" / terrain / f"{module}.py"
    spec = importlib.util.spec_from_file_location(f"{terrain}_{module}", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load(terrain, nom):
    return json.loads((PKG / "examples" / terrain / nom).read_text(encoding="utf-8"))


def test_terrain02_reproduit_expected():
    rc2 = _charger("TERRAIN-02", "run_core")
    out = rc2.run(PKG / "examples/TERRAIN-02/sir.json")
    assert out == _load("TERRAIN-02", "expected.json")
    assert out["conservation_violation"] == 0.0
    assert abs(out["perturbation_violation"] - 1e-6) < 1e-18
    assert out["betti_reseau"] == [1, 1]
    assert out["coherence_score"] == 1.0


def test_terrain02_generation_deterministe():
    gen2 = _charger("TERRAIN-02", "generate")
    data = gen2.build_sir()
    committed = _load("TERRAIN-02", "sir.json")
    assert data == committed


def test_terrain03_reproduit_expected():
    rc3 = _charger("TERRAIN-03", "run_core")
    out = rc3.run(PKG / "examples" / "TERRAIN-03" / "heat.json")
    assert out == _load("TERRAIN-03", "expected.json")
    st, ins = out["stable"], out["instable"]
    assert st["violation_masse"] <= 1e-9 and ins["violation_masse"] <= 1e-9
    assert st["amplitude_decroissante"] is True
    assert ins["amplitude_decroissante"] is False
    assert ins["amplitude_finale"] > 2.0 * ins["amplitude_initiale"]
    assert out["coherence_score"] == 1.0


def test_terrain03_graine_documentee():
    data = _load("TERRAIN-03", "expected.json")
    assert data["stable"]["graine_von_neumann"] == 1e-3
    assert data["stable"]["graine_von_neumann"] == data["instable"]["graine_von_neumann"]


def test_tombstones_orphelins():
    texte = (PKG / "docs/ORPHELINS.md").read_text(encoding="utf-8")
    assert texte.count("GELÉ") >= 14
    assert "jamais supprimer" in texte
    for sha in ("2cf2cc618c46f23e", "4f8a4ddb1aef5cb8", "48a89bf8c0e63f19"):
        assert sha in texte
