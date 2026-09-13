"""Topologie géologique appliquée au calcul.

Phase 2 : outillage topologique (source ratiss-topological-decoherence-engine).
Phase 1 : squelette uniquement.
"""


def brep_surface(surface_path: str) -> list[float]:
    """Langue n/m des faces d'une surface BREP.

    Retourne la description topologique de surface structurée en phase 2.
    En phase 1 : guerre de signature, aucune valeur calculée.
    """
    raise NotImplementedError("phase 2")


def compute_euler_characteristic(mesh: object) -> int:
    """Caractéristique d'Euler d'un maillage orienté (V - E + F).

    Nécessite une topologie complète (phase 2, source decoherence engine).
    """
    raise NotImplementedError("phase 2")


def validate_manifold(surface: object) -> tuple[bool, str]:
    """Vérifie qu'une surface est bien un manifold sans bord.

    (ok, raison). Pas de calcul en phase 1.
    """
    raise NotImplementedError("phase 2")