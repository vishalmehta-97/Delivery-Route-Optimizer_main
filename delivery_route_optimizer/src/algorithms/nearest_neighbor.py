"""
Nearest Neighbor heuristic TSP solver.
"""

from ..graph.distance_calculator import DistanceCalculator


class NearestNeighborSolver:
    """Solve TSP using Nearest Neighbor greedy heuristic."""

    def __init__(self):
        self.calc = DistanceCalculator()

    def solve(self, cities, distance_matrix, start_city=0):
        """
        Find approximate tour using Nearest Neighbor heuristic.

        Args:
            cities: List of City objects
            distance_matrix: Precomputed distance matrix
            start_city: Starting city index (default: 0)

        Returns:
            tuple: (tour, cost)

        Note:
            Time Complexity: O(n²)
            Space Complexity: O(n)
            Does not guarantee optimal solution
        """
        n = len(cities)

        if n == 0:
            return [], 0
        if n == 1:
            return [0], 0

        unvisited = set(range(n))
        tour = [start_city]
        unvisited.remove(start_city)
        current = start_city
        total_cost = 0

        while unvisited:
            # Find nearest unvisited city
            nearest = min(unvisited, key=lambda city: distance_matrix[current][city])

            total_cost += distance_matrix[current][nearest]
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        # Return to start
        total_cost += distance_matrix[current][start_city]

        return tour, total_cost

    def solve_multi_start(self, cities, distance_matrix):
        """
        Run NN from multiple starting cities and return best solution.

        Args:
            cities: List of City objects
            distance_matrix: Precomputed distance matrix

        Returns:
            tuple: (best_tour, best_cost)
        """
        n = len(cities)
        best_tour = None
        best_cost = float('inf')

        for start in range(n):
            tour, cost = self.solve(cities, distance_matrix, start)
            if cost < best_cost:
                best_cost = cost
                best_tour = tour

        return best_tour, best_cost
