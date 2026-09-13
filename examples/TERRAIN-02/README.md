# TERRAIN-02 — SIR discret (invariant exact)

Source d'inspiration : RATISS-BIOLAB (github.com/jonathansearch/RATISS-BIOLAB,
sha `7b9455ba61c94aaecd1610fb67a890c396c0341d`) — réécriture provenancée,
aucune copie de code.

Modèle : SIR discret (β=0.3, γ=0.1, N=1000, 30 pas), S+I+R conservé
EXACTEMENT (transferts symétriques) + réseau de contacts cycle4
(Betti analytique (1,1)). Aucune RNG : formule pure, déterministe.

    python3 generate.py    # écrit sir.json
    python3 run_core.py    # écrit expected.json (mesures core)

Mesures : violation de conservation (~0), perturbation ε=1e-6 détectée
(violation ≈ ε), Betti cycle4, score de cohérence.
