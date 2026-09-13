"""Chargeur PDB — colonnes standards ATOM/HETATM.

Phase 6 (méthode neuve ; relais Rouge). Analyseur minimal au format PDB
(colonnes fixes du wwPDB), stdlib seule, déterministe. Aucun réseau :
le texte vient d'un fichier local ou d'une chaîne fournie par l'appelant.
"""

from __future__ import annotations


def parse_pdb(source: object, params: dict) -> list:
    """Analyse un PDB (chemin ou texte) → liste d'atomes dict.

    Colonnes wwPDB : nom d'atome 13-16, resname 18-20, chaîne 22,
    resseq 23-26, x/y/z 31-38/39-46/47-54. params : {"records": [...]}
    optionnel (défaut ATOM+HETATM). Lignes malformées ignorées et
    comptées dans le rapport (voir parse_pdb_report).
    """
    records = tuple(params.get("records", ("ATOM", "HETATM")))
    if isinstance(source, str) and ("\n" in source or source.startswith("ATOM")
                                    or source.startswith("HETATM")):
        texte = source
    else:
        with open(source, encoding="utf-8") as fh:
            texte = fh.read()
    atomes = []
    for ligne in texte.splitlines():
        if not ligne.startswith(records):
            continue
        try:
            atomes.append({
                "name": ligne[12:16].strip(),
                "resname": ligne[17:20].strip(),
                "chain": ligne[21:22].strip(),
                "resseq": int(ligne[22:26]),
                "xyz": [float(ligne[30:38]), float(ligne[38:46]),
                        float(ligne[46:54])],
            })
        except (ValueError, IndexError):
            continue  # ligne malformée : ignorée, comptée au rapport
    return atomes


def parse_pdb_report(source: object, params: dict) -> dict:
    """parse_pdb + rapport honnête : {"n_atomes", "n_lignes", "n_ignores"}."""
    atomes = parse_pdb(source, params)
    if isinstance(source, str) and ("\n" in source or source.startswith("ATOM")
                                    or source.startswith("HETATM")):
        lignes = source.splitlines()
    else:
        with open(source, encoding="utf-8") as fh:
            lignes = fh.read().splitlines()
    records = tuple(params.get("records", ("ATOM", "HETATM")))
    enregistrements = [l for l in lignes if l.startswith(records)]
    return {"n_atomes": len(atomes), "n_lignes": len(lignes),
            "n_ignores": len(enregistrements) - len(atomes)}


__all__ = ["parse_pdb", "parse_pdb_report"]
