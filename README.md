# Graph Game (Node Kayles)

This program lets two players play a simple strategy game on a graph. On each turn, a player picks a node, and that node plus all its neighbors get removed. The game ends when no nodes remain, and the player who made the last move wins. Even though the rules are short, the game can get interesting on larger graphs.

## Files
- main.py — runs the menu, handles input, and controls the game loop
- game_helpers.py — functions for drawing graphs, generating random graphs, removing nodes, and computing Grundy values
- README.md — this file

## Requirements
Install the following before running:
pip install networkx matplotlib numpy

## How to Run
Run the program with:
python main.py

## What the Program Does
When it starts, a basic menu appears:

1. play a random graph  
2. play a sample graph  
3. type in your own edges and analyze the graph  
4. exit  

Graphs are drawn in a window using matplotlib. Moves update the drawing so you can see the game progress visually. The program also prints out the Grundy value of the current position and any winning moves it detects.

## Game Rules
- players alternate turns  
- on your turn, choose any node still in the graph  
- that node and all its neighbors are removed  
- the player who causes the graph to become empty wins  

## Grundy Values (short explanation)
The program computes a Grundy value for the current graph. This comes from combinatorial game theory but is simple to interpret:

- Grundy > 0 → the position is winning for the player to move  
- Grundy = 0 → the position is losing if both players play optimally  

The program also prints which nodes are “winning moves” (moves that force the Grundy value to become 0 for the opponent).

## Creating Your Own Graph
You can enter edges manually like:
a b
1 4
x y
(press Enter on a blank line to finish)

The program builds the graph, shows it, and prints the Grundy value and winning moves.

## Example Session
nodes: [0, 1, 2, 3, 4]  
grundy now: 2  
winning moves: [1, 3]  
enter node to remove: 1  
removed 1  
also removed 0  
also removed 2  

The graph then redraws to show what remains.

## Notes
This project was made for a course assignment. The code is intentionally simple: short variable names, direct loops, and minimal extra structure, so it’s easy to read and change. The focus is on implementing the rules, showing the graph clearly, and computing the Grundy values without relying on advanced frameworks.
