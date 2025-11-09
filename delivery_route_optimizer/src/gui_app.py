"""
Tkinter GUI application for TSP solver with complete graph visualization.
Shows all cities connected to demonstrate the Travelling Salesman Problem.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from src.graph.city import City
from src.graph.distance_calculator import DistanceCalculator
from src.algorithms.held_karp import HeldKarpSolver
from src.algorithms.nearest_neighbor import NearestNeighborSolver
from src.algorithms.two_opt import TwoOptSolver
from src.io.csv_loader import CSVLoader


class TSPVisualizerGUI:
    """Interactive GUI for TSP solver with complete graph visualization."""

    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Route Optimizer - TSP Solver with Complete Graph")
        self.root.geometry("1600x800")

        self.cities = []
        self.distances = None
        self.current_tour = None
        self.current_cost = 0

        self.setup_ui()

    def setup_ui(self):
        """Create GUI layout with side-by-side visualization."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Control panel (left side)
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Input section
        ttk.Label(control_frame, text="Input Data:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=5)

        ttk.Button(control_frame, text="📂 Load CSV File", 
                  command=self.load_file).grid(row=1, column=0, columnspan=2, 
                                               sticky=(tk.W, tk.E), pady=5)

        ttk.Button(control_frame, text="🎲 Generate Random Cities",
                  command=self.generate_random).grid(row=2, column=0, columnspan=2,
                                                     sticky=(tk.W, tk.E), pady=5)

        ttk.Separator(control_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.algo_var = tk.StringVar(value="Held-Karp DP")
        algorithms = ["Held-Karp DP", "Nearest Neighbor", "2-Opt"]

        for i, algo in enumerate(algorithms):
            ttk.Radiobutton(control_frame, text=algo, variable=self.algo_var,
                           value=algo).grid(row=5+i, column=0, columnspan=2,
                                          sticky=tk.W, pady=2)

        ttk.Separator(control_frame, orient='horizontal').grid(
            row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Visualization options
        ttk.Label(control_frame, text="Display Options:", font=('Arial', 10, 'bold')).grid(
            row=9, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.show_names_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Show City Names", 
                       variable=self.show_names_var,
                       command=self.update_plots).grid(row=10, column=0, columnspan=2,
                                                      sticky=tk.W, pady=2)

        self.show_all_edges_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Show All Edges (Problem)", 
                       variable=self.show_all_edges_var,
                       command=self.update_plots).grid(row=11, column=0, columnspan=2,
                                                      sticky=tk.W, pady=2)

        self.show_distances_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Show Edge Distances", 
                       variable=self.show_distances_var,
                       command=self.update_plots).grid(row=12, column=0, columnspan=2,
                                                      sticky=tk.W, pady=2)

        self.show_order_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Show Visit Order", 
                       variable=self.show_order_var,
                       command=self.update_plots).grid(row=13, column=0, columnspan=2,
                                                      sticky=tk.W, pady=2)

        ttk.Separator(control_frame, orient='horizontal').grid(
            row=14, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Solve button
        solve_btn = ttk.Button(control_frame, text="🚀 Solve TSP", 
                              command=self.solve_tsp)
        solve_btn.grid(row=15, column=0, columnspan=2,
                      sticky=(tk.W, tk.E), pady=10)

        # Results display
        ttk.Label(control_frame, text="Results:", font=('Arial', 10, 'bold')).grid(
            row=16, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Results text with scrollbar
        result_frame = ttk.Frame(control_frame)
        result_frame.grid(row=17, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(result_frame, height=14, width=40, 
                                   yscrollcommand=scrollbar.set, wrap=tk.WORD,
                                   font=('Courier', 9))
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)

        # Visualization panels (right side) - Side by side
        viz_left_frame = ttk.LabelFrame(main_frame, text="📊 TSP Problem (All Edges)", padding="10")
        viz_left_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Left plot - All edges
        self.fig_left = Figure(figsize=(6.5, 7), dpi=100)
        self.ax_left = self.fig_left.add_subplot(111)
        self.canvas_left = FigureCanvasTkAgg(self.fig_left, viz_left_frame)
        self.canvas_left.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        viz_right_frame = ttk.LabelFrame(main_frame, text="✅ Optimal Solution (Best Path)", padding="10")
        viz_right_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Right plot - Optimal tour
        self.fig_right = Figure(figsize=(6.5, 7), dpi=100)
        self.ax_right = self.fig_right.add_subplot(111)
        self.canvas_right = FigureCanvasTkAgg(self.fig_right, viz_right_frame)
        self.canvas_right.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=2)
        main_frame.rowconfigure(0, weight=1)
        control_frame.rowconfigure(17, weight=1)

        self.update_plots()

    def load_file(self):
        """Load cities from CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            try:
                loader = CSVLoader()
                self.cities = loader.load_cities(filename)

                calc = DistanceCalculator()
                self.distances = calc.calculate_distance_matrix(self.cities)

                self.current_tour = None
                self.current_cost = 0

                messagebox.showinfo("Success", f"Loaded {len(self.cities)} cities\n\n" + 
                                   "\n".join([f"• {c.name}" for c in self.cities[:5]]) +
                                   ("\n..." if len(self.cities) > 5 else ""))
                self.update_plots()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def generate_random(self):
        """Generate random cities."""
        try:
            n = simpledialog.askinteger("Input", 
                                       "Number of cities (3-15):", 
                                       minvalue=3, maxvalue=15,
                                       initialvalue=6)
            if n:
                np.random.seed()
                self.cities = [
                    City(i, 
                         np.random.rand()*100, 
                         np.random.rand()*100, 
                         f"City_{i}" if i > 0 else "Warehouse")
                    for i in range(n)
                ]

                calc = DistanceCalculator()
                self.distances = calc.calculate_distance_matrix(self.cities)

                self.current_tour = None
                self.current_cost = 0

                messagebox.showinfo("Success", f"Generated {n} random cities")
                self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate cities:\n{str(e)}")

    def solve_tsp(self):
        """Solve TSP with selected algorithm."""
        if not self.cities:
            messagebox.showwarning("Warning", "Please load or generate cities first!")
            return

        try:
            algo = self.algo_var.get()

            # Show progress
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Solving with {algo}...\n")
            self.root.update()

            import time
            start_time = time.time()

            if algo == "Held-Karp DP":
                solver = HeldKarpSolver()
            elif algo == "Nearest Neighbor":
                solver = NearestNeighborSolver()
            else:  # 2-Opt
                solver = TwoOptSolver()

            self.current_tour, self.current_cost = solver.solve(self.cities, self.distances)

            elapsed = time.time() - start_time

            # Update results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"✓ Solution Found!\n\n")
            self.result_text.insert(tk.END, f"Algorithm: {algo}\n")
            self.result_text.insert(tk.END, f"Cities: {len(self.cities)}\n")
            self.result_text.insert(tk.END, f"Total Distance: {self.current_cost:.2f}\n")
            self.result_text.insert(tk.END, f"Time: {elapsed:.4f} sec\n\n")
            self.result_text.insert(tk.END, "="*40 + "\n")
            self.result_text.insert(tk.END, "Optimal Route Order:\n")
            self.result_text.insert(tk.END, "="*40 + "\n\n")

            for i, city_id in enumerate(self.current_tour, 1):
                city = self.cities[city_id]
                self.result_text.insert(tk.END, f"{i:2d}. {city.name}\n")
                self.result_text.insert(tk.END, f"    ({city.x:.0f}, {city.y:.0f})\n")

                if i < len(self.current_tour):
                    next_id = self.current_tour[i]
                    dist = self.distances[city_id][next_id]
                    self.result_text.insert(tk.END, f"    ↓ {dist:.2f}\n")

            # Return to start
            return_dist = self.distances[self.current_tour[-1]][self.current_tour[0]]
            self.result_text.insert(tk.END, f"    ↓ {return_dist:.2f}\n")
            self.result_text.insert(tk.END, f"→ {self.cities[self.current_tour[0]].name}\n")

            self.update_plots()

        except Exception as e:
            messagebox.showerror("Error", f"Solving failed:\n{str(e)}")
            import traceback
            traceback.print_exc()

    def update_plots(self):
        """Update both visualizations."""
        self.update_problem_plot()
        self.update_solution_plot()

    def update_problem_plot(self):
        """Update left plot showing the complete TSP problem."""
        self.ax_left.clear()

        if not self.cities:
            self.ax_left.text(0.5, 0.5, 'No data loaded\n\nLoad CSV or Generate Random Cities', 
                        ha='center', va='center', fontsize=12, color='gray')
            self.ax_left.set_xlim(0, 1)
            self.ax_left.set_ylim(0, 1)
            self.fig_left.tight_layout()
            self.canvas_left.draw()
            return

        x = [c.x for c in self.cities]
        y = [c.y for c in self.cities]

        # Draw ALL edges (complete graph)
        if self.show_all_edges_var.get():
            for i in range(len(self.cities)):
                for j in range(i+1, len(self.cities)):
                    self.ax_left.plot([self.cities[i].x, self.cities[j].x],
                                     [self.cities[i].y, self.cities[j].y],
                                     'lightgray', linewidth=0.8, alpha=0.4, zorder=1)

        # Draw cities
        # Warehouse (first city) - special marker
        self.ax_left.scatter(x[0], y[0], c='green', s=600, marker='*', 
                            zorder=10, edgecolors='darkgreen', linewidths=2, 
                            label='Start/Warehouse')

        # Other cities
        self.ax_left.scatter(x[1:], y[1:], c='red', s=250, 
                            zorder=5, edgecolors='darkred', linewidths=2,
                            label='Delivery Points')

        # Add city names
        if self.show_names_var.get():
            for city in self.cities:
                self.ax_left.annotate(city.name, 
                                     (city.x, city.y),
                                     xytext=(8, 8),
                                     textcoords='offset points',
                                     fontsize=9,
                                     fontweight='bold',
                                     bbox=dict(boxstyle='round,pad=0.4', 
                                             facecolor='yellow', alpha=0.85,
                                             edgecolor='black', linewidth=0.8),
                                     zorder=15)

        # Add edge distances if enabled
        if self.show_distances_var.get() and len(self.cities) <= 8:
            for i in range(len(self.cities)):
                for j in range(i+1, len(self.cities)):
                    mid_x = (self.cities[i].x + self.cities[j].x) / 2
                    mid_y = (self.cities[i].y + self.cities[j].y) / 2
                    dist = self.distances[i][j]
                    self.ax_left.text(mid_x, mid_y, f'{dist:.1f}',
                                    fontsize=7, ha='center', va='center',
                                    bbox=dict(boxstyle='round,pad=0.2', 
                                            facecolor='white', alpha=0.8, 
                                            edgecolor='gray', linewidth=0.5))

        self.ax_left.set_xlabel('X Coordinate', fontsize=10)
        self.ax_left.set_ylabel('Y Coordinate', fontsize=10)
        self.ax_left.set_title('TSP Problem: Complete Graph\n(All Possible Routes)', 
                              fontsize=12, fontweight='bold', pad=10)
        self.ax_left.grid(True, alpha=0.3, linestyle='--')
        self.ax_left.legend(loc='upper right', fontsize=9)
        self.ax_left.axis('equal')

        # Add padding
        if len(x) > 0:
            x_margin = (max(x) - min(x)) * 0.12
            y_margin = (max(y) - min(y)) * 0.12
            self.ax_left.set_xlim(min(x) - x_margin, max(x) + x_margin)
            self.ax_left.set_ylim(min(y) - y_margin, max(y) + y_margin)

        self.fig_left.tight_layout()
        self.canvas_left.draw()

    def update_solution_plot(self):
        """Update right plot showing the optimal solution."""
        self.ax_right.clear()

        if not self.cities:
            self.ax_right.text(0.5, 0.5, 'Solve TSP to see\noptimal solution', 
                        ha='center', va='center', fontsize=12, color='gray')
            self.ax_right.set_xlim(0, 1)
            self.ax_right.set_ylim(0, 1)
            self.fig_right.tight_layout()
            self.canvas_right.draw()
            return

        x = [c.x for c in self.cities]
        y = [c.y for c in self.cities]

        # Draw all edges in light gray as background
        if self.show_all_edges_var.get():
            for i in range(len(self.cities)):
                for j in range(i+1, len(self.cities)):
                    self.ax_right.plot([self.cities[i].x, self.cities[j].x],
                                      [self.cities[i].y, self.cities[j].y],
                                      'lightgray', linewidth=0.5, alpha=0.2, zorder=1)

        if self.current_tour:
            # Draw optimal tour
            tour_x = [self.cities[i].x for i in self.current_tour]
            tour_y = [self.cities[i].y for i in self.current_tour]
            tour_x.append(self.cities[self.current_tour[0]].x)
            tour_y.append(self.cities[self.current_tour[0]].y)

            # Highlight the optimal route
            self.ax_right.plot(tour_x, tour_y, 'b-', linewidth=3.5, alpha=0.8, 
                             label='Optimal Route', zorder=3)

            # Add direction arrows
            for i in range(len(self.current_tour)):
                start_idx = self.current_tour[i]
                end_idx = self.current_tour[(i + 1) % len(self.current_tour)]

                dx = self.cities[end_idx].x - self.cities[start_idx].x
                dy = self.cities[end_idx].y - self.cities[start_idx].y

                mid_x = self.cities[start_idx].x + dx * 0.5
                mid_y = self.cities[start_idx].y + dy * 0.5

                self.ax_right.annotate('', xy=(mid_x + dx*0.08, mid_y + dy*0.08), 
                                      xytext=(mid_x, mid_y),
                                      arrowprops=dict(arrowstyle='->', color='blue', 
                                                    lw=2, alpha=0.8), zorder=4)

                # Show edge distances if enabled
                if self.show_distances_var.get():
                    dist = self.distances[start_idx][end_idx]
                    self.ax_right.text(mid_x, mid_y, f'{dist:.1f}',
                                     fontsize=8, ha='center', va='bottom',
                                     bbox=dict(boxstyle='round,pad=0.3', 
                                             facecolor='white', alpha=0.9, 
                                             edgecolor='blue', linewidth=1))

            # Highlight start/end
            start_city = self.cities[self.current_tour[0]]
            self.ax_right.scatter(start_city.x, start_city.y, c='green', s=700, 
                                 marker='*', zorder=10, edgecolors='darkgreen', 
                                 linewidths=3, label='Start/End', alpha=0.9)

            # Plot other cities
            other_x = [self.cities[i].x for i in self.current_tour[1:]]
            other_y = [self.cities[i].y for i in self.current_tour[1:]]
            self.ax_right.scatter(other_x, other_y, c='red', s=300, 
                                 zorder=5, edgecolors='darkred', linewidths=2.5,
                                 label='Delivery Points', alpha=0.9)

            # Add city names
            if self.show_names_var.get():
                for city in self.cities:
                    self.ax_right.annotate(city.name, 
                                          (city.x, city.y),
                                          xytext=(8, 8),
                                          textcoords='offset points',
                                          fontsize=9,
                                          fontweight='bold',
                                          bbox=dict(boxstyle='round,pad=0.4', 
                                                  facecolor='yellow', alpha=0.85,
                                                  edgecolor='black', linewidth=0.8),
                                          zorder=15)

            # Add visit order numbers
            if self.show_order_var.get():
                for i, city_id in enumerate(self.current_tour, 1):
                    city = self.cities[city_id]
                    self.ax_right.text(city.x, city.y, str(i),
                                     fontsize=11, fontweight='bold',
                                     ha='center', va='center', color='white',
                                     zorder=20)
        else:
            # No solution yet - show just the cities
            self.ax_right.scatter(x[0], y[0], c='green', s=600, marker='*', 
                                 zorder=10, edgecolors='darkgreen', linewidths=2,
                                 label='Warehouse')
            self.ax_right.scatter(x[1:], y[1:], c='red', s=250, 
                                 zorder=5, edgecolors='darkred', linewidths=2,
                                 label='Delivery Points')

            if self.show_names_var.get():
                for city in self.cities:
                    self.ax_right.annotate(city.name, 
                                          (city.x, city.y),
                                          xytext=(8, 8),
                                          textcoords='offset points',
                                          fontsize=9,
                                          fontweight='bold',
                                          bbox=dict(boxstyle='round,pad=0.4', 
                                                  facecolor='yellow', alpha=0.85,
                                                  edgecolor='black', linewidth=0.8),
                                          zorder=15)

        title = 'Optimal Solution'
        if self.current_tour:
            title += f' - Distance: {self.current_cost:.2f}'

        self.ax_right.set_xlabel('X Coordinate', fontsize=10)
        self.ax_right.set_ylabel('Y Coordinate', fontsize=10)
        self.ax_right.set_title(title, fontsize=12, fontweight='bold', pad=10)
        self.ax_right.grid(True, alpha=0.3, linestyle='--')
        self.ax_right.legend(loc='upper right', fontsize=9)
        self.ax_right.axis('equal')

        # Add padding
        if len(x) > 0:
            x_margin = (max(x) - min(x)) * 0.12
            y_margin = (max(y) - min(y)) * 0.12
            self.ax_right.set_xlim(min(x) - x_margin, max(x) + x_margin)
            self.ax_right.set_ylim(min(y) - y_margin, max(y) + y_margin)

        self.fig_right.tight_layout()
        self.canvas_right.draw()


def main():
    """Launch GUI application."""
    root = tk.Tk()
    app = TSPVisualizerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
