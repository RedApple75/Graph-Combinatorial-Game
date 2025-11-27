"""
helper functions for the nodepocalypse game
simple, short names and minimal comments
NOW WITH XOR OPTIMIZATION FOR DISCONNECTED COMPONENTS
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import math
from matplotlib.patches import FancyArrowPatch

# graph gen

def gen_graph(min_n=5, max_n=12, max_deg=3):
    """
    generate random graph, prefer short edges (nearby nodes)
    nodes get a 'pos' attribute (random in unit square)
    """
    if min_n == max_n:
        n = min_n
    else:
        n = random.randint(min_n, max_n)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    pos = {i: (random.random(), random.random()) for i in range(n)}
    nx.set_node_attributes(g, pos, "pos")

    edges = []
    for u, v in itertools.combinations(range(n), 2):
        ux, uy = pos[u]
        vx, vy = pos[v]
        d = math.hypot(ux - vx, uy - vy)
        edges.append((d, u, v))
    edges.sort(key=lambda x: x[0])

    deg = {i: 0 for i in range(n)}
    for d, u, v in edges:
        if deg[u] < max_deg and deg[v] < max_deg:
            g.add_edge(u, v)
            deg[u] += 1
            deg[v] += 1
        if all(x >= max_deg for x in deg.values()):
            break

    return g

def sample_graph():
    """small sample graph"""
    g = nx.Graph()
    g.add_edges_from([
        ('A','B'), ('A','C'), ('B','D'),
        ('C','D'), ('C','E'), ('E','F'),
        ('G','H'), ('H','I'), ('I','G'),
        ('A','G')
    ])
    return g

# layout and draw

def _rand_spread(g, w=10.0, h=8.0, min_d=0.9, reps=250, pull=0.06):
    """
    random-ish positions then simple repulsion + small edge pull
    w,h: box size
    min_d: desired min distance between nodes
    reps: number of repulsion iterations
    pull: tiny attraction along edges to keep neighbors close
    """
    n = len(g)
    if n == 0:
        return {}

    # start from stored pos if present, else uniform random
    old = nx.get_node_attributes(g, "pos")
    pos = {}
    for i, nd in enumerate(g.nodes()):
        if nd in old:
            x, y = old[nd]
            # scale stored pos into box roughly
            pos[nd] = ( (x % 1.0) * w, (y % 1.0) * h )
        else:
            pos[nd] = (random.random() * w, random.random() * h)

    # crude repulsion iterations
    nodes = list(g.nodes())
    for it in range(reps):
        # small random jitter so system doesn't lock into bad sym
        for nd in nodes:
            jx = (random.random() - 0.5) * 0.01
            jy = (random.random() - 0.5) * 0.01
            x, y = pos[nd]
            pos[nd] = (x + jx, y + jy)

        # repel pairs that are too close
        for i in range(n):
            u = nodes[i]
            ux, uy = pos[u]
            for j in range(i+1, n):
                v = nodes[j]
                vx, vy = pos[v]
                dx = ux - vx
                dy = uy - vy
                dist = math.hypot(dx, dy) + 1e-6
                if dist < min_d:
                    # push them apart a bit (crude)
                    need = (min_d - dist) * 0.5
                    nx_u = ux + (dx/dist) * need
                    ny_u = uy + (dy/dist) * need
                    nx_v = vx - (dx/dist) * need
                    ny_v = vy - (dy/dist) * need
                    pos[u] = (nx_u, ny_u)
                    pos[v] = (nx_v, ny_v)
                    ux, uy = pos[u]  # update for next pairs

        # pull neighbors slightly together so edges look short
        for (a, b) in g.edges():
            ax, ay = pos[a]
            bx, by = pos[b]
            dx = bx - ax
            dy = by - ay
            # move each a bit towards the other
            pos[a] = (ax + dx * pull, ay + dy * pull)
            pos[b] = (bx - dx * pull, by - dy * pull)

    return pos


def draw(g, title="graph"):
    """
    draw graph using straight edges and spread random positions
    """
    fig = plt.figure(figsize=(9,7))
    ax = fig.gca()
    ax.clear()

    pos = _rand_spread(g, w=10.0, h=8.0, min_d=0.9, reps=250, pull=0.05)

    # draw straight edges then nodes/labels on top
    nx.draw_networkx_edges(g, pos, ax=ax, width=1.2, alpha=0.9)
    nx.draw_networkx_nodes(g, pos, ax=ax, node_color='lightblue',
                           node_size=650, edgecolors='k')
    nx.draw_networkx_labels(g, pos, ax=ax, font_weight='bold', font_size=10)

    ax.set_title(title)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


def draw_with_pos(g, title="graph"):
    """
    same as draw (kept for compatibility)
    """
    fig, ax = plt.subplots(figsize=(9,7))
    ax.clear()

    if len(g.nodes()) == 0:
        ax.text(0.5, 0.5, "empty graph", ha='center', va='center')
        ax.set_title(title)
        plt.show()
        return

    pos = _rand_spread(g, w=10.0, h=8.0, min_d=0.9, reps=250, pull=0.05)

    nx.draw_networkx_edges(g, pos, ax=ax, width=1.2, alpha=0.9)
    nx.draw_networkx_nodes(g, pos, ax=ax, node_color='lightblue',
                           node_size=650, edgecolors='k')
    nx.draw_networkx_labels(g, pos, ax=ax, font_weight='bold', font_size=10)

    ax.set_title(title)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
# game mechanics

def remove_node_and_neighbors(g, node, verbose=True):
    """
    remove node and its neighbors (in place)
    """
    if node not in g.nodes():
        if verbose:
            print("no such node")
        return False
    nb = list(g.neighbors(node))
    g.remove_node(node)
    if verbose:
        print("removed", node)
    for n in nb:
        if n in g.nodes():
            g.remove_node(n)
            if verbose:
                print(" also removed", n)
    return True

# sprague-grundy analyzer (naive recursive + memo + XOR optimization)
def mex(s):
    i = 0
    while i in s:
        i += 1
    return i

class SG:
    """
    simple sprague-grundy analyzer with XOR optimization
    use SG(g).grundy() or .winning_moves()
    """
    def __init__(self, g, use_xor=True):
        self.g = g.copy()
        self.nodes = tuple(sorted(self.g.nodes()))
        self.edges = set(self.g.edges())
        self.memo = {}
        self.use_xor = use_xor
        # stats for analysis
        self.xor_hits = 0
        self.recursive_calls = 0

    def _nbrs(self, node, rem):
        out = []
        for n in rem:
            if n != node and ((node,n) in self.edges or (n,node) in self.edges):
                out.append(n)
        return out

    def _find_components(self, state):
        """find connected components in subgraph induced by state"""
        rem = set(state)
        visited = set()
        comps = []
        
        for node in state:
            if node in visited:
                continue
            # bfs to find component
            comp = set()
            queue = [node]
            while queue:
                curr = queue.pop(0)
                if curr in visited:
                    continue
                visited.add(curr)
                comp.add(curr)
                # add neighbors that are still in state
                for nb in self._nbrs(curr, rem):
                    if nb not in visited:
                        queue.append(nb)
            comps.append(frozenset(comp))
        
        return comps

    def _next_states(self, state):
        out = []
        rem = set(state)
        for node in state:
            nb = set(self._nbrs(node, rem))
            new = rem - {node} - nb
            out.append(frozenset(new))
        return out

    def grundy(self, state=None):
        self.recursive_calls += 1
        
        if state is None:
            state = frozenset(self.nodes)
        if len(state) == 0:
            return 0
        if state in self.memo:
            return self.memo[state]
        
        # XOR optimization: check for disconnected components
        if self.use_xor:
            comps = self._find_components(state)
            if len(comps) > 1:
                self.xor_hits += 1
                xor_val = 0
                for comp in comps:
                    xor_val ^= self.grundy(comp)
                self.memo[state] = xor_val
                return xor_val
        
        # standard recursive logic
        vals = set()
        for ns in self._next_states(state):
            vals.add(self.grundy(ns))
        g = mex(vals)
        self.memo[state] = g
        return g

    def winning_moves(self, state=None):
        if state is None:
            state = frozenset(self.nodes)
        if self.grundy(state) == 0:
            return []
        out = []
        rem = set(state)
        for node in state:
            nb = set(self._nbrs(node, rem))
            new = rem - {node} - nb
            if self.grundy(frozenset(new)) == 0:
                out.append(node)
        return out