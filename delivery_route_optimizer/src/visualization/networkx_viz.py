"""
NetworkX-based graph visualization.
"""

import matplotlib.pyplot as plt
import networkx as nx


class NetworkXVisualizer:
    """Visualize TSP as graph using NetworkX."""

    @staticmethod
    def plot_graph(cities, tour, distance_matrix, title="TSP Graph"):
        """
        Visualize TSP solution as a graph.

        Args:
            cities: List of City objects
            tour: Ordered list of city indices
            distance_matrix: Distance matrix
            title: Plot title
        """
        G = nx.Graph()

        # Add nodes with positions
        pos = {}
        for i, city in enumerate(cities):
            G.add_node(i, name=city.name)
            pos[i] = (city.x, city.y)

        # Add edges for the tour
        edge_labels = {}
        for i in range(len(tour)):
            current = tour[i]
            next_city = tour[(i + 1) % len(tour)]
            weight = distance_matrix[current][next_city]
            G.add_edge(current, next_city, weight=weight)
            edge_labels[(current, next_city)] = f"{weight:.1f}"

        # Create plot
        plt.figure(figsize=(12, 8))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                              node_size=700, edgecolors='black', linewidths=2)

        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='blue', 
                              width=2, alpha=0.6)

        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

        # Draw edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

        # Highlight start node
        nx.draw_networkx_nodes(G, pos, nodelist=[tour[0]], 
                              node_color='green', node_size=900,
                              node_shape='*', edgecolors='black', linewidths=2)

        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
