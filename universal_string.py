# python3
import sys
from collections import defaultdict, deque


def build_de_bruijn_graph(k):
    """Build de Bruijn graph for k-universal circular string"""
    # Generate all possible k-mers
    k_mers = []
    for i in range(2**k):
        binary = format(i, '0' + str(k) + 'b')
        k_mers.append(binary)
    
    # Build adjacency list
    graph = defaultdict(list)
    for kmer in k_mers:
        prefix = kmer[:-1]  # (k-1)-mer prefix
        suffix = kmer[1:]   # (k-1)-mer suffix
        graph[prefix].append(suffix)
    
    return graph


def find_eulerian_cycle(graph):
    """Find Eulerian cycle using Hierholzer's algorithm"""
    # Check if Eulerian cycle exists
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for u in graph:
        out_degree[u] = len(graph[u])
        for v in graph[u]:
            in_degree[v] += 1
    
    # Check if in-degree equals out-degree for all vertices
    all_vertices = set(graph.keys()) | set(in_degree.keys())
    for v in all_vertices:
        if in_degree[v] != out_degree[v]:
            return None
    
    # Start from any vertex
    start = next(iter(graph.keys()))
    stack = [start]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            # Follow an edge
            next_vertex = graph[current].pop(0)
            stack.append(next_vertex)
        else:
            # Backtrack
            path.append(stack.pop())
    
    return path[::-1]  # Reverse to get the correct order


def reconstruct_string(path, k):
    """Reconstruct the k-universal circular string from the path"""
    if not path:
        return ""
    
    result = path[0]
    for i in range(1, len(path)):
        result += path[i][-1]
    
    return result


def main():
    k = int(input().strip())
    
    # Build de Bruijn graph
    graph = build_de_bruijn_graph(k)
    
    # Find Eulerian cycle
    cycle = find_eulerian_cycle(graph)
    
    if cycle is None:
        print("No Eulerian cycle found")
        return
    
    # Reconstruct the string
    result = reconstruct_string(cycle, k)
    print(result)


if __name__ == "__main__":
    main()