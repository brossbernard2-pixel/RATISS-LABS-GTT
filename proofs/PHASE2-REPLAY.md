# Reçu R7 — rejeu phase 2

Deux runs consécutifs de `scripts/replay_phase2.sh` (même poste, même commit).
Les deux reçus sont strictement identiques (SHA-256 des étapes).

## Runs

| Étape | run 1 (073907) | run 2 (073908) |
|---|---|---|
| pytest core (normalisé) | `dabf355f…bcdf82` | identique |
| terrain generate | `b28b0809…b9ca6` | identique |
| terrain run_core | `b7b363b7…71cda` | identique |
| expected.json (sha256) | `631083aa…42b06` | identique |
| juge (gtt.judge --ci) | `e3b0c442…52b855` | identique |

Reçus bruts :
- `proofs/PHASE2-REPLAY-20260913-073907.md`
- `proofs/PHASE2-REPLAY-20260913-073908.md`

## Rejouabilité

    bash scripts/replay_phase2.sh      # rejoue en 1 commande
    diff proofs/PHASE2-REPLAY-*.md     # deux runs consécutifs -> identiques

## Audi­tion

| Acteur | Statut |
|---|---|
| Auditeur indépendant (Rouge) | EN ATTENTE |

*(reçu généré le 2026-09-13 par l'équipe de création, phase 2)*