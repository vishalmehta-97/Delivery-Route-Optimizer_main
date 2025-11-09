"""
Brute-force TSP solver - exhaustive search.
"""

from itertools import permutations
from ..graph.distance_calculator import DistanceCalculator


class BruteForceSolver:
    """Solve TSP by examining all possible permutations."""

    def __init__(self):
        self.calc = DistanceCalculator()

    def solve(self, cities, distance_matrix):
        """
        Find optimal tour using brute-force enumeration.

        Args:
            cities: List of City objects
            distance_matrix: Precomputed distance matrix

        Returns:
            tuple: (optimal_tour, minimum_cost)

        Note:
            Time Complexity: O(n!)
            Space Complexity: O(n)
            Practical limit: n <= 10-12 cities
        """
        n = len(cities)

        if n == 0:
            return [], 0
        if n == 1:
            return [0], 0
        if n == 2:
            return [0, 1], distance_matrix[0][1] * 2

        # Generate all permutations starting from city 0
        city_indices = list(range(1, n))
        min_cost = float('inf')
        best_tour = None

        for perm in permutations(city_indices):
            tour = [0] + list(perm)
            cost = self.calc.calculate_tour_cost(tour, distance_matrix)

            if cost < min_cost:
                min_cost = cost
                best_tour = tour

        return best_tour, min_cost
