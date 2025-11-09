"""
City data structure for representing delivery locations.
"""

class City:
    """Represents a delivery location with coordinates and metadata."""

    def __init__(self, city_id, x, y, name=None):
        """
        Initialize a city.

        Args:
            city_id (int): Unique identifier for the city
            x (float): X coordinate
            y (float): Y coordinate
            name (str, optional): Human-readable name
        """
        self.id = city_id
        self.x = float(x)
        self.y = float(y)
        self.name = name if name else f"City_{city_id}"

    def __repr__(self):
        return f"City({self.id}, {self.x}, {self.y}, '{self.name}')"

    def __str__(self):
        return f"{self.name} at ({self.x:.2f}, {self.y:.2f})"

    def to_dict(self):
        """Convert city to dictionary."""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'name': self.name
        }
