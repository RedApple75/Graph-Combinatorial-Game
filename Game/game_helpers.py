"""
Graph Combinatorial Game - Helper Functions
Node Kayles: Remove a node and all its neighbors. Last player to move wins.

This module contains all helper functions for:
- Graph generation and visualization
- Node removal mechanics
- Sprague-Grundy analysis
- N/P position visualization
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
from matplotlib.patches import Patch


# =============================================================================
# GRAPH GENERATION FUNCTIONS
# =============================================================================

def generate_random_graph(min_nodes=5, max_nodes=15, max_degree=3):
    """
    Generate a random graph with degree constraints.
    
    Args:
        min_nodes: Minimum number of nodes
        max_nodes: Maximum number of nodes  
        max_degree: Maximum degree per node
    
    Returns:
        NetworkX Graph
    """
    num_nodes = random.randint(min_nodes, max_nodes)
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    
    possible_edges = list(itertools.combinations(range(num_nodes), 2))
    random.shuffle(possible_edges)
    
    degrees = {i: 0 for i in range(num_nodes)}
    
    for u, v in possible_edges:
        if degrees[u] < max_degree and degrees[v] < max_degree:
            G.add_edge(u, v)
            degrees[u] += 1
            degrees[v] += 1
        if all(d >= max_degree for d in degrees.values()):
            break
    
    return G


def create_sample_graph():
    """Create a sample graph for demonstration."""
    G = nx.Graph()
    G.add_edges_from([
        ('A', 'B'), ('A', 'C'), ('B', 'D'),
        ('C', 'D'), ('C', 'E'), ('E', 'F'),
        ('G', 'H'), ('H', 'I'), ('I', 'G'),
        ('A', 'G')
    ])
    return G


def create_disconnected_graph():
    """Create a disconnected graph with multiple components."""
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 0),  # Triangle
        (3, 4), (4, 5),          # Path
        (6, 7)                    # Edge
    ])
    return G


# =============================================================================
# GRAPH VISUALIZATION FUNCTIONS
# =============================================================================

def draw_graph(G, title="Current Graph State"):
    """
    Visualize the graph with labeled nodes.
    
    Args:
        G: NetworkX graph
        title: Title for the plot
    """
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', 
            node_size=800, font_weight='bold', font_size=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def draw_graph_with_position(G, title="Graph", analyzer_class=None):
    """
    Draw graph with N/P position indicator in the corner.
    
    Args:
        G: NetworkX graph
        title: Title for the plot
        analyzer_class: SpragueGrundyAnalyzer class (passed to avoid circular import)
    
    Returns:
        Grundy number if graph has nodes, else None
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if len(G.nodes()) == 0:
        ax.text(0.5, 0.5, "Empty Graph", ha='center', va='center', 
                fontsize=20, transform=ax.transAxes)
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.show()
        return None
    
    # Draw the graph
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', 
            node_size=800, font_weight='bold', font_size=12)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Add N/P position indicator
    if analyzer_class is not None:
        analyzer = analyzer_class(G)
        grundy = analyzer.grundy()
        
        if grundy > 0:
            pos_text = f"N-position\n(G={grundy})"
            box_color = '#27AE60'  # Green
            status = "Player to move can WIN"
        else:
            pos_text = "P-position\n(G=0)"
            box_color = '#E74C3C'  # Red
            status = "Player to move will LOSE"
        
        # Add position box in top-right corner
        props = dict(boxstyle='round,pad=0.5', facecolor=box_color, alpha=0.9)
        ax.text(0.98, 0.98, pos_text, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', horizontalalignment='right',
                bbox=props, color='white', fontweight='bold')
        
        # Add status text below the graph
        ax.text(0.5, -0.05, status, transform=ax.transAxes, fontsize=12,
                ha='center', fontweight='bold', 
                color='green' if grundy > 0 else 'red')
        
        plt.tight_layout()
        plt.show()
        return grundy
    
    plt.tight_layout()
    plt.show()
    return None


# =============================================================================
# GAME MECHANICS FUNCTIONS
# =============================================================================

def remove_node(G, node):
    """
    Remove a single node from the graph (helper function).
    
    Args:
        G: NetworkX graph
        node: Node to remove
    
    Returns:
        True if successful, False otherwise
    """
    if node in G.nodes:
        G.remove_node(node)
        return True
    return False


def remove_node_and_neighbors(G, node, verbose=True):
    """
    Remove a node and all its adjacent neighbors from the graph.
    
    Args:
        G: NetworkX graph
        node: Node to remove
        verbose: If True, print removal info
    
    Returns:
        True if successful, False otherwise
    """
    if node not in G.nodes:
        if verbose:
            print(f"Node '{node}' not found in the graph.")
        return False
    
    neighbors = list(G.neighbors(node))
    G.remove_node(node)
    
    if verbose:
        print(f"Removed node: {node}")
    
    for neighbor in neighbors:
        if neighbor in G.nodes:
            G.remove_node(neighbor)
            if verbose:
                print(f"  → Also removed neighbor: {neighbor}")
    
    return True


# =============================================================================
# SPRAGUE-GRUNDY ANALYZER
# =============================================================================

def mex(s):
    """
    Minimum excludant: smallest non-negative integer not in set s.
    
    Args:
        s: Set of integers
    
    Returns:
        Smallest non-negative integer not in s
    """
    i = 0
    while i in s:
        i += 1
    return i


class SpragueGrundyAnalyzer:
    """
    Analyze graph game positions using Sprague-Grundy theorem.
    
    This class computes Grundy numbers (nimbers) for Node Kayles game positions,
    determining whether positions are N-positions (winning) or P-positions (losing).
    """
    
    def __init__(self, G):
        """
        Initialize analyzer with a graph.
        
        Args:
            G: NetworkX graph to analyze
        """
        self.original_graph = G.copy()
        self.nodes = tuple(sorted(G.nodes()))
        self.edges = set(G.edges())
        self.memo = {}  # Memoization for dynamic programming
        
    def _get_neighbors(self, node, remaining_nodes):
        """Get neighbors of a node within remaining nodes."""
        neighbors = []
        for n in remaining_nodes:
            if n != node and ((node, n) in self.edges or (n, node) in self.edges):
                neighbors.append(n)
        return neighbors
    
    def _get_next_states(self, state):
        """Get all possible next states from current state."""
        next_states = []
        remaining = set(state)
        
        for node in state:
            neighbors = set(self._get_neighbors(node, remaining))
            new_state = remaining - {node} - neighbors
            next_states.append(frozenset(new_state))
        
        return next_states
    
    def grundy(self, state=None):
        """
        Compute Grundy number for a game state using dynamic programming.
        
        Args:
            state: frozenset of remaining nodes (None = full graph)
        
        Returns:
            Grundy number (0 = P-position, >0 = N-position)
        """
        if state is None:
            state = frozenset(self.nodes)
        
        if len(state) == 0:
            return 0
        
        if state in self.memo:
            return self.memo[state]
        
        next_grundy_values = set()
        for next_state in self._get_next_states(state):
            next_grundy_values.add(self.grundy(next_state))
        
        g = mex(next_grundy_values)
        self.memo[state] = g
        return g
    
    def is_N_position(self, state=None):
        """Check if position is N-position (winning for player to move)."""
        return self.grundy(state) > 0
    
    def is_P_position(self, state=None):
        """Check if position is P-position (losing for player to move)."""
        return self.grundy(state) == 0
    
    def get_position_type(self, state=None):
        """Get position type as string."""
        g = self.grundy(state)
        if g > 0:
            return f"N-position (Grundy={g})"
        return "P-position (Grundy=0)"
    
    def get_winning_moves(self, state=None):
        """
        Find all winning moves from current position.
        
        Args:
            state: frozenset of remaining nodes (None = full graph)
        
        Returns:
            List of nodes that are winning moves
        """
        if state is None:
            state = frozenset(self.nodes)
        
        if self.is_P_position(state):
            return []
        
        winning_moves = []
        remaining = set(state)
        
        for node in state:
            neighbors = set(self._get_neighbors(node, remaining))
            new_state = remaining - {node} - neighbors
            
            if self.grundy(frozenset(new_state)) == 0:
                winning_moves.append(node)
        
        return winning_moves


# =============================================================================
# XOR ANALYSIS FOR DISCONNECTED COMPONENTS
# =============================================================================

def analyze_with_xor(G, verbose=True):
    """
    Analyze graph using XOR of independent components.
    
    For disconnected graphs: G(total) = G(comp1) ⊕ G(comp2) ⊕ ...
    
    Args:
        G: NetworkX graph
        verbose: If True, print analysis details
    
    Returns:
        Total Grundy number
    """
    components = list(nx.connected_components(G))
    
    if verbose:
        print(f"Graph has {len(components)} connected component(s)")
        print("-" * 40)
    
    component_grundy = []
    for i, comp_nodes in enumerate(components):
        subgraph = G.subgraph(comp_nodes).copy()
        analyzer = SpragueGrundyAnalyzer(subgraph)
        g = analyzer.grundy()
        component_grundy.append(g)
        if verbose:
            print(f"Component {i+1}: nodes={list(comp_nodes)}, Grundy={g}")
    
    total_grundy = 0
    for g in component_grundy:
        total_grundy ^= g
    
    if verbose:
        print("-" * 40)
        print(f"Total Grundy (XOR): {' ⊕ '.join(map(str, component_grundy))} = {total_grundy}")
        
        if total_grundy > 0:
            print("Result: N-position (Player 1 can WIN)")
        else:
            print("Result: P-position (Player 1 will LOSE)")
    
    return total_grundy


# =============================================================================
# N/P POSITION VISUALIZATION (CHESSBOARD GRID)
# =============================================================================

def get_path_grundy(max_size=12):
    """
    Compute Grundy numbers for path graphs of size 0 to max_size.
    
    Args:
        max_size: Maximum path size to compute
    
    Returns:
        Dictionary mapping path size to Grundy number
    """
    path_grundy = {0: 0}
    for n in range(1, max_size + 1):
        P = nx.path_graph(n)
        analyzer = SpragueGrundyAnalyzer(P)
        path_grundy[n] = analyzer.grundy()
    return path_grundy


def create_np_grid(max_size=12):
    """
    Create N/P position grid for two-path component games.
    
    Args:
        max_size: Maximum path size
    
    Returns:
        Tuple of (grid array, path_grundy dictionary)
    """
    path_grundy = get_path_grundy(max_size)
    grid = np.zeros((max_size + 1, max_size + 1))
    
    for i in range(max_size + 1):
        for j in range(max_size + 1):
            total_grundy = path_grundy[i] ^ path_grundy[j]
            grid[j, i] = 1 if total_grundy > 0 else 0
    
    return grid, path_grundy


def draw_chessboard_grid(grid, title='N/P Positions: Two-Path Component Game'):
    """
    Draw chessboard-style N/P position grid.
    
    Args:
        grid: 2D numpy array (0=P, 1=N)
        title: Title for the plot
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    rows, cols = grid.shape
    colors = {0: '#E74C3C', 1: '#27AE60'}  # Red=P, Green=N
    
    for i in range(cols):
        for j in range(rows):
            color = colors[int(grid[j, i])]
            rect = plt.Rectangle((i - 0.5, j - 0.5), 1, 1, 
                                  facecolor=color, edgecolor='black', linewidth=1.5)
            ax.add_patch(rect)
            label = 'N' if grid[j, i] == 1 else 'P'
            ax.text(i, j, label, ha='center', va='center', 
                   fontsize=11, fontweight='bold', color='white')
    
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(-0.5, rows - 0.5)
    ax.set_aspect('equal')
    ax.set_xlabel('Path 1 Size (nodes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Path 2 Size (nodes)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    
    # Add legend
    legend_elements = [
        Patch(facecolor='#27AE60', edgecolor='black', label='N-position (Player 1 WINS)'),
        Patch(facecolor='#E74C3C', edgecolor='black', label='P-position (Player 1 LOSES)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    plt.tight_layout()
    plt.show()


def show_np_grid(max_size=10):
    """
    Show the N/P position grid for two-path component games.
    
    Args:
        max_size: Maximum path size to show
    """
    print("Computing Grundy numbers for path graphs...")
    grid, path_grundy = create_np_grid(max_size)
    
    print("\nGrundy numbers for individual paths:")
    print("-" * 40)
    for size in range(max_size + 1):
        g = path_grundy[size]
        pos_type = "P" if g == 0 else "N"
        print(f"  Path P_{size}: Grundy = {g} ({pos_type}-position)")
    
    print("\nDisplaying N/P position grid...")
    draw_chessboard_grid(grid, f'N/P Positions: Two-Path Component Game\n(Grid size: {max_size}x{max_size})')
    
    print("""
INTERPRETATION:
• Each cell (m, n) = game with two disconnected paths: P_m and P_n
• GREEN (N): Player 1 can WIN with optimal play  
• RED (P): Player 1 will LOSE with optimal opponent play
• Result = G(P_m) ⊕ G(P_n) where G = Grundy number
""")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_game_rules():
    """Print the rules of the Node Kayles game."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    GRAPH COMBINATORIAL GAME                          ║
║                        (Node Kayles)                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  RULES:                                                              ║
║  • Two players take turns                                            ║
║  • On your turn, select a node to remove                             ║
║  • The selected node AND ALL ITS NEIGHBORS are removed               ║
║  • The player who removes the last node(s) WINS                      ║
║                                                                      ║
║  STRATEGY (Sprague-Grundy Theory):                                   ║
║  • N-position (Grundy > 0): Player to move can WIN                   ║
║  • P-position (Grundy = 0): Player to move will LOSE                 ║
║  • Winning strategy: Always move to a P-position                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")


def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

