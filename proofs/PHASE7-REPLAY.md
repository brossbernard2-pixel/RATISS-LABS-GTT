# Reçu R7 — rejeu phase 7 (examples (terrains))

Deux runs consécutifs de `scripts/replay_phase7.sh` (même poste, même
commit), reçus strictement identiques. Reçu machine-indépendant
(normalisation `<ROOT>`).

## Runs

| Étape | run 1 (155832) | run 2 (155833) |
|---|---|---|
| pytest (102 passed, normalisé) | `0c4cb670be8a4b9f…` | identique |
| vérifications examples (terrains) (CONFORME) | `5be9b9bd1b8d736f…` | identique |
| juge (gtt.judge --ci) | `e3b0c44298fc1c14…` | identique |

Reçus bruts :
- `proofs/PHASE7-REPLAY-20260913-155832.md`
- `proofs/PHASE7-REPLAY-20260913-155833.md`

## Rejouabilité

    bash scripts/replay_phase7.sh   # rejoue en 1 commande

## Audi­tion

| Acteur | Statut |
|---|---|
| Construction | **Rouge en relais, ordre du chef** (2026-09-13, « lance tous les protocoles ») — divulgation complète. |
| Auditeur indépendant | EN ATTENTE — constructeur ≠ auditeur (règle N2). Rejeu indépendant possible à tout moment sur clone frais. |

*(reçu généré le 2026-09-13, phase 7, relais Rouge)*
