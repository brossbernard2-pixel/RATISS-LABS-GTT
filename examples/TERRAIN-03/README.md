# TERRAIN-03 — chaleur 1D, masses et stabilité

Source d'inspiration : RATISS-HPC (github.com/jonathansearch/RATISS-HPC,
sha `5aae7f4f8929af4ea8a49e90dfaca100ae901e4f`) — réécriture provenancée,
aucune copie de code.

Modèle : diffusion 1D (n=21, dx=1, D=1) en volumes finis à bords de
Neumann miroir — la masse totale Σu est conservée exactement
(télescopage des fluxes), STABILITÉ OU PAS. Deux sondes : r=0.4 (stable,
amplitude décroît) et r=0.6 (instable, amplitude explose). Les deux
sondes reçoivent la même graine de von Neumann ε·(−1)^i (ε=1e-3,
documentée — tout schéma réel contient l'équivalent en arrondi) : sans
elle, le mode de Nyquist met des dizaines de pas à se voir. Bosse
gaussienne en formule pure : aucune RNG, déterministe.

    python3 generate.py    # écrit heat.json
    python3 run_core.py    # écrit expected.json (mesures core)

L'audit doit VOIR les deux : masse conservée dans les deux sondes,
amplitude conforme à la théorie de la stabilité (critère r ≤ 0.5).
