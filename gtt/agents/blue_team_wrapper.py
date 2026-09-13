"""Wrapper bleu — défense constructive face au rapport juge.

Phase 6 (relais Rouge). Le Bleu ne « se défend » qu'avec des REJEUX (R7) :
chaque réponse à une finding est un rejeu exécutable et chiffré. Aucune
approbation ici non plus (C3) — la réponse est documentaire, le verdict
appartient au protocole et au chef.
"""

from __future__ import annotations

import hashlib
import subprocess


def reproduce(claim: dict, params: dict) -> tuple[bool, str]:
    """Rejoue une affirmation et rend un verdict calculé (R7).

    claim : {"command": [argv...], "expected_exit": 0,
             "expected_sha256": optionnel (de stdout+stderr)}.
    Retourne (ok, message chiffré). Aucun shell, aucune interprétation :
    exit code et scellé comparés, point.
    """
    timeout = int(params.get("timeout", 300))
    proc = subprocess.run([str(c) for c in claim["command"]],
                          capture_output=True, text=True, timeout=timeout)
    ok = proc.returncode == claim.get("expected_exit", 0)
    msg = f"exit {proc.returncode} (attendu {claim.get('expected_exit', 0)})"
    attendu_sha = claim.get("expected_sha256")
    if attendu_sha:
        calcule = hashlib.sha256(
            (proc.stdout + proc.stderr).encode("utf-8")).hexdigest()
        ok = ok and calcule == attendu_sha
        msg += f" ; sha256 {'identique' if calcule == attendu_sha else 'DIVERGENT'}"
    return ok, msg


def respond_to_findings(findings: dict, evidence: list, params: dict) -> dict:
    """Assemble une réponse d'équipe bleue à partir de rejouages exploitables.

    findings : {"items": [{"id", "texte"}]}. evidence : [{"finding_id",
    "claim"}] — chaque claim est rejouée via reproduce(). Retourne des
    réponses chiffrées, SANS autorité : {"responses", "authority": aucune}.
    """
    by_id = {}
    for ev in evidence:
        by_id.setdefault(ev["finding_id"], []).append(ev["claim"])
    responses = []
    for item in findings.get("items", []):
        claims = by_id.get(item["id"], [])
        if not claims:
            responses.append({"finding": item["id"], "rejoue": False,
                              "message": "aucune preuve rejouable fournie"})
            continue
        for claim in claims:
            ok, msg = reproduce(claim, params)
            responses.append({"finding": item["id"], "rejoue": True,
                              "ok": ok, "message": msg})
    return {"responses": responses,
            "authority": "aucune — réponses documentées par rejeux"}


__all__ = ["reproduce", "respond_to_findings"]
