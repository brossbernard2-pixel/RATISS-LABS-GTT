#!/usr/bin/env python3
"""Vérifications déterministes quantum phase 3 (sortie stable, scellable).

Imprime une ligne par contrôle avec valeurs arrondies à 12 décimales :
mêmes entrées -> exactement la même sortie sur toute machine (R7).
"""

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gtt.quantum import lanczos as lz
from gtt.quantum import mps_dmrg as md
from gtt.quantum import decoherence as dec
from gtt.quantum import qpu_connectors as qpu
from gtt.quantum._linalg import jacobi_eig_sym
from gtt.quantum._tfim import tfim_open_dense


def r(x: float) -> float:
    return round(x, 12)


def laplacien_chemin(n):
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        l[i][i] = 1.0 if i in (0, n - 1) else 2.0
        if i + 1 < n:
            l[i][i + 1] = l[i + 1][i] = -1.0
    return l


def ed_ground(n, j, h):
    vals, _ = jacobi_eig_sym(tfim_open_dense(n, j, h))
    return vals[0]


def main() -> int:
    ok = True
    # TFIM N=2 : forme fermée -sqrt(J^2 + 4h^2)
    e2 = ed_ground(2, 1.0, 0.7)
    ff = -math.sqrt(1.0 + 4 * 0.49)
    d = abs(e2 - ff)
    ok &= d < 1e-12
    print(f"ED N=2 J=1 h=0.7 : E0={r(e2)} forme_fermee={r(ff)} delta={r(d)}")
    # ED vs DMRG N=4 et N=5
    for n in (4, 5):
        e_ed = ed_ground(n, 1.0, 0.7)
        rng = random.Random(20260913)
        state = [rng.uniform(-1, 1) for _ in range(1 << n)]
        mps = md.mps_from_statevector(state, 4, {})
        out = md.dmrg_sweep(mps, {"N": n, "J": 1.0, "h": 0.7},
                            {"sweeps": 2, "max_bond": 4})
        d = abs(out["energy"] - e_ed)
        ok &= d < 1e-8
        print(f"ED vs DMRG N={n} : E_ed={r(e_ed)} E_dmrg={r(out['energy'])} delta={r(d)}")
    # Lanczos chemin P8 : 2-2cos(pi k/8)
    n = 8
    res = lz.lanczos_iteration(laplacien_chemin(n), 4,
                               {"tolerance": 1e-10, "max_iter": 64,
                                "seed": 20260913})
    att = sorted(2 - 2 * math.cos(math.pi * k / n) for k in range(n))[:4]
    d = max(abs(a - b) for a, b in zip(res["eigenvalues"], att))
    ok &= d < 1e-8 and res["converged"]
    print(f"Lanczos P8 k=4 : max_err={r(d)} converged={res['converged']}")
    # Décohérence : lois exactes
    out_d = dec.apply_dephasing([[0.5 + 0j, 0.5 + 0j], [0.5 + 0j, 0.5 + 0j]],
                                37.0, 37.0)
    d = abs(out_d[0][1].real - 0.5 * math.exp(-1.0))
    ok &= d < 1e-14
    print(f"Dephasage t=T2 : hors_diag={r(out_d[0][1].real)} attendu={r(0.5 * math.exp(-1.0))} delta={r(d)}")
    out_r = dec.apply_amplitude_damping([[0j, 0j], [0j, 1 + 0j]], 53.0, 53.0)
    d = abs(out_r[1][1].real - math.exp(-1.0))
    ok &= d < 1e-14
    print(f"Relaxation t=T1 : p1={r(out_r[1][1].real)} attendu={r(math.exp(-1.0))} delta={r(d)}")
    # QPU dry-run déterministe
    bell = {"qubits": 2, "gates": [("h", 0), ("cx", 0, 1), ("m", [0, 1])]}
    j1 = qpu.submit(bell, "ibm_fez", {})
    j2 = qpu.submit(bell, "ibm_fez", {})
    ok &= j1 == j2 and j1.startswith("dry-")
    print(f"QPU dry-run Bell/ibm_fez : job_id={j1} deterministe={j1 == j2}")
    print("RESULTAT:", "CONFORME" if ok else "DIVERGENCE")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
