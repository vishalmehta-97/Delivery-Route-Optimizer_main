"""
Distance calculation utilities for TSP.
"""

import numpy as np
from math import sqrt, radians, sin, cos, asin, atan2


class DistanceCalculator:
    """Calculate distances between cities using various metrics."""

    @staticmethod
    def euclidean_distance(city1, city2):
        """
        Calculate Euclidean distance between two cities.

        Args:
            city1: First city
            city2: Second city

        Returns:
            float: Euclidean distance
        """
        return sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calculate great-circle distance using Haversine formula.

        Args:
            lat1, lon1: Coordinates of first point
            lat2, lon2: Coordinates of second point

        Returns:
            float: Distance in kilometers
        """
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return 6371 * c  # Earth's radius in km

    def calculate_distance_matrix(self, cities, metric='euclidean'):
        """
        Build distance matrix for all city pairs.

        Args:
            cities: List of City objects
            metric: Distance metric ('euclidean' or 'haversine')

        Returns:
            numpy.ndarray: n x n distance matrix
        """
        n = len(cities)
        distances = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                if metric == 'euclidean':
                    dist = self.euclidean_distance(cities[i], cities[j])
                else:
                    dist = self.haversine_distance(
                        cities[i].x, cities[i].y,
                        cities[j].x, cities[j].y
                    )
                distances[i][j] = dist
                distances[j][i] = dist  # Symmetric

        return distances

    @staticmethod
    def calculate_tour_cost(tour, distance_matrix):
        """
        Calculate total cost of a tour.

        Args:
            tour: List of city indices
            distance_matrix: Distance matrix

        Returns:
            float: Total tour cost
        """
        cost = 0
        n = len(tour)
        for i in range(n):
            current = tour[i]
            next_city = tour[(i + 1) % n]
            cost += distance_matrix[current][next_city]
        return cost
