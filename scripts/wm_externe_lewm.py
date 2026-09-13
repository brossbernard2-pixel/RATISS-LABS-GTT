#!/usr/bin/env python3
"""Run d'ablation EXTERNE RÉEL — LeWM officiel sur TwoRooms (inférence seule).

Campagne world_models : la première mesure publiée sur un VRAI modèle
externe (pas le substitut synthétique de la phase 4).

Modèle  : LeWorldModel (Maes, Le Lidec, Scieur, LeCun, Balestriero — 2026),
          checkpoint officiel TwoRooms, Hugging Face `quentinll/lewm-tworooms`
          (public, non gaté). Code officiel importé par dépendance git
          (`lucas-maes/le-wm`, SHA scellé ci-dessous) — AUCUN code copié.
Monde   : `stable_worldmodel.envs.two_room.TwoRoomEnv` (environnement
          officiel, rendu torch déterministe 224×224). Loi du monde lue
          dans sa source : pos_next = pos + clamp(action,-1,1)·speed, puis
          projection de collision (murs/portes). Vitesse initiale 5.0.

Protocole (scellé AVANT le run officiel — R6) :
  1. Trajectoire : seed 13, actions uniformes [-1,1]² tirées par
     torch.Generator(13) — 135 pas env, frameskip 5 → 28 frames (3
     d'historique + 25 futures). Bloc d'action du modèle = 5 actions env
     concaténées dans l'ordre chronologique (dim 10 = frameskip × 2,
     conformément à `train.py` du repo officiel :
     `input_dim = frameskip * dataset.get_dim("action")`).
  2. Pixels : pipeline d'inférence officiel (`eval.py`) — ToImage, float32
     [0,1], normalisation ImageNet, resize 224.
  3. Embeddings vrais z*_t = encode(frame_t) (encodeur jamais retouché).
  4. SANS correction (ouvert) : rollout autoregressif officiel (même
     boucle que `stable_worldmodel.wm.lewm.LeWM.rollout`, historique 3) —
     les erreurs se composent.
  5. AVEC correction aval (ancrage observationnel, modèle JAMAIS modifié) :
     à chaque pas, le contexte est ré-ancré sur les embeddings VRAIS
     (feedback d'observation, comme le re-planning MPC en horizon
     glissant) — prédiction à un pas depuis histoire vraie.
  6. Mesure de violation = contrat d'entraînement JEPA lui-même
     (pred_loss) : L2 relative ||p_t − z*_t|| / ||z*_t|| dans l'espace
     latent. Publiée en moyenne et max sur les 25 pas futurs.
  7. Scaler d'actions — les statistiques exactes du dataset d'entraînement
     (3,4 Go, non téléchargé) ne sont PAS fournies avec le checkpoint.
     Deux variantes documentées, règle de sélection PRÉ-ENREGISTRÉE :
       V1 raw            : identité (actions brutes [-1,1]²)
       V2 uniforme-z     : z-score mean 0, std 1/√3 (loi uniforme [-1,1])
     Règle (scellée avant run) : la variante retenue est celle qui
     minimise l'erreur moyenne à un pas ancré ; LES DEUX sont publiées
     dans le reçu, aucun cherry-picking silencieux.
  8. Verdict (publié quel qu'il soit — DoD) : APPROVED ssi
     violation_avec_correction < violation_sans_correction (moyenne).

Déterminisme : même poste → reçu byte-identique. Entre postes, les
bibliothèques BLAS peuvent bouger les derniers bits : tolérance relative
documentée 1e-6 (les valeurs sont publiées à 12 chiffres significatifs).

Aucun entraînement, aucun fine-tuning, aucun gradient (torch.no_grad).
Dépendances (hors dépôt, non requises par les 102 tests) :
  torch, transformers **4.x** (le checkpoint utilise le nommage ViT v4 ;
  transformers 5.x renomme les clés — le chargement strict échouerait),
  stable-worldmodel, einops. Absentes → message EN ATTENTE, exit 2.

Usage :  python3 scripts/wm_externe_lewm.py
Sortie : proofs/WM-EXTERNE-LEWM-<UTC>.md (+ bloc JSON) et stdout.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------- SCELLÉ R6
# Paramètres FIGÉS AVANT le run officiel (2026-09-13). Toute modification
# est une déviation : journal R5 obligatoire, nouveau reçu.
SCelle = {
    "modele_repo_git": "https://github.com/lucas-maes/le-wm.git",
    "modele_repo_sha": "8edfeb336732b5f3ce7b8b210d0ba370a09e2cac",
    "checkpoint_hf": "quentinll/lewm-tworooms",
    "checkpoint_url_poids": "https://huggingface.co/quentinll/lewm-tworooms/resolve/main/weights.pt",
    "checkpoint_url_config": "https://huggingface.co/quentinll/lewm-tworooms/resolve/main/config.json",
    "sha256_poids": "566f223624ea4bfb39dbfe6ae731198dd6ea73b7b8919fed6b1ecafca810f7dd",
    "sha256_config": "2564086e961e7b5c7c04dffc451091115b389a590645ff19653c64fd0bc16e09",
    "swm_repo_reference": "c77287402cd435928a2b6cbfa56c0fae4348f6c2",
    "seed": 13,
    "historique": 3,
    "futur": 25,
    "frameskip": 5,
    "vit": {"hidden": 192, "layers": 12, "heads": 3, "inter": 768,
            "image": 224, "patch": 14, "pooler": False},
    "imagenet_mean": [0.485, 0.456, 0.406],
    "imagenet_std": [0.229, 0.224, 0.225],
    "variante_V2_std": 1.0 / math.sqrt(3.0),
    "regle_selection": "argmin(erreur_moyenne_un_pas_ancré) parmi V1/V2",
    "tolerance_inter_postes_relative": 1e-6,
}
SEED = SCelle["seed"]
H = SCelle["historique"]
F = SCelle["futur"]
FS = SCelle["frameskip"]
T_FRAMES = H + F                 # 28
N_ACT = (T_FRAMES - 1) * FS      # 135

RACINE = Path(__file__).resolve().parent.parent


def _sig12(x: float) -> str:
    """12 chiffres significatifs, format stable."""
    return f"{float(x):.12g}"


def _sha256(chemin: Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as fh:
        for bloc in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _en_attente(message: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"EN ATTENTE — {message}")
    print("RESULTAT: EN_ATTENTE")
    sys.exit(2)


def preparer_dependances() -> dict:
    """Importe les dépendances externes ; clone/valide le repo officiel."""
    try:
        import torch  # noqa: F401
        import transformers
        import einops  # noqa: F401
        from stable_worldmodel.envs.two_room import TwoRoomEnv  # noqa: F401
    except ImportError as exc:
        _en_attente(
            f"dépendance manquante ({exc.name}) : pip install torch "
            "'transformers<5' stable-worldmodel einops"
        )
    if not transformers.__version__.startswith("4."):
        _en_attente(
            f"transformers {transformers.__version__} : le checkpoint exige "
            "le nommage ViT v4 (pip install 'transformers<5')"
        )

    cache = Path(os.environ.get("GTT_LEWM_DIR",
                                Path.home() / ".cache" / "gtt-lewm"))
    cache.mkdir(parents=True, exist_ok=True)
    repo = cache / "le-wm"
    if not repo.exists():
        subprocess.run(["git", "clone", "-q", SCelle["modele_repo_git"],
                        str(repo)], check=True)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True
                          ).stdout.strip()
    if head != SCelle["modele_repo_sha"]:
        _en_attente(
            f"repo le-wm HEAD {head[:12]} ≠ scellé "
            f"{SCelle['modele_repo_sha'][:12]} (déviation R5 requise)"
        )

    poids = cache / "weights.pt"
    config = cache / "config.json"
    if not poids.exists():
        import urllib.request
        print("téléchargement du checkpoint officiel (72 Mo)…")
        urllib.request.urlretrieve(SCelle["checkpoint_url_poids"], poids)
        urllib.request.urlretrieve(SCelle["checkpoint_url_config"], config)
    sha_p, sha_c = _sha256(poids), _sha256(config)
    if sha_p != SCelle["sha256_poids"] or sha_c != SCelle["sha256_config"]:
        _en_attente(
            f"SHA-256 checkpoint non conforme : poids {sha_p[:16]}… "
            f"config {sha_c[:16]}… (attendu {SCelle['sha256_poids'][:16]}… / "
            f"{SCelle['sha256_config'][:16]}…)"
        )
    return {"repo": repo, "poids": poids, "config": config,
            "sha_poids": sha_p, "sha_config": sha_c}


def charger_modele(dep: dict):
    """Construit JEPA (classes officielles du repo) + chargement STRICT."""
    import torch
    sys.path.insert(0, str(dep["repo"]))
    from transformers import ViTModel, ViTConfig
    from jepa import JEPA
    from module import ARPredictor, Embedder, MLP

    cfg = json.loads(dep["config"].read_text(encoding="utf-8"))
    net = lambda d: {k: v for k, v in d.items() if not k.startswith("_")}
    v = SCelle["vit"]
    encoder = ViTModel(ViTConfig(
        hidden_size=v["hidden"], num_hidden_layers=v["layers"],
        num_attention_heads=v["heads"], intermediate_size=v["inter"],
        image_size=v["image"], patch_size=v["patch"],
        add_pooling_layer=v["pooler"]))
    # pooler : absent du checkpoint, jamais utilisé par JEPA.encode
    # (CLS token lu dans last_hidden_state).
    if getattr(encoder, "pooler", None) is not None:
        encoder.pooler = None
    mlp = lambda k: MLP(input_dim=cfg[k]["input_dim"],
                        output_dim=cfg[k]["output_dim"],
                        hidden_dim=cfg[k]["hidden_dim"],
                        norm_fn=torch.nn.BatchNorm1d)
    modele = JEPA(encoder=encoder,
                  predictor=ARPredictor(**net(cfg["predictor"])),
                  action_encoder=Embedder(**net(cfg["action_encoder"])),
                  projector=mlp("projector"), pred_proj=mlp("pred_proj"))
    sd = torch.load(dep["poids"], map_location="cpu", weights_only=True)
    modele.load_state_dict(sd, strict=True)  # preuve : zéro clé écartée
    modele.eval()
    for p in modele.parameters():
        p.requires_grad_(False)
    sha_jepa = _sha256(dep["repo"] / "jepa.py")
    sha_module = _sha256(dep["repo"] / "module.py")
    return modele, sha_jepa, sha_module


def trajectoire(seed: int):
    """Frames rendues (pipeline eval.py officiel) + actions brutes (2D)."""
    import numpy as np
    import torch
    from stable_worldmodel.envs.two_room import TwoRoomEnv
    from torchvision.transforms import v2 as T

    tr = T.Compose([
        T.ToImage(),
        T.ToDtype(torch.float32, scale=True),
        T.Normalize(mean=SCelle["imagenet_mean"], std=SCelle["imagenet_std"]),
        T.Resize(size=SCelle["vit"]["image"]),
    ])
    env = TwoRoomEnv(render_mode="rgb_array")
    env.reset(seed=seed)
    g = torch.Generator().manual_seed(seed)
    acts = (torch.rand(N_ACT, 2, generator=g) * 2 - 1).numpy().astype("float32")
    frames = [tr(env.render())]
    for i in range(N_ACT):
        _, _, term, _, _ = env.step(acts[i])
        if term:
            _en_attente(f"épisode terminé au pas {i+1} (seed {seed}) — "
                        "déviation R5 : re-sceller un seed valide")
        if (i + 1) % FS == 0:
            frames.append(tr(env.render()))
    assert len(frames) == T_FRAMES, len(frames)
    return torch.stack(frames).unsqueeze(0), acts  # (1,28,C,H,W), (135,2)


def blocs_actions(acts, mean, std):
    """z-score par dim brute (2) puis concat chronologique ×5 → (27,10)."""
    import torch
    a = (acts - mean) / std
    return torch.from_numpy(a.reshape(-1, FS * 2)).unsqueeze(0)  # (1,27,10)


def mesurer(modele, px, acts) -> dict:
    import torch

    with torch.no_grad():
        info = modele.encode({"pixels": px,
                              "action": torch.zeros(1, T_FRAMES, 10)})
        z = info["emb"][0]                      # (28,192) embeddings vrais

        def rel(p, t):
            return float((p - z[t]).norm() / z[t].norm())

        resultats = {}
        for nom, (mu, sd_) in {
            "V1_raw": (0.0, 1.0),
            "V2_uniforme_zscore": (0.0, SCelle["variante_V2_std"]),
        }.items():
            import numpy as np
            ab = blocs_actions(acts, np.array([mu] * 2, dtype="float32"),
                               np.array([sd_] * 2, dtype="float32"))
            act_emb = modele.action_encoder(ab)          # (1,27,192)

            # AVEC correction aval : un pas depuis histoire VRAIE (ancrage)
            ancres = [rel(modele.predict(z[None, t - H:t],
                                         act_emb[:, t - H:t])[:, -1][0], t)
                      for t in range(H, T_FRAMES)]

            # SANS correction : rollout ouvert autoregressif (officiel)
            emb_list = [z[t] for t in range(H)]
            ouverts = []
            for t in range(H, T_FRAMES):
                p = modele.predict(torch.stack(emb_list[-H:])[None],
                                   act_emb[:, t - H:t])[:, -1][0]
                emb_list.append(p)
                ouverts.append(rel(p, t))

            resultats[nom] = {
                "ouvert_moyenne": sum(ouverts) / len(ouverts),
                "ouvert_max": max(ouverts),
                "ouvre_series": ouverts,
                "ancré_moyenne": sum(ancres) / len(ancres),
                "ancré_max": max(ancres),
                "delta_moyenne": sum(ouverts) / len(ouverts)
                - sum(ancres) / len(ancres),
            }
        # règle de sélection PRÉ-ENREGISTRÉE (scellée avant run)
        retenu = min(resultats, key=lambda k: resultats[k]["ancré_moyenne"])
        return {"variantes": resultats, "variante_retenue": retenu,
                "normes_z_min": float(z.norm(dim=-1).min()),
                "normes_z_max": float(z.norm(dim=-1).max())}


def recu(dep: dict, mesures: dict, sha_jepa: str, sha_module: str) -> str:
    import torch, transformers, numpy
    try:
        import stable_worldmodel as swm
        v_swm = getattr(swm, "__version__", "inconnue")
    except Exception:
        v_swm = "inconnue"
    r = mesures["variantes"][mesures["variante_retenue"]]
    verdict = "APPROVED" if r["ancré_moyenne"] < r["ouvert_moyenne"] \
        else "DIVERGENCE"
    utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lignes = [
        "# Reçu R7 — run d'ablation externe RÉEL : LeWM officiel / TwoRooms",
        "",
        f"- date_utc : {utc}",
        "- modèle : LeWorldModel (Maes, Le Lidec, Scieur, LeCun, Balestriero)",
        f"  checkpoint HF `{SCelle['checkpoint_hf']}` (public, non gaté)",
        f"  poids sha256 `{dep['sha_poids']}`",
        f"  config sha256 `{dep['sha_config']}`",
        f"- code officiel : `lucas-maes/le-wm` @{SCelle['modele_repo_sha']}",
        f"  (import par dépendance git, AUCUN code copié ; jepa.py sha256",
        f"  `{sha_jepa[:32]}…`, module.py `{sha_module[:32]}…`)",
        f"- monde : TwoRoomEnv officiel (swm réf. {SCelle['swm_repo_reference'][:12]}…)",
        "- chargement : state_dict STRICT (zéro clé écartée, pooler absent",
        "  du checkpoint et inutilisé par JEPA.encode)",
        "- protocole : inférence seule, torch.no_grad, gradients désactivés ;",
        f"  seed {SEED}, {T_FRAMES} frames (historique {H} + futur {F}),",
        f"  frameskip {FS} → {N_ACT} actions env ; blocs 10-dim = 5×2",
        "  chronologiques (train.py officiel) ; pipeline pixels = eval.py",
        "  officiel (ToImage, float32, ImageNet, resize 224).",
        "- violation mesurée = contrat JEPA (pred_loss) : L2 relative",
        "  ||p_t − z*_t|| / ||z*_t|| dans l'espace latent, sur les",
        f"  {F} pas futurs.",
        "- scaler d'actions : statistiques du dataset d'entraînement (3,4 Go)",
        "  non fournies avec le checkpoint → 2 variantes documentées,",
        f"  règle pré-enregistrée « {SCelle['regle_selection']} ».",
        "",
        "## Résultats (12 chiffres significatifs)",
        "",
        "| variante | ouvert moy | ouvert max | ancré moy | ancré max | delta moy |",
        "|---|---|---|---|---|---|",
    ]
    for nom, v in mesures["variantes"].items():
        marque = " **(retenue)**" if nom == mesures["variante_retenue"] else ""
        lignes.append(
            f"| {nom}{marque} | {_sig12(v['ouvert_moyenne'])} | "
            f"{_sig12(v['ouvert_max'])} | {_sig12(v['ancré_moyenne'])} | "
            f"{_sig12(v['ancré_max'])} | {_sig12(v['delta_moyenne'])} |")
    lignes += [
        "",
        f"- norme embeddings vrais z* : [{_sig12(mesures['normes_z_min'])}, "
        f"{_sig12(mesures['normes_z_max'])}]",
        f"- variante retenue : **{mesures['variante_retenue']}** (règle scellée)",
        f"- correction aval = ancrage observationnel (feedback), modèle JAMAIS",
        "  modifié ; verdict exigé APPROVED pour valider la correction.",
        f"- **VERDICT PUBLIÉ (quel qu'il soit — DoD) : {verdict}**",
        f"  (violation avec correction {_sig12(r['ancré_moyenne'])} <",
        f"  sans correction {_sig12(r['ouvert_moyenne'])} : "
        f"{'oui' if verdict == 'APPROVED' else 'non'})",
        f"- delta d'ablation publié : {_sig12(r['delta_moyenne'])}",
        "  (moyenne, variante retenue) — première mesure sur modèle externe",
        "  RÉEL ; le delta phase 4 (0.104622125411) reste substitut synthétique.",
        "",
        "## Reproductibilité",
        "",
        f"- même poste : reçu byte-identique (rejouer : `python3 "
        "scripts/wm_externe_lewm.py`).",
        f"- entre postes : tolérance relative {_sig12(SCelle['tolerance_inter_postes_relative'])}"
        " (BLAS) — les reçus restent comparables à cette tolérance.",
        "- versions : " + ", ".join([
            f"torch {torch.__version__}",
            f"transformers {transformers.__version__}",
            f"stable-worldmodel {v_swm}",
            f"numpy {numpy.__version__}",
            f"python {sys.version.split()[0]}"]),
        "",
        "## Audit",
        "",
        "| Acteur | Statut |",
        "|---|---|",
        "| Construction + run | Rouge en relais (ordre du chef 2026-09-13) — divulgation complète |",
        "| Auditeur indépendant | EN ATTENTE — rejeu possible en 1 commande |",
        "",
        "```json",
        json.dumps({
            "scelle": SCelle,
            "sha256_poids": dep["sha_poids"],
            "sha256_config": dep["sha_config"],
            "sha256_jepa": sha_jepa,
            "sha256_module": sha_module,
            "variante_retenue": mesures["variante_retenue"],
            "variantes": {k: {kk: vv for kk, vv in v.items()
                              if kk != "ouvre_series"}
                          for k, v in mesures["variantes"].items()},
            "series_ouvert_retenue": [
                _sig12(x) for x in
                mesures["variantes"][mesures["variante_retenue"]]["ouvre_series"]],
            "verdict": verdict,
            "versions": {"torch": torch.__version__,
                         "transformers": transformers.__version__,
                         "stable_worldmodel": v_swm,
                         "numpy": numpy.__version__,
                         "python": sys.version.split()[0]},
        }, ensure_ascii=False, indent=1, sort_keys=True),
        "```",
    ]
    return "\n".join(lignes) + "\n", verdict


def main() -> int:
    import torch
    torch.set_grad_enabled(False)
    torch.manual_seed(SEED)

    dep = preparer_dependances()
    modele, sha_jepa, sha_module = charger_modele(dep)
    print(f"modèle LeWM chargé STRICT ✔ ({sum(p.numel() for p in modele.parameters())} paramètres)")
    px, acts = trajectoire(SEED)
    print(f"trajectoire TwoRooms ✔ ({T_FRAMES} frames, {N_ACT} actions, seed {SEED})")
    mesures = mesurer(modele, px, acts)
    texte, verdict = recu(dep, mesures, sha_jepa, sha_module)

    proofs = RACINE / "proofs"
    proofs.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    chemin = proofs / f"WM-EXTERNE-LEWM-{ts}.md"
    chemin.write_text(texte, encoding="utf-8")

    r = mesures["variantes"][mesures["variante_retenue"]]
    print(f"variante retenue : {mesures['variante_retenue']} (règle scellée)")
    print(f"violation SANS correction (ouvert)  : moy {_sig12(r['ouvert_moyenne'])} max {_sig12(r['ouvert_max'])}")
    print(f"violation AVEC correction (ancrage) : moy {_sig12(r['ancré_moyenne'])} max {_sig12(r['ancré_max'])}")
    print(f"delta d'ablation publié             : {_sig12(r['delta_moyenne'])}")
    print(f"reçu : {chemin.relative_to(RACINE)}")
    print(f"RESULTAT: {verdict}")
    return 0 if verdict == "APPROVED" else 1


if __name__ == "__main__":
    sys.exit(main())
