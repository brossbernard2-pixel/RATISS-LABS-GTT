"""Graphe de preuves — texte DOT déterministe.

Phase 6 (méthode neuve ; relais Rouge). DOT (Graphviz) en TEXTE : aucun
binaire requis, aucune exécution — le graphe se lit, se diff et se scelle
comme n'importe quel artefact. Les arêtes doivent référencer des nœuds
déclarés (validation stricte). Déterministe : tri lexicographique.
"""

from __future__ import annotations


def graph_to_dot(nodes: list, edges: list, params: dict) -> str:
    """Graphe de dépendances de preuves en DOT.

    nodes : [{"id", "label"?, "statut"?}] — statut ∈ {"prouve",
    "en_attente", "divergence"} (couleurs fixées). edges : [{"de", "vers",
    "label"?}]. params : {"name"} optionnel. Toute arête vers un nœud
    inconnu → ValueError (un graphe de preuves ne référence pas du vent).
    """
    ids = sorted({str(n["id"]) for n in nodes})
    if len(ids) != len(nodes):
        raise ValueError("nœuds en double")
    couleurs = {"prouve": "#27ae60", "en_attente": "#7f8c8d",
                "divergence": "#c0392b"}
    name = params.get("name", "preuves_gtt")
    lines = [f'digraph {name} {{', '  rankdir=LR;',
             '  node [shape=box, style=filled, fontname="monospace"];']
    for n in sorted(nodes, key=lambda n: str(n["id"])):
        statut = n.get("statut", "en_attente")
        if statut not in couleurs:
            raise ValueError(f"statut inconnu : {statut}")
        label = str(n.get("label", n["id"])).replace('"', "'")
        lines.append(f'  "{n["id"]}" [label="{label}", '
                     f'fillcolor="{couleurs[statut]}", fontcolor="#ffffff"];')
    for e in sorted(edges, key=lambda e: (str(e["de"]), str(e["vers"]))):
        if str(e["de"]) not in ids or str(e["vers"]) not in ids:
            raise ValueError(
                f"arête vers nœud inconnu : {e['de']} -> {e['vers']}")
        lab = f' [label="{e["label"]}"]' if e.get("label") else ""
        lines.append(f'  "{e["de"]}" -> "{e["vers"]}"{lab};')
    lines.append("}")
    return "\n".join(lines) + "\n"


__all__ = ["graph_to_dot"]
