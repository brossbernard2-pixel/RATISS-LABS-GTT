"""Journal des déviations des prévisions (R5 — chaîné).

Phase 5 (méthode R5 ; relais Rouge). Réutilise ratiss.journal du JUGE :
chaîne SHA-256 (entrée N contient le hash de l'entrée N−1), une seule loi.
Aucune déviation n'est supprimée ; toute altération casse la chaîne.
"""

from __future__ import annotations

from ratiss.journal import append_entry, read_chain, verify_chain

AUTHOR_DEFAUT = "gtt-forecast"


def append_deviation(path: str, text: str, params: dict) -> None:
    """Ajoute une déviation au journal chaîné (juge : ratiss.journal).

    params : {"author"} optionnel (défaut : gtt-forecast). Le texte doit
    être non vide ; l'entrée est horodatée UTC par le juge.
    """
    if not text or not text.strip():
        raise ValueError("texte de déviation non vide requis")
    append_entry(path, params.get("author", AUTHOR_DEFAUT), text)


def verify_journal(path: str) -> bool:
    """Vérifie l'intégrité de la chaîne du journal (juge)."""
    return verify_chain(path)


def deviations(path: str) -> list:
    """Liste les entrées du journal (lecture seule, chaîne vérifiée).

    Lève ValueError si la chaîne est cassée — on ne lit pas un journal
    altéré comme s'il était sain.
    """
    if not verify_chain(path):
        raise ValueError("chaîne du journal cassée — déviation à signaler")
    return read_chain(path)


__all__ = ["append_deviation", "verify_journal", "deviations",
           "AUTHOR_DEFAUT"]
