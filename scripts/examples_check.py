#!/usr/bin/env python3
"""Vérifications déterministes examples phase 7 (terrains, R7)."""
import json, sys, importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def charger(terrain, module):
    chemin = ROOT / "examples" / terrain / f"{module}.py"
    spec = importlib.util.spec_from_file_location(f"{terrain}_{module}", chemin)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def r(x): return round(x, 12)

def main():
    ok = True
    rc2 = charger("TERRAIN-02", "run_core")
    out2 = rc2.run(ROOT / "examples/TERRAIN-02/sir.json")
    exp2 = json.loads((ROOT / "examples/TERRAIN-02/expected.json").read_text(encoding="utf-8"))
    ok &= out2 == exp2
    print(f"TERRAIN-02 SIR : conservation={r(out2['conservation_violation'])} perturbation={r(out2['perturbation_violation'])} betti={out2['betti_reseau']} coherence={r(out2['coherence_score'])} ==expected:{out2 == exp2}")
    rc3 = charger("TERRAIN-03", "run_core")
    out3 = rc3.run(ROOT / "examples/TERRAIN-03/heat.json")
    exp3 = json.loads((ROOT / "examples/TERRAIN-03/expected.json").read_text(encoding="utf-8"))
    ok &= out3 == exp3
    print(f"TERRAIN-03 chaleur : masse stable={r(out3['stable']['violation_masse'])} instable={r(out3['instable']['violation_masse'])} | amp stable {r(out3['stable']['amplitude_initiale'])}->{r(out3['stable']['amplitude_finale'])} instable {r(out3['instable']['amplitude_initiale'])}->{r(out3['instable']['amplitude_finale'])} | coherence={r(out3['coherence_score'])} ==expected:{out3 == exp3}")
    print("RESULTAT:", "CONFORME" if ok else "DIVERGENCE")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
