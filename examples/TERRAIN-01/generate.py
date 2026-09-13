"""Génère une grille de tension synthétique déterministe (seed 20260913).

Réécriture provenancée de l'idée RATISS-GRID (aucune copie de code) :
une maille 4x4 de nœuds alimentés en tension quasi-50 Hz, avec un bruit
déterministe piloté par le seed. Même seed -> mêmes données sur tout poste.
"""

import json
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent / "grid.json"
SEED = 20260913
NODES = 16
FS = 4000          # Hz
DURATION = 0.06    # s (~3 périodes de 50 Hz)
FREQ = 50.0


def build_grid(seed: int = SEED) -> dict:
    """Construit la grille (déterministe) : séries temporelles par nœud."""
    rng = random.Random(seed)
    amplitude = 230.0 * math.sqrt(2.0)
    samples = int(FS * DURATION)
    series = {f"n{i}": [] for i in range(NODES)}
    for t in range(samples):
        th = 2.0 * math.pi * FREQ * t / FS
        for i in range(NODES):
            bruit = rng.uniform(-1.5, 1.5)
            series[f"n{i}"].append(round(amplitude * math.sin(th) + bruit, 6))
    return {
        "seed": seed,
        "fs": FS,
        "freq": FREQ,
        "duration": DURATION,
        "nodes": NODES,
        "nominal_rms": 230.0,
        "series": series,
    }


if __name__ == "__main__":
    OUT.write_text(
        json.dumps(build_grid(), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"grille écrite : {OUT}")