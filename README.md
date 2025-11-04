# Graph Removal Game: A Combinatorial Analysis

## 🧩 Overview
The **Graph Removal Game** is a two-player impartial game played on an undirected graph.  
When a player removes a vertex, all its adjacent vertices and incident edges are also deleted.  
The player who cannot make a move loses (normal play convention).  
This project uses **Combinatorial Game Theory** (Sprague–Grundy theorem) to compute Grundy numbers, identify P- and N-positions, and visualize game dynamics.

## ⚙️ Features
- Interactive gameplay using `NetworkX` and `matplotlib`
- Recursive computation of Grundy numbers with memoization
- Analysis for standard graph families (paths, cycles, stars, trees)
- Visualization of winning vs losing positions
- Extensible framework for exploring new graph-based games

## 🧠 Rules of the Game
1. The game starts with an undirected graph \( G = (V, E) \).  
2. On each turn, a player selects one vertex \( v \).  
3. The chosen vertex and **all its adjacent vertices** are removed along with their edges.  
4. If no vertices remain to remove, the player who cannot move **loses**.  
5. Both players have the same set of moves (impartial game).

## 🧮 Methodology
- **Graph Representation:** `NetworkX` graphs.  
- **Computation:** Recursive Grundy number calculation using `functools.lru_cache`.  
- **Decomposition:** Connected components are treated as independent subgames (XOR rule).  
- **Visualization:** Live graph updates after each move with color-coded nodes.

## 🚀 Installation
```bash
git clone https://github.com/<your-username>/graph-removal-game.git
cd graph-removal-game
pip install -r requirements.txt
