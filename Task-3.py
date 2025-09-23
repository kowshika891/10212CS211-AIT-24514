def aStarAlgo(start_node, stop_node):
    open_set = set([start_node])
    closed_set = set()

    g = {}         # store distance from starting node
    parents = {}   # parents contain an adjacency map of all nodes

    g[start_node] = 0
    parents[start_node] = start_node

    while len(open_set) > 0:
        n = None

        # node with the lowest f() = g(n) + h(n)
        for v in open_set:
            if n is None or g[v] + heuristic(v) < g[n] + heuristic(n):
                n = v

        if n is None:
            print('Path does not exist!')
            return None

        # if the current node is the stop_node,
        # reconstruct the path
        if n == stop_node:
            path = []
            while parents[n] != n:
                path.append(n)
                n = parents[n]
            path.append(start_node)
            path.reverse()
            print('Path found:', path)
            return path

        # for all neighbors of current node
        for m, weight in get_neighbors(n):
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                g[m] = g[n] + weight
            else:
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n
                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        open_set.remove(n)
        closed_set.add(n)

    print('Path does not exist!')
    return None


# define function to return neighbors and their distances
def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        return None


# modified heuristic distances
def heuristic(n):
    h_dist = {
        'A': 11,
        'B': 6,
        'C': 4,   # lowered from 5 → favors path via C
        'D': 7,
        'E': 2,   # lowered from 3 → favors path via E
        'F': 10,  # increased to discourage F
        'G': 9,   # increased to discourage G
        'H': 8,   # increased to discourage H
        'I': 1,
        'J': 0
    }
    return h_dist[n]


# modified graph edges
Graph_nodes = {
    'A': [('B', 6), ('F', 20)],   # made F expensive (20 instead of 3)
    'B': [('A', 6), ('C', 3), ('D', 2)],
    'C': [('B', 3), ('D', 1), ('E', 5)],
    'D': [('B', 2), ('C', 1), ('E', 8)],
    'E': [('C', 5), ('D', 8), ('I', 5), ('J', 5)],
    'F': [('A', 20), ('G', 1), ('H', 7)],
    'G': [('F', 1), ('I', 3)],
    'H': [('F', 7), ('I', 2)],
    'I': [('E', 5), ('G', 3), ('H', 2), ('J', 3)],
}


# driver code
print("Following is the A* Algorithm:")
aStarAlgo('A', 'J')
