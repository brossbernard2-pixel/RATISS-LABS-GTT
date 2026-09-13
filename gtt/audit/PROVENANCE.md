# Provenance des couches — RATISS-LABS-GTT

Règle N2 : la colonne **auditeur** est `EN ATTENTE` tant qu'un humain du
labo n'a pas revu la ligne.

## Phase 2 — couche core (réécrite)

Réécriture provenancée : lecture anonyme des dépôts sources puis rédaction
indépendante (aucun bloc > 10 lignes copié — vérifié au portique §6.2).
Les cinq dépôts sources sont PUBLICS (correction Rouge 2026-09-13 : la
mention « privés » de la première rédaction était fausse) ; les SHAs HEAD
ci-dessous ont été relevés anonymement le 2026-09-13 par Rouge et sont
re-vérifiables par `git ls-remote`.

| Couche | Dépôt source | Commit source | Réécrit-copié | Auditeur |
|---|---|---|---|---|
| core | github.com/jonathansearch/Algorithmes-quantique-Ratiss-labs- | `533d2647c16731fd78b1f8e01ae6580a8da83ec3` | réécrit | EN ATTENTE |
| core | github.com/jonathansearch/RATISS-ODV-AEON | `a686e92cd25178eeaa5e5e5e5bf87a4663a1031a` | réécrit | EN ATTENTE |
| core | github.com/jonathansearch/RATISS-V10-Physical-Complexity-Audit | `60e9d68788f031fa972de00570f2bcf6083a6455` | réécrit | EN ATTENTE |
| core | github.com/jonathansearch/ratiss-topological-decoherence-engine | `ab13ba369087345b281f078036797599ba60313b` | réécrit | EN ATTENTE |
| core | github.com/jonathansearch/RATISS-GRID | `864db22e0610533fa132943fa577d60333fc527d` | réécrit | EN ATTENTE |
| quantum | (phase 3) | — | — | EN ATTENTE |
| world_models | (phase 4) | — | — | EN ATTENTE |
| forecast | (phase 5) | — | — | EN ATTENTE |
| agents | (phase 6) | — | — | EN ATTENTE |
| receipts | (phase 7) | — | — | EN ATTENTE |
| audit | aucun | — | squelette | EN ATTENTE |
| viz | (phase 6) | docstrings | — | EN ATTENTE |
| io | (phase 6) | docstrings | — | EN ATTENTE |

Toutes les sources sont sur le compte public `jonathansearch` (correction
Rouge 2026-09-13 : la première rédaction indiquait à tort
`brossbernard2-pixel`, qui est le banc d'essai de livraison, pas la source).
Le terrain TERRAIN-01 est une réécriture de l'idée RATISS-GRID (même ligne
source ci-dessus). Vérification des SHAs : `git ls-remote
https://github.com/jonathansearch/<nom>.git HEAD`.