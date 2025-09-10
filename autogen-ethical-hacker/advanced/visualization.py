
"""
Visualization Hooks
Basic attack graph generation using networkx and matplotlib.
"""

import networkx as nx
import matplotlib.pyplot as plt
import os

def generate_visualization(data):
    """
    Generate and save a simple attack graph from data.
    data: dict with 'nodes' and 'edges' (optional, demo if missing)
    """
    print(f"[visualization] Generating visualization for: {data}")
    G = nx.DiGraph()
    # Demo data if none provided
    if not data or 'nodes' not in data:
        nodes = ['Attacker', 'Phishing', 'User', 'Internal Server', 'Database']
        edges = [('Attacker', 'Phishing'), ('Phishing', 'User'), ('User', 'Internal Server'), ('Internal Server', 'Database')]
    else:
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    plt.figure(figsize=(8, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, arrows=True)
    out_path = os.path.abspath('attack_graph.png')
    plt.title('Attack Graph')
    plt.savefig(out_path)
    plt.close()
    print(f"[visualization] Attack graph saved to {out_path}")
    return out_path
