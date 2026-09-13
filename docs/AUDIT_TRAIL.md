# AUDIT TRAIL — journal public des états d'audit (GTT)

Document vivant. Chaque certification, chaque run scellé et chaque état
d'attente y est visible publiquement — les états `EN ATTENTE` avec la
même rigueur que les succès (règle N2 : constructeur ≠ auditeur ; R7 :
toute valeur a un reçu rejouable). Les artefacts liés sont immuables :
le test gardien `tests/integration/test_wm_coherence_external.py`
verrouille leurs SHA-256 ; toute altération casse la CI.

Journal des déviations côté construction : `gtt/audit/PROVENANCE.md`
(sources) et le journal du chef (workspace, D-001…D-013).

---

## 2026-09-13 : Certification WM Externe LeWM (v1)

- **Statut :** CONFORME (auto-audit Rouge, disclosed) | ⏳ Auditeur
  Indépendant EN ATTENTE (kit fourni : `docs/AUDIT-INDEPENDANT-KIT.md`,
  rejeu en 1 commande)
- **Artefact canonique :**
  `docs/certifications/external/2026-09-13_CERT-GTT-WM-LEWM-EXT-v1.md`
  (byte-identique à l'original, SHA-256
  `b300911feb17f6cd33c12ffa931b655514691d36b002f7f516cb98b6514735b6`,
  verrouillé par test gardien)
- **Reçus R7 :** `proofs/WM-EXTERNE-LEWM-20260913-161848.md` et
  `…-161856.md` (runs ×2 identiques ; reproduction sur clone frais
  identique ; immuables, SHA-256 verrouillés)
- **Résultat clé :** delta d'ablation = **0.626131533384** (violation
  ouverte 0.840789108872 → correction aval ancrée 0.214657575488),
  verdict **APPROVED**, variante retenue V1_raw (règle de sélection
  pré-enregistrée). Portée divulguée : 1 trajectoire, 1 seed, métrique
  latente (contrat JEPA) — aucune généralisation revendiquée.
- **Commit source :** `8266ed6` (run) · intégration gardien : ordre du
  chef « GO 1-4 » du 2026-09-13.
- **Prochaine étape :** attente verdict auditeur externe OU lancement
  multi-seeds (ordre du Chef).

## 2026-09-13 : Décision R3 — architecture des dépôts (ÉTAPE 5 GELÉE)

Proposition externe de fusionner GTT dans un dépôt monolithique puis
d'archiver `RATISS-LABS-GTT` : **refusée par l'Équipe Rouge** (brise la
séparation juge/jugé et la décision des deux produits), **gelée
indéfiniment par le Chef**. Les deux dépôts restent séparés et actifs :
`RATISS-Framework` (méthode/juge, couche 1) juge `RATISS-LABS-GTT`
(vaisseau, 9 couches) par dépendance git scellée en CI. Toute migration
future = campagne journalisée avec re-scellage, sur ordre explicite du
Chef (porte R3).

## 2026-09-13 : Phases 5+6+7 (forecast, agents/receipts/viz/io, examples)

- **Statut :** CONSTRUITE + AUTO-AUDITÉE (relais Rouge, ordre du chef,
  divulgation complète) | ⏳ Auditeur Indépendant EN ATTENTE
- **Artefacts :** `proofs/PHASE5-REPLAY.md`, `PHASE6-REPLAY.md`,
  `PHASE7-REPLAY.md` (+ reçus bruts ×2 par phase) ; certificat compact
  phases 5–7 (workspace chef) ; commits `4600ec1`…`de8dfbe`.
- **Résultats clés :** 5 checks déterministes CONFORME ; rejeux ×2
  byte-identiques, y compris entre poste de construction et clone frais.

## 2026-09-13 : Phase 4 · world_models (substitut synthétique)

- **Statut :** CONSTRUITE + AUTO-AUDITÉE `d99ec26` | ⏳ Auditeur EN ATTENTE
- **Résultat clé :** delta d'ablation 0.104622125411 sur substitut
  synthétique (dérive analytique apprise) ; corrigé ≈ 3.33e-16.
  Remplacé comme référence externe par le run LeWM réel (voir plus haut)
  — les deux restent publiés, aucun n'est écrasé.

## 2026-09-13 : Phases 1–3 (core/audit, quantum, fondations)

- **Statut :** Phase 1 CERTIFIÉE `abbdfdb` (OpenHands construit, Rouge
  audite) ; Phase 2 CERTIFIÉE `539f747` et Phase 3 CERTIFIÉE `1f53dbb`
  (relais Rouge, auto-audit disclosed, findings F1–F4 divulgués) |
  ⏳ Auditeur Indépendant EN ATTENTE sur 2–3.

---

*Règle de ce journal : on ajoute, on ne réécrit jamais (comme l'histoire
git). Un état EN ATTENTE n'est effacé que par le reçu de l'auditeur
indépendant ou l'ordre du Chef.*
