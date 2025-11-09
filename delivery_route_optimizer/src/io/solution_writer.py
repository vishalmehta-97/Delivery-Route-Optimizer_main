"""
Solution output writer.
"""

import json
import csv


class SolutionWriter:
    """Write TSP solutions to various formats."""

    @staticmethod
    def write_text(tour, cost, cities, filename):
        """Write solution to text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== TSP Solution ==\n\n")
            f.write(f"Total Cost: {cost:.2f}\n")
            f.write(f"Number of Cities: {len(tour)}\n\n")
            f.write("Tour Order:\n")

            for idx, city_id in enumerate(tour, 1):
                city = cities[city_id]
                f.write(f"{idx}. {city.name} (ID: {city_id})\n")

            f.write(f"\nReturn to: {cities[tour[0]].name}\n")

    @staticmethod
    def write_json(tour, cost, cities, filename):
        """Write solution to JSON file."""
        solution = {
            'tour': tour,
            'cost': float(cost),
            'num_cities': len(tour),
            'cities': [cities[i].to_dict() for i in tour]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(solution, f, indent=2)

    @staticmethod
    def write_csv(tour, cost, cities, filename):
        """Write solution to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Step', 'City_ID', 'City_Name', 'X', 'Y'])

            for idx, city_id in enumerate(tour, 1):
                city = cities[city_id]
                writer.writerow([idx, city.id, city.name, city.x, city.y])
