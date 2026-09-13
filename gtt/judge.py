"""Juge local GTT — re-scellé des MANIFESTS avec le juge RATISS.

Le dépôt GTT est jugé par la couche 1 (dépendance git ratiss-framework).
Ce module re-calcule le sceau SHA-256 de chaque MANIFEST.json (JSON
canonique via ratiss.seal) et le compare à gtt/SEALS.json. Toute
divergence : exit 1.

Usage :
    python -m gtt.judge            # rendu verbeux
    python -m gtt.judge --ci       # rendu compact pour CI
"""

import argparse
import json
import sys
from pathlib import Path

from ratiss.seal import seal_manifest

LAYERS = (
    "core", "quantum", "world_models", "forecast",
    "agents", "receipts", "audit", "viz", "io",
)
PKG = Path(__file__).resolve().parent
SEALS_PATH = PKG / "SEALS.json"


def _load_manifest(layer: str) -> dict:
    return json.loads((PKG / layer / "MANIFEST.json").read_text(encoding="utf-8"))


def judge(verbose: bool = True) -> int:
    seals = json.loads(SEALS_PATH.read_text(encoding="utf-8"))
    expected = {(seal["layer"]): seal["sha256"] for seal in seals["seals"]}
    errors = []
    for layer in LAYERS:
        manifest = _load_manifest(layer)
        digest = seal_manifest(manifest)
        ref = expected.get(layer)
        ok = ref == digest
        if verbose:
            print(f"{layer:14s} {'OK ' if ok else 'KO'} {digest[:16]}")
        if not ok:
            errors.append(f"{layer}: attendu {ref[:16]} trouve {digest[:16]}")
    ok_all = not errors
    if not ok_all and verbose:
        print("DIVERGENCE", file=sys.stderr)
    for err in errors:
        print(err, file=sys.stderr)
    return 0 if ok_all else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m gtt.judge")
    parser.add_argument("--ci", action="store_true", help="sortie compacte pour la CI")
    args = parser.parse_args(argv)
    return judge(verbose=not args.ci)


if __name__ == "__main__":
    raise SystemExit(main())