"""
Graph algorithms module for shortest path calculations.
Contains implementations of Dijkstra and Bellman-Ford algorithms.
"""

class Graph:
    """Graph representation with nodes and weighted edges."""
    
    def __init__(self):
        self.graph = {
            'A': [('M', 20), ('S', 28), ('C', 36)],
            'B': [('M', 16), ('S', 24), ('F', 28), ('A', 25)],
            'C': [('M', 30), ('R', 11), ('T', 27)],
            'R': [('M', 22), ('F', 14)],
            'T': [('F', 22), ('H', 35)],
            'F': [('H', 30), ('O', 42)],
            'H': [('O', 11)],
            'M': [],
            'S': [],
            'O': []
        }
        self.nodes = list(self.graph.keys())
        self.node_index = {node: i for i, node in enumerate(self.nodes)}
        
        # Full city names
        self.city_names = {
            'A': 'Agadir',
            'B': 'Benguerir',
            'C': 'Casablanca',
            'F': 'Fes',
            'H': 'Hoceima',
            'M': 'Marrakech',
            'O': 'Oujda',
            'R': 'Rabat',
            'S': 'Safi',
            'T': 'Tanger'
        }
    
    def get_nodes(self):
        """Return list of all nodes."""
        return self.nodes.copy()
    
    def get_city_name(self, code):
        """Return full city name for a code."""
        return self.city_names.get(code, code)
    
    def get_city_names_dict(self):
        """Return dictionary of city names."""
        return self.city_names.copy()
    
    def get_edges(self):
        """Return list of all edges as tuples (source, destination, weight)."""
        edges = []
        for source, neighbors in self.graph.items():
            for dest, weight in neighbors:
                edges.append((source, dest, weight))
        return edges
    
    def dijkstra(self, source_node):
        """
        Dijkstra's algorithm for shortest path.
        
        Args:
            source_node: Starting node name
            
        Returns:
            tuple: (distances dict, predecessors dict)
        """
        if source_node not in self.nodes:
            raise ValueError(f"Node {source_node} not in graph")
        
        n = len(self.graph)
        source_idx = self.node_index[source_node]
        
        # Initialize
        L = [float('inf')] * n
        P = [None] * n
        M = [False] * n
        
        L[source_idx] = 0
        P[source_idx] = source_idx
        current = source_idx
        
        while True:
            M[current] = True
            
            # Update neighbors
            for neighbor_node, weight in self.graph[self.nodes[current]]:
                neighbor_idx = self.node_index[neighbor_node]
                
                if not M[neighbor_idx]:
                    new_distance = L[current] + weight
                    if new_distance < L[neighbor_idx]:
                        L[neighbor_idx] = new_distance
                        P[neighbor_idx] = current
            
            # Find next unvisited node with minimum distance
            min_distance = float('inf')
            next_node = -1
            
            for i in range(n):
                if not M[i] and L[i] < min_distance:
                    min_distance = L[i]
                    next_node = i
            
            if next_node == -1:
                break
            
            current = next_node
        
        # Convert to dictionary format
        distances = {self.nodes[i]: L[i] for i in range(n)}
        predecessors = {self.nodes[i]: (self.nodes[P[i]] if P[i] is not None else None) for i in range(n)}
        
        return distances, predecessors
    
    def bellman_ford(self, source_node):
        """
        Bellman-Ford algorithm for shortest path.
        
        Args:
            source_node: Starting node name
            
        Returns:
            tuple: (distances dict, predecessors dict)
        """
        if source_node not in self.nodes:
            raise ValueError(f"Node {source_node} not in graph")
        
        # Initialize
        distances = {node: float('inf') for node in self.graph}
        predecessors = {node: None for node in self.graph}
        
        distances[source_node] = 0
        predecessors[source_node] = source_node
        
        # Relax edges
        continue_flag = True
        iterations = 0
        
        while continue_flag:
            continue_flag = False
            iterations += 1
            
            for node in self.graph:
                for neighbor, weight in self.graph[node]:
                    if distances[node] + weight < distances[neighbor]:
                        distances[neighbor] = distances[node] + weight
                        predecessors[neighbor] = node
                        continue_flag = True
            
            # Prevent infinite loops
            if iterations > len(self.nodes):
                break
        
        return distances, predecessors
    
    def reconstruct_path(self, predecessors, source, destination):
        """
        Reconstruct the path from source to destination.
        
        Args:
            predecessors: Dictionary of predecessors from algorithm
            source: Starting node
            destination: Target node
            
        Returns:
            list: Path from source to destination, or empty list if no path exists
        """
        if destination not in predecessors or predecessors[destination] is None:
            return []
        
        path = []
        current = destination
        
        while current is not None and current != source:
            path.insert(0, current)
            if predecessors[current] == current:
                break
            current = predecessors[current]
        
        if current == source:
            path.insert(0, source)
            return path
        
        return []
    
    def get_path_with_weights(self, path):
        """
        Get path with edge weights.
        
        Args:
            path: List of nodes in path
            
        Returns:
            list: List of tuples (from_node, to_node, weight)
        """
        if not path or len(path) < 2:
            return []
        
        path_with_weights = []
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            
            # Find weight
            for neighbor, weight in self.graph[from_node]:
                if neighbor == to_node:
                    path_with_weights.append((from_node, to_node, weight))
                    break
        
        return path_with_weights
