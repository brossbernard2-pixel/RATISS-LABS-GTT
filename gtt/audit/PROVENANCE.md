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
| quantum/lanczos, mps_dmrg | github.com/jonathansearch/Algorithmes-quantique-Ratiss-labs- | `533d2647c16731fd78b1f8e01ae6580a8da83ec3` | réécrit | EN ATTENTE |
| quantum/mps_dmrg | github.com/jonathansearch/Travaux | `a341bf7392264c722be343d9c87e526fbf1c2a98` | réécrit | EN ATTENTE |
| quantum/qpu_connectors | github.com/jonathansearch/QPU-Ratiss-COSMOS | `00eecbd63a9a18ad374b0fc8da84b9f6de2b8977` | réécrit | EN ATTENTE |
| quantum/decoherence | github.com/jonathansearch/RATISS-QPU-AMBIENT | `0e7a6f3614f798f480571cdc43671fb51e5f98ec` | réécrit | EN ATTENTE |
| quantum/decoherence | github.com/jonathansearch/ratiss-topological-decoherence-engine | `ab13ba369087345b281f078036797599ba60313b` | réécrit | EN ATTENTE |
| world_models | github.com/jonathansearch/ratiss-lewm-integration | `68a1921b8cf720c80bacaab91ae6fd808cf27337` | réécrit (méthode) | EN ATTENTE |
| world_models (dynamiques) | méthode neuve — vérités analytiques (harmonique, Euler (1+ω²dt²)^t) | aucun code source | neuf | EN ATTENTE |
| forecast | github.com/jonathansearch/metac-bot-template (couche Jonathan seule) | `ab2397d347ac777dbfbe1c0e629fc3272de0f6c8` | réécrit | EN ATTENTE |
| agents | github.com/jonathansearch/ratiss-cypher-odv-scientist-v3 | `d7083f78c80cedddc544193c30d1b69360357777` | réécrit | EN ATTENTE |
| agents | github.com/jonathansearch/ratiss-scientist-agent | `d07619cf4f1675f7b090f74962f81e1e6bb066f2` | réécrit | EN ATTENTE |
| receipts | github.com/jonathansearch/Ratiss-Fusion-stark- (historique gelé) | `e1217791e9691a221d49221b763fa773ebbd6994` | reconstruit (neuf) | EN ATTENTE |
| audit | aucun | — | squelette | EN ATTENTE |
| viz | github.com/jonathansearch/ratiss-decoherence-atlas | `d4225414583005de049db1d48061f264e04b81bc` | réécrit (méthode visuelle) | EN ATTENTE |
| viz | github.com/jonathansearch/quantum-circuit-studio | `793ab9d1eb8e95c027160d5c6acd6ed1a110b98f` | réécrit (méthode visuelle) | EN ATTENTE |
| io | méthode neuve (PDB wwPDB public, APIs OSF/GitHub documentées) | aucun code source | neuf | EN ATTENTE |
| examples/TERRAIN-02 | github.com/jonathansearch/RATISS-BIOLAB | `7b9455ba61c94aaecd1610fb67a890c396c0341d` | réécrit | EN ATTENTE |
| examples/TERRAIN-03 | github.com/jonathansearch/RATISS-HPC | `5aae7f4f8929af4ea8a49e90dfaca100ae901e4f` | réécrit | EN ATTENTE |

Toutes les sources sont sur le compte public `jonathansearch` (correction
Rouge 2026-09-13 : la première rédaction indiquait à tort
`brossbernard2-pixel`, qui est le banc d'essai de livraison, pas la source).
Le terrain TERRAIN-01 est une réécriture de l'idée RATISS-GRID (même ligne
source ci-dessus). Vérification des SHAs : `git ls-remote
https://github.com/jonathansearch/<nom>.git HEAD`.

## Phase 3 — couche quantum (relais Rouge, ordre du chef 2026-09-13)

Construction par Rouge (pas le Bleu) sur ordre direct « Continue » après
phase 2 jugée « trop longue » — divulgation intégrale, règle N2 respectée :
colonne auditeur laissée `EN ATTENTE` puisque constructeur et auditeur
seraient la même main. SHAs sources relevés anonymement le 2026-09-13
(`git ls-remote`), dépôts publics.


## Phase 4 — couche world_models (relais Rouge, ordre du chef 2026-09-13)

Construction par Rouge (le Bleu est indisponible, réaffecté par le chef).
Paramètres scellés AVANT le code (R6, commit `0f06028`). Pont réel
LeWM/JEPA : campagne ultérieure, inférence seule, jamais de réentraînement.
Colonne auditeur `EN ATTENTE` : constructeur ≠ auditeur.


## Phases 5–7 — forecast, agents/receipts/viz/io, examples (relais Rouge, ordre du chef 2026-09-13)

Construction par Rouge (« lance tous les protocoles en même temps »).
Paramètres scellés AVANT le code (R6, commit `9990d7e`). Lean proof :
stub EN ATTENTE respecté (C5) — aucun reçu fabriqué. Bot Metaculus :
hors-ligne et désarmé par construction (plafond 200, soumission réelle
interdite dans le dépôt). Syncs OSF/GitHub : dry-run, tokens par
environnement jamais echo. Orphelins : `docs/ORPHELINS.md`, 14 tombstones
avec SHAs relevés anonymement — jamais copiés, jamais supprimés.
Colonnes auditeur `EN ATTENTE` : constructeur ≠ auditeur.

## Campagne externe world_models — run réel LeWM/TwoRooms (2026-09-13, relais Rouge)

| artefact | source | SHA / empreinte | nature | visa chef |
|---|---|---|---|---|
| scripts/wm_externe_lewm.py | github.com/lucas-maes/le-wm (code officiel LeWM) | `8edfeb336732b5f3ce7b8b210d0ba370a09e2cac` | import par dépendance git à SHA scellé — **zéro copie** | EN ATTENTE |
| checkpoint TwoRooms | Hugging Face `quentinll/lewm-tworooms` (public, non gaté) | poids sha256 `566f223624ea4bfb39dbfe6ae731198dd6ea73b7b8919fed6b1ecafca810f7dd` | inférence seule, chargement state_dict STRICT | EN ATTENTE |
| environnement TwoRooms | github.com/lucas-maes/stable-worldmodel (pip `stable-worldmodel`) | réf. repo `c77287402cd435928a2b6cbfa56c0fae4348f6c2` | dépendance pip, aucun code copié | EN ATTENTE |
| reçu | proofs/WM-EXTERNE-LEWM-20260913-*.md | delta publié 0.626131533384 (APPROVED) | mesure originale GTT | EN ATTENTE |

Divulgations : (1) les statistiques exactes du scaler d'actions du
dataset d'entraînement (3,4 Go, non téléchargé) ne sont pas fournies avec
le checkpoint → deux variantes documentées (V1 raw, V2 z-score uniforme),
règle de sélection pré-enregistrée (argmin erreur un pas ancré), les DEUX
publiées dans le reçu ; V1 retenue. (2) Portée : une trajectoire, un seed
(13), métrique latente = contrat JEPA ; aucune généralisation revendiquée.
(3) transformers v4 exigé (nommage ViT du checkpoint) ; versions exactes
dans le reçu. (4) Run construit et exécuté par Rouge en relais (ordre du
chef) — auditeur indépendant EN ATTENTE, kit : docs/AUDIT-INDEPENDANT-KIT.md.
