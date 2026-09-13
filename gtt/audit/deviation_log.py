"""Journal des déviations du dépôt GTT (R5).

Phase 1 : squelette. Le format chaîné est celui de ratiss.journal (juge) ;
toute déviation servira via cet appel.
"""


def append(path: str, text: str, params: dict) -> None:
    """Ajoute une entrée au journal de déviations du dépôt GTT."""
    raise NotImplementedError("phase 2")


def verify(path: str, params: dict) -> bool:
    """Vérifie la chaîne du journal (bool). Squelette."""
    raise NotImplementedError("phase 2")