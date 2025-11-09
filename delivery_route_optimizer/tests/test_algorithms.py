"""
Unit tests for TSP algorithms.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph.city import City
from src.graph.distance_calculator import DistanceCalculator
from src.algorithms.brute_force import BruteForceSolver
from src.algorithms.held_karp import HeldKarpSolver
from src.algorithms.nearest_neighbor import NearestNeighborSolver


class TestTSPAlgorithms(unittest.TestCase):
    """Test TSP solving algorithms."""

    def setUp(self):
        """Set up test data."""
        self.cities = [
            City(0, 0, 0, "A"),
            City(1, 1, 0, "B"),
            City(2, 1, 1, "C"),
            City(3, 0, 1, "D")
        ]
        self.calc = DistanceCalculator()
        self.distances = self.calc.calculate_distance_matrix(self.cities)

    def test_brute_force_small(self):
        """Test brute force on small instance."""
        solver = BruteForceSolver()
        tour, cost = solver.solve(self.cities, self.distances)

        self.assertEqual(len(tour), 4)
        self.assertEqual(len(set(tour)), 4)
        self.assertGreater(cost, 0)

    def test_held_karp_small(self):
        """Test Held-Karp on small instance."""
        solver = HeldKarpSolver()
        tour, cost = solver.solve(self.cities, self.distances)

        self.assertEqual(len(tour), 4)
        self.assertEqual(len(set(tour)), 4)
        self.assertGreater(cost, 0)

    def test_nearest_neighbor(self):
        """Test Nearest Neighbor heuristic."""
        solver = NearestNeighborSolver()
        tour, cost = solver.solve(self.cities, self.distances)

        self.assertEqual(len(tour), 4)
        self.assertEqual(len(set(tour)), 4)
        self.assertGreater(cost, 0)

    def test_algorithms_consistency(self):
        """Test that exact algorithms produce same optimal cost."""
        bf_solver = BruteForceSolver()
        hk_solver = HeldKarpSolver()

        _, bf_cost = bf_solver.solve(self.cities, self.distances)
        _, hk_cost = hk_solver.solve(self.cities, self.distances)

        self.assertAlmostEqual(bf_cost, hk_cost, places=5)


if __name__ == '__main__':
    unittest.main()
