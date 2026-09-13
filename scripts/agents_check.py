#!/usr/bin/env python3
"""Vérifications déterministes agents+receipts+viz+io phase 6 (R7)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gtt.agents import orchestrator, protocol, red_team_wrapper, blue_team_wrapper
from gtt.receipts import replayable_hash, verification, lean_proof
from gtt.viz import coherence_atlas, proof_graph, topology_3d
from gtt.io import osf_sync, github_sync, pdb_loader
from ratiss.seal import seal_manifest
import math

def main():
    ok = True
    o = orchestrator.orchestrate(
        [{"name": "d", "fn": lambda c, p: {"v": c.get("v", 1) * 3, "ok": True}}],
        {"v": 2}, {})
    ok &= o["context"]["v"] == 6 and o["authority"].startswith("aucune")
    print(f"Orchestrateur : v=6 autorite=aucune ✔={o['context']['v'] == 6}")
    steps = protocol.protocol_steps("1.0", {})
    ok &= steps == ["bleu-construit", "rouge-audite", "chef-arbitre", "recu-r7", "visa-provenance"]
    print(f"Protocole 1.0 : {len(steps)} etapes, ordre scelle")
    rc = red_team_wrapper.run_check("gtt.judge", ["--ci"], {})
    ok &= rc["exit"] == 0
    conf, _ = red_team_wrapper.audit_against({"layer": "x"}, seal_manifest({"layer": "x"}))
    ok &= rc["exit"] == 0 and conf
    print(f"Wrapper rouge : judge {rc['verdict']}, audit_against conforme={conf}")
    rep, msg = blue_team_wrapper.reproduce({"command": ["true"], "expected_exit": 0}, {})
    ok &= rep
    print(f"Wrapper bleu : rejeu 'true' ok={rep} ({msg})")
    h = replayable_hash.replayable_command_hash("pytest -q", {})
    recu = {"command": "pytest -q", "command_sha256": h, "artifact_sha256": "a" * 64, "source": "chk"}
    v_ok, raison = verification.verify_receipt(recu, {})
    ok &= h == replayable_hash.replayable_command_hash("pytest -q", {}) and v_ok
    print(f"Reçus : hash stable={h[:16]}… verify={v_ok} ({raison})")
    try:
        lean_proof.lean_proof_check("x", {}, {})
        lean_en_attente = False
    except NotImplementedError as e:
        lean_en_attente = "EN ATTENTE" in str(e)
    ok &= lean_en_attente
    print(f"Lean proof : EN ATTENTE respecté={lean_en_attente} (C5, rien de fabriqué)")
    svg1 = topology_3d.diagram_to_svg([(0.0, 1.0), (1.0, math.inf)], {"size": 300})
    svg2 = coherence_atlas.atlas_svg([[0.0, 1.0], [0.5, 0.25]], {"cell": 10})
    dot = proof_graph.graph_to_dot([{"id": "a", "statut": "prouve"}], [], {})
    ok &= svg1 == topology_3d.diagram_to_svg([(1.0, math.inf), (0.0, 1.0)], {"size": 300})
    ok &= svg2.count("<rect") == 5 and dot.startswith("digraph")
    print(f"Viz : SVG déterministe=True, atlas rects=5, DOT ok")
    ro = osf_sync.sync("wf7qm", {"OSF_TOKEN": "SECRET-X"}, {})
    rg = github_sync.sync("a/b", {"GITHUB_TOKEN": "SECRET-Y"}, {})
    fuite = "SECRET-X" in str(ro) or "SECRET-Y" in str(rg)
    ok &= ro["token"] == "***" and rg["token"] == "***" and not fuite
    print(f"IO syncs : dry-run, tokens masqués, fuite={fuite}")
    pdb = "ATOM      1  N   ALA A   1      11.104  13.207  10.000  1.00 20.00           N"
    at = pdb_loader.parse_pdb(pdb, {})
    ok &= len(at) == 1 and at[0]["xyz"] == [11.104, 13.207, 10.0]
    print(f"PDB : colonnes wwPDB lues, xyz={at[0]['xyz']}")
    print("RESULTAT:", "CONFORME" if ok else "DIVERGENCE")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
