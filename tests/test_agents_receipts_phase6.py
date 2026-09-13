"""Tests agents + receipts — phase 6.

Aucune autorité dans le code (C3) ; wrappers = primitives du juge et
rejeux R7 ; reçus cohérents ; Lean EN ATTENTE (C5, rien de fabriqué).
"""

import json

import pytest

from gtt.agents import (blue_team_wrapper, orchestrator, protocol,
                        red_team_wrapper)
from gtt.receipts import lean_proof, replayable_hash, verification
from ratiss.seal import seal_manifest


# ---------- Orchestrateur : exécution, jamais autorité ----------

def test_orchestrate_enchaine_sans_autorite():
    def double(ctx, params):
        return {"v": ctx.get("v", 0) * 2, "ok": True}

    def ajoute(ctx, params):
        return {"v": ctx["v"] + params["c"], "ok": True}

    out = orchestrator.orchestrate(
        [{"name": "double", "fn": double}, {"name": "ajoute", "fn": ajoute}],
        {"v": 3}, {"c": 4})
    assert out["context"]["v"] == 10 and out["ok"] is True
    assert out["authority"].startswith("aucune")


def test_orchestrate_drapeau_rouge_remonte():
    out = orchestrator.orchestrate(
        [{"name": "x", "fn": lambda ctx, p: {"ok": False}}], {}, {})
    assert out["ok"] is False


def test_handoff_enveloppe():
    env = orchestrator.handoff("rouge-audite", {"commit": "abc"}, {})
    assert env["step"] == "rouge-audite" and env["payload"] == {"commit": "abc"}
    assert "approbation" in env["note"]
    with pytest.raises(ValueError):
        orchestrator.handoff("", {}, {})


# ---------- Wrapper rouge : verdicts bruts, liste scellée ----------

def test_run_check_juge_verdict_brut():
    r = red_team_wrapper.run_check("gtt.judge", ["--ci"], {})
    assert r["exit"] == 0 and r["verdict"] == "exit 0"


def test_run_check_liste_scellee():
    with pytest.raises(ValueError):
        red_team_wrapper.run_check("module_invente", [], {})


def test_audit_against_conforme_et_divergent():
    m = {"layer": "test", "v": 1}
    s = seal_manifest(m)
    ok, msg = red_team_wrapper.audit_against(m, s)
    assert ok is True and "CONFORME" in msg
    ok2, msg2 = red_team_wrapper.audit_against({"layer": "test", "v": 2}, s)
    assert ok2 is False and "DIVERGENCE" in msg2


# ---------- Wrapper bleu : réponses par rejeux ----------

def test_reproduce_verdict_calcule():
    ok, msg = blue_team_wrapper.reproduce(
        {"command": ["true"], "expected_exit": 0}, {})
    assert ok is True and "exit 0" in msg
    ko, msg2 = blue_team_wrapper.reproduce(
        {"command": ["false"], "expected_exit": 0}, {})
    assert ko is False and "exit 1" in msg2


def test_respond_to_findings_sans_autorite():
    findings = {"items": [{"id": "F1", "texte": "x"}]}
    evidence = [{"finding_id": "F1",
                 "claim": {"command": ["true"], "expected_exit": 0}}]
    r = blue_team_wrapper.respond_to_findings(findings, evidence, {})
    assert r["responses"][0]["rejoue"] is True
    assert r["responses"][0]["ok"] is True
    assert r["authority"].startswith("aucune")
    r2 = blue_team_wrapper.respond_to_findings(findings, [], {})
    assert r2["responses"][0]["rejoue"] is False


# ---------- Protocole : description, pas exécution ----------

def test_protocol_steps_scelle():
    steps = protocol.protocol_steps("1.0", {})
    assert steps == ["bleu-construit", "rouge-audite", "chef-arbitre",
                     "recu-r7", "visa-provenance"]
    with pytest.raises(ValueError):
        protocol.protocol_steps("9.9", {})


# ---------- Reçus : hash rejouable + vérification ----------

def test_hash_rejouable_stable():
    h1 = replayable_hash.replayable_command_hash("pytest -q", {})
    h2 = replayable_hash.replayable_command_hash("pytest -q", {})
    assert h1 == h2 and len(h1) == 64
    assert replayable_hash.verify_command_hash("pytest -q", h1) is True
    assert replayable_hash.verify_command_hash("pytest", h1) is False
    with pytest.raises(ValueError):
        replayable_hash.replayable_command_hash("  ", {})


def test_verify_receipt_cohérence():
    cmd = "python3 -m pytest -q"
    recu = {
        "command": cmd,
        "command_sha256": replayable_hash.replayable_command_hash(cmd, {}),
        "artifact_sha256": "a" * 64,
        "source": "phase 6",
    }
    ok, raison = verification.verify_receipt(recu, {})
    assert ok is True and "cohérent" in raison
    fautif = dict(recu, command="autre commande")
    ok2, raison2 = verification.verify_receipt(fautif, {})
    assert ok2 is False and "divergent" in raison2
    ok3, raison3 = verification.verify_receipt({"command": cmd}, {})
    assert ok3 is False and "manquants" in raison3
    ok4, _ = verification.verify_receipt(dict(recu, artifact_sha256="xy"), {})
    assert ok4 is False


# ---------- Lean : EN ATTENTE, rien de fabriqué (C5) ----------

def test_lean_proof_en_attente():
    with pytest.raises(NotImplementedError) as exc:
        lean_proof.lean_proof_check("1+1=2", {}, {})
    assert "EN ATTENTE" in str(exc.value)


# ---------- MANIFEST agents/receipts scellés ----------

def test_manifests_phase6_scelles():
    from pathlib import Path
    pkg = Path(__file__).resolve().parents[1]
    seals = json.loads((pkg / "gtt/SEALS.json").read_text(encoding="utf-8"))
    for layer in ("agents", "receipts"):
        m = json.loads((pkg / f"gtt/{layer}/MANIFEST.json")
                       .read_text(encoding="utf-8"))
        exp = next(s["sha256"] for s in seals["seals"] if s["layer"] == layer)
        assert seal_manifest(m) == exp
        assert m["status"] == "implemented-p6"
    ag = json.loads((pkg / "gtt/agents/MANIFEST.json").read_text(encoding="utf-8"))
    assert ag["params"]["protocol_steps"] == protocol.protocol_steps("1.0", {})
