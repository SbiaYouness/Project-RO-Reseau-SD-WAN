# Shortest Path Finder - Operations Research Project

A professional Streamlit web application for finding optimal paths between cities using Dijkstra and Bellman-Ford algorithms.

## 🚀 Features

- **Interactive UI**: Select start and destination cities via dropdown menus
- **Multiple Algorithms**: Choose between Dijkstra, Bellman-Ford, or compare both
- **Visual Graph**: NetworkX-powered graph visualization with highlighted paths
- **Detailed Results**: View total latency, number of hops, execution time, and step-by-step routes
- **Performance Comparison**: Side-by-side algorithm comparison with metrics

## 📋 Prerequisites

- Python 3.11+
- Virtual environment (included)

## 🔧 Installation & Setup

1. **Activate the virtual environment** (already created):

```powershell
.\.venv\Scripts\Activate.ps1
```

2. **Install dependencies** (if not already installed):

```powershell
pip install -r requirements.txt
```

## ▶️ Running the Application

```powershell
streamlit run app.py
```

The application will open automatically in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
Projet R.O/
├── app.py                  # Main Streamlit application
├── graph_algorithms.py     # Graph class with Dijkstra & Bellman-Ford
├── requirements.txt        # Python dependencies
├── djikstra.py            # Original Dijkstra implementation
├── bellman_ford.py        # Original Bellman-Ford implementation
├── MatriceAdj.py          # Matrix adjacency operations
└── README.md              # This file
```

## 🎯 How to Use

1. **Select Cities**: Use the sidebar to choose your start and destination cities
2. **Choose Algorithm**: Pick Dijkstra, Bellman-Ford, or compare both
3. **Find Path**: Click "Find Shortest Path" button
4. **View Results**: See the optimal route, latency, and visualization

## 🧮 Algorithms

### Dijkstra's Algorithm

- Best for graphs with non-negative weights
- Greedy approach with priority queue
- Time complexity: O((V+E)log V)

### Bellman-Ford Algorithm

- Can handle negative weights
- Dynamic programming approach
- Time complexity: O(V×E)

## 🗺️ Graph Structure

The network consists of 10 cities (A, B, C, M, R, T, F, H, S, O) connected by weighted edges representing latency values.

## 👨‍💻 Author

Operations Research Project - 2026

## 📄 License

Academic project for educational purposes.
