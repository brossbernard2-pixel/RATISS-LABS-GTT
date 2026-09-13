"""Test GARDIEN hors-ligne — intégrité du run externe réel LeWM (R6/R7).

Gardien statique (stdlib, sans réseau, sans torch) : il verrouille
1. le certificat canonique (byte-identique, SHA-256 scellé),
2. les reçus R7 du run externe (immuables, SHA-256 scellés),
3. les paramètres scellés R6 du script (aucune re-scelle silencieuse),
4. les chiffres publiés (verbatim dans les reçus),
5. les verrous de sécurité du script (chargement strict, transformers v4).

Toute modification d'un de ces artefacts fait ÉCHOUER ce test → blocage
immédiat (CI rouge). Re-sceller légitimement = déviation journalisée (R5)
ET mise à jour de ce fichier dans le même commit — visible en revue.

Le rejeu LOURD du run (torch, transformers v4, checkpoint 72 Mo) n'est
pas exigé ici : il reste optionnel via `scripts/wm_externe_lewm.py` et le
kit `docs/AUDIT-INDEPENDANT-KIT.md` — un test CI dépendant du réseau ou
de Hugging Face serait fragile par construction (divulgation D-012).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]

# ------------------------------------------------------------------ SCELLÉS
# Valeurs d'or figées à l'intégration (ordre du chef « GO 1-4 », 2026-09-13,
# commit source du run : 8266ed6). NE MODIFIER QU'AVEC DÉVIATION JOURNALISÉE.
CERTIFICAT = RACINE / "docs/certifications/external/2026-09-13_CERT-GTT-WM-LEWM-EXT-v1.md"
SHA_CERTIFICAT = "b300911feb17f6cd33c12ffa931b655514691d36b002f7f516cb98b6514735b6"

RECUS = {
    RACINE / "proofs/WM-EXTERNE-LEWM-20260913-161848.md":
        "bc9cf09941fd86df6fe0c2e15adb39c131fedc91e7ee3d8cf5c614aa9978eedf",
    RACINE / "proofs/WM-EXTERNE-LEWM-20260913-161856.md":
        "96fb6d3e94c0c00cf135e444c7fa57c10850c3bdccefca554528258109254e64",
}

SCRIPT = RACINE / "scripts/wm_externe_lewm.py"
SCELLES_OR = {
    "modele_repo_git": "https://github.com/lucas-maes/le-wm.git",
    "modele_repo_sha": "8edfeb336732b5f3ce7b8b210d0ba370a09e2cac",
    "checkpoint_hf": "quentinll/lewm-tworooms",
    "sha256_poids": "566f223624ea4bfb39dbfe6ae731198dd6ea73b7b8919fed6b1ecafca810f7dd",
    "sha256_config": "2564086e961e7b5c7c04dffc451091115b389a590645ff19653c64fd0bc16e09",
    "swm_repo_reference": "c77287402cd435928a2b6cbfa56c0fae4348f6c2",
    "seed": 13,
    "historique": 3,
    "futur": 25,
    "frameskip": 5,
    "regle_selection": "argmin(erreur_moyenne_un_pas_ancré) parmi V1/V2",
    "tolerance_inter_postes_relative": 1e-6,
}

CHIFFRES_PUBLIES = [
    "0.840789108872",   # violation ouverte, moyenne (variante retenue)
    "1.17440366745",    # violation ouverte, max
    "0.214657575488",   # violation ancrée (correction aval), moyenne
    "0.275687664747",   # violation ancrée, max
    "0.626131533384",   # delta d'ablation publié
    "V1_raw",           # variante retenue (règle pré-enregistrée)
    "APPROVED",         # verdict publié
]


def _sha256(chemin: Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as fh:
        for bloc in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _module_script():
    """Charge le module du script SANS l'exécuter (garde __main__, imports
    lourds uniquement dans les fonctions) — sûr hors-ligne."""
    spec = importlib.util.spec_from_file_location("wm_externe_lewm", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_certificat_canonique_byte_identique():
    """Le certificat archivé est byte-identique à l'artefact d'origine."""
    assert CERTIFICAT.exists(), f"certificat absent : {CERTIFICAT}"
    assert _sha256(CERTIFICAT) == SHA_CERTIFICAT


def test_recus_externes_immuables():
    """Les deux reçus R7 du run externe sont immuables (SHA-256 scellés)."""
    for chemin, sha_or in RECUS.items():
        assert chemin.exists(), f"reçu absent : {chemin}"
        assert _sha256(chemin) == sha_or, f"reçu altéré : {chemin.name}"


def test_parametres_scelles_r6_intacts():
    """Aucun paramètre R6 du script n'a bougé (re-scelle silencieuse = échec)."""
    module = _module_script()
    for cle, valeur in SCELLES_OR.items():
        assert cle in module.SCelle, f"clé scellée disparue : {cle}"
        assert module.SCelle[cle] == valeur, f"scellé modifié : {cle}"
    # variante V2 = z-score de la loi uniforme [-1,1] (std 1/√3)
    assert math.isclose(module.SCelle["variante_V2_std"], 1.0 / math.sqrt(3.0),
                        rel_tol=0, abs_tol=1e-15)


def test_chiffres_publies_verbatim_dans_recus():
    """Les chiffres publiés figurent verbatim dans CHAQUE reçu."""
    for chemin in RECUS:
        texte = chemin.read_text(encoding="utf-8")
        for chiffre in CHIFFRES_PUBLIES:
            assert chiffre in texte, f"{chiffre} absent de {chemin.name}"


def test_verrous_de_securite_du_script():
    """Verrous critiques présents dans le source : chargement STRICT,
    garde transformers v4, vérification SHA du checkpoint, no_grad."""
    source = SCRIPT.read_text(encoding="utf-8")
    assert "load_state_dict(sd, strict=True)" in source
    assert 'transformers.__version__.startswith("4.")' in source
    assert "sha256_poids" in source and "sha256_config" in source
    assert "torch.set_grad_enabled(False)" in source
    assert "requires_grad_(False)" in source


def test_recu_json_contient_scelles():
    """Le bloc JSON de chaque reçu contient le SHA du checkpoint (traçabilité)."""
    for chemin in RECUS:
        texte = chemin.read_text(encoding="utf-8")
        assert SCELLES_OR["sha256_poids"] in texte, chemin.name
        donnees = json.loads(texte.split("```json")[1].split("```")[0])
        assert donnees["verdict"] == "APPROVED"
        assert donnees["variante_retenue"] == "V1_raw"
        assert math.isclose(donnees["variantes"]["V1_raw"]["delta_moyenne"],
                            0.626131533384, rel_tol=1e-9)
