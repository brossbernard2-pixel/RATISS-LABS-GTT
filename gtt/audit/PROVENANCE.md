# Provenance des couches — RATISS-LABS-GTT

Règle N2 : la colonne **auditeur** est `EN ATTENTE` tant qu'un humain du
labo n'a pas revu la ligne.

## Phase 2 — couche core (réécrite)

Réécriture provenancée : lecture anonyme des dépôts sources puis rédaction
indépendante (aucun bloc > 10 lignes copié — vérifié au portique §6.2).
Les dépôts étant privés, le re-clonage n'est pas possible sur tout poste ;
les SHAs lus au moment de la collecte doivent être confirmés par un auditeur
ayant accès aux dépôts.

| Couche | Dépôt source | Commit source | Réécrit-copié | Auditeur |
|---|---|---|---|---|
| core | Algorithmes-quantique-Ratiss-labs- | SHAs lus en anonyme (vérif. auditeur requise) | réécrit | EN ATTENTE |
| core | RATISS-ODV-AEON | idem | réécrit | EN ATTENTE |
| core | RATISS-V10-Physical-Complexity-Audit | idem | réécrit | EN ATTENTE |
| core | ratiss-topological-decoherence-engine | idem | réécrit | EN ATTENTE |
| core | RATISS-GRID | idem | réécrit | EN ATTENTE |
| quantum | (phase 3) | — | — | EN ATTENTE |
| world_models | (phase 4) | — | — | EN ATTENTE |
| forecast | (phase 5) | — | — | EN ATTENTE |
| agents | (phase 6) | — | — | EN ATTENTE |
| receipts | (phase 7) | — | — | EN ATTENTE |
| audit | aucun | — | squelette | EN ATTENTE |
| viz | (phase 6) | docstrings | — | EN ATTENTE |
| io | (phase 6) | docstrings | — | EN ATTENTE |

URLs supposées : `https://github.com/brossbernard2-pixel/<nom>` (orga de
livraison du labo) sauf le terrain RATISS-GRID lisible sur
`https://github.com/jonathansearch/RATISS-GRID` (précisé au prompt §3).
Vérification du SHA et de l'accès : auditeur humain ayant les droits lecture
sur les dépôts.