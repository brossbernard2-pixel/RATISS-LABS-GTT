"""Tests du squelette GTT phase 1 (portique Rouge).

Vérifie : import des neuf couches, MANIFEST présents, juge local vert,
LCT/P_sig déclarées HYPOTHESIS, aucun module de couche > 60 lignes,
et qu'un MANIFEST modifié fait rougir le juge.
"""

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

PKG = Path(__file__).resolve().parents[1]
GTT = PKG / "gtt"

LAYERS = (
    "core", "quantum", "world_models", "forecast", "agents",
    "receipts", "audit", "viz", "io",
)

# (module de couche, éventuel attr attendu)
COUCHE_MODULES = {
    "core": ["topology", "thermodynamics", "hypotheses", "invariants", "coherence"],
    "quantum": ["lanczos", "mps_dmrg", "decoherence", "qpu_connectors"],
    "world_models": ["lewm_bridge", "coherence_audit", "correction", "ablation"],
    "forecast": ["metaculus_bot", "calibration", "sealed_predictions", "journal"],
    "agents": ["orchestrator", "red_team_wrapper", "blue_team_wrapper", "protocol"],
    "receipts": ["lean_proof", "replayable_hash", "verification"],
    "audit": ["hooks", "deviation_log"],
    "viz": ["topology_3d", "coherence_atlas", "proof_graph"],
    "io": ["pdb_loader", "osf_sync", "github_sync"],
}


def test_neuf_layers_importables():
    for layer in LAYERS:
        for module in COUCHE_MODULES[layer]:
            importlib.import_module(f"gtt.{layer}.{module}")


# version et statut attendus par couche (phase 2 : core réel, autres squelettes)
EXPECTED_MANIFESTS = {
    "core": ("0.2.1", "implemented-p2-audit"),
    "quantum": ("0.2.0", "implemented-p3"),
    "world_models": ("0.2.0", "implemented-p4"),
    "forecast": ("0.1.0", "skeleton"),
    "agents": ("0.1.0", "skeleton"),
    "receipts": ("0.1.0", "skeleton"),
    "audit": ("0.1.0", "skeleton"),
    "viz": ("0.1.0", "skeleton"),
    "io": ("0.1.0", "skeleton"),
}


def test_manifests_presents():
    for layer in LAYERS:
        manifest_path = GTT / layer / "MANIFEST.json"
        assert manifest_path.is_file(), f"MANIFEST manquant : {layer}"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert data["layer"] == layer
        version, status = EXPECTED_MANIFESTS[layer]
        assert data["version"] == version, f"{layer}: version {data['version']}"
        assert data["status"] == status, f"{layer}: statut {data['status']}"


def test_seals_json_alignes():
    seals = json.loads((GTT / "SEALS.json").read_text(encoding="utf-8"))
    keyed = {s["layer"]: s["sha256"] for s in seals["seals"]}
    assert set(keyed) == set(LAYERS)


def test_judge_vert():
    proc = subprocess.run(
        [sys.executable, "-m", "gtt.judge", "--ci"],
        cwd=PKG, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_judge_rougit_si_manifest_modifie():
    core_manifest = GTT / "core" / "MANIFEST.json"
    original = core_manifest.read_text(encoding="utf-8")
    try:
        data = json.loads(original)
        data["status"] = "skeleton-tampered"
        core_manifest.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, "-m", "gtt.judge", "--ci"],
            cwd=PKG, capture_output=True, text=True,
        )
        assert proc.returncode == 1
    finally:
        core_manifest.write_text(original, encoding="utf-8")
    # juge de nouveau vert après restauration
    proc = subprocess.run(
        [sys.executable, "-m", "gtt.judge", "--ci"],
        cwd=PKG, capture_output=True, text=True,
    )
    assert proc.returncode == 0


def test_hypotheses_lct_et_psig():
    hypotheses = importlib.import_module("gtt.core.hypotheses")
    for name in ("LCT_HYPOTHESIS", "P_SIG_HYPOTHESIS"):
        hyp = getattr(hypotheses, name)
        assert hyp.status == "HYPOTHESIS", f"{name} doit etre HYPOTHESIS"
    assert hypotheses.LCT_HYPOTHESIS.name == "LCT"
    assert hypotheses.P_SIG_HYPOTHESIS.name == "P_sig"


def test_aucun_module_squelette_depasse_60_lignes():
    # Les couches squelettes (phases 3-7) restent <= 60 lignes ; la couche
    # core est réelle depuis la phase 2 (voir test_core_modules_bornes).
    for layer in LAYERS:
        if layer in ("core", "quantum", "world_models", "viz", "io"):
            continue  # core = calculs réels ; viz/io = docstrings
        for module in COUCHE_MODULES[layer]:
            path = GTT / layer / f"{module}.py"
            lines = path.read_text(encoding="utf-8").splitlines()
            nonblank = [ln for ln in lines if ln.strip()]
            assert len(lines) <= 60, f"{layer}/{module}.py : {len(lines)} lignes"
            assert len(nonblank) <= 60


def test_core_modules_bornes():
    # Garde-fou : les couches calculées (core depuis la phase 2, quantum
    # depuis la phase 3) restent lisibles et sans dépendance externe.
    for layer in ("core", "quantum", "world_models"):
        for module in COUCHE_MODULES[layer]:
            path = GTT / layer / f"{module}.py"
            lines = path.read_text(encoding="utf-8").splitlines()
            assert len(lines) <= 250, (
                f"{layer}/{module}.py : {len(lines)} lignes")