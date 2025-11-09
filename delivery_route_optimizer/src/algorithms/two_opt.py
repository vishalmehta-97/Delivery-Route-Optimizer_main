"""
2-Opt local search optimization for TSP.
"""

from ..graph.distance_calculator import DistanceCalculator


class TwoOptSolver:
    """Improve TSP tours using 2-Opt local search."""

    def __init__(self):
        self.calc = DistanceCalculator()

    def solve(self, cities, distance_matrix, initial_tour=None):
        """
        Optimize tour using 2-Opt swaps.

        Args:
            cities: List of City objects
            distance_matrix: Precomputed distance matrix
            initial_tour: Starting tour (if None, uses simple order)

        Returns:
            tuple: (optimized_tour, cost)

        Note:
            Time Complexity: O(n³)
            Space Complexity: O(n)
            Improves existing tours iteratively
        """
        n = len(cities)

        if n <= 1:
            return list(range(n)), 0

        # Initialize with provided tour or simple order
        if initial_tour is None:
            tour = list(range(n))
        else:
            tour = initial_tour.copy()

        improved = True

        while improved:
            improved = False

            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    # Calculate current cost
                    current_cost = (
                        distance_matrix[tour[i-1]][tour[i]] +
                        distance_matrix[tour[j]][tour[(j+1) % n]]
                    )

                    # Calculate cost after swap
                    swap_cost = (
                        distance_matrix[tour[i-1]][tour[j]] +
                        distance_matrix[tour[i]][tour[(j+1) % n]]
                    )

                    # If improvement found, apply swap
                    if swap_cost < current_cost:
                        tour[i:j+1] = reversed(tour[i:j+1])
                        improved = True

        cost = self.calc.calculate_tour_cost(tour, distance_matrix)
        return tour, cost

    def optimize_tour(self, tour, distance_matrix, max_iterations=1000):
        """
        Apply 2-Opt optimization with iteration limit.

        Args:
            tour: Initial tour
            distance_matrix: Distance matrix
            max_iterations: Maximum optimization iterations

        Returns:
            tuple: (optimized_tour, cost)
        """
        best_tour = tour.copy()
        best_cost = self.calc.calculate_tour_cost(best_tour, distance_matrix)

        for _ in range(max_iterations):
            improved = False
            n = len(tour)

            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    new_tour = best_tour.copy()
                    new_tour[i:j+1] = reversed(new_tour[i:j+1])
                    new_cost = self.calc.calculate_tour_cost(new_tour, distance_matrix)

                    if new_cost < best_cost:
                        best_tour = new_tour
                        best_cost = new_cost
                        improved = True

            if not improved:
                break

        return best_tour, best_cost
