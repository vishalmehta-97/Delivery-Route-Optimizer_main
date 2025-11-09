"""
Matplotlib-based TSP visualization.
"""

import matplotlib.pyplot as plt
import numpy as np


class MatplotlibVisualizer:
    """Visualize TSP solutions using Matplotlib."""

    @staticmethod
    def plot_tour(cities, tour, cost, title="TSP Solution"):
        """
        Plot TSP tour with cities and routes.

        Args:
            cities: List of City objects
            tour: Ordered list of city indices
            cost: Total tour cost
            title: Plot title
        """
        if not tour:
            print("No tour to visualize")
            return

        # Extract coordinates
        x_coords = [cities[i].x for i in tour]
        y_coords = [cities[i].y for i in tour]

        # Close the loop
        x_coords.append(cities[tour[0]].x)
        y_coords.append(cities[tour[0]].y)

        # Create plot
        plt.figure(figsize=(12, 8))

        # Plot routes
        plt.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.6, label='Route')

        # Plot cities
        plt.scatter(x_coords[:-1], y_coords[:-1], c='red', s=200, 
                   zorder=5, edgecolors='black', linewidths=2)

        # Highlight start/end
        plt.scatter(x_coords[0], y_coords[0], c='green', s=400, 
                   marker='*', zorder=6, edgecolors='black', 
                   linewidths=2, label='Start/End')

        # Add city labels
        for i, city_id in enumerate(tour):
            city = cities[city_id]
            plt.annotate(city.name, 
                        (city.x, city.y),
                        xytext=(10, 10),
                        textcoords='offset points',
                        fontsize=9,
                        bbox=dict(boxstyle='round,pad=0.5', 
                                facecolor='yellow', alpha=0.7))

        # Add step numbers
        for i in range(len(tour)):
            plt.text(x_coords[i], y_coords[i], str(i+1),
                    fontsize=12, fontweight='bold',
                    ha='center', va='center', color='white')

        plt.title(f"{title}\nTotal Distance: {cost:.2f}", fontsize=14, fontweight='bold')
        plt.xlabel('X Coordinate', fontsize=12)
        plt.ylabel('Y Coordinate', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_comparison(cities, solutions, titles):
        """
        Plot multiple solutions for comparison.

        Args:
            cities: List of City objects
            solutions: List of (tour, cost) tuples
            titles: List of solution titles
        """
        n = len(solutions)
        fig, axes = plt.subplots(1, n, figsize=(6*n, 5))

        if n == 1:
            axes = [axes]

        for idx, (ax, (tour, cost), title) in enumerate(zip(axes, solutions, titles)):
            x_coords = [cities[i].x for i in tour]
            y_coords = [cities[i].y for i in tour]
            x_coords.append(cities[tour[0]].x)
            y_coords.append(cities[tour[0]].y)

            ax.plot(x_coords, y_coords, 'b-', linewidth=2)
            ax.scatter(x_coords[:-1], y_coords[:-1], c='red', s=100, zorder=5)
            ax.scatter(x_coords[0], y_coords[0], c='green', s=200, marker='*', zorder=6)

            ax.set_title(f"{title}\nCost: {cost:.2f}", fontweight='bold')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.grid(True, alpha=0.3)
            ax.axis('equal')

        plt.tight_layout()
        plt.show()
