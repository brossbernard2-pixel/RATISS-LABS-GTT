# Reçu R7 — rejeu phase 6 (agents+receipts+viz+io)

Deux runs consécutifs de `scripts/replay_phase6.sh` (même poste, même
commit), reçus strictement identiques. Reçu machine-indépendant
(normalisation `<ROOT>`).

## Runs

| Étape | run 1 (155830) | run 2 (155831) |
|---|---|---|
| pytest (102 passed, normalisé) | `0c4cb670be8a4b9f…` | identique |
| vérifications agents+receipts+viz+io (CONFORME) | `41ac775b864ebba1…` | identique |
| juge (gtt.judge --ci) | `e3b0c44298fc1c14…` | identique |

Reçus bruts :
- `proofs/PHASE6-REPLAY-20260913-155830.md`
- `proofs/PHASE6-REPLAY-20260913-155831.md`

## Rejouabilité

    bash scripts/replay_phase6.sh   # rejoue en 1 commande

## Audi­tion

| Acteur | Statut |
|---|---|
| Construction | **Rouge en relais, ordre du chef** (2026-09-13, « lance tous les protocoles ») — divulgation complète. |
| Auditeur indépendant | EN ATTENTE — constructeur ≠ auditeur (règle N2). Rejeu indépendant possible à tout moment sur clone frais. |

*(reçu généré le 2026-09-13, phase 6, relais Rouge)*
