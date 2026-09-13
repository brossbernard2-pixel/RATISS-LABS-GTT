# Protocole rouge/bleu — RATISS-LABS-GTT

Règles de conduite de l'audit croisé du système GTT. Ce document est la
référence du protocole (C3) : le code ne contient **aucune** logique
d'approbation.

## Rôles

- **Équipe rouge** : applique le juge (dépendance git RATISS-Framework,
  commande `python -m ratiss`) sur chaque couche et sur toute valeur
  publiée. Rend des verdicts bruts, rejouables.
- **Équipe bleue** : répond à chaque rapport par une reproduction
  (commande exacte, mêmes entrées) ; ne discute jamais un verdict sans
  le rejouer.
- **Chef de labo** : arbitre les divergences. Aucune décision hors de
  cette triade rouge/bleu/chef.

## Déroulé d'un cycle

1. La couche est soumise au juge (scellé de son MANIFEST + rejouabilité
   R7).
2. L'équipe rouge écrit un rapport (`gtt/audit/`), verdict par verdict.
3. L'équipe bleue rejoue les commandes et joint les sorties.
4. Divergence résolue soit par correction du code, soit par deviation
   journalisée (`gtt/audit/deviation_log.py`, format R5 chaîné).
5. Le chef arbitre si le désaccord persiste.

## Règle N2

Toute table de provenance porte une colonne **auditeur** :
`EN ATTENTE` tant qu'un humain n'a pas validé la ligne. Aucune ligne de
provenance n'est considérée comme revue sans nom d'auditeur humain.

## Portique CI

Avant chaque poussée :

1. `python -m pytest -q` vert (tests hors réseau).
2. `python -m gtt.judge --ci` vert (les MANIFEST servis correspondent
   aux scellés de `SEALS.json`).
3. Scan secrets des deux dépôts : vide.
4. Zéro occurrence du vocabulaire interdit (voir prompt §3).

Un seul point raté = divergence. On casse-construit jusqu'à passer.