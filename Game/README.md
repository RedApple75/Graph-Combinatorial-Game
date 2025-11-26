# Graph Combinatorial Game (Node Kayles)

A two-player turn-based game played on graphs where players remove nodes along with all adjacent neighbors. The player who removes the last node(s) wins.

## Files

| File | Description |
|------|-------------|
| `main.py` | Main program with interactive menu |
| `game_helpers.py` | Helper functions and classes |
| `game_mechanics.ipynb` | Jupyter notebook version |

## Requirements

```bash
pip install networkx matplotlib numpy
```

## How to Run

```bash
python main.py
```

## Menu Options

```
╔══════════════════════════════════════════════════════════════════════╗
║                    GRAPH COMBINATORIAL GAME                          ║
║                        (Node Kayles)                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   1. Play game with RANDOM graph                                     ║
║   2. Play game with CUSTOM graph (predefined)                        ║
║   3. Analyze a graph (show N/P position & winning moves)             ║
║   4. Show N/P position grid (chessboard visualization)               ║
║   5. Analyze disconnected graph (XOR decomposition)                  ║
║   6. Show game rules                                                 ║
║   7. Exit                                                            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

## Game Rules

1. Two players take turns
2. On your turn, select a node to remove
3. The selected node **AND ALL ITS NEIGHBORS** are removed
4. The player who removes the last node(s) **WINS**

## Sprague-Grundy Theory

- **N-position** (Grundy > 0): Player to move can WIN with optimal play
- **P-position** (Grundy = 0): Player to move will LOSE with optimal opponent play
- **Winning Strategy**: Always move to a P-position

### XOR Property

For disconnected graphs with multiple components:
```
G(total) = G(component₁) ⊕ G(component₂) ⊕ ... ⊕ G(componentₙ)
```

## Features

- ✅ Real-time N/P position indicator on graph
- ✅ Winning moves suggestion
- ✅ Random graph generation
- ✅ Sprague-Grundy analysis
- ✅ XOR decomposition for disconnected graphs
- ✅ N/P position chessboard visualization (like Nim)

## Example Usage

### Playing a Game

```
============================================================
GAME START: Random Graph (8 nodes)
============================================================

Graph: 8 nodes, 11 edges
Nodes: [0, 1, 2, 3, 4, 5, 6, 7]

Initial Grundy Number: 2
Initial Position: N-position → Player 1 can WIN!
Winning moves for Player 1: [3, 5]
```

### N/P Position Grid

The chessboard grid shows N/P positions for games with two path components:
- **Green (N)**: Player 1 wins
- **Red (P)**: Player 1 loses

## Author

IE211 - Graph Combinatorial Game Project

