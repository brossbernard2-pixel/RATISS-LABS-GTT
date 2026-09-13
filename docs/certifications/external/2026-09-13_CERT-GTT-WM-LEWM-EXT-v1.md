# CERTIFICATION COMPACTE — GTT : PREMIER RUN EXTERNE RÉEL + CLÔTURE v1 (côté construction)

**Dépôt** : github.com/brossbernard2-pixel/RATISS-LABS-GTT
**HEAD certifié** : `8266ed6` (25 commits) · **CI** : success
**Date** : 2026-09-13 · **Constructeur/exécuteur** : Rouge en relais
(ordre du chef « pleine puissance », renouvelé ce jour). **Auditeur
indépendant** : EN ATTENTE — kit fourni `docs/AUDIT-INDEPENDANT-KIT.md`
(rejeu en 1 commande + formulaire de verdict). Auto-audit disclosed.

## 1. L'événement : première mesure sur un VRAI modèle du monde externe

`scripts/wm_externe_lewm.py` — **LeWorldModel officiel** (Maes, Le Lidec,
Scieur, LeCun, Balestriero 2026) sur l'environnement officiel TwoRooms :

- checkpoint HF public `quentinll/lewm-tworooms`, SHA-256 scellé
  `566f2236…f7dd`, chargé en **state_dict STRICT** (301/301 clés, pooler
  légitimement absent) — 18 034 478 paramètres, inférence seule,
  gradients désactivés, modèle jamais modifié.
- code officiel `lucas-maes/le-wm` @`8edfeb33…` importé par **dépendance
  git à SHA scellé** (comme le juge analyse GTT) — anti-copie : 0 bloc
  commun ≥11 lignes vs 66 fichiers le-wm+stable-worldmodel.
- paramètres scellés AVANT le run (R6) : seed 13, 28 frames (3 historique
  + 25 futur), frameskip 5 → 135 actions env, blocs 10-dim = 5×2
  chronologiques (conformes au `train.py` officiel), pipeline pixels =
  `eval.py` officiel (ImageNet, 224).
- violation = contrat JEPA lui-même (L2 relative prédiction vs embedding
  ancré) : **ouvert 0.840789108872 (max 1.17440366745) → correction aval
  (ancrage observationnel) 0.214657575488 (max 0.275687664747)**.
- **delta d'ablation publié : 0.626131533384 — verdict APPROVED** (publié
  quel qu'il soit, DoD). Reçus ×2 byte-identiques + reproduction sur
  clone frais identique.
- Divulgations : statistiques du scaler d'entraînement absentes du
  checkpoint (dataset 3,4 Go non téléchargé) → 2 variantes documentées,
  règle de sélection pré-enregistrée (argmin erreur un pas ancré), les
  DEUX publiées (V1 raw retenue : 0.2147 vs V2 : 0.3158). Portée : 1
  trajectoire, 1 seed, métrique latente — aucune généralisation, aucun
  « définitivement ».

## 2. Clôture construction v1 vérifiée ce jour (kit exécuté en vrai)

Clone frais `/tmp/gtt-audit-independant` @`8266ed6` : **102 tests
passed**, juge exit 0, **5/5 checks CONFORME** (wm, quantum, forecast,
agents, examples), rejeux R7 ×2 phases 4–7 reçus identiques, secrets
historique 0, run externe reproduit à l'identique. README v1 = vision
fusion + carte 9 couches à jour + provenance + rejeu (DoD).

## 3. Réserves (assumées, non bloquantes)

1. Auditeur indépendant EN ATTENTE sur phases 2–7 + run externe (kit prêt).
2. Run externe = première mesure, pas une campagne : multi-seeds/mondes
   = étape suivante sur ordre du chef.
3. lean_proof EN ATTENTE (C5) au run IBM M2.
4. Visas PROVENANCE = main du chef.
5. transformers v4 exigé (nommage ViT du checkpoint) — gardé fou dans le
   script (v5 → message EN ATTENTE explicite, exit 2).

**Verdict Rouge (auto-audit disclosed) : CONFORME. Le DoD « un run
d'ablation externe réel publié (verdict quelconque) » est REMPLI côté
construction. GTT v1 attend ses deux signatures : auditeur indépendant +
visas du chef.**
