"""Connecteurs QPU — IBM Open Plan uniquement.

Phase 3 (source QPU-Ratiss-COSMOS ; réécriture provenancée, relais Rouge).
Aucun token dans le code (C5) : `env["IBM_TOKEN"]` uniquement, jamais
committé, jamais renvoyé dans une sortie. Mode phase 3 : DRY-RUN — la
soumission réelle appartient à la campagne M2–M4 du chef (compte d'essai
manuel, export par session) ; `verify_receipt` validera les reçus réels
(job_id + scellés) quand ils existeront. STDLIB seule, déterministe.
"""

from __future__ import annotations

import hashlib
import json

PLAN_AUTORISE = "open-plan"
TOKEN_ENV = "IBM_TOKEN"
_GATES_1Q = {"h", "x", "y", "z", "s", "sdg", "t", "tdg", "rx", "ry", "rz"}
_GATES_2Q = {"cx", "cz", "swap"}


class Connector:
    """Connecteur dry-run. Le token reste privé ; repr/str ne le fuient pas."""

    def __init__(self, plan: str, token: str | None):
        if plan != PLAN_AUTORISE:
            raise ValueError(f"plan non autorise : {plan} (seul {PLAN_AUTORISE})")
        self.plan = plan
        self.has_token = token is not None and token != ""
        self.mode = "dry-run"
        self._token = token  # privé, jamais sérialisé

    def __repr__(self) -> str:
        return (f"Connector(plan={self.plan!r}, mode={self.mode!r}, "
                f"has_token={self.has_token})")


def connect(plan: str, env: dict) -> object:
    """Connecte un plan QPU (Open Plan). env['IBM_TOKEN'] si fourni."""
    return Connector(plan, env.get(TOKEN_ENV))


def build_qasm(circuit: dict) -> str:
    """Construit l'OpenQASM 3 déterministe d'un circuit dict.

    circuit : {"qubits": n, "gates": [("h", 0), ("cx", 0, 1), ("m", [0, 1])]}.
    """
    n = circuit["qubits"]
    lines = ["OPENQASM 3.0;", 'include "stdgates.inc";', f"qubit[{n}] q;",
             f"bit[{n}] c;"]
    for gate in circuit["gates"]:
        name, args = gate[0], gate[1:]
        if name == "m":
            for qb in args[0]:
                lines.append(f"measure q[{qb}] -> c[{qb}];")
        elif name in _GATES_1Q:
            if name in ("rx", "ry", "rz"):
                lines.append(f"{name}({args[1]}) q[{args[0]}];")
            else:
                lines.append(f"{name} q[{args[0]}];")
        elif name in _GATES_2Q:
            lines.append(f"{name} q[{args[0]}], q[{args[1]}];")
        else:
            raise ValueError(f"porte inconnue : {name}")
    return "\n".join(lines) + "\n"


def build_payload(circuit: dict, backend: str) -> dict:
    """Charge scellable : {qasm, backend, seal = sha256 canonique}."""
    qasm = build_qasm(circuit)
    canon = json.dumps({"backend": backend, "qasm": qasm},
                       sort_keys=True, separators=(",", ":"))
    seal = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    return {"qasm": qasm, "backend": backend, "seal": seal}


def submit(circuit: object, backend: object, params: dict) -> str:
    """Soumet un circuit sur un backend. Token via variable env uniquement.

    Phase 3 : dry-run — retourne `dry-<16 premiers du scellé>`, identifiant
    déterministe et reproductible (aucun réseau). `params["live"]=True` →
    NotImplementedError : la soumission réelle est la campagne M2–M4 du chef.
    """
    if params.get("live"):
        raise NotImplementedError(
            "soumission reelle : campagne M2-M4, compte d'essai du chef, "
            "hors phase 3 (aucun reseau dans le depot)")
    payload = build_payload(circuit, backend)
    return f"dry-{payload['seal'][:16]}"


def verify_receipt(receipt: dict) -> bool:
    """Vérifie un reçu de campagne : le scellé doit correspondre à la charge.

    receipt : {"job_id", "backend", "qasm", "seal"} — reçu RÉEL (M2–M4) ou
    dry-run. Toute altération du qasm/backend invalide le scellé.
    """
    canon = json.dumps({"backend": receipt["backend"], "qasm": receipt["qasm"]},
                       sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest() == receipt["seal"]


__all__ = ["Connector", "connect", "build_qasm", "build_payload", "submit",
           "verify_receipt", "PLAN_AUTORISE", "TOKEN_ENV"]
