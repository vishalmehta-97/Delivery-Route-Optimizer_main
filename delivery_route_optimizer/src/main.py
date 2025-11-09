"""
Main command-line interface for TSP Delivery Route Optimizer.
"""

import argparse
import sys
from pathlib import Path

from .graph.city import City
from .graph.distance_calculator import DistanceCalculator
from .algorithms.brute_force import BruteForceSolver
from .algorithms.held_karp import HeldKarpSolver
from .algorithms.nearest_neighbor import NearestNeighborSolver
from .algorithms.two_opt import TwoOptSolver
from .io.csv_loader import CSVLoader
from .io.solution_writer import SolutionWriter
from .visualization.matplotlib_viz import MatplotlibVisualizer
from .utils.benchmarking import Benchmark


def main():
    parser = argparse.ArgumentParser(
        description='Delivery Route Optimizer - TSP Solver',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Solve using Held-Karp and visualize
  python -m src.main --input data/sample_cities.csv --algorithm dp --visualize

  # Use Nearest Neighbor heuristic
  python -m src.main --input data/sample_cities.csv --algorithm nn

  # Run benchmarks
  python -m src.main --input data/sample_cities.csv --benchmark
        '''
    )

    parser.add_argument('--input', '-i', required=True,
                       help='Input CSV file with city coordinates')
    parser.add_argument('--algorithm', '-a', 
                       choices=['brute', 'dp', 'nn', '2opt'],
                       default='dp',
                       help='Algorithm: brute (Brute Force), dp (Held-Karp), '
                            'nn (Nearest Neighbor), 2opt (2-Opt)')
    parser.add_argument('--visualize', '-v', action='store_true',
                       help='Display graphical visualization')
    parser.add_argument('--output', '-o',
                       help='Output file for solution (supports .txt, .json, .csv)')
    parser.add_argument('--benchmark', '-b', action='store_true',
                       help='Run performance benchmarks')

    args = parser.parse_args()

    try:
        # Load cities
        print(f"Loading cities from {args.input}...")
        loader = CSVLoader()
        cities = loader.load_cities(args.input)
        print(f"Loaded {len(cities)} cities")

        # Calculate distance matrix
        calc = DistanceCalculator()
        distances = calc.calculate_distance_matrix(cities)

        if args.benchmark:
            # Run benchmarks
            print("\nRunning benchmarks...")
            benchmark = Benchmark()
            results = benchmark.run_benchmark(cities, distances)
            benchmark.print_results(results)
        else:
            # Solve with selected algorithm
            print(f"\nSolving TSP using {args.algorithm.upper()}...")

            solvers = {
                'brute': BruteForceSolver(),
                'dp': HeldKarpSolver(),
                'nn': NearestNeighborSolver(),
                '2opt': TwoOptSolver()
            }

            solver = solvers[args.algorithm]
            tour, cost = solver.solve(cities, distances)

            print(f"\nOptimal Tour Found!")
            print(f"Total Distance: {cost:.2f}")
            print(f"Tour Order: {' -> '.join([cities[i].name for i in tour[:5]])}...")

            # Save solution
            if args.output:
                writer = SolutionWriter()
                ext = Path(args.output).suffix.lower()

                if ext == '.json':
                    writer.write_json(tour, cost, cities, args.output)
                elif ext == '.csv':
                    writer.write_csv(tour, cost, cities, args.output)
                else:
                    writer.write_text(tour, cost, cities, args.output)

                print(f"\nSolution saved to {args.output}")

            # Visualize
            if args.visualize:
                print("\nGenerating visualization...")
                viz = MatplotlibVisualizer()
                viz.plot_tour(cities, tour, cost, 
                            title=f"TSP Solution - {args.algorithm.upper()}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
