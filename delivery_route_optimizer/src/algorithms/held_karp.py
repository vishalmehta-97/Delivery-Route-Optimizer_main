"""
Held-Karp dynamic programming TSP solver.
"""

from ..graph.distance_calculator import DistanceCalculator


class HeldKarpSolver:
    """Solve TSP using Held-Karp dynamic programming algorithm."""

    def __init__(self):
        self.calc = DistanceCalculator()

    def solve(self, cities, distance_matrix):
        """
        Find optimal tour using Held-Karp algorithm.

        Args:
            cities: List of City objects
            distance_matrix: Precomputed distance matrix

        Returns:
            tuple: (optimal_tour, minimum_cost)

        Note:
            Time Complexity: O(n² × 2^n)
            Space Complexity: O(n × 2^n)
            Practical limit: n <= 20-25 cities
        """
        n = len(cities)

        if n == 0:
            return [], 0
        if n == 1:
            return [0], 0
        if n == 2:
            return [0, 1], distance_matrix[0][1] * 2

        # DP table: dp[mask][i] = minimum cost to visit cities in mask ending at i
        dp = [[float('inf')] * n for _ in range(1 << n)]
        parent = [[None] * n for _ in range(1 << n)]

        # Base case: start from city 0
        dp[1][0] = 0

        # Iterate through all subsets
        for mask in range(1 << n):
            for i in range(n):
                if not (mask & (1 << i)):  # i not in mask
                    continue

                if dp[mask][i] == float('inf'):
                    continue

                # Try extending to city j
                for j in range(n):
                    if mask & (1 << j):  # j already in mask
                        continue

                    new_mask = mask | (1 << j)
                    new_cost = dp[mask][i] + distance_matrix[i][j]

                    if new_cost < dp[new_mask][j]:
                        dp[new_mask][j] = new_cost
                        parent[new_mask][j] = i

        # Find minimum cost to return to start
        full_mask = (1 << n) - 1
        min_cost = float('inf')
        last_city = -1

        for i in range(1, n):
            cost = dp[full_mask][i] + distance_matrix[i][0]
            if cost < min_cost:
                min_cost = cost
                last_city = i

        # Reconstruct tour
        tour = self._reconstruct_tour(parent, full_mask, last_city, n)

        return tour, min_cost

    def _reconstruct_tour(self, parent, mask, last_city, n):
        """Reconstruct optimal tour from parent pointers."""
        tour = []
        current = last_city

        while current is not None:
            tour.append(current)
            prev = parent[mask][current]
            if prev is not None:
                mask ^= (1 << current)
            current = prev

        tour.reverse()
        return tour
