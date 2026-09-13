"""Wrapper rouge — applique les primitives du juge, sans approuver.

C3 : ce module n'a AUCUNE identité d'approbation. Il exécute la CLI couche 1
(ratiss) ou gtt.judge en sous-processus et renvoie les verdicts BRUTS
(exit code + sortie) ; le sens est interprété par le protocole
(docs/PROTOCOL.md), jamais par ce code. Phase 6 (relais Rouge).
"""

from __future__ import annotations

import subprocess
import sys

from ratiss.seal import seal_manifest

MODULES_AUTORISES = ("ratiss", "gtt.judge")


def run_check(module: str, args: list, params: dict) -> dict:
    """Exécute une primitive du juge et renvoie {verdict, exit, output}.

    module ∈ MODULES_AUTORISES (liste scellée au MANIFEST agents).
    verdict = "exit N" brut — aucune interprétation, aucune approbation.
    """
    if module not in MODULES_AUTORISES:
        raise ValueError(f"module hors liste scellée : {module}")
    timeout = int(params.get("timeout", 120))
    proc = subprocess.run(
        [sys.executable, "-m", module, *[str(a) for a in args]],
        capture_output=True, text=True, timeout=timeout)
    return {"verdict": f"exit {proc.returncode}",
            "exit": proc.returncode,
            "output": (proc.stdout + proc.stderr).strip()}


def audit_against(manifest: dict, seal: str) -> tuple[bool, str]:
    """Re-scelle un manifeste et compare au scellé (ratiss.seal).

    Retourne (conforme, message brut avec préfixes des deux scellés).
    """
    calcule = seal_manifest(manifest)
    ok = calcule == seal
    msg = (f"scellé attendu {seal[:16]}… calculé {calcule[:16]}… — "
           + ("CONFORME" if ok else "DIVERGENCE"))
    return ok, msg


__all__ = ["run_check", "audit_against", "MODULES_AUTORISES"]
