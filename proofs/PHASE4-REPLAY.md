# Reçu R7 — rejeu phase 4 (world_models)

Deux runs consécutifs de `scripts/replay_phase4.sh` (même poste, même
commit), reçus strictement identiques. Reçu machine-indépendant
(normalisation `<ROOT>`).

## Runs

| Étape | run 1 (20260913-153300) | run 2 (20260913-153300) |
|---|---|---|
| pytest (64 passed, normalisé) | `eb8d5233f18a7bdd…` | identique |
| vérifications world_models (CONFORME) | `2c343b0bbe40c3f4…` | identique |
| juge (gtt.judge --ci) | `e3b0c44298fc1c14…` | identique |

Reçus bruts :
- `proofs/PHASE4-REPLAY-20260913-153300.md`
- `proofs/PHASE4-REPLAY-20260913-153300.md`

## Contrôles scellés par `scripts/wm_check.py`

Harmonique exact : violation ~0 ; surrogate appris (Euler) : violation =
forme fermée (1+ω²dt²)^10 − 1 = 0.104622125411 (delta 0) ; correction en
aval : violation → précision machine, modèle intact ; ablation :
sans=0.104622125411 avec≈3.3e-16 delta=0.104622125411 ; scores de
cohérence exact=1.0 appris=0.0. Paramètres figés et scellés AVANT les runs
(R6, commit 0f06028 antérieur au code).

## Rejouabilité

    bash scripts/replay_phase4.sh   # rejoue en 1 commande
    python3 scripts/wm_check.py     # vérifications seules

## Audi­tion

| Acteur | Statut |
|---|---|
| Construction | **Rouge en relais, ordre du chef** (2026-09-13, « passe à la phase 4 … le blue est indisponible ») — divulgation complète. |
| Auditeur indépendant | EN ATTENTE — Rouge ayant construit, la colonne attend un rejeu indépendant (le Bleu quand il sera libre, ou tout tiers) sur clone frais. |

*(reçu généré le 2026-09-13, phase 4, relais Rouge)*
