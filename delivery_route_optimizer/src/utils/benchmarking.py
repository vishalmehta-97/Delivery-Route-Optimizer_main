"""
Performance benchmarking utilities.
"""

import time
from ..algorithms.brute_force import BruteForceSolver
from ..algorithms.held_karp import HeldKarpSolver
from ..algorithms.nearest_neighbor import NearestNeighborSolver
from ..algorithms.two_opt import TwoOptSolver


class Benchmark:
    """Benchmark TSP algorithms."""

    def __init__(self):
        self.solvers = {
            'Brute Force': BruteForceSolver(),
            'Held-Karp DP': HeldKarpSolver(),
            'Nearest Neighbor': NearestNeighborSolver(),
            '2-Opt': TwoOptSolver()
        }

    def run_benchmark(self, cities, distance_matrix):
        """
        Run all algorithms and collect performance metrics.

        Args:
            cities: List of City objects
            distance_matrix: Distance matrix

        Returns:
            dict: Results for each algorithm
        """
        results = {}
        n = len(cities)

        for name, solver in self.solvers.items():
            # Skip brute force for large instances
            if name == 'Brute Force' and n > 10:
                results[name] = {
                    'skipped': True,
                    'reason': f'Too many cities ({n} > 10)'
                }
                continue

            try:
                start_time = time.perf_counter()
                start_cpu = time.process_time()

                tour, cost = solver.solve(cities, distance_matrix)

                wall_time = time.perf_counter() - start_time
                cpu_time = time.process_time() - start_cpu

                results[name] = {
                    'tour': tour,
                    'cost': cost,
                    'wall_time': wall_time,
                    'cpu_time': cpu_time,
                    'skipped': False
                }
            except Exception as e:
                results[name] = {
                    'skipped': True,
                    'error': str(e)
                }

        return results

    def print_results(self, results):
        """Print formatted benchmark results."""
        print("\n" + "="*70)
        print("BENCHMARK RESULTS")
        print("="*70)

        for name, data in results.items():
            print(f"\n{name}:")
            print("-" * 50)

            if data.get('skipped'):
                if 'reason' in data:
                    print(f"  SKIPPED: {data['reason']}")
                else:
                    print(f"  ERROR: {data.get('error', 'Unknown error')}")
            else:
                print(f"  Cost: {data['cost']:.2f}")
                print(f"  Wall Time: {data['wall_time']:.6f} seconds")
                print(f"  CPU Time: {data['cpu_time']:.6f} seconds")
                print(f"  Tour: {data['tour'][:10]}{'...' if len(data['tour']) > 10 else ''}")

        print("\n" + "="*70)
