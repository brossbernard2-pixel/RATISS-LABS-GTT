# KIT D'AUDIT INDÉPENDANT — GTT (phases 1–7 + run externe)

Destiné à **tout auditeur indépendant** (humain ou agent) : constructeur
≠ auditeur (règle N2). Les phases 2–7 ont été construites par Rouge en
relais (ordre du chef, divulgation complète) — leurs certifications sont
des **auto-audits disclosed**. Ce kit permet de tout rejouer sans faire
confiance à aucun document : une commande, des sorties attendues exactes.

## 0. Ne pas faire confiance — vérifier

Ne croyez AUCUN reçu, AUCUN certificat, AUCUN chiffre de ce dépôt avant
de les avoir rejoués. Les colonnes « auditeur indépendant » sont
`EN ATTENTE` : c'est vous.

## 1. Rejeu complet (dépendances légères, ~2 min)

```bash
bash scripts/audit_independant.sh
```

Le script clone le dépôt, installe, et exécute TOUTES les vérifications
ci-dessous en séquence, puis imprime un **formulaire de verdict** à
remplir. Sortie attendue en fin : `FORMULAIRE PRÊT — à signer par l'auditeur`.

## 2. Vérifications manuelles (si vous préférez)

```bash
git clone https://github.com/brossbernard2-pixel/RATISS-LABS-GTT.git && cd RATISS-LABS-GTT
pip install "ratiss-framework @ git+https://github.com/brossbernard2-pixel/RATISS-Framework.git"
pip install -e .
python -m pytest -q                    # ATTENDU : 102 passed
python -m gtt.judge --ci; echo $?      # ATTENDU : 0
python scripts/wm_check.py       | tail -1   # ATTENDU : RESULTAT: CONFORME
python scripts/quantum_check.py  | tail -1   # ATTENDU : RESULTAT: CONFORME
python scripts/forecast_check.py | tail -1   # ATTENDU : RESULTAT: CONFORME
python scripts/agents_check.py   | tail -1   # ATTENDU : RESULTAT: CONFORME
python scripts/examples_check.py | tail -1   # ATTENDU : RESULTAT: CONFORME
for p in 4 5 6 7; do bash scripts/replay_phase$p.sh; done
# ATTENDU : exit 0 à chaque fois, reçus proofs/PHASE*-REPLAY-*.md ;
# deux runs consécutifs → reçus byte-identiques hors horodatage.
```

## 3. Valeurs scellées à comparer (vérités déterministes)

| contrôle | valeur attendue (exacte, stdlib) |
|---|---|
| wm_check — violation substitut synthétique | 0.104622125411 |
| wm_check — corrigé | 3.33e-16 (ordre de grandeur, epsilon machine) |
| forecast_check — Brier(0.75, vrai) | 0.0625 |
| forecast_check — ECE jeu connu | 0.4 |
| forecast_check — plafond bot | 250 questions → n=200, truncated=True |
| examples_check — SIR conservation | 0.0 exact ; Betti cycle4 [1,1] |
| examples_check — chaleur stable r=0.4 | amplitude 1.001 → 0.405814158613 |
| examples_check — chaleur instable r=0.6 | amplitude 1.001 → 4.60735959433 |
| agents_check — protocole 1.0 | 5 étapes, judge exit 0, lean EN ATTENTE |

## 4. Run externe réel LeWM (optionnel, dépendances lourdes, ~5 min)

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "transformers<5" stable-worldmodel einops
python scripts/wm_externe_lewm.py
```

ATTENDU (même poste : identique ; entre postes : tolérance relative 1e-6,
BLAS) : variante retenue `V1_raw` ; ouvert moy **0.840789108872** ;
ancré moy **0.214657575488** ; delta **0.626131533384** ;
`RESULTAT: APPROVED`. Le script vérifie lui-même : SHA-256 du checkpoint
HF (`566f2236…f7dd`), SHA du repo officiel `lucas-maes/le-wm`
(`8edfeb33…`), chargement state_dict STRICT. Toute divergence → exit ≠ 0.

## 5. Hygiène (à vérifier aussi)

```bash
git log -p | grep -cE '^\+.*(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-)'
# ATTENDU : 0
grep -rniE 'certifi|garanti|pionnier|seule solution' gtt/ README.md --include='*.py' | wc -l
# ATTENDU : 0 occurrence revendiquée (les « certifié » ne visent que des
# artefacts hors GTT ou sont dans ce kit/README à titre descriptif)
```

Anti-copie : le dépôt ne contient aucun bloc ≥11 lignes commun avec les
dépôts sources listés dans `gtt/audit/PROVENANCE.md` (méthode : fenêtres
glissantes normalisées + SHA-256). Le run externe importe le code
officiel LeWM par clone git à SHA scellé — jamais copié dans ce dépôt.

## 6. Ce qui reste volontairement EN ATTENTE (ne pas combler)

- `gtt/receipts/lean_proof.py` : stub — aucun reçu Lean fabriqué (C5).
  À combler au run IBM M2 avec de vrais reçus.
- Colonnes « auditeur indépendant » des reçus phases 2–7 : à remplir par
  VOUS après rejeu, avec votre identité et le SHA du commit rejoué.
- Visas PROVENANCE : réservés au chef (Jonathan).
- Bot Metaculus : jamais armé (`SUBMIT_AUTORISE = False`, plafond 200).
  Toute soumission réelle exigerait un ordre explicite du chef.

## 7. Formulaire de verdict (à copier dans votre rapport)

```
AUDIT INDÉPENDANT GTT
Auditeur (identité) : ______________________
Commit rejoué (SHA) : ______________________
Date (UTC)          : ______________________
pytest 102 passed   : OUI / NON
judge exit 0        : OUI / NON
5 checks CONFORME   : OUI / NON
rejeux ×2 identiques: OUI / NON
run externe LeWM    : APPROVED / DIVERGENCE / NON EXÉCUTÉ
secrets 0           : OUI / NON
VERDICT FINAL       : CONFORME / DIVERGENCE
Réserves            : ______________________
Signature           : ______________________
```
