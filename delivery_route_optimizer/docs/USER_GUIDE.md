# User Guide - Delivery Route Optimizer

## Introduction

The Delivery Route Optimizer is a comprehensive Python application for solving the Travelling Salesman Problem (TSP) using multiple algorithms with graphical visualization.

## Installation

### Requirements
- Python 3.7 or higher
- pip package manager

### Setup Steps

1. Extract the project files
2. Navigate to project directory:
   ```bash
   cd delivery_route_optimizer
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Methods

### 1. Command-Line Interface (CLI)

#### Basic Usage
```bash
python -m src.main --input data/sample_cities.csv --algorithm dp --visualize
```

#### Available Arguments
- `--input, -i`: Path to input CSV file (required)
- `--algorithm, -a`: Algorithm choice:
  - `brute`: Brute Force (n ≤ 10)
  - `dp`: Held-Karp Dynamic Programming (n ≤ 20)
  - `nn`: Nearest Neighbor Heuristic
  - `2opt`: 2-Opt Local Search
- `--visualize, -v`: Show graphical visualization
- `--output, -o`: Save solution to file (.txt, .json, .csv)
- `--benchmark, -b`: Run all algorithms and compare

#### Examples

Solve with Held-Karp and visualize:
```bash
python -m src.main -i data/sample_cities.csv -a dp -v
```

Use fast heuristic:
```bash
python -m src.main -i data/cities_10.csv -a nn -v
```

Run benchmark comparison:
```bash
python -m src.main -i data/sample_cities.csv --benchmark
```

Save solution:
```bash
python -m src.main -i data/sample_cities.csv -a dp -o solution.json
```

### 2. Graphical User Interface (GUI)

#### Launch GUI
```bash
python -m src.gui_app
```

#### GUI Features
1. **Load Data**: Click "Load CSV File" to import cities
2. **Generate Random**: Create random test instances
3. **Select Algorithm**: Choose from Held-Karp, Nearest Neighbor, or 2-Opt
4. **Solve**: Click "Solve TSP" to compute optimal route
5. **Visualize**: View interactive route visualization

### 3. Python API

#### Basic Usage
```python
from src.graph.city import City
from src.graph.distance_calculator import DistanceCalculator
from src.algorithms.held_karp import HeldKarpSolver

# Create cities
cities = [
    City(0, 0, 0, "Warehouse"),
    City(1, 20, 30, "Customer A"),
    City(2, 40, 10, "Customer B")
]

# Calculate distances
calc = DistanceCalculator()
distances = calc.calculate_distance_matrix(cities)

# Solve TSP
solver = HeldKarpSolver()
tour, cost = solver.solve(cities, distances)

print(f"Optimal tour: {tour}")
print(f"Total distance: {cost:.2f}")
```

## Input File Format

### CSV Format
The application accepts CSV files with the following structure:

```csv
id,x,y,name
0,0,0,Warehouse
1,20,30,Customer A
2,40,10,Customer B
```

**Columns:**
- `id`: Unique integer identifier
- `x`: X coordinate (float)
- `y`: Y coordinate (float)
- `name`: Optional location name (string)

### Creating Input Files

#### Using Excel
1. Create spreadsheet with columns: id, x, y, name
2. Enter location data
3. Save As → CSV (Comma delimited)

#### Using Python
```python
from src.io.csv_loader import CSVLoader
from src.graph.city import City

cities = [
    City(0, 10, 20, "Store 1"),
    City(1, 30, 40, "Store 2")
]

loader = CSVLoader()
loader.save_cities(cities, "my_cities.csv")
```

## Algorithm Selection Guide

### When to Use Each Algorithm

#### Brute Force
- **Use for**: 3-10 cities
- **Pros**: Guarantees optimal solution
- **Cons**: Extremely slow for n > 10
- **Complexity**: O(n!)

#### Held-Karp Dynamic Programming
- **Use for**: 3-20 cities
- **Pros**: Guarantees optimal solution, much faster than brute force
- **Cons**: High memory usage
- **Complexity**: O(n² × 2^n)

#### Nearest Neighbor
- **Use for**: Quick approximations, any size
- **Pros**: Very fast, simple
- **Cons**: No optimality guarantee (typically 20-30% above optimal)
- **Complexity**: O(n²)

#### 2-Opt
- **Use for**: Improving heuristic solutions
- **Pros**: Improves tour quality significantly
- **Cons**: Only finds local optimum
- **Complexity**: O(n³)

### Recommended Strategy
1. **Small instances (n ≤ 10)**: Use Brute Force or Held-Karp
2. **Medium instances (10 < n ≤ 20)**: Use Held-Karp
3. **Large instances (n > 20)**: Use Nearest Neighbor + 2-Opt

## Troubleshooting

### Common Issues

#### "FileNotFoundError"
- Check that input file path is correct
- Use absolute paths if relative paths fail

#### "Memory Error" with Held-Karp
- Too many cities (> 25)
- Use Nearest Neighbor or 2-Opt instead

#### Visualization not showing
- Ensure matplotlib is installed: `pip install matplotlib`
- Check display environment variables

#### "Module not found"
- Ensure you're in project root directory
- Run as module: `python -m src.main` not `python src/main.py`

## Tips and Best Practices

1. **Test with small datasets** first
2. **Use benchmarking** to compare algorithm performance
3. **Save solutions** for documentation
4. **Verify input data** before solving
5. **Use appropriate algorithms** for problem size

## Support

For issues or questions:
- Check documentation in `docs/` folder
- Review example files in `data/` folder
- Run unit tests: `python -m pytest tests/`
