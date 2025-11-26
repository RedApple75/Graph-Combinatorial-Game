"""
simple main for nodepocalypse
short names, crude style, minimal comments
"""

import networkx as nx
from game_helpers import (
    gen_graph,
    sample_graph,
    draw,
    draw_with_pos,
    remove_node_and_neighbors,
    SG
)

def menu():
    print("NODEPOCALYPSE")
    print("1. play random graph")
    print("2. play sample graph")
    print("3. analyze graph (enter edges)")
    print("4. exit")

def play(g, name="game"):
    """play loop on graph g"""
    gg = g.copy()
    print("starting", name, "nodes:", len(gg.nodes()))
    sgan = SG(gg)
    g0 = sgan.grundy()
    print("initial grundy:", g0)
    if g0 > 0:
        print("initial: N-position (first can win)")
        print("winning moves:", sgan.winning_moves())
    else:
        print("initial: P-position (first will lose if opponent plays well)")
    draw_with_pos(gg, "initial "+name)

    players = ["p1", "p2"]
    turn = 0
    while len(gg.nodes()) > 0:
        cur = players[turn % 2]
        print("\nturn:", cur)
        print("nodes:", sorted(gg.nodes()))
        s = SG(gg)
        gnow = s.grundy()
        print("grundy now:", gnow)
        if gnow > 0:
            print("winning moves:", s.winning_moves())
        else:
            print("no winning moves")

        choice = input("enter node to remove (or q to quit): ").strip()
        if choice.lower() == 'q':
            print("aborted")
            return
        # try to parse int, else leave as string
        try:
            node = int(choice)
        except:
            node = choice
        if node not in gg.nodes():
            print("invalid node")
            continue
        remove_node_and_neighbors(gg, node)
        if len(gg.nodes()) == 0:
            print(cur, "wins")
            break
        draw_with_pos(gg, "after "+str(node))
        turn += 1

    print("game over")

def play_rand():
    mn = input("min nodes (default 5): ").strip()
    mx = input("max nodes (default 10): ").strip()
    md = input("max degree (default 3): ").strip()
    try:
        mn = int(mn) if mn else 5
        mx = int(mx) if mx else 10
        md = int(md) if md else 3
    except:
        mn, mx, md = 5,10,3
    g = gen_graph(mn, mx, md)
    play(g, "random")

def play_sample():
    g = sample_graph()
    play(g, "sample")

def analyze():
    print("build graph by entering edges like 'a b' or '1 2'. empty line to finish")
    g = nx.Graph()
    while True:
        s = input("edge: ").strip()
        if s == "":
            break
        parts = s.split()
        if len(parts) != 2:
            print("bad input")
            continue
        a, b = parts[0], parts[1]
        try:
            a = int(a)
            b = int(b)
        except:
            pass
        g.add_edge(a, b)
        print("added", a, b)
    print("nodes:", sorted(g.nodes()))
    print("edges:", list(g.edges()))
    s = SG(g)
    gg = s.grundy()
    print("grundy:", gg)
    if gg > 0:
        print("N-position, winning moves:", s.winning_moves())
    else:
        print("P-position")
    draw_with_pos(g, "analyzed graph")

def main():
    while True:
        menu()
        c = input("choice: ").strip()
        if c == "1":
            play_rand()
        elif c == "2":
            play_sample()
        elif c == "3":
            analyze()
        elif c == "4":
            print("bye")
            break
        else:
            print("bad choice")

if __name__ == "__main__":
    main()
