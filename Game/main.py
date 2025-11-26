"""
Graph Combinatorial Game - Main Program
Node Kayles: Remove a node and all its neighbors. Last player to move wins.

Run this file to play the game with various options.
"""

import networkx as nx
from game_helpers import (
    # Graph generation
    generate_random_graph,
    create_sample_graph,
    create_disconnected_graph,
    # Visualization
    draw_graph,
    draw_graph_with_position,
    # Game mechanics
    remove_node_and_neighbors,
    # Analysis
    SpragueGrundyAnalyzer,
    analyze_with_xor,
    # N/P grid
    show_np_grid,
    # Utilities
    print_game_rules,
    clear_screen
)


def print_menu():
    """Print the main menu."""
    print("""
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
""")


def play_game(G, game_name="Game"):
    """
    Play the Node Kayles game on a given graph.
    
    Args:
        G: NetworkX graph to play on
        game_name: Name of the game for display
    """
    G_initial = G.copy()
    
    print("\n" + "=" * 60)
    print(f"GAME START: {game_name}")
    print("=" * 60)
    
    # Analyze initial position
    analyzer = SpragueGrundyAnalyzer(G_initial)
    initial_grundy = analyzer.grundy()
    winning_moves = analyzer.get_winning_moves()
    
    print(f"\nGraph: {len(G.nodes())} nodes, {len(G.edges())} edges")
    print(f"Nodes: {sorted(G.nodes())}")
    print(f"\nInitial Grundy Number: {initial_grundy}")
    
    if initial_grundy > 0:
        print(f"Initial Position: N-position → Player 1 can WIN!")
        print(f"Winning moves for Player 1: {winning_moves}")
    else:
        print(f"Initial Position: P-position → Player 1 will LOSE with optimal play")
    
    # Show initial graph with position indicator
    draw_graph_with_position(G, f"INITIAL GRAPH - {game_name}", SpragueGrundyAnalyzer)
    
    # Game loop
    players = ["Player 1", "Player 2"]
    turn = 0
    
    while len(G.nodes) > 0:
        current_player = players[turn % 2]
        print(f"\n{'='*60}")
        print(f"{current_player}'s turn")
        print("=" * 60)
        print(f"Available nodes: {sorted(G.nodes)}")
        
        # Show current position analysis
        if len(G.nodes) > 0:
            temp_analyzer = SpragueGrundyAnalyzer(G)
            current_grundy = temp_analyzer.grundy()
            current_winning = temp_analyzer.get_winning_moves()
            
            if current_grundy > 0:
                print(f"Current position: N-position (Grundy={current_grundy})")
                print(f"Winning moves: {current_winning}")
            else:
                print(f"Current position: P-position (Grundy=0)")
                print("No winning moves - any move leads to N-position for opponent")
        
        # Get player input
        while True:
            node_input = input("\nEnter a node to remove (or 'q' to quit): ").strip()
            
            if node_input.lower() == 'q':
                print("\nGame aborted.")
                return
            
            # Handle integer nodes
            try:
                node = int(node_input)
            except ValueError:
                node = node_input
            
            if node in G.nodes:
                break
            print("Invalid node. Try again.")
        
        # Make the move
        remove_node_and_neighbors(G, node)
        
        # Check for game end
        if len(G.nodes) == 0:
            print(f"\n{'='*60}")
            print(f"🎉 {current_player} removed the last node(s) and WINS!")
            print("=" * 60)
            break
        
        # Show updated graph
        draw_graph_with_position(G, f"After {current_player} removed '{node}'", SpragueGrundyAnalyzer)
        turn += 1
    
    print("\nGame Over!")
    input("\nPress Enter to continue...")


def play_random_game():
    """Play a game with a randomly generated graph."""
    print("\n" + "=" * 60)
    print("RANDOM GRAPH GENERATOR")
    print("=" * 60)
    
    # Get parameters from user
    try:
        min_nodes = int(input("Minimum nodes (default 5): ") or "5")
        max_nodes = int(input("Maximum nodes (default 12): ") or "12")
        max_degree = int(input("Maximum degree per node (default 3): ") or "3")
    except ValueError:
        print("Invalid input. Using defaults.")
        min_nodes, max_nodes, max_degree = 5, 12, 3
    
    # Generate graph
    G = generate_random_graph(min_nodes, max_nodes, max_degree)
    play_game(G, f"Random Graph ({len(G.nodes())} nodes)")


def play_custom_game():
    """Play a game with a predefined custom graph."""
    G = create_sample_graph()
    play_game(G, "Custom Graph")


def analyze_graph():
    """Analyze a graph and show N/P position with winning moves."""
    print("\n" + "=" * 60)
    print("GRAPH ANALYZER")
    print("=" * 60)
    
    print("\nChoose graph type:")
    print("  1. Random graph")
    print("  2. Sample graph (predefined)")
    print("  3. Custom edges (enter manually)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        try:
            num_nodes = int(input("Number of nodes (default 8): ") or "8")
        except ValueError:
            num_nodes = 8
        G = generate_random_graph(num_nodes, num_nodes, 3)
    elif choice == "2":
        G = create_sample_graph()
    elif choice == "3":
        G = nx.Graph()
        print("\nEnter edges (format: 'A B' or '1 2'), empty line to finish:")
        while True:
            edge_input = input("Edge: ").strip()
            if not edge_input:
                break
            try:
                parts = edge_input.split()
                if len(parts) == 2:
                    # Try to convert to int, otherwise keep as string
                    try:
                        u, v = int(parts[0]), int(parts[1])
                    except ValueError:
                        u, v = parts[0], parts[1]
                    G.add_edge(u, v)
                    print(f"  Added edge: {u} -- {v}")
            except Exception as e:
                print(f"  Invalid edge format: {e}")
        
        if len(G.nodes()) == 0:
            print("No edges entered. Using sample graph.")
            G = create_sample_graph()
    else:
        print("Invalid choice. Using sample graph.")
        G = create_sample_graph()
    
    # Show and analyze the graph
    print("\n" + "-" * 60)
    print("ANALYSIS RESULT")
    print("-" * 60)
    
    print(f"\nNodes ({len(G.nodes())}): {sorted(G.nodes())}")
    print(f"Edges ({len(G.edges())}): {list(G.edges())}")
    
    analyzer = SpragueGrundyAnalyzer(G)
    grundy = analyzer.grundy()
    winning_moves = analyzer.get_winning_moves()
    
    print(f"\nGrundy Number: {grundy}")
    
    if grundy > 0:
        print(f"Position Type: N-position")
        print(f"  → Player 1 (first to move) can WIN!")
        print(f"  → Winning moves: {winning_moves}")
    else:
        print(f"Position Type: P-position")
        print(f"  → Player 1 will LOSE with optimal opponent play")
        print(f"  → No winning moves available")
    
    # Show graph with position indicator
    draw_graph_with_position(G, "Graph Analysis", SpragueGrundyAnalyzer)
    
    input("\nPress Enter to continue...")


def show_np_visualization():
    """Show the N/P position chessboard grid."""
    print("\n" + "=" * 60)
    print("N/P POSITION GRID VISUALIZATION")
    print("=" * 60)
    
    print("""
This shows N/P positions for games with TWO disconnected path components.
Each cell (m, n) represents a game with: Path₁ (m nodes) + Path₂ (n nodes)
""")
    
    try:
        max_size = int(input("Grid size (default 10, max 15): ") or "10")
        max_size = min(max_size, 15)  # Limit to prevent long computation
    except ValueError:
        max_size = 10
    
    show_np_grid(max_size)
    
    input("\nPress Enter to continue...")


def analyze_disconnected():
    """Analyze a disconnected graph using XOR decomposition."""
    print("\n" + "=" * 60)
    print("DISCONNECTED GRAPH ANALYZER (XOR)")
    print("=" * 60)
    
    print("\nChoose graph type:")
    print("  1. Random disconnected graph")
    print("  2. Sample disconnected graph")
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        # Create a random disconnected graph with multiple components
        G = nx.Graph()
        num_components = 3
        
        for c in range(num_components):
            # Create a small random component
            comp_size = 2 + c
            start_node = c * 10
            nodes = list(range(start_node, start_node + comp_size))
            G.add_nodes_from(nodes)
            
            # Add some edges within component
            for i in range(len(nodes) - 1):
                G.add_edge(nodes[i], nodes[i + 1])
    else:
        G = create_disconnected_graph()
    
    # Show the graph
    print(f"\nGraph: {len(G.nodes())} nodes, {len(G.edges())} edges")
    draw_graph(G, "Disconnected Graph")
    
    # Analyze with XOR
    print("\n" + "-" * 60)
    print("XOR ANALYSIS")
    print("-" * 60)
    analyze_with_xor(G)
    
    input("\nPress Enter to continue...")


def main():
    """Main program loop."""
    while True:
        clear_screen()
        print_menu()
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            play_random_game()
        elif choice == "2":
            play_custom_game()
        elif choice == "3":
            analyze_graph()
        elif choice == "4":
            show_np_visualization()
        elif choice == "5":
            analyze_disconnected()
        elif choice == "6":
            clear_screen()
            print_game_rules()
            input("\nPress Enter to continue...")
        elif choice == "7":
            print("\nThanks for playing! Goodbye.")
            break
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

