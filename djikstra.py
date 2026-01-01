graph = {
    'A': [('M',20), ('S',28), ('B',25), ('C',36)],
    'B': [('M',16), ('S',24), ('F',28)],
    'C': [('M',30), ('R',11), ('T',27)],
    'R': [('M',22), ('F',14)],
    'T': [('F',22), ('H',35)],
    'F': [('H',30), ('O',42)],
    'H': [('O',11)],
    'M': [],
    'S': [],
    'O': []
}

nodes = list(graph.keys())
node_index = {node: i for i, node in enumerate(nodes)}

def dijkstra(graphe, s):
    n = len(graphe)
    L = [float('inf')] * n
    P = ["-"] * n
    M = [False] * n
    L[s] = 0
    P[s] = s
    c = s
    while True:
        M[c] = True
        for v_node, p in graphe[nodes[c]]:
            v = node_index[v_node]
            if not M[v]:
                nd = L[c] + p
                if nd < L[v]:
                    L[v] = nd
                    P[v] = c
        md = float('inf')
        nv = -1
        for i in range(n):
            if not M[i] and L[i] < md:
                md = L[i]
                nv = i
        if nv == -1:
            break
        c = nv
    return L, P

def chemin_plus_court(P, destination, nodes):
    chemin = []
    current = destination
    while current != "-":
        chemin.insert(0, nodes[current])
        if P[current] == current:
            break
        current = P[current]
    return chemin

source = node_index['C']
distances, predecessors = dijkstra(graph, source)

print("Distances minimales depuis C :")
for i, d in enumerate(distances):
    print(f"{nodes[i]} : {d}")

print("\nPlus courts chemins depuis C :")
for i in range(len(nodes)):
    if i != source:
        chemin = chemin_plus_court(predecessors, i, nodes)
        if chemin:
            print(f"C -> {nodes[i]} : {' -> '.join(chemin)}")
        else:
            print(f"C -> {nodes[i]} : Aucun chemin")
