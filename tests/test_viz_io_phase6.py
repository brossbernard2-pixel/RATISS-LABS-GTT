"""Tests viz + io — phase 6.

SVG/DOT déterministes stdlib seule ; PDB au colonnage wwPDB ; syncs
dry-run sans réseau, tokens par environnement et JAMAIS echo.
"""

import math

import pytest

from gtt.io import github_sync, osf_sync, pdb_loader
from gtt.viz import coherence_atlas, proof_graph, topology_3d


# ---------- viz : déterminisme et structure ----------

def test_diagramme_svg_deterministe():
    pts = [(0.0, 1.0), (0.5, 2.0), (1.0, math.inf)]
    a = topology_3d.diagram_to_svg(pts, {"size": 400})
    b = topology_3d.diagram_to_svg(list(reversed(pts)), {"size": 400})
    assert a == b  # tri appliqué : l'ordre d'entrée ne change rien
    assert a.count("<circle") == 3
    assert "#2980b9" in a  # classe essentielle en bleu
    with pytest.raises(ValueError):
        topology_3d.diagram_to_svg([], {})


def test_atlas_svg_structure():
    mat = [[0.0, 0.5], [1.0, 0.25]]
    svg = coherence_atlas.atlas_svg(mat, {"cell": 10, "labels": True})
    assert svg.count("<rect") == 5  # fond + 4 cases
    assert "#000000" in svg and "#ffffff" in svg and "#808080" in svg
    assert coherence_atlas.atlas_svg(mat, {"cell": 10}) == \
        coherence_atlas.atlas_svg([r[:] for r in mat], {"cell": 10})
    with pytest.raises(ValueError):
        coherence_atlas.atlas_svg([[1.5]], {})
    with pytest.raises(ValueError):
        coherence_atlas.atlas_svg([[0.1, 0.2], [0.3]], {})


def test_graphe_dot_valide_aretes():
    nodes = [{"id": "M2", "statut": "prouve"},
             {"id": "M4", "statut": "en_attente"}]
    edges = [{"de": "M2", "vers": "M4", "label": "scelle"}]
    dot = proof_graph.graph_to_dot(nodes, edges, {"name": "g"})
    assert dot.startswith("digraph g {") and '"M2" -> "M4"' in dot
    assert "#27ae60" in dot and "#7f8c8d" in dot
    with pytest.raises(ValueError):
        proof_graph.graph_to_dot(nodes, [{"de": "M2", "vers": "FANTOME"}], {})
    with pytest.raises(ValueError):
        proof_graph.graph_to_dot([{"id": "a", "statut": "magique"}], [], {})


# ---------- io : PDB au colonnage wwPDB ----------

PDB_FIXTURE = "\n".join([
    "HEADER    TEST",
    "ATOM      1  N   ALA A   1      11.104  13.207  10.000  1.00 20.00           N",
    "ATOM      2  CA  ALA A   1      12.000  14.000  10.500  1.00 20.00           C",
    "HETATM    3  O   HOH B   2      13.000  15.000  11.500  1.00 20.00           O",
    "ATOM   malformée",
    "END",
])


def test_pdb_colonnes_wwpdb():
    atomes = pdb_loader.parse_pdb(PDB_FIXTURE, {})
    assert len(atomes) == 3
    a0 = atomes[0]
    assert a0["name"] == "N" and a0["resname"] == "ALA"
    assert a0["chain"] == "A" and a0["resseq"] == 1
    assert a0["xyz"] == [11.104, 13.207, 10.000]
    rapport = pdb_loader.parse_pdb_report(PDB_FIXTURE, {})
    assert rapport == {"n_atomes": 3, "n_lignes": 6, "n_ignores": 1}


def test_pdb_records_filtrables(tmp_path):
    f = tmp_path / "t.pdb"
    f.write_text(PDB_FIXTURE, encoding="utf-8")
    seulement = pdb_loader.parse_pdb(str(f), {"records": ("ATOM",)})
    assert len(seulement) == 2


# ---------- io : syncs dry-run, tokens jamais echo ----------

def test_osf_dry_run_sans_fuite():
    r = osf_sync.sync("wf7qm", {"OSF_TOKEN": "SECRET-OSF"}, {})
    assert r["mode"] == "dry-run"
    assert r["request"]["url"] == "https://api.osf.io/v2/nodes/wf7qm/"
    assert r["token_present"] is True and r["token"] == "***"
    assert "SECRET-OSF" not in repr(r) and "SECRET-OSF" not in str(r)
    vide = osf_sync.sync("x", {}, {})
    assert vide["token_present"] is False and vide["token"] is None
    with pytest.raises(NotImplementedError):
        osf_sync.sync("wf7qm", {}, {"live": True})


def test_github_dry_run_sans_fuite():
    r = github_sync.sync("brossbernard2-pixel/RATISS-LABS-GTT",
                         {"GITHUB_TOKEN": "SECRET-GH"}, {"endpoint": "commits"})
    assert r["request"]["url"].endswith("/RATISS-LABS-GTT/commits")
    assert r["token"] == "***" and "SECRET-GH" not in str(r)
    with pytest.raises(ValueError):
        github_sync.build_request("pas_un_repo", {})
    with pytest.raises(NotImplementedError):
        github_sync.sync("a/b", {}, {"live": True})


# ---------- MANIFEST viz/io scellés ----------

def test_manifests_viz_io_scelles():
    import json
    from pathlib import Path
    from ratiss.seal import seal_manifest
    pkg = Path(__file__).resolve().parents[1]
    seals = json.loads((pkg / "gtt/SEALS.json").read_text(encoding="utf-8"))
    for layer in ("viz", "io"):
        m = json.loads((pkg / f"gtt/{layer}/MANIFEST.json")
                       .read_text(encoding="utf-8"))
        exp = next(s["sha256"] for s in seals["seals"] if s["layer"] == layer)
        assert seal_manifest(m) == exp
        assert m["status"] == "implemented-p6"
    viz = json.loads((pkg / "gtt/viz/MANIFEST.json").read_text(encoding="utf-8"))
    assert viz["params"]["rounding"] == topology_3d.ARRONDI
    assert viz["params"]["rounding"] == coherence_atlas.ARRONDI
