# RATISS-LABS-GTT

**GTT — Geological Topological Tech.** Un seul dépôt, neuf couches, une
loi unique (R7 : rejouabilité), un juge mécanique (couche 1 du
[RATISS-Framework](https://github.com/brossbernard2-pixel/RATISS-Framework),
dépendance git), une méthode rouge/bleu.

**Vision** : outiller la *cohérence physique des modèles du monde* —
mesurer la violation des lois physiques dans les prédictions d'un modèle
externe, la réduire **en aval sans jamais toucher au modèle**, et publier
le delta, quel qu'il soit. « Corriger définitivement » est une vision,
jamais une affirmation : aucun résultat n'est revendiqué avant ses reçus.

> **Banc d'essai public.** Ce dépôt est un terrain de travail et
> d'épreuve. Les valeurs chiffrées n'y apparaissent que sous scellé
> (R6 : paramètres figés avant le premier run) et avec reçu rejouable
> (R7). Rien n'est publié sans le visa du chef.

## Carte des neuf couches (statut 2026-09-13)

| Couche | Rôle | Statut |
|---|---|---|
| `gtt/core` | topologie, thermodynamique, invariants, hypothèse LCT | implémentée (phase 2) |
| `gtt/quantum` | Lanczos, MPS/DMRG, décohérence T1/T2, connecteur QPU dry-run | implémentée (phase 3) |
| `gtt/world_models` | pont LEWM, audit de cohérence, correction aval, ablation | implémentée (phase 4) + **run externe réel** |
| `gtt/forecast` | calibration Brier/ECE, prédictions scellées R5, journal chaîné, bot Metaculus hors-ligne désarmé | implémentée (phase 5) |
| `gtt/agents` | orchestrateur sans autorité, wrappers rouge/bleu, protocole 1.0 | implémentée (phase 6) |
| `gtt/receipts` | hash rejouable, vérification de reçus ; **Lean proof EN ATTENTE (run M2)** | implémentée (phase 6) |
| `gtt/audit` | hooks juge, PROVENANCE, journal des déviations | implémentée (phase 1) |
| `gtt/viz` | topologie 3D isométrique (SVG), atlas de cohérence, graphe de preuves (DOT) | implémentée (phase 6) |
| `gtt/io` | PDB wwPDB, syncs OSF/GitHub **dry-run**, tokens par environnement jamais echo | implémentée (phase 6) |

Terrains d'épreuve : `examples/TERRAIN-02` (SIR), `examples/TERRAIN-03`
(chaleur 1D Neumann) avec `expected.json` scellés. Dépôts historiques
gelés : `docs/ORPHELINS.md` (14 tombstones avec SHA-256 — rien copié,
rien supprimé).

## Loi unique et juge

La seule loi appliquée est **R7 : rejouabilité**. `gtt/judge.py` re-scelle
les MANIFEST de chaque couche et compare à `SEALS.json` (SHA-256 en JSON
canonique, API du juge couche 1 `python -m ratiss`) : toute divergence
fait échouer la CI (job `judge`). L'hypothèse **LCT** est déclarée statut
`HYPOTHESIS` dans `gtt/core/hypotheses.py` ; elle ne fonde aucune
construction.

## Première mesure sur modèle externe RÉEL

`scripts/wm_externe_lewm.py` — inférence seule, chargement strict :
**LeWorldModel** officiel (Maes, Le Lidec, Scieur, LeCun, Balestriero —
checkpoint HF public `quentinll/lewm-tworooms`, code `lucas-maes/le-wm`
importé par dépendance git à SHA scellé, zéro copie) sur l'environnement
officiel TwoRooms. Violation = contrat JEPA (L2 relative prédiction vs
embedding ancré) :

| régime | violation moyenne | violation max |
|---|---|---|
| ouvert (sans correction) | 0.840789108872 | 1.17440366745 |
| correction aval (ancrage observationnel, modèle intact) | 0.214657575488 | 0.275687664747 |

**Delta d'ablation publié : 0.626131533384** — verdict APPROVED, une
trajectoire, un seed, métrique latente : portée limitée et divulguée.
Reçu : `proofs/WM-EXTERNE-LEWM-20260913-*.md`. Le delta de la phase 4
(0.104622125411) reste celui du substitut synthétique.

## Méthode rouge/bleu

Protocole : [`docs/PROTOCOL.md`](docs/PROTOCOL.md). L'orchestrateur n'a
aucune autorité (registre) ; l'équipe rouge applique le juge et publie
des verdicts bruts ; l'équipe bleue répond uniquement par reproductions
rejouables (reçus R7). **Phases 2–7 construites par Rouge en relais, sur
ordre du chef, avec divulgation complète** : la colonne « auditeur » de
tous les reçus reste `EN ATTENTE` (règle N2 : constructeur ≠ auditeur).
Kit de rejeu indépendant : [`docs/AUDIT-INDEPENDANT-KIT.md`](docs/AUDIT-INDEPENDANT-KIT.md).

## Installation et vérifications

```bash
pip install "ratiss-framework @ git+https://github.com/brossbernard2-pixel/RATISS-Framework.git"
pip install -e .
python -m pytest -q          # 108 tests, stdlib seulement (dont 6 gardiens hors-ligne du run externe)
python -m gtt.judge --ci     # exit 0 = sceaux intacts
python scripts/wm_check.py && python scripts/quantum_check.py \
  && python scripts/forecast_check.py && python scripts/agents_check.py \
  && python scripts/examples_check.py     # 5 × « RESULTAT: CONFORME »
bash scripts/replay_phase4.sh             # reçu R7 (idem phases 5, 6, 7)
```

Run externe réel (dépendances lourdes hors dépôt, optionnel) :

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "transformers<5" stable-worldmodel einops
python scripts/wm_externe_lewm.py         # reçu dans proofs/
```

## Provenance

Chaque ligne de code a sa source dans
[`gtt/audit/PROVENANCE.md`](gtt/audit/PROVENANCE.md) (dépôt, SHA relevé,
nature : réécrit/neuf/import). Anti-copie vérifiée par scan de blocs
(≥11 lignes) contre tous les dépôts sources : 0 bloc commun. Les visas
du chef y sont `EN ATTENTE` jusqu'à sa signature.
