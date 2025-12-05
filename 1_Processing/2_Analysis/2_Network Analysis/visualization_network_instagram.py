from pathlib import Path
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
import numpy as np
from matplotlib.cm import get_cmap


# If you haven't loaded it yet:
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
output_csv = PROJECT_ROOT / "1_Processing" / "2_Analysis" / "2_Network Analysis"
edges_df = pd.read_csv(output_csv / "party_mentions_edges_instagram.csv")

# ------------------------------------------------------
# 0) Kanten vorbereiten
# ------------------------------------------------------
edges_plot = edges_df.copy()
edges_plot = edges_plot[edges_plot["weight"] >= 2]  # Schwelle nach Bedarf
edges_plot = edges_plot[edges_plot["source_party"] != edges_plot["target_party"]]

# gerichteter Graph
G = nx.from_pandas_edgelist(
    edges_plot,
    source="source_party",
    target="target_party",
    edge_attr="weight",
    create_using=nx.DiGraph(),
)

# ------------------------------------------------------
# 1) Knotengrössen nach Stärke
# ------------------------------------------------------
node_strength = {}
for node in G.nodes():
    out_w = sum(d["weight"] for _, _, d in G.out_edges(node, data=True))
    in_w  = sum(d["weight"] for _, _, d in G.in_edges(node, data=True))
    node_strength[node] = in_w + out_w

min_size, max_size = 700, 3500
if node_strength:
    min_s = min(node_strength.values())
    max_s = max(node_strength.values())
    if max_s == min_s:
        node_sizes = [2000 for _ in G.nodes()]
    else:
        node_sizes = [
            min_size + (max_size - min_size) * (node_strength[n] - min_s) / (max_s - min_s)
            for n in G.nodes()
        ]
else:
    node_sizes = []

# ------------------------------------------------------
# 2) Politische Ordnung im Kreis
# ------------------------------------------------------
political_order = [
    "JUSO",
    "SP",
    "Junge Grüne",
    "Grüne",
    "Junge GLP",
    "GLP",
    "Mitte",
    "Junge Mitte",
    "EVP",
    "Junge EVP",
    "FDP",
    "JF",
    "SVP",
    "JSVP",
]

ordered_nodes = [n for n in political_order if n in G.nodes()]
ordered_nodes += [n for n in G.nodes() if n not in ordered_nodes]

pos = {}
angles = {}
N = len(ordered_nodes)
for k, node in enumerate(ordered_nodes):
    angle = 2 * math.pi * k / N
    angles[node] = angle
    pos[node] = (math.cos(angle), math.sin(angle))

# ------------------------------------------------------
# 3) JEDER Knoten seine eigene Farbe
# ------------------------------------------------------
cmap = get_cmap("tab20", len(ordered_nodes))
node_color_map = {
    node: cmap(i) for i, node in enumerate(ordered_nodes)
}
node_colors = [node_color_map[n] for n in G.nodes()]

# ------------------------------------------------------
# 4) Kantenbreiten + Aufsplitten in single / mutual
# ------------------------------------------------------
weights_raw = [d["weight"] for _, _, d in G.edges(data=True)]
if weights_raw:
    min_w, max_w = min(weights_raw), max(weights_raw)
    if max_w == min_w:
        edge_widths = [2 for _ in weights_raw]
    else:
        edge_widths = [
            0.5 + 4.0 * (w - min_w) / (max_w - min_w)
            for w in weights_raw
        ]
else:
    edge_widths = []

edge_width_map = {
    (u, v): w for (u, v, _), w in zip(G.edges(data=True), edge_widths)
}

mutual_edges_pos = []   # Bogen nach aussen
mutual_edges_neg = []   # Bogen nach innen
single_edges = []
seen_mutual = set()

for u, v in G.edges():
    if G.has_edge(v, u) and (v, u) not in seen_mutual:
        mutual_edges_pos.append((u, v))
        mutual_edges_neg.append((v, u))
        seen_mutual.add((u, v))
        seen_mutual.add((v, u))
    elif (u, v) not in seen_mutual:
        single_edges.append((u, v))

single_widths   = [edge_width_map[(u, v)] for (u, v) in single_edges]
mut_pos_widths  = [edge_width_map[(u, v)] for (u, v) in mutual_edges_pos]
mut_neg_widths  = [edge_width_map[(u, v)] for (u, v) in mutual_edges_neg]

# Kantenfarben = Farbe der Quellpartei
edge_colors_single  = [node_color_map[u] for (u, v) in single_edges]
edge_colors_mut_pos = [node_color_map[u] for (u, v) in mutual_edges_pos]
edge_colors_mut_neg = [node_color_map[u] for (u, v) in mutual_edges_neg]

# ------------------------------------------------------
# 5) Edge-Labels (jede Richtung separat)
# ------------------------------------------------------
label_threshold = 3  # nur Labels ab x Posts

edge_labels_single = {
    (u, v): d["weight"]
    for u, v, d in G.edges(data=True)
    if (u, v) in single_edges and d["weight"] >= label_threshold
}
edge_labels_mut_pos = {
    (u, v): d["weight"]
    for u, v, d in G.edges(data=True)
    if (u, v) in mutual_edges_pos and d["weight"] >= label_threshold
}
edge_labels_mut_neg = {
    (u, v): d["weight"]
    for u, v, d in G.edges(data=True)
    if (u, v) in mutual_edges_neg and d["weight"] >= label_threshold
}

bbox_style = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8)

# ------------------------------------------------------
# 6) Plot
# ------------------------------------------------------
plt.figure(figsize=(9, 9))

# Knoten
nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=node_colors,
    alpha=0.95,
)

# Einfache gerichtete Kanten
nx.draw_networkx_edges(
    G, pos,
    edgelist=single_edges,
    width=single_widths,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=20,
    connectionstyle="arc3,rad=0.0",
    edge_color=edge_colors_single,
    alpha=0.9,
)

# Gegenseitige Kanten – zwei Bögen
nx.draw_networkx_edges(
    G, pos,
    edgelist=mutual_edges_pos,
    width=mut_pos_widths,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=20,
    connectionstyle="arc3,rad=0.30",
    edge_color=edge_colors_mut_pos,
    alpha=0.95,
)
nx.draw_networkx_edges(
    G, pos,
    edgelist=mutual_edges_neg,
    width=mut_neg_widths,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=20,
    connectionstyle="arc3,rad=-0.30",
    edge_color=edge_colors_mut_neg,
    alpha=0.95,
)

# Knotenlabels
nx.draw_networkx_labels(
    G, pos,
    font_size=10,
    font_weight="bold",
)

# Edge-Labels (mit weissem Hintergrund)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels_single,
    font_size=8,
    label_pos=0.5,
    bbox=bbox_style,
)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels_mut_pos,
    font_size=8,
    label_pos=0.35,
    bbox=bbox_style,
)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels_mut_neg,
    font_size=8,
    label_pos=0.65,
    bbox=bbox_style,
)

# Optional: grobe Block-Beschriftung am Kreis behalten
block_definitions = {
    "links / linksgruen": {"JUSO", "SP", "Junge Grüne", "Grüne"},
    "gruenliberal": {"Junge GLP", "GLP"},
    "Mitte / EVP": {"Mitte", "Junge Mitte", "EVP", "Junge EVP"},
    "buergerlich / rechts": {"FDP", "JF", "SVP", "JSVP"},
}
radius_label = 1.3
for label, nodes_block in block_definitions.items():
    angles_block = [angles[n] for n in nodes_block if n in angles]
    if not angles_block:
        continue
    mean_angle = float(np.angle(np.mean(np.exp(1j * np.array(angles_block)))))
    x = radius_label * math.cos(mean_angle)
    y = radius_label * math.sin(mean_angle)
    plt.text(
        x, y, label,
        ha="center", va="center",
        fontsize=10, fontweight="bold",
    )

# Legende (nur Regel erklären)
legend_elements = [
    Line2D([0], [0], marker="o", color="w",
           label="Partei (Farbe)", markerfacecolor="grey", markersize=8),
    Line2D([0], [0], color="grey", lw=2,
           label="Pfeilfarbe = Quellpartei"),
]
plt.legend(handles=legend_elements, loc="upper left")

plt.title("Netzwerk der Parteierwähnungen\nKreislayout, jede Partei eigene Farbe\nPfeilfarbe = Quelle, Richtung = Quellpartei → Zielpartei")
plt.axis("off")
plt.tight_layout()
plt.show()