# python3
import sys
from collections import defaultdict


def read_graph():
    """Read graph from input"""
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    m = int(data[1])
    
    graph = defaultdict(list)
    in_degree = [0] * (n + 1)
    out_degree = [0] * (n + 1)
    
    for i in range(m):
        u = int(data[2 * i + 2])
        v = int(data[2 * i + 3])
        graph[u].append(v)
        out_degree[u] += 1
        in_degree[v] += 1
    
    return n, m, graph, in_degree, out_degree


def has_eulerian_cycle(n, in_degree, out_degree):
    """Check if graph has Eulerian cycle"""
    for i in range(1, n + 1):
        if in_degree[i] != out_degree[i]:
            return False
    return True


def find_eulerian_cycle(n, m, graph):
    """Find Eulerian cycle using Hierholzer's algorithm"""
    # Start from any vertex with outgoing edges
    start = 1
    for i in range(1, n + 1):
        if graph[i]:
            start = i
            break
    
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


def main():
    n, m, graph, in_degree, out_degree = read_graph()
    
    if not has_eulerian_cycle(n, in_degree, out_degree):
        print(0)
        return
    
    print(1)
    cycle = find_eulerian_cycle(n, m, graph)
    print(' '.join(map(str, cycle[:-1])))  # Remove the last vertex to avoid duplication


if __name__ == "__main__":
    main()