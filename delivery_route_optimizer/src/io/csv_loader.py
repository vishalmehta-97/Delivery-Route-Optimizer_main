"""
CSV file loader for city data.
"""

import csv
from ..graph.city import City


class CSVLoader:
    """Load city data from CSV files."""

    @staticmethod
    def load_cities(filename, encoding='utf-8'):
        """
        Load cities from CSV file.

        Expected format: id,x,y,name

        Args:
            filename: Path to CSV file
            encoding: File encoding (default: utf-8)

        Returns:
            list: List of City objects

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        cities = []

        try:
            with open(filename, 'r', newline='', encoding=encoding) as file:
                # Remove BOM if present
                content = file.read()
                if content.startswith('\ufeff'):
                    content = content[1:]

                # Parse CSV
                reader = csv.reader(content.splitlines())
                header = next(reader, None)

                if header is None:
                    raise ValueError("Empty CSV file")

                for row_num, row in enumerate(reader, start=2):
                    if not row or all(cell.strip() == '' for cell in row):
                        continue  # Skip empty rows

                    try:
                        city_id = int(row[0])
                        x = float(row[1])
                        y = float(row[2])
                        name = row[3].strip() if len(row) > 3 else f"City_{city_id}"

                        cities.append(City(city_id, x, y, name))
                    except (ValueError, IndexError) as e:
                        raise ValueError(f"Invalid data in row {row_num}: {row}") from e

            return cities

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")

    @staticmethod
    def save_cities(cities, filename):
        """
        Save cities to CSV file.

        Args:
            cities: List of City objects
            filename: Output file path
        """
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'x', 'y', 'name'])

            for city in cities:
                writer.writerow([city.id, city.x, city.y, city.name])
