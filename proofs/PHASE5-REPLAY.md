# Reçu R7 — rejeu phase 5 (forecast)

Deux runs consécutifs de `scripts/replay_phase5.sh` (même poste, même
commit), reçus strictement identiques. Reçu machine-indépendant
(normalisation `<ROOT>`).

## Runs

| Étape | run 1 (155828) | run 2 (155829) |
|---|---|---|
| pytest (102 passed, normalisé) | `0c4cb670be8a4b9f…` | identique |
| vérifications forecast (CONFORME) | `adf64973622c3dd9…` | identique |
| juge (gtt.judge --ci) | `e3b0c44298fc1c14…` | identique |

Reçus bruts :
- `proofs/PHASE5-REPLAY-20260913-155828.md`
- `proofs/PHASE5-REPLAY-20260913-155829.md`

## Rejouabilité

    bash scripts/replay_phase5.sh   # rejoue en 1 commande

## Audi­tion

| Acteur | Statut |
|---|---|
| Construction | **Rouge en relais, ordre du chef** (2026-09-13, « lance tous les protocoles ») — divulgation complète. |
| Auditeur indépendant | EN ATTENTE — constructeur ≠ auditeur (règle N2). Rejeu indépendant possible à tout moment sur clone frais. |

*(reçu généré le 2026-09-13, phase 5, relais Rouge)*
