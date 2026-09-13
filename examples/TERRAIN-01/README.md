# TERRAIN-01 — grille synthétique (phase 2)

But : exercer la couche `core` (topologie, invariants,
cohérence) sur une grille de tension synthétique 4x4 inspirée de
RATISS-GRID (réécriture provenancée, aucun bloc copié).

## Commandes

    python3 generate.py          # écrit grid.json (seed 20260913, déterministe)
    python3 run_core.py          # calcule et écrit expected.json (déterministe)

Sorties portées : Betti du réseau, P_sig (aire de Takens m=2), invariants
de conservation/symplecticité/réversibilité, score de cohérence.

## Reproductibilité

Même seed (20260913) sur toute machine -> mêmes grid.json et expected.json.
Le hash du reçu R7 (PHASE2-REPLAY) ancre ces sorties.