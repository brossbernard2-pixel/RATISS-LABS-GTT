# Reçu R7 — rejeu phase 3 (quantum)

Deux runs consécutifs de `scripts/replay_phase3.sh` (même poste, même commit),
reçus strictement identiques. Reçu machine-indépendant (normalisation
`<ROOT>`, héritée du correctif phase 2).

## Runs

| Étape | run 1 (124501) | run 2 (124502) |
|---|---|---|
| pytest (50 passed, normalisé) | `0ab513fb734ef99c…` | identique |
| vérifications quantum (CONFORME) | `7506a2c644fcf72f…` | identique |
| juge (gtt.judge --ci) | `e3b0c44298fc1c14…` | identique |

Reçus bruts :
- `proofs/PHASE3-REPLAY-20260913-124501.md`
- `proofs/PHASE3-REPLAY-20260913-124502.md`

## Contrôles scellés par `scripts/quantum_check.py`

ED N=2 = forme fermée −√(J²+4h²) (delta 0) ; ED vs DMRG N=4 et N=5
(delta 0) ; Lanczos P8 vs spectre analytique (delta 0) ; lois exactes
déphasage/relaxation T1-T2 (delta 0) ; connecteur QPU dry-run déterministe.

## Rejouabilité

    bash scripts/replay_phase3.sh    # rejoue en 1 commande
    python3 scripts/quantum_check.py # vérifications seules

## Audi­tion

| Acteur | Statut |
|---|---|
| Construction | **Rouge en relais, sur ordre direct du chef** (2026-09-13, « Continue ») — divulgation complète : cette phase n'a PAS été construite par le Bleu. |
| Auditeur indépendant | EN ATTENTE — Rouge ayant construit, la colonne auditeur attend un rejeu indépendant (le Bleu peut rejouer `scripts/replay_phase3.sh` sur clone frais, ou tout tiers). Auto-audit Rouge documenté dans audit/CERTIFICATION-GTT-PHASE3 (workspace chef). |

*(reçu généré le 2026-09-13, phase 3, relais Rouge)*
