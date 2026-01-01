graph = {
    'A': [('M',20), ('S',28), ('B',25), ('C',36)],
    'B': [('M',16), ('S',24), ('F',28)],
    'C': [('M',30), ('R',11), ('T',27)],
    'R': [('M',22), ('F',14)],
    'T': [('F',22), ('H',35)],
    'F': [('H',30), ('O',42)],
    'H': [('O',11)],
    'M': [],
    'S': [('E',-5)],
    'O': [],
    'E': []
}

def bellman_ford(graph, source):
    L = {v: float('inf') for v in graph}
    P = {v: None for v in graph}
    L[source] = 0
    P[source] = source
    continue_flag = True
    
    while continue_flag:
        continue_flag = False
        for x in graph:
            for y, weight in graph[x]:
                if L[x] + weight < L[y]:
                    L[y] = L[x] + weight
                    P[y] = x
                    continue_flag = True
    return L, P

def chemin_plus_court(predecessors, destination):
    chemin = []
    current = destination
    while current is not None and predecessors[current] is not None:
        chemin.insert(0, current)
        if current == predecessors[current]:
            break
        current = predecessors[current]
    return chemin

distances, predecessors = bellman_ford(graph, 'C')

print("Distances minimales depuis C :")
for v in distances:
    print(f"{v} : {distances[v]}")

print("\nPrédécesseurs pour le plus court chemin depuis C :")
for v in predecessors:
    print(f"{v} : {predecessors[v]}")

print("\nPlus courts chemins depuis C :")
for v in graph:
    if v != 'C':
        chemin = chemin_plus_court(predecessors, v)
        if chemin:
            print(f"C -> {v} : {' -> '.join(chemin)}")
        else:
            print(f"C -> {v} : Aucun chemin")
