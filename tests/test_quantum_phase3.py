"""Tests quantum — phase 3 (vérités analytiques + validations croisées).

Portique : spectres de graphes (chemin, cycle), limites exactes du TFIM,
forme fermée N=2, ED vs DMRG, lois exponentielles T1/T2, connecteur
dry-run déterministe sans fuite de token, scellés MANIFEST.
"""

import json
import math
import random
from pathlib import Path

import pytest

from gtt.quantum import decoherence, lanczos, mps_dmrg, qpu_connectors
from gtt.quantum._linalg import jacobi_eig_sym
from gtt.quantum._tfim import energy_dense, state_from_mps, tfim_open_dense

PKG = Path(__file__).resolve().parents[1]
PARAMS_LANCZOS = {"tolerance": 1e-10, "max_iter": 64, "seed": 20260913}


def _laplacien_chemin(n):
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        l[i][i] = 1.0 if i in (0, n - 1) else 2.0
        if i + 1 < n:
            l[i][i + 1] = l[i + 1][i] = -1.0
    return l


def _laplacien_cycle(n):
    l = _laplacien_chemin(n)
    for i in range(n):
        l[i][i] = 2.0
    l[0][n - 1] = l[n - 1][0] = -1.0
    return l


def _ed_ground(n, j, h):
    vals, vecs = jacobi_eig_sym(tfim_open_dense(n, j, h))
    return vals[0], [vecs[r][0] for r in range(len(vals))]


# ---------- Lanczos : vérités analytiques ----------

def test_lanczos_chemin_p8():
    n = 8
    res = lanczos.lanczos_iteration(_laplacien_chemin(n), 4, PARAMS_LANCZOS)
    attendu = sorted(2 - 2 * math.cos(math.pi * k / n) for k in range(n))[:4]
    assert res["converged"] is True
    assert all(abs(a - b) < 1e-8 for a, b in zip(res["eigenvalues"], attendu))


def test_lanczos_cycle_c6_ritz_distincts():
    """Spectre dégénéré : la dimension de Krylov = nb de valeurs DISTINCTES.

    C6 : {0, 1, 1, 3, 3, 4} -> Krylov dim 4 ; Lanczos réorthogonalisé rend
    les valeurs distinctes [0, 1, 3, 4], jamais les multiplicités (documenté).
    """
    n = 6
    res = lanczos.lanczos_iteration(_laplacien_cycle(n), 3, PARAMS_LANCZOS)
    distinct = sorted({round(2 - 2 * math.cos(2 * math.pi * k / n), 9)
                       for k in range(n)})
    attendu = distinct[:3]  # [0.0, 1.0, 3.0]
    assert res["iterations"] == len(distinct)
    assert res["converged"] is True
    assert all(abs(a - b) < 1e-8 for a, b in zip(res["eigenvalues"], attendu))


def test_critere_convergence():
    assert lanczos.convergence_criterion(1e-12, 1e-10) is True
    assert lanczos.convergence_criterion(1e-8, 1e-10) is False


# ---------- TFIM : limites exactes et forme fermée N=2 ----------

def test_ed_limite_h_nul():
    e0, _ = _ed_ground(4, 1.0, 0.0)
    assert abs(e0 - (-3.0)) < 1e-9  # -J*(N-1), tous spins alignes en X


def test_ed_limite_j_nul():
    e0, _ = _ed_ground(5, 0.0, 0.7)
    assert abs(e0 - (-3.5)) < 1e-9  # -h*N, tous spins alignes en Z


def test_ed_forme_fermee_n2():
    j, h = 1.0, 0.7
    e0, _ = _ed_ground(2, j, h)
    assert abs(e0 - (-math.sqrt(j * j + 4 * h * h))) < 1e-12


# ---------- DMRG vs ED (validation croisée) ----------

@pytest.mark.parametrize("n", [4, 5])
def test_dmrg_rejoint_ed(n):
    j, h = 1.0, 0.7
    e_ed, v_ed = _ed_ground(n, j, h)
    rng = random.Random(20260913)
    state = [rng.uniform(-1, 1) for _ in range(1 << n)]
    mps = mps_dmrg.mps_from_statevector(state, 4, {})
    out = mps_dmrg.dmrg_sweep(mps, {"N": n, "J": j, "h": h},
                              {"sweeps": 2, "max_bond": 4})
    assert abs(out["energy"] - e_ed) < 1e-8
    assert out["energy"] >= e_ed - 1e-9  # variationnel
    assert out["energy"] == out["history"][-1]
    overlap = abs(sum(a * b for a, b in
                      zip(state_from_mps(out["tensors"]), v_ed)))
    assert overlap > 0.999999


# ---------- MPS : décomposition, reconstruction, troncature ----------

def test_mps_etat_produit_liens_1():
    n = 3
    state = [1.0 / math.sqrt(1 << n)] * (1 << n)  # |+>^{⊗n}
    mps = mps_dmrg.mps_from_statevector(state, 4, {})
    assert mps["error"] < 1e-12
    # état produit : TOUS les liens (gauche len(t), droite len(t[0][0])) = 1
    for t in mps["tensors"]:
        assert len(t) == 1, "lien gauche d'un état produit doit valoir 1"
        assert len(t[0][0]) == 1, "lien droit d'un état produit doit valoir 1"


def test_mps_reconstruction_exacte():
    rng = random.Random(1234)
    state = [rng.uniform(-1, 1) for _ in range(16)]
    mps = mps_dmrg.mps_from_statevector(state, 4, {})
    assert mps["error"] < 1e-12
    rec = state_from_mps(mps["tensors"])
    nrm_o = math.sqrt(sum(x * x for x in state))
    nrm_r = math.sqrt(sum(x * x for x in rec))
    ov = sum(a * b for a, b in zip(state, rec)) / (nrm_o * nrm_r)
    assert abs(ov) > 1 - 1e-10


def test_troncature_liens():
    rng = random.Random(7)
    state = [rng.uniform(-1, 1) for _ in range(16)]
    mps = mps_dmrg.mps_from_statevector(state, 4, {})
    tr = mps_dmrg.truncate_bond_dimension(mps, 1)
    for t in tr["tensors"]:
        assert len(t) <= 2 and len(t[0][0]) <= 2  # liens bornes par max_bond
    assert tr["trunc_error"] > 0.0  # etat generique : tronquer coute
    tr4 = mps_dmrg.truncate_bond_dimension(mps, 4)
    assert tr4["trunc_error"] < 1e-12  # deja <= 4 : rien a perdre


# ---------- Décohérence : lois exponentielles exactes ----------

def test_dephasage_loi_exacte():
    rho = [[0.5 + 0j, 0.5 + 0j], [0.5 + 0j, 0.5 + 0j]]  # |+><+|
    t2 = 37.0
    for t in (0.0, t2, 2 * t2):
        out = decoherence.apply_dephasing(rho, t, t2)
        assert abs(out[0][1].real - 0.5 * math.exp(-t / t2)) < 1e-14
        assert out[0][0].real == 0.5 and out[1][1].real == 0.5


def test_relaxation_t1_loi_exacte():
    rho = [[0j, 0j], [0j, 1 + 0j]]  # |1><1|
    t1 = 53.0
    for t in (0.0, t1, 2 * t1):
        out = decoherence.apply_amplitude_damping(rho, t, t1)
        assert abs(out[1][1].real - math.exp(-t / t1)) < 1e-14
        assert abs(out[0][0].real - (1 - math.exp(-t / t1))) < 1e-14


def test_purete_et_entropie():
    pur = [[1 + 0j, 0j], [0j, 0j]]
    mixte = [[0.5 + 0j, 0j], [0j, 0.5 + 0j]]
    assert abs(decoherence.purity(pur) - 1.0) < 1e-14
    assert abs(decoherence.purity(mixte) - 0.5) < 1e-14
    assert abs(decoherence.von_neumann_entropy_bits(pur)) < 1e-14
    assert abs(decoherence.von_neumann_entropy_bits(mixte) - 1.0) < 1e-14


def test_coherence_time_combinaison_harmonique():
    q = {"T1": 120.0, "T2": 100.0}
    amb = {"extra_dephasing_rate": 1.0 / 100.0}
    assert abs(decoherence.coherence_time(q, amb, {"model": "t2_star"})
               - 50.0) < 1e-12


def test_decoherence_rate_modele_scelle():
    circuit = {"duration_us": 50.0, "qubits": [{"T2": 100.0}, {"T2": 100.0}]}
    r = decoherence.decoherence_rate(circuit, {"model": "exp_t2_harmonic"})
    assert abs(r - (1 - math.exp(-0.5))) < 1e-14


def test_carte_couplage_classes():
    qubits = [{"id": "q0", "T1": 200.0, "T2": 200.0},
              {"id": "q1", "T1": 100.0, "T2": 100.0},
              {"id": "q2", "T1": 50.0, "T2": 60.0},
              {"id": "q3", "T1": 30.0, "T2": 25.0}]
    carte = decoherence.ambient_coupling_map(
        qubits, {"good_rate_max": 0.01, "mid_rate_max": 0.02})
    assert carte["q0"]["class"] == "good"
    assert carte["q1"]["class"] == "good"  # taux == seuil : inclus
    assert carte["q2"]["class"] == "mid"
    assert carte["q3"]["class"] == "bad"


# ---------- Connecteur QPU : dry-run sûr et déterministe ----------

def _bell():
    return {"qubits": 2, "gates": [("h", 0), ("cx", 0, 1), ("m", [0, 1])]}


def test_connect_plan_et_token():
    c0 = qpu_connectors.connect("open-plan", {})
    assert c0.has_token is False and c0.mode == "dry-run"
    c1 = qpu_connectors.connect("open-plan", {"IBM_TOKEN": "SECRET-TEST"})
    assert c1.has_token is True
    assert "SECRET-TEST" not in repr(c1) and "SECRET-TEST" not in str(c1)
    with pytest.raises(ValueError):
        qpu_connectors.connect("premium-inexistant", {})


def test_submit_dry_run_deterministe():
    id1 = qpu_connectors.submit(_bell(), "ibm_fez", {})
    id2 = qpu_connectors.submit(_bell(), "ibm_fez", {})
    id3 = qpu_connectors.submit(_bell(), "ibm_nairobi", {})
    assert id1 == id2 and id1 != id3 and id1.startswith("dry-")
    with pytest.raises(NotImplementedError):
        qpu_connectors.submit(_bell(), "ibm_fez", {"live": True})


def test_qasm_et_recu():
    payload = qpu_connectors.build_payload(_bell(), "ibm_fez")
    assert "h q[0];" in payload["qasm"]
    assert "cx q[0], q[1];" in payload["qasm"]
    assert payload["qasm"].count("measure") == 2
    recu = {"job_id": "dry-x", "backend": payload["backend"],
            "qasm": payload["qasm"], "seal": payload["seal"]}
    assert qpu_connectors.verify_receipt(recu) is True
    recu_faux = dict(recu, qasm=payload["qasm"].replace("h q[0];", "x q[0];"))
    assert qpu_connectors.verify_receipt(recu_faux) is False
    with pytest.raises(ValueError):
        qpu_connectors.build_qasm({"qubits": 1, "gates": [("porte_inconnue", 0)]})


# ---------- MANIFEST quantum scellé ----------

def test_manifest_quantum_scelle():
    from ratiss.seal import seal_manifest
    manifest = json.loads(
        (PKG / "gtt/quantum/MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "0.2.0"
    assert manifest["status"] == "implemented-p3"
    p = manifest["params"]
    assert p["lanczos"]["tolerance"] == PARAMS_LANCZOS["tolerance"]
    assert p["mps_dmrg"]["model"] == "tfim_open"
    assert p["qpu"]["mode"] == "dry-run" and p["qpu"]["token_env"] == "IBM_TOKEN"
    seals = json.loads((PKG / "gtt/SEALS.json").read_text(encoding="utf-8"))
    expected = next(s["sha256"] for s in seals["seals"]
                    if s["layer"] == "quantum")
    assert seal_manifest(manifest) == expected


def test_energie_dense_coherente():
    h = tfim_open_dense(3, 1.0, 0.7)
    vals, vecs = jacobi_eig_sym(h)
    v0 = [vecs[r][0] for r in range(len(vals))]
    assert abs(energy_dense(h, v0) - vals[0]) < 1e-10
