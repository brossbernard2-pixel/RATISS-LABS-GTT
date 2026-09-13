"""Thermodynamique de l'information topologique.

Phase 3 : calculs de température topologique et théorie de l'information.
Phase 1 : squelette uniquement.
"""


def topological_temperature(structure: object, params: dict) -> float:
    """Température topologique d'une structure.

    Entrée : représentation topologique calculée en phase 2 + paramètres
    scellés (R5). Non implémenté en phase 1.
    """
    raise NotImplementedError("phase 3")


def information_entropy(topological_state: object) -> float:
    """Entropie informationnelle d'un état topologique.

    La valeur calculée n'existera qu'avec la couche core complète.
    """
    raise NotImplementedError("phase 3")


def odv_temperature_landscape(region: object, params: dict) -> dict:
    """Paysage de température ODV (région, params) -> résultats.

    Squelette : aucune valeur publiée avant calcul effectif (R4).
    """
    raise NotImplementedError("phase 3")