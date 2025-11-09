# 🚚 Delivery Route Optimizer — Interactive TSP Visual Dashboard


> **A modern Python dashboard for learning and optimizing delivery routes using classic Travelling Salesman Problem (TSP) algorithms — with easy-to-use controls, named city points, and beautiful graphical output!**

---

## 🏆 Features

- **Interactive Tkinter dashboard** — intuitive controls, dynamic updates
- **Graphical Visualization** — named cities, animated routes, and icons
- **Algorithms** — Brute Force (exact), Held-Karp DP, Nearest Neighbor, and 2-Opt
- **All Cities Connected** — see the complete TSP graph before/after solving!
- **Step-by-step tour info**, cost, and algorithm complexity
- **Support for custom and random city datasets** (CSV loading or generate)
- **Professional design** — clear panels, color scheme, hover info, and more

---

## 📂 Project Structure

project_root/
<br>
│
<br>
├── data/ # Store your .csv city datasets here
<br>
│ └── sample_cities.csv
<br>
│
<br>
├── src/
<br>
│ ├── gui_app.py # Main GUI dashboard (run this)
<br>
│ ├── main.py # CLI/extra launcher (if present)
<br>
│ ├── graph/ # Data & algorithm modules
<br>
│ ├── algorithms/ # TSP algorithm code
<br>
│ └── ... # Other supporting files
<br>
│
<br>
├── assets/ # Add your bike/package PNG icons here!
<br>
│ ├── bike.png # Starter icon (depot/delivery man)
<br>
│ ├── house.png # City icon (delivery location)
<br>
│ └── ...
<br>
│
<br>
├── README.md
<br>
├── requirements.txt
<br>
└── docs/
<br>
└── USER_GUIDE.md


text

---

## 🚀 Quick Start — Setup & Run

**Open your terminal or PowerShell and type:**

cd "C:\Users\visha\OneDrive\Desktop\Programming\Projects\delivery_route_optimizer\delivery_route_optimizer"
python -m src.gui_app

text

- You must be in the directory that **contains the `src/` folder**!
- Never run the file directly — always launch with `python -m src.gui_app`.

---

## 🖥️ What You Can Do

- **🗺️ Visualize** the full TSP problem: every city connected!
- **🔢 Label** and color-code each city (start, delivery points)
- **🚦 Solve** using different algorithms — watch route order and complexity in real time
- **🚚 Animate** a bike or delivery man along the optimal route (add PNGs in assets/)
- **📋 Export** and import city datasets (CSV)

---

## ⚡ How It Looks

| Before Solving            | After Solving                |
|---------------------------|------------------------------|
| ![](https://i.imgur.com/KOu6B8F.png) | ![](https://i.imgur.com/MSU14tD.png) |

> All cities connected? All possible routes? The blue path is the **best**!
> (Add your own icons for full effect!)

---

## 📥 Sample Data (data/sample_cities.csv)

id,x,y,name
0,10,20,Warehouse
1,25,35,CustomerA
2,50,55,CustomerB
3,80,30,CustomerC
4,40,10,CustomerD
5,65,50,CustomerE

text

---

## 🧑‍💻 Algorithm Complexity Reference

| Algorithm         | Time Complexity    | Space | Use For          |
|-------------------|-------------------|-------|------------------|
| Brute Force       | O(n!)             | O(n)  | n < 10           |
| Held-Karp DP      | O(n²·2ⁿ)          | O(n·2ⁿ)| n < 20           |
| Nearest Neighbor  | O(n²)             | O(n)  | Quick, Any size  |
| 2-Opt             | O(n³)             | O(n)  | Local improving  |

---

## 📦 Requirements

All necessary packages are listed in `requirements.txt`:
pip install -r requirements.txt

text
> *Tkinter is usually included with Python. Install Pillow and matplotlib if prompted.*

---

## 🪄 Customizations & Tips

- **🖼️ Add your PNGs:** Put `bike.png` and `house.png` in `assets/`, or use your favorite icons.
- **🗂️ Try your own data!** Save as `.csv` and load from GUI.
- **🔄 “Reset”** to try new city configurations. No restart needed.
- **🔬 See the difference!** Compare outputs of different algorithms visually.

---

## 🤝 Credits & Acknowledgments

- Created for academic/sports analytics and route learning.
- Uses [Matplotlib](https://matplotlib.org/), [Tkinter](https://docs.python.org/3/library/tkinter.html), [Pillow](https://python-pillow.org/).
- Free and open for educational re-use!

---

### ❓ Need Help?

- Can't run the GUI? Check "How to Run" above!
- Dataset or icon isn’t showing? Double-check folder and file locations.
- Still confused? Ask here for step-by-step CLI instructions!

---


> **Let's optimize delivery the smart way—visually!**

