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

*(reçu généré le 2026-09-13 par l'équipe de création, phase 2 ;
rejoué et visé par Rouge le 2026-09-13 — voir ci-dessous.)*

---

## Rejeu Rouge après correctifs (2026-09-13, commits du jour — audit Rouge)

Correctifs audités puis rejoués : (1) `persistent_pairs` — classes
essentielles en dimension ≥ 1 détectées sur colonnes RÉDUITES vides
(+ 2 tests de régression : cercle dim1, tore essentielles = Betti) ;
(2) reçu machine-indépendant — normalisation `<ROOT>` des sorties et des
commandes, option pytest bruitante retirée ; (3) MANIFEST core 0.2.1
(`implemented-p2-audit`) rescellé, juge vert ; (4) PROVENANCE core — URLs
et SHAs HEAD réels des cinq sources publiques.

| Étape | run 1 (090605) | run 2 (090606) |
|---|---|---|
| pytest (28 passed, normalisé) | `01ac6615d7bcb4d1…` | identique |
| terrain generate | `25edbf72b799c328…` | identique |
| terrain run_core | `223c2389ba3a7102…` | identique |
| expected.json (sha256) | `631083aa3c500fca…` | identique — **inchangé avant/après correctifs** |
| juge (gtt.judge --ci) | `e3b0c44298fc1c14…` | identique |

Reçus bruts : `proofs/PHASE2-REPLAY-20260913-090605.md` et `-090606.md`.
Les reçus du Bleu (073907/073908) restent au dépôt, non modifiés.

## Audi­tion

| Acteur | Statut |
|---|---|
| Équipe Rouge (auditeur) | **VÉRIFIÉ le 2026-09-13** — rejeu indépendant : 2 runs consécutifs, scellés identiques ; correctifs appliqués et re-testés (28 passed, juge exit 0, expected.json inchangé). Colonne remplie par Rouge seul, selon la règle N2 du labo. |
