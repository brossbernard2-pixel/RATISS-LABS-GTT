# CARTOGRAPHIE GTT — extrait public (territoires T1–T6)

Extrait public de la cartographie de fusion rédigée par l'Équipe Rouge
(2026-09-13) : ce que les dépôts historiques du chef contiennent
vraiment, organisé en six territoires. Le scan complet des 43 dépôts
(détails fichier à fichier, notes de gel/reconstruction) reste un
matériau privé du Chef — cet extrait n'en publie que la carte et les
ancrages de preuve. Rien n'est copié des dépôts sources : voir
`gtt/audit/PROVENANCE.md` (SHA relevés) et `docs/ORPHELINS.md`
(14 tombstones).

| Territoire | Force (scan 2026-09-13) | Devenu dans GTT |
|---|---|---|
| **T1 · Topologie computationnelle** | ★★★★★ | `gtt/core` (phase 2) + terrains d'épreuve |
| **T2 · Quantique classique + décohérence** | ★★★★ | `gtt/quantum` (phase 3) |
| **T3 · Agents & orchestration** | ★★★★ | `gtt/agents` (phase 6, wrappers sans autorité) |
| **T4 · Prévision & calibration** | ★★★ | `gtt/forecast` (phase 5, bot désarmé) |
| **T5 · Modèles du monde** | ★★ (graine) | `gtt/world_models` (phase 4 + campagne externe) |
| **T6 · Incarné / robotique** | ★★ | hors périmètre v1 (campagne ultérieure possible) |

## Territoire T5 · Modèles du monde — Preuve vivante v1

**Graine LeWM validée : voir
[Certification Externe 2026-09-13](certifications/external/2026-09-13_CERT-GTT-WM-LEWM-EXT-v1.md).
Premier run réel sur checkpoint public, delta d'ablation mesuré et
scellé.**

- Modèle : LeWorldModel officiel (Maes, Le Lidec, Scieur, LeCun,
  Balestriero), checkpoint TwoRooms public, inférence seule.
- Mesure publiée : violation ouverte 0.840789108872 → correction aval
  (ancrage observationnel, modèle intact) 0.214657575488 ; **delta
  0.626131533384**, verdict APPROVED. Portée divulguée : 1 trajectoire,
  1 seed, métrique latente (contrat JEPA).
- Rejeu : `scripts/wm_externe_lewm.py` (1 commande, dépendances lourdes
  optionnelles) ; intégrité verrouillée par
  `tests/integration/test_wm_coherence_external.py` (gardien hors-ligne).
- État d'audit : `docs/AUDIT_TRAIL.md` (auditeur indépendant EN ATTENTE).

La cartographie initiale disait de T5 : « La graine LeWM existe déjà :
couplage topologie ↔ dynamique latente. C'est ton pont vers LeCun. »
La preuve vivante v1 est le premier pas mesuré sur ce pont — la
topologie entre en jeu aux runs suivants (atlas de cohérence, M2–M4).
