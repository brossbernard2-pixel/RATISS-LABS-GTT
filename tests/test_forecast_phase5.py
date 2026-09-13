"""Tests forecast — phase 5 (vérités analytiques + règles du labo).

Brier exact, calibration sur jeu connu, scellement R5 (stabilité +
altération), plafond 200, soumission désarmée, journal chaîné du juge
(intégrité + altération détectée).
"""

import json

import pytest

from gtt.forecast import calibration, journal, metaculus_bot, sealed_predictions


# ---------- Calibration : vérités analytiques ----------

def test_brier_analytique():
    assert calibration.brier_score(0.75, True) == 0.0625
    assert calibration.brier_score(0.75, False) == 0.5625
    assert calibration.brier_score(0.0, False) == 0.0
    with pytest.raises(ValueError):
        calibration.brier_score(1.2, True)


def test_calibration_curve_jeu_connu():
    preds = [0.05, 0.15, 0.25, 0.95]
    outs = [False, False, True, True]
    curve = calibration.calibration_curve(preds, outs, bins=10)
    b0 = curve[0]  # [0.0, 0.1) : 0.05 -> n=1, freq 0
    assert (b0["n"], b0["mean_pred"], b0["freq_outcome"]) == (1, 0.05, 0.0)
    b1 = curve[1]  # [0.1, 0.2) : 0.15 -> n=1, freq 0
    assert (b1["n"], b1["mean_pred"], b1["freq_outcome"]) == (1, 0.15, 0.0)
    b2 = curve[2]  # [0.2, 0.3) : 0.25 -> n=1, freq 1
    assert b2["freq_outcome"] == 1.0
    b9 = curve[9]  # [0.9, 1.0] : 0.95 -> n=1, freq 1
    assert (b9["n"], b9["freq_outcome"]) == (1, 1.0)
    assert curve[5]["n"] == 0 and curve[5]["mean_pred"] is None


def test_ece_analytique():
    # bac unique : pred 0.6, 5 issues dont 3 vraies -> |0.6 - 0.6| = 0
    curve = calibration.calibration_curve([0.6] * 5, [True, True, True,
                                                       False, False], bins=1)
    assert calibration.expected_calibration_error(curve) == 0.0
    # pred 0.9, freq 0.5 -> ECE = 0.4
    curve2 = calibration.calibration_curve([0.9, 0.9], [True, False], bins=1)
    assert abs(calibration.expected_calibration_error(curve2) - 0.4) < 1e-12


def test_delta_brier_mesure():
    outs = [True, False]
    before = [0.5, 0.5]   # Brier moyen = 0.25
    after = [0.75, 0.25]  # Brier moyen = 0.0625
    assert abs(calibration.delta_brier(before, after, outs) - 0.1875) < 1e-12


# ---------- Scellement R5 ----------

def test_scellement_stable_et_alteration():
    params = {"context": {"run_id": "r1", "date": "2026-09-13"}}
    s1 = sealed_predictions.seal_prediction("p=0.62 pour Q1", params)
    s2 = sealed_predictions.seal_prediction("p=0.62 pour Q1", params)
    assert s1 == s2 and len(s1) == 64
    assert sealed_predictions.verify_prediction("p=0.62 pour Q1", s1, params)
    assert not sealed_predictions.verify_prediction("p=0.99 pour Q1", s1, params)
    # contexte différent -> scellé différent (pas de collision de run)
    s3 = sealed_predictions.seal_prediction(
        "p=0.62 pour Q1", {"context": {"run_id": "r2"}})
    assert s3 != s1


def test_enveloppe_deux_temps():
    env = sealed_predictions.sealed_envelope("p=0.4", {"context": {"run": 7}})
    assert env["seal"] == sealed_predictions.seal_prediction(
        "p=0.4", {"context": {"run": 7}})
    assert env["reveal"]["content"] == "p=0.4"
    assert "AVANT" in env["rule"]


# ---------- Bot désarmé ----------

def test_plafond_200():
    fixture = [{"id": f"q{i}", "question": f"Q{i} ?"} for i in range(250)]
    qs = metaculus_bot.collect_questions({"fixture": fixture})
    assert len(qs) == 200
    assert metaculus_bot.count_source({"fixture": fixture}) == 250
    out = metaculus_bot.run_offline({"fixture": fixture})
    assert out["truncated"] is True and out["n_questions"] == 200


def test_soumission_desarmee():
    q = {"id": "q1", "question": "Q1 ?"}
    recu = metaculus_bot.submit_forecast(q, 0.5, {})
    assert recu.startswith("dry-") and len(recu) == 20
    assert metaculus_bot.SUBMIT_AUTORISE is False
    with pytest.raises(ValueError):
        metaculus_bot.submit_forecast(q, 0.5, {"submit_predictions": True})
    with pytest.raises(ValueError):
        metaculus_bot.submit_forecast(q, 1.5, {})
    # déterministe : même question+p+contexte -> même reçu
    assert recu == metaculus_bot.submit_forecast(q, 0.5, {})


def test_questions_invalides():
    with pytest.raises(ValueError):
        metaculus_bot.collect_questions({"fixture": [{"pas_id": 1}]})
    with pytest.raises(NotImplementedError):
        metaculus_bot.collect_questions({"source": "reseau"})


# ---------- Journal chaîné (juge) ----------

def test_journal_chaine_integre(tmp_path):
    p = str(tmp_path / "journal.jsonl")
    journal.append_deviation(p, "déviation 1 : fixture tronquée à 200", {})
    journal.append_deviation(p, "déviation 2 : seed changé", {"author": "rouge"})
    journal.append_deviation(p, "déviation 3 : rien", {})
    assert journal.verify_journal(p) is True
    entrees = journal.deviations(p)
    assert len(entrees) == 3
    with pytest.raises(ValueError):
        journal.append_deviation(p, "   ", {})


def test_journal_altere_casse_la_chaine(tmp_path):
    p = str(tmp_path / "journal.jsonl")
    journal.append_deviation(p, "entrée honnête", {})
    journal.append_deviation(p, "entrée sensible", {})
    assert journal.verify_journal(p) is True
    lignes = open(p, encoding="utf-8").read().splitlines()
    e = json.loads(lignes[0])
    e["text"] = "entrée RÉÉCRITE"
    lignes[0] = json.dumps(e)
    open(p, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    assert journal.verify_journal(p) is False
    with pytest.raises(ValueError):
        journal.deviations(p)


# ---------- MANIFEST scellé ----------

def test_manifest_forecast_scelle():
    from pathlib import Path
    from ratiss.seal import seal_manifest
    pkg = Path(__file__).resolve().parents[1]
    m = json.loads((pkg / "gtt/forecast/MANIFEST.json").read_text(encoding="utf-8"))
    assert m["version"] == "0.2.0" and m["status"] == "implemented-p5"
    assert m["params"]["cap_questions"] == metaculus_bot.CAP_QUESTIONS
    assert m["params"]["bins"] == 10
    seals = json.loads((pkg / "gtt/SEALS.json").read_text(encoding="utf-8"))
    exp = next(s["sha256"] for s in seals["seals"] if s["layer"] == "forecast")
    assert seal_manifest(m) == exp
