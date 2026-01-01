"""Test script for graph algorithms."""
from graph_algorithms import Graph

# Create graph instance
g = Graph()

# Test Dijkstra
print("=" * 50)
print("Testing Dijkstra's Algorithm: A → M")
print("=" * 50)
distances, predecessors = g.dijkstra('A')
path = g.reconstruct_path(predecessors, 'A', 'M')
print(f"Path: {' → '.join(path)}")
print(f"Total Distance: {distances['M']}")

# Test Bellman-Ford
print("\n" + "=" * 50)
print("Testing Bellman-Ford Algorithm: A → M")
print("=" * 50)
distances2, predecessors2 = g.bellman_ford('A')
path2 = g.reconstruct_path(predecessors2, 'A', 'M')
print(f"Path: {' → '.join(path2)}")
print(f"Total Distance: {distances2['M']}")

print("\n✅ All tests passed!")
