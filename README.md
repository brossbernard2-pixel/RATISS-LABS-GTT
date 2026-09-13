# RATISS-LABS-GTT

**GTT — Geological Topological Tech.**

Un dépôt, neuf couches, une loi R7 (rejouabilité), une hypothèse testée
(LCT), une méthode rouge/bleu. Bâtir ici le système de calcul géologique
topologique de RATISS Labs, jugé couche par couche par le
[RATISS-Framework](https://github.com/brossbernard2-pixel/RATISS-Framework)
(dépendance git).

> **Banc d'essai public.** Ce dépôt est un terrain de travail et
> d'épreuve. Rien de ce qui s'y trouve n'est un résultat : les valeurs
> chiffrées n'apparaissent qu'avec l'outillage de la phase 2+ et sous
> scellé. Aucune affirmation n'est publiée ici.

## Carte des neuf couches

| Couche | Rôle | Statut phase 1 |
|---|---|---|
| `gtt/core` | topologie, thermodynamique, invariants, hypothèses | squelette |
| `gtt/quantum` | lanczos, MPS/DMRG, décohérence, connecteurs QPU | squelette |
| `gtt/world_models` | LEWM, audit de cohérence, correction, ablation | squelette |
| `gtt/forecast` | prévisions scellées, calibration, Metaculus | squelette |
| `gtt/agents` | orchestration, wrappers rouge/bleu, protocole | squelette |
| `gtt/receipts` | reçus vérifiables (Lean proof EN ATTENTE) | squelette |
| `gtt/audit` | hooks juge couche 1, provenance, journal des déviations | squelette |
| `gtt/viz` | topologie 3D, atlas de cohérence, graphe **phase 6** | docstrings |
| `gtt/io` | PDB, OSF, GitHub **phase 6** | docstrings |

## Loi unique et juge

La seule loi appliquée est **R7 : rejouabilité**. Toute valeur, tout
scellé, tout verdict passe par la commande du juge
`python -m ratiss` (couche 1 du RATISS-Framework). `gtt/judge.py`
re-scelle les MANIFEST de chaque couche et compare à `SEALS.json`
(SHA-256 en JSON canonique) : toute divergence fait échouer la CI.

Une hypothèse est testée : **LCT**, déclarée statut `HYPOTHESIS` dans
`gtt/core/hypotheses.py`. Elle ne fonde aucune construction.

## Méthode rouge/bleu

Le protocole rouge/bleu est décrit dans [`docs/PROTOCOL.md`](docs/PROTOCOL.md).
Aucun code n'exprime d'approbation : l'équipe rouge applique le juge,
l'équipe bleue répond par des reproductions rejouables.

## Installation et vérifications

```bash
pip install "ratiss-framework @ git+https://github.com/brossbernard2-pixel/RATISS-Framework.git"
pip install -e .
python -m pytest -q
python -m gtt.judge --ci
```

Les deux commandes doivent être vertes (portique CI).